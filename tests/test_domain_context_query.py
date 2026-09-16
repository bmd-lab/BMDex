import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.domain_context import query as domain_query


REPO_ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = (
    REPO_ROOT
    / "vasp"
    / "contextual_reference"
    / "records"
    / "vasp.hybrid.exact_exchange_iteration_cost.json"
)


class DomainContextQueryTests(unittest.TestCase):
    def snapshot_context_paths(self):
        roots = [
            REPO_ROOT / "tools" / "domain_context",
            REPO_ROOT / "vasp" / "contextual_reference",
        ]
        snapshot = {}

        for root in roots:
            for path in root.rglob("*"):
                if "__pycache__" in path.parts or not path.is_file():
                    continue

                stat = path.stat()
                snapshot[path.relative_to(REPO_ROOT).as_posix()] = (
                    stat.st_size,
                    stat.st_mtime_ns,
                )

        return snapshot

    def load_record(self):
        return json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def test_first_record_validates(self):
        record = self.load_record()

        domain_query.validate_record(record, RECORD_PATH)
        self.assertEqual(record["id"], "vasp.hybrid.exact_exchange_iteration_cost")
        self.assertEqual(record["schema_version"], 1)
        self.assertEqual(record["evidence_type"], "contextual_reference_evidence")

    def test_required_source_provenance_is_present(self):
        record = self.load_record()

        self.assertGreaterEqual(len(record["sources"]), 5)
        for source in record["sources"]:
            self.assertTrue(source["source_type"])
            self.assertTrue(source["title"])
            self.assertTrue(source["authority"])
            self.assertTrue(source["url"].startswith("https://vasp.at/"))
            self.assertEqual(source["retrieved_on"], "2026-09-16")
            self.assertTrue(source["applicability_note"])

    def test_record_is_json_safe_and_source_provenance_survives_serialization(self):
        record = self.load_record()
        serialized = json.dumps(record, sort_keys=True)
        restored = json.loads(serialized)

        self.assertEqual(restored["sources"], record["sources"])
        self.assertEqual(
            restored["record_provenance"]["machine_readable_schema"],
            "bmdex.contextual_reference.v1",
        )

    def test_structured_applicability_is_preserved(self):
        record = self.load_record()
        applicability = record["applicability"]

        self.assertEqual(applicability["code"], "VASP")
        self.assertIn("hybrid_functional", applicability["calculation_families"])
        self.assertIn("HSE06", applicability["functional_examples"])
        self.assertIn("Damped", applicability["electronic_algorithms"])
        self.assertIn(
            "initial_DAV_steps_followed_by_large_walltime_increase",
            applicability["relevant_observed_patterns"],
        )

    def test_matching_returns_record_for_vasp_hse06_damped_context(self):
        payload = domain_query.query_records(
            {
                "code": "VASP",
                "calculation_family": "hybrid_functional",
                "functional": "HSE06",
                "electronic_algorithm": "Damped",
                "topic": "electronic_iteration_behavior",
                "observed_patterns": [
                    "initial_DAV_steps_followed_by_large_walltime_increase"
                ],
            }
        )

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["result_count"], 1)

        match = payload["records"][0]
        record = match["record"]
        self.assertEqual(record["id"], "vasp.hybrid.exact_exchange_iteration_cost")
        self.assertIn("functional", match["match"]["matched_fields"])
        self.assertIn("electronic_algorithm", match["match"]["matched_fields"])
        self.assertEqual(
            match["match"]["match_type"],
            "deterministic_structured_field_overlap",
        )

    def test_unrelated_query_returns_no_records(self):
        payload = domain_query.query_records(
            {
                "code": "VASP",
                "calculation_family": "semilocal_dft",
                "functional": "PBE",
                "topic": "ionic_relaxation",
            }
        )

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["result_count"], 0)
        self.assertEqual(payload["records"], [])

    def test_algorithm_alone_does_not_return_domain_context(self):
        payload = domain_query.query_records(
            {
                "code": "VASP",
                "electronic_algorithm": "Damped",
            }
        )

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["result_count"], 0)
        self.assertEqual(payload["records"], [])

    def test_limitations_and_diagnostic_relevance_are_returned(self):
        payload = domain_query.query_records(
            {
                "code": "VASP",
                "calculation_family": "hybrid_functional",
                "functional": "HSE06",
                "topic": "electronic_iteration_behavior",
            }
        )
        record = payload["records"][0]["record"]

        self.assertTrue(record["diagnostic_relevance"])
        self.assertTrue(record["limitations"])
        limitations_text = " ".join(record["limitations"])
        self.assertIn("does not diagnose any specific VASP run", limitations_text)
        self.assertIn("does not recommend changing INCAR tags", limitations_text)
        self.assertIn("not evidence that VASP is hung", record["diagnostic_relevance"])

    def test_cli_stdout_json_is_valid_and_uncontaminated(self):
        request = {
            "query": {
                "code": "VASP",
                "calculation_family": "hybrid_functional",
                "functional": "HSE06",
                "electronic_algorithm": "Damped",
                "topic": "electronic_iteration_behavior",
            }
        }
        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.domain_context.query",
            ],
            input=json.dumps(request),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stderr, "")
        payload = json.loads(process.stdout)
        self.assertEqual(
            process.stdout,
            json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        )
        self.assertEqual(payload["result_count"], 1)

    def test_query_is_read_only_and_does_not_leak_environment_secret(self):
        before = self.snapshot_context_paths()
        secret_value = "SHOULD_NOT_APPEAR_IN_DOMAIN_CONTEXT_OUTPUT"
        env = os.environ.copy()
        env["BMD_SECRET_TEST_TOKEN"] = secret_value

        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.domain_context.query",
            ],
            input=json.dumps(
                {
                    "query": {
                        "code": "VASP",
                        "calculation_family": "hybrid_functional",
                        "functional": "HSE06",
                    }
                }
            ),
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        after = self.snapshot_context_paths()
        self.assertEqual(process.returncode, 0)
        self.assertEqual(before, after)
        self.assertNotIn(secret_value, process.stdout)
        self.assertNotIn(secret_value, process.stderr)

    def test_no_network_call_is_required_at_runtime(self):
        def fail_if_called(*_args, **_kwargs):
            raise AssertionError("network API was unexpectedly called")

        with patch("urllib.request.urlopen", fail_if_called, create=True):
            with patch("socket.create_connection", fail_if_called):
                payload = domain_query.query_records(
                    {
                        "code": "VASP",
                        "calculation_family": "hybrid_functional",
                        "functional": "HSE06",
                    }
                )

        self.assertEqual(payload["result_count"], 1)

    def test_no_agent_or_compute_dependency_is_introduced(self):
        module_source = (
            REPO_ROOT / "tools" / "domain_context" / "query.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("bmd_agent", module_source.lower())
        self.assertNotIn("bmd_compute", module_source.lower())
        self.assertNotIn("BMD Agent", module_source)
        self.assertNotIn("BMD Compute", module_source)

    def test_calculation_file_inputs_are_rejected(self):
        with self.assertRaises(domain_query.ContractError) as error:
            domain_query.parse_request(
                json.dumps(
                    {
                        "query": {
                            "code": "VASP",
                            "functional": "HSE06",
                            "OUTCAR": "OUTCAR",
                        }
                    }
                )
            )

        self.assertEqual(error.exception.code, "invalid_query")


if __name__ == "__main__":
    unittest.main()
