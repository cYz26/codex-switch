## Target State

The tracked workflow contract and minimal configuration select only OpenSpec,
DevFlow, and triggered members of the approved six-item Matt allowlist. Every
approved legacy DevFlow/GSD/Superpowers provider surface is outside active
discovery/runtime paths and recoverable from the registered quarantine. Project history,
pre-existing parity work, runtime/profile state, dependencies, and Git history
remain unchanged.

## Scope / Non-Goals

**Write set:**

- `AGENTS.md`
- `.dev-flow.json`
- this OpenSpec change
- `.planning/devflow/STATE.md`
- `.planning/devflow/plugin-project-migration/**`
- `.planning/devflow/provider-migration/20260804T165042+0800/**`
- `.planning/devflow/verification/20260804T165042-devflow-provider-migration.md`
- the exact active provider paths listed in the Quarantine Manifest below
- `.codex/provider-migration-quarantine/20260804T165042+0800/**`

**Non-goals:** product/parity source, the active parity OpenSpec change,
`TASK_LEDGER.md`, `.planning/STATE.md`, `.planning/checkpoints/**`, profiles,
credentials, application processes, dependencies, Git commit/push, release,
archive, or quarantine purge.

## Completion Contract

- [x] The latest DevFlow guidance is merged and the internal-binary contract is preserved.
- [x] `.dev-flow.json` is the minimal `full-openspec` configuration.
- [x] The active project layout has zero `legacy_duplicate` and zero `manual_review_required` items.
- [x] Sixteen DevFlow, six OpenSpec 1.7, and the current five triggered Matt project skills remain healthy; skipped `domain-modeling` remains absent.
- [x] GSD/Superpowers are absent from active project discovery and GSD hooks/config/runtime are inactive.
- [x] Every move has a durable exact rollback mapping; physical quarantine remains retained.
- [x] Pre-existing parity and other unrelated dirty paths match their pre-migration fingerprint.
- [x] Workflow validation, Doctor/cache drift, scaffold dry-run, strict OpenSpec, and scoped Git checks pass.
- [x] No commit, push, restart, release, archive, dependency, profile, credential, or product-code effect occurs.

## Quarantine Manifest

Contract ID: `DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800`.

Legacy DevFlow links under `.codex/skills`:

```text
capability-research
change-plan
checkpoint-compact
claude-code-delegate
context-tool-audit
execute-task
feature-intake
plugin-project-migration
project-orchestrator
project-setup
verify-and-archive
workflow-doctor
```

GSD skills under `.codex/skills`:

```text
gsd-code-review
gsd-config
gsd-discuss-phase
gsd-execute-phase
gsd-help
gsd-import
gsd-new-project
gsd-pause-work
gsd-phase
gsd-plan-phase
gsd-progress
gsd-quick
gsd-resume-work
gsd-review
gsd-settings
gsd-surface
gsd-update
gsd-verify-work
gsd-workspace
```

Superpowers links under both `.codex/skills` and `.agents/skills`:

```text
brainstorming
test-driven-development
verification-before-completion
writing-plans
```

GSD skills under `.agents/skills`:

```text
gsd-discuss-phase
gsd-execute-phase
gsd-new-project
gsd-plan-phase
gsd-progress
gsd-verify-work
```

Whole provider-owned paths:

```text
.codex/.gsd-profile
.codex/agents
.codex/config.toml
.codex/get-shit-done
.codex/gsd-core
.codex/gsd-file-manifest.json
.codex/gsd-install-state.json
.codex/hooks
.codex/hooks.json
```

Manifest-owned GSD script files:

```text
.codex/scripts/changeset/cli.cjs
.codex/scripts/changeset/github-release-notes.cjs
.codex/scripts/changeset/lint.cjs
.codex/scripts/changeset/new.cjs
.codex/scripts/changeset/parse.cjs
.codex/scripts/changeset/render.cjs
.codex/scripts/changeset/serialize.cjs
.codex/scripts/lib/allowlist-ratchet.cjs
.codex/scripts/lib/cli-exit.cjs
```

