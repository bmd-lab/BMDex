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
python3 tools/metadata/validate_bmdex_metadata.py
```

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
