## Context

The switch implementation currently has two mutation paths. Independent/shared mode creates an `entries` backup, while snapshot/custom paths mutate the live home and create a legacy `files` backup that the restore command does not consume. Capture writes managed files in place before validating the whole source, restore validates each entry only as it reaches it, directory states are not recursive, and Desktop binding occurs after other mutations without a common rollback owner. There is also no store-wide serialization. A July 25 official-switch incident exposed an additional ownership defect: the installed release treated the internal home's `ipc` directory as shared support, created an incomplete `29-ipc` backup entry, and failed while copying the live `ipc.sock` Unix socket before binding or active-state commit.

The approved product boundary is two profiles only: `openai-official` (the public `official` alias) and `internal`. This change does not generalize the profile namespace. It makes every supported mutation of those profiles transactional.

## Skill Routing Ledger

- request kind: bug repair, persistence/error-handling/compatibility change
- workflow mode: Full OpenSpec
- capability-research: used; current store, switch paths, backup manifests, and runtime ownership were inspected without mutation
- decision-resolution: used; user fixed the profile set and approved the systemic route
- decision-grilling: skipped; no open product decision remains
- implementation-planning: used through DevFlow/OpenSpec and AI-native plan structure
- architecture-guidance: used; the selected deep module concentrates planning, mutation, rollback, and evidence behind one interface
- domain-language-modeling: skipped; existing profile/switch vocabulary is sufficient
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Build and validate the complete mutation plan before any destination changes.
- Keep shared and snapshot config strategies inside the target profile home.
- Use one versioned backup representation for switch and restore.
- Detect post-switch changes recursively before non-force restore.
- Replace capture's complete managed-file set atomically.
- Roll back all mutations, including Desktop binding, after a failed apply.
- Serialize profile-store mutations from the initial read through backup finalization.
- Keep known runtime-owned IPC and OAuth lock state local to the profile that created it.

**Non-Goals:**

- Supporting additional or arbitrary profile names.
- Cleaning legacy `.codex/skills`, migrating DevFlow root state, or changing providers.
- Running a real workstation switch as part of implementation.
- Automatically restoring legacy `files` manifests whose intended destination state cannot be attested.

## Capability Evidence

- `authoritative_current`: the repository's existing OpenSpec contracts require a backup before mutations and a restore conflict gate.
- `local_scan`: `switch_profile()` dispatches snapshot mode outside the independent path; `backup_live_files()` writes `files`; `restore_backup()` consumes `entries`; `states_match()` compares directory kind only; launch binding is a late mutation; `shared_support_entries()` includes any top-level entry not listed as profile, runtime, or non-shareable state.
- `incident_evidence`: installed `codex-switch 0.1.13` failed the `internal -> openai-official` backup with `Operation not supported on socket`; the incomplete backup retained an empty `29-ipc` directory and no terminal `backup.json`, while official CLI app-server smoke passed independently.
- `comparison`: isolated line fixes leave multiple planning/backup/apply owners. One transaction module gives callers a single seam and makes dry-run and apply consume the same immutable plan.
- `assumptions`: legacy `files` manifests are not safely self-describing enough for automatic conversion; explicit rejection is safer than false success.
- `contract`: delta scenarios cover snapshot isolation, preflight, rollback, legacy rejection, capture replacement, and lock contention.

## Decisions

### Decision 1: Introduce a deep Profile Transaction module

Create `codex_switch_transaction.py` with this external interface:

```python
@dataclass(frozen=True)
class TransactionRequest:
    operation: str
    profile: str
    options: Mapping[str, object]

@dataclass(frozen=True)
class TransactionReceipt:
    operation: str
    outcome: str
    preview_lines: tuple[str, ...]
    backup_id: str | None

def execute_transaction(
    store: Store,
    request: TransactionRequest,
    *,
    dry_run: bool = False,
) -> TransactionReceipt: ...
```

`execute_transaction` acquires the store lock before the first canonical read. Its implementation then builds an immutable internal plan, performs path/state/payload preflight, and either returns a read-only preview or stages payloads, persists the pending backup, applies, rolls back, and finalizes. The internal plan is never exposed across the lock seam, so callers cannot commit stale observations. Dry-run performs no store, backup, or destination write; callers may render `preview_lines` but do not reproduce plan logic.

