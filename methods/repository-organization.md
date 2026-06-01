# Repository Organization

This document describes the organizational structure and design philosophy of BMDex.

The goal of the repository structure is to:
- preserve institutional computational knowledge
- separate reusable infrastructure from project-specific workflows
- distinguish maturity and validation state through metadata and documentation
- group content by scientific topic where practical
- maintain long-term maintainability as the repository evolves

## Core Philosophy

BMDex is intended to function as:
- a reusable computational infrastructure repository
- a curated methodological resource
- and a long-term institutional memory system for the BMD Lab.

The repository prioritizes:
1. scientific correctness
2. reproducibility
3. maintainability
4. transparency
5. workflow standardization
6. onboarding efficiency

## Access and Execution Model

BMDex is intended to sit behind the public tutorials repository and the private
GitHub repository or website. Tutorials remain pedagogical. BMDex preserves the
private operational layer.

The expected workflow is:

1. edit and curate BMDex from a laptop or workstation checkout
2. push changes through version control
3. pull BMDex onto the cluster
4. run or copy tools from the cluster-side checkout inside the real scientific
   software environment

Codex may help curate BMDex from the local checkout, but Codex should not be a
runtime dependency for cluster workflows.

Students onboarding into BMDex are assumed to be materials scientists first.
They may have little experience with Git, Codex, metadata schemas, or package
architecture. Repository structure should therefore make the useful research
action obvious before exposing the maintainability machinery behind it.

## Organizational Structure

Top-level sections describe content type. Within those sections, subdirectories
should usually follow materials-science topics such as structure, composition,
or DFT workflow domain rather than software package names alone.

### `tools/`

Reusable computational primitives and utilities.

Examples:
- structure manipulation
- composition screening
- slab generation
- supercell generation
- electroneutral composition generation
- oxidation-state datasets

Tools should:
- remain reusable
- avoid unnecessary project-specific assumptions
- prioritize interoperability and maintainability
- be directly runnable or easy to copy into calculation folders when practical
- expose clear user settings before internal helper abstractions

### `methods/`

Scientific conventions, methodological standards, and workflow philosophy.

Examples:
- VASP input standards
- convergence philosophy
- structure-manipulation conventions
- composition-screening conventions
- repository design philosophy and governance decisions

Methods explain:
- why workflows exist
- what assumptions are used
- and how standards should be interpreted.

Repository-level design records live under `methods/repository-governance/`.
They are treated as governance methods rather than as a separate top-level
content type.

### Lifecycle Metadata

BMDex does not use separate top-level lifecycle buckets such as `incoming/`,
`experimental/`, `validated/`, or `deprecated/`.

Instead, lifecycle state should be recorded in canonical metadata sidecars and
described locally in the relevant README files. Directory-backed objects use
`bmdex.yaml`; single-file objects may use `<filename>.bmdex.yaml`.

Scratch work, temporary notebooks, and speculative experiments should remain
outside BMDex until they are useful enough to curate in a canonical section.

Physical placement in the repository should answer "what kind of thing is
this?" rather than "what is its current status?"

Metadata sidecars should validate with
`methods/repository-governance/metadata/validate_bmdex_metadata.py`.

Software package names may still appear inside canonical sections when they are
the clearest way to describe a method, but they should not create redundant
top-level buckets when the underlying topic already has a better scientific
home.

### `templates/`

Reusable starting points and reference configurations.

Examples:
- INCAR templates
- SLURM templates
- KPOINTS templates

Templates are intended to:
- accelerate onboarding
- improve consistency
- preserve operational conventions

### `examples/`

Minimal executable demonstrations and onboarding workflows.

Examples should prioritize:
- clarity
- reproducibility
- maintainability
over excessive optimization or abstraction.

## Workflow Hierarchy

BMDex distinguishes between:

### Reusable Primitives

Generic reusable infrastructure.

Examples:
- slab generation
- supercell construction
- oxidation-state datasets

### Scientific Workflows

Higher-level orchestrated methodologies built from reusable primitives.

Examples:
- MSS-Auto under `tools/structure_transform/mss_auto/`
- layered-material screening workflows
- high-throughput structure generation

### Validated Examples

Concrete trusted workflows used for onboarding and operational reference. These
live in their canonical content directories, with validation state recorded in
metadata rather than through a separate top-level folder.

Examples:
- Si bulk relaxation
- canonical slab-generation examples

## Long-Term Goals

The repository is intended to evolve incrementally through:
- real workflow usage
- onboarding experience
- contribution refinement
- and preservation of institutional knowledge.

The repository should avoid:
- uncontrolled project dumping
- excessive abstraction
- duplication of reusable logic
- undocumented workflow drift
- silent methodological inconsistencies
- making metadata, Git, or Codex knowledge a prerequisite for using curated tools
