# SLURM Submission Template for VASP

## Purpose

This template provides a validated reference SLURM submission script for VASP calculations within the BMD Lab computational environment.

The template is intended to:
- standardize resource requests
- reduce onboarding friction
- preserve operational cluster knowledge
- provide reproducible execution behavior

## Resource Philosophy

Default resource requests are intentionally conservative.

Users should adjust:
- memory
- walltime
- task count
based on:
- system size
- calculation type
- convergence behavior

## Module Environment

The template assumes:
- Intel-based compilation environment
- cluster-provided VASP modules
- MPI execution through `mpirun`

Cluster-specific module names may evolve over time and should be validated periodically.

## Execution Model

```bash
mpirun -n $SLURM_NTASKS vasp_std > output
```

is currently used as the standard execution approach.

Alternative parallelization strategies should be documented explicitly when used.

## Notes

The submission script should remain:
- simple
- transparent
- maintainable

Workflow orchestration layers should not obscure the underlying execution behavior.
