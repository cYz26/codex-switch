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
- bind `item_ids` acceptance to the already proven exact
  `thread/resume.params.history` transform and fail closed if another observed
  core dependency appears;
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
