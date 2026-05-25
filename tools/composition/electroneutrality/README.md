# Electroneutrality Matching Tools

Reusable utilities and examples for generating chemically charge-balanced
candidate compositions from oxidation-state assignments.

Canonical metadata:
- `bmdex.yaml`

Canonical dataset:
- `datasets/oxidation_states/representative_84/`

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

- `examples/`: lightweight executable examples.
- `oxidation_states/`: compatibility pointer to canonical datasets.
