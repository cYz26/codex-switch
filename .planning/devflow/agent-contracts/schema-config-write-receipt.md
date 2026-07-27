# Agent Task Contract

## Goal
Complete `schema-scoped-app-proxy` tasks 2.1-2.5 by strict vertical TDD: generate a schema- and backend-digest-bound behavioral config-write receipt in an isolated temporary home, promote that receipt with the managed internal launcher, reject unproven writes before backend or filesystem mutation, forward proven writes exactly once with the backend version unchanged, and remove every proxy-side post-response config repair.

## Worker ID
`schema-config-write-receipt`

## Stable Input Snapshot
- `scripts/codex_switch_protocol_adapter.py`: `90c3ffd65a56dee8ee2595e977b3ef4ab5bf1d9736ae71ac511b65b512b0df0b`
- `scripts/codex_switch_app_proxy.py`: `031ab224aca2b0143b3d4897cf72825e62ad58ecca8e218fd063453d9dd726c6`
- `scripts/codex_switch_app_wrapper.py`: `7bac5b5484af1856484da3a037265bf5ddef6e09e8c02990dd03dd48e479e476`
- `scripts/codex_switch_bindings.py`: `13dc2b6c5e17958f01d149bee944aa64fc7d52b1da0d10fad703c83ba4042d69`
- `scripts/codex_switch_transaction.py`: `8c7fae2b0e0a43ee20cb1758a910ae1890a02eb48a9a93fb044c6838c32c82d0`
- `scripts/test_codex_protocol_config.py`: `ddc02f5278da1af499ee9f39bfff443128dae9126d701b8eaec89a2c12b1b505`
- `scripts/test_codex_runtime_binding.py`: `d9dd5872f5ac2c8276c890f9c94b021eb8cbca306eb0a9559802186e8458b5f2`
- `scripts/test_codex_transaction.py`: `b1b0b9ad6aa102c0d905fbd102fbfac42203d60d823d13b48be8be77efe1c955`
- canonical OpenSpec: proposal `06e04fe59272c1ffe9ac27b4ffe9f83334a1b036a3243d9d6315ffbbc201206d`, design `6479d33287daaed053f9cd4ee890d41f04385463a4709fcf225de4c9f8af8fd7`, spec `46927872ad596ffd07004b03421e35c2510f2233ff37ca1ff0773c99b00c6bc6`, tasks `924b2efd47f7ab056b7a1095e97dff0fed8fccb0b1bf9669bcab8cb000688993`.

Stop before editing if any listed production, test, or OpenSpec hash differs. OpenSpec and control-plane files are main-owned and read-only for the worker.

## Scope
Allowed write set for worker `schema-config-write-receipt` only:
- `scripts/codex_switch_protocol_adapter.py`
- `scripts/codex_switch_app_proxy.py`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/codex_switch_bindings.py`
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_protocol_config.py`
- `scripts/test_codex_runtime_binding.py`
- `scripts/test_codex_transaction.py`

Read-only inputs include the full approved `openspec/changes/schema-scoped-app-proxy/` change, current runtime-binding and transaction contracts, `scripts/codex_switch_store.py`, `scripts/codex_switch_verify.py`, and existing profile tests. Forbidden: all other paths, especially OpenSpec, `.planning/`, `TASK_LEDGER.md`, release artifacts, installed trees, live profile stores, App bundles, rollout/session files, plugin caches, network, Git staging/commit/push, install/update/release, or dependency changes. You are the sole production writer for this slice but not alone in the worktree; preserve every unrelated/main-agent change and never revert it.

## Constraints
The pre-agreed public seams are `CapabilityReceipt`, the internal `cmd_set_bin` rebind path, generated launcher/proxy JSONL behavior, and the existing durable runtime-binding promotion seam. Use Python 3.9-compatible standard-library code and one RED-to-GREEN vertical slice at a time. The isolated behavioral probe must use a fresh temporary `CODEX_HOME`, bounded process and message deadlines, representative unrelated MCP/marketplace/plugin/skill data, canonical initialize plus versioned write requests, exact response validation, and semantic before/after preservation checks. Persist only sanitized tri-state capability data and backend/schema digests; no temporary paths, config values, credentials, stdout/stderr, or secrets may enter the durable receipt.

The receipt must be promoted consistently with the launcher and manifest. Extend the existing durable runtime-rebind promotion only as needed to include the companion receipt, preserving rollback, recovery, symlink rejection, concurrent-state protection, and old two-file evidence compatibility if required by existing tests. The proxy must load and validate the receipt against the actual backend and generated schema evidence available to the launcher. Missing, malformed, stale, failed, timed-out, error, unknown, or wrong-target evidence must return one stable JSON-RPC compatibility error for `config/value/write` and `config/batchWrite` before backend forwarding or filesystem mutation. Non-write traffic and exact legacy schema transforms continue unchanged.

For a valid receipt, forward each write once, preserve request ordering, track concurrent write IDs directionally, and return the backend `status`, `filePath`, and `version` unchanged except the already-approved exact model alias transform. Delete `remember_config_write_request()`, `restore_config_write_response()`, their pending snapshot state, and every post-response `atomic_write` path. Backend errors, malformed responses, invalid path/status/version, orphan responses, same-ID server requests, and old receipt generations must never trigger a compensating write. Do not implement Config Document tasks 3.x, launcher home-sync tasks 4.1-4.3, general E2E task 5.1, fail-safe update/release, custom profiles, or any new public CLI.

## Verification
Record exact RED and GREEN output for focused tests, then run:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v
openspec validate schema-scoped-app-proxy --strict --no-interactive
python3.12 -m py_compile scripts/codex_switch_protocol_adapter.py scripts/codex_switch_app_proxy.py scripts/codex_switch_app_wrapper.py scripts/codex_switch_bindings.py scripts/codex_switch_transaction.py
git diff --check
```

Also run focused proxy subprocess tests for valid, missing, stale, failed, timeout, malformed, backend-error, response-order, and concurrent-write cases; transaction recovery tests for interruption before and after companion receipt promotion; `rg` proof that the deleted snapshot/restore helpers have no supported caller; stable SHA-256 for every changed file; and a final rerun against unchanged hashes.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with exact changed files and final hashes; ordered RED then GREEN commands/results; complete test logs or validation results; every added test name; behavioral probe request/response state machine; receipt schema and sanitization proof; promotion/rollback/recovery matrix; valid and invalid write-gating matrix; request-count and zero-mutation assertions; dual-interpreter focused/full results with exit codes and counts; strict OpenSpec, compile, `rg`, and diff results; residual risks and unverified areas; incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`; and review needs. Do not mark task checkboxes or edit verification, ledger, state, or OpenSpec files.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing a public CLI or persistence contract beyond the approved receipt companion, accepting an unproven config write, weakening digest/schema/response validation, adding a dependency, expanding product profiles, editing outside the exclusive write set, touching live workstation/App/session/install/plugin state, bypassing a failing required test, or performing Git/network/release actions. If a required change needs another file or a new compatibility decision, report the exact seam and reason without editing it.
