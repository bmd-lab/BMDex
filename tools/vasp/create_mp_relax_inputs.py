#!/usr/bin/env python3

"""
Create VASP relaxation input folders from Materials Project IDs.

This utility:
- fetches structures from the Materials Project API
- writes pymatgen MPRelaxSet inputs
- writes POTCAR.spec by default instead of licensed POTCAR content

Typical use cases:
- preparing reference calculations
- generating starting inputs for screening workflows
- reproducing Materials Project-like relaxation inputs
"""

import os
from pathlib import Path

from mp_api.client import MPRester
from pymatgen.io.vasp.sets import MPRelaxSet


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

MP_IDS = [
    "mp-149",  # Si
]

OUTPUT_ROOT = "mp_relax_inputs"

API_KEY_ENV = "MP_API_KEY"

# Keep this True for repository-safe input generation.
WRITE_POTCAR_SPEC_ONLY = True


# ----------------------------------------------------------------------
# Fetch structures and write inputs
# ----------------------------------------------------------------------

api_key = os.environ.get(API_KEY_ENV)

if not api_key:
    raise EnvironmentError(
        f"Set {API_KEY_ENV} before running this script."
    )

output_root = Path(OUTPUT_ROOT)
output_root.mkdir(exist_ok=True)

with MPRester(api_key) as mpr:
    for mp_id in MP_IDS:
        print(f"Fetching: {mp_id}")
        structure = mpr.get_structure_by_material_id(mp_id)

        output_dir = output_root / mp_id
        input_set = MPRelaxSet(structure)
        input_set.write_input(
            output_dir,
            make_dir_if_not_present=True,
            potcar_spec=WRITE_POTCAR_SPEC_ONLY,
        )

        print(f"Wrote:    {output_dir}")
