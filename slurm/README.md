# SLURM

Private infrastructure assets for TAU PowerSLURM. The university controls the
cluster; BMDex records the current lab working defaults and copyable files.

## Templates

Copy these into calculation or workflow folders and edit job names, resources,
modules, and environment activation as needed:

- `submit_vasp.sbatch`: CPU VASP
- `submit_vasp_gpu.sbatch`: GPU VASP
- `submit_python.sbatch`: scheduled Python utilities

Current defaults:

- CPU partition/account: `leeburton-pool` / `power-leeburton-users_v2`
- GPU partition/account: `gpu-leeburton-pool` / `power-leeburton-users_v2`
- CPU VASP modules: `intel/rocky8-oneAPI-2023`, `vasp/rocky8-intel-6.4.1`
- GPU VASP module: `vasp/vasp.6.5.1-hpc_sdk`
- POTCAR root: `/bmd-db/lee/potcars`
- Python env root: `/leeburton-data/$USER/envs/`

## Utilities

Submit many VASP calculation folders:

```bash
python3 slurm/submit_many_vasp.py --root screening-root
python3 slurm/submit_many_vasp.py --root screening-root --submit
```

Scan VASP calculation status:

```bash
python3 slurm/vasp_status.py --root screening-root
```

Prepare controlled relaxation restarts:

```bash
python3 slurm/restart_relaxations.py --root screening-root
python3 slurm/restart_relaxations.py --root screening-root --apply
```

Check the current cluster-side environment:

```bash
bash slurm/check_power_environment.sh
```

## Operating Rules

- Run from `"$SLURM_SUBMIT_DIR"` inside job scripts.
- Load required modules inside each submitted script.
- Use `squeue -u "$USER"` for queue checks.
- Keep `POTCAR.spec` in BMDex and generate licensed `POTCAR` files only in a
  licensed VASP environment.
- Treat resource requests as starting points, not convergence validation.
- Recheck this directory when accounts, partitions, modules, filesystem paths,
  or university cluster policy changes.

VASP-specific execution notes, input templates, and examples live under
`../vasp/`.
