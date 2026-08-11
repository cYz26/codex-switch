# Agent Task Contract

## Goal
Add one production plugin-materialization adapter to the existing plugin module so the shared-configuration coordinator can make an enabled desired generation independently ready in the target profile cache and return attested receipts.

## Worker ID
`split-shared-plugin-materializer-green`

## Scope
Allowed write set for worker `split-shared-plugin-materializer-green` only:
- `scripts/codex_switch_plugins.py`

Read-only inputs include the active OpenSpec, `scripts/test_codex_shared_materialization.py`, current plugin repair/catalog/runtime helpers and tests, and the in-progress `codex_switch_shared_configuration.py` desired/receipt public dataclasses. Shared core, tests, lifecycle, diagnostics, release metadata, docs, OpenSpec/control-plane files, and integration remain main-owned. Forbidden: write any other path; touch live profile/home/cache; invoke a real backend, network, App process, install/update, Git mutation, release, archive, cleanup, or destructive effect.

## Constraints
Expose `materialize_shared_plugins(*, store, selection, source_profile, target_profile, desired_plugins, generation)` with the adapter contract locked by the RED tests. Preserve existing repair behavior and public output. Take a zero-command fast path when target receipts already attest the requested generation. Enabled `portable_exact` identities must return exact cache key, manifest version, and content-tree digest; `backend_managed` may return a target-compatible version but must record it. Missing/unverified/unavailable/unsafe/running-process cases raise `SwitchError` with the approved `shared_configuration.materialization.*` code. Never symlink or use the other profile cache, never remove or garbage-collect old cache versions, and do not publish target config. Reuse deep existing catalog/runtime primitives; do not add a dependency or duplicate reconciliation/generation logic. If exact native target-backend materialization cannot be implemented without a new staging/transaction seam or automatic unpinned/network behavior outside the approved contract, stop and report the concrete seam instead of implementing a weaker copy/latest path.

## Verification
Run relevant existing plugin repair tests and isolated fake-home checks only, plus `python3.12 -m py_compile scripts/codex_switch_plugins.py` and `git diff --check -- scripts/codex_switch_plugins.py`. Do not run a real plugin command. Report any integration failure outside the owned write set without changing it.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; complete test logs or validation results; exact commands; fast-path, exact/backend-managed, cache-containment, running-process, and no-cleanup evidence; residual risks; unverified areas; review needs; and incidental-finding classification.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before expanding the write set, adopting source-cache copying as a substitute for target-backend materialization, adding automatic unpinned/latest or unapproved network behavior, changing existing repair output/semantics, adding a staging/transaction/dependency seam outside this file, touching live state/App/network, bypassing a failing test, deleting cache data, Git mutation, release, or archive. Report the exact blocked seam and proposed owner.
