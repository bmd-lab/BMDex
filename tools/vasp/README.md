# VASP Tools

Practical utilities for preparing and maintaining VASP calculation inputs.

These scripts are meant to be simple enough to copy into a calculation or
screening folder and edit directly.

## Tools

### `make_potcar_from_spec.py`

Generate a local `POTCAR` from a repository-safe `POTCAR.spec` file using the
configured pymatgen POTCAR directory.

```bash
python3 tools/vasp/make_potcar_from_spec.py
```

### `create_mp_relax_inputs.py`

Fetch structures from Materials Project IDs and write pymatgen `MPRelaxSet`
input folders.

```bash
python3 tools/vasp/create_mp_relax_inputs.py
```

By default this writes `POTCAR.spec` instead of an actual `POTCAR`.

## Related Standards

- `vasp/input-standards.md`
- `vasp/potcar-setup.md`
