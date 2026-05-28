#!/usr/bin/env python3

"""
Generate surface slabs from a VASP CONTCAR/POSCAR using pymatgen.

This utility:
- loads a structure
- optionally applies oxidation states
- generates slabs up to a chosen Miller index
- writes VASP-compatible POSCAR slab files

Typical use cases:
- surface calculations
- slab generation
- layered-material workflows
- adsorption studies
"""

from pathlib import Path

from pymatgen.core.surface import generate_all_slabs
from pymatgen.io.vasp import Poscar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_STRUCTURE = "CONTCAR"

MAX_MILLER_INDEX = 2

MIN_SLAB_SIZE = 10.0      # Angstrom
MIN_VACUUM_SIZE = 15.0    # Angstrom

CENTER_SLAB = True

# Optional oxidation states. Leave empty if not needed.
OXIDATION_STATES = {
    # "Fe": 3,
    # "La": 3,
    # "O": -2,
}

# Output directory for generated POSCAR files.
OUTPUT_DIR = "generated_slabs"


# ----------------------------------------------------------------------
# Load structure
# ----------------------------------------------------------------------

input_path = Path(INPUT_STRUCTURE)

if not input_path.exists():
    raise FileNotFoundError(f"Structure file not found: {INPUT_STRUCTURE}")

structure = Poscar.from_file(input_path).structure


# ----------------------------------------------------------------------
# Apply oxidation states if provided
# ----------------------------------------------------------------------

if OXIDATION_STATES:
    structure.add_oxidation_state_by_element(OXIDATION_STATES)


# ----------------------------------------------------------------------
# Generate slabs
# ----------------------------------------------------------------------

slabs = generate_all_slabs(
    structure=structure,
    max_index=MAX_MILLER_INDEX,
    min_slab_size=MIN_SLAB_SIZE,
    min_vacuum_size=MIN_VACUUM_SIZE,
    center_slab=CENTER_SLAB,
)


# ----------------------------------------------------------------------
# Write slabs
# ----------------------------------------------------------------------

output_dir = Path(OUTPUT_DIR)
output_dir.mkdir(exist_ok=True)

print(f"Generated {len(slabs)} slabs\n")

seen_miller_indices = {}

for slab in slabs:
    miller = "".join(
        str(index).replace("-", "m")
        for index in slab.miller_index
    )
    seen_miller_indices[miller] = seen_miller_indices.get(miller, 0) + 1

    output_file = output_dir / (
        f"POSCAR_{miller}_{seen_miller_indices[miller]:02d}.vasp"
    )

    Poscar(slab).write_file(output_file)

    print(f"Wrote: {output_file}")
