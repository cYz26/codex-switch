# Internal Installer Isolation — Approved Scheme A

Date: 2026-07-28
Change: `internal-official-feature-parity`
Progress after plan expansion: 70/84
Next item: 8.3A.1

## Target State

The trusted internal installer runs only inside a private disposable
environment. It cannot mutate live Codex config, shell startup state, active
profile, manifest, wrapper, bound binary, or runtime bundle during candidate
preparation. A retained failed candidate never enters live PATH. The three
confirmed pre-fix candidates and shell blocks are repaired precisely into a
recoverable backup before one controlled internal retry.

## Completion Contract

- Harmful fake-installer RED becomes GREEN on Python 3.12 and system Python
  3.9.
- Private `HOME`/`CODEX_HOME` and candidate-first child PATH are observed.
- Live shell/config sentinels remain byte/mode-identical.
- Scratch is mode 0700 and absent after every supported exit.
- Focused/full/static/OpenSpec/workflow/package/diff validation passes.
- `.zshrc` and candidate recovery targets match exact preflight identity before
  mutation and remain recoverable afterward.
- One exact-source internal update/rebind/switch and bounded ChatGPT restart
  prove complete config/plugins and manifest/wrapper/App/proxy/app-server
  ownership of the configured internal binary.

## Write and Effect Boundary

Production/test writes are limited to `scripts/codex_env_setup` and
`scripts/test_codex_update_release.py`; `scripts/codex-switch` is conditional
on a newly recorded wrapper-seam RED. Canonical OpenSpec/control-plane updates
are main-owned. Live effects are limited to the exact backup, three shell
blocks, three candidate moves, supported install/profile/runtime artifacts, and
one restart.

No proxy behavior, plugin refresh, Desktop global-state allowlist,
credential/identity migration, dependency, legacy skill migration/cleanup,
destructive deletion, provider-backed Desktop task, Git, release, or archive
effect is in scope.

## Execution Ledger

- [ ] 8.3A.1 harmful-installer RED
- [ ] 8.3A.2 hermetic helper GREEN
- [ ] 8.3A.3 source/package validation
- [ ] 8.3A.4 exact recoverable workstation repair
- [ ] 8.3A.5 controlled install/update/rebind/switch/restart verification

## Resume Command

Resume from task 8.3A.1 in
`openspec/changes/internal-official-feature-parity/tasks.md`. Re-attest all live
targets immediately before task 8.3A.4; never reuse only this checkpoint as
mutation authority.
