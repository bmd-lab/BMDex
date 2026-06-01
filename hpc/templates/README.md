# HPC Templates

Reusable starting points for TAU PowerSLURM jobs and VASP calculations.

Templates should preserve stable operational conventions while remaining easy
to inspect and adapt. Scientific validation state belongs in metadata sidecars
or in workflows and examples that use the templates.

## SLURM Templates

Current TAU PowerSLURM starting points live under `hpc/templates/slurm/`:

- `submit_vasp.sbatch`: standard CPU VASP job
- `submit_vasp_gpu.sbatch`: GPU VASP job
- `submit_python.sbatch`: simple Python or pymatgen utility job

Cluster-specific standards are documented in `hpc/`.

## VASP Input Templates

Current VASP starting points live under `hpc/templates/vasp/`:

- `INCAR.relax`: conservative structural relaxation settings
- `INCAR.static`: conservative static calculation settings
- `KPOINTS.example`: example Monkhorst-Pack mesh
- `POTCAR.spec.example`: repository-safe pseudopotential specification
