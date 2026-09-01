#!/usr/bin/env python3
"""PostToolUse — join against the parked timestamp and log one telemetry line.

Inert unless eval-workspace/.eval-active exists. Writes exactly one line to
eval-workspace/telemetry.jsonl per completed MCP tool call, per
references/workspace-contract.md.
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

    response = payload.get("tool_response")
    error_kind = _metrics.classify_error(response)
    text = _metrics.response_text(response)

    # Written before the telemetry line, so a line always has its payload file.
    if tool_use_id:
        _metrics.write_payload(workspace, tool_use_id, text)

    line = {
        "case_id": _metrics.marker_case_id(workspace),
        "tool_use_id": tool_use_id,
        "tool_name": tool_name,
        "ts_pre": ts_pre,
        "ts_post": ts_post,
        # None when the PreToolUse record is missing — the call still happened
        # and its payload economics still count.
        "duration_ms": (ts_post - ts_pre) if isinstance(ts_pre, int) else None,
        "args": _metrics.safe_args(payload.get("tool_input")),
    }
    line.update(_metrics.measure_payload(text))
    line.update({
        "is_error": error_kind != "none",
        "error_kind": error_kind,
        "agent_id": payload.get("agent_id"),
        "host_duration_ms": payload.get("duration_ms"),
    })

    _metrics.append_jsonl(os.path.join(workspace, "telemetry.jsonl"), line)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # telemetry loss is acceptable; interfering with the session is not
    sys.exit(0)
