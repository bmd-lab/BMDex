#!/bin/bash
#SBATCH --job-name=vasp_gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=24:00:00
#SBATCH --mem=16G
#SBATCH -p gpu-leeburton-pool
#SBATCH -A power-leeburton-users_v2
#SBATCH --gres=gpu:H100:1

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"
ulimit -s 81920

module purge
module load vasp/vasp.6.5.1-hpc_sdk

echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset}"

mpirun -n "$SLURM_NTASKS" vasp_std > output
