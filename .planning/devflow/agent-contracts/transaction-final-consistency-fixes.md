# Agent Task Contract

## Goal
Close every actionable final-review gap in `transactional-profile-state` through one serialized RED-to-GREEN implementation slice. The result must have one crash-durable pending-transaction protocol for new switch/restore mutations, an immutable and identity-guarded switch plan, a single authoritative commit point, complete restore/switch recovery preflight, strict schema validation, and the same store lock around the preserved custom route. No transaction may destroy unplanned external drift or cross an unresolved recovery boundary.

## Worker ID
`transaction-consistency-finish`

## Stable Input Snapshot
- `scripts/codex_switch_transaction.py`: `7af13d846fd266f1abdc7e949f10114149929908814a0f5ee66bf0a110ff16d0`
- `scripts/test_codex_transaction.py`: `a210e5c9b12a83ede29af6dd15e01f3838af96f966af2bc579850bb873257edd`
- `scripts/codex_switch_restore.py`: `71c42c51e23a52a7ed7134eae519dac3bb8886187837c5eff558d1981b99fdb7`
- `scripts/codex_switch_switching.py`: `ea01bbd4e9da3bebe6dec611111e838bcc09b265313e55e65d36e271f722611b`
- `scripts/codex_switch_home_select.py`: `0404d915ebe51e812c87d5452c3cf2d9c0f636069f54a17474ba9d7769ca2b6c`
- `scripts/codex_switch_launch.py`: `5f08c0a73753f22bd8f34f58695ea4d62751974ad34da6535857d5f8d55f1dc2`
- `scripts/codex_switch_io.py`: `86dd60ce5459b67c9f759c8c3a4dc24a9af9a3c3c8ffae42ef635118a85c2970`

Stop before editing if any of these hashes drift. Report the changed path rather than merging concurrent production edits.

