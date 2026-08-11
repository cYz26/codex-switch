---
workflow_version: 0.3.0
project_mode: brownfield
current_stage: awaiting_human

current_phase:
  id: 01-foundation
  status: planning

current_change:
  id: internal-official-feature-parity
  status: awaiting_human

gates:
  workflow_initialized: true
  spec_approved: true
  plan_written: true
  tests_baseline_known: true
  implementation_done: false
  verification_passed: false
  state_updated: true
  archive_allowed: false

context_management:
  compact_policy: checkpoint_boundary
  last_checkpoint_id: 2026-07-27-parity-method-coverage-live-retry
  last_checkpoint_file: .planning/checkpoints/2026-07-27-parity-method-coverage-live-retry.md
  compact_recommended: false
  compact_status: skipped
  last_compact_result_file: none
  compact_source: checkpoint
  compact_updated_at: 2026-07-27T19:23:50+08:00
  compact_skip_reason: official_first_pause_human_gate
  compact_error: none
  compact_after:
    - project_setup_completed
    - codebase_mapping_completed
    - design_saved
    - openspec_change_planned
    - phase_plan_saved
    - verification_passed
    - change_archived
    - phase_shipped
  skip_compact_for:
    - small_task_update
    - typo_fix
    - docs_only_micro_change
  require_before_compact:
    - state_updated
    - durable_context_written
    - next_action_recorded
    - risks_recorded
    - validation_recorded_if_applicable

goal_gate:
  required: true
  status: blocked
  reason: task 8.3 source/package milestone is verified; live retry is deferred at PARITY-8.3-LIVE-RETRY while official remains primary
  suggested_goal: none

context_health:
  last_report: .planning/context-health/reports/20260629130742-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Official/internal independent home switching regression repaired and hardened. Doctor now accepts the managed internal Desktop app-server proxy chain, stale unavailable enabled plugin selectors have an explicit disable cleanup path, unavailable browser-use/local-personal dev-flow selectors were disabled in local config, pdf primary-runtime cache was refreshed, the generated local bundle was installed, internal Desktop config writes now preserve existing shared settings, current workstation configs were restored from the latest valid switch backup, the official unannotated runtime seed contamination regression is repaired broadly, source-profile plugin support snapshots now act as shared fallback after runtime narrowing, one-key switches now run target-profile verification before doctor, standalone verify supports safe repair, reports, and explicit runtime smoke, bidirectional shared settings shrink prevention is verified, and profile switches now preserve target-only Desktop/apps/memories/plugin/skill settings when the source runtime is narrowed.
---

# Workflow State

## Current Status

On 2026-07-27, task 8.3 reached the source/package-verified
`OFFICIAL_FIRST_PAUSE_READY` milestone. The approved RED/GREEN now closes the
saved thirteen-error preparation blocker through exact method coverage,
nullable-union semantic equivalence, a structured Protocol Adapter manifest,
the exact `thread/resume` rule, deterministic optional-extension records, a
versioned official Desktop acceptance trace, and final post-probe evidence.
Receipt schema v2 binds those records and exactly passed `core_protocol` plus
`typed_subagent_v2` results; schema v1 is stale and regenerated rather than
patched. Dual-runtime Protocol Adapter 41/41, parity 93/93, verifier 30/30,
and Runtime Binding 75/75 suites pass. The isolated release bundle validates,
and the six packaged task paths are byte-exact with source.

The user plans to use the official profile as the primary runtime, so live
same-backend rebind and Desktop switching acceptance are intentionally
deprioritized. No install, rebind, provider call, ChatGPT restart, profile/App
mutation, dependency, Git, release, archive, or cleanup occurred. Task 8.3
therefore remains unchecked at 70/79, tasks 8.4-8.7 remain unavailable, and
the active change remains unarchived. The durable source milestone and resume
contract are
`.planning/checkpoints/2026-07-27-parity-method-coverage-repair-verified.md`
and
`.planning/checkpoints/2026-07-27-parity-method-coverage-live-retry.md`.

### Human Gate

Stop at `PARITY-8.3-LIVE-RETRY`. Resumption requires a new explicit
authorization and fresh ownership/fingerprint attestation; the historical
internal pid/config snapshot and this temporary package are not standing live
authority. The gate covers at most a rebuilt/verified exact-source install if
needed, one supported same-backend preparation/rebind, its bounded
provider-backed typed-v2 probe, and resulting profile/runtime artifacts. It
does not authorize task 8.4, a ChatGPT restart, Desktop acceptance, dependency
changes, Git, release, archive, cleanup, or provider/model/API/auth migration.

On 2026-07-27, authorized task 8.3 produced a safe live RED and remains
incomplete at 70/79. The supported same-backend command exited 2 after 2.342
seconds during parity preparation with two `parity.feature.core_drift`, eight
`parity.protocol.core_incompatible`, and three
`parity.protocol.unclassified_drift` findings. The health gate stopped before
the runtime transaction: the internal manifest, managed launcher, capability
receipt, profile config, official config, active record, backend inode/hash,
and ChatGPT/proxy/backend pids were byte-for-byte unchanged at the immediate
post-failure snapshot; no parity directory, temporary rebind directory, or
schema-v3 marker remained. At 12:30 the running Codex session independently
rewrote the managed-home config after that snapshot, changing its digest and
size while the profile/manifest/launcher/active/backend ownership remained
unchanged. That later concurrent write is not evidence of an 8.3 transaction
and must be recaptured as a current input before any retry. The next action is
one read-only in-process diagnostic that stops immediately after bundle
preparation and records sanitized feature/method finding details. Do not retry
the rebind, bypass the health gate into commit, edit production behavior, or
start task 8.4. Evidence is
`.planning/checkpoints/2026-07-27-parity-same-backend-rebind-red.md`.

On 2026-07-27, authorized task 8.2 completed at 70/79 after one safe live RED
and a bounded TDD repair. The installer now accepts only the exact supported
historical manifest-v1 16-path set when reading immutable existing
`current`/`rollback` references; new candidates remain strict on the current
20-path set. The focused regression was RED with the live
`candidate_invalid` message on Python 3.12 and system Python 3.9, then GREEN
1/1 and adjacent 5/5 on both. The exact install command promoted payload
`d55005d6...4392`; old `ed5d74c1...28ab` is rollback, the prebuilt package and
installed tree are byte-exact, strict validation reports 66 files, 5
directories, and 20 required paths, and staging/bytecode residue is zero. No
restart output occurred and the existing ChatGPT/proxy/backend process chain
remains unchanged. Task 8.3 same-backend parity preparation/rebind is next.
Evidence is
`.planning/checkpoints/2026-07-27-parity-exact-source-install-verified.md`.

On 2026-07-27, `internal-official-feature-parity` task 8.1 completed at 69/79.
The user explicitly authorized the supported exact-source local install,
same-backend parity rebind for `/Users/cY/.local/bin/codex`, resulting
profile/App/runtime mutations, a bounded full ChatGPT quit/reopen, and one real
provider-backed typed `explorer` Subagent task. Mutation-preflight
re-attestation still resolves active profile `internal`, ChatGPT pid `95489`,
managed App launcher `/Users/cY/.codex-switch/bin/codex-internal-app`, App
Proxy/backend pids `95838`/`95842`, bundled reference
`codex-cli 0.146.0-alpha.3.1`, and internal backend `codex-cli 0.144.6`.
Read-only status, Doctor, and verify agree on the expected pre-rebind finding
`parity.receipt.missing`. The installed `0.1.13` release lacks the parity
module, while current source trust-anchor hashes match `install.sh`. The
DevFlow capability check reports the known project/legacy skill-layout
conflicts but confirms OpenSpec and project-local Matt `tdd` readiness; legacy
cleanup is unauthorized and remains `DEFER_AND_CONTINUE`. Task 8.2 exact-source
installation is next. Commit, push, tag, release, archive, retained-evidence
cleanup, dependency changes, and provider/model/API/auth migration remain
excluded.

On 2026-07-27, `internal-official-feature-parity` task 7.9 completed at 68/79.
The verification record now consolidates all 23 RED sections and GREEN
closures, exact dual-runtime suite counts, stable finding codes, fixture and
package digests, changed-file ownership, optional queue policy, and every live
prerequisite. It distinguishes synthetic/retained evidence from live
receipt/overlay/config evidence, which is intentionally absent before an
authorized rebind. The active change owns 73 dirty paths, including 35 parity
checkpoints; 130 pre-existing/unrelated paths remain preserved. Scoped
`git diff --check` and active strict OpenSpec validation pass. Automated
implementation and integrated review are complete with no acceptance-criterion
failure. Task 8.1 is the next item and is blocked pending explicit user
authorization for the supported source install, same-backend parity rebind,
ChatGPT quit/reopen, real provider-backed typed Subagent task, and resulting
profile/App mutations. Evidence is
`.planning/checkpoints/2026-07-27-parity-pre-live-evidence-verified.md`.

On 2026-07-27, `internal-official-feature-parity` task 7.8 completed at 67/79.
The read-only main review found no acceptance-criterion failure in receipt
health, source/config mutation boundaries, runtime recovery, executable
replacement, secret persistence, Protocol Adapter scope, or rollback coverage.
The manifest-digest-bound canonical receipt load and runtime-generation
validation remain the health authority; config/catalog preparation is
read-only until exact journaled promotion; and all seven promotion-handshake
failure regressions require complete old-generation restoration with no
restart output. A crash after committed-marker retirement but before
executable-backup retirement may leave a stale backup without a marker. The
promoted generation is already durable and the approved interruption window
does not cover that cleanup residue, so it is `DEFER_AND_CONTINUE` rather than
a new fault axis. Task 7.9 evidence consolidation is next. Evidence is
`.planning/checkpoints/2026-07-27-parity-main-review-verified.md`.

On 2026-07-27, `internal-official-feature-parity` task 7.7 completed at 66/79.
`git diff --check` passes. A deterministic dirty-worktree audit attributes 71
paths to this active change and preserves 130 pre-existing/unrelated paths; the
canonical write set now explicitly includes the actual runtime/release seams
and limits `install.sh`/`run.sh` ownership to the two verified trust-anchor
hashes. Runtime Binding, Protocol Adapter, Capability Receipt, and production
caller authority scans are clean. All 66 delta scenarios map to 60 named
automated rows plus the six unexecuted Human-Gated live Desktop rows. Task 7.8
read-only main review is next. Evidence is
`.planning/checkpoints/2026-07-27-parity-diff-coverage-verified.md`.

On 2026-07-27, `internal-official-feature-parity` task 7.6 completed at 65/79.
The isolated package passes manifest/file/mode/digest/import/archive integrity:
66 manifest files, 5 directories, 20 required paths, 47 production imports,
and 73 archive members. Parity is present; retained probes, config/auth
evidence, and bytecode are absent. Task 7.7 diff/write-set/coverage audit is
next. Evidence is
`.planning/checkpoints/2026-07-27-parity-isolated-package-verified.md`.

On 2026-07-26, `internal-official-feature-parity` task 6.7 completed at 56/79.
Release staging now requires the parity and generated-launcher runtime modules,
validates packaged imports in an isolated immutable copy, rejects unresolved
generated-script references, and uses Python 3.11+ for packaging. Python
3.12.13 and system Python 3.9.6 each pass the focused package contract 5/5,
four adjacent release/promotion regressions 4/4, and the profile package
adapter 1/1. The isolated real package contains parity and excludes retained
probe/config evidence and bytecode. Task 6.8 is next. Evidence is
`.planning/checkpoints/2026-07-26-parity-package-verified.md`.

On 2026-07-26, `internal-official-feature-parity` task 6.4 completed at 53/79.
One verifier-owned presentation seam now prints shared parity health, stable
finding codes, and deterministic optional synchronization rows. Verify uses its
single preloaded report; status reports only for the active internal profile;
Doctor reports and fails only when its active Runtime Binding is internal.
Error messages are sanitized and no caller reconstructs parity policy. Python
3.12.13 and system Python 3.9.6 pass the focused diagnostics 2/2 and parity
verifier 6/6; three adjacent Python 3.12 status/Doctor regressions pass, and
dual-runtime AST covers all four touched files. A legacy one-key internal
fixture with no receipt is intentionally unhealthy and is deferred to the
planned 6.5/6.6 repair route. Task 6.5 tests-only RED is next. Evidence is
`.planning/checkpoints/2026-07-26-parity-diagnostics-verified.md`.

On 2026-07-26, `internal-official-feature-parity` task 6.3 completed tests-only
RED at 52/79. Two focused profile tests require status, Doctor, and verify to
collect one shared `ParityReport`, print the same health and stable finding
codes, keep optional-only drift healthy, and preserve deterministic
feature-before-protocol queue ordering. The first run found a verify fixture
error from a missing temporary manifest; a tests-only empty-manifest stub now
lets the test reach the parity seam. Python 3.12.13 and system Python 3.9.6
each run 2 tests with 6 expected assertion failures and 0 errors. Status and
Doctor do not collect parity yet; verify collects once but does not print the
shared diagnostics. No production code changed. Task 6.4 narrow integration is
next. Evidence is
`.planning/checkpoints/2026-07-26-parity-diagnostics-red.md`.

On 2026-07-26, `internal-official-feature-parity` task 6.2 completed at 51/79.
The verifier now loads existing parity receipt evidence read-only, validates
its manifest/runtime-generation ownership and current adapter, binary, source,
and config fingerprints, and reuses one `ParityReport` through collection,
structured reporting, and `cmd_verify`. Missing old-manifest evidence reports
`parity.receipt.missing`; error findings are unhealthy, optional-only findings
remain a deterministic queue, report messages are sanitized, and
`--repair=none` performs zero store writes. One focused loader test first failed
only because the entry point was absent. Final focused results are 6/6 parity
verifier tests and 4/4 adjacent collect/report regressions on both Python
3.12.13 and system Python 3.9.6. Task 6.3 tests-only RED is next. Evidence is
`.planning/checkpoints/2026-07-26-parity-verifier-verified.md`.

On 2026-07-26, `internal-official-feature-parity` task 6.1 completed tests-only
RED at 50/79. Five focused verifier tests define stable parity evidence codes,
unhealthy core/unclassified/probe findings, healthy deterministic optional
queue reporting, structured-report sanitization, one collected parity result
reused by collect/report, and `--repair=none` zero writes. Python 3.12.13 and
system Python 3.9.6 each produce the same five expected assertion failures and
zero errors; the failures are exactly the missing parity-report integration,
not fixture/import/runtime errors. No production code changed. Task 6.2 is
next. Evidence is
`.planning/checkpoints/2026-07-26-parity-verifier-red.md`.

On 2026-07-26, `internal-official-feature-parity` task 5.6 integrated staged
internal updates with the production parity-safe promotion path. Public
`--install-dir` and `CODEX_INSTALL_DIR` retain their historical bound-profile
directory contract, while every real helper invocation targets a fresh private
mode-0700 `.codex-internal-update-*` sibling. The wrapper delegates exact
bound/candidate/backup paths to `promote-internal-update`; that path prepares
candidate capability/parity/overlay/config/runtime artifacts, revalidates
immutable inputs while the store mutation lock is held, commits the typed
executable swap and schema-v3 runtime bundle together, and prints success only
after installed version, canonical Runtime Binding, app-server child
attestation, capability receipt, and parity receipt postconditions pass. Fresh
results are staged update 10/10 on Python 3.12 and system Python 3.9,
update/release 123/123 on Python 3.12, profile update routes 30/30 on both,
complete profile 201/201 on Python 3.12, parity 83/83 on both, Runtime Binding
65/65 on both, and executable swap 5/5 on both. The real `~/.zshrc` retains the
stable post-task-5.3 hash/stat tuple and no bytecode residue exists. Progress
is 45/79; task 5.7 is next. No live profile, App, provider, install/update,
release, archive, or Git history effect occurred. Evidence is
`.planning/checkpoints/2026-07-26-parity-staged-update-verified.md`.

Earlier on 2026-07-26, `internal-official-feature-parity` task 5.1 recorded the staged
internal update RED contract. Seven command-boundary tests now require a
mode-0700 private sibling candidate, unchanged bound bytes through installer
and candidate probes, exact intended-version rejection, code-sign ordering,
exact installer failure propagation, complete zero-mutation dry-run output,
and no bound replacement before candidate parity/compatibility succeeds.
Focused Python 3.12 and system Python 3.9 runs reproduce the same seven
expected RED methods without fixture or import errors. The complete Python
3.12 update/release suite ran 120 tests: all 113 prior tests remain green and
the only failures are 12 expected assertions across those seven methods.
Progress is 40/79; task 5.2 is next. No production source or live state changed.
Evidence is
`.planning/checkpoints/2026-07-26-parity-staged-internal-update-red.md`.

On 2026-07-25, the final Goal verification was rerun without a PTY after an
isolated profile-test process had waited for interactive input. The hung
process group was terminated and was not counted as pass or failure. Fresh
non-interactive results passed update/release 113/113, profile 198/198, Runtime
Binding 55/55 and Protocol/SAP 37/37 on both Python 3.12.13 and system Python
3.9.6, strict OpenSpec 17/17, Bash syntax, isolated package validation, and
`git diff --check`. Read-only status confirms the live profile and Desktop
app-server chain remain bound to `internal`. No Goal completion confirmation
is pending; publication, archive, destructive mutation, and the queued parity
change remain separate gates. Evidence is
`.planning/checkpoints/2026-07-25-goal-final-verification.md`.

On 2026-07-25, FSR-002 and the authorized rollout repair completed. Trusted
explicit/default-latest version metadata is now compared before any candidate
download or staging, so installed strict `0.1.13` checking trusted latest
`v0.1.13` returns `already up to date 0.1.13` without `source_invalid` or the
generic sync-failed warning. Older releases use the same no-materialization
path; newer malformed candidates still fail closed. Fresh serial verification
passed update/release 113/113 and profile 198/198, with dual-Python focused
self-update 5/5 and Python selection/fail-before-write 3/3. Strict OpenSpec,
Bash, dual-runtime AST/import, workflow static checks, isolated package
validation, and diff integrity passed. The supported local-source install
promoted payload `9e9c9cd4...fcecbd3`; normal status retained internal
ownership. ChatGPT pid 4983 and proxy/backend pids 5332/5346 did not restart,
and launchd contains no temporary restart job. The earlier restart loop was
caused by keepalive-capable `launchctl submit`; that mechanism is prohibited
for future one-shot rollout restarts.

On 2026-07-25, `VER-001` passed the fresh post-integration source matrix.
Transaction passed 215/215, profile passed 195/195, update/release passed
108/108, Runtime Binding passed 55/55 on Python 3.12 and system Python 3.9,
Protocol/SAP passed 37/37 on both runtimes, Config Document passed 24/24,
Verifier passed 22/22 on both supported test routes, and official advisory
passed 6/6 on both runtimes. Strict OpenSpec passed 17/17; Bash passed 5/5;
dual-runtime AST/import passed 54/54 and 46/46; workflow YAML passed 2/2 and
release contracts passed 7/7; isolated package validation produced version
0.1.13, 64 manifest files, mode 0755, a 381951-byte archive, and payload
SHA-256 `d79769dff0241bf68c5e256bfcc2398a19d8dd6c1fb8c83678caef3199d31fd5`.
`git diff --check` passed. CRB and SAP reopened tasks are complete.
At that checkpoint, `ROLLOUT-001` was the next authorized action; it is now
closed by the leading status entry. `PARITY-001` remains a queued independent
Full OpenSpec. Evidence is
`.planning/verification/20260725151329-final-source-verification.md`.

On 2026-07-25, the separately authorized
`official-release-version-advisory` change reached 13/13 implementation and
verification completion. Normal official/internal update checks and one-key
switches now print a stable-only `openai/codex` comparison through a pure
SemVer policy and bounded redirect lookup. Internal comparison runs after any
auto-update and cannot select an install target, invoke the helper because of
upstream drift, or write profile state. Failure and skip paths remain
non-blocking. Review added the advisory module to the release-bundle required
manifest and refreshed installer/runner trusted hashes after RED proved an
incomplete candidate could otherwise build. Fresh results are policy 4/4,
focused wrapper 7/7, and release dependency 1/1 on Python 3.12.13 and 3.9.6;
full profile 171/171 and update/release 64/64 on Python 3.12.13; strict OpenSpec
17/17; AST 53/53 and production imports 46/46 on both runtimes; Bash syntax,
isolated bundle validation, trusted hash binding, and `git diff --check`.
Read-only checks reported internal `0.144.6` behind stable `0.145.0` and the
bundled official `0.146.0-alpha.3` ahead. No live switch/update/install/App
restart/plugin/release/Git mutation ran. Evidence is
`.planning/verification/20260725013044-official-release-version-advisory.md`.
That statement predates the now-complete FSR, integration, and `VER-001`
source verification recorded above.

On 2026-07-24, `fail-safe-update-release` task 2.4 passed implementation,
main review, and focused verification, bringing the change to 10/38. Installed
self-update now canonicalizes and validates candidates through the trusted
bundle/promotion modules, preserves immutable `current` and `rollback`, checks
the promotion receipt's run id, version, digest, and digest root, disables
recursive self-update, and executes the original command exactly once from the
receipt root. Sync failures continue through the prior verified implementation.
Main review migrated the old directory-only fixtures and found that release
bundle extraction without `tar -p` violated manifest executable modes under
`umask 0077`; a deterministic regression now covers that boundary. Fresh
results are update/release 53/53 and focused profile self-update 10/10 on both
Python 3.12.13 and system Python 3.9.6, plus strict OpenSpec, Bash syntax,
dual-runtime AST, obsolete in-place-path scan, and `git diff --check`. No live
install/self-update/profile/App/plugin/release/network/Git mutation ran. The
durable checkpoint is
`.planning/checkpoints/2026-07-24-fsr-self-update-verified.md`; task 3.1 is next.

On 2026-07-24, `schema-scoped-app-proxy` reached 32/32 implementation and
verification completion. Final current-version research found that installed
internal `0.144.6` and bundled official `0.146.0-alpha.3` renamed
`PluginMarketplaceKind` to `PluginListMarketplaceKind` and reject historical
marketplace `source_type = "github"`. RED reproduced marketplace and
config-write capability `UNKNOWN`; GREEN recognizes both schema names and uses
a network-free local marketplace probe fixture. Fresh isolated receipts for
both binaries prove canonical dynamic tools, remote marketplace kind, and
versioned config-write preservation. Final results are protocol 35/35 on
Python 3.9.6 and 3.12, Config Document 24/24, runtime binding 55/55,
transaction 211/211, profile 139/139, strict OpenSpec 16/16, Python AST 47/47
and production imports 42/42 on both runtimes, plus Bash, caller, and diff
checks. No live profile/App/install/update/plugin/release/network/Git mutation
ran. The durable checkpoint is
`.planning/checkpoints/2026-07-24-sap-final-verified.md`; FSR-001 is next.

On 2026-07-24, SAP tasks 5.2-5.3 passed cleanup review and focused regression.
`rg` reports no production or test caller for the eleven superseded recursive
or line-only TOML helpers, so their definitions were removed. The explicit
`0.140` dynamic-tools and marketplace compatibility rules, stable diagnostics,
and their focused tests remain. Fresh results are Config Document 24/24,
protocol 34/34 on Python 3.9.6 and 3.12, and profile 139/139 on Python 3.12.
The affected modules compile on both runtimes and `git diff --check` passes.
SAP task 5.4 complete regression and static verification are next.

On 2026-07-24, SAP task 5.1 passed TDD and main review. Generated wrappers now
exercise the complete `prepare-launch -> proxy -> fake backend` chain for
modern `0.142.4`, legacy `0.140`, unknown capabilities, config-write gating,
response masking, raw CRLF payloads, stderr, pre-EOF flush, EOF, bounded stream
drain, and nonzero exits. RED reproduced a lost 20 MB final response, a
five-second inherited-pipe hang, and an early-exit `BrokenPipeError` traceback.
The proxy now drains stdout/stderr against one two-second deadline, emits one
stable timeout diagnostic, preserves the backend exit status, and suppresses
only expected client-pipe close errors. The real-chain matrix passes 7/7 and
the complete protocol suite passes 34/34 on Python 3.9 and 3.12. Strict SAP
OpenSpec, dual-runtime compile, and `git diff --check` pass. That checkpoint
preceded the task 5.2 cleanup recorded above.

On 2026-07-24, SAP tasks 4.1-4.3 passed main-agent review and are complete.
Launcher preparation now runs through
`codex_switch_home_sync.py prepare-launch`, precomputes all required TOML,
snapshot, and Desktop settings results before mutation, removes every isolated
runtime/non-shareable symlink, and rejects relative, dangling,
self-referential, source-home, target-home, and resolved target-home-alias
shareable links while retaining absolute external links. Normal switch planning
and the pinned transaction adapter use the same classifier. The generated
wrapper pins validated Python 3.11+, contains no embedded `find`, copy/link,
TOML, or auth-deletion policy, preserves complete app-server argv, and restores
the backend's original `PYTHONPATH`. Initial RED was 4/4; review added two
failing guards for a target-home alias and malformed canonical profile config,
and all became GREEN. Fresh results are launcher-focused 10/10, shared support
3/3, profile 139/139, transaction 211/211, Config Document 24/24, runtime
binding 55/55, and protocol 27/27 on Python 3.12. Python 3.9.6 and 3.12 syntax
compile, strict SAP OpenSpec, Bash syntax, and `git diff --check` pass. SAP 5.1
real-chain E2E is next. The durable checkpoint is
`.planning/checkpoints/2026-07-24-sap-launcher-preparation-verified.md`.

On 2026-07-24, SAP tasks 3.1-3.5 passed main-agent review and are complete.
The semantic Config Document uses `tomllib`, complete source spans, parsed
quoted/dotted paths, lexical `[[skills.config]].path` identity, protected path
relations, and post-edit reparsing. Offline config merge/overlay callers now use
that seam. Current Plugin/Skill usage state remains authoritative while stale
snapshots recover support metadata only. Malformed TOML has no basic-parser
fallback; the shell resolves Python 3.11+, generated app wrappers pin a
validated interpreter, and direct Python 3.9 entry fails before store mutation.
Fresh results are Config Document 24/24, profile 136/136, runtime binding 55/55,
transaction 211/211, and protocol 27/27 on Python 3.9 and 3.12. Strict SAP
OpenSpec, Bash syntax, dual-runtime syntax compile, and `git diff --check` pass.
The first transaction run found two old invalid-TOML sentinel fixtures; the
fixtures now use valid TOML while preserving byte-exact restore and mode
assertions. Dead line-only helper definitions remain for task 5.2. This is not a
SAP completion claim: canonical launcher sync, real-chain E2E, cleanup, and
final SAP verification remain pending. Task 4.1 is next. The durable checkpoint
is `.planning/checkpoints/2026-07-24-sap-config-document-verified.md`.

Earlier on 2026-07-24, SAP tasks 2.1-2.5 passed main-agent change review and are
complete. The protocol adapter generates one backend/schema-digest-bound
capability receipt from isolated schema generation plus a temporary-home
behavioral config-write probe. The managed launcher passes only the receipt
path and expected schema digest. The proxy accepts only a regular schema-v2
receipt whose backend and schema digests match, forwards proven writes exactly
once, and rejects missing, unsafe, malformed, stale, or old-generation
receipts before backend or config-file mutation. The legacy post-response
config repair has been removed. Review repairs covered the missing `stat`
import, process-tree cleanup, bounded schema output, receipt symlink TOCTOU,
and dangling rebind-marker recovery. Fresh Python 3.9 and 3.12 protocol suites
each pass 27/27, runtime binding 55/55, and transaction 211/211. Strict SAP
OpenSpec, dual-runtime `py_compile` of 9 affected files, `git diff --check`,
and all eight review-baseline SHA-256 values pass. That checkpoint preceded the
Config Document slice.

On 2026-07-23, the `schema-scoped-app-proxy` Plugin/Skill usage-state
regression was repaired in source. The active runtime is now authoritative for
`[plugins.*]` and `[[skills.config]]`: official/internal switches and internal
Desktop restart replace those blocks exactly, including removals and
`enabled = false`. Older target runtimes, legacy profile layers, and snapshots
may recover marketplace/hook support metadata but cannot revive deleted usage
entries. Snapshot refresh retains current usage exactly. Focused RED was 8/8
expected failures; GREEN is 8/8 plus the complete 129/129 profile suite on
Python 3.9 and 3.12, protocol 17/17, focused transaction 3/3, strict OpenSpec,
compile, and diff checks. The full transaction suite remains 205/207 because
two pre-existing permission tests assume `0755` despite the current `0077`
process umask. No live profile/App/plugin/install/release/Git mutation ran, so
the source repair is not an installed-release or live-restart claim.

On 2026-07-22, `transactional-profile-state` reached a stable 154/154
transaction baseline under Python 3.9 and 3.12 plus the 123/123 legacy suite,
but independent final review rejected completion. Reviewers reproduced
store-wide recovery-gate bypasses, `init --capture-current` writes before its
lock, incomplete rollback and authoritative-terminal evidence, unjournaled
restore parent cleanup, missing recovery durability and complete preflight,
read-to-freeze and staged/produced identity gaps, path-based restore actions,
repeated-path recovery failure, and strict metadata holes. The contract-to-test
audit mapped only 14/25 required rows as covered, with 6 weak and 5 missing.

