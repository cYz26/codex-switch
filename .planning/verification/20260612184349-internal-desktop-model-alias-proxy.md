# Internal Desktop Model Alias Proxy Verification

Date: 2026-06-12

## Scope

Fix the Codex Desktop internal profile reasoning-effort dropdown showing `Max`
because the frontend treats the versioned Azure/AIDP deployment model
`gpt-5.5-2026-04-24` as a custom model and falls back to its static effort
list.

## Root Cause

The managed internal configs correctly stored
`model_reasoning_effort = "xhigh"` and the backend `model/list` response for
the deployment exposed only `low`, `medium`, `high`, and `xhigh`. The remaining
`Max` option came from the Desktop frontend fallback path when the saved model
could not be matched to the frontend-visible model list.

Changing the persisted model directly to `gpt-5.5` was rejected by the
Azure/AIDP backend with `invalid model or product name, product not right`, so
the durable fix must preserve the versioned deployment model for backend
requests.

## Implementation

- Added `scripts/codex_switch_app_proxy.py`.
- The managed internal Desktop wrapper now routes only
  `app-server --stdio` through the proxy.
- The proxy masks `model/list` and `config/read` responses from
  `gpt-5.5-2026-04-24` to Desktop-compatible `gpt-5.5`.
- The proxy translates Desktop alias selections or config writes back to
  `gpt-5.5-2026-04-24` before forwarding them to the backend.
- Non-app-server wrapper invocations continue to exec the real Codex binary.
- The local managed internal wrapper was regenerated with
  `scripts/codex-switch switch internal --skip-launchctl`.

## Commands And Results

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_versioned_model_alias_without_max_effort \
  CodexProfileSwitchTests.test_desktop_app_proxy_translates_desktop_model_alias_for_backend
```

Result: `Ran 3 tests in 0.995s`, `OK`.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 55 tests in 15.613s`, `OK`.

```bash
python3 -m py_compile scripts/*.py
```

Result: exit 0.

```bash
bash -n scripts/codex-switch scripts/codex_env_setup install.sh run.sh
```

Result: exit 0.

```bash
openspec validate --all --strict --no-interactive
```

Result: `4 passed, 0 failed`.

```bash
git diff --check
```

Result: exit 0.

```bash
scripts/codex-switch switch internal --skip-launchctl
```

Result: regenerated the local internal app wrapper at
`/Users/cY/.codex-switch/bin/codex-internal-app`.

```bash
/Users/cY/.codex-switch/bin/codex-internal-app app-server --stdio
```

Probed with `initialize`, `model/list`, and `config/read`.

Result:

```json
{
  "models": [
    {
      "id": "gpt-5.5",
      "model": "gpt-5.5",
      "efforts": ["low", "medium", "high", "xhigh"]
    }
  ],
  "config": {
    "model": "gpt-5.5",
    "effort": "xhigh"
  }
}
```

Config files still store the backend deployment model:

```text
/Users/cY/.codex-switch/homes/internal/config.toml: model = "gpt-5.5-2026-04-24"
/Users/cY/.codex-switch/profiles/internal/config.toml: model = "gpt-5.5-2026-04-24"
/Users/cY/.codex-switch/app-homes/internal/config.toml: model = "gpt-5.5-2026-04-24"
```

## Remaining Risk

The currently running Codex Desktop process may already have an app-server
connection open. Reopen Codex Desktop, or switch away and back after restart,
so the app uses the regenerated wrapper.
