# Schema-Scoped App Proxy Final Verification Checkpoint

Date: 2026-07-24

## Outcome

`schema-scoped-app-proxy` is complete at 32/32 tasks. Schema-scoped protocol
transforms, digest-bound config-write receipts, semantic offline TOML recovery,
canonical launcher home preparation, real-chain lifecycle behavior, and dead
helper cleanup have passed final verification.

## Current-Version Compatibility

Completion-time isolated research covered:

- internal backend `codex-cli 0.144.6`;
- ChatGPT bundled official CLI `codex-cli 0.146.0-alpha.3`.

Both generated `PluginListMarketplaceKind`, retained
`created-by-me-remote`, and returned canonical versioned config-write
responses. The adapter now recognizes historical `PluginMarketplaceKind` and
current `PluginListMarketplaceKind`. The behavioral probe uses a network-free
local marketplace fixture because current binaries reject historical
`source_type = "github"`.

Exact backend, schema, receipt, source, and test SHA-256 values are recorded in
`.planning/devflow/verification/schema-scoped-app-proxy.md`.

## Final Validation

- Protocol: 35/35 on Python 3.9.6 and 35/35 on Python 3.12.
- Config Document: 24/24 on Python 3.12.
- Runtime binding: 55/55 on Python 3.12.
- Transaction: 211/211 on Python 3.12.
- Full profile: 139/139 on Python 3.12.
- Generated-wrapper E2E: 7/7.
- Strict OpenSpec: 16/16 repository items.
- Python static: AST 47/47 and production imports 42/42 on both runtimes.
- Bash syntax, removed-helper caller scan, and tracked/untracked whitespace
  checks passed.

## Safety Boundary

No live profile switch, App restart, install/update, plugin mutation, release,
commit, push, or rollout edit was performed. Source completion does not update
the installed launcher or running App; any rebind/restart remains a separate
explicitly authorized action.

## Next Action

Apply `fail-safe-update-release` from its approved OpenSpec task list, then run
the overall integration and final verification ledger items. Keep the separate
official-latest advisory behavior at `INC-006 BLOCKED_AWAITING_HUMAN` until its
stable-only versus stable-plus-prerelease output contract is approved.
