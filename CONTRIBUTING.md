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

New student contributors are not expected to understand the metadata system
immediately. A useful script, template, example, or operational note can be
reviewed first; maintainers can help add or repair metadata during curation.

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

For student contributors, a good first contribution is usually a practical
workflow artifact:

- a working script used in a real calculation folder
- a corrected SLURM template
- a documented failure mode and fix
- a small VASP or pymatgen example that others can rerun

Do not start by designing metadata, package structure, or broad abstractions
unless the workflow need is already clear.

## Access and Execution Model

BMDex contributions are usually curated from a laptop or workstation checkout.
Cluster execution should happen from a normal git checkout on the cluster after
changes have been pushed and pulled.

Do not require Codex on the cluster for ordinary tool usage. Tools and templates
should remain usable by students who only have Git, SSH, and the scientific
software stack available on the cluster.
