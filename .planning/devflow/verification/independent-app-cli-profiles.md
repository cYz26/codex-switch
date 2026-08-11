# Independent App/CLI Profiles Verification

## Scope and Boundaries

- Change: `independent-app-cli-profiles`
- Canonical execution source:
  `openspec/changes/independent-app-cli-profiles/tasks.md`
- Approved effects: scoped source, tests, README/SKILL, OpenSpec, ledger,
  namespaced state, this evidence record, and one task-13 non-interactive
  functional command through the current managed internal CLI shim with its
  bounded internal Plugin/config/cache/shared-generation effects.
- Excluded effects: split retry or another install; App stop/restart/mutation;
  internal binary update; cache copy/delete/cleanup; parity runner; dependency
  or migration; Git; release; archive; credentials; and destructive work.
- Pre-existing parity/provider-migration worktree changes are preserved.

## Task 13 Planning and Live Root Cause

The 2026-08-11 functional invocation reached shared materialization and failed
with `shared_configuration.materialization.unverified_catalog`. Read-only
reproduction proved the catalog command itself exits zero with a supported JSON
schema. Its installed `browser@openai-bundled` record reports target cache key
`26.721.41059`, `installed=true`, and `enabled=true`; the safely resolved local
marketplace source manifest is current at `26.803.61601`.

The parser currently drops installed provenance and can overwrite an installed
version with an available duplicate. The backend-managed classifier then uses
one overloaded `entry.version` for both source and target and requires their
manifest versions/trees to match. The resulting pre-add
`unverified_catalog` is therefore a product bug, not invalid live data.

The confirmed systemic contract is OpenSpec task 13: preserve available/source
and installed/target identities independently; attest the desired source;
always call the target backend for pending backend-managed selectors; obtain
one fresh catalog for the whole batch; require a unique installed target key;
independently attest its safe cache, selector manifest, tree, and Skill roots;
then commit receipts. Revision cache keys and manifest versions remain separate.
No public persistent schema or dependency is needed.

Public RED seams are raw catalog JSON parsing, production shared
materialization using the live version split, post-add installed proof and
receipt identity, plus precise invalid-catalog/source-mismatch/unverified-target/
unsafe-cache boundaries. No production file changes before these REDs.

Task 13.1 RED command ran seven focused production-seam tests. Results were two
catalog-axis `AttributeError`s plus six behavioral failures/errors: live
source `26.803.61601` versus target `26.721.41059` still raised
`unverified_catalog`; a fresh revision target was ignored and fell into
`unsafe_cache`; available-only post state incorrectly succeeded; missing target
and safe source drift collapsed to `failed`; and the two-selector batch stopped
before native add/post-catalog. These are the intended pre-production failures.

## Task 13.2 GREEN

`PluginCatalogEntry` now preserves available/source projection separately from
installed provenance and the sorted unique installed target keys. Envelope
order and duplicate selectors cannot erase installed state. Backend-managed
source attestation uses only the desired source manifest/tree, never the
internal target version.

Every pending backend-managed selector now executes through the target backend;
all adds finish before one fresh batch catalog query. Receipt construction
requires one installed target key and independently verifies its contained
cache root, selector manifest, version relation, tree, and Skill roots.
Revision-like keys may differ from manifest versions. Missing/ambiguous targets
and safe manifest proof failures use `unverified_target`; unsafe structure,
source drift, catalog failure, and backend failure retain their distinct codes.

The seven original RED methods plus new ambiguous-target and manifest-mismatch
guards pass. The complete shared materialization/configuration/lifecycle matrix
passes 88/88 in 3.529 seconds, including config restoration, last-known-good
state, SIGKILL/store-lease recovery, unchanged-generation zero-work behavior,
portable-exact behavior, and no cache copy/link/delete.

## Task 13.3 Final Source, Package, and Review Proof

The final review found four additional boundary REDs before acceptance:
available-without-source fallback, safe source manifest drift classification,
dangling target-link classification, and catalog subprocess spawn
classification. GREEN now preserves an installed record's safe source path,
maps safe source identity failure to `source_mismatch`, keeps link hazards at
`unsafe_cache`, and maps catalog command/schema failure to
`unverified_catalog` while native add failure remains `failed`.

Fresh final-byte results:

```text
shared configuration/materialization/lifecycle: 93/93 in 3.745s
Runtime Binding:                              90/90 in 123.937s
Profile/wrapper:                             226/226 in 292.104s
Update/release:                              140/140 in 344.975s
packaged shared matrix:                       93/93 in 4.577s
```

All `scripts/*.py` compile under Python 3.12; wrapper/environment/installer/
runner/package Bash syntax and repository JSON parsing pass. Active strict
OpenSpec is valid and repository-wide strict validation is 22/22. DevFlow
workflow validation returns `ok=true`, zero issues, and only the existing
project-refresh guidance warning under INC-018. `git diff --check` passes.
Both independent Spec and Standards rereviews return PASS after the four
boundary repairs.

Generated Artifact Contract
`SPLIT-BACKEND-MANAGED-20260811T113820+0800` retains the isolated, uninstalled
counterpart at
`/private/tmp/codex-switch-backend-managed-repair-20260811T113820+0800`.
The 71-file package payload is `23477b06...428f1`, its archive is
`0b18c7a1...ed48`, the four task paths are byte-exact, and the package-local
shared matrix passes 93/93. Release-counterpart Plugin Eval is 54/100 under
the updated INC-012 exception. The read-only DevFlow updater audit reports
the named installed Plugin caches, including DevFlow 0.4.0 and Workshop 0.2.0,
`matches-source`; project migration remains pending and no apply ran.

## Task 13.4 Managed-Shim Acceptance and Cache-Lifecycle Closure

Exactly one functional command ran through the current managed internal shim:

```text
/Users/cY/.codex-switch/bin/codex plugin list --json
```

Stdout was consumed only by a JSON shape validator. The command printed the
flushed source-attestation and `materializing 18 Plugins for internal` phases,
then exited zero with a valid two-key JSON object. There was no retry or second
functional invocation.

