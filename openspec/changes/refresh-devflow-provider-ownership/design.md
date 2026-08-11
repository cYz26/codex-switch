## Context

See `proposal.md` for motivation. DevFlow
`0.3.0+codex.20260529145038` is installed and verified `matches-source`; the
six OpenSpec 1.7 skills and sixteen DevFlow skills are already current under
`.agents/skills`. The active conflict comes from the older provider contract
and ignored project-local artifacts: twelve legacy DevFlow links, nineteen
GSD skills, GSD agents/hooks/runtime configuration, active GSD/Superpowers
skills under `.agents/skills`, and four broken legacy Superpowers links.

The installed migration launcher reports these legacy items but deliberately
does not remove them. Its generated zipapp-subpath command is invalid on this
installation; the adjacent `scripts/activate_project_dependencies.py` launcher
is the verified operational path.

## Target State

- `AGENTS.md` is the latest brownfield DevFlow contract plus the preserved
  codex-switch internal-binary upgrade section.
- `.dev-flow.json` contains only `{"workflow":{"mode":"full-openspec"}}`.
- Active project discovery contains sixteen DevFlow skills, exactly six
  OpenSpec 1.7 skills, and only triggered members of the approved six-item Matt
  allowlist. The current set is five; `domain-modeling` remains absent because
  `domain-language-modeling` is skipped.
- GSD/Superpowers project providers and legacy `.codex/skills` duplicates are
  absent from active paths but recoverable from the registered quarantine.
- Existing parity work, `.planning` history, `.codex/gsd-migration-journal`,
  product/runtime configuration, and Git history remain unchanged.

## Goals / Non-Goals

**Goals:**

- Resolve the durable provider-ownership conflict and active legacy layout.
- Make every cleanup move ownership-checked, exact-path, and reversible.
- Produce fresh diagnostics and a terminal migration receipt.

**Non-Goals:**

- Physical deletion of the quarantine or historical planning data.
- Changes to codex-switch product behavior, dependencies, profiles,
  credentials, running processes, parity source, Git history, release, or
  archive state.
- Repairing the DevFlow-generated invalid zipapp-subpath recommendation; it is
  recorded as a non-blocking upstream/tooling finding and the supported
  adjacent launcher is used locally.

## Capability Evidence Ledger

- `authoritative_current`: installed DevFlow cache
  `0.3.0+codex.20260529145038`; updater evidence reports `matches-source`;
  OpenSpec reports 1.7.0 and its six expected skills.
- `local_scan`: current/template `AGENTS.md`, `.agents/skills`,
  `.codex/skills`, GSD config/hooks/runtime, GSD file manifest, migration
  reports, `.planning/devflow/STATE.md`, active parity change, and Git status.
- `comparison`: automatic layout apply preserves duplicates/manual items;
  narrow cleanup leaves old runtime providers active; recoverable full
  provider migration is the only option satisfying the approved Target State.
- `assumptions`: none that can change the task breakdown. A new Codex task is
  still required to observe the refreshed startup-time skill inventory.
- `contract`: `specs/devflow-provider-ownership/spec.md` plus the validation
  commands in `tasks.md`.

## Skill Routing Ledger

| Field | Status | Reason / Evidence |
|---|---|---|
| artifact-status | final | User approved方案 A; no design question remains. |
| request-kind | migration + workflow repair | Provider ownership, active skill layout, and runtime configuration change. |
| workflow-mode | Full OpenSpec | Migration and compatibility behavior require it. |
| capability-research | required / used | Current cache, launcher behavior, skill inventory, and GSD ownership were verified locally. |
| decision-resolution | required / used | Three approaches were compared and the user approved the systemic recoverable migration. |
| decision-grilling | skipped | Evidence and explicit方案 A approval resolved all open decisions. |
| implementation-planning | required / used | `change-plan`, `ai-native-tech-plan`, and OpenSpec own this plan. |
| architecture-guidance | skipped | No product architecture or new interface is designed; the current DevFlow template fixes the provider boundary. |
| domain-language-modeling | skipped | No domain model or invariant vocabulary changes; `domain-modeling` therefore remains uninstalled. |
| openspec-routing | required / used | New change `refresh-devflow-provider-ownership`. |
| test-first-execution | required / used | The pre-migration layout diagnostics are the characterization RED; post-migration diagnostics must turn current without code changes. |
| subagents | skipped | Shared control-plane and provider roots make the work serial; the user did not request delegation. |

## Decisions

### Merge the template; do not overwrite project guidance

Start from the current DevFlow template, substitute `brownfield`, and insert
the existing `Codex Internal Binary Upgrade Context` after Purpose. This keeps
the template authoritative for generic workflow rules without losing the only
project-specific section. The older GSD/Superpowers ownership sections are not
retained because preserving them would recreate the conflict.

Alternative rejected: keep both ownership models. That would leave ambiguous
capability routing and continue discovering retired providers.

### Use a registered, in-repository ignored quarantine

Physical quarantine root:
`.codex/provider-migration-quarantine/20260804T165042+0800/`.
Durable contract and receipts root:
`.planning/devflow/provider-migration/20260804T165042+0800/`.

The durable contract MUST exist before the physical root is created. Moves use
explicit source and destination paths, never wildcards or recursive deletion.
The quarantine remains ignored and recoverable; a later physical purge is a
separate Human Gate.

