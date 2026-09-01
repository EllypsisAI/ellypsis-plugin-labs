#!/usr/bin/env python3
"""
mcp-eval report generator.

Reads an eval workspace (shapes defined in references/workspace-contract.md) and
writes one self-contained HTML dashboard. Python 3 stdlib only, and the page
itself has no external dependencies: CSS and JS inline, data inlined as a single
JSON blob.

Every workspace file is optional. A missing or malformed file degrades its
section and is listed in the report's data-gaps note; nothing here raises on a
partial workspace.

Usage:
    python3 scripts/report.py [workspace-dir] [--output FILE] [--context-window N]
"""

import argparse
import html
import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_WORKSPACE = "eval-workspace"
DEFAULT_CONTEXT_WINDOW = 200000

# Honesty labels that are never derived from the workspace — they are true of
# every run this tool produces, so they are baked in and always rendered.
STANDING_CAVEATS = [
    "Token figures are estimates (chars/4 of the raw payload), not measured token counts. "
    "Every token cell and axis on this page is labelled \"est.\" for that reason.",
    "Latency is wall clock between the PreToolUse and PostToolUse hook timestamps and "
    "includes hook overhead. Every latency figure is prefixed \"~\" for that reason.",
    "Not measured anywhere on this page, because it is not honestly capturable in-session: "
    "exact per-call token cost, isolated schema overhead, per-tool memory or CPU, and "
    "concurrency behaviour.",
]

VERDICT_WORDS = {
    "ship": "Ship",
    "ship-with-caveats": "Ship with caveats",
    "dont-ship": "Don't ship",
    "don't-ship": "Don't ship",
}
VERDICT_CLASS = {
    "ship": "v-ship",
    "ship-with-caveats": "v-caveats",
    "dont-ship": "v-stop",
    "don't-ship": "v-stop",
}


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def read_json(path, gaps, label, default=None):
    """Load a JSON object, recording a gap instead of raising."""
    if default is None:
        default = {}
    if not path.exists():
        gaps.append("%s is missing" % label)
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        gaps.append("%s could not be read (%s)" % (label, exc.__class__.__name__))
        return default
    if not isinstance(data, type(default)):
        gaps.append("%s has an unexpected top-level shape" % label)
        return default
    return data


def read_jsonl(path, gaps, label):
    """Load a JSONL file, skipping malformed lines."""
    if not path.exists():
        gaps.append("%s is missing" % label)
        return []
    rows, bad = [], 0
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    bad += 1
                    continue
                if isinstance(row, dict):
                    rows.append(row)
                else:
                    bad += 1
    except (OSError, UnicodeDecodeError) as exc:
        gaps.append("%s could not be read (%s)" % (label, exc.__class__.__name__))
        return rows
    if bad:
        gaps.append("%s: %d malformed line(s) skipped" % (label, bad))
    return rows


def dget(obj, key, default=None):
    """dict.get that tolerates the object not being a dict."""
    return obj.get(key, default) if isinstance(obj, dict) else default


def dlist(obj, key):
    val = dget(obj, key)
    return val if isinstance(val, list) else []


# --------------------------------------------------------------------------
# formatting
# --------------------------------------------------------------------------

esc = html.escape
DASH = "&mdash;"


def as_number(value):
    """Telemetry is written by hooks; a field may be missing or junk."""
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def fmt_tokens(n):
    n = as_number(n)
    if n is None:
        return DASH
    if n >= 1_000_000:
        return "%.1fM" % (n / 1_000_000)
    if n >= 1_000:
        return "%.1fk" % (n / 1_000)
    return "%d" % int(n)


def fmt_ms(ms):
    ms = as_number(ms)
    if ms is None:
        return DASH
    if ms >= 1000:
        # round half up: %.1f would render 1450ms as 1.4s
        return "%.1fs" % (int(ms / 100 + 0.5) / 10)
    return "%dms" % int(ms + 0.5)


def fmt_bytes(b):
    b = as_number(b)
    if b is None:
        return DASH
    if b >= 1_048_576:
        return "%.1f MB" % (b / 1_048_576)
    if b >= 1024:
        return "%.1f KB" % (b / 1024)
    return "%d B" % int(b)


def fmt_pct(x):
    return "%.0f%%" % (x * 100)


def median_of(values):
    vals = [v for v in values if isinstance(v, (int, float))]
    return statistics.median(vals) if vals else None


