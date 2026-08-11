# Internal Installer Live Recovery

Timestamp: 2026-07-28T16:20:06+08:00

Active change: `internal-official-feature-parity`

Progress: 74/84

Completed: task 8.3A.4

## Recovery

The exact `.zshrc` target and three exact failed candidate directories matched
their diagnosed text, hash, type, owner, mode, inode, contents, and version
before mutation.

Recovery directory:

`/Users/cY/.codex-switch/backups/20260728T161949+0800-installer-side-effect-recovery`

It is mode 0700 and contains:

- `.zshrc.before-installer-side-effect-recovery`, mode 0600, SHA-256
  `7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807`;
- `.codex-internal-update-cb601999175c954128459e72`;
- `.codex-internal-update-8c8e097f976e26a0ed76655a`; and
- `.codex-internal-update-a17a48054bfaf3fedbae231a`.

The candidate directories retained their original mode-0700 inodes. Nothing
was deleted.

The live `.zshrc` remains mode 0600 and its diff removes only the three
confirmed installer blocks. Its new SHA-256 is
`8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4`.
The plugin app-server PATH and canonical codex-switch shell block remain. A
clean-environment interactive zsh resolves bare `codex` to
`/Users/cY/.codex-switch/bin/codex` and reports the active official
`codex-cli 0.146.0-alpha.3.1`.

## Next Action

Execute task 8.3A.5 only: install the exact verified repository source, verify
immutable installed identity, run one supported internal update/rebind/switch,
perform one bounded ChatGPT quit/reopen, and attest configuration, plugin, and
runtime ownership. Stop before provider-backed Desktop work and every excluded
effect.