Readback proves the primary repair outcome: shared generation 1 is committed
from `openai-official`, `pending_target` is null, all 18 internal receipts
re-attest, and the read-only report is `status=current`, `cli_ready=true`, with
zero findings. Revision cache keys remain distinct from manifest versions in
live receipts, including `11c74d6b` with manifests `0.1.2`, `2.0.13`, and
other compatible versions. No pending commit or materialization intent remains.

The official App stayed open. ChatGPT PID 68428 and official app-server PID
68766 retained their start times and executable paths. The following hashes
are identical before and after:

```text
managed shim:   fcb7b8e54ac55b29eb43711578ce31b1f7739283576ac69ee1ee35d9b69242e5
active record:  01087a5d63ced942fc0629e16191125f2b04068d539d84f01d8d6f4c4e97b2b2
LaunchAgent:    6291f689ddde8f03acb43ee85de1da0db33954d8a7cbd96553aff7d95cf4967b
official CLI:   04ddea2f332bd524bf6cc02f8efcf45f0afa0c7d9b97d77aaef7bb84adf3d4c5
```

Internal config changed from `f13b2548...63a` to `4ab19476...8ee` as the
authorized shared projection committed; the current read-only report proves
the final config/cache receipts agree. No split, install, App stop/restart or
mutation, internal binary update command, project migration, dependency, Git,
release, archive, credential, or cleanup action ran.

The same acceptance exposed a required contract decision. Native internal
`codex plugin add` replaced seven upgraded cache versions and removed the old
version directories for browser, chrome, computer-use, dev-flow, visualize,
pdf, and template-creator. The native help surface has no retain-old-version
option. Although codex-switch performs no direct copy/link/delete, this system
effect contradicted the earlier retention promise and therefore stopped the
task before a completion claim.

The user then explicitly selected native Plugin cache lifecycle. OpenSpec now
assigns installed-version retention, replacement, and removal to the native
backend while continuing to prohibit direct cache copy/link/delete or garbage
collection by codex-switch. A fresh post-call catalog and independently safe
target proof, not preservation of an older directory, authorize each receipt.
No second functional command, restoration, download, or cleanup was needed or
run. INC-025 is resolved and task 13.4 is complete.

This was a contract correction rather than new product logic. The public
`materialize_shared_plugins` seam therefore received characterization coverage
instead of an artificial failing implementation test: portable and
backend-managed fake native updates may replace prior installed versions, while
disable/remove without a native call proves codex-switch performs no direct
cache deletion. This justified no-RED exception is bounded to the lifecycle
ownership wording and test expectations.

Final source verification after the last edit is shared materialization 36/36,
the complete shared matrix 94/94, Runtime Binding 90/90, profile/wrapper
226/226, and serial Update/Release 140/140. The single earlier update/release
error was a 1.0-second fixture smoke timeout under concurrent suite load; its
isolated case and the complete serial suite both pass, including the same test.
Python/Bash static checks, strict active and repository-wide OpenSpec 22/22,
workflow validation, `git diff --check`, and local spec/standards review pass.

Generated Artifact Contract
`SPLIT-NATIVE-CACHE-LIFECYCLE-20260811T123157+0800` retains the final
uninstalled release counterpart at
`/private/tmp/codex-switch-native-cache-lifecycle-20260811T123157+0800`.
Its payload is `3f2852e6...48ab`, archive `f5c4bc6a...1a24`, and manifest
`57c320bf...ab07`; the four task paths are source/package byte-exact and the
package-local shared matrix passes 94/94. Plugin Eval is 54/100 under the
existing INC-012 exception. The earlier retained package root was not
overwritten after final edits; its immutable manifest rejected reuse and no
cleanup followed.

## Task 1.1 Selection and Parser RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_runtime_binding.py ActiveProfileSelectionTests
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_switch_help_exposes_explicit_app_profile_selection
```

Result:

- Selection interface: 8 tests, 8 expected errors because
  `codex_switch_selection` does not exist.
- CLI parser/help: 1 test, 1 expected failure because `--app-profile` is absent.
- No production file changed before RED.

Next: implement only the selection interface, additive record fields, and
parser option required to close these failures.

## Task 1.2 Selection and Parser GREEN

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_runtime_binding.py ActiveProfileSelectionTests
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_switch_help_exposes_explicit_app_profile_selection
python3.12 -m py_compile \
  scripts/codex_switch_selection.py \
  scripts/codex_switch_record.py \
  scripts/codex_switch_switching.py \
  scripts/codex_profile_switch.py
git diff --check -- \
  scripts/codex_switch_selection.py \
  scripts/codex_switch_record.py \
  scripts/codex_switch_switching.py \
  scripts/codex_profile_switch.py \
  scripts/test_codex_runtime_binding.py \
  scripts/test_codex_profile_switch.py
```

Result:

- Selection interface: 8 tests passed.
- CLI parser/help: 1 test passed.
- Python compilation and scoped whitespace validation passed.
- `ProfileSelection` is the only parser for requested and active identities;
  `active_record()` writes `profile`, `cli_profile`, and `app_profile` from
  that immutable value.

Next: finish the adjacent Runtime Binding/profile-state regression before
adding transaction REDs.

## Task 1.3 Adjacent Selection/Binding Regression

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_runtime_binding.py \
  RuntimeBindingTests.test_official_resolution_uses_bundled_cli_for_full_chain \
  RuntimeBindingTests.test_official_alias_normalizes_without_broadening_other_profiles \
  RuntimeBindingTests.test_internal_resolution_uses_managed_launcher_and_manifest_backend \
  RuntimeBindingTests.test_internal_raw_app_path_is_migration_drift_not_authority \
  RuntimeBindingTests.test_stale_active_record_is_not_binding_authority \
  RuntimeBindingTests.test_status_without_gui_env_prints_expected_binding \
  RuntimeBindingTests.test_status_doctor_and_verify_share_finding_codes \
  RuntimeBindingTests.test_verify_manifest_expectation_wins_over_stale_active_record
