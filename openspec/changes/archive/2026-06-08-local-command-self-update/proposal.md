# Local Command Self Update

## Why

Other projects can now invoke `codex-switch` directly through the remote
`run.sh`, but projects such as `app_ai_doctor` intentionally use a persistent
local `codex-switch` command. That local command can become stale after a new
release, so normal command execution needs a bounded way to sync the installed
implementation with the remote release bundle.

## What Changes

- Add a local command self-update check for release-installed `codex-switch`
  wrappers.
- Keep source-tree usage safe: `scripts/codex-switch` from this repository does
  not rewrite the working tree.
- Use a cached interval so ordinary commands do not perform network work every
  time.
- Provide explicit opt-out for scripts and for the remote runner, which already
  downloads the release bundle before dispatching.
- Keep update failures non-blocking for normal commands; an unavailable GitHub
  release should not prevent status, switch, or doctor workflows from running.

## Target State

When users run a persistent local command such as `codex-switch status`, the
wrapper checks whether it is running from the release implementation directory.
If it is, and the check interval has elapsed, the wrapper downloads or copies
the configured release bundle, replaces the stable `current` implementation
directory, and re-execs the command once against the synced wrapper. If the
sync cannot complete, the wrapper records the attempt and continues with the
currently installed implementation.

## Scope

- In scope: local wrapper self-update, run.sh skip behavior, docs, tests,
  OpenSpec artifacts, verification evidence.
- Out of scope: publishing a GitHub release, changing internal Codex CLI update
  semantics, or making source checkout commands rewrite the repository.

## Completion Contract

- [ ] Local release-installed commands can sync from the remote release bundle.
- [ ] Self-update is skipped for source-tree execution unless explicitly forced
      by environment configuration.
- [ ] Self-update can be skipped with an environment variable or global CLI
      option.
- [ ] Remote `run.sh` avoids a redundant self-update check.
- [ ] Failures to reach the release bundle do not block normal local commands.
- [ ] Regression tests, shell syntax checks, packaging, and OpenSpec validation
      pass.
