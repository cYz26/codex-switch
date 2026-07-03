# Tasks: Independent official and internal Codex homes with backup gate

## Target State

Implement the complete approved behavior for `independent-profile-homes`, not a partial delivery. Keep GSD phases as workflow governance and use the slices below as executable technical checkpoints.

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
- `openspec/changes/independent-profile-homes/proposal.md`
- `openspec/changes/independent-profile-homes/design.md`
- `openspec/changes/independent-profile-homes/specs/`
- relevant source and test files

**Implementation**
- [x] Review requirements and scenarios.
- [x] Record local capability evidence; no external capability dependency is required.
- [x] Identify affected files and compatibility constraints.

**Tests**
- [x] Added failing tests for independent homes, backup gate, dry-run output, and restore.

**Validation Commands**
```bash
openspec validate independent-profile-homes --strict --no-interactive
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
- `scripts/codex_switch_home_sync.py`
- `scripts/codex_switch_backup.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add failing tests for independent homes, backup gate, dry-run output, and restore.
- [x] Implement shared-state classification and sync planning.
- [x] Implement backup capture/finalize and restore.
- [x] Implement official/internal independent activation.
- [x] Keep edits scoped to the active change.

**Tests**
- [x] Run focused regression tests.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_switch_uses_managed_home_and_backup_plan
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_restore_backup_dry_run_and_apply
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_backup_failure_aborts_before_mutation
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
- `openspec/changes/independent-profile-homes/tasks.md`

**Implementation**
- [x] Run broader project verification where applicable.
- [x] Record verification evidence.
- [x] Update workflow state and this ledger.

**Tests**
- [x] Run the smallest relevant broader suite.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Done When**
- [x] Verification evidence exists and the Completion Contract is checked.

**Risks / Rollback**
- Keep archive blocked until verification evidence is recorded.

### Slice 4: Runtime-first config merge follow-up

**Status:** done

**Goal**
- Preserve target profile runtime config edits across switches while keeping a
  refreshed canonical fallback and clear TOML section comments.

**Files / Modules**
- `scripts/codex_switch_config.py`
- `scripts/codex_switch_home_sync.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_toml_validate.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`

**Implementation**
- [x] Add failing tests for target runtime config preference, invalid-runtime
  fallback, official runtime profile preservation, and managed TOML comments.
- [x] Prefer the target profile's last valid runtime config as the
  profile-specific merge seed.
- [x] Fall back to canonical profile config when the target runtime config is
  missing or invalid.
- [x] Refresh canonical profile config from validated runtime config without
  copying shared settings into canonical config.
- [x] Add managed TOML comments marking profile-specific and shared settings.
- [x] Add Python 3.9-compatible basic TOML validation so fallback protection is
  active when `tomllib` is unavailable.

**Tests**
- [x] Run focused regression tests for runtime-first config merge and fallback.
- [x] Run broader project verification.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical \
  CodexProfileSwitchTests.test_internal_switch_falls_back_to_canonical_when_last_runtime_config_is_invalid \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Done When**
- [x] Full verification passes and evidence is recorded.

**Risks / Rollback**
- If merge validation rejects a valid Codex config shape, narrow the basic
  validator and add a regression case before completion.

### Slice 5: Profile home selection and legacy internal adoption

**Status:** done

**Goal**
- Let legacy internal users keep using the existing `~/.codex` home for
  `internal` while assigning `openai-official` a distinct managed home, with
  persisted profile home bindings and collision protection.

**Files / Modules**
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- `scripts/codex_switch_store.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`

**Implementation**
- [x] Add failing tests for internal adopting the existing Codex home, explicit
  home collision rejection, and wrapper argument forwarding.
- [x] Add `--internal-codex-home <path>` and persist profile home bindings in
  manifests.
- [x] Resolve independent profile homes from CLI override, manifest binding, and
  default managed homes.
- [x] Auto-assign `openai-official` to a managed home when `internal` explicitly
  adopts the previous official home and official was not explicitly locked to
  that same path.
- [x] Refuse explicit identical homes before backup or mutation.
- [x] Add interactive home selection for TTY switches with existing-home,
  managed-home, and custom-path options.
- [x] Ensure backup plans include any profile manifests whose home bindings will
  be written.

**Tests**
- [x] Run focused home adoption tests.
- [x] Run broader project verification.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_can_adopt_live_home_and_move_official_home \
  CodexProfileSwitchTests.test_switch_rejects_explicit_identical_independent_homes \
  CodexProfileSwitchTests.test_wrapper_forwards_internal_codex_home_option
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Done When**
- [x] Full verification passes and evidence is recorded.