def short_json(obj, limit=140):
    try:
        text = json.dumps(obj, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        text = str(obj)
    return text if len(text) <= limit else text[: limit - 1] + "…"


# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------

def tool_matches(qualified, plan_name):
    """`mcp__acme__search_contacts` matches plan tool `search_contacts`."""
    if not qualified or not plan_name:
        return False
    return qualified == plan_name or qualified.endswith("__" + plan_name)


def resolve_tool(qualified, plan_tool_names):
    for name in plan_tool_names:
        if tool_matches(qualified, name):
            return name, True
    return qualified, False


def case_outcome(status, assertions, has_grading):
    """One word for how a case landed. Never defaults an unknown to failure."""
    if status == "subagent_failed":
        return "failed-to-run"
    if status == "skipped":
        return "skipped"
    if not has_grading:
        return "ungraded"
    states = [a.get("passed") for a in assertions]
    if any(s is False for s in states):
        return "fail"
    if any(s is None for s in states):
        return "partial"
    if states and all(s is True for s in states):
        return "pass"
    return "ungraded"


def claim_state(claim):
    """Trinary grounding. A bare legacy `false` with no reason is still a fabrication."""
    grounded = claim.get("grounded")
    if grounded is True:
        return "verified"
    if grounded is False:
        return "fabricated"
    return "unverifiable"


def payload_info(payloads_dir, tool_use_id):
    """Locate the captured payload file for a call and note whether it hit the cap."""
    if not tool_use_id:
        return None
    path = payloads_dir / ("%s.txt" % tool_use_id)
    if not path.is_file():
        return None
    truncated = False
    try:
        with open(path, "rb") as fh:
            fh.seek(max(0, path.stat().st_size - 200))
            truncated = b"[truncated]" in fh.read()
    except OSError:
        pass
    return {"path": "payloads/%s.txt" % tool_use_id, "truncated": truncated}


def interview_rows(interview):
    """Interview facts in display order, each marked assumed or answered.

    `unanswered` names the fields the user declined; their values are the
    orchestrator's assumptions and must never read as requirements.
    """
    unanswered = [str(x) for x in dlist(interview, "unanswered")]
    rows, shown = [], set()

    def add(key, label, value):
        shown.add(key)
        rows.append({
            "key": key, "label": label, "value": value,
            "assumed": key in unanswered,
        })

    labels = [("use_case", "Use case"), ("audience", "Audience"),
              ("operator_model", "Operator model")]
    for key, label in labels:
        if isinstance(interview, dict) and key in interview:
            add(key, label, str(interview.get(key)))

    domain = dget(interview, "domain_inputs", {}) or {}
    if isinstance(domain, dict):
        shown.add("domain_inputs")
        for k, v in domain.items():
            rows.append({
                "key": "domain_inputs.%s" % k,
                "label": "Domain input · %s" % k,
                "value": str(v),
                "assumed": "domain_inputs" in unanswered or ("domain_inputs.%s" % k) in unanswered,
            })

    if isinstance(interview, dict):
        for key, value in interview.items():
            if key in shown or key == "unanswered":
                continue
            add(key, key.replace("_", " ").capitalize(), short_json(value, 200))

    # a declined field the plan never carried a value for still has to show up
    for key in unanswered:
        if key not in shown and not any(r["key"] == key for r in rows):
            rows.append({"key": key, "label": key.replace("_", " ").capitalize(),
                         "value": "not recorded", "assumed": True})
    return rows, unanswered


def build_model(workspace, context_window):
    ws = Path(workspace)
    gaps = []

    plan = read_json(ws / "plan.json", gaps, "plan.json")
    summary = read_json(ws / "grades_summary.json", gaps, "grades_summary.json")
    telemetry = read_jsonl(ws / "telemetry.jsonl", gaps, "telemetry.jsonl")
    payloads_dir = ws / "payloads"

    plan_tools = [t for t in dlist(plan, "tools") if isinstance(t, dict)]
    plan_tool_names = [t.get("name") for t in plan_tools if t.get("name")]

    # --- cases: plan order first, then any case dir the plan doesn't know about
    plan_cases = [c for c in dlist(plan, "cases") if isinstance(c, dict)]
    ordered_ids, seen = [], set()
    for case in plan_cases:
        cid = case.get("id")
        if cid and cid not in seen:
            ordered_ids.append(cid)
            seen.add(cid)
    cases_dir = ws / "cases"
    if cases_dir.is_dir():
        for entry in sorted(os.listdir(cases_dir)):
            if (cases_dir / entry).is_dir() and entry not in seen:
                ordered_ids.append(entry)
                seen.add(entry)
                gaps.append("cases/%s is on disk but not in plan.json" % entry)
    plan_by_id = {c.get("id"): c for c in plan_cases if c.get("id")}

    calls_by_case = {}
    for row in telemetry:
        calls_by_case.setdefault(row.get("case_id"), []).append(row)
    for rows in calls_by_case.values():
        rows.sort(key=lambda r: r.get("ts_pre") or 0)

    cases = []
    for cid in ordered_ids:
        pc = plan_by_id.get(cid, {})
        cdir = cases_dir / cid
        result = read_json(cdir / "result.json", [], "result") if cdir.is_dir() else {}
        grading_path = cdir / "grading.json"
        has_grading = grading_path.exists()
        grading = read_json(grading_path, [], "grading") if has_grading else {}

        graded = [a for a in dlist(grading, "assertions") if isinstance(a, dict)]
        if graded:
            assertions = [
                {
                    "text": a.get("text") or "",
                    "method": a.get("method") or "",
                    "passed": a.get("passed"),
                    "evidence": a.get("evidence") or "",
                }
                for a in graded
            ]
        else:
            # grading.json absent, or present with no assertions: fall back to the
            # planned assertion text, all ungraded. Nothing becomes a failure here.
            assertions = [
                {"text": str(t), "method": "", "passed": None, "evidence": "not graded"}
                for t in dlist(pc, "assertions")
            ]
            has_grading = False

        status = dget(result, "status") or ("no-result" if not result else "unknown")
        calls = calls_by_case.get(cid, [])
        target = pc.get("tool")

        marked_calls = []
        for row in calls:
            qualified = row.get("tool_name") or "(unnamed tool)"
            resolved, in_plan = resolve_tool(qualified, plan_tool_names)
            marked_calls.append(
                {
                    "row": row,
                    "qualified": qualified,
                    "resolved": resolved,
                    "in_plan": in_plan,
                    "on_target": tool_matches(qualified, target) if target else in_plan,
                    "excerpt": row.get("payload_excerpt") or "",
                    "payload": payload_info(payloads_dir, row.get("tool_use_id")),
                }
            )

        cases.append(
            {
                "id": cid,
                "level": (pc.get("level") or "").upper(),
                "tool": target,
                "task": pc.get("task") or "",
                "model": dget(result, "model") or dget(dget(plan, "interview", {}), "operator_model"),
                "status": status,
                "deliverable": dget(result, "deliverable") or "",
                "claimed_sources": dlist(result, "claimed_sources"),
                "friction": dlist(result, "friction"),
                "assertions": assertions,
                "has_grading": has_grading,
                "grounding": dget(grading, "grounding", {}) or {},
                "trajectory": dget(grading, "trajectory", {}) or {},
                "calls": marked_calls,
                "outcome": case_outcome(status, assertions, has_grading),
            }
        )

    unattributed = [
        row for row in telemetry
        if row.get("case_id") not in seen
    ]
    if unattributed:
        gaps.append("%d telemetry line(s) reference an unknown case_id" % len(unattributed))

    # --- headline numbers
    est_tokens_total = sum(
        r.get("est_tokens") or 0 for r in telemetry if isinstance(r.get("est_tokens"), (int, float))
    )
    err_tokens = sum(
        r.get("est_tokens") or 0
        for r in telemetry
        if r.get("is_error") and isinstance(r.get("est_tokens"), (int, float))
    )
    median_latency = median_of([r.get("duration_ms") for r in telemetry])

    cases_run = sum(1 for c in cases if c["status"] not in ("no-result", "skipped"))
    cases_total = dget(summary, "cases_total")
    if not isinstance(cases_total, int):
        cases_total = len(cases)
    cases_passed = dget(summary, "cases_passed")
    if not isinstance(cases_passed, int):
        cases_passed = sum(1 for c in cases if c["outcome"] == "pass")

    a_counts = {"passed": 0, "failed": 0, "ungradable": 0}
    for case in cases:
        if not case["has_grading"]:
            continue
        for a in case["assertions"]:
            if a["passed"] is True:
                a_counts["passed"] += 1
            elif a["passed"] is False:
                a_counts["failed"] += 1
            else:
                a_counts["ungradable"] += 1
    for key in ("passed", "failed", "ungradable"):
        val = dget(summary, key)
        if isinstance(val, int):
            a_counts[key] = val

    # --- grounding
    grounding_rows, fabrication_reported = [], 0
    tool_by_use_id = {
        r.get("tool_use_id"): r.get("tool_name") for r in telemetry if r.get("tool_use_id")
    }
    for case in cases:
        g = case["grounding"]
        rep = dget(g, "fabrications")
        if isinstance(rep, int):
            fabrication_reported += rep
        for claim in dlist(g, "claims"):
            if not isinstance(claim, dict):
                continue
            src = claim.get("source")
            state = claim_state(claim)
            grounding_rows.append(
                {
                    "case": case["id"],
                    "claim": claim.get("claim") or "",
                    "source_id": src,
                    "source_tool": tool_by_use_id.get(src),
                    "state": state,
                    "reason": claim.get("reason") or ("" if state == "verified" else "no reason recorded"),
                }
            )
    fabrication_listed = sum(1 for r in grounding_rows if r["state"] == "fabricated")
    unverifiable_listed = sum(1 for r in grounding_rows if r["state"] == "unverifiable")
    # the contract makes the claim rows authoritative for the fabrication count
    fabrications = fabrication_listed if grounding_rows else fabrication_reported

    # --- per-tool aggregation
    per_tool_summary = dget(summary, "per_tool", {}) or {}
    tools = {}

    def tool_slot(name, in_plan, write_capable=None, in_scope=None, skip_reason=None):
        slot = tools.setdefault(
            name,
            {
                "name": name,
                "in_plan": in_plan,
                "write_capable": write_capable,
                "in_scope": in_scope,
                "skip_reason": skip_reason,
                "calls": [],
                "cases": [],
                "capped": False,
                "found_in": 0,
                "found_of": 0,
                "detours": [],
                "calls_to_first": [],
                "assertions": {"passed": 0, "failed": 0, "ungradable": 0},
            },
        )
        if write_capable is not None:
            slot["write_capable"] = write_capable
        if in_scope is not None:
            slot["in_scope"] = in_scope
        if skip_reason:
            slot["skip_reason"] = skip_reason
        return slot

    for t in plan_tools:
        if t.get("name"):
            tool_slot(
                t["name"], True,
                write_capable=t.get("write_capable"),
                in_scope=t.get("in_scope"),
                skip_reason=t.get("skip_reason"),
            )

    for case in cases:
        for call in case["calls"]:
            slot = tool_slot(call["resolved"], call["in_plan"])
            slot["calls"].append(call["row"])
            if call["payload"] and call["payload"]["truncated"]:
                slot["capped"] = True
            if case["id"] not in slot["cases"]:
                slot["cases"].append(case["id"])
        if case["tool"]:
            slot = tool_slot(case["tool"], case["tool"] in plan_tool_names)
            if case["id"] not in slot["cases"]:
                slot["cases"].append(case["id"])
            traj = case["trajectory"]
            if traj:
                slot["found_of"] += 1
                if traj.get("found_tool") is True:
                    slot["found_in"] += 1
                for d in dlist(traj, "detours"):
                    slot["detours"].append(str(d))
                ctf = traj.get("calls_to_first_correct")
                if isinstance(ctf, (int, float)):
                    slot["calls_to_first"].append(ctf)
            for a in case["assertions"]:
                if not case["has_grading"]:
                    continue
                if a["passed"] is True:
                    slot["assertions"]["passed"] += 1
                elif a["passed"] is False:
                    slot["assertions"]["failed"] += 1
                else:
                    slot["assertions"]["ungradable"] += 1

    tool_cards = []
    for name, slot in tools.items():
        calls = slot["calls"]
        errors = [c for c in calls if c.get("is_error")]
        reported = per_tool_summary.get(name) if isinstance(per_tool_summary, dict) else None
        reported = reported if isinstance(reported, dict) else {}
        tool_cards.append(
            {
                "name": name,
                "in_plan": slot["in_plan"],
                "write_capable": slot["write_capable"],
                "in_scope": slot["in_scope"],
                "skip_reason": slot["skip_reason"],
                "n_calls": len(calls),
                "n_cases": len(slot["cases"]),
                "case_ids": slot["cases"],
                "capped": slot["capped"],
                "est_tokens_median": (
                    reported.get("est_tokens_median")
                    if isinstance(reported.get("est_tokens_median"), (int, float))
                    else median_of([c.get("est_tokens") for c in calls])
                ),
                "est_tokens_total": sum(
                    c.get("est_tokens") or 0 for c in calls
                    if isinstance(c.get("est_tokens"), (int, float))
                ),
                "bytes_median": median_of([c.get("payload_bytes") for c in calls]),
                "duration_median": (
                    reported.get("duration_ms_median")
                    if isinstance(reported.get("duration_ms_median"), (int, float))
                    else median_of([c.get("duration_ms") for c in calls])
                ),
                "duration_max": max(
                    [c.get("duration_ms") for c in calls if isinstance(c.get("duration_ms"), (int, float))],
                    default=None,
                ),
                "error_rate": (
                    reported.get("error_rate")
                    if isinstance(reported.get("error_rate"), (int, float))
                    else (len(errors) / len(calls) if calls else None)
                ),
                "error_kinds": sorted({c.get("error_kind") for c in errors if c.get("error_kind")}),
                "found_in": slot["found_in"],
                "found_of": slot["found_of"],
                "detours": slot["detours"],
                "calls_to_first": median_of(slot["calls_to_first"]),
                "assertions": slot["assertions"],
            }
        )
    # in-scope, exercised tools first; skipped ones last
    tool_cards.sort(key=lambda c: (c["in_scope"] is False, -c["n_calls"], c["name"]))

    caveats = [str(c) for c in dlist(summary, "caveats")]
    i_rows, unanswered = interview_rows(dget(plan, "interview", {}) or {})

    raw = {
        "plan": plan,
        "grades_summary": summary,
        "telemetry": telemetry,
        "cases": {
            c["id"]: {
                "status": c["status"],
                "outcome": c["outcome"],
                "assertions": c["assertions"],
                "grounding": c["grounding"],
                "trajectory": c["trajectory"],
            }
            for c in cases
        },
        "context_window": context_window,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    return {
        "workspace": str(ws),
        "server": dget(plan, "server") or "unknown server",
        "created": dget(plan, "created") or "",
        "interview": dget(plan, "interview", {}) or {},
        "verdict": dget(summary, "verdict"),
        "reasoning": dget(summary, "reasoning") or "",
        "gaps": gaps,
        "cases": cases,
        "telemetry": telemetry,
        "tool_cards": tool_cards,
        "grounding_rows": grounding_rows,
        "fabrications": fabrications,
        "fabrication_reported": fabrication_reported,
        "fabrication_listed": fabrication_listed,
        "unverifiable": unverifiable_listed,
        "interview_rows": i_rows,
        "unanswered": unanswered,
        "caveats": caveats,
        "context_window": context_window,
        "stats": {
            "cases_run": cases_run,
            "cases_total": cases_total,
            "cases_passed": cases_passed,
            "assertions": a_counts,
            "est_tokens_total": est_tokens_total,
            "est_tokens_error": err_tokens,
            "median_latency": median_latency,
            "n_calls": len(telemetry),
        },
        "raw": raw,
    }


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0d1117; --surface: #161b22; --surface-2: #1c2129;
  --border: #30363d; --border-subtle: #21262d;
  --text: #c9d1d9; --text-muted: #8b949e; --text-bright: #e6edf3;
  --primary: #58a6ff; --primary-muted: rgba(88,166,255,0.12);
  --green: #3fb950; --green-muted: rgba(63,185,80,0.15);
  --red: #f85149; --red-muted: rgba(248,81,73,0.15);
  --yellow: #d29922; --yellow-muted: rgba(210,153,34,0.15);
  --mono: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
}
html { font-size: 14px; }
body {
  background: var(--bg); color: var(--text); line-height: 1.5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}
.page { max-width: 1100px; margin: 0 auto; padding: 28px 24px 64px; }
a { color: var(--primary); }

.topbar {
  display: flex; align-items: baseline; justify-content: space-between;
  flex-wrap: wrap; gap: 8px; padding-bottom: 10px;
  border-bottom: 1px solid var(--border); margin-bottom: 20px;
}
.topbar h1 { font-size: 16px; font-weight: 600; color: var(--text-bright); font-family: var(--mono); }
.topbar .meta { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-muted); }

