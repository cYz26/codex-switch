# Fail-Safe Update and Release Implementation Plan

**Goal:** Make packaging, install/self-update, internal update, plugin repair,
release, and verification fail closed, recoverable, and structurally evidenced.

**Architecture:** Shared pure policy modules own bundle containment,
immutable-release promotion, semantic version decisions, catalog state, and
bounded process outcomes. Shell/workflow entrypoints become explicit adapters.

**Tech Stack:** Python 3.12 standard library, Bash, `unittest`, Git/GitHub fake
adapters, existing GitHub Actions YAML.

## Global Constraints

- No live installation, plugin mutation, Git push/tag/release, commit, or
  workstation profile switch.
- No signing claim, new production dependency, or public distribution redesign.
- Source fallback never executes a downloaded archive script.
- Verification never prints or persists raw secrets or exec prompts.
- Every production change follows RED then GREEN; main owns shared evidence.

## Target State

Only validated immutable candidates can become current; the prior verified
release stays recoverable until a structured handshake succeeds. Ordered
internal updates never downgrade a healthy newer binary. Unknown plugin catalog
state cannot authorize writes. Release assets exist and validate before refs.
Every diagnostic process is bounded, typed, sanitized, and no-clobber persisted.

## Completion Contract

- [x] Destructive package paths and unmarked destinations are rejected before
  removal, with sentinels preserved.
- [x] Candidate/copy/handshake failure retains a runnable prior release.
- [x] Same-version and older trusted self-update releases stop before candidate
  materialization while newer malformed candidates still fail closed.
- [x] Internal helper failure and postcondition mismatch cannot report success.
- [x] Invalid/empty/unknown plugin catalog states are distinct and fail closed.
- [x] Revision-named curated plugin caches are recognized without weakening
  marker or source/cache identity validation.
- [x] Workflow/planner tests prove package-before-ref and reconciliation.
- [x] Secret, timeout, oversized-output, and initialize-error tests pass.
- [x] Focused/full tests, strict OpenSpec, syntax, package, and diff checks pass.

## Critical Path

Bundle contract → immutable promotion → install/self-update → update policy →
catalog policy → bounded verify → release ordering/reconciliation.

## 1. Bundle Containment and Immutable Promotion

- [x] 1.1 Add RED tests in `scripts/test_codex_update_release.py` for output
  equal to repo/root/ancestor, symlink target, unrelated existing directory,
  missing marker, and copy failure; every case preserves repository sentinels.
- [x] 1.2 Create `scripts/codex_switch_release_bundle.py` with canonical layout,
  fixed allowlist, staging marker, required-file/mode/digest manifest, and safe
  finalization; migrate `scripts/package-release.sh`; make 1.1 GREEN.
- [x] 1.3 Add RED tests that a downloaded source archive containing a malicious
  `package-release.sh` is never executed and only the trusted fixed allowlist is
  copied; implement the source fallback and make them GREEN.
- [x] 1.4 Add RED tests for immutable `releases/<digest>`, atomic `current` and
  `rollback` refs, lock contention, invalid candidate, interrupted legacy
  migration, handshake error/timeout/mismatch, and original command exactly once.
- [x] 1.5 Create `scripts/codex_switch_promotion.py` with structured receipt,
  candidate validation, promotion lock/state, legacy-current migration,
  structured hidden handshake, and rollback; make 1.4 GREEN.

## 2. Installer and Self-Update Adapters

- [x] 2.1 Add RED shell/integration tests for installer copy/import/syntax/smoke
  failures that previously passed inside Bash conditionals; assert explicit
  nonzero status and byte-identical current/rollback references.
- [x] 2.2 Refactor `install.sh` and `run.sh` to stage and call the promotion
  module, check every helper result explicitly, and preserve public
  `current/scripts/codex-switch`; make 2.1 GREEN.
- [x] 2.3 Add RED tests for self-update invalid structure/version, re-exec
  protocol mismatch, timeout, concurrent promotion, and successful command
  replay exactly once.
- [x] 2.4 Migrate `scripts/codex-switch` self-update to immutable promotion and a
  schema/run-id/version/digest/root handshake with recursion disabled; make 2.3
  GREEN and retain the prior verified release until completion.