**Risks / Rollback**
- If interactive prompting makes wrapper dry-run/apply flows inconsistent, keep
  prompting limited to direct TTY switches and require explicit CLI paths for
  non-interactive automation.

### Slice 6: Interactive home prompt refinement

**Status:** done

**Goal**
- Improve interactive home selection so the target profile is prompted first,
  recommended directories are first and labelled, and same-home collisions can
  be corrected without exiting.

**Files / Modules**
- `scripts/codex_switch_home_select.py`
- `scripts/codex_switch_switching.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`

**Implementation**
- [x] Add failing tests for target-first prompt order, recommended option
  labelling, and interactive same-home collision recovery.
- [x] Pass the target profile into home resolution.
- [x] Order prompts as target profile first, then the other independent profile.
- [x] Order prompt options with the recommended path first, the other profile's
  current path second, and custom path available.
- [x] Re-prompt interactively when both independent profiles resolve to the same
  home; keep non-interactive same-home rejection.

**Tests**
- [x] Run focused prompt refinement tests.
- [x] Run broader project verification.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_interactive_home_prompt_prioritizes_target_profile_and_recommended_option \
  CodexProfileSwitchTests.test_interactive_same_home_collision_prompts_for_other_profile_home
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Done When**
- [x] Full verification passes and evidence is recorded.

**Risks / Rollback**
- If prompt behavior becomes awkward in automation, keep prompts disabled for
  dry-run and non-TTY execution and preserve explicit CLI path overrides.

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Capability evidence and validation surface | done | `openspec validate independent-profile-homes --strict --no-interactive` |
| Implementation and focused verification | done | `python3 scripts/test_codex_profile_switch.py` |
| Broader verification and state update | done | `.planning/verification/20260608230035-independent-profile-homes-verification.md` |
| Runtime-first config merge follow-up | done | `.planning/verification/20260609115253-runtime-config-merge-follow-up.md` |
| Profile home selection and legacy internal adoption | done | `.planning/verification/20260609174225-home-selection-adoption.md` |
| Interactive home prompt refinement | done | `.planning/verification/20260609180600-interactive-home-prompt-refinement.md` |
| Bulky support sync exclusion repair | done | `.planning/verification/20260609183515-bulky-support-sync-exclusion.md` |
| Active-home-aware prompt repair | done | `.planning/verification/20260609185052-active-home-aware-prompt-repair.md` |
| Semantic prompt recommendation repair | done | `.planning/verification/20260609185938-semantic-prompt-recommendation-repair.md` |
| Desktop wrapper runtime config comments | done | `.planning/verification/20260609204042-desktop-wrapper-runtime-config-comments.md` |
| Shared support symlink loop repair | done | `.planning/verification/20260609210522-shared-support-symlink-loop-repair.md` |
| Official Desktop personality preservation | done | `.planning/verification/20260610123723-official-personality-preservation.md` |
| Removed profile setting preservation | done | `.planning/verification/20260610125325-removed-profile-setting-preservation.md` |
| Invalid reasoning effort runtime guard | done | `.planning/verification/20260610145055-invalid-reasoning-effort-runtime-guard.md` |
| Internal Desktop model alias proxy | done | `.planning/verification/20260612184349-internal-desktop-model-alias-proxy.md` |
| Official switch contamination and plugin layer repair | done | `.planning/verification/20260624152010-official-switch-contamination-plugin-repair.md` |
| Active profile plugin materialization repair | done | `.planning/verification/20260624180317-plugin-materialization-repair.md` |
| Plugin repair help and unavailable-catalog hardening | done | `.planning/verification/20260624193841-plugin-repair-hardening.md` |
| Proxy-aware doctor and stale plugin cleanup hardening | done | `.planning/verification/20260624205509-proxy-doctor-stale-plugin-cleanup.md` |
| Profile-local plugin support snapshot repair | verified | `.planning/verification/20260630145758-profile-plugin-support-snapshot-repair.md` |
| Bidirectional shared settings shrink prevention | verified | `.planning/verification/20260703215156-bidirectional-shared-settings-shrink-prevention.md` |

### Bidirectional Shared Settings Shrink Prevention

**Status:** verified

**Skill Routing Ledger**
- request kind: repeated workflow repair / compatibility hardening
- systematic-debugging: used; backup timelines, current profile homes,
  wrapper startup, switch-time merge, and snapshot refresh were inspected
  before implementation
- brainstorming: used; selected systemic shared-config merge repair instead
  of a one-off Desktop settings restore
