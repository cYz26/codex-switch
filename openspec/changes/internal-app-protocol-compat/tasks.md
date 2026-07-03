# Tasks: Internal Desktop App Protocol Compatibility

## Target State

Internal Desktop mode keeps using the configured internal binary and the app
wrapper always routes Desktop app-server launches through the proxy. The app
proxy normalizes known newer Desktop request shapes so older internal
app-server versions can start threads and list plugins.

## Completion Contract

- [x] Target State is implemented for both `0.140` and `0.141+` internal
      backend compatibility, with an additional post-update app-server startup
      readiness slice verified.
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

### Slice 5: 0.141 canonical dynamic tool compatibility

**Status:** done

**Goal**
- Preserve canonical namespace dynamic tool requests for upgraded internal
  backends while keeping the older `0.140` flattening path.

**Capability Evidence**
- `codex-switch status` shows internal `codex_bin` is
  `/Users/cY/.local/bin/codex`.
- `/Users/cY/.local/bin/codex --version` returns `codex-cli 0.141.0`.
- Direct `app-server --stdio` probe against `0.141.0` accepts canonical
  `[namespace, function]` dynamic tools far enough to return `Not initialized`.
- The same probe rejects current proxy mixed output with
  `Invalid request: dynamic tools must use either canonical or legacy format
  consistently`.

**Files / Modules**
- `scripts/codex_switch_app_proxy.py`
- `scripts/test_codex_profile_switch.py`
- `.planning/verification/`
- `.planning/STATE.md`
- `openspec/changes/internal-app-protocol-compat/`

**Implementation**
- [x] Add a failing test that canonical namespace dynamic tool requests remain
      canonical when backend namespace dynamic tools are supported.
- [x] Add focused tests for backend version parsing.
- [x] Detect namespace dynamic tool support from the configured backend
      `codex --version` output.
- [x] Pass the detected capability through the app proxy forwarding path.
- [x] Keep existing `0.140` legacy flattening tests passing.
- [x] Refresh installed codex-switch runtime and generated internal wrapper.
- [x] Record verification evidence and update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_preserves_canonical_dynamic_tools_for_namespace_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_detects_namespace_dynamic_tool_support_from_backend_version -v
```

### Slice 6: Post-update app-server startup readiness

**Status:** done

**Goal**
- Prevent one-key internal switches from reporting success after an internal
  backend auto-update if the selected Desktop app-server exits during the
  startup/plugin-list window.

**Capability Evidence**
- Desktop logs from `2026-07-03T03:52:08Z` show the first internal Desktop
  app-server after switch reported `0.142.4`, initialized, routed
  `plugin/list`, then closed with exit code `241`.
- The same Desktop session restarted app-server, reported `0.142.5`, routed
  `plugin/list` again, logged the same featured plugin `401 Unauthorized`
  warning, and stayed connected until explicitly stopped.
- Direct `0.142.5` stdio probing shows `plugin/list` can return a JSON-RPC auth
  error when ChatGPT remote plugin catalog auth is unavailable; that response
  does not imply app-server startup failure.

**Files / Modules**
- `scripts/codex_switch_verify.py`
- `scripts/codex_profile_switch.py`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`
- `.planning/verification/`
- `.planning/STATE.md`
- `openspec/changes/internal-app-protocol-compat/`

**Implementation**
- [x] Add OpenSpec proposal/design/spec/task coverage for the startup smoke.
- [x] Add failing tests for successful app-server smoke with plugin-list auth
      error, non-zero `241` startup exit, and one-key internal auto-update
      smoke forwarding.
- [x] Add `--app-server-smoke` to standalone verification.
- [x] Implement bounded stdio app-server probe with initialize, initialized,
      `plugin/list`, and a short settle window.
- [x] Treat JSON-RPC plugin-list auth errors as responses, not failures.
- [x] Add one-key switch forwarding and automatic forwarding after internal
      auto-update.
- [x] Run focused tests until green.
- [x] Run broad verification, package/install the local bundle, record
      evidence, and update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_accepts_plugin_auth_error_response \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_reports_early_241_exit \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_runs_app_server_smoke
```

### Slice 7: Blocked internal release pin and shell CLI alignment

**Status:** done

**Goal**
- Keep internal switches on known-good `0.142.4` while latest remains known-bad
  `0.142.5`, then resume normal auto-update when a successor release appears.
- Make bare command-line `codex` drift visible when the current shell does not
  execute the codex-switch shim for the active profile.

**Capability Evidence**
- `SDGLBL/codex` releases show `internal-rust-v0.142.5` as latest and
  `internal-rust-v0.142.4` as the previous release.
- Local rollback/reinstall evidence shows internal `0.142.4` passes both
  `--app-server-smoke` and `--responses-tool-smoke`.
- Current shell evidence shows bare `codex` can still resolve to the internal
  plugin-appserver `0.142.5` path even after the profile manifest, shim, and
  Desktop wrapper are rebound to `/Users/cY/.local/bin/codex` at `0.142.4`.

**Files / Modules**
- `scripts/codex-switch`
- `scripts/codex_switch_bindings.py`
- `scripts/codex_switch_status_shell.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `.planning/verification/`
- `.planning/STATE.md`
- `openspec/changes/internal-app-protocol-compat/`

