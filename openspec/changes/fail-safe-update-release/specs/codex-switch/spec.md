## ADDED Requirements

### Requirement: Safe package destination
Release packaging SHALL validate canonical containment before recursive cleanup and SHALL build in a temporary staging directory before publishing outputs.

#### Scenario: Repository or ancestor destination is rejected
- **WHEN** the configured output makes the package directory equal to the repository, a repository ancestor, or filesystem root
- **THEN** packaging fails before recursive removal
- **AND** repository sentinel files remain unchanged.

#### Scenario: Unrelated existing directory is preserved
- **WHEN** the package destination is an existing directory not classified as this build's staging/output
- **THEN** packaging refuses to replace it automatically.

#### Scenario: Successful staged package promotion
- **WHEN** an allowed output root is used and all package validation succeeds
- **THEN** the verified bundle, runner, and archive are promoted into the output root
- **AND** temporary staging is cleaned without touching unrelated paths.

#### Scenario: Special files and unsafe root mode are rejected
- **WHEN** a package contains a FIFO, socket, device, symlink, or a package root
  with a mode outside the fixed release policy
- **THEN** validation fails before archive publication
- **AND** a nested file named `bundle-manifest.json` remains payload rather than
  being silently excluded.

### Requirement: Fail-safe installation and self-update promotion
Installer and self-update paths SHALL validate a complete candidate and retain last-known-good until the promoted command completes a success handshake.

#### Scenario: Copy failure preserves current install
- **WHEN** staging copy fails because of an injected permission, capacity, or I/O error
- **THEN** install returns nonzero
- **AND** the previous current installation and public command remain usable.

#### Scenario: Invalid candidate is rejected before promotion
- **WHEN** a candidate lacks VERSION, a required Python module, executable scripts, valid syntax, or the expected version
- **THEN** promotion fails before replacing current.

#### Scenario: Same or older trusted release skips legacy candidate validation
- **GIVEN** the installed current release has a valid version
- **AND** trusted release metadata selects the same version or an older version
- **WHEN** the selected remote asset uses a historical layout that lacks modules required by the current strict bundle
- **THEN** self-update reports that the implementation is already up to date before downloading, extracting, canonicalizing, or validating that asset
- **AND** it does not emit `source_invalid` or the generic sync-failed warning
- **AND** a trusted newer version still requires complete strict candidate validation before promotion.

#### Scenario: Source fallback does not execute downloaded scripts
- **WHEN** installer, runner, or self-update stages from a downloaded source archive
- **THEN** the currently trusted implementation copies only the fixed required allowlist
- **AND** no executable or packaging script from that archive runs before candidate validation and promotion.

#### Scenario: Promoted command failure rolls back
- **WHEN** the candidate passes static validation but its promoted health/re-exec command fails
- **THEN** the last-known-good root is restored atomically
- **AND** failure is reported without deleting the recoverable candidate evidence.

#### Scenario: Successful handshake retires previous
- **WHEN** the promoted command completes the bounded success handshake
- **THEN** the new root remains current
- **AND** the previous verified root remains addressable through the rollback reference.

#### Scenario: Legacy current-directory migration is reversible
- **WHEN** the first promotion encounters the pre-existing directory-based `current` layout
- **THEN** it preserves and validates that directory as the legacy last-known-good before changing the public reference
- **AND** any migration failure leaves the prior command executable.

#### Scenario: Historical current directory predates strict bundle modules
- **WHEN** the pre-existing directory-based `current` layout does not contain release modules introduced by the strict bundle format
- **THEN** migration canonicalizes a private immutable rollback copy without modifying the original legacy directory
- **AND** only absent manifest-required release modules receive inert compatibility placeholders in that private copy
- **AND** a symlinked legacy `scripts` directory is rejected before any external target can be written.

#### Scenario: Normal commands preserve immutable release bytes
- **WHEN** a user runs the installed CLI, installer, runner, packager, or generated Desktop wrapper without setting Python bytecode controls
- **THEN** Python helper imports do not create `__pycache__` or `.pyc` files inside the active immutable release
- **AND** strict candidate validation still succeeds after the command
- **AND** bytecode controls are not exported into the Codex backend or user task environment.

### Requirement: Ordered internal update outcome
Internal update policy SHALL compare semantic versions in order, propagate helper failure, and report success only after the installed binary matches the intended target.

#### Scenario: Healthy newer current is not downgraded
- **WHEN** the current internal version is greater than the reported latest version and is not explicitly blocked
- **THEN** update policy returns `newer_current`
- **AND** no installer is invoked.

#### Scenario: Blocked current may use fallback
- **WHEN** the current internal version is explicitly blocked and the configured fallback is valid
- **THEN** update policy may select that fallback even when it is lower.

#### Scenario: Helper failure is not success
- **WHEN** the internal update helper returns nonzero or the installed version does not equal the intended target
- **THEN** the one-key flow reports update failure
- **AND** does not set the auto-updated flag or print update completion.

