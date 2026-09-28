#!/usr/bin/env python3

"""
Query local BMDex contextual reference knowledge records.

The command reads one JSON object from stdin:

    {"query": {"code": "VASP", "functional": "HSE06"}}

It writes exactly one JSON object to stdout. It does not inspect calculation
files, call external services, or import ecosystem component code.

Every record in the store is validated before a query is answered. One
malformed record fails the whole query with a structured error, so malformed
content never reaches producer output. Queries return only records whose
status is "active".
"""

from __future__ import annotations

from pathlib import Path
import json
import math
import re
import subprocess
import sys
from typing import Any
from urllib.parse import urlsplit


SCHEMA_VERSION = 1
EVIDENCE_TYPE = "contextual_reference_evidence"
PRODUCER_NAME = "BMDex"
CONTRACT_MODULE = "tools.domain_context.query"
CONTRACT_COMMAND = "python -B -m tools.domain_context.query"

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORD_ROOT = REPO_ROOT / "vasp" / "contextual_reference" / "records"
# BMDex owns the observed-pattern vocabulary. Records may list only these
# identifiers in applicability.relevant_observed_patterns, and queries may send
# only these identifiers as observed_patterns; anything else is rejected rather
# than silently failing to match.
OBSERVED_PATTERN_VOCABULARY_PATH = (
    REPO_ROOT / "vasp" / "contextual_reference" / "observed_patterns.json"
)
OBSERVED_PATTERN_VOCABULARY_ID = "bmdex.contextual_reference.observed_patterns"
SUPPORTED_OBSERVED_PATTERN_VOCABULARY_VERSIONS = frozenset({1})

SUPPORTED_RECORD_SCHEMA_VERSIONS = frozenset({1})
RECORD_STATUSES = frozenset({"active", "deprecated", "retired"})
QUERYABLE_RECORD_STATUSES = frozenset({"active"})
ALLOWED_SOURCE_URL_SCHEMES = frozenset({"https"})

ALLOWED_REQUEST_KEYS = {"query"}
# Query fields that take a single string (``domain`` is an alias of ``code``).
SINGLE_STRING_QUERY_KEYS = {"code", "domain"}
# Query fields that take a string or a list of strings.
STRING_OR_LIST_QUERY_KEYS = {
    "calculation_family",
    "functional",
    "electronic_algorithm",
    "topic",
    "observed_patterns",
}
# Query fields that take an object mapping VASP tag names to scalar values.
MAPPING_QUERY_KEYS = {"input_tags"}
ALLOWED_QUERY_KEYS = SINGLE_STRING_QUERY_KEYS | STRING_OR_LIST_QUERY_KEYS | MAPPING_QUERY_KEYS

REQUIRED_RECORD_FIELDS = {
    "schema_version",
    "id",
    "title",
    "evidence_type",
    "status",
    "domain",
    "topics",
    "applicability",
    "contextual_statement",
    "diagnostic_relevance",
    "limitations",
    "sources",
    "record_provenance",
}
OPTIONAL_RECORD_FIELDS = {"shorthand_correction"}
ALLOWED_RECORD_FIELDS = REQUIRED_RECORD_FIELDS | OPTIONAL_RECORD_FIELDS
RECORD_TEXT_FIELDS = (
    "id",
    "title",
    "status",
    "contextual_statement",
    "diagnostic_relevance",
)
SOURCE_TEXT_FIELDS = (
    "source_type",
    "title",
    "authority",
    "url",
    "retrieved_on",
    "applicability_note",
)


