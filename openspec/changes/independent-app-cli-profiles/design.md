## Context

See `proposal.md` for motivation and
`specs/codex-switch/spec.md` for observable behavior. Current local evidence on
2026-08-04 shows ChatGPT Desktop running the verified bundle at
`/Applications/ChatGPT.app/Contents/Resources/codex`, while the interactive
shell reaches an internal plugin binary ahead of the managed switch shim. The
current `--skip-app-cli` option can preserve that accident for one operation,
but `active.json` has only one profile identity and every diagnostic resolves a
single `RuntimeBinding` for both shell and Desktop.

The worktree already contains unrelated parity and completed DevFlow-provider
migration changes. This change is independent: it preserves their bytes,
does not cross the parity live Human Gate, and does not apply a workstation
switch.

## Skill Routing Ledger

- request_kind: feature, runtime binding, state compatibility, and error
  handling
- artifact-status: final; no Open Questions remain
- workflow_mode: Full OpenSpec
- capability-research: required / used; current wrapper help, manifests,
  active record, PATH, LaunchAgent, App bundle, running app-server, transaction,
  status, Doctor, verifier, release packaging, official Plugin/Skill surface
  documentation, live sanitized Plugin/Skill projections, and both profile
  cache layouts were inspected
- decision-resolution: required / used; the user selected internal CLI and
  official App, with internal binary/home and official bundle/home as the
  concrete interpretation
- decision-grilling: skipped; the requested ownership split and safest default
  home mapping are unambiguous after local evidence
- implementation-planning: required / used; this design and `tasks.md` own the
  executable contract
- architecture-guidance: required / used; one deep active-selection module
  owns profile identity while one deep shared-configuration module owns
  desired-state reconciliation, materialization policy, and receipts
- domain-language-modeling: skipped; existing profile, binding, home, shim, and
  Desktop terms are sufficient
- openspec-routing: required / used; behavior and compatibility are canonical
  in this independent change
- test-first-execution: required / used for slices 1-5; required / pending for
  the reopened shared-capability slices, which start with public-seam REDs
- root-cause-diagnosis: required / used; initial feature work was a missing
  supported state, while the 2026-08-10 live bootstrap failure was reproduced
  as an installed-version/source-identity conflation in the production
  materializer
- change-review: required / pending after the shared-capability implementation;
  the previous two-axis split-selection review remains recorded
- completion-proof: required / pending for the reopened change; the previous
  split-selection source matrices remain baseline evidence only
- execution-orchestration: required / used; `tasks.md` is the sole execution
  source for this change

## Capability Evidence

- `authoritative_current`: `scripts/codex-switch --help` and
  `scripts/codex_profile_switch.py` expose synchronized `internal`/`official`
  switching plus `--skip-app-cli`; `codex-switch --skip-self-update status`,
  both product manifests, LaunchAgent state, and the running process prove the
  App and shell paths can already differ at runtime.
- `local_scan`: `codex_switch_record.py`, `codex_switch_transaction.py`,
  `codex_switch_runtime_binding.py`, status/Doctor/verify modules, wrapper
  orchestration, focused tests, release bundle allowlists, README, and SKILL.
- `comparison`: leaving `--skip-app-cli` as the operator workaround is smallest
  but cannot persist intent or verify health; a synthetic profile would mix
  profile-home semantics; changing all internal switches to leave Desktop
  official would break current behavior. An additive explicit App-profile
  override plus canonical selection state is the smallest safe product path.
- `assumptions`: the verified ChatGPT bundled binary remains the official App
  authority and the internal manifest remains the internal CLI authority; both
  are re-resolved at execution time rather than copied from this observation.
- `contract`: the delta scenarios require additive state compatibility,
  atomic rollback, surface-specific diagnostics/smokes, unchanged defaults,
  and packaged parity.
- `live_repair_evidence`: the official desired artifact for
  `dev-flow@cy-codex-skills` is `0.4.0`; the internal target retains
  `0.3.0+codex.20260529145038`; and the target backend's verified JSON reports
  only that older installed version while resolving the local marketplace
  source whose manifest and tree are already `0.4.0`. Other `portable_exact`
  selectors attest successfully, and no cache-root, symlink, or special-file
  violation explains the failure.
- `backend_managed_live_evidence`: the verified internal catalog reports
  `browser@openai-bundled` installed at `26.721.41059` while its resolved local
  marketplace source manifest is `26.803.61601`. The same installed/source
  version split affects six bundled selectors. The current parser drops the
  installed provenance, and the current classifier requires source and target
  manifest versions to match, so a valid catalog is collapsed into the false
  `shared_configuration.materialization.unverified_catalog` finding.

## Target State

`codex-switch internal --app-profile official` is a first-class, dry-runnable
switch, and `codex-switch split` is its concise wrapper preset. It prepares and
selects the internal profile for shell execution while binding Desktop to the
current canonical official bundle. Normal `split` preserves codex-switch and
internal update behavior; `split --keep-version` explicitly freezes both
update layers for controlled activation. Active state records both identities;
all readers agree on the split and diagnose each surface against its owner.
Existing same-profile commands and legacy active records continue to work
without migration. In the supported split, one store-owned Plugin/Skill desired
generation is rendered into both homes, each backend owns its materialized
cache, and the internal CLI never starts with an incomplete generation.

## Goals / Non-Goals

**Goals:**

- Add one explicit, backward-compatible split-selection interface.
- Add one concise preset without duplicating or weakening the existing
  update, switch, repair, verification, Doctor, or status workflow.
- Keep profile identity, path resolution, and legacy-record interpretation
  behind one shared selection interface.
