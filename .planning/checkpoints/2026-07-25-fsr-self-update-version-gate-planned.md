# FSR Same-Version Self-Update Repair Planned

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `2.7`

## Incident

Installed strict `0.1.13` and trusted GitHub latest `v0.1.13` are the same
version. The current wrapper downloads and validates the historical release
asset before comparing versions, so the asset's missing strict release module
produces `source_invalid` and a non-blocking sync warning.

## Target State

- Resolve explicit or fixed default-latest trusted release metadata first.
- Return `already up to date` before workdir creation when remote is equal to
  or older than current.
- Pin a newer default-latest tag and retain complete strict candidate
  validation and immutable promotion.
- Keep custom unversioned source/tarball overrides on the strict validation
  path.
- Preserve existing Python 3.11+ fail-before-write behavior.
- Prohibit keepalive-capable `launchctl submit` in rollout restart procedures.

## Verification

1. RED same-version and older malformed legacy candidate tests.
2. GREEN focused self-update tests, including newer malformed fail-closed.
3. Existing Python auto-selection and old-Python fail-before-write tests.
4. Full update/release and profile suites, strict OpenSpec, Bash syntax, and
   `git diff --check`.
5. Supported local-source reinstall and normal installed `status` without
   `source_invalid` or the sync-failed warning.

## Boundaries

No App restart, commit, push, tag, release publication, archive, dependency
change, destructive cleanup, plugin mutation, or internal backend update is
authorized by this repair.
