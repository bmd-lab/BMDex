import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.composition import context_producer


REPO_ROOT = Path(__file__).resolve().parents[1]


class CompositionContextProducerTests(unittest.TestCase):
    def snapshot_producer_paths(self):
        roots = [
            REPO_ROOT / "tools" / "composition",
            REPO_ROOT / "datasets" / "element_abundances",
            REPO_ROOT / "datasets" / "element_charges",
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

    def test_mncu5_context_contains_bmdex_dataset_records(self):
        payload = context_producer.build_context("MnCu5")

        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["evidence_type"], "composition_context")
        self.assertEqual(payload["composition"]["supplied_formula"], "MnCu5")
        self.assertEqual(payload["composition"]["reduced_formula"], "MnCu5")
        self.assertEqual(payload["composition"]["elements"], ["Mn", "Cu"])
        self.assertEqual(
            payload["composition"]["stoichiometric_amounts"],
            [
                {"element": "Mn", "amount": 1},
                {"element": "Cu", "amount": 5},
            ],
        )

        abundance = {
            record["element"]: record
            for record in payload["datasets"]["element_abundances"]["records"]
        }
        self.assertEqual(abundance["Mn"]["abundance"], 950.0)
        self.assertEqual(abundance["Cu"]["abundance"], 60.0)
        self.assertEqual(payload["datasets"]["element_abundances"]["units"], "mg/kg")

        charges = {
            record["element"]: record
            for record in payload["datasets"]["element_charges"]["records"]
        }
        self.assertEqual(charges["Mn"]["representative_oxidation_states"], [2])
        self.assertEqual(charges["Cu"]["representative_oxidation_states"], [1, 2])
        self.assertEqual(payload["missing_evidence"], [])

    def test_si_context_is_deterministic_for_scientific_fields(self):
        first = context_producer.build_context("Si")
        second = context_producer.build_context("Si")

        for payload in (first, second):
            payload.pop("producer")

        self.assertEqual(first, second)
        self.assertEqual(
            first["datasets"]["element_charges"]["records"],
            [
                {
                    "element": "Si",
                    "status": "present",
                    "representative_oxidation_states": [4],
                }
            ],
        )

    def test_fe2o3_context_preserves_counts_and_element_order(self):
        payload = context_producer.build_context("Fe2O3")

        self.assertEqual(payload["composition"]["reduced_formula"], "Fe2O3")
        self.assertEqual(payload["composition"]["elements"], ["Fe", "O"])
        self.assertEqual(
            payload["composition"]["stoichiometric_amounts"],
            [
                {"element": "Fe", "amount": 2},
                {"element": "O", "amount": 3},
            ],
        )

        charges = {
            record["element"]: record
            for record in payload["datasets"]["element_charges"]["records"]
        }
        self.assertEqual(charges["Fe"]["representative_oxidation_states"], [2, 3])
        self.assertEqual(charges["O"]["representative_oxidation_states"], [-2])

    def test_valid_formula_with_missing_charge_evidence_still_returns_ok(self):
        payload = context_producer.build_context("He")

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["datasets"]["element_abundances"]["records"][0]["status"], "present")
        self.assertEqual(payload["datasets"]["element_charges"]["records"][0]["status"], "missing")
        self.assertEqual(
            payload["missing_evidence"],
            [
                {
                    "dataset": "element_charges",
                    "element": "He",
                    "reason": "element_not_present_in_dataset",
                }
            ],
        )

    def test_malformed_formula_returns_structured_error_without_traceback(self):
        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.composition.context_producer",
            ],
            input=json.dumps({"formula": "Fe2(O3"}),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stderr, "")

        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["error"]["code"], "malformed_formula")
        self.assertNotIn("Traceback", process.stdout)

    def test_stdout_json_is_valid_uncontaminated_and_has_provenance(self):
        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.composition.context_producer",
            ],
            input=json.dumps({"formula": "MnCu5"}),
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stderr, "")

        payload = json.loads(process.stdout)
        self.assertEqual(process.stdout, json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        self.assertEqual(payload["producer"]["name"], "BMDex")
        self.assertEqual(
            payload["producer"]["contract_module"],
            "tools.composition.context_producer",
        )
        self.assertRegex(payload["producer"]["git"]["commit"], r"^[0-9a-f]{40}$")
        self.assertIn(payload["producer"]["git"]["state"], {"clean", "dirty"})
        self.assertIsInstance(payload["producer"]["git"]["dirty"], bool)

    def test_limitations_are_preserved(self):
        payload = context_producer.build_context("MnCu5")
        limitation_codes = {item["code"] for item in payload["limitations"]}
        limitation_text = " ".join(item["text"] for item in payload["limitations"])

        self.assertIn("abundance_element_level_only", limitation_codes)
        self.assertIn("oxidation_states_element_level_only", limitation_codes)
        self.assertIn("does not establish compound viability or sustainability", limitation_text)
        self.assertIn("do not establish oxidation states", limitation_text)
        self.assertIn("stability, or existence", limitation_text)

    def test_no_network_access_in_context_build(self):
        def fail_if_called(*_args, **_kwargs):
            raise AssertionError("network API was unexpectedly called")

        with patch("urllib.request.urlopen", fail_if_called, create=True):
            with patch("socket.create_connection", fail_if_called):
                payload = context_producer.build_context("MnCu5")

        self.assertEqual(payload["status"], "ok")

    def test_cli_does_not_write_or_leak_secret_environment_values(self):
        before = self.snapshot_producer_paths()
        secret_value = "SHOULD_NOT_APPEAR_IN_COMPOSITION_CONTEXT_OUTPUT"
        env = os.environ.copy()
        env["BMD_SECRET_TEST_TOKEN"] = secret_value

        process = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.composition.context_producer",
            ],
            input=json.dumps({"formula": "MnCu5"}),
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        after = self.snapshot_producer_paths()

        self.assertEqual(process.returncode, 0)
        self.assertEqual(before, after)
        self.assertNotIn(secret_value, process.stdout)
        self.assertNotIn(secret_value, process.stderr)

    def test_rejects_unknown_request_fields(self):
        with self.assertRaises(context_producer.ContractError) as error:
            context_producer.parse_request(json.dumps({"formula": "Si", "api_key": "secret"}))

        self.assertEqual(error.exception.code, "invalid_request")


if __name__ == "__main__":
    unittest.main()
