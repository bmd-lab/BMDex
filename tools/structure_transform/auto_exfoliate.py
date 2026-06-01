#!/usr/bin/env python3

"""
Automatically generate an exfoliated slab from a VASP POSCAR/CONTCAR.

This utility is inspired by the original MSS-Auto workflow.

It:
- loads a bulk structure
- builds a supercell along a chosen direction if needed
- searches candidate cleavage positions using a probe point
- chooses the cleavage position with the largest nearest-neighbour distance
- inserts vacuum along the chosen direction
- shifts atoms across the cleavage plane
- writes a VASP-compatible POSCAR slab

Typical use cases:
- generating slabs from layered or van der Waals materials
- finding natural cleavage planes
- preparing exfoliated structures for VASP calculations
"""

from pathlib import Path

import numpy as np
from pymatgen.core import Structure
from pymatgen.io.vasp import Poscar


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_STRUCTURE = "CONTCAR"
OUTPUT_STRUCTURE = "POSCAR_auto_exfoliated.vasp"

# Cleavage direction: "x", "y", or "z"
CLEAVAGE_DIRECTION = "z"

# Minimum supercell length along cleavage direction before cleavage search.
MIN_CELL_LENGTH = 15.0  # Angstrom

# Vacuum inserted along cleavage direction.
VACUUM_SIZE = 15.0  # Angstrom

# Fractional probe grid used to search for open cleavage regions.
# More points = finer search but slower.
PROBE_GRID_ALONG_CLEAVAGE = np.linspace(0.005, 0.995, 100)
PROBE_GRID_PERPENDICULAR = np.arange(0.05, 0.95, 0.25)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

DIRECTION_TO_AXIS = {
    "x": 0,
    "y": 1,
    "z": 2,
}


def lattice_vector_length(structure, axis):
    """Return lattice-vector length along Cartesian lattice axis index."""

    vector = structure.lattice.matrix[axis]

    return float(np.linalg.norm(vector))


def scaling_for_min_length(structure, axis, min_length):
    """
    Return a diagonal supercell scaling matrix that makes the selected
    lattice vector at least min_length.
    """

    length = lattice_vector_length(structure, axis)

    factor = max(1, int(np.ceil(min_length / length)))

    scaling = [1, 1, 1]
    scaling[axis] = factor

    return scaling


def make_directional_supercell(structure, direction, min_length):
    """Make a supercell along one lattice direction if needed."""

    axis = DIRECTION_TO_AXIS[direction]

    scaling = scaling_for_min_length(structure, axis, min_length)

    supercell = structure.copy()
    supercell.make_supercell(scaling)

    return supercell, scaling


def probe_fractional_coordinates(direction):
    """
    Generate fractional probe coordinates.

    The probe scans densely along the cleavage direction and coarsely
    across the perpendicular directions.
    """

    axis = DIRECTION_TO_AXIS[direction]

    coordinates = []

    for cleavage_coord in PROBE_GRID_ALONG_CLEAVAGE:
        for u in PROBE_GRID_PERPENDICULAR:
            for v in PROBE_GRID_PERPENDICULAR:

                coord = [0.0, 0.0, 0.0]
                coord[axis] = cleavage_coord

                perpendicular_axes = [i for i in range(3) if i != axis]
                coord[perpendicular_axes[0]] = u
                coord[perpendicular_axes[1]] = v

                coordinates.append(coord)

    return coordinates


def nearest_atom_distance(structure, fractional_coord):
    """Return nearest distance from a fractional probe point to any atom."""

    cart_coord = structure.lattice.get_cartesian_coords(fractional_coord)

    distances = [
        structure.lattice.get_distance_and_image(
            cart_coord,
            site.coords,
        )[0]
        for site in structure
    ]

    return min(distances)


def find_best_cleavage_fraction(structure, direction):
    """
    Find the fractional coordinate along direction that maximizes the
    nearest-neighbour distance from a probe point to the structure.
    """

    best_coord = None
    best_distance = -1.0

    for coord in probe_fractional_coordinates(direction):

        distance = nearest_atom_distance(structure, coord)

        if distance > best_distance:
            best_distance = distance
            best_coord = coord

    axis = DIRECTION_TO_AXIS[direction]

    return best_coord[axis], best_distance


def insert_vacuum(structure, direction, vacuum_size):
    """Increase lattice length along selected direction."""

    axis = DIRECTION_TO_AXIS[direction]

    new_lattice = structure.lattice.matrix.copy()
    vector = new_lattice[axis]
    length = np.linalg.norm(vector)

    new_lattice[axis] = vector * ((length + vacuum_size) / length)

    new_structure = structure.copy()
    new_structure.modify_lattice(new_lattice)

    return new_structure


def shift_across_cleavage(structure, direction, cleavage_fraction, vacuum_size):
    """
    Shift atoms on one side of the cleavage plane to open a vacuum gap.

    Coordinates are handled fractionally before writing the final POSCAR.
    """

    axis = DIRECTION_TO_AXIS[direction]

    shifted = structure.copy()
    frac_coords = shifted.frac_coords.copy()

    lattice_length = lattice_vector_length(structure, axis)
    fractional_shift = vacuum_size / lattice_length

    for i, coord in enumerate(frac_coords):

        if coord[axis] > cleavage_fraction:
            coord[axis] += fractional_shift

        frac_coords[i] = coord

    shifted = Structure(
        lattice=shifted.lattice,
        species=shifted.species,
        coords=frac_coords,
        coords_are_cartesian=False,
        site_properties=shifted.site_properties,
    )

    return shifted


# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------

input_path = Path(INPUT_STRUCTURE)

if not input_path.exists():
    raise FileNotFoundError(f"Structure file not found: {input_path}")

if CLEAVAGE_DIRECTION not in DIRECTION_TO_AXIS:
    raise ValueError("CLEAVAGE_DIRECTION must be one of: x, y, z")

structure = Poscar.from_file(input_path).structure

print(f"Input structure: {input_path}")
print(f"Initial sites:   {len(structure)}")
print(f"Direction:       {CLEAVAGE_DIRECTION}")

supercell, scaling = make_directional_supercell(
    structure,
    CLEAVAGE_DIRECTION,
    MIN_CELL_LENGTH,
)

print(f"Supercell scale: {scaling}")
print(f"Supercell sites: {len(supercell)}")

cleavage_fraction, probe_distance = find_best_cleavage_fraction(
    supercell,
    CLEAVAGE_DIRECTION,
)

print(f"Best cleavage fraction: {cleavage_fraction:.4f}")
print(f"Probe nearest distance: {probe_distance:.4f} Angstrom")

with_vacuum = insert_vacuum(
    supercell,
    CLEAVAGE_DIRECTION,
    VACUUM_SIZE,
)

slab = shift_across_cleavage(
    with_vacuum,
    CLEAVAGE_DIRECTION,
    cleavage_fraction,
    VACUUM_SIZE,
)

output_path = Path(OUTPUT_STRUCTURE)
Poscar(slab).write_file(output_path)

print(f"Wrote: {output_path}")
