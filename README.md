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

BMDex assumes most new users are materials scientists first. Student-facing
tools and examples should be runnable, copyable, and understandable without
requiring prior experience with Git internals, Codex, metadata schemas, or
software-engineering conventions.

## Access Model

BMDex is intended to sit behind a staged student access path:

1. public `tutorials` repository for pedagogy and first exposure
2. private GitHub repository or website for curated BMDex standards and examples
3. cluster-side BMDex checkout once students can use SSH and the terminal
4. Codex-assisted curation once users are comfortable working at the console

Codex normally operates on a laptop or workstation checkout of BMDex. Cluster
execution should happen from a normal git clone or pull of BMDex on the
cluster. The cluster should not require Codex to run BMDex tools.

See `methods/repository-access-model.md` for the full convention.

For students, the first useful interaction with BMDex should usually be:

```bash
cp templates/slurm/submit_vasp.sbatch my-calc/submit.sbatch
python3 tools/structure/supercells/make_supercell.py
```

The metadata and validation layer supports maintainers underneath this
researcher-facing workflow.

## Repository Layout

BMDex is organized by content type rather than lifecycle bucket.

- `tools/` reusable computational primitives and utilities
- `methods/` methodological standards, conventions, and design guidance
- `templates/` reusable starting points for calculations and job submission
- `examples/` minimal runnable reference workflows
- `datasets/` curated scientific datasets used by tools and workflows
- `hpc/` cluster-specific operational guidance

Validation state, provenance, and limitations belong in each object's metadata
sidecar, not in separate top-level status directories. Directory-backed
objects use `bmdex.yaml`; single-file objects may use `<filename>.bmdex.yaml`.
Content should enter BMDex through its canonical section once it is useful
enough to curate; scratch or exploratory work should remain outside the
repository until then.
Repository-level design decisions and institutional reasoning live under
`methods/repository-governance/`.

Metadata sidecars are validated with:

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
