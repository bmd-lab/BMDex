# VASP Execution Standards

This document records BMD Lab conventions for running VASP on TAU PowerSLURM.

## CPU Execution

Current standard CPU module stack:

```bash
module load intel/rocky8-oneAPI-2023
module load vasp/rocky8-intel-6.4.1
```

Current execution command:

```bash
mpirun -n "$SLURM_NTASKS" vasp_std > output
```

The canonical CPU starting template is:

```text
templates/slurm/submit_vasp.sbatch
```

## Input Expectations

Every production VASP calculation should preserve:

- `INCAR`
- `POSCAR`
- `KPOINTS`
- `POTCAR.spec`
- the submission script used
- the VASP standard output file

Actual `POTCAR` files are not stored in BMDex.

## Parallelization Policy

For VASP 6 workflows, prefer explicit `NCORE` and `KPAR` choices over old
`NPAR` defaults unless a legacy workflow documents why `NPAR` is required.

`KPAR` must divide the number of irreducible k-points and must be compatible
with the total MPI rank count.

## Completion and Restart Policy

A VASP run is not considered scientifically complete only because SLURM ended.
Operational checks should inspect:

- whether `OUTCAR` contains the normal VASP completion marker
- whether `OSZICAR` reached the `NSW` limit
- whether `CONTCAR` exists and is non-empty
- whether the final geometry and energy trend are scientifically reasonable

Use `tools/hpc/vasp_status.py` for a first-pass directory scan and
`tools/hpc/restart_relaxations.py` for controlled `CONTCAR -> POSCAR` restarts.
