# Structure Comparison Utilities

Small pymatgen-native scripts for checking structural equivalence and framework
similarity.

## `compare_frameworks.py`

Compare a reference structure against a candidate structure:

```bash
python3 tools/structure/comparison/compare_frameworks.py
```

This is useful after structure generation, SQS construction, primitive-cell
reduction, or relaxation restarts.
