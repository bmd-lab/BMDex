# Electroneutrality Matching Tools

Runnable utilities for generating chemically charge-balanced candidate
compositions from oxidation-state assignments.

Canonical metadata:
- `bmdex.yaml`

Canonical dataset:
- `datasets/element_charges/`

Provenance:
- `ORIGIN.md`

Dependencies:
- Python
- PyYAML

## Scope

The tool logic matches combinations of positive and negative oxidation states
whose weighted sum is zero. Typical uses include composition generation,
candidate formula screening, and oxidation-state constrained enumeration.

Electroneutrality is a necessary but insufficient condition for chemical
realizability. Generated formulas still require structural, thermodynamic, and
electronic validation where relevant.

## Layout

- `generate_binary_oxides.py`: generate electroneutral binary oxide formulas.
- `generate_ternaries.py`: generate electroneutral ternary oxide formulas.
- `_datasets.py`: load the canonical oxidation-state dataset.

Run from the repository root:

```bash
python3 tools/composition/electroneutrality/generate_binary_oxides.py
python3 tools/composition/electroneutrality/generate_ternaries.py
```
