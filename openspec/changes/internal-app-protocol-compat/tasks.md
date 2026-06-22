# Tasks: Internal Desktop App Protocol Compatibility

## Target State

Internal Desktop mode keeps using the configured internal binary and the app
wrapper always routes Desktop app-server launches through the proxy. The app
proxy normalizes known newer Desktop request shapes so older internal
app-server versions can start threads and list plugins.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Failing proxy compatibility tests

**Status:** done

**Goal**
- Lock the observed compatibility failures before production code changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add a failing test for flattening namespace dynamic tools into `0.140`
      compatible flat specs.
- [x] Add a failing test for filtering unsupported `plugin/list` marketplace
      kinds.
- [x] Verify both tests fail for the expected missing behavior.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind
```

### Slice 2: Request normalization implementation

**Status:** done

**Goal**
- Add the smallest proxy compatibility layer needed for the observed protocol
  gap.

**Files / Modules**
- `scripts/codex_switch_app_proxy.py`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add pure helpers that recursively normalize newer dynamic tool specs.
- [x] Preserve existing model alias replacement behavior.
- [x] Drop unsupported `created-by-me-remote` plugin marketplace kinds.
- [x] Run focused compatibility and existing proxy model alias tests.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_translates_desktop_model_alias_for_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup
```

### Slice 3: Wrapper app-server routing

**Status:** done

**Goal**
- Ensure real Desktop app-server launches enter the compatibility proxy even
  when Desktop passes flags other than `--stdio`.

**Files / Modules**
- `scripts/codex_switch_app_wrapper.py`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add a failing wrapper regression for app-server routing that is not
      pinned to `--stdio`.
- [x] Update generated wrapper logic to proxy every `app-server` invocation.
- [x] Preserve direct execution for non-app-server CLI commands.
- [x] Install the local source checkout and regenerate the internal app wrapper.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config -v
```

### Slice 4: Verification and state update

**Status:** done

**Goal**
- Prove the repair is complete without changing internal binary bindings.

**Files / Modules**
- `.planning/STATE.md`
- `.planning/verification/`
- `openspec/changes/internal-app-protocol-compat/tasks.md`

**Implementation**
- [x] Run full Python regression and syntax checks.
- [x] Run OpenSpec validation.
- [x] Record verification evidence.
- [x] Update workflow state and this ledger.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
python3 -m py_compile scripts/*.py
openspec validate internal-app-protocol-compat --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Failing proxy compatibility tests | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Request normalization implementation | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Wrapper app-server routing | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Verification and state update | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |

## Acceptance Criteria

- [x] Internal `codex_bin` remains configured as the specified internal binary.
- [x] Generated internal Desktop wrapper proxies all `app-server` invocations,
      not only `app-server --stdio`.
- [x] Namespace dynamic tool specs are forwarded as flat function specs, not as
      namespace specs.
- [x] `created-by-me-remote` is not forwarded to `0.140` plugin listing.
- [x] Existing proxy model alias behavior remains covered and passing.

## Final Verification

- [x] Focused regressions pass.
- [x] Full Python regression passes.
- [x] Compile, OpenSpec, and diff checks pass.
- [x] Verification evidence is recorded.
