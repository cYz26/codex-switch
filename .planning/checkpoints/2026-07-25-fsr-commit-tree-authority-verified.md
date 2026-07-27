# Fail-Safe Commit Tree Authority Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.5`
Progress: `31/38`

## Result

Release validation now reads the exact target Git commit tree and blob bytes.
It compares the release source file set, contents, and executable-bit class
against that commit even when index flags hide worktree drift. `git status` is
no longer release authority.

Strict bundle validation now:

- excludes only the package-root `bundle-manifest.json`;
- treats a nested file with that name as normal protected payload;
- rejects symlinks and special files before archive validation;
- requires package-root mode `0755`;
- compares the complete package file/directory set and evidence.

Explicit historical routing remains separate from strict new-format routing.
Only trusted `v0.1.12` and `v0.1.13` layouts may omit the manifest, and their
archive canonicalization remains deterministic.

The final bundle-module SHA-256 pinned by `install.sh` and `run.sh` is:

`a301822fc5347c2225c4a73c9be2f31a05bebf4fac2c80083cd4f3698f49c9b3`

## RED / GREEN

RED produced six failures:

- nested manifest payload omitted;
- FIFO not rejected;
- package-root `0777` accepted;
- `assume-unchanged` content drift accepted;
- `skip-worktree` content drift accepted;
- hidden executable-bit drift accepted.

GREEN:

- Python 3.12.13 bundle/asset/bootstrap group: 33/33 passed.
- System Python 3.9.6 bundle/asset/bootstrap group: 33/33 passed.
- strict `fail-safe-update-release` OpenSpec validation: passed.
- dual-runtime compile, Bash syntax, and `git diff --check`: passed.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 6.6 by RED against exact remote semantic-tag resolution, trusted
tooling checkout, credential persistence, and repeated remote-tag identity
checks.
