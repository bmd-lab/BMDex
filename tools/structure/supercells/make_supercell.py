#!/usr/bin/env python3

"""
Build a supercell from a VASP CONTCAR/POSCAR using pymatgen.

This utility:
- loads a structure
- applies a user-defined supercell scaling matrix
- writes a VASP-compatible POSCAR supercell

Typical use cases:
- defect calculations
- phonon supercells
- dilute substitutions
- convergence tests
- larger slab or interface construction
"""

from pathlib import Path

from pymatgen.io.vasp import Poscar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_STRUCTURE = "CONTCAR"

# Common examples:
# 2x2x2 supercell:
# SCALING_MATRIX = [2, 2, 2]
#
# General 3x3 matrix:
# SCALING_MATRIX = [
#     [2, 0, 0],
#     [0, 2, 0],
#     [0, 0, 1],
# ]
SCALING_MATRIX = [2, 2, 2]

OUTPUT_STRUCTURE = "POSCAR_supercell.vasp"


# ----------------------------------------------------------------------
# Load structure
# ----------------------------------------------------------------------

input_path = Path(INPUT_STRUCTURE)

if not input_path.exists():
    raise FileNotFoundError(f"Structure file not found: {INPUT_STRUCTURE}")

structure = Poscar.from_file(input_path).structure

initial_sites = len(structure)


# ----------------------------------------------------------------------
# Build supercell
# ----------------------------------------------------------------------

supercell = structure.copy()
supercell.make_supercell(SCALING_MATRIX)


# ----------------------------------------------------------------------
# Write output
# ----------------------------------------------------------------------

output_path = Path(OUTPUT_STRUCTURE)
Poscar(supercell).write_file(output_path)

print(f"Input structure: {input_path}")
print(f"Initial sites:   {initial_sites}")
print(f"Final sites:     {len(supercell)}")
print(f"Wrote:           {output_path}")
