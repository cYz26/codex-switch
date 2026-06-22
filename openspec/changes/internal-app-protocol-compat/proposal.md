# Internal Desktop App Protocol Compatibility

## Why

Codex Desktop/App bundle `0.142.0-alpha.6` can send app-server requests that
the internal profile's specified Codex binary `0.140.0` does not understand.
When `codex-switch` is in internal mode, the Desktop wrapper must keep using
the configured internal binary instead of switching to the Desktop App bundle,
but the current app proxy only translates model aliases.

The observed failures are:

- `thread/start`: `Invalid request: missing field inputSchema`
- `plugin/list`: `Invalid request: unknown variant created-by-me-remote`
- After the first proxy normalization repair, a real Desktop internal run still
  failed because Desktop launched `app-server --analytics-default-enabled` while
  the generated wrapper only proxied `app-server --stdio`.

Generated app-server schemas show the compatibility gap:

- `0.142` accepts namespace dynamic tool specs while `0.140` only accepts flat
  function dynamic tool specs with top-level `inputSchema`.
- `0.142` accepts the `created-by-me-remote` plugin marketplace kind while
  `0.140` does not.

## What Changes

- Keep internal mode bound to its configured Codex binary.
- Route every generated-wrapper `app-server` invocation through the app proxy,
  regardless of additional Desktop app-server flags.
- Extend the internal Desktop app proxy to normalize known newer Desktop
  request shapes before forwarding them to the older internal app-server.
- Convert namespace dynamic tool specs into flat function tool specs compatible
  with `0.140`.
- Remove unsupported `plugin/list.marketplaceKinds` values before forwarding to
  the older backend.
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
- [ ] The app proxy converts namespace dynamic tool specs into `0.140`
      compatible flat specs.
- [ ] The app proxy filters unsupported `created-by-me-remote` plugin list
      marketplace kinds.
- [ ] Focused regression tests fail before implementation and pass after.
- [ ] Full Python regression tests, compile checks, OpenSpec validation, and
      diff checks pass or blockers are recorded.
