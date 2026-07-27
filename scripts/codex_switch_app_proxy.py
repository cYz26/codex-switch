from __future__ import annotations

import hashlib
import json
import os
import re
import select
import stat
import subprocess
import sys
import threading
import time
from pathlib import Path

from codex_switch_config import string_assignment_value
from codex_switch_io import atomic_write
from codex_switch_protocol_adapter import (
    BackendCapabilities,
    CapabilityReceipt,
    PendingRequestTracker,
    ProtocolAdapter,
)
from codex_switch_running_app import argv_invokes_app_server
from codex_switch_toml_edit import top_level_assignment


DATE_SUFFIX = re.compile(r"-\d{4}-\d{2}-\d{2}$")
CODEX_CLI_VERSION = re.compile(r"\bcodex-cli\s+(\d+)\.(\d+)\.(\d+)")
MIN_CANONICAL_DYNAMIC_TOOLS_VERSION = (0, 141, 0)
CONFIG_WRITE_METHODS = {"config/value/write", "config/batchWrite"}
ORIGINAL_PYTHONPATH = "CODEX_SWITCH_PROXY_ORIGINAL_PYTHONPATH"
PYTHONPATH_WAS_SET = "CODEX_SWITCH_PROXY_PYTHONPATH_WAS_SET"
CAPABILITY_RECEIPT_ENV = "CODEX_SWITCH_CAPABILITY_RECEIPT"
EXPECTED_SCHEMA_SHA256_ENV = "CODEX_SWITCH_EXPECTED_SCHEMA_SHA256"
EXPECTED_RECEIPT_SHA256_ENV = "CODEX_SWITCH_EXPECTED_RECEIPT_SHA256"
CONFIG_WRITE_UNPROVEN_ERROR_CODE = -32096
CONFIG_WRITE_UNPROVEN_ERROR_MESSAGE = (
    "codex-switch: config write blocked because backend capability receipt "
    "is not proven"
)
BACKEND_STREAM_DRAIN_TIMEOUT_SECONDS = 2.0
CLIENT_INPUT_POLL_SECONDS = 0.05


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


def protocol_capabilities_for_version(
    version_text: str,
) -> BackendCapabilities:
    match = CODEX_CLI_VERSION.search(version_text)
    if not match:
        return BackendCapabilities(None, None, None)
    version = tuple(int(part) for part in match.groups())
    supports_modern_protocol = version >= MIN_CANONICAL_DYNAMIC_TOOLS_VERSION
    return BackendCapabilities(
        canonical_dynamic_tools=supports_modern_protocol,
        remote_marketplace_kind=(
            False if not supports_modern_protocol else None
        ),
        versioned_config_write_preserves_unrelated=None,
    )


