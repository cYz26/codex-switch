## Why

The internal Desktop proxy currently rewrites matching field names recursively
and modifies `config.toml` locally after AppServer reports a successful write.
It can miss the real `keyPath` schema, mutate unrelated payload data, remove
capabilities the backend now supports, revive stale array-table entries, and
invalidate AppServer's returned config version. The generated App launcher also
uses a weaker duplicate home-sync policy.

## What Changes

- Replace recursive field-name rewriting with adapters selected by RPC method,
  direction, exact schema path, and independent backend capability.
- Normalize Desktop-supplied `thread/resume.params.history` to the same
  identifier-free ResponseItem form produced by disk resume, preventing local
  UUID item identifiers from being replayed as server-owned Responses IDs.
- Translate model aliases for the real `config/value/write` and
  `config/batchWrite.edits[*]` shapes while preserving unknown payloads.
- Preserve canonical `dynamicTools` and marketplace kinds whenever the
  generated backend schema advertises them; retain legacy conversion only
  behind evidence-backed capability checks.
- Remove proxy-side post-response config rewrites. Probe the backend's
  versioned atomic config-write behavior in an isolated home; pass through
  proven safe writes and fail closed before forwarding unproven writes.
- Introduce a semantic Config Document for offline generation/merge paths, with
  complete value spans and stable array-table identity so changed or disabled
  entities are not revived.
- Treat `[plugins.*]` and `[[skills.config]]` as authoritative usage state from
  the currently running profile. Profile switches and internal Desktop restart
  copy that state exactly, including removals and `enabled = false`; stale
  runtime or snapshot fallbacks may recover marketplace and hook support but
  may not revive deleted plugin or skill entries.
- Fail closed when a real TOML parser is unavailable, without adding a
  production dependency.
- Make the generated launcher call canonical Python home sync and verify the
  real launcher-to-proxy-to-fake-backend stdio path.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: app-server transforms, config-write safety, TOML editing,
  launcher home synchronization, and proxy integration verification change.

## Impact

Primary impact is in app proxy/config/TOML/launcher/home-sync modules and
isolated tests. Generated schemas from official `0.145.0-alpha.27` and internal
`0.142.4` both expose `dynamicTools`, `keyPath`,
`ConfigBatchWriteParams.edits`, required `ConfigWriteResponse` fields, and
`created-by-me-remote`. An isolated temporary-home probe also proves internal
`0.142.4` preserves unrelated MCP, marketplace, plugin, and skill config while
returning a versioned response. Modern internal traffic must therefore not be
downgraded or locally rewritten. No live workstation traffic or production
dependency is required.

A completion-time compatibility recheck against installed internal `0.144.6`
and bundled official `0.146.0-alpha.3` found two schema-adjacent naming/config
drifts without a capability loss: the marketplace enum is now named
`PluginListMarketplaceKind`, and marketplace config accepts `git` or `local`
rather than the historical `github` source type. The adapter will recognize
both enum names, and the isolated behavioral probe will use a cross-version
local marketplace fixture so current safe config writes remain provable.
