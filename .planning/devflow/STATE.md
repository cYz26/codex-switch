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
  key: sha256:ff784b1fcb442d96936f0e01152cf87fd771be1d33d49cf2887eb69a34c67447
  status: resolved
  resolution_digest: sha256:155a6edbdb42eea4ec2a90bf4af3fe8b3697d62f9ce65beacaea3929b4f1f30f
  evidence_digest: sha256:96ff6e337e308ca2d8289e0e0badcbc147c3f74eb4114442ec7e1a8be0863c34
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
  last_checkpoint_id: 2026-08-13-python312-v0.1.15-submit-authorized
  last_checkpoint_file: .planning/devflow/verification/independent-app-cli-profiles.md
  compact_recommended: false
  compact_status: not_needed
  last_compact_result_file: none
  compact_source: openspec
  compact_updated_at: 2026-08-13T18:18:00+08:00
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
  last_decision: authorize_python312_fix_and_publish_v0.1.15
  last_goal_status: aligned
  goal_summary: Separate backend-managed official source identity from internal target identity and prove the managed CLI starts successfully.
---

# Workflow State

## Current Status

Tasks 16.13-16.14 are complete. Both Release workflows select Python 3.12
before any Python command, and gate `ff784b1f...` is resolved by the user's
2026-08-13 authorization for one verified commit/push and the exact
`v0.1.15` Auto Release chain. `v0.1.14` tag and Release mutation remain
excluded.

## Next Action

Run the final non-interactive candidate and control-plane verification, stage
only the verified Python-runtime repair and authority evidence, fast-forward
push once to `origin/main`, then require `v0.1.15` tag, published Release,
canonical three assets, and checksum readback before completing task 16.15.
