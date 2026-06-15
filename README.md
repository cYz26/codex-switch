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
codex-switch restore <backup-id> --dry-run
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

When a self-update check runs, status is printed to stderr before the command's
normal output. A current install reports `codex-switch self-update: already up
to date <version>`; an updated install reports the synced version transition.
Explicitly skipped checks and interval-skipped checks stay quiet.

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

Release assets are published by GitHub Actions. When release-relevant changes
land on `main`, the automatic release workflow verifies the repository, bumps
`VERSION` to the next patch version, creates the matching `v*` tag, runs
`scripts/package-release.sh`, and uploads `install.sh`, `run.sh`, and
`codex-switch.tar.gz` to the matching GitHub release. Planning, OpenSpec,
verification, and docs-only changes do not create a release. A manually pushed
`v*` tag still runs the tag release workflow for explicit reruns.

## Config Model

Profile switching uses independent Codex homes.

`codex-switch official` keeps official mode on the official Codex home,
defaulting to `~/.codex`, and uses the official Codex.app CLI path when it is
available. `codex-switch internal` prepares and activates a managed internal
home at `~/.codex-switch/homes/internal` by default. The shell shim and Codex
Desktop binding are switched to the target profile's effective home.

Only shareable non-auth configuration and stable support files move between the
official and internal homes. Auth files, sessions, history, logs, sqlite state,
temporary/browser/process state, and profile-specific model/provider layers are
not shared across modes. Codex-switch also excludes bulky or credential-like
support state such as `agent-kb`, `plugins`, `computer-use`, `cache`,
`model-catalogs`, `.credentials.json`, global state files, installation/version
markers, and vendor/update caches from cross-home sync plans. Shared support
sync also refuses to copy self-referential symlinks or symlinks that point back
into the target home, so profile switches do not create symlink loops.

When switching, the target home `config.toml` is generated by merging shared
settings from the source home with profile-specific settings from the target
profile's last valid runtime `config.toml`. If the target runtime config is
missing or invalid, codex-switch falls back to
`~/.codex-switch/profiles/<profile>/config.toml`. After a successful validated
switch, that canonical profile config is refreshed from the runtime config so
future fallback data stays current. The internal Codex Desktop wrapper may fold
shared app-home settings back into the official home, but it preserves official
profile-specific runtime settings such as `model` and `personality`. When a
profile-specific runtime setting is removed, refresh preserves that removal
instead of resurrecting an older fallback value; auth storage metadata is kept
as structural profile metadata.

Generated TOML keeps managed `# codex-switch:` comments. These comments mark
which settings came from the shared layer and which settings are
profile-specific; they are only annotations, and the file remains normal TOML.

For legacy users who have always used the internal profile in `~/.codex`,
`internal` can adopt that existing home:

```bash
codex-switch internal --internal-codex-home ~/.codex
```

When `internal` adopts the same path that `openai-official` would otherwise use,
codex-switch assigns `openai-official` to
`~/.codex-switch/homes/openai-official` and persists both home bindings in the
profile manifests. If both profiles are explicitly assigned the same directory,
codex-switch prompts for a different directory in an interactive terminal and
rejects the switch before mutation when no prompt is available. Interactive
selection prompts for the target profile first, lists the recommended directory
first with a recommendation marker, then offers the other profile's current
directory and a custom path. The semantic defaults are `~/.codex` for
`openai-official` and `~/.codex-switch/homes/internal` for `internal`; those
defaults are recommended first unless the directory is forbidden by the current
active-profile conflict. Persisted home bindings created by migration or
automatic collision handling are prompted for confirmation the next time an
interactive switch can ask. When switching from one active profile to another,
the target profile must use a different home from the current active profile;
interactive switches ask for a different target home, while non-interactive
real switches fail before mutation.

Every non-dry-run switch creates a backup first. The backup includes all paths
that the switch plans to write, delete, replace, link, or unlink, plus a
`backup.json` manifest with path metadata. If backup capture fails, switching
aborts before applying the mutation plan. Use `--dry-run` to print both the
backup plan and mutation plan.

Restore a switch backup explicitly:

```bash
codex-switch restore <backup-id> --dry-run
codex-switch restore <backup-id> --apply
codex-switch restore <backup-id> --apply --force
```

By default restore refuses to overwrite paths that no longer match the
post-switch state recorded in the backup. Use `--force` only when you have
reviewed the dry-run output and accept replacing those current paths.

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
