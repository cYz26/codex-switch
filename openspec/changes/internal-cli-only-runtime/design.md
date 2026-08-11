## Context

See `proposal.md` for motivation and
`specs/codex-switch/spec.md` for observable behavior. The current staged-update
path always delegates to the full internal Runtime Binding rebind. That path
generates a Desktop launcher, app-server capability receipt, parity overlay,
parity receipt, projected configs, and then executes an internal app-server
handshake before swapping the candidate into the stable internal bin path.

The supported `split` state has two independent owners: the stable internal
path and internal home own shell CLI execution, while the verified ChatGPT.app
bundle and official home own Codex App. The App may be running during a split
CLI update. The existing schema-v3 rebind journal already provides the correct
CAS, rollback, durable marker, and executable-swap primitives, but it currently
requires the complete Desktop artifact set.

The worktree contains unrelated and prior approved work. This change uses a
narrow write set and does not rewrite the paused
`internal-official-feature-parity` change or claim its Desktop acceptance.

Post-implementation operator acceptance exposed two gaps in the original
completion proof. A valid 276,128,448-byte internal backend was rejected by the
managed shim because the 16 MiB text-artifact limit was also used while hashing
the executable. The final runtime smoke bypassed that shim and invoked the raw
backend, so the wrapper incorrectly reported success. The same acceptance also
showed that unconditional `Restart ChatGPT` guidance is false when the split
transaction reports `App action: preserve`. These are required-contract
failures, so the earlier 19/19 completion claim is reopened rather than treated
as an incidental follow-up.

## Skill Routing Ledger

- artifact-status: final; the accepted repair has no Open Questions
- capability-research: required / used; local wrapper, staged updater, Runtime
  Binding, transaction recovery, selection, shell entrypoint, diagnostics, and
  regression seams were inspected
- decision-resolution: required / used; the user explicitly selected internal
  CLI-only support and deferred internal App compatibility
- decision-grilling: skipped; the runtime ownership decision is explicit
- implementation-planning: required / used; this design and `tasks.md` own the
  execution contract
- architecture-guidance: required / used; one generation marker separates CLI
  readiness from App readiness while the existing transaction remains the
  atomic mutation owner
- domain-language-modeling: skipped; CLI generation, App readiness, profile,
  binding, and parity are sufficient existing terms
- openspec-routing: required / used; behavior, compatibility, error handling,
  and rollback are specified in this independent Full OpenSpec change
- test-first-execution: required / used and reopened; repair slices begin at the
  managed shell, CLI-only promotion, verifier, and wrapper-output seams
- root-cause-diagnosis: required / used; the original split failure was caused
  by routing through Desktop parity, while the live acceptance failure is the
  combination of a text-artifact size limit on executable hashing and verifier
  bypass of the managed shell generation guard
- change-review: required / pending after implementation
- completion-proof: required / pending; source verification cannot claim live
  promotion or installed activation
- execution-orchestration: required / used; `tasks.md` is the sole execution
  source for this change

## Target State and Scope / Non-Goals

`codex-switch split` continues to perform ordered internal update detection,
but promotes a selected candidate under a CLI-only generation contract. The
candidate must be an exact executable/version match, the stable bin and
manifest change atomically, and the managed shell path must validate the
recorded binary digest before execution. Executable identity is captured with a
stable streaming read and an executable-specific safety bound; it is never
loaded through the bounded text-artifact reader or buffered as one payload.
Existing shared Plugin/Skill preflight continues to protect functional CLI
commands.

Internal App protocol parity, proxy conversion, model aliases, Desktop wrapper
generation, App-server schemas, and App smoke are not acceptance criteria for
that promotion. Codex App remains official and does not need to exit. A future
request to bind App to that internal generation fails before mutation until an
explicit full-parity rebind succeeds.

Non-goals are changing the public meaning of direct `update-internal` or
`set-bin internal`, removing the historical full-parity path, making internal
App work with the newly promoted binary, relaxing Plugin/Skill preflight,
provider/model/auth traffic, installing this source, applying a live switch,
restarting App, release, archive, commit, push, migration, or cleanup.

## Architecture Decisions

### Decision 1: Scope only split auto-promotion

The wrapper's split auto-update call passes an internal-only promotion scope to
the hidden `promote-internal-update` command. Direct `update-internal` and
`set-bin internal` retain their current full Desktop generation contract.