```

Result: 8 tests passed. Requested and active identity parsing remains confined
to `codex_switch_selection.py`; Runtime Binding continues to own only concrete
binary/home authority.

## Task 2.1 Split Transaction/Profile RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_split_switch_preview_names_cli_and_app_profiles \
  CodexProfileSwitchTests.test_split_switch_uses_internal_cli_and_official_app_atomically \
  CodexProfileSwitchTests.test_unsupported_split_request_preserves_committed_switch_state \
  CodexProfileSwitchTests.test_switch_updates_shim_and_app_cli_to_target_profile
```

Result: 4 tests ran; the two expected split failures were:

- dry-run omitted `CLI profile: internal` and `App profile: openai-official`;
- commit wrote `app_profile: internal` instead of `openai-official`.

The same-profile default and unsupported-combination zero-write guard passed.
This proves the public selection reaches the transaction options but the
transaction still overloads the CLI profile for Desktop planning.

## Tasks 2.2-2.3 Split Transaction GREEN and Recovery Contract

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_split_switch_preview_names_cli_and_app_profiles \
  CodexProfileSwitchTests.test_split_switch_uses_internal_cli_and_official_app_atomically \
  CodexProfileSwitchTests.test_unsupported_split_request_preserves_committed_switch_state \
  CodexProfileSwitchTests.test_switch_updates_shim_and_app_cli_to_target_profile
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_transaction.py \
  TransactionTests.test_split_selected_manifest_drift_preserves_state_per_journal_contract \
  TransactionTests.test_split_official_desktop_failure_rolls_back_both_surfaces
```

Result:

- Success/default/unsupported matrix: 4 tests passed.
- Desktop failure and selected-manifest drift matrix: 2 tests passed, with two
  manifest targets exercised in subtests.
- A Desktop plist failure after CLI effects restores both surfaces and the
  prior active record.
- Read-only official-manifest drift rolls back cleanly. A transaction-produced
  internal manifest replaced by an external writer is preserved and retains
  `rollback_failed` recovery evidence, matching the existing fail-closed
  journal contract instead of overwriting unknown state.

## Tasks 3.1-3.2 Status and Doctor RED/GREEN

RED command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_runtime_binding.py \
  RuntimeBindingTests.test_split_status_reports_separate_cli_and_app_profiles \
  RuntimeBindingTests.test_split_doctor_uses_official_app_binding_without_cross_surface_drift \
  RuntimeBindingTests.test_split_doctor_reports_only_the_drifted_surface \
  RuntimeBindingTests.test_malformed_split_active_selection_is_reported_stably
```

RED result: 4 tests ran with 1 error and 3 failures. Status returned one string
profile, Doctor selected the internal binding for Desktop, shell drift was not
reported independently, and partial split state was accepted.

GREEN result: the same 4 tests passed. Status reports both identities and
manifest-derived bindings; Doctor attests App state with the App binding,
checks the managed shell shim with the CLI binding, routes parity through the
internal CLI binding, and reports malformed state without guessing.

## Tasks 3.3-3.4 Verifier RED/GREEN

RED command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_verify.py \
  BoundedVerificationTests.test_split_verifier_routes_cli_and_app_checks_to_distinct_bindings \
  BoundedVerificationTests.test_split_active_verification_attests_official_app_and_internal_home
```

RED result: both tests errored because verifier collection exposed only one
Runtime Binding.

GREEN result:

- The same 2 routing tests passed.
- The complete `scripts/test_codex_verify.py` suite passed: 32 tests in
  13.675 seconds.
- Runtime, exec, and Responses checks retain the internal binary/home;
  app-server smoke and live observation use the official App binding; parity
  remains attached to the internal CLI binding.

## Task 2.4 Complete Transaction Regression

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py
```

The first run found one compatibility regression: default `--skip-app-cli`
calls were forwarded as though `--app-profile` were explicit. After restricting
transaction option forwarding to explicit overrides, the focused regression
passed and the complete suite passed: 241 tests in 25.550 seconds.

## Tasks 4.1-4.2 Wrapper and Package RED/GREEN

RED results:

- the one-key split applied successfully but its final result omitted separate
  CLI/App identities;
- the release bundle did not require `codex_switch_selection.py`.

GREEN commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_wrapper_one_key_split_reports_both_profiles_after_apply \
  CodexProfileSwitchTests.test_wrapper_profile_dry_run_allows_empty_switch_args_on_bash_32
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_update_release.py \
  CodexUpdateReleaseTests.test_release_bundle_requires_independent_selection_module \
  CodexUpdateReleaseTests.test_release_bundle_rejects_missing_required_python_modules
```

Both wrapper tests and both package tests passed. The wrapper usage, final
summary, README, and SKILL now describe the explicit split and unchanged
synchronized default.

## Task 4.3 Release Counterpart and Plugin Eval

The isolated release bundle built successfully at
`/private/tmp/codex-switch-split-release.xcq6bx/out/codex-switch.tar.gz`.
Its manifest includes `scripts/codex_switch_selection.py`, and the packaged
Python switcher successfully previewed `internal --app-profile official` with
separate CLI/App labels without importing the source checkout.

Plugin Eval command:

```bash
node /Users/cY/.codex/plugins/cache/openai-curated-remote/plugin-eval/0.1.2/scripts/plugin-eval.js \
  analyze \
  /private/tmp/codex-switch-split-release.xcq6bx/out/codex-switch/SKILL.md \
  --format markdown
