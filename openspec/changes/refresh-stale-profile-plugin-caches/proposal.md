## Why

Profile switching currently refreshes plugin catalogs and installs missing
enabled plugins, but it treats any non-empty same-version cache as current.
That leaves local marketplace source updates invisible until an operator
manually runs `codex plugin add`, even though the one-key switch already owns
the safe pre-restart maintenance window.

## What Changes

- Resolve plugin maintenance through the target profile's canonical runtime
  binding and set that profile's `CODEX_HOME` explicitly.
- Retain inspectable available-plugin metadata so local source path and version
  can be compared with the installed enabled-plugin cache.
- Refresh only enabled caches that are provably different from their matching
  local source; keep current caches as no-ops and preserve existing missing and
  unavailable-plugin behavior.
- Ignore known runtime residue when comparing trees and report uninspectable
  sources truthfully instead of reinstalling them blindly.
- Defer stale-cache replacement when the target profile app-server is already
  running, so an active Codex session is never hot-replaced underneath itself.
- Keep project-local DevFlow/OpenSpec refresh outside `codex-switch`; this
  change is global profile-cache maintenance only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: plugin repair and one-key switching gain deterministic stale
  local-plugin cache detection, canonical target-runtime execution, and an
  active-runtime safety gate.

## Impact

The primary implementation surface is `scripts/codex_switch_plugins.py`, with
CLI regressions in `scripts/test_codex_profile_switch.py` and bounded user
documentation updates. The change reuses the standard library and the existing
runtime-binding/process observation modules; it adds no dependency, performs
no project migration, and does not change plugin configuration ownership.
