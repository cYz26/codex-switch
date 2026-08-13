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
  key: sha256:614cc0253ca0735cf2af34acc60564687b7b081de9fa2e417045ea447a851d38
  status: resolved
  resolution_digest: sha256:7b9fe68038e69c22b8f8d74e447bfe666377bc2087e89461d7829cf7df5d011d
  evidence_digest: sha256:365009cf9858a43be8471fc4f3cd543357e1298c1c14da5ea95331ef5a3a2ccd
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
  last_checkpoint_id: 2026-08-13-release-recreation-submit-ready
  last_checkpoint_file: .planning/devflow/verification/independent-app-cli-profiles.md
  compact_recommended: false
  compact_status: not_needed
  last_compact_result_file: none
  compact_source: openspec
  compact_updated_at: 2026-08-13T12:07:11+08:00
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

Tasks 16.1-16.3, 17.1-17.6, and 18.1-18.4 are complete in source. Typed bounded
Release recreation, Official-authoritative shared readiness, and post-switch
shared synchronization pass fresh focused, complete, package, static, strict
OpenSpec, workflow, diff, Plugin Eval, and independent Spec/Standards review
gates. Review-discovered 4xx precedence, equals-form wrapper routing, transport
classification, and diagnostic control-character injection gaps are closed.
The final retained package is byte-exact for the changed runtime paths.

## Next Action

Use the resolved `614cc025...` authority and the user's 2026-08-13 submit
request to stage only the verified source/test/docs/OpenSpec/control-plane and
authority evidence, excluding `.planning/devflow/context-health/events.jsonl`.
Create one commit on `main`, require a native Git fast-forward preflight against
`origin/main`, push, then monitor the authorized Auto Release through restored
`v0.1.14` assets and atomic `v0.1.15` publication. Archive, project migration,
install/live split, dependency/credential changes, cleanup, force push, and
unrelated runtime effects remain excluded.
