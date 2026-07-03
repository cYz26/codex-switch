# Design: Internal Desktop App Protocol Compatibility

## Skill Routing Ledger

- Request kind: bug repair for Codex Desktop/internal profile compatibility.
- Workflow mode: brownfield, OpenSpec-required compatibility and error-handling
  change.
- `capability-research`: used. Current local CLI help/schema generation,
  Desktop logs, `codex-switch status`, and direct `app-server --stdio` probes
  define the compatibility contract.
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
| Version-gate namespace dynamic tool conversion | `0.140` needs legacy flat specs, while `0.141+` accepts canonical namespace specs and rejects mixed canonical/legacy arrays. | Always flatten; rejected because it breaks `0.141`. Never flatten; rejected because it breaks `0.140`. |
| Filter unsupported plugin marketplace kinds | `0.140` rejects unknown enum values during request parsing. | Map to another kind; would misrepresent the user's requested collection. |
| Block only the known-bad internal release | The verified regression is tied to `0.142.5`; pinning every future release would prevent recovery when a later internal release skips the bad version. | Disable all internal auto-update; rejected because it would leave users stuck after a fixed successor appears. |
| Align shell `codex` through the switch shim | Matching only version strings is insufficient because a different binary may use the wrong `CODEX_HOME` or bypass wrapper behavior. | Compare versions only; rejected because it misses stale plugin-appserver paths. |
| Use a managed shell bootstrap instead of overwriting PATH binaries | Shell startup PATH ordering is the durable boundary for command-line `codex`; replacing whatever binary appears first on PATH could corrupt plugin caches or user-managed installs. | Rewrite the first `codex` found on PATH; rejected because stale paths may be real binaries, not shims. |

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
- Local current version evidence: `codex-switch status` and direct version
  checks show the internal `codex_bin` is `/Users/cY/.local/bin/codex` at
  `0.141.0`, while the Desktop bundle remains `0.142.0-alpha.6`.
- Local direct probe evidence for `0.141.0`: a canonical `thread/start`
  dynamicTools array containing one namespace spec and one function spec passes
  dynamicTools parsing and reaches the later `Not initialized` gate; the proxy's
  current mixed legacy/canonical output fails immediately with `Invalid request:
  dynamic tools must use either canonical or legacy format consistently`.
- Current profile evidence: `codex-switch status` shows active profile
  `openai-official`; the internal profile manifest keeps `codex_bin` bound to
  `/Users/cY/.local/bin/codex`.
- Real Desktop internal-run evidence: Desktop spawned
  `/Users/cY/.codex-switch/bin/codex-internal-app` and the current Desktop
  app-server launch pattern includes `app-server --analytics-default-enabled`,
  so a wrapper condition limited to `app-server --stdio` does not cover the
  observed path.
- July 2026 startup evidence: after `codex-switch internal` upgraded the
  internal app-server backend to `0.142.5`, the first Desktop restart connected
  to a `0.142.4` app-server process. It initialized and routed `plugin/list`,
  then closed stdio with exit code `241`. Desktop spawned another process,
  which reported `0.142.5`, routed the same `plugin/list` flow, logged the same
  featured plugin `401 Unauthorized` warning, and remained connected. This
  separates the local readiness bug from the unauthenticated featured plugin
  warning.
- Direct app-server probe evidence: a current `0.142.5` internal app-server
  accepts `initialize` over stdio and responds to a Desktop-like `plugin/list`
  with a JSON-RPC auth error when remote plugin catalog auth is unavailable;
  that response is not a startup crash and must not fail readiness by itself.
- July 2026 rollback evidence: after reinstalling and rebinding the internal
  profile to `0.142.4`, both `--app-server-smoke` and
  `--responses-tool-smoke` passed. The `SDGLBL/codex` release page still marks
  `internal-rust-v0.142.5` as latest and lists `internal-rust-v0.142.4` as the
  previous release.
- Shell evidence: the active internal manifest, generated Desktop wrapper, and
  codex-switch shim delegate to `/Users/cY/.local/bin/codex` at `0.142.4`, but
  the current terminal can still resolve bare `codex` first from the internal
  plugin-appserver path at `0.142.5` due to PATH ordering.
- Shell mutation boundary: a child `codex-switch` process cannot directly
  mutate the parent shell's in-memory PATH, so automatic alignment must be
  persisted through shell startup configuration and verified for the current
  shell.

## Completion Contract

- [ ] No internal profile binding is changed to the Desktop App bundle.
- [ ] The generated wrapper sends any `app-server` invocation through the
      proxy while leaving non-app-server CLI commands direct.
- [ ] `0.141+` internal backends receive canonical dynamic tool specs unchanged.
- [ ] Older internal backends receive namespace dynamic tool specs converted to
      flat function specs with `namespace`, `type`, `name`, `description`,
      `inputSchema`, and optional `deferLoading`.
