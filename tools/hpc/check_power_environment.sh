#!/bin/bash

# Check common TAU PowerSLURM environment assumptions for BMDex workflows.

set -u

status=0

check_path() {
    label="$1"
    path="$2"

    if [ -e "$path" ]; then
        echo "OK   $label: $path"
    else
        echo "WARN $label not found: $path"
        status=1
    fi
}

check_command() {
    name="$1"

    if command -v "$name" >/dev/null 2>&1; then
        echo "OK   command available: $name"
    else
        echo "WARN command not found: $name"
        status=1
    fi
}

echo "BMDex TAU PowerSLURM environment check"
echo

if type module >/dev/null 2>&1; then
    echo "OK   module command is available"
else
    echo "WARN module command is not available in this shell"
    status=1
fi

check_command python
check_command python3

echo
echo "Standard SLURM settings:"
echo "  CPU partition: leeburton-pool"
echo "  GPU partition: gpu-leeburton-pool"
echo "  Account:       power-leeburton-users_v2"

echo
echo "Standard VASP modules:"
echo "  CPU: module load intel/rocky8-oneAPI-2023"
echo "       module load vasp/rocky8-intel-6.4.1"
echo "  GPU: module purge"
echo "       module load vasp/vasp.6.5.1-hpc_sdk"

echo
if [ -n "${PMG_VASP_PSP_DIR:-}" ]; then
    echo "OK   PMG_VASP_PSP_DIR=$PMG_VASP_PSP_DIR"
    check_path "PMG_VASP_PSP_DIR" "$PMG_VASP_PSP_DIR"
else
    echo "WARN PMG_VASP_PSP_DIR is not set"
    echo "     Expected: export PMG_VASP_PSP_DIR=/bmd-db/lee/potcars"
    status=1
fi

echo
if [ -d "/leeburton-data/$USER/envs" ]; then
    echo "OK   Python env root: /leeburton-data/$USER/envs"
else
    echo "WARN Python env root not found: /leeburton-data/$USER/envs"
fi

exit "$status"
