"""
Reusable slab-generation utilities for BMDex.
"""

from pymatgen.core.surface import SlabGenerator
from pymatgen.core.structure import Structure


def generate_slab(
    structure: Structure,
    miller_index=(0, 0, 1),
    min_slab_size=10.0,
    min_vacuum_size=15.0,
    center_slab=True
):
    """
    Generate a slab structure.

    Args:
        structure:
            pymatgen Structure object

        miller_index:
            Surface orientation

        min_slab_size:
            Minimum slab thickness in Å

        min_vacuum_size:
            Minimum vacuum thickness in Å

        center_slab:
            Whether to center slab in the cell

    Returns:
        pymatgen Slab object
    """

    slabgen = SlabGenerator(
        initial_structure=structure,
        miller_index=miller_index,
        min_slab_size=min_slab_size,
        min_vacuum_size=min_vacuum_size,
        center_slab=center_slab
    )

    slabs = slabgen.get_slabs()

    if not slabs:
        raise RuntimeError("No slabs generated.")

    return slabs[0]
