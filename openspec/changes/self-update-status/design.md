# Design: Self-Update Status Output

## Approach

The Bash wrapper already owns self-update. The smallest compatible change is to
add status messages inside the existing `maybe_self_update` and
`sync_self_update` paths:

- `maybe_self_update` prints a single check-start line only after eligibility
  and interval gates pass.
- `sync_self_update` prints an up-to-date line when the staged bundle version
  matches the current bundle version.
- Existing sync success and failure warning lines stay unchanged.

All status messages go to stderr so command stdout remains parseable.

## Output Contract

When a check runs:

```text
codex-switch self-update: checking latest release...
```

If no update is needed:

```text
codex-switch self-update: already up to date <version>
```

If a sync is needed, the existing line remains:

```text
codex-switch self-update: synced implementation <old> -> <new>
```

If a sync fails, the existing warning remains:

```text
codex-switch self-update: warning: sync failed; continuing with current implementation
```

## Compatibility

No new flags are needed. Existing controls keep their behavior:

- `--skip-self-update`
- `CODEX_SWITCH_SKIP_SELF_UPDATE=1`
- `CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS`

Skipped invocations remain quiet by default.

## Testing

Regression tests simulate a release-installed wrapper and file URL release
bundles. They assert stderr contains status lines for due checks and remains
quiet when `--skip-self-update` is used.
