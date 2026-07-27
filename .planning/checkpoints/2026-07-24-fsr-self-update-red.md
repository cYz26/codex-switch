# Fail-Safe Self-Update RED Checkpoint

## Status

`fail-safe-update-release` task 2.3 is complete at 9/38. Task 2.4 is the next
dependency-ready item.

## RED Contract

Six isolated public-wrapper tests cover:

- invalid self-update candidate structure;
- expected-version mismatch;
- structured handshake field mismatch;
- bounded handshake timeout;
- concurrent promotion after the primary receipt;
- nonzero user-command replay exactly once.

Python 3.12.13 and system Python 3.9.6 each failed all six cases for the
expected reason: legacy self-update replaced immutable `current` with a mutable
directory instead of using promotion, rollback, and receipt-root replay.

The Python 3.9 test process used Python 3.12 as the CLI runtime because the
current wrapper contract requires Python 3.11+ with `tomllib`. This is a
test-fixture boundary, not a production change.

## Static Validation

- Python 3.12 AST: passed.
- Python 3.9 AST: passed.
- Test-file whitespace check: passed.

## Scope

Only tests and control-plane evidence changed. No production code, live
install/self-update, profile/App switch, plugin mutation, network release,
commit, push, tag, or archive action ran.

## Next Action

Implement task 2.4 in `scripts/codex-switch`: use the trusted immutable
promotion path, preserve prior refs on candidate or handshake failure, and
execute the original command once from the promoted receipt root even when a
concurrent promotion changes `current`.
