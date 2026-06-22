from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import threading
from pathlib import Path

from codex_switch_config import string_assignment_value
from codex_switch_toml_edit import top_level_assignment


DATE_SUFFIX = re.compile(r"-\d{4}-\d{2}-\d{2}$")
CODEX_CLI_VERSION = re.compile(r"\bcodex-cli\s+(\d+)\.(\d+)\.(\d+)")
MIN_CANONICAL_DYNAMIC_TOOLS_VERSION = (0, 141, 0)
MODEL_VALUE_KEYS = {
    "model",
    "latestModel",
    "previousTurnModel",
    "userSavedModelString",
}
UNSUPPORTED_OLDER_BACKEND_PLUGIN_MARKETPLACE_KINDS = {
    "created-by-me-remote",
}


def desktop_alias_for_model(model: str) -> str:
    return DATE_SUFFIX.sub("", model)


def read_desktop_model_alias(config_path: Path) -> tuple[str | None, str | None]:
    if not config_path.exists():
        return None, None
    assignment = top_level_assignment(config_path.read_text(), "model")
    if not assignment:
        return None, None
    actual_model = string_assignment_value(assignment)
    if not actual_model:
        return None, None
    desktop_model = os.environ.get("CODEX_SWITCH_DESKTOP_MODEL_ALIAS")
    if not desktop_model:
        desktop_model = desktop_alias_for_model(actual_model)
    if desktop_model == actual_model:
        return actual_model, None
    return actual_model, desktop_model


def codex_version_supports_canonical_dynamic_tools(version_text: str) -> bool:
    match = CODEX_CLI_VERSION.search(version_text)
    if not match:
        return False
    version = tuple(int(part) for part in match.groups())
    return version >= MIN_CANONICAL_DYNAMIC_TOOLS_VERSION


