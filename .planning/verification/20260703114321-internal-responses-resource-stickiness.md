# Internal Responses Resource Stickiness Verification

Date: 2026-07-03

## Scope

Change `internal-responses-resource-stickiness` adds an explicit
`--responses-tool-smoke` verification path for internal Azure Responses
tool-call follow-up failures. It also records troubleshooting guidance for the
cross-Azure-resource routing scenario.

The repair is local diagnostic hardening. It does not claim to fix AIDP
resource routing; the upstream service contract remains that all requests
sharing a Responses context must be routed to the same Azure OpenAI resource,
or a supported sticky routing key must be provided.

## Red / Green Evidence

Focused RED command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
```

Result before implementation: failed because `--responses-tool-smoke` was not
recognized and no report was written.

Focused GREEN command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
```

Result after implementation: passed, 4 tests.

Packaging RED/GREEN:

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_package_release_includes_troubleshooting_docs
```

Result before package script change: failed because the release package did not
include `docs/`. Result after implementation: passed, 1 test.

## Final Verification

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
```

Result: passed, 102 tests.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch scripts/package-release.sh install.sh run.sh
```

Result: passed.

```bash
openspec validate --all --strict --no-interactive
```

Result: passed, 11 items.

```bash
git diff --check
```

Result: passed.

```bash
scripts/package-release.sh
```

Result: generated `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz`.

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch/dist/codex-switch ./install.sh
```

Result: installed `/Users/cY/.local/bin/codex-switch` pointing to
`/Users/cY/.local/share/codex-switch/current/scripts/codex-switch`.

Installed help checks:

```bash
codex-switch --skip-self-update verify --help | rg -- '--responses-tool-smoke|Responses API tool-call'
codex-switch --skip-self-update internal --help | rg -- '--responses-tool-smoke|Responses tool'
```

Result: both commands found the new `--responses-tool-smoke` flag.

## Files Changed

- `scripts/codex_switch_verify.py`: deterministic Responses tool smoke,
  resource mismatch parsing, structured sanitized diagnostics, JSON report
  fields.
- `scripts/codex_profile_switch.py`: `verify --responses-tool-smoke` parser.
- `scripts/codex-switch`: one-key forwarding and help text.
- `scripts/test_codex_profile_switch.py`: verifier, report, one-key, and
  release-package regressions.
- `scripts/package-release.sh`: include `docs/` in release bundles.
- `docs/troubleshooting/internal-azure-responses-resource-stickiness.md`:
  scenario documentation and upstream ownership boundary.
- `README.md`: internal upgrade checkpoint command and troubleshooting link.
- `openspec/changes/internal-responses-resource-stickiness/`: proposal,
  design, tasks, and spec delta.

## Remaining Risk

If live internal Azure Responses still fails, that is expected until AIDP or
the internal backend makes Responses contexts sticky to a single Azure OpenAI
resource. The new local command is:

```bash
codex-switch --skip-self-update verify internal --responses-tool-smoke --report
```

Archive remains unavailable because the archive gate is closed. No archive
action was taken.
