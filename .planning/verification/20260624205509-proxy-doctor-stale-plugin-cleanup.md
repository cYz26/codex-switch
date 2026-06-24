# Verification: Proxy-aware Doctor and Stale Plugin Cleanup

## Scope

- Updated `codex-switch doctor` / `status` process checks so a Desktop
  app-server child launched through `codex_switch_app_proxy.py` is treated as
  the expected managed internal Desktop binding.
- Added explicit `repair-plugins <profile> --disable-unavailable` cleanup for
  enabled plugin selectors that remain unavailable after a real catalog refresh.
- Disabled stale local config entries for `browser-use@openai-bundled` and
  `dev-flow@local-personal-plugins` in the current internal profile state.
- Refreshed `pdf@openai-primary-runtime` in the internal profile cache.

## Evidence

| Command | Result |
| --- | --- |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_running_desktop_problem_accepts_internal_proxy_child_app_server` | pass |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_disable_unavailable_stale_enabled_plugins` | pass |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_skips_unavailable_enabled_plugins_after_catalog_refresh` | pass |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins` | pass |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_repair_plugins_dry_run_does_not_claim_unverified_plugin_add` | pass |
| `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_running_desktop_problem_reports_stale_app_server` | pass |
| `python3 scripts/test_codex_profile_switch.py` | pass, 84 tests |
| `python3 -m py_compile scripts/*.py` | pass |
| `bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh` | pass |
| `openspec validate independent-profile-homes --strict --no-interactive` | pass |
| `git diff --check` | pass |
| `python3 scripts/codex_profile_switch.py repair-plugins internal --disable-unavailable` | pass, disabled two unavailable stale plugin selectors |
| `python3 scripts/codex_profile_switch.py doctor` | pass |
| `scripts/package-release.sh` | pass, generated `dist/codex-switch.tar.gz` |
| `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch/dist/codex-switch ./install.sh` | pass, installed local bundle |
| `CODEX_HOME=/Users/cY/.codex-switch/homes/internal codex plugin add pdf@openai-primary-runtime --json` | pass, installed `pdf@openai-primary-runtime` `26.623.12021` |
| `python3.12 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/codex_auto_update_plugins_skills.py --codex-home /Users/cY/.codex-switch/homes/internal --skip-external-updaters --json` | pass; plugin cache verify reports `pdf@openai-primary-runtime` matches source |
| `codex-switch --skip-self-update doctor` | pass |

## Remaining Risks

- `gsd-core` still has an external update available (`1.4.5` to `1.5.0`), but
  that update is outside this codex-switch repair and was intentionally not
  applied.
- DevFlow project-local skill layout remains `migration-pending` with a
  `skill_layout_conflict`; that migration is a separate project-setup cleanup.
- The OpenAI bundled `browser`, `chrome`, and `computer-use` plugin caches
  match source. The updater still reports them as `would-refresh` because its
  apply path would reinstall configured plugins, not because drift remains.
