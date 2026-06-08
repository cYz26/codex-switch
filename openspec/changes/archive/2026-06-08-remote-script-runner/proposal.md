# Remote Script Runner

## Why

Other projects should be able to invoke `codex-switch` without vendoring this
repository or requiring a pre-existing PATH install. The current install flow is
good for persistent setup, but it does not provide a one-line remote execution
entrypoint such as `curl .../run.sh | bash -s -- status`.

## What Changes

- Add a remote runner script that downloads or copies the release bundle into a
  stable local implementation directory and then executes `scripts/codex-switch`
  with the provided arguments.
- Keep install behavior separate: the runner does not create the public
  `~/.local/bin/codex-switch` symlink.
- Include the runner in release output so it can be published as a direct GitHub
  release asset.
- Document usage from any project directory.

## Target State

Users can run:

```bash
curl -fsSL "https://github.com/cYz26/codex-switch/releases/latest/download/run.sh" | bash -s -- status
```

The script fetches the matching release tarball, places it under
`~/.local/share/codex-switch/current` by default, and executes
`~/.local/share/codex-switch/current/scripts/codex-switch` with the supplied
arguments. It supports the same release override environment variables as the
installer where practical.

## Scope

- In scope: remote runner script, packaging, docs, regression tests.
- Out of scope: changing profile-switching semantics, adding production
  dependencies, or publishing a release from this task.

## Completion Contract

- [x] Remote runner executes a packaged `codex-switch` command with arguments.
- [x] Remote runner bootstraps to a stable local directory instead of a transient
      temp path.
- [x] Install symlink behavior remains owned by `install.sh`, not `run.sh`.
- [x] Release package output includes the runner.
- [x] Verification evidence is recorded before archive.
