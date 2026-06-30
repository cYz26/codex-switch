---
workflow_version: 0.3.0
project_mode: brownfield
current_stage: verified

current_phase:
  id: 01-foundation
  status: planning

current_change:
  id: switch-verification-contract
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
  last_report: .planning/context-health/reports/20260629130742-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Official/internal independent home switching regression repaired and hardened. Doctor now accepts the managed internal Desktop app-server proxy chain, stale unavailable enabled plugin selectors have an explicit disable cleanup path, unavailable browser-use/local-personal dev-flow selectors were disabled in local config, pdf primary-runtime cache was refreshed, the generated local bundle was installed, internal Desktop config writes now preserve existing shared settings, current workstation configs were restored from the latest valid switch backup, the official unannotated runtime seed contamination regression is repaired broadly, source-profile plugin support snapshots now act as shared fallback after runtime narrowing, one-key switches now run target-profile verification before doctor, standalone verify supports safe repair, reports, and explicit runtime smoke, and the real workstation ends active on internal with restored shared plugin config, verify passing, and doctor passing.
---

# Workflow State

## Current Status

On 2026-06-29, the internal Desktop config-write regression was repaired.
Codex Desktop/app-server `config/value/write` and `config/batchWrite` calls are
now guarded in the internal app proxy by snapshotting the managed runtime
config before the write and restoring missing unrelated shared defaults after a
successful response, without overwriting the newly written Desktop value or
copying profile-specific model/provider settings from the snapshot. Regression
coverage was added for missing shared default restoration plus both app-server
config write methods.

The real workstation config was restored from
`/Users/cY/.codex-switch/backups/20260629T040238Z-switch-openai-official-to-internal/3-config.toml`
using the same merge helper. Pre-repair copies were saved in
`/Users/cY/.codex-switch/backups/20260629T043729Z-pre-config-preservation-repair/`.
Both `/Users/cY/.codex/config.toml` and
`/Users/cY/.codex-switch/homes/internal/config.toml` now validate as TOML and
again contain Desktop appearance settings, memories, restored enabled plugin
entries for `agent-kb@cy-codex-skills` and
`lark-feishu-ops@cy-codex-skills`, and the other missing shared support blocks
from the valid switch backup. The local release bundle was regenerated and
installed to `/Users/cY/.local/share/codex-switch/current`, and
`/Users/cY/.codex-switch/bin/codex-internal-app` now points `SWITCH_SCRIPTS` at
that installed bundle. The already-running Desktop app-server process must be
restarted by Codex Desktop before it loads the repaired proxy code.

On 2026-06-30, the official unannotated runtime seed contamination regression
was repaired. A real `codex-switch official` attempt had written
internal/Azure model-provider settings into the official profile layer and
canonical profile config even though the pre-switch official profile layer had
clean official `gpt-5.5` settings. The repair adds regression coverage for an
unannotated official runtime config that matches the internal source home,
skips that runtime seed when a clean explicit official profile layer exists,
and compares profile seeds after removing codex-switch managed comments. The
local bundle was rebuilt and installed, polluted official layer files were
backed up under
`/Users/cY/.codex-switch/backups/20260630111802-pre-official-layer-repair/`,
the clean layer was restored from
`20260630T025400Z-switch-internal-to-openai-official`, a real official switch
was verified to generate official `gpt-5.5` config without internal Azure
provider settings, and the workstation was switched back to `internal`.

On 2026-06-30, the repeated plugin/config loss after official-to-internal
switching was repaired more systemically. The root failure path was that
plugin support blocks were treated as shared config, while the canonical
profile config intentionally excluded them; if the current source home was
narrowed by another profile or Desktop write, switching back to `internal`
could use the old internal runtime only as the model/profile seed and discard
the runtime's marketplace/plugin/skill/hook blocks. The repair adds
profile-local plugin support snapshots named
`<profile>.plugin-support.config.toml`, merges previous runtime/snapshot
plugin support blocks as missing defaults when the source home lacks them, and
refreshes those snapshots from every generated runtime config, including the
managed internal Desktop wrapper path. The canonical profile config remains
profile-specific. Regression coverage was added for recovery from the target
runtime and from the profile-local snapshot after runtime loss, stale plugin
cleanup now updates snapshot files, and Desktop wrapper tests verify snapshot
refresh. Full profile-switch tests passed (90 tests), OpenSpec validated, the
local bundle was packaged and installed, and a real workstation
official-to-internal switch cycle ended active on `internal` with plugin repair
reporting no missing enabled plugins and doctor passing. The running Desktop
app-server process should still be restarted to load the updated proxy code.

