#!/bin/bash

# Submit many VASP calculation directories on a SLURM cluster.
#
# Default behavior is a dry run. Use --submit to call sbatch.

set -u

ROOT="."
JOB_SCRIPT_NAMES=(
  "submit.sh"
  "job_script.sh"
  "submit_vasp.sh"
)
REQUIRED_INPUTS=("INCAR" "POSCAR" "KPOINTS")
COMPLETION_MARKER="Voluntary"
MAX_QUEUED_JOBS=20
POLL_SECONDS=60
RECURSIVE=0
SUBMIT=0
CUSTOM_JOB_SCRIPTS=()

usage() {
  cat <<'EOF'
Usage: bash cluster/submit_many_vasp.sh [options]

Submit many VASP calculation directories with queue throttling.

Options:
  --root PATH           Root directory containing calculation subdirectories.
  --job-script NAME     Accepted SLURM script name. May be supplied repeatedly.
  --max-queued N        Maximum number of current-user jobs before waiting.
  --poll-seconds N      Seconds to wait before checking the queue again.
  --recursive           Scan directories recursively.
  --submit              Actually submit jobs. Without this, print a dry run.
  -h, --help            Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="${2:?Missing value for --root}"
      shift 2
      ;;
    --job-script)
      CUSTOM_JOB_SCRIPTS+=("${2:?Missing value for --job-script}")
      shift 2
      ;;
    --max-queued)
      MAX_QUEUED_JOBS="${2:?Missing value for --max-queued}"
      shift 2
      ;;
    --poll-seconds)
      POLL_SECONDS="${2:?Missing value for --poll-seconds}"
      shift 2
      ;;
    --recursive)
      RECURSIVE=1
      shift
      ;;
    --submit)
      SUBMIT=1
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

missing_required_inputs() {
  local directory="$1"
  local missing=()
  local name

  for name in "${REQUIRED_INPUTS[@]}"; do
    if [[ ! -f "$directory/$name" ]]; then
      missing+=("$name")
    fi
  done

  if [[ ${#missing[@]} -eq 0 ]]; then
    printf '\n'
    return 0
  fi

  local IFS=,
  printf '%s\n' "${missing[*]}"
}

calculation_complete() {
  local directory="$1"
  grep -qF "$COMPLETION_MARKER" "$directory/OUTCAR" 2>/dev/null
}

queued_job_count() {
  local user="${USER:-}"

  if ! command -v squeue >/dev/null 2>&1; then
    printf '0\n'
    return 0
  fi

  squeue -h -u "$user" 2>/dev/null | awk 'NF {count++} END {print count + 0}'
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

submitted=0
skipped=0

echo "Scanning: $ROOT_PATH"
if [[ "$SUBMIT" -eq 1 ]]; then
  echo "Mode: submit"
else
  echo "Mode: dry run"
fi
echo

while IFS= read -r directory; do
  [[ -n "$directory" ]] || continue

  job_script="$(find_job_script "$directory" || true)"
  missing_inputs="$(missing_required_inputs "$directory")"

  if [[ -z "$job_script" && -n "$missing_inputs" ]]; then
    continue
  fi

  if [[ -n "$missing_inputs" ]]; then
    echo "SKIP missing inputs [$missing_inputs]: $directory"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ -z "$job_script" ]]; then
    echo "SKIP missing job script: $directory"
    skipped=$((skipped + 1))
    continue
  fi

  if calculation_complete "$directory"; then
    echo "SKIP complete: $directory"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ "$SUBMIT" -ne 1 ]]; then
    echo "DRY RUN submit $(basename "$job_script"): $directory"
    submitted=$((submitted + 1))
    continue
  fi

  while [[ "$(queued_job_count)" -ge "$MAX_QUEUED_JOBS" ]]; do
    queue_count="$(queued_job_count)"
    echo "Queue has $queue_count jobs for ${USER:-unknown}; waiting $POLL_SECONDS seconds."
    sleep "$POLL_SECONDS"
  done

  echo "Submitting $(basename "$job_script"): $directory"
  submit_job "$directory" "$job_script"
  submitted=$((submitted + 1))
done < <(discover_directories)

echo
if [[ "$SUBMIT" -eq 1 ]]; then
  echo "Done: submitted $submitted; skipped $skipped."
else
  echo "Done: would submit $submitted; skipped $skipped."
fi
