#!/usr/bin/env python3

"""
Submit many VASP calculation directories on a SLURM cluster.

This utility:
- scans calculation folders
- skips completed or incomplete calculations
- limits submissions based on the current user's queue
- submits local SLURM scripts with sbatch

Typical use cases:
- high-throughput VASP screening
- restarting batches after input generation
- submitting many independent relaxation directories
"""

from __future__ import annotations

import argparse
import os
import subprocess
import time
from pathlib import Path
from typing import List
from typing import Optional


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

ROOT = "."

JOB_SCRIPT_NAMES = [
    "submit.sbatch",
    "job.script",
    "job_script.sh",
    "submit_vasp.sbatch",
]

REQUIRED_INPUTS = [
    "INCAR",
    "POSCAR",
    "KPOINTS",
]

COMPLETION_MARKER = "Voluntary"

MAX_QUEUED_JOBS = 20
POLL_SECONDS = 60


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def calculation_complete(directory: Path) -> bool:
    return COMPLETION_MARKER in read_text(directory / "OUTCAR")


def missing_required_inputs(directory: Path) -> List[str]:
    return [
        name
        for name in REQUIRED_INPUTS
        if not (directory / name).is_file()
    ]


def find_job_script(directory: Path, names: List[str]) -> Optional[Path]:
    for name in names:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def discover_directories(root: Path, recursive: bool) -> List[Path]:
    if recursive:
        candidates = [path for path in root.rglob("*") if path.is_dir()]
    else:
        candidates = [path for path in root.iterdir() if path.is_dir()]
    return sorted(candidates)


def queued_job_count(user: str) -> int:
    try:
        result = subprocess.run(
            ["squeue", "-h", "-u", user],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return 0

    if result.returncode != 0:
        return 0

    return sum(1 for line in result.stdout.splitlines() if line.strip())


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
        description="Submit many VASP calculation directories with queue throttling.",
    )
    parser.add_argument(
        "--root",
        default=ROOT,
        help="Root directory containing calculation subdirectories.",
    )
    parser.add_argument(
        "--job-script",
        action="append",
        dest="job_scripts",
        help="Accepted SLURM script name. May be supplied more than once.",
    )
    parser.add_argument(
        "--max-queued",
        type=int,
        default=MAX_QUEUED_JOBS,
        help="Maximum number of current-user jobs allowed before waiting.",
    )
    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=POLL_SECONDS,
        help="Seconds to wait before checking the queue again.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan directories recursively instead of only direct children.",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Actually submit jobs. Without this flag, only print a dry run.",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    job_script_names = args.job_scripts or JOB_SCRIPT_NAMES
    user = os.environ.get("USER", "")

    if not root.is_dir():
        raise NotADirectoryError(f"Root directory not found: {root}")

    candidates = discover_directories(root, recursive=args.recursive)
    submitted = 0
    skipped = 0

    print(f"Scanning: {root}")
    print(f"Mode: {'submit' if args.submit else 'dry run'}")
    print()

    for directory in candidates:
        job_script = find_job_script(directory, job_script_names)
        missing_inputs = missing_required_inputs(directory)

        if job_script is None and missing_inputs:
            continue

        if missing_inputs:
            print(f"SKIP missing inputs {missing_inputs}: {directory}")
            skipped += 1
            continue

        if job_script is None:
            print(f"SKIP missing job script: {directory}")
            skipped += 1
            continue

        if calculation_complete(directory):
            print(f"SKIP complete: {directory}")
            skipped += 1
            continue

        if not args.submit:
            print(f"DRY RUN submit {job_script.name}: {directory}")
            submitted += 1
            continue

        while queued_job_count(user) >= args.max_queued:
            print(
                f"Queue has {queued_job_count(user)} jobs for {user}; "
                f"waiting {args.poll_seconds} seconds."
            )
            time.sleep(args.poll_seconds)

        print(f"Submitting {job_script.name}: {directory}")
        submit(directory, job_script)
        submitted += 1

    action = "submitted" if args.submit else "would submit"
    print()
    print(f"Done: {action} {submitted}; skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
