## Context

Package, install, self-update, internal-update, plugin-repair, release, and verification code currently own their failure semantics independently. Recursive package cleanup is based on a caller-controlled path. Installer and update helpers are invoked from Bash `if` conditions where `errexit` does not provide reliable propagation. Self-update removes its previous copy before proving the promoted wrapper can run. Internal version policy treats inequality as upgrade need. Plugin catalog parse errors collapse into an empty set that authorizes disable writes. Auto-release pushes refs before package creation. Verify persists unbounded raw process output and infers smoke states from strings.

The target is not a new release mechanism. It is a shared fail-safe promotion/evidence contract that preserves current successful install, fallback, plugin, and release behavior while making failure explicit and recoverable.

## Skill Routing Ledger

- request kind: security, error-handling, release, integration, and diagnostic repair
- workflow mode: Full OpenSpec
- capability-research: used; current installed/update paths, GitHub workflows, plugin CLI parsing, and verification contracts were inspected
- decision-resolution: used; systemic staged promotion and fail-closed behavior are approved
- decision-grilling: skipped; no open product decision remains
- implementation-planning: used through DevFlow/OpenSpec and AI-native plan structure
- architecture-guidance: used; promotion, update policy, catalog result, and smoke outcome are explicit deep-module interfaces
- domain-language-modeling: skipped; release/update terms are already established
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Prove a package destination is safe before recursive cleanup.
- Validate complete candidates before atomic install/self-update promotion.
- Retain and restore last-known-good until a promoted command succeeds.
- Propagate internal helper failure and avoid healthy-version downgrade.
- Distinguish verified catalog state from parse/command uncertainty.
- Package and validate assets before release refs, with missing-asset reconciliation.
- Produce bounded, timed, globally sanitized, uniquely persisted verification outcomes.

**Non-Goals:**

- Installing into the user's live `~/.local` tree during tests.
- Disabling real workstation plugins.
- Publishing a real GitHub release, tag, commit, or push.
- Adding a signing service or new production dependency.

## Capability Evidence

- `authoritative_current`: GitHub Actions can build artifacts before ref publication and workflow-dispatch an existing tag to reconcile assets; existing project release workflow already supports `gh release upload --clobber`.
- `local_scan`: `package-release.sh` recursively removes `$OUT_DIR/codex-switch`; installer removes current before copy; self-update validates one executable; internal update runs under an `if` call stack; catalog stderr is merged into stdout; release refs precede packaging; verification outputs are raw and unbounded.
- `comparison`: patching each status check still leaves different safety definitions. Shared Python policy modules plus thin shell adapters make candidate validation and outcomes directly unit-testable.
- `assumptions`: isolated temporary-directory promotion and fake command/plugin/GitHub responses accurately test failure handling without external effects.
- `contract`: delta scenarios cover containment, candidate validation, rollback handshake, version order, catalog uncertainty, release order/reconciliation, sanitizer, timeout, and report uniqueness.

## Decisions

### Decision 1: Centralize candidate validation and staged promotion

Create `codex_switch_promotion.py`:

```python
@dataclass(frozen=True)
class PromotionCandidate:
    root: Path
    version: str

@dataclass(frozen=True)
class PromotionReceipt:
    outcome: str
    active_root: Path
    rollback_root: Path | None

def validate_candidate(root: Path, expected_version: str | None) -> PromotionCandidate: ...
def promote_candidate(candidate: PromotionCandidate, layout: PromotionLayout, health_command: Sequence[str]) -> PromotionReceipt: ...
def validate_package_destination(repo: Path, output_root: Path, package_dir: Path) -> None: ...
```

Validation requires a manifest/digests, expected files, executable modes, exact VERSION when supplied, shell syntax, Python import/AST checks, and a bounded no-mutation command smoke. The internal layout is `releases/<content-digest>/`, an atomic `current` reference, an atomic `rollback` reference to the previous verified release, `promotion-state.json`, and a promotion lock. Promotion stages an immutable candidate on the target filesystem, records the previous verified reference, switches `current`, runs a hidden structured health command as a child with self-update disabled, marks the candidate verified only after the returned run-id/version/digest/root match, and restores the previous reference on failure. The original user command runs exactly once only after a successful handshake.