The canonical proposal, design, specification, and tasks for
`transactional-profile-state` now include the complete bound marker/journal,
immutable plan, descriptor-relative restore/recovery, lock-owned init capture,
strict state metadata, and 25-row acceptance target. `openspec validate
transactional-profile-state --strict --no-interactive` passes. The new
machine-valid Agent Task Contract is
`.planning/devflow/agent-contracts/transaction-final-review-closure.md`
(SHA-256 `de6548ce5552dc9250cecfbb1e6f4c74387dce7f2c6e58e4dfcd3a2d9ec6cd5e`).
Both independent contract reviews accepted. Final-review tasks 6.2-6.12 are now
complete: one store-wide classifier gates switch/capture/restore and is reused
by custom/init paths; rollback terminal evidence is atomic, corrupt-primary
fallback is narrowly marker-bound, and terminal-marker retry is dry-run safe
across supported and custom routes. Switch rollback/recovery effects and
terminal evidence are durable, target-home recovery identity is preflighted,
and checkpoint retries are idempotent. Restore-created parent cleanup is a
durable identity-bound journal effect; catchable and later recovery share one
engine, preserve the exact prior mode across a second interruption, preflight
the complete recovery before writing, and strictly validate the committed
terminal before marker cleanup. Switch planning inputs are now frozen as state
plus inode at their producing read and revalidated across each dependent
effect; the 14-family matrix rejects all tested drift before backup. File
replacement installs the exact phase-specific durable stage through a pinned
parent descriptor, native file/directory actions retain their produced
identity across adapter return, repeated destinations recover through their
intermediate stage/identity chain, and all deterministic file/directory
families recover after action-before-checkpoint interruption. Restore apply,
recovery, and created-parent cleanup are now route-attested,
descriptor-relative, staged-identity-bound, and idempotent after file or
directory recovery interruption. Uniform v1/v2 metadata validation now covers
every state kind/mode position, special bits, recursive directory entry counts,
both supported adopted-home authorities, and nested-home rollback retention.
`cmd_init` now keeps classification, initial managed writes, and optional
capture under one inode-revalidated store lock and uses an explicit already-held
capture dispatch. Successful switch CLI output now appends structured,
outcome-correct retained-marker guidance, and direct supported/custom/capture
contention coverage is byte-preserving. Strict switch terminal reread now
requires complete marker-bound entries, payloads, identities, effect chain, and
finalize evidence; invalid claimed commits retain recovery evidence. Failed
init capture restores the exact pre-init managed tree and modes without partial
stdout. Final review also reattests actual terminal stage state/inode/route on
both normal and exceptional writes and supports only a contiguous attested
created-parent chain for nested adopted homes. All 25 required review rows and
all 36 OpenSpec scenarios map to 111 existing named tests with no weak or
missing row. Final suites pass 207/207 on Python 3.9 and 3.12 plus 123/123
legacy, including a second dual-runtime run against unchanged hashes. All TPS
verification gates pass; `canonical-runtime-binding` is now the active change.

On 2026-06-29, the internal Desktop config-write regression was repaired.
Codex Desktop/app-server `config/value/write` and `config/batchWrite` calls are
now guarded in the internal app proxy by snapshotting the managed runtime
config before the write and restoring missing unrelated shared defaults after a
successful response, without overwriting the newly written Desktop value or
copying profile-specific model/provider settings from the snapshot. Regression
coverage was added for missing shared default restoration plus both app-server
config write methods.

The real workstation config was restored from
`/Users/cY/.codex-switch/backups/20260629T040238Z-switch-openai-official-to-internal/3-config.toml`
using the same merge helper. Pre-repair copies were saved in
`/Users/cY/.codex-switch/backups/20260629T043729Z-pre-config-preservation-repair/`.
Both `/Users/cY/.codex/config.toml` and
`/Users/cY/.codex-switch/homes/internal/config.toml` now validate as TOML and
again contain Desktop appearance settings, memories, restored enabled plugin
entries for `agent-kb@cy-codex-skills` and
`lark-feishu-ops@cy-codex-skills`, and the other missing shared support blocks
from the valid switch backup. The local release bundle was regenerated and
installed to `/Users/cY/.local/share/codex-switch/current`, and
`/Users/cY/.codex-switch/bin/codex-internal-app` now points `SWITCH_SCRIPTS` at
that installed bundle. The already-running Desktop app-server process must be
restarted by Codex Desktop before it loads the repaired proxy code.

On 2026-06-30, the official unannotated runtime seed contamination regression
was repaired. A real `codex-switch official` attempt had written
internal/Azure model-provider settings into the official profile layer and
canonical profile config even though the pre-switch official profile layer had
clean official `gpt-5.5` settings. The repair adds regression coverage for an
unannotated official runtime config that matches the internal source home,
skips that runtime seed when a clean explicit official profile layer exists,
and compares profile seeds after removing codex-switch managed comments. The
local bundle was rebuilt and installed, polluted official layer files were
backed up under
`/Users/cY/.codex-switch/backups/20260630111802-pre-official-layer-repair/`,
the clean layer was restored from
`20260630T025400Z-switch-internal-to-openai-official`, a real official switch
was verified to generate official `gpt-5.5` config without internal Azure
provider settings, and the workstation was switched back to `internal`.

On 2026-06-30, the repeated plugin/config loss after official-to-internal
switching was repaired more systemically. The root failure path was that
plugin support blocks were treated as shared config, while the canonical
profile config intentionally excluded them; if the current source home was
narrowed by another profile or Desktop write, switching back to `internal`
could use the old internal runtime only as the model/profile seed and discard
the runtime's marketplace/plugin/skill/hook blocks. The repair adds
profile-local plugin support snapshots named
`<profile>.plugin-support.config.toml`, merges previous runtime/snapshot
plugin support blocks as missing defaults when the source home lacks them, and
refreshes those snapshots from every generated runtime config, including the
managed internal Desktop wrapper path. The canonical profile config remains
profile-specific. Regression coverage was added for recovery from the target
runtime and from the profile-local snapshot after runtime loss, stale plugin
cleanup now updates snapshot files, and Desktop wrapper tests verify snapshot
refresh. Full profile-switch tests passed (90 tests), OpenSpec validated, the
local bundle was packaged and installed, and a real workstation
official-to-internal switch cycle ended active on `internal` with plugin repair
reporting no missing enabled plugins and doctor passing. The running Desktop
app-server process should still be restarted to load the updated proxy code.

After a Desktop restart on 2026-06-30, another gap was confirmed: the new
plugin-support snapshot mechanism prevented future loss only when at least one
current target runtime/snapshot still had the shared plugin blocks. The real
workstation's current official/internal runtime configs and snapshots had
already been narrowed, so the missing historical shared config was not
recovered. The official profile layer was also polluted again because the
previous official seed guard only skipped an unannotated provider runtime when
its profile seed exactly matched the internal source home; the real config was
similar but not identical. The repair now skips any unannotated
`openai-official` runtime seed containing `model_provider` when a clean
explicit official profile layer with `model` and no provider exists, and it
uses the source profile's `<profile>.plugin-support.config.toml` as shared
fallback defaults when switching profiles. Post-restart regressions were added
and verified. Current workstation configs were backed up under
`/Users/cY/.codex-switch/backups/20260630152911-pre-post-restart-shared-config-repair/`,
then restored from rich backup
`20260630T062435Z-switch-openai-official-to-internal/3-config.toml` and clean
official layers from
`20260630T065702Z-switch-internal-to-openai-official`. A real
`official -> internal` switch cycle passed. Final state: official runtime
`/Users/cY/.codex/config.toml` is `gpt-5.5` without `model_provider`;
internal runtime is Azure; both runtime/snapshot sets contain 5 marketplaces,
24 plugin blocks, and 43 hook trust blocks including agent-kb, lark-feishu-ops,
pdf, and game-design-workshop; `codex-switch --skip-self-update doctor`
passes.

Change `independent-profile-homes` has an additional verified repair for the
official/internal switch regression reported on 2026-06-24. The repair prevents
`openai-official` from using a contaminated managed runtime config as its
profile seed when a clean explicit `openai-official.config.toml` layer exists,
merges legacy profile-layer plugin support blocks into generated independent
home configs, refreshes target-home profile layers from validated runtime
configs, and adds active-profile plugin materialization checks plus
`repair-plugins <profile>` remediation. One-key `codex-switch internal` and
`codex-switch official` now run plugin repair after a successful switch and
before doctor; `--skip-plugin-repair` skips that repair step. Plugin
directories and caches remain profile-local; repair refreshes target-profile
plugin marketplace/catalog state, primes the available plugin catalog, and
installs missing enabled plugins through the target profile's configured Codex
binary only when those plugins appear in the refreshed available catalog.
Unavailable enabled plugins are skipped by repair and left for doctor to report
as active-profile materialization issues. One-key `internal --help` and
`official --help` now print help without running self-update, switch, plugin
repair, doctor, or status steps.

The repair was hardened again on 2026-06-24. `codex-switch doctor` and
`codex-switch status` now recognize the valid managed internal Desktop chain
where Codex Desktop starts `codex-internal-app`, that wrapper starts
`codex_switch_app_proxy.py`, and the proxy starts the configured internal
`codex_bin` child app-server. `repair-plugins <profile>` also has an explicit
`--disable-unavailable` cleanup path that disables missing enabled plugin
selectors only after a real catalog refresh proves they are unavailable. This
keeps normal doctor checks read-only, keeps default repair behavior
catalog-aware, and gives stale config a durable cleanup path.

