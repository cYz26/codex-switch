# Internal Installer Isolation RED

Date: 2026-07-28
Change: `internal-official-feature-parity`
Task: 8.3A.1
Progress: 71/84

The public `codex_env_setup update-internal` seam ran a harmful fake trusted
installer that writes `$CODEX_HOME/config.toml` and appends its candidate to
`$HOME/.zshrc` when absent from PATH.

```text
Python 3.12: 1 test, 1 failure, 0 errors
command return: 0
candidate: created
expected live config: live-config-sentinel = true
observed live config: installer-default-config
```

This is the exact intended RED. No production code or live workstation state
changed. Next: implement only private installer environment and exact normal
exit cleanup, then rerun the named test.
