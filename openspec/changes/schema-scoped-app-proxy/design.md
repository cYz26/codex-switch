## Context

The proxy recursively traverses arbitrary JSON looking for names such as
`model`, `type`, and `tools`. This misses real control shapes such as
`config/batchWrite.params.edits[*].keyPath`, while changing unrelated user or
tool payloads. Marketplace filtering is coupled to the dynamic-tools version
check even though the capabilities are independent.

Config handling has two distinct defects. Offline line-oriented helpers see
only the first line of a value and compare array-table blocks byte-for-byte, so
they can leave stale continuation lines or append an old logical entity after
it was disabled. Separately, the proxy patches `config.toml` after a successful
AppServer write but returns the backend's pre-patch `version`, creating an
immediate `expectedVersion` conflict. The generated launcher also embeds a
second home-sync policy with weaker symlink rules.

## Skill Routing Ledger

- request kind: protocol compatibility, persistence, and integration repair
- workflow mode: Full OpenSpec
- capability-research: used; installed generated schemas, current source, and
  an isolated internal AppServer write probe were compared
- decision-resolution: used; schema-scoped transforms, backend-owned versions,
  and fail-closed unproven writes are approved
- decision-grilling: skipped; evidence resolves the prior version question
- implementation-planning: used through DevFlow/OpenSpec and AI-native plan
- architecture-guidance: used; Protocol Adapter, capability receipt, and
  Config Document are explicit deep-module seams
- domain-language-modeling: skipped; schemas and TOML define the vocabulary
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Transform only documented methods, directions, and exact field paths.
- Track dynamic-tools, marketplace-kind, and config-write safety independently.
- Preserve unknown messages and non-control payload values unchanged.
- Keep AppServer as the sole owner of config write/version state.
- Validate TOML with a real parser and edit complete offline value spans.
- Merge offline array-table defaults only by stable logical identity.
- Use one canonical home-sync implementation from CLI and launcher.
- Test real JSONL framing and lifecycle through launcher, proxy, and backend.

**Non-Goals:**

- Building a general JSON-RPC or formatting-preserving TOML framework.
- Sending requests through the user's live profile or running AppServer.
- Adding a production dependency.
- Removing legacy transforms still justified by generated schema evidence.

## Capability Evidence

- `authoritative_current`: both installed CLIs provide
  `app-server generate-json-schema --experimental`.
- `local_scan`: official `0.145.0-alpha.27` and internal `0.142.4` expose
  canonical `dynamicTools`, `ConfigValueWriteParams.keyPath`,
  `ConfigBatchWriteParams.edits[*].keyPath`, required
  `ConfigWriteResponse.filePath/status/version`, and marketplace kind
  `created-by-me-remote`. Existing `0.140` evidence proves legacy dynamic-tool
  and marketplace incompatibility but not safe versioned config persistence.
- `behavior_probe`: internal `0.142.4`, launched with a temporary
  `CODEX_HOME`, completed initialize plus `config/value/write`, returned a
  schema-valid version, changed only the requested feature, and preserved
  unrelated MCP, marketplace, plugin, and `[[skills.config]]` entries.
- `current_recheck`: installed internal `0.144.6` and bundled official
  `0.146.0-alpha.3` generated `PluginListMarketplaceKind` rather than
  `PluginMarketplaceKind`, while retaining `created-by-me-remote`. Their
  isolated config-write flows still return canonical path/status/version and
  preserve unrelated config. The old probe fixture alone was invalid because
  `source_type = "github"` is now rejected in favor of `git` or `local`.
- `primary_source`: current OpenAI Codex config service applies batch edits
  atomically to the user layer and returns the resulting layer version. This
  supports backend ownership; it does not authorize a local post-response edit.
- `contract`: focused scenarios cover exact paths, negative payloads,
  independent capabilities, behavioral write gating, identity, multiline
  spans, parser absence, symlink policy, and JSONL process behavior.

## Decisions

### Decision 1: Method-scoped Protocol Adapter

Create `codex_switch_protocol_adapter.py`:

```python
@dataclass(frozen=True)
class BackendCapabilities:
    canonical_dynamic_tools: bool | None
    remote_marketplace_kind: bool | None
    versioned_config_write_preserves_unrelated: bool | None

@dataclass(frozen=True)
class ProtocolAdapter:
    actual_model: str
    desktop_model: str
    capabilities: BackendCapabilities

    def client_request(self, message: Mapping[str, object]) -> AdaptResult: ...
    def server_message(
        self,
        message: Mapping[str, object],
        *,
        pending_method: str | None,
    ) -> AdaptResult: ...
```

