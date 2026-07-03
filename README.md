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

Persistent local commands installed by `install.sh` also check for a
codex-switch implementation self-update before every ordinary command execution.
A release-installed wrapper syncs `~/.local/share/codex-switch/current` from the
configured release tarball when a newer bundle is available, and re-runs the
original command against the synced wrapper. Source checkout usage such as
`scripts/codex-switch status` does not self-modify.

When a self-update check runs, status is printed to stderr before the command's
normal output. A current install reports `codex-switch self-update: already up
to date <version>`; an updated install reports the synced version transition.
Explicitly skipped checks stay quiet.

Self-update controls:

```bash
codex-switch --skip-self-update status
CODEX_SWITCH_SKIP_SELF_UPDATE=1 codex-switch status
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
markers, and vendor/update caches from generic cross-home sync plans. Desktop
settings stored in `.codex-global-state.json` are merged as a sanitized settings
subset; prompt history, thread permissions, queued follow-ups, remote thread
summaries, credentials, and remote routing identifiers stay profile-local. The
Desktop Settings Pets support directory `pets/` is treated as stable settings
support and can sync across homes.
Shared support sync also refuses to copy self-referential symlinks or symlinks
that point back into the target home, so profile switches do not create symlink
loops.

Internal Codex binary upgrades are compatibility checkpoints. When
`codex-switch update-internal` or a manual profile edit changes the internal
profile's configured `codex_bin`, re-check internal Desktop compatibility
instead of assuming the existing shim still applies.

```bash
codex-switch --skip-self-update status
codex-switch internal --skip-update-check
codex-switch --skip-self-update verify internal --responses-tool-smoke --report
```

For each internal binary upgrade, verify the actual Desktop App bundle binary,
the internal `codex_bin`, the generated app wrapper, and the running
app-server path. Re-compare Desktop bundle and internal app-server schemas when
request compatibility may have changed, then update or remove proxy
conversions such as namespace dynamic tool flattening, unsupported marketplace
kind filtering, model alias handling, and app-server flag routing as needed.
Finish with a real internal Desktop switch test and the focused regression
tests that cover the affected compatibility path.

If internal mode fails only after a tool call with an Azure message saying the
requested item was created under a different Azure OpenAI resource, use the
Responses tool-follow-up smoke and the troubleshooting note in
`docs/troubleshooting/internal-azure-responses-resource-stickiness.md`. That
scenario usually means AIDP routed one Responses context across different Azure
resources; codex-switch records sanitized routing evidence, while the durable
fix belongs in AIDP/internal backend resource stickiness.

As of 2026-07-03, internal release `0.142.5` is treated as a known-bad default
upgrade target for this workstation flow. `codex-switch internal` keeps or
installs pinned fallback `0.142.4` while `internal-rust-v0.142.5` remains the
latest release, then resumes ordinary latest auto-update when a later internal
release appears. Override only for explicit testing with:

```bash
CODEX_SWITCH_INTERNAL_BLOCKED_VERSIONS= codex-switch internal
codex-switch update-internal --version 0.142.5
```

Profile switches write a `codex` shim under `~/.codex-switch/bin` and install
an idempotent managed block in the shell startup file so newly opened shells
prefer that shim over older binaries earlier on PATH. To align an already-open
shell immediately, run:

```bash
eval "$(codex-switch shim-env)"
codex-switch --skip-self-update status
```

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

Plugin enablement and plugin installation are separate layers. Profile
switching syncs shared plugin configuration such as marketplaces, enabled
plugins, skill config, and hook trust into the target `config.toml`, but it
does not copy or symlink another profile's `plugins/` cache. One-key switches
(`codex-switch internal` and `codex-switch official`) run plugin repair after a
successful switch, before doctor, by refreshing the target profile's
marketplace/catalog view and installing missing enabled plugins into the target
profile home. Use `--skip-plugin-repair` to skip that repair step.

The explicit repair command is:

```bash
codex-switch repair-plugins <profile>
```

That command runs the profile's configured Codex binary with `CODEX_HOME` set
to the profile home. It first refreshes configured plugin marketplaces with
`codex plugin marketplace upgrade --json`, primes the available plugin catalog
with `codex plugin list --available --json`, and then installs missing enabled
plugins through `codex plugin add` only when they are present in the refreshed
available plugin catalog. Enabled plugins that are no longer available from the
configured marketplaces are skipped by repair and remain visible to
`codex-switch doctor` as active-profile materialization issues. This keeps
uninstalled official plugins visible in the target profile without copying
another profile's `plugins/` directory. `codex-switch doctor` still checks the
active profile's plugin materialization state and reports this command if
enabled plugins are missing, including after low-level
`codex-switch switch <profile>` invocations that bypass the one-key
post-switch flow. `codex-switch internal --help` and
`codex-switch official --help` are pure help paths and do not run update,
switch, plugin repair, doctor, or status steps.

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
