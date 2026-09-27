"""Adversarial regression tests for the contextual-reference record contract.

These tests exercise malformed records and requests against
``tools.domain_context.query``. Record-store tests use temporary directories
outside the repository; the committed records are never modified.
"""

import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.domain_context import query as domain_query


REPO_ROOT = Path(__file__).resolve().parents[1]
RECORD_ID = "vasp.hybrid.exact_exchange_iteration_cost"
RECORD_PATH = (
    REPO_ROOT / "vasp" / "contextual_reference" / "records" / f"{RECORD_ID}.json"
)
VALID_QUERY = {
    "code": "VASP",
    "calculation_family": "hybrid_functional",
    "functional": "HSE06",
    "electronic_algorithm": "Damped",
    "topic": "electronic_iteration_behavior",
}
STUB_PROVENANCE = {"name": "BMDex", "git": {"state": "stubbed"}}


def load_valid_record():
    return json.loads(RECORD_PATH.read_text(encoding="utf-8"))


def record_with_id(record_id, **overrides):
    record = load_valid_record()
    record["id"] = record_id
    record.update(overrides)
    return record


class TemporaryRecordStore:
    """Point the producer at a temporary record directory."""

    def __init__(self, files):
        self.files = files

    def __enter__(self):
        self.root = Path(tempfile.mkdtemp(prefix="bmdex-records-"))
        record_root = self.root / "records"
        record_root.mkdir()
        for name, content in self.files.items():
            if isinstance(content, (dict, list)):
                content = json.dumps(content)
            if isinstance(content, bytes):
                (record_root / name).write_bytes(content)
            else:
                (record_root / name).write_text(content, encoding="utf-8")

        self.patches = [
            patch.object(domain_query, "REPO_ROOT", self.root),
            patch.object(domain_query, "RECORD_ROOT", record_root),
            patch.object(domain_query, "producer_provenance", lambda: dict(STUB_PROVENANCE)),
        ]
        for active_patch in self.patches:
            active_patch.start()
        return self

    def __exit__(self, *exc_info):
        for active_patch in reversed(self.patches):
            active_patch.stop()
        shutil.rmtree(self.root, ignore_errors=True)
        return False


