#!/usr/bin/env python3

"""
Sort a VASP POSCAR/CONTCAR by species using pymatgen.

This utility:
- loads a POSCAR or CONTCAR
- sorts sites by species
- writes a VASP-compatible POSCAR

Typical use cases:
- aligning POSCAR species order with POTCAR.spec
- cleaning SQS or substituted structures
- preparing structures for VASP input generation
"""

from pathlib import Path

from pymatgen.io.vasp import Poscar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_STRUCTURE = "POSCAR"
OUTPUT_STRUCTURE = "POSCAR_sorted.vasp"


# ----------------------------------------------------------------------
# Load and sort structure
# ----------------------------------------------------------------------

input_path = Path(INPUT_STRUCTURE)

if not input_path.exists():
    raise FileNotFoundError(f"Structure file not found: {INPUT_STRUCTURE}")

structure = Poscar.from_file(input_path).structure

sorted_structure = structure.get_sorted_structure()


# ----------------------------------------------------------------------
# Write output
# ----------------------------------------------------------------------

output_path = Path(OUTPUT_STRUCTURE)
Poscar(sorted_structure).write_file(output_path)

print(f"Input:  {input_path}")
print(f"Output: {output_path}")
