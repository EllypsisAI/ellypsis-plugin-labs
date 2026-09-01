"""Shared helpers for the mcp-eval telemetry hooks.

Python 3 stdlib only. Payload parsing, token estimation and error detection are
adapted from the v0 plugin's scripts/_metrics.py; the gating and JSONL append
are new and implement references/workspace-contract.md.

Nothing in here may raise on hostile input — the hooks that call it run inside
the user's tool calls and must never interfere with them.
"""

import json
import os

CHARS_PER_TOKEN = 4
MAX_FIELDS = 50
MAX_ARGS_CHARS = 8000
MAX_ERROR_CHARS = 300
MAX_PAYLOAD_BYTES = 200 * 1024
PAYLOAD_EXCERPT_CHARS = 500
TRUNCATION_MARKER = "…[truncated]"

try:
    import fcntl
except ImportError:  # non-POSIX: appends stay unlocked
    fcntl = None


# --- gating ----------------------------------------------------------------

def active_workspace(payload):
    """Path of the live eval-workspace, or None when no eval is running.

    The orchestrator writes .eval-active immediately before spawning a case and
    deletes it as soon as the case returns, so its absence means these hooks
    must do nothing at all. Checked against the session cwd from the hook
    payload, falling back to the hook process cwd.
    """
    candidates = []
    for base in (payload.get("cwd"), _getcwd()):
        if base and base not in candidates:
            candidates.append(base)
    for base in candidates:
        workspace = os.path.join(base, "eval-workspace")
        if os.path.isfile(os.path.join(workspace, ".eval-active")):
            return workspace
    return None


def marker_case_id(workspace):
    """case_id of the running case, read from the marker file."""
    try:
        with open(os.path.join(workspace, ".eval-active"), encoding="utf-8") as f:
            return json.load(f).get("case_id")
    except Exception:
        return None


def _getcwd():
    try:
        return os.getcwd()
    except OSError:
        return None


# --- payload measurement ---------------------------------------------------

def count_fields(obj, prefix=""):
    """Recursively enumerate field paths in a JSON structure.

    Lists collapse to their first element so a 1000-item array of identical
    shapes produces one path per field, not 1000.
    """
    fields = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            fields.append(path)
            fields.extend(count_fields(v, path))
    elif isinstance(obj, list) and obj:
        fields.extend(count_fields(obj[0], f"{prefix}[0]"))
    return fields


def response_text(response):
    """The tool result as the model sees it — the string that costs context.

    MCP wraps results as {"content": [{"type": "text", "text": ...}], ...}.
    Non-text blocks (images, resources) are serialized whole because they
    occupy the context window too.
    """
    if response is None:
        return ""
    if isinstance(response, str):
        return response
    blocks = None
    if isinstance(response, list):
        blocks = response
    elif isinstance(response, dict):
        content = response.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            blocks = content
    if blocks is None:
        return _dumps(response)
    parts = []
    for block in blocks:
        if isinstance(block, dict) and isinstance(block.get("text"), str):
            parts.append(block["text"])
        else:
            parts.append(_dumps(block))
    return "".join(parts)


def measure_payload(text):
    """Size, estimated tokens, excerpt and field inventory for one payload."""
    fields = count_fields(_loads(text))
    return {
        "payload_bytes": len(text.encode("utf-8", "replace")),
        "payload_chars": len(text),
        "est_tokens": len(text) // CHARS_PER_TOKEN,
        "payload_excerpt": text[:PAYLOAD_EXCERPT_CHARS],
        "field_count": len(fields),
        "fields": fields[:MAX_FIELDS],
    }


def classify_error(response):
    """error_kind for a completed call: none | mcp_error | jsonrpc_error.

    'exception' is not detectable here — it comes from the PostToolUseFailure
    hook, where the runtime hands us the error directly.
    """
    if not isinstance(response, dict):
        return "none"
    candidates = [response]
    if isinstance(response.get("result"), dict):
        candidates.append(response["result"])
    for candidate in candidates:
        if candidate.get("isError"):
            return "mcp_error"
    if "error" in response and "result" not in response and response["error"] is not None:
        return "jsonrpc_error"
    return "none"


def safe_args(tool_input):
    """Tool arguments, capped so one huge argument can't bloat the log.

    Downstream the orchestrator reads telemetry.jsonl into its context; an
    uncapped write payload would defeat the point of payload containment.
    """
    if tool_input is None:
        return {}
    raw = _dumps(tool_input)
    if len(raw) <= MAX_ARGS_CHARS:
        return tool_input if isinstance(tool_input, (dict, list)) else raw
    return {"_truncated": True, "_chars": len(raw), "_preview": raw[:MAX_ARGS_CHARS]}


def truncate_error(message):
    text = message if isinstance(message, str) else _dumps(message)
    return text.split("\n")[0][:MAX_ERROR_CHARS]


# --- workspace io ----------------------------------------------------------

def pending_path(workspace, tool_use_id):
    return os.path.join(workspace, ".pending", _safe_name(tool_use_id) + ".json")


def write_payload(workspace, tool_use_id, text):
    """Persist the full inner text payload for independent grounding checks.

    Grading verifies a sub-agent's claimed excerpts against this file rather
    than against the sub-agent's own account of what the tool returned.
    """
    path = os.path.join(workspace, "payloads", _safe_name(tool_use_id) + ".txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    encoded = text.encode("utf-8", "replace")
    if len(encoded) > MAX_PAYLOAD_BYTES:
        keep = MAX_PAYLOAD_BYTES - len(TRUNCATION_MARKER.encode("utf-8"))
        # errors="ignore" drops a multibyte character split by the cut.
        text = encoded[:keep].decode("utf-8", "ignore") + TRUNCATION_MARKER
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _safe_name(tool_use_id):
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(tool_use_id))[:120]


def take_pending(workspace, tool_use_id):
    """Read and delete the parked PreToolUse record. {} when there is none."""
    path = pending_path(workspace, tool_use_id)
    try:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
    except Exception:
        record = {}
    try:
        os.remove(path)
    except OSError:
        pass
    return record if isinstance(record, dict) else {}


def append_jsonl(path, obj):
    """Append one line, locked — parallel tool calls append concurrently."""
    line = _dumps(obj) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        if fcntl is not None:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(line)
        f.flush()


def _dumps(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, default=str)
    except Exception:
        return str(obj)


def _loads(text):
    try:
        return json.loads(text)
    except Exception:
        return None
