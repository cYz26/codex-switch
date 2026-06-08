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
CODEX_SWITCH_VERSION="v0.1.3"
CODEX_SWITCH_TARBALL_URL="https://example.com/codex-switch.tar.gz"
CODEX_SWITCH_SOURCE_TARBALL_URL="https://github.com/cYz26/codex-switch/archive/refs/tags/v0.1.3.tar.gz"
CODEX_SWITCH_SOURCE_DIR="/path/to/local/codex-switch"
CODEX_SWITCH_DRY_RUN=1
```

If the release bundle asset is unavailable, the installer can fall back to a
source archive. When the source archive contains `scripts/package-release.sh`,
the installer packages it locally before installing the implementation.

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

Persistent local commands installed by `install.sh` also perform a bounded
codex-switch implementation self-update before ordinary command execution. By
default, a release-installed wrapper checks at most once per day, syncs
`~/.local/share/codex-switch/current` from the configured release tarball when a
newer bundle is available, and re-runs the original command against the synced
wrapper. Source checkout usage such as `scripts/codex-switch status` does not
self-modify.

Self-update controls:

```bash
codex-switch --skip-self-update status
CODEX_SWITCH_SKIP_SELF_UPDATE=1 codex-switch status
CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS=0 codex-switch status
CODEX_SWITCH_TARBALL_URL="https://example.com/codex-switch.tar.gz" codex-switch status
CODEX_SWITCH_SOURCE_TARBALL_URL="https://github.com/cYz26/codex-switch/archive/refs/tags/v0.1.3.tar.gz" codex-switch status
```

Self-update failures are warnings for ordinary commands; the current local
implementation continues to run. If the configured release bundle is missing
and a source archive fallback is available, self-update stages from the source
archive instead.

Run without installing a PATH command:

```bash
curl -fsSL "https://github.com/cYz26/codex-switch/releases/latest/download/run.sh" | bash -s -- status
curl -fsSL "https://github.com/cYz26/codex-switch/releases/latest/download/run.sh" | bash -s -- internal
curl -fsSL "https://github.com/cYz26/codex-switch/releases/latest/download/run.sh" | bash -s -- official --dry-run
```

The remote runner downloads the release bundle to
`~/.local/share/codex-switch/current` and executes the bundled
`scripts/codex-switch`. It does not create `~/.local/bin/codex-switch`; use the
installer when you want a persistent PATH command. Like the installer, it can
fall back to a source archive when the release bundle asset is unavailable.

Release assets are published by GitHub Actions when a `v*` tag is pushed. The
workflow verifies the repository, runs `scripts/package-release.sh`, and uploads
`install.sh`, `run.sh`, and `codex-switch.tar.gz` to the matching GitHub
release.

## Config Model

Profile switching keeps `config.toml` as the shared workstation configuration.
Plugin marketplace entries, enabled plugin state, skill config, hook trust
state, projects, UI preferences, MCP servers, and other non-auth settings stay
shared across `internal` and `official`. Profile-specific auth/model settings
are written to `<profile>.config.toml` and layered onto the shared base during
switching.

When the internal Desktop profile uses `~/.codex-switch/bin/codex-internal-app`,
`codex-switch internal` refreshes that wrapper so the app-specific
`CODEX_HOME` is rebuilt from the shared live config plus `internal.config.toml`.
Before each Desktop launch, the wrapper also folds non-auth shared settings that
Codex Desktop wrote into the app home back into the live shared config. This
keeps plugins, hook trust, feature flags, MCP servers, project trust, and UI
preferences visible after restarting Codex Desktop while still keeping official
`auth.json` out of the internal app home.

## Development

```bash
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
python3 -m py_compile scripts/*.py
python3 scripts/test_codex_profile_switch.py
bash -n install.sh
bash -n run.sh
```

Package a release tarball:

```bash
scripts/package-release.sh
```
