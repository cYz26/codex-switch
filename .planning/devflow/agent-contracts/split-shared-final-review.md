# Agent Task Contract

## Goal
Perform an independent, read-only code/spec review of the implemented shared App/CLI Plugin and Skill configuration feature, finding concrete correctness, security, transaction, compatibility, and test-coverage defects before the final completion claim.

## Worker ID
`split-shared-final-review`

## Scope
Allowed write set for worker `split-shared-final-review` only: none. All repository writes are forbidden. Review the active OpenSpec and only the implementation/test/docs/distribution paths changed for shared configuration: `scripts/codex_switch_shared_configuration.py`, `scripts/codex_switch_plugins.py`, Runtime Binding/CLI routing, status/Doctor/verify, release-required lists and fixtures, the three new tests, README, and SKILL. Read adjacent primitives as needed. Preserve unrelated WIP. Forbidden: live state/cache/App/backend/network mutation, dependency changes, cleanup, Git writes, release, archive, or any filesystem write.

## Constraints
Read `.agents/skills/code-review/SKILL.md` fully and use its review rubric. Check the real public behavior, not merely test satisfaction: secret-safe projection, generation/baseline conflict rules, semantic no-op, App-running pending behavior, source CAS, target-config rollback, state commit ordering, crash residues, personal-Skill link safety, plugin-cache independence, exact/backend-managed attestation, informational/non-split lifecycle behavior, diagnostic read-only authority, package isolation, and docs accuracy. Distinguish blockers from residual design limitations. Do not recommend unrelated cleanup or broader configuration migration.

## Verification
Use read-only source/diff/test-evidence inspection. You may run focused isolated tests only if they do not mutate repository or live state. Report file/line evidence for every finding and identify a missing regression test for each correctness defect. Run no live plugin/backend command.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED`; changed files (`none`); commands run; complete test logs or validation results; findings ordered by severity with file/line evidence, impact, and recommended repair; OpenSpec/task mismatches; residual risks; unverified areas; and incidental-finding classification.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before any repository write, write-set expansion, live mutation, network/backend/plugin operation, dependency, destructive effect, cleanup, Git write, release, archive, or product/ownership decision beyond the approved OpenSpec. Main owns all repairs and final integration.

## Decision 15 Follow-up Amendment

Re-review the final bytes after the prior P1 orphan-backend finding was promoted
into OpenSpec Decision 15 and repaired. Stable inputs:

- `scripts/codex_switch_transaction.py`: `87a43573d3d98de0b7b1c072b4dfd13ae4fe08fb00b55c3ae40888cc1648b8ad`
- `scripts/codex_switch_shared_configuration.py`: `fcb517de94c2f2fe01fb2e799c92be5da7998dddf78f23d1feb4ac081b98a88e`
- `scripts/codex_switch_plugins.py`: `97542fd391a3cf98a15be89d5821a591684e4f4c6b776351a388ad803ef4560f`
- `scripts/test_codex_shared_configuration.py`: `9f8cbba30d5b1cbb8d972709a5f7df9fb4c96de600ecc0bc4c6c2c797e3112ff`
- `scripts/test_codex_shared_materialization.py`: `d60e6ddf69312ce7dc84c3ebfca76d79eb5c5249f6e53d96207adc7e769cc77d`
- `README.md`: `5979f3540a0b575a311bc1d8dca622c5f179eaf2628ea4cfb57d3403f2015343`
- `SKILL.md`: `20343b465409d604114901afd40e13c4fec1c908652fb0e13495eace4b1ed497`
- design/spec/tasks: `f432f642dbbad8cb8641518dcec67417a1710b37010980e204f5736c296130bb`,
  `ded292550cacb5e626a9932fc589ef733e0576171fa7bc32f04628fff3297c45`,
  `b0080fb60f8e2922e6b0b35a8068778cc51e3c21532be851947e90fffdd1da3f`

Stop and report input drift before reviewing if any hash differs. Reproduce or
otherwise independently verify the original race with a real task-owned
subprocess, not an in-process fake. Require all of the following before
`DONE`/approval:

1. target CAS and official stopped-App proof still precede materializer entry;
2. durable/read-back intent still precedes the first backend subprocess;
3. the exact active store-root lock FD is exposed only inside locked reconcile,
   validated against the Store identity, and inherited by both catalog/list and
   plugin/add subprocesses without entering env/config/state/receipt/log output;
4. parent SIGKILL leaves a surviving backend holding the lock, so early apply
   fails closed before recovery/plan, retains exact intent and target bytes,
   and cannot invoke another materializer;
5. after backend exit, late selector-only, selector-plus-foreign,
   foreign-only, and unclassifiable changes retain Decision 14 behavior;
6. intent/main-journal mutual exclusion and report/plan zero-write behavior
   remain intact;
7. interrupted cache artifacts remain retained and require ordinary current
   attestation, with no cleanup or automatic trust leap;
8. all original secret/path/receipt/cache/App/CAS/backend/catalog/state/
   generation/legacy and distribution review axes remain closed.

Return a single explicit final verdict: `APPROVE` only when no P1/P2 blocker
remains, otherwise `BLOCKED`, with exact file/line evidence. Changed files must
remain `none`.
