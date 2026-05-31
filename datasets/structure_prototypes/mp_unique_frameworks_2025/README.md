# Materials Project Unique Structure Prototypes 2025

Canonical metadata:

- `bmdex.yaml`

This dataset contains a Materials Project-derived collection of structure
prototype CIFs grouped by anonymous stoichiometry labels. Each group contains
the associated CIF files and a generated `unique_structures.txt` summary.

The source material was developed for the master's thesis:

- *The Unique Structure Prototypes of All Materials*, Tel Aviv University, 2025

## Included Files

- `sorted-structures/` stoichiometry-grouped CIF files and prototype summaries
- `all-prototypes-unfiltered.txt` unfiltered prototype summary
- `SOURCE_README.md` README preserved from the source repository
- `scripts/` provenance scripts from the source workflow
- `bmdex.yaml` structured BMDex metadata

## Repository Role

This is now a canonical BMDex dataset. Reusable code for loading, filtering, or
matching prototypes should live under `tools/` and reference this dataset by
metadata ID.

## Important Limitations

The dataset is derived from Materials Project structures and inherits the
assumptions, coverage limits, and redistribution considerations of the source
data. License and redistribution terms should be documented explicitly before
broader reuse outside the private lab repository.
