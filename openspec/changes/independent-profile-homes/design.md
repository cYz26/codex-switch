# Design: Independent official and internal Codex homes with backup gate

## Target State

`official` and `internal` no longer share a mutable activation home. Official
mode uses the official home directly, defaulting to `~/.codex`. Internal mode
uses a managed home, defaulting to `~/.codex-switch/homes/internal`, and the
shell shim/Desktop wrapper point Codex at that home. Shared non-auth config and
stable support assets can move between homes; auth and runtime state cannot.

Every non-dry-run switch builds a mutation plan, captures a restorable backup
for every target path in that plan, and only then applies mutations. Restore is
an explicit command with dry-run/apply modes.

## Scope / Non-Goals

- In scope: official/internal switching, backup manifest capture, restore,
  dry-run plan output, status/doctor fields, README, and regression tests.
- Non-goals: backup retention, external dependencies, changing the internal
  installer/update source, or archiving unrelated OpenSpec changes.

## Architecture Decisions

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| Official home is the source of truth for official mode | Matches upstream Codex behavior and keeps official auth/runtime state out of the profile store activation path. | Continue rewriting the live home for both profiles |
| Internal uses a managed home under the store | Keeps internal auth/config/runtime isolated and easy to back up. | Keep using the old app-home only for Desktop |
| Sync only classified shared state | Prevents auth/session/model leakage while preserving plugin and preference continuity. | Full home copy; config-only sync |
| Merge Desktop global settings as a sanitized subset | Keeps Electron/UI settings continuous across independent homes without copying prompt history, thread permissions, credentials, queued follow-ups, or remote routing state. | Share `.codex-global-state.json` wholesale; keep all Desktop settings isolated |
| Treat `pets/` as Settings support, not runtime state | The Desktop Settings sidebar exposes Pets as user-facing configuration; syncing the small support directory keeps the panel continuous while still excluding plugin caches, credentials, and session data. | Keep `pets/` profile-local; copy all Desktop home state |
| Backup gate wraps all switch mutations | Ensures no planned write happens unless original state has been captured. | Best-effort backups after mutation |
| Restore uses post-switch state checks | Allows normal restore after a completed switch while refusing unrelated user edits unless `--force` is used. | Always overwrite; always require force |

## Completion Contract

- [ ] Target State is implemented.
- [ ] Required behavior is covered by tests or documented manual checks.
- [ ] No required capability remains outside the active change.
- [ ] Verification evidence is recorded before archive.

## Capability Slices

### Slice 1: Shared-state planner

Classify official/internal home entries, produce backup/mutation plans, and
merge shared config through existing TOML helpers.

### Slice 2: Backup and restore

Capture path metadata and contents before mutation, finalize post-switch state,
and restore from `backup.json` with dry-run/apply/force behavior.

### Slice 3: Independent activation

Route internal activation through the managed home and official activation
through the official home while preserving one-key command compatibility.

### Slice 4: Diagnostics and docs

Expose effective home, backup id, sync source/target, shell CLI, Desktop CLI,
and restore guidance in status/doctor/README.

## Execution Ledger

Track slice status in `tasks.md`, `.planning/STATE.md`, or a repo-specific ledger file. Mark a slice done only after its validation command passes or a blocker is recorded.

## Capability Evidence

- authoritative/current: `/Applications/Codex.app/Contents/Resources/codex
  --version` reports `codex-cli 0.142.3`; `/Users/cY/.local/bin/codex
  --version` reports `codex-cli 0.142.2`; both app-server binaries expose
  `config/value/write`, `config/batchWrite`, and `config/read` in generated
  TypeScript protocol bindings.
- local scan: inspected the active LaunchAgent and running Desktop process,
  the managed internal wrapper, `codex_switch_app_proxy.py`,
  `codex_switch_config.py`, current and backed-up
  `~/.codex-switch/homes/internal/config.toml`, and the active plugin cache.
  The latest switch backup retained Desktop preferences and enabled
  `agent-kb`/`lark-feishu-ops`, while the current runtime config retained only
  a narrow `[desktop]` table after Desktop started.
- comparison: switch-time config merging already preserves shared settings,
  but runtime Desktop config writes can rewrite the managed internal runtime
  config after the switch. The durable repair belongs in the internal
  app-server proxy so future Desktop config writes preserve existing unrelated
  shared settings while keeping the newly written value.
- assumptions: the active running app-server must be restarted by Codex
  Desktop to load a regenerated proxy; the file-level repair still restores
  config immediately.
- contract: regression tests cover `config/value/write` and
  `config/batchWrite` preservation, plus workstation restoration is validated
  by `codex-switch status`, `doctor`, and targeted config checks.

## Approach

Add small modules instead of expanding the existing switch function into a
large mixed-responsibility file. Keep the shell wrapper as a coordinator and
delegate stateful logic to Python.

## Data Flow

Internal switch:
official home -> classify shared state -> backup mutation targets -> prepare
managed internal home -> merge sanitized Desktop global settings -> write
internal config layer -> update shim/Desktop -> write active record -> finalize
backup post-state.

Official switch:
internal home -> classify shared state -> backup official mutation targets ->
sync shared config/support into official home -> merge sanitized Desktop global
settings -> update shim/Desktop -> write active record -> finalize backup
post-state.

Internal Desktop runtime config write:
Desktop JSON-RPC request -> `codex_switch_app_proxy.py` snapshots the current
managed internal `config.toml` for `config/value/write` and
`config/batchWrite` -> backend applies the requested write -> proxy restores
missing unrelated shared settings from the snapshot without overwriting the new
Desktop value -> response is forwarded to Desktop.

Internal Desktop wrapper startup:
wrapper removes stale links for non-shareable state -> links stable support
entries only -> merges sanitized Desktop global settings from the live official
home into the managed internal home -> folds shared TOML config overlay back
through the existing Python helper -> launches the internal backend.

## Compatibility

`--live-codex-home` remains accepted as a legacy alias for the official home.
Existing profile manifests remain valid. Legacy internal app homes can remain in
place; the new managed home becomes the activation target.

## Testing

Add or update tests before implementation for behavior changes. Record verification evidence before archive.

## Acceptance Criteria

- [ ] The Target State is satisfied.
- [ ] The Completion Contract is fully checked.
- [ ] Required validation commands pass or have recorded blockers.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

## Final Verification

- [ ] Focused tests pass.
- [ ] Broader tests, lint, typecheck, or build pass where applicable.
- [ ] Verification evidence is recorded.
