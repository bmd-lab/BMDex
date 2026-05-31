#!/usr/bin/env python3

"""
Report operational status for VASP calculation directories.

This utility:
- scans folders for VASP input and output files
- checks OUTCAR for normal termination
- compares OSZICAR ionic steps with INCAR NSW
- identifies directories that are likely restartable

This is an operational triage script, not a scientific convergence validator.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

ROOT = "."
RECURSIVE = False

REQUIRED_INPUTS = [
    "INCAR",
    "POSCAR",
    "KPOINTS",
]

COMPLETION_MARKER = "Voluntary"


# ----------------------------------------------------------------------
# Parsers
# ----------------------------------------------------------------------

def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def strip_incar_comment(line: str) -> str:
    for marker in ("!", "#"):
        if marker in line:
            line = line.split(marker, 1)[0]
    return line.strip()


def parse_nsw(incar: Path) -> Optional[int]:
    for line in read_text(incar).splitlines():
        clean = strip_incar_comment(line)
        match = re.match(r"^NSW\s*=\s*(\d+)", clean, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def count_ionic_steps(oszicar: Path) -> int:
    count = 0
    for line in read_text(oszicar).splitlines():
        if re.match(r"^\s*\d+\s+F=", line):
            count += 1
    return count


def nonempty(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


# ----------------------------------------------------------------------
# Status logic
# ----------------------------------------------------------------------

def missing_required_inputs(directory: Path) -> List[str]:
    return [
        name
        for name in REQUIRED_INPUTS
        if not (directory / name).is_file()
    ]


def classify(directory: Path) -> Tuple[str, Optional[int], Optional[int], str]:
    outcar = directory / "OUTCAR"
    oszicar = directory / "OSZICAR"
    incar = directory / "INCAR"
    contcar = directory / "CONTCAR"

    missing = missing_required_inputs(directory)
    nsw = parse_nsw(incar) if incar.is_file() else None
    ionic_steps = count_ionic_steps(oszicar) if oszicar.is_file() else None

    if missing:
        return "missing_inputs", ionic_steps, nsw, ",".join(missing)

    if not outcar.is_file():
        return "not_started", ionic_steps, nsw, ""

    normal_end = COMPLETION_MARKER in read_text(outcar)

    if normal_end and nsw and ionic_steps is not None and ionic_steps >= nsw:
        if nonempty(contcar):
            return "restartable_reached_nsw", ionic_steps, nsw, "CONTCAR available"
        return "reached_nsw_no_contcar", ionic_steps, nsw, ""

    if normal_end:
        return "complete", ionic_steps, nsw, ""

    if nonempty(contcar):
        return "stopped_with_contcar", ionic_steps, nsw, "manual review"

    return "running_or_failed", ionic_steps, nsw, "manual review"


def discover_directories(root: Path, recursive: bool) -> List[Path]:
    candidates = root.rglob("*") if recursive else root.iterdir()
    result = []
    for path in candidates:
        if not path.is_dir():
            continue
        files = {child.name for child in path.iterdir() if child.is_file()}
        if files.intersection({"INCAR", "OUTCAR", "OSZICAR", "CONTCAR"}):
            result.append(path)
    return sorted(result)


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize VASP calculation directory status.",
    )
    parser.add_argument(
        "--root",
        default=ROOT,
        help="Root directory containing calculation subdirectories.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        default=RECURSIVE,
        help="Scan recursively instead of only direct children.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.is_dir():
        raise NotADirectoryError(f"Root directory not found: {root}")

    print(f"{'status':<25} {'steps':>6} {'NSW':>6}  path")
    print(f"{'-' * 25} {'-' * 6} {'-' * 6}  {'-' * 40}")

    for directory in discover_directories(root, recursive=args.recursive):
        status, steps, nsw, note = classify(directory)
        steps_text = "-" if steps is None else str(steps)
        nsw_text = "-" if nsw is None else str(nsw)
        suffix = f"  ({note})" if note else ""
        print(
            f"{status:<25} {steps_text:>6} {nsw_text:>6}  "
            f"{directory}{suffix}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
