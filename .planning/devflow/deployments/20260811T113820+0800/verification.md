# Package Verification: SPLIT-BACKEND-MANAGED-20260811T113820+0800

## Boundary

This is the retained, uninstalled release counterpart for
`independent-app-cli-profiles` task 13.3. It grants no installation, split,
internal update, App action, cache cleanup, release, archive, Git, migration,
or destructive authority.

## Package and Identity

The owner command completed inside the absent-at-seal physical root:

```text
/private/tmp/codex-switch-backend-managed-repair-20260811T113820+0800
```

`validate_release_outputs` accepted version `0.1.13`, the 22-path allowlist,
71 files, five directories, modes, digests, runner, and archive. Identity:

```text
payload SHA-256:  23477b064dca4ca8a1e25b45c78c1acb94d95d3c59e8e0080889f135443428f1
archive SHA-256:  0b18c7a1617a376443ee9bcb20d086cd030766c1349c242bc1c34ce8ea15ed48
manifest SHA-256: b7c360d0ab7b4467609d03b5044f0337c16d6f4fbba9098d103ca541062084a5
README SHA-256:   33455a6bcc742ad185ed833986b4d535a7f2a8a66cd7a3a546e5022569e4d791
SKILL SHA-256:    cdfe03a74e1e49ed775281c183caa8a431433c61b6970db206bd34e9b94b72be
```

README, SKILL, `scripts/codex_switch_plugins.py`, and
`scripts/test_codex_shared_materialization.py` are byte-exact with source.
Package-local shared configuration/materialization/lifecycle tests pass 93/93.

## Release-Counterpart Plugin Eval

The installed Plugin Eval entrypoint analyzed the isolated release root and
returned 54/100, grade F, high static risk: two token-budget failures, four
warnings, and two informational checks. The 4,592-token invoke estimate,
1,074,555-token deferred estimate, progressive-disclosure/top-level README,
historical Python complexity/long-line, and unavailable-coverage findings are
the existing INC-012 package-architecture class. Fixing them requires a
benchmark-backed Skill/package refactor outside task 13.

## Terminal Receipt

- Owner exit: package validation, identity, package-local tests, and Plugin
  Eval completed.
- Terminal disposition: `RETAIN`.
- Cleanup complete: false; cleanup was not authorized.
- Installation/promotion/live activation: not run from this counterpart.