- Reuse the existing transactional journal and Desktop adapter so the split is
  no less recoverable than synchronized switches.
- Verify shell behavior through the internal binding and App behavior through
  the official binding.
- Share a narrow, secret-safe Plugin/Skill desired state while keeping runtime
  configs, plugin caches, credentials, and sessions independently owned.
- Make App-originated changes usable by the next functional internal CLI
  invocation and expose a safe explicit boundary for pending CLI-to-App apply.

**Non-Goals:**

- General custom-profile combinations or official CLI with internal App.
- Changing internal parity policy, proxy schemas, binary update policy,
  credentials, providers, models, or broad shared-config ownership outside the
  explicitly classified Plugin/Skill desired-state projection.
- Installing source, applying the split to this workstation, restarting
  ChatGPT, committing, pushing, releasing, archiving, or purging retained data.

## Architecture Decisions

### Decision 1: Explicit App override, synchronized default

The wrapper and Python switch command accept `--app-profile official` while the
positional profile remains the CLI target. Omission means the App target equals
the CLI target, preserving every existing command. The only new cross-profile
combination is internal CLI plus official App; other combinations fail before
planning mutations.

Using the positional profile as a generic single target plus
`--skip-app-cli` was rejected because skip means "do not manage," not "manage a
different owner." Making Desktop permanently official was rejected because it
removes supported internal Desktop behavior.

### Decision 2: One active-selection module is the identity seam

A new module owns profile alias normalization, requested-selection validation,
legacy active-record interpretation, explicit-field validation, and stable
selection errors. Its small interface returns immutable CLI/App identities;
transaction, status, Doctor, verify, and result presentation consume it.

Embedding the same fallback rules in each caller was rejected because partial
state would be interpreted differently. Extending `RuntimeBinding` to contain
two unrelated runtimes was rejected because its current interface assumes one
backend/home/Desktop chain and would make App-server smoke accidentally reuse
the internal backend.

### Decision 3: Compose two existing runtime bindings

For product profiles, callers resolve a CLI binding for the selected CLI
profile and an App binding for the selected App profile. CLI path/home checks
and runtime smokes consume the former; LaunchAgent/GUI/process attestation and
App-server smoke consume the latter. Same-profile selections may reuse one
resolved binding, but that is an implementation optimization rather than an
interface promise.

### Decision 4: Additive active record with strict mixed-schema handling

New records write `profile=<cli>`, `cli_profile=<cli>`, and
`app_profile=<app>`. A record with neither new field is legacy and maps both
surfaces to `profile`. A record with only one new field, an invalid identity, or
`profile != cli_profile` is malformed and fails closed. No eager migration is
needed; the next successful switch writes the new schema.

### Decision 5: Extend the existing transaction, not a post-switch patch

The switch planner freezes both selected manifests and resolved paths. It
prepares the CLI home/shim from the CLI target, the Desktop path/home from the
App target, and commits one active record after all effects succeed. Existing
journal rollback covers the shim, LaunchAgent, state, and home/config effects.
The explicit App target and `--skip-app-cli` are mutually exclusive.

A two-command sequence (`switch internal --skip-app-cli` followed by direct
LaunchAgent editing) was rejected because it has a failure window and no single
rollback receipt.

### Decision 6: Keep preparation and parity scoped to internal CLI

The one-key wrapper still checks/updates and repairs plugins for the positional
CLI profile. Internal parity remains a stored internal-generation requirement
for the managed shell shim, but live Desktop attestation uses the official App
binding. App-server smoke therefore executes the official bundle/home in split
mode.

### Decision 7: One neutral Plugin/Skill desired state, two rendered configs

The store owns a versioned shared-capability sidecar rather than treating
either runtime `config.toml` or either plugin cache as the permanent canonical
file. It contains only the secret-screened semantic projection of
`marketplaces.*`, `plugins.*`, and `skills.config`, a monotonic generation,
per-home last-applied baselines, source artifact identities, pending/conflict
state, and per-profile materialization receipts. Each runtime config keeps its
profile-local model/provider/auth/feature data and receives an authoritative
render of only that projection.

The official App projection is the explicit bootstrap authority for the
supported split because the user selected App-originated add/update as the
initial workflow. Once bootstrapped, both sides are compared with their common
baseline: a single-side change advances the desired generation, identical
changes coalesce, and divergent changes to the same desired snapshot fail
closed. No mtime or last-writer-wins rule is allowed.

Every fast-path receipt is evidence, not authority by itself. Before reporting
`cli_ready`, reconcile and diagnostics re-attest the referenced target cache,
manifest, tree digest, and contributed-Skill roots. A missing, corrupt, moved,
or escaped artifact makes the generation stale/blocked and causes a functional
preflight to repair through the target backend or fail before backend exec.

### Decision 8: Functional CLI preflight is the automatic lifecycle boundary

After internal Runtime Binding generation validation and before `os.execve`, a
functional internal CLI invocation acquires the store mutation lock, performs
a stable reconcile, renders the internal projection, independently
materializes every enabled plugin with the internal backend, verifies plugin
and contributed-Skill availability, writes a receipt, and only then executes
the user command. An unchanged committed generation takes a zero-write,
zero-network fast path. `--help` and `--version` retain read-only behavior.

The preflight also observes changes left by a prior CLI session. When the
official App/app-server is running, a CLI-originated change advances canonical
state as `pending_app_apply` but does not overwrite the live App config. A new
`sync-shared` command previews or applies that pending projection only after the
App is stopped. “Stopped” is fail-closed evidence from process enumeration: a
recognized Desktop host, any relevant app-server (including a mismatched
binding), or an unreadable process inventory blocks apply. The stopped proof
and target config identity are checked again after materialization and directly
before the first target write. This change intentionally preserves the shim's `os.execve`
process/TTY/signal/exit-status contract; supervisor postflight, an official App
wrapper, a watcher, and a daemon are rejected.