After a Desktop restart on 2026-06-30, another gap was confirmed: the new
plugin-support snapshot mechanism prevented future loss only when at least one
current target runtime/snapshot still had the shared plugin blocks. The real
workstation's current official/internal runtime configs and snapshots had
already been narrowed, so the missing historical shared config was not
recovered. The official profile layer was also polluted again because the
previous official seed guard only skipped an unannotated provider runtime when
its profile seed exactly matched the internal source home; the real config was
similar but not identical. The repair now skips any unannotated
`openai-official` runtime seed containing `model_provider` when a clean
explicit official profile layer with `model` and no provider exists, and it
uses the source profile's `<profile>.plugin-support.config.toml` as shared
fallback defaults when switching profiles. Post-restart regressions were added
and verified. Current workstation configs were backed up under
`/Users/cY/.codex-switch/backups/20260630152911-pre-post-restart-shared-config-repair/`,
then restored from rich backup
`20260630T062435Z-switch-openai-official-to-internal/3-config.toml` and clean
official layers from
`20260630T065702Z-switch-internal-to-openai-official`. A real
`official -> internal` switch cycle passed. Final state: official runtime
`/Users/cY/.codex/config.toml` is `gpt-5.5` without `model_provider`;
internal runtime is Azure; both runtime/snapshot sets contain 5 marketplaces,
24 plugin blocks, and 43 hook trust blocks including agent-kb, lark-feishu-ops,
pdf, and game-design-workshop; `codex-switch --skip-self-update doctor`
passes.

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

On 2026-06-30, the switch verification contract was implemented as change
`switch-verification-contract`. `codex-switch verify <profile>` now validates
target active state, runtime config, official provider contamination, Desktop
binding/process observations in the managed default context, plugin support
snapshots, optional runtime smoke, explicit exec smoke, and optional JSON
reports. `--repair=safe` refreshes profile-local plugin support snapshots and
uses the existing catalog-aware plugin repair path only when enabled plugins
are actually missing. One-key `codex-switch internal` and
`codex-switch official` now run a Verification section after plugin repair and
before doctor; `--skip-verify`, `--runtime-smoke`, `--exec-smoke <prompt>`,
and `--verification-report` control diagnostic and post-upgrade depth. The
full profile-switch test file passed 97 tests, OpenSpec validation passed 10
items, the release bundle was packaged and installed locally, installed
`codex-switch --skip-self-update verify internal --repair=safe --report`
passed, installed `codex-switch --skip-self-update verify internal
--repair=safe --runtime-smoke --report` passed, and installed
`codex-switch --skip-self-update doctor` passed.

Archive remains unavailable because the archive gate is closed.

## Next Action

No immediate code or config repair action remains for the repeated
official/internal plugin-support loss or for the switch verification contract:
focused tests pass, the full test file passes, OpenSpec validates, the local
bundle and generated wrapper were refreshed, installed `verify internal
--repair=safe --report` passes, installed doctor passes, and profile-local
plugin support snapshots now exist for both profiles with the restored shared
plugin config. For a future internal Codex backend upgrade, run
`codex-switch internal --runtime-smoke --verification-report` after the update;
add `--exec-smoke <prompt>` only when a model-backed smoke is explicitly
desired. Restart Codex Desktop once more to make the currently running
app-server load the latest proxy/wrapper code. Archive remains unavailable
because the archive gate is closed. Do not archive until the gate is explicitly
opened. Separate follow-ups remain available for project-local DevFlow skill
layout migration and external `gsd-core` update, but they are outside this
repair.