- [x] 2.5 Reproduce the live local-source install failure against a historical
  directory-based `current` that lacks strict-bundle release modules;
  canonicalize only a private rollback copy with inert placeholders, reject a
  symlinked `scripts/` directory before external writes, and make
  installer/runner plus dual-Python focused regressions GREEN.
- [x] 2.6 Reproduce strict manifest failure after running installed `status`;
  invoke CLI, installer, runner, packager, and generated Desktop Python helpers
  with interpreter-scoped `-B`, preserve backend/task environment semantics, and
  make immutable-release plus wrapper regressions GREEN.
- [x] 2.7 Reproduce a strict current `1.0.0` checking same-version and older
  malformed legacy releases; resolve trusted explicit/default-latest version
  metadata before workdir creation or candidate validation, keep newer malformed
  candidates fail closed, confirm Python 3.9 fails before switch/store mutation,
  and record that rollout restarts must not use keepalive-capable
  `launchctl submit`.

## 3. Ordered Internal Update

- [x] 3.1 Add RED policy tests for healthy newer current, healthy older current,
  blocked current fallback, blocked latest with newer current, blocked latest
  with older current, missing/unparseable versions, and prerelease ordering.
- [x] 3.2 Create `scripts/codex_switch_update_policy.py` returning structured
  decisions/results; downgrade only when current is explicitly blocked; make
  3.1 GREEN.
- [x] 3.3 Add RED adapter tests for helper exit 17, helper success with wrong
  after-version, blocked-current repair failure, and compatibility-smoke failure.
- [x] 3.4 Refactor internal update functions in `scripts/codex-switch` to check
  helper status, re-read version, set `INTERNAL_AUTO_UPDATED=1` only on exact
  postcondition, and require the runtime compatibility boundary; make 3.3 GREEN.

## 4. Plugin Catalog and Repair

- [x] 4.1 Add RED tests distinguishing valid empty catalog, command failure,
  empty stdout, malformed/truncated JSON, stderr warning, unsupported schema,
  and complete catalog.
- [x] 4.2 Add typed `CatalogResult` and separate stdout/stderr in
  `scripts/codex_switch_plugins.py`; only `verified` authorizes availability
  decisions; make 4.1 GREEN.
- [x] 4.3 Add RED tests that uncertain catalog invokes zero add/disable/config
  writes, partial cache directories are not installed, dry-run returns a plan,
  and multi-write failure is rolled back or journaled.
- [x] 4.4 Split plugin repair into pure plan and apply seams, validate markers
  and all config inputs before mutation, and make 4.3 GREEN.
- [x] 4.5 Reproduce the live official-to-internal Doctor false failure with an
  opaque catalog/cache revision and semantic plugin manifest version; add RED
  Doctor and repair-plan tests, separate cache-key identity from manifest
  identity, preserve wrong-name/malformed/symlink/source-cache mismatch
  rejection, and make focused plus full profile regressions GREEN.

## 5. Structured Bounded Verification

- [x] 5.1 Add RED tests for hanging/term-resistant fake processes, excessive or
  malformed output, stdout/stderr separation, missing binary prerequisite, and
  unique no-clobber report names.
- [x] 5.2 Add a bounded process runner with monotonic deadline, chunk/ring
  limits, terminate/kill escalation, process groups, and typed
  `passed|failed|not_run` outcomes; migrate verify subprocesses; make 5.1 GREEN.
- [x] 5.3 Add RED tests containing Authorization, Bearer, API-key, cookie, signed
  query, exec prompt, and routing headers across stdout/stderr/exception paths;
  assert forbidden values appear in neither CLI nor JSON report.
- [x] 5.4 Implement one allowlist-first sanitizer before print/persist, never
  store raw prompts, retain only explicitly safe routing values, and make 5.3
  GREEN.
- [x] 5.5 Add RED app-server tests for initialize error, missing result,
  malformed/oversized line, pre-initialize plugin auth error, and permitted
  post-initialize auth error; implement an explicit protocol state machine.

## 6. Release Ordering and Reconciliation

- [x] 6.1 Add RED planner tests for non-ancestor base tag, tag on different
  commit, missing asset resume, matching complete tag, remote-main race,
  deterministic checksum mismatch, and publish failure rerun.
- [x] 6.2 Refactor `scripts/release_auto.py` into prepare/reconcile decisions:
  package/validate local commit assets before tag, confirm remote base, atomic
  push main+tag, publish, then download/hash all required assets; make 6.1 GREEN.
