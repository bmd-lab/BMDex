# VASP

Private BMD Lab VASP assets: calculation standards, reusable input examples,
runnable examples, and practical VASP utility scripts.

Some details describe TAU PowerSLURM execution and licensed VASP
pseudopotential access. Those details are current operational conventions, not
lab-controlled cluster behavior.

Status:

- validated operational guidance for current BMD Lab VASP practice
- reusable input examples are starting points, not universal production settings
- cluster module names, partitions, accounts, and POTCAR paths may change

## Standards

Use conservative, documented settings before aggressive optimization.
Production workflows should record:

- scientific purpose and assumptions
- pseudopotential functional
- convergence checks for the target property
- deviations from the reusable examples
- expected outputs and known limitations

Validated calculations should converge electronically, converge ionically where
appropriate, preserve expected physical behavior, and include basic sanity
checks.

## Inputs

Every production VASP calculation should preserve:

- `INCAR`
- `POSCAR`
- `KPOINTS`
- `POTCAR.spec`
- the submission script used
- the VASP standard output file

Relaxation calculations normally enable ionic relaxation, use conservative
force and electronic convergence, and include the stress tensor when cell
relaxation is required.

Static calculations normally use fixed geometry, tighter electronic
convergence, and no ionic updates.

K-point density should scale with cell size. Production calculations should
document k-point convergence, the chosen mesh rationale, and sensitivity of the
target property.

## POTCAR Policy

Actual `POTCAR` files must not be committed to BMDex.

Use `POTCAR.spec` files instead. The order of entries in `POTCAR.spec` must
match the species ordering in `POSCAR`.

Current group standard functional:

```text
PBE_64
```

Current TAU PowerSLURM POTCAR root:

```text
/bmd-db/lee/potcars
```

Expected compatibility symlinks:

```text
POT_PAW_PBE_64 -> PBE_64
POT_GGA_PAW_PBE_64 -> PBE_64
```

Users should define:

```bash
export PMG_VASP_PSP_DIR=/bmd-db/lee/potcars
```

Generate `POTCAR` files only inside the licensed computational environment.
Mixing pseudopotential families should be avoided unless scientifically
justified and documented.

## Execution

Current CPU module stack:

```bash
module load intel/rocky8-oneAPI-2023
module load vasp/rocky8-intel-6.4.1
```

Current CPU launch:

```bash
mpirun -n "$SLURM_NTASKS" vasp_std > output
```

CPU starting script:

```text
cluster/submit_vasp.sh
```

For VASP 6 workflows, prefer explicit `NCORE` and `KPAR` choices over old
`NPAR` defaults unless a legacy workflow documents why `NPAR` is required.
`KPAR` must divide the number of irreducible k-points and must be compatible
with the total MPI rank count.

## GPU Execution

Current GPU module:

```bash
module purge
module load vasp/vasp.6.5.1-hpc_sdk
```

Full H100 request:

```bash
#SBATCH -p gpu-leeburton-pool
#SBATCH -A power-leeburton-users_v2
#SBATCH --gres=gpu:H100:1
```

MIG slice request:

```bash
#SBATCH -p gpu-leeburton-pool
#SBATCH -A power-leeburton-users_v2
#SBATCH --gres=gpu:1g.10gb:1
```

Use MIG only when the calculation has been checked to fit the memory and
performance profile. Large VASP workflows should start with a full GPU request.

GPU starting script:

```text
cluster/submit_vasp_gpu.sh
```

GPU workflows should document whether they used a full GPU or MIG slice, the
VASP GPU module version, MPI ranks, CPU threads per task, and any change from
the standard script.

## Completion And Restarts

A VASP run is not scientifically complete only because SLURM ended. Operational
checks should inspect:

- whether `OUTCAR` contains the normal VASP completion marker
- whether `OSZICAR` reached the `NSW` limit
- whether `CONTCAR` exists and is non-empty
- whether the final geometry and energy trend are scientifically reasonable

Use `cluster/vasp_status.sh` for a first-pass directory scan and
`cluster/restart_relaxations.sh` for controlled `CONTCAR -> POSCAR` restarts.

## Validation Evidence

Concrete validation evidence records live under `evidence/`.

- `evidence/2026-08-21-si-hse06-band-structure-powerslurm.md`: crystalline-Si
  HSE06 band-structure PowerSLURM validation evidence.

## Examples And Reusable Inputs

Reusable inputs and runnable examples live under `examples/`.

- `examples/INCAR.relax`
- `examples/INCAR.static`
- `examples/KPOINTS.example`
- `examples/POTCAR.spec.example`
- `examples/si_bulk_relax/`

See `examples/README.md` for notes on the reusable input files.

## Utilities

Generate a local `POTCAR` from a repository-safe `POTCAR.spec` file using the
configured pymatgen POTCAR directory:

```bash
python3 vasp/make_potcar_from_spec.py
```

Fetch structures from Materials Project IDs and write pymatgen `MPRelaxSet`
input folders:

```bash
python3 vasp/create_mp_relax_inputs.py
```

By default, `create_mp_relax_inputs.py` writes `POTCAR.spec` instead of an
actual `POTCAR`.

Utility dependencies include pymatgen. `create_mp_relax_inputs.py` also
requires `mp-api` and a valid Materials Project API key. `make_potcar_from_spec.py`
requires access to the licensed VASP pseudopotential directory in the
computational environment.

Cluster submission standards and reusable batch scripts live under `cluster/`.
