## ADDED Requirements

### Requirement: Schema-scoped app-server translation
The internal Desktop proxy SHALL transform messages only for documented RPC
methods, directions, exact field paths, and backend capabilities, and SHALL
preserve unknown or non-control payload data.

#### Scenario: Model keyPath write is translated
- **WHEN** `config/value/write.params.keyPath` is `model` and its value is the
  Desktop alias
- **THEN** only that value uses the configured internal model
- **AND** sibling and nested non-control fields are unchanged.

#### Scenario: Batch model keyPath write is translated
- **WHEN** `config/batchWrite.params.edits` contains a model edit among unrelated
  edits
- **THEN** only the model edit value is translated.

#### Scenario: Arbitrary user payload is not rewritten
- **WHEN** an unknown method, error payload, tool schema/result, metadata object,
  or user payload contains `model`, `type`, `tools`, or `namespace`
- **THEN** the proxy forwards that payload unchanged.

#### Scenario: Dynamic tools capability is independent
- **WHEN** the capability receipt confirms canonical `dynamicTools`
- **THEN** namespace and function specs remain canonical
- **AND** marketplace handling uses its separate capability.

#### Scenario: Supported marketplace kind is retained
- **WHEN** the backend schema advertises `created-by-me-remote`
- **THEN** `plugin/list.params.marketplaceKinds` retains that value.

#### Scenario: Historical and current marketplace schema names are recognized
- **WHEN** generated schema exposes either `PluginMarketplaceKind` or
  `PluginListMarketplaceKind`
- **THEN** the adapter derives the remote marketplace capability from its enum
- **AND** conflicting recognized definitions remain unknown.

#### Scenario: Unknown transform capability preserves canonical data
- **WHEN** schema probing is unavailable and no verified historical rule applies
- **THEN** canonical fields and enum values are not removed
- **AND** any backend rejection remains visible.

#### Scenario: Request IDs are direction aware
- **WHEN** client and server traffic contain equal IDs, orphan responses, errors,
  or boolean IDs
- **THEN** only a valid backend response consumes its matching client method
- **AND** other traffic is not masked as that method's response.

#### Scenario: Desktop memory history matches disk resume identifiers
- **WHEN** Desktop resumes a thread with ResponseItems in
  `thread/resume.params.history`
- **THEN** the proxy removes each history item's top-level `id` before
  forwarding, matching disk-resume request construction
- **AND** a reasoning item with no encrypted content, content, or summary is
  omitted because it is only an unavailable remote reference
- **AND** item order, content, `call_id`, nested metadata, and data outside the
  exact resume-history path remain unchanged.

### Requirement: Version-safe config-write ownership
The proxy SHALL leave AppServer as the sole owner of versioned config writes and
SHALL never patch the config file after AppServer returns a version.

#### Scenario: Proven backend write passes through
- **WHEN** a digest-bound isolated receipt proves the backend preserves unrelated
  config and returns canonical `filePath`, `status`, and `version`
- **THEN** a schema-valid config write is forwarded exactly once
- **AND** the backend response/version is returned without local file rewrite.

#### Scenario: Behavioral probe uses current-valid unrelated config
- **WHEN** a backend accepts current `git` or `local` marketplace source types
  but rejects the historical `github` value
- **THEN** the isolated probe uses a network-free local marketplace fixture
- **AND** safe config-write capability is not reported unknown because of stale
  unrelated fixture syntax.

#### Scenario: Unproven backend write fails before mutation
- **WHEN** the behavioral receipt is missing, stale, failed, or unknown
- **THEN** `config/value/write` and `config/batchWrite` return a stable
  compatibility error before forwarding
- **AND** neither backend nor config file is mutated.

#### Scenario: Backend error triggers no compensation
- **WHEN** the backend rejects a config write
- **THEN** the proxy forwards the error
- **AND** performs no local or private follow-up write.

### Requirement: Semantic offline config preservation
Offline config generation and merge paths SHALL validate TOML with a real
parser, edit complete assignment spans, and restore defaults by stable logical
identity rather than byte equality.

#### Scenario: Malformed TOML fails closed without a parser
- **WHEN** no real TOML parser is available or the document is invalid
- **THEN** the operation fails before writing a destination
- **AND** the diagnostic explains the supported interpreter requirement.

