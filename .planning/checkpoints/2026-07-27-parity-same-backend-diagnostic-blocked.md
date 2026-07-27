---
checkpoint_id: 2026-07-27-parity-same-backend-diagnostic-blocked
created_at: 2026-07-27T12:47:57+08:00
boundary: live_rebind_diagnostic_blocked
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Plan one focused complete task-8.3 repair; do not retry rebind or start 8.4
---

# Checkpoint: Same-Backend Diagnostic Blocked

## Current goal

Complete `internal-official-feature-parity` while preserving the fixed internal
binary, model, endpoint, provider, and auth differences and preventing
unproven parity evidence from reaching runtime promotion.

## Current status

- OpenSpec progress remains `70/79`.
- Task 8.3 remains unchecked.
- Task 8.4 is not dependency-ready.
- The active Goal is blocked on a real task-8.3 acceptance failure.

## Diagnostic result

The one permitted read-only diagnostic completed in 1.9558 seconds and stopped
before smoke or transaction code.

Errors:

- `parity.feature.core_drift`: `item_ids`, `multi_agent_v2`.
- `parity.protocol.core_incompatible`: client requests
  `thread/realtime/start`, `thread/resume`, `turn/start`, `turn/steer`;
  server requests `item/commandExecution/requestApproval`,
  `item/permissions/requestApproval`; server notifications
  `item/autoApprovalReview/started`,
  `item/autoApprovalReview/completed`.
- `parity.protocol.unclassified_drift`: client requests
  `account/login/start`, `externalAgentConfig/import`,
  `plugin/share/updateTargets`.

Fourteen warnings match the existing optional synchronization queue.

## Root blocker

Task 1.11 already classifies the eight `thread/`, `turn/`, and `item/` methods
as core. Policy evaluation runs before probes. The parity receipt binds only a
global Protocol Adapter rule-set digest and consumes no exact per-method
coverage. The core app-server probe exercises only `initialize`, `initialized`,
`collaborationMode/list`, and `thread/start`; the typed-subagent probe does not
prove the eight official method shapes.

The current evidence therefore cannot satisfy the requirement that each core
incompatibility be natively compatible or covered by one exact
capability-proven adapter rule. The three unclassified methods also cannot be
silently downgraded.

## Safety proof

All persistent target hashes/stat tuples, parity and marker paths, diagnostic
temporary-directory identities, and ChatGPT/proxy/backend pids
`95489`/`95838`/`95842` matched before and after the diagnostic. No rebind
retry, smoke, transaction, restart, provider-backed task, dependency, commit,
push, tag, release, archive, cleanup, or provider/model/API/auth change
occurred.

## Validation

```text
openspec validate internal-official-feature-parity --strict: valid
openspec instructions apply: 70/79, task 8.3 unchecked
AI-native plan lint: passed
DevFlow workflow validation: ok=true, issues=[]
targeted diff hygiene: passed
```

The existing DevFlow legacy root-state migration warning remains
`DEFER_AND_CONTINUE`; no migration or cleanup ran. No unchanged Python suite
was repeated.

## Resume contract

Do not retry the live rebind and do not start task 8.4. Resume only after a
focused plan names the exact failing acceptance criterion and demonstrates
that one bounded RED/GREEN can close the complete 13-error blocker. Do not
implement a partial finding suppression, unrelated fault matrix, shared
abstraction without that proof, or an adjacent full-suite rerun.
