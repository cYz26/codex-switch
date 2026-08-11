## Why

The installed DevFlow cache and official project-local skills are current, but
the repository still exposes the superseded GSD/Superpowers provider model,
legacy `.codex/skills` duplicates, and GSD hooks/runtime configuration. This
leaves the durable `AGENTS.md` contract in conflict with the latest DevFlow
ownership model and allows a nominally refreshed project to continue loading
retired providers.

## What Changes

- **BREAKING**: Make OpenSpec, DevFlow, and only the triggered members of the
  six-item bounded Matt allowlist the active project workflow providers;
  deactivate project-local GSD and Superpowers discovery/runtime surfaces.
- Merge the latest DevFlow `AGENTS.md` template into the tracked project rules
  while preserving the codex-switch-specific internal binary upgrade contract.
- Add the minimal `full-openspec` `.dev-flow.json` configuration.
- Move only ownership-verified legacy DevFlow, GSD, and Superpowers artifacts
  out of active discovery/runtime paths into a recoverable, receipt-bound
  quarantine; retain project planning history and the GSD migration journal.
- Refresh migration receipts and verify that no legacy duplicate or manual
  review item remains in the active skill layout.

## Capabilities

### New Capabilities

- `devflow-provider-ownership`: Defines the canonical workflow providers,
  active project skill layout, recoverable legacy-provider migration, and
  completion evidence for a refreshed brownfield DevFlow project.

### Modified Capabilities

None.

## Impact

- Affects `AGENTS.md`, `.dev-flow.json`, project-local ignored skill/provider
  configuration, and DevFlow migration/state/evidence artifacts.
- Does not change codex-switch product code, profile data, credentials, public
  APIs, persistence schemas, dependencies, the active parity implementation,
  Git history, release state, or running ChatGPT/profile processes.
- A new Codex task is required before relying on the refreshed skill inventory
  because the current task may retain its startup-time discovery results.
