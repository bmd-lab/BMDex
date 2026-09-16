#!/usr/bin/env python3

"""
Query local BMDex contextual reference knowledge records.

The command reads one JSON object from stdin:

    {"query": {"code": "VASP", "functional": "HSE06"}}

It writes exactly one JSON object to stdout. It does not inspect calculation
files, call external services, or import ecosystem component code.
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess
import sys
from typing import Any


SCHEMA_VERSION = 1
EVIDENCE_TYPE = "contextual_reference_evidence"
PRODUCER_NAME = "BMDex"
CONTRACT_MODULE = "tools.domain_context.query"
CONTRACT_COMMAND = "python -B -m tools.domain_context.query"

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORD_ROOT = REPO_ROOT / "vasp" / "contextual_reference" / "records"

ALLOWED_REQUEST_KEYS = {"query"}
ALLOWED_QUERY_KEYS = {
    "code",
    "domain",
    "calculation_family",
    "functional",
    "electronic_algorithm",
    "topic",
    "observed_patterns",
    "input_tags",
}
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


class ContractError(Exception):
    """Expected query error reported as structured JSON."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


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
        request = json.loads(raw_stdin)
    except json.JSONDecodeError as exc:
        raise ContractError("invalid_json", f"Request body is not valid JSON: {exc.msg}") from exc

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

    return query


def load_records() -> list[dict[str, Any]]:
    records = []

    if not RECORD_ROOT.exists():
        raise ContractError("record_store_error", f"Record directory not found: {repo_relative(RECORD_ROOT)}")

    for path in sorted(RECORD_ROOT.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ContractError(
                "record_store_error",
                f"Record is not valid JSON: {repo_relative(path)}: {exc.msg}",
            ) from exc

        validate_record(record, path)
        record = dict(record)
        record["_record_path"] = repo_relative(path)
        records.append(record)

    return records


def validate_record(record: dict[str, Any], path: Path | None = None) -> None:
    missing = sorted(REQUIRED_RECORD_FIELDS - set(record))
    label = repo_relative(path) if path else record.get("id", "<record>")

    if missing:
        raise ContractError(
            "record_validation_error",
            f"Missing required field(s) in {label}: {', '.join(missing)}",
        )

    if record["evidence_type"] != EVIDENCE_TYPE:
        raise ContractError(
            "record_validation_error",
            f"Unsupported evidence_type in {label}: {record['evidence_type']}",
        )

    if not isinstance(record["sources"], list) or not record["sources"]:
        raise ContractError("record_validation_error", f"Record has no sources: {label}")

    for source in record["sources"]:
        if not isinstance(source, dict):
            raise ContractError("record_validation_error", f"Source is not an object in {label}")
        for field in ("source_type", "title", "authority", "url", "retrieved_on", "applicability_note"):
            if not source.get(field):
                raise ContractError(
                    "record_validation_error",
                    f"Source missing {field} in {label}",
                )

    if not isinstance(record["limitations"], list) or not record["limitations"]:
        raise ContractError("record_validation_error", f"Record has no limitations: {label}")


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

    query_patterns = normalize_many(query.get("observed_patterns"))
    record_patterns = normalize_many(applicability.get("relevant_observed_patterns", []))
    if query_patterns and query_patterns & record_patterns:
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
        if (match := match_record(record, query)) is not None
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
