# Agent Task Contract

## Goal
Make status, Doctor, and verify consume the same read-only shared-configuration authority and expose its generation, state, pending target, and stable finding codes.

## Worker ID
`split-shared-diagnostics-green`

## Scope
Allowed write set for worker `split-shared-diagnostics-green` only:
- `scripts/codex_switch_status.py`
- `scripts/codex_switch_doctor.py`
- `scripts/codex_switch_verify.py`
- Allowed read-only scope: active OpenSpec, lifecycle RED tests, selection/store APIs, existing diagnostic helpers/tests, and shared-configuration public report API.
- Primary-owned paths: OpenSpec/control plane, shared core, runtime/CLI, plugin materializer, release package, docs, and integration remain main-owned.
- Forbidden: any write outside the named set; reconciliation/mutation from diagnostics; live profile/home/cache mutation; backend/plugin/network execution; dependency, Git, release, archive, cleanup, or destructive effects.

## Constraints
Each diagnostic entrypoint calls `shared_configuration_report` exactly once and never calls reconcile. All three surfaces must expose the same `Shared configuration generation: <n>` text and stable finding codes. Resolve active CLI/App selection through the existing canonical selection API. If state is absent or legacy, report read-only state without creating files. Preserve current diagnostic behavior and output otherwise.

## Verification
Run the shared lifecycle diagnostic test and focused status/Doctor/verify tests, plus `python3.12 -m py_compile` and `git diff --check` for the owned files. Report failures outside the write set without changing them.

## Evidence
Report canonical status, changed files, exact commands/results, complete test logs or validation results, output mapping, residual risks, unverified areas, and review needs.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before write-set expansion, diagnostic-side mutation, dependency, live state/network/App effects, destructive effects, Git writes, release, archive, bypass of a failing test, or an unapproved public-contract change. If a required fix lies outside the exclusive write set, report the exact seam and proposed owner instead of editing it.