- [ ] Existing flat function dynamic tool specs remain valid for older
      backends.
- [ ] `plugin/list.params.marketplaceKinds` drops unsupported newer values.
- [ ] Existing model alias masking tests still pass.
- [ ] A new app-server startup smoke initializes the selected internal backend
      and sends a Desktop-like `plugin/list` request.
- [ ] The smoke passes when `plugin/list` returns a JSON-RPC auth error and
      the app-server remains healthy.
- [ ] The smoke fails if the app-server exits non-zero, including exit code
      `241`, during the startup settle window.
- [ ] One-key internal switches automatically include app-server startup smoke
      in verification after an internal backend auto-update.
- [ ] One-key internal switches do not auto-upgrade a healthy `0.142.4`
      fallback to blocked latest `0.142.5`.
- [ ] One-key internal switches pin installer invocations to `0.142.4` if the
      current internal profile binary is on blocked `0.142.5` and no later
      latest release exists.
- [ ] One-key internal switches resume unpinned latest updates once latest is a
      successor to `0.142.5`.
- [ ] `codex-switch status` exposes shell PATH drift when bare `codex` does not
      resolve to the codex-switch shim.
- [ ] Profile switches install or refresh an idempotent managed shell startup
      block that prepends the codex-switch shim directory and clears command
      lookup cache for future shells.
- [ ] Existing shell profile content outside the managed block is preserved.
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

### Slice 5: 0.141 canonical dynamic tool compatibility

Add a focused failing test for the upgraded internal backend path, detect
backend namespace dynamic tool support from the configured `codex --version`,
preserve canonical dynamic tool specs for `0.141+`, and keep `0.140` legacy
flattening behavior covered.

### Slice 6: Post-update app-server startup readiness

Add verifier support for a Desktop-like app-server startup smoke. The smoke
uses the target profile `CODEX_HOME`, starts the configured `codex_bin
app-server --analytics-default-enabled`, sends `initialize`, `initialized`, and
`plugin/list`, then waits briefly for the process to stay healthy. JSON-RPC
responses containing expected auth errors are accepted; process crashes and
non-zero exits are reported as verification problems. One-key internal switch
forwards the smoke automatically when the internal update check actually ran an
auto-update, and users can request it explicitly with `--app-server-smoke`.

### Slice 7: Blocked internal release pin and shell CLI alignment

Add focused tests for known-bad latest handling and shell PATH drift. The
wrapper treats `0.142.5` as a blocked latest release by default, with
environment-variable overrides for the blocked list and fallback version. If
latest is blocked and the current internal CLI is already the fallback, the
switch skips auto-update and explains why. If the current CLI is blocked, the
switch runs `update-internal --version 0.142.4`. If latest advances to a
successor release, the switch returns to the ordinary latest update path.

`codex-switch status` compares bare `codex` resolution against the
codex-switch shim and prints the `eval "$(codex-switch shim-env)"` remediation
when the current shell would execute a different binary. `shim-env` also clears
the shell command hash table after prepending the shim directory.

### Slice 8: Switch-time shell bootstrap alignment

Add focused tests for shell startup bootstrap installation during profile
switches. When a switch updates the codex-switch command-line shim, it also
ensures a marker-managed block exists in the user's shell startup file. The
block prepends the active store `bin` directory to PATH and clears shell command
lookup cache. Existing user content is preserved, repeated switches replace the
managed block rather than duplicating it, and `CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP`
skips the mutation for controlled environments.

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
- [ ] The proxy no longer converts `0.141+` canonical namespace dynamic tool
      requests into mixed legacy/canonical arrays.
- [ ] The proxy no longer forwards `created-by-me-remote` to a `0.140`
      `plugin/list` backend.
- [ ] Existing proxy model alias behavior remains unchanged.
- [ ] App-server startup readiness is verified after one-key internal backend
      auto-updates.
- [ ] `plugin/list` auth errors are treated as responses, not as app-server
      crashes.
- [ ] A known-bad `0.142.5` latest release is skipped or replaced with pinned
      `0.142.4` during internal switch/update checks.
- [ ] A later internal latest release resumes unpinned auto-update.
- [ ] The status command reports whether bare `codex` executes the active
      profile shim and prints the shell command that fixes PATH ordering.
- [ ] Profile switches automatically install or refresh the managed shell
      bootstrap that makes new command-line shells use the active profile shim.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_preserves_canonical_dynamic_tools_for_namespace_backend \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_accepts_plugin_auth_error_response \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_app_server_smoke_reports_early_241_exit \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_runs_app_server_smoke
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
- [ ] Startup readiness failures include enough stderr/stdout context to
      distinguish app-server crash from expected plugin auth errors.
