# Isolate Desktop Session State

## Why

The internal Codex Desktop wrapper currently symlinks nearly every non-auth file
from the live `CODEX_HOME` into the profile app home. That includes sessions,
session indexes, history, sqlite state, logs, temporary files, and process
manager state. Reusing those runtime files across profile/model boundaries can
resume Responses API history with tool-call items but without the matching
reasoning item required by the provider, producing intermittent unrecoverable
turn failures.

## What Changes

- Keep shared workstation assets available in the profile app home.
- Stop sharing conversation/request runtime state across the internal Desktop
  app home and live `CODEX_HOME`.
- Remove existing live-state symlinks from the internal app home on wrapper
  launch so already-installed wrappers recover after refresh.
- Document the new compatibility boundary and focused regression coverage.

## Target State

When `codex-switch internal` refreshes `~/.codex-switch/bin/codex-internal-app`,
the wrapper rebuilds internal Desktop config from shared config plus
`internal.config.toml`, shares only stable support assets, and keeps response
history/runtime state profile-local. Existing stale symlinks for excluded state
paths are removed before Codex starts.

## Scope

- Change type: bug-fix, compatibility repair.
- In scope: internal profile Desktop wrapper app-home symlink policy.
- Out of scope: changing Codex CLI/Desktop request construction or editing
  existing transcript contents.

## Capability Evidence

- authoritative/current: OpenAI Responses API reasoning documentation search on
  2026-06-05 showed that reasoning items from previous responses must be carried
  forward either through `previous_response_id` or by passing output items.
- local scan: `scripts/codex_switch_app_wrapper.py` symlinks all live
  `CODEX_HOME` entries except config/auth/profile config; local
  `~/.codex-switch/app-homes/internal` currently has symlinks for `sessions`,
  `session_index.jsonl`, `history.jsonl`, `state_*.sqlite`, `log`, `tmp`, and
  related runtime state.
- comparison: A minimal transcript scrubber would edit user history and still
  depend on Codex internals. The durable repair is to keep profile runtime state
  isolated while preserving stable shared assets and config overlay behavior.

## Non-Goals

- Do not delete live `~/.codex` session data.
- Do not isolate plugin, skill, model catalog, cache, or config-support assets
  unless they are runtime transcript/state files.
- Do not add dependencies.

## Completion Contract

- [x] Regression test proves stale live runtime symlinks are removed.
- [x] Regression test proves future wrapper launches do not recreate excluded
      runtime symlinks.
- [x] Existing app-home config overlay behavior still passes.
- [x] Verification evidence and workflow state are updated.

## Risks

- Internal Desktop will no longer show live/shared conversation history after the
  wrapper is refreshed and the app is restarted. This is intentional because the
  shared history is the compatibility risk.
