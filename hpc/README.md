# HPC

This section records BMD Lab conventions for running computational materials
science workflows on the group HPC system.

BMDex is curated from a laptop or workstation checkout, then pulled onto the
cluster when tools or templates need to be executed. Do not assume Codex is
installed on the cluster.

BMDex keeps this section operational rather than pedagogical. Content is split
by how researchers look for it:

- `slurm/`: cluster resources, SLURM submission conventions, Python
  environments, batch operation, common failures, and SLURM job templates
- `vasp/`: VASP execution guidance, GPU notes, POTCAR policy, VASP input
  templates, and runnable VASP examples

## Entry Points

- `slurm/README.md`
- `vasp/README.md`

## Related Repository Objects

SLURM templates:

- `hpc/slurm/templates/submit_vasp.sbatch`
- `hpc/slurm/templates/submit_vasp_gpu.sbatch`
- `hpc/slurm/templates/submit_python.sbatch`

VASP templates:

- `hpc/vasp/templates/INCAR.relax`
- `hpc/vasp/templates/INCAR.static`
- `hpc/vasp/templates/KPOINTS.example`
- `hpc/vasp/templates/POTCAR.spec.example`

Examples:

- `hpc/vasp/examples/si_bulk_relax`

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
