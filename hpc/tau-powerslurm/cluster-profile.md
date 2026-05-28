# TAU PowerSLURM Cluster Profile

This document records the current BMD Lab operating profile for TAU
PowerSLURM. Recheck these values when the cluster image, module stack, account
policy, or VASP installation changes.

## Standard Accounts and Partitions

| Use case | Partition | Account |
| --- | --- | --- |
| CPU VASP and Python jobs | `leeburton-pool` | `power-leeburton-users_v2` |
| GPU VASP jobs | `gpu-leeburton-pool` | `power-leeburton-users_v2` |

## Standard CPU VASP Modules

```bash
module load intel/rocky8-oneAPI-2023
module load vasp/rocky8-intel-6.4.1
```

Current CPU VASP jobs use:

```bash
mpirun -n "$SLURM_NTASKS" vasp_std > output
```

## Standard GPU VASP Module

```bash
module purge
module load vasp/vasp.6.5.1-hpc_sdk
```

Current GPU VASP jobs use one MPI rank unless a workflow explicitly validates a
different launch model.

## Standard Resource Tiers

| Job type | Nodes | Tasks | Memory | Walltime |
| --- | ---: | ---: | ---: | ---: |
| Python utility | 1 | 1 | 40G | 24:00:00 |
| Standard CPU VASP | 1 | 24 | 120G | 72:00:00 |
| Large CPU VASP | 2 | 96 | 920G | 99:00:00 |
| Single GPU VASP | 1 | 1 | 16G | 24:00:00 |

These are starting points, not scientific guarantees. Larger slabs, supercells,
hybrid calculations, magnetic systems, and long relaxations need workflow-level
resource checks.

## Filesystem Conventions

Current POTCAR root:

```text
/bmd-db/lee/potcars
```

Current pymatgen setting:

```bash
export PMG_VASP_PSP_DIR=/bmd-db/lee/potcars
```

Current Python environment root:

```text
/leeburton-data/$USER/envs/
```

Older tutorial-era paths may appear in historical scripts. Promote only one
canonical path into BMDex workflows unless a specific legacy workflow requires
otherwise.

## Source Provenance

This profile is distilled from the group tutorials repository and should be
treated as operational lab knowledge rather than a general TAU cluster manual.
