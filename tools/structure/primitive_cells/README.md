# Primitive-Cell Utilities

Practical scripts for reducing VASP structures to primitive cells.

These utilities are intended to be copied into calculation folders or run from
the repository with simple path edits in the user-settings block.

## Primary Script

```bash
python3 tools/structure/primitive_cells/make_primitive_cell.py
```

Default behavior:

- reads `CONTCAR`
- uses pymatgen symmetry analysis to generate a primitive standard structure
- writes `POSCAR_primitive.vasp`

Edit the user settings at the top of the script for different input files,
output names, or symmetry tolerances.
