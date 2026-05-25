"""
Reusable supercell-generation utilities for BMDex.
"""

from pymatgen.core.structure import Structure


def make_supercell(structure: Structure, scaling_matrix):
    """
    Generate a supercell.

    Args:
        structure:
            pymatgen Structure object

        scaling_matrix:
            Supercell scaling matrix

    Returns:
        pymatgen Structure object
    """

    supercell = structure.copy()

    supercell.make_supercell(scaling_matrix)

    return supercell
