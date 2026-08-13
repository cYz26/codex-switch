---
workflow_version: 0.4.0
project_mode: brownfield
current_stage: external_effects

current_change:
  id: independent-app-cli-profiles
  status: external_effects

standing_milestone:
  status: inactive
  contract_path: none
  contract_sha256: none
  goal_id: none
  change_id: none
  candidate_digest: none
  validation_digest: none
  review_digest: none

authority_gate:
  key: sha256:a40cea2a985a0eb898ee82bc975cf4049822325e3e2cf6eb57f0846ca095e8c9
  status: resolved
  resolution_digest: sha256:6b34738467e335cab5f6641a1323cc41b3fe96e8709e3b0ffe82fda45ff319f4
  evidence_digest: sha256:89be09a2391c8b7d17e27ec780c4a1866553e4420243982bad3afb5f09aa15d1
  next_question: none
  missing_authority: []

gates:
  workflow_initialized: true
  spec_approved: true
  plan_written: true
  tests_baseline_known: true
  implementation_done: true
  verification_passed: true
  state_updated: true
  archive_allowed: false
  release_allowed: true

implementation_readiness:
  required: false

context_management:
  compact_policy: checkpoint_boundary
  last_checkpoint_id: 2026-08-13-draft-release-discovery-submit-authorized
  last_checkpoint_file: .planning/devflow/verification/independent-app-cli-profiles.md
  compact_recommended: false
  compact_status: not_needed
  last_compact_result_file: none
  compact_source: openspec
  compact_updated_at: 2026-08-13T16:16:02+08:00
  compact_skip_reason: bounded_change_context_is_healthy
  compact_error: none
  compact_after:
    - project_setup_completed
    - codebase_mapping_completed
    - design_saved
    - openspec_change_planned
    - verification_passed
    - change_archived
  skip_compact_for:
    - small_task_update
    - typo_fix
    - docs_only_micro_change
  require_before_compact:
    - state_updated
    - durable_context_written
    - next_action_recorded
    - risks_recorded
    - validation_recorded_if_applicable

goal_gate:
  id: 019f8f8f-e64c-7093-af73-2c0247cf2891
  required: true
  status: satisfied
  reason: the existing repository Goal Contract covers the confirmed task 13 cache-lifecycle decision
  suggested_goal: none

context_health:
  last_report: .planning/context-health/reports/20260629130742-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Separate backend-managed official source identity from internal target identity and prove the managed CLI starts successfully.
---

# Workflow State

## Current Status

Tasks 16.6-16.8 are complete and authority gate `a40cea2a...` is resolved.
The exact task 16.9 commit, fast-forward push, push-triggered `v0.1.14`
recovery, and atomic `v0.1.15` publication are authorized. Fresh pre-submit
Update/Release passes 171/171 and Profile/Wrapper passes 227/227.

## Next Action

Stage only the verified draft-discovery repair, tests, OpenSpec, ledger, state,
verification, and authority evidence. Exclude
`.planning/devflow/context-health/events.jsonl`. Require the native Git
fast-forward preflight, commit and push once to `origin/main`, then monitor Auto
Release through remote ref, Release metadata, canonical asset, and checksum
readback. Archive, project migration, install/live split,
dependency/credential changes, cleanup, force push, manual broad Release edits,
and unrelated runtime effects remain excluded.