def backend_protocol_capabilities(codex_bin: str) -> BackendCapabilities:
    try:
        result = subprocess.run(
            [codex_bin, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return BackendCapabilities(None, None, None)
    return protocol_capabilities_for_version(
        f"{result.stdout}\n{result.stderr}"
    )


def _valid_sha256(value: str) -> bool:
    return len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _read_regular_file(path: Path) -> bytes | None:
    try:
        before = path.lstat()
    except OSError:
        return None
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISREG(before.st_mode):
        return None
    try:
        descriptor = os.open(
            path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
    except OSError:
        return None
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_dev != before.st_dev
            or opened.st_ino != before.st_ino
        ):
            return None
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > 65536:
                return None
            chunks.append(chunk)
        try:
            after = path.lstat()
        except OSError:
            return None
        if after.st_dev != opened.st_dev or after.st_ino != opened.st_ino:
            return None
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _load_capability_receipt(
    path: Path,
    expected_sha256: str,
) -> CapabilityReceipt | None:
    if not _valid_sha256(expected_sha256):
        return None
    payload = _read_regular_file(path)
    if payload is None or hashlib.sha256(payload).hexdigest() != expected_sha256:
        return None
    try:
        return CapabilityReceipt.from_dict(json.loads(payload))
    except (json.JSONDecodeError, UnicodeDecodeError, RuntimeError):
        return None


def proxy_capabilities(
    codex_bin: str,
) -> tuple[BackendCapabilities, bool]:
    fallback = backend_protocol_capabilities(codex_bin)
    raw_path = os.environ.get(CAPABILITY_RECEIPT_ENV, "")
    expected_schema = os.environ.get(EXPECTED_SCHEMA_SHA256_ENV, "")
    expected_receipt = os.environ.get(EXPECTED_RECEIPT_SHA256_ENV, "")
    if not raw_path or not expected_schema or not expected_receipt:
        return fallback, False
    receipt = _load_capability_receipt(
        Path(raw_path).expanduser(),
        expected_receipt,
    )
    backend_path = Path(codex_bin).expanduser()
    if (
        receipt is None
        or not receipt.matches_backend_and_schema_digest(
            backend_path,
            expected_schema,
        )
    ):
        return fallback, False
    return (
        receipt.capabilities,
        receipt.schema_version == 2
        and receipt.capabilities.versioned_config_write_preserves_unrelated
        is True,
    )


def mask_backend_message_for_desktop(
    message: dict,
    *,
    method: str | None,
    actual_model: str,
    desktop_model: str,
) -> dict:
    adapter = ProtocolAdapter(
        actual_model=actual_model,
        desktop_model=desktop_model,
        capabilities=BackendCapabilities(None, None, None),
    )
    return adapter.server_message(
        message,
        pending_method=method,
    ).message


def translate_desktop_message_for_backend(
    message: dict,
    *,
    actual_model: str,
    desktop_model: str,
    supports_canonical_dynamic_tools: bool = False,
    supports_remote_marketplace_kind: bool | None = None,
) -> dict:
    if supports_remote_marketplace_kind is None:
        supports_remote_marketplace_kind = supports_canonical_dynamic_tools
    adapter = ProtocolAdapter(
        actual_model=actual_model,
        desktop_model=desktop_model,
        capabilities=BackendCapabilities(
            canonical_dynamic_tools=supports_canonical_dynamic_tools,
            remote_marketplace_kind=supports_remote_marketplace_kind,
            versioned_config_write_preserves_unrelated=None,
        ),
    )
    return adapter.client_request(message).message


def adapt_client_json_line(
    line: str | bytes,
    adapter: ProtocolAdapter,
    tracker: PendingRequestTracker,
) -> tuple[str | bytes, dict | None]:
    try:
        message = json.loads(line)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return line, None
    if not isinstance(message, dict):
        return line, None
    tracker.observe_client(message)
    result = adapter.client_request(message)
    if not result.changed:
        return line, message
    output = json.dumps(result.message, separators=(",", ":")) + "\n"
    return (output.encode() if isinstance(line, bytes) else output, message)


def adapt_backend_json_line(
    line: str | bytes,
    adapter: ProtocolAdapter,
    tracker: PendingRequestTracker,
) -> tuple[str | bytes, dict | None, str | None]:
    try:
        message = json.loads(line)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return line, None, None
    if not isinstance(message, dict):
        return line, None, None
    pending_method = tracker.consume_backend_response(message)
    result = adapter.server_message(
        message,
        pending_method=pending_method,
    )
    if not result.changed:
        return line, message, pending_method
    output = json.dumps(result.message, separators=(",", ":")) + "\n"
    return (
        output.encode() if isinstance(line, bytes) else output,
        message,
        pending_method,
    )


def _config_write_rejection(message: dict) -> bytes:
    request_id = message.get("id")
    if not (type(request_id) is int or isinstance(request_id, str)):
        request_id = None
    return (
        json.dumps(
            {
                "id": request_id,
                "error": {
                    "code": CONFIG_WRITE_UNPROVEN_ERROR_CODE,
                    "message": CONFIG_WRITE_UNPROVEN_ERROR_MESSAGE,
                },
            },
            separators=(",", ":"),
        )
        + "\n"
    ).encode()


def _write_client_output(
    payload: bytes,
    output_lock: threading.Lock,
) -> None:
    with output_lock:
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()


def forward_client_to_backend(
    backend: subprocess.Popen[bytes],
    adapter: ProtocolAdapter,
    tracker: PendingRequestTracker,
    config_write_proven: bool,
    output_lock: threading.Lock,
    stop_event: threading.Event,
) -> None:
    assert backend.stdin is not None
    input_fd = sys.stdin.fileno()
    buffered = bytearray()
    try:
        while not stop_event.is_set():
            readable, _, _ = select.select(
                [input_fd],
                [],
                [],
                CLIENT_INPUT_POLL_SECONDS,
            )
            if not readable:
                continue
            chunk = os.read(input_fd, 64 * 1024)
            if not chunk:
                if buffered:
                    lines = (bytes(buffered),)
                    buffered.clear()
                else:
                    lines = tuple()
                reached_eof = True
            else:
                buffered.extend(chunk)
                lines_list: list[bytes] = []
                while True:
                    newline_index = buffered.find(b"\n")
                    if newline_index < 0:
                        break
                    lines_list.append(bytes(buffered[: newline_index + 1]))
                    del buffered[: newline_index + 1]
                lines = tuple(lines_list)
                reached_eof = False
            for line in lines:
                if stop_event.is_set():
                    return
                try:
                    request = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    request = None
                if (
                    isinstance(request, dict)
                    and request.get("method") in CONFIG_WRITE_METHODS
                    and not config_write_proven
                ):
                    _write_client_output(
                        _config_write_rejection(request),
                        output_lock,
                    )
                    continue
                output_line, message = adapt_client_json_line(
                    line,
                    adapter,
                    tracker,
                )
                backend.stdin.write(output_line)
                backend.stdin.flush()
            if reached_eof:
                return
    except (BrokenPipeError, OSError, ValueError, select.error):
        return
    finally:
        try:
            backend.stdin.close()
        except (BrokenPipeError, OSError, ValueError):
            pass


def forward_backend_to_client(
    backend: subprocess.Popen[bytes],
    adapter: ProtocolAdapter,
    tracker: PendingRequestTracker,
    output_lock: threading.Lock,
) -> None:
    assert backend.stdout is not None
    for line in backend.stdout:
        output_line, _message, _pending_method = adapt_backend_json_line(
            line,
            adapter,
            tracker,
        )
        assert isinstance(output_line, bytes)
        _write_client_output(output_line, output_lock)


def forward_backend_stderr(backend: subprocess.Popen[bytes]) -> None:
    assert backend.stderr is not None
    for line in backend.stderr:
        sys.stderr.buffer.write(line)
        sys.stderr.buffer.flush()


def wait_for_backend_stream_drain(
    threads: tuple[threading.Thread, ...],
    *,
    timeout_seconds: float,
) -> bool:
    deadline = time.monotonic() + timeout_seconds
    for thread in threads:
        thread.join(timeout=max(0.0, deadline - time.monotonic()))
    return all(not thread.is_alive() for thread in threads)


def backend_environment() -> dict[str, str]:
    environment = os.environ.copy()
    original_pythonpath = environment.pop(ORIGINAL_PYTHONPATH, "")
    pythonpath_marker = environment.pop(PYTHONPATH_WAS_SET, None)
    if pythonpath_marker is None:
        return environment
    pythonpath_was_set = pythonpath_marker == "1"
    if pythonpath_was_set:
        environment["PYTHONPATH"] = original_pythonpath
    else:
        environment.pop("PYTHONPATH", None)
    return environment


def run_proxy(codex_bin: str, config_path: Path, args: list[str]) -> int:
    actual_model, desktop_model = read_desktop_model_alias(config_path)
    capabilities, config_write_proven = proxy_capabilities(codex_bin)
    adapter = ProtocolAdapter(
        actual_model=actual_model or "",
        desktop_model=desktop_model or actual_model or "",
        capabilities=capabilities,
    )
    tracker = PendingRequestTracker()
    output_lock = threading.Lock()
    stop_event = threading.Event()
    backend = subprocess.Popen(
        [codex_bin, *args],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=backend_environment(),
    )
    child_receipt = os.environ.get("CODEX_SWITCH_PROXY_CHILD_RECEIPT", "")
    if child_receipt:
        atomic_write(
            Path(child_receipt),
            (
                json.dumps(
                    {
                        "pid": backend.pid,
                        "codex_bin": str(Path(codex_bin).expanduser().resolve()),
                        "args": list(args),
                        "codex_home": os.environ.get("CODEX_HOME", ""),
                        "capability_receipt_path": os.environ.get(
                            CAPABILITY_RECEIPT_ENV,
                            "",
                        ),
                        "expected_schema_sha256": os.environ.get(
                            EXPECTED_SCHEMA_SHA256_ENV,
                            "",
                        ),
                        "expected_receipt_sha256": os.environ.get(
                            EXPECTED_RECEIPT_SHA256_ENV,
                            "",
                        ),
                        "config_write_proven": config_write_proven,
                    },
                    sort_keys=True,
                )
                + "\n"
            ).encode(),
            mode=0o600,
        )
    client_thread = threading.Thread(
        target=forward_client_to_backend,
        args=(
            backend,
            adapter,
            tracker,
            config_write_proven,
            output_lock,
            stop_event,
        ),
    )
    stdout_thread = threading.Thread(
        target=forward_backend_to_client,
        args=(
            backend,
            adapter,
            tracker,
            output_lock,
        ),
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=forward_backend_stderr,
        args=(backend,),
        daemon=True,
    )
    client_thread.start()
    stdout_thread.start()
    stderr_thread.start()
    returncode = backend.wait()
    stop_event.set()
    if not wait_for_backend_stream_drain(
        (client_thread, stdout_thread, stderr_thread),
        timeout_seconds=BACKEND_STREAM_DRAIN_TIMEOUT_SECONDS,
    ):
        print(
            "codex-switch app proxy: backend stream drain timed out; "
            f"returning backend exit status {returncode}",
            file=sys.stderr,
            flush=True,
        )
    return returncode


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
    if not argv_invokes_app_server(args):
        os.execve(codex_bin, [codex_bin, *args], backend_environment())
    return run_proxy(codex_bin, config_path, args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
