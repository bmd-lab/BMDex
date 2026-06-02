# Python Environment Standards

This document records current BMD Lab conventions for Python and pymatgen
workflows on TAU PowerSLURM.

## Mamba Module

Tutorial-era workflows use:

```bash
module load mamba > /dev/null
```

New BMDex scripts should load mamba explicitly inside SLURM scripts when an
environment is required. Do not assume an interactive shell has already loaded
the environment.

## Environment Location

Current canonical environment root:

```text
/leeburton-data/$USER/envs/
```

Example:

```bash
mamba create --prefix /leeburton-data/$USER/envs/pymatgen-env python=3.10
mamba activate /leeburton-data/$USER/envs/pymatgen-env
```

Some historical tutorials mention `/bmd/<username>/envs/`. Treat that as a
legacy path unless a specific existing workflow depends on it.

## Common Packages

Common computational materials workflows often require:

- `pymatgen`
- `ase`
- `spglib`
- `numpy`
- `scipy`

Workflow-specific tools such as ATAT, atomate2, jobflow, USPEX, and XtalOpt
should document their own environment requirements locally.

## Submission Template

Use:

```text
slurm/templates/submit_python.sbatch
```

for simple Python utilities that need scheduled cluster execution.
