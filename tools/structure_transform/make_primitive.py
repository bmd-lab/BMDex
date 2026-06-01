#!/usr/bin/env python3

"""
Generate a primitive cell from a VASP CONTCAR/POSCAR using pymatgen.

This utility:
- loads a structure
- optionally uses symmetry analysis to find a primitive standard cell
- falls back to pymatgen's direct primitive-cell reduction
- writes a VASP-compatible POSCAR primitive cell

Typical use cases:
- reducing relaxed supercells
- preparing compact reference structures
- cleaning up imported CIF/POSCAR structures
- checking whether a calculation cell can be simplified
"""

from pathlib import Path

from pymatgen.io.vasp import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_STRUCTURE = "CONTCAR"

OUTPUT_STRUCTURE = "POSCAR_primitive.vasp"

# Try symmetry-based primitive standardization first.
USE_SYMMETRY_ANALYZER = True

SYMPREC = 0.01
ANGLE_TOLERANCE = 5.0


# ----------------------------------------------------------------------
# Load structure
# ----------------------------------------------------------------------

input_path = Path(INPUT_STRUCTURE)

if not input_path.exists():
    raise FileNotFoundError(f"Structure file not found: {INPUT_STRUCTURE}")

structure = Poscar.from_file(input_path).structure

initial_sites = len(structure)


# ----------------------------------------------------------------------
# Generate primitive cell
# ----------------------------------------------------------------------

if USE_SYMMETRY_ANALYZER:
    analyzer = SpacegroupAnalyzer(
        structure,
        symprec=SYMPREC,
        angle_tolerance=ANGLE_TOLERANCE,
    )
    primitive = analyzer.get_primitive_standard_structure()
else:
    primitive = structure.get_primitive_structure()


# ----------------------------------------------------------------------
# Write output
# ----------------------------------------------------------------------

output_path = Path(OUTPUT_STRUCTURE)
Poscar(primitive).write_file(output_path)

print(f"Input structure: {input_path}")
print(f"Initial sites:   {initial_sites}")
print(f"Final sites:     {len(primitive)}")
print(f"Wrote:           {output_path}")
