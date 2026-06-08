#!/usr/bin/env bash
set -euo pipefail

REPO_TARBALL_BASE="https://github.com/cYz26/codex-switch/releases"
LIB_DIR="${CODEX_SWITCH_LIB_DIR:-$HOME/.local/share/codex-switch}"
INSTALL_VERSION="${CODEX_SWITCH_VERSION:-}"
SOURCE_DIR="${CODEX_SWITCH_SOURCE_DIR:-}"
TARBALL_URL="${CODEX_SWITCH_TARBALL_URL:-}"
DRY_RUN="${CODEX_SWITCH_DRY_RUN:-0}"
PROXY_URL="${CODEX_SWITCH_GITHUB_PROXY:-}"

if [[ -z "$TARBALL_URL" ]]; then
  if [[ -n "$INSTALL_VERSION" ]]; then
    TARBALL_URL="$REPO_TARBALL_BASE/download/$INSTALL_VERSION/codex-switch.tar.gz"
  else
    TARBALL_URL="$REPO_TARBALL_BASE/latest/download/codex-switch.tar.gz"
  fi
fi

is_dry_run() {
  [[ "$DRY_RUN" == 1 || "$DRY_RUN" == "true" ]]
}

print_cmd() {
  printf '[DRY-RUN]'
  printf ' %q' "$@"
  printf '\n'
}

copy_source() {
  local src="$1"
  local dest="$2"
  local staged="${dest}.tmp.$$"

  if [[ ! -x "$src/scripts/codex-switch" ]]; then
    echo "Invalid codex-switch source directory: $src" >&2
    exit 1
  fi

  if is_dry_run; then
    print_cmd rm -rf "$staged"
    print_cmd mkdir -p "$(dirname "$dest")"
    print_cmd cp -R "$src" "$staged"
    print_cmd rm -rf "$dest"
    print_cmd mv "$staged" "$dest"
    return
  fi

  rm -rf "$staged"
  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$staged"
  rm -rf "$staged/scripts/__pycache__"
  rm -rf "$dest"
  mv "$staged" "$dest"
}

download_source() {
  local dest="$1"
  local tmp
  tmp="$(mktemp -d)"

  if [[ -n "$PROXY_URL" ]]; then
    export https_proxy="${https_proxy:-$PROXY_URL}"
    export http_proxy="${http_proxy:-$PROXY_URL}"
  fi

  if is_dry_run; then
    print_cmd curl -fsSL "$TARBALL_URL" -o "$tmp/codex-switch.tar.gz"
    print_cmd tar -xzf "$tmp/codex-switch.tar.gz" -C "$tmp"
    print_cmd install extracted codex-switch to "$dest"
    return
  fi

  curl -fsSL "$TARBALL_URL" -o "$tmp/codex-switch.tar.gz"
  tar -xzf "$tmp/codex-switch.tar.gz" -C "$tmp"
  local src
  if [[ -d "$tmp/codex-switch" ]]; then
    src="$tmp/codex-switch"
  else
    src="$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  fi
  if [[ -z "$src" || ! -x "$src/scripts/codex-switch" ]]; then
    echo "Downloaded archive does not contain scripts/codex-switch" >&2
    exit 1
  fi
  copy_source "$src" "$dest"
  rm -rf "$tmp"
}

main() {
  local target_lib="$LIB_DIR/current"
  local target_cmd="$target_lib/scripts/codex-switch"

  if [[ -n "$SOURCE_DIR" ]]; then
    copy_source "$SOURCE_DIR" "$target_lib"
  else
    download_source "$target_lib"
  fi

  if is_dry_run; then
    print_cmd exec "$target_cmd" "$@"
    return
  fi

  CODEX_SWITCH_SKIP_SELF_UPDATE=1 exec "$target_cmd" "$@"
}

main "$@"
