# MSS-Auto

MSS-Auto is a workflow for automated slab and supercell generation from crystalline structures.

The workflow was originally developed to support:
- identification of potentially exfoliable materials
- automated generation of slab structures
- high-throughput computational screening
- dimensionality analysis of materials

The workflow operates on VASP POSCAR structures and automates:
- supercell construction
- vacuum insertion
- slab preparation
- crystallographic-direction processing

## Scientific Context

The methodology was used in:

> Predicting two-dimensional semiconductors using conductivity effective mass
> Phys. Chem. Chem. Phys. (2024)

The work investigated whether conductivity effective mass anisotropy could predict exfoliation behavior and layered crystallography.

## Repository Role

Within BMDex, MSS-Auto serves as:
- a reusable structure-generation workflow
- an automated slab-generation utility
- a bridge between crystallographic analysis and VASP workflows

## Dependencies

- pymatgen
- numpy

## Notes

The workflow is intended as a practical structure-generation tool and should not be interpreted as a full thermodynamic exfoliation framework.
