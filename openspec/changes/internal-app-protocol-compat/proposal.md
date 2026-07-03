# Internal Desktop App Protocol Compatibility

## Why

Codex Desktop/App bundle `0.142.0-alpha.6` can send app-server requests that
older internal profile Codex binaries do not understand consistently.
When `codex-switch` is in internal mode, the Desktop wrapper must keep using
the configured internal binary instead of switching to the Desktop App bundle,
but the current app proxy only translates model aliases.

The observed failures are:

- `thread/start`: `Invalid request: missing field inputSchema`
- `plugin/list`: `Invalid request: unknown variant created-by-me-remote`
- After the first proxy normalization repair, a real Desktop internal run still
  failed because Desktop launched `app-server --analytics-default-enabled` while
  the generated wrapper only proxied `app-server --stdio`.
- After the internal configured binary was upgraded to `0.141.0`, Desktop
  internal mode failed with `Invalid request: dynamic tools must use either
  canonical or legacy format consistently`. The proxy was still flattening
  namespace dynamic tools for `0.140` compatibility, which converted a canonical
  `[namespace, function]` request into a mixed legacy/canonical array.
- After the internal configured binary was upgraded again to `0.142.5`, the
  first Desktop restart briefly launched an older `0.142.4` app-server process.
  That process initialized successfully, responded to `plugin/list`, then
  closed stdio with exit code `241` while the latest stderr line was a featured
  plugin `401 Unauthorized` warning. Desktop retried and the next `0.142.5`
  app-server stayed connected even though the same featured plugin request still
  produced a warning, so the local switch gap is startup readiness after an
  internal backend update rather than the featured plugin `401` itself.

Generated app-server schemas show the compatibility gap:

- `0.142` accepts namespace dynamic tool specs while `0.140` only accepts flat
  function dynamic tool specs with top-level `inputSchema`.
- `0.141` accepts canonical namespace dynamic tool specs but rejects mixed
  canonical and legacy dynamic tool arrays.
- `0.142` accepts the `created-by-me-remote` plugin marketplace kind while
  `0.140` does not.

## What Changes

- Keep internal mode bound to its configured Codex binary.
- Route every generated-wrapper `app-server` invocation through the app proxy,
  regardless of additional Desktop app-server flags.
- Extend the internal Desktop app proxy to normalize known newer Desktop
  request shapes before forwarding them to the older internal app-server.
- Detect whether the configured backend supports canonical namespace dynamic
  tools.
- Preserve canonical dynamic tool arrays for `0.141+` backends.
- Convert namespace dynamic tool specs into flat function tool specs compatible
  with `0.140` backends.
- Remove unsupported `plugin/list.marketplaceKinds` values before forwarding to
  the older backend.
- Add an explicit Desktop app-server startup smoke and run it automatically
  after one-key internal switches that performed an internal backend update.
  The smoke verifies that the selected internal backend can initialize and
  survive a Desktop-like `plugin/list` request before the switch is reported as
  healthy.
- Treat internal release `0.142.5` as a blocked release because local rollback
  evidence shows `0.142.4` passes the internal app-server and Responses
  tool-follow-up smokes while `0.142.5` can hit the Azure Responses
  resource-stickiness failure. While `0.142.5` remains latest, one-key internal
  switches pin fallback installs to `0.142.4`; once a later latest release is
  published, normal latest-version auto-upgrade resumes.
- Report when the current shell's bare `codex` command does not resolve through
  the codex-switch shim, and provide the `shim-env` command needed to align CLI
  execution with the active profile.
- During each profile switch that updates the command-line shim, install or
  refresh a managed shell startup bootstrap so newly opened shells place the
  codex-switch shim directory before stale profile/plugin binaries on PATH.
- Add focused regression tests for both compatibility conversions.

## Target State

Users can keep Codex Desktop in official mode while repairing the internal
profile. After switching back to internal, Desktop still launches the internal
configured binary through the generated proxy wrapper, and known `0.142`
Desktop requests no longer fail before the internal backend can create a task
or list plugins.

## Scope

In scope:

- Internal Desktop app proxy request normalization.
- Regression tests for `thread/start` namespace dynamic tool compatibility.
- Regression tests for unsupported `plugin/list` marketplace kind filtering.
- Regression tests for Desktop wrapper app-server flag routing.
- Verification tests for app-server startup smoke success, exit-code `241`
  failure, and automatic post-update forwarding.
- Internal update policy for the known-bad `0.142.5` release and fallback
  pinning to `0.142.4`.
- Shell CLI alignment status for the active profile shim.
- Managed shell startup bootstrap for command-line `codex` alignment.
- OpenSpec tasks, verification evidence, and workflow state.

Out of scope:

- Binding internal mode to the Desktop App bundle.
- Updating or replacing the internal Codex binary.
- Changing official profile behavior.
- Supporting every possible future app-server protocol difference.
- Archiving this or any other change.

## Completion Contract

- [ ] Internal profile manifests still point at the configured internal binary.
- [ ] The generated internal Desktop wrapper proxies `app-server` invocations
      regardless of whether Desktop passes `--stdio` or another app-server
      flag.
- [ ] The app proxy preserves canonical namespace dynamic tool specs for
      `0.141+` internal backends.
- [ ] The app proxy converts namespace dynamic tool specs into `0.140`
      compatible flat specs only for backends that need legacy dynamic tools.
- [ ] The app proxy filters unsupported `created-by-me-remote` plugin list
      marketplace kinds.
- [ ] Internal backend updates trigger app-server startup smoke during one-key
      internal switch verification.
- [ ] The app-server startup smoke treats JSON-RPC auth errors from
      `plugin/list` as non-fatal responses but fails if the app-server exits
      non-zero during the startup window.
- [ ] A latest internal release of `0.142.5` does not auto-upgrade the internal
      profile away from a healthy `0.142.4` fallback.
- [ ] If the internal profile is currently on blocked `0.142.5` while `0.142.5`
      is still latest, one-key internal switch invokes the installer with
      `--version 0.142.4`.
- [ ] When latest advances past `0.142.5`, one-key internal switch resumes the
      ordinary latest auto-update path without the fallback pin.
- [ ] `codex-switch status` reports whether bare `codex` resolves to the
      codex-switch shim and prints the `shim-env` remediation when it does not.
- [ ] Each profile switch that updates the command-line shim also installs or
      refreshes an idempotent managed shell startup block pointing PATH at the
      current store `bin` directory.
- [ ] The shell bootstrap preserves unrelated shell profile content and can be
      skipped by explicit environment opt-out.
- [ ] Focused regression tests fail before implementation and pass after.
- [ ] Full Python regression tests, compile checks, OpenSpec validation, and
      diff checks pass or blockers are recorded.
