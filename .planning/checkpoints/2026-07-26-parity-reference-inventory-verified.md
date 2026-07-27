---
checkpoint_id: 2026-07-26-parity-reference-inventory-verified
created_at: 2026-07-26T11:12:11+08:00
boundary: verification_passed
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 2.1 RED ParityReceiptTests
---

# Checkpoint: Internal Official Feature Parity Reference/Inventory Verified

Date: 2026-07-26 11:12:11 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `verification_passed`
Status: `CHECKPOINT_AND_CONTINUE`

## Current goal

Complete the approved `internal-official-feature-parity` Full OpenSpec while
preserving the five allowed internal identity differences and all explicit
live, dependency, Git, release, archive, cleanup, and migration gates.

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- OpenSpec progress: 13/79
- Next dependency-ready item: task 2.1
- Task 8.1 remains the explicit live Human Gate

## Completed work

Tasks 1.1-1.13 are complete. The Reference/inventory slice now provides:

- verified ChatGPT bundled-reference and internal fingerprints;
- deterministic feature and direction-aware protocol inventories;
- exact Protocol Adapter rule-set digest evidence;
- versioned core, optional, pending-provider, and unclassified policy;
- deterministic synchronization-queue ordering; and
- bounded sanitized receipt-facing policy serialization.

The Protocol Adapter rule-set digest is:

`b9ac004f3801eaf094745e6e45754c7e5a058b33775746e49682aef7c240f849`

## Durable context written

- `openspec/changes/internal-official-feature-parity/proposal.md`
- `openspec/changes/internal-official-feature-parity/design.md`
- `openspec/changes/internal-official-feature-parity/specs/codex-switch/spec.md`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `scripts/codex_switch_protocol_adapter.py`
- `scripts/test_codex_protocol_config.py`

## Validation performed

```text
result: pass
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 38 tests in 0.066s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 38 tests in 0.071s
OK
```

The DevFlow checkpoint dry-run classified this as a major
`verification_passed` boundary with continuation and recommended compact.
Actual namespaced checkpoint creation was intentionally not attempted because
the repository state resolves as `legacy_read_only`; migrating it to
`.planning/devflow/STATE.md` is outside this task's authorization. This
project-format checkpoint and the legacy state pointer preserve the boundary
without migration.

## Key decisions

- Protocol Adapter owns exact transformations; parity owns classification.
- The fixed allowed differences remain internal binary, model, endpoint,
  provider, and auth.
- No receipt, overlay, probe, caller integration, live profile/App/provider
  mutation, dependency addition, retained-evidence cleanup, release, archive,
  commit, push, or other Git history mutation ran.
- Legacy `.codex/skills` entries remain untouched.

## Open questions

None. The next dependency-ready item and its RED contract are explicit.

## Risks

- The retained real-schema classification remains intentionally unhealthy:
  8 core incompatibilities, 6 optional queue items, and 3 unclassified methods.
- Receipt, overlay, adapter-coverage, config, and probe tasks must resolve the
  applicable core contract before any promotion or health claim.
- The current checkpoint is recoverable, but DevFlow namespaced state remains a
  separately gated migration recommendation.

## Next action

Execute task 2.1 by RED. Add `ParityReceiptTests` covering canonical payload
bytes, policy version, complete fingerprints and digests, profile-local mode
`0600` paths, manifest metadata, unsafe or malformed receipt states, digest and
provider/runtime staleness, and optional-queue health. Do not implement receipt
serialization or loading until the expected RED is captured.

## Compact instruction

Compact is recommended at this verified slice boundary, but continuation is
safe from this checkpoint. The active thread should continue to task 2.1
without requesting routine confirmation.
