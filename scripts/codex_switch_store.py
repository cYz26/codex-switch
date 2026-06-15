from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from codex_switch_constants import MANAGED_FILES, SwitchError
from codex_switch_io import ensure_private_dir, read_json


PROFILE_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def validate_profile_name(name: str) -> None:
    if not PROFILE_RE.match(name):
        raise SwitchError(
            f"Invalid profile name {name!r}. Use letters, numbers, '.', '_' or '-'."
        )


class Store:
    def __init__(
        self,
        root: Path,
        official_codex_home: Path | None = None,
        launch_agent_path: Path | None = None,
        launch_agent_label: str = "",
        live_codex_home: Path | None = None,
        official_codex_home_source: str = "default",
        internal_codex_home: Path | None = None,
        internal_codex_home_source: str = "default",
    ) -> None:
        if official_codex_home is None:
            official_codex_home = live_codex_home
        if official_codex_home is None:
            raise SwitchError("official_codex_home is required")
        if launch_agent_path is None:
            raise SwitchError("launch_agent_path is required")
        self.root = root
        self.official_codex_home = official_codex_home
        self.official_codex_home_source = official_codex_home_source
        self.internal_codex_home = internal_codex_home
        self.internal_codex_home_source = internal_codex_home_source
        self.live_codex_home = official_codex_home
        self.launch_agent_path = launch_agent_path
        self.launch_agent_label = launch_agent_label
        self.profiles_dir = root / "profiles"
        self.backups_dir = root / "backups"
        self.bin_dir = root / "bin"
        self.homes_dir = root / "homes"
        self.active_path = root / "active.json"

    def ensure(self) -> None:
        ensure_private_dir(self.root)
        ensure_private_dir(self.profiles_dir)
        ensure_private_dir(self.backups_dir)
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.homes_dir.mkdir(parents=True, exist_ok=True)

    def profile_dir(self, name: str) -> Path:
        validate_profile_name(name)
        return self.profiles_dir / name

    def managed_home(self, name: str) -> Path:
        validate_profile_name(name)
        return self.homes_dir / name

    def manifest_path(self, name: str) -> Path:
        return self.profile_dir(name) / "manifest.json"

    def load_manifest(self, name: str) -> dict[str, Any]:
        path = self.manifest_path(name)
        if not path.exists():
            raise SwitchError(f"Profile not found: {name} ({path})")
        manifest = read_json(path)
        manifest.setdefault("name", name)
        manifest.setdefault("managed_files", list(MANAGED_FILES))
        manifest.setdefault("app_cli_binding", "launchagent")
        return manifest

    def list_profiles(self) -> list[str]:
        if not self.profiles_dir.exists():
            return []
        names = []
        for child in self.profiles_dir.iterdir():
            if child.is_dir() and (child / "manifest.json").exists():
                names.append(child.name)
        return sorted(names)


def make_store(args: Any) -> Store:
    official_codex_home = getattr(args, "official_codex_home", None)
    if official_codex_home is None:
        official_codex_home = getattr(args, "live_codex_home", None)
    internal_codex_home = getattr(args, "internal_codex_home", None)
    return Store(
        args.store_dir,
        official_codex_home,
        args.launch_agent_path,
        args.launch_agent_label,
        official_codex_home_source=getattr(args, "official_codex_home_source", "default"),
        internal_codex_home=internal_codex_home,
        internal_codex_home_source=getattr(args, "internal_codex_home_source", "default"),
    )
