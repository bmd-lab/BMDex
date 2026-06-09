# SLURM

This directory records private infrastructure knowledge for using TAU
PowerSLURM, a university-managed HPC system that the BMD Lab depends on but
does not control.

It contains current BMD Lab conventions, cluster-side templates researchers
copy into calculation folders, and practical operational scripts for batch VASP
workflows. Cluster policies, modules, accounts, partitions, and filesystem
paths can change outside this repository and should be rechecked periodically.

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

## Operational Utilities

### `submit_many_vasp.py`

Submit many VASP calculation directories with a configurable queue limit.

```bash
python3 slurm/submit_many_vasp.py --root screening-root
python3 slurm/submit_many_vasp.py --root screening-root --submit
```

### `vasp_status.py`

Scan VASP calculation directories and report operational status.

```bash
python3 slurm/vasp_status.py --root screening-root
```

### `restart_relaxations.py`

Prepare controlled relaxation restarts by backing up `POSCAR` and copying
`CONTCAR` to `POSCAR`.

```bash
python3 slurm/restart_relaxations.py --root screening-root
python3 slurm/restart_relaxations.py --root screening-root --apply
```

### `check_power_environment.sh`

Check common TAU PowerSLURM environment assumptions.

```bash
bash slurm/check_power_environment.sh
```

VASP-specific execution notes, input templates, and examples live under
`../vasp/`.