## Scope
Allowed write set for worker `transaction-consistency-finish` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_home_select.py`
- `scripts/codex_switch_launch.py`
- `scripts/codex_switch_io.py`

Read-only inputs include the entire `openspec/changes/transactional-profile-state/` change, existing tests/helpers, and prior task contracts. Forbidden: every other path, including OpenSpec files, `TASK_LEDGER.md`, `.planning/STATE.md`, verification records, `scripts/test_codex_profile_switch.py`, live profile stores, App bundles, launchctl state, plugin caches, Git staging, commits, pushes, installation, update, release, or network state. You are not alone in the worktree: preserve unrelated/main-agent changes and never revert them.

## Constraints
Implement the complete validated design below with Python 3.9-compatible standard-library code, strict RED-before-GREEN TDD, one production writer, temporary/fake runtime fixtures only, and no expansion beyond the named write set or approved compatibility boundaries.

## Authoritative Product and Compatibility Boundaries
- Product profiles remain only `internal` and `openai-official` (`official` is the existing alias). Do not add arbitrary-profile product behavior.
- Preserve the existing custom-profile route only as a compatibility path. Its internals are not being made fully transactional, but every applying custom switch must hold the same store lock and must fail closed before writes when a supported transaction is unresolved.
- Preserve schema-v2 plus evidence-bounded v1 restore and explicit v0 rejection. Historical backups are never rewritten or migrated.
- Preserve the public `execute_transaction(Store, TransactionRequest, dry_run=...)` seam and successful CLI output.
- No real Desktop/launchctl command may run in tests; use injected adapters/runners only.

## Required Design

### 1. Crash-durable pending-transaction evidence
Use one additive marker protocol for every newly armed supported official/internal switch or restore transaction. The preserved custom-profile route never arms or claims this marker/journal protocol; it only holds the common lock and runs the unresolved-transaction gate. Publish an immutable sidecar beneath the store root, named from a validated backup ID (for example `.pending-transaction-<backup-id>.json`), containing schema, operation, backup ID, a random transaction ID, creation time, and `prepared_journal_sha256`. Define one canonical JSON representation for the complete prepared journal with the `prepared_journal_sha256` field omitted, compute its SHA-256 before marker publication, and then persist the resulting digest in the journal, marker, and independent failure evidence. The same transaction ID, marker name, digest, and `recovery_marker_required=true` bind all evidence. Any backup-helper metadata needed for this protocol must remain optional so custom and historical v1/v2 callers retain their existing representation.

Do not block on arbitrary historical corrupt backup directories. Marker-bearing new transactions are authoritative; valid markerless legacy prepared switch journals retain their current compatibility recovery. If a new journal says a marker is required but the marker is missing, only an effect-free journal may be closed as never-started; any begun effect fails closed. A corrupt/symlinked/mismatched marker, missing/corrupt matching manifest, conflicting transaction IDs, ambiguous evidence, multiple unresolved markers, or `rollback_failed` evidence blocks every new mutation and reports the backup ID. The sole manifest-corruption exception is a durably written independent `failure.json` created only after complete rollback verification and containing the exact same marker name, backup ID, transaction ID, operation, and prepared-journal digest already trusted from the immutable marker; it may prove only terminal `rolled_back`. A digest asserted only by `failure.json` is not trusted. It may never turn `rollback_failed`, unknown, incomplete, or mismatched evidence into success.

The durability order is mandatory:
1. fully create and fsync backup payload/stage trees, `backup.json`, the backup directory, and `backups/`;
2. atomically persist and fsync the prepared journal;
3. atomically publish and fsync the store-root marker;
4. only then persist the first effect intent and execute a destination/Desktop mutation;
5. persist each intent before its effect, make the effect durable, observe it, then persist `applied`;
6. write lifecycle `committed` plus journal terminal/finalize-applied state in one atomic durable manifest write;
7. only after that terminal write, durably unlink the marker.

Fix `codex_switch_io.atomic_write()` to perform `write -> fchmod -> fsync(file) -> replace -> fsync(parent directory)`. It may create a missing parent privately, but it must not chmod an already-existing parent as an incidental child-file write. Fix transaction `_atomic_write_at()` to fsync its parent descriptor after rename. Add a standard-library-only durable unlink and effect durability boundary as needed. File, directory-tree, symlink, deletion, directory creation/chmod, manifest, and recovery effects must become durable before an `applied` checkpoint; external Desktop effects must be freshly observed before both intent and applied checkpoints rather than recording a planned state as an observation.

Marker cleanup is outside every rollback-capable region. Failure to unlink or fsync marker cleanup after the terminal commit must return outcome `committed` with the committed backup ID plus explicit retained-marker recovery guidance in the receipt; it must never return `rolled_back`, use semantically false `rollback_failed`, or roll the transaction back. The next applying transaction must recognize the matching committed evidence, durably retire the marker, and proceed safely.

### 2. Store-wide recovery gate
Inside `_StoreLock`, before operation dispatch or any new canonical mutation, classify all pending switch/restore evidence. A dry-run performs byte-for-byte zero writes: it reports a recoverable pending transaction or raises on corrupt/ambiguous evidence, but neither recovers nor cleans a marker.

For an applying operation:
- safely recover one deterministic prepared switch or restore before starting the requested operation;
- retire a stale marker only when matching terminal `committed`, `rolled_back`, or `recovered` evidence is durably valid;
- fail closed on multiple, corrupt, ambiguous, or rollback-failed recoveries;
- never let capture or restore pass an unresolved switch, and never let switch/capture/restore pass an unresolved restore.

Keep current markerless legacy prepared-switch recovery compatible. An unfinished, malformed, changed, or otherwise unresolved capture journal is also a store-wide recovery gate: it blocks switch, restore, custom apply, and capture for the other product profile before any new write. Only a capture retry for that exact product profile may enter the established pinned-directory recovery path. Dry-run and blocked operations must leave the capture journal, stage, previous directory, destination, backups, and every other store byte unchanged.

Expose only the smallest internal lock/gate seam needed by the preserved custom apply route. The custom route must acquire the same directory-inode lock before its first canonical read and retain it through backup finalization. Avoid nested locking for supported official/internal routes.

### 3. Immutable, identity-guarded switch plan
Freeze every source or read-modify-write input consumed by planning, including:
- both product manifests and `active.json` used for collision decisions;
- profile/base/target configs, auth bytes, shell profile, existing plugin-support snapshots, Desktop global-state inputs, shared-support sources, stale-link inputs, and wrapper/binding sources;
- any composite config/plugin input read indirectly by builders.

Apply only frozen payloads. Recheck each frozen source at the appropriate pre-mutation and pre-commit boundary; once this transaction intentionally writes a frozen path, compare it against its frozen planned commit state.

Each filesystem effect must persist and enforce an expected predecessor state, not merely adopt whatever exists at `begin()`. Maintain the expected chain for repeated writes to one path. Persist a crash-recoverable route guard containing the approved canonical anchor plus every lexical target/parent component's kind, device, inode, and symlink target. Stable lexical symlink ancestors already valid under current custom or evidence-bounded v1/v2 behavior remain compatible when their identity and target match; do not replace this with a blanket symlink ban. Marker/backup evidence I/O is likewise anchored through pinned store/backups descriptors.

For a replacement effect, pre-stage and persist the staged artifact identity before intent. The actual path action must use the already validated canonical-root/no-follow parent descriptor with `dir_fd`-relative mutation (or an equivalently race-free adapter primitive); a separate `resolve()` check followed by a path-based write is not sufficient. After action and before `applied`, accept only the persisted staged identity or the precisely planned non-replacement terminal state. A byte-identical foreign inode is not proof that this transaction produced the path. An unexpected predecessor, route identity, or produced identity aborts before overwrite or fails closed during recovery. Rollback may overwrite only a state and route provably produced/begun by this transaction; later external drift is preserved and classified as rollback failure/ambiguous recovery rather than destroyed. Open descriptors solve the live action race; the persisted route and staged identities solve next-process recovery.

Persist a planned after-state for every deterministic effect family: home-binding JSON, directory ensure/mode, shared support copy/link, Desktop global state, stale-link removal, config/canonical/profile/plugin/auth, shim, shell bootstrap, wrapper, plist, active, and all deterministic restore effects. Add after-action/before-checkpoint hard-interruption coverage rather than relying only on catchable exceptions.

### 4. Authoritative commit and idempotent switch recovery
All fallible source checks, payload checks, state checks, and journal preparation occur before the terminal manifest write. Switch commit must atomically write `lifecycle=committed` and finalize effect `status=applied`; restore commit must atomically write `lifecycle=committed` and `restore_journal.state=committed`. Nothing afterward may enter rollback.

If an adapter writes the terminal manifest and then raises, re-read the on-disk evidence. A matching durable committed lifecycle is authoritative and must never be rewritten to rolled_back. The same rule applies to switch and restore.

Prepared-switch recovery must completely preflight all entries, payloads, effect paths, strict modes/states, transaction IDs, persisted route/staged identities, and the canonical allowlist before its first recovery write. Missing later payloads cannot permit an earlier live target mutation. Recovery destinations must be allowed by canonical Store roots plus frozen/current official/internal manifest-bound homes; never trust an arbitrary serialized journal path.

Desktop recovery must be retry-idempotent. If the fresh observation already equals the persisted complete `desktop_before` state, skip reverse effect simulation/reconcile and continue terminal recovery. Hard interruption after Desktop reconcile but before lifecycle finalization must succeed on the next retry.

### 5. Durable restore journal and recovery
Replace the in-memory `applied` list as the recovery authority with an additive schema-1 `restore_journal` in the schema-v2 safety backup. Persist intent before every target materialization and every original-parent cleanup effect. Record expected before, deterministic planned after, observed after, entry index/path, staged identity, and all planned/actually created parent paths. At initial preflight, also persist the exact approved canonical destination, its no-follow route guard, and allowlist provenance derived from frozen canonical Store roots plus frozen before/planned official/internal manifest-home bindings. Recovery validates and consumes that frozen provenance; it must not recalculate authority only from a current manifest that the interrupted restore may already have changed.

Normal catchable failure and next-invocation recovery must use the same reverse recovery engine:
- validate the entire safety manifest, payload set, path allowlist, journal, and marker before the first rollback write;
- process begun effects in reverse, with `current == before` as already restored, `current == planned/observed after` as safely restorable, and every third state as ambiguous/fail closed;
- restore ordinary targets before active state and keep active restoration last;
- restore or remove only explicitly journaled parent-directory effects, deepest first, without deleting non-empty or externally changed directories;
- make recovery retry-idempotent across a second hard interruption;
- atomically persist `lifecycle=rolled_back` plus `restore_journal.state=recovered`, then durably remove the marker.

Prepared or rollback-failed restore evidence from the pre-marker implementation must block with the backup ID rather than be guessed or silently ignored.

### 6. Strict schema, allowlist, and reversible directory state
- Reject empty v1 and v2 entry lists before creating a safety backup.
- For every recorded permission mode, reject booleans, negative values, and values greater than `0o7777`; `--force` bypasses only current-state conflict, never schema/payload/path validation.
- Add canonical current official/internal manifest-bound homes to restore target roots. Validate them as absolute canonical paths and keep `backups/` excluded. A supported switch to an adopted manifest home must produce an immediately restorable backup.
- Do not create an overlapping whole-home backup entry merely to restore mode. Preserve the mode of an already-existing real target-home directory on successful switch; create a missing home as `0700`. Journal that directory predecessor/identity so rollback and recovery can prove the effect, and treat missing rollback state as an error. If the home was created, remove only the transaction-created empty directory chain.
- Persist the complete `created_target_directories` chain on the appropriate missing switch entry, deepest to shallowest, so a successful historical restore removes every still-empty transaction-created ancestor.

### 7. Bounded cleanup
After all correctness tests are green, use `rg` to prove and remove only the superseded dead helpers:
- the unused independent-switch planning/apply cluster in `codex_switch_switching.py`, while retaining `read_active_record()` and the live custom route;
- its now-unused `write_home_binding_updates()` helper/imports in `codex_switch_home_select.py`;
- unused legacy mutation helpers in `codex_switch_restore.py`, while retaining v0/v1 readers, `path_state`, schema-v2 creation/finalization, CLI adapter, and every live custom caller.

Do not retire `backup_live_files()` or the custom route because they remain compatibility callers. Do not broaden this cleanup to unrelated architecture.

## Required RED/GREEN Matrix
Add individually named tests, first proving RED against the stable hashes and then GREEN, for at least:

1. terminal switch write followed by catchable error remains committed and never rolls back;
2. terminal restore write followed by catchable error remains committed;
3. marker/backup tree is durable before the first intent/action, including `atomic_write` and `_atomic_write_at` ordering;
4. hard interruption after prepared journal, marker, intent, action, applied, terminal write, and marker unlink; retries classify deterministically;
5. corrupt marker, corrupt manifest, missing payload, mismatched transaction ID, multiple markers, and rollback_failed evidence block switch/capture/restore without new writes;
6. unrelated historical corrupt backup does not block, and valid markerless legacy prepared switch still recovers;
7. `recovery_marker_required=true` with a missing marker closes only an effect-free journal; any begun effect blocks; markerless pre-marker restore `prepared|rollback_failed` blocks; only a fully bound independent `failure.json=rolled_back` whose digest matches marker-bound `prepared_journal_sha256` may prove terminal state;
8. pending switch blocks capture/restore; pending restore blocks switch/capture/restore; unfinished/corrupt capture blocks switch/restore/custom/other-profile capture; matching capture retry alone recovers; every dry-run and blocked path is byte-identical;
9. restore hard interruption after the first target, then another interruption during recovery, then an idempotent successful retry;
10. restore first applies an official/internal manifest change, then hard-interrupts before an adopted-home effect; recovery uses frozen allowlist provenance and restores safely despite the changed current manifest;
11. restore parent-cleanup interruption rolls back the cleanup state;
12. Desktop already at `desktop_before` after interrupted reconcile is accepted and finalized;
13. every deterministic filesystem effect family can recover after action/before applied checkpoint;
14. late active/shell/plugin/auth/shared/composite-source drift is caught before overwrite;
15. target or parent swapped for symlink/byte-identical replacement is rejected before mutation, including an injection after route validation and before action proving the pinned parent descriptor prevents redirection;
16. hard interruption after replacement but before `applied`, followed by a byte-identical foreign inode, is rejected because it does not match the persisted staged identity;
17. late external target drift is not overwritten by rollback;
18. successful and failed switches preserve an existing target-home mode; a new home is `0700`, and failed switch or historical restore removes its complete nested created chain;
19. adopted official/internal manifest home switch backup restores successfully;
20. empty v1/v2 entries and modes `-1`, boolean, or `>0o7777` fail before safety backup even with force;
21. prepared recovery rejects an out-of-allowlist path or any missing/corrupt later payload before its first write;
22. terminal switch/restore marker unlink or parent-fsync failure still returns `committed` with retained-marker guidance, and the next apply safely retires it without rollback;
23. stable, attested symlink ancestors remain compatible, while changed symlink identity/target fails closed;
24. a custom apply receives `profile store is busy` and performs no write while the common lock is held and never arms a transaction marker;
25. final `rg` proves removed helpers have no callers.

Use only temporary roots, fake adapters, fake Desktop state, and child processes that touch temporary fixtures. Do not invoke real launchctl or live store paths.

## Verification
Run and return exact results for:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate transactional-profile-state --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
```

