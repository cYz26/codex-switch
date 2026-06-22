# Design: Always Check Self-Update

## Skill Routing Ledger

- Request kind: user-visible CLI behavior change.
- Workflow mode: brownfield OpenSpec change with TDD.
- capability-research: skipped; no external or platform capability decision is
  needed. Local source, docs, and installed wrapper behavior provide the
  authority for this change.
- brainstorming: used in minimal form; the user supplied the target behavior
  directly, so no unresolved design alternatives remain.
- writing-plans: used; this canonical OpenSpec design/tasks file is the plan
  artifact per repository instructions.
- OpenSpec/GSD routing: OpenSpec required because self-update compatibility and
  user-visible CLI behavior change. GSD phase planning skipped because this is a
  narrow single-change repair.

## Target State

Release-installed `codex-switch` wrappers run self-update eligibility and sync
logic on every ordinary command invocation. The wrapper no longer reads or
writes a cooldown stamp before deciding whether to check. Explicit skips and
non-release source checkout detection remain unchanged.

## Scope / Non-Goals

- Do not change how release tarball URLs or source archive fallbacks are
  resolved.
- Do not change internal Codex CLI update checks.
- Do not introduce a separate status command or persistent update log.
- Do not remove the existing non-blocking failure contract.

## Architecture Decisions

- Remove the interval gate from the Bash wrapper rather than setting the default
  interval to zero. This avoids keeping a public no-op cooldown policy in the
  implementation.
- Leave `--skip-self-update`, `CODEX_SWITCH_SKIP_SELF_UPDATE=1`, and
  `CODEX_SWITCH_SELF_UPDATE_REEXECED=1` unchanged because they serve different
  purposes: scripting control and re-exec loop prevention.
- Treat the existing `.last-self-update-check` file as legacy state. The new
  wrapper simply ignores it.

## Completion Contract

- The wrapper checks self-update on consecutive eligible invocations even when a
  prior invocation just checked.
- The wrapper still prints the check-start and already-current/synced status
  lines when checks run.
- Skip controls stay quiet.
- Source checkout usage does not rewrite the repository.
- Verification evidence is recorded before completion.

## Capability Slices

1. Add a RED regression test for repeated eligible invocations.
2. Remove cooldown gate and stamp writes from `scripts/codex-switch`.
3. Update docs and stable/OpenSpec specs.
4. Run focused and full verification, then update workflow state.

## Risks / Rollback

This increases network checks for ordinary release-installed commands. Rollback
is straightforward: restore the interval gate and stamp check, then restore the
old docs/spec wording.
