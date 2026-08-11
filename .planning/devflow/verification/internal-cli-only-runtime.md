# Internal CLI-Only Runtime Verification

## 2026-08-10 Live Acceptance Repair

The previous 19/19 and 990/990 source claim was reopened after the real managed
shim rejected the valid 276,128,448-byte internal backend with
`CLI backend exceeds the size limit`. Diagnosis found three coupled defects:

1. CLI executable hashing reused the 16 MiB buffered text-artifact reader.
2. Final CLI-only runtime smoke invoked the raw backend instead of the managed
   store shim used by the operator-facing `codex` command.
3. Successful split output printed an App restart step even when the observed
   App action was `preserve`; its first action-capture implementation also made
   the upstream Python producer block-buffer stdout.

Independent review found one additional prepared-transaction gap: generation
metadata validation did not execute a freshly rendered managed shell
entrypoint before commit.

### RED Evidence

- A valid sparse 17 MiB backend failed with `CLI backend exceeds the size
  limit`; an over-2-GiB fixture did not produce the executable-bound error.
- A raw candidate with an invalid managed Home incorrectly committed and
  printed `CLI-only promotion: passed`.
- Verifier smoke called a deliberately failing raw backend instead of the
  successful managed store shim.
- `App action: preserve` still printed `Restart ChatGPT` in the final result.
- A candidate that succeeds under raw probing but fails through managed
  `CODEX_HOME` incorrectly committed instead of rolling back.
- A fake switcher that emitted progress and remained blocked exposed no progress
  within two seconds; the output appeared only after process exit.

### GREEN Implementation and Focused Proof

- Executables use descriptor-based stable streaming SHA-256 with identity
  checks across open/read/close and an independent 2 GiB bound. Text artifacts
  retain the 16 MiB limit and CLI-generation schema remains v1.
- Prepared CLI-only promotion validates generation metadata, renders the exact
  internal shim into a private temporary directory, and executes its bounded
  `--version` path. Failure remains inside the prepared journal and restores
  the old binary plus manifest byte-for-byte.
- Final CLI-only runtime smoke invokes `store/bin/codex`; the raw backend is no
  longer sufficient to pass verification.
- The wrapper captures only `App action: preserve|rebind`, keeps stderr on its
  original channel, runs the Python producer with `-u`, flushes the downstream
  filter, omits restart guidance for `preserve`, and retains it for `rebind`.
- Initial focused GREEN matrices passed for production-sized/over-bound
  generation 2/2, promotion 4/4, wrapper 3/3, verifier managed smoke 1/1, and
  the two review-driven public seams 2/2.

### Final Source, Package, and Live Read-Only Proof

```text
full source discover: 997/997 in 788.299s
Python in-memory compile: 61 files
Bash syntax: 5 entrypoints
eval JSON: valid
strict target OpenSpec: passed
strict repository OpenSpec: 22/22
workflow validator: ok=true, issues=0
git diff --check: passed
package-local focused tests: 9/9 in 6.279s
release counterpart: valid, 71 files, 5 directories
source/package key-file identity: byte-exact
release-counterpart Plugin Eval: 58/100, existing INC-012 classes
managed live shim: codex-cli 0.145.0, exit 0, 0.28s
```

The workflow validator retains only the pre-existing INC-018 warning that
`AGENTS.md` lacks Project-Directed Implementation Readiness guidance. The
repository-local reference-audit script named by policy is absent, so no cache
refresh or project migration was attempted.

Two independent read-only re-reviews returned PASS after the review-driven
repairs: Standards found no new P1/P2 or hard violation, and Spec confirmed the
prepared temporary shim, actual final store shim, unbuffered producer/filter,
schema-v1 compatibility, rollback, and scope boundaries.

The isolated release counterpart and immutable receipt are under
`.planning/devflow/deployments/20260810T202906+0800/`. It is retained and was
not installed.

### Residual Boundary

- No internal update, re-run of split, App stop/restart, install, cache refresh,
  provider/model/auth traffic, dependency or project migration, Git, release,
  archive, cleanup, credential, or destructive effect ran.
- Internal App compatibility remains intentionally unverified; App-owner
  `internal` still requires the full parity path.
- An abrupt signal can leave the mode-0600 action receipt and there remains a
  same-user path-replacement window between validated digest and `execve`.
  INC-022 and INC-023 retain these non-blocking follow-ups without authorizing
  implementation.

## Outcome and Boundary

- Change: `internal-cli-only-runtime`
- Result: source implementation verified; OpenSpec tasks 19/19 complete.
- Supported target: internal Codex for shell CLI, official bundled Codex for
  Codex App.
- Explicitly unclaimed: live internal update/promotion, installed-source
  activation, profile switch, App stop/restart, internal App compatibility,
  provider/model/auth traffic, dependency or project migration, Git, release,
  archive, cleanup, credentials, and destructive effects.
- The paused `internal-official-feature-parity` work and its historical
  evidence were not rewritten.

## Implemented Contract

1. `codex-switch split` keeps ordered internal update detection but promotes a
   selected candidate as an atomic CLI-only binary-plus-manifest generation.
2. The internal manifest records an exact version/digest-bound
   `internal_cli_generation` and `internal_app_readiness=unverified`.
3. Schema-v4 recovery validates the exact CLI-only artifact set; schema-v3
   full bundles and direct `update-internal`/`set-bin internal` retain their
   prior full-parity contract.
4. Managed internal shell execution validates the CLI generation before exec,
   ignores stale App parity for that generation, and retains functional shared
   Plugin/Skill preflight.
5. Official App bytes, Home, binding, LaunchAgent, global state, wrapper, and
   parity artifacts are outside CLI-only promotion; a running official App
   does not need to exit for that promotion.
