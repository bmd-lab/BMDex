# TAU PowerSLURM Operational Standards

This section records BMD Lab conventions for running computational materials
science workflows on TAU PowerSLURM systems.

BMDex is curated from a laptop or workstation checkout, then pulled onto the
cluster when tools or templates need to be executed. Do not assume Codex is
installed on the cluster.

BMDex keeps this section operational rather than pedagogical. It should answer:

- which cluster resources and modules are standard
- how VASP jobs are submitted and restarted
- how Python and pymatgen utilities are run
- which filesystem conventions preserve reproducibility
- which recurring failure modes have already been debugged

## Core Documents

- `cluster-profile.md`: partitions, accounts, modules, and filesystem paths
- `slurm-standards.md`: canonical SLURM submission conventions
- `vasp-execution.md`: CPU VASP execution and input expectations
- `gpu-vasp.md`: GPU VASP and MIG/full-GPU resource conventions
- `python-environments.md`: mamba and Python environment conventions
- `high-throughput.md`: batch submission, status checks, and restart policy
- `potcar-setup.md`: POTCAR policy and `PMG_VASP_PSP_DIR`
- `common_failures.md`: known operational failures and debugging checks

## Related Repository Objects

Templates:

- `hpc/templates/slurm/submit_vasp.sbatch`
- `hpc/templates/slurm/submit_vasp_gpu.sbatch`
- `hpc/templates/slurm/submit_python.sbatch`
- `hpc/templates/vasp/INCAR.relax`
- `hpc/templates/vasp/INCAR.static`
- `hpc/templates/vasp/KPOINTS.example`
- `hpc/templates/vasp/POTCAR.spec.example`

Operational tools:

- `tools/hpc/submit_many_vasp.py`
- `tools/hpc/vasp_status.py`
- `tools/hpc/restart_relaxations.py`
- `tools/hpc/check_power_environment.sh`

## Operating Principle

Cluster guidance should stay close to real group workflows. Prefer short,
direct standards and copyable scripts over hidden orchestration layers.

Run cluster-facing tools from a cluster-side BMDex checkout, or copy them into a
calculation folder when that is more convenient for the workflow.