### Decision 9: Independent materialization uses explicit artifact policy

Plugin cache roots must be distinct, real directories with no cross-home
symlink. `portable_exact` local artifacts bind selector, source identity,
manifest version, and content-tree digest. `backend_managed` bundled or remote
artifacts share the logical selector and enabled state while allowing the
official and internal backends to materialize different compatible cache keys
or versions; the divergence is explicit in receipts. Native target-backend
installation runs only for a new generation that needs materialization, never
on the no-op path. That native operation owns its installed-version cache
lifecycle and may replace or remove prior versions. A backend-managed artifact
is accepted only when target
catalog/cache compatibility is inspectable; `uninspectable` is not a successful
receipt. Unavailable selectors, ambiguous active versions, unverified catalog
schemas, wrong digests, unsafe links, or a running target process fail before
backend launch. Multiple versions that remain present never silently downgrade a local
`portable_exact` identity to `backend_managed`; an active version must be
selected by a configured Plugin-Skill path or other deterministic attested
identity, otherwise reconciliation blocks.

Disable and remove update desired/runtime usage only and never invoke a native
plugin-remove operation. `codex-switch` never directly copies, links, deletes,
garbage-collects, or recreates Plugin cache artifacts. This boundary is not a
retention promise: a bounded native add/update may replace its backend's prior
installed versions, and only its fresh post-call catalog plus target
attestation can authorize a receipt.

### Decision 10: Standalone and plugin-contributed Skills have different owners

Personal standalone Skills use the official personal Skills directory as the
explicit canonical root; the internal home may reference it only through one
validated, non-circular directory link. An existing real or foreign-linked
internal Skills directory is a migration conflict and is not overwritten.
Project-local Skills remain owned by the shared repository worktree.
Plugin-contributed Skills remain inside each independently materialized plugin
cache; any configured plugin-cache path is rendered for the target home rather
than copied with the source-home absolute prefix. Both source classification
and target rendering resolve existing paths and reject `..`, absolute/relative
escape, special files, and symlink traversal outside the attested artifact and
target cache.

### Decision 11: Shared projection is secret-safe and narrow

The new canonical layer rejects credential-like marketplace fields and never
persists credential-bearing field values. URL-like source values reject
userinfo, credential-like query parameters, and fragments; nested source
descriptors receive the same value-level screening. It never contains auth
files, tokens, OAuth state, sessions, history, SQLite, logs,
browser/process state, model/provider/catalog/reasoning/personality, MCP/apps,
Desktop permissions/account/cloud/update state, or derived caches. Hook trust
remains profile-local until a separate digest-bound portability contract is
proved. The existing broad switch-time config merge is reviewed as a separate
safety finding; it is not silently reclassified or migrated here.

The configuration review classifies common UI/TUI/desktop preferences,
features/agents, MCP/apps/connectors, memory preferences, project roots, trust,
permissions, and automation state. None is added to canonical ownership without
a field-level compatibility and secret audit plus a separately approved
OpenSpec delta.

### Decision 12: Stable receipts are the diagnostic authority

Status, Doctor, and verify consume one read-only shared-capability report with
stable finding codes for generation, pending apply, conflict, materialization,
cache separation, and personal-Skill ownership. They do not independently
guess source direction or repair state. Dry-run and verify perform no writes,
catalog refresh, plugin install, cache replacement, or link creation.

### Decision 13: Shared publication has one recoverable commit point

Before changing a rendered config, personal-Skill link, generation artifact,
or state, reconcile writes and durably publishes one prepared journal under the
shared store. It binds the old state/generation, source and target config
identities, target file kind/bytes/mode, prior Skill-link state, planned
projection, target materialization receipts, immutable generation payload, and
expected committed-state digest. Materialization is re-attested, source and
target CAS identities are rechecked, and an official target receives a second
fail-closed stopped-App check before the first target write.

The prepared journal is non-canonical, machine-local recovery evidence. Exact
rollback requires it to retain the target config before/after bytes and mode,
so those private bytes may include profile-local values that are deliberately
excluded from the shared projection. The journal remains inside private
`0700` store directories as a `0600` file, is never materialized into the other
profile, and is removed after committed cleanup or successful rollback.
Canonical state and immutable generation artifacts remain secret-screened.

Rendered config/link effects precede an immutable collision-safe generation;
atomic publication of `state.json` is the only commit point. Terminal journal
cleanup happens only after the committed state is read back. On every later
apply, the store lock first classifies a prepared journal: if committed state
matches, it completes terminal cleanup; otherwise it restores only an expected
transaction-produced target/link state to the recorded predecessor. Foreign
post-crash edits block recovery rather than being overwritten. Orphan immutable
generations are retained and skipped by the next monotonic allocation, so an
interruption cannot create a permanent generation collision. Plan/report modes
remain read-only and report the pending recovery boundary.

### Decision 14: Backend materialization has a pre-call recovery intent

The target backend may persist a Plugin selector activation while materializing
its cache, so the main prepared-commit journal is not early enough by itself.
Immediately before any external target-backend materializer call, reconcile
rechecks target config CAS and, for an official target, performs a fail-closed
stopped-App proof. It then durably publishes a private
`pending-materialization.json` intent that binds the target path, exact
before-kind/bytes/mode, source and target profile identities, and the bounded
enabled selector set that the operation may activate. A main prepared-commit
journal and a materialization intent may not coexist.

