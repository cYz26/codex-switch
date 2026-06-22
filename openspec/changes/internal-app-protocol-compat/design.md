# Design: Internal Desktop App Protocol Compatibility

## Skill Routing Ledger

- Request kind: bug repair for Codex Desktop/internal profile compatibility.
- Workflow mode: brownfield, OpenSpec-required compatibility and error-handling
  change.
- `capability-research`: skipped as a separate workflow; local generated
  app-server schemas and Desktop logs provide the required capability evidence.
- `superpowers:systematic-debugging`: used to establish root cause before
  fixing.
- `superpowers:writing-plans`: used for implementation planning discipline;
  canonical plan content is recorded in this OpenSpec change.
- `superpowers:test-driven-development`: required for implementation.
- OpenSpec routing: new change `internal-app-protocol-compat`.
- GSD routing: not required; this is a narrow repair, not phase planning.

## Target State

Internal mode keeps using the configured internal `codex_bin` through the
generated Desktop app wrapper. The wrapper launches `codex_switch_app_proxy.py`
for every `app-server` invocation, and the proxy normalizes known newer Desktop
app-server request shapes into forms accepted by the older internal app-server
before forwarding.

## Scope / Non-Goals

- In scope: app-server routing in `scripts/codex_switch_app_wrapper.py`,
  request normalization inside `scripts/codex_switch_app_proxy.py`, regression
  tests in `scripts/test_codex_profile_switch.py`, verification evidence, and
  workflow state.
- Non-goals: replacing the internal binary, pointing internal at the Desktop App
  bundle, changing official behavior, changing LaunchAgent binding semantics,
  or adding protocol negotiation infrastructure.

## Architecture Decisions

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| Normalize in the existing app proxy | The proxy is already the boundary between newer Desktop and profile-specific backend binaries. | Change profile bin binding; rejected because internal must use the specified bin. |
| Keep conversions narrow and request-side only | The observed failures happen before backend work starts, and current response masking already works for model aliases. | Broad generic protocol shim; too risky for a local repair. |
| Proxy all wrapper `app-server` invocations | Desktop can launch app-server with flags other than `--stdio`; the proxy is still the compatibility boundary for those launches. | Proxy only `app-server --stdio`; rejected because it bypasses the shim for `--analytics-default-enabled`. |
| Flatten namespace dynamic tools | `0.140` supports flat specs with optional `namespace`; this preserves namespace identity without requiring newer schema support. | Drop namespace tools; would make task creation work but silently remove tool access. |
| Filter unsupported plugin marketplace kinds | `0.140` rejects unknown enum values during request parsing. | Map to another kind; would misrepresent the user's requested collection. |

## Capability Evidence

- Local Desktop log evidence: `thread/start` failed with
  `Invalid request: missing field inputSchema`; `plugin/list` failed with
  `unknown variant created-by-me-remote`.
- Local schema evidence:
  `/Applications/Codex.app/Contents/Resources/codex app-server generate-json-schema`
  for `0.142.0-alpha.6` includes namespace `DynamicToolSpec` and
  `created-by-me-remote`.
- Local schema evidence:
  `/Users/cY/.local/bin/codex app-server generate-json-schema` for `0.140.0`
  only accepts flat dynamic tool specs requiring `inputSchema` and does not
  accept `created-by-me-remote`.
- Current profile evidence: `codex-switch status` shows active profile
  `openai-official`; the internal profile manifest keeps `codex_bin` bound to
  `/Users/cY/.local/bin/codex`.
- Real Desktop internal-run evidence: Desktop spawned
  `/Users/cY/.codex-switch/bin/codex-internal-app` and the current Desktop
  app-server launch pattern includes `app-server --analytics-default-enabled`,
  so a wrapper condition limited to `app-server --stdio` does not cover the
  observed path.

## Completion Contract

- [ ] No internal profile binding is changed to the Desktop App bundle.
- [ ] The generated wrapper sends any `app-server` invocation through the
      proxy while leaving non-app-server CLI commands direct.
- [ ] Namespace dynamic tool specs are converted to flat function specs with
      `namespace`, `type`, `name`, `description`, `inputSchema`, and optional
      `deferLoading`.
- [ ] Existing flat function dynamic tool specs remain valid for `0.140`.
- [ ] `plugin/list.params.marketplaceKinds` drops unsupported newer values.
- [ ] Existing model alias masking tests still pass.
- [ ] Verification evidence records focused and broad commands.

## Capability Slices

### Slice 1: Failing proxy compatibility tests

Add focused tests for the exact incoming request shapes:

- `thread/start` with a namespace dynamic tool spec nested inside request params.
- `plugin/list` with `created-by-me-remote` mixed with older supported
  marketplace kinds.

### Slice 2: Request normalization implementation

Implement pure helper functions in `codex_switch_app_proxy.py` and call them
from `translate_desktop_message_for_backend` after model alias replacement.

### Slice 3: Wrapper app-server routing

Update the generated Desktop wrapper so every `app-server` invocation goes
through `codex_switch_app_proxy.py`, regardless of which app-server flags
Desktop passes.

### Slice 4: Verification and state

Run focused tests, full Python regression, compile checks, OpenSpec validation,
diff checks, then record verification and update `.planning/STATE.md`.

## Execution Ledger

Track status in `tasks.md`. Mark a slice done only after its validation command
passes or a blocker is recorded.

## Acceptance Criteria

- [ ] Switching to internal after this change does not require using the Desktop
      App bundle as the backend binary.
- [ ] Desktop app-server launches with non-`--stdio` flags still enter the app
      proxy.
- [ ] The proxy no longer forwards namespace dynamic tool specs in a shape that
      causes `missing field inputSchema` on `0.140`.
- [ ] The proxy no longer forwards `created-by-me-remote` to a `0.140`
      `plugin/list` backend.
- [ ] Existing proxy model alias behavior remains unchanged.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
python3 -m py_compile scripts/*.py
openspec validate internal-app-protocol-compat --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
```

## Risks / Rollback

- If a future Desktop request introduces a different incompatible shape, this
  narrow compatibility shim may need another conversion. Roll back by removing
  the proxy helper changes and tests; profile bindings remain untouched.

## Goal Mode Prompt

Repair internal Desktop app-server protocol compatibility while keeping internal
bound to its configured binary. Done means focused and broad verification pass,
OpenSpec evidence is recorded, workflow state is updated, and no archive is
attempted.

## Continue Prompt

Resume `internal-app-protocol-compat`: inspect `tasks.md`, run the next
unchecked validation command, and keep internal `codex_bin` distinct from the
Desktop App bundle.

## Review Checklist

- [ ] Root cause is tied to local logs and generated schemas.
- [ ] Tests fail before production code and pass after.
- [ ] Proxy conversions are request-side only and narrowly scoped.
- [ ] No unrelated files or profile bindings are modified.
- [ ] Verification evidence and state are updated before completion.
