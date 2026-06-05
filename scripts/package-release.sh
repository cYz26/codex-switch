#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="${CODEX_SWITCH_DIST_DIR:-$REPO_ROOT/dist}"
PACKAGE_DIR="$OUT_DIR/codex-switch"
TARBALL="$OUT_DIR/codex-switch.tar.gz"

rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR" "$OUT_DIR"

cp "$REPO_ROOT/README.md" "$PACKAGE_DIR/"
cp "$REPO_ROOT/SKILL.md" "$PACKAGE_DIR/"
cp "$REPO_ROOT/VERSION" "$PACKAGE_DIR/"
cp -R "$REPO_ROOT/agents" "$PACKAGE_DIR/"
cp -R "$REPO_ROOT/evals" "$PACKAGE_DIR/"
cp -R "$REPO_ROOT/scripts" "$PACKAGE_DIR/"
rm -rf "$PACKAGE_DIR/scripts/__pycache__"

tar -C "$OUT_DIR" -czf "$TARBALL" codex-switch
echo "$TARBALL"