class ContractError(Exception):
    """Expected query error reported as structured JSON."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class NonFiniteNumberError(ValueError):
    """Raised for NaN/Infinity, which strict JSON does not allow."""


def _reject_json_constant(name: str) -> Any:
    raise NonFiniteNumberError(name)


def _parse_finite_float(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise NonFiniteNumberError(text)
    return value


def loads_strict_json(text: str) -> Any:
    """Parse JSON, rejecting NaN, Infinity, and overflowing numbers."""
    return json.loads(
        text,
        parse_constant=_reject_json_constant,
        parse_float=_parse_finite_float,
    )


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_strict_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    command = [
        "git",
        "--no-optional-locks",
        "-c",
        f"safe.directory={REPO_ROOT.as_posix()}",
        "-C",
        str(REPO_ROOT),
        *args,
    ]
    try:
        return subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(
            command,
            returncode=1,
            stdout="",
            stderr=str(exc),
        )


def producer_provenance() -> dict[str, Any]:
    commit_result = run_git(["rev-parse", "HEAD"])
    status_result = run_git(["status", "--porcelain", "--untracked-files=all"])

    git_info: dict[str, Any] = {
        "commit": None,
        "dirty": None,
        "state": "unavailable",
    }

    if commit_result.returncode == 0:
        git_info["commit"] = commit_result.stdout.strip()

    if status_result.returncode == 0:
        dirty = bool(status_result.stdout.strip())
        git_info["dirty"] = dirty
        git_info["state"] = "dirty" if dirty else "clean"

    if commit_result.returncode != 0 or status_result.returncode != 0:
        git_info["provenance_gap"] = "git_state_unavailable"

    return {
        "name": PRODUCER_NAME,
        "contract_module": CONTRACT_MODULE,
        "contract_command": CONTRACT_COMMAND,
        "git": git_info,
    }


def normalize(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def normalize_many(values: Any) -> set[str]:
    if values is None:
        return set()
    if isinstance(values, (list, tuple, set)):
        return {normalize(value) for value in values if str(value).strip()}
    return {normalize(values)}


def parse_request(raw_stdin: str) -> dict[str, Any]:
    try:
        request = loads_strict_json(raw_stdin)
    except json.JSONDecodeError as exc:
        raise ContractError("invalid_json", f"Request body is not valid JSON: {exc.msg}") from exc
    except NonFiniteNumberError as exc:
        raise ContractError(
            "invalid_json",
            "Request body contains a non-finite number, which is not valid JSON.",
        ) from exc

    if not isinstance(request, dict):
        raise ContractError("invalid_request", "Request must be a JSON object.")

    extra_keys = sorted(set(request) - ALLOWED_REQUEST_KEYS)
    if extra_keys:
        raise ContractError(
            "invalid_request",
            f"Unsupported request field(s): {', '.join(extra_keys)}",
        )

    query = request.get("query")
    if not isinstance(query, dict):
        raise ContractError("invalid_request", "Field 'query' must be an object.")

    extra_query_keys = sorted(set(query) - ALLOWED_QUERY_KEYS)
    if extra_query_keys:
        raise ContractError(
            "invalid_query",
            f"Unsupported query field(s): {', '.join(extra_query_keys)}",
        )

    validate_query(query)
    return query


def _require_query_text(label: str, value: Any) -> None:
    if not isinstance(value, str) or not normalize(value):
        raise ContractError(
            "invalid_query",
            f"Query field '{label}' must be a non-empty string containing letters or digits.",
        )


def validate_query(query: dict[str, Any]) -> None:
    """Reject malformed query values instead of letting them silently not match.

    ``null`` and empty lists are accepted and mean "not specified".
    """
    for key in sorted(SINGLE_STRING_QUERY_KEYS & query.keys()):
        if query[key] is not None:
            _require_query_text(key, query[key])

    for key in sorted(STRING_OR_LIST_QUERY_KEYS & query.keys()):
        value = query[key]
        if value is None:
            continue
        if isinstance(value, str):
            _require_query_text(key, value)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                _require_query_text(f"{key}[{index}]", item)
        else:
            raise ContractError(
                "invalid_query",
                f"Query field '{key}' must be a string or a list of strings.",
            )

    observed_patterns = query.get("observed_patterns")
    if observed_patterns:
        values = [observed_patterns] if isinstance(observed_patterns, str) else list(observed_patterns)
        unknown = _unknown_observed_patterns(values, load_observed_pattern_vocabulary())
        if unknown:
            raise ContractError(
                "invalid_query",
                "Query field 'observed_patterns' contains identifier(s) not in the BMDex "
                f"observed-pattern vocabulary: {', '.join(brief(value) for value in unknown)}",
            )

    input_tags = query.get("input_tags")
    if input_tags is not None:
        if not isinstance(input_tags, dict):
            raise ContractError(
                "invalid_query",
                "Query field 'input_tags' must be an object mapping tag names to values.",
            )
        for name, value in input_tags.items():
            _require_query_text(f"input_tags key {brief(name)}", name)
            if value is not None and not isinstance(value, (str, int, float)):
                raise ContractError(
                    "invalid_query",
                    f"Query field 'input_tags' value for {brief(name)} must be a string, number, boolean, or null.",
                )

    code = query.get("code")
    domain = query.get("domain")
    if code is not None and domain is not None and normalize(code) != normalize(domain):
        raise ContractError(
            "invalid_query",
            "Query fields 'code' and 'domain' are aliases and must not disagree.",
        )


def load_observed_pattern_vocabulary() -> frozenset[str]:
    """Return the BMDex-defined observed-pattern identifiers.

    The vocabulary is part of the producer contract, so a malformed vocabulary
    fails the query as a store error instead of weakening validation.
    """

    path = OBSERVED_PATTERN_VOCABULARY_PATH
    try:
        label = repo_relative(path)
    except ValueError:
        label = path.name
    try:
        vocabulary = loads_strict_json(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError("record_store_error", f"Observed-pattern vocabulary not found: {label}") from exc
    except (json.JSONDecodeError, NonFiniteNumberError, UnicodeDecodeError) as exc:
        raise ContractError("record_store_error", f"Observed-pattern vocabulary is not valid JSON: {label}") from exc

    if not isinstance(vocabulary, dict):
        raise ContractError("record_store_error", f"Observed-pattern vocabulary must be an object: {label}")
    version = vocabulary.get("schema_version")
    if not is_strict_int(version) or version not in SUPPORTED_OBSERVED_PATTERN_VOCABULARY_VERSIONS:
        raise ContractError(
            "record_store_error",
            f"Unsupported observed-pattern vocabulary schema_version {brief(version)}: {label}",
        )
    if vocabulary.get("vocabulary") != OBSERVED_PATTERN_VOCABULARY_ID:
        raise ContractError("record_store_error", f"Unexpected observed-pattern vocabulary id: {label}")

    patterns = vocabulary.get("patterns")
    if not isinstance(patterns, list) or not patterns:
        raise ContractError("record_store_error", f"Observed-pattern vocabulary has no patterns: {label}")

    identifiers: set[str] = set()
    for index, entry in enumerate(patterns):
        if not isinstance(entry, dict) or not is_text(entry.get("id")) or not is_text(entry.get("definition")):
            raise ContractError(
                "record_store_error",
                f"Observed pattern {index} must have non-empty 'id' and 'definition' strings: {label}",
            )
        identifier = entry["id"]
        if normalize(identifier) != identifier:
            raise ContractError(
                "record_store_error",
                f"Observed pattern id {brief(identifier)} is not a canonical lower_snake_case identifier: {label}",
            )
        if identifier in identifiers:
            raise ContractError(
                "record_store_error",
                f"Duplicate observed pattern id {brief(identifier)}: {label}",
            )
        identifiers.add(identifier)
    return frozenset(identifiers)


def _unknown_observed_patterns(values: list[str], vocabulary: frozenset[str]) -> list[str]:
    return [value for value in values if value not in vocabulary]


def load_records() -> list[dict[str, Any]]:
    records = []

    if not RECORD_ROOT.exists():
        raise ContractError("record_store_error", f"Record directory not found: {repo_relative(RECORD_ROOT)}")

    seen_ids: dict[str, str] = {}

    for path in sorted(RECORD_ROOT.glob("*.json")):
        try:
            record = loads_strict_json(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ContractError(
                "record_store_error",
                f"Record is not valid JSON: {repo_relative(path)}: {exc.msg}",
            ) from exc
        except NonFiniteNumberError as exc:
            raise ContractError(
                "record_store_error",
                f"Record contains a non-finite number, which is not valid JSON: {repo_relative(path)}",
            ) from exc
        except UnicodeDecodeError as exc:
            raise ContractError(
                "record_store_error",
                f"Record is not valid UTF-8: {repo_relative(path)}",
            ) from exc

        validate_record(record, path)

        # Case-insensitive, so IDs stay unique on case-insensitive filesystems.
        id_key = record["id"].casefold()
        if id_key in seen_ids:
            raise ContractError(
                "record_validation_error",
                f"Duplicate record id {brief(record['id'])} in {repo_relative(path)} "
                f"(already defined in {seen_ids[id_key]})",
            )
        seen_ids[id_key] = repo_relative(path)

        record = dict(record)
        record["_record_path"] = repo_relative(path)
        records.append(record)

    return records


def brief(value: Any, limit: int = 60) -> str:
    """Short repr for error messages, so record content is never echoed at length."""
    text = repr(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _record_error(label: str, message: str) -> ContractError:
    return ContractError("record_validation_error", f"{message} in {label}")


def _require_text_list(record: dict[str, Any], field: str, label: str) -> None:
    values = record[field]
    if not isinstance(values, list) or not values:
        raise _record_error(label, f"Field '{field}' must be a non-empty list")
    for index, value in enumerate(values):
        if not is_text(value):
            raise _record_error(label, f"Field '{field}[{index}]' must be a non-empty string")


def validate_source_url(url: str, label: str) -> None:
    parts = urlsplit(url)
    if parts.scheme not in ALLOWED_SOURCE_URL_SCHEMES or not parts.netloc:
        allowed = ", ".join(sorted(ALLOWED_SOURCE_URL_SCHEMES))
        raise _record_error(label, f"Source url must be an absolute {allowed} URL")


def validate_record(record: Any, path: Path | None = None) -> None:
    if isinstance(record, dict) and isinstance(record.get("id"), str):
        fallback_label = record["id"]
    else:
        fallback_label = "<record>"
    label = repo_relative(path) if path else fallback_label

    if not isinstance(record, dict):
        raise _record_error(label, "Record must be a JSON object")

    missing = sorted(REQUIRED_RECORD_FIELDS - set(record))
    if missing:
        raise ContractError(
            "record_validation_error",
            f"Missing required field(s) in {label}: {', '.join(missing)}",
        )

    unexpected = sorted(set(record) - ALLOWED_RECORD_FIELDS)
    if unexpected:
        raise _record_error(label, f"Unexpected field(s) {', '.join(unexpected)}")

    schema_version = record["schema_version"]
    if not is_strict_int(schema_version) or schema_version not in SUPPORTED_RECORD_SCHEMA_VERSIONS:
        raise _record_error(label, f"Unsupported schema_version {brief(schema_version)}")

    if record["evidence_type"] != EVIDENCE_TYPE:
        raise ContractError(
            "record_validation_error",
            f"Unsupported evidence_type in {label}: {record['evidence_type']}",
        )

    for field in RECORD_TEXT_FIELDS:
        if not is_text(record[field]):
            raise _record_error(label, f"Field '{field}' must be a non-empty string")

    if path is not None and record["id"] != path.stem:
        raise _record_error(label, f"Record id {brief(record['id'])} does not match filename stem {brief(path.stem)}")

    if record["status"] not in RECORD_STATUSES:
        allowed = ", ".join(sorted(RECORD_STATUSES))
        raise _record_error(label, f"Unsupported status {brief(record['status'])} (allowed: {allowed})")

    for field in ("domain", "applicability"):
        if not isinstance(record[field], dict):
            raise _record_error(label, f"Field '{field}' must be an object")

    _require_text_list(record, "topics", label)
    _require_text_list(record, "limitations", label)

    if "relevant_observed_patterns" in record["applicability"]:
        patterns = record["applicability"]["relevant_observed_patterns"]
        if not isinstance(patterns, list) or not patterns or not all(is_text(item) for item in patterns):
            raise _record_error(
                label,
                "Field 'applicability.relevant_observed_patterns' must be a non-empty list of strings",
            )
        unknown = _unknown_observed_patterns(patterns, load_observed_pattern_vocabulary())
        if unknown:
            raise _record_error(
                label,
                "Field 'applicability.relevant_observed_patterns' uses identifier(s) not in the "
                f"BMDex observed-pattern vocabulary: {', '.join(brief(value) for value in unknown)}",
            )

    if "shorthand_correction" in record:
        shorthand = record["shorthand_correction"]
        if not isinstance(shorthand, dict) or not all(
            is_text(shorthand.get(key)) for key in ("shorthand", "correction")
        ):
            raise _record_error(
                label,
                "Field 'shorthand_correction' must be an object with non-empty 'shorthand' and 'correction' strings",
            )

    if not isinstance(record["sources"], list) or not record["sources"]:
        raise ContractError("record_validation_error", f"Record has no sources: {label}")

    for source in record["sources"]:
        if not isinstance(source, dict):
            raise ContractError("record_validation_error", f"Source is not an object in {label}")
        for field in SOURCE_TEXT_FIELDS:
            if not is_text(source.get(field)):
                raise ContractError(
                    "record_validation_error",
                    f"Source missing {field} in {label}",
                )
        validate_source_url(source["url"], label)

    provenance = record["record_provenance"]
    if not isinstance(provenance, dict):
        raise _record_error(label, "Field 'record_provenance' must be an object")
    record_version = provenance.get("record_version")
    if not is_strict_int(record_version) or record_version < 1:
        raise _record_error(
            label,
            f"record_provenance.record_version must be a positive integer, got {brief(record_version)}",
        )


def input_tag_names(record: dict[str, Any]) -> set[str]:
    tags = record.get("applicability", {}).get("input_tags", [])
    return {
        normalize(tag.get("name"))
        for tag in tags
        if isinstance(tag, dict) and tag.get("name")
    }


def match_record(record: dict[str, Any], query: dict[str, Any]) -> dict[str, Any] | None:
    applicability = record.get("applicability", {})
    matched_fields: list[str] = []

    query_code = normalize(query.get("code") or query.get("domain") or "")
    record_code = normalize(applicability.get("code") or record.get("domain", {}).get("code") or "")
    if query_code and query_code != record_code:
        return None

    if query_code and query_code == record_code:
        matched_fields.append("code")

    substantive_match = False

    field_pairs = [
        ("calculation_family", "calculation_families"),
        ("functional", "functional_examples"),
    ]
    for query_field, record_field in field_pairs:
        query_values = normalize_many(query.get(query_field))
        record_values = normalize_many(applicability.get(record_field, []))
        if query_values and query_values & record_values:
            matched_fields.append(query_field)
            substantive_match = True

    query_algorithms = normalize_many(query.get("electronic_algorithm"))
    record_algorithms = normalize_many(applicability.get("electronic_algorithms", []))
    if query_algorithms and query_algorithms & record_algorithms:
        matched_fields.append("electronic_algorithm")

    query_topics = normalize_many(query.get("topic"))
    record_topics = normalize_many(record.get("topics", []))
    if query_topics and query_topics & record_topics:
        matched_fields.append("topic")
        substantive_match = True

    # Observed patterns are vocabulary identifiers compared exactly. They are
    # additional evidence: a record can still match on its calculation and
    # input fields, and matched_observed_patterns reports whether trajectory
    # observations contributed to this match.
    query_patterns = query.get("observed_patterns") or []
    if isinstance(query_patterns, str):
        query_patterns = [query_patterns]
    matched_observed_patterns = [
        pattern
        for pattern in applicability.get("relevant_observed_patterns", [])
        if pattern in set(query_patterns)
    ]
    if matched_observed_patterns:
        matched_fields.append("observed_patterns")
        substantive_match = True

    query_input_tags = query.get("input_tags")
    if isinstance(query_input_tags, dict):
        query_tag_names = {normalize(name) for name in query_input_tags}
        if query_tag_names & input_tag_names(record):
            matched_fields.append("input_tags")
            substantive_match = True

    if not substantive_match:
        return None

    return {
        "record": public_record(record),
        "match": {
            "matched_fields": matched_fields,
            "matched_observed_patterns": matched_observed_patterns,
            "match_type": "deterministic_structured_field_overlap",
        },
    }


def public_record(record: dict[str, Any]) -> dict[str, Any]:
    public = {
        key: value
        for key, value in record.items()
        if not key.startswith("_")
    }
    public["record_path"] = record["_record_path"]
    return public


def query_records(query: dict[str, Any]) -> dict[str, Any]:
    matches = [
        match
        for record in load_records()
        if record["status"] in QUERYABLE_RECORD_STATUSES
        and (match := match_record(record, query)) is not None
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "evidence_type": EVIDENCE_TYPE,
        "producer": producer_provenance(),
        "query": query,
        "records": matches,
        "result_count": len(matches),
    }


def error_response(error: ContractError) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "evidence_type": EVIDENCE_TYPE,
        "producer": producer_provenance(),
        "error": {
            "code": error.code,
            "message": error.message,
        },
    }


def emit_json(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")


def main() -> int:
    try:
        query = parse_request(sys.stdin.read())
        emit_json(query_records(query))
        return 0
    except ContractError as error:
        emit_json(error_response(error))
        return 2
    except Exception as error:
        emit_json(
            error_response(
                ContractError(
                    "producer_error",
                    f"Domain-context query failed safely: {type(error).__name__}",
                )
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