Dispatch binds direction + method + exact JSON path to a transform. Required
request paths include:

- `thread/start.params.dynamicTools`;
- `plugin/list.params.marketplaceKinds`;
- documented thread/turn/realtime model fields;
- `config/value/write.params.value` only when `keyPath == "model"`;
- `config/batchWrite.params.edits[*].value` only when the adjacent
  `keyPath == "model"`.

Response and notification masking is limited to paths present in the generated
schema, such as `model/list.result.data`, `config/read.result.config.model`, and
documented thread/turn/item model fields. Unknown methods, `error.data`, tool
input schemas, arbitrary nested `model`, and synthetic legacy paths are not
rewritten. Copy-on-write occurs only when a target changes; otherwise the
original JSONL line is forwarded byte-for-byte.

Request tracking is direction-aware. Only a backend response consumes the
matching client request. Server requests, same-number IDs in the opposite
direction, orphan responses, and error responses do not corrupt the tracker.
JSON-RPC IDs accept strings or integers but reject Python `bool`.

Some internal provider responses return `encrypted_content = null` even though
the request uses `store = false` and includes `reasoning.encrypted_content`.
Such a history entry contains no portable content: after its `rs_` ID becomes
unavailable, it cannot be replayed. The adapter omits only reasoning entries
whose encrypted content, content, and summary are all empty. This is an
explicit degraded-continuity fallback: visible messages, tool calls, and tool
outputs remain, while upstream AIDP must still return encrypted reasoning
content or provide stable item routing for full-fidelity continuation.

Desktop can resume a non-running thread by supplying raw ResponseItems in
`thread/resume.params.history`. A captured 0.144.6 failure showed that this
path preserved the local UUID of a synthetic hook message at history index 77,
while the backend's disk-resume path removed top-level ResponseItem IDs before
creating the Responses request. The adapter therefore removes only top-level
`id` fields from entries in this exact history path. It preserves item order,
content, `call_id`, nested metadata, and every payload outside this documented
resume-history boundary.

### Decision 2: Independent tri-state capability receipts

At internal rebind/launcher generation, generate schema into a temporary
directory and persist a digest-bound receipt beside the launcher. Dynamic-tools
flattening and marketplace filtering use separate `SUPPORTED`, `UNSUPPORTED`,
or `UNKNOWN` fields. A capability is removed only when explicitly
`UNSUPPORTED`; `UNKNOWN` passes canonical data through and exposes any backend
error.

Config-write safety is behavioral, not inferred from schema shape. The
candidate backend runs in an isolated temporary home containing representative
unrelated config, performs initialized versioned writes, and must preserve
those entries while returning canonical path/status/version. The receipt binds
the result to backend and schema digests. A missing, stale, failed, or unknown
receipt makes `config/value/write` and `config/batchWrite` fail before backend
forwarding. Internal `0.142.4` has current local evidence; `0.140` receives no
unsafe fallback.

Marketplace capability extraction recognizes both the historical
`PluginMarketplaceKind` and current `PluginListMarketplaceKind` generated
definitions. Conflicting recognized definitions remain `UNKNOWN`. The
behavioral probe uses a representative `source_type = "local"` marketplace
entry so probe validity does not depend on historical remote source syntax or
network access.

### Decision 3: AppServer owns versioned config writes

Delete proxy snapshot/post-response recovery. For a proven backend, the proxy
forwards the request exactly once and returns the backend response/version
unchanged except exact model aliasing. For an unproven backend, it emits a
stable compatibility error without mutating the backend or file.

A local post-write patch is rejected because it invalidates the returned
version. A private follow-up batch is also rejected because the proxy would
have to invent edit ordering and version semantics beyond generated-schema
evidence.

### Decision 4: Semantic Config Document for offline merges

Create `codex_switch_config_document.py`:

```python
class ConfigDocument:
    @classmethod
    def parse(cls, text: str, label: str) -> "ConfigDocument": ...

    def recover_missing_from(
        self,
        snapshot: "ConfigDocument",
        *,
        protected_paths: frozenset[tuple[str, ...]],
    ) -> RecoveryResult: ...
```

`tomllib` performs semantic parsing. The generated launcher uses the resolved
`CODEX_SWITCH_PYTHON` or generation-time `sys.executable`; if a real parser is
unavailable, the operation fails before mutation with Python 3.11+ guidance.
No production dependency is added.

