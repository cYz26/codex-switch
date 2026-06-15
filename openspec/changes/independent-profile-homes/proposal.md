# Independent official and internal Codex homes with backup gate

## Why

The current switching model rewrites the live Codex home as the activation
surface for both official and internal profiles. That makes official mode less
faithful to upstream Codex behavior and increases the blast radius of internal
switching. The redesigned model keeps official on the official home and moves
internal execution into a managed independent home. Because switching still
touches user workstation state, every mutation must be protected by a
restorable backup gate.

## What Changes

- Add `--official-codex-home <path>` and keep `--live-codex-home` as a legacy
  alias.
- Activate `official` through the official home and official CLI/Desktop paths.
- Activate `internal` through `~/.codex-switch/homes/internal` by default.
- Sync only shareable config/support state between homes.
- Exclude auth, runtime state, sessions, history, logs, sqlite files, temp
  files, browser/process state, and profile-specific model/provider layers from
  cross-home sharing.
- Create a backup manifest before every non-dry-run mutation.
- Add `restore <backup-id> --dry-run|--apply [--force]`.

## Target State

`codex-switch official` preserves official Codex semantics by using the
official Codex home directly. `codex-switch internal` prepares and activates an
independent managed home. Switching between them moves only shareable
configuration/support state and never moves auth or runtime/session state. All
real switches are guarded by backups that can be inspected or restored.

## Scope

- Project mode: brownfield
- Change type: behavior-change

## Capability Evidence

- authoritative/current: local CLI help and existing project specs define the
  current supported command surface; no external API capability is required.
- local scan: inspected `scripts/codex_profile_switch.py`,
  `scripts/codex-switch`, `scripts/codex_switch_switching.py`,
  `scripts/codex_switch_config.py`, `scripts/codex_switch_app_wrapper.py`,
  `scripts/codex_switch_backup.py`, status/doctor modules, README, and the
  existing regression suite.
- comparison: native Codex has a single official home; this change keeps that
  path intact for official mode and uses a managed fallback home only for
  internal mode.

## Non-Goals

- Do not add production dependencies.
- Do not archive the unrelated `remote-release-packaging` change.
- Do not add backup retention or automatic cleanup policy.
- Do not copy full runtime/session history between homes.

## Completion Contract

- [ ] OpenSpec scenarios cover independent homes, backup gate, and restore.
- [ ] Regression tests cover dry-run plans, backup failure, sync exclusions, and restore.
- [ ] Implementation preserves existing one-key commands and release packaging.
- [ ] Verification evidence is recorded before archive.

## Risks

- Switching touches user workstation state; backup failure must abort before
  mutation.
- Config merging must avoid leaking internal model/provider settings into the
  official home.
- Desktop activation depends on macOS LaunchAgent behavior and is covered by
  isolated tests with fake binaries rather than a live app process.