Shell scripts remain entrypoint adapters and explicitly check every helper/copy status. Alternative A was more `set -e`; it was rejected because Bash conditional contexts disable the assumed behavior. Alternative B was a sibling-directory overwrite with one temporary previous copy; it was rejected because it weakens last-known-good retention and recovery after interruption.

Self-update performs a metadata version gate before creating a staging
directory or invoking candidate validation. An explicit
`CODEX_SWITCH_SELF_UPDATE_VERSION` is trusted as the selected release version.
For the normal fixed GitHub `releases/latest` path, the wrapper resolves the
exact semantic tag from the trusted release redirect and pins subsequent asset
and source fallback URLs to that tag. If the trusted remote version is equal to
or older than the installed current version, self-update returns the existing
`already up to date` outcome without downloading, extracting, canonicalizing,
or validating the release asset. This allows a strict current implementation
to coexist with a same-version historical asset that predates required release
modules. A newer trusted version still traverses the complete strict candidate
validation and immutable promotion path. Custom source or tarball overrides
without explicit version metadata retain strict candidate validation rather
than inferring trust from archive contents.

### Decision 2: Package cleanup is contained and staging-only

The packager resolves the repository, output root, and package directory
canonically. It rejects the repository root, any repository ancestor, the
filesystem root, an unrelated pre-existing directory without a codex-switch
build marker, symlinks, and special files. Build occurs in `mktemp -d`; a
manifest records schema, VERSION, required paths, modes, and SHA-256 digests
before the verified bundle/tarball move into the allowed output root. The
package root mode is fixed, and only the package-root manifest is excluded from
payload comparison; a nested file with the same basename remains ordinary
payload. Source-archive fallback copies a fixed allowlist using the currently
trusted installer/runner implementation and never executes a script from the
downloaded archive. This provides candidate integrity, not source
authenticity; signing remains out of scope. Tests use sentinel repositories and
parent output paths to prove no deletion.

### Decision 3: Internal update policy returns a structured decision/result

Create `codex_switch_update_policy.py` with ordered semantic-version tuples and outcomes `up_to_date`, `upgrade`, `blocked_fallback`, `newer_current`, and `failed`. A healthy current version greater than latest is `newer_current` and is never downgraded. Fallback is allowed only when the current version itself appears in the blocked set. The shell adapter checks helper exit status, re-reads the installed binary version, and sets `INTERNAL_AUTO_UPDATED=1` only when it equals the intended target.

### Decision 4: Plugin availability is a tri-state result

`run_profile_plugin_command` captures stdout and stderr separately. Parsing returns `CatalogResult(status="verified", selectors=...)` only for an exit-zero response that matches the supported JSON schema; a valid empty catalog remains distinct from `status="unknown"` with parse/command diagnostics. `--disable-unavailable` requires verified state. Installed materialization requires a cache-key directory and `.codex-plugin` marker (or authoritative installed-catalog evidence), not any cache child. The catalog/cache key and the plugin manifest version are separate identities: official curated snapshots can use a Git revision such as `11c74d6b` for the directory while the marker retains a semantic plugin version. Materialization validates the marker name and non-empty version without requiring it to equal the cache key; stale-cache comparison still requires the selected catalog source and cache marker to agree on plugin name and manifest version before any refresh write.

### Decision 5: Release planning reconciles assets and orders local proof before refs

Auto-release verifies the base tag is an ancestor, bumps VERSION, runs full
verification, creates the local release commit, packages and validates
deterministic assets/checksums against the exact Git commit tree, then creates
the local tag and atomically pushes main plus tag after confirming the remote
base has not moved. Worktree status flags such as `assume-unchanged` and
`skip-worktree` are never authority.

Publishing uploads from the same validated workspace and
re-downloads/verifies required assets. Manifest-less bundles are accepted only
through an explicit historical reconciliation mode with a trusted,
version-scoped layout. Their validated package is re-archived by trusted
deterministic tooling before asset hashing, so retries reproduce the same
archive bytes. New-format releases fail if their manifest is absent.

