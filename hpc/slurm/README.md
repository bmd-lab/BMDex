# SLURM

This directory contains BMD Lab conventions for using TAU PowerSLURM and the
cluster-side templates researchers copy into calculation or workflow folders.

## Core Documents

- `cluster-profile.md`: partitions, accounts, modules, and filesystem paths
- `slurm-standards.md`: canonical SLURM submission conventions
- `python-environments.md`: mamba and Python environment conventions
- `high-throughput.md`: batch submission, status checks, and restart policy
- `common_failures.md`: known operational failures and debugging checks

## Templates

- `templates/submit_vasp.sbatch`
- `templates/submit_vasp_gpu.sbatch`
- `templates/submit_python.sbatch`

VASP-specific execution notes, input templates, and examples live under
`../vasp/`.
