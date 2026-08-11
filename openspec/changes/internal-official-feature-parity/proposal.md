## Why

The internal profile can remain correctly bound to its internal binary and
provider while silently drifting from the official Codex protocol, feature
surface, model metadata, and Desktop behavior. The confirmed drift for
`gpt-5.6-sol` selects legacy multi-agent v1 because the internal Azure catalog
omits official `multi_agent_version = "v2"`, producing random Subagent
nicknames instead of the task-oriented names and descriptions shown by the
official Desktop experience.

## What Changes

- Add a repeatable official/internal parity inventory for CLI versions,
  feature names and stages, experimental app-server schemas, active-model
  catalog metadata, and runtime protocol behavior.
- Preserve a fixed allowed-difference whitelist: internal keeps its configured
  `codex_bin`, model, API endpoint, provider, and auth, and never binds to the
  official bundle binary.
- Classify non-whitelisted drift as core or optional with stable finding codes.
  Core drift makes internal unhealthy; optional drift remains visible in the
  verification report and synchronization queue.
- Extend backend capability evidence and add a provider-bound parity receipt so
  every internal binary update or rebind rechecks schema and behavior before
  compatibility metadata is promoted.
- Generate a managed catalog overlay from the configured internal source
  catalog. Preserve every internal model/provider/API field and enable only
  approved official metadata whose schema and real Azure behavior probes pass.
- Enable `multi_agent_version = "v2"` only after the internal backend accepts
  the v2 collaboration tool contract. Missing, stale, failed, or unknown
  evidence is a stable unhealthy finding; there is no silent v1 fallback.
- Integrate parity checks into internal rebind, update, verify, Doctor, release
  packaging, and verification reports, then require a real Desktop Subagent
  smoke proving task-oriented names/descriptions and actual runtime ownership.

### Task 8.3 Planning Revision

The first authorized same-backend preparation stopped safely before probes or
transaction publication with thirteen error findings: `item_ids` and
`multi_agent_v2`; eight incompatible core protocol methods; and three
unclassified client requests. The retained diagnostic proves that the current
global Protocol Adapter digest cannot close those findings because it neither
names the exact direction/method/rule coverage nor participates in a final
policy evaluation after probes.

Task 8.3 is revised as one complete method-scoped evidence repair. The repair
will:

- replace global-digest-only acceptance with deterministic coverage records
  that bind direction, method, official/internal method-schema digests,
  incompatibility reasons, disposition, and any exact adapter rule digest;
- distinguish actual adapter transforms from schema-semantic equivalence and
  from explicitly classified optional extensions;
- normalize the four nullable-string spelling differences without calling
  them adapter coverage;
- bind `item_ids` acceptance to the exact observed
  `thread/resume.params.history` dependency, discharged either by native
  official-to-internal method compatibility or by the already proven exact
  transform, and fail closed if another observed core dependency appears;
- make `multi_agent_v2` provisional until the managed overlay/config and
  bounded typed-v2 probe all pass, then perform one final policy evaluation;
- classify only the exact known realtime/audio, Bedrock-login, external-agent
  import, and listed-plugin-share extensions as optional-unless-observed, with
  any changed schema digest or observed dependency returning to an unhealthy
  core/unclassified result; and
- upgrade the parity receipt so diagnostics can verify the exact coverage
  evidence instead of inferring it from a global rule-set hash.

This planning revision authorizes no implementation, provider call, rebind,
restart, dependency, public CLI change, Git effect, release, archive, or
cleanup. Those actions remain behind the revised execution and live Human
Gates.

The later `PARITY-8.3-IMPLEMENT` authorization was consumed only for the
recorded source write set and isolated validation. That implementation is now
source/package verified and paused at `PARITY-8.3-LIVE-RETRY`; no live
installation, rebind, provider probe, restart, or profile/App mutation was
performed. Because the user is prioritizing the official profile, this is the
durable development milestone and task 8.3 remains unchecked until a future
authorized live receipt-v2 promotion and clean diagnostics complete it.

### Installer Side-Effect Isolation Revision

The 2026-07-28 live retry exposed a separate preparation defect before parity
promotion. `scripts/codex_env_setup` passed the live shell `HOME`,
`CODEX_HOME`, and `PATH` into the trusted internal installer. The current
installer always writes `$CODEX_HOME/config.toml` and appends its install
directory to `$HOME/.zshrc` when that directory is absent from the child PATH.
Because the requested install directory was a retained sibling candidate, a
failed preparation could therefore narrow the live official config and leave
that failed candidate ahead of the codex-switch shim. This made Plugins and UI
settings appear reset after the attempted switch and made bare `codex` bypass
the configured internal wrapper even though the manifest, generated wrapper,
and direct app-server smoke still named the correct internal binary.

The approved Scheme A repair makes installer preparation hermetic:

- run the installer with a private disposable `HOME` and `CODEX_HOME`;
- prepend the validated sibling candidate to the installer child `PATH`;
- remove the private scratch root on success, failure, interruption, or
  termination without persisting generated config or credentials;
- preserve the live shell profile, live Codex config, active record, manifest,
  wrapper, bound internal binary, and runtime bundle on every preparation
  failure; and
- retain existing candidate-failure semantics while ensuring no retained
  candidate is placed on the live shell PATH.

The same approval authorizes one recoverable workstation repair: back up the
current `.zshrc`, remove only the three confirmed installer-added candidate
blocks, move the three confirmed failed candidates into a timestamped
codex-switch backup directory rather than deleting them, install the exact
verified source, and perform one controlled internal update/rebind/switch plus
bounded ChatGPT restart and ownership/config/plugin verification.

The implementation write set is limited to `scripts/codex_env_setup` and
`scripts/test_codex_update_release.py`. `scripts/codex-switch` remains
read-only unless a failing wrapper-seam regression proves that the helper
boundary cannot enforce the invariant; any such expansion must be recorded
before editing. No proxy conversion, plugin refresh, global-state allowlist
expansion, legacy skill cleanup, credential/identity migration, dependency,
release, Git effect, or destructive deletion belongs to this repair.

### Internal 0.145 Native-Resume Compatibility Boundary

The first Scheme A update correctly isolated the trusted installer and stopped
before promotion, but exposed one new compatibility false negative. For
internal 0.145.0, `item_ids` differs in feature metadata/effective state while
`client_request:thread/resume` is natively compatible with the official
Desktop schema. Native compatibility produces no incompatibility record and
therefore correctly produces no adapter coverage record. The current
`item_ids` policy nevertheless requires adapter coverage unconditionally and
reports `parity.feature.core_drift`.

The durable correction is not a parity bypass. The exact observed dependency
remains `thread/resume.params.history`; it is satisfied only when that exact
method is either natively compatible in the current official/internal schema
comparison or covered by the exact named adapter rule. Missing, incompatible,
uncovered, stale/broader adapter evidence, or any additional observed
dependency remains unhealthy.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: internal health, capability receipts, managed model-catalog
  binding, update/rebind verification, Doctor/report findings, and Desktop
  Subagent compatibility requirements are changed.

## Impact

Primary impact is a focused parity/catalog module plus the existing Protocol
Adapter, capability receipt, Runtime Binding, transaction/rebind, verifier,
Doctor, package manifest, and regression suites. Current evidence compares
latest stable upstream `rust-v0.145.0`, bundled official
`codex-cli 0.146.0-alpha.3.1`, and internal `codex-cli 0.144.6`; generated
experimental schemas contain 347 official and 337 internal documents. No
production dependency, official-binary rebinding, provider/auth migration,
release, commit, push, destructive cleanup, or OpenSpec archive is included.