Also run Python 3.9 and 3.12 compile/AST/import checks for all changed modules, focused tests for every named RED/GREEN vector, and `rg` caller checks for cleanup. Before reporting, record stable SHA-256 for every changed file and rerun the full transaction suite once against those hashes.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus:
- exact changed files and stable hashes;
- ordered RED failure reasons and GREEN commands/results;
- complete test logs or validation results for every focused and full command;
- marker/journal schema examples and durability event order;
- pending-transaction classification table results;
- switch/restore/second-interruption recovery matrices;
- immutable input and path/parent identity vectors;
- commit-authority, Desktop idempotence, schema/allowlist/mode, adopted-home, nested-parent, and custom-lock results;
- dual-interpreter/full legacy/strict/syntax/diff results;
- residual risks and unverified areas;
- incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`.

Do not mark OpenSpec tasks or edit main-owned evidence/control-plane files.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing a public CLI or persistence compatibility contract beyond the additive marker/journal fields above, auto-restoring ambiguous or unallowlisted evidence, rewriting historical backups, removing the custom route, changing product profiles, weakening v0/v1/v2 validation, expanding the write set, adding a dependency, running a live Desktop/store mutation, bypassing a failing test, or performing Git/install/update/release/network actions. If a required repair needs another path, report the exact seam and reason rather than editing it.
