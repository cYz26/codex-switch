# Fail-Safe Obsolete Path Cleanup Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `7.1`
Implementation progress: `31/35`
OpenSpec checkbox progress: `35/42`

## Result

Production scans prove the retired fail-open implementations are absent:

- mutable `current.self-update` / `current.previous` replacement;
- internal update by raw current/latest inequality;
- catalog parse failure collapsing to an empty selector set;
- app-server success inferred by scanning raw stdout lines;
- tag/ref creation before packaging or `--clobber` release upload.

No production deletion was needed. Remaining `current`/`backup` renames belong
to the reversible legacy migration in `codex_switch_promotion.py` and remain
covered by interruption/rollback tests.

## Verification

- cleanup plus workflow static group: 7/7 on Python 3.12.13;
- cleanup plus workflow static group: 7/7 on system Python 3.9.6;
- exact `rg` zero-match scan: passed;
- strict FSR OpenSpec, dual-runtime test compile, focused diff check: passed.

## Next Action

Run the complete update/release suite for task 7.2.
