# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Automatic release tag gate

The system SHALL automatically publish a new patch release when
release-relevant changes land on `main`.

#### Scenario: Main push with runtime changes publishes a patch release

- GIVEN the latest release tag is `v0.1.3`
- AND `main` contains release-relevant changes after that tag
- WHEN the automatic release workflow runs on the `main` push
- THEN it runs release-equivalent verification
- AND updates `VERSION` to `0.1.4`
- AND commits the version bump to `main`
- AND creates and pushes tag `v0.1.4`
- AND publishes `install.sh`, `run.sh`, and `codex-switch.tar.gz` as release
  assets for `v0.1.4`.

#### Scenario: Main push with planning-only changes does not publish

- GIVEN the latest release tag is `v0.1.3`
- AND the only changes after that tag are under `.planning/**`,
  `openspec/**`, or docs-only files
- WHEN the automatic release workflow runs on the `main` push
- THEN it reports that no release is required
- AND it does not update `VERSION`
- AND it does not create a tag
- AND it does not publish release assets.

#### Scenario: Existing tag release workflow remains available

- GIVEN a `v*` tag is pushed outside the automatic `main` release workflow
- WHEN the existing release workflow runs
- THEN it verifies the tagged source
- AND publishes `install.sh`, `run.sh`, and `codex-switch.tar.gz` for that tag.

#### Scenario: Bot-created tag publication does not rely on recursive workflow triggers

- GIVEN the automatic release workflow uses `GITHUB_TOKEN`
- WHEN it creates and pushes the next `v*` tag
- THEN release asset publication happens in the same workflow run
- AND does not require the bot-created tag push to trigger a second workflow.
