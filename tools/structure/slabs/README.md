# Slab Utilities

Practical slab-generation utilities for computational materials workflows.

These tools are intended to be directly useful in VASP calculation folders.
They can be run from the repository or copied into a working directory and
edited in place.

## Primary Script

```bash
python3 tools/structure/slabs/generate_slabs.py
```

Default behavior:

- reads `CONTCAR`
- generates slabs up to Miller index 2
- adds 15 Angstrom vacuum
- writes slab POSCAR files under `generated_slabs/`
- keeps multiple terminations for the same Miller index without overwriting files

Edit the user settings at the top of the script to change the input file,
Miller-index limit, slab thickness, vacuum thickness, centering behavior, or
oxidation states.

The utilities are intended to support:
- surface generation
- layered-material workflows
- exfoliation studies
- VASP slab preparation
- automated structure screening

## Design Philosophy

These utilities should remain:
- runnable by students
- easy to copy into calculation folders
- pymatgen-native
- clean, lightweight, and hackable

Higher-level workflows such as MSS-Auto build upon these reusable tools.

## Typical Features

- slab construction
- vacuum insertion
- orientation handling
- structure export
- VASP compatibility

## Dependencies

Typical dependencies include:
- pymatgen
- numpy
