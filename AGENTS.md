# BMDex Agent Instructions

BMDex is the private computational operations and assets repository of the BMD
Lab.

BMDex's canonical ecosystem role is BMD-curated supporting scientific data,
reference evidence, and non-core scientific tools outside the BMD Compute VASP
data-generation pipeline.

If a capability determines how BMD generates a VASP calculation, its
authoritative implementation belongs in BMD Compute. If it provides supporting
scientific data or tooling but is not part of the core VASP data-generation
pipeline, it belongs in BMDex. BMD Agent consumes and coordinates these
capabilities without duplicating their authority.

BMDex complements the public `tutorials` repository:
- `tutorials` focuses on public educational knowledge, onboarding material, and
  conceptual guidance
- BMDex focuses on private infrastructure notes and lab-controlled computational
  assets

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
- HPC workflow support and operational standardization
- private infrastructure documentation
- reusable computational assets

## Repository Philosophy

BMDex is intended to function as:
- a private infrastructure reference for externally managed HPC systems
- a curated home for lab-controlled computational assets
- and a long-term operational memory system for the research group

## Research-Group Information Model

BMD Lab computational information has three broad classes:
- knowledge: public-facing concepts, explanations, tutorials, and onboarding
  material. This should primarily live in the public `tutorials` repository and
  group tutorial pages.
- infrastructure: private operational information about university-managed
  systems such as SLURM, cluster accounts, modules, partitions, filesystems, and
  VASP execution environments. BMDex may document current practice, but the BMD
  Lab does not control the underlying infrastructure.
- assets: private lab-controlled tools, codes, scripts, datasets, templates,
  examples, reference evidence, non-core workflow aids, and supporting
  standards. These are the parts BMDex owns, adapts, and maintains.

Do not blur these boundaries. Move broadly teachable material toward public
tutorials, record infrastructure assumptions with explicit limitations, and keep
assets practical, runnable, and easy for students to adapt.

Priorities:
1. scientific correctness
2. reproducibility
3. maintainability
4. supporting workflow evidence and reuse
5. onboarding efficiency
6. institutional knowledge preservation

## Organizational Principles

Prefer:
- reusable primitives over workflow duplication
- concise README provenance and structured data over duplicated prose
- validated reference examples over undocumented experimentation
- maintainable assets and infrastructure notes over excessive abstraction

Distinguish clearly between:
- reusable tools and primitives
- higher-level supporting scientific workflows
- validated operational examples
- lower-maturity but curated content documented with clear limitations

## Metadata Guidance

Metadata should support maintainers underneath the user experience. Do not make
metadata, schemas, or repository mechanics the first thing students encounter.

Do not add BMDex metadata sidecars such as `bmdex.yaml` or
`*.bmdex.yaml` unless explicitly asked. Preserve useful curation information in
the place students and maintainers will naturally read:
- human-facing provenance, validation state, limitations, and usage notes belong
  in the nearest relevant `README.md`
- agent-facing repository policy, information-model guidance, and curation
  conventions belong in `AGENTS.md`
- scientific YAML files are acceptable when the YAML is the dataset itself, such
  as element abundance or element-charge tables

Do not recreate top-level `metadata/`, `methods/`, `hpc/`, `examples/`,
`templates/`, `CONTRIBUTING.md`, `TOOLS.md`, or `repository*` governance
structures unless explicitly asked. Human-facing repository guidance belongs in
`README.md`; agent-facing guidance belongs in `AGENTS.md`.

## Contribution Guidance

When integrating contributions:
- preserve validated reference evidence
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
- reference evidence for validated workflows
- templates
- private operational guidance for externally managed infrastructure
- troubleshooting knowledge
- supporting computational standards outside the core BMD Compute VASP generation pipeline
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
