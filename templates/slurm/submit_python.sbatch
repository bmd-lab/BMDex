#!/bin/bash
#SBATCH --job-name=python_job
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=40G
#SBATCH -p leeburton-pool
#SBATCH -A power-leeburton-users_v2

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"
ulimit -s 81920

# Load or activate the environment needed by your script.
# module load mamba > /dev/null
# mamba activate /leeburton-data/$USER/envs/pymatgen-env

PYTHON_SCRIPT="${PYTHON_SCRIPT:-run.py}"

python "$PYTHON_SCRIPT" > python.out