Alternative A was to patch snapshot, restore, capture, and launch independently. It was rejected because it retains four mutation owners and cannot prove whole-operation rollback. Alternative B was a full CLI rewrite. It was rejected because the existing brownfield helpers and successful shared-mode behavior can be adapted behind the new seam.

### Decision 2: Use a versioned backup manifest with recursive path attestations

New manifests use `schema_version: 2`, an explicit lifecycle state (`prepared`, `committed`, `rolled_back`, or `rollback_failed`), and ordered entries containing destination, before-state, committed-after-state, and an optional contained payload. Directory state is a deterministic digest over relative name, kind, file digest/size, symlink target, and permission mode for every descendant. Timestamps are not conflict evidence; unsupported filesystem object kinds are rejected.

All payload paths are resolved beneath the backup directory, restore destinations are checked against the operation's canonical target allowlist, and hashes are verified before commit. Compatibility is explicit: schema-v2 is strict; an unversioned `entries` v1 manifest may restore file/symlink/missing entries only when it has sufficient digest/target evidence; v1 directories lack recursive attestation and are rejected even with `--force`; an unversioned `files` v0 manifest is rejected. Historical manifests are never rewritten in place. Rejection occurs before mutation with the backup ID and manual recovery guidance.

### Decision 3: Stage before mutation and roll back in reverse order

Every mutation has a staged replacement plus a captured before-state. While still holding the same lock, commit rechecks that the live state equals the internal plan's before-state, persists the prepared backup, applies mutations in order, and records each applied mutation. Restore first creates its own schema-v2 safety backup of the current state, so both a failed and a successful historical restore remain reversible. Any exception reverses applied mutations, restores prior LaunchAgent/plist/environment/service observations through the binding adapter, marks the backup `rolled_back`, and returns failure; rollback failure retains all material, marks `rollback_failed`, and reports the backup ID. Only a completely applied plan writes the active record/post-state and marks the backup committed.

### Decision 4: Atomic capture is a cloned-directory exchange under the store lock

Capture clones the existing profile directory into a sibling staging directory so non-managed profile artifacts such as plugin-support snapshots remain intact. It then replaces only the complete managed set (`config.toml`, `auth.json`, and manifest), validates TOML and required auth policy, renames the existing destination aside, and renames staging into place. The old directory is retained until transaction finalization succeeds; if any later rename, binding, or finalization step fails, the journal restores it. If the source lacks auth and missing auth is allowed, the staged profile intentionally removes `auth.json`; stale credentials cannot survive. This guarantees locked transactional rollback, not a single-syscall exchange of two non-empty directories.

### Decision 5: Store mutations use a non-blocking interprocess lock

Use a standard-library `fcntl.flock` adapter on the stable `store.root` directory inode, avoiding a lock-file write during dry-run. The lock is acquired before reading `active.json` or manifests and held through backup finalization. A mutating first-time bootstrap may atomically create the store root and then lock it before any canonical store read; a dry-run against a missing store fails read-only. Contention returns a precise busy error without backup or destination writes. Tests use two processes and a deterministic held-lock fixture.

### Decision 6: New switch and restore transactions use bound pending markers

Every newly armed supported switch or restore writes one store-root pending marker after its complete prepared backup tree and journal are durable and before the first destination or Desktop intent. The marker, prepared journal, and any independent terminal failure record bind the same operation, backup ID, random transaction ID, marker name, and SHA-256 of the canonical prepared journal with the digest field omitted. A terminal manifest atomically records both the outer lifecycle and the operation journal's terminal state before the marker is durably retired.

One classifier runs under the store lock before operation dispatch for switch, capture, restore, `init --capture-current`, and the preserved custom route. It handles marker-bearing current transactions, markerless legacy prepared switches, marker-required journals whose marker is missing, pre-marker prepared or rollback-failed restores, and unfinished capture journals. A marker-required journal with no begun effect may be closed as never started; begun marker-required work blocks rather than being treated as legacy. A narrowly bound `failure.json` may prove only a fully verified `rolled_back` terminal result after `backup.json` becomes unreadable. Valid terminal markers are retired before a new applying operation; cleanup failure retains the marker and reports outcome-specific guidance without reversing a committed result.

### Decision 7: Plan inputs and filesystem identities are frozen at their producing read

