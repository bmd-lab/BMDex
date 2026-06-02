# HPC Tools

Practical operational utilities for BMD Lab cluster workflows.

These tools are intentionally shallow and filesystem-oriented. They are meant
to be run from the repository or copied into calculation directories when that
is more convenient.

## Tools

### `submit_many_vasp.py`

Submit many VASP calculation directories with a configurable queue limit.

Default behavior is a dry run:

```bash
python3 tools/hpc/submit_many_vasp.py --root screening-root
```

Submit jobs after checking the dry run:

```bash
python3 tools/hpc/submit_many_vasp.py --root screening-root --submit
```

### `vasp_status.py`

Scan VASP calculation directories and report operational status:

```bash
python3 tools/hpc/vasp_status.py --root screening-root
```

### `restart_relaxations.py`

Prepare controlled relaxation restarts by backing up `POSCAR` and copying
`CONTCAR` to `POSCAR`.

Default behavior is a dry run:

```bash
python3 tools/hpc/restart_relaxations.py --root screening-root
```

Apply restarts:

```bash
python3 tools/hpc/restart_relaxations.py --root screening-root --apply
```

### `check_power_environment.sh`

Check common TAU PowerSLURM environment assumptions:

```bash
bash tools/hpc/check_power_environment.sh
```

## Related Standards

Cluster standards are documented in:

```text
slurm/
vasp/
```
