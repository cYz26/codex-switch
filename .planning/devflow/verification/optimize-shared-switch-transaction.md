# Shared Switch Transaction Optimization Verification

## Scope and Boundaries

- Change: `optimize-shared-switch-transaction`
- Canonical execution source:
  `openspec/changes/optimize-shared-switch-transaction/tasks.md`
- Approved effects: scoped source, tests, README/SKILL, OpenSpec, ledger,
  namespaced state, and this evidence record.
- Excluded effects: live profile/App switch, App stop/restart, internal binary
  update, install, dependency activation, migration apply, Git, release,
  archive, cleanup, credentials, and destructive work.
- Pre-existing split/parity/provider-migration worktree changes are preserved.

## Task 1.1 Explicit Home Support Ownership RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_support_allowlist_preserves_ignored_targets
```

Result: 1 test, 1 expected assertion failure. The transaction propagated the
unknown `unknown-support` directory into the internal Home, proving that the
current generic selector still admits every name not present in its denylist.
The fixture first normalized the macOS `/var` versus `/private/var` symlink
comparison; the recorded failure is therefore the intended ownership RED and
not a path-alias artifact. No production source changed before RED.

Next: define the single V1 allowlist, remove recursive child state from the
entry-set metadata capture, and rerun this test plus link-safety adjacency.

## Task 1.2 Explicit Home Support Ownership GREEN

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_support_allowlist_preserves_ignored_targets \
  TransactionTests.test_shared_switch_uses_frozen_support_entry_set
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_shared_support_sync_removes_target_home_symlink_instead_of_copying_loop \
  CodexProfileSwitchTests.test_shared_support_sync_does_not_propagate_source_self_symlink \
  CodexProfileSwitchTests.test_shared_support_directory_copy_skips_nested_target_home_symlinks
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_does_not_create_self_referential_rules_symlink
python3.12 -m py_compile \
  scripts/codex_switch_home_sync.py scripts/codex_switch_transaction.py
git diff --check -- \
  scripts/codex_switch_home_sync.py scripts/codex_switch_transaction.py \
  scripts/test_codex_transaction.py scripts/test_codex_profile_switch.py
```

Result: transaction ownership 2/2, direct link-safety 3/3, real rules switch
1/1, Python compilation, and scoped whitespace validation passed. The V1
allowlist is defined once in `codex_switch_home_sync.py`; source and target
entry-set captures contain only deterministic member role/identity metadata,
while each selected child retains its independent full frozen state. Ignored
source/target paths are neither planned nor removed.

Next: record the deterministic recursive-work-budget RED and retain source/
final-CAS drift coverage.

## Task 2.1 Bounded Validation RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_directory_validation_work_is_effect_bounded \
  TransactionTests.test_switch_rejects_late_shared_source_drift_before_shared_action \
  TransactionTests.test_shared_directory_final_cas_detects_late_drift
```

Result: 3 tests ran; the work-budget test produced the one expected failure,
with 39 complete captures of the same unchanged 32-skill source directory
against a fixed budget of 8. The current-source and final-CAS drift guards
both passed and rolled back safely, establishing the safety baseline before
changing validation cost.

## Task 2.2 Bounded Validation GREEN

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_support_allowlist_preserves_ignored_targets \
  TransactionTests.test_shared_switch_uses_frozen_support_entry_set \
  TransactionTests.test_shared_directory_validation_work_is_effect_bounded \
  TransactionTests.test_switch_rechecks_frozen_before_states_before_first_mutation \
  TransactionTests.test_switch_rejects_late_shared_source_drift_before_shared_action \
  TransactionTests.test_shared_directory_final_cas_detects_late_drift \
  TransactionTests.test_switch_rechecks_unchanged_required_bindings_at_commit \
  TransactionTests.test_codex_bin_deletion_at_last_preterminal_intent_rolls_back \
  TransactionTests.test_split_selected_manifest_drift_preserves_state_per_journal_contract
```

Result: 9/9 passed. Repeated effect checkpoints now fully validate files,
symlinks, missing paths, composite allowlisted membership, and every path
identity while using identity-only checks for unrelated directory contents.
Each current shared source receives full content checks immediately before and
after its action. One complete final CAS remains after the active write and
before backup commit. The deep-directory public budget is now at most 8 rather
than the prior 39, while pre-mutation, current-source, binding, split-manifest,
and final directory drift all retain exact rollback behavior.

