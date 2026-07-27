# Official Release Version Advisory Implementation Plan

## Target State

Every normal official/internal update check shows a read-only comparison between
the selected profile CLI and the latest stable `openai/codex` release. Internal
one-key switching prints the comparison after any internal auto-update. Lookup
or parsing failure is bounded and non-blocking. The comparison never selects an
internal install target or writes profile state.

## Completion Contract

- [x] Stable-tag and SemVer comparison policy is covered by RED/GREEN tests.
- [x] Internal and official update-check flows print profile-aware advisories.
- [x] Network, redirect, tag, and version failures remain non-blocking.
- [x] Internal helper invocation is unchanged by the upstream comparison.
- [x] Focused dual-runtime, full profile, strict OpenSpec, syntax, and diff
  checks pass.

## 1. Comparison Policy

- [x] 1.1 Add RED tests in `scripts/test_codex_official_release.py` for behind,
  matching, ahead, current prerelease, invalid current output, invalid tag, and
  prerelease-tag rejection.
- [x] 1.2 Create `scripts/codex_switch_official_release.py` with an immutable
  `behind|matches|ahead|unknown` result that reuses strict SemVer parsing but
  exposes no install target; make 1.1 GREEN on Python 3.9 and 3.12.

## 2. Shell Flow Integration

- [x] 2.1 Add RED wrapper tests for standalone internal/official checks,
  one-key internal after auto-update, lookup timeout/failure, invalid stable
  tag, `--skip-update-check`, and an internal-behind result that invokes no
  update helper.
- [x] 2.2 Add bounded official-latest redirect lookup and profile-aware output
  to `scripts/codex-switch`; place internal comparison after any auto-update,
  retain ChatGPT.app ownership output, require the advisory module in release
  bundles, and make 2.1 GREEN.

## 3. Documentation and Verification

- [x] 3.1 Update `README.md` and `SKILL.md` to document stable-only,
  non-blocking comparison and the internal update-source boundary.
- [x] 3.2 Run focused policy/wrapper tests on Python 3.9 and 3.12, including
  byte-identical profile-store snapshots proving zero advisory writes.
- [x] 3.3 Run the full profile suite, strict repository OpenSpec validation,
  Bash syntax, Python AST/import checks, isolated package generation, and
  `git diff --check`.
- [x] 3.4 Record authoritative release evidence, RED/GREEN commands, changed
  files, and residual risks in the task ledger, state, and a verification note.

## Capability Slices

1. Pure comparison policy.
2. Bounded retrieval and shell placement.
3. Documentation and integrated verification.

## Execution Ledger

| Slice | Write Set | Evidence | Human Gate | Status |
|---|---|---|---|---|
| Policy | advisory module and focused test | dual-runtime RED/GREEN | none | done |
| Flow | wrapper and profile integration tests | fake-curl/helper calls and zero-write snapshots | live switch/update | done |
| Verification | docs/control plane only after tests | full commands and hashes | release/commit/push | done |

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_official_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_official_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate --all --strict --no-interactive
bash -n scripts/codex-switch
git diff --check
```