#### Scenario: Multiline assignment is replaced as one value
- **WHEN** an overlay changes a multiline array, string, or inline-table value
- **THEN** the complete prior value span is replaced
- **AND** no stale continuation line remains.

#### Scenario: Modified array-table entity is not revived
- **WHEN** `[[skills.config]]` contains the same parsed `path` identity with
  changed or disabled values
- **THEN** offline recovery treats the current entity as present
- **AND** does not append the old entity.

#### Scenario: Plugin uninstall survives internal restart
- **WHEN** the internal AppServer removes a `[plugins.*]` entry from its current
  runtime config and the internal Desktop app restarts
- **THEN** launcher preparation copies the current plugin usage state exactly
  to the shared base and rebuilt internal runtime
- **AND** an older profile snapshot does not recreate the removed plugin.

#### Scenario: Plugin and skill usage follows the active profile
- **WHEN** official and internal profiles are switched in either direction
- **THEN** `[plugins.*]` and `[[skills.config]]` in the source runtime replace
  the destination usage state exactly
- **AND** installs, removals, `enabled = true`, and `enabled = false` converge
  without duplicate skill identities.

#### Scenario: Stale snapshots recover support metadata only
- **WHEN** an older snapshot contains plugin or skill entries missing from the
  current runtime plus marketplace or hook support metadata
- **THEN** snapshot recovery may retain the marketplace and hook metadata
- **AND** it does not restore the missing plugin or skill usage entries.

#### Scenario: Truly missing entity is restored once
- **WHEN** a known identity is absent from the current document and present in
  validated defaults
- **THEN** recovery adds it exactly once while preserving current entities.

#### Scenario: Intentional offline deletion is protected
- **WHEN** an offline operation protects a deleted or replaced key path
- **THEN** missing-default recovery does not recreate that path, its ancestor,
  or its descendant.

#### Scenario: Ambiguous identity fails closed
- **WHEN** a managed array-table block lacks a scalar identity, duplicates an
  identity, or belongs to an unknown family
- **THEN** recovery does not append a potentially stale block
- **AND** emits a stable diagnostic.

### Requirement: Canonical launcher home preparation
The generated internal Desktop launcher SHALL use the same canonical Python
home-sync policy as normal profile switching.

#### Scenario: Relative and cross-profile isolated links are removed
- **WHEN** an isolated entry is a relative, dangling, live-home, other-profile,
  or self-referential symlink
- **THEN** launcher preparation removes or rejects it before backend startup
  according to the canonical policy.

#### Scenario: Shareable symlink loop is rejected
- **WHEN** a source shareable symlink would point within the target home
- **THEN** launcher preparation does not create the loop.

#### Scenario: CLI and launcher policies stay equivalent
- **WHEN** identical source and target homes are prepared by normal switching
  and launcher startup
- **THEN** both classify runtime, isolated, and shareable entries equivalently.

#### Scenario: Restart and switch share usage-state ownership
- **WHEN** the same current runtime config is prepared by internal Desktop
  restart or by an official/internal switch
- **THEN** both paths produce the same plugin and skill usage state
- **AND** neither path unions that state with a stale snapshot.

### Requirement: Proxy chain integration verification
The system SHALL verify generated launcher, proxy, and backend as one isolated
JSONL process chain.

#### Scenario: End-to-end request and response translation
- **WHEN** a generated launcher starts a fake backend and receives initialize,
  config-write, plugin-list, model, and thread messages
- **THEN** the backend observes only required schema-scoped request changes
- **AND** the client observes only required response masking.

#### Scenario: Config write keeps backend version authority
- **WHEN** a verified fake backend successfully applies a Desktop config write
- **THEN** the client receives exactly its schema-valid response/version
- **AND** no proxy-side file write follows.

#### Scenario: Unverified config write is blocked end to end
- **WHEN** the chain uses a backend without a valid behavioral receipt
- **THEN** the backend observes no config-write request
- **AND** the client receives the stable compatibility diagnostic.

#### Scenario: Stream and exit behavior is preserved
- **WHEN** stdin reaches EOF, backend writes stderr, or backend exits nonzero
- **THEN** proxy streams close without hanging, diagnostic stderr is bounded,
  and the appropriate exit status is returned.