Next: record stopped-App and deterministic progress RED at the public
transaction boundary.

## Task 3.1 Stopped-App and Progress RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_split_running_app_fails_before_backup \
  TransactionTests.test_split_unreadable_app_inventory_fails_before_backup \
  TransactionTests.test_split_dry_run_reports_stopped_app_requirement_without_observing_processes \
  TransactionTests.test_shared_support_progress_is_counted_and_ordered \
  TransactionTests.test_split_late_app_state_drift_rolls_back_after_stopped_preflight
```

Result: 5 tests ran with 4 expected failures and 1 passing safety baseline.
Running and unreadable App probes were ignored, split preview omitted the
stopped-App requirement, and no per-entry progress was emitted. The existing
late Desktop global-state CAS already rolled the split back, establishing the
post-preflight race baseline.

## Task 3.2 Stopped-App and Progress GREEN

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_shared_support_allowlist_preserves_ignored_targets \
  TransactionTests.test_split_running_app_fails_before_backup \
  TransactionTests.test_split_unreadable_app_inventory_fails_before_backup \
  TransactionTests.test_split_live_process_probe_fails_closed_before_backup \
  TransactionTests.test_split_dry_run_reports_stopped_app_requirement_without_observing_processes \
  TransactionTests.test_shared_support_progress_is_counted_and_ordered \
  TransactionTests.test_split_late_app_state_drift_rolls_back_after_stopped_preflight
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_split_selected_manifest_drift_preserves_state_per_journal_contract \
  TransactionTests.test_split_official_desktop_failure_rolls_back_both_surfaces
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_split_switch_preview_names_cli_and_app_profiles \
  CodexProfileSwitchTests.test_split_switch_uses_internal_cli_and_official_app_atomically
python3.12 -m py_compile \
  scripts/codex_switch_home_sync.py scripts/codex_switch_transaction.py
git diff --check -- \
  scripts/codex_switch_home_sync.py scripts/codex_switch_transaction.py \
  scripts/test_codex_transaction.py scripts/test_codex_profile_switch.py
```

Result: new public matrix 7/7, adjacent split transaction 2/2, adjacent split
profile 2/2, Python compilation, and scoped whitespace validation passed. A
supported live split now probes before planning/backup through either the
production process inventory or an isolated injected seam. Running or
unprovable state raises a stable stopped-App instruction with zero backup or
journal; dry-run remains process-read-free. Progress is frozen-plan-derived:
success reports exactly `1/4` through `4/4`, while an injected rules failure
reports only `1/4` through the failing `3/4` effect. A post-preflight App write
still triggers CAS rollback.

Next: run the complete transaction/profile/shared adjacency and migrate only
legacy fixtures whose purpose was independent of broad unknown sharing.

