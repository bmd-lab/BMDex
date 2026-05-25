# Electroneutrality Matching Tools

This module contains utilities for generating chemically charge-balanced compositions from combinations of oxidation states.

The original motivation was to support:
- compositional screening
- candidate compound generation
- oxidation-state enumeration
- chemically plausible formula generation

The workflow is based on matching combinations of positive and negative oxidation states that sum to zero.

## Origins

This module derives from the earlier:
- `electroneutral_match`
repository developed within the BMD Lab.

The original implementation explored combinations of oxidation states associated with known elements and identified electroneutral compositions.

## Purpose in BMDex

Within BMDex, this module is intended to become:
- a reusable compositional reasoning utility
- a bridge between oxidation-state logic and pymatgen workflows
- a standardized internal tool for chemically plausible composition generation

## Planned Future Directions

Potential future integration includes:
- pymatgen Composition objects
- oxidation-state decorators
- prototype structure generation
- automated compositional filtering
- integration with structure prediction workflows

## Validation Philosophy

Generated compositions should not automatically be treated as chemically realizable materials.

Electroneutrality is a necessary but insufficient condition for stability or synthesizability.

Further:
- structural
- thermodynamic
- and electronic
validation may be required.

## Repository Organization

- `oxidation_states/`
    curated oxidation-state datasets
- `examples/`
    example composition generation workflows
- `validation/`
    sanity checks and tests