- writing-plans: used; this OpenSpec ledger is the canonical implementation
  plan for the repair
- test-driven-development: used; regressions are added before production code
- OpenSpec routing: existing `independent-profile-homes` change is updated
  because profile switching persistence and compatibility behavior change

**Target State**
- Shared TOML config sync is bidirectional and non-destructive: the source
  profile's present shared values can update the target profile, but source
  omissions do not delete target-only shared Desktop, memories, apps, plugin,
  skill, MCP, hook, or related shared settings.
- Internal Desktop wrapper startup cannot narrow the official home when the
  managed internal app home has a smaller shared config.
- Switching back to `openai-official` from a narrowed internal runtime keeps
  official-only shared settings while applying new source shared values.
- Plugin support snapshot refresh keeps existing richer plugin/skill/hook
  support as missing defaults when the current runtime was narrowed.

**Completion Contract**
- [x] Focused regressions fail before implementation and pass after the fix.
- [x] Existing plugin support, Desktop wrapper, and official contamination
  regressions still pass.
- [x] OpenSpec validates after the scenario update.
- [x] Verification evidence and workflow state are updated.

**Capability Slice**
- [x] Add regression for internal Desktop wrapper startup preserving official
  shared Desktop/apps/memories/plugin/skill settings while folding in new
  internal shared values.
- [x] Add regression for `internal -> openai-official` preserving target
  shared settings when the internal source runtime is narrowed.
- [x] Add regression for plugin support snapshot refresh refusing to shrink to
  an empty runtime-derived snapshot.
- [x] Change table merge semantics from whole-table replacement to
  assignment-level overlay with missing-key preservation.
- [x] Merge target runtime shared config as missing defaults during switch
  config generation, not only plugin-support blocks.
- [x] Refresh plugin support snapshots by unioning runtime-derived support with
  existing snapshots as missing defaults.
