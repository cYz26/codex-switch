# Deployment Verification: SPLIT-SHORTCUT-20260810T120157+0800

## Outcome

- Status: `VERIFIED_AND_INSTALLED`.
- Generated-artifact disposition: `RETAIN`.
- Live profile activation: not performed; remains behind
  `SPLIT-DEPLOY-APP-RESTART`.
- Cleanup: not authorized and not performed.

## Package Identity

```text
archive:
  /private/tmp/codex-switch-shortcut-20260810T120157+0800/codex-switch.tar.gz
archive SHA-256:
  c38a619fc2ccb9ed38eec161f54adcf793b2806313a2248b40c999a1204e174b
manifest SHA-256:
  02c9598a5c76297c4d20bf51dbc6aa40ba0779dc9bc60919b8d0481806d07012
payload SHA-256:
  b88326ff747278543b94176b00816f8c9b4e692afbf31fee5a490da107cff49d
version: 0.1.13
required paths: 22
files: 71
directories: 5
```

The wrapper, README, SKILL, and complete profile test file are byte-exact
between source and package. The packaged shortcut preview passes 1/1 without
checkout code or workstation-state mutation.

## Test and Review Evidence

```text
focused shortcut matrix: 10/10 passed in 27.496s
complete profile suite: 219/219 passed in 316.252s
adjacent update/release: 4/4 passed in 9.317s
packaged preview: 1/1 passed in 2.570s
Bash syntax: 5/5 entrypoints passed
changed Python test AST: passed
active strict OpenSpec: passed
repository strict OpenSpec: 20/20 passed
git diff --check: passed
```

Final release-counterpart Plugin Eval reports 58/100, grade D, high static
risk, with two budget failures, three warnings, and two informational checks.
The 43-token trigger, 3,667-token invoke cost, and 1,026,059-token deferred
support tree are recorded as existing INC-012 `DEFER_AND_CONTINUE`; the
shortcut introduced no separate structural finding.

## Installed Identity and Non-Claim

```text
current:
  releases/b88326ff747278543b94176b00816f8c9b4e692afbf31fee5a490da107cff49d
rollback:
  releases/e6caa91b8b456bf16083b81d76042637d1c3aaa48ca78f072dc8a0eaed2e4983
installed/source wrapper SHA-256:
  6132984ce3ad62394ee17b3e4c1888194eaa3f9ba9303c988d25aad69e82d6e0
installer staging residue: none
installed Doctor: passed
```

Installed help exposes `split` and `--keep-version`. Read-only status remains
CLI/App `openai-official`; ChatGPT pid 2375 and official app-server pid 2920
are unchanged. `verify internal --repair=none` exits 1 before activation with
active selection/home/binary mismatches, `binding.observation.active_stale`,
and `parity.receipt.missing`. No App stop/restart, live split, internal update,
parity repair, credential, Git, release, archive, migration, or cleanup effect
occurred.

## Workflow and Local Reference Audit

The DevFlow 0.4.0 authority-gate receipt replayed successfully. Workflow state
validation reports `ok=true` with no issues. Its one warning says `AGENTS.md`
is missing `Project-Directed Implementation Readiness`; the read-only local
reference audit likewise reports broader project migration pending while the
installed DevFlow cache itself `matches-source`. INC-018 defers both to a
separately authorized project refresh/migration. No apply path ran.