Alternative rejected: delete the legacy artifacts. Deletion is unnecessary
for provider deactivation and weakens rollback. Moving them into tracked
`.planning` was also rejected because it would add hundreds of generated GSD
files to the repository.

### Move only proven active/provider-owned surfaces

The approved move set is:

- twelve named legacy DevFlow symlinks under `.codex/skills`;
- nineteen named GSD skill directories under `.codex/skills`;
- four broken legacy Superpowers symlinks under `.codex/skills`;
- six GSD directories and four Superpowers symlinks under `.agents/skills`;
- `.codex/agents`, `.codex/gsd-core`, `.codex/hooks`, `.codex/config.toml`,
  `.codex/hooks.json`, `.codex/.gsd-profile`,
  `.codex/gsd-file-manifest.json`, `.codex/gsd-install-state.json`, and the
  empty `.codex/get-shit-done` compatibility tree;
- the nine installer-manifest-owned files below `.codex/scripts`.

The GSD manifest contains 391 files; all 391 preflight hashes match, with zero
missing or drifted files. `.codex/scripts/changeset/README.md` is not in that
manifest and remains in place as preserved unknown content. The GSD migration
journal and all `.planning` content remain in place as history.

### Treat the migration launcher as verifier, not cleanup owner

Run the official dry-run before mutation and after mutation. Because its apply
path intentionally does not remove duplicates/manual items, exact moves are
owned by this OpenSpec change and guarded by the pre-created quarantine
contract. Ordinary `plugin_project_migration.py --apply` runs afterward only
to refresh its audit state.

## Generated Artifact Contract

- Contract ID: `DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800`.
- Owner: this main task and OpenSpec change only; no subagent or hook owns it.
- Precondition: physical quarantine root is absent and every source matches
  its recorded type/target/hash/inventory.
- Root: `.codex/provider-migration-quarantine/20260804T165042+0800/`.
- Retention: `RETAIN` after successful migration for rollback evidence.
- Cleanup policy: no automatic purge; physical purge requires a new Human Gate.
- Terminal evidence: durable contract, before inventory, move mapping,
  post-move checks, rollback instructions, and completion receipt under the
  durable receipts root.
- Owner exit: after final verification or on the first attestation/move
  failure. A failure records `HUMAN_GATE` and stops further mutation.

## Critical Path

1. Seal contract and capture exact pre-migration evidence.
2. Merge guidance and add minimal workflow configuration.
3. Move the exact approved provider surfaces into quarantine.
4. Refresh migration audit state and prove the active layout is current.
5. Record verification, state, and rollback evidence.

## Incidental Finding Budget

One bounded classification cycle is allowed. The invalid generated zipapp
command is `DEFER_AND_CONTINUE`: it does not invalidate the adjacent launcher
or the Completion Contract and is recorded without modifying DevFlow source.
Any failure of an acceptance validator is required behavior and cannot be
deferred.

## Escalation Triggers

Stop before further mutation if a source path drifts, an unexpected child is
found in a whole-directory move, a non-GSD configuration shares a targeted
file, the quarantine root already exists, parity-owned content changes,
dependency or runtime/process mutation becomes necessary, or the write set
must expand.

## Migration Plan

1. Create the durable quarantine contract and preflight receipt.
2. Re-attest Git scope, GSD manifest hashes, path types, symlink targets,
   whole-directory inventories, and absence of the quarantine root.
3. Merge `AGENTS.md` and add `.dev-flow.json`.
4. Create the quarantine root and move exact approved paths, preserving
   relative source mapping.
5. Rerun the layout dry-run, ordinary migration apply, workflow validation,
   Doctor/cache drift, scaffold dry-run, strict OpenSpec, and Git checks.
6. Update tasks, namespaced state, and terminal receipt. Do not archive,
   commit, push, restart, or purge.

Rollback moves each receipt-listed quarantine path back to its exact original
path only after confirming the original path is absent. Restore the pre-merge
`AGENTS.md` and remove `.dev-flow.json` only from a receipt-bound rollback;
rollback itself is not automatically exercised after successful validation.

## Continuation Policy

Execution is `auto-until-terminal`. Each dependency-ready task continues to
the next task without a routine confirmation. Terminal outcomes are
`CONTINUE_NEXT_ITEM`, `CHECKPOINT_AND_CONTINUE`, `VERIFY_ACTIVE_CHANGE`,
`AWAIT_HUMAN`, `READY_FOR_EXTERNAL_EFFECT`, or `COMPLETE`. Only an escalation
trigger produces `AWAIT_HUMAN`; commit, push, restart, archive, release, and
quarantine purge remain excluded external-effect gates.

## Risks / Trade-offs

- Running tasks can retain the old skill inventory -> Require a new task before
  relying on provider discovery.
- Ignored quarantine is not transported by Git -> Keep the durable mapping and
  do not claim cross-machine rollback; this migration concerns this workstation.
- Moving GSD hooks/config disables their project-local behavior immediately ->
  Perform exact preflight, retain recovery bytes, and validate DevFlow/OpenSpec
  replacements before completion.
- A broad directory could hide user content -> Compare its full inventory to
  the approved manifest/name set and stop on any unexpected child.