## Task 4.1 Complete Adjacent Regression

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_configuration.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_lifecycle.py
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_shared_materialization.py
```

Result: transaction 250/250, profile 219/219, shared configuration 45/45,
shared lifecycle 8/8, and shared materialization 19/19 passed (541 total).
The first broad runs identified only legacy fixtures whose subject names no
longer belong to V1: `support-file`, `support-directory`, `visualizations`,
`stable-support`, `pets`, unsafe `*-share` aliases, an unknown socket, and an
unknown entry-set insertion. Effect/recovery fixtures now use an allowlisted
name; unknown socket and `pets` cases now assert preservation plus no
propagation; allowed symlink fixtures retain safe-external and unsafe relative,
dangling, source-Home, target-Home, and self/loop coverage. The focused repair
set passed before both full suites were rerun. No production ownership was
broadened to satisfy a legacy fixture.

Next: update README/SKILL operator guidance and validate the isolated release
counterpart without installation.

## Task 4.2 Docs, Package, and Plugin Eval

The README and Skill now state the exact V1 generic Home allowlist, ignored
target preservation, stopped-App split contract, `--keep-version` safety
boundary, dry-run availability, counted progress, final CAS, and separate
Plugin/Skill desired-state versus cache ownership.

Generated Artifact Contract
`SHARED-SWITCH-OPT-20260810T162102+0800` was sealed while its physical root was
absent. The owner package command completed in that exact root. Final identity:

```text
version: 0.1.13
archive SHA-256: 1314f7c83de6d77c9487f69b44e5ccc1dec698feba572b3f959e2acfea630751
manifest SHA-256: 2a41b93478d3f1489d574778e6e7f154aa8ffd479a0dc6e2ea0e7e33d364fa03
payload SHA-256: bb30440a284d6e120a48de19c42f3995795220085d2f8c7a1c6fd8b8bda829d3
required paths: 22
files: 71
directories: 5
source/package key-file identity: passed
package-local transaction focus: 8/8
package-local profile focus: 4/4
```

Release-counterpart Plugin Eval reports 58/100, grade D, 2 fail / 3 warn / 2
info. Compressing the new Skill guidance reduced active budget from 3,878 to
3,810 tokens. The remaining static budget, top-level README, historical Python
complexity, seven long lines, and missing coverage-artifact findings are the
existing INC-012 package-architecture classes. They remain
`DEFER_AND_CONTINUE`: resolving them requires a separate benchmark-backed
Skill/package change and is not necessary to satisfy this transaction repair's
runtime completion contract. Full details and the retained no-install boundary
are in
`.planning/devflow/deployments/20260810T162102+0800/verification.md`.

Next: run final static, OpenSpec, workflow, diff, and read-only scope review;
then update terminal control-plane status without archive, Git, install, or
live effects.

## Task 4.3 Final Control-Plane Proof

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 -c \
  'from pathlib import Path; files=sorted(Path("scripts").glob("*.py")); [compile(p.read_bytes(), str(p), "exec") for p in files]; print(f"compiled={len(files)}")'
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
bash -n scripts/package-release.sh
python3.12 -m json.tool evals/evals.json >/dev/null
openspec validate optimize-shared-switch-transaction --strict --no-interactive
openspec validate --all --strict --no-interactive
python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.4.0/scripts/validate_workflow_state.py --repo . --json
git diff --check
```

Result: 61 Python sources compiled in memory without generating new bytecode;
all five Shell entry points and the eval JSON passed syntax validation. The
active change is strictly valid, and repository-wide strict OpenSpec is 21/21.
DevFlow workflow validation reports `ok=true`, zero issues, and only the
pre-existing INC-018 Project-Directed Implementation Readiness guidance
warning. `git diff --check` is clean.

The repository's read-only local-reference reminder command was checked, but
`dev/scripts/codex_auto_update_plugins_skills.py` is not present in this
repository; no cache refresh, project migration, or reference mutation was
attempted. The sealed no-install package identity and package-local tests from
task 4.2 remain the release-counterpart proof.

The final review used the project `code-review` standards/spec separation but
could not use its commit-range worker procedure because this task is an
uncommitted, mixed-WIP worktree with no user-supplied fixed point. A scoped
main-agent review instead compared the exact task files against `AGENTS.md`,
`ENGINEERING_POLICY.md`, and this change's design/spec. Standards findings: 0.
Spec findings: 0. The review confirmed exact allowlist ownership, ignored
target preservation, independent Plugin caches, source guards around each
shared action, one final complete CAS, stopped-App failure before backup,
side-effect-free preview, deterministic failure-bounded progress, and retained
rollback coverage.

Terminal source outcome: `READY_FOR_EXTERNAL_EFFECT`. All 9/9 change tasks are
complete. No live split, App stop/restart, internal update, installation,
dependency activation, migration, Git, release, archive, cleanup, credential,
or destructive effect occurred. `SPLIT-DEPLOY-APP-RESTART` remains a separate,
unconsumed authority gate.

## Task 5 Reopen: Conditional App-Preserving Split

The user confirmed that a split should not require App shutdown when the App
is already healthy on the official binding and the requested work is only
internal CLI capability synchronization. The existing OpenSpec proposal,
delta spec, design, and tasks were reconciled in place because the change is
unarchived and the earlier optimized source is not installed. Strict active
and repository-wide OpenSpec validation pass 21/21 after the revision.

The revised contract derives one `preserve` or `rebind` App-effect plan.
`preserve` produces no LaunchAgent, GUI environment, App wrapper, official
Home, process, or Desktop global-state effect and permits a running healthy
official App. `rebind` retains the stopped-App and rollback contract. Split no
longer consumes Desktop settings projection; generationed Plugin/Skill
App-to-internal reconciliation remains the capability authority.

