#!/usr/bin/env python3

"""
Emit BMDex composition-context evidence from local curated datasets.

The command reads one JSON object from stdin:

    {"formula": "MnCu5"}

It writes exactly one JSON object to stdout. The producer intentionally uses
only local BMDex data and fixed local Git commands for repository provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from math import gcd
from pathlib import Path
import json
import re
import subprocess
import sys
from typing import Any


SCHEMA_VERSION = 1
EVIDENCE_TYPE = "composition_context"
PRODUCER_NAME = "BMDex"
CONTRACT_MODULE = "tools.composition.context_producer"
CONTRACT_COMMAND = "python -B -m tools.composition.context_producer"

REPO_ROOT = Path(__file__).resolve().parents[2]
ABUNDANCE_PATH = REPO_ROOT / "datasets" / "element_abundances" / "earth-abundance.yaml"
CHARGE_PATH = REPO_ROOT / "datasets" / "element_charges" / "oxidation_states_84.yaml"

PERIODIC_TABLE_SYMBOLS = frozenset(
    [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
        "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
        "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
    ]
)

FORMULA_TOKEN_RE = re.compile(r"([A-Z][a-z]?)([0-9]*)")
DATASET_SCALAR_RE = re.compile(
    r"^([A-Z][a-z]?):\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*$"
)
DATASET_KEY_RE = re.compile(r"^([A-Z][a-z]?):\s*$")
DATASET_LIST_ITEM_RE = re.compile(r"^\s+-\s*([-+]?\d+)\s*$")


class ContractError(Exception):
    """Expected producer error reported as structured JSON."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ParsedComposition:
    supplied_formula: str
    reduced_formula: str
    elements: list[str]
    amounts: dict[str, int]


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


def parse_request(raw_stdin: str) -> str:
    try:
        request = json.loads(raw_stdin)
    except json.JSONDecodeError as exc:
        raise ContractError("invalid_json", f"Request body is not valid JSON: {exc.msg}") from exc

    if not isinstance(request, dict):
        raise ContractError("invalid_request", "Request must be a JSON object.")

    allowed_keys = {"formula"}
    extra_keys = sorted(set(request) - allowed_keys)
    if extra_keys:
        raise ContractError(
            "invalid_request",
            f"Unsupported request field(s): {', '.join(extra_keys)}",
        )

    formula = request.get("formula")
    if not isinstance(formula, str):
        raise ContractError("invalid_request", "Field 'formula' must be a string.")

    if not formula:
        raise ContractError("malformed_formula", "Formula must not be empty.")

    if formula != formula.strip() or any(ch.isspace() for ch in formula):
        raise ContractError("malformed_formula", "Formula must not contain whitespace.")

    return formula


def parse_formula(formula: str) -> ParsedComposition:
    pos = 0
    elements: list[str] = []
    amounts: dict[str, int] = {}

    while pos < len(formula):
        match = FORMULA_TOKEN_RE.match(formula, pos)
        if not match:
            raise ContractError(
                "malformed_formula",
                "Formula syntax is unsupported or malformed.",
            )

        element, count_text = match.groups()

        if element not in PERIODIC_TABLE_SYMBOLS:
            raise ContractError("malformed_formula", f"Unknown element symbol: {element}")

        if count_text.startswith("0"):
            raise ContractError(
                "malformed_formula",
                f"Invalid stoichiometric amount for element {element}: {count_text}",
            )

        amount = int(count_text) if count_text else 1
        if amount <= 0:
            raise ContractError(
                "malformed_formula",
                f"Invalid stoichiometric amount for element {element}: {count_text}",
            )

        if element not in amounts:
            elements.append(element)

        amounts[element] = amounts.get(element, 0) + amount
        pos = match.end()

    if not amounts:
        raise ContractError("malformed_formula", "Formula contains no elements.")

    divisor = reduce(gcd, amounts.values())
    reduced_amounts = {
        element: amount // divisor
        for element, amount in amounts.items()
    }
    reduced_formula = format_formula(elements, reduced_amounts)

    return ParsedComposition(
        supplied_formula=formula,
        reduced_formula=reduced_formula,
        elements=elements,
        amounts=amounts,
    )


def format_formula(elements: list[str], amounts: dict[str, int]) -> str:
    parts = []
    for element in elements:
        amount = amounts[element]
        parts.append(element if amount == 1 else f"{element}{amount}")
    return "".join(parts)


def parse_scalar_dataset(path: Path) -> dict[str, float]:
    records: dict[str, float] = {}

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = DATASET_SCALAR_RE.match(line)
        if not match:
            raise ContractError(
                "dataset_error",
                f"Unsupported scalar dataset line in {repo_relative(path)}:{line_number}",
            )

        element, value = match.groups()
        records[element] = float(value)

    if not records:
        raise ContractError("dataset_error", f"Dataset is empty: {repo_relative(path)}")

    return records


