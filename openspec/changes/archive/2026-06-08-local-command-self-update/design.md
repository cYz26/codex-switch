# Design: Local Command Self Update

## Approach

The Bash wrapper owns self-update because it is the first code that runs for the
persistent `codex-switch` command. The wrapper will only auto-sync when its
resolved `SCRIPT_DIR` equals `${CODEX_SWITCH_LIB_DIR:-~/.local/share/codex-switch}/current/scripts`.
That keeps source checkouts and local development paths immutable by default.

## Sync Source

The sync source follows the existing installer and remote runner contract:

- `CODEX_SWITCH_SOURCE_DIR` copies a local source tree for tests and local
  debugging.
- `CODEX_SWITCH_SELF_UPDATE_TARBALL_URL` or `CODEX_SWITCH_TARBALL_URL` points to
  a tarball.
- `CODEX_SWITCH_VERSION` pins a GitHub release tag when no explicit tarball URL
  is provided.
- `CODEX_SWITCH_GITHUB_PROXY` sets `http_proxy` and `https_proxy` when needed.

The extracted tree must contain executable `scripts/codex-switch`.

## Interval and Skip Rules

The wrapper writes a timestamp under the implementation library directory and
uses `CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS`, defaulting to one day. A value
of `0` forces a check on every eligible invocation.

The check is skipped when:

- `CODEX_SWITCH_SKIP_SELF_UPDATE` is truthy.
- global option `--skip-self-update` is present.
- the wrapper has already re-execed after a sync attempt.
- the command is help, version, install, or shim-env.
- the wrapper is not running from the release implementation directory.

`run.sh` exports `CODEX_SWITCH_SKIP_SELF_UPDATE=1` when it dispatches the
bundled wrapper because it already prepared the implementation directory.

## Update Semantics

Normal command execution treats sync errors as warnings. If the remote release
cannot be downloaded, the archive is invalid, or replacement fails, the command
continues with the currently installed implementation. If a sync succeeds, the
wrapper re-execs itself once with the original arguments so the user command
runs against the freshly synced scripts.

The replacement is staged in a temporary directory and swaps `current` through a
backup path so a failed replace restores the previous implementation.

## Testing

Regression tests create a fake release-installed layout and a fake remote
tarball. They verify:

- eligible local commands sync `current`, then execute the synced script.
- `--skip-self-update` preserves the old implementation.
- `run.sh` dispatches with self-update disabled.