The planner/workflow recognizes an existing latest tag missing any required
asset and selects reconciliation without inventing another version solely for
the retry. If the triggering `HEAD` also contains release-relevant changes, the
same run reconciles the historical tag, returns to the original source commit,
and prepares the next release. A tag pointing at a different commit is a
conflict, never clobbered.

The separate tag/manual release workflow first resolves an exact semantic tag
through trusted tooling, confirms its remote commit before executing target
code, checks out the target commit without persisted credentials, and keeps
trusted release tooling on `main`. Reconciliation rechecks the remote tag
before every release mutation and after final verification. Protected release
tags remain an operational prerequisite because GitHub release mutation and Git
ref observation cannot form one atomic transaction.

### Decision 6: Verification emits structured, sanitized outcomes

Introduce `SmokeOutcome(status, kind, summary, details)` and one sanitizer that redacts authorization/bearer/API-key/cookie/query-signature patterns before any print or report write. Subprocess execution uses explicit timeouts, bounded incremental capture, process-group termination, and `not_run` for failed prerequisites. Raw exec prompts are never persisted. Report names use a no-clobber unique run ID with sub-second entropy.

Alternative A was adding sanitization to the known Azure mismatch branch only; it was rejected because every subprocess can emit secrets. Alternative B was dropping diagnostic output entirely; it was rejected because bounded sanitized excerpts remain useful.

## Critical Path

1. Add RED tests for destructive package paths, copy failure masking, invalid self-update candidate/re-exec failure, failed internal helper/newer current, invalid catalog/missing marker, release ordering/reconciliation, secret output, timeout, prerequisite states, and report collision.
2. Implement promotion/path safety and migrate packager/installer/self-update.
3. Implement ordered update policy and explicit shell result propagation.
4. Implement tri-state catalog/materialization checks.
5. Reorder/reconcile release workflows.
6. Implement structured bounded verification and run isolated integration tests.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover another failure point already inside a staged promotion or structured outcome. New signing infrastructure, live release mutation, new dependencies, or public distribution redesign is `BLOCKED_AWAITING_HUMAN`; cosmetic shell/test splitting is `DEFER_AND_CONTINUE`.

## Risks / Trade-offs

- [Candidate validation invokes several subprocesses] → bound each check and reuse the same validator across installer/self-update tests.
- [Rename rollback can be interrupted] → deterministic sibling names and startup recovery preserve both roots; never recursively delete an unclassified root.
- [GitHub asset state needs network at runtime] → unit-test planner parsing with fixtures and keep real publication outside completion claims.
- [Aggressive sanitization may hide useful context] → preserve field names/status and short non-secret excerpts while redacting values.

## Migration Plan

Existing installations keep the public `current/scripts/codex-switch` path. On the first updated install/self-update, the existing directory is copied into an immutable legacy release, validated as last-known-good, and only then replaced by the atomic `current` reference; any migration failure leaves the old directory executable. Interrupted state is classified and recovered before a new promotion. Workflows change only after merge; no tag or asset is modified by local implementation. Rollback restores previous references, scripts, and workflow ordering.

Historical directory-based installs may predate the strict bundle's release,
promotion, update-policy, and official-advisory modules. Canonicalization copies
the legacy source into private staging and adds inert placeholders for only
those absent manifest-required modules before building the immutable rollback
release. It never edits the original legacy directory. A symlinked `scripts/`
directory is rejected before placeholder writes so canonicalization cannot
write through staging into an external target.

Installed immutable releases must also remain byte-identical while serving
normal commands. Every shell entrypoint and generated Desktop wrapper invokes
Python helpers with `-B`, scoped to that interpreter invocation, so helper
imports cannot create `__pycache__` inside `releases/<digest>/`. The flag is not
exported into the internal backend or user task environment.

## Continuation Policy

- Execution policy: `auto-until-terminal`.
- Canonical execution source: this change's `tasks.md`.
- After each validated item, select the next dependency-ready fail-safe item.
- Genuine Human Gates: live install/plugin/release mutation, dependency addition, distribution layout migration beyond compatible sibling promotion, or public API expansion.
- Commit, push, tag, release, archive, and workstation mutation remain separately unauthorized.

## Open Questions

None.
