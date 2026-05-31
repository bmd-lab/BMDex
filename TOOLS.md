# BMDex Tools Overview

This document summarizes reusable computational tools available within BMDex.

## Structure Utilities

Location:
```text
tools/structure/
```

Includes:
- slab generation
- supercell construction
- primitive-cell generation
- POSCAR cleanup and species sorting
- framework comparison
- orientation handling
- vacuum manipulation
- MSS-Auto layered-material structure screening

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

MSS-Auto location:
```text
tools/structure/mss_auto/
```

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
hpc/tau-powerslurm/
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
hpc/tau-powerslurm/potcar-setup.md
```
