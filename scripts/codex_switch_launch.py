from __future__ import annotations

import os
import plistlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from codex_switch_core import APP_CLI_ENV, Store, SwitchError, atomic_write, run_quiet


@dataclass(frozen=True)
class _DesktopBindingObservation:
    gui_env: str | None
    service_loaded: bool


class _DesktopBindingAdapter:
    def __init__(
        self,
        store: Store,
        *,
        runner: Callable[[list[str]], tuple[int, str]] = run_quiet,
        uid_provider: Callable[[], int] = os.getuid,
    ) -> None:
        self.store = store
        self.runner = runner
        self.uid_provider = uid_provider
        self._setenv_attempted = False
        self._bootout_succeeded = False
        self._bootstrap_succeeded = False
        self._effect_journal: object | None = None

    @staticmethod
    def _observation_state(
        observation: _DesktopBindingObservation,
    ) -> dict[str, object]:
        return {
            "gui_env": observation.gui_env,
            "service_loaded": observation.service_loaded,
        }

    def bind_effect_journal(self, journal: object) -> None:
        if not callable(getattr(journal, "begin", None)) or not callable(
            getattr(journal, "complete", None)
        ):
            raise SwitchError("Desktop effect journal is invalid")
        self._effect_journal = journal

    def _begin_effect(
        self,
        phase: str,
        before_state: dict[str, object],
        planned_after_state: dict[str, object],
    ) -> object | None:
        journal = self._effect_journal
        if journal is None:
            return None
        begin = getattr(journal, "begin")
        return begin(
            kind="desktop",
            phase=phase,
            before_state=before_state,
            planned_after_state=planned_after_state,
        )

    def _complete_effect(
        self,
        effect: object | None,
        observed_after_state: dict[str, object],
    ) -> None:
        if effect is None:
            return
        complete = getattr(self._effect_journal, "complete")
        complete(effect, observed_after_state=observed_after_state)

    def observe(
        self,
        *,
        skip_launchctl: bool = False,
    ) -> _DesktopBindingObservation:
        if skip_launchctl:
            return _DesktopBindingObservation(gui_env=None, service_loaded=False)
        env_code, env_output = self.runner(
            ["/bin/launchctl", "getenv", APP_CLI_ENV]
        )
        gui_env = env_output if env_code == 0 and env_output else None
        domain = f"gui/{self.uid_provider()}"
        service_code, _ = self.runner(
            ["/bin/launchctl", "print", f"{domain}/{self.store.launch_agent_label}"]
        )
        return _DesktopBindingObservation(
            gui_env=gui_env,
            service_loaded=service_code == 0,
        )

    def apply(
        self,
        app_cli_path: Path,
        observation: _DesktopBindingObservation,
        *,
        skip_launchctl: bool,
    ) -> None:
        if skip_launchctl:
            return
        current_state = self._observation_state(observation)
        setenv_state = {
            "gui_env": str(app_cli_path),
            "service_loaded": observation.service_loaded,
        }
        setenv_effect = self._begin_effect(
            "desktop_setenv",
            current_state,
            setenv_state,
        )
        self._setenv_attempted = True
        code, output = self.runner(
            ["/bin/launchctl", "setenv", APP_CLI_ENV, str(app_cli_path)]
        )
        if code != 0:
            raise SwitchError(f"launchctl setenv failed: {output}")
        self._complete_effect(setenv_effect, setenv_state)
        current_state = setenv_state
        if observation.service_loaded:
            domain = f"gui/{self.uid_provider()}"
            bootout_state = {
                "gui_env": str(app_cli_path),
                "service_loaded": False,
            }
            bootout_effect = self._begin_effect(
                "desktop_bootout",
                current_state,
                bootout_state,
            )
            code, output = self.runner(
                [
                    "/bin/launchctl",
                    "bootout",
                    domain,
                    str(self.store.launch_agent_path),
                ]
            )
            if code != 0:
                raise SwitchError(f"launchctl bootout failed: {output}")
            self._bootout_succeeded = True
            self._complete_effect(bootout_effect, bootout_state)
            current_state = bootout_state
        domain = f"gui/{self.uid_provider()}"
        bootstrap_state = {
            "gui_env": str(app_cli_path),
            "service_loaded": True,
        }
        bootstrap_effect = self._begin_effect(
            "desktop_bootstrap",
            current_state,
            bootstrap_state,
        )
        code, output = self.runner(
            [
                "/bin/launchctl",
                "bootstrap",
                domain,
                str(self.store.launch_agent_path),
            ]
        )
        if code != 0:
            raise SwitchError(f"launchctl bootstrap failed: {output}")
        self._bootstrap_succeeded = True
        self._complete_effect(bootstrap_effect, bootstrap_state)

    def rollback(
        self,
        observation: _DesktopBindingObservation,
        *,
        skip_launchctl: bool,
    ) -> None:
        if skip_launchctl or not self._setenv_attempted:
            return
        self.reconcile(observation, skip_launchctl=skip_launchctl)

    def reconcile(
        self,
        observation: _DesktopBindingObservation,
        *,
        skip_launchctl: bool,
    ) -> None:
        if skip_launchctl:
            return
        domain = f"gui/{self.uid_provider()}"
        rollback_errors: list[str] = []
        current = self.observe(skip_launchctl=False)
        if current.service_loaded:
            code, output = self.runner(
                [
                    "/bin/launchctl",
                    "bootout",
                    domain,
                    str(self.store.launch_agent_path),
                ]
            )
            if code != 0:
                rollback_errors.append(
                    f"launchctl rollback bootout failed: {output}"
                )
        if observation.service_loaded:
            code, output = self.runner(
                [
                    "/bin/launchctl",
                    "bootstrap",
                    domain,
                    str(self.store.launch_agent_path),
                ]
            )
            if code != 0:
                rollback_errors.append(
                    f"launchctl service rollback failed: {output}"
                )
        if observation.gui_env is None:
            command = ["/bin/launchctl", "unsetenv", APP_CLI_ENV]
        else:
            command = [
                "/bin/launchctl",
                "setenv",
                APP_CLI_ENV,
                observation.gui_env,
            ]
        code, output = self.runner(command)
        if code != 0:
            rollback_errors.append(
                f"launchctl GUI environment rollback failed: {output}"
            )
        if rollback_errors:
            raise SwitchError("; ".join(rollback_errors))
        observed = self.observe(skip_launchctl=False)
        if observed != observation:
            raise SwitchError(
                "Desktop rollback observation mismatch: "
                f"expected={observation!r}, observed={observed!r}"
            )


