# Agent Task Contract

## Goal
Independently review the live-acceptance repair for documented engineering
standard violations and material code smells.

## Worker ID
`internal-cli-only-repair-review-standards`

## Scope
Read only the new executable streaming digest, prepared generation validator,
managed runtime-smoke routing, App-action output capture, their named tests,
and matching docs/OpenSpec. Unrelated dirty-worktree changes are excluded.
All repository writes are forbidden. Worker
`internal-cli-only-repair-review-standards` is read-only and has no allowed path
for writes. Also forbidden: every live workstation, cache, install, App,
provider, Git, release, archive, cleanup, network, or destructive effect.

## Constraints
Read-only execution only. Do not modify source, tests, control-plane, cache,
install, App, provider, Git, release, archive, or cleanup state. Review against
`AGENTS.md`, `ENGINEERING_POLICY.md`, `REVIEW_CHECKLIST.md`, plus the Fowler
smell baseline supplied in the worker prompt. Distinguish hard documented
violations from judgement-call smells.

## Verification
Inspect exact repair symbols and hunks for correctness, rollback,
schema-v1 compatibility, bounded streaming, progress streaming, cleanup, and
public-seam coverage. Cite exact files/lines or symbols. The review is complete
only after both production and tests are inspected. Run read-only commands only:
`git diff HEAD -- scripts/codex_switch_runtime_binding.py
scripts/codex_switch_bindings.py scripts/codex_switch_verify.py
scripts/codex-switch scripts/test_codex_shared_lifecycle.py
scripts/test_codex_update_release.py scripts/test_codex_verify.py
scripts/test_codex_profile_switch.py README.md SKILL.md`, plus targeted `rg` and
`sed` inspection. Test execution is not required because this is a read-only
review of already recorded 995/995 main-agent validation.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with a concise findings list.
Include changed files inspected (expected worker changes: none), commands run,
test logs or validation results relied upon, unverified areas, and risk notes.
Explicitly state no findings only after every named seam is checked.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before any write, shared-file need,
scope expansion, dependency change, ambiguous deletion, failing production
contract, severe correctness/security finding, missing standard, live
validation, or external effect. Human review and approval are required before
continuation; the worker never applies a fix.
