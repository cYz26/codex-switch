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
  supported pairing. Normal `split` retains the existing codex-switch
  self-update and internal update-check behavior; `split --keep-version`
  freezes both update layers for a controlled activation while leaving switch,
  Plugin repair, verify, Doctor, and status behavior intact.
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
- Add an explicit shared-capability sync command for safely applying pending
  CLI-originated Plugin/Skill changes to the official App home when the App is
  stopped. Divergent edits fail closed rather than using last-writer-wins.
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
  validation, read back the release, then upload and hash the canonical bytes.
  Uploaded, non-zero, duplicate, or unknown-state assets remain fail closed and
  are never clobbered.
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

- Public CLI: additive `--app-profile` switch option plus `split` and its
  split-scoped `--keep-version` convenience option on the one-key wrapper.
- State: additive `cli_profile` and `app_profile` fields in `active.json`; old
  records without them remain readable as same-profile selections.
- Runtime code: active-selection resolution, transactional switching, status,
  Doctor, verify, wrapper result presentation, shared-capability reconciliation,
  independent plugin materialization, installed/source version interpretation,
  post-reconcile target catalog attestation, functional-preflight progress
  reporting, idempotent managed runtime-config annotation, and state-aware
  release-asset reconciliation.
- Shared state: additive store-owned desired generation and per-profile
  materialization receipts plus one store-owned prepared-commit recovery
  journal. Runtime `config.toml` files remain rendered views, not a shared
  mutable file, physical plugin caches remain profile-local, and their
  installed-version lifecycle remains backend-owned.
- Verification and distribution: focused Python/Bash tests, README and skill
  instructions, release allowlist/package identity, strict OpenSpec, workflow,
  static, and plugin-eval checks.
- No new dependency, credential migration, live profile/App switch, App
  restart, install, release, archive, commit, push, standalone cache cleanup,
  or direct codex-switch cache mutation is authorized by this change. A
  separately confirmed acceptance task may run one functional managed internal
  CLI command and its required profile-local native Plugin materialization,
  including backend-owned replacement of prior installed versions, while the
  official App remains running.
