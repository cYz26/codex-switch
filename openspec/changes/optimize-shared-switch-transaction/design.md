## Context

See `proposal.md` for motivation. The captured
`20260810T070723Z-switch-openai-official-to-internal` transaction froze 99
inputs, selected 39 generic Home entries, and reached only eight applied
shared-support effects plus one intent in approximately ten minutes. The
largest selected tree was `worktrees` with 8,028 recorded nodes. One full
frozen-input validation measured about 7.9 seconds, while each filesystem
effect currently performs that validation before intent, after intent, and
after action. All begun effects recovered when the App rewrote the canonical
Desktop global-state file.

The existing shared-capability module already owns Plugin selectors,
marketplace descriptors, configured Skills, personal-Skill linking, and
per-profile cache materialization. Generic Home support is a legacy transport
and must not become a second Plugin/Skill ownership system.

The supported split currently reuses the synchronized-switch Desktop path even
when the App is already healthy on the official bundle. It rewrites the
LaunchAgent, invokes `launchctl setenv/bootout/bootstrap`, and freezes Desktop
global-state projection inputs. Those unnecessary App effects, rather than
App-to-internal capability reconciliation, are what make stopped-App proof a
blanket requirement.

### Skill Routing Ledger

- artifact-status: final; the user confirmed the systemic repair and no Open
  Questions remain.
- capability-research: skipped; the failure receipt, current filesystem, source
  code, and deterministic local timing establish every required capability
  assumption without external or time-sensitive evidence.
- decision-resolution: used; the user explicitly selected the systemic
  allowlist, bounded validation, progress solution, and an effect-derived
  App-preserving split that requires stopped-App proof only for real rebinds.
- decision-grilling: skipped; there is no unresolved product or ownership
  choice after that confirmation.
- implementation-planning: used; this design, delta spec, and task list are the
  canonical executable contract.
- architecture-guidance: used; `codebase-design` concentrates selection and
  validation policy behind the existing Home and transaction interfaces.
- domain-language-modeling: skipped; no new domain concepts or invariants are
  needed beyond existing source/target/effect/CAS terminology.
- openspec-routing: used; the previously deferred INC-014 compatibility
  migration receives this dedicated Full OpenSpec change instead of expanding
  the split-profile change silently.

## Target State

A supported split observes the App surface before backup. When that surface is
already healthy on the canonical official binding, the transaction preserves
it and applies only the internal CLI side while the App remains running. When
an App-owned effect is required, the existing stopped-App proof remains
fail-closed. Generic Home sync considers exactly four V1 support names
(`AGENTS.md`, `prompts`, `rules`, and `skills`), reports deterministic item
progress, and completes with deep source validation work bounded independently
of unrelated effect count. A late source mutation or App mutation during an
actual rebind still causes exact journal rollback before commit.

## Goals / Non-Goals

**Goals:**

- Make generic Home support ownership explicit, reviewable, versioned, and
  non-destructive for ignored entries.
- Reduce the long transaction window without weakening source generation,
  target predecessor, route, identity, final CAS, or rollback proofs.
- Preserve an already healthy official App without process interruption, while
  retaining an early stopped-App error for a real rebind and counted mutation
  progress for CLI-owned effects.
- Preserve the existing Plugin/Skill desired-state and independent-cache model.

**Non-Goals:**

- Sharing memories, worktrees, generated images, visualizations, history,
  logs, caches, credentials, sessions, UI state, or unknown future entries.
- Deleting or migrating previously propagated unknown entries.
- Changing synchronized-switch Desktop global-state behavior, Plugin
  materialization, profile config merge semantics, update policy, or supported
  profile pairs. The supported split simply stops consuming Desktop settings.
- Live activation, App stop/restart, installation, internal binary upgrade,
  release, archive, Git effects, dependency activation, or cleanup.

## Architecture Decisions

### Decision 1: One versioned allowlist owns generic Home selection

`shared_support_entries` remains the single interface used by planning,
application, launcher preparation, and tests. Its V1 allowlist is
`AGENTS.md`, `prompts`, `rules`, and `skills`. Special Desktop settings remain
outside this interface, and Plugin caches remain explicitly excluded. Ignored
source and target entries are never removed.

A longer denylist or a prefix-only temporary-file patch was rejected because
both continue treating every future unknown entry as shared. Reusing the
shared-capability desired state for rules/prompts was rejected because it would
mix unrelated ownership and persistence models.

### Decision 2: Entry-set capture proves membership and identity, not content

The shared-entry-set capture records the Home identity and deterministic
allowlisted entry names/roles/identities. It does not recursively capture each
entry's content again. Each selected child remains an independently frozen
input, so content has one authoritative source observation while membership
changes and path replacement still fail closed.

Keeping recursive child state inside both the parent entry-set and every child
was rejected because it duplicates all tree traversal without adding an
independent invariant.

### Decision 3: Continuous guards and final CAS have distinct costs

