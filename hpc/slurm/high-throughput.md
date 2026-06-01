# High-Throughput VASP Operations

This document records practical BMD Lab conventions for managing many VASP
calculation directories on TAU PowerSLURM.

## Directory Model

High-throughput VASP utilities should assume a filesystem-oriented layout:

```text
screening-root/
  material_001/
    INCAR
    POSCAR
    KPOINTS
    POTCAR.spec
    submit.sbatch
  material_002/
    ...
```

This layout is easy for students to inspect, copy, restart, and debug.

## Queue Throttling

Batch submission should:

- count only the current user's jobs with `squeue -u "$USER"`
- use a configurable maximum queue count
- support dry-run mode
- skip completed calculations
- skip directories missing required inputs

Use:

```bash
python3 tools/hpc/submit_many_vasp.py --root screening-root --submit
```

after checking the dry-run output.

## Status Checks

Before resubmitting a directory, inspect:

- `OUTCAR`
- `OSZICAR`
- `INCAR`
- `CONTCAR`

Use:

```bash
python3 tools/hpc/vasp_status.py --root screening-root
```

for a first-pass scan.

## Restart Policy

Relaxation restarts should:

- require a non-empty `CONTCAR`
- back up the existing `POSCAR`
- copy `CONTCAR` to `POSCAR`
- optionally resubmit only after a dry run has been checked

Use:

```bash
python3 tools/hpc/restart_relaxations.py --root screening-root --apply
```

and add `--resubmit` only when the submission target has been verified.

## Scientific Review

Batch utilities can identify operational states. They do not replace scientific
review of convergence, structure quality, magnetism, smearing, or final energy
trends.
