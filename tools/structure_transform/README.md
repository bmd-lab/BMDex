# Structure Transform Tools

Practical pymatgen-native utilities for transforming, cleaning, and comparing
crystal structures.

These scripts are intended to be directly useful in VASP calculation folders.
They can be run from the repository or copied into a working directory and
edited in place.

## Runnable Scripts

### `generate_all_slabs.py`

Generate VASP-compatible slab POSCAR files from `CONTCAR` or `POSCAR`.

```bash
python3 tools/structure_transform/generate_all_slabs.py
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

### `auto_exfoliate.py`

Generate an exfoliated slab by searching for an open cleavage region and
inserting vacuum along a selected lattice direction.

```bash
python3 tools/structure_transform/auto_exfoliate.py
```

Default behavior:

- reads `CONTCAR`
- builds a directional supercell if the cell is too short
- searches candidate cleavage positions with a probe grid
- inserts 15 Angstrom vacuum along the cleavage direction
- writes `POSCAR_auto_exfoliated.vasp`

Edit the user settings at the top of the script to change the input file,
cleavage direction, minimum cell length, vacuum size, probe grid, or output
filename.

### `make_supercell.py`

Build a supercell from `CONTCAR` or `POSCAR`.

```bash
python3 tools/structure_transform/make_supercell.py
```

Default behavior:

- reads `CONTCAR`
- builds a `2 x 2 x 2` supercell
- writes `POSCAR_supercell.vasp`

### `make_primitive.py`

Reduce a VASP structure to a primitive cell.

```bash
python3 tools/structure_transform/make_primitive.py
```

Default behavior:

- reads `CONTCAR`
- uses pymatgen symmetry analysis to generate a primitive standard structure
- writes `POSCAR_primitive.vasp`

### `sort_poscar_by_species.py`

Sort a POSCAR or CONTCAR by species and write a VASP-compatible POSCAR.

```bash
python3 tools/structure_transform/sort_poscar_by_species.py
```

This is useful after SQS generation, substitutions, or imported structure
workflows where species ordering needs to match a `POTCAR.spec`.

### `compare_frameworks.py`

Compare a reference structure against a candidate structure.

```bash
python3 tools/structure_transform/compare_frameworks.py
```

This is useful after structure generation, SQS construction, primitive-cell
reduction, or relaxation restarts.

## Helper Modules

The directory also contains small helper modules used by examples and workflow
bundles:

- `slab_generator.py`
- `supercell_builder.py`
- `orientation_utils.py`

These helpers may be imported by other scripts, but the primary researcher
interface should remain the runnable scripts above.

## Design Philosophy

Structure transform tools should remain:

- runnable by students
- easy to copy into calculation folders
- pymatgen-native
- clean, lightweight, and hackable
- organized around researcher tasks rather than ontology labels

Structure prototype datasets live under:

```text
datasets/structure_prototypes/
```

Only reusable operations acting on those datasets should live under `tools/`.
