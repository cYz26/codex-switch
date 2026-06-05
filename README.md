# codex-switch

Project-agnostic Codex workstation CLI for switching Codex profiles, managing
profile auth snapshots, binding CLI/App binaries, and updating the internal
Codex CLI.

## Install

```bash
curl -fsSL "https://github.com/cYz26/codex-switch/releases/latest/download/install.sh" | bash
```

The installer writes the implementation to
`~/.local/share/codex-switch/current` and creates
`~/.local/bin/codex-switch`.

Useful installer overrides:

```bash
CODEX_SWITCH_INSTALL_DIR="$HOME/.local/bin"
CODEX_SWITCH_LIB_DIR="$HOME/.local/share/codex-switch"
CODEX_SWITCH_VERSION="v0.1.1"
CODEX_SWITCH_TARBALL_URL="https://example.com/codex-switch.tar.gz"
CODEX_SWITCH_SOURCE_DIR="/path/to/local/codex-switch"
CODEX_SWITCH_DRY_RUN=1
```

## Usage

```bash
codex-switch status
codex-switch internal
codex-switch official
codex-switch check-update
codex-switch update-internal --dry-run
codex-switch env check-internal
```

`codex-switch internal` checks the internal profile's bound Codex CLI and
automatically delegates to `codex-switch update-internal` when a newer internal
release is detected.

## Development

```bash
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
python3 -m py_compile scripts/*.py
python3 scripts/test_codex_profile_switch.py
bash -n install.sh
```

Package a release tarball:

```bash
scripts/package-release.sh
```
