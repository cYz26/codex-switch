# Official Release Version Advisory Verification

Date: 2026-07-25

Change: `official-release-version-advisory`

## Outcome

Normal official/internal update checks and one-key switches now show a
read-only comparison with the latest stable `openai/codex` release. The
advisory is bounded, stable-only, non-blocking, and incapable of selecting an
internal install target or writing profile state.

## Authoritative Release Evidence

Evidence refreshed on 2026-07-25:

- `https://github.com/openai/codex/releases/latest` redirected to
  `rust-v0.145.0`.
- The GitHub releases API reported `rust-v0.145.0`, published
  `2026-07-21T18:21:04Z`, as the latest non-draft stable release.
- The same API reported `rust-v0.146.0-alpha.6`, published
  `2026-07-24T05:31:18Z`, as the latest non-draft prerelease.
- Read-only local status reported internal `codex-cli 0.144.6` and the
  ChatGPT.app bundled CLI `codex-cli 0.146.0-alpha.3`.

## Implemented Contract

- `scripts/codex_switch_official_release.py` reuses strict SemVer parsing and
  returns immutable `behind`, `matches`, `ahead`, or `unknown` results with no
  install target.
- `scripts/codex-switch` resolves the official latest redirect with a
  3-second connect timeout and 8-second total timeout.
- Internal comparison runs after any successful auto-update and retains the
  internal release source as the only installer authority.
- Official comparison retains ChatGPT.app ownership of the bundled CLI.
- Curl absence is handled by an explicit command-availability guard. Lookup
  failure, invalid/prerelease stable tag, current-version probe failure, and
  unparseable versions print one unavailable advisory and preserve the existing
  command outcome.
- `--skip-update-check` skips both profile-specific and upstream network work.
- Profile-store snapshots remain byte-identical across standalone advisories,
  and an internal-behind result makes zero update-helper calls.
- Release bundles require the advisory module. Installer and runner bootstrap
  hashes were refreshed to the exact release-bundle module digest.

## RED / GREEN Evidence

Policy RED, before the comparison module existed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_official_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_official_release.py -v
```

Both failed because `codex_switch_official_release` was absent. After the pure
policy implementation, both runtimes passed 4/4.

Shell-flow RED, before the wrapper integration existed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_check_compares_with_official_stable_without_helper \
  CodexProfileSwitchTests.test_official_check_compares_bundled_prerelease_with_stable \
  CodexProfileSwitchTests.test_internal_switch_compares_after_successful_auto_update \
  CodexProfileSwitchTests.test_official_stable_lookup_failure_is_nonblocking \
  CodexProfileSwitchTests.test_prerelease_tag_is_not_used_as_stable_baseline \
  CodexProfileSwitchTests.test_skip_update_check_skips_official_release_lookup -v
```

The cases failed before the resolver/advisory call sites were added. The final
focused matrix adds unparseable-version, bounded-argument, zero-write, and
zero-helper assertions and passes 7/7 on Python 3.12.13 and Python 3.9.6.

Release dependency RED:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py \
  CodexUpdateReleaseTests.test_release_bundle_rejects_missing_required_python_modules -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py \
  CodexUpdateReleaseTests.test_release_bundle_rejects_missing_required_python_modules -v
```

Both runtimes reproduced that a missing
`codex_switch_official_release.py` incorrectly built successfully. After
adding it to `REQUIRED_PYTHON_MODULES`, both passed 1/1.

## Final Validation

- Advisory policy: 4/4 on Python 3.12.13 and 4/4 on Python 3.9.6.
- Focused advisory wrapper: 7/7 on both runtimes.
- Release missing-module regression: 1/1 on both runtimes.
- Full profile suite: 171/171 on Python 3.12.13.
- Full update/release suite: 64/64 on Python 3.12.13.
- Strict OpenSpec: 17/17 repository items.
- Python static: AST 53/53 and production imports 46/46 on Python 3.12.13
  and Python 3.9.6.
- Bash syntax passed for `scripts/codex-switch`, `install.sh`, `run.sh`, and
  `scripts/package-release.sh`.
- `git diff --check` passed.
- Isolated bundle `0.1.13` validated with payload digest
  `37d2c414db4b429646fc31fce789a7c6f9ee5d77cd65bf506a62b931f730bb2`;
  its manifest and tarball both contain
  `scripts/codex_switch_official_release.py`.
- Read-only `check-update internal` reported internal `0.144.6` behind stable
  `0.145.0` and no internal update.
- Read-only `check-update official` reported bundled
  `0.146.0-alpha.3` ahead of stable `0.145.0` and retained ChatGPT.app
  ownership.

Key source hashes:

- advisory module:
  `d6a33104fe72b84de6a32464386535042a3a7dec20c6d80beaf7ce8d3fc288b7`
- wrapper:
  `4fdce598185f0769f21802af58713fd2940cf5c1b668c6a1e4139cfe4c25bf9a`
- release-bundle module and trusted bootstrap pin:
  `6d7a37ddc4df5d58c19afc99eaa205761fe14b0f81005be744235871cda50274`

## Changed Files

- `scripts/codex_switch_official_release.py`
- `scripts/codex-switch`
- `scripts/codex_switch_release_bundle.py`
- `install.sh`
- `run.sh`
- `scripts/test_codex_official_release.py`
- `scripts/test_codex_profile_switch.py`
- `scripts/test_codex_update_release.py`
- `README.md`
- `SKILL.md`
- `openspec/changes/official-release-version-advisory/**`
- `TASK_LEDGER.md`
- `.planning/STATE.md`

## Safety And Residual Risk

No live profile switch, internal update, install/self-update, ChatGPT restart,
plugin mutation, release, commit, push, tag, or OpenSpec archive action ran.
The local installed release is not refreshed by this source change.

GitHub availability can add up to the bounded eight-second advisory latency;
`--skip-update-check` remains the explicit no-network path. The latest stable
version is deliberately resolved at runtime rather than persisted.

Read-only status also observed an unrelated VS Code app-server process and
reported a runtime-binding mismatch before listing the ChatGPT managed proxy
chain. That pre-existing live-process state was not changed by this work and
still requires the separately gated App restart/attestation follow-up.