On a synchronous return or failure, reconcile accepts only exact selector
activation deltas attributable to that bounded call. It restores the exact
pre-call bytes when those are the only changes. When an operation-owned
selector delta and foreign edits coexist, it removes only the selector delta,
preserves the foreign bytes and semantics, and blocks with target drift. A
foreign-only or unclassifiable change is preserved and blocks. The intent is
durably removed only after this classification and recovery completes.

If SIGKILL or power loss interrupts the backend, read-only modes expose the
pending recovery without writes. The next apply recovers the intent under the
store lock before loading state or planning new work, using the same selective
rules. Cache artifacts left by the interrupted backend are not trusted; their
continued presence or later replacement remains governed by the native backend
lifecycle, and normal materialization attestation decides whether a later retry
can use them. The ordinary post-materialization stopped-App and target CAS
checks still run before the main prepared commit.

### Decision 15: External materializers inherit the store mutation lease

The durable intent alone cannot prove that a backend process has stopped. If
the reconciling parent is killed after spawning `codex plugin add`, the backend
may remain alive and write the target config after an early recovery observes
the unchanged pre-call bytes. Every external command issued by the production
shared Plugin materializer therefore inherits the already-held store mutation
lock descriptor. The descriptor is validated against the exact locked store
root before dispatch and is passed only for this bounded materialization path.

On normal completion the command exits before reconcile releases the lock. If
the parent is killed, the surviving backend retains the same kernel lock lease;
a new apply fails closed as store-busy and cannot retire the materialization
intent while that backend is alive. After the backend exits, a later apply can
acquire the store lock and classify any late selector activation through
Decision 14. Read-only report/plan modes still perform no recovery write and
need not acquire the mutation lease. A real subprocess regression must prove
parent SIGKILL, backend survival, blocked early recovery with the intent still
present, late target write, backend exit, and selective recovery before a new
plan.

### Decision 16: Release promotion recognizes every exact supported manifest generation

Immutable promotion revalidates both the new candidate and the installed
`current`/`rollback` releases before replacing references. Adding selection and
shared-configuration modules expanded the latest required-path list from the
immediately prior 20-path generation to 22 paths. Historical validation
therefore owns an ordered collection of exact required-path tuples: the legacy
16-path generation and the immediately prior 20-path generation. It never
accepts a subset, superset, reordering, or arbitrary manifest merely because
every named file happens to exist.

The public installer regression must build a latest candidate, place exact
20-path releases behind both installed references, and prove successful
promotion plus byte-exact rollback retention. Existing malformed-manifest
tests remain the fail-closed guard. The trusted release-bundle hashes in both
bootstrap entrypoints advance with this validator change.

### Decision 17: The concise split command normalizes into the existing workflow

`codex-switch split` is an additive wrapper preset for
`internal --app-profile official`; it does not add a second switch planner,
transaction, verifier, or result path. All ordinary split options continue to
flow through `switch_profile internal`, and normal invocation retains the
existing wrapper self-update plus internal update-check/promotion behavior.

`--keep-version` is scoped to `split` and makes the controlled-version intent
explicit. Argument normalization recognizes it before wrapper self-update,
suppresses that update layer, and forwards the existing
`--skip-update-check` behavior to the internal workflow. It does not imply
`--skip-verify`, `--skip-plugin-repair`, `--skip-doctor`, or `--no-status`.
Other commands reject `--keep-version` rather than silently ignoring it.
Because the preset owns the official App target, it rejects any additional
`--app-profile` before self-update or planning instead of allowing option order
to retarget the shortcut.

An independent `split` implementation was rejected because it would duplicate
ordering and error handling. Making `split` silently freeze versions by default
was rejected because it would contradict the already accepted internal update
contract.

### Decision 18: Installed target version and portable source identity are separate axes

A target backend may report one selector only as an installed record. Its
reported `version` describes the observed target cache, even when the same
record resolves a local marketplace source whose manifest and tree have moved
forward. The materializer therefore uses backend-reported version as target
state, never as authority for a `portable_exact` source identity.

For `portable_exact`, the configured source path must still be absolute,
resolvable, contained, regular-directory based, manifest-matched to the
selector, and byte-attested against the desired cache key, manifest version,
and tree digest. If that source identity is exact while the installed target is
older, native target-backend add/update may run and the resulting independent
target artifact must then pass the same exact attestation before config or
canonical state commits. The older target cache is never selected as source
authority or directly mutated by `codex-switch`; the native operation may
retain, replace, or remove it according to its own lifecycle. A source identity
mismatch gets a dedicated materialization finding; `unsafe_cache` remains
reserved for paths, file kinds, links, or cache identities that are actually
unsafe.

Treating the older installed version as the available source version was
rejected because it blocks the required same-selector App update. Copying the
official cache was rejected because it violates independent backend ownership.
Trusting the marketplace path without manifest/tree attestation was rejected
because local-source drift would become an unverified install authority.

### Decision 19: Functional preflight reports bounded progress without moving the lifecycle boundary

The next functional managed internal CLI invocation remains the automatic
bootstrap and reconciliation boundary. Before potentially expensive source
attestation it writes one flushed progress line to stderr; when a plan requires
materialization it reports the target profile and enabled Plugin count before
the target catalog/backend phase. Findings and exit behavior remain unchanged,
and help/version stay read-only. A committed unchanged generation retains its
zero-write and zero-network contract; progress is observational and does not
authorize repair, refresh, or cleanup.

Moving materialization into the split transaction was rejected for this repair
because backend cache/config effects have their own intent and lease lifecycle
and cannot be made part of the existing switch rollback without a broader
transaction redesign. Silent first-use work was rejected because a cold source
attestation plus catalog query can otherwise look like a hung CLI.

