# Agent Task Contract

## Goal
Close the final crash-ordering blocker by durably journaling target-config recovery before any external Plugin materializer can write, selectively recovering operation-owned selector activation without erasing foreign edits, and proving an official target is stopped before that first possible write.

## Worker ID
`split-shared-materialization-intent`

## Stable Input Snapshot
- `scripts/codex_switch_shared_configuration.py`: `1d5d70055ff6a8d41027fc73a468881afeb1b91c6070fdc7a4d97906f430cc33`
- `scripts/codex_switch_plugins.py`: `ad5bd9769ffe6e855aa3ad76089d26be8c5c0413319969f5271cc37a22d5962b`
- `scripts/test_codex_shared_configuration.py`: `35d2d5f0d635e718a6ac76ab8a45381aa8c122d3ecde3a60be4916f2aed3db53`
- `scripts/test_codex_shared_materialization.py`: `8cbef96c486fd9310a1f8852c6a43bc6f18cf4f2d46055d7eeb7f61329f3358d`
- OpenSpec design: `5a1b1bbf30224e9ccde0b6e66e1d3ec1ca5ab05cbc62051ed1a9062120698e16`
- OpenSpec spec: `ba15dd9db01541b1d0a273027ab9f2fc1f1128d4eb80225b09ce013bbe390378`
- OpenSpec tasks: `af7464c8716919fcd1cd0d9c46eed10726f37876acb845a124cbd9e3bdb4f571`

Stop before editing if any stable input differs. Tests and OpenSpec are read-only inputs. Main will not edit either allowed production file while this worker runs.

## Scope
Allowed write set for worker `split-shared-materialization-intent` only:
- `scripts/codex_switch_shared_configuration.py`
- `scripts/codex_switch_plugins.py` only if needed to expose/reuse the existing exact selector-delta scrub helper without changing its semantics

Read adjacent config-document, store/IO, transaction lock, runtime process proof, and tests as needed. Forbidden: every other write, live profile/cache/App/backend/network operations, dependencies, cleanup, Git, release, archive, or deletion of retained Plugin cache artifacts.

## Constraints
Read `.agents/skills/diagnosing-bugs/SKILL.md` and `.agents/skills/tdd/SKILL.md` fully. Treat Decision 14 and the named REDs as canonical. Preserve strict receipt attestation, the existing main prepared journal/state commit point, independent caches, retained interrupted cache artifacts, exact native-add synchronous scrub, and read-only report/plan semantics.

Implement systemically:

1. Before any external target materializer call, under the existing store lock, recheck raw target-config CAS. For an official target, perform a fail-closed Desktop/app-server stopped proof before the materializer and retain the existing post-materialization proof.
2. Durably publish private `shared-configuration/pending-materialization.json` before calling the adapter. Bind schema/digest, supported source/target profiles, exact allowed target config path, exact before kind/bytes/mode, and the sorted unique enabled selector set. Create/fsync private directories as already required. It and `pending-commit.json` must never coexist.
3. Normal return or ordinary exception must classify target config before deleting the intent. Reuse the production exact selector-activation scrub semantics rather than a broad whole-file restore.
4. If only operation-owned activation changed, restore exact before bytes/mode (or durably remove an originally absent file), then delete the intent and continue/rethrow as appropriate. If exact operation-owned selector deltas coexist with foreign edits, remove only those deltas using target CAS, preserve foreign bytes/semantics/mode, durably delete the intent, and return `shared_configuration.target_changed_during_plan`.
5. Foreign-only target drift is preserved and blocks. An unsafe/unclassifiable selector change remains fail-closed and must not be broadly overwritten. No state/generation/main journal may publish from a drifted materialization.
6. A `BaseException` crash injection and real child SIGKILL intentionally bypass in-process cleanup and leave the durable intent. Read-only report/plan return `shared_configuration.pending_recovery` with zero writes. The next apply recovers the intent under lock before main-journal recovery, state loading, or new planning.
7. Cache files left by an interrupted materializer remain retained and untrusted; the next ordinary materializer/receipt attestation decides readiness. Do not clean, replace broadly, or infer readiness from the intent.
8. Preserve the new shared-root/generations symlink/permission fail-closed guards and all 64 previously green focused tests.

## Verification
Run and report exact results for:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_official_app_recheck_blocks_before_target_materialization \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_interrupted_materializer_activation_recovers_before_next_plan \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_sigkill_during_materializer_leaves_recoverable_intent \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_interrupted_materializer_preserves_foreign_edit_and_scrubs_selector \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_shared_storage_symlink_ancestors_fail_closed_without_external_write
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_configuration
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_materialization
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_configuration scripts.test_codex_shared_materialization scripts.test_codex_shared_lifecycle
PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile scripts/codex_switch_shared_configuration.py scripts/codex_switch_plugins.py
openspec validate independent-app-cli-profiles --strict --no-interactive
git diff --check -- scripts/codex_switch_shared_configuration.py scripts/codex_switch_plugins.py
```

Do not execute a live backend, Plugin command, App process mutation, or network request.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` and report:
- changed files and final hashes;
- commands run;
- complete test logs or validation results with initial RED and final GREEN counts;
- intent schema/order/recovery mapping;
- proof of the SIGKILL child status and recovery;
- stopped-App call ordering and read-only behavior;
- unverified areas, risk notes, and incidental-finding classification.

## Human Gate
The worker must wait for human review and report `BLOCKED_AWAITING_HUMAN`
before any write-set expansion, public profile/API/persistence expansion beyond
the additive private recovery intent, dependency, weakening of strict
receipt/cache/path/App proof, inability to selectively preserve foreign edits,
shared-file needs outside the named write set, ambiguous deletion, a failing
production contract, unverified severe risk, live/backend/network/process
action, cache cleanup/deletion, Git, install, release, or archive.