The immutable plan owns the exact bytes and state read for manifests, active collision checks, configs, auth, plugin snapshots, shell/bootstrap sources, Desktop read-modify-write state, stale-link inputs, wrappers, bindings, shared-support entry sets, and indirect composite builders. Planning may not read a value, later freeze a newer value, and then apply a payload derived from the older read. Every dependent effect revalidates its frozen sources and expected predecessor before intent and again through an already-open parent descriptor immediately before action.

Replacement effects persist a staged artifact and its device/inode identity before intent, then install that exact staged artifact through a descriptor-relative operation. The applied checkpoint revalidates the live produced identity, not just byte equality. Repeated effects on one canonical destination carry a predecessor and produced-identity chain; recovery validates the chain against intermediate journal state rather than comparing every historical identity to the final live inode. Directory create, chmod, and removal effects use the same identity and durability model. Stable attested lexical symlink ancestors remain compatible only while their recorded identity and target remain unchanged.

### Decision 8: Recovery is planned completely before its first write

Switch and restore recovery first validate the full manifest, marker binding, payload set, allowlist provenance, current states, route identities, staged/produced identities, Desktop chain, active state, directory effects, and parent cleanup. Only after this read-only simulation succeeds is a reverse action list executed. Every materialized file/tree/link/removal/chmod and every parent-directory mutation reaches its effect-specific durability boundary before the journal records `applied` or a terminal `rolled_back`/`recovered` state.

Restore records each original-parent cleanup as a journal effect with intent, expected before, planned missing state, observed after, identity, and durability evidence. Normal catchable rollback and next-invocation recovery share the same engine, restore active state last, accept already-restored state idempotently, and preserve any unrelated later state as an ambiguous recovery instead of overwriting it.

### Decision 9: A terminal reread must validate the complete bound commit

If an adapter writes the terminal manifest and then raises, the on-disk terminal state is authoritative only after strict validation against the still-present marker and prepared evidence. Validation includes schema, operation, backup and transaction IDs, marker name, prepared-journal digest, recovery requirement, authority/allowlist provenance, complete entries and payloads, applied effect chain, and terminal lifecycle/journal agreement. A minimal or unbound `committed` object never permits marker cleanup.

### Decision 10: Init with capture is one lock-owned dispatch

`cmd_init --capture-current` performs pending-state classification, initial official manifest/config creation, managed capture, and final init output under one store lock. The internal capture path accepts an already-held lock rather than reacquiring it. Busy or unresolved state is byte-for-byte read-only, while successful stdout ordering remains capture receipt followed by the existing `Initialized` and shim lines.

### Decision 11: Strict state metadata is uniform

Every recorded mode in v1/v2 before, after, committed, missing, file, directory, and symlink states rejects booleans, negatives, and values above `0o7777`; valid special permission bits through `0o7777` remain representable. Schema-v2 directory `entry_count` must agree with the attested recursive tree. Manifest-bound homes for both supported profiles must be absolute canonical roots outside `backups/`. `--force` bypasses only a current-state conflict, never schema, payload, route, identity, or authority validation.

### Decision 12: Runtime ownership is resolved before shared-support planning

`ipc` and `mcp-oauth-locks` are exact-name profile-local runtime directories. `shared_support_entries()` excludes them before the transaction freezes the shared-support entry set, captures recursive state, plans backup targets, or copies material. The entry-set observation attests the home identity plus the recursively captured state and identity of the filtered shared candidates and any top-level runtime/non-shareable symlink that may be removed as stale; it re-enumerates to detect additions or removals. Runtime directories themselves are never traversed. The source observation remains frozen through every mutation effect, while the target observation is planning-only because target changes are expected. Dry-run and apply consume that same filtered plan, so neither runtime directory crosses profile homes or enters a switch backup.

Only directories returned by `_missing_parent_paths()` receive a `target_home_ensure` effect. An existing target home has no no-op ensure effect and is never recursively captured merely to prove that it exists. Actual target writes remain route- and identity-attested, while a genuinely missing target-home chain retains its journaled creation and cleanup contract.

This is an ownership classification, not a general exception for sockets or other special files. Any unknown top-level or nested special filesystem object that reaches transactional state capture remains unsupported and fails closed before backup publication or mutation.

### Decision 13: A Desktop global-state no-op is not a transaction effect

