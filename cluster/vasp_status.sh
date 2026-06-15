#!/bin/bash

# Report operational status for VASP calculation directories.
#
# This is an operational triage script, not a scientific convergence validator.

set -u

ROOT="."
RECURSIVE=0
REQUIRED_INPUTS=("INCAR" "POSCAR" "KPOINTS")
COMPLETION_MARKER="Voluntary"

usage() {
  cat <<'EOF'
Usage: bash cluster/vasp_status.sh [options]

Summarize VASP calculation directory status.

Options:
  --root PATH     Root directory containing calculation subdirectories.
  --recursive     Scan recursively instead of only direct children.
  -h, --help      Show this help.
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

if [[ ! -d "$ROOT" ]]; then
  echo "Root directory not found: $ROOT" >&2
  exit 1
fi

ROOT_PATH="$(cd "$ROOT" && pwd)"

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
    return 0
  fi

  awk '/^[[:space:]]*[0-9]+[[:space:]]+F=/ {count++} END {print count + 0}' "$oszicar"
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

classify() {
  local directory="$1"
  local outcar="$directory/OUTCAR"
  local oszicar="$directory/OSZICAR"
  local incar="$directory/INCAR"
  local contcar="$directory/CONTCAR"
  local missing
  local nsw
  local ionic_steps

  missing="$(missing_required_inputs "$directory")"
  nsw="$(parse_nsw "$incar")"
  ionic_steps="$(count_ionic_steps "$oszicar")"

  if [[ -n "$missing" ]]; then
    printf '%s|%s|%s|%s\n' "missing_inputs" "${ionic_steps:-}" "${nsw:-}" "$missing"
    return 0
  fi

  if [[ ! -f "$outcar" ]]; then
    printf '%s|%s|%s|%s\n' "not_started" "${ionic_steps:-}" "${nsw:-}" ""
    return 0
  fi

  if grep -qF "$COMPLETION_MARKER" "$outcar" 2>/dev/null; then
    if [[ -n "$nsw" && -n "$ionic_steps" && "$ionic_steps" -ge "$nsw" ]]; then
      if [[ -s "$contcar" ]]; then
        printf '%s|%s|%s|%s\n' "restartable_reached_nsw" "$ionic_steps" "$nsw" "CONTCAR available"
      else
        printf '%s|%s|%s|%s\n' "reached_nsw_no_contcar" "$ionic_steps" "$nsw" ""
      fi
      return 0
    fi

    printf '%s|%s|%s|%s\n' "complete" "${ionic_steps:-}" "${nsw:-}" ""
    return 0
  fi

  if [[ -s "$contcar" ]]; then
    printf '%s|%s|%s|%s\n' "stopped_with_contcar" "${ionic_steps:-}" "${nsw:-}" "manual review"
    return 0
  fi

  printf '%s|%s|%s|%s\n' "running_or_failed" "${ionic_steps:-}" "${nsw:-}" "manual review"
}

discover_directories() {
  if [[ "$RECURSIVE" -eq 1 ]]; then
    find "$ROOT_PATH" -mindepth 1 -type d | sort
  else
    find "$ROOT_PATH" -mindepth 1 -maxdepth 1 -type d | sort
  fi
}

printf '%-25s %6s %6s  %s\n' "status" "steps" "NSW" "path"
printf '%-25s %6s %6s  %s\n' "-------------------------" "------" "------" "----------------------------------------"

while IFS= read -r directory; do
  [[ -n "$directory" ]] || continue

  if [[ ! -f "$directory/INCAR" && ! -f "$directory/OUTCAR" && ! -f "$directory/OSZICAR" && ! -f "$directory/CONTCAR" ]]; then
    continue
  fi

  IFS='|' read -r status steps nsw note < <(classify "$directory")
  steps="${steps:-"-"}"
  nsw="${nsw:-"-"}"

  if [[ -n "${note:-}" ]]; then
    printf '%-25s %6s %6s  %s  (%s)\n' "$status" "$steps" "$nsw" "$directory" "$note"
  else
    printf '%-25s %6s %6s  %s\n' "$status" "$steps" "$nsw" "$directory"
  fi
done < <(discover_directories)
