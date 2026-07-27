## Context

`codex-switch` currently checks the internal release channel for automatic
internal updates and states that the official profile is managed by
ChatGPT.app. Neither path compares the selected profile CLI with upstream
`openai/codex`.

Authoritative evidence collected on 2026-07-24:

- `https://github.com/openai/codex/releases/latest` redirects to
  `rust-v0.145.0`.
- GitHub's release API reports `rust-v0.145.0` as the latest non-draft stable
  release and `rust-v0.146.0-alpha.6` as the latest non-draft prerelease.
- The configured internal CLI is `codex-cli 0.144.6`.
- ChatGPT.app bundles `codex-cli 0.146.0-alpha.3`.

The existing `codex_switch_update_policy.py` already provides strict SemVer
parsing and ordering. The new behavior must reuse that semantic authority
without coupling the upstream advisory to internal installation decisions.

## Goals / Non-Goals

**Goals:**

- Show the latest stable upstream Codex release beside the selected profile's
  current CLI version.
- Classify the selected CLI as `behind`, `matches`, or `ahead` of the stable
  baseline.
- Make the advisory especially visible during one-key internal switching.
- Bound network work and continue when lookup or parsing is unavailable.
- Keep comparison policy independently testable and Python 3.9 compatible.

**Non-Goals:**

- Selecting, downloading, or installing an internal binary from
  `openai/codex`.
- Treating the newest prerelease as the default compatibility baseline.
- Replacing ChatGPT.app's bundled CLI or changing profile/runtime bindings.
- Persisting release metadata, adding a background updater, or adding a
  production dependency.

## Decisions

### Decision 1: The default baseline is the latest stable GitHub release

Resolve the redirect from `https://github.com/openai/codex/releases/latest`
and require a `rust-v<semver>` tag whose semantic version has no prerelease
component. Output labels it `Latest openai/codex stable`.

The release list/API can expose a newer alpha, but prereleases are not used for
the default baseline. This avoids telling internal users that an alpha is the
required compatibility target. A current prerelease may still compare as
`ahead` of the stable baseline and is described as a prerelease or vendor build,
not as an upgrade recommendation.

Alternative: query the releases API and show both stable and prerelease on every
switch. Rejected because it adds JSON/API/rate-limit failure modes and makes the
primary action ambiguous.

### Decision 2: Comparison policy is pure and separate from update policy

Create `scripts/codex_switch_official_release.py`. It imports the existing
strict SemVer parser and returns an immutable comparison with:

- outcome: `behind`, `matches`, `ahead`, or `unknown`;
- normalized current and stable versions;
- a stable human-readable reason.

The module does not return an install target and cannot mutate internal update
globals. Shell code only formats the result. The existing release-bundle
manifest treats this module as a required runtime file so a package cannot pass
validation and then fail only when the advisory is invoked.

Alternative: reuse `decide_internal_update`. Rejected because its outcomes and
blocked/fallback semantics are installation policy, not an advisory contract.

### Decision 3: Shell owns bounded retrieval and flow placement

Add a generic latest-release redirect resolver and a profile-aware advisory
function in `scripts/codex-switch`. Retrieval uses `curl` with a short
connect/total timeout and an overridable official-latest URL for isolated tests.

Placement:

- `check-update internal`: print after the internal channel decision.
- one-key `internal`: print after any successful internal auto-update, so the
  comparison reflects the final binary entering the switch.
- `check-update official` and one-key official update check: print after the
  ChatGPT.app ownership message.
- `--skip-update-check`: skip the advisory with the rest of update checking.

Alternative: print inside `check_internal_update`. Rejected because a
successful auto-update could make the just-printed comparison stale.

### Decision 4: Advisory failure is explicit and non-blocking

Missing `curl`, timeout, redirect failure, invalid tag, failed current-version
probe, or unparseable version prints one concise
`Official stable comparison: unavailable (...)` line and returns success to the
switch flow. Existing fatal internal update checks remain fatal for their own
reasons; the advisory neither hides nor escalates them.

No result is written to the profile store, config, backup, report, or cache.

## Risks / Trade-offs

- [GitHub lookup adds switch latency] -> use short bounded timeouts and preserve
  `--skip-update-check`.
- [A bundled alpha sorts ahead of the latest stable] -> label the baseline and
  explain that `ahead` is informational, not an update recommendation.
- [GitHub changes redirect/tag shape] -> validate the exact `rust-v<stable
  semver>` contract and fail non-blockingly.
- [Comparison accidentally drives internal update] -> keep a separate result
  type with no target version and add zero-helper-call regression tests.
- [Packaged wrapper omits the advisory module] -> require it in the existing
  release-bundle manifest and reject incomplete candidates before promotion.

## Migration Plan

No state migration is needed. Rollback removes the advisory module and shell
call sites; profile manifests, homes, update sources, and installed binaries
remain unchanged.

## Open Questions

None. The user approved stable-only default comparison; prerelease display can
be proposed later as an explicit opt-in change.
