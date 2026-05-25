# POTCAR Setup and Policy

## Purpose

This document describes the BMD Lab conventions for VASP pseudopotential management.

The goal is to maintain:
- reproducibility
- functional consistency
- transparent provenance
- compatibility across workflows and users

Actual POTCAR files are not stored in BMDex.

Instead:
- `POTCAR.spec` files are committed
- local POTCAR generation is performed within the licensed computational environment

## Current Standard Functional

Current group standard:
- `PBE_64`

All workflows should document the pseudopotential functional explicitly.

Mixing pseudopotential families within a workflow should be avoided unless scientifically justified.

## Cluster POTCAR Location

Current TAU PowerSLURM convention:

```text
/bmd-db/lee/potcars
```

Expected symlink structure:

```text
POT_PAW_PBE_64 -> PBE_64
POT_GGA_PAW_PBE_64 -> PBE_64
```

These symlinks are maintained for compatibility with pymatgen and VASP workflows.

## Environment Variable

Users should define:

```bash
export PMG_VASP_PSP_DIR=/bmd-db/lee/potcars
```

This allows pymatgen and related workflows to locate pseudopotentials consistently.

## POTCAR.spec Convention

BMDex workflows use `POTCAR.spec` files instead of storing actual POTCAR data.

Example:

```text
Si
```

or:

```text
Mg
O
```

The order of entries must match the species ordering in `POSCAR`.

## POTCAR Generation

POTCAR files should be generated locally within the licensed environment.

Typical pymatgen-based workflows should automatically construct POTCARs using:
- the configured pseudopotential directory
- the documented functional
- the provided `POTCAR.spec`

## Validation Expectations

Validated workflows should:
- document pseudopotential functional explicitly
- avoid mixing incompatible pseudopotential families
- preserve reproducibility across users
- avoid undocumented POTCAR substitutions

## Repository Policy

Actual POTCAR files should not be committed to BMDex.

Reasons include:
- licensing considerations
- portability
- provenance clarity
- repository maintainability
- prevention of silent pseudopotential drift

Only:
- specifications
- policies
- setup conventions
- generation workflows
should be stored in the repository.