The transaction journal keeps its existing external interface and recovery
format. During an effect, continuous validation fully checks files, symlinks,
missing paths, shared-entry membership, and all filesystem identities, but it
does not recursively hash every unrelated directory. The current shared source
is checked immediately around its action: files and copied directories use
content state; linked directories use identity plus the final full proof.

Before the active record/finalized backup commits, the existing complete
frozen-input comparison runs once against commit states. Thus unrelated effect
count cannot multiply deep scans, while any late directory drift still causes
rollback.

Removing CAS, validating only modification times, or relying only on the App
preflight was rejected because each loses an existing race or recovery proof.

### Decision 4: One App-effect plan owns preserve versus rebind

After resolving the canonical official target and observing the existing
Desktop binding, the transaction derives one internal App-effect plan. The
`preserve` variant is available only when the current active App identity,
LaunchAgent payload, GUI environment, and any running Desktop/app-server owner
are compatible with the canonical official binding. It records the official
App identity in the new active selection but produces no App-owned effect. The
`rebind` variant retains the existing wrapper/LaunchAgent/`launchctl` journal.

Only `rebind` invokes the fail-closed stopped-App process seam. Running or
unreadable App state fails before store creation and backup; a stopped result
allows the existing recoverable effects. Isolated tests inject both the binding
observation and process adapter. Preview reports the derived variant but never
observes or mutates processes.

A public `--skip-app-cli`-style flag was rejected because callers should not
override safety or encode the plan themselves. Treating every matching path as
healthy without checking the live owner was rejected because an existing App
process may still belong to another generation. Retaining a blanket stop was
rejected because it makes a no-op App surface operationally expensive.

### Decision 5: Split excludes Desktop global-state projection

The canonical `.codex-global-state.json` carries UI, workspace, permission,
thread, and other App-owned state; it is not part of Plugin/Skill capability
configuration required by the internal CLI. The supported split therefore does
not freeze, merge, back up, or write either the official source or internal
target global-state file. Synchronized same-profile switches retain their
existing behavior, so this is a selection-scoped plan change rather than a
field-ownership migration.

App-originated `marketplaces.*`, `plugins.*`, and `skills.config` continue
through the existing stable generation/CAS module, which already materializes
only the internal cache while the official App runs. Generic allowlisted
support still uses its source guards and final CAS. Concurrent source changes
therefore retry/fail or roll back without writing the App.

### Decision 6: Progress is derived from the immutable shared plan

The transaction prints one deterministic `current/total/name` line immediately
before each selected shared-support effect. The total and order come from the
frozen allowlisted source tuple, so progress cannot enumerate unknown runtime
state and contains no file contents. Later phases retain their existing output.

## Completion Contract

- Public transaction tests are RED then GREEN for allowlisted selection,
  unknown/temp exclusion, ignored-target preservation, counted progress,
  running healthy-App preservation, required-rebind stopped proof, preview,
  and late-App rollback.
- A deterministic filesystem adapter proves recursive capture work for an
  unchanged directory is constant with respect to unrelated effect count.
- Current-source drift before/during copy and final frozen-input drift retain
  exact rollback behavior and no partial active selection.
- Existing rules/skills sharing, synchronized-switch Desktop settings
  projection, split/default switching, transaction recovery, and shared
  Plugin/Skill suites remain green.
- README and Skill guidance match the conditional App preserve/rebind contract
  and V1 ownership list; packaged source remains self-contained and
  byte-consistent.
- Strict OpenSpec, workflow, static, diff, Plugin Eval, focused, and broad
  verification pass with no live/install/Git/release/archive/cleanup effects.

## Critical Path

Selection/progress/preflight/performance RED -> V1 selector GREEN -> bounded
continuous validation and per-source guards GREEN -> initial stopped-App and
progress GREEN -> App-preserving CLI-only RED/GREEN -> adjacent regression/docs/
package proof -> control-plane completion.

## Incidental Finding Budget

One bounded RED/GREEN guard is available only for a newly observed defect that
blocks an acceptance scenario inside the named Home/transaction/test write
set. Optional sharing candidates or unrelated transaction cleanup are
`DEFER_AND_CONTINUE`; any dependency, live state, deletion, public profile, or
schema expansion is `BLOCKED_AWAITING_HUMAN`.

## Escalation Triggers

Stop before dependency activation, deleting legacy targets, expanding the V1
allowlist, changing Desktop settings fields, changing Plugin/cache ownership,
adding a persisted schema, performing a live switch/App stop/restart, installing
a package, or any Git/release/archive/cleanup effect. The prior
`SPLIT-DEPLOY-APP-RESTART` authority remains separate and unconsumed.

## Capability Slices

1. Selection and observable RED: public tests define V1 ownership, ignored
   preservation, progress, and stopped-App outcomes.
2. Bounded validation RED/GREEN: entry-set metadata and continuous/final modes
   remove effect-multiplied deep work while source/final drift remains safe.
3. Conditional App effects: public transaction tests define preserve versus
   rebind, no-App mutation, no split Desktop settings projection, and retained
   stopped-App rollback.
