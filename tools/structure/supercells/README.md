# Supercell Utilities

Practical supercell-generation utilities for computational materials workflows.

These tools are intended to be directly useful in VASP calculation folders.
They can be run from the repository or copied into a working directory and
edited in place.

## Primary Script

```bash
python3 tools/structure/supercells/make_supercell.py
```

Default behavior:

- reads `CONTCAR`
- builds a `2 x 2 x 2` supercell
- writes `POSCAR_supercell.vasp`

Edit the user settings at the top of the script to change the input file,
scaling matrix, or output filename.

Typical use cases include:
- defect calculations
- phonon workflows
- surface generation
- convergence testing
- high-throughput structure generation

The utilities are intended as lightweight, hackable research scripts within
BMDex. Importable helper functions may exist when useful, but the researcher
entry point should remain a runnable script.
