# Common TAU PowerSLURM Failures

This document collects common operational issues encountered in BMD Lab computational workflows on TAU PowerSLURM systems.

The goal is to:
- reduce repeated debugging effort
- preserve operational knowledge
- accelerate onboarding
- and document known workflow pitfalls.

---

# SLURM Submission Issues

## Job Runs From the Wrong Directory

Typical symptoms:
- VASP cannot find `INCAR`, `POSCAR`, `KPOINTS`, or `POTCAR`
- output files appear in an unexpected directory

Recommended convention:

```bash
cd "$SLURM_SUBMIT_DIR"
```

Add this before loading or running workflow-specific commands.

---

## Job Remains Pending

Typical causes:
- insufficient requested resources
- unavailable partition resources
- account mismatch
- walltime too large

Useful commands:

```bash
squeue -u $USER
scontrol show job <JOBID>
```

---

## Invalid Account or Partition

Typical symptoms:
- immediate job rejection
- sbatch submission errors

Current validated defaults:

```text
Partition:
leeburton-pool

Account:
power-leeburton-users_v2
```

---

## Batch Script Submits Too Many Jobs

Typical causes:
- hardcoded username in `squeue` checks
- queue count includes other users
- no configurable maximum job count

Recommended convention:

```bash
squeue -u "$USER"
```

Batch utilities should provide a dry-run mode and a configurable queue limit.

---

# Module Issues

## VASP Module Not Found

Typical symptom:

```text
module: command not found
```

or:

```text
Unable to locate module
```

Recommended modules:

```bash
module load intel/rocky8-oneAPI-2023
module load vasp/rocky8-intel-6.4.1
```

Cluster module naming may change over time.

---

## Noninteractive Shell Does Not Load Expected Environment

Typical symptoms:
- `module` or `mamba` setup works interactively but fails inside SLURM
- VASP or Python environments are unavailable in submitted jobs

Recommended mitigation:
- load required modules inside the SLURM script
- avoid relying on interactive shell state
- print key environment variables in debugging jobs

---

# POTCAR Issues

## Missing POTCAR

Typical symptoms:
- VASP startup failure
- POTCAR parsing errors

Current standard environment variable:

```bash
export PMG_VASP_PSP_DIR=/bmd-db/lee/potcars
```

BMDex workflows use:
- `POTCAR.spec`
rather than committed POTCAR files.

---

# VASP Runtime Issues

## Electronic Convergence Failure

Typical symptoms:
- excessive SCF cycles
- unconverged calculations
- unstable energies

Potential causes:
- poor initial geometry
- problematic smearing
- unrealistic magnetic initialization
- insufficient ENCUT

Possible mitigations:
- adjust smearing settings
- improve starting structure
- tighten or loosen convergence parameters appropriately

---

## Ionic Relaxation Failure

Typical symptoms:
- oscillating forces
- failure to converge geometry
- excessive ionic steps

Potential causes:
- poor initial structure
- unrealistic cell geometry
- problematic relaxation parameters

---

# Filesystem Issues

## Permission Errors

Typical causes:
- writing outside allocated directories
- incorrect filesystem ownership
- quota limitations

Useful commands:

```bash
quota
ls -l
```

---

## Corrupted WAVECAR

Typical symptoms:
- VASP startup crash
- WAVECAR read failure

Common mitigation:
- remove WAVECAR
- restart cleanly

---

## Relaxation Reaches NSW Limit

Typical symptoms:
- `OUTCAR` contains normal completion text
- `OSZICAR` reaches the `NSW` step limit
- forces are not converged

Recommended mitigation:
- inspect energy and force trends
- back up the existing `POSCAR`
- copy `CONTCAR` to `POSCAR`
- resubmit only after confirming the structure is physically reasonable

Use `tools/hpc/vasp_status.py` and `tools/hpc/restart_relaxations.py` for a
first-pass operational check.

---

# GPU Issues

## Full GPU and MIG Resource Requests Are Confused

Typical symptoms:
- job remains pending unexpectedly
- job runs with less GPU memory than expected
- `CUDA_VISIBLE_DEVICES` does not match expectations

Current full GPU request:

```bash
#SBATCH --gres=gpu:H100:1
```

Current MIG request:

```bash
#SBATCH --gres=gpu:1g.10gb:1
```

Use full GPU resources for large or untested VASP jobs unless the workflow has
been checked on a MIG slice.

---

# pymatgen Issues

## POTCAR Functional Mismatch

Typical causes:
- inconsistent pseudopotential setup
- mixed functional usage

Current validated standard:
- `PBE_64`

---

# General Debugging Recommendations

When troubleshooting:
1. inspect SLURM output files
2. check module environment
3. verify POTCAR setup
4. confirm filesystem paths
5. validate input files
6. isolate minimal reproducible examples

Prefer:
- conservative validated workflows
over:
- premature optimization or excessive complexity.
