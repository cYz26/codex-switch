# Verification: Internal App Protocol Compatibility Startup Smoke

## Context

After `codex-switch internal` updated the internal profile backend, Codex
Desktop first connected to an app-server that reported `0.142.4`, initialized,
routed `plugin/list`, then closed stdio with exit code `241`. Desktop retried
and the next app-server reported `0.142.5`, routed the same `plugin/list`
window, logged the same featured plugin `401 Unauthorized` warning, and stayed
connected. The local repair adds an app-server startup smoke so internal mode is
not reported healthy after backend update if that startup window exits.

## Red Tests

Command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_accepts_plugin_auth_error_response \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_reports_early_241_exit \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_runs_app_server_smoke
```

Result before implementation:

- Failed because `verify --app-server-smoke` was not registered.
- Failed because one-key internal auto-update verification did not include
  app-server startup smoke.

## Green and Regression Validation

Focused app-server startup smoke tests:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_accepts_plugin_auth_error_response \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_reports_early_241_exit \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_runs_app_server_smoke
```

Result: passed, 3 tests.

Neighbor verifier smoke tests:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_runtime_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
```

Result: passed, 5 tests.

Full Python regression:

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
```

Result: passed, 104 tests.

Syntax checks:

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: passed.

OpenSpec validation:

```bash
openspec validate internal-app-protocol-compat --strict --no-interactive
openspec validate --all --strict --no-interactive
```

Result: `internal-app-protocol-compat` passed; all 11 OpenSpec items passed.

Diff check:

```bash
git diff --check
```

Result: passed.

## Runtime Evidence

Direct internal app-server smoke against the real internal profile backend:

```bash
PYTHONPATH=scripts python3 - <<'PY'
from pathlib import Path
from codex_switch_verify import run_app_server_smoke
codex = '/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex'
home = Path('/Users/cY/.codex-switch/homes/internal')
code, output = run_app_server_smoke(codex, home)
print(f'code={code}')
print(output)
raise SystemExit(code)
PY
```

Result:

```text
code=0
app-server smoke passed
```

Installed bundle refresh:

```bash
scripts/package-release.sh
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
/Users/cY/.local/bin/codex-switch --skip-self-update internal --help | rg -- '--app-server-smoke|--responses-tool-smoke|--runtime-smoke'
```

Result:

- `dist/codex-switch.tar.gz` generated.
- Installed `/Users/cY/.local/bin/codex-switch` points at
  `/Users/cY/.local/share/codex-switch/current/scripts/codex-switch`.
- Installed one-key internal help lists `--app-server-smoke`,
  `--runtime-smoke`, and `--responses-tool-smoke`.

## Workflow Gate Notes

`scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json`
was requested by the change-plan gate but is unavailable in this checkout:

```text
zsh:1: no such file or directory: scripts/validate_workflow_state.py
```

Archive remains closed by DevFlow. No archive command was run.