/* -- verdict, the loudest thing on the page -- */
.verdict {
  border: 1px solid var(--border); border-left: 4px solid var(--text-muted);
  border-radius: 8px; background: var(--surface);
  padding: 22px 26px; margin-bottom: 22px;
}
.verdict.v-ship { border-left-color: var(--green); background: linear-gradient(90deg, var(--green-muted), var(--surface) 42%); }
.verdict.v-caveats { border-left-color: var(--yellow); background: linear-gradient(90deg, var(--yellow-muted), var(--surface) 42%); }
.verdict.v-stop { border-left-color: var(--red); background: linear-gradient(90deg, var(--red-muted), var(--surface) 42%); }
.verdict-label {
  font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--text-muted); margin-bottom: 6px;
}
.verdict-word { font-size: 34px; line-height: 1.15; font-weight: 700; color: var(--text-bright); }
.verdict.v-ship .verdict-word { color: var(--green); }
.verdict.v-caveats .verdict-word { color: var(--yellow); }
.verdict.v-stop .verdict-word { color: var(--red); }
.verdict-reasoning { margin-top: 10px; font-size: 14px; max-width: 78ch; color: var(--text); }
.verdict-tally {
  margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border);
  display: flex; flex-wrap: wrap; gap: 20px; font-size: 12px; color: var(--text-muted);
}
.verdict-tally b { color: var(--text-bright); font-variant-numeric: tabular-nums; }

