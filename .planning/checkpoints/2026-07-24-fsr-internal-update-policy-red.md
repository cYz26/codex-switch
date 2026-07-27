# Fail-Safe Internal Update Policy RED Checkpoint

## Status

`fail-safe-update-release` task 3.1 is complete at 11/38. Task 3.2 is the next
dependency-ready item.

## Public Seam

`decide_internal_update(...)` returns a structured decision for equal, newer,
older, blocked, invalid, and prerelease version cases.

## RED Evidence

- Python 3.12.13: 8/8 expected failures.
- System Python 3.9.6: 8/8 expected failures.
- Every failure is caused by the deliberate absence of
  `scripts/codex_switch_update_policy.py`.
- No fixture, import, or legacy shell behavior obscures the policy boundary.

## Scope

No production code, shell adapter, live update, install/self-update,
profile/App switch, plugin mutation, network release, commit, push, tag, or
archive action ran.

## Next Action

Create the Python 3.9-compatible structured update policy, implement ordered
SemVer decisions, allow downgrade only for an explicitly blocked current with
a valid fallback, and make all eight task 3.1 contracts GREEN.
