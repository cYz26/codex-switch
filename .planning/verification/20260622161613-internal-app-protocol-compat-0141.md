# Verification: Internal App Protocol Compatibility 0.141 Dynamic Tools

Date: 2026-06-22
Change: `internal-app-protocol-compat`

## Root Cause

After the internal profile backend moved to `codex-cli 0.141.0`, the Desktop
client sent canonical `dynamicTools` containing both namespace and function
specs. The proxy still flattened namespace specs for the older `0.140` backend
shape, but left function specs canonical. That produced a mixed legacy/canonical
array and the backend rejected `thread/start` with:

```text
Invalid request: dynamic tools must use either canonical or legacy format consistently
```

Direct probes showed `0.141.0` accepts canonical `[namespace, function]`
dynamic tool arrays far enough to pass request deserialization, and rejects the
mixed proxy output with the same error shown by Desktop.

## Repair

- Added backend capability detection from `codex --version`.
- Preserved canonical dynamic tool specs for backend versions `>= 0.141.0`.
- Kept the legacy namespace flattening path for older internal backends.
- Passed the detected capability through the app proxy forwarding path.
- Added regression coverage for both the preserved canonical path and the
  existing older-backend flattening path.
- Confirmed the branch baseline has `VERSION=0.1.8`, matching the current
  release tag, so a source install of this working tree is not immediately
  overwritten by self-update before this fix is released.
- Reinstalled local source and regenerated
  `/Users/cY/.codex-switch/bin/codex-internal-app`.

## Local Runtime Checks

- `codex-switch status`
  - Active profile remained `openai-official`.
  - PATH codex: `/Users/cY/.local/bin/codex`
  - PATH codex version: `codex-cli 0.141.0`
  - Bundled app codex: `/Applications/Codex.app/Contents/Resources/codex`
  - Bundled app codex version: `codex-cli 0.142.0-alpha.6`
  - Running app-server stayed on the official bundle while this repair was made.
- `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch bash install.sh`
  - Installed `/Users/cY/.local/bin/codex-switch`.
  - Installed runtime `VERSION` is `0.1.8`.
  - Installed proxy contains `MIN_CANONICAL_DYNAMIC_TOOLS_VERSION`.
- Regenerated wrapper:
  - `CODEX_BIN=/Users/cY/.local/bin/codex`
  - `SWITCH_SCRIPTS=/Users/cY/.local/share/codex-switch/current/scripts`
  - `app-server` invokes `codex_switch_app_proxy.py`.
- `codex-switch status`
  - Reported `codex-switch self-update: already up to date 0.1.8`.
  - Installed proxy still contained the 0.141 capability detection afterward.
- Installed proxy probe:
  - `backend_supports_canonical_dynamic_tools('/Users/cY/.local/bin/codex')`
    returned `True`.
  - A canonical namespace tool remained `type=namespace` with no legacy
    top-level `namespace` field.
- Wrapper/proxy stdio probe:
  - Command path:
    `/Users/cY/.codex-switch/bin/codex-internal-app app-server --stdio`
  - Sent canonical `[namespace, function]` `dynamicTools`.
  - The previous invalid dynamicTools request error did not recur.
  - Backend emitted only remote-control/connection shutdown warnings after EOF.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_preserves_canonical_dynamic_tools_for_namespace_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_detects_namespace_dynamic_tool_support_from_backend_version -v
# Ran 3 tests: OK

PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests -v
# Ran 68 tests: OK

python3 -m py_compile scripts/*.py
# OK

bash -n scripts/codex-switch && \
  bash -n scripts/codex_env_setup && \
  bash -n install.sh && \
  bash -n run.sh && \
  python3 -m json.tool evals/evals.json >/dev/null
# OK

scripts/package-release.sh
# /Users/cY/dev/codex-switch/dist/codex-switch.tar.gz

openspec validate internal-app-protocol-compat --strict --no-interactive
# Change 'internal-app-protocol-compat' is valid

openspec validate --all --strict --no-interactive
# Totals: 9 passed, 0 failed (9 items)

git diff --check
# OK

PYTHONPATH=/Users/cY/.local/share/codex-switch/current/scripts \
  python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_preserves_canonical_dynamic_tools_for_namespace_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_detects_namespace_dynamic_tool_support_from_backend_version -v
# Ran 3 tests against installed runtime: OK
```

## Residual Risk

A full interactive Desktop switch to internal was not run in this session to
avoid changing the active official-mode Desktop session while the repair was in
progress. The installed runtime and generated internal wrapper are refreshed,
and the full wrapper/proxy app-server path no longer reproduces the reported
dynamicTools request-format error.

Archive gate remains closed.
