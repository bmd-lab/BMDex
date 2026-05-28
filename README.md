# BMDex

Curated computational methods, workflows, and standards for the BMD Lab.

BMDex serves as the lab’s shared computational knowledge base and institutional memory for reproducible computational materials science research.

Primary focus areas include:
- VASP-based density functional theory (DFT)
- atomic structure workflows and structure manipulation
- chemical formula and composition screening
- HPC workflow standardization
- reusable computational methods and templates
- onboarding and knowledge transfer between group members

The repository is intended to evolve collaboratively while maintaining scientific rigor, reproducibility, and clear documentation standards.

BMDex complements the public `tutorials` repository by serving as the private operational and methodological knowledge base of the BMD Lab.

While the tutorials repository focuses on educational and onboarding material, BMDex focuses on reusable computational tools, workflow standardization, operational guidance, and long-term institutional computational knowledge.

## Repository Layout

BMDex is organized by content type rather than lifecycle bucket.

- `tools/` reusable computational primitives and utilities
- `methods/` methodological standards, conventions, and design guidance
- `templates/` reusable starting points for calculations and job submission
- `examples/` minimal runnable reference workflows
- `datasets/` curated scientific datasets used by tools and workflows
- `hpc/` cluster-specific operational guidance
- `schemas/` canonical metadata schema and validation contract

Validation state, provenance, and limitations belong in each object's metadata
sidecar, not in separate top-level status directories. Directory-backed
objects use `bmdex.yaml`; single-file objects may use `<filename>.bmdex.yaml`.
Content should enter BMDex through its canonical section once it is useful
enough to curate; scratch or exploratory work should remain outside the
repository until then.
Repository-level design decisions and institutional reasoning live under
`methods/repository-governance/`.

Metadata sidecars are validated against `schemas/bmdex.schema.yaml` with:

```bash
python3 tools/metadata/validate_bmdex_metadata.py
```

## Topic Grouping

Within those top-level sections, BMDex should group material by materials
science topic rather than by software package name.

- atomic structure: structure generation, orientations, supercells, slabs, and prototype references
- chemical formula and composition: oxidation-state data and electroneutral composition generation
- DFT methods and workflows: VASP inputs, submission templates, and executable calculation examples
- HPC operations: cluster-specific execution and troubleshooting guidance

Software frameworks such as `pymatgen` should appear inside method notes or
tool documentation where relevant, but should not generally define repository
layout on their own.
