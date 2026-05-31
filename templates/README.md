# Templates

Reusable starting points for calculations and job submission.

Templates should preserve stable operational conventions while remaining easy
to inspect and adapt. Scientific validation state belongs in metadata sidecars
or in workflows and examples that use the templates.

## SLURM Templates

Current TAU PowerSLURM starting points live under `templates/slurm/`:

- `submit_vasp.sbatch`: standard CPU VASP job
- `submit_vasp_gpu.sbatch`: GPU VASP job
- `submit_python.sbatch`: simple Python or pymatgen utility job

Cluster-specific standards are documented in `hpc/tau-powerslurm/`.
