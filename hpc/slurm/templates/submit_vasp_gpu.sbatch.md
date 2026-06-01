# SLURM Submission Template for GPU VASP

## Purpose

This template provides a practical starting point for GPU VASP jobs on TAU
PowerSLURM.

## Resource Request

The default requests one full H100 GPU:

```bash
#SBATCH --gres=gpu:H100:1
```

For a MIG slice, use the cluster-supported request documented in
`hpc/vasp/gpu-vasp.md`.

## Execution Model

```bash
mpirun -n "$SLURM_NTASKS" vasp_std > output
```

The template prints `CUDA_VISIBLE_DEVICES` to help diagnose GPU visibility.

## Notes

GPU calculations should record whether a full GPU or MIG slice was used. Large
or untested workflows should start from a full GPU request before moving to
smaller MIG resources.
