# MSS-Auto

MSS-Auto is a workflow for automated structure screening and slab-generation analysis within computational materials science workflows.

The workflow was originally developed to support:
- identification of potentially exfoliable materials
- automated slab and supercell generation
- crystallographic orientation analysis
- high-throughput screening of layered materials

The methodology was associated with:

> Predicting two-dimensional semiconductors using conductivity effective mass
> Phys. Chem. Chem. Phys. (2024)

## Scientific Context

The workflow explores relationships between:
- conductivity effective mass anisotropy
- crystal structure
- layered behavior
- and exfoliation likelihood.

MSS-Auto combines:
- crystallographic analysis
- structure manipulation
- and automated workflow logic
to facilitate large-scale screening studies.

## Repository Role

Within BMDex, MSS-Auto serves as:
- a reusable screening workflow
- a bridge between crystallographic analysis and VASP workflows
- an example of reusable workflow orchestration built on shared BMDex primitives

Generic reusable structure utilities are maintained separately under:

```text
tools/structure/
```

including:
- slab generation
- supercell construction
- vacuum manipulation
- orientation utilities

## Dependencies

Typical dependencies include:
- pymatgen
- numpy

## Notes

MSS-Auto should be interpreted as:
- a practical workflow framework
- a screening methodology
- and a reusable infrastructure example

rather than a complete thermodynamic exfoliation model.
