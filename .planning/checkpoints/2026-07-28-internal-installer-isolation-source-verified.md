# Internal Installer Isolation Source Verified

Timestamp: 2026-07-28T16:17:46+08:00

Active change: `internal-official-feature-parity`

Progress: 73/84

Completed: tasks 8.3A.1-8.3A.3

## Result

The trusted internal installer now runs with a private identity-bound
mode-0700 root, private `HOME` and `CODEX_HOME`, candidate-first child PATH,
bounded signal forwarding/reaping, and exact scratch cleanup. Harmful-installer
tests prove live config/shell sentinels and modes are unchanged on success,
ordinary failure, initialization failure, `HUP`, `INT`, and `TERM`.

Final serial update/release verification passes 132/132 on Python 3.12 and
132/132 on system Python 3.9. Active/all strict OpenSpec, AI-plan lint, pinned
workflow validation, Bash/dual-runtime AST, isolated package validation,
source/package identity, diff/write-set, and residue checks pass.

The isolated package root is
`/private/tmp/codex-switch-installer-isolation.rZHFJ2`. Its packaged
`scripts/codex_env_setup` is byte-identical to source with SHA-256
`0e7334481204785517ac68ac4a9086b77cc9b1136718fbc15234459b25c61bd9`.

The real `.zshrc` remains mode 0600 with SHA-256
`7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807`.
No live workstation mutation occurred during tasks 8.3A.1-8.3A.3.

## Next Action

Execute task 8.3A.4 only: re-attest the exact three shell blocks and exact
three mode-0700 candidate directories, create a private timestamped recovery
backup, copy `.zshrc` with digest/mode evidence, remove only the confirmed
blocks, and move only the confirmed directories. Stop on any drift; delete
nothing.

## Scope Boundary

No proxy, plugin refresh, global-state allowlist, credential/identity,
dependency, legacy layout, destructive cleanup, provider-backed Desktop task,
Git, release, or archive effect is authorized.
