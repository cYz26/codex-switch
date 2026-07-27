# Agent Task Contract

## Goal
Complete `fail-safe-update-release` tasks 1.4 and 1.5 by strict TDD: define and
implement one Python 3.9-compatible immutable promotion module that validates a
release-bundle candidate, stores it under `releases/<digest>`, atomically manages
`current` and `rollback`, recovers an interrupted legacy-current migration, and
rolls back when the structured health handshake fails.

## Worker ID
`fail-safe-immutable-promotion`

## Stable Input Snapshot
- `scripts/test_codex_update_release.py`:
  `bbb4b64eea78f874e9d723647c5d6fe848df3fd65668cb3ee9a792369a5a1b55`
- read-only bundle module:
  `eaba9e7e3d0b2a447057e3a084d59ae7b78408ff7827f88ac6db2dd676e8f671`
- read-only transaction reference:
  `9591ee92d8e8f9b8bb3d5e5a5a3e0fa0ca5b1cc42e445ed95955425f313f00f9`
- canonical OpenSpec tasks:
  `02fa9a7f590822f35b006001b30c735c6267caf8a75a9e33505aa5c162706797`
- canonical design:
  `32112285bf93fde1faf59f68697dd39667a228cc0be79bbac33fe00d5800248a`
- canonical delta spec:
  `0e7ab1c4c00a31eeaa51802c72ef406ccda1b1ca0eb63277e3aaec9afacd1adf`

Stop before editing if any listed hash differs. OpenSpec, control-plane,
installer/runner/wrapper adapters, the bundle module, and the transaction module
are main-owned and read-only.

## Scope
Allowed write set for worker `fail-safe-immutable-promotion` only:
- `scripts/codex_switch_promotion.py`
- `scripts/test_codex_update_release.py`

Read-only inputs include the approved `fail-safe-update-release` artifacts,
`scripts/codex_switch_release_bundle.py`, and the lock/recovery patterns in
`scripts/codex_switch_transaction.py`. Forbidden: every other path, especially
`install.sh`, `run.sh`, `scripts/codex-switch`, OpenSpec, `.planning/`,
`TASK_LEDGER.md`, installed release trees, live profile stores, App bundles,
plugin caches, rollout/session files, network URLs, Git staging/commit/push/tag/
release, live install/update/profile-switch commands, or dependency changes.
The worker is not alone in the worktree; preserve all unrelated edits and make
only narrow changes inside the two listed files.

## Constraints
- Follow strict RED/GREEN order. The initial promotion tests must fail for the
  expected missing contract before production implementation is added.
- Use only the Python 3.9 standard library and existing project modules.
- Keep all test roots, processes, commands, locks, and state in temporary
  directories with bounded waits and deterministic cleanup.
- Preserve bundle validation as the candidate authority; do not weaken or copy
  its manifest/digest policy into a divergent implementation.
- Never infer success from `set -e`, a path existing, or a subprocess returning
  output. Every mutation and handshake postcondition is explicit.
- A failure may retain classified candidate/state evidence, but must not delete
  or overwrite an unclassified path or the last runnable current release.

## Required Internal Contract
Keep the approved design surface recognizable:

```python
class PromotionError(RuntimeError):
    reason: str

@dataclass(frozen=True)
class PromotionCandidate:
    root: Path
    version: str
    digest: str

@dataclass(frozen=True)
class PromotionLayout:
    root: Path

@dataclass(frozen=True)
class PromotionReceipt:
    outcome: str
    active_root: Path
    rollback_root: Path | None

def validate_candidate(
    root: Path,
    expected_version: str | None = None,
    ...
) -> PromotionCandidate: ...

def promote_candidate(
    candidate: PromotionCandidate,
    layout: PromotionLayout,
    health_command: Sequence[str],
    ...
) -> PromotionReceipt: ...
```

Additional frozen receipt fields and keyword-only injectable test seams are
allowed when they directly evidence run id, version, digest, root, timeout,
fault phase, or original-command count. Do not create a second package builder,
transaction framework, installer, update policy, or public CLI.

## Behavioral Requirements
- Candidate validation delegates manifest/path/mode/digest authority to
  `validate_release_outputs(candidate_root)` and requires exact VERSION when
  supplied. It rejects symlinks, missing or tampered required material, invalid
  shell syntax, invalid Python syntax/import readiness, and a failing or timed
  out bounded no-mutation candidate smoke.