class RecordValidationTests(unittest.TestCase):
    def assert_record_rejected(self, record, path=RECORD_PATH):
        with self.assertRaises(domain_query.ContractError) as error:
            domain_query.validate_record(record, path)
        self.assertEqual(error.exception.code, "record_validation_error")
        return error.exception

    def test_committed_record_still_validates(self):
        domain_query.validate_record(load_valid_record(), RECORD_PATH)

    def test_record_must_be_an_object(self):
        for value in ([], ["id"], "record", 1, None):
            with self.subTest(value=value):
                self.assert_record_rejected(value)

    def test_schema_version_must_be_supported_integer(self):
        for value in (0, 2, 99, "1", 1.0, True, None):
            with self.subTest(value=value):
                record = load_valid_record()
                record["schema_version"] = value
                self.assert_record_rejected(record)

    def test_record_version_must_be_positive_integer(self):
        for value in (0, -1, "1", "x", 1.5, True, None, [1]):
            with self.subTest(value=value):
                record = load_valid_record()
                record["record_provenance"]["record_version"] = value
                self.assert_record_rejected(record)

    def test_record_version_is_required(self):
        record = load_valid_record()
        del record["record_provenance"]["record_version"]
        self.assert_record_rejected(record)

    def test_record_provenance_must_be_an_object(self):
        for value in ([], "BMDex", None, 1):
            with self.subTest(value=value):
                record = load_valid_record()
                record["record_provenance"] = value
                self.assert_record_rejected(record)

    def test_id_must_match_filename_stem(self):
        record = load_valid_record()
        record["id"] = "vasp.some_other_record"
        error = self.assert_record_rejected(record)
        self.assertIn("filename", error.message)

        record = load_valid_record()
        self.assert_record_rejected(record, RECORD_PATH.with_name("renamed.json"))

    def test_status_must_be_defined(self):
        for value in ("banana", "Active", "ACTIVE", "", "  ", 1, None, ["active"]):
            with self.subTest(value=value):
                record = load_valid_record()
                record["status"] = value
                self.assert_record_rejected(record)

    def test_defined_non_active_statuses_are_valid_records(self):
        for status in ("deprecated", "retired"):
            with self.subTest(status=status):
                record = load_valid_record()
                record["status"] = status
                domain_query.validate_record(record, RECORD_PATH)

    def test_core_text_fields_must_be_non_empty_strings(self):
        for field in ("id", "title", "contextual_statement", "diagnostic_relevance"):
            for value in (12345, "", "   ", None, ["text"], {"text": "x"}, True):
                with self.subTest(field=field, value=value):
                    record = load_valid_record()
                    record[field] = value
                    self.assert_record_rejected(record)

    def test_limitations_must_be_non_empty_list_of_non_empty_strings(self):
        for value in ([], [""], ["   "], ["valid", 3], ["valid", None], "a string", None, {"a": "b"}):
            with self.subTest(value=value):
                record = load_valid_record()
                record["limitations"] = value
                self.assert_record_rejected(record)

    def test_topics_must_be_non_empty_list_of_non_empty_strings(self):
        for value in ([], [""], [1], "electronic_iteration_behavior", None):
            with self.subTest(value=value):
                record = load_valid_record()
                record["topics"] = value
                self.assert_record_rejected(record)

    def test_domain_and_applicability_must_be_objects(self):
        for field in ("domain", "applicability"):
            for value in ([], "VASP", None, 1):
                with self.subTest(field=field, value=value):
                    record = load_valid_record()
                    record[field] = value
                    self.assert_record_rejected(record)

    def test_shorthand_correction_must_be_well_formed_when_present(self):
        for value in (None, "text", [], {"shorthand": "x"}, {"shorthand": "", "correction": "y"}):
            with self.subTest(value=value):
                record = load_valid_record()
                record["shorthand_correction"] = value
                self.assert_record_rejected(record)

        record = load_valid_record()
        del record["shorthand_correction"]
        domain_query.validate_record(record, RECORD_PATH)

    def test_unexpected_top_level_fields_are_rejected(self):
        for field in ("extra_untrusted_field", "_record_path", "record_path", "remediation"):
            with self.subTest(field=field):
                record = load_valid_record()
                record[field] = "<script>alert(1)</script>"
                error = self.assert_record_rejected(record)
                self.assertIn(field, error.message)

    def test_source_urls_must_be_absolute_https(self):
        for url in (
            "javascript:alert(1)",
            "http://vasp.at/wiki/NELMDL",
            "file:///etc/passwd",
            "data:text/html,<script>alert(1)</script>",
            "ftp://vasp.at/wiki",
            "vasp.at/wiki/NELMDL",
            "//vasp.at/wiki/NELMDL",
            "https://",
            "HTTPS:/vasp.at",
        ):
            with self.subTest(url=url):
                record = load_valid_record()
                record["sources"][0]["url"] = url
                self.assert_record_rejected(record)

    def test_rejected_source_url_is_not_echoed_in_error(self):
        url = "javascript:alert('INJECTED_URL_CONTENT')"
        record = load_valid_record()
        record["sources"][0]["url"] = url
        error = self.assert_record_rejected(record)
        self.assertNotIn("INJECTED_URL_CONTENT", error.message)

    def test_long_invalid_values_are_truncated_in_errors(self):
        record = load_valid_record()
        record["status"] = "x" * 500
        error = self.assert_record_rejected(record)
        self.assertLess(len(error.message), 300)

    def test_source_text_fields_must_be_non_empty_strings(self):
        for field in domain_query.SOURCE_TEXT_FIELDS:
            for value in (123, "", "   ", None, ["x"]):
                with self.subTest(field=field, value=value):
                    record = load_valid_record()
                    record["sources"][0][field] = value
                    self.assert_record_rejected(record)

    def test_sources_must_be_non_empty_list_of_objects(self):
        for value in ([], None, "https://vasp.at/wiki/NELMDL", ["https://vasp.at/wiki/NELMDL"]):
            with self.subTest(value=value):
                record = load_valid_record()
                record["sources"] = value
                self.assert_record_rejected(record)