/* -- assumption chips + the interview facts the verdict rests on -- */
.chip {
  display: inline-block; font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
  font-weight: 600; padding: 1px 7px; border-radius: 999px;
  background: var(--yellow-muted); color: var(--yellow);
  border: 1px solid rgba(210,153,34,0.4); white-space: nowrap;
}
.params {
  margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border);
  display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px 22px;
}
.params-label {
  grid-column: 1 / -1; font-size: 11px; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--text-muted);
}
.param-label { font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
.param-value { font-size: 12px; color: var(--text); }
.param.assumed .param-value { color: var(--yellow); }

/* -- stat row -- */
.stats { display: flex; gap: 1px; background: var(--border); border-radius: 6px; overflow: hidden; margin-bottom: 20px; }
.stat { flex: 1; background: var(--surface); padding: 10px 14px; min-width: 140px; }
.stat-val { font-size: 20px; font-weight: 600; color: var(--text-bright); font-variant-numeric: tabular-nums; }
.stat-val.green { color: var(--green); } .stat-val.red { color: var(--red); } .stat-val.yellow { color: var(--yellow); }
.stat-label { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* -- budget -- */
.budget { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 12px 16px; margin-bottom: 8px; }
.budget-header { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
.budget-track { height: 10px; background: var(--surface-2); border-radius: 5px; overflow: hidden; display: flex; }
.budget-seg { height: 100%; }
.budget-legend { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 8px; font-size: 11px; color: var(--text-muted); }
.budget-legend-item { display: flex; align-items: center; gap: 5px; }
.budget-dot { width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0; }

/* -- sections -- */
.section-title {
  font-size: 13px; font-weight: 600; color: var(--text-bright);
  margin: 28px 0 10px; padding-bottom: 6px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: baseline; gap: 12px;
}
.section-title .hint { font-size: 11px; font-weight: 400; color: var(--text-muted); }
.empty { font-size: 12px; color: var(--text-muted); padding: 10px 0; }

/* -- tool cards -- */
.tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 10px; }
.tool-card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 12px 14px; }
.tool-card.skipped { opacity: 0.65; }
.tool-card-head { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 8px; }
.tool-card-name { font-family: var(--mono); font-size: 13px; color: var(--text-bright); font-weight: 500; word-break: break-all; }
.metric-group { border-top: 1px solid var(--border-subtle); padding-top: 6px; margin-top: 6px; }
.metric-group:first-of-type { border-top: none; margin-top: 0; padding-top: 0; }
.metric-group h4 { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 3px; }
.kv { display: flex; justify-content: space-between; gap: 12px; padding: 1px 0; font-size: 12px; }
.kv .k { color: var(--text-muted); }
.kv .v { color: var(--text); font-family: var(--mono); font-variant-numeric: tabular-nums; }
.kv .v.red { color: var(--red); } .kv .v.green { color: var(--green); } .kv .v.yellow { color: var(--yellow); }

/* -- badges -- */
.badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 1px 7px; border-radius: 4px; white-space: nowrap; }
.badge-pass { background: var(--green-muted); color: var(--green); }
.badge-fail { background: var(--red-muted); color: var(--red); }
.badge-partial { background: var(--yellow-muted); color: var(--yellow); }
.badge-neutral { background: var(--surface-2); color: var(--text-muted); }
.badge-info { background: var(--primary-muted); color: var(--primary); }
.badge-level { background: var(--surface-2); color: var(--primary); font-family: var(--mono); }

/* -- trajectory -- */
.traj { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 12px 14px; margin-bottom: 8px; }
.traj-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.traj-head .cid { font-family: var(--mono); font-size: 13px; color: var(--text-bright); }
.traj-path { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; font-size: 12px; }
.node {
  font-family: var(--mono); font-size: 11px; padding: 3px 8px; border-radius: 4px;
  border: 1px solid var(--border); background: var(--bg); color: var(--text-muted);
}
.node.hit { border-color: var(--green); color: var(--green); }
.node.detour { border-color: var(--yellow); color: var(--yellow); }
.node.err { border-color: var(--red); color: var(--red); }
.node.start { border-style: dashed; }
.arrow { color: var(--text-muted); font-size: 12px; }
.traj-note { margin-top: 8px; font-size: 12px; color: var(--text-muted); }
.traj-note.bad { color: var(--red); }

/* -- tables -- */
.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.tbl th {
  text-align: left; padding: 7px 10px; font-weight: 600; font-size: 11px;
  color: var(--text-muted); border-bottom: 1px solid var(--border); white-space: nowrap;
}
.tbl td { padding: 7px 10px; border-bottom: 1px solid var(--border-subtle); vertical-align: top; }
.tbl td.num { text-align: right; font-family: var(--mono); font-size: 12px; white-space: nowrap; font-variant-numeric: tabular-nums; }
.tbl td.mono { font-family: var(--mono); font-size: 12px; word-break: break-all; }
.tbl tr.fabrication { background: var(--red-muted); }
.tbl tr.fabrication td { color: var(--red); }
.tbl tr.unverifiable { background: var(--yellow-muted); }
.tbl tr.unverifiable td { color: var(--yellow); }
.counts { display: flex; gap: 28px; flex-wrap: wrap; margin-bottom: 12px; }
.fab-count { display: flex; align-items: baseline; gap: 10px; }
.fab-count .n { font-size: 26px; font-weight: 700; font-variant-numeric: tabular-nums; }
.fab-count .n.zero { color: var(--green); }
.fab-count .n.some { color: var(--red); }
.fab-count .n.warn { color: var(--yellow); }
.fab-count .n.none { color: var(--text-muted); }
.fab-count .lbl { font-size: 12px; color: var(--text-muted); max-width: 34ch; }
.claim-reason { display: block; font-size: 11px; opacity: 0.85; margin-top: 2px; }