The selection-scoped dependency audit reports aggregate
`status=missing_required`/`workflowReady=false` from the pre-existing INC-018
project-local DevFlow mirror drift. Its methodology evidence independently
reports required `tdd` `ready=true`, with empty missing/nonlocal/drifted/
unexpected sets and verified vendored source; OpenSpec 1.7 is also verified.
No dependency activation or migration was applied. Task 5.1 public RED is the
next executable item.

### Task 5.1 RED Evidence

Public transaction coverage now fixes the conditional App-effect contract at
the existing `execute_transaction` seam. The healthy official-App apply case
expects a committed internal-CLI/official-App split with the App process probe
observed once, no Desktop adapter mutation, no LaunchAgent or official-Home
change, no Desktop global-state source/target in the backup, and no App-owned
journal effect. The preview case expects `App action: preserve`, omits the
stopped-App instruction, and proves no process, backup, or mutation effect.
The two stale-binding cases require Desktop observation before the existing
running/unreadable stopped proof and retain the pre-backup failure boundary.

Expected RED results:

```text
test_split_running_official_app_preserves_desktop_surface
  ERROR: Supported split requires you to fully quit ChatGPT/Codex App...
test_split_preview_reports_preserve_without_stopped_app_probe
  FAIL: `App action: preserve` absent; preview still reports the blanket
        stopped-App requirement and Desktop/global-state mutation plan
test_split_running_app_fails_when_rebind_is_required
test_split_unreadable_app_inventory_fails_when_rebind_is_required
  FAIL: expected Desktop observe:getenv/observe:service before stopped proof,
        observed no Desktop binding observation
```

The first attempted dotted `unittest` invocation from the repository root was
an invocation-only error because the project scripts directory was not on
`PYTHONPATH`; rerunning from `scripts/` produced the two intended RED failures
above. No product outcome is inferred from that invocation error.

Next: implement task 5.2 from these public failures without adding a CLI flag.

### Task 5.2 GREEN Evidence

The transaction now derives one private App-effect plan after resolving the
official target and observing the active selection, exact LaunchAgent payload,
GUI environment, service state, and running Desktop/app-server owner. Preview
uses the static evidence only and reports `preserve` or `rebind`. Apply accepts
`preserve` only when the live owner is compatible; otherwise a running or
unreadable required rebind retains the original pre-backup failure. No public
bypass or CLI flag was added.

`preserve` removes the App wrapper, LaunchAgent, launchctl adapter, Desktop
journal recovery, official Home, and Desktop global-state projection from the
mutation write set. The existing LaunchAgent remains recorded in the explicit
active selection. Every split now excludes both global-state source and target
from frozen, backup, preview, and mutation plans; synchronized same-profile
switches retain their prior settings projection.

Fresh results:

```text
conditional App-effect/public owner tests: 10/10
complete transaction suite: 252/252
shared configuration: 45/45
shared lifecycle: 8/8
shared materialization: 19/19
```

The first complete profile run exposed a real rebind-CAS omission: the current
LaunchAgent was frozen, but its canonical planned payload was not registered as
the commit state, so four valid rebind paths rolled back at final CAS. Adding
that exact payload to the rebind commit plan made all four named failures GREEN
and retained the late-drift rollback test. The healthy owner and mismatched
owner cases also pass through the production process-classification seam, not
only the injected stopped-process seam.

The attempted adjacent-suite command named a nonexistent
`test_codex_internal_materialization.py`; the repository's actual
`test_codex_shared_materialization.py` then passed 19/19. This was a command
invocation error, not a product failure.

Next: task 5.3 docs, fresh complete profile/transaction/adjacent verification,
new isolated retained package, release-counterpart Plugin Eval, and terminal
control-plane proof.

### Task 5.3 Terminal Verification

README and SKILL now describe the exact conditional rule: preview reports an
App action of `preserve` or `rebind`; a healthy canonical official App may
remain running for `preserve`; only `rebind` requires the stopped-App proof.
Both documents also state that split excludes Desktop global state while
Plugin/Skill desired-state reconciliation and independent caches remain
unchanged.

Fresh source results after the final implementation and documentation bytes:

```text
transaction:             254/254
profile switch:          219/219
shared configuration:     45/45
shared lifecycle:           8/8
shared materialization:    19/19
total:                    545/545
```