Changing every internal update to CLI-only was rejected because explicit
internal-App operators still need the existing fail-closed parity path.
Allowlisting the currently observed parity errors was rejected because it
would claim App compatibility rather than remove App from the split CLI
acceptance surface.

### Decision 2: Persist a digest-bound CLI generation and negative App readiness

The internal manifest receives one additive `internal_cli_generation` object
containing a schema version, `scope=cli-only`, exact backend SHA-256, and exact
semantic version. It also receives `internal_app_readiness=unverified`.
Manifest `codex_bin` continues to point to the stable bound path.

The repair keeps this schema at version 1. SHA-256 already binds the complete
byte length, while the stable streaming reader compares file identity and size
before, during, and after hashing. Adding a redundant persisted size field and
a migration was rejected because it would expand the compatibility surface
without strengthening the digest-bound generation contract.

The explicit marker is preferred over inferring CLI-only state from a stale
parity receipt: inference cannot distinguish an intentional CLI promotion from
corruption and produces unstable error messages. A full internal rebind removes
both fields in the same transaction that publishes fresh Desktop evidence.
Legacy manifests without the fields continue through the existing parity
contract.

### Decision 3: Add a narrow transaction bundle scope

The runtime-rebind transaction accepts `full` (current default) and `cli-only`
bundle scopes. `full` preserves the exact schema-v3 required/optional artifact
sets. `cli-only` requires exactly the internal manifest plus the executable
swap and publishes a schema-v4 marker with an explicit scope. Recovery validates
the scope-specific target set before applying either the old or new generation.

A separate ad-hoc rename/write sequence was rejected because the manifest and
binary could disagree across process termination. Reusing the full artifact
set with old Desktop bytes was rejected because those bytes would falsely
attest the new backend.

The prepared validator checks the promoted stable binary identity, backup
identity, candidate retirement, exact version output, and exact manifest. Any
failure while the marker is prepared restores both executable and manifest.
The old executable backup is retired only after the committed marker is durable
and recovery converges.

### Decision 4: The shell entrypoint validates CLI-only state explicitly

When `internal_cli_generation` is present, the managed shell entrypoint checks
its schema, scope, digest, version, stable path, executable type, and internal
home. It executes the recorded backend without loading App capability/parity
artifacts. Functional commands still run shared-configuration reconciliation;
help/version remain informational.

Treating the generation as a generic legacy manifest was rejected because it
would lose the digest postcondition. Mutating or deleting old parity artifacts
was rejected because they are retained evidence and are outside this change's
cleanup authority.

### Decision 5: App selection has a pre-mutation readiness guard

The canonical switch path and the underlying switch transaction both call one
readiness guard whenever the requested App profile is internal. A CLI-only or
malformed readiness marker raises a stable `internal.app_readiness.*` error
before backup capture, Desktop observation/rebind, LaunchAgent/global-state
planning, or active-record mutation. The duplicate boundary prevents a direct
transaction caller from bypassing the public switch check.

The internal App launcher also rejects a CLI-only manifest if invoked outside
the switch command. This is defense in depth, not an internal-App compatibility
implementation.

### Decision 6: Parity applicability follows the App owner

Verify, Doctor, and status collect internal parity only when the active App
profile is internal. For internal CLI plus official App, they emit a concise
not-applicable diagnostic; CLI binding/config/runtime checks continue against
internal, while Desktop observation and optional app-server smoke resolve the
official binding.

Each diagnostic command resolves the active record into one immutable
selection snapshot and carries that snapshot through binding, shared-config,
parity, and active-state evaluation. A parity repair binds its expected active
record bytes into the full-rebind request; the rebind rechecks that exact
snapshot after acquiring the store mutation lock and fails before preparation
or mutation if the selection changed. This prevents one invocation from
mixing CLI/App owners across concurrent switch generations.

After a split auto-update, the wrapper forces bounded internal runtime smoke
(`--version` and local plugin listing) instead of forcing an internal Desktop
compatibility handshake. No provider prompt or model request is added.

That runtime smoke resolves the managed store shim for an explicit CLI-only
generation rather than invoking `RuntimeBinding.backend_cli` directly. The
prepared promotion validator calls the same CLI-generation validator before the
transaction commits. Consequently, an invalid home, backend identity, size,
digest, schema, scope, or readiness marker rolls the candidate and manifest
back, and the final verifier cannot attest a backend path that the operator's
`codex` command cannot use.

