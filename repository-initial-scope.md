# Initial Scope and Purpose of BMDex

Date: 2026-05

## Motivation

BMDex was created to preserve and standardize computational knowledge within the BMD Lab.

The repository is intended to reduce loss of institutional knowledge caused by:
- student turnover
- undocumented workflows
- fragmented computational practices
- inconsistent file structures
- duplicated troubleshooting effort

The goal is not only to store files, but to curate reusable and reproducible computational methods.

## Initial Scope

The initial focus of BMDex is intentionally narrow and centered on the group’s most stable and widely used computational tools.

Primary focus areas:
- VASP-based density functional theory (DFT)
- atomic structure workflows and structure manipulation
- chemical formula and composition screening
- reproducible HPC workflows
- reusable templates and examples
- onboarding resources for new students

The repository is intended to contain:
- validated workflows
- reusable templates
- canonical examples
- troubleshooting guidance
- methodological notes
- reusable utilities

The repository is not intended to become:
- a dump of active project files
- a storage location for large calculation outputs
- a replacement for personal exploratory notebooks
- a substitute for scientific judgment

## Repository Philosophy

BMDex prioritizes:
1. scientific correctness
2. reproducibility
3. maintainability
4. transparency
5. onboarding efficiency
6. workflow standardization

The repository should favor:
- reusable workflows over one-off scripts
- explicit assumptions over implicit knowledge
- validated methods over speculative optimization
- clarity over unnecessary abstraction

## Role of Codex

Codex may be used by maintainers to:
- integrate contributions
- improve documentation
- standardize workflows
- identify inconsistencies
- curate reusable methods

Codex-generated contributions should remain reviewable and scientifically validated by group members.

## Historical Organizational Structure

The repository was initially organized around separate top-level buckets for
methods, templates, examples, tools, datasets, and repository governance
records.

That structure has since been simplified. BMDex now favors shallow
researcher-facing sections, with templates and examples kept near the workflows
that use them and metadata recording object type and maturity.

## Future Development

Potential future additions may include:
- automated validation tools
- workflow testing
- convergence benchmarking
- standardized analysis pipelines
- broader workflow automation

These are intentionally outside the initial scope in order to keep the repository focused and maintainable during early development.
