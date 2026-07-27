# Evidence: FSR-001

## Claim

OpenSpec `fail-safe-update-release` tasks 1.1-7.5 are complete. Release bundle
packaging rejects destructive or unclassified destinations before removal,
builds and validates a fixed-allowlist candidate in marker-owned staging, and
restores all prior public outputs after copy or partial-finalization failure.
Downloaded source fallback copies only the trusted fixed allowlist and never
executes an archive-owned packaging script. Immutable promotion retains
content-addressed releases, switches only identity-bound relative refs, requires
a structured health handshake, and recovers interrupted candidate or legacy
migrations before accepting new work. Installer and runner adapters use
hash-bound trusted bootstrap modules, promote through the immutable layout, and
replay the requested command exactly once from the promoted digest root.
Installed self-update now uses the same trusted bundle and immutable promotion
seams, validates the promotion receipt against run id, version, digest, and
digest root, disables recursion, and replays the user command exactly once from
that root. Trusted same-version and older release metadata is compared before
download or candidate staging; newer candidates still require strict
validation. Sync failure retains and runs the prior verified implementation.
Internal updates use ordered semantic-version decisions plus exact
postcondition and compatibility checks. Plugin repair distinguishes verified
catalogs from every uncertain state, validates complete cache markers, returns
a typed plan, recognizes revision-named curated cache keys separately from
semantic manifest versions, and applies prevalidated config updates with drift
checks and rollback. Verification is bounded and sanitized. Release planning binds to
exact commit trees and remote tags, packages before refs, reconciles incomplete
releases, and preserves pending source work. Final source verification passes
the complete update/release and profile suites plus strict OpenSpec, dual
Python static/import checks, shell syntax, workflow parsing/static checks,
isolated package validation, and diff integrity.

## Scope

- Contract:
  `.planning/devflow/agent-contracts/fail-safe-bundle-containment.md`
- Contract:
  `.planning/devflow/agent-contracts/fail-safe-source-fallback.md`
- Contract:
  `.planning/devflow/agent-contracts/fail-safe-immutable-promotion.md`
- Production write set:
  `scripts/codex_switch_release_bundle.py`,
  `scripts/codex_switch_promotion.py`,
  `scripts/codex_switch_update_policy.py`,
  `scripts/codex_switch_plugins.py`,
  `scripts/codex_switch_verify.py`,
  `scripts/release_auto.py`,
  `scripts/package-release.sh`,
  `install.sh`,
  `run.sh`,
  `scripts/codex-switch`,
  `.github/workflows/auto-release.yml`,
  `.github/workflows/release.yml`
- Test write set:
  `scripts/test_codex_update_release.py`,
  `scripts/test_codex_profile_switch.py`
- Documentation write set:
  `README.md`,
  `SKILL.md`
- FSR-001 source verification used no live install or profile/App mutation.
  FSR-002 used one explicitly authorized local-source install and normal status
  check; it did not switch profiles, restart the App, mutate plugins, publish a
  release, or perform Git mutation.

## Commands Run

