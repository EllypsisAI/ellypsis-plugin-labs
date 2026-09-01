#!/usr/bin/env python3
"""PostToolUseFailure — log the calls that threw instead of returning.

PostToolUse does not fire when a tool call raises, times out or is interrupted;
the runtime emits PostToolUseFailure with the error string instead. Without this
hook those calls leave a stale .pending file and never reach telemetry.jsonl,
which would silently understate the reliability numbers. This is the only
producer of error_kind "exception".
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))

import _metrics  # noqa: E402


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return
    if not isinstance(payload, dict):
        return

    tool_name = str(payload.get("tool_name") or "")
    if not tool_name.startswith("mcp__"):
        return

    workspace = _metrics.active_workspace(payload)
    if workspace is None:
        return

    ts_post = int(time.time() * 1000)
    tool_use_id = payload.get("tool_use_id")
    pending = _metrics.take_pending(workspace, tool_use_id) if tool_use_id else {}
    ts_pre = pending.get("ts_pre")

    line = {
        "case_id": _metrics.marker_case_id(workspace),
        "tool_use_id": tool_use_id,
        "tool_name": tool_name,
        "ts_pre": ts_pre,
        "ts_post": ts_post,
        "duration_ms": (ts_post - ts_pre) if isinstance(ts_pre, int) else None,
        "args": _metrics.safe_args(payload.get("tool_input")),
        # No payload exists, so no payloads/<id>.txt is written either.
        "payload_bytes": 0,
        "payload_chars": 0,
        "est_tokens": 0,
        "payload_excerpt": "",
        "field_count": 0,
        "fields": [],
        "is_error": True,
        "error_kind": "exception",
        "error": _metrics.truncate_error(payload.get("error")),
        # A user interrupt is not a server fault — the report must not count it
        # against reliability.
        "is_interrupt": bool(payload.get("is_interrupt")),
        "agent_id": payload.get("agent_id"),
        "host_duration_ms": payload.get("duration_ms"),
    }

    _metrics.append_jsonl(os.path.join(workspace, "telemetry.jsonl"), line)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
