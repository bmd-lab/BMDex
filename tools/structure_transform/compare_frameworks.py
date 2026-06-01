#!/usr/bin/env python3

"""
Compare two structures using pymatgen StructureMatcher.

This utility:
- loads two VASP POSCAR/CONTCAR files
- optionally compares only the structural framework
- reports whether the structures match

Typical use cases:
- checking whether a generated structure preserves a parent framework
- comparing relaxed and starting structures
- validating SQS or substitution workflows
"""

from pathlib import Path

from pymatgen.analysis.structure_matcher import FrameworkComparator
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.io.vasp import Poscar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

REFERENCE_STRUCTURE = "POSCAR_reference"
CANDIDATE_STRUCTURE = "POSCAR_candidate"

# If True, compare frameworks while ignoring species identity.
USE_FRAMEWORK_COMPARATOR = True

LATTICE_TOLERANCE = 0.2
SITE_TOLERANCE = 0.3
ANGLE_TOLERANCE = 5.0


# ----------------------------------------------------------------------
# Load structures
# ----------------------------------------------------------------------

reference_path = Path(REFERENCE_STRUCTURE)
candidate_path = Path(CANDIDATE_STRUCTURE)

if not reference_path.exists():
    raise FileNotFoundError(f"Reference structure not found: {reference_path}")

if not candidate_path.exists():
    raise FileNotFoundError(f"Candidate structure not found: {candidate_path}")

reference = Poscar.from_file(reference_path).structure
candidate = Poscar.from_file(candidate_path).structure


# ----------------------------------------------------------------------
# Compare structures
# ----------------------------------------------------------------------

if USE_FRAMEWORK_COMPARATOR:
    matcher = StructureMatcher(
        ltol=LATTICE_TOLERANCE,
        stol=SITE_TOLERANCE,
        angle_tol=ANGLE_TOLERANCE,
        comparator=FrameworkComparator(),
    )
else:
    matcher = StructureMatcher(
        ltol=LATTICE_TOLERANCE,
        stol=SITE_TOLERANCE,
        angle_tol=ANGLE_TOLERANCE,
    )

matches = matcher.fit(reference, candidate)
rms = matcher.get_rms_dist(reference, candidate)


# ----------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------

print(f"Reference: {reference_path}")
print(f"Candidate: {candidate_path}")
print(f"Framework comparator: {USE_FRAMEWORK_COMPARATOR}")
print(f"Matches: {matches}")

if rms is not None:
    print(f"RMS distance: {rms}")