### Requirement: Fail-closed plugin availability
Plugin cleanup SHALL distinguish verified catalog results from command, parse, or schema uncertainty and SHALL validate complete installed materialization.

#### Scenario: Invalid catalog cannot authorize disable
- **WHEN** the plugin command fails, writes warnings/errors, returns invalid JSON, or returns an unsupported schema
- **THEN** availability status is unknown
- **AND** `--disable-unavailable` changes no config or snapshot.

#### Scenario: Verified empty catalog is explicit
- **WHEN** an exit-zero catalog response matches the supported schema and contains zero selectors
- **THEN** the catalog is verified empty
- **AND** cleanup may use that result only after reporting it distinctly from parse failure.

#### Scenario: Partial cache is not installed
- **WHEN** a plugin cache contains only temporary files, `.DS_Store`, an incomplete version directory, or lacks the required plugin marker
- **THEN** Doctor and verify report it as not materialized.

#### Scenario: Revision-named curated cache is materialized
- **GIVEN** a verified plugin catalog uses an opaque snapshot revision as its
  cache key
- **AND** the corresponding cache directory contains a regular
  `.codex-plugin/plugin.json` whose plugin name matches and whose manifest
  version is a non-empty string
- **WHEN** Doctor or plugin repair inspects the enabled plugin
- **THEN** the cache is treated as materialized even when the manifest version
  differs from the cache key
- **AND** malformed, symlinked, wrong-name, or source/cache manifest-version
  mismatches remain fail closed.

### Requirement: Release promotion and asset reconciliation
Automatic release workflow SHALL package and validate required assets before pushing release refs and SHALL reconcile an existing release missing required assets.

#### Scenario: Packaging failure precedes ref push
- **WHEN** package creation or asset validation fails
- **THEN** the workflow has not pushed the version commit or tag.

#### Scenario: Existing tag missing asset is reconciled
- **WHEN** the latest release tag already exists but one or more required assets are absent
- **THEN** release planning selects asset reconciliation for that tag
- **AND** does not require unrelated source changes or create a new version solely to retry upload.

#### Scenario: Validated assets publish for the exact tag
- **WHEN** source verification and packaging succeed and refs are created
- **THEN** main and tag refs are pushed atomically after remote-base validation
- **AND** publication uploads and revalidates the exact `install.sh`, `run.sh`, and `codex-switch.tar.gz` for that tag.

#### Scenario: Commit tree is the release authority
- **WHEN** worktree files differ from the target commit, including paths hidden
  by `assume-unchanged` or `skip-worktree`
- **THEN** release validation rejects the package or standalone asset
- **AND** file bytes, file set, and executable bits are compared with the exact
  target commit tree rather than `git status`.

#### Scenario: Historical reconciliation is explicit and deterministic
- **WHEN** an explicitly supported historical tag produces a manifest-less
  package
- **THEN** trusted version-scoped layout validation is required
- **AND** trusted tooling rewrites the archive deterministically before hashing
- **AND** a new-format tag with a missing manifest is rejected.

#### Scenario: Manual recovery binds an exact remote tag before target code
- **WHEN** a manual release recovery is requested
- **THEN** trusted tooling accepts only an exact semantic tag ref and resolves
  its remote commit before checkout
- **AND** target code runs without persisted Git credentials
- **AND** trusted release tooling remains sourced from `main`.

#### Scenario: Reconciliation preserves a pending new release
- **WHEN** the latest tag needs reconciliation and the triggering source commit
  also has release-relevant changes
- **THEN** the workflow reconciles the existing tag
- **AND** returns to the original source commit to prepare and publish the next
  release in the same run.

#### Scenario: Remote tag movement aborts publication
- **WHEN** the remote release tag moves before an upload, release creation,
  publish action, or final verification
- **THEN** reconciliation fails with a tag conflict
- **AND** no later release mutation is attempted.

### Requirement: Safe structured verification evidence
Verification SHALL represent every requested smoke as a structured bounded outcome and SHALL sanitize all externally produced text before printing or persistence.

#### Scenario: Failed prerequisite is not reported passed
- **WHEN** a requested smoke cannot run because its binary, home, or config prerequisite is missing
- **THEN** its status is `not_run`
- **AND** output does not contain a contradictory passed line.

#### Scenario: Hung smoke times out
- **WHEN** a model, plugin, exec, or app-server smoke exceeds its configured timeout
- **THEN** the process group is terminated
- **AND** the outcome is a bounded timeout failure.

#### Scenario: Secrets are redacted globally
- **WHEN** any subprocess output contains bearer tokens, authorization headers, API keys, cookies, credentials, or signed query values
- **THEN** printed and persisted output redacts the secret values
- **AND** no raw exec prompt is stored.

#### Scenario: Large output is bounded
- **WHEN** a subprocess produces output above the configured line/byte limit
- **THEN** verification retains a deterministic sanitized excerpt and truncation marker
- **AND** memory/report size remains bounded.

#### Scenario: Concurrent reports do not overwrite
- **WHEN** multiple verification reports are created for the same profile within one second
- **THEN** each uses a unique no-clobber path and preserves its own outcome.
