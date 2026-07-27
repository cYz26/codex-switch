---
checkpoint_id: 2026-07-27-parity-same-backend-rebind-red
created_at: 2026-07-27T12:32:27+08:00
boundary: live_rebind_safe_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Diagnose task 8.3 parity findings read-only; do not retry rebind
---

# Checkpoint: Same-Backend Rebind Safe RED

## Current goal

Complete the approved `internal-official-feature-parity` change without
changing the fixed internal binary/provider/model/API/auth boundary, and stop
before any unhealthy parity evidence can reach runtime transaction or Desktop
restart.

## Completed work

- Task 8.2 installed and verified the exact source payload.
- Task 8.3 ran once and failed safely at the parity health gate.
- Immediate post-failure hashes, stat tuples, backend identity, process
  ownership, and absence of transaction artifacts were captured.

## Durable context written

- `.planning/STATE.md`
- `TASK_LEDGER.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- this checkpoint

## Key decisions

- Keep task 8.3 unchecked and progress at 70/79.
- Do not retry rebind or bypass the unhealthy bundle into commit.
- Permit one read-only sanitized finding-detail diagnostic before deciding
  whether the acceptance failure requires code, plan, or external capability
  action.

## Open questions

- Which exact feature names, protocol directions/methods, and reason codes
  produced the 13 unhealthy findings?
- Are those findings true unsupported core drift, stale classification inputs,
  or protocol-normalization defects?

## Risks

- A rebind retry before diagnosis could repeat provider-backed preparation
  without changing the failed acceptance condition.
- The running Codex session rewrote managed-home config after the exact
  post-failure snapshot, so all current inputs must be recaptured before any
  future retry.
- DevFlow checkpoint validation also requires namespaced state migration; that
  migration remains outside the authorized task.

## Validation performed

```text
command: openspec validate internal-official-feature-parity --strict --no-interactive
result: pass
notes: progress remains 70/79 and task 8.3 remains unchecked
```

## Git state

```text
branch: main
changed_files: large pre-existing dirty worktree preserved; only canonical
control-plane files were changed for this checkpoint
```

Date: 2026-07-27 12:32:27 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Status: `RED_SAFE`
Progress: `70/79`

## Result

The authorized task-8.3 command ran exactly once:

```bash
/Users/cY/.local/bin/codex-switch --skip-self-update \
  set-bin internal /Users/cY/.local/bin/codex
```

It exited 2 after 2.3416 seconds during parity preparation:

```text
parity.feature.core_drift: 2
parity.protocol.core_incompatible: 8
parity.protocol.unclassified_drift: 3
```

The parity health gate stopped before the runtime transaction.

## No-Mutation Proof

The exact immediate post-failure snapshot matched the preflight hashes and stat
tuples for the internal manifest, managed launcher, capability receipt, profile
config, official config, managed-home config, active record, and backend.
Backend SHA-256 remained `410ebcd3...e8b6`; ChatGPT/proxy/backend pids remained
`95489`/`95838`/`95842`. No parity directory, `.runtime-rebind-*` directory, or
`.runtime-binding-rebind.json` marker remained.

At 12:30 the running Codex session independently rewrote the managed-home
config after that snapshot. This later concurrent write is not attributed to
the failed transaction and requires fresh input capture before any future
retry.

## Boundary

Task 8.3 remains unchecked. No restart, provider-backed task, dependency,
commit, push, tag, release, archive, cleanup, provider/model/API/auth change,
or production edit occurred.

## Next action

Run one read-only in-process diagnostic through the same parity preparation
path. Intercept the prepared bundle at the health gate, print only sanitized
finding category/code/severity/message details, and raise immediately before
smoke or transaction code. Do not retry the live rebind or begin task 8.4.
