#!/bin/bash

# Prepare VASP relaxation restarts by copying CONTCAR to POSCAR.
#
# Default behavior is a dry run. Use --apply to modify calculation folders.

set -u

ROOT="."
RECURSIVE=0
JOB_SCRIPT_NAMES=(
  "submit.sh"
  "job_script.sh"
  "submit_vasp.sh"
)
COMPLETION_MARKER="Voluntary"
ALL_WITH_CONTCAR=0
APPLY=0
RESUBMIT=0
CUSTOM_JOB_SCRIPTS=()

usage() {
  cat <<'EOF'
Usage: bash slurm/restart_relaxations.sh [options]

Prepare VASP relaxation restarts from CONTCAR files.

Options:
  --root PATH           Root directory containing calculation subdirectories.
  --recursive           Scan recursively instead of only direct children.
  --job-script NAME     Accepted SLURM script name. May be supplied repeatedly.
  --all-with-contcar    Restart every directory with a non-empty CONTCAR.
  --apply               Actually copy CONTCAR to POSCAR. Default is dry run.
  --resubmit            Submit the local job script after applying restart.
  -h, --help            Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="${2:?Missing value for --root}"
      shift 2
      ;;
    --recursive)
      RECURSIVE=1
      shift
      ;;
    --job-script)
      CUSTOM_JOB_SCRIPTS+=("${2:?Missing value for --job-script}")
      shift 2
      ;;
    --all-with-contcar)
      ALL_WITH_CONTCAR=1
      shift
      ;;
    --apply)
      APPLY=1
      shift
      ;;
    --resubmit)
      RESUBMIT=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ${#CUSTOM_JOB_SCRIPTS[@]} -gt 0 ]]; then
  JOB_SCRIPT_NAMES=("${CUSTOM_JOB_SCRIPTS[@]}")
fi

if [[ ! -d "$ROOT" ]]; then
  echo "Root directory not found: $ROOT" >&2
  exit 1
fi

ROOT_PATH="$(cd "$ROOT" && pwd)"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"

parse_nsw() {
  local incar="$1"
  local line

  [[ -f "$incar" ]] || return 0

  while IFS= read -r line; do
    line="${line%%!*}"
    line="${line%%#*}"
    if [[ "$line" =~ ^[[:space:]]*NSW[[:space:]]*=[[:space:]]*([0-9]+) ]]; then
      printf '%s\n' "${BASH_REMATCH[1]}"
      return 0
    fi
  done < "$incar"
}

count_ionic_steps() {
  local oszicar="$1"

  if [[ ! -f "$oszicar" ]]; then
    printf '0\n'
    return 0
  fi

  awk '/^[[:space:]]*[0-9]+[[:space:]]+F=/ {count++} END {print count + 0}' "$oszicar"
}

reached_nsw() {
  local directory="$1"
  local outcar="$directory/OUTCAR"
  local oszicar="$directory/OSZICAR"
  local incar="$directory/INCAR"
  local nsw
  local ionic_steps

  nsw="$(parse_nsw "$incar")"

  if [[ -z "$nsw" || ! -f "$outcar" || ! -f "$oszicar" ]]; then
    return 1
  fi

  if ! grep -qF "$COMPLETION_MARKER" "$outcar" 2>/dev/null; then
    return 1
  fi

  ionic_steps="$(count_ionic_steps "$oszicar")"
  [[ "$ionic_steps" -ge "$nsw" ]]
}

restartable() {
  local directory="$1"
  local contcar="$directory/CONTCAR"

  [[ -s "$contcar" ]] || return 1

  if [[ "$ALL_WITH_CONTCAR" -eq 1 ]]; then
    return 0
  fi

  reached_nsw "$directory"
}

find_job_script() {
  local directory="$1"
  local name

  for name in "${JOB_SCRIPT_NAMES[@]}"; do
    if [[ -f "$directory/$name" ]]; then
      printf '%s\n' "$directory/$name"
      return 0
    fi
  done

  return 1
}

apply_restart() {
  local directory="$1"
  local poscar="$directory/POSCAR"
  local contcar="$directory/CONTCAR"
  local backup="$directory/POSCAR.before_restart.$TIMESTAMP"

  if [[ -e "$poscar" ]]; then
    cp -p "$poscar" "$backup"
  fi

  cp -p "$contcar" "$poscar"
  printf '%s\n' "$backup"
}

submit_job() {
  local directory="$1"
  local job_script="$2"

  (cd "$directory" && sbatch "$(basename "$job_script")")
}

discover_directories() {
  if [[ "$RECURSIVE" -eq 1 ]]; then
    find "$ROOT_PATH" -mindepth 1 -type d | sort
  else
    find "$ROOT_PATH" -mindepth 1 -maxdepth 1 -type d | sort
  fi
}

changed=0
skipped=0

echo "Scanning: $ROOT_PATH"
if [[ "$APPLY" -eq 1 ]]; then
  echo "Mode: apply"
else
  echo "Mode: dry run"
fi
echo

while IFS= read -r directory; do
  [[ -n "$directory" ]] || continue

  if [[ ! -e "$directory/CONTCAR" ]]; then
    continue
  fi

  if ! restartable "$directory"; then
    skipped=$((skipped + 1))
    continue
  fi

  job_script="$(find_job_script "$directory" || true)"

  if [[ "$APPLY" -ne 1 ]]; then
    echo "DRY RUN restart: $directory"
    changed=$((changed + 1))
    continue
  fi

  backup="$(apply_restart "$directory")"
  echo "Restarted: $directory"
  if [[ -e "$backup" ]]; then
    echo "  Backup: $(basename "$backup")"
  fi

  if [[ "$RESUBMIT" -eq 1 ]]; then
    if [[ -z "$job_script" ]]; then
      echo "  No job script found; not submitted."
    else
      submit_job "$directory" "$job_script"
      echo "  Submitted: $(basename "$job_script")"
    fi
  fi

  changed=$((changed + 1))
done < <(discover_directories)

echo
if [[ "$APPLY" -eq 1 ]]; then
  echo "Done: changed $changed; skipped $skipped."
else
  echo "Done: would restart $changed; skipped $skipped."
fi
