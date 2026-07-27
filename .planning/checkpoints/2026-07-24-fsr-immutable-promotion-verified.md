# Fail-Safe Immutable Promotion Verified Checkpoint

Date: 2026-07-24

## Outcome

`fail-safe-update-release` tasks 1.4-1.5 are complete, bringing the change to
6/38. `codex_switch_promotion.py` validates complete candidates, publishes
content-addressed releases, manages relative atomic `current` and `rollback`
references, serializes promotion, records identity-bound state, migrates
legacy directory-based current installs reversibly, requires a structured
health handshake, and restores prior verified references on failure.

## Main Review

Main review added RED/GREEN coverage for macOS canonical path aliases, isolated
Python imports without bytecode mutation, foreign state/ref replacement,
staging ownership, candidate and legacy hard-interruption recovery, active-state
failure rollback, pre-move legacy failure, strict integer schema versions, and
cleanup that never removes a replaced staging tree.

The release-bundle authority now rejects Boolean manifest/workdir schema
versions instead of accepting `true` as integer `1`.

## Verification

- Python 3.9.6: 34/34 update/release tests passed.
- Python 3.12.13: 34/34 update/release tests passed.
- Python AST passed for promotion, bundle, and update/release test modules on
  both interpreters.
- Strict `fail-safe-update-release` OpenSpec validation passed.
- Static caller scan found no installer, runner, wrapper, or production caller
  of the promotion module yet.
- `git diff --check` passed.

An isolated two-release receipt produced two immutable digest directories,
`current -> releases/07cd...daa6`, and
`rollback -> releases/80a8...a730`; health ran once, the prior release remained
addressable, and no temporary promotion path remained.

## Safety Boundary

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or archive action ran. The promotion module is not
wired into installer/self-update adapters; that belongs to tasks 2.1-2.4.

## Next Action

Execute task 2.1 by RED/GREEN: add isolated installer/runner adapter tests for
copy/import/syntax/smoke failures inside Bash conditional contexts, asserting
explicit nonzero status and byte-identical current/rollback references.
