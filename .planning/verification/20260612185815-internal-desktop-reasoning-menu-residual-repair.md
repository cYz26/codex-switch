# Verification: internal Desktop reasoning menu residual repair

Date: 2026-06-12

## Scope

Repair the remaining Codex Desktop reasoning-effort menu path where `Max`
still appeared for the internal profile after the first model alias proxy
change.

## Root Cause

The first proxy fix masked `model/list` and `config/read`, but Codex Desktop
also uses thread and conversation model fields when building the composer
reasoning-effort menu. When those fields still contained the versioned backend
deployment model `gpt-5.5-2026-04-24`, the frontend could not find that model
in the alias-masked `model/list` response and fell back to its static effort
set, which includes `max`.

## Implementation

- Added a regression test for backend thread/conversation payloads containing
  `model`, `latestModel`, `previousTurnModel`, and model write records.
- Updated `codex_switch_app_proxy.py` so backend-to-Desktop messages map all
  Desktop-visible model fields from `gpt-5.5-2026-04-24` to `gpt-5.5`, not only
  `model/list` and `config/read`.
- Kept Desktop-to-backend translation symmetric, so alias selections still
  route back to the versioned deployment model.
- Updated the OpenSpec scenario and task ledger to cover this thread payload
  path.

## Commands And Results

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup
```

Result before implementation: failed with `conversation["model"]` still equal
to `gpt-5.5-2026-04-24`.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_versioned_model_alias_without_max_effort \
  CodexProfileSwitchTests.test_desktop_app_proxy_translates_desktop_model_alias_for_backend
```

Result: `Ran 3 tests`, `OK`.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_falls_back_when_runtime_reasoning_effort_is_unsupported \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup \
  CodexProfileSwitchTests.test_desktop_app_proxy_masks_versioned_model_alias_without_max_effort \
  CodexProfileSwitchTests.test_desktop_app_proxy_translates_desktop_model_alias_for_backend
```

Result: `Ran 5 tests`, `OK`.

```bash
python3 -m py_compile scripts/codex_switch_app_proxy.py scripts/test_codex_profile_switch.py
```

Result: exit 0.

```bash
openspec validate independent-profile-homes --strict --no-interactive
```

Result: `Change 'independent-profile-homes' is valid`.

```bash
git diff --check -- \
  scripts/codex_switch_app_proxy.py \
  scripts/test_codex_profile_switch.py \
  openspec/changes/independent-profile-homes/specs/codex-switch/spec.md \
  openspec/changes/independent-profile-homes/tasks.md \
  .planning/STATE.md
```

Result: exit 0.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 56 tests in 14.691s`, `OK`.

```bash
python3 -m py_compile scripts/*.py
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

## Runtime Notes

`launchctl getenv CODEX_CLI_PATH` currently points to
`/Users/cY/.codex-switch/bin/codex-internal-app`, and that wrapper loads
`/Users/cY/dev/codex-switch/scripts/codex_switch_app_proxy.py`. Existing
Desktop app-server processes may already have the old proxy code loaded, so the
visible UI requires a fresh Codex Desktop app-server connection after this
repair.

## Remaining Risk

This verification covers the proxy behavior and OpenSpec contract. It does not
restart the currently running Codex Desktop process from inside this session,
because doing so could interrupt the active Codex conversation.
