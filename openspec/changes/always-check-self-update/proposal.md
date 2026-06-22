# Always Check Self-Update

## Why

Persistent release-installed `codex-switch` commands currently use a daily
self-update cooldown. That reduces network checks, but it also means a local
install can stay stale for the remainder of the cooldown after a release lands.
The requested target is simpler: every ordinary release-installed command checks
whether the implementation needs to sync before running.

## What Changes

- Remove the self-update interval/cooldown gate from the local wrapper.
- Keep release-install eligibility checks unchanged, so source checkout commands
  still do not self-modify.
- Keep explicit skip controls: `--skip-self-update`,
  `CODEX_SWITCH_SKIP_SELF_UPDATE=1`, and remote runner redundant-check
  suppression.
- Stop documenting `CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS` as an active
  self-update control.

## Target State

Every ordinary command executed through a release-installed `codex-switch`
wrapper checks the configured release source before command execution. If the
bundle is current, stderr reports the already-current status. If a newer bundle
is available, the wrapper syncs and re-execs once. Explicit skip paths stay
quiet and source checkout usage remains non-mutating.

## Scope

In scope:

- Local wrapper self-update frequency.
- Regression coverage for repeated invocations.
- README, skill docs, OpenSpec spec, workflow state, and verification evidence.

Out of scope:

- Internal Codex CLI update behavior.
- Install path, symlink, release asset, or source fallback semantics.
- New dependencies or background update daemons.

## Completion Contract

- [ ] Repeated eligible release-installed command invocations check self-update
      every time.
- [ ] Explicit skip controls still suppress self-update output and sync.
- [ ] Source checkout commands still do not self-modify.
- [ ] Focused regressions, full tests, shell syntax checks, package generation,
      diff check, and OpenSpec validation pass.
