#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="${CODEX_SWITCH_DIST_DIR:-$REPO_ROOT/dist}"

python_candidate_path() {
  local candidate="$1"
  if [[ "$candidate" == */* ]]; then
    [[ -x "$candidate" ]] || return 1
    printf '%s\n' "$candidate"
    return
  fi
  command -v "$candidate" 2>/dev/null
}

python_supports_runtime() {
  "$1" -c \
    'import sys, tomllib; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' \
    >/dev/null 2>&1
}

resolve_python_bin() {
  local raw candidate seen
  local explicit="${CODEX_SWITCH_PYTHON:-}"
  local candidates=(
    python3
    python3.13
    python3.12
    python3.11
    /opt/homebrew/bin/python3
    /opt/homebrew/bin/python3.13
    /opt/homebrew/bin/python3.12
    /opt/homebrew/bin/python3.11
    /usr/local/bin/python3
    /usr/local/bin/python3.13
    /usr/local/bin/python3.12
    /usr/local/bin/python3.11
  )
  if [[ -n "$explicit" ]]; then
    candidate="$(python_candidate_path "$explicit" || true)"
    if [[ -z "$candidate" ]] || ! python_supports_runtime "$candidate"; then
      echo "CODEX_SWITCH_PYTHON must resolve to Python 3.11+ with tomllib: $explicit" >&2
      return 1
    fi
    printf '%s\n' "$candidate"
    return
  fi
  seen="|"
  for raw in "${candidates[@]}"; do
    candidate="$(python_candidate_path "$raw" || true)"
    [[ -n "$candidate" ]] || continue
    case "$seen" in
      *"|$candidate|"*) continue ;;
    esac
    seen="${seen}${candidate}|"
    if python_supports_runtime "$candidate"; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  echo "Python 3.11+ with tomllib not found; set CODEX_SWITCH_PYTHON" >&2
  return 1
}

PYTHON_BIN="$(resolve_python_bin)"
export CODEX_SWITCH_PYTHON="$PYTHON_BIN"

exec "$PYTHON_BIN" -B "$SCRIPT_DIR/codex_switch_release_bundle.py" \
  --repo-root "$REPO_ROOT" \
  --output-root "$OUT_DIR"
