# VASP

This section contains BMD Lab VASP calculation standards, execution guidance,
input templates, and runnable examples.

It is separate from `tools/vasp/`, which contains directly runnable VASP
utility scripts.

## Standards

- `input-standards.md`: lab-wide VASP input, pseudopotential, convergence, and
  documentation conventions
- `potcar-setup.md`: POTCAR policy and `PMG_VASP_PSP_DIR`

## Execution

- `vasp-execution.md`: CPU VASP execution and input expectations
- `gpu-vasp.md`: GPU VASP and MIG/full-GPU resource conventions

## Templates

- `templates/INCAR.relax`
- `templates/INCAR.static`
- `templates/KPOINTS.example`
- `templates/POTCAR.spec.example`

## Examples

- `examples/si_bulk_relax/`: minimal runnable silicon bulk relaxation example

SLURM submission standards and reusable batch scripts live under `../slurm/`.