### Decision 20: Backend-managed source proof and target proof are independent

The catalog adapter preserves two identities for each selector instead of
merging them into one overloaded version. Source identity comes from the
available marketplace record and is attested against the desired manifest and
tree. Target identity comes only from a unique installed record, including an
installed-envelope hint when the record omits an explicit flag. When installed
and available collections both expose a selector, installed provenance and
target version cannot be overwritten by collection order, while a safe source
path from either record can still support source attestation.

For every pending `backend_managed` selector in a changed generation, the
materializer runs the target backend's native add/update even when an older
target cache is inspectable. The native operation may replace that prior
installed version. The materializer then obtains one fresh verified
catalog for the whole backend-managed batch. Each selector must now be uniquely
reported installed, and its independent target cache must be contained,
non-symlinked, structurally inspectable, selector-matched, and Skill-root safe.
The installed cache key and plugin manifest version are recorded separately;
revision-like cache keys remain compatible and are not required to equal the
manifest version. The pre-call catalog, the official source tree, and an
unreconciled pre-call target cannot substitute for this post-call proof.

Catalog command/schema failure remains `unverified_catalog`. A safe but absent
or ambiguous installed record, missing target artifact, or unprovable target
manifest/tree is `unverified_target`. Desired source identity drift is
`source_mismatch`. Path containment, symlink, traversal, and non-regular
file-kind violations remain `unsafe_cache`; native command failure remains
`failed`. Directly copying, linking, deleting, or comparing official and
internal trees in `codex-switch` was rejected because backend-managed
compatibility intentionally permits their bytes and versions to diverge. This
does not constrain replacement or removal performed internally by the native
backend command itself.

### Decision 21: Managed runtime rendering is byte-idempotent

The runtime renderer may reuse the previous managed runtime as the
profile-specific seed, but generated `# codex-switch:` section annotations are
presentation metadata rather than seed-owned TOML trivia. Before re-annotation,
removing a managed annotation also removes only the contiguous blank lines
immediately preceding that annotation. User comments and blank lines that are
not adjacent to a managed annotation remain unchanged.

After the previous managed runtime becomes the selected seed, rendering the
same profile and shared inputs repeatedly must produce byte-identical output.
The initial canonical-to-last-runtime source annotation transition remains
allowed. This prevents the profile-provider block from absorbing an old
managed shared-section marker and growing one blank line per switch. Global
whitespace compaction was rejected because it would rewrite unrelated user
formatting; changing TOML semantics or profile/shared ownership is outside this
repair.

### Decision 22: Release reconciliation owns exact zero-byte starter recovery

GitHub can retain a failed release upload as a same-name asset in `starter`
state while the normal release view exposes no downloadable custom asset. The
release adapter therefore inventories assets from the release-assets endpoint,
retaining each asset's ID, name, state, and size rather than deriving authority
from the embedded uploaded-asset list alone.

Reconciliation treats a canonical name as recoverable only when exactly one
record has `state=starter` and `size=0`. Immediately before deleting that exact
asset ID it rechecks the remote tag identity. It then reads the inventory back,
uploads only if the canonical name is still absent, and performs the existing
download/hash verification. An uploaded asset is never deleted; non-zero
starter records, duplicate names, unsupported states, or readback drift fail
closed. `--clobber` remains prohibited because it cannot distinguish an empty
failed upload from a valid conflicting artifact.

Auto Release run `31500533015` exposed a second state transition after the
first repair was submitted: the reconcile step failed after the exact starter
deletion path, and the release was no longer addressable through the available
tag-based readback. The complete authenticated command log is unavailable, so
the disappearance branch is the leading evidence-backed hypothesis rather than
a claimed verbatim remote error.

Reconciliation therefore treats a missing post-delete readback as recoverable
only after a fresh tag-identity check. It creates one draft release through the
existing verified-tag adapter, immediately reads it back, and requires an
existing, empty, draft snapshot before any upload. Creation failure, missing
readback, a published or non-empty readback, and tag movement all fail closed
before later mutations. Successful recovery then follows the unchanged
canonical upload, download/hash, publish, final readback, and final checksum
proof. The same readback rule applies when reconciliation begins with no
Release record.

Each exact starter deletion is followed by its own readback. If more than one
canonical starter was observed and the first deletion removes the Release,
reconciliation stops using every remaining asset ID from the vanished Release,
records those names as recovered, and enters the same empty-draft recreation
path. If the Release remains, any changed replacement starter record fails
closed before deletion; an unchanged remaining starter may proceed through the
next tag-check/delete/readback iteration.

## Completion Contract

- The named split command has a failing-then-passing wrapper and transaction
  regression.
- The concise `split` preset and split-scoped `--keep-version` option have
  failing-then-passing wrapper, help, normal-update, frozen-update, and dry-run
  regressions without a duplicated orchestration path.
- New and legacy active-state parsing, partial/conflicting-state rejection, and
  unsupported/contradictory request rejection are covered.
- A successful isolated split proves internal shim/home plus official
  LaunchAgent/App path; injected Desktop failure proves complete rollback.
- Status, Doctor, and verify agree on CLI/App identities and detect drift on
  the correct surface.
- Existing synchronized switch, internal parity, transaction, verifier, and
  release-bundle suites remain green.
- A release whose uploaded asset view is empty but whose explicit inventory
  contains a canonical zero-byte `starter` asset is repaired by exact-ID
  deletion, readback, upload, and hash verification without clobbering any
  uploaded or ambiguous asset. If the post-delete Release readback is missing,
  the tag is revalidated and one empty draft is created and read back before
  the same upload, publish, and checksum proof.