```

Result: 54/100, grade F, high static risk; 2 budget failures, 4 warnings, and
2 informational findings. The failures are dominated by the existing bundled
support tree and 3,112-token invoked skill, while warnings cover the fixed
top-level README layout, existing transaction complexity, seven long lines,
and absent coverage artifacts. These are recorded as INC-012
`DEFER_AND_CONTINUE`: resolving them requires a separate benchmark-backed
skill/package architecture change rather than expanding this behavior change.

## Review RED/GREEN and Scope Closure

Two independent read-only review axes inspected the completed implementation:
observable OpenSpec behavior and repository engineering standards. Review REDs
proved and then closed these in-scope gaps:

- split planning could trust a legacy manifest's arbitrary official App path;
  it now re-resolves the verified official bundle authority;
- Doctor could accept a matching profile label while both the CLI home and shim
  drifted; it now checks both concrete CLI binding values;
- malformed active selection could reach repair, live observation, or smoke
  helpers; command preflight now fails closed before any of them run;
- unsupported-selection errors omitted the only supported split pair, and the
  packaged dry-run omitted the two binary paths; both public contracts now have
  focused regressions.

The final spec review reported no remaining spec deviation or scope creep. The
final standards spot check was clean. The larger transaction target-object
refactor suggested during structural review is non-blocking and remains covered
by the existing INC-012 package/complexity follow-up rather than expanding this
change. Pre-existing parity and provider-migration paths were not rewritten for
this feature.

## Fresh Complete Source Matrix

Commands and results after the last source change:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_runtime_binding \
  scripts.test_codex_transaction \
  scripts.test_codex_verify
# 362 tests in 144.888s: Runtime Binding 88, Transaction 241, Verify 33; OK

PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
# 210 tests in 261.046s; OK

PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py
# 133 tests in 284.896s; OK
```

The final verifier matrix includes the new malformed-selection preflight guard
and completes at 33/33. Interrupted stale full runs are excluded from evidence;
only the completed commands above count.

## Verified Release Counterpart

The final retained release counterpart is:

`/private/tmp/codex-switch-split-release.xcq6bx/verified-out/codex-switch.tar.gz`

With the working directory inside the extracted package and `PYTHONPATH`
unset, its split dry-run reported:

- CLI profile `internal`, binary `/bin/echo`, and the isolated internal home;
- App profile `openai-official`, binary
  `/Applications/ChatGPT.app/Contents/Resources/codex`, and the isolated
  official home;
- dry-run only, with no workstation mutation.

Source and extracted-package SHA-256 pairs are identical:

| Path | SHA-256 |
|---|---|
| `scripts/codex_switch_selection.py` | `d792e0fc289e8eca4bbdf2729fa64726633b96ef894c794eb5fad3f468d73730` |
| `scripts/codex_switch_switching.py` | `bb13dd78986e7e214b244a2dd2cd18690fc6054cd596dd07083f60394b337926` |
| `scripts/codex_switch_transaction.py` | `d33270d137b51a4d0e024bef27db99c8a3465401ad6be5f1e9645d581af60856` |
| `scripts/codex_switch_verify.py` | `01ef3ec86fda3ee470f98925c4cf542f97246ecd6fd05e5bcc78428880715247` |
| `scripts/codex-switch` | `9b8014436bfe995b082acee18133fd158143af247a73dc2bd09356ccf540f686` |
| `SKILL.md` | `a11c756db5793b6cf478d3a7befb0d614f64760bf6695deab77174202d5adfc3` |

Plugin Eval was rerun against that verified counterpart and retained the same
54/100, grade F, high-risk result: 2 failures, 4 warnings, 2 informational
findings, with a 3,112-token invoked skill and 939,328-token deferred support
tree. INC-012 remains `DEFER_AND_CONTINUE`; no benchmark, package architecture
refactor, paid run, install, release, or cleanup is authorized by this change.

## Final Static, Spec, Workflow, and Parity Validation

Fresh commands after the last source change and after control-plane
reconciliation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py
# 95 tests in 2.177s; OK

