# BMDex Agent Instructions

BMDex is the private computational knowledge repository of the BMD Lab.

BMDex complements the public `tutorials` repository:
- `tutorials` focuses on educational and onboarding material
- BMDex focuses on operational workflows, reusable tools, computational standards, and institutional knowledge

Intended access model:
- public tutorials introduce concepts and basic workflows
- the private GitHub repository or website is the first curated BMDex entry point
- cluster execution uses a normal git checkout or pull of BMDex on the cluster
- Codex is used from a laptop or workstation checkout for curation, review, and extension

Do not assume Codex is installed on the cluster. Cluster-facing tools should be
directly runnable or copyable from a cluster-side BMDex checkout.

Student audience assumption:
- most students are materials scientists, not software engineers
- many have little or no initial experience with Git, Codex, metadata, schemas, or package design
- they are primarily learning Python, VASP, pymatgen, SLURM, and computational materials science
- student-facing workflows should expose concrete research actions before repository mechanics
- metadata and ontology should support maintainers underneath, not dominate the first user experience

Primary focus areas:
- VASP-based density functional theory (DFT)
- atomic structure workflows and structure manipulation
- chemical formula and composition screening
- reproducible computational materials science
- HPC workflow standardization
- reusable computational infrastructure

## Repository Philosophy

BMDex is intended to function as:
- a reusable computational infrastructure repository
- a curated methodological resource
- and a long-term institutional memory system

Priorities:
1. scientific correctness
2. reproducibility
3. maintainability
4. workflow standardization
5. onboarding efficiency
6. institutional knowledge preservation

## Organizational Principles

Prefer:
- reusable primitives over workflow duplication
- structured metadata over duplicated prose
- validated workflows over undocumented experimentation
- maintainable infrastructure over excessive abstraction

Distinguish clearly between:
- reusable tools and primitives
- higher-level scientific workflows
- validated operational examples
- lower-maturity but curated content recorded through metadata

## Contribution Guidance

When integrating contributions:
- preserve validated workflows
- document assumptions explicitly
- identify conflicting conventions
- avoid undocumented workflow changes
- favor interoperability and maintainability
- preserve scientific provenance where applicable

## Git Workflow

- Always create new feature branches from current `main`.
- Feature branches are temporary.
- After a feature branch is merged, delete it locally and remotely.
- Assume BMDex normally has only `main` and at most one active feature branch.

## Repository Boundaries

BMDex should prioritize:
- reusable tools
- validated workflows
- templates
- operational guidance
- troubleshooting knowledge
- computational standards
- curated scientific datasets

BMDex should avoid becoming:
- a dump of active project files
- a collection of temporary notebooks
- a storage location for large calculation outputs
- a purely pedagogical tutorial repository

## Newcomer Guidance

Newcomer-facing workflows should:
- minimize implicit knowledge
- contain executable examples
- prioritize clarity over abstraction
- distinguish validated workflows from lower-maturity workflows
- avoid requiring Git, Codex, or metadata knowledge for ordinary tool usage