### Decision 7: Preserve App bytes and active official operation

The CLI-only artifact allowlist contains only the internal manifest. It cannot
target the managed Desktop launcher, capability/parity files, projected App
config, LaunchAgent, App global state, official manifest/home, or active record.
No App-process stopped proof is needed because none of those targets is written.

### Decision 8: Separate executable hashing from text-artifact loading

Manifest, launcher, receipt, overlay, and config payloads retain the existing
16 MiB bounded reader because callers need their bytes. Backend executables use
a separate descriptor-based streaming SHA-256 helper with a 2 GiB safety bound.
It rejects symlinks and non-regular files, compares device, inode, size, mode,
mtime, and ctime across `lstat`/`fstat`, and never accumulates executable chunks.
Both CLI-only and legacy full-generation backend digest checks use this helper,
so the generic artifact limit cannot regress either executable path.

Raising the text-artifact limit to a larger constant was rejected: it would
still allocate the whole backend and would couple future binary growth to JSON
artifact policy. Removing every bound was rejected because a corrupt local
backend could otherwise force an unbounded validation read.

### Decision 9: Completion guidance consumes the observed App action

The wrapper uses a line-flushing stream filter while retaining only the stable
`App action:` receipt value from the apply step in a mode-0600 temporary file.
`preserve` omits App restart guidance; `rebind` prints it. The capture must not
buffer switch output because progress must remain visible during long shared
synchronization. The Python producer itself runs unbuffered before the
line-flushing filter; flushing only the downstream filter is insufficient once
stdout is a pipe. A public wrapper timing test must observe a progress line
while the fake switcher is still blocked, not merely after process exit.
Failure paths retain their existing targeted recovery guidance.

### Decision 10: Prepared promotion executes a freshly rendered managed shim

Generation metadata validation alone does not prove that the managed shell
entrypoint can load the runtime module and reach the promoted backend. During
the prepared transaction state, render the exact internal shim payload into a
private temporary directory and execute its bounded `--version` probe against
the staged manifest and binary. A failure remains inside the prepared
validator, so binary plus manifest roll back byte-for-byte. The ambient
`store/bin/codex` is not used for this check because a split may still be on the
official pre-switch selection; the later final runtime smoke separately invokes
the actual post-switch store shim.

## Completion Contract

Completion requires all of the following source evidence:

1. Split auto-update selects CLI-only promotion while direct update keeps the
   full path.
2. CLI-only promotion is atomic and rolls back binary plus manifest on a failed
   postcondition or injected transaction fault.
3. The managed shell runs a valid CLI-only generation and rejects digest drift.
4. Split verify/Doctor/status do not fail on internal-App parity and still
   resolve the official App owner.
5. Internal App dry-run/apply and direct transaction requests fail before any
   mutation when readiness is unverified.
6. Full promotion and legacy manifest behavior remain covered by regression
   tests.
7. Documentation states that internal is CLI-only in split mode, App need not
   exit, and source completion is not live installation.
8. A valid executable larger than 16 MiB passes the managed shell contract
   without whole-file buffering, while an executable beyond the independent
   safety bound fails closed.
9. Prepared promotion invokes the managed generation validator and rolls back
   binary plus manifest when that contract fails.
10. Final split runtime smoke fails on a broken managed shim generation even
    when the raw backend itself is runnable.
11. Successful `App action: preserve` output contains no App restart step;
    actual `rebind` retains the guidance.

The completion claim is repository-source-only. No live internal candidate is
promoted and no installed wrapper is updated in this change.

## Capability Slices and Execution Ledger

1. **Contract and RED seams** — write set: this change, transaction/update/
   runtime/switch/diagnostic tests; evidence: focused tests fail for the intended
   missing behavior; Human Gate: user decision already recorded.
2. **Atomic CLI generation** — write set: transaction, bindings, parser, wrapper;
   evidence: commit/rollback and wrapper routing matrices pass.
3. **Runtime and App guard** — write set: runtime binding, switching,
   transaction; evidence: shell generation and pre-mutation guard matrices pass.
4. **Surface diagnostics** — write set: verify, Doctor, status, wrapper;
   evidence: split parity applicability and smoke-routing matrices pass.
