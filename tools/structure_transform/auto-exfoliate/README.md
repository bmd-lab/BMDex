# Auto-Exfoliate

Canonical metadata:

- `bmdex.yaml`

Auto-Exfoliate is a workflow for automated structure screening, slab
generation, and layered-material exfoliation analysis within computational
materials science workflows.

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

Auto-Exfoliate combines:
- crystallographic analysis
- structure manipulation
- and automated workflow logic
to facilitate large-scale screening studies.

## Repository Role

Within BMDex, Auto-Exfoliate serves as:
- structure-focused screening workflow tooling
- a bridge between crystallographic analysis and VASP workflows
- an example of reusable workflow orchestration built on shared BMDex primitives

Auto-Exfoliate now lives under the structure-transform tool category:

```text
tools/structure_transform/auto-exfoliate/
```

and builds on reusable structure primitives including:
- slab generation
- supercell construction
- vacuum manipulation
- orientation utilities

## Dependencies

Typical dependencies include:
- pymatgen
- numpy

## Notes

Auto-Exfoliate should be interpreted as:
- a practical workflow framework
- a screening methodology
- and a reusable infrastructure example

rather than a complete thermodynamic exfoliation model.
