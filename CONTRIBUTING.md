# Contributing to BMDex

BMDex is the shared computational knowledge base of the BMD Lab.

The goal of this repository is to preserve and standardize computational knowledge across the group while maintaining scientific rigor, reproducibility, and maintainability.

## What Belongs in BMDex

Examples of useful contributions include:
- reproducible computational workflows
- reusable VASP input templates
- pymatgen utilities and transformations
- HPC workflow guidance
- convergence-testing procedures
- onboarding documentation
- troubleshooting notes
- reusable analysis scripts
- examples with clear scientific purpose

## Contribution Principles

Contributions should prioritize:
- scientific correctness
- reproducibility
- clarity
- maintainability
- reusability
- transparency of assumptions

When possible:
- document why a workflow or parameter choice is used
- include validation information
- prefer reusable methods over one-off scripts
- keep examples minimal and executable

## Status and Maturity

Content should be added to BMDex only when it is useful enough to curate in a
canonical location. Scratch work, temporary notebooks, and speculative
experiments should remain outside the repository until they are ready to become
maintained lab knowledge.

Lower-maturity but useful content may still be recorded with an appropriate
metadata status and explicit limitations.

Production-ready workflows should:
- contain sufficient documentation
- include expected inputs and outputs
- describe known limitations or failure modes
- avoid undocumented dependencies

Do not create top-level lifecycle buckets such as `incoming/`, `experimental/`,
`validated/`, or `deprecated/`. Place content in its canonical section
(`tools/`, `examples/`, `datasets/`, `methods/`, and so on) and record status
in local metadata and documentation.

## Documentation Expectations

Contributions should aim to document:
- scientific purpose
- assumptions
- required software/tools
- expected outputs
- validation procedure
- computational cost considerations when relevant

## Metadata Expectations

Canonical repository objects should include metadata sidecars. Directory-backed
objects use `bmdex.yaml`; single-file objects may use `<filename>.bmdex.yaml`.

Sidecars should follow `schemas/bmdex.schema.yaml` and record:
- stable object ID
- object type
- lifecycle status
- validation level
- provenance or origin when relevant
- validation evidence
- known limitations
- maintainers

Before review, run:

```bash
python3 tools/metadata/validate_bmdex_metadata.py
```

## Repository Philosophy

BMDex is intended to function as long-term institutional memory for the lab.

The repository should favor:
- durable workflows over temporary hacks
- explicit assumptions over implicit knowledge
- reusable structure over fragmented notes
- clear examples over excessive abstraction

## Getting Started

New contributors are encouraged to:
- improve documentation
- add examples
- clarify existing workflows
- propose reusable templates and utilities

Incomplete or speculative work should be kept outside BMDex until it is ready
to be curated in a canonical section.
