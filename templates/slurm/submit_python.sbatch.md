# SLURM Submission Template for Python Utilities

## Purpose

This template provides a simple starting point for scheduled Python utilities on
TAU PowerSLURM.

Typical use cases:

- pymatgen structure processing
- high-throughput directory preparation
- post-processing and status checks
- lightweight workflow helpers

## Usage

Copy the template into a working directory and edit:

- job name
- walltime
- memory
- environment activation
- `PYTHON_SCRIPT`

Default execution:

```bash
python "$PYTHON_SCRIPT" > python.out
```

By default, `PYTHON_SCRIPT` is `run.py`.

## Environment

Load mamba and activate the required environment inside the SLURM script. Do
not rely on interactive shell state.
