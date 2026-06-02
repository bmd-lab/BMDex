#! /usr/bin/env python3

"""
Validate BMDex metadata sidecars.

The validator checks the lightweight BMDex sidecar contract. It is
intentionally repository-local and avoids assuming a packaging layout.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - depends on local environment
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ID_PREFIXES = {
    "dataset",
    "example",
    "hpc",
    "method",
    "template",
    "tool",
    "workflow",
}


METADATA_CONTRACT: dict[str, Any] = {
    "schema_version": 1,
    "required_fields": [
        "schema_version",
        "id",
        "type",
        "status",
        "validation_level",
        "title",
        "domain",
        "description",
        "validation",
        "limitations",
        "maintainers",
    ],
    "allowed_values": {
        "type": [
            "dataset",
            "example",
            "hpc",
            "method",
            "template",
            "tool",
            "tool_data",
            "workflow",
        ],
        "status": [
            "draft",
            "experimental",
            "validated",
            "deprecated",
        ],
        "validation_level": [
            "documented",
            "example_only",
            "external_source_import",
            "publication_backed",
            "reference",
            "validated_workflow",
        ],
    },
    "required_list_fields": [
        "domain",
        "validation",
        "limitations",
        "maintainers",
    ],
    "reference_fields": [
        "methods",
        "templates",
        "uses",
        "used_by",
        "related",
    ],
    "soft_reference_fields": [
        "planned_integrations",
    ],
    "id_pattern": r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$",
}


def load_yaml(path: Path) -> Any:
    with path.open() as stream:
        return yaml.safe_load(stream)


def is_sidecar(path: Path) -> bool:
    return path.name == "bmdex.yaml" or path.name.endswith(".bmdex.yaml")


def find_sidecars(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and is_sidecar(path)
        and ".git" not in path.parts
    )


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(flatten_strings(item))
        return result
    return []


def looks_like_bmdex_id(value: str, id_re: re.Pattern[str]) -> bool:
    if not id_re.match(value):
        return False
    prefix = value.split(".", 1)[0]
    return prefix in ID_PREFIXES


def validate_sidecar(
    path: Path,
    data: Any,
    schema: dict[str, Any],
    id_re: re.Pattern[str],
) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [f"{path}: sidecar must contain a YAML mapping"]

    for field in schema["required_fields"]:
        if field not in data or data[field] in (None, "", []):
            errors.append(f"{path}: missing required field '{field}'")

    expected_schema_version = schema["schema_version"]
    if data.get("schema_version") != expected_schema_version:
        errors.append(
            f"{path}: schema_version must be {expected_schema_version}"
        )

    object_id = data.get("id")
    if isinstance(object_id, str):
        if not id_re.match(object_id):
            errors.append(f"{path}: id has invalid format '{object_id}'")
    elif "id" in data:
        errors.append(f"{path}: id must be a string")

    allowed_values = schema["allowed_values"]
    for field, allowed in allowed_values.items():
        if field in data and data[field] not in allowed:
            errors.append(
                f"{path}: {field} '{data[field]}' is not allowed"
            )

    for field in schema["required_list_fields"]:
        if field in data:
            if not isinstance(data[field], list) or not data[field]:
                errors.append(
                    f"{path}: field '{field}' must be a non-empty list"
                )

    return errors


def collect_references(
    data: dict[str, Any],
    fields: list[str],
    id_re: re.Pattern[str],
) -> list[str]:
    refs: list[str] = []
    for field in fields:
        if field not in data:
            continue
        for value in flatten_strings(data[field]):
            if looks_like_bmdex_id(value, id_re):
                refs.append(value)
    return refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to validate",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    schema = METADATA_CONTRACT
    id_re = re.compile(schema["id_pattern"])

    sidecars = find_sidecars(root)
    errors: list[str] = []
    warnings: list[str] = []
    objects: dict[str, Path] = {}
    parsed: list[tuple[Path, dict[str, Any]]] = []

    for path in sidecars:
        data = load_yaml(path)
        errors.extend(validate_sidecar(path, data, schema, id_re))
        if isinstance(data, dict):
            parsed.append((path, data))
            object_id = data.get("id")
            if isinstance(object_id, str):
                if object_id in objects:
                    errors.append(
                        f"{path}: duplicate id '{object_id}' also in "
                        f"{objects[object_id]}"
                    )
                else:
                    objects[object_id] = path

    for path, data in parsed:
        for ref in collect_references(
            data,
            schema["reference_fields"],
            id_re,
        ):
            if ref not in objects:
                errors.append(f"{path}: unresolved reference '{ref}'")

        for ref in collect_references(
            data,
            schema["soft_reference_fields"],
            id_re,
        ):
            if ref not in objects:
                warnings.append(
                    f"{path}: planned reference not yet present '{ref}'"
                )

    for warning in warnings:
        print(f"WARNING: {warning}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Metadata validation failed: {len(errors)} error(s), "
            f"{len(warnings)} warning(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"Metadata validation passed: {len(objects)} object(s), "
        f"{len(warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
