# Verification: internal-app-protocol-compat

Date: 2026-06-22 11:26 Asia/Shanghai

## Scope

Repair internal Desktop app-server protocol compatibility without rebinding the
internal profile to the Codex Desktop App bundle.

## Root Cause Evidence

- Codex Desktop/App bundle: `0.142.0-alpha.6`.
- Internal configured binary: `/Users/cY/.local/bin/codex`, version `0.140.0`.
- Desktop logs showed `thread/start` failing with
  `Invalid request: missing field inputSchema`.
- Desktop logs showed `plugin/list` failing with
  `unknown variant created-by-me-remote`.
- Generated schema diff showed `0.142` adds namespace dynamic tool specs and
  `created-by-me-remote`; `0.140` only accepts flat dynamic tool specs with
  top-level `inputSchema` and does not accept `created-by-me-remote`.
- After the first proxy normalization repair, a real internal Desktop run still
  failed. Local Desktop logs showed Desktop spawned
  `/Users/cY/.codex-switch/bin/codex-internal-app` and reported backend version
  `0.140.0`, while the generated wrapper only proxied `app-server --stdio`.
  The current Desktop app-server launch pattern uses
  `app-server --analytics-default-enabled`, so the request-normalizing proxy was
  bypassed for the real launch path.

## Red-Green Evidence

Red command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind -v
```

Result before implementation: failed with two assertion failures. The proxy did
not flatten namespace dynamic tools and did not filter
`created-by-me-remote`.

Focused green command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_translates_desktop_model_alias_for_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup -v
```

Result after implementation: passed, 4 tests.

Wrapper routing red command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config -v
```

Result before wrapper implementation: failed because the generated wrapper
contained `if [ "${1:-}" = "app-server" ] && [ "${2:-}" = "--stdio" ]; then`
instead of routing all `app-server` invocations through the proxy.

Wrapper routing green command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config -v
```

Result after wrapper implementation: passed, 1 test.

Focused combined green command:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind -v
```

Result after wrapper implementation: passed, 3 tests.

## Final Verification

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests -v
```

Result: passed, 65 tests.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
openspec validate internal-app-protocol-compat --strict --no-interactive
```

Result: passed.

```bash
openspec validate --all --strict --no-interactive
```

Result: passed, 8 items.

```bash
git diff --check
```

Result: passed.

```bash
codex-switch status
```

Result: active profile remains `openai-official`; PATH codex remains
`/Users/cY/.local/bin/codex` at `0.140.0`; Desktop/App bundle remains
`/Applications/Codex.app/Contents/Resources/codex` at `0.142.0-alpha.6`.

## Installed Runtime Verification

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch bash install.sh
```

Result: installed the current source checkout to
`/Users/cY/.local/share/codex-switch/current` and preserved the PATH symlink
`/Users/cY/.local/bin/codex-switch`.

```bash
PYTHONPATH=/Users/cY/.local/share/codex-switch/current/scripts python3 - <<'PY'
from pathlib import Path
from codex_switch_app_wrapper import maybe_refresh_profile_app_wrapper
from codex_switch_store import Store

store = Store(
    Path('/Users/cY/.codex-switch'),
    Path('/Users/cY/.codex'),
    Path('/Users/cY/Library/LaunchAgents/com.openai.codex-cli-path.plist'),
    'com.openai.codex-cli-path',
)
manifest = store.load_manifest('internal')
print(maybe_refresh_profile_app_wrapper(
    store=store,
    name='internal',
    manifest=manifest,
    app_cli_path=str(manifest.get('app_cli_path') or ''),
    switch_scripts=Path('/Users/cY/.local/share/codex-switch/current/scripts'),
))
PY
```

Result: rewrote `/Users/cY/.codex-switch/bin/codex-internal-app`.

```bash
sed -n '1,28p' /Users/cY/.codex-switch/profiles/internal/manifest.json
rg -n '^CODEX_BIN=|^SWITCH_SCRIPTS=|codex_switch_app_proxy.py' \
  /Users/cY/.codex-switch/bin/codex-internal-app
```

Result: internal manifest keeps `codex_bin` as `/Users/cY/.local/bin/codex`;
the generated wrapper has `CODEX_BIN=/Users/cY/.local/bin/codex` and
`SWITCH_SCRIPTS=/Users/cY/.local/share/codex-switch/current/scripts`.
The generated wrapper now routes `if [ "${1:-}" = "app-server" ]; then` through
`codex_switch_app_proxy.py`; it no longer requires `--stdio`.

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind -v
```

Result from `/Users/cY/.local/share/codex-switch/current`: passed, 3 tests.

```bash
PYTHONPATH=scripts python3 -m py_compile scripts/*.py
```

Result from `/Users/cY/.local/share/codex-switch/current`: passed.

## Residual Risk

This is a narrow compatibility shim for the observed `0.142` Desktop to `0.140`
backend protocol gap. Future Desktop protocol additions may require additional
request normalization. Archive was not attempted because the archive gate is
closed.
