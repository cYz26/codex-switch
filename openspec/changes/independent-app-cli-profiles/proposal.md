## Why

`codex-switch` currently treats the shell CLI and ChatGPT Desktop as one active
profile. `--skip-app-cli` can leave Desktop untouched for one transaction, but
the active record, status, Doctor, and verifier still expect both surfaces to
use the same profile, so the requested "internal CLI + official App" state is
accidental and cannot be managed or reported as healthy.

## What Changes

- Add an explicit App-profile override to profile switching so
  `codex-switch internal --app-profile official` selects the managed internal
  binary/home for shell `codex` while binding ChatGPT Desktop to the verified
  official bundled binary/home.
- Add `codex-switch split` as the concise, additive preset for that exact
  supported pairing. A real `split` apply retains the existing codex-switch
  self-update and internal update-check behavior on real apply;
  `split --dry-run` and the equivalent long-form preview skip self-update so
  preview remains zero-write and zero-network. `split --keep-version`
  freezes both update layers for a controlled activation. After a real split
  switch commits, the wrapper proactively runs the same Official-to-internal
  shared readiness apply used by functional CLI preflight before Plugin repair,
  verify, Doctor, or status; split preview remains zero-write and names that
  pending readiness step.
- Persist separate CLI and App profile identities in `active.json` while
  retaining the existing `profile` field as a backward-compatible CLI-profile
  alias.
- Make switch planning/commit, status, Doctor, and verify resolve both active
  targets from one canonical selection module and fail closed on partial,
  contradictory, or drifted state.
- Keep existing `codex-switch internal` and `codex-switch official` behavior
  unchanged when no App-profile override is supplied.
- Document and package the split-profile command and add transaction,
  diagnostics, wrapper, compatibility, and release-bundle regressions.
- Add a secret-safe, generationed Plugin/Skill desired-state layer for the
  supported internal-CLI/official-App split. The official App and managed
  internal CLI keep separate runtime homes and plugin caches, while functional
  internal CLI invocations reconcile App changes before backend execution and
  materialize the internal cache with the internal backend.
- Make the official App the sole authority for the supported shared
  Plugin/Skill projection and treat the internal CLI as a derived target.
  A successful split apply and every later functional internal CLI preflight
  automatically repair safe Official-only, internal-only, disjoint,
  overlapping, disable, and removal drift without writing the official App;
  unrelated internal configuration remains local.
- Keep an explicit `sync-shared` preview/apply command for the same
  Official-to-internal reconciliation, and make unsafe failures actionable
  without a background watcher: status, Doctor, verify, preflight, and explicit
  sync report secret-safe changed operations, stable causes, readiness, and
  exact preview/apply/Doctor remediation. No prompt or manual source-selection
  command is exposed.
- Make shared projection publication crash-recoverable: bind source and target
  identities in a prepared journal, re-prove target/App/cache state before the
  first write, publish state as the only commit point, and recover an
  interrupted prepared commit under the store lock before any later apply.
- Correct functional CLI bootstrap when a target backend reports an older
  installed `portable_exact` version while its attested marketplace source has
  already advanced. Installed target state no longer overrides source
  artifact identity, real cache hazards remain fail-closed, and potentially
  slow first-generation preflight exposes bounded progress instead of appearing
  hung.
- Correct the corresponding `backend_managed` bootstrap boundary: a current
  official marketplace source and an older compatible internal target version
  are independent identities. A changed generation reconciles through the
  internal backend, then requires a fresh installed catalog record plus exact
  target-cache attestation before the functional CLI executes.
- Assign each profile-local installed Plugin cache lifecycle to its native
  backend. `codex-switch` never directly copies, links, deletes, or garbage-
  collects Plugin cache artifacts, while a bounded native add/update may
  replace its own prior installed versions; only the freshly attested target
  can authorize a materialization receipt.
- Make managed runtime-config rendering byte-idempotent when the prior managed
  runtime is reused as the profile seed. Consecutive last-runtime renders with
  unchanged profile and shared inputs must not accumulate blank lines or
  managed annotation trivia.
- Make release reconciliation recover GitHub's exact failed-upload residue:
  when a required name is absent from the uploaded asset view but reserved by
  one zero-byte `starter` asset, delete only that asset ID after tag-identity
  validation, read back after each deletion, then upload and hash the canonical
  bytes without reusing stale asset IDs.
  If deleting the residue makes the release unaddressable, revalidate the tag,
  recreate one empty draft release, read that draft back, and continue through
  the same no-clobber upload, publish, and checksum proof. Uploaded, non-zero,
  duplicate, unknown-state, or non-empty recreated states remain fail closed.
  Draft recreation tolerates only typed, bounded GitHub propagation failures:
  exact `Release.tag_name already exists`, server/transport failure, or delayed
  post-success visibility. Every create retry revalidates the tag and missing
  Release, a successful create receives readback-only retries, and permission,
  rate-limit, unknown validation, or conflicting state still fails immediately.
- Review every other known configuration surface and classify its target
  ownership. This change implements only Plugin/Skill desired state and the
  bounded safety guards it requires; credentials, sessions, broad TOML state,
  App permissions, runtime caches, and unrelated migrations remain outside the
  shared layer.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: Profile switching can persist, attest, and report distinct
  CLI and ChatGPT Desktop profile selections, including internal CLI with the
  official Desktop bundle.

## Impact

- Public CLI: additive `--app-profile` switch option plus `split`, its
  split-scoped `--keep-version` convenience option, and `sync-shared` preview/
  apply for explicit Official-to-internal readiness repair.
- State: additive `cli_profile` and `app_profile` fields in `active.json`; old
  records without them remain readable as same-profile selections.
- Runtime code: active-selection resolution, transactional switching, status,
  Doctor, verify, wrapper result presentation and post-switch readiness
  ordering, shared-capability reconciliation, independent plugin
  materialization, installed/source version interpretation, post-reconcile
  target catalog attestation, functional-preflight progress reporting,
  idempotent managed runtime-config annotation, and state-aware release-asset
  reconciliation.
- Shared state: additive store-owned desired generation and per-profile
  materialization receipts plus one store-owned prepared-commit recovery
  journal. Per-profile baselines retain only secret-safe projection evidence
  needed for drift reporting and legacy-state migration; the current official
  observation is always the source for a new generation. Runtime `config.toml`
  files remain rendered views, not a shared mutable file, physical plugin
  caches remain profile-local, and their installed-version lifecycle remains
  backend-owned.
- Verification and distribution: focused Python/Bash tests, README and skill
  instructions, release allowlist/package identity, strict OpenSpec, workflow,
  static, and plugin-eval checks.
- No new dependency, credential migration, live profile/App switch, App
  restart, install, archive, standalone cache cleanup, direct codex-switch cache
  mutation, reverse sync, background watcher/daemon, source-choice prompt, or
  unrelated migration is authorized by this change. A separately
  confirmed acceptance task may run one functional managed internal CLI command
  and its required profile-local native Plugin materialization, including
  backend-owned replacement of prior installed versions, while the official App
  remains running. The 2026-08-12 task-16 grant separately authorizes the
  bounded release-recreation source repair, its commit/push to `origin/main`,
  the push-triggered `v0.1.14` recovery, and the planned atomic `v0.1.15`
  tag/Release publication.