6. Selecting internal for App from an unverified generation fails at public and
   deepest transaction boundaries before backup or App mutation. A successful
   full rebind atomically clears the CLI-only readiness fields.
7. Verify, Doctor, and status collect internal parity only when App is owned by
   internal. Verify and Doctor carry one immutable active-selection snapshot;
   parity repair performs an exact active-record CAS inside the store mutation
   lock before parity preparation.
8. `split --keep-version` continues to skip internal update detection and
   promotion.

## TDD and Review Closure

Initial public RED coverage exposed the missing CLI-only transaction scope,
promotion parser/routing, generation validation, App guard, and split
diagnostic ownership. Focused GREEN coverage closed binary/manifest commit and
rollback, exact candidate version/digest checks, stale parity independence,
shared preflight, pre-mutation App rejection, split runtime smoke, and unchanged
full-rebind behavior.

Independent standards review then found one blocking concurrent-selection
race: verify and Doctor could reread `active.json` and mix App owners, and a
safe parity repair could act on the earlier owner. OpenSpec design/spec/task
4.3 were updated before repair. Three focused RED tests reproduced verify owner
mixing, Doctor multi-read behavior, and full-rebind preparation after selection
drift. The single-snapshot plus locked exact-payload CAS implementation turned
all three GREEN. Both standards and spec reviewers reran the focused matrix and
returned PASS with no residual blocker or scope expansion.

## Fresh Final Test Matrix

All commands used Python 3.12 because the repository requires Python 3.11+
features and the system `python3` is 3.9.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_runtime_binding \
  scripts.test_codex_transaction \
  scripts.test_codex_verify
```

Result: 382 tests in 154.731 seconds, all passed.

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
```

Result: 224 tests in 292.917 seconds, all passed.

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py
```

Result: 138 tests in 312.531 seconds, all passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_config_document \
  scripts.test_codex_official_release \
  scripts.test_codex_parity \
  scripts.test_codex_protocol_config \
  scripts.test_codex_shared_configuration \
  scripts.test_codex_shared_lifecycle \
  scripts.test_codex_shared_materialization
```

Result: 246 tests in 32.055 seconds, all passed.

Final aggregate: 990 tests in 792.234 seconds, all passed.

## Broad-Suite Incidental Guards

- INC-020: one generated-wrapper protocol fixture still expected an arbitrary
  `shared-support.txt` entry to cross homes. The fixture now uses allowlisted
  `AGENTS.md`; production sharing ownership did not change. Focused and full
  support matrices pass.
- INC-021: the immutable-promotion success helper used a test-only 1.0-second
  candidate smoke budget instead of the production 5.0-second default and
  flaked twice under cumulative load. A deterministic 1.2-second successful
  candidate reproduced the timeout RED. The test helper now uses the existing
  production budget, while a separate 0.05-second explicit-timeout guard proves
  timeout rejection remains active. The focused five-test matrix and final
  138-test update/release suite pass; production code did not change for this
  guard.

## Static and Control-Plane Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 -c \
  'from pathlib import Path; files=sorted(Path("scripts").glob("*.py")); [compile(p.read_bytes(), str(p), "exec") for p in files]; print(f"compiled={len(files)}")'
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
bash -n scripts/package-release.sh
python3.12 -m json.tool evals/evals.json >/dev/null
openspec validate internal-cli-only-runtime --strict --no-interactive
openspec validate --all --strict --no-interactive
python3.12 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.4.0/scripts/validate_workflow_state.py --repo . --json
git diff --check
```

Results:

- 61 Python sources compiled in memory without new bytecode.
- Five Shell entrypoints and eval JSON passed syntax validation.
- The target change passed strict validation; repository-wide strict OpenSpec
  passed 22/22.
- DevFlow workflow validation returned `ok=true`, zero issues, and only the
  pre-existing INC-018 warning that `AGENTS.md` lacks Project-Directed
  Implementation Readiness guidance. No migration or dependency activation was
  authorized or applied.
- `git diff --check` passed.
- `dev/scripts/codex_auto_update_plugins_skills.py` is absent, so no local
  reference check or cache/project migration apply was available or attempted.

## Release-Counterpart Skill Evaluation

The unchanged current `SKILL.md` is byte-identical to the isolated release
counterpart used for Plugin Eval:

```text
source SKILL SHA-256: 8568c96b9239fa39c88414a7e59c633c7a0f5d529ea8ffdc9f69a871f0d4dc81
counterpart SKILL SHA-256: 8568c96b9239fa39c88414a7e59c633c7a0f5d529ea8ffdc9f69a871f0d4dc81
Plugin Eval: 58/100, grade D, 2 fail, 3 warn, 2 info
```

The findings are the pre-existing INC-012 static token-budget, top-level
README, historical Python complexity/line-length, and coverage-artifact
classes. Fixing them requires a separate benchmark-backed package/Skill
architecture change and is not necessary for this runtime completion contract.
The earlier isolated archive is evaluation evidence only; it is not claimed as
a deployment artifact for the later code-only selection-race repair.

## Residual Risk and Next Gate

- Internal App readiness is intentionally `unverified`; attempts to select it
  are blocked until a separately authorized full-parity rebind succeeds.
- Current installed Codex Switch was not updated, and no candidate was promoted.
- Manual live validation requires a separate install/update authorization. A
  source-tree preview may be run first; the official App may remain running for
  CLI-only promotion, while any separately derived App `rebind` action retains
  its own stopped-App requirement.
- Archive, commit, push, release, migration, cache refresh, and cleanup remain
  separate Human Gates.
