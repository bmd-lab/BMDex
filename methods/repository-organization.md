# Repository Organization

This document describes the organizational structure and design philosophy of BMDex.

The goal of the repository structure is to:
- preserve institutional computational knowledge
- separate reusable infrastructure from project-specific workflows
- distinguish validated methods from exploratory work
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

## Organizational Structure

### `tools/`

Reusable computational primitives and utilities.

Examples:
- structure manipulation
- slab generation
- supercell generation
- electroneutral composition generation
- oxidation-state datasets

Tools should:
- remain reusable
- avoid unnecessary project-specific assumptions
- prioritize interoperability and maintainability

### `methods/`

Scientific conventions, methodological standards, and workflow philosophy.

Examples:
- VASP input standards
- convergence philosophy
- pymatgen usage conventions
- repository design philosophy

Methods explain:
- why workflows exist
- what assumptions are used
- and how standards should be interpreted.

### `validated/`

Stable workflows and tools considered suitable for regular group use.

Validated content should:
- contain sufficient documentation
- be reproducible
- specify assumptions explicitly
- avoid undocumented dependencies

### `experimental/`

Exploratory or actively developing workflows.

Experimental content may:
- change substantially
- contain incomplete validation
- rely on unstable assumptions

Experimental content should not automatically be treated as production-ready.

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

### `decisions/`

Repository-level design decisions and institutional reasoning.

These files preserve:
- why standards were adopted
- workflow evolution
- organizational philosophy
- important methodological decisions

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
- MSS-Auto
- layered-material screening workflows
- high-throughput structure generation

### Validated Examples

Concrete trusted workflows used for onboarding and operational reference.

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