class RecordStoreTests(unittest.TestCase):
    def test_only_active_records_are_returned(self):
        files = {
            "vasp.a_active.json": record_with_id("vasp.a_active", status="active"),
            "vasp.b_deprecated.json": record_with_id("vasp.b_deprecated", status="deprecated"),
            "vasp.c_retired.json": record_with_id("vasp.c_retired", status="retired"),
        }
        with TemporaryRecordStore(files):
            payload = domain_query.query_records(dict(VALID_QUERY))

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["result_count"], 1)
        self.assertEqual(
            [match["record"]["id"] for match in payload["records"]],
            ["vasp.a_active"],
        )

    def test_store_with_only_non_active_records_returns_no_records(self):
        files = {
            "vasp.retired.json": record_with_id("vasp.retired", status="retired"),
        }
        with TemporaryRecordStore(files):
            payload = domain_query.query_records(dict(VALID_QUERY))

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["result_count"], 0)
        self.assertEqual(payload["records"], [])

    def test_invalid_non_active_record_still_fails_the_store(self):
        files = {
            "vasp.ok.json": record_with_id("vasp.ok"),
            "vasp.bad.json": record_with_id("vasp.bad", status="retired", title=""),
        }
        with TemporaryRecordStore(files):
            with self.assertRaises(domain_query.ContractError) as error:
                domain_query.query_records(dict(VALID_QUERY))

        self.assertEqual(error.exception.code, "record_validation_error")

    def test_filename_mismatch_in_store_is_rejected(self):
        files = {"vasp.renamed.json": record_with_id("vasp.original")}
        with TemporaryRecordStore(files):
            with self.assertRaises(domain_query.ContractError) as error:
                domain_query.load_records()

        self.assertEqual(error.exception.code, "record_validation_error")
        self.assertIn("filename", error.exception.message)

    def test_duplicate_ids_are_rejected_even_if_filename_rule_is_bypassed(self):
        # Two files cannot share a stem in one directory, so disable per-record
        # validation to exercise the independent uniqueness guard directly.
        cases = {
            "exact duplicate": ("vasp.dup", "vasp.dup"),
            "case-variant duplicate": ("vasp.dup", "VASP.Dup"),
        }
        for label, (first_id, second_id) in cases.items():
            with self.subTest(label=label):
                files = {
                    "a.json": record_with_id(first_id),
                    "b.json": record_with_id(second_id),
                }
                with TemporaryRecordStore(files):
                    with patch.object(domain_query, "validate_record", lambda *_args: None):
                        with self.assertRaises(domain_query.ContractError) as error:
                            domain_query.load_records()

                self.assertEqual(error.exception.code, "record_validation_error")
                self.assertIn("Duplicate record id", error.exception.message)

    def test_non_finite_numbers_in_records_are_rejected(self):
        valid_text = json.dumps(record_with_id("vasp.nonfinite"))
        for token in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(token=token):
                text = valid_text.replace('"schema_version": 1', f'"schema_version": {token}')
                self.assertIn(token, text)
                with TemporaryRecordStore({"vasp.nonfinite.json": text}):
                    with self.assertRaises(domain_query.ContractError) as error:
                        domain_query.load_records()

                self.assertEqual(error.exception.code, "record_store_error")

    def test_non_utf8_record_is_a_store_error(self):
        with TemporaryRecordStore({"vasp.binary.json": b"\xff\xfe{\x00"}):
            with self.assertRaises(domain_query.ContractError) as error:
                domain_query.load_records()

        self.assertEqual(error.exception.code, "record_store_error")

    def test_malformed_record_content_never_reaches_cli_output(self):
        injected = "INJECTED_UNREVIEWED_CONTENT"
        files = {
            "vasp.ok.json": record_with_id("vasp.ok"),
            "vasp.bad.json": record_with_id("vasp.bad", injected_field=injected),
        }
        stdout = io.StringIO()
        with TemporaryRecordStore(files):
            with patch("sys.stdin", io.StringIO(json.dumps({"query": VALID_QUERY}))):
                with patch("sys.stdout", stdout):
                    exit_code = domain_query.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["error"]["code"], "record_validation_error")
        self.assertNotIn("records", payload)
        self.assertNotIn(injected, stdout.getvalue())

    def test_record_that_is_not_an_object_is_a_contract_error(self):
        with TemporaryRecordStore({"vasp.list.json": [{"id": "vasp.list"}]}):
            with self.assertRaises(domain_query.ContractError) as error:
                domain_query.load_records()

        self.assertEqual(error.exception.code, "record_validation_error")


