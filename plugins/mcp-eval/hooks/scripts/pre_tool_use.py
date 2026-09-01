#!/usr/bin/env python3
"""PreToolUse — park the start timestamp of an in-flight MCP tool call.

Inert unless eval-workspace/.eval-active exists: this hook is installed in every
session of everyone who has the plugin, so outside a running eval it must cost
nothing and change nothing.
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

    # Belt and braces: the matcher already restricts this to mcp__* tools.
    if not str(payload.get("tool_name") or "").startswith("mcp__"):
        return

    workspace = _metrics.active_workspace(payload)
    if workspace is None:
        return

    tool_use_id = payload.get("tool_use_id")
    if not tool_use_id:
        return

    path = _metrics.pending_path(workspace, tool_use_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"tool_use_id": tool_use_id, "ts_pre": int(time.time() * 1000)}, f)
    os.replace(tmp, path)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # telemetry loss is acceptable; blocking a tool call is not
    print("{}")
    sys.exit(0)
