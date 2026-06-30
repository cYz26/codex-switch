# Switch verification contract

## Why

Recent official/internal profile switching repairs exposed that a switch can
look successful while the machine still has contaminated profile config,
missing shared plugin support snapshots, stale Desktop app-server bindings, or
an unverified internal backend after a Codex CLI upgrade. The switch workflow
needs a first-class verification contract so future switches and backend
upgrades fail with actionable diagnostics instead of relying on post-hoc manual
inspection.

## What Changes

- Add a `verify <profile>` command that checks the requested target profile
  against active switch state, runtime config, Desktop app binding, plugin
  support snapshots, and optional runtime smoke checks.
- Report missing or invalid profile-local plugin support snapshots, and add a
  safe repair mode that can refresh those snapshots and materialize missing
  enabled plugins through the existing catalog-aware repair path.
- Run verification by default during one-key `codex-switch internal` and
  `codex-switch official` after plugin repair and before doctor.
- Add opt-outs and explicit deeper checks: `--skip-verify`,
  `--runtime-smoke`, `--exec-smoke <prompt>`, and verification reports.
- Record the upgrade boundary: after internal `codex_bin` changes, verification
  must include direct runtime smoke before treating internal mode as healthy.

## Target State

`codex-switch` treats profile switching as an observable state transition. A
real one-key switch validates its own result before reporting success, and a
standalone `verify` command can be run outside a Codex conversation to check or
repair the current workstation state. Full post-upgrade acceptance can opt into
real Codex runtime smoke while ordinary switching remains CLI-first and
non-interactive.

## Scope

- Project mode: brownfield.
- Change type: behavior, CLI workflow, error-handling, compatibility.

## Capability Evidence

- authoritative/current: current local CLI help exposes one-key switching,
  `doctor`, `status`, and `repair-plugins`; there is no existing `verify`
  command.
- local scan: inspected `scripts/codex-switch`,
  `scripts/codex_profile_switch.py`, doctor/status modules, plugin repair,
  profile-home selection, running app-server detection, existing OpenSpec
  `independent-profile-homes` tasks, and current workstation status.
- comparison: current `doctor` finds health problems, but it is not target
  profile aware and does not express switch-specific invariants such as official
  provider contamination or profile support snapshot completeness.

## Non-Goals

- Do not force Codex Desktop to quit or restart.
- Do not run model-backed `codex exec` smoke unless explicitly requested.
- Do not copy plugin cache directories between profiles.
- Do not archive existing OpenSpec changes.

## Completion Contract

- [ ] OpenSpec scenarios cover standalone verify, one-key verification,
      missing snapshot diagnostics, safe repair, reports, and runtime smoke
      boundaries.
- [ ] Regression tests fail before implementation and pass after.
- [ ] One-key switch output includes verification status.
- [ ] Existing doctor, plugin repair, and profile switch behavior remains
      compatible.
- [ ] Verification evidence is recorded and workflow state is updated.

## Risks

- Runtime smoke can trigger external service/model behavior; keep it explicit.
- Verification must distinguish action-required diagnostics from destructive
  automatic fixes.
- Current worktree has uncommitted repairs; keep this follow-up scoped to new
  verification artifacts and related code.
