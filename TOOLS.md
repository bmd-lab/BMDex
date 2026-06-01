# BMDex Tools Overview

This document summarizes reusable computational tools available within BMDex.

## Structure Transform Utilities

Location:
```text
tools/structure_transform/
```

Includes:
- `generate_all_slabs.py`
- `auto_exfoliate.py`
- `make_supercell.py`
- `make_primitive.py`
- `sort_poscar_by_species.py`
- `compare_frameworks.py`
- lightweight helper modules for slabs, supercells, and orientations

Related structure prototype datasets:
```text
datasets/structure_prototypes/
```

## Composition Utilities

Location:
```text
tools/composition/
```

Includes:
- formula generation
- electroneutral composition matching

Primary tool:
```text
tools/composition/electroneutrality/
```

Canonical dataset:
```text
datasets/oxidation_states/representative_84/
```

Associated publication:
- J. Phys. Chem. Lett. 2020

## HPC Utilities

Location:
```text
tools/hpc/
```

Includes:
- VASP batch submission with queue throttling
- VASP status scanning
- controlled relaxation restarts from `CONTCAR`
- TAU PowerSLURM environment checks

Canonical operational standards:
```text
hpc/slurm/
hpc/vasp/
```

## VASP Input Utilities

Location:
```text
tools/vasp/
```

Includes:
- local `POTCAR` generation from `POTCAR.spec`
- Materials Project relaxation input generation

Related standards:
```text
methods/vasp/input-standards.md
hpc/vasp/potcar-setup.md
```
