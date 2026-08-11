# Agent Task Contract

## Goal
Independently compare the live-acceptance repair with the reopened
`internal-cli-only-runtime` proposal, design, spec, and tasks.

## Worker ID
`internal-cli-only-repair-review-spec`

## Scope
Read only the repair requirements, production seams, and named tests for tasks
6.2-6.4. Report missing or partial requirements, incorrect behavior, and scope
creep. Unrelated dirty-worktree changes and historical completed slices are
excluded. All repository writes are forbidden. Worker
`internal-cli-only-repair-review-spec` is read-only and has no allowed write
path. Also forbidden: every live workstation, cache, install, App, provider,
Git, release, archive, cleanup, network, or destructive effect.

## Constraints
Read-only execution only. Do not modify source, tests, control-plane, cache,
install, App, provider, Git, release, archive, or cleanup state. Preserve the
approved internal-CLI/official-App boundary and schema-v1 compatibility.

## Verification
Trace each repair scenario to current code and tests: valid backend above 16
MiB, over-bound failure, stable streaming identity, promotion rollback,
managed-shim final smoke, and preserve/rebind guidance. Cite exact files/lines
or symbols and check for unrequested behavior. Run read-only commands only:
`openspec show internal-cli-only-runtime --json`, targeted `rg`/`sed`, and
`git diff HEAD -- scripts/codex_switch_runtime_binding.py
scripts/codex_switch_bindings.py scripts/codex_switch_verify.py
scripts/codex-switch scripts/test_codex_shared_lifecycle.py
scripts/test_codex_update_release.py scripts/test_codex_verify.py
scripts/test_codex_profile_switch.py README.md SKILL.md`. Test execution is not
required because this is a read-only review of already recorded 995/995
main-agent validation.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with a concise findings list.
Include changed files inspected (expected worker changes: none), commands run,
test logs or validation results relied upon, unverified areas, and risk notes.
Explicitly state whether every repair scenario is covered.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before any write, shared-file need,
scope expansion, dependency change, ambiguous deletion, failing production
contract, severe correctness/security finding, missing spec authority, live
validation, or external effect. Human review and approval are required before
continuation; the worker never applies a fix.