- [x] Run focused, broader, OpenSpec, and diff validation.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_does_not_narrow_official_shared_settings \
  CodexProfileSwitchTests.test_official_switch_does_not_narrow_existing_shared_settings \
  CodexProfileSwitchTests.test_plugin_support_snapshot_refresh_does_not_shrink_to_runtime_loss
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
openspec validate independent-profile-homes --strict --no-interactive
git diff --check
```

**Verification Evidence**
- Focused regressions failed before implementation because wrapper startup
  narrowed official `[desktop]`, official switch generated a narrowed
  official runtime config from the narrowed internal source, and plugin support
  snapshot refresh overwrote a rich snapshot with an empty snapshot.
- Focused repaired regressions passed, 3 tests.
- Adjacent plugin support, app proxy config-write, official contamination, and
  Desktop wrapper regressions passed, 14 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 120 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed, and `openspec validate --all --strict --no-interactive` passed 11
  items.
- `git diff --check` passed.
- `scripts/package-release.sh` passed and wrote
  `dist/codex-switch.tar.gz`.
- `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh` passed and
  refreshed the local installed `codex-switch` bundle.
- Installed `codex-switch --skip-self-update status` passed; it reports the
  existing current-shell `PATH codex` mismatch and recommends
  `eval "$(codex-switch shim-env)"` for shell alignment.
- Evidence recorded in
  `.planning/verification/20260703215156-bidirectional-shared-settings-shrink-prevention.md`.

### Profile-local Plugin Support Snapshot Repair

**Status:** verified

**Skill Routing Ledger**
- request kind: repeated workflow repair / compatibility hardening
- systematic-debugging: used; current wrapper, app-server process chain,
  profile homes, manifests, plugin lists, and switch backups were inspected
  before implementation
- test-driven-development: used; add failing regressions before production
  code
- OpenSpec routing: existing `independent-profile-homes` behavior change is
  updated because profile switching compatibility and error handling change

**Target State**
- Profile-local plugin support settings (`marketplaces.*`, `plugins.*`,
  `skills.config`, and `hooks.state.*`) have a durable profile-local snapshot
  and are not solely dependent on the current source home retaining those
  blocks.
- Switching back to `internal` after `official` or after an internal CLI update
  restores previously configured plugin support blocks from the target
  runtime/snapshot when the source home has been narrowed.
- The canonical profile config remains profile-specific and does not become a
  second shared-plugin source of truth.

**Completion Contract**
- [x] Focused regressions fail before implementation and pass after the fix.
- [x] Existing official contamination and plugin materialization regressions
  still pass.
- [x] OpenSpec validates after the scenario update.
- [x] Verification evidence and workflow state are updated.

**Capability Slice**
- [x] Add regression for switching back to `internal` when the official source
  config lacks plugin support blocks but the internal runtime retained them.
- [x] Add regression for the profile-local plugin support snapshot restoring
  plugin blocks after the target runtime was narrowed.
- [x] Implement snapshot refresh and fallback merge without copying plugin
  cache directories between profiles.
- [x] Include snapshot files in backup and stale-selector cleanup paths.
- [x] Run focused and broader validation.

**Post-restart Follow-up**
- [x] Add regression for source profile plugin-support snapshots acting as
  shared fallback when the source runtime config is narrowed.
- [x] Add regression for explicit official profile layer winning over any
  unannotated provider runtime, even when the provider runtime is not an exact
  profile-seed match for the internal source home.
- [x] Restore the real workstation shared config from the latest rich backup,
  regenerate plugin-support snapshots, and re-run real switch/doctor checks.

**Post-restart Verification Evidence**
- New post-restart regressions failed before implementation:
  `test_official_switch_ignores_unannotated_provider_runtime_when_explicit_layer_is_clean`
  preserved `workspace-provider-model`/`model_provider = "azure"` in official,
  and `test_internal_switch_restores_plugin_support_from_source_profile_snapshot`
  dropped `[marketplaces.cy-codex-skills]`.
- The two new regressions passed after implementation.
- Focused neighboring regression set passed, 9 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 92 tests.
- `python3 -m py_compile scripts/*.py`, shell syntax checks,
  `openspec validate --all --strict --no-interactive`, and `git diff --check`
  passed.
- `scripts/package-release.sh` passed and the local bundle was installed.
- Current real workstation configs were backed up under
  `/Users/cY/.codex-switch/backups/20260630152911-pre-post-restart-shared-config-repair/`.
- Real workstation shared config was restored from rich backup
  `20260630T062435Z-switch-openai-official-to-internal/3-config.toml`, clean
  official profile layers were restored from
  `20260630T065702Z-switch-internal-to-openai-official`, official/internal
  runtime configs and plugin-support snapshots were regenerated, and a real
  `official -> internal` switch cycle passed.
- Final real state: `/Users/cY/.codex/config.toml` is official `gpt-5.5`
  without `model_provider`; `/Users/cY/.codex-switch/homes/internal/config.toml`
  is internal Azure; both runtime/snapshot sets contain 5 marketplaces, 24
  plugin blocks, and 43 hook trust blocks including agent-kb, lark-feishu-ops,
  pdf, and game-design-workshop. `codex-switch --skip-self-update doctor`
  passed.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_target_runtime_when_source_lost_it \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_profile_snapshot_after_runtime_loss
openspec validate independent-profile-homes --strict --no-interactive
```

**Verification Evidence**
- New regression failed before implementation because internal switch dropped
  `[marketplaces.cy-codex-skills]` and the profile-local plugin support
  snapshot did not exist.
- Focused regression command passed, 2 tests.
- Neighboring contamination, plugin cleanup, Desktop wrapper, and one-key
  auto-update regressions passed, 7 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 90 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed, and `openspec validate --all --strict --no-interactive` passed 9
  items.
- `git diff --check` passed.
- `scripts/package-release.sh` passed and wrote `dist/codex-switch.tar.gz`.
- Installed the repaired local bundle with
  `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh`.
- Real workstation switch cycle completed:
  `codex-switch --skip-self-update official --skip-login --skip-update-check --skip-plugin-repair --skip-doctor --no-status --skip-launchctl`
  then
  `codex-switch --skip-self-update internal --skip-update-check --skip-launchctl`.
  The final internal switch ran plugin repair, reported no missing enabled
  plugins, doctor passed, and status showed active `internal`.
- Real internal runtime and both internal plugin-support snapshots contain the
  expected marketplace, plugin, and hook trust blocks; generated
  `codex-internal-app` imports and calls
  `refresh_profile_plugin_support_snapshot`.

### Proxy-aware Doctor and Stale Plugin Cleanup Hardening

**Status:** done

**Skill Routing Ledger**
- request kind: workflow repair / compatibility hardening
- `capability-research`: used; local process tree, wrapper, plugin catalog, and
  profile cache state were inspected before selecting the implementation path
- `brainstorming`: used; selected systemic repair over another restart-only or
  manual-config-only recommendation
- `writing-plans`: used; this OpenSpec ledger is the canonical plan instead of
  a parallel Superpowers document
- OpenSpec routing: existing `independent-profile-homes` change updated before
  implementation because behavior, compatibility, and error-handling change

**Target State**
- `codex-switch doctor` accepts the valid internal Desktop app-server launch
  chain where `codex-internal-app` starts `codex_switch_app_proxy.py` and the
  proxy starts the configured internal `codex_bin` child process.
- Missing enabled plugin checks keep reporting real profile-local cache gaps,
  but stale enabled plugin selectors that are unavailable in the refreshed
  catalog have an explicit `--disable-unavailable` cleanup path.
- The cleanup path disables stale selectors in runtime and reseeding config
  files without deleting plugin directories, copying plugin state across
  profiles, or silently changing config during normal doctor checks.

**Completion Contract**
- [x] Focused regression tests fail before implementation and pass after it.
- [x] Existing plugin repair install/skip behavior remains compatible.
- [x] `codex-switch doctor` stops reporting the proxy-child app-server as a
  stale process while still reporting direct mismatched app-server processes.
- [x] `repair-plugins <profile> --disable-unavailable` disables unavailable
  stale selectors and makes the focused doctor check pass for those selectors.
- [x] Verification evidence and workflow state are updated.

**Files / Modules**
- `scripts/codex_switch_running_app.py`
- `scripts/codex_switch_plugins.py`
- `scripts/codex_profile_switch.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`
- `.planning/STATE.md`
- `.planning/verification/`

**Capability Slices**
- [x] Add process-tree parsing and proxy-aware app-server doctor/status
  behavior.
- [x] Add unavailable enabled plugin disable support behind explicit
  `repair-plugins <profile> --disable-unavailable`.
- [x] Preserve existing default repair behavior and dry-run truthfulness.
- [x] Record validation evidence and update state.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_running_desktop_problem_accepts_internal_proxy_child_app_server
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_disable_unavailable_stale_enabled_plugins
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_skips_unavailable_enabled_plugins_after_catalog_refresh
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_running_desktop_problem_reports_stale_app_server
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
git diff --check
```

### Active Profile Plugin Materialization Repair

**Status:** done

**Goal**
- Keep plugin directories and caches profile-local while detecting when the
  active profile's synced plugin configuration references enabled plugins that
  are not installed in that profile's `CODEX_HOME`.
- Provide an explicit repair command that installs missing enabled plugins
  through the target profile's configured Codex binary, without copying or
  symlinking another profile's `plugins` directory.

**Files / Modules**
- `scripts/codex_switch_plugins.py`
- `scripts/codex_switch_doctor_active.py`
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`
- `.planning/verification/`

**Implementation**
- [x] Add active-profile doctor checks for enabled plugin configs whose
  profile-local install cache is missing.
- [x] Add `repair-plugins <profile>` with a dry-run option and target
  `CODEX_HOME` scoping.
- [x] Refresh the target profile's plugin marketplace/catalog view inside
  `repair-plugins <profile>` before checking for missing enabled plugins.
- [x] Run `repair-plugins <profile>` automatically after successful one-key
  switches, before doctor, with `--skip-plugin-repair` as the explicit opt-out.
- [x] Filter missing enabled plugin installs through the refreshed available
  plugin catalog so unavailable enabled plugins do not fail the repair step.
- [x] Keep `repair-plugins --dry-run` from printing unverified `plugin add`
  commands before the available catalog has actually been refreshed.
- [x] Make one-key `internal --help` and `official --help` side-effect free.
- [x] Keep plugin cache materialization explicit instead of expanding shared
  support sync to include `plugins/`.

**Tests**
- [x] Run focused doctor and repair-plugin regression tests.
- [x] Run available plugin catalog refresh regression tests for missing and
  already-installed enabled plugin states.
- [x] Run unavailable plugin, plugin repair dry-run, and one-key help
  regression tests.
- [x] Run one-key switch post-switch repair regression tests.
- [x] Run the smallest relevant broader regression set.

### Official Switch Contamination and Plugin Layer Repair

**Status:** done

**Goal**
- Repair the regression where switching back to `official` can preserve
  internal-only model/provider settings from a managed official runtime config,
  and where legacy profile-layer plugin enablement is dropped when profiles use
  independent homes.

**Files / Modules**
- `scripts/codex_switch_home_sync.py`
- `scripts/codex_switch_switching.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`
- `.planning/verification/`

**Implementation**
- [x] Add regression tests for contaminated managed official runtime config
  repair.
- [x] Add regression tests for legacy profile-layer plugin settings merging
  into generated independent home configs.
- [x] Prefer explicit profile-layer seeds over contaminated managed official
  runtime seeds.
- [x] Merge plugin support shared blocks from legacy profile layers into the
  generated runtime shared config.
- [x] Refresh target-home profile layers and canonical profile configs from the
  validated generated runtime config.

**Tests**
- [x] Run focused official/plugin regression tests.
- [x] Run the smallest relevant broader regression set.

### Invalid Reasoning Effort Runtime Guard

**Status:** done

**Goal**
- Prevent unsupported runtime `model_reasoning_effort` values from persisting
  into managed internal homes when the active model catalog declares the
  supported effort set.

**Files / Modules**
- `scripts/codex_switch_home_sync.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`

**Implementation**
- [x] Add a failing regression test for a valid TOML runtime config whose
  `model_reasoning_effort` is unsupported by the configured model catalog.
- [x] Treat that runtime seed as invalid and fall back to the canonical
  profile config.
- [x] Preserve existing runtime-first behavior when no catalog support data is
  available.

**Tests**
- [x] Run focused regression coverage for the invalid reasoning effort guard.
- [x] Run the smallest relevant broader regression set.

### Internal Desktop Model Alias Proxy

**Status:** done

**Goal**
- Prevent Codex Desktop from showing the static fallback reasoning-effort list
  with `Max` when the internal profile uses a versioned Azure/AIDP deployment
  model that the Desktop frontend treats as a custom model.

**Files / Modules**
- `scripts/codex_switch_app_proxy.py`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`

**Implementation**
- [x] Add a regression test for masking a versioned deployment model to a
  Desktop-compatible alias while preserving the catalog-supported effort list.
- [x] Add a regression test for masking thread and conversation model fields
  that the Desktop composer uses for reasoning-effort lookup.
- [x] Add a regression test for translating Desktop alias selections back to
  the versioned backend deployment model.
- [x] Route managed internal `app-server --stdio` launches through the proxy
  while keeping non-app-server wrapper invocations unchanged.
- [x] Regenerate the local internal Desktop wrapper and verify the proxied
  `model/list`, `config/read`, and thread/conversation payloads expose
  `gpt-5.5` with `low`, `medium`, `high`, and `xhigh` only.

**Tests**
- [x] Run focused regression coverage for the app proxy and wrapper route.
- [x] Run the smallest relevant broader regression set.

### Internal Desktop Config Write Preservation

**Status:** verified

**Goal**
- Prevent Codex Desktop config writes in internal mode from dropping unrelated
  shared settings such as Desktop appearance, memories, apps, plugin
  marketplaces, enabled plugins, skill config, MCP servers, and hook trust
  state, then restore the current workstation config from the latest valid
  switch backup.

**Files / Modules**
- `scripts/codex_switch_config.py`
- `scripts/codex_switch_app_proxy.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/independent-profile-homes/specs/codex-switch/spec.md`
- `.planning/STATE.md`

**Implementation**
- [x] Add failing regression tests for preserving missing shared config blocks
  while keeping the newly written Desktop value.
- [x] Add failing regression tests for app proxy repair after
  `config/value/write` and `config/batchWrite`.
- [x] Implement a missing-default shared config merge helper that excludes
  profile-specific model/provider settings.
- [x] Have the internal app proxy snapshot managed runtime config before
  Desktop config writes and restore missing unrelated shared settings after
  successful backend writes.
- [x] Restore the current workstation shared/internal runtime config from the
  latest valid backup using the same preservation helper.
- [x] Refresh the installed codex-switch bundle and generated internal Desktop
  wrapper so future Desktop launches use the repaired proxy.

**Tests**
- [x] Run focused config preservation and proxy tests.
- [x] Run the smallest relevant broader regression set.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_missing_shared_config_defaults_preserve_new_desktop_value \
  CodexProfileSwitchTests.test_app_proxy_restores_missing_shared_config_after_config_value_write \
  CodexProfileSwitchTests.test_app_proxy_restores_missing_shared_config_after_config_batch_write
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
scripts/codex-switch --skip-self-update doctor
```

**Verification Evidence**
- Focused config preservation/proxy tests: 3 tests passed.
- Full `scripts/test_codex_profile_switch.py`: 87 tests passed.
- Syntax checks passed for Python scripts and shell entrypoints.
- Workstation configs restored from
  `~/.codex-switch/backups/20260629T040238Z-switch-openai-official-to-internal/3-config.toml`;
  pre-repair copies saved under
  `~/.codex-switch/backups/20260629T043729Z-pre-config-preservation-repair/`.
- Installed bundle refreshed at
  `~/.local/share/codex-switch/current`; generated internal app wrapper points
  `SWITCH_SCRIPTS` at that installed bundle.
- `codex-switch --skip-self-update doctor` passed after restoration.

### Official Unannotated Runtime Seed Contamination Repair

**Status:** verified

**Skill Routing Ledger**
- request kind: bug repair for profile switching behavior
- capability-research: used; local status, manifests, LaunchAgent, backups,
  and runtime configs were inspected
- systematic-debugging: used; root cause was traced before code changes
- writing-plans: used; AGENTS.md routes the execution ledger into this
  OpenSpec task file instead of a secondary Superpowers plan file
- test-driven-development: used; add a failing regression before
  implementation
- OpenSpec routing: use existing `independent-profile-homes` behavior change

**Target State**
- `codex-switch official` must not treat an unannotated config copied from or
  matching the internal source home as the official profile seed when an
  explicit `openai-official.config.toml` profile layer exists.
- Official runtime and canonical profile configs keep official model/provider
  settings, while shared settings from internal still merge forward.

**Completion Contract**
- [x] Regression test fails before implementation and passes after the fix.
- [x] Existing contamination, runtime-first, and shared-preference regressions
  still pass.
- [x] OpenSpec validates after the scenario update.
- [x] Verification evidence is recorded.

**Capability Slice**
- [x] Add a regression for unannotated official runtime contamination where
  live `config.toml` matches the internal source home but
  `openai-official.config.toml` contains the clean official model.
- [x] Skip that contaminated runtime seed and use explicit profile-layer or
  canonical profile seed instead.
- [x] Run focused and OpenSpec validation.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings \
  CodexProfileSwitchTests.test_switch_preserves_live_shared_preferences
openspec validate independent-profile-homes --strict --no-interactive
```

**Verification Evidence**
- New regression failed before implementation because official runtime kept
  `model = "internal-model"` and `model_provider = "azure"`.
- Focused regression command passed, 4 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 88 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed, and `openspec validate --all --strict --no-interactive` passed 9
  items.
- `scripts/package-release.sh` passed and wrote `dist/codex-switch.tar.gz`.
- Installed the repaired bundle through local `install.sh`, restored the
  polluted official profile layer from pre-contamination backup
  `20260630T025400Z-switch-internal-to-openai-official`, verified a real
  `official` switch generated official `gpt-5.5` config without internal
  Azure provider settings, then switched back to `internal`.

### Desktop Global Settings State Sync Repair

**Status:** verified

**Skill Routing Ledger**
- request kind: bug repair after internal switch; settings state missing
- systematic-debugging: used; root cause was traced to Desktop settings stored
  in `.codex-global-state.json`, while TOML settings were already syncing
- writing-plans / ai-native-tech-plan: used; canonical plan is recorded in this
  OpenSpec task ledger instead of a second Superpowers plan file
- test-driven-development: used; write failing regressions before production
  changes
- capability-research: skipped; evidence is from local installed homes,
  Desktop state file contents, and repository code/tests
- OpenSpec routing: update existing `independent-profile-homes` compatibility
  change
- archive gate: closed; do not archive, record verification and state only

**Target State**
- Switching to `internal` and launching its Desktop wrapper keeps user-facing
  Desktop settings continuous when those settings live in
  `.codex-global-state.json`.
- `.codex-global-state.json` is not copied, linked, or treated as generic
  shared support. Only a safe Desktop settings subset is merged.
- Prompt history, thread permissions, queued follow-ups, remote thread
  summaries, credentials, and remote routing identifiers stay profile-local.

**Completion Contract**
- [x] Regression test fails before implementation and passes after the fix.
- [x] Switch-time sync covers official -> internal and internal -> official.
- [x] Internal Desktop wrapper startup covers live official -> managed internal.
- [x] Existing runtime-state isolation tests still prove disallowed state is not
  linked or copied wholesale.
- [x] Verification evidence is recorded and `.planning/STATE.md` is updated.

**Capability Slice**
- [x] Add failing tests for sanitized Desktop global settings state merge and
  wrapper startup behavior.
- [x] Add a JSON merge helper that allowlists top-level Desktop settings and
  filters session/runtime keys from `electron-persisted-atom-state`.
- [x] Call the helper from independent switch flows and the generated internal
  Desktop wrapper.
- [x] Run focused regressions, broader profile-switch tests, syntax checks,
  OpenSpec validation, and release packaging.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Verification Evidence**
- The new focused regressions failed before implementation:
  `merge_desktop_global_state_settings` was missing, internal switch did not
  create `.codex-global-state.json`, and wrapper startup left stale internal
  Desktop settings unchanged.
- Focused new regressions passed, 3 tests.
- Adjacent shared-state and wrapper isolation regressions passed, 9 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 107 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed, and `openspec validate --all --strict --no-interactive` passed 11
  items.
- `scripts/package-release.sh` passed and wrote `dist/codex-switch.tar.gz`.
- `git diff --check` passed.
- Installed bundle refreshed through `./install.sh`.
- Current workstation internal home was repaired by merging the sanitized
  Desktop global settings subset from `/Users/cY/.codex` into
  `/Users/cY/.codex-switch/homes/internal/.codex-global-state.json`; key-only
  verification showed no copied prompt-history, thread permission, draft,
  unread-thread, remote-summary, or thread-client-id atom keys.

### Settings Panel Pets Support Sync Repair

**Status:** verified

**Skill Routing Ledger**
- request kind: follow-up bug repair for Desktop Settings panel parity and
  Plugins/Skills sync audit
- plugin-project-migration: used sync-only; report is `migration_pending` due
  to legacy `.codex/skills` duplicates and conflicts with `.agents/skills`; no
  apply was run
- systematic-debugging: used; evidence shows TOML config, global Desktop
  settings, Plugins/Skills config, hooks, and MCP entries are synced, while
  `pets/` remains excluded from shared support
- writing-plans / OpenSpec routing: use existing `independent-profile-homes`
  change and this task ledger
- test-driven-development: used; add failing `pets/` shared-support regression
  before production changes
- archive gate: closed; do not archive, record verification and state only

**Target State**
- The Desktop Settings sidebar categories remain continuous when switching to
  `internal`: General/Appearance/Configuration/Personalization use the existing
  TOML and sanitized global-state sync, while Pets gets its `pets/` support
  directory through shared support sync.
- Plugins, Skills, marketplaces, hooks, and MCP config continue to sync through
  TOML/plugin-support snapshots and profile-local plugin repair/materialized
  caches; `plugins/` cache directories are not copied or symlinked wholesale.
- Credentials, secrets, browser/process state, sqlite state, sessions,
  histories, and model catalogs remain profile-local or excluded.

**Completion Contract**
- [x] Regression test fails before implementation and passes after the fix.
- [x] `pets/` is included in shared support targets and can be linked/copied
  like other stable support directories.
- [x] Existing bulky-state exclusion tests still prove `plugins/`, credentials,
  caches, and runtime state are excluded.
- [x] Local audit confirms current Plugins/Skills config parity.
- [x] Verification evidence is recorded and `.planning/STATE.md` is updated.

**Capability Slice**
- [x] Add a failing shared-support test for `pets/` during internal switch.
- [x] Remove `pets` from the Python and generated-shell non-shareable lists.
- [x] Update README wording for Settings support versus bulky/runtime state.
- [x] Run focused regressions, full tests, syntax checks, OpenSpec validation,
  package generation, and diff check.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_pets_settings_support
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_excludes_bulky_support_state_from_sync_plan \
  CodexProfileSwitchTests.test_internal_switch_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_doctor_accepts_active_profile_enabled_plugin_cache \
  CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
codex-switch --skip-self-update repair-plugins internal --dry-run
```

**Verification Evidence**
- The new `pets/` regressions failed before implementation because internal
  switch and the generated Desktop wrapper did not materialize `pets/`.
- Focused `pets/` regressions passed, 2 tests.
- Adjacent settings/shared-support/wrapper/plugin regressions passed, 11 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 109 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed, and `openspec validate --all --strict --no-interactive` passed 11
  items.
- `scripts/package-release.sh` passed and wrote `dist/codex-switch.tar.gz`.
- `git diff --check` passed.
- Installed bundle refreshed through `./install.sh`.
- Current workstation internal home now has
  `/Users/cY/.codex-switch/homes/internal/pets -> /Users/cY/.codex/pets`.
- Current workstation `repair-plugins internal --dry-run` reports no missing
  enabled plugins. Internal `skills` is a symlink to `/Users/cY/.codex/skills`,
  and internal `plugins` remains a profile-local directory.
- `verify internal --runtime-smoke --report` passed runtime smoke but failed
  profile-active assertions because the active profile intentionally remained
  `openai-official`; this is recorded as context mismatch, not plugin failure.

## Acceptance Criteria

- [x] Required behavior matches the OpenSpec scenarios.
- [x] Tests cover the changed behavior.
- [x] No required capability remains unimplemented without a blocker.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

## Final Verification

- [x] Focused tests pass.
- [x] Broader tests, lint, typecheck, or build pass where applicable.
- [x] Verification evidence is recorded.