/* -- caveats -- */
.caveats { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 14px 18px; }
.caveats h4 { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin: 10px 0 4px; }
.caveats h4:first-child { margin-top: 0; }
.caveats ul { margin: 0; padding-left: 18px; }
.caveats li { font-size: 12px; color: var(--text-muted); margin: 5px 0; }
.caveats li.standing { color: var(--text); }

/* -- case detail -- */
details.case { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 6px; }
details.case > summary {
  cursor: pointer; padding: 9px 14px; display: flex; align-items: center;
  gap: 10px; flex-wrap: wrap; list-style: none;
}
details.case > summary::-webkit-details-marker { display: none; }
details.case > summary::before { content: "\\25B6"; font-size: 9px; color: var(--text-muted); }
details.case[open] > summary::before { content: "\\25BC"; }
details.case > summary:hover { background: var(--surface-2); }
summary .cid { font-family: var(--mono); font-size: 13px; color: var(--text-bright); }
.spacer { flex: 1; }
.mini { font-size: 11px; color: var(--text-muted); font-variant-numeric: tabular-nums; }
.case-body { padding: 4px 14px 14px; border-top: 1px solid var(--border); }
.case-block { margin-top: 12px; }
.case-block h4 { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 5px; }
pre.box {
  background: var(--bg); border: 1px solid var(--border-subtle); border-radius: 4px;
  padding: 10px; font-family: var(--mono); font-size: 12px; line-height: 1.5;
  color: var(--text); white-space: pre-wrap; word-break: break-word;
  max-height: 320px; overflow-y: auto;
}
pre.box.excerpt { font-size: 11px; color: var(--text-muted); max-height: 150px; margin-top: 4px; }
.payload-note { font-size: 11px; color: var(--text-muted); }
.payload-note .path { font-family: var(--mono); color: var(--primary); }
.payload-note .capped { color: var(--yellow); }
ul.plain { list-style: none; }
ul.plain li { font-size: 12px; padding: 3px 0; border-bottom: 1px solid var(--border-subtle); }
ul.plain li:last-child { border-bottom: none; }
.assert-state { font-weight: 700; margin-right: 6px; font-size: 11px; }
.assert-state.pass { color: var(--green); }
.assert-state.fail { color: var(--red); }
.assert-state.ungradable { color: var(--yellow); }
.assert-evidence { color: var(--text-muted); font-size: 11px; margin-top: 2px; padding-left: 22px; }
.excerpt-row td { padding-top: 0; border-bottom: 1px solid var(--border); }

.controls { display: flex; gap: 8px; }
.controls button {
  background: none; border: 1px solid var(--border); color: var(--text-muted);
  font-size: 11px; padding: 3px 10px; border-radius: 4px; cursor: pointer;
}
.controls button:hover { border-color: var(--text-muted); color: var(--text); }

.gaps { background: var(--surface); border: 1px solid var(--yellow); border-radius: 6px; padding: 10px 14px; margin-bottom: 18px; }
.gaps h4 { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--yellow); margin-bottom: 4px; }
.gaps li { font-size: 12px; color: var(--text-muted); margin-left: 18px; }

.foot { margin-top: 32px; padding-top: 14px; border-top: 1px solid var(--border);
        display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;
        font-size: 11px; color: var(--text-muted); }

