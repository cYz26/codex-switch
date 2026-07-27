# Task 8.3 Method-Coverage Repair Planned

Recorded: 2026-07-27T18:00:37+08:00
Change: `internal-official-feature-parity`
Task: 8.3
Progress: 70/79
Status: `BLOCKED_AWAITING_HUMAN`
Next gate: `PARITY-8.3-IMPLEMENT`

## Outcome

The authorized planning-only revision is complete. Task 8.3 now defines one
atomic method-scoped RED/GREEN for the retained two core-feature, eight
core-protocol, and three unclassified-protocol errors. Task 8.3 remains
unchecked, task 8.4 remains dependency-blocked, and no implementation or live
effect was authorized.

## Authoritative Artifacts

- `openspec/changes/internal-official-feature-parity/proposal.md`
- `openspec/changes/internal-official-feature-parity/design.md`
- `openspec/changes/internal-official-feature-parity/specs/codex-switch/spec.md`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

The specification now contains 12 requirements and 75 scenarios. The active
task file remains the only implementation queue.

## Current Runtime Boundary

Planning re-attestation found active profile `openai-official`, configured
shell/App CLI `/Applications/ChatGPT.app/Contents/Resources/codex`, bundled
version `codex-cli 0.146.0-alpha.3.1`, ChatGPT pid `86658`, and official
app-server pid `86992`. PATH resolves through
`/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex` and
does not match the expected switch shim.

No switch, repair, rebind, restart, provider task, or PATH mutation ran. The
retained internal pids `95489`/`95838`/`95842` and config hashes are historical
RED evidence only. Every future boundary must re-attest current ownership and
regenerate schema/config fingerprints.

## Repair Architecture

1. Protocol Adapter exposes a canonical structured manifest only for actual
   transformations. The global digest is derived from it but is never
   sufficient method coverage.
2. Parity coverage binds direction, method, official/internal normalized
   method-schema digests, reasons, disposition, and required rule digests.
3. The four approval/auto-review nullable-string differences become native
   semantic equivalents; they are not described as adapter transforms.
4. `thread/resume` binds the existing exact top-level ID and non-portable
   opaque-reasoning transform. Its `input_audio` variant is a separately named
   optional-unless-observed extension.
5. Realtime-v3/handoff/initial-items, turn audio, Bedrock login,
   external-agent memory/provider/migration, and listed sharing are accepted
   only for exact schema pairs while unobserved. Changed or observed variants
   fail closed.
6. `item_ids` requires exact observed-path coverage. `multi_agent_v2` remains
   provisional until overlay/config and typed-v2 probe evidence pass.
7. Preparation runs coverage and fail-closed eligibility before probes, then
   revalidates fingerprints and performs final policy before constructing a
   receipt.
8. Receipt schema v2 stores sorted coverage and final evidence. Version 1 is
   stale/unsupported and is regenerated through staged repair, never patched.

Removing any required proof must recreate a stable unhealthy finding; no
subset of the thirteen can satisfy the task.

## Exact Planning Write Set

This revision changed only:

- the four active OpenSpec artifacts;
- `TASK_LEDGER.md`;
- `.planning/STATE.md`;
- the existing parity verification record; and
- this checkpoint.

No production, test, fixture, operator-doc, installed, live, dependency, Git,
release, archive, or cleanup write occurred.

The future implementation write set is explicitly enumerated inside task 8.3.
Its three future checkpoint paths are fixed as
`.planning/checkpoints/2026-07-27-parity-method-coverage-repair-red.md`,
`.planning/checkpoints/2026-07-27-parity-method-coverage-repair-verified.md`,
and
`.planning/checkpoints/2026-07-27-parity-method-coverage-live-retry.md`.
Any additional production/test/doc/checkpoint path is
`BLOCKED_AWAITING_HUMAN`.

## Verification

```text
active strict OpenSpec:
  valid
all strict OpenSpec:
  18 passed, 0 failed
AI-native plan lint:
  passed
DevFlow workflow validation:
  ok=true, issues=[]
DevFlow warning:
  legacy root state is read-only; migration remains unauthorized
targeted/full git diff hygiene:
  passed for tracked worktree and all six untracked planning artifacts
```

No Python suite was run because the authorized write set contains no
production or test source.

## Rollback and Continuation

- Planning rollback may touch only the exact planning write set and must
  preserve unrelated dirty bytes.
- A future RED/GREEN failure has no live artifact effect.
- A future authorized live retry uses the existing schema-v3 recovery contract:
  preparation failure preserves the old generation; prepared interruption
  rolls back; committed interruption rolls forward; foreign state stops.
- Resume first at `PARITY-8.3-IMPLEMENT`. After implementation, reviewed
  tests, package identity, and planning gates pass, checkpoint and stop at
  `PARITY-8.3-LIVE-RETRY`.
- Do not infer either gate from the consumed planning authorization or the old
  task-8.1 approval. Do not begin task 8.4.

## Stop Conditions

Stop for a changed official/internal binary or unsupported schema pair, an
unresolved product classification, public compatibility expansion, dependency,
additional live effect, destructive action, or any write-set expansion.
