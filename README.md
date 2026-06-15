# BMDex

Curated computational methods, tools, workflows, and operational standards for
the BMD Lab.

BMDex serves as the lab's private operational memory for reproducible
computational materials science research.

BMDex complements the public `tutorials` repository:

* `tutorials` preserves public-facing knowledge, education, onboarding, and
  conceptual guidance
* BMDex preserves private infrastructure notes and lab-controlled computational
  assets used in day-to-day research

## Philosophy

BMDex is designed for materials scientists working in a research group.

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

## Information Model

BMD Lab computational information falls into three practical categories:

* **Knowledge**: public-facing concepts, explanations, tutorials, and onboarding
  material. This primarily belongs in the open `tutorials` repository and group
  tutorial pages. BMDex may point to it, but should not become the main home for
  broadly teachable material.
* **Infrastructure**: private operational information about university-managed
  systems, especially SLURM and HPC conventions. BMDex records the current
  working reality, but the lab does not control the underlying cluster policies,
  modules, accounts, partitions, or filesystem layout.
* **Assets**: private lab-controlled tools, codes, scripts, datasets, templates,
  examples, and workflows. These are the parts of BMDex the group owns,
  maintains, adapts, and reuses.

This distinction should guide curation. Public knowledge should graduate toward
`tutorials`; externally controlled infrastructure should be documented with
clear limitations; lab assets should remain practical, runnable, and reusable.

## Repository Layout

### `tools/`

Private lab-controlled computational assets: reusable utilities and
transformations.

Examples include:

* structure transformations
* composition generation and screening
* structure prototype analysis utilities

### `datasets/`

Private lab-controlled or lab-curated scientific assets used by tools and
workflows.

Examples include:

* element-charge datasets
* structure prototype datasets
* element abundance datasets

### `slurm/`

Private infrastructure notes for university-managed HPC: cluster-specific
operational guidance, troubleshooting notes, SLURM submission templates, and
batch workflow utilities for the group HPC system.

### `vasp/`

Private lab-controlled VASP assets and standards, plus infrastructure-facing
execution guidance for running those assets on the group HPC system.

Examples include:

* input standards
* pseudopotential conventions
* convergence and documentation expectations
* VASP execution guidance
* VASP utility scripts
* input templates and runnable examples

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
python3 tools/composition/electroneutrality/generate_ternaries.py
```

Score a composition by element abundance:

```bash
python3 tools/structure_prototypes/abundance_rank.py
```

Submit or inspect many VASP calculation folders:

```bash
bash slurm/submit_many_vasp.sh --root screening-root
bash slurm/vasp_status.sh --root screening-root
```

Generate VASP input helpers:

```bash
python3 vasp/make_potcar_from_spec.py
python3 vasp/create_mp_relax_inputs.py
```

## Topic Areas

BMDex currently focuses on:

* VASP-based density functional theory (DFT)
* atomic structure workflows and structure manipulation
* chemical formula and composition screening
* structure prototype analysis
* HPC workflow standardization
* private infrastructure documentation
* reusable computational assets

## Curation And Metadata

BMDex is the private operational layer behind the public tutorials repository.
Tutorials introduce concepts; BMDex preserves reusable tools, standards,
templates, datasets, examples, and institutional workflow knowledge.

Curated content should expose the useful researcher action first. Most students
are materials scientists, so ordinary tool usage should not require knowledge
of metadata, Codex, schemas, or repository governance.

Canonical repository objects may include lightweight YAML sidecars:

* directory-backed objects use `bmdex.yaml`
* single-file objects may use `<filename>.bmdex.yaml`

Sidecars should record:

* stable object ID
* object type
* information class
* visibility
* stewardship
* lifecycle status
* validation level
* provenance or origin when relevant
* validation evidence
* known limitations
* maintainers

Common object types include `dataset`, `example`, `method`, `section`,
`template`, `tool`, `tool_data`, and `workflow`. Common status values include `draft`,
`experimental`, `validated`, and `deprecated`.

Common information classes are `knowledge`, `infrastructure`, and `asset`.
Most BMDex entries should be private `asset` or private `infrastructure`
objects. Public `knowledge` should usually live in `tutorials` unless it is
needed locally to explain an operational BMDex object.

In sidecars, `stewardship` records who controls the underlying resource or
system; `maintainers` records who curates the BMDex entry.

Metadata supports maintainers; it should not dominate the student-facing
experience.

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

## Adding Content

Add content only when it is useful enough to curate in a canonical location.
Scratch work, temporary notebooks, and speculative experiments should stay
outside BMDex until they become maintained lab knowledge.

Good first additions are usually practical workflow artifacts:

* a working script used in a real calculation folder
* a corrected SLURM template
* a documented operational failure mode and fix
* a small VASP or pymatgen example that others can rerun

Do not start by designing metadata, package structure, or broad abstractions
unless the workflow need is already clear. Metadata can be repaired during
curation.

Cluster execution should happen from a normal git checkout on the cluster after
changes have been pushed and pulled. Do not require Codex on the cluster for
ordinary tool usage.

The goal is to preserve and share the computational knowledge that repeatedly
proves useful across the BMD Lab.
