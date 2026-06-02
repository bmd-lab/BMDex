# Metadata Tools

Repository curation utilities for BMDex metadata.

BMDex uses lightweight YAML sidecars to make curated repository objects
discoverable, reviewable, and machine-checkable.

Directory-backed objects use:

```text
bmdex.yaml
```

Single-file objects may use:

```text
<filename>.bmdex.yaml
```

Validate object sidecars with:

```bash
python3 metadata/validate_bmdex_metadata.py
```

## Curation Principles

BMDex is the private operational layer behind the public tutorials repository.
Tutorials introduce concepts; BMDex preserves reusable tools, standards,
templates, datasets, examples, and institutional workflow knowledge.

Curated content should expose the useful researcher action first. Most students
are materials scientists, so ordinary tool usage should not require knowledge
of metadata, Codex, schemas, or repository governance.

Preferred access model:

1. students learn concepts through public tutorials
2. students use the private repository or website as their first BMDex entry
3. cluster-side work uses a normal git checkout or pull of BMDex
4. Codex-assisted curation happens from a laptop or workstation checkout

Do not assume Codex is installed on the cluster. Cluster-facing scripts,
templates, and examples should be directly runnable or copyable from a
cluster-side checkout.

Repository evolution should stay shallow and practical:

- put content in the section where students will look for it
- keep tools directly runnable and easy to adapt
- keep templates and examples close to the workflows that use them
- record maturity with metadata rather than lifecycle directories
- keep scratch work, temporary notebooks, and large calculation outputs outside
  BMDex until they are ready to curate

## Minimal Sidecar Contract

Sidecars should include:

- `schema_version`
- `id`
- `type`
- `status`
- `validation_level`
- `title`
- `domain`
- `description`
- `validation`
- `limitations`
- `maintainers`

Allowed object types:

- `dataset`
- `example`
- `hpc`
- `method`
- `template`
- `tool`
- `tool_data`
- `workflow`

The `method` object type remains valid for scientific standards and repository
conventions even though BMDex no longer has a top-level `methods/` directory.

Allowed status values:

- `draft`
- `experimental`
- `validated`
- `deprecated`

Allowed validation levels:

- `documented`
- `example_only`
- `external_source_import`
- `publication_backed`
- `reference`
- `validated_workflow`

This contract is intentionally small and is maintained in
`validate_bmdex_metadata.py`. It supports maintainers without making metadata
the first thing new students need to understand.