A source scanner records complete assignment/table spans, including multiline
strings, arrays, inline tables, comments, quoted keys, and CRLF, but never acts
as the TOML semantic parser. Edits apply in reverse span order and the result is
parsed again. No-op output remains byte-identical.

Normal table entries use decoded semantic key paths. The first managed
array-table identity is `[[skills.config]]` keyed by its parsed scalar `path`,
without filesystem normalization. Current entities win. Missing, non-scalar,
or duplicate identities and unknown array families are skipped with a stable
diagnostic, never appended by byte guess. A protected path blocks candidates
equal to, above, or below it. This seam is for offline generation/merge only;
the proxy does not invoke it after AppServer writes.

`[plugins.*]` and `[[skills.config]]` are usage state, not recoverable defaults.
The config of the profile that is currently running is authoritative for
install, uninstall, enable, disable, and skill removal. Before a switch or an
internal Desktop restart builds another runtime config, it removes all usage
blocks from the destination and copies the authoritative blocks exactly.
Fallback runtime configs, profile layers, and plugin-support snapshots may
recover missing `[marketplaces.*]` and `[hooks.state.*]` metadata, but they
cannot add usage blocks. Snapshot refresh likewise copies usage blocks exactly
from the runtime and only merges missing non-usage support metadata from older
snapshots. This preserves repair inputs without allowing stale snapshots to
undo an explicit user action.

### Decision 5: Canonical Python launcher home sync

Add `sync_profile_app_home_for_launch(...)` in
`codex_switch_home_sync.py`. It preflights parser/config results, removes all
forbidden profile-local symlinks (relative, cross-profile, dangling, and
self-referential), synchronizes shared support, preserves target runtime keys,
copies authoritative plugin/skill usage state, rebuilds app config, refreshes
snapshots, and applies the existing auth policy.
Normal switch and launcher paths call this same policy.

The shell wrapper only invokes canonical sync, exports `CODEX_HOME`, routes
`app-server` through the proxy, and sends other commands directly to the
backend. It contains no independent `find`, symlink classifier, or TOML logic.

### Decision 6: Isolated real-chain harness

Tests generate a launcher in a temporary store and point it to a fake backend
with configurable modern/legacy/unknown capabilities. The fake records argv,
environment, raw JSONL, response flush, and exit behavior. The harness covers
modern pass-through, exact legacy transforms, unknown payload preservation,
proven write pass-through, unproven write rejection, launcher home prep,
stderr, EOF, and nonzero exits. A separate isolated real-binary fixture covers
the behavioral receipt without touching live state.

## Critical Path

1. RED tests for exact transforms, tracking, and independent capabilities.
2. Protocol Adapter plus schema/behavior receipt; remove post-response writes.
3. Config Document RED/GREEN for parser, spans, identity, and protected paths.
4. Canonical launcher home sync and thin wrapper.
5. Complete modern/legacy/unknown/write/lifecycle E2E matrix.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover another schema path already inside the
adapter or another managed offline config entity already inside the document
policy. New protocol support, dependency introduction, or live backend traffic
is `BLOCKED_AWAITING_HUMAN`; cosmetic cleanup is `DEFER_AND_CONTINUE`.

## Risks / Trade-offs

- Unusual schema generation can fail: transform capabilities remain unknown
  without deleting data, while config writes fail closed.
- Generated definition names and unrelated probe config syntax can drift:
  current and historical names are explicit fixtures, and the behavioral probe
  uses only locally valid, network-free representative config.
- Span preservation is subtle: semantic parsing plus focused scanner tests and
  post-edit parsing bound the risk.
- Python 3.9 has no `tomllib`: managed launchers pin a verified Python 3.11+
  interpreter rather than accepting malformed TOML.
- Blocking an unproven legacy config write is stricter than unsafe recovery:
  the diagnostic directs the user to rebind/probe a supported backend.

## Migration Plan

Managed launchers regenerate on the next explicit internal switch/rebind and
include the capability receipt. Existing config is not eagerly rewritten.
Offline Config Document changes affect only paths already performing writes.
Rollback restores the previous proxy, wrapper, receipt, and helpers. No live
profile switch or migration is part of isolated verification.

## Continuation Policy

- execution policy: `auto-until-terminal`
- canonical source: this change's `tasks.md`
- proceed to the next dependency-ready item after validated evidence
- Human Gates: new dependency, live backend/profile mutation, unsupported
  required schema transform, or public compatibility expansion
- commit, push, tag, release, archive, install, and live switch remain separate

## Open Questions

None.
