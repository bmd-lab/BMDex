# TAU PowerSLURM Notes

## Standard Modules

Validated VASP workflows currently assume the cluster-provided Intel and VASP
module stack documented in the local submission templates and troubleshooting
notes. Module names should be rechecked when the cluster image changes.

## Recommended SLURM Defaults

Use conservative defaults from `templates/slurm/submit_vasp.sbatch` as the
starting point for onboarding and reference calculations.

## VASP Execution

BMDex examples use `mpirun` with `vasp_std` unless a workflow documents a
different execution model.

## Filesystem Conventions

Pseudopotential lookup is standardized through `PMG_VASP_PSP_DIR` and the
local POTCAR policy in `potcar-setup.md`.

## Common Failure Modes

See `common_failures.md`.

## Debugging Tips

Start from a minimal reproducible calculation, inspect SLURM output, verify the
module environment, confirm POTCAR setup, and then check VASP convergence.

## Known Cluster Behaviors

Cluster-specific behavior should be recorded here only after it has been
observed by the group and is useful for future reproducibility or onboarding.
