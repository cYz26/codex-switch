# Package Verification: SPLIT-NATIVE-CACHE-LIFECYCLE-20260811T123157+0800

## Boundary

This retained, uninstalled release counterpart verifies the final task-13.4
contract after the user assigned Plugin installed-cache lifecycle to the native
backend. It grants no installation, split retry, App action, internal binary
update, direct cache mutation by codex-switch, cleanup, Git, release, archive,
migration, dependency, credential, or destructive authority.

The earlier retained package root
`/private/tmp/codex-switch-native-cache-lifecycle-20260811T122033+0800` was not
overwritten after final source/test edits. Its immutable manifest correctly
rejected reuse with `invalid_existing_bundle`; no cleanup followed. A fresh
Generated Artifact Contract was sealed while the physical root below was
absent.

## Package and Identity

The owner command completed successfully in:

```text
/private/tmp/codex-switch-native-cache-lifecycle-20260811T123157+0800
```

`validate_release_outputs` accepted version `0.1.13`, the 22-path allowlist,
72 files, five manifest directories, file modes, digests, runner, and archive.

```text
payload SHA-256:  3f2852e649537aee05f88f830f853d603ae2fccf3278f8047568507384a048ab
archive SHA-256:  f5c4bc6a37b44512194d1d0104d6aa26a992aa80a5cfa852d1db4b3e7f771a24
manifest SHA-256: 57c320bf8018681d0c05409cebe7f5a0d7e4dad0df0d5edac8a9f56a3f53ab07
README SHA-256:   158df084f9446cb4fed4ab5b3c292dfb5d5690673146261cfa0beb72f994ab95
SKILL SHA-256:    4cbc07a0115b0fd8990ac6c3b4e38340a09ab31ae6eca8427a078326b08ce0f5
```

README, SKILL, `scripts/codex_switch_plugins.py`, and
`scripts/test_codex_shared_materialization.py` are byte-exact with source.

## Package-Local Verification

The package-local shared suites pass 94/94:

```text
shared configuration:   45/45 PASS
shared materialization: 36/36 PASS
shared lifecycle:       13/13 PASS
```

## Release-Counterpart Plugin Eval

The installed Plugin Eval script analyzed this exact isolated package and
returned 54/100, grade F, high static risk: two token-budget failures, four
warnings, and two informational checks. Active budget is 4,684 tokens;
deferred support cost is 1,075,529 tokens. These are the existing INC-012
Skill/package-architecture classes and do not indicate a new cache-lifecycle or
runtime regression. A benchmark-backed Skill/package refactor remains outside
task 13.

## Terminal Receipt

- Owner exit: package validation, source/package identity, package-local tests,
  and release-counterpart Plugin Eval completed.
- Terminal disposition: `RETAIN`.
- Cleanup complete: false; cleanup was not authorized.
- Installation/promotion/live activation: not run from this counterpart.
