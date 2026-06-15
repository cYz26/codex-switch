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

Complete this section when the design depends on current, external, platform, plugin, API, hook, CLI, installed-cache, or local-vs-platform capability.

- authoritative/current: source or command used, observed capability, version or date when available.
- local scan: files, config, cache paths, scripts, tests, or generated artifacts inspected.
- comparison: native option, local state, fallback option, recommendation, and tradeoffs.
- assumptions: what remains unverified and why it is acceptable or blocking.
- contract: scenarios and validation commands that prove the selected behavior.

## Approach

Add small modules instead of expanding the existing switch function into a
large mixed-responsibility file. Keep the shell wrapper as a coordinator and
delegate stateful logic to Python.

## Data Flow

Internal switch:
official home -> classify shared state -> backup mutation targets -> prepare
managed internal home -> write internal config layer -> update shim/Desktop ->
write active record -> finalize backup post-state.

Official switch:
internal home -> classify shared state -> backup official mutation targets ->
sync shared config/support into official home -> update shim/Desktop -> write
active record -> finalize backup post-state.

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