@media (max-width: 760px) {
  .stats { flex-direction: column; }
  .tool-grid { grid-template-columns: 1fr; }
  .verdict-word { font-size: 26px; }
}
"""

JS = """
document.addEventListener('click', function (e) {
  var btn = e.target.closest('button[data-all]');
  if (!btn) return;
  var open = btn.dataset.all === 'open';
  document.querySelectorAll('details.case').forEach(function (d) { d.open = open; });
});
"""


def section(title, hint="", extra=""):
    right = ""
    if hint:
        right += '<span class="hint">%s</span>' % esc(hint)
    if extra:
        right += extra
    return '<div class="section-title"><span>%s</span>%s</div>' % (esc(title), right)


def render_verdict(m):
    verdict = m["verdict"]
    key = (verdict or "").strip().lower()
    cls = VERDICT_CLASS.get(key, "")
    word = VERDICT_WORDS.get(key)
    if word is None:
        word = verdict if verdict else "No verdict recorded"
    reasoning = m["reasoning"]
    if not reasoning:
        reasoning = (
            "No reasoning paragraph in grades_summary.json. The verdict is unavailable "
            "until grading completes; the sections below show whatever the workspace does hold."
            if not verdict else "No reasoning paragraph was recorded with this verdict."
        )
    st = m["stats"]
    a = st["assertions"]
    tally = [
        "cases <b>%d/%d</b> passed" % (st["cases_passed"], st["cases_total"]),
        "assertions <b>%d</b> passed &middot; <b>%d</b> failed &middot; <b>%d</b> ungradable"
        % (a["passed"], a["failed"], a["ungradable"]),
        "fabrications <b>%d</b>" % m["fabrications"],
    ]
    if m["unverifiable"]:
        tally.append("unverifiable claims <b>%d</b>" % m["unverifiable"])
    tally.append(
        "tested with <b>%s</b>" % esc(str(m["interview"].get("operator_model") or "unrecorded model"))
    )
    if m["unanswered"]:
        tally.append(
            '<span class="chip">%d interview answer(s) assumed</span>' % len(m["unanswered"])
        )
    return (
        '<section class="verdict %s">' % cls
        + '<div class="verdict-label">Verdict</div>'
        + '<div class="verdict-word">%s</div>' % esc(str(word))
        + '<p class="verdict-reasoning">%s</p>' % esc(reasoning)
        + '<div class="verdict-tally">%s</div>' % "".join("<span>%s</span>" % t for t in tally)
        + render_params(m)
        + "</section>"
    )


def render_params(m):
    """The interview facts the whole eval was parameterised by, inside the verdict
    card so an assumed answer can never be read as a stated requirement."""
    rows = m["interview_rows"]
    if not rows:
        return ""
    cells = '<div class="params-label">Run parameters%s</div>' % (
        " · %d assumed, not answered by the user" % len(m["unanswered"]) if m["unanswered"] else ""
    )
    for row in rows:
        chip = '<span class="chip">assumed</span>' if row["assumed"] else ""
        cells += (
            '<div class="param%s"><div class="param-label">%s%s</div>'
            '<div class="param-value">%s</div></div>'
            % (" assumed" if row["assumed"] else "", esc(row["label"]), chip, esc(row["value"]))
        )
    return '<div class="params">%s</div>' % cells


def render_stats(m):
    st = m["stats"]
    pass_rate = (st["cases_passed"] / st["cases_total"]) if st["cases_total"] else None
    rate_cls = ""
    if pass_rate is not None:
        rate_cls = "green" if pass_rate >= 0.8 else ("yellow" if pass_rate >= 0.5 else "red")
    cells = [
        ("%d / %d" % (st["cases_run"], st["cases_total"]), "cases run", ""),
        (fmt_pct(pass_rate) if pass_rate is not None else DASH, "case pass rate", rate_cls),
        ("est. " + fmt_tokens(st["est_tokens_total"]), "total tokens (est., chars/4)", ""),
        ("~" + fmt_ms(st["median_latency"]), "median latency (~, incl. hook overhead)", ""),
    ]
    html_out = '<div class="stats">'
    for val, label, cls in cells:
        html_out += '<div class="stat"><div class="stat-val %s">%s</div><div class="stat-label">%s</div></div>' % (
            cls, val, esc(label),
        )
    return html_out + "</div>"


def render_budget(m):
    st = m["stats"]
    window = m["context_window"] or DEFAULT_CONTEXT_WINDOW
    total = st["est_tokens_total"]
    errs = st["est_tokens_error"]
    useful = max(total - errs, 0)
    pct = (total / window) if window else 0
    over = pct > 1
    body = (
        '<div class="budget-header">'
        '<span>%d tool call(s) across %d case(s), payload only</span>'
        '<span>est. %s / %s tokens (%s of context window)</span>'
        "</div>"
        % (st["n_calls"], st["cases_total"], fmt_tokens(total), fmt_tokens(window), fmt_pct(min(pct, 9.99)))
    )
    useful_pct = min(useful / window * 100, 100) if window else 0
    err_pct = min(errs / window * 100, 100 - useful_pct) if window else 0
    body += (
        '<div class="budget-track">'
        '<div class="budget-seg" style="width:%.1f%%;background:var(--green)"></div>'
        '<div class="budget-seg" style="width:%.1f%%;background:var(--red)"></div>'
        "</div>" % (useful_pct, err_pct)
    )
    body += (
        '<div class="budget-legend">'
        '<div class="budget-legend-item"><span class="budget-dot" style="background:var(--green)"></span>'
        "successful payloads (est. %s)</div>"
        '<div class="budget-legend-item"><span class="budget-dot" style="background:var(--red)"></span>'
        "error payloads (est. %s)</div>"
        '<div class="budget-legend-item">window: %s tokens</div>'
        "</div>" % (fmt_tokens(useful), fmt_tokens(errs), fmt_tokens(window))
    )
    if over:
        body += (
            '<div class="traj-note bad">These payloads together exceed the %s-token window '
            "(est.). Sub-agent containment is the only reason a single session survived them.</div>"
            % fmt_tokens(window)
        )
    return section(
        "Context budget", "payload est. tokens vs a %s-token window" % fmt_tokens(window)
    ) + '<div class="budget">%s</div>' % body


def render_tool_cards(m):
    cards = m["tool_cards"]
    out = section("Per-tool", "token figures est. (chars/4) · latency ~ (incl. hook overhead)")
    if not cards:
        return out + '<div class="empty">No tools in plan.json and no tool calls in telemetry.</div>'
    out += '<div class="tool-grid">'
    for c in cards:
        skipped = c["in_scope"] is False
        a = c["assertions"]
        graded_n = a["passed"] + a["failed"] + a["ungradable"]
        if skipped:
            grade = '<span class="badge badge-neutral">skipped</span>'
        elif graded_n == 0:
            grade = '<span class="badge badge-neutral">ungraded</span>'
        elif a["failed"]:
            grade = '<span class="badge badge-fail">%d/%d assertions</span>' % (a["passed"], graded_n)
        elif a["ungradable"]:
            grade = '<span class="badge badge-partial">%d/%d assertions</span>' % (a["passed"], graded_n)
        else:
            grade = '<span class="badge badge-pass">%d/%d assertions</span>' % (a["passed"], graded_n)

        body = ""
        if skipped:
            body += '<div class="kv"><span class="k">not run</span><span class="v">%s</span></div>' % esc(
                str(c["skip_reason"] or "out of scope")
            )
        if c["write_capable"]:
            body += '<div class="kv"><span class="k">write-capable</span><span class="v yellow">yes</span></div>'
        if not c["in_plan"]:
            body += '<div class="kv"><span class="k">source</span><span class="v yellow">not in plan (other server)</span></div>'

        if c["n_calls"] == 0:
            body += '<div class="kv"><span class="k">calls</span><span class="v">0 &mdash; never called</span></div>'
        else:
            err_rate = c["error_rate"]
            err_cls = "green" if not err_rate else ("red" if err_rate >= 0.25 else "yellow")
            body += (
                '<div class="metric-group"><h4>Payload economics</h4>'
                '<div class="kv"><span class="k">calls</span><span class="v">%d in %d case(s)</span></div>'
                '<div class="kv"><span class="k">median payload</span><span class="v">%s</span></div>'
                '<div class="kv"><span class="k">median tokens</span><span class="v">est. %s</span></div>'
                '<div class="kv"><span class="k">total tokens</span><span class="v">est. %s</span></div>'
                "%s</div>"
                % (
                    c["n_calls"], c["n_cases"], fmt_bytes(c["bytes_median"]),
                    fmt_tokens(c["est_tokens_median"]), fmt_tokens(c["est_tokens_total"]),
                    '<div class="kv"><span class="k">payload capture</span>'
                    '<span class="v yellow">hit the 200 KB cap</span></div>' if c["capped"] else "",
                )
            )
            body += (
                '<div class="metric-group"><h4>Latency</h4>'
                '<div class="kv"><span class="k">median</span><span class="v">~%s</span></div>'
                '<div class="kv"><span class="k">slowest</span><span class="v">~%s</span></div>'
                "</div>" % (fmt_ms(c["duration_median"]), fmt_ms(c["duration_max"]))
            )
            body += (
                '<div class="metric-group"><h4>Reliability</h4>'
                '<div class="kv"><span class="k">error rate</span><span class="v %s">%s</span></div>'
                "%s</div>"
                % (
                    err_cls,
                    fmt_pct(err_rate) if isinstance(err_rate, (int, float)) else DASH,
                    '<div class="kv"><span class="k">error kinds</span><span class="v red">%s</span></div>'
                    % esc(", ".join(c["error_kinds"])) if c["error_kinds"] else "",
                )
            )
        if c["found_of"]:
            found_cls = "green" if c["found_in"] == c["found_of"] else "red"
            body += (
                '<div class="metric-group"><h4>Discoverability</h4>'
                '<div class="kv"><span class="k">found by the agent</span><span class="v %s">%d/%d case(s)</span></div>'
                '<div class="kv"><span class="k">median calls to first correct</span><span class="v">%s</span></div>'
                "%s</div>"
                % (
                    found_cls, c["found_in"], c["found_of"],
                    ("%g" % c["calls_to_first"]) if c["calls_to_first"] is not None else DASH,
                    '<div class="kv"><span class="k">detours</span><span class="v yellow">%s</span></div>'
                    % esc(", ".join(sorted(set(c["detours"])))) if c["detours"] else "",
                )
            )
        out += (
            '<div class="tool-card%s"><div class="tool-card-head">'
            '<span class="tool-card-name">%s</span>%s</div>%s</div>'
            % (" skipped" if skipped else "", esc(c["name"]), grade, body)
        )
    return out + "</div>"


def render_trajectories(m):
    cases = [c for c in m["cases"] if c["level"] in ("L0", "L1")]
    out = section(
        "Discovery trajectory",
        "L0/L1 only · did the agent find the right tool, and what did it touch first?",
    )
    if not cases:
        return out + '<div class="empty">No L0 or L1 cases in this plan &mdash; nothing to trace.</div>'
    for c in cases:
        traj = c["trajectory"]
        found = traj.get("found_tool")
        detours = [str(d) for d in dlist(traj, "detours")]
        ctf = traj.get("calls_to_first_correct")

        head = (
            '<div class="traj-head"><span class="badge badge-level">%s</span>'
            '<span class="cid">%s</span>%s' % (
                esc(c["level"] or "?"), esc(c["id"]),
                '<span class="badge badge-info">target: %s</span>' % esc(c["tool"]) if c["tool"]
                else '<span class="badge badge-neutral">no named target (server-level discovery)</span>',
            )
        )
        head += '<span class="spacer"></span></div>'

        nodes = ['<span class="node start">task issued</span>']
        for call in c["calls"]:
            row = call["row"]
            cls = "err" if row.get("is_error") else ("hit" if call["on_target"] else "detour")
            nodes.append(
                '<span class="node %s">%s%s</span>'
                % (
                    cls, esc(call["qualified"]),
                    " &middot; error" if row.get("is_error") else "",
                )
            )
        if len(nodes) == 1:
            for d in detours:
                nodes.append('<span class="node detour">%s</span>' % esc(d))
            if found is True and c["tool"]:
                nodes.append('<span class="node hit">%s</span>' % esc(c["tool"]))
        path = '<div class="traj-path">%s</div>' % '<span class="arrow">&rarr;</span>'.join(nodes)

        notes = []
        if found is True:
            notes.append("Found the target tool.")
        elif found is False:
            notes.append("Never reached the target tool.")
        else:
            notes.append("Whether the target tool was found was not graded.")
        if detours:
            notes.append("Detoured into: %s." % ", ".join(detours))
        elif found is True:
            notes.append("No detours.")
        if isinstance(ctf, (int, float)):
            notes.append("%g call(s) before the first correct one." % ctf)
        n_err = sum(1 for call in c["calls"] if call["row"].get("is_error"))
        if n_err:
            notes.append("%d call(s) returned an error." % n_err)
        if not c["calls"]:
            notes.append("No telemetry recorded for this case.")
        note_cls = "traj-note bad" if found is False else "traj-note"
        out += '<div class="traj">%s%s<div class="%s">%s</div></div>' % (
            head, path, note_cls, esc(" ".join(notes)),
        )
    return out


STATE_LABEL = {
    "verified": "verified",
    "fabricated": "NO &mdash; fabrication",
    "unverifiable": "unverifiable",
}
STATE_ROW_CLASS = {"verified": "", "fabricated": "fabrication", "unverifiable": "unverifiable"}


def render_grounding(m):
    rows = m["grounding_rows"]
    fabs, unver = m["fabrications"], m["unverifiable"]
    out = section(
        "Grounding",
        "every claim in a deliverable, checked against the captured payload of the call it cites",
    )
    out += (
        '<div class="counts">'
        '<div class="fab-count"><span class="n %s">%d</span><span class="lbl">%s</span></div>'
        '<div class="fab-count"><span class="n %s">%d</span><span class="lbl">%s</span></div>'
        "</div>"
        % (
            "zero" if fabs == 0 else "some", fabs,
            "fabrication(s) &mdash; claims contradicted by, or absent from, an intact payload",
            "none" if unver == 0 else "warn", unver,
            "unverifiable &mdash; no intact payload to check against; not counted as fabrication",
        )
    )
    if m["fabrication_reported"] != m["fabrication_listed"] and rows:
        out += (
            '<div class="traj-note">grades_summary/grading reported %d fabrication(s); the claim '
            "rows list %d. The claim rows are authoritative per the workspace contract, so the "
            "count above comes from them.</div>"
            % (m["fabrication_reported"], m["fabrication_listed"])
        )
    if not rows:
        out += '<div class="empty">No claims were recorded in any grading.json.</div>'
        return out
    out += (
        '<table class="tbl"><thead><tr><th>Case</th><th>Claim</th><th>Source tool call</th>'
        "<th>Grounded</th><th>Reason</th></tr></thead><tbody>"
    )
    for r in rows:
        if r["source_tool"]:
            src = '<span class="mono">%s</span><span class="mini claim-reason">%s</span>' % (
                esc(str(r["source_tool"])), esc(str(r["source_id"])),
            )
        elif r["source_id"]:
            src = '<span class="mono">%s</span>' % esc(str(r["source_id"]))
        else:
            src = "no source cited"
        out += (
            '<tr class="%s"><td class="mono">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
            % (
                STATE_ROW_CLASS[r["state"]], esc(r["case"]), esc(r["claim"]), src,
                STATE_LABEL[r["state"]], esc(r["reason"]) if r["reason"] else DASH,
            )
        )
    return out + "</tbody></table>"


def render_caveats(m):
    out = section("Caveats", "what this report does not claim")
    body = '<h4>True of every mcp-eval report</h4><ul>%s</ul>' % "".join(
        '<li class="standing">%s</li>' % esc(c) for c in STANDING_CAVEATS
    )
    if m["caveats"]:
        body += '<h4>From this run</h4><ul>%s</ul>' % "".join(
            "<li>%s</li>" % esc(c) for c in m["caveats"]
        )
    else:
        body += '<h4>From this run</h4><div class="empty">No run-specific caveats were recorded.</div>'
    return out + '<div class="caveats">%s</div>' % body


def render_payload(call):
    """Payload excerpt for one call, plus where the full capture lives.

    The full payloads are up to 200 KB each and never inlined into this page.
    """
    excerpt = call["excerpt"]
    payload = call["payload"]
    out = ""
    if excerpt:
        out += '<pre class="box excerpt">%s</pre>' % esc(excerpt)
    if payload:
        note = 'full payload: <span class="path">%s</span>' % esc(payload["path"])
        if payload["truncated"]:
            note += (
                ' <span class="capped">&mdash; truncated at the 200 KB cap, so anything past '
                "that point cannot be grounded</span>"
            )
        out += '<div class="payload-note">%s</div>' % note
    elif excerpt:
        out += (
            '<div class="payload-note">excerpt only &mdash; no payload file captured for this '
            "call</div>"
        )
    else:
        out += '<div class="payload-note">no payload captured for this call</div>'
    return out


def render_cases(m):
    out = section(
        "Case detail",
        "click a case to expand",
        '<span class="controls"><button data-all="open">expand all</button>'
        '<button data-all="close">collapse all</button></span>',
    )
    if not m["cases"]:
        return out + '<div class="empty">No cases found in plan.json or on disk.</div>'

    badge_for = {
        "pass": ("badge-pass", "pass"),
        "fail": ("badge-fail", "fail"),
        "partial": ("badge-partial", "partial"),
        "ungraded": ("badge-neutral", "ungraded"),
        "failed-to-run": ("badge-fail", "sub-agent failed"),
        "skipped": ("badge-neutral", "skipped"),
    }
    for c in m["cases"]:
        cls, label = badge_for.get(c["outcome"], ("badge-neutral", c["outcome"]))
        tokens = sum(
            r["row"].get("est_tokens") or 0 for r in c["calls"]
            if isinstance(r["row"].get("est_tokens"), (int, float))
        )
        summary_line = (
            '<summary><span class="badge %s">%s</span>'
            '<span class="badge badge-level">%s</span>'
            '<span class="cid">%s</span>'
            '<span class="spacer"></span>'
            '<span class="mini">%s &middot; %d call(s) &middot; est. %s tokens</span></summary>'
            % (
                cls, esc(label), esc(c["level"] or "?"), esc(c["id"]),
                esc(str(c["tool"] or "server-level")), len(c["calls"]), fmt_tokens(tokens),
            )
        )

        body = '<div class="case-body">'
        body += (
            '<div class="case-block"><h4>Run</h4>'
            '<div class="kv"><span class="k">status</span><span class="v">%s</span></div>'
            '<div class="kv"><span class="k">ran on</span><span class="v">%s</span></div>'
            "</div>" % (esc(str(c["status"])), esc(str(c["model"] or "unrecorded")))
        )
        if c["task"]:
            body += '<div class="case-block"><h4>Task given to the sub-agent</h4><pre class="box">%s</pre></div>' % esc(c["task"])
        if c["deliverable"]:
            body += '<div class="case-block"><h4>Deliverable</h4><pre class="box">%s</pre></div>' % esc(c["deliverable"])
        elif c["outcome"] == "failed-to-run":
            body += '<div class="case-block"><h4>Deliverable</h4><div class="empty">The sub-agent failed; no deliverable was returned.</div></div>'

        if c["assertions"]:
            items = ""
            for a in c["assertions"]:
                if a["passed"] is True:
                    state, scls = "PASS", "pass"
                elif a["passed"] is False:
                    state, scls = "FAIL", "fail"
                else:
                    state, scls = "UNGRADABLE", "ungradable"
                method = ' <span class="badge badge-neutral">%s</span>' % esc(a["method"]) if a["method"] else ""
                evidence = '<div class="assert-evidence">%s</div>' % esc(a["evidence"]) if a["evidence"] else ""
                items += '<li><span class="assert-state %s">%s</span>%s%s%s</li>' % (
                    scls, state, esc(a["text"]), method, evidence,
                )
            heading = "Assertions" if c["has_grading"] else "Assertions (planned, not graded)"
            body += '<div class="case-block"><h4>%s</h4><ul class="plain">%s</ul></div>' % (esc(heading), items)

        if c["claimed_sources"]:
            body += '<div class="case-block"><h4>Sources the sub-agent claimed</h4><ul class="plain">%s</ul></div>' % "".join(
                "<li>%s</li>" % esc(str(s)) for s in c["claimed_sources"]
            )
        if c["friction"]:
            body += '<div class="case-block"><h4>Friction the sub-agent reported</h4><ul class="plain">%s</ul></div>' % "".join(
                "<li>%s</li>" % esc(str(f)) for f in c["friction"]
            )

        if c["calls"]:
            rows = ""
            for i, call in enumerate(c["calls"], 1):
                r = call["row"]
                err = r.get("is_error")
                rows += (
                    '<tr class="%s"><td class="num">%d</td><td class="mono">%s</td>'
                    '<td class="mono">%s</td><td class="num">~%s</td><td class="num">%s</td>'
                    '<td class="num">est. %s</td><td>%s</td></tr>'
                    % (
                        "fabrication" if err else "", i, esc(call["qualified"]),
                        esc(short_json(r.get("args"))), fmt_ms(r.get("duration_ms")),
                        fmt_bytes(r.get("payload_bytes")), fmt_tokens(r.get("est_tokens")),
                        esc(str(r.get("error_kind") or "none")),
                    )
                )
                rows += (
                    '<tr class="excerpt-row"><td></td><td colspan="6">%s</td></tr>'
                    % render_payload(call)
                )
            body += (
                '<div class="case-block"><h4>Tool calls (telemetry)</h4>'
                '<table class="tbl"><thead><tr><th>#</th><th>Tool</th><th>Args</th>'
                "<th>~Latency</th><th>Payload</th><th>Tokens (est.)</th><th>Error</th></tr></thead>"
                "<tbody>%s</tbody></table></div>" % rows
            )
        else:
            body += '<div class="case-block"><h4>Tool calls (telemetry)</h4><div class="empty">No tool calls recorded for this case.</div></div>'

        out += "<details class=\"case\">%s%s</div></details>" % (summary_line, body)
    return out


def render_gaps(m):
    if not m["gaps"]:
        return ""
    return '<div class="gaps"><h4>Partial workspace</h4><ul>%s</ul></div>' % "".join(
        "<li>%s</li>" % esc(g) for g in m["gaps"]
    )


def render_html(m):
    interview = m["interview"]
    meta_bits = []
    if m["created"]:
        meta_bits.append(esc("planned %s" % m["created"]))
    if interview.get("operator_model"):
        bit = esc("operator model: %s" % interview["operator_model"])
        if "operator_model" in m["unanswered"]:
            bit += ' <span class="chip">assumed</span>'
        meta_bits.append(bit)
    meta_bits.append(esc("%d case(s)" % m["stats"]["cases_total"]))
    meta = "".join("<span>%s</span>" % b for b in meta_bits)

    blob = json.dumps(m["raw"], ensure_ascii=False, default=str).replace("<", "\\u003c")

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>%s &middot; mcp-eval report</title>" % esc(m["server"]),
        "<style>%s</style></head><body><div class=\"page\">" % CSS,
        '<div class="topbar"><h1>%s</h1><div class="meta">%s</div></div>' % (esc(m["server"]), meta),
        render_gaps(m),
        render_verdict(m),
        render_stats(m),
        render_budget(m),
        render_tool_cards(m),
        render_trajectories(m),
        render_grounding(m),
        render_caveats(m),
        render_cases(m),
        '<div class="foot"><span>mcp-eval &middot; workspace: %s</span><span>generated %s</span></div>'
        % (esc(m["workspace"]), esc(m["raw"]["generated"])),
        "</div>",
        '<script type="application/json" id="eval-data">%s</script>' % blob,
        "<script>%s</script>" % JS,
        "</body></html>",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Render an mcp-eval workspace into a self-contained HTML dashboard."
    )
    parser.add_argument("workspace", nargs="?", default=DEFAULT_WORKSPACE,
                        help="eval workspace directory (default: %s)" % DEFAULT_WORKSPACE)
    parser.add_argument("--output", help="output HTML path (default: <workspace>/eval-report.html)")
    parser.add_argument("--context-window", type=int, default=DEFAULT_CONTEXT_WINDOW,
                        help="context window the budget bar is drawn against (default: %d)" % DEFAULT_CONTEXT_WINDOW)
    args = parser.parse_args(argv)

    ws = Path(args.workspace)
    if not ws.is_dir():
        print("Error: %s is not a directory. Pass the eval workspace path." % ws, file=sys.stderr)
        return 1

    model = build_model(ws, args.context_window)
    out_path = Path(args.output) if args.output else ws / "eval-report.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(model), encoding="utf-8")

    st = model["stats"]
    print("Report: %s" % out_path)
    print(
        "  verdict: %s | cases %d/%d passed | est. %s tokens | ~%s median latency"
        % (
            model["verdict"] or "none recorded",
            st["cases_passed"], st["cases_total"],
            fmt_tokens(st["est_tokens_total"]), fmt_ms(st["median_latency"]),
        )
    )
    for gap in model["gaps"]:
        print("  note: %s" % gap)
    return 0


if __name__ == "__main__":
    sys.exit(main())
