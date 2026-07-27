## Why

Supported profile switches and restores can currently mix official/internal homes, produce backups that restore nothing, overwrite changed directory contents, or leave a half-applied state after a late failure. A live official switch also proved that known profile-local runtime directories can be misclassified as shared support: backing up `ipc/ipc.sock` failed on the Unix socket before the switch could commit. A later live official switch proved that a byte-identical Desktop global-state merge was still journaled as a filesystem effect and frozen as a later mutation dependency; a concurrent ChatGPT write then caused both the switch and rollback to fail even though codex-switch had no global-state bytes to write. The first compatibility recovery attempt then proved that the same legacy journal also claimed ownership of other byte-identical shared-support effects: a later App-owned write under `visualizations` made recovery fail even though that effect had no planned state change. These are reachable data-safety failures, so profile mutation needs one transactional contract before further feature work.

## What Changes

- Keep `snapshot` and `shared` configuration strategies inside the selected profile's independent home; neither strategy may collapse `internal` into the official live home.
- Replace the legacy `files` backup path with one versioned backup manifest and a single mutation plan used by dry-run, apply, rollback, and restore.
- Preflight every restore entry, payload, recursive directory state, symlink target, and mode before the first mutation; reject conflicting current state unless `--force` is explicit.
- Stage and validate captures before atomically replacing the managed profile files; absent source auth explicitly clears stale destination auth when missing auth is allowed.
- Serialize store mutations with a store-scoped interprocess lock and roll back all profile/home/shim/Desktop-binding changes when a switch cannot commit.
- Publish crash-durable, marker-bound switch/restore journals; classify every unresolved or terminal transaction before any switch, capture, restore, init-capture, or preserved custom-route write.
- Freeze every planning input at the read that produces the plan, install the exact staged artifacts recorded by the journal, and bind filesystem actions and recovery to attested directory and object identities.
- Journal and durably recover target writes, Desktop effects, active state, and parent-directory cleanup before publishing one authoritative terminal manifest.
- Keep `init --capture-current` inside the same lock and recovery gate as capture without nested locking, and surface any retained-marker guidance through the successful CLI path.
- Validate every recorded state field, mode, directory entry count, payload, allowlist root, and terminal reread before mutation or marker retirement.
- Treat `ipc` and `mcp-oauth-locks` as profile-local runtime state that is never shared, backed up, or copied across profile homes, while continuing to reject unknown special filesystem objects.
- Exclude a byte-identical Desktop global-state merge from the mutation journal,
  backup set, rollback set, and retained frozen inputs so a concurrent App-owned
  write is preserved; keep a real merge identity-bound and fail closed. For the
  exact marker-bound pre-fix incident only, recover by releasing ownership of
  every journaled filesystem effect whose before, planned, and observed states
  strictly prove a byte-identical no-op, while retaining fail-closed recovery
  for every real planned change.
- Keep the current product profile set (`openai-official`/`official` and `internal`) unchanged. Arbitrary-profile naming and store-containment expansion are not part of this change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: profile switching, capture, backup, restore, failure rollback, and concurrent mutation requirements become transactional and independently homed.

## Impact

Primary impact is in `codex_switch_transaction.py`, `codex_switch_switching.py`, `codex_switch_lifecycle.py`, `codex_switch_home_sync.py`, backup/restore/capture/plan/launch/store helpers, and isolated regression tests. Backup manifests gain an explicit schema version plus additive marker/journal bindings; compatible legacy manifests are classified or rejected with recovery guidance rather than falsely reported as restored. No production dependency, live profile switch, or workstation migration is required for implementation verification.
