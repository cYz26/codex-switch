---
workflow_version: 0.3.0
project_mode: brownfield
current_stage: verified

current_phase:
  id: 01-foundation
  status: planning

current_change:
  id: auto-release-tags
  status: verified

gates:
  workflow_initialized: true
  spec_approved: true
  plan_written: true
  tests_baseline_known: true
  implementation_done: true
  verification_passed: true
  state_updated: true
  archive_allowed: false

context_management:
  compact_policy: checkpoint_boundary
  last_checkpoint_id: 2026-06-08-change_archived-local-command-self-update
  last_checkpoint_file: .planning/checkpoints/2026-06-08-change_archived-local-command-self-update.md
  compact_recommended: false
  compact_status: not_needed
  last_compact_result_file: none
  compact_source: checkpoint
  compact_updated_at: 2026-06-08T12:58:56+08:00
  compact_skip_reason: none
  compact_error: none
  compact_after:
    - project_setup_completed
    - codebase_mapping_completed
    - design_saved
    - openspec_change_planned
    - phase_plan_saved
    - verification_passed
    - change_archived
    - phase_shipped
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

context_health:
  last_report: .planning/context-health/reports/20260615174938-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Automatic release tags and packaging are implemented and verified. Main pushes with release-relevant changes now plan the next patch tag, bump VERSION, create and push the tag, and publish release assets in the same workflow run; planning/spec/docs-only changes are skipped. Full tests, py_compile, shell syntax, eval JSON, OpenSpec strict validation, package generation, and diff whitespace checks passed. Archive remains closed by gate.
---

# Workflow State

## Current Status

Change `auto-release-tags` is implemented and locally verified. It automatically creates the next patch tag and publishes release assets when release-relevant changes land on `main`, while skipping planning/spec/docs-only changes.

## Next Action

Review and submit the verified `auto-release-tags` change. Archive remains unavailable because the archive gate is closed. Do not archive until the gate is explicitly opened.