Explicit retained paths:

```text
.codex/gsd-migration-journal
.codex/scripts/changeset/README.md
.planning
```

## 1. Seal and Validate the Migration Contract

- [x] 1.1 Create the durable generated-artifact contract at `.planning/devflow/provider-migration/20260804T165042+0800/contract.md` before creating the physical quarantine root; include contract ID, exact roots, move set, retained set, owner exit, rollback rules, and purge Human Gate.
- [x] 1.2 Capture pre-migration evidence in `.planning/devflow/provider-migration/20260804T165042+0800/preflight.md`: the invalid mandated zipapp command exit, successful adjacent-launcher characterization RED, all 391 GSD manifest hashes, exact symlink targets/types, whole-directory inventories, GSD-only config/hook ownership, and the unrelated dirty-work fingerprint.
- [x] 1.3 Run strict validation of this change and confirm the physical quarantine root is absent; stop on any OpenSpec failure, existing root, ownership drift, or unexpected child.

## 2. Refresh the Durable Control Plane

- [x] 2.1 Replace generic workflow guidance in `AGENTS.md` with the current installed DevFlow template, substitute project mode `brownfield`, and preserve the exact `Codex Internal Binary Upgrade Context` section after Purpose.
- [x] 2.2 Add `.dev-flow.json` with exactly `{"workflow":{"mode":"full-openspec"}}` and validate it as JSON.
- [x] 2.3 Run workflow validation and scaffold dry-run; confirm durable markers pass and no unresolved `AGENTS.md.generated` source remains before provider moves.

## 3. Quarantine the Approved Legacy Providers

- [x] 3.1 Re-attest every manifest entry immediately before mutation, create only `.codex/provider-migration-quarantine/20260804T165042+0800/`, and record its device/inode/mode in the durable receipt root.
- [x] 3.2 Move the twelve exact legacy DevFlow links and four exact broken legacy Superpowers links from `.codex/skills` into quarantine while preserving their relative source mapping; verify all official `.agents/skills` DevFlow targets remain valid.
- [x] 3.3 Move the nineteen exact GSD `.codex/skills` directories, six exact GSD `.agents/skills` directories, and four exact active Superpowers `.agents/skills` links into quarantine; verify no other skill path moved.
- [x] 3.4 Move the exact GSD agents, hooks, runtime, configuration, installer metadata, empty compatibility tree, and nine manifest-owned script files into quarantine after final whole-root inventory checks; retain the GSD journal and unowned README in place.
- [x] 3.5 Verify each original path is absent, each quarantine destination has the expected type/content or symlink target, active provider counts are 16 DevFlow + 6 OpenSpec + 5 triggered Matt, skipped `domain-modeling` remains absent, and no GSD/Superpowers provider remains active.

## 4. Refresh Migration State and Diagnose the Final Layout

- [x] 4.1 Rerun the adjacent-launcher official-layout dry-run and require `status: current` with zero `legacy_duplicate` and zero `manual_review_required` items.
- [x] 4.2 Run `plugin_project_migration.py --apply --json` to refresh only its ordinary audit state, then verify stored/runtime version parity and no missing/stale/conflicting official skills.
- [x] 4.3 Run workflow validation, Doctor with cache drift, and scaffold dry-run; require healthy/current results, `AGENTS` disposition `merged` or `unchanged`, and no generated competitor file.

## 5. Completion Proof and State