**Implementation**
- [x] Add failing tests for blocked latest skip, blocked current fallback
      install, successor latest auto-update, and shell PATH mismatch status.
- [x] Add wrapper policy for default blocked internal releases and fallback
      install version, with environment-variable overrides.
- [x] Update internal auto-update to pass `--version 0.142.4` only when latest
      is blocked and fallback install is required.
- [x] Update `status` and `shim-env` output for shell CLI alignment.
- [x] Refresh README troubleshooting guidance.
- [x] Run focused and broad validation.
- [x] Record verification evidence and update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_update_check_skips_blocked_latest_on_fallback \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_pins_blocked_current_to_fallback \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_resumes_for_successor_latest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_update_internal_command_pins_blocked_latest_without_explicit_version \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_status_reports_shell_codex_alignment
```

### Slice 8: Switch-time shell bootstrap alignment

**Status:** done

**Goal**
- Make profile switches automatically prepare future command-line shells to use
  the same codex-switch shim that Desktop/App switching already maintains.
- Keep current-shell drift visible because a child process cannot mutate an
  already-running parent shell's in-memory PATH.

**Capability Evidence**
- Current shell evidence shows bare `codex` can resolve to a stale internal
  plugin-appserver binary even when the active profile shim is correct.
- `codex-switch shim-env` already emits the correct PATH update and shell hash
  reset. The missing behavior is persistent, switch-time shell startup
  installation.

**Files / Modules**
- `scripts/codex_switch_shell.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_plan.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `.planning/verification/`
- `.planning/STATE.md`
- `openspec/changes/internal-app-protocol-compat/`

**Implementation**
- [x] Add failing tests for switch-time shell bootstrap installation,
      idempotent replacement, and explicit opt-out.
- [x] Add shell bootstrap helper with marker-managed block replacement and
      configurable target path for tests/advanced users.
- [x] Call the helper from profile switch flows whenever the command-line shim
      is updated.
- [x] Include the shell profile path in switch dry-run/backup plans when it will
      be mutated.
- [x] Refresh README guidance from manual eval-only to automatic future-shell
      alignment plus current-shell remediation.
- [x] Run focused and broad validation.
- [x] Record verification evidence and update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_installs_shell_bootstrap_for_cli_alignment \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_replaces_existing_shell_bootstrap_without_duplication \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_can_skip_shell_bootstrap
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Failing proxy compatibility tests | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Request normalization implementation | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Wrapper app-server routing | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| Verification and state update | done | `.planning/verification/20260622112616-internal-app-protocol-compat.md` |
| 0.141 canonical dynamic tool compatibility | done | `.planning/verification/20260622161613-internal-app-protocol-compat-0141.md` |
| Post-update app-server startup readiness | done | `.planning/verification/20260703060556-internal-app-protocol-compat-startup-smoke.md` |
| Blocked internal release pin and shell CLI alignment | done | `.planning/verification/20260703212846-internal-01425-block-pin.md` |
| Switch-time shell bootstrap alignment | done | `.planning/verification/20260703213928-switch-shell-bootstrap-alignment.md` |

## Acceptance Criteria

- [x] Internal `codex_bin` remains configured as the specified internal binary.
- [x] Generated internal Desktop wrapper proxies all `app-server` invocations,
      not only `app-server --stdio`.
- [x] Namespace dynamic tool specs are preserved for `0.141+` backends.
- [x] Namespace dynamic tool specs are forwarded as flat function specs for
      `0.140` backends, not as namespace specs.
- [x] `created-by-me-remote` is not forwarded to `0.140` plugin listing.
- [x] Existing proxy model alias behavior remains covered and passing.
- [x] `verify --app-server-smoke` fails on app-server exit code `241`.
- [x] `verify --app-server-smoke` passes when `plugin/list` returns a JSON-RPC
      auth error and the app-server stays healthy.
- [x] One-key internal switch verification automatically runs app-server smoke
      after an internal backend auto-update.
- [x] Known-bad latest `0.142.5` is skipped or replaced with pinned fallback
      `0.142.4` during internal switch/update checks.
- [x] A later internal latest release resumes unpinned auto-update.
- [x] `codex-switch status` reports whether bare `codex` resolves to the
      active profile shim and prints the PATH remediation when it does not.
- [x] Profile switches automatically install or refresh an idempotent managed
      shell bootstrap for future command-line shells.

## Final Verification

- [x] Focused regressions pass for the new `0.141` compatibility case.
- [x] Full Python regression passes.
- [x] Compile, OpenSpec, and diff checks pass.
- [x] Verification evidence is recorded.
- [x] Slice 6 focused regressions pass.
- [x] Broad tests, compile checks, OpenSpec validation, package/install, and
      workstation verification evidence are refreshed for Slice 6.
- [x] Slice 7 focused regressions pass.
- [x] Broad tests, compile checks, OpenSpec validation, package/install, and
      workstation verification evidence are refreshed for Slice 7.
- [x] Slice 8 focused regressions pass.
- [x] Broad tests, compile checks, OpenSpec validation, package/install, and
      workstation verification evidence are refreshed for Slice 8.