def validate_executable_path(raw_path: str, field_name: str) -> Path:
    if not raw_path:
        raise SwitchError(f"Profile manifest has no {field_name}.")
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        raise SwitchError(f"{field_name} must be an absolute path: {raw_path}")
    if not path.exists():
        raise SwitchError(f"{field_name} does not exist: {path}")
    if not path.is_file():
        raise SwitchError(f"{field_name} is not a file: {path}")
    if not os.access(path, os.X_OK):
        raise SwitchError(f"{field_name} is not executable: {path}")
    return path


def launch_agent_payload(label: str, app_cli_path: Path) -> bytes:
    payload = {
        "Label": label,
        "ProgramArguments": [
            "/bin/launchctl",
            "setenv",
            APP_CLI_ENV,
            str(app_cli_path),
        ],
        "RunAtLoad": True,
    }
    return plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False)


def write_app_cli_launch_agent(
    store: Store,
    app_cli_path: str,
    skip_launchctl: bool,
) -> Path:
    path = validate_executable_path(app_cli_path, "app_cli_path")
    atomic_write(
        store.launch_agent_path,
        launch_agent_payload(store.launch_agent_label, path),
        mode=0o644,
    )
    if skip_launchctl:
        return store.launch_agent_path

    code, output = run_quiet(["/bin/launchctl", "setenv", APP_CLI_ENV, str(path)])
    if code != 0:
        raise SwitchError(f"launchctl setenv failed: {output}")

    domain = f"gui/{os.getuid()}"
    run_quiet(["/bin/launchctl", "bootout", domain, str(store.launch_agent_path)])
    code, output = run_quiet(["/bin/launchctl", "bootstrap", domain, str(store.launch_agent_path)])
    if code != 0:
        raise SwitchError(f"launchctl bootstrap failed: {output}")
    return store.launch_agent_path


def read_launch_agent_cli_path(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        payload = plistlib.loads(path.read_bytes())
    except Exception as exc:
        return f"<invalid plist: {exc}>"
    args = payload.get("ProgramArguments", [])
    if (
        isinstance(args, list)
        and len(args) >= 4
        and args[1] == "setenv"
        and args[2] == APP_CLI_ENV
    ):
        return str(args[3])
    return "<not managed by codex-switch>"
