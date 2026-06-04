#!/usr/bin/env python3

"""
Generate a VASP POTCAR from a POTCAR.spec file using pymatgen.

This utility:
- reads element or POTCAR symbols from POTCAR.spec
- uses the local pymatgen POTCAR setup
- writes a VASP POTCAR in the current calculation directory

Actual POTCAR files should not be committed to BMDex.
"""

from pathlib import Path

from pymatgen.io.vasp.inputs import Potcar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

POTCAR_SPEC = "POTCAR.spec"
OUTPUT_POTCAR = "POTCAR"

FUNCTIONAL = "PBE_64"


# ----------------------------------------------------------------------
# Read POTCAR.spec
# ----------------------------------------------------------------------

spec_path = Path(POTCAR_SPEC)

if not spec_path.exists():
    raise FileNotFoundError(f"POTCAR spec not found: {POTCAR_SPEC}")

symbols = [
    line.strip()
    for line in spec_path.read_text().splitlines()
    if line.strip() and not line.strip().startswith("#")
]

if not symbols:
    raise ValueError(f"No POTCAR symbols found in {POTCAR_SPEC}")


# ----------------------------------------------------------------------
# Build and write POTCAR
# ----------------------------------------------------------------------

potcar = Potcar(symbols=symbols, functional=FUNCTIONAL)
output_path = Path(OUTPUT_POTCAR)
potcar.write_file(output_path)

print(f"Functional: {FUNCTIONAL}")
print(f"Symbols:    {', '.join(symbols)}")
print(f"Wrote:      {output_path}")