The real workstation was repaired and remains active on `internal`: active
`CODEX_HOME` is `/Users/cY/.codex-switch/homes/internal`, LaunchAgent and GUI
`CODEX_CLI_PATH` point to `/Users/cY/.codex-switch/bin/codex-internal-app`,
installed `codex-switch --skip-self-update doctor` passes, and status reports
the running app-server as `/Users/cY/.local/bin/codex (via app proxy pid
29858)`. The stale unavailable `browser-use@openai-bundled` and
`dev-flow@local-personal-plugins` selectors were disabled in the live shared
config, managed internal runtime config, and internal profile layer; the
enabled `dev-flow@cy-codex-skills` cache remains present.
`pdf@openai-primary-runtime` was refreshed to `26.623.12021` and now matches
source in the updater cache verification. The source checkout passes
verification, and
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`; that
generated local bundle was explicitly installed to
`/Users/cY/.local/share/codex-switch/current`.

On 2026-06-30, the switch verification contract was implemented as change
`switch-verification-contract`. `codex-switch verify <profile>` now validates
target active state, runtime config, official provider contamination, Desktop
binding/process observations in the managed default context, plugin support
snapshots, optional runtime smoke, explicit exec smoke, and optional JSON
reports. `--repair=safe` refreshes profile-local plugin support snapshots and
uses the existing catalog-aware plugin repair path only when enabled plugins
are actually missing. One-key `codex-switch internal` and
`codex-switch official` now run a Verification section after plugin repair and
before doctor; `--skip-verify`, `--runtime-smoke`, `--exec-smoke <prompt>`,
and `--verification-report` control diagnostic and post-upgrade depth. The
full profile-switch test file passed 97 tests, OpenSpec validation passed 10
items, the release bundle was packaged and installed locally, installed
`codex-switch --skip-self-update verify internal --repair=safe --report`
passed, installed `codex-switch --skip-self-update verify internal
--repair=safe --runtime-smoke --report` passed, and installed
`codex-switch --skip-self-update doctor` passed.

Archive remains unavailable because the archive gate is closed.

On 2026-07-03, `independent-profile-homes` was extended with bidirectional
shared settings shrink prevention after switching `internal` on pinned
`0.142.4` and then back to `official` exposed missing Codex Desktop settings,
Plugins, and Skills configuration. The root cause was not the Settings UI:
wrapper startup and switch-time shared TOML generation treated a narrower
source profile config as an authoritative whole-table overlay. In practice,
`[desktop]` from the internal app home could replace the richer official
`[desktop]` table with only `followUpQueueMode`, and official switch
generation could rebuild official from a narrowed internal source while only
restoring plugin-support blocks from target runtime/snapshots. A third gap was
that plugin-support snapshot refresh could overwrite an existing rich
plugin/skill snapshot with an empty runtime-derived snapshot.

The repair changes shared TOML table overlay semantics to assignment-level
overlay: present source keys can update target keys, but missing source keys do
not delete target-only settings. Switch-time runtime config generation now
uses the target profile's last valid runtime config as full shared missing
defaults, not only marketplace/plugin/skill/hook defaults. Plugin-support
snapshot refresh now unions runtime-derived support with existing snapshots as
missing defaults, so runtime narrowing does not shrink richer snapshots without
an explicit deletion mechanism. OpenSpec scenarios and the task ledger were
updated under `independent-profile-homes`; verification evidence is recorded in
`.planning/verification/20260703215156-bidirectional-shared-settings-shrink-prevention.md`.

Verification for this repair: focused regressions failed before implementation
and passed after the fix; adjacent wrapper/plugin/official contamination
regressions passed, 14 tests; full
`python3 scripts/test_codex_profile_switch.py` passed, 120 tests;
`python3 -m py_compile scripts/*.py`, shell syntax checks,
`openspec validate independent-profile-homes --strict --no-interactive`,
`openspec validate --all --strict --no-interactive`, `git diff --check`, and
`scripts/package-release.sh` all passed. The local installed bundle was
refreshed with
`CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh`, and
installed `codex-switch --skip-self-update status` passed. That status check
also reported the pre-existing current-shell `PATH codex` mismatch and
recommended `eval "$(codex-switch shim-env)"` to align this shell.

On 2026-07-03, a new internal Azure Responses failure was diagnosed after an
internal-profile backend update surfaced the service message `The requested
item was created under a different Azure OpenAI resource. Use the same
resource that created the item to access it.` Fresh internal threads also
failed, so the symptom is not stale conversation state. A local plain-text
internal `codex exec --json` smoke succeeded, while a smoke that forced a shell
tool call and tool-result follow-up reproduced the error. Client tracing showed
the initial `/responses` request succeeded on
`x-account-id: globalttswedencentral010`, while the follow-up failed after
being routed to `x-account-id: globalttswedencentral053` for the same returned
deployment. The detailed sanitized evidence is recorded in
`.planning/verification/20260703112226-internal-azure-resource-stickiness-diagnosis.md`.

Current diagnosis: AIDP is not keeping a Responses context sticky to one Azure
OpenAI resource across tool-result follow-up requests. codex-switch does not
currently proxy model HTTP `/responses` traffic, so the durable upstream fix is
AIDP/backend resource stickiness or a supported sticky routing mechanism. The
local codex-switch gap is verification: `--runtime-smoke` does not exercise a
Responses tool-follow-up path, and `--exec-smoke` only catches the problem when
the caller supplies a tool-forcing prompt.

DevFlow project migration sync was re-run on 2026-07-03 before this repair.
The sync completed successfully and still reports `migration_pending` for the
official skill-layout migration, with legacy duplicates and conflicts between
`.codex/skills` and `.agents/skills`. Runtime and stored DevFlow versions are
both `0.3.0+codex.20260529145038`; no migration apply command was run because
the current repair does not need project-local skill-layout mutation.

The local repair was then implemented as OpenSpec change
`internal-responses-resource-stickiness`. `codex-switch verify <profile>` now
supports `--responses-tool-smoke`, which runs a deterministic ephemeral
`codex exec --json` smoke that forces a harmless shell tool call and
tool-result follow-up using the target profile `CODEX_HOME`. One-key
`codex-switch internal` and `codex-switch official` forward
`--responses-tool-smoke` into post-switch verification. Azure resource mismatch
output is diagnosed as an internal Responses resource-stickiness failure, and
JSON reports record only sanitized routing fields: `x-account-id`,
`x-account-deployment`, `x-model-request-id`, and `x-tt-logid`.

The scenario is documented in
`docs/troubleshooting/internal-azure-responses-resource-stickiness.md` and
linked from `README.md`. `scripts/package-release.sh` now includes `docs/` in
release bundles so the troubleshooting note ships with the installed tool.
Verification evidence is recorded in
`.planning/verification/20260703114321-internal-responses-resource-stickiness.md`.
The full profile-switch test file passed 102 tests, Python compile checks
passed, shell syntax checks passed, OpenSpec validated 11 items, `git diff
--check` passed, the release bundle was generated, and the local installed
codex-switch was refreshed from `/Users/cY/dev/codex-switch/dist/codex-switch`.
Installed help confirms `--responses-tool-smoke` is available for both
standalone `verify` and one-key switch flows.

## Next Action

Use
`codex-switch --skip-self-update verify internal --responses-tool-smoke --report`
after internal backend upgrades or when internal Desktop fails after a tool
call. If it reports an internal Responses resource-stickiness failure, hand the
sanitized account/deployment/request/log IDs to the AIDP/internal backend owner.
The upstream repair remains with AIDP or the internal backend: Responses
follow-up/retry requests that share context must be routed to the same Azure
OpenAI resource, or the backend must provide a supported sticky routing key.
Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened. Separate follow-ups remain available for
project-local DevFlow skill layout migration and external `gsd-core` update,
but they are outside this repair.

On 2026-07-03, the internal Desktop startup crash after `codex-switch i` was
diagnosed and repaired under OpenSpec change `internal-app-protocol-compat`.
Desktop logs showed the first internal app-server after the switch reported
`0.142.4`, initialized, routed `plugin/list`, then closed stdio with exit code
`241`. Desktop's retry reported `0.142.5`, routed the same `plugin/list` flow,
logged the same featured plugin `401 Unauthorized` warning, and stayed
connected. The warning is therefore a noisy last stderr line from an
unauthenticated featured-plugin fetch, while the local health gap was that
codex-switch did not verify the Desktop app-server startup window after an
internal backend auto-update.

The repair adds `codex-switch verify <profile> --app-server-smoke`. The smoke
starts the profile `codex_bin app-server --analytics-default-enabled` with the
target profile `CODEX_HOME`, sends `initialize`, `initialized`, and a
Desktop-like `plugin/list` request, then waits briefly for the process to stay
healthy. JSON-RPC auth errors from `plugin/list` are accepted as responses; a
non-zero app-server exit such as `241` fails verification with bounded
stdout/stderr context. One-key `codex-switch internal` now automatically adds
`--app-server-smoke` to post-switch verification when the internal update check
actually ran an auto-update. Users can also request it explicitly for manual
internal backend rebinding or upgrades.

Verification evidence is recorded in
`.planning/verification/20260703060556-internal-app-protocol-compat-startup-smoke.md`.
The focused red tests failed before implementation for the missing
`--app-server-smoke` flag and missing one-key auto-update forwarding. Focused
green tests passed for plugin-list auth error success, exit-code `241`
failure, and automatic one-key internal auto-update smoke. Neighbor verifier
smoke tests passed, the full profile-switch regression suite passed 104 tests,
Python and shell syntax checks passed, OpenSpec validated all 11 items, `git
diff --check` passed, and a direct real internal app-server smoke returned
`code=0` with `app-server smoke passed`. The release bundle was regenerated
and installed locally; installed `codex-switch --skip-self-update internal
--help` lists `--app-server-smoke`.

`scripts/validate_workflow_state.py` is still unavailable in this checkout, so
that gate is recorded as unavailable rather than executed. Archive remains
unavailable because the archive gate is closed. Do not archive until the gate
is explicitly opened.

On 2026-07-03, the internal Desktop settings sync gap after switching to
`internal` was diagnosed and repaired under OpenSpec change
`independent-profile-homes`. `config.toml` shared settings were already syncing;
the missing values were Desktop/Electron UI settings stored in
`.codex-global-state.json`. That file had been excluded wholesale from
cross-home sync with credentials and runtime state, which protected prompt
history and thread state but also prevented safe settings such as window bounds,
hotkeys, sidebar state, and composer preferences from following the internal
home.

The repair keeps `.codex-global-state.json` excluded from generic shared
support copy/link plans, then merges only a sanitized Desktop settings subset.
Top-level Desktop settings and allowlisted `electron-persisted-atom-state`
settings are copied; prompt history, thread permissions, prompt drafts, queued
follow-ups, remote thread summaries, unread-thread state, thread client IDs,
credentials, and remote routing identifiers remain profile-local. Independent
switch flows now run this merge in both directions, and the generated internal
Desktop wrapper runs the same helper on startup. README and the
`independent-profile-homes` design/spec/tasks were updated.

Verification evidence is recorded in
`.planning/verification/20260703174622-desktop-global-settings-state-sync.md`.
The new focused regressions failed before implementation for the missing merge
helper, missing switch-created state file, and stale wrapper state, then passed
after implementation. Adjacent shared-state/wrapper isolation regressions
passed, the full profile-switch suite passed 107 tests, Python compile and
shell syntax checks passed, OpenSpec strict validation passed all 11 items,
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`, and `git
diff --check` passed. The installed bundle was refreshed with `./install.sh`.

The current workstation internal home was repaired without changing the active
profile by merging the sanitized settings subset from `/Users/cY/.codex` into
`/Users/cY/.codex-switch/homes/internal/.codex-global-state.json`. A key-only
safety check showed no copied prompt-history, thread permission, draft,
unread-thread, remote-summary, or thread-client-id atom keys. Current
`codex-switch --skip-self-update status` still reports active profile
`openai-official`. Archive remains unavailable because the archive gate is
closed; do not archive until the gate is explicitly opened.

On 2026-07-03, the user clarified that the missing settings were the Codex
Desktop Settings sidebar categories: General, Appearance, Configuration,
Personalization, Pets, and Keyboard shortcuts. A follow-up audit showed
General/Appearance/Configuration/Personalization settings were covered by the
existing `config.toml` and sanitized `.codex-global-state.json` sync, but
`pets/` was still excluded from shared support despite backing the user-facing
Pets settings panel.

The repair keeps plugin caches, credentials, browser/process state, sqlite
state, sessions, histories, secrets, and model catalogs excluded, but removes
`pets` from the Python and generated-shell non-shareable lists so the existing
shared-support sync/link logic handles it. Regression tests were added for
switch-time `pets/` sync and generated internal Desktop wrapper startup sync.
README and the `independent-profile-homes` OpenSpec design/spec/tasks were
updated.

Plugins/Skills were audited at the same time. Official and internal
`config.toml` currently have matching plugin/marketplace/hook/MCP config
counts: 25 plugins, 5 marketplaces, 43 hooks, and 2 MCP entries. Internal
`skills` is a symlink to `/Users/cY/.codex/skills`. Internal `plugins` remains
a profile-local cache directory by design; `codex-switch --skip-self-update
repair-plugins internal --dry-run` reports no missing enabled plugins. DevFlow
plugin-project migration sync-only still reports `migration_pending` because
of legacy `.codex/skills` duplicates/conflicts with `.agents/skills`; no apply
was run.

Verification evidence is recorded in
`.planning/verification/20260703181220-settings-panel-pets-plugins-skills-sync.md`.
The focused `pets/` regressions failed before implementation and passed after
the fix. Adjacent settings/shared-support/wrapper/plugin regressions passed,
the full profile-switch suite passed 109 tests, Python compile and shell
syntax checks passed, OpenSpec strict validation passed all 11 items,
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`, and `git
diff --check` passed. The installed bundle was refreshed with `./install.sh`.
The current workstation internal home now has
`/Users/cY/.codex-switch/homes/internal/pets -> /Users/cY/.codex/pets`, and
the active profile remains `openai-official`.

On 2026-07-03, after the user reported that switching to `internal` still
showed `The requested item was created under a different Azure OpenAI resource`,
the live issue was rechecked. The installed `codex-switch` initially did not
show `--responses-tool-smoke` because `./install.sh` had been run without
`CODEX_SWITCH_SOURCE_DIR`, so it installed the latest GitHub release instead of
the current working-tree repair. On the 2026-07-03 20:00 CST recheck, installed
`codex-switch --skip-self-update verify internal --responses-tool-smoke
--report` again failed before verification with `unrecognized arguments:
--responses-tool-smoke`, confirming installed bundle drift. The working-tree
wrapper reproduced the backend failure and wrote
`/Users/cY/.codex-switch/verification/20260703T115956Z-internal.json`. The
current working tree was then installed explicitly with
`CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh`, and
installed `verify --help` now includes both `--responses-tool-smoke` and
`--app-server-smoke`.

`codex-switch --skip-self-update verify internal --responses-tool-smoke
--report` wrote
`/Users/cY/.codex-switch/verification/20260703T120052Z-internal.json` after
the install refresh. Because the active profile had already returned to
`openai-official`, the report also contains active-profile mismatch
diagnostics. The Responses smoke nevertheless reproduced and classified the
user-visible error as
`internal Responses resource-stickiness failure; Responses context follow-up
must stay on the same Azure OpenAI resource`. No account/deployment headers
were present in this repro, but the diagnostic kind is
`azure_responses_resource_mismatch`.

Verification evidence is recorded in
`.planning/verification/20260703110316-internal-responses-stickiness-live-repro.md`.
This is not the previous plugin/list app-server crash and not the
Settings/Plugins/Skills sync issue. The remaining durable repair belongs in
AIDP/internal backend routing: Responses context follow-up requests must stay
on the same Azure OpenAI resource, or the backend must expose a supported sticky
routing key. Archive remains unavailable because the archive gate is closed.

On 2026-07-03, the Lark internal Codex setup document
`OOYBdDO2MoSU7nxb8iLcQAWMnPf` was checked against the current
`codex-switch` internal profile. The document says internal mode must use the
script-installed internal Codex CLI, write Azure ModelHub provider config
(`https://aidp.bytedance.net/api/modelhub/online`, `wire_api = "responses"`,
AK query param), and force Codex Desktop to use the internal CLI via a
LaunchAgent `CODEX_CLI_PATH` override. The referenced LaunchAgent Wiki
`GfnEwy3u3ixJ9bk0bvxco8msnIb` describes the same
`~/Library/LaunchAgents/com.openai.codex-cli-path.plist` mechanism used by
`codex-switch`.

Verification evidence is recorded in
`.planning/verification/20260703201031-internal-profile-doc-procedure-check.md`.
Current live state remains `openai-official`: LaunchAgent and running
app-server point to `/Applications/Codex.app/Contents/Resources/codex`.
Stored internal profile state matches the document's contract with an extra
codex-switch Desktop wrapper layer:
`codex_bin=/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex`,
`app_cli_path=/Users/cY/.codex-switch/bin/codex-internal-app`, and internal
config uses `model_provider = "azure"`, ModelHub base URL, Responses wire API,
and a present AK query param. Conclusion: the stored internal profile setup is
equivalent to the document's required local setup, but the current live machine
is intentionally back on official. The remaining Azure resource mismatch occurs
after local internal binary/provider selection, inside AIDP/internal backend
Responses follow-up routing.

On 2026-07-03, the internal profile was experimentally rolled back from the
latest internal Codex release `0.142.5` to the previous release `0.142.4`.
GitHub `SDGLBL/codex` releases show latest `internal-rust-v0.142.5` and
previous `internal-rust-v0.142.4`. Local `/Users/cY/.local/bin/codex` already
contained `codex-cli 0.142.4`, so the internal profile was rebound with
`codex-switch --skip-self-update set-bin --preserve-app-cli internal
/Users/cY/.local/bin/codex`, then activated with
`codex-switch --skip-self-update internal --skip-update-check --skip-doctor
--no-status` to avoid auto-updating back to 0.142.5. The internal manifest,
switch shim, and generated Desktop wrapper now delegate to
`/Users/cY/.local/bin/codex`.

Verification evidence is recorded in
`.planning/verification/20260703205658-internal-bin-rollback-01424-smoke.md`.
The working-tree verifier command
`./scripts/codex-switch --skip-self-update verify internal --app-server-smoke
--responses-tool-smoke --report` wrote
`/Users/cY/.codex-switch/verification/20260703T125615Z-internal.json`.
With 0.142.4, both `App-server smoke` and `Responses tool smoke` passed; the
report has no smoke diagnostics. The only remaining verification issues are
that the currently running Codex Desktop/app-server processes still use
`/Applications/Codex.app/Contents/Resources/codex` and must be fully quit and
reopened to inherit `/Users/cY/.codex-switch/bin/codex-internal-app`. Current
shell `PATH` still resolves bare `codex` first from the older internal
plugin-appserver path at 0.142.5, so profile-bound commands are corrected but
current-terminal bare `codex` resolution remains a separate shell environment
detail.

On 2026-07-03, the previous internal release `0.142.4` was reinstalled through
the real internal installer flow instead of reusing the existing local binary.
Preflight confirmed the internal install AK was present without printing it,
and dry-run confirmed the pinned install target
`codex-switch --skip-self-update update-internal --version 0.142.4
--install-dir /Users/cY/.local/bin`. A preinstall backup was written under
`/Users/cY/.codex-switch/backups/20260703T210044-pre-reinstall-internal-0.142.4`.
The real installer downloaded Codex CLI and bundled rg, resolved version
`0.142.4`, installed to `/Users/cY/.local/bin`, and configured internal Azure
provider settings. The preinstall and postinstall sha256 were both
`8bdbbf4b1a3b391425fcda4e86537805e51ddea97d896a563eaa1494c4eef6f1`, so the
previous local 0.142.4 binary was not corrupt, but the download/install flow
was fully re-run.

Verification evidence is recorded in
`.planning/verification/20260703210228-internal-bin-01424-reinstall.md`.
After reinstall, `codex-switch --skip-self-update set-bin --preserve-app-cli
internal /Users/cY/.local/bin/codex` and
`codex-switch --skip-self-update internal --skip-update-check --skip-verify
--skip-doctor --no-status` reactivated the profile without auto-upgrading back
to 0.142.5. Current internal manifest, switch shim, and Desktop wrapper all
delegate to `/Users/cY/.local/bin/codex`, which reports `codex-cli 0.142.4`.
`codex-switch --skip-self-update verify internal --app-server-smoke
--responses-tool-smoke --report` wrote
`/Users/cY/.codex-switch/verification/20260703T130213Z-internal.json`; both
smokes passed. The report remains `ok=false` only because the already-running
Desktop/app-server processes still use the official app bundle and need a full
Desktop quit/reopen to inherit `/Users/cY/.codex-switch/bin/codex-internal-app`.
The current terminal's bare `codex` still resolves first to the old
plugin-appserver 0.142.5 path, which is separate PATH-ordering drift from the
profile-bound shim/wrapper state.

On 2026-07-03, `internal-app-protocol-compat` was extended with a blocked
release policy for internal Codex CLI `0.142.5` and shell CLI alignment
diagnostics. The user confirmed that switching back to internal `0.142.4`
works, so `0.142.5` is now treated as a known-bad default update target.
`codex-switch internal` keeps or installs pinned fallback `0.142.4` while
GitHub latest remains `internal-rust-v0.142.5`; when latest advances to a
successor release, one-key internal switching resumes the ordinary unpinned
latest auto-update path. Direct `codex-switch update-internal` also pins to
`0.142.4` by default when latest is blocked, unless the caller explicitly
passes `--version`.

`codex-switch status` now reports whether bare command-line `codex` resolves
to the codex-switch shim. `codex-switch shim-env` prepends the shim directory
and clears the shell command cache with `hash -r`. Installed status currently
shows active profile `openai-official`; the current terminal's `PATH codex`
still points first to the old internal plugin-appserver binary, but status now
reports that as a mismatch and prints
`eval "$(codex-switch shim-env)"`. In a child shell after applying that command,
`which codex` resolves to `/Users/cY/.codex-switch/bin/codex` and status
reports `PATH codex alignment: ok`.

Verification evidence is recorded in
`.planning/verification/20260703212846-internal-01425-block-pin.md`. The new
focused regressions failed before implementation for missing blocked-release
handling and missing PATH alignment status, then passed after implementation.
The focused Slice 7 tests passed, the adjacent one-key auto-update app-server
smoke test passed, the full profile-switch regression suite passed 114 tests,
Python compile checks passed, shell syntax checks passed, `git diff --check`
passed, OpenSpec strict validation passed all 11 items, workflow validation
reported `ok=true`, the release package was regenerated, and the local
installed codex-switch was refreshed from this checkout. Installed
`codex-switch --skip-self-update check-update internal` now reports latest
`0.142.5` as blocked and skips updating `/Users/cY/.local/bin/codex` away from
`0.142.4`. Installed
`codex-switch --skip-self-update update-internal --dry-run` shows pinned
version `0.142.4`.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.

On 2026-07-03, `always-check-self-update` was extended with version-ordered
self-update after `codex-switch internal` re-downloaded internal Codex
`0.142.5`. The root cause was that the installed local-source `codex-switch`
repair was overwritten by the published `0.1.12` bundle because wrapper
self-update replaced the implementation whenever bundle `VERSION` strings were
different. The correct contract is version ordering: a release bundle should
replace the installed implementation only when the release version is newer.

`sync_self_update` now compares current and staged bundle versions by ordering.
Same-version and older-release checks remove the staged bundle and report the
current implementation as already up to date; newer releases still sync and
re-exec. Prerelease ordering treats `0.1.13-dev` as newer than `0.1.12` but
older than formal `0.1.13`, so a future real release can still take over. The
temporary local-source marker path was removed from `install.sh` and
`scripts/codex-switch`. The local checkout `VERSION` is now `0.1.13-dev`.
Active profile was not switched and is expected to remain `openai-official`.

Verification evidence is recorded in
`.planning/verification/20260703221616-version-ordered-self-update.md`.
Focused RED tests failed before implementation and passed after the fix. The
full profile-switch regression suite passed 123 tests; Python compile checks,
shell syntax checks, `git diff --check`, `scripts/package-release.sh`,
`openspec validate always-check-self-update --strict --no-interactive`,
`openspec validate internal-app-protocol-compat --strict --no-interactive`, and
`openspec validate --all --strict --no-interactive` all passed. Installed
`codex-switch check-update internal` ran self-update without
`--skip-self-update`, reported local `0.1.13-dev` already up to date, and kept
internal Codex at `0.142.4` while blocking latest `0.142.5`. DevFlow
plugin-project-migration reported `ok=true` with control plane current, but
existing skill-layout duplicate/conflict migration findings remain and were
left untouched.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.

On 2026-07-03, `internal-app-protocol-compat` was extended again so profile
switches automatically prepare command-line `codex` alignment instead of only
diagnosing PATH drift after the fact. When a switch updates the
`~/.codex-switch/bin/codex` shim, codex-switch now installs or refreshes a
marker-managed shell startup block. The block prepends the store `bin`
directory to PATH and runs `hash -r` when the shell supports it. Existing shell
profile content outside the managed block is preserved, repeated switches
replace the block instead of duplicating it, and
`CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP=1` skips the mutation for controlled
environments. The shell profile path is also included in independent switch
dry-run/backup plans when it will be mutated.

The implementation deliberately does not overwrite whichever `codex` binary is
currently first on PATH. That path may be a plugin cache binary or another
user-managed install, and replacing it would be unsafe. A child
`codex-switch` process also cannot mutate the already-running parent shell's
in-memory PATH, so current-shell drift remains visible through
`codex-switch status` and can still be repaired immediately with
`eval "$(codex-switch shim-env)"`; newly opened shells will inherit the managed
bootstrap after the next real switch.

Verification evidence is recorded in
`.planning/verification/20260703213928-switch-shell-bootstrap-alignment.md`.
The focused regressions failed before implementation for missing switch-time
bootstrap installation and missing managed-block replacement, then passed after
implementation. The Slice 8 focused tests passed, adjacent CLI alignment and
internal blocked-update tests passed, the full profile-switch regression suite
passed 117 tests, Python compile checks passed, shell syntax checks passed,
`git diff --check` passed, OpenSpec strict validation passed all 11 items, the
release package was regenerated, and the local installed codex-switch was
refreshed from this checkout. Installed dry-run evidence with
`CODEX_SWITCH_SHELL_PROFILE=/tmp/codex-switch-shell-bootstrap-check.zshrc`
shows the shell profile path in both backup and mutation plans. No real
workstation profile switch was run during this verification; active profile
remains `openai-official`.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.

## 2026-07-22 DevFlow Refresh and Core Implementation Review

The targeted global `dev-flow@cy-codex-skills` cache was refreshed to
`0.3.0+codex.20260529145038` and verified `matches-source`. Project-local
DevFlow/OpenSpec dependencies were refreshed in the supported isolated flow;
all required links and six OpenSpec 1.6 skills were already current. Durable
template drift for the Matt methodology contract and bounded-subagent contract
was merged into `AGENTS.md`. Workflow validation reports `ok=true`; legacy
`.codex/skills` duplicate cleanup and root-state migration remain explicitly
deferred.

A read-only review of the current core implementation found no P0, but it did
find concrete P1 correctness and state-safety issues. The leading root causes
are fragmented profile transaction semantics, contradictory runtime/App
ownership sources, non-fail-safe install/update/release promotion, schema-blind
App-server transformations, plugin catalog parse failures that can become
writes, and verification paths that can false-pass or persist raw secrets.
Existing verification remains green: 123 regression tests passed, OpenSpec
strict validation passed all 11 items, and source syntax checks passed. Those
tests do not cover the identified failure branches.

Durable findings, refresh receipts, architecture deepening candidates,
validation commands, and residual risks are recorded in
`.planning/verification/20260722113700-dev-flow-refresh-and-core-implementation-review.md`.
No production implementation, real profile switch, release, commit, push,
provider migration, legacy cleanup, or root-state migration was performed.

## 2026-07-22 Core Systemic Repair Planning Checkpoint

The user authorized implementation of the systemic review route and clarified
two product boundaries: only official/internal profiles are in scope, and the
current merged Desktop product is `/Applications/ChatGPT.app`. Arbitrary-profile
path hardening is deferred. ChatGPT.app with bundle id `com.openai.codex` is the
only current healthy host; Codex.app is migration observation only and ChatGPT
Classic is excluded.

Four Full OpenSpec changes are complete and strict-valid:

- `transactional-profile-state`
- `canonical-runtime-binding`
- `schema-scoped-app-proxy`
- `fail-safe-update-release`

Current evidence includes installed official/internal generated schemas, the
real ChatGPT app-server command shape with global options before the subcommand,
and an isolated internal `0.142.4` temporary-home write probe. That probe
returned a canonical versioned response and preserved unrelated MCP,
marketplace, plugin, and skill entries. Therefore the approved proxy design no
longer performs local post-response recovery: proven writes remain
backend-owned, and unproven writes fail before forwarding.

The active goal, scope/non-goals, finding map, serialized dependency order,
Human Gates, and validation contract are recorded in `TASK_LEDGER.md`.
Implementation and verification remain incomplete; no live workstation switch,
rebind, install, update, release, or Git publication action has run.

### Next Action

Apply `transactional-profile-state` through its task list and a validated Agent
Task Contract. Record each RED/GREEN cycle, review the diff, and pass focused
verification before advancing to `canonical-runtime-binding`.

## 2026-07-22 Transaction Restore Core Review Checkpoint

The first implementation slice is reviewed and dependency-ready for capture.
The store-directory lock, transaction receipt, recursive path attestations,
schema-v2 restore reader/writer boundaries, v0/v1 compatibility rejection,
complete restore preflight, safety backup, ordered apply/reverse rollback,
payload-copy verification, parent cleanup journal, and failure evidence are now
implemented. Review-discovered Python 3.9 incompatibility, initial-state TOCTOU,
terminal-parent escape, parent symlink redirection, weak finalization checks,
and rollback residue received focused RED/GREEN regressions.

Default Python 3.9 and Python 3.12 each pass all 41 transaction tests; syntax
and `git diff --check` pass. A fresh full 123-test legacy suite also passed
after the final focused hardening. Tasks 1.2-1.4 and 2.3-2.5 are complete.
Tasks 1.1, 2.1, and 2.2 stay
open because the supported snapshot/switch caller still owns an unfinalized
prepared backup outside the transaction seam.

### Next Action

Execute transactional capture tasks 3.1-3.4 through a separately validated
Agent Task Contract. Preserve unmanaged profile artifacts, remove stale auth
only under the approved missing-auth policy, and prove directory-exchange and
finalization rollback before migrating `cmd_capture` and indirect init callers.

## 2026-07-22 Transaction Capture Review-Fix Checkpoint

The initial capture slice reached 50/50 transaction tests on both default
Python 3.9 and Python 3.12, and the independently rerun legacy suite passed
123/123. Source preflight, cloned sibling staging, allowed-missing stale-auth
removal, unmanaged-artifact preservation, directory exchange, journal recovery,
and successful CLI-output compatibility are implemented, but the slice is not
accepted yet.

Two independent reviews reproduced safety gaps that the green suite did not
cover: cloned managed symlinks can write outside the stage; required auth can
disappear after preflight and still permit commit; rollback can install an
unattested replacement; and committed cleanup failure can be reported as a
failed operation after the new profile is already permanent. Additional
hardening is required for atomic lock-root creation, profiles-parent identity,
stage cleanup, causal error evidence, exact journal schema typing, independent
recovery proof, and journal/rename durability ordering.

The validated `transaction-capture-review-fixes` Agent Task Contract now owns
only the transaction module/test and capture adapter. No switch/Desktop task
may start until these review findings receive focused RED/GREEN evidence and
the capture slice passes independent re-review.

### Next Action

Complete the capture review-fix contract, independently rerun dual-version
transaction tests plus the 123-test legacy suite, and re-review the resulting
capture diff. Only then close tasks 3.1-3.4 and transfer the shared transaction
files to the validated switch/effects contract.

## 2026-07-22 Transaction Capture Accepted Checkpoint

Transactional capture tasks 3.1-3.4 are accepted on stable SHA-256
`807a95249b06547c` for `codex_switch_transaction.py`, `fe8f4dfcbe3c4a5a`
for `test_codex_transaction.py`, and `902e57b9723eddae` for
`codex_switch_capture.py`. The final capture path freezes unmanaged and managed
expectations before injectable writes, uses a pinned descriptor for profile
workspace operations, validates canonical prepared/committed journal bytes,
restores a verified previous profile before classifying unknown staging
artifacts, and checks the complete terminal artifact vector before any clean
claim. A committed marker becomes durable only after both journal-file and
profiles-parent fsync; pre-commit rollback first durably restores the prepared
marker. Existing-profile capture preview now pins the workspace read-only and
performs zero writes.

Main independently passed 86/86 transaction tests on both default Python 3.9
and Python 3.12, the complete 123-test legacy suite, dual-version compilation,
strict OpenSpec validation, and diff/whitespace checks. Independent spec and
engineering reviewers found no actionable P0-P3 on the final hashes. The
engineering review additionally passed 20 finalize exception/crash-retry
cases, 8 prepared-downgrade interruption cases, all terminal-vector checks,
and existing/missing-profile dry-run zero-write checks.

Residual boundaries are explicit: the capture-only descriptor seam does not
rewrite restore/backup or pin store-root ancestry through a single dirfd, and
no finite operation claims protection from an arbitrary same-UID mutation
after its final filesystem instruction. `cmd_init`'s pre-existing non-capture
initialization writes remain outside the capture sub-transaction. No live
profile, App, launchctl, install, update, release, or Git mutation was run.

### Next Action

Transfer the shared transaction files to the validated
`transaction-switch-effects-implementation` contract. Implement tasks 1.1,
2.1-2.2, and 4.1-4.6 with immutable switch planning, schema-v2 committed
snapshot backups, binding preflight before backup, fake Desktop-effect
adapters, active-record-last commit, and reverse rollback. Preserve the custom
profile compatibility path and run no real launchctl or workstation switch.

## 2026-07-23 Transaction Recovery Classifier Checkpoint

Final-review task 6.2 is complete. DevFlow dependency readiness was restored by
copying only the missing project-local pinned `diagnosing-bugs` skill; no
official install, provider migration, or legacy-skill cleanup ran. One
classifier now examines bound pending markers, marker-required missing-marker
journals, markerless legacy switches, pre-marker restores, and capture journals
under the store lock before supported dispatch. Custom and init compatibility
paths consult the same classification result before their first write.

Focused RED tests reproduced three independent bypasses: cross-operation
capture ignored a begun switch whose required marker was missing, the custom
gate ignored a pre-marker restore, and init wrote files before rejecting the
same evidence. GREEN coverage additionally proves safe effect-free
switch/restore closure, begun restore blocking, legacy markerless recovery in
the presence of corrupt historical backup data, `prepared|rollback_failed`
pre-marker blocking, corrupt/multiple evidence failure, capture-journal gates,
and dry-run byte identity. The complete transaction suite passes 164/164 on
both Python 3.9 and Python 3.12; strict OpenSpec, dual-runtime AST, and diff
checks pass. Evidence is recorded in
`.planning/devflow/verification/transactional-profile-state.md`.

The slice does not claim the still-open contracts: terminal/fallback marker
evidence is task 6.3, full recovery durability and preflight are 6.4-6.5,
identity-bound planning/materialization are 6.6-6.9, and a single held lock for
all init writes plus capture is 6.10. No live profile/App/launchctl, install,
update, release, or Git publication action ran.

### Next Action

Execute task 6.3 by TDD: reproduce inconsistent switch rollback terminal
evidence, validate a narrowly bound `failure.json` fallback, preserve
outcome-correct marker cleanup guidance, and retire valid terminal markers on
the custom route without weakening corrupt-evidence failure.

## 2026-07-23 Transaction Terminal Evidence Checkpoint

Final-review task 6.3 is complete. Switch rollback terminalization now updates
the outer manifest lifecycle and embedded journal state in the same atomic
manifest write. When that primary manifest cannot be read, recovery accepts
only a verified `rolled_back` failure receipt whose operation, backup and
transaction IDs, marker name, prepared-journal digest, marker requirement, and
journal terminal state all bind to the trusted marker. Mismatched or
`rollback_failed` fallback evidence remains corrupt/ambiguous and causes no
store writes.

Retained-marker diagnostics now name `committed` or `rolled_back` accurately
and state that the next applying command will retry cleanup. Dry-run leaves the
terminal marker and complete store byte identity unchanged; the next applying
supported transaction or custom gate validates and retires it before the new
write path proceeds. Focused positive and negative regressions pass, followed
by 168/168 transaction tests twice on both Python 3.9 and Python 3.12 against
stable source hashes. Strict OpenSpec, dual-runtime AST, and diff checks pass.
No live profile/App/launchctl, install, update, release, or Git publication
action ran.

### Next Action

Execute task 6.4 by TDD: prove switch rollback/recovery durability, simulate the
complete prepared recovery before its first write, bind target-home ensure
identity, handle an already-restored Desktop retry, and cover every required
prepared/marker/intent/action/applied/terminal/cleanup interruption point.

## 2026-07-23 Transaction Switch Recovery Durability Checkpoint

Final-review task 6.4 is complete. Switch rollback and prepared recovery now
verify each restored result, make its file/tree and parent directory durable,
then publish and sync one terminal manifest. Each effect receives a terminal
`recovered` or conservative `rollback_failed` state. A failed marker unlink
whose parent-sync durability is uncertain republishes the exact bound marker,
so the visible warning and next-apply retry contract remain true.

Prepared recovery simulates ordinary effects and Desktop state and now also
validates target-home ensure identity before its first write. A Desktop already
restored to the predecessor state is accepted without replay. Direct tests
cover prepared journal, marker publication, intent, action, applied, terminal,
marker unlink, parent sync, recovery durability interruption/re-entry, corrupt
later payload, foreign produced identity, and rollback durability failure.
Both Python 3.9 and Python 3.12 pass 176/176 twice against stable hashes;
strict OpenSpec, Python 3.9 AST, and diff checks pass. No live profile/App,
launchctl, install, update, release, or Git publication action ran.

### Next Action

Execute task 6.5 by TDD: make restore parent cleanup a first-class durable
journal effect, share catchable rollback and next-invocation recovery, prove
second-interruption idempotence and exact prior-mode recreation, preflight the
complete restore recovery plan, and strictly reread terminal evidence before
marker cleanup.

## 2026-07-23 Transaction Restore Recovery Durability Checkpoint

Final-review task 6.5 is complete. Restore-created parent cleanup is now an
identity-bound journal effect with durable intent, action observation, and
applied checkpoints. Catchable rollback and next-invocation recovery use the
same prepared-restore engine. They recreate the exact prior directory mode,
persist the recovery-produced identity, and resume idempotently after a second
hard interruption.

Prepared restore recovery validates all safety entries, payloads, target
effects, created-parent identities, and cleanup-parent identities before its
first write. Normal completion and the catch path accept a committed restore
only after one strict marker-bound reread validates the full effect chain,
current target results, removed cleanup parents, and absent staging material.
Focused tests cover cleanup ordering and durability, catchable failure, exact
`0751` recreation, second interruption, zero-write preflight rejection,
legacy v1 file/symlink compatibility, nested parent cleanup, and corrupt or
unbound terminal evidence. Python 3.9 and Python 3.12 each pass 181/181;
strict OpenSpec, dual-runtime AST, stable hashes, and tracked/untracked diff
checks pass. No live profile/App/launchctl, install, update, release, or Git
publication action ran.

### Next Action

Execute task 6.6 by TDD: freeze every direct and indirect plan input at its
producing read, including Desktop read-modify-write state, and reject any
read-to-effect drift before the dependent mutation.

## 2026-07-23 Transaction Producing-Read Freeze Checkpoint

Final-review task 6.6 is complete. A single planning-input tracker captures
the complete state and device/inode identity immediately before a value is
read to produce the plan, verifies the same evidence immediately after that
read, persists it in the switch journal, and revalidates it before intent and
after action. Planned replacement paths may acquire the produced inode while
unchanged inputs must retain the original inode.

The exact mandatory test
`test_planning_reads_are_frozen_atomically_for_every_switch_input` first
reproduced all 14 gaps: product manifest, active state, profile/base/target and
indirect composite configs, auth bytes, plugin snapshot, Desktop global-state
source and target RMW state, shell profile, shared-support enumeration, stale
runtime link, and executable binding all completed without raising after the
producing read changed. All cases now reject before backup creation and retain
the externally newer source or target. The hard-interruption-after-terminal
compatibility regression confirms a planned same-content replacement may use
its new inode without weakening unchanged-input identity checks.

Python 3.9 and Python 3.12 each pass 182/182. Strict OpenSpec, dual-runtime
AST, stable hashes, and tracked/untracked diff checks pass. No live
profile/App/launchctl, install, update, release, or Git publication action ran.

### Next Action

Execute task 6.7 by TDD: install the exact persisted staged object, validate
its produced identity before `applied`, make repeated-path predecessor chains
recoverable, and cover action-before-checkpoint interruption for every
deterministic file and directory effect.

## 2026-07-23 Transaction Staged Identity Checkpoint

Final-review task 6.7 is complete. Every file replacement now has a
phase-specific artifact staged and synced inside its backup before intent. The
action installs that exact inode with descriptor-relative hard-link plus
rename operations through the already-pinned destination parent. The adapter
records native produced identity before returning, so a subclass or external
actor cannot substitute a byte-identical file or same-tree directory before
the `applied` checkpoint.

Repeated writes to one canonical destination retain separate stages by
`(path, phase)`. Completion advances the intermediate frozen state rather than
requiring the final state too early, and recovery simulates both state and
identity backward. An intermediate predecessor may be restored from the
earlier effect's still-persisted hard-linked stage before the original backup
payload is restored. Shared file, symlink, and directory targets now mutate
through the pinned parent descriptor; copied trees are recursively synced
before publication and no longer chmod their existing parent as an incidental
side effect.

RED evidence reproduced fresh-inode installation, acceptance of a
byte-identical foreign file, premature repeated-path final-state comparison,
lexical shared-directory parent drift, and acceptance of a same-tree foreign
directory. GREEN coverage includes exact staged inode installation, foreign
file and directory rejection, interrupted repeated-path recovery, all 15
deterministic file phases, target-home creation, and shared-directory copy.
Python 3.9 and Python 3.12 each pass 187/187. Strict OpenSpec, dual-runtime AST,
stable hashes, and tracked/untracked diff checks pass. No live profile/App,
launchctl, install, update, release, or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `c2fd2e061e5e7aeeaff7d373005c214d097b5a4309b24aad44f97b2697f058d8`
- `scripts/codex_switch_switching.py`:
  `f1c90770d4cd8b5c7bed2f38a33de2e14b6d49df544f486918c8566877260a55`
- `scripts/test_codex_transaction.py`:
  `bec7493fcc9323fa35d108553575f75da0b2e847339b373f2952e7463a8f1922`

### Next Action

Execute task 6.9 by TDD: close strict v1/v2 state metadata, mode, directory
entry-count, adopted-home authority, failed nested-home rollback, and later
non-empty parent-edit coverage before any restore mutation.

## 2026-07-23 Restore Descriptor-Bound Checkpoint

Final-review task 6.8 is complete. Restore planning now records both the
lexical route and canonical descriptor chain, the exact safety/restore-stage
identity, the predecessor identity, and the produced identity. Apply,
rollback, prepared recovery, and parent cleanup operate through pinned
directory descriptors. An unchanged lexical symlink ancestor remains valid;
an identity/target swap is rejected without writing through the new route.

Recovery records intent and action-observed state/identity around its own
materialization. A cleanup parent recreated at its exact prior mode is an
explicitly authorized route replacement, while later unrelated targets and
foreign empty-parent replacements remain untouched. Directory rollback can
resume after its attested safety payload inode was moved into place and a
second hard interruption occurred.

Python 3.9 and Python 3.12 each pass 192/192. Strict OpenSpec, dual-runtime
AST, stable hashes, and diff checks pass. No live profile/App, launchctl,
install, update, release, or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `bbb62bdaaebd54792a16c8d26dabf0d8b5208c1deb01702c7e4e3d22c3dc2ebb`
- `scripts/codex_switch_switching.py`:
  `f1c90770d4cd8b5c7bed2f38a33de2e14b6d49df544f486918c8566877260a55`
- `scripts/test_codex_transaction.py`:
  `7706cc522c075a28d6048799fbe2e55b4bc88d81a61f7197e175e9ac0e1abaa4`

### Next Action

Execute task 6.9 by TDD: close strict restore metadata and adopted-home
authority coverage, including failed nested-home rollback and preservation of
later non-empty parent edits.

## 2026-07-23 Strict Restore Metadata Checkpoint

Final-review task 6.9 is complete. Every recorded v1/v2 mode is range-checked
without treating booleans as integers; file and directory modes remain
required, while legacy v1 symlink compatibility permits an omitted mode but
strictly validates one when present. Valid special bits through `0o7777` remain
representable. Schema-v2 directory `entry_count` must match the attested tree
in before and committed states and cannot be bypassed with `--force`.

Official and internal adopted homes now share one authority validator: roots
must be absolute, lexically normalized, outside the backup tree, and must not
use a symlink as the final home component. Stable platform ancestor aliases
such as macOS `/var` remain compatible. Catchable nested-home rollback removes
only the exact journaled directory inode; a later non-empty edit or same-path
replacement is retained with recovery evidence.

Python 3.9 and Python 3.12 each pass 195/195 transaction tests. The legacy
profile-switch suite passes 123/123. Strict OpenSpec, dual-runtime AST, stable
hashes, and tracked/untracked diff checks pass. No live profile/App, launchctl,
install, update, release, or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `54407e9cbdd9689cf9e97358f737133fb37448f618c5c6e4532e4f56961b3435`
- `scripts/codex_switch_home_select.py`:
  `eab9c43935a7f3cab268b076fbce840cc0d26092858ae8e1473edc21d8b6a921`
- `scripts/codex_switch_switching.py`:
  `f1c90770d4cd8b5c7bed2f38a33de2e14b6d49df544f486918c8566877260a55`
- `scripts/test_codex_transaction.py`:
  `eedb98b656670397271763377a452020dfb1355c7443acdf64bc372bc36f8fb3`

### Next Action

Execute task 6.10 by TDD: move every `cmd_init --capture-current` prewrite into
one outer store lock and call capture through an already-locked dispatch while
preserving exact successful output and byte identity on busy or pending state.

## 2026-07-23 Init Capture Single-Lock Checkpoint

Final-review task 6.10 is complete. A `LockedStoreMutation` owns classification
and init/capture dispatch against one revalidated store-directory inode. When a
store is absent, only the root needed for locking is created before acquisition;
all layout, official manifest/config, capture workspace, and output work remains
inside the lock. The capture adapter accepts the active locked dispatcher and
does not attempt nested acquisition.

RED evidence observed two `_StoreLock` entries for one successful
`init --capture-current`. GREEN coverage proves one entry, exact stdout order,
and byte-identical busy and pending-capture failures with their precise existing
guidance. Python 3.9 and Python 3.12 each pass 197/197 transaction tests. The
legacy profile-switch suite passes 123/123. Strict OpenSpec, dual-runtime AST,
stable hashes, and tracked/untracked diff checks pass. No live profile/App,
launchctl, install, update, release, or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `0082c547e18f530660679a1b0c7c6461f4a016bb21b76c2c88d1aafdb3d3dc81`
- `scripts/codex_switch_capture.py`:
  `9d305266ff6a152d79e73e794930aeb7a2b817e651fc9b47c16b207f313daef9`
- `scripts/codex_switch_lifecycle.py`:
  `c99f9f21cf84206160b4ef51016a0e9cc5a9ece1cdf76c80041b473cfaf877db`
- `scripts/test_codex_transaction.py`:
  `135e1dc5c26b7b25650141cddf89aae8f1147c9d27ff4233b17e673ede35bf3a`

### Next Action

Execute task 6.11 by TDD: render retained-marker guidance from the actual
transaction outcome, add the missing custom/capture contention regressions,
and remove only imports proven dead by caller checks.

## 2026-07-23 Transaction CLI Guidance Checkpoint

Final-review task 6.11 is complete. `TransactionReceipt` now separates
successful guidance from the mutation preview while retaining the existing
preview compatibility. The supported switch CLI appends only those structured
guidance lines after its established output, so a committed transaction whose
marker cleanup fails reports `committed` and the exact retry path without
printing or duplicating the full internal plan.

Direct tests cover supported-switch lock contention and pending capture blocking
the custom compatibility route before any write. An AST import-use scan plus
`rg` showed `managed_profile_app_cli_path` was imported but never called from
`codex_switch_switching.py`; that import alone was removed, while its live
transaction/app-wrapper callers and all custom-route helpers remain.

Python 3.9 and Python 3.12 each pass 200/200 transaction tests. The legacy
profile-switch suite passes 123/123. Strict OpenSpec, dual-runtime AST/import,
stable hashes, and tracked/untracked diff checks pass. No live profile/App,
launchctl, install, update, release, or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `73131cbf103aa08447a1bfd8cfb4c725964dbba73930b99507970ef97e29002f`
- `scripts/codex_switch_switching.py`:
  `df1ee11d5d03b63f1d043641e65948d878eb5679fbef0f582bccd5380a1c70f1`
- `scripts/codex_switch_capture.py`:
  `9d305266ff6a152d79e73e794930aeb7a2b817e651fc9b47c16b207f313daef9`
- `scripts/codex_switch_lifecycle.py`:
  `c99f9f21cf84206160b4ef51016a0e9cc5a9ece1cdf76c80041b473cfaf877db`
- `scripts/test_codex_transaction.py`:
  `d76371ebb134c4920dae64f0f788010f029513db7d685839a183abc152187f73`

### Next Action

Execute task 6.12: produce a fresh named-test map for all 25 acceptance rows
and every OpenSpec scenario, adding focused coverage wherever a row cannot yet
be classified `COVERED`.

## 2026-07-23 Transaction Coverage Matrix Checkpoint

Final-review task 6.12 is complete. The fresh audit found two genuine direct
coverage gaps. Switch terminal reread accepted an unbound or incomplete object
that merely claimed `committed`; it now requires the retained marker's binding
and digest plus complete approved entries, payloads, identities, applied effect
chain, staged evidence, and unique finalize effect. Invalid claimed terminal
evidence returns `rollback_failed` and retains the marker without speculative
cleanup or rollback. Failed `init --capture-current` previously left layout and
official-profile prewrites plus a changed root mode; it now snapshots and
restores the init-owned managed state under the same lock before propagating the
capture error, while leaving stdout empty.

Direct regressions also cover restore committed-marker cleanup retry and
next-apply retirement, later external changes to an already-produced switch
target, failed existing-home mode preservation, nested non-empty/replaced
parent retention, and the final removed-helper caller contract. The durable
evidence file maps 25/25 required review rows and 36/36 OpenSpec scenarios to
109 existing test methods. A name/sequence validator found zero missing names;
the focused task selection passed 9/9 and strict OpenSpec validation passed.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `86cf0ea564244b00bdb05fe0ada49b048c3f285d379142d99be1b3a5e9f7ce9c`
- `scripts/codex_switch_switching.py`:
  `df1ee11d5d03b63f1d043641e65948d878eb5679fbef0f582bccd5380a1c70f1`
- `scripts/codex_switch_capture.py`:
  `9d305266ff6a152d79e73e794930aeb7a2b817e651fc9b47c16b207f313daef9`
- `scripts/codex_switch_lifecycle.py`:
  `df0054dfa5b3b82a6c210f15d27506bdf9df8c13744597c0acee9a35a6077fc9`
- `scripts/test_codex_transaction.py`:
  `0fb70c2bc09e6f2fef9b066f05b0716ec62b2189de11e78915b9aeac5ef83997`

### Next Action

Execute task 6.13: run the required dual-interpreter transaction suites,
123-test legacy suite, strict OpenSpec, Bash syntax, dual-runtime AST/import,
contract validation, caller checks, stable hashes, and diff checks; only then
close TPS completion items.

## 2026-07-23 Transactional Profile State Verified Checkpoint

`transactional-profile-state` is complete and verified. Final completion review
added two terminal-evidence guards: actual persisted-stage state, inode, and
route are reattested, and a non-raising corrupt terminal writer cannot bypass
the authoritative on-disk reread before marker cleanup. The first full rerun
then caught a valid nested adopted-home regression. Terminal validation and
prepared recovery now share a narrow created-parent authority: paths must form
the contiguous canonical backup-external chain declared by a missing entry and
must be covered by missing-predecessor `target_home_ensure` effects. Normal
commit, crash recovery, historical restore, and later non-empty/replaced parent
retention all pass.

Final evidence is 207/207 transaction tests on Python 3.9, 207/207 on Python
3.12, and 123/123 legacy tests. The two transaction suites passed a second time
against unchanged hashes. `openspec validate transactional-profile-state
--strict --no-interactive` and `openspec validate --all --strict
--no-interactive` pass (15/15 total items). Bash syntax, dual-runtime AST/import,
the final Agent Task Contract, the 25/25 and 36/36 coverage map, retained/dead
caller checks, `git diff --check`, and relevant untracked whitespace checks all
pass. No live workstation, Desktop/launchctl, install, update, release, network,
or Git publication action ran.

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`:
  `05b6a277b1c8685bb35c082bbbaa0fd4c3e5e991986fb2af182aa607d8d318e7`
- `scripts/test_codex_transaction.py`:
  `b1b0b9ad6aa102c0d905fbd102fbfac42203d60d823d13b48be8be77efe1c955`
- `scripts/codex_switch_restore.py`:
  `b4392bfb8629b864060f180c60dc047c9bde283ae995bcccab244384e832b41a`
- `scripts/codex_switch_switching.py`:
  `df1ee11d5d03b63f1d043641e65948d878eb5679fbef0f582bccd5380a1c70f1`
- `scripts/codex_switch_lifecycle.py`:
  `df0054dfa5b3b82a6c210f15d27506bdf9df8c13744597c0acee9a35a6077fc9`
- `scripts/codex_switch_capture.py`:
  `9d305266ff6a152d79e73e794930aeb7a2b817e651fc9b47c16b207f313daef9`

### Next Action

Apply `canonical-runtime-binding` by TDD from its approved task list. Preserve
the user decisions that only official/internal product profiles are in scope
and that current Desktop ownership is `/Applications/ChatGPT.app`; legacy
`Codex.app` remains migration-only and ChatGPT Classic remains excluded.

## 2026-07-23 Runtime Binding Inventory and Resolution Checkpoint

`canonical-runtime-binding` tasks 1.1-1.4 are complete. The new leaf-only
runtime-binding module discovers only injected exact Desktop roots, certifies
the current ChatGPT.app shape with bundle id `com.openai.codex`, preserves
Codex.app as migration-only evidence, and excludes ChatGPT Classic even when it
contains a fake executable `codex`. Official binding uses the verified bundled
CLI for shell, Desktop, and backend without PATH or active-record fallback.
Internal binding uses the manifest backend plus deterministic managed launcher,
reports raw app-path and stale active observations as drift, and rejects
missing, relative, non-regular, non-executable, or recursive managed backends.

The initial missing-module RED became 17/17 on Python 3.9 and 17/17 on Python
3.12. Dual compile, leaf-import guard, Agent Task Contract validation, strict
OpenSpec, and tracked/untracked whitespace checks pass. All bundle/backend
inputs were temporary fixtures; no live Desktop, profile, launchctl, install,
update, release, network, or Git mutation ran.

### Next Action

Execute CRB task 2.1 by adding real-shape token parser RED tests, then implement
one immutable process/environment/launchctl observation and shared runtime
attestation through tasks 2.2-2.5.

## 2026-07-23 Runtime Observation and Attestation Checkpoint

`canonical-runtime-binding` tasks 2.1-2.5 are complete. The fixed app-server
regex and Codex.app process marker are replaced by conservative token parsing
and DesktopInventory-derived host executables. One immutable observation holds
process, GUI, LaunchAgent, and launcher fingerprint data and can be supplied to
status, Doctor, and verify views without another process scan. Full-chain
attestation accepts official direct and internal proxy chains, while rejecting
stale children, proxy bypass, launch/environment drift, legacy running hosts,
and launcher fingerprint mismatch using stable finding codes.

The parser/attestation RED produced five failures and six errors. GREEN is
30/30 on Python 3.9 and 30/30 on Python 3.12; six pre-existing process/proxy
regressions and the full 123-test legacy suite on Python 3.9 also pass. Dual
compile, strict OpenSpec, and whitespace checks pass. No live Desktop/profile,
launchctl, install, update, release, network, or Git mutation ran.

### Next Action

Execute CRB task 3.1: add lifecycle/diagnostic integration REDs, then migrate
init, capture, switch, status, Doctor, and verify binding inputs to the shared
canonical resolution and attestation interfaces.

## 2026-07-23 Canonical Runtime Binding Verified Checkpoint

`canonical-runtime-binding` is complete. Only a verified ChatGPT.app with
bundle id `com.openai.codex`, its `Contents/MacOS/ChatGPT` host, and bundled
Codex CLI is current; Codex.app is migration-only and ChatGPT Classic is
excluded. Official defaults do not use PATH or managed-shim authority.
Internal Desktop intent is always the managed proxy launcher plus the separately
attested manifest backend.

All lifecycle and diagnostic consumers share the canonical binding and one
immutable observation. Internal rebind stages the candidate launcher, runs a
real app-server protocol smoke through the proxy, attests the exact child, and
promotes manifest plus launcher through a durable journal. Launcher fingerprints
are persisted and checked by Doctor; prepared/committed recovery is
deterministic, dry-run is non-mutating, concurrent foreign state is preserved,
and symlink markers fail closed.

Final evidence is 53/53 runtime tests on Python 3.9 and 3.12, 207/207
transaction tests on both, and 123/123 legacy tests on both. Strict OpenSpec,
Shell syntax, 43-file dual-runtime AST, 17-module dual-runtime import smoke,
obsolete-authority scans, and `git diff --check` pass. No live workstation,
ChatGPT/launchctl, install, update, release, network, or Git publication action
ran.

### Next Action

Apply `schema-scoped-app-proxy` by TDD from its approved task list, using the
canonical backend/launcher seam from this checkpoint and preserving the
official/internal-only product scope.

## 2026-07-23 Internal Profile Handoff Checkpoint

The user requested a fast, usable boundary before continuing full development
under the internal profile. TPS and CRB are fully implemented and verified;
they are the safe usable baseline. SAP tasks 1.1-1.3 are also complete as a
pure, isolated protocol-adapter foundation: exact method/path transforms,
direction-aware pending IDs, independent tri-state capabilities, and
backend/schema digest binding pass 14/14 tests on Python 3.9 and 3.12.

The adapter is intentionally not wired into the production proxy. Task 1.4 and
all of 2.x must land together so internal config writes never occupy a mixed
state between the old post-response file repair and the new digest-bound,
backend-owned version contract. Strict SAP OpenSpec, dual-runtime AST/import,
and diff checks pass. No live switch or external mutation ran.

### Next Action

Resume at `openspec/changes/schema-scoped-app-proxy/tasks.md` task 1.4. Migrate
JSONL forwarding to the exact adapter, then complete behavioral receipt
generation and fail-closed write gating through tasks 2.1-2.5 before enabling
the new proxy path or claiming SAP usable.

## 2026-07-23 Desktop Resume History Compatibility Finding

An internal Desktop continuation reproduced a Responses validation failure at
`input[77].id`: the raw history item was a synthetic stop-hook user message
whose local UUID was preserved by Desktop's memory-history resume path. The
same rollout resumed through isolated CLI and app-server disk paths produced
identifier-free ResponseItems and reached a local capture server without the
invalid ID. SAP task 1.4 now removes only top-level IDs from
`thread/resume.params.history`, preserving all other data. The live rollout
remains untouched.

### Next Action

Add RED adapter coverage for exact resume-history normalization, then wire the
adapter into the production proxy under SAP task 1.4.

The RED and GREEN cycle is complete. Python 3.9 and 3.12 each pass 16/16
protocol tests and eight focused proxy compatibility tests. The real 78-item
rollout fixture removes 78/78 top-level IDs without changing the source.
Strict SAP OpenSpec, compile, and diff checks pass. The current live ChatGPT
app-server still bypasses this repo proxy, so no live-fix claim is made.

### Next Action

Finish the remaining SAP task 1.4 JSONL/tracker migration and tasks 2.1-2.5,
then use an explicitly authorized install/rebind or separately authorized live
rollout repair before retrying the affected Desktop task.

## 2026-07-23 Desktop Reasoning Continuity and Proxy Routing Checkpoint

SAP task 1.4 and incident-driven launcher task 4.4 are complete. The production
proxy no longer performs recursive model/namespace traversal: parsed requests
and responses use the exact `ProtocolAdapter`, one direction-aware pending
tracker, and byte-identical forwarding for unchanged JSONL lines. Exact
`thread/resume.params.history` normalization removes top-level IDs and drops
only reasoning entries with no encrypted content, visible content, or summary.

The repeated live failure also exposed why the existing managed launcher was
ineffective. ChatGPT invokes Codex as
`-c features.code_mode_host=true app-server --analytics-default-enabled`,
while the launcher checked only whether `$1` was `app-server`; it therefore
executed `/Users/cY/.local/bin/codex` directly. The generated launcher now
routes every invocation through one Python dispatcher. The dispatcher detects
supported global options before the subcommand, preserves the complete
app-server argv, and uses `execv` for non-app-server commands.

RED evidence was the missing JSONL adapter entrypoints and a generated-wrapper
subprocess that produced `internal-codex` directly without a proxy-child
receipt. GREEN evidence is protocol 17/17, app-proxy 12/12, runtime 53/53, and
profile 127/127 under both Python 3.9 and Python 3.12. Both affected OpenSpec
changes validate strictly; compile, imports, and diff checks pass. Read-only
replay of thread `019f8e16-477d-79d3-b968-cf41d15446b4` retained 43/56 items,
removed 13 opaque reasoning references, and preserved source SHA-256
`fc30a6a0710038add99920dedf9a4850187de24562bfa7e30a3621d6522f7800`.

Independent review then identified five compatibility gaps. Same-ID server
requests could consume config-write snapshots; text streams normalized CRLF;
legacy marketplace and `result.models` behavior was incomplete; process
inspection could classify non-Codex binaries; and the wrapper's import
`PYTHONPATH` leaked into the backend. All five are fixed with focused
regressions, and the complete dual-runtime runtime/profile suites passed again.

The source repair is not active on the workstation. Installed release `0.1.13`
lacks the adapter/dispatcher, and the running ChatGPT app-server still bypasses
the managed proxy. No live install, rebind, restart, or rollout mutation ran.

### Next Action

Continue SAP tasks 2.1-2.5 for digest-bound config-write receipts and removal of
post-response file repair. For immediate workstation recovery, obtain explicit
INC-005 authorization before applying a scoped install/rebind and restarting
ChatGPT, or obtain separate authorization to back up and repair selected live
rollouts.

## 2026-07-23 Scoped Live Internal Rebind Applied

The user authorized the immediate INC-005 rebind path. Before mutation, the
internal manifest and managed launcher were copied to
`/Users/cY/.codex-switch/backups/manual-20260723T103336Z-resume-proxy-rebind`.
The backup manifest SHA-256 is
`de3069115457665bb5f1ea82acafda6900017f0abcaba0e9104592af1db92615`;
the backup launcher SHA-256 is
`1cf82aadfc5e6ca1bbc30d4a43fd45fb337fa9dff6455d6d5e1adf32c58da709`.

Immediately before the live mutation, Python 3.9 and 3.12 each passed protocol
17/17, runtime 53/53, and profile 127/127. Strict SAP OpenSpec and
`git diff --check` also passed. The canonical command
`./scripts/codex-switch set-bin internal /Users/cY/.local/bin/codex` then
staged the source-backed launcher, ran its temporary-home app-server smoke,
attested the requested child, and transactionally committed the manifest and
launcher pair.

The committed manifest now records
`app_cli_path=/Users/cY/.codex-switch/bin/codex-internal-app`,
`runtime_binding=canonical`, backend `codex-cli 0.144.6`, and launcher SHA-256
`f3854fe0b509b09cdccd79722c5b1c35e904812ef0310e14afbe511642920f6d`.
The launcher uses `SWITCH_SCRIPTS=/Users/cY/dev/codex-switch/scripts`, so this
was not a full installation of the unfinished worktree. A second smoke against
the committed launcher passed with backend
`/Users/cY/.local/bin/codex` and argv
`["app-server", "--analytics-default-enabled"]`; a smoke-mode `--version`
returned `codex-cli 0.144.6`.

ChatGPT was deliberately not exited. Its existing app-server pid still runs the
raw backend directly, so the continuation repair is configured but not yet
active in that process. No rollout, release, plugin, Git, or installed release
tree was modified.

### Next Action

Review the SAP 2.1-2.5 diff against the approved OpenSpec and
`.planning/devflow/agent-contracts/schema-config-write-receipt.md`. Fix every
actionable finding, rerun the dual-runtime focused and adjacent regression
suites, then mark tasks 2.1-2.5 complete only if the review gate is green.
Continue SAP 3.x-5.x afterward. The separately authorized ChatGPT quit/reopen
acceptance remains pending but is not required for this source review; do not
perform another live mutation without its Human Gate.

## 2026-07-24 Fail-Safe Bundle Containment Verified Checkpoint

`fail-safe-update-release` tasks 1.1-1.2 are complete after delegated TDD and
main review. `scripts/package-release.sh` is now a thin adapter over
`codex_switch_release_bundle.py`. The builder canonically rejects repository,
filesystem-root, repository-ancestor, symlink, foreign, and unmarked package
destinations; copies only the fixed release allowlist into a marker-owned
temporary directory; records required paths, modes, sizes, and SHA-256 digests;
validates the package, top-level runner, and archive; and rolls all three public
outputs back together on partial finalization failure.

Main review found and repaired a stale-classification deletion window. A
destination swapped after preflight could previously be renamed into the
owned backup and removed. Finalization now reclassifies immediately, binds
approved outputs by `lstat` device/inode/type before and after rename, validates
the exact moved bundle before promotion and cleanup, and preserves any unbound
backup evidence.

Fresh focused results are 14/14 on Python 3.9.6 and Python 3.12.13. The adjacent
troubleshooting-doc package test passes on both interpreters; Bash syntax,
dual-runtime compile, strict OpenSpec, and `git diff --check` pass. A fresh
temporary output root packaged successfully twice with exactly
`codex-switch/`, `run.sh`, and `codex-switch.tar.gz`, 59 manifest file records,
66 archive members, payload SHA-256
`b715fc98afb786417a9a3c5aef8286ffc51b9553a49477b04b765a3722c2c114`,
and no staging or backup residue. No live install/update/profile/plugin/App,
network, release, or Git mutation ran.

### Next Action

Execute task 1.3 by RED/GREEN: prove a malicious downloaded source archive
cannot execute its `package-release.sh`, then make `install.sh` and `run.sh`
use the trusted local fixed-allowlist bundle seam without changing live
installation state.

## 2026-07-24 Fail-Safe Source Fallback Verified Checkpoint

`fail-safe-update-release` task 1.3 is complete, bringing the change to 4/38.
Downloaded source fallback in `install.sh`, `run.sh`, and
`scripts/codex-switch` now uses the currently trusted shell implementation to
validate and copy only `README.md`, `SKILL.md`, `VERSION`, `run.sh`, `agents/`,
`docs/`, `evals/`, and `scripts/`. The downloaded
`scripts/package-release.sh` remains inert copied data; malicious-sentinel tests
prove it is not executed. Extra root files and root `scripts/__pycache__` are
excluded, required top-level paths and executables reject symlinks, and explicit
local `CODEX_SWITCH_SOURCE_DIR` behavior remains unchanged.

Main review found and repaired two Bash failure-propagation defects. First,
installer and runner ignored a failed `scripts/__pycache__` removal and reported
success after promoting the incomplete staging tree. Second, self-update ignored
a failed downloaded-source staging result when `sync_self_update` ran inside an
`if` condition, allowing a partially staged candidate to replace `current`.
Injected `rm` failures reproduced both defects before the fixes; both paths now
return nonzero before promotion. `tar -p` remains intentional because a fresh
probe under this workstation's umask changed `0741/0751/0701` to `0700/0700/0700`
without it and preserved the exact modes with it.

Fresh Python 3.9.6 and Python 3.12.13 runs each pass 14/14 release tests and 7/7
focused source-fallback, required-path, cleanup-failure, local-source, and
self-update-failure tests. Bash syntax, strict OpenSpec, static proof that no
downloaded-source path invokes `package-release.sh`, and `git diff --check`
also pass. No live install/update/profile/plugin/App, network, release, or Git
mutation ran.

Archive-member path traversal and symlinks nested inside allowlisted directories
remain outside task 1.3 and are recorded as INC-008. Task 1.3 proves trusted
copy selection and no archive-owned staging-script execution, not source
authenticity or extraction containment.

### Next Action

Execute task 1.4 by RED/GREEN: specify immutable `releases/<digest>`, atomic
`current` and `rollback` references, lock contention, reversible legacy-current
migration, bounded handshake failure/mismatch, and original-command exactly-once
behavior before implementing the promotion module in task 1.5.

## 2026-07-24 Fail-Safe Immutable Promotion Verified Checkpoint

`fail-safe-update-release` tasks 1.4-1.5 are complete, bringing the change to
6/38. The new promotion module validates bundle authority, shell syntax, Python
AST/import readiness, and no-mutation command smoke before publishing a
same-filesystem staged candidate under `releases/<payload-sha256>`. Relative
atomic `current` and `rollback` refs, a directory-inode lock, structured
promotion state, an exact run-id/version/digest/root health handshake, and
optional original-command exactly-once replay now form one isolated contract.

Main review added identity-bound state/ref writes, strict malformed/Boolean
schema rejection, owned staging cleanup, reversible pre-move/post-move/post-ref
legacy migration, and recovery when a process exits after candidate ref or
active-state publication but before the handshake. A failure after candidate
activation restores prior verified refs before the original command can run.
The canonical bundle validator also rejects Boolean manifest/workdir schema
versions.

Fresh Python 3.9.6 and Python 3.12.13 runs each pass 34/34 update/release tests.
Dual-runtime AST for promotion/bundle/tests, strict FSR OpenSpec, static proof
that installer/runner/wrapper production paths do not call the promotion module
yet, an isolated two-release receipt, and `git diff --check` pass. The receipt
retained both digest roots with relative current/rollback targets and no
temporary promotion residue.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or archive action ran. Full profile verification
remains deferred to task 7.3.

### Next Action

Execute task 2.1 by RED/GREEN: add isolated installer/runner adapter tests for
copy/import/syntax/smoke failures inside Bash conditional contexts, requiring
explicit nonzero status and byte-identical current/rollback references. Do not
wire production adapters until those RED contracts are recorded.

## 2026-07-24 Fail-Safe Installer and Runner Adapters Verified Checkpoint

`fail-safe-update-release` tasks 2.1-2.2 are complete, bringing the change to
8/38. `install.sh` and `run.sh` now stage source or release candidates under the
target library root, resolve bootstrap modules through an explicit trust
boundary, canonicalize source fallback, validate complete candidates, and call
immutable promotion before exposing the stable public path.

Piped entrypoints no longer require `BASH_SOURCE[0]`. Explicit or real
script-local module directories are trusted directly; installed and downloaded
module pairs must match embedded SHA-256 values, are copied into candidate-local
trusted staging, and are re-hashed before execution. Malicious module sentinels
remain absent. Candidate bundles now require `codex_profile_switch.py`,
`codex_switch_release_bundle.py`, and `codex_switch_promotion.py`.

The promotion CLI now runs the original command inside the promoted
`releases/<digest>` root and records exactly one execution. A deterministic
concurrent-promotion test changes `current` before the CLI returns and proves
the command still executes the intended release; nonzero and signal-derived
exit codes remain preserved. Archive-root selection no longer uses
`find | head`, and primary/helper cleanup outcomes are handled explicitly.

Fresh final verification passed: Python 3.12.13 update/release 47/47, Python
3.9.6 installer/runner 10/10, six adjacent profile adapter tests on both
interpreters, dual Python compile, Bash syntax, strict FSR OpenSpec, embedded
digest matching, isolated package validation with exactly three public outputs,
and `git diff --check`. The current package receipt has 60 manifest file
records, 67 archive members, and payload SHA-256
`75c79fb0608d55c780b9b27bfc8b07c918e1249e5ca2f836cf0eda5792e7ee46`.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran. Full profile-suite
verification remains deferred to task 7.3.

### Next Action

Execute task 2.3 by RED/GREEN: specify self-update rejection for invalid
structure/version, handshake mismatch, timeout, concurrent promotion, and
successful replay exactly once before migrating `scripts/codex-switch` in task
2.4.

## 2026-07-24 Fail-Safe Self-Update RED Contract Checkpoint

`fail-safe-update-release` task 2.3 is complete, bringing the change to 9/38.
Six public-wrapper tests now start from an immutable two-release layout and
cover invalid candidate structure, expected-version mismatch, handshake field
mismatch, handshake timeout, a deterministic concurrent promotion, and a
nonzero user command that must still execute exactly once.

The RED contract is stable on both supported test interpreters. Python 3.12.13
failed all 6 cases because legacy self-update replaced the `current` symlink
with a mutable directory. System Python 3.9.6, using Python 3.12 as the wrapper
runtime required by the current CLI contract, produced the same 6 behavior
failures with no fixture errors. Both interpreters parsed the test file and the
test-file whitespace check passed.

No production code, live install/self-update, profile/App switch, plugin
mutation, network release, commit, push, tag, or OpenSpec archive action ran.

### Next Action

Execute task 2.4: migrate `scripts/codex-switch` self-update to the trusted
bundle/promotion modules, preserve immutable `current`/`rollback`, validate the
structured handshake, and replay the original command exactly once from the
receipt's digest root. Keep sync failure fallback to the prior implementation,
but never reinterpret a replayed user command's nonzero exit as sync failure.

## 2026-07-24 Fail-Safe Self-Update Verified Checkpoint

`fail-safe-update-release` task 2.4 is complete, bringing the change to 10/38.
The installed wrapper stages on the target filesystem, canonicalizes raw source
through the trusted bundle builder, validates exact candidate version and
digest, promotes through the immutable layout, validates the structured
promotion receipt, and re-executes from the receipt's `releases/<digest>` root
with self-update recursion disabled. Candidate, version, handshake, and timeout
failure keep the prior verified refs and command runnable. A concurrent
promotion cannot redirect replay, and a nonzero user command is not retried or
misreported as sync failure.

Main review initialized all new self-update locals for `set -u`, migrated
legacy directory-only profile fixtures to canonical bundles and immutable refs,
and reproduced a release-archive mode failure under restrictive umask. Bundle
extraction now uses `tar -p`; the primary upgrade regression explicitly sets
`umask 0077` and proves manifest `0755` modes survive extraction.

Fresh final verification passed on both Python 3.12.13 and system Python 3.9.6:
53/53 update/release tests and 10/10 focused profile self-update tests. The six
task 2.3 contracts pass on both interpreters. Strict FSR OpenSpec, Bash syntax,
dual-runtime AST, obsolete in-place self-update path scan, and
`git diff --check` pass. One exploratory parallel focused run hit the test
fixture's one-second candidate-smoke timeout; sequential reruns passed on both
runtimes and the full suites were run serially.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran. Full profile-suite
verification remains deferred to task 7.3.

### Next Action

Execute task 3.1 by RED: add ordered internal-update policy tests for healthy
newer/older current versions, blocked latest/current combinations,
missing/unparseable versions, and prerelease ordering. Do not modify the shell
adapter until that policy contract is recorded.

## 2026-07-24 Fail-Safe Internal Update Policy RED Checkpoint

`fail-safe-update-release` task 3.1 is complete, bringing the change to 11/38.
The public policy seam is `decide_internal_update(...)`, returning a structured
decision for equal, newer, older, blocked, invalid, and prerelease version
cases.

Python 3.12.13 and system Python 3.9.6 each produced the same 8/8 expected RED
failures. Every failure is the deliberate missing-module contract for
`scripts/codex_switch_update_policy.py`; no fixture, import, or legacy shell
behavior obscured the policy boundary.

No production code, shell adapter, live update, install/self-update,
profile/App switch, plugin mutation, network release, commit, push, tag, or
OpenSpec archive action ran.

### Next Action

Execute task 3.2: create the Python 3.9-compatible structured update policy,
implement ordered SemVer decisions, allow downgrade only for an explicitly
blocked current version with a valid fallback, and make all eight contracts
GREEN.

## 2026-07-24 Fail-Safe Internal Update Policy Verified Checkpoint

`fail-safe-update-release` task 3.2 is complete, bringing the change to 12/38.
`scripts/codex_switch_update_policy.py` now owns strict SemVer core/prerelease
ordering and immutable structured outcomes. Healthy newer current versions are
never downgraded. Healthy older versions upgrade only to an unblocked latest.
Fallback may lower the version only when the current version itself is
explicitly blocked and the fallback is valid and unblocked.

The eight policy contracts pass on Python 3.12.13 and system Python 3.9.6.
Complete update/release suites pass 61/61 on each interpreter. Strict FSR
OpenSpec, dual-runtime AST/compile, and `git diff --check` pass. The policy
module SHA-256 is
`921e87cdb027175ff501d86e52232ae85aabf3ee92c9e43241cf13770959cf0c`.

No shell adapter, live update, install/self-update, profile/App switch, plugin
mutation, network release, commit, push, tag, or OpenSpec archive action ran.

### Next Action

Execute task 3.3 by RED: add public wrapper tests for helper exit 17, helper
success with a wrong installed version, blocked-current repair failure, and
runtime compatibility-smoke failure. Do not change the adapter until all four
failure contracts are stable.

## 2026-07-24 Fail-Safe Internal Update Adapter RED Checkpoint

`fail-safe-update-release` task 3.3 is complete, bringing the change to 13/38.
Four public wrapper contracts cover helper exit 17, helper success with a wrong
after-version, blocked-current fallback repair failure, and app-server
compatibility-smoke failure.

Python 3.12.13 and system Python 3.9.6 each produced 4/4 expected behavior
failures. The current adapter swallowed helper exits 17 and 23, accepted an
unchanged `1.0.0` after targeting `1.1.0`, omitted the explicit `1.1.0` target
for a normal upgrade, and printed completion before the required app-server
compatibility result. The system-Python run used Python 3.12 only for the
existing Config Document initialization prerequisite; the wrapper behavior
remained under the invoking test environment.

An earlier package-style unittest command failed before collection because
`scripts/` was not on `sys.path`; it is excluded from RED evidence. Dual test
compile and `git diff --check` pass.

No production adapter, live update, install/self-update, profile/App switch,
plugin mutation, network release, commit, push, tag, or OpenSpec archive action
ran.

### Next Action

Execute task 3.4: route check decisions through the structured policy, bind
every helper call to the intended target, propagate helper status, require an
exact after-version, and defer completion until the app-server compatibility
boundary passes.

## 2026-07-24 Fail-Safe Internal Update Adapter Verified Checkpoint

`fail-safe-update-release` task 3.4 is complete, bringing the change to 15/38.
Standalone and one-key internal updates now share ordered policy targets,
explicit helper status, exact after-version verification, and an app-server
compatibility boundary before success or completion output.

The review gate also closed three adapter escape paths: Bash 3.2-safe empty
arguments, complete helper value-option parsing that prevents `--dry-run` from
being consumed as a value, and fail-closed handling for malformed existing
internal manifests. A plugin-repair failure after a completed binary update
still runs mandatory verification before returning the original repair status.

Python 3.12.13 passed 26/26 focused profile tests. System Python 3.9.6 passed
20/20 shell/adapter tests. Complete update/release suites passed 64/64 on both
interpreters. Strict FSR OpenSpec, Bash syntax, and `git diff --check` passed.

No live update, install/self-update, profile/App switch, plugin mutation,
network release, commit, push, tag, or OpenSpec archive action ran.

### Next Action

Execute task 4.1 by RED: distinguish verified empty plugin catalogs from command
failure, empty output, malformed/truncated JSON, stderr warnings, unsupported
schema, and complete catalog responses before changing plugin repair behavior.

## 2026-07-25 Fail-Safe Plugin Catalog and Repair Verified Checkpoint

`fail-safe-update-release` tasks 4.1-4.4 are complete, bringing the change to
20/38. Plugin catalog results now preserve stdout, stderr, return status, schema
classification, and verified-empty state. Any command, output, JSON, or schema
uncertainty fails before plugin add, disable, or config writes.

Installed materialization now requires a version directory with a matching
`.codex-plugin/plugin.json`; temporary/cache residue and partial directories are
not accepted. Repair builds and returns a typed `PluginRepairPlan`, validates
all config inputs before mutation, rejects config drift after planning, and
rolls back every attempted config update if a later write fails.

Python 3.12.13 passed 35/35 plugin-related regressions and the six focused task
4.3/4.4 contracts. System Python 3.9.6 passed the catalog, zero-write, and
cache-marker subset 3/3 and imported the plugin module. Focused
`git diff --check` passed. No live update, install/self-update, profile/App
switch, plugin mutation, network release, commit, push, tag, or OpenSpec archive
action ran.

### Next Action

Execute task 5.1 by RED: specify timeout escalation, excessive/malformed
capture, stdout/stderr separation, missing prerequisites, and no-clobber report
paths before changing verification subprocess behavior.

## 2026-07-25 Fail-Safe Structured Verification Verified Checkpoint

`fail-safe-update-release` tasks 5.1-5.5 are complete, bringing the change to
26/38. Verification subprocesses now return typed `SmokeOutcome` records,
capture stdout and stderr independently within byte limits, enforce monotonic
deadlines, terminate process groups through TERM/KILL escalation, and clean
descendants that retain output pipes after the parent exits.

Verification reports are allocated with exclusive no-clobber names and contain
structured outcome metadata without raw commands or exec prompts. One
allowlist-first sanitizer runs before terminal output and report persistence;
authorization, bearer, API-key, cookie, credential, password, and signed-query
values are redacted while conservative account/deployment/request routing
identifiers remain available.

App-server smoke now parses bounded JSONL through explicit
`await_initialize -> initialize_complete -> await_plugin -> plugin_complete`
states. Initialize errors, missing result/error, malformed or oversized lines,
and pre-initialize plugin auth responses fail. The known post-initialize plugin
authentication response remains permitted.

Python 3.12.13 and system Python 3.9.6 each passed 17/17 focused verification
tests. Existing profile verify tests passed 12/12, and the runtime
initialize-error regression passed 1/1. Strict FSR OpenSpec, dual-runtime
syntax, and focused `git diff --check` passed. No live smoke with secret input,
profile/App switch, plugin/install/update mutation, network release, commit,
push, tag, or OpenSpec archive action ran.

### Next Action

Execute task 6.1 by RED against release planner decisions for ancestry, tag
identity, missing assets, remote-main races, deterministic checksums, and
publish-rerun recovery.

## 2026-07-25 TPS Runtime-State Incident Verified Checkpoint

`transactional-profile-state` TPS-002 is source-complete. Exact-name runtime
ownership excludes `ipc` and `mcp-oauth-locks` before shared-support planning,
and an existing target home no longer receives a no-op
`target_home_ensure` that recursively captures runtime sockets. Truly missing
target-home chains retain their journaled creation, identity, rollback, and
cleanup contract.

The source/target Unix-socket regression first failed at
`official/ipc/oi.sock`, then passed with unknown-special fail-closed,
new/nested-home cleanup, mode-preservation, and recovery coverage in a 9/9
focused run. The complete Python 3.12 transaction suite passed 213/213. The
adjacent profile suite passed 175/179; all four errors are the current FSR
fake-catalog fixtures rejected as `invalid_json`, after their TPS switch and
required app-server checks succeeded. Strict TPS OpenSpec, Bash syntax, Python
compile, and diff checks passed.

The repository-source official dry-run returned `Outcome: DRY RUN OK`. Its
33,717-entry bounded snapshot retained SHA-256
`f079b653f75690bff3aad70a69e3e48a41db599245166f7a00e811d0defe7382`
before and after, including stable official `ipc.sock` device/inode identity.
No install, live switch, App restart, failed-backup cleanup, release, Git
publication, or archive action ran.

Evidence is
`.planning/devflow/verification/transactional-profile-state.md`. The durable
checkpoint is
`.planning/checkpoints/2026-07-25-tps-runtime-state-incident-verified.md`.

### Next Action

Resume `fail-safe-update-release` task 6.1. Installing this source and running a
live official switch remain separately approval-gated.

## 2026-07-25 Fail-Safe Release Planner RED Checkpoint

`fail-safe-update-release` task 6.1 is complete, bringing the change to 27/38.
Seven planner/fake-GitHub contracts cover non-ancestor tags, tag identity,
missing-asset reconciliation, complete-tag no-op, remote-main races, checksum
drift, and publish-failure reruns.

Python 3.12.13 and system Python 3.9.6 each produced the same single expected
RED failure: a matching, complete, published latest tag at `HEAD` still returns
`release_action="reconcile"` instead of `release_action="none"`. The other six
contracts pass, isolating task 6.2 to planner decision behavior.

The previously written but unexecuted historical-layout tests were recovered
to 10/10 on Python 3.12. Missing manifests now require explicit historical
mode; only the trusted `v0.1.12` and `v0.1.13` layouts are accepted; bounded
AppleDouble metadata is validated and discarded before deterministic archive
rewriting. This is partial evidence for tasks 6.5 and 6.7, which remain open.

Dual-runtime compile and focused `git diff --check` pass. No live install,
self-update, profile/App switch, plugin mutation, network release, commit,
push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-release-planner-red.md`.

### Next Action

Execute task 6.2: correct prepare/reconcile/no-op selection and make all seven
planner contracts GREEN on both supported Python interpreters.

## 2026-07-25 Fail-Safe Release Planner Verified Checkpoint

`fail-safe-update-release` task 6.2 is complete, bringing the change to 28/38.
The planner now reconciles only a missing, draft, or incomplete latest release.
A matching, complete, published latest tag at `HEAD` selects no action.

All seven planner contracts pass on Python 3.12.13 and system Python 3.9.6.
The bundle-module bootstrap hash in `install.sh` and `run.sh` now matches the
current source SHA-256
`bf6d221ff937cb9d66e9a4c8cd0705c9f76f37333982d2989b399e9d8a226228`;
the combined planner/bootstrap group passes 8/8 on both interpreters.

The full Python 3.12 update/release suite ran 87 tests. Before the bootstrap
hash refresh it passed 82 and failed five: the two hash-bound bootstrap tests
are now GREEN, while the remaining three are the explicitly pending task 6.5
RED contracts for nested manifest handling, special files, and package-root
mode. Strict FSR OpenSpec, dual-runtime compile, Bash syntax, hash equality,
and `git diff --check` pass.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-release-planner-verified.md`.

### Next Action

Execute task 6.3 by RED: add static workflow-order tests before changing
`.github/workflows/auto-release.yml` and `.github/workflows/release.yml`.

## 2026-07-25 Fail-Safe Release Workflow Order Verified Checkpoint

`fail-safe-update-release` task 6.3 is complete, bringing the change to 29/38.
Four static contracts prove automatic package/validate/remote-base/atomic-push/
reconcile ordering, manual validate-before-reconcile ordering, absence of
failure-bypass flags, and shared serial release concurrency.

The workflow adapters already contained the intended ordering when this
resumed slice started, so the tests passed immediately and no further workflow
mutation was required. The combined planner/workflow group passes 11/11 on
Python 3.12.13 and system Python 3.9.6. Strict FSR OpenSpec and focused diff
integrity pass.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-release-workflow-order-verified.md`.

### Next Action

Execute task 6.4 by RED: cover incomplete latest-tag reconciliation, same-tag
rerun, and commit/asset conflicts that must not clobber.

## 2026-07-25 Fail-Safe Release Reconciliation Verified Checkpoint

`fail-safe-update-release` task 6.4 is complete, bringing the change to 30/38.
Four additional reconciliation contracts prove missing-only upload, read-only
complete reruns, checksum-conflict zero mutation, and tag-conflict zero GitHub
calls.

The inherited reconciliation implementation passed all four without production
edits. The planner/reconciliation group passes 11/11 on Python 3.12.13 and
system Python 3.9.6. Strict FSR OpenSpec, dual-runtime compile, and focused diff
integrity pass.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-release-reconciliation-verified.md`.

### Next Action

Execute task 6.5: close the observed strict-bundle REDs and add commit-tree
authority coverage for hidden index flags and exact modes.

## 2026-07-25 Fail-Safe Commit Tree Authority Verified Checkpoint

`fail-safe-update-release` task 6.5 is complete, bringing the change to 31/38.
Release validation now compares the exact target Git commit tree, blob bytes,
file set, and executable bits instead of trusting `git status`. Hidden
`assume-unchanged` and `skip-worktree` drift fails closed.

Strict bundles now exclude only the root manifest, protect nested
manifest-named payload, reject special files, and require package-root mode
`0755`. Explicit trusted historical layouts remain a separate route. The final
bundle SHA-256 pinned by installer and runner is
`a301822fc5347c2225c4a73c9be2f31a05bebf4fac2c80083cd4f3698f49c9b3`.

The six RED failures are GREEN. Bundle/asset/bootstrap results are 33/33 on
Python 3.12.13 and system Python 3.9.6. Strict FSR OpenSpec, dual-runtime
compile, Bash syntax, and diff integrity pass.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-commit-tree-authority-verified.md`.

### Next Action

Execute task 6.6 by RED: bind manual recovery to an exact remote semantic tag,
disable persisted credentials, keep trusted tooling on `main`, and recheck tag
identity around every release mutation.

## 2026-07-25 Fail-Safe Remote Tag Identity Verified Checkpoint

`fail-safe-update-release` task 6.6 is complete, bringing the change to 32/38.
Manual recovery now stages trusted release tooling from `main`, resolves an
exact semantic tag against the configured remote before target checkout, and
checks out the resolved commit with persisted credentials disabled.

Reconciliation rechecks the remote tag immediately before release creation,
each asset upload, publication, final release inspection, and after downloaded
asset verification. A moved or missing tag aborts before any later mutation.

The inherited RED contracts were made GREEN before this continuation. Fresh
focused results are 4/4 on Python 3.12.13 and 4/4 on system Python 3.9.6.
No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-remote-tag-identity-verified.md`.

### Next Action

Execute task 6.7: finish trusted versioned historical-layout and deterministic
legacy archive validation for supported release retries.

## 2026-07-25 Fail-Safe Historical Release Retry Verified Checkpoint

`fail-safe-update-release` task 6.7 is complete, bringing the change to 33/38.
The release-assets CLI now exposes an explicit `--allow-legacy` gate, and the
manual recovery workflow passes it only after an exact remote tag has been
resolved. Missing manifests remain rejected by default, and the legacy route
still accepts only trusted version-scoped layouts.

Exact `v0.1.12` and `v0.1.13` checkouts were packaged with their historical
scripts. Different raw archive timestamps produced different input hashes but
trusted canonicalization produced identical retry hashes for each tag.

Fresh results are 13/13 historical/CLI/workflow contracts on Python 3.12.13
and system Python 3.9.6, strict FSR OpenSpec, dual-runtime compile, and focused
diff integrity. No live install, profile/App switch, plugin mutation, network
release, commit, push, tag, or archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-historical-release-retry-verified.md`.

### Next Action

Execute task 6.8 by RED: represent reconciliation plus a pending release as a
single planner result and make the workflow restore the original source commit
before the prepare path.

## 2026-07-25 Fail-Safe Reconcile-Then-Prepare Verified Checkpoint

`fail-safe-update-release` task 6.8 is complete. Canonical progress is 30/35
implementation tasks and 34/42 OpenSpec checkboxes; the earlier `/38`
shorthand mixed implementation and Completion Contract rows and is no longer
used.

The planner now emits independent `reconcile_required` and `prepare_required`
outputs and selects `reconcile_then_prepare` when both are true. The automatic
workflow packages and reconciles the existing tag in isolated temp outputs,
then checks out the originally recorded source commit before bumping,
verifying, packaging, atomically pushing, and reconciling the pending release.
The two release attempts never share a dist root or asset manifest.

Fresh planner/workflow results are 21/21 on Python 3.12.13 and 21/21 on system
Python 3.9.6, plus the prepare-only guard on both runtimes. Strict FSR OpenSpec,
dual-runtime compile, workflow YAML parsing, and focused diff integrity pass.
No live install, profile/App switch, plugin mutation, network release, commit,
push, tag, or OpenSpec archive action ran.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-reconcile-then-prepare-verified.md`.

### Next Action

Execute task 7.1: prove obsolete unsafe branches have no supported callers,
remove only confirmed dead paths, and then begin the complete verification
matrix.

## 2026-07-25 Fail-Safe Obsolete Path Cleanup Verified Checkpoint

`fail-safe-update-release` task 7.1 is complete. Canonical progress is 31/35
implementation tasks and 35/42 OpenSpec checkboxes.

Caller and marker scans found no remaining production definition or caller for
the retired mutable self-update roots, internal latest/current inequality
branch, catalog parse-to-empty fallback, app-server stdout string-response
inference, direct non-atomic release push, or clobber upload path. No production
deletion was needed. The remaining current/backup renames are confined to the
tested reversible legacy migration in `codex_switch_promotion.py`.

The cleanup/static workflow group passes 7/7 on Python 3.12.13 and system
Python 3.9.6. Explicit zero-match scans, strict FSR OpenSpec, dual-runtime test
compile, and focused diff integrity pass.

Evidence is
`.planning/checkpoints/2026-07-25-fsr-obsolete-path-cleanup-verified.md`.

### Next Action

Execute task 7.2: run the complete update/release suite on Python 3.12.13 and
repair every failure before continuing.

## 2026-07-25 Fail-Safe Full Update/Release Suite Passed

`fail-safe-update-release` task 7.2 is complete. The exact command
`PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v`
passed 107/107 tests in 191.044 seconds with no failures or skips. Canonical
progress is 32/35 implementation tasks and 36/42 OpenSpec checkboxes.

### Next Action

Execute task 7.3 by running the complete profile suite; release planner
coverage is already included in the fresh 107-test result.

## 2026-07-25 Fail-Safe Full Profile Suite Passed

`fail-safe-update-release` task 7.3 is complete. The exact command
`PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py`
passed 193/193 tests in 183.009 seconds with no failures or skips.

The first full run exposed duplicate release tests that still expected the old
always-reconcile planner, single-shell-step workflow, fixed automatic `dist/`
root, and pre-commit-tree source fixture. It also exposed update-only tests
that unintentionally exercised the new fail-closed plugin catalog contract.
Those tests now assert the approved release behavior or skip unrelated plugin
repair. The dedicated plugin-repair failure compatibility test remains active.
No production fail-closed behavior was weakened.

Candidate/copy/handshake retention and package-before-ref/reconciliation
Completion Contract rows are now checked. Canonical progress is 33/35
implementation tasks and 39/42 OpenSpec checkboxes. Evidence is
`.planning/checkpoints/2026-07-25-fsr-profile-suite-verified.md`.

### Queued Follow-up: Internal/Official Feature Parity

The user approved a subsequent independent Full OpenSpec,
`internal-official-feature-parity`, but it must not overlap the active Goal.
`PARITY-001` is queued only after FSR, integration review, final verification,
the authorized live rollout, and current Goal stabilization.

The allowed-difference whitelist is fixed: internal retains its internal
`codex_bin`, model, API endpoint, provider, and auth, and must not bind to the
official bundle binary. Outside those fields, protocol, capabilities, and
Desktop experience should track official. Core experience drift makes internal
unhealthy; optional capability drift may degrade only with explicit reporting,
a synchronization queue entry, and recheck after every internal binary
update/rebind.

The first recorded parity finding is Subagent metadata selection: official
declares `multi_agent_version=v2`, while the internal Azure model catalog lacks
that field and selects v1, producing random nicknames. The future change must
design a controlled catalog overlay/metadata sync that preserves internal
model/provider/API fields, enables v2 only after internal capability and
behavior probes pass, and validates task-oriented names/descriptions through a
real Desktop Subagent smoke. Silent fallback is forbidden.

Current `INT-001` and `VER-001` may preserve extension boundaries and record
this follow-up only. They must not implement parity inventory, overlays,
adapters, new finding codes, or update/rebind parity behavior.

### Next Action

Execute task 7.4: strict OpenSpec, shell syntax, Python AST/import, isolated
package generation and validation, workflow YAML/static checks, and
`git diff --check`.

## 2026-07-25 Fail-Safe Static and Package Verification Passed

`fail-safe-update-release` task 7.4 is complete. Strict OpenSpec passed 17/17;
Bash syntax passed 5/5; Python 3.12.13 and system Python 3.9.6 each passed AST
54/54 and production imports 46/46; both release workflows parsed as YAML and
their six static ordering/identity contracts passed; `git diff --check`
passed.

The supported package adapter generated and validated an isolated `0.1.13`
bundle with 64 manifest files, package mode `0755`, archive size 370922 bytes,
and payload SHA-256
`6dab0fc4e820d5f5e511e0115154d28ccfbd5e7a9db75468174a0baefd014ede`.
The package, runner, archive, and required Python modules all passed
`validate_release_outputs`.

The final focused/full/static/package Completion Contract row is checked.
Canonical progress is 34/35 implementation tasks and 41/42 OpenSpec
checkboxes. Evidence is
`.planning/checkpoints/2026-07-25-fsr-static-package-verified.md`.

### Next Action

Execute task 7.5: consolidate RED/GREEN logs, promotion and rollback receipts,
sanitizer evidence, changed files, fake Git/GitHub call evidence, and residual
risks in `.planning/devflow/verification/fail-safe-update-release.md`.

## 2026-07-25 Fail-Safe Update and Release Complete

`fail-safe-update-release` is complete at 35/35 implementation tasks and 42/42
OpenSpec checkboxes. The authoritative evidence file now includes the complete
RED/GREEN history, bundle and immutable promotion/rollback receipts, ordered
internal update and plugin catalog contracts, bounded sanitizer evidence,
release planner/workflow decisions, fake Git/GitHub call ordering, exact
commit-tree and historical retry evidence, changed files, current hashes,
final commands, and residual risks.

Final FSR source results are update/release 107/107, profile 193/193, strict
OpenSpec 17/17, Bash 5/5, Python AST 54/54 and production imports 46/46 on both
Python 3.12.13 and system Python 3.9.6, workflow YAML 2/2, release static 6/6,
isolated bundle validation, and `git diff --check`.

Evidence:

- `.planning/devflow/verification/fail-safe-update-release.md`
- `.planning/checkpoints/2026-07-25-fsr-final-verified.md`

At this historical checkpoint, integrated whole-goal review, `INT-001`,
`VER-001`, and `ROLLOUT-001` remained. They are superseded by the final closure
below. No live install, profile/App switch, plugin mutation, release, Git
publication, OpenSpec archive, or destructive cleanup ran during that source
verification step.

## 2026-07-25 Same-Version Self-Update Rollout Repair Verified

`fail-safe-update-release` is complete at 39/39 implementation tasks and 48/48
OpenSpec checkboxes after the rollout-discovered self-update and curated-cache
repairs. `FSR-002`, `INC-011`, and `ROLLOUT-001` are closed. Evidence:

- `.planning/devflow/verification/fail-safe-update-release.md`
- `.planning/verification/20260725151858-live-official-internal-rollout.md`
- `.planning/checkpoints/2026-07-25-fsr-same-version-rollout-verified.md`

No commit, push, tag, release, OpenSpec archive, dependency change, destructive
cleanup, parity implementation, or additional App restart was performed.

### Next Action

No further action is required for this repair. OpenSpec archive and the queued
`PARITY-001` remain separate, explicitly authorized work.

## 2026-07-26 TPS Desktop No-Op Incident Closed

`transactional-profile-state` is complete at 52/52 OpenSpec checkboxes.
The Desktop global-state no-op path no longer enters the transaction backup,
journal, rollback set, or frozen commit inputs. The exact pre-fix legacy
`rollback_failed` shape releases only strictly evidenced byte-identical no-op
effects; a real planned write remains fail closed.

Fresh source verification passed focused incident 4/4, transaction 219/219,
profile 198/198, strict OpenSpec 17/17, Bash 5/5, dual-runtime AST 54/54 and
production imports 46/46, isolated package validation with 64 files and payload
`ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab`,
and `git diff --check`.

The exact current payload is installed. The supported live recovery retired
backup `20260725T123636Z-switch-internal-to-openai-official` as
`rolled_back/recovered`, then committed official backup
`20260725T171620Z-switch-internal-to-openai-official`. ChatGPT pid `92488`
spawned official app-server pid `92903` from the ChatGPT bundle, completed
initialize, mounted routes, and served the expected App requests.

The supported restoration committed
`20260725T172136Z-switch-openai-official-to-internal`. Current ownership is
ChatGPT `95489`, managed proxy `95838` from the current payload, and backend
app-server `95842` at `/Users/cY/.local/bin/codex`. Repository-source status,
`verify internal --repair=none`, and Doctor pass.

Evidence:

- `.planning/devflow/verification/transactional-profile-state.md`
- `.planning/verification/20260725151858-live-official-internal-rollout.md`
- `.planning/checkpoints/2026-07-26-tps-desktop-noop-incident-verified.md`

### Next Action

The active Goal is now `internal-official-feature-parity`. Create its
independent Full OpenSpec, strictly validate the planning artifacts, then
execute its dependency-ordered TDD ledger. Commit, push, release, destructive
cleanup, dependency additions, and changing the fixed internal
binary/model/API/provider/auth boundary remain outside authorization.

## 2026-07-26 Internal/Official Feature Parity Planning Complete

After the Codex restart, the active Goal remained
`internal-official-feature-parity`. Repository ownership is unchanged:
`main`, `HEAD`, and `origin/main` are all `0a9400d`; the large pre-existing
dirty worktree was preserved.

The Full OpenSpec planning boundary is now durable:

- proposal, design, delta specs, and tasks all report `done`;
- the delta contains 12 requirements and 66 scenarios;
- the implementation ledger contains 79 unchecked tasks;
- the plan records Target State, Completion Contract, Acceptance Criteria,
  Capability Slices, Execution Ledger, validation, rollback, escalation, and
  the explicit live Desktop Human Gate.

The first plan-lint run found one structural omission: the acceptance criteria
were present in the Completion Contract but lacked the required explicit
heading. `tasks.md` now includes that heading and concrete pass conditions.
Fresh validation then passed:

- AI-native plan lint: passed;
- active-change strict OpenSpec validation: passed;
- all strict OpenSpec validation: 18/18 passed;
- DevFlow workflow validation: `ok: true`, with only the pre-existing
  legacy-root-state migration warning;
- `git diff --check`: passed.

No production implementation, install, internal update, profile/App mutation,
provider-backed probe, ChatGPT restart, retained-probe cleanup, dependency
change, commit, push, tag, release, archive, or destructive cleanup ran.
Evidence is
`.planning/checkpoints/2026-07-26-internal-official-feature-parity-planned.md`.

### Next Action

Stop at the design/spec/task review gate. After explicit review clearance,
execute task 1.1 through `openspec-apply-change`: add the first reference-policy
RED tests only, then run the recorded focused failure command before writing
production parity code.

## 2026-07-26 Parity Reference Foundation Verified

The Goal continuation cleared the source implementation review gate while
leaving every task 8.1 live effect gated. `internal-official-feature-parity`
tasks 1.1-1.3 are complete.

The first focused run failed exactly because `codex_switch_parity` did not
exist. The new module now provides the verified ChatGPT-bundle reference,
immutable fixed whitelist for binary/model/endpoint/provider/auth differences,
canonical official and internal fingerprints, stale-evidence checks, and the
planned immutable candidate/finding/queue/report/policy records. Runtime
Binding remains the authority for executable and Desktop-host intent.

Fresh results:

- parity reference suite: 7/7 on Python 3.12.13;
- parity reference suite: 7/7 on system Python 3.9.6;
- existing Runtime Binding suite: 55/55 on Python 3.12.13;
- Python 3.12 and 3.9 AST/import checks for the new module/test: passed;
- focused changed-file `git diff --check`: passed.

The only intermediate GREEN failure was a canonical JSON serialization error
for a read-only mapping. The serialization boundary now copies that mapping to
a plain dictionary before deterministic encoding.

No feature execution, schema comparison, overlay, config projection, probe,
caller integration, live profile/App state, provider traffic, retained-probe
cleanup, dependency, release, archive, or Git history mutation ran. Detailed
RED/GREEN evidence is
`.planning/devflow/verification/internal-official-feature-parity.md`.

### Next Action

Execute task 1.4 by RED: add feature-inventory tests for isolated defaults,
effective internal state, side-only feature retention, deterministic ordering,
malformed output, and canonical-byte stability. Do not add the feature runner
until that RED is captured.

## 2026-07-26 Parity Feature Inventory Verified

`internal-official-feature-parity` tasks 1.4-1.5 are complete. The recorded RED
failed because the feature inventory public seam did not exist. The parity
module now owns bounded `codex features list` execution behind an injected
runner, strict version-bound three-column parsing, isolated-default versus
effective-state separation, deterministic canonical inventory bytes, and
official/internal side-only feature comparison.

Malformed, duplicate, stage-changing, nonzero, timeout, and truncated results
fail closed with stable parity validation codes. Tests use isolated temporary
paths and injected command results; they do not read or write live config.

Fresh results:

- parity suite: 12/12 on Python 3.12.13;
- parity suite: 12/12 on system Python 3.9.6;
- Runtime Binding suite: 55/55 on Python 3.12.13;
- Runtime Binding suite: 55/55 on system Python 3.9.6;
- Python 3.12 and 3.9 AST/import checks for the parity module: passed;
- test-first capability dependency check: ready;
- legacy project-skill layout findings: nonblocking recommendations only.

No schema comparison, classification policy, receipt, overlay, config
projection, provider probe, caller integration, live profile/App mutation,
retained-probe cleanup, dependency change, release, archive, or Git history
mutation ran. Detailed evidence is
`.planning/devflow/verification/internal-official-feature-parity.md`.

### Next Action

Execute task 1.6 by RED: add direction-aware protocol inventory tests for all
four protocol directions, method-scoped transitive closure, deterministic
normalization, compatibility rules, cycles, and unsupported constructs. Do not
implement the protocol evaluator until that RED is captured.

## 2026-07-26 Parity Protocol Inventory RED

`internal-official-feature-parity` task 1.6 is complete. Eight new
`ParityProtocolInventoryTests` define the parity-owned public seam for:

- client requests and notifications;
- server requests and notifications;
- method extraction and transitive local `$ref` closure;
- documentation-insensitive deterministic canonical bytes;
- official-only and internal-only method retention;
- producer-direction compatibility;
- additive optional properties;
- required-field and enum incompatibility;
- reference-cycle rejection; and
- unsupported-schema fail-closed behavior.

The test file passed AST parsing. The focused suite then failed at import with
the expected missing `ProtocolInventory` public type. No production code,
Protocol Adapter policy, live state, or external effect changed.

### Next Action

Execute task 1.7: implement method-scoped schema normalization and the
direction-aware compatibility evaluator inside `codex_switch_parity.py`, then
make the protocol RED tests GREEN.

## 2026-07-26 Parity Protocol Inventory Verified

`internal-official-feature-parity` task 1.7 is complete. The parity module now
owns method-scoped transitive schema normalization and direction-aware native
compatibility comparison for all four protocol directions. Local references
are expanded, documentation-only fields are removed, canonical ordering is
stable, side-only methods remain visible, and unsupported constructs fail
closed.

The retained real-schema smoke exposed valid Draft-07 boolean schemas in array
`items`. Focused RED tests then also proved false-health gaps for boolean
property schemas, boolean combinator branches, and an explicit
`additionalProperties` restriction. The implementation applies one schema
subset rule across those positions while retaining stable reason-code
families.

Fresh results:

- parity suite: 25/25 on Python 3.12.13;
- parity suite: 25/25 on system Python 3.9.6;
- real schema inventory on both runtimes: 347 official documents and 337
  internal documents;
- real normalized methods: 208 official and 202 internal;
- real comparison: 208 merged entries, 15 raw native incompatibilities, and
  six retained side-only methods;
- official inventory digest:
  `323adadf709882fe18aba53c76e5fa4a2310ac1d87ce895ebb9b0fc6e28ca146`;
- internal inventory digest:
  `880578b7724156225e5f3bff4268d92be3b980de842ba9e1223466056438a9c1`;
- Runtime Binding: 55/55 on both Python runtimes;
- dual-runtime AST/import, source-owned TDD capability, parity-authority scan,
  and `git diff --check`: passed.

The 15 native incompatibilities are inventory evidence only; core/optional/
unclassified health policy remains task 1.10-1.11. Protocol Adapter was not
modified, and no live profile/App/provider effect, retained-schema cleanup,
dependency change, release, archive, or Git history mutation ran.

### Next Action

Execute task 1.8 by RED: add Protocol Adapter evidence tests proving the
existing adapter exposes one deterministic rule-set digest without importing
parity policy.

## 2026-07-26 Protocol Adapter Rule-Set Digest RED

`internal-official-feature-parity` task 1.8 is complete. Two
`ProtocolAdapterEvidenceTests` now define the narrow adapter-owned evidence
seam:

- one deterministic lowercase SHA-256 digest;
- canonical mapping-order independence;
- digest sensitivity to the exact request, response, and notification
  model-path tables, config-write method set, and remote-marketplace literal;
- no import of `codex_switch_parity` or parity policy.

The test file passes AST parsing. The focused two-test run and the complete
39-test Protocol Adapter suite fail only at the expected missing
`protocol_adapter_rule_set_digest` seam; all 37 pre-existing tests pass.
Neither Protocol Adapter production code nor parity policy changed.

### Next Action

Execute task 1.9: implement the deterministic digest from the existing exact
Protocol Adapter transform tables, then bind that evidence into parity input
without moving classification policy into the adapter.

## 2026-07-26 Protocol Adapter Rule-Set Digest Verified

`internal-official-feature-parity` task 1.9 is complete. Protocol Adapter now
exposes one deterministic digest over the exact request, response, and
notification model-path tables, config-write method set, and
remote-marketplace literal. The canonical digest is
`b9ac004f3801eaf094745e6e45754c7e5a058b33775746e49682aef7c240f849`
on both Python 3.12.13 and system Python 3.9.6.

`ParityCandidate` requires the digest as caller-supplied
`adapter_rule_set_sha256` evidence and rejects non-canonical values with
`parity.candidate.adapter_rule_set_digest_invalid`. Protocol Adapter remains
policy-free, parity does not import adapter implementation, and neither module
owns the other's policy.

Fresh results are Protocol Adapter 39/39 and parity 26/26 on both supported
Python runtimes. Dual-runtime AST/import checks, strict active OpenSpec
validation, ownership scans, and `git diff --check` pass. No classification,
receipt, overlay, config projection, probe, caller integration, live state,
dependency, retained-evidence cleanup, release, archive, or Git history
mutation ran.

### Next Action

Execute task 1.10 by RED: add `ParityPolicyTests` for the approved core,
optional-unless-observed, optional, pending-provider, escalation, and unknown
drift classifications without implementing policy yet.

## 2026-07-26 Parity Policy RED

`internal-official-feature-parity` task 1.10 is complete. Eight
`ParityPolicyTests` define one parity-owned `evaluate_parity_policy` seam over
the existing feature/protocol comparisons, official/internal active-model
metadata, and observed protocol/feature sets.

The contracts cover baseline initialize/config/model/collaboration/thread/
turn/item/tool/approval/completion closures, `multi_agent_v2`, the six exact
official-only optional-unless-observed methods, `skill_search`, known
under-development features, stage/default-only drift, pending-provider
`tool_mode`, observed escalation, unknown drift, stable code/severity/health
semantics, and deterministic finding/queue sorting.

Python 3.12.13 and system Python 3.9.6 each ran 34 parity tests. All 26 existing
tests passed; the eight new tests failed only with
`Parity policy evaluation seam is missing`. The test file passes AST parsing
on both runtimes and `git diff --check` passes. No production policy or other
implementation changed.

### Next Action

Execute task 1.11: implement the explicit versioned policy table and
`evaluate_parity_policy`, then make all eight policy tests GREEN without
moving classification into Runtime Binding, Protocol Adapter, or callers.

## 2026-07-26 Parity Policy Verified

`internal-official-feature-parity` task 1.11 is complete. The parity module now
owns one immutable classification table keyed by policy version `1` and one
`evaluate_parity_policy` seam. It classifies approved core protocol families,
the six exact optional-unless-observed methods, core and optional feature sets,
metadata-only drift, active-model v2 metadata, pending-provider `tool_mode`,
observed escalation, and unknown drift.

The result applies stable core, optional, observed-core, pending-provider, and
unclassified finding-code families. Error findings make the result unhealthy;
warnings remain visible in a synchronization queue sorted by category,
identifier, and finding code. A bounded review RED/GREEN guard additionally
proves that known official-optional labels do not whitelist internal-only
protocol or feature drift.

Fresh dual-runtime results are parity 35/35, Protocol Adapter 39/39, and Runtime
Binding 55/55. The retained real 347-official/337-internal schema comparison
classifies identically on Python 3.12.13 and system Python 3.9.6: unhealthy,
8 core incompatibilities, 6 exact optional queue items, and 3 unclassified
methods (`account/login/start`, `externalAgentConfig/import`, and
`plugin/share/updateTargets`). Strict active OpenSpec validation, AI plan lint,
dual-runtime AST/import, classification-authority scan, and
`git diff --check` pass.

No caller integration, receipt, overlay, config projection, probe, live state,
dependency, retained-evidence cleanup, release, archive, or Git history
mutation ran.

### Next Action

Execute task 1.12: add and pass serialization tests proving inventory and
future receipt-facing policy payloads retain no credential, raw config/prompt/
model output, authorization/query secret, absolute temporary probe path, or
unbounded process text.

## 2026-07-26 Parity Serialization Verified

`internal-official-feature-parity` task 1.12 is complete. Three
`ParitySerializationTests` prove:

- feature inventory canonical bytes omit runner stderr, command/home context,
  and a 128 KiB external-output payload;
- protocol inventory canonical bytes omit documentation fields containing the
  same sensitive payload; and
- receipt-facing policy bytes use a structural allowlist containing only
  health, policy version, finding category/code/severity, and validated queue
  identity.

Free-text finding message/expected/observed fields are not serialized. The
fixtures include a credential value and 64-character credential digest,
Authorization and query secrets, raw config, raw prompt, raw model output, an
absolute temporary probe path, and unbounded process text; none enters
canonical bytes. Queue identifiers are bounded and grammar-checked, and unsafe
absolute-path identity fails with
`parity.policy.serialization_invalid`.

Fresh parity results are 38/38 on Python 3.12.13 and system Python 3.9.6.
Strict active OpenSpec validation, AI plan lint, dual-runtime AST/import, and
`git diff --check` pass. No receipt file, overlay, probe, caller integration,
live state, dependency, retained-evidence cleanup, release, archive, or Git
history mutation ran.

### Next Action

Execute task 1.13: rerun the complete parity suite on both Python runtimes
after this control-plane edit, record exact counts, and only then select task
2.1.

## 2026-07-26 Parity Reference/Inventory Slice Verified

`internal-official-feature-parity` task 1.13 is complete. After the Codex
restart boundary, the complete parity suite was rerun from the preserved dirty
worktree:

- Python 3.12.13: 38/38 in 0.066s;
- system Python 3.9.6: 38/38 in 0.071s.

Tasks 1.1-1.13 now provide deterministic bundled-reference, feature, protocol,
adapter-digest, classification, queue, and sanitized receipt-facing policy
evidence. The retained real-schema result remains intentionally unhealthy with
8 core incompatibilities, 6 optional queue items, and 3 unclassified methods;
later receipt, overlay, adapter-coverage, and probe work must resolve the
applicable core contract before any promotion claim.

No receipt or overlay file, probe, caller integration, live profile/App/provider
state, dependency, retained-evidence cleanup, release, archive, or Git history
mutation ran. Progress is 13/79.

### Next Action

Create and validate the Reference/inventory checkpoint, then execute task 2.1
by RED: add `ParityReceiptTests` for the approved canonical receipt, path,
manifest, malformed-state, staleness, and optional-queue contracts.

## 2026-07-26 Parity Receipt RED

`internal-official-feature-parity` task 2.1 is complete. Eight
`ParityReceiptTests` now specify the parity-owned receipt seam:

- canonical byte-identical payloads with current schema/policy version;
- complete official/internal fingerprints and inventory, adapter, overlay, and
  bounded probe evidence digests;
- profile-local `parity/receipt.json` and `parity/model-catalog.json` paths;
- `0700` parity directory and `0600` regular non-symlink receipt;
- exact receipt-facing manifest metadata;
- optional synchronization queue retention without unhealthy status;
- stable failure codes for missing, unsafe, mode-invalid, oversized,
  malformed, unsupported, and digest-mismatched receipts; and
- stale detection for official-reference, provider, and backend changes.

Python 3.12.13 and system Python 3.9.6 each ran 46 tests. The 38 pre-existing
tests passed; the eight new methods failed only because
`PARITY_RECEIPT_SCHEMA_VERSION`, `ParityReceipt`, `ParityReceiptArtifact`,
`resolve_parity_artifact_paths`, `write_parity_receipt_artifact`, and
`load_parity_receipt_artifact` do not exist yet. Subtests expand this to 12
failure reports with zero errors. Both runtimes compile the test file, and the
focused diff check passes.

No parity production code, caller, manifest promotion, overlay implementation,
live state, dependency, release, archive, cleanup, or Git history changed.
Progress is 14/79.

### Next Action

Execute task 2.2: implement the smallest bounded canonical receipt,
profile-local path resolver, mode-safe artifact writer, and no-follow
identity-checked loader required to make all eight receipt tests GREEN. Do not
integrate receipt preparation into callers.

## 2026-07-26 Parity Receipt Verified

`internal-official-feature-parity` task 2.2 is complete. The parity module now
owns receipt schema version `1`, a bounded canonical `ParityReceipt`, immutable
artifact/path records, and exact internal profile artifact resolution:

- `profiles/internal/parity/receipt.json`;
- `profiles/internal/parity/model-catalog.json`.

Receipt payloads bind the complete official reference and internal fingerprint,
feature/protocol inventory digests, Protocol Adapter rule-set digest, overlay
path/digest/change set, bounded probe result codes/digests, current policy,
findings, queue, and health. Writer operations pin the profile/parity
directories with no-follow descriptors, create a mode-`0600` temporary file,
fsync it, and rename it inside the pinned mode-`0700` directory. The loader
rejects missing, symlinked, non-regular, wrong-mode, oversized, digest-drifted,
duplicate-key, malformed, unsupported, non-canonical, or stale evidence before
returning a reusable artifact.

Fresh results:

- parity: 46/46 on Python 3.12.13 and system Python 3.9.6;
- Protocol Adapter: 39/39 on both runtimes;
- Runtime Binding: 55/55 on both runtimes;
- strict active OpenSpec and AI-native plan lint: passed;
- dual-runtime AST/import and `git diff --check`: passed;
- ownership scan: no Protocol Adapter, Runtime Binding, binding, or verifier
  caller imports or reconstructs the parity receipt.

No receipt preparation is connected to callers, no overlay is generated, and
no live profile/App/provider state, dependency, release, archive, cleanup, or
Git history changed. Progress is 15/79.

### Next Action

Execute task 2.3 by RED: add `ParityOverlayTests` for unique active-model
selection, absent-to-v2 or already-v2 exact diffs, deep source preservation,
unsafe source shapes/identities, broader mutation rejection, and source race
detection. Do not implement overlay generation until the RED is captured.

## 2026-07-26 Parity Overlay RED

`internal-official-feature-parity` task 2.3 is complete. Eight
`ParityOverlayTests` now specify the parity-owned overlay seam:

- unique active-model slug selection and exact active index;
- the sole allowed addition
  `/models/<index>/multi_agent_version = "v2"`;
- already-v2 zero semantic diff and canonical overlay bytes;
- deep preservation plus byte- and mode-preserved source catalogs;
- stable rejection of missing/duplicate slugs, unsupported roots, symlinks,
  directories, and source `v1`;
- stable rejection of added or changed `tool_mode`;
- stable rejection of provider/API/reasoning/instruction/modality/visibility,
  other-model, and top-level mutations; and
- stale rejection for pre-read digest drift and during-read inode/content
  races.

Python 3.12.13 and system Python 3.9.6 each ran 54 tests. All 46 pre-existing
tests passed; the eight new methods produced 17 expected subtest failures only
because `ParityOverlayArtifact`, `prepare_parity_overlay`, and
`validate_parity_overlay` do not exist yet. Both runtimes compile the test
file, and the focused diff check passes.

No parity production code, overlay file, caller, manifest promotion, live
profile/App/provider mutation, dependency, release, archive, cleanup, or Git
history changed. Progress is 16/79.

### Next Action

Execute task 2.4: implement bounded no-follow and identity-checked source
reading, deep-copy overlay generation, exact JSON-pointer validation, canonical
payload bytes, and source/overlay digest evidence. Keep generation disconnected
from callers and promoted paths.

## 2026-07-26 Parity Overlay Verified

`internal-official-feature-parity` task 2.4 is complete. The parity module now
owns a bounded source-preserving managed-overlay seam:

- source catalogs are opened no-follow and bounded to 16 MiB;
- lstat/open/fstat/post-read identity, size, mode, mtime, ctime, and expected
  digest must remain stable;
- duplicate keys, non-finite constants, unsupported roots, unsafe files,
  missing/duplicate active slugs, and non-absent/non-v2 source metadata fail
  with stable overlay codes;
- generation deep-copies the parsed catalog and adds only the active model's
  `multi_agent_version = "v2"` when absent;
- recursive JSON Pointer diff validation rejects `tool_mode`, provider/API,
  reasoning, instructions, modalities, visibility, another model, root, or
  any other mutation;
- canonical overlay bytes, source/overlay SHA-256 evidence, source mode,
  active slug/index, and immutable approved changes are bound in
  `ParityOverlayArtifact`; and
- direct artifact construction revalidates canonical JSON, active-model v2,
  digest, and empty-or-single-add change evidence.

Fresh results:

- overlay: 8/8 on Python 3.12.13 and system Python 3.9.6;
- parity: 54/54 on both runtimes;
- Protocol Adapter: 39/39 on both runtimes, run serially because concurrent
  cross-runtime probe suites share test state;
- Runtime Binding: 55/55 on both runtimes;
- strict active OpenSpec, AI-native plan lint, dual-runtime AST, authority
  scans, and `git diff --check`: passed.

A read-only run against
`/Users/cY/.codex/model-catalogs/azure-models.json` selected model index `0`,
preserved source SHA-256 `75c9e8d4dadbe3f612f1b6fbabfe6785c312460bd6b5bedfe1565acdedd41f9a`
and mode `0600`, generated only
`/models/0/multi_agent_version = "v2"`, and produced canonical overlay SHA-256
`2437757759c89c96dbee4204d716ad77f3b7a24bb1b96d6fef9dfc9ad290d85f`.

No overlay was written or promoted; no caller, live profile/App/provider state,
dependency, release, archive, cleanup, or Git history changed. Progress is
17/79.

### Next Action

Execute task 2.5 by RED: specify complete manifest-candidate binding for the
receipt and overlay paths/digests, policy/reference/source digests, and
adapter/capability evidence before any promotion.

## 2026-07-26 Parity Manifest Candidate RED

`internal-official-feature-parity` task 2.5 is complete. Four
`ParityBundleManifestTests` now specify:

- the exact manifest candidate fields for receipt/overlay target paths and
  payload digests, policy version, official-reference digest, source-catalog
  path/digest, Protocol Adapter digest, capability-receipt digest, and internal
  fingerprint digest;
- stable rejection of every missing or mismatched field before promotion;
- a private `0700` staging root containing only regular mode-`0600`
  `receipt.json` and `model-catalog.json`; and
- zero writes to the final profile parity directory while preserving source
  catalog bytes and mode.

Python 3.12.13 and system Python 3.9.6 each ran the focused four tests and the
complete 58-test parity suite. Both runtimes produced the same four expected
failures only because `ParityBundle` and
`prepare_parity_bundle_artifacts` do not exist; all 54 pre-existing tests pass.
The focused diff check passes.

No production code, profile artifact, caller, live profile/App/provider state,
dependency, release, archive, cleanup, or Git history changed. Progress is
18/79.

### Next Action

Execute task 2.6: implement immutable `ParityBundle`, exact manifest metadata
validation, and private receipt/overlay staging. Keep final profile paths
unwritten and do not integrate callers or transaction promotion.

## 2026-07-26 Parity Receipt/Overlay Slice Verified

`internal-official-feature-parity` tasks 2.6-2.7 are complete, closing the
receipt/overlay capability slice at 20/79.

The parity module now provides immutable `ParityBundle` and
`prepare_parity_bundle_artifacts` seams that:

- require receipt and overlay evidence to bind the same target path, source
  catalog, source digest, active model, overlay digest, and exact change set;
- generate an exact 12-key manifest candidate covering receipt/overlay paths
  and payload digests, policy version, official/internal fingerprints, source
  catalog path/digest, Protocol Adapter digest, capability-receipt digest, and
  receipt schema version;
- reject every missing, extra, or mismatched manifest field;
- stage canonical receipt and overlay bytes as fsynced regular `0600` files
  under one private mode-`0700` temporary directory; and
- leave the final `profiles/internal/parity/` targets absent until the later
  schema-v3 transaction task.

Fresh results:

- Parity: 58/58 on Python 3.12.13 and system Python 3.9.6;
- Protocol Adapter: 39/39 on both runtimes, run serially;
- Runtime Binding: 55/55 on both runtimes, run serially;
- focused source structure/byte/mode preservation: 3/3 on both runtimes;
- strict active OpenSpec, AI-native plan lint, dual-runtime AST/import,
  no-caller authority scan, and `git diff --check`: passed.

No caller imports the bundle seam. No final profile artifact, transaction,
rebind, update, live profile/App/provider state, dependency, release, archive,
cleanup, or Git history changed.

### Next Action

Execute task 3.1 by RED: specify internal config projection for
`model_catalog_json`, `features.multi_agent_v2 = true`, exact scalar
`agents.max_threads` removal, unrelated-setting preservation, and idempotence
across parity and Config Document tests.

## 2026-07-26 Parity Config Projection RED

`internal-official-feature-parity` task 3.1 is complete. The approved test
seams are now explicit:

- Parity owns immutable `ConfigInputs`, `ConfigProjection`, and
  `prepare_parity_config_projection` behavior.
- Config Document owns one exact scalar-assignment removal method rather than a
  generic TOML rewrite framework.
- Only the internal profile receives the managed `model_catalog_json` and
  `features.multi_agent_v2 = true` projection.
- The one authoritative `[agents].max_threads` assignment is removed while the
  section, sibling keys, comments where structurally possible, and unrelated
  profile/shared settings remain.
- Source files remain byte-identical during preparation, and already-clean
  inputs produce a byte-identical deterministic no-op projection.

Fresh RED results:

- Parity Python 3.12.13: 60 tests, 58 passed and 2 expected failures.
- Parity system Python 3.9.6: 60 tests, 58 passed and 2 expected failures.
- Config Document Python 3.12.13: 26 tests, 24 passed and 2 expected failures.
- Test compile and focused `git diff --check`: passed.

The parity failures name only the missing `ConfigInputs`, `ConfigProjection`,
and `prepare_parity_config_projection` seams. The Config Document failures name
only missing `ConfigDocument.remove_exact_scalar_assignment`. There are no
errors or unrelated regressions.

No production code, source config, caller, active profile/App/provider state,
dependency, release, archive, cleanup, or Git history changed. Progress is
21/79.

### Next Action

Execute task 3.2 by RED: add duplicate, dotted, non-scalar, invalid TOML,
multiply sourced, symlinked, and concurrent-change config migration tests.
Require stable unhealthy evidence and prove every source file remains
byte-identical.

## 2026-07-26 Parity Config Ambiguity/TOCTOU RED

`internal-official-feature-parity` task 3.2 is complete. Seven parity tests now
cover duplicate, dotted, non-scalar, invalid-TOML, multiply sourced, symlinked,
and concurrently replaced `agents.max_threads` inputs. Invalid preparation
must return one stable unhealthy error finding with no changed paths or
authoritative removal source; all regular source bytes remain unchanged, and
the concurrent-replacement fixture preserves bytes while changing identity.

Two direct Config Document tests require the exact removal seam to reject
dotted and non-scalar forms with `config_exact_assignment_ambiguous`.

Fresh RED results:

- Parity Python 3.12.13: 67 tests, 58 passed and 9 expected failures.
- Parity system Python 3.9.6: 67 tests, 58 passed and 9 expected failures.
- Config Document Python 3.12.13: 28 tests, 24 passed and 4 expected failures.
- Test compile and focused `git diff --check`: passed.

Every parity failure still names only missing `ConfigInputs`,
`ConfigProjection`, and `prepare_parity_config_projection`. Every Config
Document failure names only missing
`ConfigDocument.remove_exact_scalar_assignment`. No production code, source
config, caller, live state, dependency, release, archive, cleanup, or Git
history changed. Progress is 22/79.

### Next Action

Execute task 3.3: implement the smallest exact Config Document removal seam and
parity-owned safe config projection. Reparse every successful payload, return
stable unhealthy findings for ambiguity/unsafe/stale inputs, and make all 13
projection/removal RED tests GREEN without caller integration.

## 2026-07-26 Parity Config Projection GREEN

`internal-official-feature-parity` task 3.3 is complete. The Config Document now
removes only one exact scalar table assignment and reparses the result. Parity
owns immutable config inputs/projection records, bounded no-follow reads,
internal-only `model_catalog_json` and `features.multi_agent_v2 = true`
projection, exact `agents.max_threads` removal, and stable unhealthy findings
for ambiguous, invalid, unsafe, oversized, or stale sources.

Main review found one false-health gap after the interrupted session: an earlier
source could be replaced with the same bytes while a later source was being
read. A focused regression failed with a healthy projection, then passed after
adding final identity/digest revalidation for every source before returning the
payload set.

Fresh results:

- Parity: 69/69 on Python 3.12.13 and system Python 3.9.6;
- Config Document: 29/29 on Python 3.12.13;
- Protocol Adapter: 39/39 on both runtimes, run serially;
- Runtime Binding: 55/55 on both runtimes, run serially;
- focused cross-source TOCTOU RED/GREEN: 1/1 on both runtimes after the fix;
- AI-native plan lint and strict active/all OpenSpec validation: passed;
- dual-runtime production imports and AST parse, `py_compile`, no-caller
  authority scans, and `git diff --check`: passed.

No caller imports the projection seam. No source config, canonical home-sync,
transaction, rebind, update, live profile/App/provider state, dependency,
release, archive, cleanup, or Git history changed. Progress is 23/79.

### Next Action

Execute task 3.4 by RED only: add home-sync tests proving internal profile and
shared sources derive a managed-home config with the managed overlay and v2,
without stale max threads, while official/shared source bytes and unrelated
profile settings remain correct. Do not integrate production home sync until
task 3.5.

## 2026-07-26 Parity Home Sync RED

`internal-official-feature-parity` task 3.4 is complete. Two focused profile
tests now require canonical home sync to consume one healthy
`ConfigProjection` for both an unmaterialized internal home and a materialized
home containing stale model, feature, and agent values. The expected derived
text selects the managed overlay, enables `multi_agent_v2`, preserves unrelated
profile/provider/shared settings, removes only `agents.max_threads`, and leaves
profile, shared, and existing runtime files byte-identical.

Fresh RED results:

- Python 3.12.13: 2 tests, 2 expected assertion failures, 0 errors.
- System Python 3.9.6: 2 tests, 2 expected assertion failures, 0 errors.
- Python 3.12.13 adjacent home-sync/profile regressions: 6/6.
- Test compile and focused `git diff --check`: passed.

The first failure observes no projected `model_catalog_json`; the second
observes `stale-model` from the materialized runtime instead of the projected
profile model. Direct execution of the six older adjacent tests under system
Python 3.9 remains blocked by their existing Python 3.11+ `tomllib`
requirement, while the new focused tests use their bounded parser fixture and
exercise both runtimes.

No production code, source/runtime config, transaction, rebind, update, live
profile/App/provider state, dependency, release, archive, cleanup, or Git
history changed. Progress is 24/79.

### Next Action

Execute task 3.5: add the smallest canonical home-sync seam that consumes a
healthy projection and returns staged managed-home text without writing profile,
shared, or materialized runtime sources. Make both task 3.4 tests GREEN and run
the adjacent regression set before selecting task 3.6.

## 2026-07-26 Parity Home Sync GREEN

`internal-official-feature-parity` task 3.5 is complete. Canonical internal
home derivation now accepts one healthy `ConfigProjection`, requires it to match
the internal profile and canonical shared input, and consumes its projected
payloads entirely in memory. Projected profile-specific values are the only
profile seed, projected profile shared state contributes
`features.multi_agent_v2 = true`, and an existing materialized runtime is not
used to recover stale model, feature, or `agents.max_threads` values.

The resulting managed-home config is returned as staged text. Profile, shared,
and materialized runtime inputs remain byte-identical; no caller commits the
text in this task.

Fresh results:

- Focused home-sync projection: 2/2 on Python 3.12.13 and system Python 3.9.6.
- Adjacent home-sync/profile regressions: 6/6 on Python 3.12.13.
- Full profile suite: 200/200 on Python 3.12.13.
- Full transaction suite: 219/219 on Python 3.12.13.
- Parity: 69/69 on Python 3.12.13 and system Python 3.9.6.
- Config Document: 29/29 on Python 3.12.13.
- Dual-runtime home-sync import/compile and focused diff checks: passed.

The attempted direct full Config Document run under system Python 3.9
reproduced the existing unsupported-parser baseline because that suite requires
Python 3.11+ `tomllib`; the parity and focused home-sync tests install their
bounded parser fixture and passed on 3.9.

No profile/App/provider state, source/runtime config, transaction promotion,
dependency, release, archive, cleanup, or Git history changed. Progress is
25/79.

### Next Action

Execute task 3.6 by RED only: add bounded candidate-only parity probe tests for
initialize/core ordering, typed `explorer` v2 behavior, no v1 fallback,
timeouts, malformed or oversized output, process-group termination, stale
inputs, and sanitizer boundaries. Do not implement probe orchestration until
task 3.7.

## 2026-07-26 Parity Probe RED

`internal-official-feature-parity` task 3.6 is complete. Ten focused tests now
define candidate-only backend/config/overlay/capability binding, canonical
initialize/core request ordering, typed explorer v2 child and parent markers,
no v1 or nickname-only fallback, distinct timeout/malformed/missing/early-exit/
oversized results, complete process-group termination, post-run input
revalidation, and bounded secret-stable evidence digests.

Fresh RED results:

- Python 3.12.13: 79 tests, 69 passed and 10 expected failures, 0 errors.
- System Python 3.9.6: 79 tests, 69 passed and 10 expected failures, 0 errors.
- Test compile and focused `git diff --check`: passed.

Every failure names only the six missing probe seams. No production probe,
provider call, source/runtime config write, live profile/App mutation,
dependency, release, archive, cleanup, or Git history change occurred.
Progress is 26/79.

### Next Action

Execute task 3.7: implement the smallest immutable probe input/request/result/
report model, bounded default process runner, structured core/v2 validators,
stable findings and sanitized evidence digests. Make all ten probe tests GREEN
without integrating a caller or retaining raw output.

## 2026-07-26 Parity Probe GREEN

`internal-official-feature-parity` task 3.7 is complete. The parity module now
owns immutable candidate probe inputs and result records, no-follow artifact
snapshots and post-run revalidation, a bounded default runner that terminates
the complete process group, ordered core app-server response checks, and exact
typed explorer v2 spawn/child/parent completion validation.

Only stable status codes and sanitized evidence digests enter the report.
Review guards reject mixed v1/v2 output, multiple v2 spawns, completion-order
drift, and secret-dependent digests for sensitive headers, assignments, URL
userinfo, bearer values, and signed query parameters. A deterministic shell
fixture now proves descendant `SIGTERM` resistance followed by group-wide
termination without depending on Python startup latency.

Fresh results:

- Focused probes: 12/12 on Python 3.12.13 and system Python 3.9.6.
- Complete parity: 81/81 on Python 3.12.13 and system Python 3.9.6.
- Dual-runtime AST/import/export checks: passed.
- Focused `git diff --check` and process-residue inspection: passed.

The TDD methodology is ready. The broader dependency diagnostic still reports
the established unrelated project DevFlow skill-layout source conflicts; no
activation, migration, or legacy cleanup was authorized or performed.

No caller integration, retained probe fixture, provider call, source/runtime
write, live profile/App mutation, dependency, release, archive, cleanup, or Git
history change occurred. Progress is 27/79.

### Next Action

Execute task 3.8 by adding a retained redacted provider-structure fixture and
prove the probe path never copies a live credential-bearing config into
retained evidence. Keep all fixture and execution state isolated and do not run
a live provider probe.

## 2026-07-26 Retained Probe Fixture Verified

`internal-official-feature-parity` task 3.8 is complete. A synthetic retained
fixture now lives at
`testdata/parity/retained-v2-probe-redacted.json`, outside the release bundle
allowlist. It preserves provider id/name, Azure-style base URL, Responses wire
API, auth-source key name, API-version query structure, core responses, and
typed explorer v2 events while using only `[REDACTED]` credential values and a
safe routing marker.

The regression starts from two isolated temporary candidate configs containing
different transient API-key values. Both produce byte-identical healthy reports
and receipt digests. Neither secret, raw config bytes, nor config path enters
the retained report, and a before/after file-tree comparison proves the probe
path creates no config copy or other candidate file.

Fresh results:

- Focused retained fixture: 1/1 on Python 3.12.13 and system Python 3.9.6.
- Complete parity: 82/82 on Python 3.12.13 and system Python 3.9.6.
- Dual-runtime fixture JSON/AST/secret scans: passed.
- Focused `git diff --check`: passed.

The historical retained v2 probe directory was listed only for names and file
modes. Its credential-bearing config content was not read, copied, rewritten,
or deleted.

No live provider call, profile/App mutation, source/runtime write, dependency,
release, archive, cleanup, or Git history change occurred. Progress is 28/79.

### Next Action

Execute task 3.9 by rerunning parity, Config Document, home-sync/profile
focused, and verifier sanitizer suites on both required runtimes where
supported. Record the established system-Python Config Document parser boundary
without treating it as a changed-path failure, then select task 4.1 only if the
complete slice verification is clean.

## 2026-07-26 Config and Probe Slice Verified

`internal-official-feature-parity` task 3.9 and the Config/probes slice are
complete. This item changed no production source. Fresh results:

- Complete parity: 82/82 on Python 3.12.13 and system Python 3.9.6.
- Config Document: 29/29 on Python 3.12.13.
- Direct Config Document on system Python 3.9.6: the established unsupported
  `tomllib` baseline, exactly 3 failures and 22 errors.
- Focused home-sync parity projection: 2/2 on both runtimes.
- Verifier: 22/22 on Python 3.12.13 and 22/22 on the supported system-Python
  route with `CODEX_SWITCH_PYTHON=/opt/homebrew/bin/python3.12`.
- Native system-Python verifier sanitizer focus: 2/2.
- Strict active OpenSpec, dual-runtime AST for all 56 scripts, dual-runtime
  production imports for parity/config-document/home-sync/verify, and
  `git diff --check`: passed.

An initial unpinned full verifier run under system Python produced eight errors
only while generating a managed wrapper because `sys.executable` was Python
3.9. The established supported test route explicitly supplies a Python 3.11+
wrapper interpreter and passed the complete 22-test suite. Generated bytecode
was removed after testing.

No live provider call, profile/App mutation, source/runtime write, dependency,
release, archive, provider migration, legacy-skill cleanup, or Git history
effect occurred. Progress is 29/79.

### Next Action

Execute task 4.1 by RED. Add schema-v3 journal tests in
`scripts/test_codex_transaction.py` for the exact required manifest, launcher,
capability receipt, parity receipt, overlay, and profile config targets plus
the optional shared and active runtime config targets. Do not implement the
bundle transaction until the focused expected failures are captured.

## 2026-07-26 Runtime Bundle Target-Set RED

`internal-official-feature-parity` task 4.1 is complete as tests-only RED.
`scripts/test_codex_transaction.py` now specifies:

- required roles: manifest, launcher, capability receipt, parity receipt,
  parity overlay, and internal profile config;
- optional roles: authoritative shared config and active internal runtime
  config, each present only when explicitly supplied;
- all four optional-role combinations;
- schema-v3 prepared marker entries with exact role/path and new file mode; and
- a hard `after_marker` interruption that leaves every target byte unchanged.

Python 3.12.13 and system Python 3.9.6 each ran two test methods and produced
five expected failure reports, with zero errors. Every failure names only the
missing `RuntimeBindingTextArtifact` and `commit_runtime_binding_bundle` seams.
The four adjacent v1/v2 runtime-rebind tests pass on both runtimes. Strict
active OpenSpec, dual-runtime test compile, whitespace and diff integrity, and
generated-bytecode cleanup passed.

No production code, runtime target, profile/App/provider state, dependency,
release, archive, migration, cleanup, or Git history effect occurred. Progress
is 30/79.

### Next Action

Execute task 4.2 by RED. Add duplicate, unexpected, parent/child-overlap,
symlink, directory, missing-required, invalid-mode, digest-invalid, oversized
payload, and foreign old/new target safety contracts. Require every invalid
bundle to fail before marker creation or target writes.

## 2026-07-26 Runtime Bundle Target-Safety RED

`internal-official-feature-parity` task 4.2 is complete as tests-only RED.
`scripts/test_codex_transaction.py` now specifies:

- duplicate, unexpected, parent/child-overlapping, and missing-required target
  set rejection;
- symlink and directory target rejection;
- exact `0755` launcher and `0600` non-launcher mode enforcement;
- rejection of a payload larger than the existing maximum parity catalog
  artifact before marker creation;
- schema-v3 old/new embedded-state digest validation; and
- prepared rollback and committed roll-forward preflight that refuses a target
  matching neither recorded state before changing any other old/new target.

Python 3.12.13 and system Python 3.9.6 each ran five task-4.2 methods with 13
expected failure reports and zero errors. The combined task 4.1-4.2 RED set is
seven methods with 18 expected reports and zero errors on each runtime. Every
report names only the missing `RuntimeBindingTextArtifact` and
`commit_runtime_binding_bundle` seams. Existing schema-v1/v2 runtime-rebind
tests pass 4/4 on both runtimes. Dual-runtime AST and trailing-whitespace checks
pass.

No production code, runtime marker or target, live profile/App/provider state,
dependency, release, archive, migration, cleanup, or Git history effect
occurred. Progress is 31/79.

### Next Action

Execute task 4.3 GREEN by adding the typed text-artifact entry and
compatibility-preserving schema-v3 bundle implementation. Strict active
OpenSpec, `git diff --check`, dual-runtime AST, trailing-whitespace, and
generated-bytecode checks passed after the task-4.2 control-plane update. Do
not begin the task-4.4 fault matrix before task 4.3 is green and reviewed.

## 2026-07-26 Runtime Bundle Schema-v3 GREEN

`internal-official-feature-parity` task 4.3 is complete.
`scripts/codex_switch_transaction.py` now provides:

- immutable `RuntimeBindingTextArtifact` entries;
- exact required and optional role/path allowlist validation;
- duplicate, parent/child-overlap, target-type, mode, and 16 MiB payload
  rejection before marker creation;
- deterministic parity overlay, receipts, config sources, derived config,
  launcher, and manifest-last activation order;
- schema-v3 marker field, path, order, embedded payload, digest, and mode
  validation;
- full old/new foreign-state preflight before recovery writes;
- a target-level old/new recheck immediately before each recovery write; and
- compatibility-preserving schema-v1/v2 marker recovery and pair commit.

Main-agent review found one in-scope TOCTOU gap after the initial recovery
preflight. The implementation now rechecks the target immediately before
writing it. A bounded regression mutates the manifest to foreign bytes after
preflight and proves recovery retains both the foreign manifest and marker.

Fresh verification:

- schema-v3 focused: 9/9 on Python 3.12.13 and system Python 3.9.6;
- complete transaction: 228/228 on both runtimes;
- Runtime Binding: 55/55 on both runtimes; and
- the successful bundle test proves all eight roles, exact write order,
  final bytes/modes, manifest-last activation, and marker retirement.

No live profile/App/provider state, dependency, release, archive, migration,
cleanup, or Git history effect occurred. Progress is 32/79.

### Next Action

Execute task 4.4 by adding the fault-injection matrix for marker publication,
each ordered artifact class, committed marker, and marker retirement. Prove
prepared rollback and committed roll-forward convergence without changing the
legacy schema-v1/v2 contract.

## 2026-07-26 Runtime Bundle Fault Matrix Verified

`internal-official-feature-parity` task 4.4 is complete.

The schema-v3 hard-interruption matrix now covers:

- the durable prepared marker;
- parity overlay;
- capability receipt;
- parity receipt;
- authoritative shared config;
- internal profile config;
- active derived runtime config;
- launcher;
- manifest;
- committed marker publication; and
- marker retirement.

For every prepared phase, the test proves the exact deterministic new-prefix
and old-suffix state at interruption, then lock-entry recovery restores every
target's old bytes and mode and retires the marker. For both committed phases,
all targets retain or recover their complete new bytes and modes and the marker
is absent after recovery.

The tests-first RED produced ten expected failure reports and zero errors on
both runtimes because only `after_marker` existed. GREEN results:

- complete schema-v3 focused set: 11/11 on Python 3.12.13 and system Python
  3.9.6; and
- complete transaction: 230/230 on both runtimes.

Dual-runtime AST/import, strict active OpenSpec, whitespace/diff, and generated-
bytecode checks pass. No live profile/App/provider state, dependency, release,
archive, migration, cleanup, or Git history effect occurred. Progress is
33/79.

### Next Action

Execute task 4.5 by adding explicit schema-v1 and schema-v2 marker fixtures for
prepared rollback and committed roll-forward. Prove their field layout and
recovery bytes remain legacy-compatible and are never parsed as schema v3.

## 2026-07-26 Legacy Runtime Rebind Fixtures Verified

`internal-official-feature-parity` task 4.5 is complete as a tests-only
characterization item.

The new fixture matrix covers:

- schema v1 prepared rollback;
- schema v1 committed roll-forward;
- schema v2 prepared rollback; and
- schema v2 committed roll-forward.

Each marker contains the exact established legacy fields and base64/digest
state payloads. Recovery starts from a mixed valid generation and converges
manifest, launcher, and schema-v2 receipt bytes/modes to the required old or new
generation. Schema v1 leaves an unrelated receipt at its original bytes and
mode. A patched schema-v3 validator that would fail immediately is never called
for either legacy schema.

Fresh verification:

- legacy fixture method: four subtests pass on Python 3.12.13 and system Python
  3.9.6; and
- complete transaction: 231/231 on both runtimes.

No production source, live profile/App/provider state, dependency, release,
archive, migration, cleanup, or Git history effect occurred. Progress is
34/79.

### Next Action

Execute task 4.6 by RED in `scripts/test_codex_runtime_binding.py` and
`scripts/test_codex_profile_switch.py`. Prove parity preparation runs before
launcher smoke, unhealthy or unknown evidence promotes nothing, the source
catalog remains unchanged, and successful staging supplies the complete
schema-v3 bundle.

## 2026-07-26 Internal Rebind Parity Integration RED Recorded

`internal-official-feature-parity` task 4.6 is complete as a tests-only RED
item.

The runtime-binding tests now require:

- `prepare_parity_bundle()` before launcher smoke;
- launcher smoke only after healthy staged parity evidence exists;
- no call to the legacy `commit_runtime_binding_pair()` path;
- one schema-v3 commit containing manifest, launcher, capability receipt,
  parity receipt, parity overlay, profile config, shared config, and active
  runtime config; and
- unchanged configured source-catalog bytes and `0640` mode.

The profile test covers failed preparation plus unknown, core, and unclassified
unhealthy evidence. Each subtest snapshots the complete promotion target set
and requires a `SwitchError`, zero schema-v3 commit calls, zero changed targets,
and unchanged source-catalog bytes/mode.

Fresh RED evidence is identical on Python 3.12.13 and system Python 3.9.6:

- runtime-binding: two methods fail by assertion with zero errors because
  parity preparation and schema-v3 commit are not integrated and the legacy
  pair is still called; and
- profile: one method reports four expected subtest failures with zero errors
  because every unhealthy case still reaches the legacy promotion path.

Four established internal rebind tests pass on both runtimes. Dual-runtime AST,
trailing-whitespace, and tracked diff checks pass. No production source, live
profile/App/provider state, dependency, release, archive, migration, cleanup,
or Git history effect occurred. Progress is 35/79.

### Next Action

Execute task 4.7 by integrating `prepare_parity_bundle()` into
`scripts/codex_switch_bindings.py`, rejecting unhealthy evidence before smoke,
and committing the complete artifacts only through
`commit_runtime_binding_bundle()` after child-backend attestation.

## 2026-07-26 Internal Runtime Parity Rebind Verified

`internal-official-feature-parity` task 4.7 is complete.

Internal `set-bin` now:

- resolves the verified official Runtime Binding and captures immutable internal
  profile/shared config inputs;
- prepares and requires a healthy, complete parity bundle before launcher smoke;
- keeps the configured source catalog byte- and mode-unchanged;
- generates the staged launcher and manifest from the same capability receipt,
  parity receipt, overlay, config projection, and adapter-rule metadata;
- verifies the smoke child backend, receipt generation, config-write proof, and
  Runtime Binding attestation before promotion; and
- commits parity overlay, capability receipt, parity receipt, shared config,
  profile config, active runtime config, launcher, and manifest through the
  schema-v3 bundle in manifest-last order.

The post-RED review also hardened stable no-follow `active.json` reads, exact
integer schema validation, bounded marker reads, marker identity checks before
each write, and identity-bound marker retirement. Legacy schema-v1/v2 recovery
fixtures remain green.

Fresh verification on Python 3.12.13 and system Python 3.9.6:

- parity: 83/83 on each runtime;
- Runtime Binding: 60/60 on each runtime;
- transaction: 238/238 on each runtime; and
- unhealthy parity promotion guard: 1/1 method with four subtests on each
  runtime.

The source-owned DevFlow dependency check reports
`ready_with_recommendations`, Full OpenSpec ready, and TDD ready. Its legacy
skill-layout recommendations remain untouched. No live profile/App/provider
state, dependency, release, archive, provider/root-state migration, legacy
skill cleanup, destructive cleanup, or Git history effect occurred. Progress is
36/79.

### Next Action

Execute task 4.8 as tests-only RED. Prove internal shell and Desktop launchers
consume the same projected managed-home config, parity overlay, typed v2
contract, and receipt generation, and reject old-launcher/new-manifest or
new-launcher/old-overlay mixtures.

## 2026-07-26 Launcher and Shell Generation Equivalence RED

`internal-official-feature-parity` task 4.8 is complete as a tests-only RED
item.

Two new Runtime Binding methods use the real generated launch artifacts:

- active internal shell and Desktop executions must report the same backend,
  managed-home config digest, overlay path/digest, `multi_agent_v2 = true`,
  capability receipt path, and expected receipt digest; and
- old-launcher/new-manifest plus new-launcher/old-overlay mixtures must fail
  before the backend writes its invocation marker.

Fresh expected failure evidence is the same on Python 3.12.13 and system Python
3.9.6:

- two methods run;
- three assertion failures occur;
- zero test errors occur;
- the shell contract reports the old backend and no promoted capability-receipt
  generation; and
- both mixed-generation launchers return zero and reach the backend.

Adjacent verification remains green:

- ten established internal rebind, attestation, recovery, and source-preserving
  methods pass on both runtimes; and
- the four-case unhealthy parity promotion guard passes on both runtimes.

No production source, live profile/App/provider state, dependency, release,
archive, migration, cleanup, or Git history effect occurred. Progress is
37/79.

### Next Action

Execute task 4.9. Prove every current runtime-rebind caller and test has moved
to the schema-v3 bundle interface, remove only the legacy pair commit adapter,
retain schema-v1/v2 recovery, and make the task 4.8 generation contracts GREEN.

## 2026-07-26 Runtime Rebind Adapter Retirement Verified

`internal-official-feature-parity` task 4.9 is complete.

All current runtime-rebind production callers and tests use
`commit_runtime_binding_bundle()`. `commit_runtime_binding_pair()` and its
imports/callers are absent from `scripts/`, while the independent schema-v1/v2
marker validation and recovery paths remain covered by their four-fixture
prepared/committed matrix.

Internal shell execution now resolves the current manifest dynamically and
exports the promoted capability-receipt generation. Parity-aware Desktop
launchers and shell execution share
`validate_internal_runtime_generation()` before backend execution. A manifest
with zero parity fields retains established legacy behavior; the presence of
any parity field requires the complete launcher, backend, capability receipt,
parity receipt, overlay, projected config, and `multi_agent_v2` generation.

Main review found and fixed one bounded same-contract gap. The validator
previously skipped receipt generation checks when `overlay` or
`internal_fingerprint` was absent. The new guard first produced two expected
assertion failures with zero errors because both malformed receipts reached the
backend. GREEN requires both mappings, validates the receipt and manifest
capability digests against the active capability artifact, and rejects either
missing binding before the backend marker.

Fresh verification:

- Runtime Binding: 63/63 on Python 3.12.13 and 63/63 on system Python 3.9.6;
- transaction: 234/234 on both runtimes;
- complete profile: 201/201 on Python 3.12.13;
- active strict OpenSpec: valid;
- all strict OpenSpec: 18 passed, 0 failed;
- dual-runtime AST, `git diff --check`, adapter authority, and bytecode residue:
  passed/clean.

The first unisolated Runtime Binding full run exposed an existing test-only
shell-profile isolation defect and temporarily replaced the managed
`~/.zshrc` block with a deleted temporary store path. The block was immediately
restored to `/Users/cY/.codex-switch/bin`; read-only status re-attested the
active internal PATH, GUI, LaunchAgent, proxy, and backend ownership. The
triggering test now binds its shell profile to its own temporary directory.
Focused runs on both runtimes and subsequent full runs preserve the repaired
`~/.zshrc` SHA-256, inode, size, mtime, and ctime.

No profile, App, provider, install, dependency, release, archive, migration,
destructive cleanup, or Git history effect remains. Progress is 38/79.

### Next Action

Execute task 4.10. Run parity, Runtime Binding, transaction, Protocol Adapter,
and supported profile routes serially on Python 3.12 and system Python 3.9,
record the intentional Python 3.11+ profile CLI boundary, and review the
integrated runtime-bundle diff before selecting task 5.

## 2026-07-26 Runtime Bundle/Rebind Slice Verified

`internal-official-feature-parity` task 4.10 and the Runtime bundle/rebind slice
are complete at 39/79.

The integrated review confirmed schema-v3 bundle ownership, manifest-last
activation, legacy schema-v1/v2 recovery, and one shared shell/Desktop runtime
generation validator. It also found and fixed one bounded same-contract false
health gap: a manifest containing only a parity metadata field outside the
previous five-key trigger set was treated as legacy. The RED used
`parity_adapter_rule_set_sha256`; both Desktop and shell returned zero and
wrote their backend markers on Python 3.12.13 and system Python 3.9.6. GREEN
reserves the complete `parity_` manifest namespace, requiring the existing
full generation validator whenever any parity evidence is present. A manifest
with zero parity fields retains its established legacy behavior.

Fresh final serial verification:

- parity: 83/83 on Python 3.12.13 and system Python 3.9.6;
- Protocol Adapter: 39/39 on both runtimes;
- Runtime Binding: 65/65 on both runtimes;
- transaction: 234/234 on both runtimes;
- complete profile: 201/201 on Python 3.12.13;
- supported system-Python profile projection routes: 2/2;
- direct system-Python profile CLI: exit 2 before store creation with the
  required Python 3.11+ message;
- active strict OpenSpec: valid; all strict OpenSpec: 18 passed, 0 failed;
- dual-runtime AST: 56/56 scripts;
- legacy pair removal and unique authority scans: passed;
- `git diff --check`: passed; and
- generated bytecode residue: none.

All test commands used
`CODEX_SWITCH_SHELL_PROFILE=/private/tmp/codex-switch-validation.ZLjc15/.zshrc`.
The real `~/.zshrc` remains byte- and metadata-identical:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mtime: 1785055828
ctime: 1785055828
```

No live profile, App, provider, install, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred.

Evidence:

- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-runtime-bundle-verified.md`

### Next Action

Execute task 5.1 as tests-only RED in `scripts/test_codex_update_release.py`.
Specify private sibling candidate installation, unchanged bound binary during
install and probe, intended-version checks, code-sign ordering,
parity-before-replacement, helper failure propagation, and zero-mutation
dry-run output. Do not run a real internal update or cross task 8.1.

## 2026-07-26 Staged Internal Update RED

`internal-official-feature-parity` task 5.1 is complete at 40/79.

Seven new `CodexStagedInternalUpdateTests` drive only the public
`codex_env_setup update-internal` and `codex-switch update-internal` command
boundaries with temporary fake installer and codesign executables. They define:

- a validated mode-0700 private sibling candidate directory;
- byte- and mode-stable bound binary state during installer and candidate
  probes;
- exact requested-versus-observed semantic version enforcement;
- code-sign before validation of the final candidate bytes;
- exact installer failure exit propagation;
- target, candidate class, parity checks, artifact set, and promotion order in
  a zero-mutation dry-run; and
- preservation of the bound binary when candidate parity/compatibility fails.

Fresh RED evidence:

- Python 3.12.13 focused: 7 methods, 12 expected assertion failures, 0 errors;
- system Python 3.9.6 focused: the same 7 RED methods, 0 errors;
- Python 3.12.13 complete update/release: 120 tests, with all 113 prior tests
  green and only the 12 expected new assertions failing;
- dual-runtime AST: passed;
- focused `git diff --check`: passed.

The failures map to the current in-place behavior: a non-sibling target is
accepted, candidate directories inherit public mode 0755, requested version
mismatch succeeds, candidate `--version` runs before codesign, installer exit
17 becomes exit 1, dry-run advertises moving the bound binary and omits the
parity/promotion plan, and a failed post-install probe leaves the bound binary
replaced.

The real `~/.zshrc` remains unchanged:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mtime: 1785055828
ctime: 1785055828
```

No production source, live profile, App, provider, install, dependency,
release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Git history effect occurred.

Evidence:

- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-internal-update-red.md`

### Next Action

Execute task 5.2. Refactor `scripts/codex_env_setup` so a trusted installer can
write only to an explicit validated private sibling candidate directory while
the bound binary remains unchanged. Preserve model, endpoint, and auth inputs;
make the installer-focused task 5.1 tests GREEN without implementing binary
swap, runtime-bundle promotion, or the full wrapper handshake.

## 2026-07-26 Staged Internal Update Promotion Verified

`internal-official-feature-parity` task 5.6 is complete at 45/79.

The public wrapper keeps `--install-dir` and `CODEX_INSTALL_DIR` as validation
of the internal profile's bound binary directory. It allocates a fresh private
sibling candidate, strips the public binding options before helper delegation,
and passes the helper the exact bound binary plus private candidate directory.
Dry-run reports the complete candidate artifact, locked revalidation, and
promotion plan without mutation.

Real execution delegates exact bound, candidate, backup, and target-version
inputs to `promote-internal-update`. The promotion path validates the candidate,
prepares the same capability/parity/config/overlay/runtime bundle used by
internal rebind, commits the typed executable swap with the schema-v3 text
bundle under the store lock, and runs the post-commit version, canonical
Runtime Binding, app-server child, capability-receipt, and parity-receipt
handshake before any success line is emitted.

Fresh verification with
`CODEX_SWITCH_SHELL_PROFILE=/private/tmp/codex-switch-task-5.6.IkqQzy/.zshrc`:

- staged update: 10/10 on Python 3.12.13 and 10/10 on system Python 3.9.6;
- complete update/release: 123/123 on Python 3.12.13;
- profile update routes: 30/30 on both runtimes;
- complete profile: 201/201 on Python 3.12.13;
- parity: 83/83 on both runtimes;
- Runtime Binding: 65/65 on both runtimes; and
- executable swap: 5/5 on both runtimes.

Post-control-plane checks pass: the active change is strict-valid, all strict
OpenSpec validation is 18/18, OpenSpec apply reports 45/79 with task 5.7 first,
Bash syntax passes, Python 3.12 and system Python 3.9 parse all 56 scripts, and
`git diff --check` passes.

The real `~/.zshrc` remains byte- and metadata-identical:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

No generated `scripts/__pycache__` directory exists. No live profile, App,
provider, internal install/update, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred.

Evidence:

- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-update-verified.md`

### Next Action

Execute task 5.7 as tests-only RED. Prove a failed post-promotion version,
canonical binding, app-server, capability receipt, overlay, config, or parity
handshake restores the old binary backup and complete old runtime bundle. Do
not retire the backup, print restart-required output, run a live update, or
cross Human Gate 8.1.

## 2026-07-26 Post-Promotion Handshake Rollback Verified

`internal-official-feature-parity` task 5.8 is complete at 47/79.

`commit_runtime_binding_bundle()` now accepts a prepared-generation validator
and optional executable-backup retirement. It promotes the candidate binary
and complete runtime bundle while the durable marker remains `prepared`, runs
the full promotion handshake, revalidates the promoted generation, and only
then publishes `committed`. Any handshake failure uses prepared recovery, so
the old binary and all eight old runtime targets return together and the
candidate is available for diagnosis or retry. Durable commit converges the
new generation, retires the exact digest-checked old backup, and returns to
the wrapper only after the marker is gone.

`cmd_promote_internal_update()` supplies the full handshake as that prepared
validator, requests backup retirement only for the staged executable swap,
suppresses ordinary rebind output, and prints verified version, app-server,
receipt, and restart-required lines only after durable success.

Fresh verification:

- Runtime Binding: 74/74 in 109.873s on Python 3.12.13;
- Runtime Binding: 74/74 in 244.134s on system Python 3.9.6;
- transaction: 239/239 in 24.153s on Python 3.12.13;
- transaction: 239/239 in 140.002s on system Python 3.9.6;
- active strict OpenSpec: valid;
- all strict OpenSpec: 18/18;
- dual-runtime AST: 56/56 scripts;
- tracked and touched-untracked whitespace checks: passed; and
- generated bytecode residue: none.

Main review found no blocking spec, rollback-authority, foreign-state,
backup-retirement, output-order, or scope issue.

The first fresh Python 3.12 transaction run omitted shell-profile isolation.
It passed 239/239 but atomically rewrote the real `~/.zshrc` with identical
bytes. SHA-256, size, mode, and mtime remained unchanged; inode changed from
`48362010` to `48897140` and ctime from `1785062545` to `1785074064`. The
system-Python repeat was stopped. The bounded repair makes
`TransactionTests.setUp` assign a private temporary
`CODEX_SWITCH_SHELL_PROFILE` for every test. Both final full suites then ran
without an external override and preserved this stable state:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No shell content, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Action

Execute task 5.9 as a focused ownership regression. Prove
`set-bin internal <external-path>` prepares and commits the same parity bundle
while the external backend keeps its exact inode, bytes, mode, timestamps, and
parent entry set; the schema-v3 marker must not contain an executable swap or
target the external path. Do not run a live rebind or cross Human Gate 8.1.

## 2026-07-26 External Backend Ownership Verified

`internal-official-feature-parity` task 5.9 is complete at 48/79.

The new Runtime Binding characterization test executes the real
`cmd_set_bin()` internal path against a backend outside the profile store. It
captures the durable schema-v3 marker at `after_marker` and proves:

- all eight parity/runtime artifact roles are present;
- no executable-swap entry exists;
- the external backend is not an artifact target;
- the external file's device, inode, full mode, link count, size, mtime,
  ctime, and bytes remain exact;
- the external parent directory entry set remains exact;
- no store file persistently copies the backend bytes;
- the canonical manifest and returned Runtime Binding reference the external
  path; and
- the marker is retired after success.

The existing task-4.7 implementation already satisfied this contract, so task
5.9 required no production change. The first test run reached the final
managed-copy scan and failed only because the new test omitted `import stat`.
After that test-only correction:

```text
Focused ownership proof:
Python 3.12.13: 1/1 in 2.669s
system Python 3.9.6: 1/1 in 5.989s

Adjacent ownership/bundle/rollback selector:
Python 3.12.13: 3/3 in 7.752s
system Python 3.9.6: 3/3 in 17.639s
```

The real `~/.zshrc` remains at the stable post-5.8 tuple:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Action

Execute task 5.10. Run the complete update/release, transaction, Runtime
Binding, parity, and supported profile suites serially on Python 3.12.13 and
system Python 3.9.6 with the private validation shell profile. Review the
integrated staged-update diff and record exact counts before selecting task
6.1. Do not run a live update/rebind or cross Human Gate 8.1.

## 2026-07-26 Staged Update Slice Verified

`internal-official-feature-parity` task 5.10 is complete at 49/79.

Fresh serial slice-closure verification:

```text
Python 3.12.13
update/release: 123/123 in 221.574s
transaction: 239/239 in 24.524s
Runtime Binding: 75/75 in 111.688s
parity: 83/83 in 2.096s
profile: 201/201 in 280.376s

system Python 3.9.6
update/release: 123/123 in 252.430s
transaction: 239/239 in 139.227s
Runtime Binding: 75/75 in 253.637s
parity: 83/83 in 34.185s
supported profile projection: 2/2 in 4.924s
direct profile CLI: exit 2 before store creation
```

The direct system-Python complete profile attempt ran 201 tests and reported
one failure plus 83 errors, all rooted in the established explicit requirement
for Python 3.11+ `tomllib`. No acceptance criterion failed, so no parser
framework, shared abstraction, extra fault axis, or unrelated edge test was
added.

Post-control-plane checks pass: active strict OpenSpec is valid, all strict
OpenSpec is 18/18, apply reports 49/79 with task 6.1 first, the workflow
validator reports `ok=true` with zero issues, Bash syntax is 5/5,
Python 3.12/system Python 3.9 AST is 56/56, changed-file whitespace checks pass,
and generated bytecode residue is zero.

The plan now records a layered validation budget: task-local work runs focused
regressions; slice closure runs the slice's complete required dual-runtime
matrix; integrated/final gates 7.x/9.x run full-project verification. Adjacent
tasks do not repeat an unchanged complete suite unless its result was not
collected or a real failure requires it. Complexity expansion requires a named
failing acceptance criterion; otherwise it is `DEFER_AND_CONTINUE`.

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No live profile, App, provider, internal install/update, dependency, commit,
push, release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Human Gate 8.1 effect occurred.

### Next Action

Execute task 6.1 as verifier tests-only RED. Add focused cases for parity
receipt/evidence health, stable finding codes, sanitized reporting, optional
queue semantics, and `--repair=none` zero writes. Do not implement task 6.2,
expand the public CLI, run a live repair, or cross Human Gate 8.1.

## 2026-07-26 Parity Verifier RED

`internal-official-feature-parity` task 6.1 is complete at 50/79.

Five focused tests now define:

- stable codes for missing, malformed, stale reference/runtime/provider/config/
  overlay/adapter evidence;
- unhealthy core protocol, unclassified feature, and failed typed-role probe
  findings;
- a healthy deterministic optional synchronization queue;
- one preloaded parity report reused by collection and structured reporting,
  with sanitized messages and preserved codes; and
- `verify --repair=none` loading parity once with zero store writes.

Fresh expected RED:

```text
Python 3.12.13: 5 tests in 0.021s, 5 failures, 0 errors
system Python 3.9.6: 5 tests in 0.017s, 5 failures, 0 errors
```

Three failures state that `collect_verification_problems()` does not yet accept
a `parity_report`; one states that `write_verification_report()` does not yet
accept the same report; one states that `cmd_verify()` does not yet fail on the
missing parity receipt. These are the exact task-6.2 behavior gaps.

Both runtimes compile the changed test. Active strict OpenSpec is valid,
tracked and touched-untracked whitespace checks pass, bytecode residue is
zero, and the real `~/.zshrc` remains at SHA-256
`8a144f4d...224b4`, inode `48897140`, size `1959`, mode `600`, mtime
`1785055828`, ctime `1785074064`.

The DevFlow dependency check confirms the project-local `tdd` resource is
ready. Its overall false result is the existing unrelated skill source-conflict
and legacy-layout state; no activation, migration, or cleanup was authorized or
performed.

No production source, live profile, App, provider, internal install/update,
dependency, commit, push, release, archive, provider/root-state migration,
legacy skill cleanup, destructive cleanup, or Human Gate 8.1 effect occurred.

### Next Action

Execute task 6.3 as tests-only RED. Add only the focused status/Doctor/profile
contracts for shared parity codes, deterministic optional queue ordering, and
the core-versus-optional distinction. Do not implement task 6.4, add a public
CLI, run live repair, or cross Human Gate 8.1.

## 2026-07-26 Parity Verifier Integration

`internal-official-feature-parity` task 6.2 is complete at 51/79.

The implementation:

- loads only existing profile-local receipt evidence and never prepares or
  regenerates parity artifacts;
- validates receipt/manifest ownership, current adapter rules, the canonical
  runtime generation, official/internal binaries, source catalog, and config
  digests;
- normalizes missing/malformed/stale reference, runtime/provider, config,
  overlay, and adapter failures into stable parity findings;
- reuses one report through collection, structured reporting, and command
  output; and
- preserves optional-only health and deterministic queue ordering while error
  findings fail verification.

Fresh task-local evidence:

```text
Python 3.12.13: ParityVerificationTests 6/6 in 0.026s
system Python 3.9.6: ParityVerificationTests 6/6 in 0.036s
Python 3.12.13: adjacent collect/report regressions 4/4 in 0.878s
system Python 3.9.6: adjacent collect/report regressions 4/4 in 0.561s
dual-runtime AST: 2/2 touched files
```

The added loader test first failed on both runtimes only because
`collect_parity_report` did not exist, then passed after the read-only
implementation. Per the layered validation budget, no unchanged complete
verifier, diagnostics slice, or project-wide matrix was repeated.

No live profile, App, provider, internal install/update, parity/config artifact,
dependency, commit, push, release, archive, cleanup, or Human Gate 8.1 effect
occurred.

### Next Action

Execute task 6.3 tests-only RED for shared status/Doctor/profile parity
diagnostics. Stop before task 6.4 production integration.

## 2026-07-26 Parity Diagnostics RED

`internal-official-feature-parity` task 6.3 is complete at 52/79.

Two profile-level tests now define one shared diagnostic contract:

- status, Doctor, and verify collect the same parity report exactly once;
- unhealthy core drift prints `Parity health: unhealthy` and the same stable
  finding code;
- optional-only drift remains healthy and prints both finding codes; and
- the synchronization queue prints feature `skill_search` before protocol
  `client_request:app/read`.

The first dual-runtime run exposed a verify fixture error because the temporary
store had no internal manifest. The test seam now stubs an empty read-only
manifest so verify reaches the injected parity result. Fresh expected RED:

```text
Python 3.12.13: 2 tests in 0.027s, 6 failures, 0 errors
system Python 3.9.6: 2 tests in 0.026s, 6 failures, 0 errors
```

Status and Doctor fail because they never call parity collection. Verify
collects once but fails because it does not print the common health, finding,
or optional-queue lines. No production source or live state changed.

### Next Action

Execute task 7.2 serially with a private validation shell profile. Run complete
Protocol Adapter, Runtime Binding, transaction, verifier, update/release, and
profile suites on Python 3.12, then the project-required dual-runtime suites
and supported profile routes on system Python 3.9. Record the established
Python 3.11+ profile boundary without weakening it. Do not mutate live state or
cross Human Gate 8.1.

## 2026-07-26 Parity Diagnostics Integration

`internal-official-feature-parity` task 6.4 is complete at 53/79.

The verifier now owns one deterministic parity presentation:

- health comes from the existing `parity_report_data()` evaluation;
- finding output contains stable codes only;
- queue output is sorted by category, identifier, and finding code; and
- problem messages pass through the existing external-text sanitizer.

Verify prints the preloaded report once. Status collects only for active
internal. Doctor reuses its active Runtime Binding, reports parity only for
active internal, and fails only on error findings. Missing or unhealthy receipt
paths remain read-only and do not trigger repair.

Fresh task-local results:

```text
Python 3.12.13: shared diagnostics 2/2 in 0.017s
system Python 3.9.6: shared diagnostics 2/2 in 0.016s
Python 3.12.13: ParityVerificationTests 6/6 in 0.026s
system Python 3.9.6: ParityVerificationTests 6/6 in 0.039s
Python 3.12.13: adjacent status/Doctor regressions 3/3 in 4.762s
dual-runtime AST: 4/4 touched files
```

A legacy one-key internal fixture without a parity receipt now stops at the
intended `parity.receipt.missing` gate. The explicit staged repair behavior is
already tasks 6.5/6.6, so this is `DEFER_AND_CONTINUE` rather than an expansion
of task 6.4.

### Next Action

Execute task 6.5 as tests-only RED. Prove explicit parity repair delegates to
the staged internal rebind path while ordinary status, Doctor, and
`verify --repair=none` remain byte-exact and never patch receipt, overlay,
config, launcher, or manifest in place. Do not implement task 6.6 in the same
item or cross Human Gate 8.1.

## 2026-07-26 Parity Repair Routing RED

`internal-official-feature-parity` task 6.5 is complete at 54/79.

Two verifier tests now require:

- an explicit `repair_internal_parity(args, binding)` seam;
- delegation to `cmd_set_bin` for `internal` with the current canonical
  backend and managed Desktop binding;
- a second parity collection after staged rebind; and
- success only when that fresh report is healthy.

Fresh expected RED:

```text
Python 3.12.13: 2 tests in 0.015s, 2 failures, 0 errors
system Python 3.9.6: 2 tests in 0.014s, 2 failures, 0 errors
```

The first failure is the absent repair seam. The second proves
`verify --repair=safe` still prints the original missing-receipt result and
exits 1 without repair or recollection.

The read-only characterization already passes:

```text
Python 3.12.13: 1/1 in 0.018s
system Python 3.9.6: 1/1 in 0.020s
```

It verifies exact inode, mode, size, timestamps, and bytes for manifest,
receipt, overlay, profile config, and launcher after normal status, Doctor, and
`verify --repair=none`.

### Next Action

Execute task 6.6 with the smallest existing-command route. Implement
`repair_internal_parity(args, binding)` as current-backend
`cmd_set_bin internal`, call it only for explicit safe repair of unhealthy
internal parity, then recollect and report the fresh result. Do not add a new
public CLI, patch artifacts in place, or cross Human Gate 8.1.

## 2026-07-26 Parity Repair Routing Integration

`internal-official-feature-parity` task 6.6 is complete at 55/79.

The verifier now exposes one narrow repair seam that locally imports the
existing binding command and calls it with:

- `name="internal"`;
- `codex_bin=<current canonical backend>`; and
- `preserve_app_cli=False`.

`cmd_verify` invokes the seam only for explicit safe repair of an unhealthy
internal parity report. After staged rebind it reloads manifest/active state,
resolves Runtime Binding again, recollects parity, and prints/evaluates only
that fresh result.

Fresh task-local evidence:

```text
Python 3.12.13: focused repair 2/2 in 0.108s
system Python 3.9.6: focused repair 2/2 in 0.068s
Python 3.12.13: ParityVerificationTests 8/8 in 0.146s
system Python 3.9.6: ParityVerificationTests 8/8 in 0.098s
Python 3.12.13: read-only artifact characterization 1/1 in 0.015s
system Python 3.9.6: read-only artifact characterization 1/1 in 0.015s
dual-runtime syntax and targeted diff hygiene: passed
```

No public CLI, in-place receipt/overlay/config/launcher/manifest patch, live
rebind, profile/App/provider/internal update, dependency, commit, push,
release, archive, retained-evidence cleanup, or Human Gate 8.1 effect occurred.

### Next Action

Execute task 6.7 by TDD for package/release inclusion of the parity module and
its transitive imports. Keep package contents immutable and exclude retained
probe/config evidence; do not start docs task 6.8 or cross Human Gate 8.1.

## 2026-07-26 Parity Package Integration

`internal-official-feature-parity` task 6.7 is complete at 56/79.

Release construction now:

- requires the parity module and the three generated-launcher target modules;
- verifies `$SCRIPT_DIR` and `$SWITCH_SCRIPTS` Python references stay inside
  the package;
- imports every packaged non-test Python module in an isolated copy;
- rejects import failure or any import-time payload mutation before public
  finalization;
- selects Python 3.11+ with `tomllib`; and
- keeps historical immutable canonicalization compatible through inert
  placeholders for newly required modules.

Fresh task-local evidence:

```text
RED Python 3.12.13: 5 methods, 8 failures, 0 errors in 2.010s
RED system Python 3.9.6: 5 methods, 8 failures, 0 errors in 2.032s
GREEN Python 3.12.13: focused package 5/5 in 2.618s
GREEN system Python 3.9.6: focused package 5/5 in 2.683s
adjacent release/promotion: 4/4 in 10.687s and 12.311s
profile package adapter: 1/1 in 1.364s and 1.472s
Bash syntax, dual-runtime AST, and targeted diff hygiene: passed
```

Isolated real package evidence:

```text
manifest files: 66
manifest directories: 5
required paths: 20
archive members: 73
archive size: 522880 bytes
payload SHA-256: bbd79beaf00d33a48009630284ac84bb8547e215f2122e2fb1781d59c8428ae5
parity module: present
retained probe/config evidence: absent
bytecode cache: absent
```

No live profile, App, provider, internal install/update, dependency, commit,
push, release publication, OpenSpec archive, retained-evidence cleanup, or
Human Gate 8.1 effect occurred.

### Next Action

Execute task 6.8 as docs-only work. Update `README.md` and `SKILL.md` with the
approved reference/health/remediation/update/live-gate contract, then run only
focused docs/static checks. Do not start authority scan task 6.9 or cross Human
Gate 8.1.

## 2026-07-27 Parity Authority Closure

`internal-official-feature-parity` task 6.9 is complete at 58/79.

The task-local scan found one production ownership violation:
`codex_switch_verify.py` mapped parity evidence codes to categories and
constructed unresolved `ParityFinding` reports. The minimal fix moved that
policy into `codex_switch_parity.py` as `parity_error_report()`. Verifier now
passes only observed evidence inputs and no longer imports parity policy
version, fingerprint, finding, or official-bundle identity types for local
construction.

Fresh task-local evidence:

```text
RED Python 3.12.13: focused ownership 1 test, 1 failure, 0 errors
RED system Python 3.9.6: focused ownership 1 test, 1 failure, 0 errors
GREEN Python 3.12.13: focused ownership 1/1 in 0.003s
GREEN system Python 3.9.6: focused ownership 1/1 in 0.002s
Python 3.12.13: ParityVerificationTests 8/8 in 0.158s
system Python 3.9.6: ParityVerificationTests 8/8 in 0.128s
Runtime Binding policy scan: zero hits
Protocol Adapter provider/overlay policy scan: zero hits
Capability Receipt official-reference policy scan: zero hits
production parity caller construction scan: zero hits outside parity
```

No complete diagnostics, package, profile, parity, or update/release suite was
repeated because task 6.10 owns that slice-closure matrix.

Post-control-plane checks pass: active strict OpenSpec is valid, all strict
OpenSpec is 18/18, apply reports 58/79 with task 6.10 first, the DevFlow
workflow validator reports `ok=true` with zero issues and one legacy-state
migration warning, Python 3.12/system Python 3.9 AST is 3/3 touched files,
changed-file whitespace/diff checks pass, caller authority remains clean, and
generated bytecode residue is zero.

### Next Action

Execute task 6.10 only. Close the diagnostics/package slice with its recorded
dual-runtime focused matrix before selecting integrated task 7.1. Preserve
Human Gate 8.1 and all no-live-mutation, no dependency, no Git effect, no
release/archive, and no cleanup boundaries.

## 2026-07-27 Parity Diagnostics Slice Verified

`internal-official-feature-parity` task 6.10 is complete at 59/79.

Fresh private-root slice verification:

```text
Python 3.12.13
ParityReferenceTests: 9/9 in 0.073s
ParityVerificationTests: 8/8 in 0.155s
profile diagnostics/package seams: 4/4 in 1.529s
CodexUpdateReleaseTests: 37/37 in 22.639s
CodexStagedInternalUpdateTests: 10/10 in 9.721s
package/promotion/workflow adjacency: 3/3 in 9.260s
total: 71/71

system Python 3.9.6
ParityReferenceTests: 9/9 in 0.078s
ParityVerificationTests: 8/8 in 0.123s
profile diagnostics/package seams: 4/4 in 1.400s
CodexUpdateReleaseTests: 37/37 in 24.581s
CodexStagedInternalUpdateTests: 10/10 in 7.626s
package/promotion/workflow adjacency: 3/3 in 10.123s
total: 71/71
```

Validation roots were
`/private/tmp/codex-switch-parity-610-py312.oPgVL2` and
`/private/tmp/codex-switch-parity-610-py39.Bdl7GL`. The real `~/.zshrc`
retained its established hash and full stat tuple. No production code changed,
no acceptance failure occurred, and no bytecode residue remains.

### Next Action

Execute task 7.1. Run the complete parity suite on both required runtimes as
the first integrated verification gate. Do not start task 7.2 until both
results are collected, and do not cross Human Gate 8.1.

## 2026-07-27 Integrated Parity Verification

`internal-official-feature-parity` task 7.1 is complete at 60/79.

Fresh complete-suite evidence:

```text
Python 3.12.13: 84/84 in 2.151s
system Python 3.9.6: 84/84 in 32.688s
failures/errors: zero
generated bytecode residue: zero
```

The complete suite includes reference authority, deterministic feature and
protocol inventories, classification, provider-bound receipts, managed
overlay, config projection, isolated probes, runtime bundle metadata, and the
new evidence-error ownership regression.

### Next Action

Execute task 7.2 serially. Run the cross-module integrated suites on Python
3.12, then the required system-Python 3.9 routes, preserving the existing
Python 3.11+ direct profile boundary and all Human Gate 8.1 restrictions.

## 2026-07-27 Integrated Cross-Module Verification

`internal-official-feature-parity` task 7.2 is complete at 61/79.

Fresh accepted results:

```text
Python 3.12.13
Protocol Adapter: 39/39 in 23.720s
Runtime Binding: 75/75 in 112.316s
transaction: 239/239 in 23.888s
verifier: 30/30 in 10.958s
update/release: 126/126 in 253.292s
complete profile: 204/204 in 273.063s

system Python 3.9.6
Protocol Adapter: 39/39 in 22.916s
Runtime Binding: 75/75 in 249.496s
transaction: 239/239 in 137.982s
verifier: 30/30 in 10.847s
update/release: 126/126 in 300.648s
supported profile projection: 2/2 in 5.063s
direct profile CLI: exit 2 before store creation
```

The final fixture changes are limited to explicit parity-verification
isolation for unrelated profile tests and selecting an installed Python 3.12/
3.11 runtime when Python 3.9 generates managed wrappers. Production parity and
Python-version gates remain unchanged. Trusted installer/runner hashes and
invalid-candidate release fixtures now match the verified current sources.

### Next Action

Execute task 7.3 only: run active and all strict OpenSpec validation. Do not
start workflow validation task 7.4 until both results are collected, and do
not cross Human Gate 8.1.

## 2026-07-27 Strict OpenSpec Verification

`internal-official-feature-parity` task 7.3 is complete at 62/79.

```text
active strict validation: valid
all strict validation: 18 passed, 0 failed
```

### Next Action

Execute task 7.4 only with the pinned DevFlow workflow validator. Record every
gate, issue, and warning without editing generated guidance.

## 2026-07-27 Workflow State Verification

`internal-official-feature-parity` task 7.4 is complete at 63/79.

```text
ok: true
issues: []
warnings:
- Legacy DevFlow root state is read-only; migrate to
  .planning/devflow/STATE.md before the 1.0.0 sunset
```

The warning remains a recorded migration input. No generated guidance,
provider state, dependency, or legacy layout was changed.

### Next Action

Execute task 7.5 Bash syntax, dual-runtime AST, and production-import scans.

## 2026-07-27 Static and Import Verification

`internal-official-feature-parity` task 7.5 is complete at 64/79.

```text
Bash syntax: 5/5
Python 3.12.13 AST: 56/56
Python 3.12.13 production imports: 47/47
system Python 3.9.6 AST: 56/56
system Python 3.9.6 production imports: 47/47
generated bytecode residue: zero
```

### Next Action

Execute task 7.6 isolated package build and validation only.

## 2026-07-27 Isolated Package Verification

`internal-official-feature-parity` task 7.6 is complete at 65/79.

```text
manifest files: 66
manifest directories: 5
required paths: 20
production imports: 47
archive members: 73
archive size: 525008 bytes
archive SHA-256: b9d21c9f4e5e880ca5858d7111f1728084a72cf656b54db384a5be922afe598a
payload SHA-256: 5cb103bb9f454b2767a9ae3f2e7dbd7cd9ed6a291b53cbeddc99b4a14746758d
retained probe/config/auth/bytecode evidence: absent
```

### Next Action

Execute task 7.7 diff, write-set, ownership, and 66-scenario coverage audit.

## 2026-07-28 Internal Installer Side-Effect Repair Approved

The current active change is `internal-official-feature-parity`. Historical
tasks 1.1-8.2 and the task-8.3 source/package repair account for 70 completed
items. Five new Scheme A incident tasks make current progress 70/84.

Live diagnosis established:

- official and internal direct plugin inventories contain the same 24 plugin
  IDs and enabled states;
- common synchronized safe config values match, and the internal managed config
  differs only at intended internal provider/model fields;
- the internal manifest and generated wrapper bind
  `/Users/cY/.local/bin/codex`, and direct internal runtime/app-server smoke
  passes;
- the trusted installer inherited live `HOME`, `CODEX_HOME`, and `PATH`,
  narrowed live `config.toml`, and appended three failed sibling candidates to
  `.zshrc` before preparation could promote a new runtime; and
- bare shell `codex` therefore resolved a retained candidate instead of the
  codex-switch shim, explaining the apparent wrong-bin runtime failures.

The user explicitly selected Scheme A. The approved repair isolates the
installer inside a private exact-cleaned root, preserves all live state during
staging, adds harmful-installer TDD coverage, backs up and removes only the
three confirmed shell blocks, moves only the three confirmed candidates to a
recoverable codex-switch backup, installs exact verified source, and performs
one controlled internal update/rebind/switch plus bounded ChatGPT restart and
runtime/config/plugin verification.

The write boundary excludes proxy changes, plugin refresh, global-state
allowlist expansion, credential/identity migration, legacy skill
migration/cleanup, dependency changes, destructive deletion, provider-backed
Desktop tasks, Git, release, and archive effects. The required DevFlow layout
preflight was dry-run only and reported the existing source conflicts with no
writes.

### Next Action

Task 8.3A.1 is complete at 71/84. The Python 3.12 public-seam regression
returned 0 and produced the candidate, but failed because the harmful installer
replaced live `config.toml` bytes (`live-config-sentinel = true` became
`installer-default-config`). This is the intended RED and no production code
changed.

Task 8.3A.2 is complete at 72/84. The helper now creates one identity-bound
mode-0700 `/tmp/codex-switch-internal-installer.*` root, gives the installer
private `HOME`/`CODEX_HOME`, places the validated candidate first in child
PATH, and exact-cleans only the captured root inode. No wrapper change was
needed. Three incident tests pass on Python 3.12 and system Python 3.9,
including installer exit 17 plus `HUP`/`INT`/`TERM`; the complete staged-update
class passes 13/13 on both runtimes and Bash syntax passes.

Task 8.3A.3 is complete at 73/84. The final implementation also explicitly
forwards parent-only signals to the installer pipeline and waits/reaps it.
Final serial update/release suites pass 132/132 on Python 3.12 and 132/132 on
system Python 3.9. Active/all strict OpenSpec, AI-plan lint, pinned workflow
validation, Bash syntax, dual-runtime AST, isolated release-package validation,
source/package identity, `git diff --check`, exact write-set, and scratch/
credential/config/shell/bytecode residue checks pass. The isolated package is
`/private/tmp/codex-switch-installer-isolation.rZHFJ2`; packaged and source
`scripts/codex_env_setup` share SHA-256
`0e7334481204785517ac68ac4a9086b77cc9b1136718fbc15234459b25c61bd9`.
The pre-live `.zshrc` remains at the diagnosed SHA-256
`7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807`.

Execute task 8.3A.4: re-attest every exact live target, create the private
recovery backup, remove only the three confirmed installer PATH blocks, and
move only the three confirmed mode-0700 candidate directories. Stop on drift;
delete nothing.

Task 8.3A.4 is complete at 74/84. Pre-mutation attestation matched the
diagnosed `.zshrc` SHA-256, exact one-per-target block counts, regular-file
mode/owner, and all three non-symlink candidate directory modes, owners,
inodes, three-file contents, and `codex-cli 0.145.0` versions. Private recovery
directory
`/Users/cY/.codex-switch/backups/20260728T161949+0800-installer-side-effect-recovery`
is mode 0700. It contains the byte-identical mode-0600 `.zshrc` backup and the
three original mode-0700 candidate directories with unchanged inodes. The live
`.zshrc` diff removes only the three named blocks, remains mode 0600, and now
has SHA-256
`8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4`.
A clean-environment interactive zsh resolves bare `codex` to
`/Users/cY/.codex-switch/bin/codex`; the current official profile reports
`codex-cli 0.146.0-alpha.3.1`. No target was deleted.

Execute task 8.3A.5: install the exact verified source, verify immutable
installed identity, run one supported internal update/rebind/switch, then one
bounded ChatGPT quit/reopen and complete config/plugin/runtime ownership
verification. Stop before provider-backed Desktop work or any excluded effect.

Task 8.3A.5 is blocked after a safe compatibility RED. The exact source
installation promoted immutable payload
`275ad2e2fda95c0d2591fe95aa4d9e7075988da286851f6584e51c3bad771dab`;
its 66-file manifest validates and installed/source `codex_env_setup` hashes
match. The one authorized update staged internal 0.145.0 at
`/Users/cY/.local/bin/.codex-internal-update-6efc91d3f6359549077f8a00`
and stopped before promotion with `parity.feature.core_drift`. Live `.zshrc`,
official config, internal config, bound 0.144.6, manifest, launcher, and active
official profile remain unchanged; installer scratch is absent.

A forced-stop read-only diagnostic proves the sole error is `item_ids`.
Official metadata is `removed/default-on/effective-on`; internal 0.145.0 is
`under-development/default-off/effective-off`. The only observed dependency is
`thread/resume.params.history`, and current
`client_request:thread/resume` is natively compatible with both schemas and no
reason codes. Native compatibility correctly yields no adapter coverage
record, but policy incorrectly requires that record. Existing warnings are
only optional `mcp_2026_07_28` missing and provider-pending `tool_mode`.

The exact correction is planned in the active OpenSpec: accept the exact resume
dependency only when current native compatibility or the existing exact
adapter coverage proves it; missing/incompatible/uncovered/stale evidence or
another dependency remains unhealthy. TDD and production writes would be
limited to `scripts/test_codex_parity.py` and
`scripts/codex_switch_parity.py`. Those paths are outside the narrower Scheme A
incident write set, so implementation, promotion retry, switch, and restart
stop at `PARITY-0.145-NATIVE-RESUME-IMPLEMENT` pending explicit user approval.

## 2026-07-28 Internal 0.145 Native-Resume Implementation Approved

The user explicitly consumed `PARITY-0.145-NATIVE-RESUME-IMPLEMENT`. Execution
resumes from the recorded safe live state. Source changes are limited to
`scripts/test_codex_parity.py` and `scripts/codex_switch_parity.py`, with
main-owned OpenSpec/ledger/state/verification evidence. The first required
action is the named RED proving exact current native
`client_request:thread/resume` compatibility can satisfy the sole
`thread/resume.params.history` dependency without an adapter record.

After reviewed dual-runtime GREEN and source/package verification, freshly
re-attest the existing internal 0.145.0 candidate and every live fingerprint.
Retry promotion only with that retained candidate; do not download another.
The existing Scheme A authorization still excludes provider-backed Desktop
tasks, proxy/plugin/global-state changes, credential/identity migration,
dependencies, destructive cleanup, Git, release, and archive.

### Next Action

Add and run
`ParityMethodCoverageTests.test_item_ids_accepts_exact_native_resume_compatibility_without_adapter_coverage`
on Python 3.12. Record the expected policy false-negative before changing
production.

### RED Evidence

The named Python 3.12 test ran alone and failed at the expected
`self.assertTrue(...healthy)` assertion:

```text
Ran 1 test in 0.002s
FAILED (failures=1)
```

Both exact resume schemas were present, direction-aware compatibility was true,
reason codes and adapter coverage were empty, and the only observed dependency
was `thread/resume.params.history`. No production file had changed.

### Next Action

Make the smallest policy change so that exact current native compatibility or
the existing exact adapter coverage satisfies that sole dependency, then rerun
the named test.

### Focused and Full Parity GREEN

The production change performs an exact lookup of
`client_request:thread/resume` and treats it as native proof only when both
method schemas are present and `compatible=true`. The existing exact adapter
path is unchanged. Results:

```text
named regression: 1/1 on Python 3.12 and system Python 3.9
method-coverage class: 6/6 on both runtimes
complete parity: 94/94 on both runtimes
```

The named regression also proves missing official/internal schema,
incompatible resume without accepted coverage, an extra observed dependency,
and no exact resume comparison all remain unhealthy.

### Next Action

Run the complete update/release adjacency serially on Python 3.12, then system
Python 3.9. Do not run the two full suites concurrently.

### Read-Only Review Guard RED

The Standards axis found one fail-closed gap: a caller-constructed comparison
can contain `compatible=true` and non-empty incompatibility reasons. The
original native branch accepted that contradictory evidence. The Spec axis
also required independently proving both-side presence and exact
direction/method selection.

The tightened Python 3.12 negative test now has one expected failure only for
the contradictory reason tuple:

```text
Ran 1 test in 0.005s
FAILED (failures=1)
```

Missing official/internal sides retain `compatible=true` and require the
feature-level `item_ids` core finding. Compatible wrong-direction and
wrong-method entries, incompatible resume, extra dependencies, and an absent
exact comparison also remain negative.

### Next Action

Require empty reason codes for native resume proof, then rerun the focused and
complete dual-runtime parity suites before repeating any source/package claim.

## 2026-07-28 Internal 0.145 Native-Resume Source Verified

The review guard is closed. Exact native proof now requires both current
schemas, the exact direction/method, `compatible=true`, and empty reason codes.
The exact adapter alternative is unchanged. Both read-only review axes report
no remaining actionable findings.

Fresh final results are method coverage 7/7 and complete parity 95/95 on both
runtimes, plus update/release 132/132 on Python 3.12 and system Python 3.9.
Dual-runtime AST/import, active/all strict OpenSpec 18/18, AI-native plan lint,
pinned workflow (`ok=true`, zero issues), diff checks, and isolated package/
source identity pass. No new bytecode was generated after the implementation
gate was consumed. Durable evidence is
`.planning/checkpoints/2026-07-28-internal-0145-native-resume-source-verified.md`.

### Next Action

Install the exact verified source through the supported install command,
validate the new immutable payload, then freshly re-attest the retained
internal 0.145.0 candidate and all live inputs. Retry only that candidate. Do
not run `update-internal` or download another candidate.

## 2026-07-28 Retained-Candidate Promotion Ready

The supported exact-source install promoted immutable payload
`6a23d04f8408681c26ed116583b208699f4b8fba4357162717befe7af8c1f132`
and strict validation passed. Fresh candidate, bound backend, official bundle,
shell, config, manifest, launcher, active-record, backup, and transaction
marker checks pass. The retained candidate remains signed internal 0.145.0,
mode-0700 rooted, SHA-256 `a34c872c...197b8`; bound remains 0.144.6 SHA-256
`410ebcd3...e8b6`; backup and marker are absent.

Durable preflight is
`.planning/checkpoints/2026-07-28-internal-0145-retained-candidate-preflight.md`.

### Next Action

Call the installed immutable `codex_profile_switch.py
promote-internal-update` seam directly with the exact retained
bound/candidate/backup/target arguments. Do not invoke `update-internal`.

## 2026-07-28 Core-Probe EOF Failure

The retained-candidate promotion used the exact installed hidden seam and
failed before transaction with `parity.probe.missing_response`. Immediate
attestation proves the bound/candidate/live generation is unchanged and no
backup, marker, runtime temp, or installer scratch exists.

Minimal credential-free differential evidence proves official 0.146, bound
0.144.6, and candidate 0.145 all return only initialize when the runner closes
stdin immediately after writing the request batch. Candidate 0.145 returns all
three required response IDs in order when each request is response-paced and
stdin remains open until the final response. Premature EOF is the root cause.

Durable diagnosis and the three-option design are in
`.planning/checkpoints/2026-07-28-internal-0145-core-probe-eof-gate.md`.

### Human Gate

Stop at `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT`. Approval would authorize
coherent updates to the existing OpenSpec artifacts plus the exact same
two-file runner/test write set, isolated verification, exact-source reinstall,
and one more retained-candidate promotion attempt. It would not authorize a
second candidate/download or any excluded plugin/proxy/provider/dependency/Git/
release/archive/cleanup effect.
