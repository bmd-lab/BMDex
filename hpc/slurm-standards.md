# SLURM Standards

This document defines the BMD Lab conventions for SLURM scripts used by BMDex
workflows.

## Job Directory Assumptions

A VASP calculation directory should contain:

- `INCAR`
- `POSCAR`
- `KPOINTS`
- `POTCAR.spec`
- a local submission script such as `submit.sbatch`

The generated `POTCAR` file is expected to exist on the licensed cluster
filesystem when the job runs, but actual POTCAR files should not be committed to
BMDex.

## Required Script Conventions

SLURM scripts should:

- set partition and account explicitly
- set walltime, tasks, nodes, and memory explicitly
- run from `"$SLURM_SUBMIT_DIR"`
- set `ulimit -s 81920` for VASP workflows
- load modules inside the script
- write VASP output to a predictable file, currently `output`

Recommended boilerplate:

```bash
cd "$SLURM_SUBMIT_DIR"
ulimit -s 81920
```

## Standard Queue Commands

```bash
squeue -u "$USER"
scontrol show job <JOBID>
scancel <JOBID>
```

Batch-submission utilities should use `squeue -u "$USER"` rather than grepping
for a hardcoded username.

## Submission Template Policy

Templates belong in:

```text
hpc/templates/slurm/
```

Runnable batch utilities belong in:

```text
tools/hpc/
```

The template should stay simple enough to copy into a calculation folder.
Workflow-specific automation should live in a tool script rather than inside a
large SLURM file.
