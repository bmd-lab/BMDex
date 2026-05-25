#!/bin/bash
#SBATCH --job-name=vasp_job
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --time=72:00:00
#SBATCH --mem=120G
#SBATCH -p leeburton-pool
#SBATCH -A power-leeburton-users_v2

set -e -o pipefail

module load intel/rocky8-oneAPI-2023
module load vasp/rocky8-intel-6.4.1

export VASP_CMD="mpirun -n $SLURM_NTASKS vasp_std"

$VASP_CMD
