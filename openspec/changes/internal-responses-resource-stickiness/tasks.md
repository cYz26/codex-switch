# Tasks: Internal Responses Resource Stickiness Verification

## Target State

Internal Azure Responses verification can explicitly exercise a shell-tool
follow-up path and report cross-resource routing failures with sanitized
diagnostics, while ordinary local runtime smoke remains unchanged.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: OpenSpec and troubleshooting contract

**Status:** done

**Goal**
- Record the behavior contract and scenario ownership before implementation.

**Files / Modules**
- `openspec/changes/internal-responses-resource-stickiness/proposal.md`
- `openspec/changes/internal-responses-resource-stickiness/design.md`
- `openspec/changes/internal-responses-resource-stickiness/specs/codex-switch/spec.md`
- `openspec/changes/internal-responses-resource-stickiness/tasks.md`
- `docs/troubleshooting/internal-azure-responses-resource-stickiness.md`

**Implementation**
- [x] Create proposal, design, and spec delta.
- [x] Add troubleshooting documentation after verifier behavior is implemented.
- [x] Validate OpenSpec change.

**Validation Commands**
```bash
openspec validate internal-responses-resource-stickiness --strict --no-interactive
```

### Slice 2: Failing verifier tests

**Status:** done

**Goal**
- Lock the tool-follow-up smoke behavior before production code changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add a fake Codex helper that records response tool smoke invocations.
- [x] Add a failing test for `verify --responses-tool-smoke` command
      construction and target `CODEX_HOME`.
- [x] Add a failing test for Azure resource mismatch diagnosis.
- [x] Add a failing test for JSON report diagnostics.
- [x] Add a failing one-key switch forwarding test.
- [x] Run the focused tests and record the expected failures.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
```

### Slice 3: Verifier implementation

**Status:** done

**Goal**
- Add the smallest CLI and verifier implementation needed to run and diagnose
  Responses tool-follow-up smoke.

**Files / Modules**
- `scripts/codex_switch_verify.py`
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add `--responses-tool-smoke` to the Python `verify` parser.
- [x] Add the flag to shell wrapper help, parsing, and verify forwarding.
- [x] Add deterministic smoke command construction in
      `codex_switch_verify.py`.
- [x] Add sanitized Azure resource mismatch parsing.
- [x] Include structured diagnostics in JSON verification reports.
- [x] Run focused tests until green.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
```

### Slice 4: Documentation and final verification

**Status:** done

**Goal**
- Preserve the scenario and prove the repair before handoff.

**Files / Modules**
- `docs/troubleshooting/internal-azure-responses-resource-stickiness.md`
- `.planning/verification/`
- `.planning/STATE.md`
- `openspec/changes/internal-responses-resource-stickiness/tasks.md`

**Implementation**
- [x] Write troubleshooting docs.
- [x] Run focused and full validation.
- [x] Record verification evidence.
- [x] Mark OpenSpec tasks complete where validated.
- [x] Update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
python3 -m py_compile scripts/*.py
openspec validate internal-responses-resource-stickiness --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| OpenSpec and troubleshooting contract | done | `openspec validate internal-responses-resource-stickiness --strict --no-interactive` |
| Failing verifier tests | done | focused test red run recorded in conversation |
| Verifier implementation | done | focused test green run recorded in conversation |
| Documentation and final verification | done | `.planning/verification/20260703114321-internal-responses-resource-stickiness.md` |

## Acceptance Criteria

- [x] `verify --responses-tool-smoke` runs deterministic tool-follow-up smoke
      against the target profile Codex binary and `CODEX_HOME`.
- [x] Azure resource mismatch output is identified as an internal Responses
      resource-stickiness failure.
- [x] JSON verification report includes sanitized diagnostics.
- [x] One-key switch forwarding supports `--responses-tool-smoke`.
- [x] Troubleshooting docs capture symptoms, local command, safe evidence, and
      upstream AIDP/backend repair contract.
