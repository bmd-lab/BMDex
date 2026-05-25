# Common TAU PowerSLURM Failures

This document collects common operational issues encountered in BMD Lab computational workflows on TAU PowerSLURM systems.

The goal is to:
- reduce repeated debugging effort
- preserve operational knowledge
- accelerate onboarding
- and document known workflow pitfalls.

---

# SLURM Submission Issues

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