- A latest package can promote over the exact immediately prior 20-path
  manifest generation while preserving it as rollback; unknown required-path
  lists remain rejected before reference mutation.
- Strict OpenSpec, workflow validation, Bash/Python static checks,
  plugin-eval for the changed skill, isolated packaging, and diff checks pass.
- No live profile switch, App stop/restart/mutation, internal binary update,
  install, Git, release, archive, dependency, credential, standalone cache
  cleanup, or direct codex-switch cache copy/link/delete occurs; final
  acceptance may run the separately confirmed single functional managed
  internal CLI command, including backend-owned replacement of prior installed
  Plugin versions.
- App add/update/enable/disable/remove advances one desired generation and the
  next functional internal CLI invocation either completes independent
  materialization before backend execution or fails with a stable finding and
  leaves last-known-good usage active.
- A stale installed `portable_exact` version cannot override an exact current
  marketplace source identity; native target update plus post-add attestation
  has public-seam RED/GREEN coverage, and a real source mismatch is reported
  distinctly from an unsafe cache.
- A backend-managed official source version may differ from the internal
  installed target version; a changed generation always reconciles through the
  target backend and commits only after one fresh batch catalog plus independent
  target-cache attestation proves every selector installed and usable.
- A non-current functional preflight emits flushed progress before source
  attestation and again before materialization, while help/version and the
  committed zero-write/zero-network path retain their existing contracts.
- CLI-originated projection changes are captured at the next preflight; a live
  official App receives a pending marker, and stopped-App `sync-shared`
  preview/apply has zero-write and verified-apply regressions.
- Single-side, identical, divergent, delete-vs-modify, unstable-source, and
  crash/recovery/rollback cases are covered without last-writer-wins, including
  every persistent commit boundary, target CAS, and second stopped-App proof.
- Personal, plugin-contributed, and project-local Skill ownership plus
  plugin-cache separation/path remapping/traversal rejection are covered.
- Secret/profile/runtime exclusions and the reviewed classification of other
  configuration surfaces are recorded and tested at the canonical boundary,
  including credential-bearing URL values.

## Critical Path

Selection identity contract -> transaction RED/GREEN -> shared desired-state
RED/GREEN -> independent materialization RED/GREEN -> lifecycle and shared
diagnostics RED/GREEN -> wrapper/docs/package integration -> concise preset
RED/GREEN -> installed/source identity repair RED/GREEN -> preflight progress
RED/GREEN -> backend-managed catalog provenance and post-reconcile proof
RED/GREEN -> one functional managed-CLI acceptance -> focused and broad
completion proof.

## Incidental Finding Budget

One bounded RED/GREEN guard is allowed only when a discovered issue blocks the
specified split state inside the approved write set. Non-blocking findings are
`DEFER_AND_CONTINUE` and enter the tracked `TASK_LEDGER.md` register. Unknown
severity, new profile combinations, live effects, or parity/proxy policy
changes are `BLOCKED_AWAITING_HUMAN`.

## Escalation Triggers

Stop and update the change before adding a dependency, changing credentials or
public persistence beyond the additive active fields and shared-capability
sidecar specified here, supporting another profile
combination, changing internal parity/proxy/update behavior, expanding beyond
the named write set, or requiring a real install/switch/restart. Git, release,
archive, cleanup, and any destructive action remain separate Human Gates.

## Capability Slices

1. Active selection and state compatibility: pure selection interface, record
   fields, parser validation, and RED/GREEN tests.
2. Transactional split: frozen two-target planning, atomic commit/rollback,
   dry-run, and transaction/profile regressions.
3. Diagnostics and verification: split-aware status, Doctor, runtime/parity
   verification, and drift/smoke regressions.
4. Wrapper and distribution: one-key forwarding/result output, README/SKILL,
   package allowlist, packaged preview, and release-adjacent checks.
5. Integrated proof: fresh focused/broad/static/spec/workflow/plugin-eval/
   package/diff evidence and canonical state reconciliation.
6. Shared desired state: semantic projection, generation/baseline persistence,
   conflict/pending rules, secret guard, and personal-Skill ownership.
7. Independent materialization: artifact policy/inventory, conditional native
   repair, target cache/path verification, and rollback-safe config commit.
8. Lifecycle and diagnostics: internal CLI preflight, explicit `sync-shared`,
   shared status/Doctor/verify report, docs, and release packaging.
9. Reopened completion proof: fresh source matrices, Plugin Eval, independent
   review, config-policy matrix, and durable state reconciliation.
10. Concise split preset: wrapper-only normalization, split-scoped version
    freeze, help/docs/package coverage, immutable local installation, and
    non-mutating installed verification.
11. Live-bootstrap repair: stale-installed/current-source `portable_exact`
    interpretation, precise findings, functional-preflight progress, focused
    and broad source-only proof.
12. Backend-managed live acceptance repair: installed-versus-available catalog
    provenance, exact source proof independent from target version, batched
    native reconcile with fresh target proof, precise findings, and one managed
    internal CLI acceptance while the official App remains running.
13. Failed release-upload recovery: explicit asset-state inventory, exact
    zero-byte starter deletion, missing-Release draft recreation with immediate
    readback, canonical upload, checksum proof, and no live external effect
    during source verification.

## Execution Ledger

