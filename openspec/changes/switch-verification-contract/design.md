# Switch verification contract design

## Skill Routing Ledger

- request kind: behavior implementation for `codex-switch` profile switching.
- capability-research: used; local CLI help, status, doctor, plugin repair,
  running app detection, and OpenSpec state were inspected.
- brainstorming: used in the preceding design discussion; user approved the
  CLI-first verification direction and requested implementation.
- writing-plans: used; this OpenSpec change owns the executable ledger.
- OpenSpec routing: new follow-up change `switch-verification-contract`.
- TDD routing: required before production code changes.

## Architecture Decisions

1. Verification is a Python command, not a Codex-session feature.
   The direct CLI has access to profile manifests, active records, runtime
   configs, LaunchAgent bindings, running process observations, and plugin
   repair helpers. Codex conversations remain useful for code repair and manual
   review, but machine-state validation belongs in `codex-switch`.

2. Verification complements doctor instead of replacing it.
   `doctor` keeps broad store/profile health checks. `verify <profile>` adds
   target-profile invariants and switch acceptance semantics, including
   official provider contamination and plugin support snapshot durability.

3. Safe repair is bounded.
   Verification can refresh plugin support snapshots and call the existing
   catalog-aware plugin repair path. It does not kill Desktop processes, delete
   caches, disable unavailable selectors, or invent profile configuration.

4. Runtime smoke is explicit.
   Ordinary switches validate local machine state only. Upgrade validation can
   pass `--runtime-smoke`, and deeper model-backed testing can pass
   `--exec-smoke <prompt>`.

## Data Flow

`codex-switch official/internal` performs:

1. dry-run plan
2. update check and login preparation
3. switch mutation
4. plugin repair unless skipped
5. target verification unless skipped
6. doctor unless skipped
7. status unless skipped
8. final result summary

Standalone `verify <profile>` performs:

1. load profile manifest and active record
2. resolve target profile home
3. optionally run safe repair
4. collect target-profile problems
5. optionally run runtime/exec smoke
6. optionally write a JSON report
7. exit non-zero if any problems remain

## Verification Checks

- active profile equals the requested profile.
- active `CODEX_HOME` matches the resolved profile home.
- active shell/app CLI bindings match the profile manifest when they were
  written by the switch.
- runtime `config.toml` exists and is valid TOML.
- `openai-official` runtime config does not contain an internal
  `model_provider` seed.
- plugin support snapshots exist and contain marketplace, plugin, skill, or
  hook support blocks when runtime config contains those blocks.
- running Desktop/app-server observations still agree with the active profile
  where the default Desktop context is being managed.
- optional runtime smoke runs the target profile's configured Codex binary with
  `CODEX_HOME` set to the target profile home.

## Files

- `scripts/codex_switch_verify.py`: new verification command and helpers.
- `scripts/codex_profile_switch.py`: argparse registration for `verify`.
- `scripts/codex-switch`: one-key switch integration and CLI help.
- `scripts/test_codex_profile_switch.py`: red/green regression tests.
- `openspec/changes/switch-verification-contract/specs/codex-switch/spec.md`:
  behavior contract.
- `.planning/STATE.md` and `.planning/verification/...`: evidence after
  validation.

## Rollback

If verification blocks valid legacy workflows, keep the standalone `verify`
command and temporarily gate one-key verification behind `--skip-verify` while
adding a focused regression for the legitimate case.