PYTHONPYCACHEPREFIX=/private/tmp/codex-switch-pycompile.jDEW4c \
  PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile scripts/*.py
bash -n scripts/codex-switch scripts/codex_env_setup install.sh run.sh
# Python compilation and all four Bash syntax checks passed

openspec validate independent-app-cli-profiles --strict --no-interactive
# valid
openspec validate --all --strict --no-interactive
# 20 passed, 0 failed

python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py \
  --repo . --json
# ok=true, issues=[], warnings=[]

git diff --check
# passed
```

The isolated pycompile cache root is retained because cleanup was not
authorized. No repository bytecode cleanup, live install, active-profile/App
mutation, App restart, dependency, Git staging/commit/push, release, archive,
or destructive action was performed. The verified source outcome is
`READY_FOR_EXTERNAL_EFFECT`; applying it to the workstation remains a separate
Human Gate.

## Read-Only Archive Readiness

`openspec status --change independent-app-cli-profiles --json` reports all four
planning artifacts complete. The required read-only DevFlow archive check
reports `canArchive=false` and `ready=false`: archive authorization is absent,
`archive_allowed` remains false, hash-bound spec-sync evidence is intentionally
absent, and the preserved worktree contains unrelated dirty paths. No spec
sync, archive, cleanup, or unrelated-worktree mutation was attempted.

## 2026-08-05 Reopened Shared Plugin/Skill Completion

### Delivered Behavior

The split now owns one generationed, secret-screened desired projection for
`marketplaces.*`, `plugins.*`, and `skills.config`. Official is the first
bootstrap authority. A functional managed internal CLI invocation reconciles
App-originated changes and verifies an independently materialized internal
Plugin cache before backend `exec`. Help/version and all diagnostic modes stay
read-only. CLI-originated changes are captured as pending for the official App;
`sync-shared --dry-run` previews without writes, and apply requires a complete
stopped-App/process proof that is rechecked before materialization and commit.

Personal standalone Skills use the official personal `skills/` root through a
validated internal directory link. Plugin-contributed Skills remain beneath
each independently attested profile cache and have target paths remapped only
after traversal, symlink, and special-file checks. Project-local
`.agents/skills` and `AGENTS.md` remain repository-owned and are not copied
between homes. Disable/removal changes desired usage without deleting retained
cache evidence.

The final ownership audit is:

| Surface | Final ownership |
|---|---|
| Plugin selectors, secret-free marketplace descriptors, configured Skills | shared desired generation with three-way conflict detection |
| Personal standalone Skills | official root plus validated internal link |
| Plugin code and contributed Skills | independent profile caches and repair |
| Project-local Skills/instructions | shared naturally through the worktree |
| Model/provider/endpoint/reasoning/personality | profile-local; never projected |
| Auth/tokens/OAuth/sessions/history/databases/logs | private; never projected or synchronized |
| MCP/apps/connectors | deferred until field-level version and secret review |
| Hook commands/trust | deferred until executable digest/path/permission review |
| UI/features/agents/memories preferences | deferred until per-field cross-version review |
| Project trust/permissions/sandbox/cloud/account/update state | profile/host-local |
| Automations/process/browser/thread routing/catalog/cache state | runtime-derived; never synchronized as config |

### Crash, Conflict, and Materialization Closure

Decision 14 adds a private mode-0600 `pending-materialization.json` beneath the
private mode-0700 store before any target backend call. It binds supported
source/target identities, exact target path and before kind/bytes/mode, and the
sorted enabled selector set. It is mutually exclusive with the main prepared
commit journal. Normal return, ordinary exception, and later locked recovery
classify exact selector deltas: owned-only restores the predecessor;
owned-plus-foreign removes only owned activation and preserves foreign bytes;
foreign-only blocks without overwrite; unclassifiable selector mutation keeps
the intent and fails closed. Interrupted cache artifacts are retained and must
pass normal current receipt/tree/Skill-root attestation before reuse.

Independent review then reproduced one final P1: parent `SIGKILL` could leave a
real backend child alive while early recovery observed unchanged target bytes
and retired the intent. Decision 15 closes it by exposing the exact active
store-root flock FD through a private locked-mutation seam, validating
store/inode identity again at the production materializer, and passing it via
`pass_fds` to both catalog/list and plugin/add subprocesses. The real regression
proves parent SIGKILL, surviving child, store-busy early apply before any plan,
byte-exact intent/config preservation, late selector write, child exit, lease
release, and Decision 14 recovery before a new plan. Main independently reran
that test 1/1. Final independent review returned `APPROVE` with no P1/P2.

### Fresh Terminal Test Matrix

Only completed post-Decision-15 runs count:

```text
shared configuration + materialization + lifecycle: 72/72 in 3.011s
transaction:                                      241/241 in 24.016s
Runtime Binding:                                    88/88 in 117.726s
verify:                                             33/33 in 15.382s
profile:                                           211/211 in 286.080s
update/release:                                    133/133 in 307.509s
parity:                                              95/95 in 2.207s
config document:                                     29/29 in 3.599s
```

The profile matrix includes
`test_wrapper_split_still_runs_internal_update_check`, so
`codex-switch internal --app-profile official` still performs the internal
binary update check and keeps update/plugin preparation bound to internal.
A separate final named run passed 1/1 in 7.943 seconds.
One parallel update/release smoke timeout and one parallel parity process-start
timing failure were excluded; their named tests and complete suites passed when
rerun serially on final bytes.

Final static/distribution commands passed:

- Python 3.12 compile for `scripts/*.py` in retained isolated pycache
  `/tmp/codex-switch-final-pycache.pYXxcC`;
- Bash syntax for `scripts/codex-switch`, `scripts/codex_env_setup`,
  `install.sh`, `run.sh`, and `scripts/package-release.sh`;
- `evals/evals.json` parse, `git diff --check`, active strict OpenSpec, and
  repository-wide strict OpenSpec 20/20;
- final DevFlow workflow state and Agent Task Contract validation;
- isolated package
  `/private/tmp/codex-switch-final-release.SJEkjM/codex-switch.tar.gz`;
- archive SHA-256
  `05353c44e1825d64906cac6ea605518d837f24f66d48d63e05f04f9bab5a2eae`;
- packaged shared tests 72/72 and packaged split preview 1/1;
- byte-exact source/package hashes for README, SKILL, transaction, shared
  configuration, Plugin materializer, Runtime Binding, Python switcher, and
  wrapper.

### Release Counterpart and Local Reference Audit

Final Plugin Eval against the isolated release counterpart is 58/100, grade D,
high static risk: two budget failures, three warnings, and two informational
checks. Trigger cost is 43 tokens, invoked cost 3,512, and deferred support cost
1,022,064. The warnings are the top-level README, high Python complexity, and
seven long lines; coverage artifacts are unavailable. INC-012 remains
`DEFER_AND_CONTINUE` because a fix requires an observed-usage benchmark and a
material skill/package architecture change outside this behavior contract.

The final read-only local-reference check reports the installed DevFlow cache
`matches-source`, OpenSpec 1.7.0 unchanged, and project Skill layout current.
It also reports broader DevFlow project migration pending. No `--apply`, cache
refresh, project migration, marketplace upgrade, install, or external updater
was executed.

### Final Boundary

No live install, profile/App switch, stopped-App real sync, App restart, real
Codex backend or Plugin cache mutation, credential change, dependency, Git
stage/commit/push, release, archive, cleanup, or destructive action occurred.
The source is `READY_FOR_EXTERNAL_EFFECT`; applying it to the workstation is a
separate authorization gate. The unrelated
`PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT` gate remains unchanged.

## 2026-08-06 Live Deployment Attempt

The user authorized the supported local deployment and split activation. The
pre-install references were exact 20-path payloads: `current` was
`6a23d04f8408681c26ed116583b208699f4b8fba4357162717befe7af8c1f132`
and rollback was
`275ad2e2fda95c0d2591fe95aa4d9e7075988da286851f6584e51c3bad771dab`.
Both initial installer invocations failed before immutable promotion with
`Release manifest required paths mismatch`; neither reference changed.

The deployment blocker was an exact compatibility omission. The latest
release requires 22 paths and the installed generation requires 20, but
historical validation recognized only the older 16-path generation. A public
installer regression reproduced the live error:

```text
test_installer_upgrades_immediately_prior_twenty_path_manifests
Ran 1 test in 6.017s
FAILED: return code 2, candidate_invalid, required paths mismatch
```

The minimal repair owns two exact historical tuples, 16 and 20 paths; it does
not accept subset, superset, or reordered manifests. `install.sh` and `run.sh`
bind the resulting release-bundle validator SHA-256
`e7dc4a28850fe27ac2c62f160dcf364ad575679dfa7c6984567e79aa177ed9a1`.
Fresh focused evidence:

```text
new 20-path installer regression: 1/1 GREEN in 6.917s
16-path + 20-path + malformed/reordered promotion: 3/3 GREEN in 15.759s
release bundle + package adapter: 2/2 GREEN in 2.287s
Bash syntax and both trusted bootstrap hashes: passed
```

Generated Artifact Contract
`SPLIT-DEPLOY-20260806T123605+0800` owns the retained package root
`/private/tmp/codex-switch-deploy-20260806T123605+0800`. The strict package has
22 required paths, payload SHA-256
`e6caa91b8b456bf16083b81d76042637d1c3aaa48ca78f072dc8a0eaed2e4983`,
and archive SHA-256
`fc279ac81d948e3b8f75f9825520e84d77e94af6f691e8706c735b1fc1edb287`.
README, SKILL, VERSION, runner, wrapper, release validator, switcher, Runtime
Binding, Plugin materializer, and shared-configuration module are byte-exact
between source and package.

Supported installation succeeded. Installed `current` is the new 22-path
payload, installed rollback is prior current `6a23d04f...f132`, and the global
wrapper is byte-exact with source and exposes `--app-profile` plus
`sync-shared`.

Two live commands then ran with `--skip-update-check` so the separate internal
0.145 compatibility gate remained untouched:

```text
codex-switch --skip-self-update internal --app-profile official --skip-update-check
```

Both failed before commit and rolled back. The first observed the official
Desktop global-state source change after `shared_support_sync`; the second
observed it before that intent. Backups are
`20260806T043745Z-switch-openai-official-to-internal` and
`20260806T044114Z-switch-openai-official-to-internal`. Final read-only status
still reports CLI/App `openai-official`; ChatGPT pid 71620 and official
app-server pid 71957 still use the bundled official binary. The installed
payload and rollback references remain healthy.

### Gate

`SPLIT-DEPLOY-APP-RESTART` is required. The running App must quit completely so
the frozen global-state input can remain stable; one exact background switch
can then commit and reopen the App. No further retry while the App runs is
allowed. This gate excludes the internal 0.145 upgrade, unrelated stopped-App
pending sync, dependencies, Git, release, archive, package/backup cleanup, and
destructive effects.

## 2026-08-10 Concise Split Shortcut and Immutable Install

The confirmed public interface is now:

```text
codex-switch split
codex-switch split --keep-version
```

`split` is a fixed wrapper preset for the existing supported
internal-CLI/official-App workflow. It retains the normal codex-switch
self-update and internal binary update detection/promotion behavior.
`--keep-version` is split-only and suppresses both update paths while leaving
Plugin repair, verification, Doctor, status, and ordinary outcome handling
intact. `--dry-run` composes normally, and the preset rejects `--app-profile`
instead of allowing the official App target to be retargeted. No switch,
transaction, shared-configuration, parity, or repair policy was duplicated.

### Ordered RED/GREEN Evidence

The public seam is the real `scripts/codex-switch` process with assertions on
exit status, output, and forwarded public arguments.

```text
RED 1: test_wrapper_split_shortcut_routes_supported_pairing
       failed with return code 2 and `Unknown command: split`.
GREEN: 1/1 passed in 1.123s after the minimal route was added.

RED 2: test_wrapper_split_keep_version_skips_internal_update_check
       failed because `--keep-version` reached the Python parser as an
       unrecognized argument.
GREEN: the two update-semantics tests passed 2/2 in 5.890s after wrapper-only
       normalization.

RED 3: test_wrapper_split_rejects_app_profile_override
       failed because the fixed preset could be retargeted.
GREEN: 1/1 passed after pre-self-update rejection was added.
```

Final focused coverage passed 10/10 in 27.496 seconds. It includes normal and
frozen self-update behavior, normal and frozen internal update behavior,
fixed-preset routing and rejection, pure help, package preview, and rejection
of `--keep-version` outside `split`. The complete profile suite passed 219/219
in 316.252 seconds. The four adjacent bundle/package/installer tests passed
4/4 in 9.317 seconds. The final packaged preview passed 1/1 in 2.570 seconds.

Bash syntax passed for the wrapper, environment setup, installer, runner, and
package adapter. The changed Python test AST compiled, `git diff --check`
passed, and strict active plus repository-wide OpenSpec passed 20/20.

### Final Package and Plugin Eval

Generated Artifact Contract
`SPLIT-SHORTCUT-20260810T120157+0800` was sealed while its physical root was
absent. Its terminal disposition remains `RETAIN`; cleanup was not authorized.

```text
physical root:
  /private/tmp/codex-switch-shortcut-20260810T120157+0800
archive SHA-256:
  c38a619fc2ccb9ed38eec161f54adcf793b2806313a2248b40c999a1204e174b
payload SHA-256:
  b88326ff747278543b94176b00816f8c9b4e692afbf31fee5a490da107cff49d
manifest SHA-256:
  02c9598a5c76297c4d20bf51dbc6aa40ba0779dc9bc60919b8d0481806d07012
required paths: 22
files/directories: 71/5
```

Source and package are byte-exact for the wrapper, README, SKILL, and complete
profile test file. Final release-counterpart Plugin Eval is 58/100, grade D,
high static risk: two budget failures, three warnings, and two informational
checks. Trigger cost is 43 tokens, invoked cost 3,667, and deferred support
cost 1,026,059. INC-012 remains `DEFER_AND_CONTINUE`; addressing it requires a
separate benchmark-backed package/Skill architecture change.

The read-only local-reference audit reports installed DevFlow 0.4.0
`matches-source`, OpenSpec 1.7.0 unchanged, and current project Skill layout.
It also reports broader project migration pending. INC-018 records that
non-blocking drift; no apply, refresh, migration, marketplace upgrade, or
legacy cleanup ran.

### Immutable Installation and Live-State Non-Claim

The supported installer consumed the exact local archive and succeeded:

```text
current:  releases/b88326ff747278543b94176b00816f8c9b4e692afbf31fee5a490da107cff49d
rollback: releases/e6caa91b8b456bf16083b81d76042637d1c3aaa48ca78f072dc8a0eaed2e4983
wrapper SHA-256:
  6132984ce3ad62394ee17b3e4c1888194eaa3f9ba9303c988d25aad69e82d6e0
installer staging residue: none
```

Installed wrapper, manifest, and complete profile test are byte-exact with the
verified source/package. Installed help exposes `split` and `--keep-version`.
Installed Doctor passes. The isolated package preview passes without checkout
code or workstation mutation.

No live shortcut was run. Read-only status remains CLI/App
`openai-official`; ChatGPT remains pid 2375 and its official bundled app-server
remains pid 2920. `verify internal --repair=none` exits 1 with the truthful
pre-activation findings: active CLI/home/binary mismatches,
`binding.observation.active_stale`, and `parity.receipt.missing`.

`SPLIT-DEPLOY-APP-RESTART` remains the active Human Gate. The App must be fully
quit before one installed shortcut invocation can safely freeze and commit its
global-state input. This task did not stop/restart the App, activate the split,
update the internal binary, repair parity, migrate DevFlow, perform Git or
release/archive effects, or clean retained evidence.

## 2026-08-10 Live Bootstrap Portable-Identity Repair

Generated Artifact Contract
`SPLIT-BOOTSTRAP-20260810T213729+0800` was sealed after confirming the exact
root `/private/tmp/codex-switch-bootstrap-repair-20260810T213729+0800` was
absent. Task 12.4 alone owns release-counterpart files produced there by
`scripts/package-release.sh`. Its terminal disposition is `RETAIN`; no cleanup,
install, promotion, cache refresh, or release is authorized.

### Root Cause and Ordered RED/GREEN

The target backend's verified available-catalog shape may expose one installed
record whose `version` is stale while its local `source_path` has already
advanced. Production `_portable_catalog_source_is_exact()` incorrectly required
that installed version to equal the desired portable cache key before inspecting
the source manifest/tree. The first functional CLI therefore spent time on
source observation and the target catalog, then mislabeled a safe update as
`shared_configuration.materialization.unsafe_cache`; generation zero never
committed, so every functional retry repeated the work.

The public production-materializer and functional-preflight seams recorded four
ordered failures before their corresponding production changes:

```text
RED 1: stale installed 1.0.0 + exact source 2.0.0
       -> shared_configuration.materialization.unsafe_cache
RED 2: safely contained but tree-drifted source
       -> unsafe_cache instead of source_mismatch
RED 3: functional bootstrap reached materializer with empty stderr progress
RED 4: catalog source root symlink reached native add once before failing
```

GREEN now treats catalog `version` only as installed target state for
`portable_exact`. The separately resolved source must be an absolute real
directory with a matching selector manifest and complete desired tree digest.
A safe version/tree drift returns
`shared_configuration.materialization.source_mismatch`; unsafe roots/links/file
kinds/cache identities remain `unsafe_cache`. Native target add/update is still
followed by exact independent-target attestation, and the older target cache is
retained. Config restoration, receipt commit, pending-intent recovery, and
running-process boundaries are unchanged.

Functional internal preflight now flushes
`Shared configuration: attesting source configuration and Plugin identities...`
before observation and, only when target work is required, flushes the target
profile and enabled Plugin count before the catalog/backend call. The test
captures stderr at materializer entry and proves both flushes have already
occurred. Existing lifecycle regressions continue to prove help/version skip
preflight and an unchanged committed generation makes no materializer/network
call.

### Final Source and Package Proof

Final-byte suites:

```text
shared materialization/configuration/lifecycle: 81/81 in 3.365s
Runtime Binding:                            90/90 in 113.890s
Profile/wrapper/update/plugin adjacency:   226/226 in 287.115s
packaged shared materialization:             23/23 in 1.012s
```

Python AST compilation for every `scripts/*.py`, eval JSON parsing, and Bash
syntax for the wrapper, environment setup, installer, runner, and package
adapter passed. Active strict OpenSpec is valid; repository-wide strict
OpenSpec is 22/22. DevFlow workflow validation returns `ok=true` with only the
pre-existing project-refresh guidance warning covered by INC-018. Final
`git diff --check` passes.

The retained release counterpart is version `0.1.13`, with 22 required paths,
71 files, and 5 directories:

```text
payload SHA-256:  809aeda5123cb1725bc579f5b9b6d2291cd71395e149223ad392decc73f82583
archive SHA-256:  3734296c4d1bf1a8db63f012d231de63a6d6aa4432603a7f2abbb8cbcd3961e9
manifest SHA-256: c8f3b73114e589444ab3b3c1a641d600a05fbe2291961c1054913e4796e937c0
```

`codex_switch_plugins.py`, `codex_switch_shared_configuration.py`, the complete
materialization test, README, and SKILL are byte-exact between source and the
counterpart. Final release-counterpart Plugin Eval remains 58/100, grade D,
high risk, with 2 failures, 3 warnings, and 2 informational findings. The
budget/package-architecture work remains INC-012 `DEFER_AND_CONTINUE` rather
than expanding this repair.

The required read-only local-reference audit exits zero. DevFlow 0.4.0 reports
`matches-source` and current project Skill layout; project refresh remains
pending under INC-018. The unrelated plugins-mirror upstream, local
`hatch-pet`, and `game-design-workshop` cache/source findings are recorded as
INC-024. No updater apply, cache refresh, marketplace upgrade, project
migration, or local-Skill overwrite ran.

### Terminal Boundary

OpenSpec task 12 is complete 4/4; the parent change is 45/47 because the older
live install/acceptance tasks 10.3-10.4 remain separately gated. No live
`codex`, split, install, internal update, Plugin/cache mutation, App stop or
restart, dependency/migration apply, credential/provider traffic, Git,
release, archive, cleanup, or destructive effect occurred. Source is
`READY_FOR_EXTERNAL_EFFECT`; installation and one functional live validation
require a new exact authorization.

## Task 14 Managed Runtime-Config Render Idempotence

### Root Cause and RED

The active internal runtime had one 244-line blank run between
`model_providers.azure.query_params` and the generated shared-section marker.
`extract_toml_table_block()` stops at the next TOML table, so the prior
generated shared marker and its preceding whitespace were retained inside the
profile-provider seed. `strip_managed_comments()` removed the marker but left
that whitespace, and re-annotation added one more blank line on every
last-runtime render.

The focused RED persisted an initial render, then compared two consecutive
last-runtime renders with unchanged profile/shared inputs:

```text
python3.12 scripts/test_codex_config_document.py \
  ConfigDocumentTests.test_managed_runtime_render_is_byte_idempotent -v

FAIL: the later render contains one additional blank line before
# codex-switch: shared settings
```

The first canonical render is intentionally excluded from byte equality because
its provenance annotation legitimately changes from fallback canonical config
to last runtime config.

### GREEN and Preservation

`strip_managed_comments()` now removes only the contiguous blank lines
immediately preceding a generated `# codex-switch:` annotation. It does not
globally compact TOML, remove user comments, or alter non-adjacent user spacing.
The repeated-render and user-spacing guards pass 2/2.

Fresh validation:

```text
config-document suite, Python 3.12: 31/31 in 2.196s
focused profile adjacency:           4/4 in 5.229s
complete profile-switch suite:     226/226 in 306.951s
```

A read-only in-memory render against the current 244-line live input proves the
old and new outputs parse to equal TOML data while the maximum blank run changes
from 245 to 1. The live file remained byte-unchanged. The complete merge also
contains three pre-existing shared-source timestamp updates under
`marketplaces.*.last_updated`; those are unrelated to this formatting repair
and were not written.

The system `python3` is 3.9.6 and cannot run the Config Document suite because
that module intentionally requires Python 3.11+ `tomllib`; the qualifying
runtime is Python 3.12.13. The exploratory 3.9 run is not counted as validation.

### Static, Workflow, and Effect Boundary

- AST parsing passes for the two changed Python files.
- Strict active OpenSpec passes; repository-wide strict validation is 22/22.
- DevFlow workflow validation returns `ok=true` with only the pre-existing
  Project-Directed Implementation Readiness guidance warning.
- The read-only dependency audit still reports the existing project DevFlow
  source conflicts under INC-018; the required project-local TDD and diagnosis
  skills and OpenSpec 1.7 are ready, and no dependency activation ran.
- `git diff --check` passes.
- No live config rewrite, switch, install, App action, Plugin/cache operation,
  dependency/project migration, credential, Git, release, archive, cleanup, or
  destructive effect occurred.

## Task 15 Failed Release-Upload Starter Recovery

### Root Cause and RED

Auto Release run 16 at commit `2383cc2` checked out tag `v0.1.14` at
`19a243342ef9f78776b3fad0b2292198845147d3`. The public release inventory shows
only GitHub's generated source archives, while `gh release upload` rejects the
first canonical asset as already present:

```text
release_auto: Command failed (1): gh release upload v0.1.14 .../install.sh
asset under the same name already exists: [install.sh]
```

GitHub documents that a failed upload can retain an empty asset in `starter`
state. The current adapter reads only the release payload's embedded uploaded
asset names, discards asset ID/state/size, and therefore classifies the reserved
name as missing before retrying the conflicting upload.

The deterministic focused RED uses an adapter whose uploaded view is empty but
whose hidden inventory owns `install.sh` as asset ID `901`:

```text
python3 -m unittest -v \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_recovers_hidden_zero_byte_starter_asset \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_rejects_nonempty_starter_asset \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_rejects_unsupported_hidden_asset_state \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_github_release_inspection_lists_starter_assets

FAILED: 1 failure, 3 errors
primary error: asset under the same name already exists: [install.sh]
adapter failure: expected 100 explicitly listed uploaded assets, observed 0
```

No live GitHub Release mutation, workflow rerun, DevFlow migration apply,
dependency, Git, archive, cleanup, or other external effect occurred.

### GREEN

`GitHubCliAdapter.inspect_release()` now resolves the release ID and pages the
explicit release-assets endpoint at 100 records per page. Uploaded names remain
the ordinary visible set; every non-uploaded record retains exact
`asset_id/name/state/size` evidence.

`reconcile_release_assets()` accepts only a canonical `state=starter`,
`size=0` record for recovery. It rechecks tag identity, deletes that exact
asset ID, reads the release back, verifies any concurrently visible canonical
asset, uploads only remaining names, and retains the existing post-upload and
post-publish download/hash checks. It never uses `--clobber`.

Focused GREEN:

```text
Ran 7 tests in 1.027s
OK
```

The matrix covers hidden zero-byte recovery, non-zero refusal, unsupported
state refusal, tag revalidation, two-page inventory parsing, duplicate-name
refusal, and exact-ID delete command construction.

### Final Validation and Review

Fresh qualifying results on Python 3.12.13:

```text
focused starter/conflict matrix:  7/7 in 1.027s
complete update/release suite: 148/148 in 309.641s
complete profile suite:        226/226 in 338.729s
Python AST compile:                2/2
Bash syntax:                       5/5
active strict OpenSpec:          valid
all strict OpenSpec:             22/22
DevFlow 0.4.1 workflow:          ok=true, issues=[]
git diff --check:                passed
```

The workflow validator retains one existing Project-Directed Implementation
Readiness guidance warning covered by INC-018. An exploratory system Python
3.9.6 run before the final duplicate-name test passed 145/146; its only failure
was the established Python 3.11+ `tomllib` packaging boundary, so it is not
qualifying evidence.

Two profile invocations were also discarded as validation-environment errors:
one PTY-backed run waited at an otherwise captured interactive prompt, and one
run globally forced shell-bootstrap suppression and therefore failed the two
tests that intentionally exercise temporary shell-profile writes. The accepted
non-PTY run used the test suite's own per-case isolation and passed 226/226;
the real `~/.zshrc` hash, inode, and timestamps remained unchanged.

Final scope review confirms that recovery is limited to required canonical
names with `state=starter` and `size=0`, uses exact asset IDs, revalidates tag
identity before each deletion and upload, reads the inventory back before
upload, and preserves all existing download/SHA checks. Uploaded, non-zero,
duplicate-name, and unsupported-state records fail closed, and no path uses
`--clobber`.

No live GitHub Release mutation, workflow rerun, DevFlow migration apply,
dependency, credential, Git, archive, cleanup, or destructive effect occurred.