| Slice | Owner | Write Set | Evidence | Human Gate | Status |
|---|---|---|---|---|---|
| Selection/state | main, serialized | selection/record/parser plus focused tests | named RED/GREEN and legacy/error matrix | public state expansion beyond additive fields | complete; 8 adjacent binding/state tests passed |
| Transaction | main, serialized | switching/transaction plus focused tests | dry-run, commit, drift, rollback | live switch | complete; 241 transaction tests GREEN |
| Diagnostics | main, serialized | status/Doctor/verify plus focused tests | healthy split and per-surface negative matrix | parity/proxy policy change | complete; focused diagnostics and 33 verifier tests GREEN |
| Wrapper/package | main, serialized | wrapper, README, SKILL, release bundle/test | wrapper test, plugin-eval, isolated package preview | install/release | complete; update/release 133/133, verified packaged preview, source/package identity, and Plugin Eval recorded |
| Completion proof | main | this change, ledger, namespaced state, verification record | all validation commands and scope review | commit/push/archive | complete; 362 combined, profile 210, update/release 133, parity 95, strict/static/workflow/package/diff and review green |
| Shared desired state | main, serialized | shared-capability/config modules, focused unit tests, OpenSpec/control plane | generation/three-way/secret/Skill/materializer-crash RED-GREEN matrix | persistence/schema expansion beyond this additive sidecar | in progress |
| Independent materialization | main, serialized | plugin materialization seam and focused tests | add/update/remove, exact/backend-managed, cache isolation, rollback matrix | live plugin/cache mutation | pending |
| Lifecycle/diagnostics/package | main, serialized | runtime preflight, CLI parser, status/Doctor/verify, wrapper/docs/skill/package/tests | backend-not-called failures, pending apply, package identity | supervisor/watcher/App wrapper/install | pending |
| Reopened completion proof | main | tasks, ledger, state, verification record | fresh full/static/spec/workflow/plugin-eval/package/diff/review evidence | commit/push/archive | pending |
| Concise split preset | main, serialized | wrapper, wrapper tests, README, SKILL, package/control-plane evidence | RED/GREEN routing, update preservation/freeze, help, packaged and installed checks | live split/App stop/internal upgrade | pending; approved 2026-08-10 |
| Live-bootstrap repair | main, serialized | shared materializer/preflight, focused tests, README/SKILL, OpenSpec/control plane | stale-installed/current-source RED/GREEN, exact post-add attestation, progress capture, focused/broad/static/spec evidence | live cache mutation, install, split retry | approved; task 12.1 is next |
| Backend-managed acceptance repair | main, serialized | catalog adapter, shared materializer, focused tests, README/SKILL, OpenSpec/control plane | live-shape source/target divergence RED/GREEN, installed precedence, native cache-lifecycle replacement, one post-add batch catalog, precise findings, full/static/spec/package review, functional managed-shim acceptance | split/install/App stop or mutation/internal binary update/direct codex-switch cache mutation/Git/release/archive | complete 2026-08-11; tasks 13.1-13.4 verified and native cache-lifecycle decision reconciled |
| Runtime-config render idempotence | main, serialized | managed annotation cleanup and focused config/profile tests plus OpenSpec/control-plane evidence | repeated-render RED/GREEN, focused and adjacent suites, strict/static/diff proof | live config rewrite, switch/install/App action, dependency/Git/release/archive/cleanup | complete 2026-08-11; tasks 14.1-14.3 verified |
| Failed release-upload recovery | main, serialized | release adapter/reconciler, focused update-release tests, OpenSpec/control plane | hidden starter, disappearing Release, and stale multi-starter ID RED; per-delete readback/recreate/upload GREEN; conflict guards and full proof | live GitHub release mutation, workflow rerun, dependency/migration, commit/push/archive | complete in source 2026-08-11; tasks 15.1-15.6 verified, second submit awaits Human Gate |

## Continuation Policy

Execution policy is `auto-until-terminal`; `tasks.md` is the only execution
source. After each completed item, select the next dependency-ready item and
continue for `CONTINUE_NEXT_ITEM`, `CHECKPOINT_AND_CONTINUE`, or
`VERIFY_ACTIVE_CHANGE`. Stop only for an escalation trigger, live/external
effect, or missing authority. Implementation was requested explicitly, so
source/test/docs/control-plane work in this contract is approved; the Human
Gates above remain excluded.

The user's 2026-08-10 confirmation additionally authorizes immutable local
installation of the shortcut-bearing package and non-mutating installed
help/preview checks. It does not authorize stopping or restarting the App,
activating the live split, updating the internal binary, repairing parity,
release, archive, Git effects, cleanup, or destructive work.

The user's later 2026-08-10 live-bootstrap repair confirmation authorizes the
task 12 source, test, README/SKILL, OpenSpec, ledger, namespaced-state, and
verification-record write set only. It does not authorize another install,
live Plugin/cache mutation, functional `codex` retry, split retry, App
stop/restart, internal update, project migration, Git, release, archive, or
cleanup.

The user's 2026-08-11 systemic-repair confirmation additionally authorizes
task 13 source, test, README/SKILL, OpenSpec, ledger, namespaced-state, and
verification-record changes plus one functional command through the currently
managed internal CLI shim. That command may perform the bounded internal
backend Plugin add/update operations, profile-local config restoration, target
cache writes owned by that backend, and shared-generation/receipt writes needed
to prove successful CLI startup while the official App remains running,
including native replacement or removal of prior installed versions. It does
not authorize a split retry, another install, App stop/restart/mutation,
internal binary update, standalone cache cleanup, direct codex-switch cache
copy/link/delete, project migration,
dependency change, Git, release, archive, credential, or destructive effect.

## Generated Artifact Strategy

No persistent disposable output is introduced. Tests and package validation
use isolated temporary roots owned and removed by existing test/process
lifecycles. Any unexpected repository or workstation residue is retained and
classified; it is never auto-deleted from a filename or directory heuristic.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_runtime_binding \
  scripts.test_codex_transaction \
  scripts.test_codex_verify
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_wrapper_split_shortcut_routes_supported_pairing \
  CodexProfileSwitchTests.test_wrapper_split_keep_version_skips_internal_update_check \
  CodexProfileSwitchTests.test_local_wrapper_split_keep_version_skips_self_update_and_retains_workflow
