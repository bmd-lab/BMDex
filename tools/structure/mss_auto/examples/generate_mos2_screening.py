"""
Example MSS-Auto screening workflow for MoS2.

This example demonstrates:
- structure loading
- slab generation
- vacuum insertion
- orientation handling
using reusable BMDex structure utilities.
"""

from pymatgen.core import Structure

from tools.structure.slabs.slab_generator import generate_slab
from tools.structure.orientations.orientation_utils import (
    describe_orientation
)

# Load structure
structure = Structure.from_file("POSCAR")

# Generate slab
slab = generate_slab(
    structure=structure,
    miller_index=(0, 0, 1),
    min_slab_size=12.0,
    min_vacuum_size=20.0
)

# Save output
slab.to(fmt="poscar", filename="POSCAR_slab")

print(describe_orientation((0, 0, 1)))
print("Generated MoS2 slab structure.")
