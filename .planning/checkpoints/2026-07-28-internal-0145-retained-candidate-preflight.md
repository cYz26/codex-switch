# Internal 0.145 Retained-Candidate Promotion Preflight

Timestamp: 2026-07-28T18:18:00+08:00

Active change: `internal-official-feature-parity`

Status: `PROMOTION_READY`

## Installed Source

The supported exact-source install completed and promoted:

```text
/Users/cY/.local/share/codex-switch/releases/
  6a23d04f8408681c26ed116583b208699f4b8fba4357162717befe7af8c1f132
version: 0.1.13
strict candidate validation: passed
```

The immutable digest equals the release directory name. Manifest, 66 files,
modes, imports, command smoke, and source payload validate.

## Retained Candidate

```text
root:
  /Users/cY/.local/bin/.codex-internal-update-6efc91d3f6359549077f8a00
root mode/uid/gid/dev/inode:
  0700 / 502 / 20 / 16777233 / 57343443
candidate:
  codex-cli 0.145.0
candidate mode/inode/size:
  0755 / 57343496 / 276128448
candidate SHA-256:
  a34c872ccaaa02b6823bdf75138826a17177b91117a1920cedec9834772197b8
codesign strict verification:
  passed
candidate siblings:
  codex, codex-code-mode-host, rg
```

The root and executable are non-symlinks. No second installer or download ran.

## Last-Known-Good and Transaction State

```text
bound:
  /Users/cY/.local/bin/codex
bound version:
  codex-cli 0.144.6
bound mode/inode/size:
  0755 / 43110921 / 265412352
bound SHA-256:
  410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6
fixed backup:
  /Users/cY/.local/bin/.codex-internal-backup (absent)
runtime marker:
  /Users/cY/.codex-switch/.runtime-binding-rebind.json (absent)
```

## Fresh Live Inputs

```text
official reference: codex-cli 0.146.0-alpha.3.1
official reference SHA-256:
  6d8be49e49751554df16572369e636cbe02c84b208cad3dc35528c846eeca223
bundle id/version:
  com.openai.codex / 26.721.41059
.zshrc SHA-256:
  8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
official live config SHA-256:
  ca02832ff0a2b8829f976e3dcb13a18b725fd61be8eeffd0a1f0d10ee52d2ca3
internal managed-home config SHA-256:
  59a14e0e108e17b3488871d8880255bae78c85d9cad1a05778093ba638db31f1
internal manifest SHA-256:
  84392af08cca42c8ef9801ec5a8cb8af5e33e662b1cd1993cfbac98d5a693e3a
internal launcher SHA-256:
  a825716d4c7f9d633d86a87c3e893f9c3fbecbf2dd082e1838aad602c74230dc
active record SHA-256:
  0d7981f9f2f29c23f511f182888f3e848226716c179ffd1e90a8370cba18c671
clean interactive zsh codex:
  /Users/cY/.codex-switch/bin/codex
```

ChatGPT main pid 46110 currently owns bundled official app-server pid 46504.
A separate VS Code extension app-server pid 1890 causes the broad read-only
status collector to print a backend-mismatch row; it is a different host and is
not promotion authority. The inherited task shell also has the plugin
app-server directory before the shim, while a clean interactive zsh resolves
the repaired canonical shim.

## Exact Promotion Route

Invoke the installed immutable
`current/scripts/codex_profile_switch.py promote-internal-update` seam with:

- store `/Users/cY/.codex-switch`;
- bound `/Users/cY/.local/bin/codex`;
- retained candidate
  `/Users/cY/.local/bin/.codex-internal-update-6efc91d3f6359549077f8a00/codex`;
- fixed absent backup `/Users/cY/.local/bin/.codex-internal-backup`;
- target `0.145.0`.

This is the exact seam the public update wrapper calls after installer success.
Do not invoke `update-internal`; doing so would allocate/download a second
candidate.
