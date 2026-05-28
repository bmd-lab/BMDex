# BMDex Metadata Schemas

BMDex uses YAML sidecars to make repository objects discoverable, reviewable,
and machine-checkable.

Directory-backed objects use `bmdex.yaml`. Single-file objects may use
`<filename>.bmdex.yaml` next to the file they describe.

The canonical schema contract is:

- `bmdex.schema.yaml`

Validate sidecars with:

```bash
python3 tools/metadata/validate_bmdex_metadata.py
```