- [x] 6.3 Add static workflow tests proving no tag/push precedes packaging and
  failures cannot advance refs; update `.github/workflows/auto-release.yml` and
  `.github/workflows/release.yml` adapters and make them GREEN.
- [x] 6.4 Add reconciliation tests for latest tag missing assets and rerun of the
  same tag; prohibit clobber when commit/assets differ.
- [x] 6.5 Add RED/GREEN tests for commit-tree authority despite
  `assume-unchanged`/`skip-worktree`, root-only manifest exclusion, special
  files, fixed package-root mode, and strict-vs-explicit-legacy format routing.
- [x] 6.6 Bind manual recovery to an exact remote semantic tag before target
  code, disable persisted checkout credentials, keep trusted tooling on `main`,
  and recheck remote tag identity around every release mutation.
- [x] 6.7 Add trusted versioned historical layouts and deterministic legacy
  archive canonicalization so supported tag retries reproduce asset hashes.
- [x] 6.8 Add planner/workflow tests and implementation for reconciliation plus
  pending release-relevant `HEAD` changes in the same run.

## 7. Cleanup and Verification

- [x] 7.1 Remove obsolete in-place promotion, inequality policy, catalog-empty
  fallback, raw-output inference, and tag-before-package branches only after
  `rg` proves no supported caller remains.
- [x] 7.2 Run `PYTHONDONTWRITEBYTECODE=1 python3.12
  scripts/test_codex_update_release.py -v` and require zero failures.
- [x] 7.3 Run the full profile suite plus existing release planner tests and
  require zero failures.
- [x] 7.4 Run strict OpenSpec, shell syntax, Python AST/import, isolated package
  generation to a fresh temp root, workflow static checks, and `git diff --check`.
- [x] 7.5 Record RED/GREEN logs, bundle/rollback receipts, sanitizer evidence,
  changed files, release fake-adapter calls, and residual risks in
  `.planning/devflow/verification/fail-safe-update-release.md`.

## Execution Ledger

| Slice | Owner | Write Set | Evidence | Human Gate | Outcome | Status |
|---|---|---|---|---|---|---|
| Bundle/promotion | delegated worker + main review | bundle/promotion/package/test | containment and rollback log | live install/layout expansion | CONTINUE_NEXT_ITEM | complete; 1.1-1.5 verified |
| Install/self-update | delegated worker + main review | install/run/CLI/test | handshake and replay log | workstation install | CONTINUE_NEXT_ITEM | complete; tasks 2.1-2.7 verified |
| Same/older release metadata gate | main | self-update wrapper, adapter tests, FSR artifacts/evidence | no-materialization RED/GREEN, live same-version status, restart guard | no App restart or release publication | CONTINUE_NEXT_ITEM | complete; dual-Python focused 5/5, Python selection/fail-before-write 3/3, installed status clean |
| Update/catalog | delegated worker + main review | policy/CLI/plugins/test | ordering and zero-write log | live update/plugin write | CONTINUE_NEXT_ITEM | complete; tasks 3.1-4.4 verified |
| Revision-named plugin cache | main | plugin materialization, profile tests, FSR artifacts/evidence | live-layout RED/GREEN and Doctor proof | no additional plugin mutation | CONTINUE_NEXT_ITEM | complete; dual-Python 5/5, profile 198/198, live source Doctor passed |
| Verification | delegated worker + main review | verify/process/test | timeout/sanitizer/state-machine log | exec smoke with secret input | CONTINUE_NEXT_ITEM | complete; tasks 5.1-5.5 verified |
| Release | delegated worker | planner/workflows/test | fake Git/GitHub ordering log | commit/push/tag/release | VERIFY_ACTIVE_CHANGE | complete; tasks 6.1-6.8 verified |
| Final verification | main | control plane/evidence | full commands | external effects | COMPLETE | complete; update/release 113/113, profile 198/198, strict/static/package/install/status gates passed |

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate fail-safe-update-release --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
```

## Risks / Rollback

- Git/GitHub cannot form one distributed atomic transaction; reconciliation is
  the recovery contract.
- Integrity manifests do not prove source authenticity; signing remains out.
- Rollback restores previous source/workflow files. Isolated tests never mutate
  real installs, catalogs, repositories, or remotes.