| Command | Exit | Evidence File / Output Summary |
|---|---:|---|
| `check_dependencies.py --capability test-first-execution --json` | 0 | workflow ready; project-local `tdd` ready |
| `validate_agent_task_contract.py --contract ...fail-safe-bundle-containment.md --json` | 0 | contract valid; zero errors |
| `/usr/bin/python3 scripts/test_codex_update_release.py -v` before implementation | 1 | RED: 13 tests, 14 failures; module/typed contract absent |
| focused stale-classification test before review fix | 1 | RED: `BundleError not raised` after an unmarked destination swap |
| delegated malicious-source fallback tests before 1.3 implementation | 1 | RED: installer, runner, and self-update all executed the archive packager; 3/3 failed |
| delegated missing-required-path test before validation | 1 | RED: installer returned 0 for an incomplete downloaded source |
| main cleanup-failure review test before fix | 1 | RED: installer and runner both returned 0 after injected `scripts/__pycache__` removal failure |
| main self-update staging-failure review test before fix | 1 | RED: partially staged source replaced `current` and ran `raw-source:status` |
| delegated immutable-promotion tests before implementation | 1 | RED: 25 total; existing 14 passed and 11 promotion tests failed because the contract/module was absent |
| first main promotion GREEN run on Python 3.9.6 | 1 | one failure and ten errors exposed smoke mutation ordering and `/var` versus `/private/var` ref canonicalization |
| first main promotion GREEN run on Python 3.12.13 | 1 | four failures and ten errors additionally exposed isolated import bytecode mutation |
| main state/ref/staging/crash review REDs | 1 | foreign state/ref replacement, active-state rollback, replaced staging, candidate interruption, pre-move legacy failure, and Boolean schema cases failed before their guards |
| `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v` | 0 | main rerun: 14/14 passed on Python 3.9.6 |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v` | 0 | main rerun: 14/14 passed on Python 3.12.13 |
| final `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v` | 0 | 34/34 passed on Python 3.9.6 |
| final `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v` | 0 | 34/34 passed on Python 3.12.13 |
| adapter task 2.1 RED on Python 3.9.6 | 1 | 4 tests, 8 installer/runner subcases failed: copy/import/syntax paths returned success and smoke replaced current before failure |
| adapter task 2.1 RED on Python 3.12.13 | 1 | 4 tests, 8 installer/runner subcases failed with the same status/ref corruption contract |
| task 2.2 trust/replay review RED on Python 3.12.13 | 1 | missing required modules were accepted, piped entrypoints failed on unset `BASH_SOURCE`, and a concurrent promotion caused the runner to execute the wrong `current` root |
| task 2.2 malicious-bootstrap RED refinement | 1 | 4 malicious module subcases were initially blocked only by the unset `BASH_SOURCE` crash; tightened assertions required a hash-bound rejection with no sentinel execution |
| task 2.2 focused GREEN on Python 3.12.13 | 0 | 4/4 required-module, immutable-root replay, valid piped bootstrap, and malicious bootstrap tests passed |
| task 2.2 final installer/runner class on Python 3.9.6 | 0 | 10/10 adapter tests passed after explicit helper and cleanup propagation |
| task 2.2 final update/release suite on Python 3.12.13 | 0 | 47/47 tests passed |
| full update/release suite on Python 3.9.6 before final shell-only cleanup diagnostics | 0 | 47/47 tests passed; the final affected installer/runner class was rerun 10/10 afterward |
| task 2.3 self-update RED on Python 3.12.13 | 1 | 6/6 expected behavior failures; legacy self-update replaced immutable `current` with a directory |
| task 2.3 self-update RED under system Python 3.9.6 with Python 3.12 CLI runtime | 1 | same 6/6 expected behavior failures; no fixture errors |
| task 2.3 dual-runtime AST and test-file whitespace check | 0 | Python 3.9.6 and 3.12.13 parsed the tests; whitespace check passed |
| first task 2.4 existing-profile run after fixture migration | 1 | 5/10 failed because release archive extraction under `umask 0077` changed manifest `run.sh` mode from `0755` to `0700` |
| exploratory parallel task 2.4 focused run | 1 | one setup candidate hit the test fixture's one-second smoke timeout; all other cases passed, and serial reruns did not reproduce it |
| task 2.4 six self-update contracts on Python 3.12.13 | 0 | 6/6 passed: invalid structure/version, mismatch, timeout, concurrent receipt-root replay, and nonzero exactly-once |
| task 2.4 six self-update contracts on system Python 3.9.6 | 0 | 6/6 passed using the supported Python 3.12 wrapper runtime |
| final focused profile self-update tests on Python 3.12.13 | 0 | 10/10 passed, including explicit `umask 0077`, same/older versions, source fallback, and failure continuation |
| final focused profile self-update tests on system Python 3.9.6 | 0 | 10/10 passed |
| final full update/release suite on Python 3.12.13 | 0 | 53/53 passed |
| final full update/release suite on system Python 3.9.6 | 0 | 53/53 passed |
| six adjacent profile adapter tests on Python 3.9.6 and 3.12.13 | 0 | both interpreters passed source fallback, local source, cleanup failure, release runner, and immutable execution-root assertions |
| seven focused source-fallback and failure-propagation tests on both interpreters | 0 | main rerun: 7/7 passed on Python 3.9.6 and Python 3.12.13 |
| package troubleshooting regression on both interpreters | 0 | 1/1 passed on Python 3.9.6 and Python 3.12.13 |
| `bash -n install.sh run.sh scripts/codex-switch scripts/package-release.sh` | 0 | shell syntax passed |
| dual-interpreter `py_compile` for bundle module and tests | 0 | Python 3.9.6 and 3.12.13 passed |
| dual-interpreter AST for promotion, bundle, and update/release tests | 0 | Python 3.9.6 and 3.12.13 passed |
| `openspec validate fail-safe-update-release --strict --no-interactive` | 0 | change valid |
| obsolete in-place self-update `rg` | 1 | expected no matches for `current.self-update`, `current.previous`, or direct target replacement branches |
| isolated `package-release.sh` twice in one fresh temporary output root | 0 | both runs succeeded; exact three outputs; no stage/backup residue |
| source executable-mode probe with and without `tar -p` | 0 | default extraction reduced modes to `0700`; `-p` preserved `0741/0751/0701` |
| no-packager-invocation `rg` over installer, runner, and wrapper | 0 | no downloaded-source path invokes `package-release.sh` |
| promotion-caller `rg` over installer, runner, wrapper, and production scripts | 0 | no adapter caller exists before tasks 2.1-2.4 |
| isolated two-release promotion receipt | 0 | two digest roots, relative current/rollback refs, structured promoted state, no temporary residue |
| final embedded bootstrap digest check | 0 | installer and runner constants match SHA-256 `21db34...6920` for bundle and `590994...5544` for promotion |
| final isolated `package-release.sh` validation | 0 | exact outputs `codex-switch/`, `codex-switch.tar.gz`, and `run.sh`; 60 manifest files, 67 archive members, payload SHA-256 `75c79f...ee46` |
| `git diff --check` | 0 | passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v` | 0 | final 107/107 passed in 191.044s |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 0 | final 193/193 passed in 183.009s |
| `openspec validate --all --strict --no-interactive` | 0 | 17/17 repository items passed |
| `bash -n scripts/codex-switch scripts/codex_env_setup install.sh run.sh scripts/package-release.sh` | 0 | 5/5 shell entrypoints passed |
| dual-runtime AST/import harness | 0 | AST 54/54 and production imports 46/46 on Python 3.12.13 and system Python 3.9.6 |
| Ruby YAML parse plus `CodexReleaseWorkflowTests` | 0 | workflow YAML 2/2 and static release contracts 6/6 passed |
| isolated supported `scripts/package-release.sh` in `TemporaryDirectory` | 0 | version 0.1.13, 64 manifest files, mode 0755, 370922-byte archive, payload SHA-256 `6dab0fc4...14ede` |
| final `git diff --check` | 0 | passed after task 7.4 control-plane updates |
| first parallel post-repair full update/release run | 1 | one one-second candidate smoke timed out under concurrent full-suite load; the exact test passed alone and the complete serial rerun passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v` | 0 | final serial post-repair result: 113/113 passed in 205.371s |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 0 | final post-repair result: 198/198 passed in 213.240s |
| system Python focused same/older/default-latest/newer-invalid self-update matrix | 0 | 5/5 passed with the supported Python 3.12 CLI runtime |
| Python selection and fail-before-write matrix | 0 | 3/3 passed: auto-select modern Python, reject explicit old wrapper Python, reject direct Python 3.9 before store creation |
| supported local-source install plus normal `codex-switch status` | 0 | installed payload `9e9c9cd4...fcecbd3`; status printed `already up to date 0.1.13` with no `source_invalid` or sync warning |

## TDD Evidence

- Initial RED: rejection tests required `BundleError` reason codes, so a
  missing module or command could not satisfy the contract.
- Initial GREEN: canonical destination validation, fixed allowlist, staging
  marker, bundle manifest, package/runner/archive validation, and transactional
  finalization passed 13/13 tests.
- Main review finding: existing outputs were classified only before staging.
  A later unmarked directory swap could be moved into the owned backup and
  recursively deleted.
- Review RED: the injected post-preflight swap completed without raising.
- Review GREEN: finalization reclassifies current outputs, binds `lstat`
  device/inode/type across each rename, validates the exact moved package,
  runner, and archive before promotion and cleanup, and preserves unbound
  backup evidence. Final focused result is 14/14 on both interpreters.
- Task 1.3 RED: installer, runner, and self-update executed the malicious
  archive packager. An incomplete source archive was also accepted.
- Task 1.3 GREEN: all three downloaded-source paths validate regular,
  non-symlink required roots and executables, copy only the fixed allowlist,
  preserve executable modes, remove root `scripts/__pycache__`, and leave the
  archive packager inert.
- Main review RED: injected allowlist-cleanup failure was ignored by installer
  and runner. A separate partial-staging plus cleanup failure was ignored by
  self-update because Bash conditional context disabled implicit `errexit`.
- Main review GREEN: staging initialization, allowlist cleanup, and downloaded
  self-update staging are explicitly checked before destination replacement.
  Final focused result is 7/7 on both interpreters.
- Task 1.4 RED: immutable layout, lock contention, candidate validation,
  reversible legacy migration, handshake failure/timeout/mismatch, rollback,
  and original-command exactly-once tests failed while the promotion contract
  was absent.
- Task 1.5 GREEN: one Python 3.9-compatible module now delegates bundle
  authority, isolates import/smoke validation, stages on the target filesystem,
  publishes digest releases, atomically manages relative refs, and records a
  structured receipt/state around a bounded exact-field handshake.
- Main promotion review RED/GREEN: state/ref paths are identity-bound across
  writes; foreign replacements are preserved; candidate and legacy crash
  windows recover before new promotion; active-state failure restores prior
  refs; replaced staging is retained instead of recursively removed; and JSON
  Boolean schema versions are rejected by handshake, state, manifest, and
  workdir-marker validation.
- Task 2.1 RED: installer and runner accepted structurally complete candidates
  with failed Python import, shell syntax, or command smoke validation. Copy
  failure in the immutable releases directory was bypassed entirely. Seven
  subcases returned success; the runner smoke case returned nonzero only after
  replacing the `current` reference. All eight changed `current` from the prior
  symlink layout instead of preserving byte-identical `current`/`rollback`.
- Task 2.2 GREEN: both adapters now stage under the target library filesystem,
  canonicalize source fallback with trusted modules, validate and promote the
  candidate, and update only the stable public `current/scripts/codex-switch`
  path. Primary failures and cleanup failures are captured independently.
- Review RED/GREEN: stdin execution no longer dereferences an unset
  `BASH_SOURCE`; installed/archive bootstrap modules must match embedded
  digests and are copied then re-hashed before execution; malicious variants
  remain inert. The release contract now rejects candidates missing the profile,
  bundle, or promotion Python modules.
- Review RED/GREEN: the promotion CLI passes `scripts/codex-switch` as the
  original command into `promote_candidate`, so a concurrent update of
  `current` cannot redirect replay. The receipt records one execution and the
  CLI preserves nonzero and signal-derived exit status.
- Standards review GREEN: the unchecked `find | head` archive-root selection
  was replaced by an explicit single-directory classifier, and all workdir and
  source-staging cleanup paths now handle helper results explicitly.
- Task 2.3 RED: six isolated public-wrapper tests execute the installed CLI from
  an immutable two-release layout. Both supported test interpreters prove the
  legacy adapter replaces `current` with a directory, never reaches structured
  handshake rollback, cannot bind replay to a receipt digest after a concurrent
  promotion, and executes the prior digest instead of the promoted digest.
  Test-only Python shims bound timeout duration and deterministic concurrent
  promotion without changing production behavior.
- Task 2.4 GREEN: the wrapper uses only the current trusted bundle/promotion
  modules, validates a canonical candidate and expected version, promotes under
  the target library lock, validates receipt version/digest/root/run id, disables
  recursion, and re-executes from the receipt root. Candidate or handshake
  failure continues through the prior verified command; user-command nonzero is
  returned without a second execution.
- Main review RED/GREEN: old profile fixtures lacked trusted modules and used a
  mutable directory `current`; they now start from canonical bundles and
  immutable refs. After that migration, restrictive umask exposed release
  archive extraction changing manifest executable modes. `tar -p` plus an
  explicit `umask 0077` regression preserves the canonical `0755` contract.

## Bundle Receipt

- Manifest schema: `codex-switch.release-bundle`, version `1`
- Classification: `codex-switch-release-bundle`
- Fixed files: `README.md`, `SKILL.md`, `VERSION`, `run.sh`
- Fixed directories: `agents`, `docs`, `evals`, `scripts`
- Required executables normalized to `0755`: `run.sh`,
  `scripts/codex-switch`, `scripts/package-release.sh`
- Required Python modules: `scripts/codex_profile_switch.py`,
  `scripts/codex_switch_release_bundle.py`,
  `scripts/codex_switch_promotion.py`,
  `scripts/codex_switch_update_policy.py`,
  `scripts/codex_switch_official_release.py`
- Fresh main-run payload SHA-256:
  `6dab0fc4e820d5f5e511e0115154d28ccfbd5e7a9db75468174a0baefd014ede`
- Manifest file records: 64
- Package root mode: `0755`
- Archive bytes: 370922
- Public outputs: `codex-switch/`, `run.sh`, `codex-switch.tar.gz`
- Residual staging/backup paths: none

## Source Fallback Receipt

- Fixed files: `README.md`, `SKILL.md`, `VERSION`, `run.sh`
- Fixed directories: `agents`, `docs`, `evals`, `scripts`
- Required executables: `run.sh`, `scripts/codex-switch`,
  `scripts/package-release.sh`
- Preserved test modes: `0741`, `0751`, `0701`
- Installer malicious sentinel: absent
- Remote-runner malicious sentinel: absent
- Self-update malicious sentinel: absent
- Extra root file: absent
- Root `scripts/__pycache__`: absent
- Missing required directory: rejected before install
- Injected allowlist-cleanup failure: nonzero, no `current` promotion
- Injected self-update staging/cleanup failure: prior `0.1.1` remained current
- Explicit local-source behavior: unchanged and verified

## Promotion Receipt

- Layout: `releases/<payload-sha256>/`, `current`, `rollback`,
  `promotion-state.json`, and directory-inode `promotion.lock`
- First digest:
  `80a84c13a9b14fff926c5961119b4fedc56926abfb19b57b84a62b369338a730`
- Second digest:
  `07cd83775f358ba603dfc504599d6df016199c4248bf9a741d1b6a580383daa6`
- Current target: `releases/07cd83775f...580383daa6`
- Rollback target: `releases/80a84c13a...369338a730`
- Terminal outcome: `promoted`; schema
  `codex-switch.promotion-state`, version `1`
- Health count: exactly one; failed-handshake original-command count: zero
- Successful optional original-command count: exactly one
- Candidate evidence retained after handshake failure: yes
- Legacy interruption recovery points: before move, after move, and after
  legacy ref installation
- Candidate interruption recovery points: after candidate ref installation
  and after active-state publication
- Residual temporary promotion paths after success: none
- Final SHA-256 `scripts/codex_switch_promotion.py`:
  `590994799860ef13b74f2b07e45ad249e81e9dcf1e984ac7408bef7743845544`
- Final SHA-256 `scripts/codex_switch_release_bundle.py`:
  `a301822fc5347c2225c4a73c9be2f31a05bebf4fac2c80083cd4f3698f49c9b3`
- Final SHA-256 `scripts/test_codex_update_release.py`:
  `81e5789c0ab6ff2b0db7fbfe99a4fa5b196c7c491e8e72dc394b98841282c6ec`

## Changed Files

- `scripts/test_codex_update_release.py`: 53 containment, source-fallback,
  promotion, adapter, trust-bootstrap, rollback, crash-recovery, identity,
  handshake, self-update replay, concurrency, and schema tests.
- `scripts/codex_switch_release_bundle.py`: canonical bundle policy,
  validation, staging, identity binding, strict integer schema versions,
  finalization, rollback, and CLI.
- `scripts/codex_switch_promotion.py`: candidate validation, immutable release
  publication, state/ref identity binding, legacy/candidate recovery, handshake,
  rollback, and structured receipt.
- `scripts/package-release.sh`: thin Python adapter.
- `install.sh`: downloaded-source validation, hash-bound bootstrap,
  canonical candidate staging, immutable promotion, explicit helper status, and
  stable PATH symlink publication.
- `run.sh`: downloaded-source validation, hash-bound bootstrap, canonical
  candidate staging, immutable promotion, and digest-root command replay.
- `scripts/codex-switch`: trusted source staging, canonical candidate
  validation, immutable self-update promotion, receipt-root replay, recursion
  suppression, explicit helper status, and mode-preserving archive extraction.
- `scripts/codex_switch_update_policy.py`: ordered SemVer decisions and
  blocked-current fallback policy.
- `scripts/release_auto.py`: exact commit-tree authority, planner decisions,
  deterministic historical routing, asset evidence, tag identity checks, and
  reconciliation.
- `.github/workflows/auto-release.yml`: package/validate-before-ref ordering,
  isolated reconciliation and pending release paths, source restoration, and
  atomic ref publication.
- `.github/workflows/release.yml`: trusted-main tooling, exact remote tag
  resolution, credential-disabled target checkout, and reconciliation-only
  manual recovery.
- `scripts/test_codex_profile_switch.py`: malicious archive, fixed allowlist,
  required-module, canonical installed-wrapper fixtures, immutable
  execution-root, restrictive-umask archive modes, cleanup-failure, and
  self-update partial-staging regressions; plugin catalog, materialization,
  plan, config validation, rollback, and plan-drift regressions.
- `scripts/codex_switch_plugins.py`: typed catalog/command results, strict
  materialization markers, pure repair planning, prevalidated config updates,
  drift rejection, and rollback-capable application.
- `scripts/codex_switch_verify.py`: typed bounded outcomes, process-group
  deadlines, no-clobber reports, sanitizer, and bounded app-server protocol
  state machine.
- `scripts/test_codex_verify.py`: timeout, process-group, capture, report,
  sanitizer, and app-server state regressions.
- `README.md`, `SKILL.md`: downloaded scripts are inert during fallback staging.
- `openspec/changes/fail-safe-update-release/tasks.md`: completion and task
  status.
- `TASK_LEDGER.md`: FSR execution status and receipt.
- `.planning/STATE.md`: durable checkpoint and next action.
- `.planning/checkpoints/2026-07-24-fsr-*.md` and
  `.planning/checkpoints/2026-07-25-fsr-*.md`: per-slice RED/GREEN and
  verification checkpoints.

## Review

- Main review finding: one blocking stale-classification deletion window.
- Disposition: fixed by a bounded RED/GREEN guard before task completion.
- Main review finding: installer/runner could report success after source
  allowlist cleanup failed.
- Disposition: fixed by explicit staging and cleanup status checks.
- Main review finding: downloaded-source self-update could continue after a
  failed partial stage and promote the stale candidate.
- Disposition: fixed by explicitly propagating the tarball staging result out
  of `sync_self_update`.
- Main review finding: promotion could overwrite foreign state/ref paths,
  delete a replaced staging tree, or retain an unverified candidate after a
  hard interruption.
- Disposition: fixed with identity-bound publication, owned cleanup, and
  startup recovery for both candidate and legacy in-progress states.
- Main review finding: Python accepted JSON Boolean schema versions as integer
  version `1`.
- Disposition: fixed at handshake/state and canonical bundle authorities.
- Spec review finding: piped entrypoints could execute or import archive-owned
  bootstrap modules before a trusted boundary, runner replay used mutable
  `current`, and candidates with no required production Python modules passed.
- Disposition: fixed with stdin-safe source detection, embedded digest binding
  plus copy/re-hash staging, digest-root original-command replay, and required
  module enforcement.
- Standards review finding: `find | head` and ignored workdir cleanup results
  left helper propagation incomplete.
- Disposition: fixed with explicit archive classification and combined
  primary/cleanup status handling.
- Task 2.4 review finding: release bundle extraction without `tar -p` invalidated
  manifest executable modes under restrictive umask.
- Disposition: fixed with mode-preserving extraction and a deterministic
  `umask 0077` regression.
- Remaining actionable findings for tasks 1.1-2.4: none.

## Risks / Gaps

- Source authenticity and signing remain out of scope.
- System `tar` extracts before allowlist validation. Member path traversal and
  symlinks nested inside allowlisted directories are not proven contained by
  task 1.3 and are recorded as INC-008.
- Self-update source authenticity remains bounded by the existing integrity
  manifest; task 2.4 does not add signing or archive-member containment.
- Cross-process package finalizers are not serialized; identity binding
  prevents stale or unclassified destination deletion, while installation and
  self-update promotion are serialized by the promotion lock.
- Existing legacy `dist/codex-switch` directories without the new marker are
  intentionally rejected rather than automatically removed.
- Git refs and GitHub release mutation cannot form one distributed atomic
  transaction. Reconciliation, exact remote tag checks, and downloaded asset
  verification are the recovery contract; protected release tags remain an
  external operational prerequisite.
- Historical manifest-less retry support is intentionally limited to trusted
  `v0.1.12` and `v0.1.13` layouts.
- The original source-verification snapshot did not prove a live workstation
  install, Desktop launch, or profile binding. The final rollout receipt below
  now records those checks.

## Reviewer Notes

- Correctness: acceptance criteria checked against the safe package destination
  scenarios and fixed after one review RED.
- Verification: focused, adjacent, syntax, compile, strict OpenSpec, isolated
  package, and diff checks passed.
- Scope: standard library only; public release layout remains unchanged.
- Full update/release 107/107, full profile 193/193, strict/static/package
  verification, and diff integrity all pass.
- Integrated whole-goal code review and the authorized live rollout remain
  separate ledger gates after this OpenSpec implementation.

## Ordered Internal Update Policy RED

- Task: 3.1
- Public seam: `decide_internal_update(...)`
- Python 3.12.13: 8/8 expected RED failures
- System Python 3.9.6: 8/8 expected RED failures
- Failure authority: `scripts/codex_switch_update_policy.py` is absent
- Covered outcomes: `up_to_date`, `newer_current`, `upgrade`,
  `blocked_fallback`, and `failed`
- Covered ordering: stable and SemVer prerelease precedence
- Production/shell changes in this task: none
- Progress after RED: 11/38

## Ordered Internal Update Policy GREEN

- Task: 3.2
- Module: `scripts/codex_switch_update_policy.py`
- Policy SHA-256:
  `921e87cdb027175ff501d86e52232ae85aabf3ee92c9e43241cf13770959cf0c`
- Python 3.12.13 focused policy: 8/8 passed
- System Python 3.9.6 focused policy: 8/8 passed
- Python 3.12.13 complete update/release: 61/61 passed
- System Python 3.9.6 complete update/release: 61/61 passed
- Strict FSR OpenSpec: passed
- Dual-runtime AST/compile: passed
- `git diff --check`: passed
- Shell adapter changes in this task: none
- Progress after GREEN: 12/38
- Next dependency-ready item: task 3.3

## Internal Update Adapter RED

- Task: 3.3
- Public seam: one-key `codex-switch internal` wrapper flow
- Python 3.12.13: 4/4 expected behavior failures
- System Python 3.9.6: 4/4 expected behavior failures
- Existing initialization prerequisite under the 3.9 test process: Python 3.12
- Failure 1: helper exit 17 returned wrapper status 0
- Failure 2: helper exit 0 with unchanged `1.0.0` returned wrapper status 0
- Failure 3: blocked-current fallback helper exit 23 returned wrapper status 0
- Failure 4: normal upgrade omitted `--version 1.1.0` and completion preceded
  compatibility-smoke failure
- Invalid package-style unittest invocation: excluded from evidence
- Dual test compile: passed
- `git diff --check`: passed
- Progress after RED: 13/38
- Next dependency-ready item: task 3.4

## Internal Update Adapter GREEN

- Task: 3.4
- Public seams: standalone `update-internal` and one-key `internal` update flow
- Python 3.12.13 focused profile adapter: 26/26 passed
- System Python 3.9.6 shell/adapter subset: 20/20 passed
- Python 3.12.13 complete update/release: 64/64 passed
- System Python 3.9.6 complete update/release: 64/64 passed
- Helper nonzero status, wrong after-version, failed version probe, and failed
  compatibility smoke all remain non-success outcomes.
- Full helper value-option grammar is validated before forwarding, so
  `--dry-run` cannot be consumed as another option's value.
- Existing malformed internal manifests fail with status 2 and never fall back
  to the default install path.
- A plugin-repair failure after an internal update still runs mandatory
  app-server verification before returning the original repair status.
- Strict FSR OpenSpec, Bash syntax, and `git diff --check`: passed
- Wrapper SHA-256:
  `28e8a2ec2fe13bd33db0f27d4937ac939efcaec55603365c500ece177ad23798`
- Update policy SHA-256:
  `f70ed03dd0cf58c58d381778874d8e1603fc8d9375bc22f805965003f9f574d2`
- Progress after GREEN: 15/38
- Next dependency-ready item: task 4.1

## Plugin Catalog and Repair RED

- Tasks: 4.1 and 4.3
- Catalog matrix: verified empty, verified complete, command failure, empty
  stdout, malformed JSON, stderr warning, and unsupported schema.
- Initial task 4.3 run: zero-write uncertainty and partial-cache cases passed;
  dry-run failed because repair returned `int`; rollback failed because the
  first config remained changed after the second write raised.
- All-config validation RED: a malformed later config left earlier configs
  disabled.
- Plan-drift RED: generic config apply wrote despite a post-plan byte change.

## Plugin Catalog and Repair GREEN

- Tasks: 4.2 and 4.4
- `ProfileCommandResult`, `CatalogResult`, `PluginConfigUpdate`, and
  `PluginRepairPlan` are immutable typed boundaries.
- Only `CatalogResult(status="verified")` authorizes install, refresh, disable,
  or config writes.
- Materialization requires a version directory and matching
  `.codex-plugin/plugin.json`.
- Config updates are fully decoded, TOML-validated, built, and byte-bound
  before mutation; apply rejects drift and rolls back every attempted update.
- Python 3.12.13 focused task 4.3/4.4: 6/6 passed.
- Python 3.12.13 plugin-related profile tests: 35/35 passed.
- System Python 3.9.6 catalog/zero-write/cache-marker subset: 3/3 passed using
  Python 3.12 only for the existing CLI initialization prerequisite.
- System Python 3.9.6 plugin module AST/import: passed.
- Strict FSR OpenSpec: passed at 20/38.
- Focused `git diff --check`: passed.
- No live plugin, profile, App, install, update, release, network, or Git
  mutation ran.
- Next dependency-ready item: task 5.1.

## Revision-Named Plugin Cache RED / GREEN

- Task: 4.5, reopened from the authorized live `ROLLOUT-001`.
- Live RED: after official-to-internal restoration, the internal CLI reported
  the eight enabled curated plugins as installed under cache key `11c74d6b`,
  while `codex-switch doctor` reported all eight missing.
- Root cause: `plugin_cache_version_is_materialized` required the cache
  directory name to equal `.codex-plugin/plugin.json.version`. Official
  curated catalogs use the Git snapshot key `11c74d6b` for the directory while
  manifests retain semantic versions such as `figma` `2.0.13`.
- Test RED:
  `python3.12 scripts/test_codex_profile_switch.py
  CodexProfileSwitchTests.test_doctor_accepts_revision_named_enabled_plugin_cache
  CodexProfileSwitchTests.test_repair_plugins_keeps_current_revision_named_cache
  -v` failed with Doctor status 1 and an unexpected
  `plugin add figma@openai-curated`.
- Fix: cache-key identity and manifest-version identity are separate. A
  materialized cache still requires a regular version directory, regular
  marker, matching plugin name, and non-empty manifest version. Ordinary
  semantic catalog versions still require source-manifest equality; only
  revision-shaped keys may differ, and source/cache manifest-version mismatch
  remains uninspectable with zero refresh writes.
- Python 3.12.13 focused: 5/5 passed.
- System Python 3.9.6 focused: 5/5 passed, using Python 3.12 only for the
  existing CLI initialization prerequisite.
- Full profile: 198/198 passed in 210.152s.
- Full update/release: 110/110 passed in 200.716s.
- Full schema-scoped app proxy: 37/37 passed in 22.470s.
- Real current-source `doctor` and `verify internal`: passed with no additional
  plugin mutation.
- Final strict/static/package/evidence gates were rerun after this source
  change, and the repaired immutable source was installed successfully.

## Structured Verification RED

- Tasks: 5.1, 5.3, and 5.5
- Initial runner RED: four cases errored because no bounded runner existed;
  same-second reports overwrote the first path.
- First runner GREEN exposed blocking buffered reads that lost low-volume
  output from a timed-out process.
- Descendant RED: a parent exited zero while a SIGTERM-resistant child retained
  stdout/stderr pipes; the runner returned `passed` and leaked the child.
- Sanitizer RED: raw exec prompt plus authorization, bearer, API-key, cookie,
  signed-query, and password values appeared in both terminal and report.
- App-server RED: malformed JSON, a 128 KiB line, and pre-initialize plugin auth
  were ignored and incorrectly passed.

## Structured Verification GREEN

- Tasks: 5.2, 5.4, and 5.5
- `SmokeOutcome` records status, kind, summary, bounded captures, return code,
  timeout, truncation, and duration.
- `run_bounded_process` uses raw chunk reads, per-stream tail rings, monotonic
  deadlines, process sessions, TERM/KILL escalation, and process-group liveness
  checks after parent exit.
- Runtime/exec verification uses typed outcomes instead of string inference;
  missing binaries are `not_run`.
- Report filenames combine UTC stamp, nanoseconds, entropy, and `O_EXCL`;
  structured reports omit raw commands and prompts.
- One recursive sanitizer redacts credentials and signatures before print or
  persistence while preserving conservative allowlisted routing values.
- App-server smoke uses bounded JSONL parsing and explicit initialize/plugin
  request states; only post-initialize plugin auth is permitted.
- Python 3.12.13 focused verification: 17/17 passed.
- System Python 3.9.6 focused verification: 17/17 passed.
- Existing profile verify tests: 12/12 passed.
- Runtime initialize-error regression: 1/1 passed.
- Strict FSR OpenSpec: passed at 26/38.
- Dual-runtime syntax and focused `git diff --check`: passed.
- No live smoke with secret input, profile/App switch, plugin/install/update
  mutation, network release, or Git mutation ran.
- Next dependency-ready item: task 6.1.

## Release Ordering and Reconciliation RED / GREEN

- Task 6.1 RED isolated one planner error: a complete published latest tag at
  `HEAD` incorrectly selected `reconcile` instead of `none`.
- Task 6.2 GREEN made complete published releases read-only while preserving
  missing/draft reconciliation, ancestry, tag-conflict, remote-base,
  checksum-drift, and publish-rerun guards.
- Task 6.3 static contracts prove package, deterministic asset validation, and
  remote-base confirmation precede tag/atomic push. Critical paths contain no
  `continue-on-error`, `|| true`, or `--clobber`.
- Task 6.4 fake-GitHub contracts prove missing-only upload, complete same-tag
  read-only behavior, checksum-conflict zero mutation, and tag-conflict zero
  GitHub calls.
- Task 6.5 RED/GREEN covers nested manifest payload, special files, package
  mode, and worktree drift hidden by `assume-unchanged` or `skip-worktree`.
- Task 6.6 binds manual recovery to an exact remote semantic tag, trusted
  tooling from `main`, credential-disabled checkouts, and an identity check
  before every mutation plus final verification.
- Task 6.7 permits deterministic manifest-less retry only through explicit
  `--allow-legacy` for trusted `v0.1.12` and `v0.1.13` layouts.
- Task 6.8 emits independent `reconcile_required` and `prepare_required`
  decisions; `reconcile_then_prepare` uses separate dist roots/manifests and
  restores the exact original source commit before preparing the new release.

Final release-focused results include planner/workflow 21/21 on Python 3.12.13
and system Python 3.9.6, historical/CLI/workflow 13/13 on both, bundle/asset/
bootstrap 33/33 on both, and release workflow static checks 6/6.

## Fake Git / GitHub Adapter Receipt

- Missing asset: calls contain only
  `("upload", "codex-switch.tar.gz")`; no create or publish call.
- Complete same-tag release: no create, upload, or publish mutation.
- Existing checksum conflict: no create, upload, or publish mutation.
- Tag/commit conflict: GitHub adapter call list remains empty.
- Publish failure rerun: the second run reuses matching uploaded assets and
  performs no duplicate upload; final outcome is `published`.
- Mutation identity sequence: every create/upload/publish call is immediately
  preceded by a remote tag identity check; a final check follows downloaded
  verification.
- Injected tag movement on the third check: only `install.sh` uploads before
  the conflict; no later upload or publish occurs.

## Sanitizer and Bounded Verification Receipt

- Authorization, bearer, API-key, cookie, credential, password, and signed
  query values are absent from both terminal and persisted reports.
- Raw exec prompts and raw command arrays are not persisted.
- Safe routing identifiers are retained only through the conservative
  allowlist.
- Hung and TERM-resistant process groups reach bounded timeout, TERM, and KILL
  handling without descendant pipe leaks.
- Oversized/malformed app-server lines, initialize error/missing result, and
  pre-initialize plugin-auth responses fail; only post-initialize plugin-auth
  is permitted.
- Same-second reports use unique exclusive paths and do not clobber.

## Historical Final Verification Receipt

- Full update/release: 107/107 passed in 191.044s.
- Full profile: 193/193 passed in 183.009s.
- Strict OpenSpec: 17/17 passed.
- Bash syntax: 5/5 passed.
- Python 3.12.13: AST 54/54, production imports 46/46.
- System Python 3.9.6: AST 54/54, production imports 46/46.
- Workflow YAML: 2/2 parsed; static contracts 6/6 passed.
- Isolated supported package: version 0.1.13, schema
  `codex-switch.release-bundle`, mode `0755`, 64 manifest files, archive size
  370922 bytes, payload SHA-256
  `6dab0fc4e820d5f5e511e0115154d28ccfbd5e7a9db75468174a0baefd014ede`.
- `git diff --check`: passed.

Current key SHA-256:

- release bundle:
  `a301822fc5347c2225c4a73c9be2f31a05bebf4fac2c80083cd4f3698f49c9b3`
- promotion:
  `590994799860ef13b74f2b07e45ad249e81e9dcf1e984ac7408bef7743845544`
- update policy:
  `f70ed03dd0cf58c58d381778874d8e1603fc8d9375bc22f805965003f9f574d2`
- plugin policy:
  `75c36814a40d3ad801ba2ee585c794663f5fa4a41e716c3258a62cfd8068eadc`
- verification:
  `42c173374611343608ec03a521e3b2e5cb9ea6bcadf2fd2d0bcc052c99df99cb`
- release planner:
  `a402abf0b3a739194e40ff273b64106004898b7b1d7774e7287b861025aa69c8`

## Historical FSR Completion Status

All 35 implementation tasks and all 42 OpenSpec checkboxes were complete at
this historical checkpoint. No live install, self-update, profile/App switch,
plugin mutation, network release, commit, push, tag, OpenSpec archive, or
destructive cleanup was used to establish that source completion claim.

This snapshot predates the authorized rollout repairs for the same-version
self-update gate and revision-named curated plugin caches. The following
receipt supersedes its counts, hashes, and package digest.

## Authoritative Post-Rollout Repair Verification

Date: 2026-07-25 20:39:32 +0800

### Task 2.7 Metadata Gate

- The first ad hoc `python3.12 -m unittest scripts...` invocation failed before
  fixture setup because the repository root did not place `scripts/` on
  `sys.path`. The canonical direct-file test entrypoint was used afterward; no
  product code changed for this invocation error.
- Python 3.12.13 focused gate: 5/5 passed.
- System Python 3.9.6 focused gate: 5/5 passed while selecting the supported
  Python 3.12 CLI runtime.
- The focused and full tests prove same-version, older-version, and normal
  default-latest checks stop without release download or `.self-update.*`
  staging. A newer malformed candidate still fails closed before ref change.
- `ConfigDocumentTests` passed 3/3: the wrapper auto-selects an available
  Python with `tomllib`, and explicit old Python is rejected before the switch
  script or store can mutate.
- Live installed same-version behavior passed after the new immutable source
  install.

### Fresh Full Matrix

- Update/release: 113/113 passed serially in 205.371s.
- Profile: 198/198 passed in 213.240s.
- Transaction: 215/215 passed in 19.087s.
- Runtime Binding: 55/55 passed on Python 3.12.13 and 55/55 on system Python
  3.9.6.
- Schema-scoped App proxy: 37/37 passed serially on Python 3.12.13 and 37/37
  serially on system Python 3.9.6.
- Config Document: 24/24 passed.
- Verifier: 22/22 passed on Python 3.12.13 and 22/22 on the supported system
  Python route with `CODEX_SWITCH_PYTHON=python3.12`.
- Official stable advisory: 6/6 passed on both Python runtimes.
- Strict OpenSpec: 17/17 passed.
- Bash syntax: 5/5 passed.
- Python 3.12.13: AST 54/54 and production imports 46/46 passed.
- System Python 3.9.6: AST 54/54 and production imports 46/46 passed.
- Release workflow YAML: 2/2 parsed.
- Release workflow static contracts: 7/7 passed.
- `git diff --check`: passed.

### Fresh Isolated Package

- version: `0.1.13`
- schema: `codex-switch.release-bundle`
- package root mode: `0755`
- manifest files: `64`
- exact outputs: `codex-switch/`, `codex-switch.tar.gz`, `run.sh`
- archive bytes: `384585`
- archive SHA-256:
  `035fbcaad211352facc77c0b0d713b54622a2d9698dd111f71fd013971f08f0e`
- payload SHA-256:
  `9e9c9cd4bce6fd0efcc8dacd8a04e75221f7e64b4a7a3a2864423ea24fcecbd3`

`validate_release_outputs` accepted the package directory, top-level runner,
and archive. The `TemporaryDirectory` was removed automatically.

### Current Key SHA-256

- release bundle:
  `a301822fc5347c2225c4a73c9be2f31a05bebf4fac2c80083cd4f3698f49c9b3`
- promotion:
  `540a99fc15f1f5c47e6689cb014d70d4396d0f3c15d7dfdd54092301c27d4eae`
- update policy:
  `f70ed03dd0cf58c58d381778874d8e1603fc8d9375bc22f805965003f9f574d2`
- plugin policy:
  `7bb5ee4b2cb9e8ed2fc4c086a67f9495005445e8dc4a2d3ecff71f538f41bad7`
- verification:
  `50549350e4858d2b29fe61baad31e28be0fe639d6739f3b61ac4b2e36014bfeb`
- release planner:
  `a402abf0b3a739194e40ff273b64106004898b7b1d7774e7287b861025aa69c8`
- installed wrapper source:
  `2f1ed45a3c240696f08595189b212a66e743d59bb698578f14402cf25d6feced`

### Live Installed Same-Version Receipt

- Install command:
  `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch CODEX_SWITCH_PYTHON="$(command -v python3.12)" /Users/cY/dev/codex-switch/install.sh`
- Installed/current payload:
  `releases/9e9c9cd4bce6fd0efcc8dacd8a04e75221f7e64b4a7a3a2864423ea24fcecbd3`
- Rollback:
  `releases/db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`
- Installed and source wrapper SHA-256:
  `2f1ed45a3c240696f08595189b212a66e743d59bb698578f14402cf25d6feced`
- Normal `codex-switch status` printed
  `codex-switch self-update: already up to date 0.1.13`.
- Output contained neither `source_invalid` nor `sync failed`.
- Active profile remained `internal`; PATH/shim/Desktop bindings were aligned.
- ChatGPT pid 4983 and its Desktop proxy/backend pids 5332/5346 retained their
  existing uptime. No App restart was needed.
- `launchctl list` contained only the normal ChatGPT application job and
  `com.openai.codex-cli-path`; no temporary restart/relaunch job remained.
- The running proxy still uses the previously loaded immutable rollback root,
  as expected without an App restart. The repaired command wrapper is already
  active through the stable `current` symlink.

## Current FSR Completion Status

All 39 implementation tasks and all 48 OpenSpec checkboxes are complete after
the two authorized rollout repairs. The immutable install, clean same-version
status, restored internal ownership, and stable process/launchd checks are also
complete, closing `ROLLOUT-001`. Commit, push, tag, release, archive, dependency
changes, destructive cleanup, and parity implementation remain outside this
claim.
