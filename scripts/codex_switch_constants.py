from __future__ import annotations

from pathlib import Path


MANAGED_FILES = ("config.toml", "auth.json")
APP_CLI_ENV = "CODEX_CLI_PATH"
DEFAULT_LAUNCH_AGENT_LABEL = "com.openai.codex-cli-path"
DEFAULT_CHATGPT_BUNDLED_CODEX = Path(
    "/Applications/ChatGPT.app/Contents/Resources/codex"
)
CONFIG_MODE_SHARED = "shared"
CONFIG_MODE_SNAPSHOT = "snapshot"
PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE = (
    "cli_auth_credentials_store",
    "model",
    "model_provider",
    "model_catalog_json",
    "model_max_output_tokens",
    "max_output_tokens",
    "model_reasoning_effort",
    "personality",
)
SHARED_TOP_LEVEL_KEYS_FROM_PROFILE = PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE


class SwitchError(RuntimeError):
    pass