4. Integration: CLI output, docs, adjacent suites, package identity, and final
   control-plane evidence.

## Execution Ledger

| Slice | Owner | Write set | Evidence | Human Gate |
| --- | --- | --- | --- | --- |
| Planning | main | this OpenSpec change, ledger, DevFlow state | strict OpenSpec/workflow validation | none; approved |
| Selection/preflight RED | main | transaction/profile tests | named RED failures at public seams | none |
| Selector/validation GREEN | main | Home sync, transaction, focused tests | named GREEN plus bounded-work receipt | stop on public/schema expansion |
| App-preserving split RED/GREEN | main | transaction and public transaction/profile tests | running-official preserve, rebind fail-closed, no Desktop effects | stop on supported-pair/schema expansion |
| Progress/docs/integration | main | transaction output, README, SKILL, package-adjacent tests | focused/broad/static/package/Plugin Eval | no install/live effect |
| Completion proof | main | tasks, ledger, state, verification record | fresh exact commands and diff review | archive/Git/live remain gated |

## Continuation Policy

Execution is `auto-until-terminal`. The active OpenSpec task list is the sole
queue; after each GREEN receipt the next dependency-ready item begins. Routine
task, review, and verification boundaries are not gates. Stop only at an
escalation trigger or an acceptance failure requiring plan expansion.

## Generated Artifact Strategy

Focused tests use their existing temporary-directory lifecycle and introduce no
persistent output. A later isolated package build, if needed for source/package
proof, must receive a pre-created Generated Artifact Contract and remain
`RETAIN`; this source implementation does not authorize cleanup.

## Project Refresh Impact

Not applicable: no DevFlow/plugin/skill runtime bytes, project schema, refresh
contract, or migration fixture changes. INC-018's broader project refresh drift
remains deferred and no dependency activation is authorized.

## Project-Directed Implementation Readiness

`implementation_readiness.required: false`. The plan selects no external
provider, model run, credential, network, or paid implementation path.

## SubAgent Strategy

Main-agent-only serialized execution. No delegation is needed; transaction,
tests, docs, and canonical control-plane files overlap and do not provide a
safe disjoint write set.

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_support_allowlist_preserves_ignored_targets \
  TransactionTests.test_shared_support_progress_is_counted_and_ordered \
  TransactionTests.test_split_running_official_app_preserves_desktop_surface \
  TransactionTests.test_split_running_app_fails_when_rebind_is_required \
  TransactionTests.test_split_unreadable_app_inventory_fails_when_rebind_is_required \
  TransactionTests.test_shared_directory_validation_work_is_effect_bounded
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_configuration.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_lifecycle.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_materialization.py
python3.12 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
openspec validate optimize-shared-switch-transaction --strict --no-interactive
openspec validate --all --strict --no-interactive
python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.4.0/scripts/validate_workflow_state.py --repo . --json
git diff --check
```

Run release-counterpart Plugin Eval for `SKILL.md` if operator guidance changes,
and validate an isolated package/source counterpart without installing it.

## Risks / Trade-offs

- [A previously implicit support entry stops updating] -> document the exact V1
  allowlist, preserve both existing paths, and require a new approved migration
  before expansion.
- [Lightweight continuous checks miss a directory edit until commit] -> keep
  current-source guards and one complete final CAS; rollback remains exact.
- [A stale binding is incorrectly preserved] -> require agreement across active
  App identity, canonical target, LaunchAgent/GUI observation, and running owner;
  otherwise derive `rebind` and retain fail-closed process proof.
- [App changes a capability source during CLI-only apply] -> use existing stable
  generation observation, per-source guards, and final CAS; never write the App.
- [Progress claims work not begun] -> derive output from the frozen plan and
  emit only immediately before the corresponding effect.
- [Unrelated dirty work is overwritten] -> use exact patches, inspect scoped
  diffs, and preserve the existing split/parity/provider-migration changes.

Source rollback is the inverse scoped patch. No runtime rollback is required
because this change performs no live switch or installation.

## Review Checklist

- Every delta scenario maps to a named test and task.
- The allowlist is defined once and ignored targets are never removed.
- Deep validation count is independent of unrelated journal effect count.
- Final CAS, current-source drift, route guards, and recovery still fail closed.
- A running healthy official App yields zero App/Desktop effects; a required
  rebind with running/unreadable App state fails before backup.
- Split excludes Desktop global-state projection while synchronized switching
  retains its existing coverage.
- No Plugin/cache/global-state-field ownership silently changes.
- Exact write set excludes unrelated dirty work and all external effects.

## Final Verification

Run the focused RED/GREEN commands, complete adjacent suites, strict active/all
OpenSpec, workflow/static/diff checks, release-counterpart Plugin Eval when
applicable, and read-only scope review. Update tasks, ledger, namespaced state,
and a dedicated verification record, then stop. Do not archive, install,
activate the split, stop/restart the App, commit, push, release, migrate, or
clean retained evidence.