The Desktop global-state target is read under a short producing-read
observation so the merge decision cannot adopt bytes that change during that
read. If merging the source settings subset produces byte-identical target
data, the target observation is released instead of retained, the path is not
added to planned commit states or the backup set, and no
`desktop_global_state_sync` effect is created. A running App may then replace
or update the target while later switch effects execute, and the transaction
preserves that external state because codex-switch never claimed ownership of
an output for the path.

When the merge produces different bytes, the target remains a frozen
read-modify-write input and the existing staged, route-bound, identity-checked
effect and rollback contract remains unchanged. This is a no-op ownership fix,
not a relaxation for real Desktop global-state writes or unrelated frozen
inputs.

A retained pre-fix `rollback_failed` marker may be recovered automatically only
when its marker binding is valid and its final filesystem effect is exactly the
old Desktop no-op shape: the canonical target matches the selected profile
home, no staged artifact or action-observed state exists, and the before,
planned, observed, frozen commit, and produced identity evidence all prove that
codex-switch changed no bytes or identity.

After that exact incident trigger is established, recovery derives an
evidence-bound no-op set from the same ordered journal. A preceding filesystem
effect joins the set only when its status, route guard, manifest entry, before
state, planned state, and observed state are present and the three states are
byte-identical. The effect may have replaced an inode while copying identical
bytes; codex-switch still has no terminal state change to reclaim. Recovery
therefore preserves any later externally owned state at every proven no-op
path, rolls back only the remaining attested real changes, records the
compatibility action on each released effect, and retires the marker.

This is not a path whitelist and does not infer safety from the current live
state. An effect with a real planned change, missing or mismatched entry,
route, state, ordering, profile, identity, or failure evidence is not released;
if its current state cannot be reconciled by the normal recovery chain, the
transaction remains blocked for manual recovery.

## Critical Path

1. Characterize snapshot-home, legacy-restore, recursive-conflict, partial-capture, late-binding failure, and contention failures with RED tests.
2. Add recursive state/payload preflight and schema-v2 backup support.
3. Add the lock-owned transaction execution seam and migrate independent plus snapshot switching.
4. Move capture and restore onto staged transactional mutation.
5. Add full rollback and lock coverage, then remove the legacy write path.
6. Reproduce the live `ipc.sock` failure through official shared dry-run, classify only the two known runtime directories, and preserve unknown-special-file rejection.
7. Reproduce the live Desktop global-state no-op race, remove only the no-op
   target from transaction ownership, and retain strict handling for a real
   merge.

## Incidental Finding Budget

One bounded RED/GREEN guard may be added for a newly discovered mutation that is already inside the transaction write set. Optional shell-profile symlink policy or arbitrary-profile namespace work is `DEFER_AND_CONTINUE`; public CLI removal, new persistence migration, or destructive workstation work is `BLOCKED_AWAITING_HUMAN`.

## Risks / Trade-offs

- [Recursive hashing adds switch latency for large support trees] → hash only planned mutation targets and retain mutation-aware planning so no-op directories are excluded.
- [Crash between directory renames can leave recovery artifacts] → use explicit `.stage`/`.previous` names under the locked store and recover or reject them deterministically on the next plan.
- [Launchctl effects are not filesystem-atomic] → represent them as an adapter mutation with captured plist/env/service observations and test every injected failure point.
- [Legacy backups remain unrestorable automatically] → fail before mutation and retain their files for documented manual recovery.
- [A future runtime directory could contain another special object] → add names only from observed ownership evidence; unknown objects remain fail-closed instead of being silently skipped.

## Migration Plan

Newly created backups use schema version 2. The v1 compatibility adapter accepts only sufficiently attested file/symlink/missing entries; v1 directories and v0 `files` manifests are identified and rejected before mutation. No live store rewrite occurs during installation, and historical manifests are not forged into v2. Rollback is code rollback plus preservation of all existing backup directories.

## Continuation Policy

- Execution policy: `auto-until-terminal`.
- Canonical execution source: this change's `tasks.md`.
- After each validated item, select the next dependency-ready transaction item.
- Genuine Human Gates: persistence behavior beyond the documented compatibility adapters, removing a CLI mode, destructive live-store action, or scope expansion.
- External effects such as a live profile switch, install, release, commit, push, archive, or migration stay separately unauthorized.

## Open Questions

None.
