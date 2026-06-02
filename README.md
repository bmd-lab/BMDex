# BMDex

Curated computational methods, tools, workflows, and standards for the BMD Lab.

BMDex serves as the lab's shared computational knowledge base and institutional memory for reproducible computational materials science research.

BMDex complements the public `tutorials` repository:

* `tutorials` focuses on education, onboarding, and introducing concepts
* BMDex focuses on reusable tools, operational workflows, computational standards, and long-term institutional knowledge

## Philosophy

BMDex is designed for materials scientists first.

Most users should be able to:

* find a useful tool quickly
* run or adapt it with minimal setup
* understand examples without deep Git or software-engineering knowledge

The repository prioritizes:

1. scientific correctness
2. reproducibility
3. maintainability
4. workflow standardization
5. onboarding efficiency
6. institutional knowledge preservation

## Repository Layout

### `tools/`

Reusable computational utilities and transformations.

Examples include:

* structure transformations
* composition generation and screening
* VASP workflow utilities
* HPC helper scripts

### `datasets/`

Curated scientific resources used by tools and workflows.

Examples include:

* oxidation-state datasets
* structure prototype datasets
* element abundance datasets

### `slurm/`

Cluster-specific operational knowledge, troubleshooting guidance, and SLURM
submission templates for the group HPC system.

### `vasp/`

Lab-wide VASP standards, cluster execution guidance, input templates, and
runnable VASP examples.

Examples include:

* input standards
* pseudopotential conventions
* convergence and documentation expectations
* VASP execution guidance
* input templates and runnable examples

### `metadata/`

Maintainer-facing metadata validation utilities and the lightweight sidecar
contract used to keep curated objects consistent.

Repository access and curation guidance is summarized there for maintainers
without creating a separate governance tree.

## Typical Tasks

Generate surface slabs:

```bash
python3 tools/structure_transform/generate_all_slabs.py
```

Build a supercell:

```bash
python3 tools/structure_transform/make_supercell.py
```

Create a primitive cell:

```bash
python3 tools/structure_transform/make_primitive.py
```

Generate electroneutral compositions:

```bash
python3 tools/composition/generate_ternaries.py
```

## Topic Areas

BMDex currently focuses on:

* VASP-based density functional theory (DFT)
* atomic structure workflows and structure manipulation
* chemical formula and composition screening
* structure prototype analysis
* HPC workflow standardization
* reusable computational infrastructure

## Contribution Philosophy

BMDex should prioritize:

* useful tools
* reusable workflows
* curated datasets
* practical examples
* operational guidance
* scientific provenance

BMDex should avoid becoming:

* a dump of active project files
* a collection of temporary notebooks
* a storage location for large calculation outputs
* a purely pedagogical tutorial repository

The goal is to preserve and share the computational knowledge that repeatedly proves useful across the BMD Lab.