- [x] 5.1 Run strict validation for `refresh-devflow-provider-ownership`, `internal-official-feature-parity`, and all OpenSpec changes; run JSON, whitespace, symlink, retained-history, and unrelated-dirty-fingerprint checks.
- [x] 5.2 Write `.planning/devflow/verification/20260804T165042-devflow-provider-migration.md` with RED/GREEN evidence, exact moves, retained paths, commands/results, rollback instructions, residual risks, and new-task guidance.
- [x] 5.3 Update `.planning/devflow/STATE.md` with the completed maintenance change while preserving the active parity Human Gate; reconcile every checkbox here against fresh evidence.
- [x] 5.4 Run final migration sync, workflow validation, Doctor/cache drift, scaffold dry-run, strict OpenSpec, and `git status`; perform a read-only scope review and stop without archive, commit, push, restart, release, or quarantine purge.

## Capability Slices

| Slice | Production-complete result | Validation | Cleanup |
|---|---|---|---|
| Contract and preflight | Exact ownership, rollback, and unrelated-work baselines are durable before mutation | hash/type/inventory checks; strict OpenSpec | no physical root before contract |
| Durable control plane | Latest provider rules and minimal mode config are canonical | workflow validator; JSON; scaffold dry-run | no generated guidance competitor |
| Recoverable provider migration | Old providers are inactive and every byte remains recoverable | exact source/destination checks; provider counts | retain quarantine; no purge |
| Migration reconciliation | Official layout and audit state are current | migration dry-run/apply; Doctor/cache drift | no legacy discovery residue |
| Completion proof | Change and preserved boundaries are auditable | strict OpenSpec; Git/fingerprint/review | no external or Git effect |

## Execution Ledger

| Task | Owner | Write Set | Required Evidence | Human Gate | Next Outcome | Status |
|---|---|---|---|---|---|---|
| 1.1-1.3 | main, serialized | new OpenSpec/contract/preflight files | sealed contract, RED, 391/391 hashes, fingerprints | unexpected ownership/root | CONTINUE_NEXT_ITEM | complete; contract preceded physical root, strict OpenSpec passes, inventories are exact, and unrelated fingerprint is `4cd5ca8...ff61f` |
| 2.1-2.3 | main, serialized | `AGENTS.md`, `.dev-flow.json` | preserved internal section, JSON, validator/scaffold | template conflict beyond approved design | CONTINUE_NEXT_ITEM | complete; generic guidance matches the installed template, the internal section matches `HEAD`, JSON is exact, validator is healthy, and no generated competitor exists |
| 3.1-3.5 | main, serialized | exact manifest sources + quarantine | exact mappings, counts, retained paths | any drift/unowned child | CONTINUE_NEXT_ITEM | complete; all sources map to recovery destinations, 391/391 manifest bytes match, active GSD/Superpowers count is zero, history is retained, and unrelated fingerprint is unchanged |
| 4.1-4.3 | main, serialized | migration audit files only | current layout, healthy Doctor/validator | managed-target conflict | VERIFY_ACTIVE_CHANGE | complete; migration audit is current with version parity and no skill drift/conflict, validator has zero issues/warnings, Doctor is healthy with cache-drift checking, scaffold dry-run exits zero, and `AGENTS.md.generated` is absent |
| 5.1-5.4 | main, serialized | verification, namespaced state, this ledger | fresh complete command set and scope review | failing required validator | COMPLETE | complete; terminal receipt is `RETAIN`, mapping/manifest/provider/fingerprint checks pass, validator and Doctor are healthy, OpenSpec is 19/19, scoped review has no blocking finding, and all excluded effects remain absent |

No subagent is authorized. The main agent owns all control-plane, quarantine,
integration, and completion evidence.

## Characterization RED

The required pre-migration dry-run is already reproducible:

```text
mandated zipapp-subpath command: exit 1, can't find '__main__' module
adjacent launcher: exit 0, status legacy_duplicate
legacy_duplicate: 12
manual_review_required: 19
GSD manifest: 391/391 hashes match, 0 mismatch, 0 missing
```

GREEN requires the adjacent launcher to report a current layout with neither
legacy status after the exact recoverable migration.

## Validation Commands

