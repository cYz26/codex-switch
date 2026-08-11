## Why

`codex-switch split` currently stages a newer internal binary but refuses to
promote it unless that binary also passes the full Codex Desktop/App parity
contract. The supported split target is narrower: internal is required only
for shell CLI use, while Codex App remains bound to the official bundle, so an
unrelated internal-App compatibility gate can make a valid CLI update fail.

## What Changes

- Make the automatic internal update performed by `codex-switch split` use an
  atomic CLI-only promotion contract: validate the candidate as a CLI, swap the
  bound internal executable, and roll back on a failed CLI postcondition.
- Record that the promoted internal generation is not verified for Codex App
  without regenerating or mutating Desktop wrappers, parity artifacts,
  LaunchAgent state, App global state, or the official App binding.
- Treat internal Desktop parity as not applicable when the active selection is
  internal CLI plus official App; verify, Doctor, and status continue to check
  the internal CLI and the independently owned official App surface.
- Fail closed before any App mutation when a requested selection would bind
  Codex App to an internal generation whose App readiness is unverified.
- Preserve the existing full-parity promotion path for explicit internal-App
  workflows; this change does not implement, repair, or claim internal-App
  compatibility.
- Validate internal executables with a stable streaming digest under an
  executable-specific safety bound instead of the bounded text-artifact reader,
  so a valid production-sized CLI is not rejected or buffered in memory.
- Make both the prepared CLI-only promotion postcondition and the final split
  runtime smoke exercise the same managed CLI-generation contract used by the
  installed shell shim; an unusable managed generation must roll back or fail
  the command instead of being reported as successful.
- Make successful completion guidance follow the actual App effect: a preserved
  official App binding has no restart step, while a real App rebind retains
  restart/open guidance.
- Keep `internal-official-feature-parity` as historical paused work rather than
  rewriting its Desktop-parity intent or prior evidence.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: Split-mode internal updates become CLI-scoped, diagnostics
  apply parity only to an active internal App surface, and unverified internal
  App selection fails before mutation.

## Impact

- Public behavior: `codex-switch split` and `split --keep-version`, plus
  verify/Doctor/status output for the supported internal-CLI/official-App
  selection.
- Runtime code: wrapper update orchestration, internal promotion, runtime
  binding transaction metadata, switch preflight, and diagnostics.
- State: existing additive internal-manifest App-readiness metadata tied to the
  promoted backend identity; schema-v1 CLI generations and legacy manifests
  remain readable, with no repair migration.
- Tests and docs: focused Bash/Python regressions, README, and repository skill
  guidance.
- No new dependency, live binary promotion, workstation switch, App restart,
  install, release, archive, commit, push, provider traffic, or cache cleanup is
  authorized by this change.
