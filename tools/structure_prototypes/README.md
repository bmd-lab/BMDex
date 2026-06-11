# Structure Prototype Tools

Practical utilities for working with the structure prototype dataset in:

```text
datasets/structure_prototypes/
```

These scripts are researcher-facing tools, not canonical dataset contents. They
can be run from the repository or copied and edited for a specific prototype
screening workflow.

## Runnable Scripts

### `abundance_rank.py`

Score a formula using the canonical element-abundance dataset.

```bash
python3 tools/structure_prototypes/abundance_rank.py
```

Default behavior:

- reads `datasets/element_abundances/earth-abundance.yaml`
- scores `SiO2`
- prints several abundance scoring methods

### `get_abundant_prototypes.py`

Compare CIF structures in one prototype directory and rank representative
frameworks using an abundance score.

This file is primarily imported by `generate_frameworks_list.py`, but can be
adapted for one-off framework comparison tasks.

### `generate_frameworks_list.py`

Regenerate `unique_structures.txt` summaries for a folder of prototype CIF
subdirectories.

```bash
python3 tools/structure_prototypes/generate_frameworks_list.py
```

Edit the user settings at the top of the script before running. The default
`MAIN_FOLDER` placeholder is intentionally not a production path because this
script writes `unique_structures.txt` files into each processed subdirectory.

## Related Dataset

The canonical prototype CIF collection is stored under:

```text
datasets/structure_prototypes/
```

Keep prototype data in `datasets/`. Keep reusable operations that act on those
data here under `tools/`.
