## 1. Explicit Home Support Ownership

- [x] 1.1 Add public transaction RED coverage proving the V1
  `AGENTS.md`/`prompts`/`rules`/`skills` selection, Desktop temp/backup and
  unknown-entry exclusion, and preservation of existing ignored targets.
- [x] 1.2 Replace generic denylist selection with the one versioned allowlist,
  make shared-entry-set capture metadata/identity-only, and pass task 1.1 plus
  existing rules/skills/link-safety tests GREEN without deleting either Home.

## 2. Bounded Validation with Exact Rollback

- [x] 2.1 Add a deterministic public transaction RED that makes recursive
  directory attestation exceed a fixed work budget when unrelated journal
  effects multiply it; retain RED/GREEN cases for current-source and final-CAS
  drift.
- [x] 2.2 Split journal validation into continuous lightweight guards and the
  complete commit proof, bind full source checks to the relevant shared action,
  and pass task 2.1 plus transaction recovery/drift regressions GREEN.

## 3. Stopped-App Preflight and Observable Progress

- [x] 3.1 Add public transaction/CLI RED coverage for running and unreadable App
  inventory before backup, side-effect-free dry-run, late-App CAS rollback, and
  deterministic `current/total/name` shared progress that stops at failure.
- [x] 3.2 Implement the fail-closed live stopped-App probe through an injected
  process-observation seam and emit progress from the frozen shared plan; pass
  task 3.1 GREEN without stopping/restarting processes or weakening rollback.

## 4. Integration and Completion Proof

- [x] 4.1 Run complete transaction/profile/shared-configuration/lifecycle/
  materialization adjacency, update any legacy broad-sharing fixtures to the V1
  contract, and resolve every in-scope regression without expanding ownership.
- [x] 4.2 Update README and SKILL operator guidance, validate the release
  counterpart and isolated source/package identity without installation, and
  record Plugin Eval findings/decisions if the release Skill changes.
- [x] 4.3 Run Python/Bash static checks, strict active/all OpenSpec, DevFlow
  workflow validation, `git diff --check`, and read-only scope review; update
  this task list, `TASK_LEDGER.md`, namespaced state, and a dedicated
  verification record with exact evidence and residual gates.

## 5. Conditional App-Preserving Split

- [x] 5.1 Add public transaction RED coverage proving a running, healthy
  official App yields a successful CLI-only split with unchanged App process,
  LaunchAgent, GUI environment, official Home, and Desktop global-state; prove
  preview reports `preserve`, while a running or unreadable required rebind
  still fails before backup.
- [x] 5.2 Derive one internal `preserve`/`rebind` App-effect plan from the
  attested official target, exclude Desktop global-state projection from split,
  and pass task 5.1 plus late-rebind CAS/rollback and shared capability tests
  GREEN without a new public bypass flag.
- [x] 5.3 Update README/SKILL guidance, rerun complete transaction/profile/
  shared suites, refresh the retained isolated package and release-counterpart
  Plugin Eval, then record strict/static/workflow/diff/review evidence and
  terminal control-plane status without installing or applying a live split.

## Execution Policy

The user's systemic optimization request authorizes the source, test,
documentation, OpenSpec, ledger, namespaced-state, and verification-record
write set named by this change. Execution is `auto-until-terminal` and the next
dependency-ready checkbox continues automatically. It does not authorize App
stop/restart, live split activation, internal binary update, installation,
dependency activation, release, archive, Git effects, migration apply, cleanup,
credential changes, or destructive work. The existing
`SPLIT-DEPLOY-APP-RESTART` authority gate remains separate and unconsumed.