def backend_supports_canonical_dynamic_tools(codex_bin: str) -> bool:
    try:
        result = subprocess.run(
            [codex_bin, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return codex_version_supports_canonical_dynamic_tools(
        f"{result.stdout}\n{result.stderr}"
    )


def message_id(message: dict) -> str | int | None:
    value = message.get("id")
    if isinstance(value, (str, int)):
        return value
    return None


def replace_model_value(value, *, old: str, new: str):
    if isinstance(value, dict):
        replaced = {}
        key_name = value.get("key")
        path_name = value.get("path")
        for key, item in value.items():
            if key in MODEL_VALUE_KEYS and item == old:
                replaced[key] = new
            elif (
                key == "value"
                and item == old
                and (key_name in MODEL_VALUE_KEYS or path_name in MODEL_VALUE_KEYS)
            ):
                replaced[key] = new
            else:
                replaced[key] = replace_model_value(item, old=old, new=new)
        return replaced
    if isinstance(value, list):
        return [replace_model_value(item, old=old, new=new) for item in value]
    return value


def older_backend_function_dynamic_tool_spec(tool: dict, *, namespace: str | None = None) -> dict:
    spec = {}
    if namespace is not None:
        spec["namespace"] = namespace
    for key in ("type", "name", "description", "inputSchema", "deferLoading"):
        if key in tool:
            spec[key] = normalize_desktop_request_for_older_backend(tool[key])
    return spec


def flatten_namespace_dynamic_tool_spec(spec: dict) -> list[dict] | None:
    if spec.get("type") != "namespace":
        return None
    namespace = spec.get("name")
    tools = spec.get("tools")
    if not isinstance(namespace, str) or not isinstance(tools, list):
        return None
    flattened = []
    for tool in tools:
        if isinstance(tool, dict):
            flattened.append(older_backend_function_dynamic_tool_spec(tool, namespace=namespace))
        else:
            flattened.append(normalize_desktop_request_for_older_backend(tool))
    return flattened


def normalize_desktop_request_for_older_backend(value):
    if isinstance(value, list):
        normalized = []
        for item in value:
            flattened = flatten_namespace_dynamic_tool_spec(item) if isinstance(item, dict) else None
            if flattened is None:
                normalized.append(normalize_desktop_request_for_older_backend(item))
            else:
                normalized.extend(flattened)
        return normalized
    if isinstance(value, dict):
        return {
            key: normalize_desktop_request_for_older_backend(item)
            for key, item in value.items()
        }
    return value


def filter_plugin_list_marketplace_kinds_for_older_backend(message: dict) -> dict:
    if message.get("method") != "plugin/list":
        return message
    params = message.get("params")
    if not isinstance(params, dict):
        return message
    kinds = params.get("marketplaceKinds")
    if not isinstance(kinds, list):
        return message
    params["marketplaceKinds"] = [
        kind
        for kind in kinds
        if kind not in UNSUPPORTED_OLDER_BACKEND_PLUGIN_MARKETPLACE_KINDS
    ]
    return message


def mask_model_list_response(message: dict, *, actual_model: str, desktop_model: str) -> dict:
    masked = copy.deepcopy(message)
    result = masked.get("result")
    if not isinstance(result, dict):
        return masked
    for key in ("data", "models"):
        models = result.get(key)
        if not isinstance(models, list):
            continue
        for model in models:
            if not isinstance(model, dict):
                continue
            if model.get("model") == actual_model:
                model["model"] = desktop_model
            if model.get("id") == actual_model:
                model["id"] = desktop_model
    return masked


def mask_config_read_response(message: dict, *, actual_model: str, desktop_model: str) -> dict:
    masked = copy.deepcopy(message)
    result = masked.get("result")
    if not isinstance(result, dict):
        return masked
    config = result.get("config")
    if isinstance(config, dict) and config.get("model") == actual_model:
        config["model"] = desktop_model
    return masked


def mask_backend_message_for_desktop(
    message: dict,
    *,
    method: str | None,
    actual_model: str,
    desktop_model: str,
) -> dict:
    masked = message
    if method == "model/list":
        masked = mask_model_list_response(
            message,
            actual_model=actual_model,
            desktop_model=desktop_model,
        )
    elif method == "config/read":
        masked = mask_config_read_response(
            message,
            actual_model=actual_model,
            desktop_model=desktop_model,
        )
    return replace_model_value(masked, old=actual_model, new=desktop_model)


def translate_desktop_message_for_backend(
    message: dict,
    *,
    actual_model: str,
    desktop_model: str,
    supports_canonical_dynamic_tools: bool = False,
) -> dict:
    translated = replace_model_value(message, old=desktop_model, new=actual_model)
    if not supports_canonical_dynamic_tools:
        translated = normalize_desktop_request_for_older_backend(translated)
    if isinstance(translated, dict):
        translated = filter_plugin_list_marketplace_kinds_for_older_backend(translated)
    return translated


def write_json_line(stream, message: dict) -> None:
    stream.write(json.dumps(message, separators=(",", ":")) + "\n")
    stream.flush()


def forward_client_to_backend(
    backend: subprocess.Popen[str],
    pending_methods: dict[str | int, str],
    actual_model: str,
    desktop_model: str,
    supports_canonical_dynamic_tools: bool,
) -> None:
    assert backend.stdin is not None
    try:
        for line in sys.stdin:
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                backend.stdin.write(line)
                backend.stdin.flush()
                continue
            if isinstance(message, dict):
                request_id = message_id(message)
                method = message.get("method")
                if request_id is not None and isinstance(method, str):
                    pending_methods[request_id] = method
                message = translate_desktop_message_for_backend(
                    message,
                    actual_model=actual_model,
                    desktop_model=desktop_model,
                    supports_canonical_dynamic_tools=supports_canonical_dynamic_tools,
                )
                write_json_line(backend.stdin, message)
            else:
                backend.stdin.write(line)
                backend.stdin.flush()
    finally:
        backend.stdin.close()


def forward_backend_to_client(
    backend: subprocess.Popen[str],
    pending_methods: dict[str | int, str],
    actual_model: str,
    desktop_model: str,
) -> None:
    assert backend.stdout is not None
    for line in backend.stdout:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(line)
            sys.stdout.flush()
            continue
        if isinstance(message, dict):
            request_id = message_id(message)
            method = pending_methods.pop(request_id, None) if request_id is not None else None
            message = mask_backend_message_for_desktop(
                message,
                method=method,
                actual_model=actual_model,
                desktop_model=desktop_model,
            )
            write_json_line(sys.stdout, message)
        else:
            sys.stdout.write(line)
            sys.stdout.flush()


def forward_backend_stderr(backend: subprocess.Popen[str]) -> None:
    assert backend.stderr is not None
    for line in backend.stderr:
        sys.stderr.write(line)
        sys.stderr.flush()


def run_proxy(codex_bin: str, config_path: Path, args: list[str]) -> int:
    actual_model, desktop_model = read_desktop_model_alias(config_path)
    supports_canonical_dynamic_tools = backend_supports_canonical_dynamic_tools(codex_bin)
    backend = subprocess.Popen(
        [codex_bin, *args],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=os.environ.copy(),
    )
    if not actual_model or not desktop_model:
        client_thread = threading.Thread(
            target=forward_client_to_backend,
            args=(backend, {}, "", "", supports_canonical_dynamic_tools),
            daemon=True,
        )
        stdout_thread = threading.Thread(
            target=forward_backend_to_client,
            args=(backend, {}, "", ""),
            daemon=True,
        )
    else:
        pending_methods: dict[str | int, str] = {}
        client_thread = threading.Thread(
            target=forward_client_to_backend,
            args=(
                backend,
                pending_methods,
                actual_model,
                desktop_model,
                supports_canonical_dynamic_tools,
            ),
            daemon=True,
        )
        stdout_thread = threading.Thread(
            target=forward_backend_to_client,
            args=(backend, pending_methods, actual_model, desktop_model),
            daemon=True,
        )
    stderr_thread = threading.Thread(target=forward_backend_stderr, args=(backend,), daemon=True)
    client_thread.start()
    stdout_thread.start()
    stderr_thread.start()
    return backend.wait()


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(
            "usage: codex_switch_app_proxy.py CODEX_BIN CONFIG_PATH ARGS...",
            file=sys.stderr,
        )
        return 2
    codex_bin = argv[1]
    config_path = Path(argv[2])
    args = argv[3:]
    return run_proxy(codex_bin, config_path, args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
