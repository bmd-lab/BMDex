# POSCAR Utilities

Small VASP structure-file utilities for everyday calculation setup and cleanup.

## `sort_poscar_by_species.py`

Sort a POSCAR or CONTCAR by species and write a VASP-compatible POSCAR.

```bash
python3 tools/structure/poscar/sort_poscar_by_species.py
```

This is useful after SQS generation, substitutions, or imported structure
workflows where species ordering needs to match a `POTCAR.spec`.
