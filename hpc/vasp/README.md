# VASP on HPC

This directory contains BMD Lab VASP execution guidance for the group HPC
environment. It keeps runnable input templates and examples close to the
operational guidance students use when setting up calculations.

## Core Documents

- `vasp-execution.md`: CPU VASP execution and input expectations
- `gpu-vasp.md`: GPU VASP and MIG/full-GPU resource conventions
- `potcar-setup.md`: POTCAR policy and `PMG_VASP_PSP_DIR`

## Templates

- `templates/INCAR.relax`
- `templates/INCAR.static`
- `templates/KPOINTS.example`
- `templates/POTCAR.spec.example`

## Examples

- `examples/si_bulk_relax/`: minimal runnable silicon bulk relaxation example

SLURM submission standards and reusable batch scripts live under `../slurm/`.
