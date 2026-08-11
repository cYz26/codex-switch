# Agent Task Contract

## Goal
Implement the approved lifecycle and public command seams for shared App/CLI Plugin and Skill configuration: functional internal CLI preflight before backend `execve`, informational invocation bypass, and explicit `sync-shared [--dry-run]` routing.

## Worker ID
`split-shared-lifecycle-green`

## Scope
Allowed write set for worker `split-shared-lifecycle-green` only:
- `scripts/codex_switch_runtime_binding.py`
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- Allowed read-only scope: the active OpenSpec, `scripts/test_codex_shared_lifecycle.py`, the new shared-configuration public API, parser helpers, and existing runtime-binding tests.
- Primary-owned paths: OpenSpec, root control-plane files, shared-configuration core, diagnostics, plugin materializer, release packaging, docs, and integration remain main-owned.
- Forbidden: any write outside the named set; live profile/home/cache mutation; real backend/plugin/network execution; App restart; dependency, Git, release, archive, cleanup, or destructive effects.

## Constraints
Preserve `os.execve` and existing TTY/signal/exit semantics. Functional internal invocations must call `preflight_internal_shared_configuration` after generation/home/backend resolution and before backend execution; a non-ready receipt must fail closed without calling the backend. Invocations consisting only of `-h`, `--help`, `-V`, or `--version` remain read-only. Register `sync-shared` and `--dry-run` through both Python and shell entrypoints. Do not add a supervisor, watcher, daemon, App wrapper, or automatic network/update behavior. Reuse the public shared-configuration module; do not duplicate reconciliation logic.

## Verification
Run focused lifecycle and runtime/parser tests that do not touch live state, plus `python3.12 -m py_compile` and `git diff --check` for the owned files. Report any failure outside the owned write set without changing it.

## Evidence
Report canonical status, changed files, exact commands/results, complete test logs or validation results, behavior mapping, residual risks, unverified areas, and review needs.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before any write-set expansion, process-model change, dependency, live mutation, network operation, App restart, destructive effect, Git write, release, archive, bypass of a failing test, or public-contract change not already approved in OpenSpec. If a required fix lies outside the exclusive write set, report the exact seam and proposed owner instead of editing it.
