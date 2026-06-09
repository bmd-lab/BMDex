# VASP

This section contains private BMD Lab VASP assets: calculation standards, input
templates, runnable examples, and practical VASP utility scripts.

Some documents also describe infrastructure-facing execution details for
TAU PowerSLURM and licensed VASP pseudopotential access. Those details depend
on university-managed systems and should be treated as current operational
conventions rather than lab-controlled software behavior.

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

## Utilities

### `make_potcar_from_spec.py`

Generate a local `POTCAR` from a repository-safe `POTCAR.spec` file using the
configured pymatgen POTCAR directory.

```bash
python3 vasp/make_potcar_from_spec.py
```

### `create_mp_relax_inputs.py`

Fetch structures from Materials Project IDs and write pymatgen `MPRelaxSet`
input folders.

```bash
python3 vasp/create_mp_relax_inputs.py
```

By default this writes `POTCAR.spec` instead of an actual `POTCAR`.

## Examples

- `examples/si_bulk_relax/`: minimal runnable silicon bulk relaxation example

SLURM submission standards and reusable batch scripts live under `slurm/`.
