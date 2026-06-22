# Self-Update Status Output

## Why

The release-installed `codex-switch` wrapper already performs self-update
checks, but when the installed bundle is already current the check is silent.
Users cannot tell whether a run skipped the update path, checked and found no
update, or failed before ordinary command output started.

## What Changes

- Print concise self-update status messages to stderr when a self-update check
  actually runs.
- Show a check-start message before downloading or staging the configured
  bundle.
- Show an "already up to date" message when the staged bundle version matches
  the current installed version.
- Keep existing successful sync and failure warning messages.
- Keep explicitly skipped invocations quiet.

## Target State

When a release-installed `codex-switch` command checks self-update, users see
the self-update state before ordinary command output. A current install prints
that it is already up to date, a changed install prints the version sync, and a
failed check prints the existing warning before continuing.

## Scope

In scope:

- Wrapper self-update status output.
- Regression tests for same-version and sync-needed status output.
- README, skill docs, OpenSpec artifacts, workflow state, and verification
  evidence.

Out of scope:

- Changing the self-update frequency policy.
- Changing internal Codex CLI update behavior.
- Changing install path or symlink semantics.

## Completion Contract

- [ ] A same-version self-update check prints "checking" and "already up to
      date" status to stderr.
- [ ] A sync-needed self-update check prints "checking" and the existing
      synced-version status to stderr.
- [ ] Explicitly skipped invocations remain quiet.
- [ ] Focused regressions, full tests, shell syntax checks, package generation,
      JSON validation, and OpenSpec validation pass.