The final static matrix compiled 61 Python source files in memory, passed all
five Bash entry-point syntax checks, validated `evals/evals.json`, passed
`git diff --check`, strictly validated the active change and repository-wide
OpenSpec 21/21, and produced DevFlow workflow `ok=true` with zero issues. The
only workflow warning is the pre-existing INC-018 missing Project-Directed
Implementation Readiness guidance. The repository-local reference reminder
script `dev/scripts/codex_auto_update_plugins_skills.py` remains absent, so no
cache refresh or project migration was attempted.

Generated Artifact Contract
`SHARED-SWITCH-OPT-APP-PRESERVE-20260810T171250+0800` was sealed while both
its durable and physical roots were absent. The retained, uninstalled package
is version 0.1.13 with archive SHA-256
`d6fd3c95cdeb1a113809a195276f071841d2b70153ded4db24b1aa3c9bcbfc83`,
manifest SHA-256
`9268efa71afe254be804bc7c8bf672d709c2ff908e8c1f9b79c12b6839d595b8`,
and payload SHA-256
`d62dd967bb23c60851088c3f4dc621c1273a5ea648130036071551c29001252e`.
It contains 22 required paths, 72 files, and 5 directories. Key source/package
identity passed, as did package-local transaction 10/10 and profile 4/4. The
full receipt is
`.planning/devflow/deployments/20260810T171250+0800/verification.md`.

Release-counterpart Plugin Eval completed in JSON and Markdown forms: 58/100,
grade D, 2 fail / 3 warn / 2 info. Its 43 trigger, 3,837 invoke, 3,880 active,
and 1,038,218 deferred static token estimates remain the existing INC-012
package-architecture class; top-level README placement, historical Python
complexity, seven long lines, and unavailable coverage artifacts also remain.
No new finding class was introduced. Fixing these requires a separately scoped
observed-usage benchmark and package refactor, so they remain
`DEFER_AND_CONTINUE` rather than expanding this behavior change.

Final review was scoped to this OpenSpec and its exact implementation files
because the project `code-review` skill requires a user-supplied fixed Git
point and the current mixed-WIP worktree has none. Standards review found zero
hard violations: planning preceded implementation, public TDD RED/GREEN and
fresh proof are durable, no dependency or public bypass was added, and all
external effects stayed excluded. Spec review found zero missing, wrong, or
extra behaviors across healthy-running preserve, owner mismatch, required
rebind running/unreadable failure, preserve/rebind preview, split global-state
exclusion, stopped rebind, late drift rollback, and synchronized-switch
compatibility. The single private App-effect plan avoids a second public
switching interface; the two existing preview-builder branches intentionally
render the same plan fields and introduce no new ownership path.

Terminal source outcome: `READY_FOR_EXTERNAL_EFFECT`. All 12/12 change tasks
are complete. The current installed payload was not changed by this task; live
installation and activation remain separate authority. After installation, a
fresh split preview decides the operational path: `preserve` does not require
quitting the App, while `rebind` still does. No install, live split, App
stop/restart, internal update, dependency/migration, Git, release, archive,
cleanup, credential, provider, or destructive effect occurred.

Final live read-only confirmation used the new source with self/internal update
retention, dry-run, and all repair/verify/Doctor/status post-steps disabled.
Against the currently running official ChatGPT and app-server it exited zero
with `App action: preserve`, no stopped-App line, no LaunchAgent or Desktop
global-state backup target, and no App/Desktop mutation action. The separate
installed `codex-switch --skip-self-update status` confirms active CLI/App,
GUI environment, LaunchAgent, bundled CLI, ChatGPT pid, and app-server all own
the same official path. It also reports the existing unrelated shell PATH
alignment mismatch and remediation; no remediation was applied. Dry-run made
no switch or live write. The immutable installed `current` remains version
0.1.13 payload
`b88326ff747278543b94176b00816f8c9b4e692afbf31fee5a490da107cff49d`;
the new verified package was not promoted.

INC-019 records one invocation-only residue: an early `py_compile` command
generated or refreshed exactly
`scripts/__pycache__/codex_switch_transaction.cpython-312.pyc` and
`scripts/__pycache__/test_codex_transaction.cpython-312.pyc` at
2026-08-10T17:00:20+08:00. They are ignored and absent from the package, but
the pre-existing directory had no sealed Generated Artifact Contract, so
retrospective cleanup authority cannot be proven. They are retained; no
cleanup was attempted.
