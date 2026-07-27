# Fail-Safe Profile Suite Verified

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `7.3`

## Result

The complete profile suite passes after aligning duplicate release fixtures
with the approved fail-safe release contracts:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
```

Result: `193/193` passed in `183.009s`.

The preceding complete update/release result remains `107/107` passed in
`191.044s`. Together they cover immutable promotion/rollback, ordered internal
updates, fail-closed plugin catalogs, bounded verification, exact commit-tree
release authority, package-before-ref ordering, reconciliation, and
reconcile-then-prepare.

## Test Contract Repairs

- A complete published latest tag now expects `release_action=none`, no
  mutation target, and retains the observed tag in `latest_tag`.
- Automatic workflow assertions use `prepare_required` and isolated
  reconciliation/pending dist roots.
- Manual workflow assertions use trusted tooling staged under `RUNNER_TEMP`.
- Commit-binding fixtures include the required release root and prove
  untracked or ignored files under the release directory are rejected.
- Internal update tests skip unrelated plugin repair when their fake Codex does
  not provide a verified plugin catalog; the dedicated plugin-repair failure
  compatibility test remains active.

No production behavior was relaxed. No live install, profile/App switch,
plugin mutation, network release, commit, push, tag, or archive action ran.

Canonical progress is 33/35 implementation tasks and 39/42 OpenSpec
checkboxes. Task `7.4` is next.
