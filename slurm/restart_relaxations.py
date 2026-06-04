#!/usr/bin/env python3

"""
Prepare VASP relaxation restarts by copying CONTCAR to POSCAR.

This utility:
- scans VASP calculation directories
- finds runs that reached the INCAR NSW limit
- backs up POSCAR
- copies CONTCAR to POSCAR
- optionally resubmits the local SLURM job

Default behavior is a dry run.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

ROOT = "."
RECURSIVE = False

JOB_SCRIPT_NAMES = [
    "submit.sbatch",
    "job.script",
    "job_script.sh",
    "submit_vasp.sbatch",
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
# Restart logic
# ----------------------------------------------------------------------

def reached_nsw(directory: Path) -> bool:
    outcar = directory / "OUTCAR"
    oszicar = directory / "OSZICAR"
    incar = directory / "INCAR"

    nsw = parse_nsw(incar)
    if not nsw or not outcar.is_file() or not oszicar.is_file():
        return False

    normal_end = COMPLETION_MARKER in read_text(outcar)
    return normal_end and count_ionic_steps(oszicar) >= nsw


def restartable(directory: Path, all_with_contcar: bool) -> bool:
    contcar = directory / "CONTCAR"
    if not nonempty(contcar):
        return False
    if all_with_contcar:
        return True
    return reached_nsw(directory)


def find_job_script(directory: Path, names: List[str]) -> Optional[Path]:
    for name in names:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def discover_directories(root: Path, recursive: bool) -> List[Path]:
    candidates = root.rglob("*") if recursive else root.iterdir()
    result = []
    for path in candidates:
        if path.is_dir() and (path / "CONTCAR").exists():
            result.append(path)
    return sorted(result)


def apply_restart(directory: Path, timestamp: str) -> Path:
    poscar = directory / "POSCAR"
    contcar = directory / "CONTCAR"
    backup = directory / f"POSCAR.before_restart.{timestamp}"

    if poscar.exists():
        shutil.copy2(poscar, backup)

    shutil.copy2(contcar, poscar)
    return backup


def submit(directory: Path, job_script: Path) -> None:
    subprocess.run(
        ["sbatch", job_script.name],
        cwd=directory,
        check=True,
    )


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare VASP relaxation restarts from CONTCAR files.",
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
    parser.add_argument(
        "--job-script",
        action="append",
        dest="job_scripts",
        help="Accepted SLURM script name. May be supplied more than once.",
    )
    parser.add_argument(
        "--all-with-contcar",
        action="store_true",
        help="Restart every directory with a non-empty CONTCAR.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually copy CONTCAR to POSCAR. Default is dry run.",
    )
    parser.add_argument(
        "--resubmit",
        action="store_true",
        help="Submit the local job script after applying the restart.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    job_script_names = args.job_scripts or JOB_SCRIPT_NAMES
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    if not root.is_dir():
        raise NotADirectoryError(f"Root directory not found: {root}")

    mode = "apply" if args.apply else "dry run"
    print(f"Scanning: {root}")
    print(f"Mode: {mode}")
    print()

    changed = 0
    skipped = 0

    for directory in discover_directories(root, recursive=args.recursive):
        if not restartable(directory, all_with_contcar=args.all_with_contcar):
            skipped += 1
            continue

        job_script = find_job_script(directory, job_script_names)

        if not args.apply:
            print(f"DRY RUN restart: {directory}")
            changed += 1
            continue

        backup = apply_restart(directory, timestamp)
        print(f"Restarted: {directory}")
        if backup.exists():
            print(f"  Backup: {backup.name}")

        if args.resubmit:
            if job_script is None:
                print("  No job script found; not submitted.")
            else:
                submit(directory, job_script)
                print(f"  Submitted: {job_script.name}")

        changed += 1

    action = "changed" if args.apply else "would restart"
    print()
    print(f"Done: {action} {changed}; skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
