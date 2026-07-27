# Agent Task Contract

## Goal
Repair the independently reviewed capture safety and evidence defects before ownership transfers to the switch slice: prevent cloned managed symlinks from escaping the stage, freeze and attest required source files, harden the profiles workspace and rollback attestations, recover independently of a new source, make committed cleanup status truthful, preserve the causal CLI error, and durably order the journal/directory exchange.

## Worker ID
`transaction-capture-review-fixes`

## Scope
Allowed write set for worker `transaction-capture-review-fixes` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_capture.py`

Read-only inputs include `openspec/changes/transactional-profile-state/`, the completed capture implementation/reviews, direct capture callers, and current transaction tests. Forbidden: do not edit any other path. You are not alone in the repository: preserve all unrelated/main-agent changes, do not revert them, and adapt to the current shared worktree.

## Constraints
Follow strict RED-to-GREEN cycles for every repair. Before copying new managed files, remove cloned `config.toml`, `auth.json`, and `manifest.json` with lstat-based stage-local operations so an old managed symlink can never write outside the stage; assert each resulting managed payload has the intended regular-file kind and attested bytes. Freeze source config/auth presence and file attestations at preflight, validate the staged config, and reject any source disappearance or content/kind drift; `allow_missing_auth=False` can never commit without auth, while an initially absent allowed auth remains intentionally absent even if it later appears.

For first capture, replace lock-before `ensure_private_dir()` with one atomic leaf `mkdir` attempt and no lock-before chmod or parent creation; all other store layout changes occur under the directory-inode lock. Reject an existing `profiles_dir` symlink/non-directory before any follow-through, pin its opened inode for capture, and revalidate the same canonical parent identity around artifact writes, rename, cleanup, and rollback. This guard must stop static outward symlinks and injected parent replacement; record the unavoidable residual that non-cooperating hostile mutation cannot be made mathematically race-free without a complete dirfd architecture. Recovery of a prepared journal must run before validation of the next capture source, so a deliberately invalid next source can prove the old profile is restored independently. Require exact integer journal schema types.

Before rollback moves or deletes `previous`, destination, or stage, re-attest each artifact against the durable journal/current transaction state; never install an unverified replacement as the live profile. Put staged-state attestation itself inside cleanup protection so failure cannot leave an unjournaled stage. After a committed journal exists, cleanup failure must return a truthful `committed` receipt while retaining the committed journal/recovery material; it must not throw a failure after the new profile is permanent. Keep the successful public CLI output byte-for-byte unchanged. For rolled-back or rollback-failed receipts, the public wrapper error must retain the causal apply/rollback details rather than only `rollback completed`.

Durably order capture by fsyncing staged regular-file data/directories before the prepared journal, fsyncing the journal and its parent, and fsyncing the parent after each directory rename/removal. Add a system-boundary seam only as needed for deterministic tests. Use Python 3 standard library only and `apply_patch` for edits. Do not broaden arbitrary-profile behavior, modify `cmd_init`'s pre-existing non-capture initialization sequence, implement switch/Desktop work, touch live state, run network/install/release operations, or use Git mutation.

## Verification
Add focused RED tests for: cloned managed symlink escape; required-auth disappearance after preflight; first-capture busy race causing no lock-before chmod; outward `profiles_dir` symlink; replaced `previous` rejected before rollback install; staged-state attestation failure removes unjournaled stage; prepared-journal recovery restores old state before an invalid retry source is rejected; committed cleanup failure returns committed with durable journal and unchanged success output; causal public rollback error; exact integer journal schema; and fsync ordering around prepared journal and both renames. Run each test RED alone, implement the smallest systemic seam, and rerun it GREEN. Then run the entire transaction suite on Python 3.9 and 3.12, the full legacy profile-switch suite on Python 3.12, dual-version compile checks, strict OpenSpec validation, and `git diff --check`.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; ordered RED/GREEN commands/results; test names; managed-symlink external sentinel proof; config/auth attestation matrix; root/profiles parent guard evidence; recovery state proof before invalid-source failure; rollback artifact re-attestation proof; committed-cleanup receipt/journal proof; CLI error text; durability event order; complete validation results; diff stat; residual risks; unverified areas; and incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`. Do not mark OpenSpec tasks or write ledger/state/evidence files; main owns those after independent review.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing successful CLI output/flags, adopting a full dirfd rewrite, changing custom-profile behavior, expanding the write set, deleting ambiguous artifacts, touching live workstation/App state, adding a dependency, bypassing a failing test, or changing `cmd_init` initialization semantics beyond the approved capture call. If a required change lies outside the exclusive write set, report the exact seam and proposed path instead of editing it.