class RequestValidationTests(unittest.TestCase):
    def assert_query_rejected(self, query, code="invalid_query"):
        with self.assertRaises(domain_query.ContractError) as error:
            domain_query.parse_request(json.dumps({"query": query}))
        self.assertEqual(error.exception.code, code)
        return error.exception

    def test_non_object_input_tags_are_rejected(self):
        for value in (["LHFCALC"], "LHFCALC", 1, True):
            with self.subTest(value=value):
                self.assert_query_rejected({"code": "VASP", "input_tags": value})

    def test_input_tag_names_and_values_must_be_well_formed(self):
        for value in ({"": ".TRUE."}, {"  ": 1}, {"LHFCALC": {"nested": True}}, {"LHFCALC": [".TRUE."]}):
            with self.subTest(value=value):
                self.assert_query_rejected({"code": "VASP", "input_tags": value})

    def test_well_formed_input_tags_still_match(self):
        query = domain_query.parse_request(
            json.dumps({"query": {"code": "VASP", "input_tags": {"LHFCALC": ".TRUE.", "NELMDL": -5, "LSORBIT": False}}})
        )
        payload = domain_query.query_records(query)
        self.assertEqual(payload["result_count"], 1)
        self.assertIn("input_tags", payload["records"][0]["match"]["matched_fields"])

    def test_code_and_domain_must_be_single_strings(self):
        for key in ("code", "domain"):
            for value in (["VASP"], 1, {"name": "VASP"}, "", "   ", "!!!", True):
                with self.subTest(key=key, value=value):
                    self.assert_query_rejected({key: value, "functional": "HSE06"})

    def test_code_and_domain_must_not_disagree(self):
        self.assert_query_rejected({"code": "VASP", "domain": "QE", "functional": "HSE06"})

        query = domain_query.parse_request(
            json.dumps({"query": {"code": "VASP", "domain": "vasp", "functional": "HSE06"}})
        )
        self.assertEqual(domain_query.query_records(query)["result_count"], 1)

    def test_string_or_list_fields_reject_other_types(self):
        for key in sorted(domain_query.STRING_OR_LIST_QUERY_KEYS):
            for value in (1, True, {"x": "y"}, "", "  ", [""], ["ok", 1], [["nested"]], [None]):
                with self.subTest(key=key, value=value):
                    self.assert_query_rejected({"code": "VASP", key: value})

    def test_null_and_empty_list_mean_not_specified(self):
        query = domain_query.parse_request(
            json.dumps(
                {
                    "query": {
                        "code": "VASP",
                        "domain": None,
                        "functional": "HSE06",
                        "calculation_family": None,
                        "observed_patterns": [],
                        "input_tags": None,
                    }
                }
            )
        )
        payload = domain_query.query_records(query)
        self.assertEqual(payload["result_count"], 1)

    def test_non_finite_numbers_in_request_are_invalid_json(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(token=token):
                with self.assertRaises(domain_query.ContractError) as error:
                    domain_query.parse_request('{"query": {"code": "VASP", "input_tags": {"NELMDL": %s}}}' % token)
                self.assertEqual(error.exception.code, "invalid_json")

    def test_cli_reports_malformed_input_tags_as_structured_error(self):
        process = subprocess.run(
            [sys.executable, "-B", "-m", "tools.domain_context.query"],
            input=json.dumps({"query": {"code": "VASP", "input_tags": ["LHFCALC"]}}),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stderr, "")
        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["error"]["code"], "invalid_query")
        self.assertIn("input_tags", payload["error"]["message"])


class ValidQueryOutputContractTests(unittest.TestCase):
    def test_valid_query_output_shape_and_record_content_are_preserved(self):
        with patch.object(domain_query, "producer_provenance", lambda: dict(STUB_PROVENANCE)):
            query = domain_query.parse_request(json.dumps({"query": VALID_QUERY}))
            payload = domain_query.query_records(query)

        self.assertEqual(
            set(payload),
            {"schema_version", "status", "evidence_type", "producer", "query", "records", "result_count"},
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["evidence_type"], "contextual_reference_evidence")
        self.assertEqual(payload["query"], VALID_QUERY)
        self.assertEqual(payload["result_count"], 1)

        expected_record = load_valid_record()
        expected_record["record_path"] = RECORD_PATH.relative_to(REPO_ROOT).as_posix()
        self.assertEqual(
            payload["records"],
            [
                {
                    "record": expected_record,
                    "match": {
                        "matched_fields": [
                            "code",
                            "calculation_family",
                            "functional",
                            "electronic_algorithm",
                            "topic",
                        ],
                        "match_type": "deterministic_structured_field_overlap",
                    },
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
