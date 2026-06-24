---
workflow_version: 0.3.0
project_mode: brownfield
current_stage: verified

current_phase:
  id: 01-foundation
  status: planning

current_change:
  id: independent-profile-homes
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
  last_report: .planning/context-health/reports/20260624210101-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Official/internal independent home switching regression repaired and hardened. Doctor now accepts the managed internal Desktop app-server proxy chain, stale unavailable enabled plugin selectors have an explicit disable cleanup path, unavailable browser-use/local-personal dev-flow selectors were disabled in local config, pdf primary-runtime cache was refreshed, the generated local bundle was installed, and installed doctor passes on the real workstation.
---

# Workflow State

## Current Status

Change `independent-profile-homes` has an additional verified repair for the
official/internal switch regression reported on 2026-06-24. The repair prevents
`openai-official` from using a contaminated managed runtime config as its
profile seed when a clean explicit `openai-official.config.toml` layer exists,
merges legacy profile-layer plugin support blocks into generated independent
home configs, refreshes target-home profile layers from validated runtime
configs, and adds active-profile plugin materialization checks plus
`repair-plugins <profile>` remediation. One-key `codex-switch internal` and
`codex-switch official` now run plugin repair after a successful switch and
before doctor; `--skip-plugin-repair` skips that repair step. Plugin
directories and caches remain profile-local; repair refreshes target-profile
plugin marketplace/catalog state, primes the available plugin catalog, and
installs missing enabled plugins through the target profile's configured Codex
binary only when those plugins appear in the refreshed available catalog.
Unavailable enabled plugins are skipped by repair and left for doctor to report
as active-profile materialization issues. One-key `internal --help` and
`official --help` now print help without running self-update, switch, plugin
repair, doctor, or status steps.

The repair was hardened again on 2026-06-24. `codex-switch doctor` and
`codex-switch status` now recognize the valid managed internal Desktop chain
where Codex Desktop starts `codex-internal-app`, that wrapper starts
`codex_switch_app_proxy.py`, and the proxy starts the configured internal
`codex_bin` child app-server. `repair-plugins <profile>` also has an explicit
`--disable-unavailable` cleanup path that disables missing enabled plugin
selectors only after a real catalog refresh proves they are unavailable. This
keeps normal doctor checks read-only, keeps default repair behavior
catalog-aware, and gives stale config a durable cleanup path.

The real workstation was repaired and remains active on `internal`: active
`CODEX_HOME` is `/Users/cY/.codex-switch/homes/internal`, LaunchAgent and GUI
`CODEX_CLI_PATH` point to `/Users/cY/.codex-switch/bin/codex-internal-app`,
installed `codex-switch --skip-self-update doctor` passes, and status reports
the running app-server as `/Users/cY/.local/bin/codex (via app proxy pid
29858)`. The stale unavailable `browser-use@openai-bundled` and
`dev-flow@local-personal-plugins` selectors were disabled in the live shared
config, managed internal runtime config, and internal profile layer; the
enabled `dev-flow@cy-codex-skills` cache remains present.
`pdf@openai-primary-runtime` was refreshed to `26.623.12021` and now matches
source in the updater cache verification. The source checkout passes
verification, and
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`; that
generated local bundle was explicitly installed to
`/Users/cY/.local/share/codex-switch/current`.

Archive remains unavailable because the archive gate is closed.

## Next Action

No immediate repair action remains for the local Desktop/internal plugin
materialization issue: installed `codex-switch --skip-self-update doctor`
passes. Archive remains unavailable because the archive gate is closed. Do not
archive until the gate is explicitly opened. Separate follow-ups remain
available for project-local DevFlow skill layout migration and external
`gsd-core` update, but they are outside this repair.
