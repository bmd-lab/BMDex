# Cluster

Publicly shareable operational guidance for TAU PowerSLURM. The university
controls the cluster; BMDex records the current lab working defaults and
copyable files.

These scripts and notes are supporting/manual operational assets. They do not
define BMD Compute runtime behavior unless BMD Compute explicitly consumes
them; BMD Compute owns its deployed submission and execution policy for the
core VASP data-generation pipeline.

## Bash Scripts

Copy these into calculation or workflow folders and edit job names, resources,
modules, and environment activation as needed:

- `submit_vasp.sh`: CPU VASP
- `submit_vasp_gpu.sh`: GPU VASP
- `submit_python.sh`: scheduled Python utilities

These files are Bash scripts. Submit the job scripts with `sbatch`, for
example:

```bash
sbatch submit_vasp.sh
```

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
bash cluster/submit_many_vasp.sh --root screening-root
bash cluster/submit_many_vasp.sh --root screening-root --submit
```

Scan VASP calculation status:

```bash
bash cluster/vasp_status.sh --root screening-root
```

Prepare controlled relaxation restarts:

```bash
bash cluster/restart_relaxations.sh --root screening-root
bash cluster/restart_relaxations.sh --root screening-root --apply
```

Check the current cluster-side environment:

```bash
bash cluster/check_power_environment.sh
```

## Operating Rules

- Keep SLURM files in this directory as Bash scripts with `.sh` names.
- Run from `"$SLURM_SUBMIT_DIR"` inside job scripts.
- Load required modules inside each submitted script.
- Use `squeue -u "$USER"` for queue checks.
- Keep `POTCAR.spec` in BMDex and generate licensed `POTCAR` files only in a
  licensed VASP environment.
- Treat resource requests as starting points, not convergence validation.
- Recheck this directory when accounts, partitions, modules, filesystem paths,
  or university cluster policy changes.

## Script Maturity

- `submit_vasp.sh` is the standard CPU VASP starting script.
- `submit_vasp_gpu.sh` is the current GPU VASP starting script and may need
  revalidation when GPU modules or resource names change.
- `submit_python.sh` is a lightweight starting point for scheduled Python or
  pymatgen jobs and must be edited for each user's environment.
- Operational utilities provide queue management and restart triage; they do
  not replace scientific convergence review.

VASP-specific execution notes, input templates, and examples live under
`../vasp/`.