def parse_integer_list_dataset(path: Path) -> dict[str, list[int]]:
    records: dict[str, list[int]] = {}
    current_element: str | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        key_match = DATASET_KEY_RE.match(line)
        if key_match:
            current_element = key_match.group(1)
            records[current_element] = []
            continue

        item_match = DATASET_LIST_ITEM_RE.match(line)
        if item_match and current_element:
            records[current_element].append(int(item_match.group(1)))
            continue

        raise ContractError(
            "dataset_error",
            f"Unsupported list dataset line in {repo_relative(path)}:{line_number}",
        )

    empty = [element for element, values in records.items() if not values]
    if empty:
        raise ContractError(
            "dataset_error",
            f"Missing list value(s) in {repo_relative(path)} for: {', '.join(empty)}",
        )

    if not records:
        raise ContractError("dataset_error", f"Dataset is empty: {repo_relative(path)}")

    return records


def abundance_records(elements: list[str], abundance_data: dict[str, float]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    records = []
    missing = []

    for element in elements:
        if element in abundance_data:
            records.append(
                {
                    "element": element,
                    "status": "present",
                    "abundance": abundance_data[element],
                    "units": "mg/kg",
                }
            )
        else:
            records.append(
                {
                    "element": element,
                    "status": "missing",
                    "abundance": None,
                    "units": "mg/kg",
                }
            )
            missing.append(
                {
                    "dataset": "element_abundances",
                    "element": element,
                    "reason": "element_not_present_in_dataset",
                }
            )

    return records, missing


def charge_records(elements: list[str], charge_data: dict[str, list[int]]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    records = []
    missing = []

    for element in elements:
        if element in charge_data:
            records.append(
                {
                    "element": element,
                    "status": "present",
                    "representative_oxidation_states": charge_data[element],
                }
            )
        else:
            records.append(
                {
                    "element": element,
                    "status": "missing",
                    "representative_oxidation_states": None,
                }
            )
            missing.append(
                {
                    "dataset": "element_charges",
                    "element": element,
                    "reason": "element_not_present_in_dataset",
                }
            )

    return records, missing


def build_context(formula: str) -> dict[str, Any]:
    parsed = parse_formula(formula)
    abundance_data = parse_scalar_dataset(ABUNDANCE_PATH)
    charge_data = parse_integer_list_dataset(CHARGE_PATH)

    abundances, missing_abundances = abundance_records(parsed.elements, abundance_data)
    charges, missing_charges = charge_records(parsed.elements, charge_data)

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "evidence_type": EVIDENCE_TYPE,
        "producer": producer_provenance(),
        "composition": {
            "supplied_formula": parsed.supplied_formula,
            "reduced_formula": parsed.reduced_formula,
            "elements": parsed.elements,
            "stoichiometric_amounts": [
                {
                    "element": element,
                    "amount": parsed.amounts[element],
                }
                for element in parsed.elements
            ],
        },
        "datasets": {
            "element_abundances": {
                "dataset_id": "bmdex.datasets.element_abundances.earth_abundance",
                "path": repo_relative(ABUNDANCE_PATH),
                "quantity": "crustal abundance",
                "units": "mg/kg",
                "source_reference_status": "not_machine_readable",
                "records": abundances,
            },
            "element_charges": {
                "dataset_id": "bmdex.datasets.element_charges.oxidation_states_84",
                "path": repo_relative(CHARGE_PATH),
                "term": "representative oxidation states",
                "source_reference_status": "not_machine_readable",
                "records": charges,
            },
        },
        "missing_evidence": missing_abundances + missing_charges,
        "limitations": [
            {
                "code": "abundance_element_level_only",
                "text": (
                    "Element abundance is contextual element-level evidence and "
                    "does not establish compound viability or sustainability."
                ),
            },
            {
                "code": "oxidation_states_element_level_only",
                "text": (
                    "Representative oxidation-state entries are element-level "
                    "reference data and do not establish oxidation states, charge "
                    "balance, stability, or existence of the supplied compound."
                ),
            },
            {
                "code": "source_references_not_machine_readable",
                "text": (
                    "Dataset source/reference details are documented in nearby "
                    "README files but are not yet available as machine-readable "
                    "dataset fields."
                ),
            },
        ],
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
        formula = parse_request(sys.stdin.read())
        emit_json(build_context(formula))
        return 0
    except ContractError as error:
        emit_json(error_response(error))
        return 2
    except Exception as error:
        emit_json(
            error_response(
                ContractError(
                    "producer_error",
                    f"Composition-context producer failed safely: {type(error).__name__}",
                )
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
