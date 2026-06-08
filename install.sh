#!/usr/bin/env bash
set -euo pipefail

REPO_TARBALL_BASE="https://github.com/cYz26/codex-switch/releases"
REPO_SOURCE_BASE="https://github.com/cYz26/codex-switch/archive"
INSTALL_DIR="${CODEX_SWITCH_INSTALL_DIR:-$HOME/.local/bin}"
LIB_DIR="${CODEX_SWITCH_LIB_DIR:-$HOME/.local/share/codex-switch}"
INSTALL_VERSION="${CODEX_SWITCH_VERSION:-}"
SOURCE_DIR="${CODEX_SWITCH_SOURCE_DIR:-}"
TARBALL_URL="${CODEX_SWITCH_TARBALL_URL:-}"
SOURCE_TARBALL_URL="${CODEX_SWITCH_SOURCE_TARBALL_URL:-}"
DRY_RUN="${CODEX_SWITCH_DRY_RUN:-0}"
PROXY_URL="${CODEX_SWITCH_GITHUB_PROXY:-}"

if [[ -z "$TARBALL_URL" ]]; then
  if [[ -n "$INSTALL_VERSION" ]]; then
    TARBALL_URL="$REPO_TARBALL_BASE/download/$INSTALL_VERSION/codex-switch.tar.gz"
  else
    TARBALL_URL="$REPO_TARBALL_BASE/latest/download/codex-switch.tar.gz"
  fi
fi

run_cmd() {
  if [[ "$DRY_RUN" == 1 || "$DRY_RUN" == "true" ]]; then
    printf '[DRY-RUN]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

is_dry_run() {
  [[ "$DRY_RUN" == 1 || "$DRY_RUN" == "true" ]]
}

copy_source() {
  local src="$1"
  local dest="$2"
  if [[ ! -x "$src/scripts/codex-switch" ]]; then
    echo "Invalid codex-switch source directory: $src" >&2
    exit 1
  fi
  run_cmd rm -rf "$dest"
  run_cmd mkdir -p "$(dirname "$dest")"
  run_cmd cp -R "$src" "$dest"
}

source_tarball_url() {
  if [[ -n "$SOURCE_TARBALL_URL" ]]; then
    printf '%s\n' "$SOURCE_TARBALL_URL"
  elif [[ -n "$INSTALL_VERSION" ]]; then
    printf '%s/refs/tags/%s.tar.gz\n' "$REPO_SOURCE_BASE" "$INSTALL_VERSION"
  else
    printf '%s/refs/heads/main.tar.gz\n' "$REPO_SOURCE_BASE"
  fi
}

copy_packaged_source() {
  local src="$1"
  local dest="$2"
  local dist

  if [[ -x "$src/scripts/package-release.sh" ]]; then
    dist="$(mktemp -d)"
    if CODEX_SWITCH_DIST_DIR="$dist" "$src/scripts/package-release.sh" >/dev/null; then
      if [[ -x "$dist/codex-switch/scripts/codex-switch" ]]; then
        copy_source "$dist/codex-switch" "$dest"
        rm -rf "$dist"
        return
      fi
    fi
    rm -rf "$dist"
  fi

  copy_source "$src" "$dest"
}

install_archive() {
  local url="$1"
  local dest="$2"
  local mode="$3"
  local tmp src
  tmp="$(mktemp -d)"

  if [[ -n "$PROXY_URL" ]]; then
    export https_proxy="${https_proxy:-$PROXY_URL}"
    export http_proxy="${http_proxy:-$PROXY_URL}"
  fi

  if is_dry_run; then
    printf '[DRY-RUN] curl -fsSL "%s" -o "%s/codex-switch.tar.gz"\n' "$url" "$tmp"
    printf '[DRY-RUN] tar -xzf "%s/codex-switch.tar.gz" -C "%s"\n' "$tmp" "$tmp"
    printf '[DRY-RUN] install extracted codex-switch to "%s"\n' "$dest"
    rm -rf "$tmp"
    return
  fi

  if ! curl -fsSL "$url" -o "$tmp/codex-switch.tar.gz"; then
    rm -rf "$tmp"
    return 1
  fi
  if ! tar -xzf "$tmp/codex-switch.tar.gz" -C "$tmp"; then
    rm -rf "$tmp"
    return 1
  fi
  if [[ -d "$tmp/codex-switch" ]]; then
    src="$tmp/codex-switch"
  else
    src="$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  fi
  if [[ -z "$src" || ! -x "$src/scripts/codex-switch" ]]; then
    echo "Downloaded archive does not contain scripts/codex-switch" >&2
    rm -rf "$tmp"
    return 1
  fi
  if [[ "$mode" == "source" ]]; then
    copy_packaged_source "$src" "$dest"
  else
    copy_source "$src" "$dest"
  fi
  rm -rf "$tmp"
}

download_source() {
  local dest="$1"
  local fallback_url

  if install_archive "$TARBALL_URL" "$dest" "bundle"; then
    return
  fi

  fallback_url="$(source_tarball_url)"
  if [[ -n "$fallback_url" ]]; then
    echo "codex-switch install: release bundle unavailable; trying source archive fallback" >&2
    if install_archive "$fallback_url" "$dest" "source"; then
      return
    fi
  fi

  echo "codex-switch install: failed to download release bundle or source archive" >&2
  exit 1
}

main() {
  local target_lib="$LIB_DIR/current"
  local target_bin="$INSTALL_DIR/codex-switch"

  if [[ -n "$SOURCE_DIR" ]]; then
    copy_source "$SOURCE_DIR" "$target_lib"
  else
    download_source "$target_lib"
  fi

  run_cmd mkdir -p "$INSTALL_DIR"
  run_cmd ln -sfn "$target_lib/scripts/codex-switch" "$target_bin"
  echo "Installed codex-switch: $target_bin -> $target_lib/scripts/codex-switch"
  echo "Run: codex-switch status"
}

main "$@"
