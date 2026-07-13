# Verification

## Commands

- `plugin_project_migration --apply --write-report; activate_project_dependencies --skip-official-installs; check_dependencies; validate_workflow_state`
- `python3 scripts/test_codex_profile_switch.py; bash -n scripts/codex-switch; bash -n scripts/codex_env_setup; bash -n install.sh; git diff --check`

## Evidence

- `plugin_project_migration --apply --write-report; activate_project_dependencies --skip-official-installs; check_dependencies; validate_workflow_state`: pass (.planning/verification/20260605134234-plugin_project_migration---apply---write-report-activate_project.md)

- `python3 scripts/test_codex_profile_switch.py; bash -n scripts/codex-switch; bash -n scripts/codex_env_setup; bash -n install.sh; git diff --check`: pass (.planning/verification/20260605134234-python3-scripts-test_codex_profile_switch.py-bash--n-scripts-cod.md)

- `validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json; python3 scripts/test_codex_profile_switch.py; bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && git diff --check`: pass (.planning/verification/20260605134441-validate_workflow_state.py---repo-users-cy-dev-codex-switch---js.md)

- `python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state; python3 scripts/test_codex_profile_switch.py; python3 -m py_compile scripts/*.py; bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && git diff --check`: pass (.planning/verification/20260608112025-isolate-desktop-session-state-verification.md)

- `dev-flow-refresh scoped validation: project skill refresh; AGENTS durable guidance merge; validate/doctor/migration/scaffold dry-run`: pass (.planning/verification/20260708074052-dev-flow-refresh-scoped-validation-project-skill-refresh-agents-.md)

- `DevFlow release/cache refresh; project skill refresh; AGENTS durable guidance merge; validate/doctor/migration/scaffold dry-run; git diff --check`: scoped pass with provider migration deferred (.planning/verification/20260713123254-dev-flow-refresh-final-verification.md)