5. **Docs and integrated verification** — write set: README, SKILL, verification
   record, ledger/state; evidence: focused/broad tests, static checks, strict
   OpenSpec validation, diff review.
6. **Live-acceptance repair** — write set: runtime binding, promotion validator,
   verifier, wrapper, their public-seam tests, this change, and durable evidence;
   evidence: large-backend managed-shell RED/GREEN, invalid-generation promotion
   rollback, managed-shim smoke failure, preserve/rebind guidance mapping, fresh
   broad verification, and direct read-only live shim `--version` acceptance.

The main agent owns every write. No delegation or generated repository output
is needed. Test temporary directories are process-owned, isolated, and removed
by the existing test harness; this change does not authorize cleanup of any
retained workstation candidate or cache.

Continuation policy: after each green slice, continue to the next approved
slice. Stop only for a new dependency, provider/auth traffic, public contract
expansion, destructive/external effect, inability to preserve unrelated WIP,
or a failed required production contract that needs a new product decision.

## Validation Commands

Focused commands:

```bash
python3.12 scripts/test_codex_transaction.py
python3.12 scripts/test_codex_update_release.py
python3.12 scripts/test_codex_verify.py
python3.12 scripts/test_codex_profile_switch.py
PYTHONPATH=scripts python3.12 scripts/test_codex_shared_lifecycle.py
```

Integrated commands:

```bash
PYTHONPATH=scripts python3.12 -m unittest discover -s scripts -p 'test_codex_*.py'
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
openspec validate internal-cli-only-runtime --strict
git diff --check
```

Provider/model/auth smokes, live promotion, install, App restart, release,
archive, commit, push, and cleanup are intentionally absent.

## Risks / Trade-offs

- **Old App artifacts remain present and stale** -> explicit CLI-only metadata
  prevents them from being treated as current; App selection fails before use.
- **A direct transaction caller could bypass wrapper policy** -> the deepest
  switch transaction repeats the readiness guard and schema-v4 recovery
  validates the exact CLI-only target set.
- **The active App owner changes during diagnostics** -> verify and Doctor use
  one selection snapshot, and a parity repair performs a locked exact-record
  CAS before full-rebind preparation.
- **A binary changes after promotion** -> shell generation validation compares
  the stable file identity and streamed digest before each managed execution and
  fails closed.
- **A future backend is much larger than current production binaries** -> the
  executable-specific 2 GiB bound fails explicitly without reading the file;
  changing that policy requires a reviewed compatibility update, not widening
  text-artifact limits.
- **Prepared promotion validates only the raw backend** -> a freshly rendered
  internal managed shim runs `--version` before commit, so a broken runtime
  entrypoint restores the prior binary and manifest.
- **Final smoke bypasses the managed guard again** -> CLI-only smoke selects the
  actual post-switch store shim, and regression coverage makes a runnable raw
  backend insufficient.
- **Wrapper buffers long switch output while extracting App action** -> action
  capture runs the Python producer unbuffered, uses a line-flushing stream
  filter and an exact mode-0600 temporary file, preserving counted progress
  while retaining only the action value.
- **Diagnostics accidentally hide CLI faults with parity** -> only parity is
  made not applicable; binding, executable, config, Plugin/Skill preflight, and
  requested runtime smokes remain active.
- **Current internal-App users invoke split** -> the target selection is
  official App; CLI promotion never writes App state, and the subsequent switch
  owns the normal App transition. No compatibility claim is made for an already
  running internal app-server child.
- **Schema-v4 crash recovery regresses schema-v3** -> default full commits keep
  schema-v3 bytes and existing tests; new tests exercise prepared and committed
  CLI-only recovery independently.

## Migration and Rollback

No eager state migration is required. The first successful split CLI update
adds the metadata atomically. Legacy and full-parity manifests remain readable.
A later successful full internal rebind removes CLI-only metadata and publishes
fresh App evidence atomically.

During a prepared CLI promotion failure, transaction recovery restores the old
manifest and bound executable and returns the candidate to its private staged
path. After a committed promotion, the prior binary backup is retired under the
existing exact-path contract. Source rollback reverts this change's code and
docs only; live rollback is outside this turn because no live apply is
authorized.

## Project Refresh Impact

Not applicable. No DevFlow plugin, project-local skill set, dependency pin, or
workflow configuration changes. The pre-existing broader project-refresh drift
remains deferred and does not block the available OpenSpec/TDD capability path.
