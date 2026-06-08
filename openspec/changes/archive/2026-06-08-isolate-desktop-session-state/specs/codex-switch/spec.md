# Specification Delta: Isolate Desktop Session State

## ADDED Requirements

### Requirement: Profile Desktop runtime state isolation

The internal Codex Desktop wrapper SHALL keep response/session runtime state
profile-local instead of symlinking it from the live shared `CODEX_HOME`.

#### Scenario: Existing live state symlinks are removed

- GIVEN the internal profile app home contains generated symlinks for runtime
  state paths that target live `CODEX_HOME`
- WHEN the internal Desktop wrapper starts
- THEN those stale symlinks are removed before Codex launches
- AND no live `auth.json` is copied into the app home.

#### Scenario: Future runtime state links are not created

- GIVEN live `CODEX_HOME` contains session, history, log, temporary, browser, or
  sqlite runtime state
- WHEN the internal Desktop wrapper prepares the profile app home
- THEN those runtime state entries are not symlinked into the profile app home
- AND stable non-auth support assets may still be shared.

#### Scenario: Shared config overlay is preserved

- GIVEN Codex Desktop writes non-auth shared configuration into the profile app
  home
- WHEN the internal Desktop wrapper starts again
- THEN non-auth shared configuration is folded back into live shared
  `config.toml`
- AND profile-specific model/auth configuration remains in the generated app
  home config.