python3 scripts/test_codex_profile_switch.py
python3 scripts/test_codex_update_release.py
python3 -m unittest \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_recovers_hidden_zero_byte_starter_asset \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_rejects_nonempty_starter_asset \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_rejects_unsupported_hidden_asset_state \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_reconcile_rechecks_tag_identity_before_starter_delete \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_github_release_inspection_lists_starter_assets \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_github_release_inspection_rejects_duplicate_asset_names \
  scripts.test_codex_update_release.CodexReleasePlannerTests.test_github_release_delete_uses_exact_asset_id
python3 scripts/test_codex_shared_configuration.py
python3 scripts/test_codex_shared_materialization.py
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_runtime_binding
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
openspec validate independent-app-cli-profiles --strict --no-interactive
openspec validate --all --strict --no-interactive
python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py --repo . --json
node /Users/cY/.codex/plugins/cache/openai-curated-remote/plugin-eval/0.1.2/scripts/plugin-eval.js \
  analyze "${CODEX_SWITCH_RELEASE_ROOT:?}/codex-switch/SKILL.md" \
  --format markdown
git diff --check
```

An isolated package build must additionally prove the new required module is
present and a packaged split dry-run imports no checkout code.

## Risks / Rollback

- [Legacy readers ignore new fields] -> retain `profile` as the CLI identity
  and keep old synchronized semantics for readers that know only that field.
- [A composed binding uses the wrong home] -> keep separate CLI/App binding
  values through verification and add command-log home assertions.
- [Transaction writes one target before detecting other-target drift] -> freeze
  both target inputs and use the existing journal rollback path.
- [Internal parity incorrectly treats official live App as drift] -> evaluate
  stored internal parity from the CLI binding and live App attestation from the
  App binding; add negative tests for cross-wiring.
- [Unrelated dirty work is overwritten] -> edit only explicit paths, inspect
  every diff, and compare the pre-existing parity/provider-migration paths
  before the completion claim.
- [Official App writes outside the store lock] -> stable double observation,
  content fingerprints, commit-time compare-and-swap, and pending rather than
  live-App overwrite.
- [Different backends expose different plugin builds] -> explicit
  `portable_exact` versus `backend_managed` policy and per-profile receipts;
  never infer parity from one version string.
- [Automatic repair makes every CLI start slow or network-dependent] -> only a
  changed generation can invoke materialization; exact receipt match is a
  zero-write and zero-network fast path.
- [A failed installer leaves desired config active without its artifact] ->
  stage/backup the target projection, verify materialization before canonical
  receipt commit, restore last-known-good config on failure, and treat any
  backend-left cache artifact as untrusted without direct cleanup.
- [Shared config leaks credentials] -> canonical table allowlist plus
  credential-like field rejection; credentials and unreviewed tables remain
  profile-local.
- [A shortcut silently changes update semantics] -> normalize `split` into the
  existing internal workflow, prove normal update dispatch remains intact, and
  require explicit split-scoped `--keep-version` to suppress both update
  layers.
- [A backend-reported installed version is mistaken for current portable
  source identity] -> attest the resolved source manifest/tree independently,
  use the reported version only as target state, and require exact target
  post-add attestation before commit.
- [Cold bootstrap looks hung while hashing artifacts or reading the target
  catalog] -> emit bounded flushed stderr progress at the functional preflight
  and materialization boundaries without weakening the unchanged-generation
  no-write/no-network contract.
- [A backend-managed source version is mistaken for the internal target
  version] -> preserve installed and available provenance independently, attest
  desired source before mutation, always reconcile a changed generation through
  the target backend, and require one fresh post-call catalog plus independent
  target artifact proof before receipt commit.
- [A failed upload reserves a canonical release name invisibly] -> inventory
  release assets with state and ID, delete only an exact zero-byte `starter`
  record after tag validation, read back after every deletion, stop using stale
  IDs if the Release disappears, recreate and read back one empty draft, and
  retain no-clobber checksum conflict behavior for every uploaded or ambiguous
  record.

Rollback for source work is the inverse scoped patch. Runtime rollback is
tested only in isolated roots; no live rollback is needed because no live
switch is authorized.

## Review Checklist

- Every delta scenario maps to a test and task.
- The selection interface is the only legacy/new identity parser.
- Same-profile behavior and custom-profile compatibility do not regress.
- Shell and App homes/binaries are never inferred from each other in split
  mode.
- Failures restore the prior active record, shim, and Desktop binding.
- Documentation, skill, and packaged behavior match the public interface.
- No unrelated parity/provider-migration bytes or external state changed.

## Final Verification

Run the validation commands fresh after the last source/doc edit, review the
exact write set and residual risks, update the verification record, ledger, and
namespaced state, then run exactly one functional non-interactive command through
the current managed internal CLI shim while the official App remains running.
Prove exit zero, committed shared generation and per-selector receipts, internal
backend dispatch, target-cache safety, and unchanged App binding/process state.
The earlier shortcut task retains its historical installation evidence, and
this repair performs no new installation. Archive, commit, push, split retry,
App stop/restart/mutation, internal binary update, parity repair, release, cache
cleanup or direct codex-switch copy/link/delete, migration, and dependency
changes remain unperformed. The already-observed native replacement of prior
installed Plugin versions is recorded as backend-owned lifecycle behavior.
Task 15 additionally performs no live GitHub release mutation or workflow
rerun; those remain external-effect gates after source verification.