- The layout is exactly `releases/<content-digest>/`, atomic relative symlinks
  `current` and `rollback`, `promotion-state.json`, and one nonblocking
  promotion lock. A digest release is never modified or replaced in place;
  an existing digest path is reused only after full validation.
- Promotion copies to a same-filesystem temporary release, validates the copied
  candidate, and atomically renames it to the digest path before changing refs.
- The lock follows the existing directory-inode `flock` and revalidation
  pattern. Contention fails before candidate/ref/state mutation.
- A legacy directory-based `current` is validated as a runnable prior release,
  copied into its own content-addressed release, and journaled before the public
  path changes. A normal migration failure restores the original directory.
  A hard interruption at the deterministic migration fault seam is recovered on
  the next module call before a new promotion begins.
- Before health, `current` points to the candidate and the prior verified root
  remains addressable. The module runs the provided health command once with a
  bounded timeout, `CODEX_SWITCH_SKIP_SELF_UPDATE=1`, and expected structured
  values in the environment.
- The health command must return one JSON object with schema
  `codex-switch.promotion-handshake`, schema version `1`, and exact `run_id`,
  `version`, `digest`, and canonical `root`. Nonzero exit, timeout, malformed
  JSON, missing fields, or any mismatch restores the prior current reference
  atomically and leaves the failed candidate release as recoverable evidence.
- After a successful handshake, `current` remains on the candidate and
  `rollback` points to the prior verified release when one exists. A structured
  terminal state and receipt identify active/rollback roots, run id, version,
  digest, and outcome.
- If an optional original command seam is used to satisfy the approved
  exactly-once requirement, it runs zero times on validation/lock/handshake
  failure and exactly once after a successful handshake. Its ordinary nonzero
  command result is not itself a promotion-health failure.
- State/ref writes reject symlink or foreign replacement and use temp-plus-
  `os.replace`; cleanup never recursively removes an unclassified path.

## Required RED Tests
Add focused tests to `scripts/test_codex_update_release.py` that fail because the
promotion module/contract is absent, then cover at least:

1. Valid first promotion creates one digest release and atomic `current`.
2. A second valid promotion keeps both releases and sets `rollback` to the prior.
3. Existing matching digest is reused without mutation; foreign/mismatched
   digest destination is rejected.
4. Candidate invalidity: expected-version mismatch plus at least one
   manifest/digest, shell-syntax, and Python-syntax/import failure.
5. Nonblocking lock contention leaves candidate, refs, state, and prior command
   byte-identical.
6. Legacy directory-current migration failure restores the runnable directory.
7. Hard interruption during legacy migration is recovered before the next
   promotion attempt.
8. Health nonzero, timeout, malformed/error JSON, and exact-field mismatch each
   restore prior `current`, retain candidate evidence, and run the original
   command zero times.
9. Successful structured handshake records exact values and runs health and the
   optional original command exactly once.

Use only temporary roots, local helper scripts/callables, and bounded timeouts.
No test may touch the user's install/profile/App state or use the network.

## Verification
Capture exact RED and GREEN output, then run:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c \
  "import ast, pathlib; ast.parse(pathlib.Path('scripts/codex_switch_promotion.py').read_text())"
PYTHONDONTWRITEBYTECODE=1 python3.12 -c \
  "import ast, pathlib; ast.parse(pathlib.Path('scripts/codex_switch_promotion.py').read_text())"
openspec validate fail-safe-update-release --strict --no-interactive
git diff --check
```

Also run `rg` proving the new module has no caller in installer/runner/wrapper
yet; adapter migration belongs to tasks 2.1-2.4.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with exact changed files and
final hashes; all commands run; test names; complete test logs and validation
results for RED and GREEN; the layout tree and relative ref targets;
candidate/legacy digests; lock result; state/receipt examples; handshake
error/timeout/mismatch matrix; original command counts; cleanup/residue;
residual risks and unverified areas; incidental-finding disposition; and review
needs. Do not mark task checkboxes or edit verification, ledger, state,
OpenSpec, adapters, bundle/transaction modules, or other tests.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing the public distribution
layout beyond the approved compatible sibling layout, adding a dependency,
editing shell adapters, expanding into tasks 2.x, weakening bundle validation,
touching live workstation/install/plugin/App state, bypassing a failing required
test, or performing Git/network/release actions. If the approved tests reveal
that the design cannot preserve a runnable legacy current or atomic rollback,
report the exact invariant and options without weakening the contract.