```bash
python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/activate_project_dependencies.py \
  --repo /Users/cY/dev/codex-switch --skip-official-installs \
  --migrate-official-skill-layout --dry-run --json

python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/plugin_project_migration.py \
  --repo /Users/cY/dev/codex-switch --codex-home /Users/cY/.codex --apply --json

python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py \
  --repo /Users/cY/dev/codex-switch --json

python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/doctor_workflow.py \
  --repo /Users/cY/dev/codex-switch --check-cache-drift --json

python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/scaffold_workflow.py \
  --repo /Users/cY/dev/codex-switch --mode auto --dry-run --json

python3.12 /Users/cY/dev/skills/cy-codex-skills/dev/scripts/codex_auto_update_plugins_skills.py --json

python3 -m json.tool .dev-flow.json >/dev/null
openspec validate refresh-devflow-provider-ownership --strict --no-interactive
openspec validate internal-official-feature-parity --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
git status --short --untracked-files=all
```

## Risks / Rollback

- Stop on any path-type/hash/inventory drift; do not partially improvise a new
  move set.
- Rollback uses only receipt-listed destination-to-source moves after proving
  every original path is absent. Never overwrite a newly created active path.
- Restore `AGENTS.md` and `.dev-flow.json` only from their recorded pre-change
  state if rollback is explicitly selected after a failure.
- The ignored quarantine is workstation-local; it is retained, not advertised
  as a cross-machine backup.
- A new Codex task is required to observe the new discovery set.

## Incidental Finding Register

### DF-IF-PM-SOURCE-IDENTITY

- Disposition: `DEFER_AND_CONTINUE`.
- Finding: the full local updater dry-run reports
  `project-migration-sync: migration-pending` only when it invokes migration
  inspection with the local marketplace source as `plugin_root`; the same
  inspection with the installed cache reports `current`.
- Root cause: the inspector accepts only the invocation root as a valid skill
  target in this external-project layout. The sixteen official links point to
  the installed cache, so the marketplace-source invocation labels them stale
  even though source and cache are byte-identical.
- Evidence: two deterministic differential runs each produced
  installed-cache `current` with 0 stale and marketplace-source
  `migration_pending` with 16 stale; `diff -qr` between those plugin trees is
  empty, the cache verifier reports `matches-source`, and both versions are
  `0.3.0+codex.20260529145038`.
- Why non-blocking: active discovery uses the installed cache; the installed
  migration route is current, official layout is current with zero legacy
  items, and Doctor/cache drift is healthy. Applying the alternate identity
  would merely invert which inspector reports stale.
- Mitigation/follow-up: retain installed-cache links and make no additional
  apply. A separate DevFlow source change should normalize accepted
  byte-identical source/cache identities and add a differential regression.

### DF-IF-PM-ZIPAPP-COMMAND

- Disposition: `DEFER_AND_CONTINUE`.
- Finding: generated migration recommendations still compose an invalid
  `devflow_runtime.pyz/activate_project_dependencies.py` subpath.
- Why non-blocking: the adjacent installed launcher is current and is the
  command used for all RED/GREEN migration evidence.
- Mitigation/follow-up: keep using the adjacent launcher; repair recommendation
  composition in a separately scoped DevFlow source change.

## Review Checklist

- [x] Spec scenarios map to one or more tasks and validators.
- [x] Every moved source is exact and ownership-proven.
- [x] No wildcard/recursive deletion or physical purge occurred.
- [x] Project-specific internal binary guidance remains intact.
- [x] GSD/Superpowers are inactive while history and rollback bytes remain.
- [x] Parity WIP and Human Gate are unchanged.
- [x] No dependency, process, profile, credential, Git, release, or archive effect occurred.

## Final Verification

Completion requires every task and checklist item above to be checked against
fresh evidence. `openspec status --change refresh-devflow-provider-ownership`
must show all planning artifacts complete; archive remains unauthorized.
