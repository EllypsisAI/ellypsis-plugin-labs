#!/usr/bin/env python3
"""Hook telemetry tests — run with `python3 -m pytest` or `python3 tests/mcp-eval/test_hooks.py`.

Every case pipes a synthetic hook payload through the real script as a
subprocess, the way Claude Code invokes it.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLUGIN = os.path.join(REPO, "plugins", "mcp-eval")
PRE = os.path.join(PLUGIN, "hooks", "scripts", "pre_tool_use.py")
POST = os.path.join(PLUGIN, "hooks", "scripts", "post_tool_use.py")
FAIL = os.path.join(PLUGIN, "hooks", "scripts", "post_tool_use_failure.py")

CONTRACT_KEYS = {
    "case_id", "tool_use_id", "tool_name", "ts_pre", "ts_post", "duration_ms",
    "args", "payload_bytes", "payload_chars", "est_tokens", "is_error", "error_kind",
    "payload_excerpt",
}

MAX_PAYLOAD_BYTES = 200 * 1024
TRUNCATION_MARKER = "…[truncated]"

TOOL = "mcp__acme__search_contacts"
CASE = "l1-search-contacts"


def mcp_response(text):
    return {"content": [{"type": "text", "text": text}]}


class HookTest(unittest.TestCase):
    def setUp(self):
        self.cwd = tempfile.mkdtemp(prefix="mcp-eval-test-")
        self.workspace = os.path.join(self.cwd, "eval-workspace")
        os.makedirs(self.workspace)

    def tearDown(self):
        shutil.rmtree(self.cwd, ignore_errors=True)

    # --- helpers ---

    def activate(self, case_id=CASE):
        with open(os.path.join(self.workspace, ".eval-active"), "w") as f:
            json.dump({"case_id": case_id, "started": "2026-08-17T14:02:11Z"}, f)

    def run_hook(self, script, payload):
        raw = payload if isinstance(payload, str) else json.dumps(payload)
        proc = subprocess.run(
            [sys.executable, script], input=raw, capture_output=True, text=True, cwd=self.cwd)
        self.assertEqual(proc.returncode, 0, f"{script} exited {proc.returncode}: {proc.stderr}")
        return proc

    def pre_payload(self, tool_name=TOOL, tool_use_id="toolu_1", args=None):
        return {"session_id": "s", "transcript_path": "/t", "cwd": self.cwd,
                "hook_event_name": "PreToolUse", "tool_name": tool_name,
                "tool_input": args if args is not None else {"query": "Contoso"},
                "tool_use_id": tool_use_id}

    def post_payload(self, response, tool_name=TOOL, tool_use_id="toolu_1", **extra):
        payload = self.pre_payload(tool_name, tool_use_id)
        payload["hook_event_name"] = "PostToolUse"
        payload["tool_response"] = response
        payload.update(extra)
        return payload

    def telemetry(self):
        path = os.path.join(self.workspace, "telemetry.jsonl")
        if not os.path.isfile(path):
            return []
        with open(path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def pending(self):
        directory = os.path.join(self.workspace, ".pending")
        return sorted(os.listdir(directory)) if os.path.isdir(directory) else []

    def payloads(self):
        directory = os.path.join(self.workspace, "payloads")
        return sorted(os.listdir(directory)) if os.path.isdir(directory) else []

    def payload_text(self, tool_use_id="toolu_1"):
        with open(os.path.join(self.workspace, "payloads", tool_use_id + ".txt")) as f:
            return f.read()

    def one_call(self, response, **extra):
        self.activate()
        self.run_hook(PRE, self.pre_payload())
        self.run_hook(POST, self.post_payload(response, **extra))
        lines = self.telemetry()
        self.assertEqual(len(lines), 1)
        return lines[0]

    # --- gating: the requirement that matters most ---

    def test_inert_without_marker(self):
        for script, payload in ((PRE, self.pre_payload()),
                                (POST, self.post_payload(mcp_response("x"))),
                                (FAIL, self.post_payload(None, error="boom"))):
            self.run_hook(script, payload)
        self.assertEqual(os.listdir(self.workspace), [])
        self.assertEqual(self.telemetry(), [])

    def test_preflight_access_probe_leaves_no_trace(self):
        """The probe calls the target's tools before any case starts.

        Nothing it does may reach telemetry, or the eval would be grading its
        own setup. The absent marker is the only thing preventing that.
        """
        for i in range(3):
            probe = self.pre_payload(tool_use_id=f"probe_{i}")
            self.run_hook(PRE, probe)
            self.run_hook(POST, self.post_payload(
                mcp_response('{"tools": ["search_contacts"]}'), tool_use_id=f"probe_{i}"))
        self.assertEqual(os.listdir(self.workspace), [])
        self.assertEqual(self.telemetry(), [])
        self.assertEqual(self.payloads(), [])

    def test_inert_after_marker_removed_mid_call(self):
        self.activate()
        self.run_hook(PRE, self.pre_payload())
        os.remove(os.path.join(self.workspace, ".eval-active"))
        self.run_hook(POST, self.post_payload(mcp_response("x")))
        self.assertEqual(self.telemetry(), [])

    def test_ignores_non_mcp_tools(self):
        self.activate()
        self.run_hook(PRE, self.pre_payload(tool_name="Bash"))
        self.run_hook(POST, self.post_payload(mcp_response("x"), tool_name="Read"))
        self.assertEqual(self.pending(), [])
        self.assertEqual(self.payloads(), [])
        self.assertEqual(self.telemetry(), [])

    # --- the happy path ---

    def test_pre_parks_pending_record(self):
        self.activate()
        self.run_hook(PRE, self.pre_payload())
        self.assertEqual(self.pending(), ["toolu_1.json"])
        with open(os.path.join(self.workspace, ".pending", "toolu_1.json")) as f:
            record = json.load(f)
        self.assertEqual(record["tool_use_id"], "toolu_1")
        self.assertIsInstance(record["ts_pre"], int)

    def test_post_writes_contract_line_and_clears_pending(self):
        text = "x" * 400
        line = self.one_call(mcp_response(text))

        self.assertTrue(CONTRACT_KEYS.issubset(line), CONTRACT_KEYS - set(line))
        self.assertEqual(line["case_id"], CASE)
        self.assertEqual(line["tool_use_id"], "toolu_1")
        self.assertEqual(line["tool_name"], TOOL)
        self.assertEqual(line["args"], {"query": "Contoso"})
        self.assertEqual(line["payload_chars"], len(text))
        self.assertEqual(line["payload_bytes"], len(text.encode()))
        self.assertEqual(line["est_tokens"], len(text) // 4)
        self.assertFalse(line["is_error"])
        self.assertEqual(line["error_kind"], "none")
        self.assertIsInstance(line["ts_pre"], int)
        self.assertIsInstance(line["ts_post"], int)
        self.assertGreaterEqual(line["duration_ms"], 0)
        self.assertEqual(line["duration_ms"], line["ts_post"] - line["ts_pre"])
        self.assertEqual(self.pending(), [])

    def test_case_id_tracks_the_marker(self):
        line = self.one_call(mcp_response("hi"))
        self.assertEqual(line["case_id"], CASE)
        self.activate(case_id="l0-blind-research")
        self.run_hook(PRE, self.pre_payload(tool_use_id="toolu_2"))
        self.run_hook(POST, self.post_payload(mcp_response("hi"), tool_use_id="toolu_2"))
        self.assertEqual(self.telemetry()[-1]["case_id"], "l0-blind-research")

    # --- payload capture ---

    def test_payload_file_holds_the_full_inner_text(self):
        body = json.dumps({"contacts": [{"id": i} for i in range(200)]})
        line = self.one_call(mcp_response(body))
        self.assertEqual(self.payloads(), ["toolu_1.txt"])
        self.assertEqual(self.payload_text(), body)
        self.assertEqual(line["payload_chars"], len(body))

    def test_payload_dirs_are_created_by_the_hooks(self):
        self.activate()
        self.assertEqual(sorted(os.listdir(self.workspace)), [".eval-active"])
        self.run_hook(PRE, self.pre_payload())
        self.run_hook(POST, self.post_payload(mcp_response("hi")))
        self.assertEqual(sorted(os.listdir(self.workspace)),
                         [".eval-active", ".pending", "payloads", "telemetry.jsonl"])

    def test_payload_excerpt_is_first_500_chars(self):
        body = "".join(str(i % 10) for i in range(3000))
        line = self.one_call(mcp_response(body))
        self.assertEqual(line["payload_excerpt"], body[:500])
        self.assertEqual(len(line["payload_excerpt"]), 500)

    def test_short_payload_excerpt_is_the_whole_payload(self):
        line = self.one_call(mcp_response("three words here"))
        self.assertEqual(line["payload_excerpt"], "three words here")

    def test_payload_truncated_at_cap_with_marker(self):
        body = "z" * (MAX_PAYLOAD_BYTES + 5000)
        line = self.one_call(mcp_response(body))
        stored = self.payload_text()
        self.assertTrue(stored.endswith(TRUNCATION_MARKER))
        self.assertEqual(len(stored.encode()), MAX_PAYLOAD_BYTES)
        self.assertEqual(stored[:-len(TRUNCATION_MARKER)], body[:len(stored) - len(TRUNCATION_MARKER)])
        # The telemetry line reports the true size, not the truncated one.
        self.assertEqual(line["payload_chars"], len(body))

    def test_truncation_does_not_split_a_multibyte_character(self):
        # The cap leaves an even number of bytes for the body, so one leading
        # ASCII byte forces the cut to land inside a 2-byte character.
        body = "a" + "æ" * MAX_PAYLOAD_BYTES
        self.one_call(mcp_response(body))
        stored = self.payload_text()  # a split character would raise here
        self.assertTrue(stored.endswith(TRUNCATION_MARKER))
        self.assertEqual(len(stored.encode()), MAX_PAYLOAD_BYTES - 1)
        self.assertTrue(stored[:-len(TRUNCATION_MARKER)].endswith("æ"))

    def test_empty_payload_still_writes_a_file(self):
        # An empty file means "the call returned nothing"; a missing file means
        # "the call never completed". Grading needs to tell those apart.
        line = self.one_call(mcp_response(""))
        self.assertEqual(self.payloads(), ["toolu_1.txt"])
        self.assertEqual(self.payload_text(), "")
        self.assertEqual(line["payload_excerpt"], "")

    def test_failure_writes_no_payload_file(self):
        self.activate()
        self.run_hook(FAIL, self.post_payload(None, error="timeout"))
        self.assertEqual(self.payloads(), [])
        self.assertEqual(self.telemetry()[0]["payload_excerpt"], "")

    def test_field_inventory_from_json_payload(self):
        line = self.one_call(mcp_response(json.dumps({"contacts": [{"id": 1, "name": "a"}]})))
        self.assertEqual(line["field_count"], 3)
        self.assertEqual(line["fields"], ["contacts", "contacts[0].id", "contacts[0].name"])

    def test_agent_id_and_host_duration_recorded(self):
        line = self.one_call(mcp_response("hi"), agent_id="agent_7", duration_ms=1234)
        self.assertEqual(line["agent_id"], "agent_7")
        self.assertEqual(line["host_duration_ms"], 1234)

    # --- error detection ---

    def test_mcp_is_error(self):
        response = {"content": [{"type": "text", "text": "not found"}], "isError": True}
        line = self.one_call(response)
        self.assertTrue(line["is_error"])
        self.assertEqual(line["error_kind"], "mcp_error")

    def test_jsonrpc_error(self):
        line = self.one_call({"error": {"code": -32601, "message": "Method not found"}})
        self.assertTrue(line["is_error"])
        self.assertEqual(line["error_kind"], "jsonrpc_error")

    def test_failure_hook_logs_exception(self):
        self.activate()
        self.run_hook(PRE, self.pre_payload())
        self.run_hook(FAIL, self.post_payload(
            None, error="Error: connection reset\nstack frame", is_interrupt=False))
        line = self.telemetry()[0]
        self.assertTrue(CONTRACT_KEYS.issubset(line))
        self.assertTrue(line["is_error"])
        self.assertEqual(line["error_kind"], "exception")
        self.assertEqual(line["error"], "Error: connection reset")
        self.assertFalse(line["is_interrupt"])
        self.assertEqual(line["est_tokens"], 0)
        self.assertEqual(self.pending(), [])

    def test_interrupt_is_flagged(self):
        self.activate()
        self.run_hook(FAIL, self.post_payload(None, error="Interrupted", is_interrupt=True))
        self.assertTrue(self.telemetry()[0]["is_interrupt"])

    # --- degraded inputs: never crash, never block ---

    def test_post_without_pre_still_logs(self):
        self.activate()
        self.run_hook(POST, self.post_payload(mcp_response("orphan")))
        line = self.telemetry()[0]
        self.assertIsNone(line["ts_pre"])
        self.assertIsNone(line["duration_ms"])
        self.assertEqual(line["payload_chars"], 6)

    def test_garbage_stdin_is_survivable(self):
        for script in (PRE, POST, FAIL):
            for raw in ("", "not json", "[]", "null", '{"tool_name": 42}'):
                self.run_hook(script, raw)
        self.assertEqual(self.telemetry(), [])

    def test_odd_response_shapes(self):
        self.activate()
        for i, response in enumerate([None, "plain string", [], ["a"], 42,
                                      {"content": "flat"},
                                      {"content": [{"type": "image", "data": "b64"}]}]):
            tool_use_id = f"toolu_odd_{i}"
            self.run_hook(PRE, self.pre_payload(tool_use_id=tool_use_id))
            self.run_hook(POST, self.post_payload(response, tool_use_id=tool_use_id))
        lines = self.telemetry()
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[1]["payload_chars"], len("plain string"))
        self.assertEqual(lines[5]["payload_chars"], len("flat"))
        self.assertTrue(all(line["error_kind"] == "none" for line in lines))

    def test_huge_args_are_capped(self):
        self.activate()
        self.run_hook(PRE, self.pre_payload())
        payload = self.post_payload(mcp_response("ok"))
        payload["tool_input"] = {"body": "z" * 20000}
        self.run_hook(POST, payload)
        args = self.telemetry()[0]["args"]
        self.assertTrue(args["_truncated"])
        self.assertGreater(args["_chars"], 20000)
        self.assertEqual(len(args["_preview"]), 8000)

    def test_pre_tool_use_emits_no_decision(self):
        self.activate()
        proc = self.run_hook(PRE, self.pre_payload())
        self.assertEqual(json.loads(proc.stdout), {})

    def test_one_line_per_call_under_concurrency(self):
        self.activate()
        procs = []
        for i in range(8):
            self.run_hook(PRE, self.pre_payload(tool_use_id=f"toolu_{i}"))
        for i in range(8):
            payload = json.dumps(self.post_payload(mcp_response("y" * 5000), tool_use_id=f"toolu_{i}"))
            procs.append(subprocess.Popen(
                [sys.executable, POST], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, text=True, cwd=self.cwd))
            procs[-1].stdin.write(payload)
            procs[-1].stdin.close()
        for proc in procs:
            self.assertEqual(proc.wait(), 0)
        lines = self.telemetry()
        self.assertEqual(len(lines), 8)
        self.assertEqual(len({line["tool_use_id"] for line in lines}), 8)
        self.assertEqual(self.pending(), [])


class HooksManifestTest(unittest.TestCase):
    def test_manifest_shape(self):
        with open(os.path.join(PLUGIN, "hooks", "hooks.json")) as f:
            manifest = json.load(f)
        # The runtime reads parse(file).hooks — events at the root never load.
        self.assertIn("hooks", manifest)
        events = manifest["hooks"]
        self.assertEqual(set(events), {"PreToolUse", "PostToolUse", "PostToolUseFailure"})
        for entries in events.values():
            for entry in entries:
                # A bare "mcp__*" would be compared as an exact tool name and
                # match nothing; anything with regex metacharacters compiles.
                self.assertEqual(entry["matcher"], "mcp__.*")
                for hook in entry["hooks"]:
                    self.assertEqual(hook["type"], "command")
                    script = hook["command"].split("${CLAUDE_PLUGIN_ROOT}/")[1]
                    self.assertTrue(os.path.isfile(os.path.join(PLUGIN, script)), script)

    def test_plugin_manifest_does_not_declare_hooks(self):
        path = os.path.join(PLUGIN, ".claude-plugin", "plugin.json")
        with open(path) as f:
            self.assertNotIn("hooks", json.load(f))


if __name__ == "__main__":
    unittest.main(verbosity=2)
