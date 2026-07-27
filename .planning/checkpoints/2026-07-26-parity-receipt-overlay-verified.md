---
checkpoint_id: 2026-07-26-parity-receipt-overlay-verified
created_at: 2026-07-26T11:46:42+08:00
boundary: verification_passed
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 2.5 RED manifest-candidate tests
---

# Checkpoint: Internal Official Feature Parity Receipt/Overlay Verified

Date: 2026-07-26 11:46:42 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `verification_passed`
Status: `CHECKPOINT_AND_CONTINUE`

## Current goal

Complete the approved `internal-official-feature-parity` Full OpenSpec while
preserving the five allowed internal identity differences and every explicit
live, dependency, Git, release, archive, cleanup, and migration gate.

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Pre-checkpoint worktree status SHA-256:
  `e4fe67c8afdf98fd2b52cd92d7f0a32421b697e7dcc4dc118f50d327601c6d08`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 17/79
- Next dependency-ready item: task 2.5
- Task 8.1 remains the explicit live Human Gate

## Completed work

Tasks 2.1-2.4 are complete:

- the canonical provider-bound receipt is bounded, profile-local, mode checked,
  no-follow loaded, digest bound, and stale on reference/provider/runtime drift;
- optional-only synchronization evidence remains healthy and deterministic;
- the configured source catalog is opened no-follow and identity/digest checked
  without mutation;
- the managed overlay is a canonical structured deep copy whose only permitted
  semantic change is active-model `multi_agent_version = "v2"`; and
- main review guards reject forged non-canonical overlay artifacts and explicit
  null metadata.

The receipt and overlay seams remain disconnected from callers and promoted
paths. No production artifact was written outside isolated tests.

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

## Validation performed

```text
result: pass
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 54 tests in 0.129s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 54 tests in 0.127s
OK
```

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid
```

```text
git diff --check
exit 0
```

The DevFlow dependency check reports Full OpenSpec and project-local TDD ready.
Its legacy `.codex/skills` layout recommendations are nonblocking and remain
untouched.

The namespaced checkpoint dry-run recommended a compact boundary and
continuation. Actual namespaced creation was not run because this repository
resolves legacy root state as read-only and would require an unauthorized
`.planning/devflow/STATE.md` migration. This project-format checkpoint and the
legacy state pointer preserve the boundary.

## Key decisions

- Manifest-candidate preparation must bind receipt and overlay paths/digests,
  policy version, official-reference digest, source-catalog digest, adapter
  rule-set digest, and capability-receipt digest before promotion.
- Task 2.5 is tests-only RED. `ParityBundle` and private staging are not
  implemented until the expected failure is captured.
- Receipt and overlay generation remain parity-owned; Runtime Binding,
  Protocol Adapter, and Capability Receipt ownership does not change.

## Open questions

None. The next RED contract and write set are explicit.

## Risks

- Retained real-schema evidence remains intentionally unhealthy for unresolved
  core and unclassified drift.
- No manifest, launcher, config, transaction, rebind, update, diagnostic, or
  live Desktop path consumes parity evidence yet.
- Namespaced DevFlow state migration remains a separate approval boundary.

## Next action

Execute task 2.5 by RED. Add manifest-candidate tests proving complete binding
of receipt and overlay paths/digests, parity policy version, official-reference
digest, source-catalog digest, Protocol Adapter rule-set digest, and capability
receipt digest before promotion. Do not implement `ParityBundle` or staging
until the focused failure is captured.

## Compact instruction

Compact is recommended at this verified boundary, but continuation is safe from
this checkpoint. Continue directly to task 2.5 without requesting routine
confirmation.
