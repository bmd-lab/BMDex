# GPU VASP Standards

This document records current BMD Lab conventions for GPU VASP jobs on TAU
PowerSLURM.

## Standard GPU Resources

Full H100 GPU:

```bash
#SBATCH -p gpu-leeburton-pool
#SBATCH -A power-leeburton-users_v2
#SBATCH --gres=gpu:H100:1
```

MIG slice:

```bash
#SBATCH -p gpu-leeburton-pool
#SBATCH -A power-leeburton-users_v2
#SBATCH --gres=gpu:1g.10gb:1
```

Use MIG only when the calculation has been checked to fit the memory and
performance profile. Large VASP workflows should start with a full GPU request.

## Standard GPU Module

```bash
module purge
module load vasp/vasp.6.5.1-hpc_sdk
```

## Standard Launch

```bash
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
mpirun -n "$SLURM_NTASKS" vasp_std > output
```

The canonical GPU starting template is:

```text
cluster/submit_vasp_gpu.sh
```

## Documentation Requirement

GPU workflows should document whether they used:

- a full GPU or MIG slice
- the VASP GPU module version
- the number of MPI ranks
- the CPU threads per task
- any change from the standard template
