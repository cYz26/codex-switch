# Tasks: Current System Baseline

## Target State

Implement the complete approved behavior for `current-system`, not a partial delivery. Keep GSD phases as workflow governance and use the slices below as executable technical checkpoints.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Capability evidence and validation surface

**Status:** done

**Goal**
- Confirm the behavior boundary, capability evidence, and test strategy before editing implementation files.

**Files / Modules**
- `openspec/changes/current-system/proposal.md`
- `openspec/changes/current-system/design.md`
- `openspec/changes/current-system/specs/`
- relevant source and test files

**Implementation**
- [x] Review requirements and scenarios.
- [x] Capability evidence recorded through project setup, local scans, CLI help,
      and verification artifacts.
- [x] Record authoritative/current evidence, local scan findings, comparison,
      assumptions, and the selected validation contract.
- [x] Identify affected files and compatibility constraints.

**Tests**
- [x] Existing regression suite used for setup baseline; behavior-specific
      tests were added under the subsequent `isolate-desktop-session-state`
      change.

**Validation Commands**
```bash
<focused test command>
```

**Done When**
- [x] Requirements, Capability Evidence, files, tests, and validation commands are known.

**Risks / Rollback**
- Return to planning if requirements or compatibility are unclear.

### Slice 2: Implementation and focused verification

**Status:** done

**Goal**
- Implement the smallest compatible change that satisfies the Target State.

**Files / Modules**
- relevant source and test files

**Implementation**
- [x] Implement the approved setup and baseline behavior.
- [x] Keep edits scoped to the active change.

**Tests**
- [x] Run focused regression tests.

**Validation Commands**
```bash
<focused test command>
```

**Done When**
- [x] Focused verification passes.

**Risks / Rollback**
- Revert or repair this slice before starting broader verification if focused tests fail.

### Slice 3: Broader verification and state update

**Status:** done

**Goal**
- Prove the change is complete and durable.

**Files / Modules**
- `.planning/STATE.md`
- `.planning/verification/`
- `openspec/changes/current-system/tasks.md`

**Implementation**
- [x] Run broader project verification where applicable.
- [x] Record verification evidence.
- [x] Update workflow state and this ledger.

**Tests**
- [x] Run the smallest relevant broader suite.

**Validation Commands**
```bash
<broader verification command>
```

**Done When**
- [x] Verification evidence exists and the Completion Contract is checked.

**Risks / Rollback**
- Keep archive blocked until verification evidence is recorded.

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Capability evidence and validation surface | done | `.planning/verification/project-setup-2026-06-05.md`; `.planning/verification/20260608114120-final-workflow-closure.md` |
| Implementation and focused verification | done | `.planning/verification/20260605134234-python3-scripts-test_codex_profile_switch.py-bash--n-scripts-cod.md`; `.planning/verification/20260608114120-final-workflow-closure.md` |
| Broader verification and state update | done | `.planning/verification/20260608114120-final-workflow-closure.md` |

## Acceptance Criteria

- [x] Required behavior matches the OpenSpec scenarios.
- [x] Tests or documented manual checks cover the changed behavior.
- [x] No required capability remains unimplemented without a blocker.

## Validation Commands

```bash
<focused test command>
<broader verification command>
```

## Final Verification

- [x] Focused tests pass.
- [x] Broader tests, lint, typecheck, or build pass where applicable.
- [x] Verification evidence is recorded.
