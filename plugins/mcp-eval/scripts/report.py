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
import base64
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
#
# The page is one paper sheet on a desk, set in the Ellypsis OS tokens. Reading
# order follows the questions a reader actually has: what is the verdict, what
# did the run look like, which tool is the problem, did the agent find its way,
# did it make anything up, what does the report not claim, and only then the
# per-case evidence. Every number that is an estimate or approximate says so
# where it is printed; nothing is derived here that grading did not decide.

CSS = r"""
*, *::before, *::after { box-sizing: border-box; }
:root {
  --paper: #fbfaf6; --desk: #e9e3d3; --panel: #f2efe6; --ink: #191713;
  --accent: #7c3f63; --accent-tint: #f0e4eb; --accent-dark: #5e2f4b;
  --green: #55743e; --amber: #b5893a; --red: #a63a50;
  --body:  color-mix(in srgb, var(--ink) 84%, var(--paper));
  --body2: color-mix(in srgb, var(--ink) 92%, var(--paper));
  --muted: color-mix(in srgb, var(--ink) 60%, var(--paper));
  --faint: color-mix(in srgb, var(--ink) 36%, var(--paper));
  --paper2: color-mix(in srgb, var(--paper) 60%, var(--panel));
  --line:  color-mix(in srgb, var(--ink) 20%, transparent);
  --line2: color-mix(in srgb, var(--ink) 42%, transparent);
  --bar:   color-mix(in srgb, var(--ink) 58%, var(--paper));
  --track: color-mix(in srgb, var(--ink) 9%, var(--paper));
  --ok-ink: var(--green);
  --warn-ink: color-mix(in srgb, var(--amber) 72%, var(--ink));
  --bad-ink: var(--red);
  --ok-tint:   color-mix(in srgb, var(--green) 11%, var(--paper));
  --warn-tint: color-mix(in srgb, var(--amber) 14%, var(--paper));
  --bad-tint:  color-mix(in srgb, var(--red) 10%, var(--paper));
  --rx: 1; --bw: 2px; --mess: 1; --dash: dashed;
  --shadow-card: 4px 5px 0 color-mix(in srgb, var(--ink) 16%, transparent);
  --shadow-window: 0 24px 60px color-mix(in srgb, var(--ink) 22%, transparent);
  --f-display: "Tanker", "Switzer", system-ui, sans-serif;
  --f-body: "Switzer", system-ui, -apple-system, "Segoe UI", sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --f-quote: Georgia, "Times New Roman", serif;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #221e17; --desk: #131110; --panel: #2b261d; --ink: #f0ead9;
    --accent: #c795b1; --accent-tint: #3f1f33; --accent-dark: #d8aec7;
    --ok-ink:   color-mix(in srgb, var(--green) 58%, var(--ink));
    --warn-ink: color-mix(in srgb, var(--amber) 70%, var(--ink));
    --bad-ink:  color-mix(in srgb, var(--red) 60%, var(--ink));
    --ok-tint:   color-mix(in srgb, var(--green) 22%, var(--paper));
    --warn-tint: color-mix(in srgb, var(--amber) 22%, var(--paper));
    --bad-tint:  color-mix(in srgb, var(--red) 24%, var(--paper));
    --shadow-card: 4px 5px 0 color-mix(in srgb, var(--ink) 10%, transparent);
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #221e17; --desk: #131110; --panel: #2b261d; --ink: #f0ead9;
  --accent: #c795b1; --accent-tint: #3f1f33; --accent-dark: #d8aec7;
  --ok-ink:   color-mix(in srgb, var(--green) 58%, var(--ink));
  --warn-ink: color-mix(in srgb, var(--amber) 70%, var(--ink));
  --bad-ink:  color-mix(in srgb, var(--red) 60%, var(--ink));
  --ok-tint:   color-mix(in srgb, var(--green) 22%, var(--paper));
  --warn-tint: color-mix(in srgb, var(--amber) 22%, var(--paper));
  --bad-tint:  color-mix(in srgb, var(--red) 24%, var(--paper));
  --shadow-card: 4px 5px 0 color-mix(in srgb, var(--ink) 10%, transparent);
  color-scheme: dark;
}

html { font-size: 15px; }
body {
  margin: 0; background: var(--desk); color: var(--body2);
  font-family: var(--f-body); line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 2px; }
b, strong { font-weight: 600; }
small { font-size: inherit; }

/* -- the sheet ------------------------------------------------------------- */
.desk { padding: 32px 20px 72px; }
.sheet {
  max-width: 1120px; margin: 0 auto; background: var(--paper);
  border: 1.5px solid var(--line2); border-radius: calc(12px * var(--rx));
  box-shadow: var(--shadow-window); padding: 44px 52px 56px;
}
@media (max-width: 760px) {
  .desk { padding: 12px 8px 40px; }
  .sheet { padding: 26px 18px 36px; }
}

/* -- type roles ------------------------------------------------------------ */
.kicker {
  font: 500 11px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: lowercase;
  color: var(--muted); margin: 0 0 8px;
}
.mono { font-family: var(--f-mono); }
.num { font-variant-numeric: tabular-nums; }
h1.server {
  font: 400 clamp(36px, 4.4vw, 52px)/1.05 var(--f-display); margin: 0 0 14px;
  color: var(--ink); text-wrap: balance; word-break: break-word;
}
.masthead { padding-bottom: 22px; border-bottom: var(--bw) solid var(--ink); margin-bottom: 26px; }
.meta { display: flex; flex-wrap: wrap; gap: 6px 22px; font: 11.5px/1.7 var(--f-mono); color: var(--body); }
.meta .chip { margin-left: 6px; }

.sec { margin-top: 52px; }
.sec-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap;
            padding-bottom: 10px; border-bottom: 1.5px var(--dash) var(--line2); margin-bottom: 18px; }
.sec-head .kicker { margin: 0 0 4px; }
.sec-head h2 { font: 400 28px/1.15 var(--f-display); margin: 0; color: var(--ink); }
.sec-head .sub { font-size: 13.5px; color: var(--muted); margin: 4px 0 0; max-width: 70ch; }
.sec-head .tools-right { display: flex; gap: 8px; align-items: center; }
h3.sub-title { font: 500 11px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: lowercase;
               color: var(--muted); margin: 26px 0 10px; display: flex; gap: 14px; align-items: baseline; flex-wrap: wrap; }
h3.sub-title .hint { font-family: var(--f-body); letter-spacing: 0; text-transform: none; font-weight: 400; font-size: 12.5px; }
.empty { font-size: 13px; color: var(--muted); padding: 8px 0; }

/* -- chips, stamps, badges ------------------------------------------------- */
.chip {
  display: inline-block; vertical-align: middle; white-space: nowrap;
  font: 500 9.5px/1 var(--f-mono); letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--warn-ink); border: 1.5px solid var(--warn-ink);
  border-radius: calc(3px * var(--rx)); padding: 3px 6px; background: var(--paper);
  transform: rotate(calc(-2deg * var(--mess)));
}
.lvl {
  display: inline-block; font: 500 10px/1 var(--f-mono); letter-spacing: 0.06em;
  border: 1.5px solid var(--line2); border-radius: calc(4px * var(--rx));
  padding: 3px 6px; color: var(--body); background: var(--paper);
}
.tag {
  display: inline-block; font: 10.5px/1 var(--f-mono); border: 1.5px solid var(--line2);
  border-radius: calc(999px * var(--rx)); padding: 4px 9px; color: var(--muted); white-space: nowrap;
}
.tag.warn { color: var(--warn-ink); border-color: var(--warn-ink); }
.tag.dashed { border-style: var(--dash); }
.badge {
  display: inline-block; font: 500 11px/1 var(--f-mono); padding: 4px 8px;
  border-radius: calc(4px * var(--rx)); white-space: nowrap; border: 1.5px solid transparent;
}
.badge-pass { color: var(--ok-ink); border-color: var(--ok-ink); background: var(--ok-tint); }
.badge-fail { color: var(--bad-ink); border-color: var(--bad-ink); background: var(--bad-tint); }
.badge-partial { color: var(--warn-ink); border-color: var(--warn-ink); background: var(--warn-tint); }
.badge-neutral { color: var(--muted); border-color: var(--line2); border-style: var(--dash); }
.st { display: inline-flex; align-items: center; gap: 6px; font: 500 12px/1.2 var(--f-mono); white-space: nowrap; }
.st.ok { color: var(--ok-ink); } .st.warn { color: var(--warn-ink); } .st.bad { color: var(--bad-ink); } .st.none { color: var(--muted); }
.st i { font-style: normal; font-size: 11px; }
.ok { color: var(--ok-ink); } .warn { color: var(--warn-ink); } .bad { color: var(--bad-ink); }

/* -- gaps ------------------------------------------------------------------ */
.gaps {
  border: 1.5px var(--dash) var(--warn-ink); border-radius: calc(8px * var(--rx));
  padding: 12px 16px; margin-bottom: 22px; background: var(--warn-tint);
}
.gaps h4 { margin: 0 0 4px; font: 500 11px/1.4 var(--f-mono); letter-spacing: 0.08em; color: var(--warn-ink); text-transform: lowercase; }
.gaps ul { margin: 0; padding-left: 18px; }
.gaps li { font-size: 13px; color: var(--body); }

/* -- verdict --------------------------------------------------------------- */
.verdict {
  position: relative; background: var(--paper); border: var(--bw) solid var(--ink);
  border-radius: calc(10px * var(--rx)); box-shadow: var(--shadow-card);
  padding: 24px 28px 22px; margin: 0 6px 6px 0;
}
.verdict-word {
  font: 400 clamp(40px, 5.2vw, 62px)/1 var(--f-display); color: var(--ink);
  margin: 2px 0 14px; text-wrap: balance;
}
.verdict.v-ship .verdict-word { color: var(--ok-ink); }
.verdict.v-caveats .verdict-word { color: var(--warn-ink); }
.verdict.v-stop .verdict-word { color: var(--bad-ink); }
.verdict-reasoning { font-size: 16px; line-height: 1.6; color: var(--body2); max-width: 72ch; margin: 0; }
.verdict-tally {
  margin-top: 18px; padding-top: 12px; border-top: 1.5px var(--dash) var(--line2);
  display: flex; flex-wrap: wrap; gap: 6px 22px; font: 11.5px/1.8 var(--f-mono); color: var(--muted);
}
.verdict-tally b { color: var(--ink); font-weight: 500; }
.params {
  margin-top: 16px; padding-top: 14px; border-top: 1.5px var(--dash) var(--line2);
  display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px 26px;
}
.params-label { grid-column: 1 / -1; font: 500 11px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: lowercase; color: var(--muted); }
.param-label { font: 500 10px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted);
               display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
.param-value { font-size: 13.5px; color: var(--body2); line-height: 1.45; }
.param.assumed .param-value { color: var(--warn-ink); }

/* -- case strip ------------------------------------------------------------ */
.strip { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 22px; }
.cell {
  flex: 1 1 150px; min-width: 0; display: flex; flex-direction: column; gap: 5px;
  padding: 9px 11px 10px; border: 1.5px solid var(--line2); border-top: 4px solid var(--line2);
  border-radius: calc(6px * var(--rx)); background: var(--paper2); color: var(--body);
  font-family: var(--f-mono); text-decoration: none;
}
.cell:hover { text-decoration: none; background: color-mix(in srgb, var(--ink) 5%, var(--paper2)); }
.cell-id { font-size: 11.5px; color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cell-row { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.cell-tool { font-size: 10px; color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cell.pass { border-top-color: var(--green); background: var(--ok-tint); }
.cell.fail, .cell.failed-to-run { border-top-color: var(--red); background: var(--bad-tint); }
.cell.partial { border-top-color: var(--amber); background: var(--warn-tint); }
.cell.ungraded, .cell.skipped { border-style: var(--dash); border-top-style: solid; border-top-color: var(--faint); }
.cell.failed-to-run { border-style: var(--dash); border-top-style: solid; }

/* -- stat tiles ------------------------------------------------------------ */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 0 26px; margin: 0 0 8px; }
.stat { padding: 12px 0 14px; border-top: 1.5px var(--dash) var(--line2); }
.stat-label { font-size: 12.5px; color: var(--muted); }
.stat-val { font: 400 38px/1.05 var(--f-display); color: var(--ink); margin: 6px 0 4px; white-space: nowrap; }
.stat-val small { font: 500 12px/1 var(--f-mono); color: var(--muted); margin-right: 5px; vertical-align: 6px; }
.stat-val.green { color: var(--ok-ink); } .stat-val.yellow { color: var(--warn-ink); } .stat-val.red { color: var(--bad-ink); }
.stat-note { font: 11px/1.5 var(--f-mono); color: var(--muted); }
.stat-val .nodata { font: 400 30px/1 var(--f-body); color: var(--faint); }

/* -- context budget -------------------------------------------------------- */
.budget { padding: 4px 0 0; }
.budget-header { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px 16px;
                 font: 11.5px/1.6 var(--f-mono); color: var(--muted); margin-bottom: 8px; }
.budget-header b { color: var(--ink); font-weight: 500; }
.budget-track { height: 14px; background: var(--track); border-radius: calc(4px * var(--rx)); overflow: hidden; display: flex; }
.budget-seg { height: 100%; }
.budget-seg.useful { background: var(--bar); border-radius: 0 4px 4px 0; }
.budget-seg.err { background: var(--red); border-radius: 0 4px 4px 0; margin-left: 2px; }
.budget-legend { display: flex; gap: 6px 20px; flex-wrap: wrap; margin-top: 8px; font: 11px/1.6 var(--f-mono); color: var(--muted); }
.budget-legend-item { display: inline-flex; align-items: center; gap: 6px; }
.budget-dot { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
.note { font-size: 13px; color: var(--muted); margin: 10px 0 0; max-width: 78ch; }
.note.bad { color: var(--bad-ink); }

/* -- tables ---------------------------------------------------------------- */
.tbl-wrap { overflow-x: auto; }
.tbl { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.tbl th {
  text-align: left; vertical-align: bottom; padding: 8px 10px 8px 0;
  font: 500 10.5px/1.4 var(--f-mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted);
  border-bottom: 1.5px solid var(--line2); white-space: nowrap;
}
.tbl th small { display: block; text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--faint); white-space: normal; }
.tbl td { padding: 10px 10px 10px 0; border-bottom: 1px var(--dash) var(--line); vertical-align: top; }
.tbl tr:last-child td { border-bottom: none; }
.tbl td small { display: block; font: 10.5px/1.5 var(--f-mono); color: var(--muted); margin-top: 3px; }
.tbl td.num, .tbl th.num { text-align: right; font-family: var(--f-mono); font-size: 12.5px; font-variant-numeric: tabular-nums; white-space: nowrap; }
.tbl td.mono { font-family: var(--f-mono); font-size: 12px; overflow-wrap: anywhere; }
.tbl td.case { font-family: var(--f-mono); font-size: 12px; white-space: nowrap; }
.tbl td.tight { white-space: nowrap; }
.tbl tr.skipped td { color: var(--muted); }

/* per-tool rows */
.tools td.tool { min-width: 150px; max-width: 230px; }
.tool-name { font: 500 13px/1.3 var(--f-mono); color: var(--ink); word-break: break-all; }
.tool-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 6px; }
.bar-cell { min-width: 150px; }
.bar { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 8px; height: 16px; }
.bar i { display: block; height: 10px; background: var(--bar); border-radius: 0 4px 4px 0; min-width: 2px; }
.bar b { font: 500 11.5px/1 var(--f-mono); color: var(--ink); white-space: nowrap; font-variant-numeric: tabular-nums; }
.bar.zero i { display: none; }

/* claims */
.tbl tr.fabrication td:first-child { box-shadow: inset 3px 0 var(--red); padding-left: 10px; }
.tbl tr.fabrication td { background: var(--bad-tint); }
.tbl tr.unverifiable td:first-child { box-shadow: inset 3px 0 var(--amber); padding-left: 10px; }
.tbl tr.unverifiable td { background: var(--warn-tint); }
.tbl tr.err td:first-child { box-shadow: inset 3px 0 var(--red); padding-left: 10px; }
.claim-reason { display: block; font-size: 12px; color: var(--muted); margin-top: 3px; }

/* -- grounding counts ------------------------------------------------------ */
.counts { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0 26px; margin-bottom: 18px; }
.fab-count { display: flex; align-items: flex-start; gap: 16px; padding: 4px 0 14px; }
.fab-count .n { font: 400 46px/1 var(--f-display); min-width: 1.2ch; }
.fab-count .n.zero { color: var(--ok-ink); } .fab-count .n.some { color: var(--bad-ink); }
.fab-count .n.warn { color: var(--warn-ink); } .fab-count .n.none { color: var(--faint); }
.fab-count .lbl { font-size: 13px; color: var(--body); max-width: 40ch; line-height: 1.5; padding-top: 4px; }
.fab-count .lbl b { display: block; color: var(--ink); font-weight: 500; }

/* -- trajectory ------------------------------------------------------------ */
.traj { padding: 14px 0 16px; border-top: 1.5px var(--dash) var(--line); }
.traj:first-of-type { border-top: none; padding-top: 4px; }
.traj-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }
.traj-head .cid { font: 500 13px/1.3 var(--f-mono); color: var(--ink); }
.traj-head .tgt { font: 11px/1.4 var(--f-mono); color: var(--muted); }
.path { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 0; }
.path li { display: inline-flex; align-items: center; }
.path li + li::before { content: ""; display: inline-block; width: 22px; height: 1.5px; background: var(--line2); margin: 0 2px; }
.node {
  font: 11.5px/1 var(--f-mono); padding: 7px 10px; border-radius: calc(6px * var(--rx));
  border: 1.5px solid var(--line2); color: var(--body); background: var(--paper); white-space: nowrap;
}
.node.start { border-style: var(--dash); color: var(--muted); }
.node.hit { border-color: var(--green); background: var(--ok-tint); color: var(--ok-ink); font-weight: 500; }
.node.detour { border-color: var(--amber); background: var(--warn-tint); color: var(--warn-ink); }
.node.err { border-color: var(--red); background: var(--bad-tint); color: var(--bad-ink); }
.traj-note { margin: 10px 0 0; font-size: 13px; color: var(--muted); }
.traj-note.bad { color: var(--bad-ink); }

/* -- caveats --------------------------------------------------------------- */
.caveats { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 8px 40px; }
.caveats h4 { margin: 0 0 6px; font: 500 11px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: lowercase; color: var(--muted); }
.caveats ul { margin: 0; padding-left: 18px; }
.caveats li { font-size: 13px; color: var(--body); margin: 6px 0; line-height: 1.5; }
.caveats li.standing { color: var(--body2); }

/* -- case detail ----------------------------------------------------------- */
.controls { display: flex; gap: 6px; }
.controls button {
  font: 11px/1 var(--f-mono); color: var(--muted); background: var(--paper);
  border: 1.5px solid var(--line2); border-radius: calc(999px * var(--rx)); padding: 6px 12px; cursor: pointer;
}
.controls button:hover { color: var(--ink); border-color: var(--ink); }
.case-anchor { scroll-margin-top: 20px; }
details.case { border: 1.5px solid var(--line2); border-radius: calc(8px * var(--rx)); margin-bottom: 8px; background: var(--paper); }
details.case[open] { border-color: var(--ink); }
details.case > summary {
  cursor: pointer; padding: 11px 14px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; list-style: none;
}
details.case > summary::-webkit-details-marker { display: none; }
details.case > summary::before { content: "\25B8"; font-size: 12px; color: var(--muted); width: 10px; }
details.case[open] > summary::before { content: "\25BE"; }
details.case > summary:hover { background: color-mix(in srgb, var(--ink) 4%, var(--paper)); }
summary .cid { font: 500 13px/1.3 var(--f-mono); color: var(--ink); }
.spacer { flex: 1; }
.mini { font: 11px/1.5 var(--f-mono); color: var(--muted); font-variant-numeric: tabular-nums; }
.case-body { padding: 6px 16px 18px; border-top: 1.5px var(--dash) var(--line2); }
.case-block { margin-top: 16px; }
.case-block h4 { margin: 0 0 6px; font: 500 10.5px/1.4 var(--f-mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.run-line { font: 11.5px/1.7 var(--f-mono); color: var(--body); }
.run-line b { color: var(--ink); font-weight: 500; }
.quote {
  margin: 0; padding: 2px 0 2px 16px; border-left: 2px solid var(--line2);
  font: italic 400 15.5px/1.6 var(--f-quote); color: var(--body2); white-space: pre-wrap; word-break: break-word; max-width: 80ch;
}
pre.box {
  margin: 0; background: var(--paper2); border: 1px solid var(--line); border-radius: calc(6px * var(--rx));
  padding: 10px 12px; font: 12px/1.55 var(--f-mono); color: var(--body); white-space: pre-wrap; word-break: break-word;
  max-height: 320px; overflow-y: auto;
}
pre.box.excerpt { font-size: 11px; color: var(--muted); max-height: 150px; margin-top: 2px; }
.payload-note { font: 11px/1.6 var(--f-mono); color: var(--muted); margin-top: 4px; }
.payload-note .path { color: var(--accent); }
.payload-note .capped { color: var(--warn-ink); }
ul.plain { list-style: none; margin: 0; padding: 0; }
ul.plain li { font-size: 13.5px; padding: 7px 0; border-bottom: 1px var(--dash) var(--line); line-height: 1.5; }
ul.plain li:last-child { border-bottom: none; }
.assert-state { display: inline-block; font: 500 10px/1 var(--f-mono); letter-spacing: 0.06em; padding: 3px 6px; margin-right: 8px;
                border-radius: calc(3px * var(--rx)); border: 1.5px solid currentColor; vertical-align: 1px; }
.assert-state.pass { color: var(--ok-ink); } .assert-state.fail { color: var(--bad-ink); } .assert-state.ungradable { color: var(--warn-ink); }
.assert-method { font: 10.5px/1 var(--f-mono); color: var(--muted); margin-left: 8px; }
.assert-evidence { color: var(--muted); font-size: 12.5px; margin-top: 3px; }
.excerpt-row td { padding-top: 0; }
.calls td { font-size: 12.5px; }

.foot { margin-top: 44px; padding-top: 14px; border-top: 1.5px var(--dash) var(--line2);
        display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; font: 11px/1.6 var(--f-mono); color: var(--faint); }

@media (max-width: 760px) {
  .verdict { padding: 18px 18px 16px; }
  .sec-head h2 { font-size: 24px; }
  .stat-val { font-size: 32px; }
}
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
"""

JS = """
document.addEventListener('click', function (e) {
  var btn = e.target.closest('button[data-all]');
  if (btn) {
    var open = btn.dataset.all === 'open';
    document.querySelectorAll('details.case').forEach(function (d) { d.open = open; });
    return;
  }
  var cell = e.target.closest('a.cell');
  if (cell) {
    var target = document.getElementById(cell.getAttribute('href').slice(1));
    var d = target && target.querySelector('details.case');
    if (d) d.open = true;
  }
});
"""

# Tanker and Switzer are the design system's faces. They are not shipped with
# the plugin; drop the woff2 files into scripts/fonts/ and the report embeds
# them. Without them the page falls back to the system stacks declared above.
FONT_FILES = [
    ("Tanker", "400", "tanker-400.woff2"),
    ("Switzer", "400", "switzer-400.woff2"),
    ("Switzer", "500", "switzer-500.woff2"),
    ("Switzer", "600 700", "switzer-600.woff2"),
]


def font_faces():
    fonts_dir = Path(__file__).resolve().parent / "fonts"
    faces = []
    for family, weight, name in FONT_FILES:
        path = fonts_dir / name
        if not path.is_file():
            continue
        try:
            data = base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError:
            continue
        faces.append(
            '@font-face{font-family:"%s";font-weight:%s;font-style:normal;font-display:swap;'
            'src:url(data:font/woff2;base64,%s) format("woff2")}' % (family, weight, data)
        )
    return "".join(faces)


OUTCOME_BADGE = {
    "pass": ("badge-pass", "pass"),
    "fail": ("badge-fail", "fail"),
    "partial": ("badge-partial", "partial"),
    "ungraded": ("badge-neutral", "ungraded"),
    "failed-to-run": ("badge-fail", "sub-agent failed"),
    "skipped": ("badge-neutral", "skipped"),
}
# icon + word, never colour alone
OUTCOME_MARK = {
    "pass": ("ok", "&#10003;", "pass"),
    "fail": ("bad", "&#10005;", "fail"),
    "partial": ("warn", "&#9684;", "partial"),
    "ungraded": ("none", "&#9675;", "ungraded"),
    "failed-to-run": ("bad", "&#10005;", "sub-agent failed"),
    "skipped": ("none", "&ndash;", "skipped"),
}


def sec_head(number, title, sub="", extra=""):
    right = '<div class="tools-right">%s</div>' % extra if extra else ""
    return (
        '<div class="sec-head"><div><div class="kicker">%s</div><h2>%s</h2>%s</div>%s</div>'
        % (number, esc(title), '<p class="sub">%s</p>' % esc(sub) if sub else "", right)
    )


def status_mark(outcome):
    cls, icon, word = OUTCOME_MARK.get(outcome, ("none", "&#9675;", outcome))
    return '<span class="st %s"><i>%s</i>%s</span>' % (cls, icon, esc(word))


def pct_of(value, maximum):
    value, maximum = as_number(value), as_number(maximum)
    if value is None or not maximum or value <= 0:
        return 0.0
    return max(1.5, min(100.0, value / maximum * 100))


def render_masthead(m):
    interview = m["interview"]
    bits = []
    if m["created"]:
        bits.append(esc("planned %s" % m["created"]))
    if interview.get("operator_model"):
        bit = esc("operator model: %s" % interview["operator_model"])
        if "operator_model" in m["unanswered"]:
            bit += '<span class="chip">assumed</span>'
        bits.append(bit)
    st = m["stats"]
    bits.append(esc("%d case(s)" % st["cases_total"]))
    bits.append(esc("%d tool(s) in plan" % sum(1 for t in m["tool_cards"] if t["in_plan"])))
    bits.append(esc("%d tool call(s) captured" % st["n_calls"]))
    return (
        '<header class="masthead"><div class="kicker">mcp-eval &middot; evaluation report</div>'
        '<h1 class="server">%s</h1><div class="meta">%s</div></header>'
        % (esc(m["server"]), "".join("<span>%s</span>" % b for b in bits))
    )


def render_gaps(m):
    if not m["gaps"]:
        return ""
    return '<div class="gaps"><h4>partial workspace</h4><ul>%s</ul></div>' % "".join(
        "<li>%s</li>" % esc(g) for g in m["gaps"]
    )


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
        + '<div class="kicker">01 &middot; verdict</div>'
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
        " &middot; %d assumed, not answered by the user" % len(m["unanswered"]) if m["unanswered"] else ""
    )
    for row in rows:
        stamp = '<span class="chip">assumed</span>' if row["assumed"] else ""
        cells += (
            '<div class="param%s"><div class="param-label">%s%s</div>'
            '<div class="param-value">%s</div></div>'
            % (" assumed" if row["assumed"] else "", esc(row["label"]), stamp, esc(row["value"]))
        )
    return '<div class="params">%s</div>' % cells


def render_strip(m):
    """One cell per case in plan order: the shape of the run in a glance."""
    if not m["cases"]:
        return ""
    cells = ""
    for c in m["cases"]:
        cells += (
            '<a class="cell %s" href="#case-%s"><div class="cell-row"><span class="lvl">%s</span>%s</div>'
            '<span class="cell-id">%s</span><span class="cell-tool">%s</span></a>'
            % (
                esc(c["outcome"]), esc(c["id"]), esc(c["level"] or "?"), status_mark(c["outcome"]),
                esc(c["id"]), esc(c["tool"] or "server-level discovery"),
            )
        )
    return '<div class="strip">%s</div>' % cells


NODATA = '<span class="nodata">%s</span>' % DASH


def render_stats(m):
    st = m["stats"]
    pass_rate = (st["cases_passed"] / st["cases_total"]) if st["cases_total"] else None
    rate_cls = ""
    if pass_rate is not None:
        rate_cls = "green" if pass_rate >= 0.8 else ("yellow" if pass_rate >= 0.5 else "red")
    cells = [
        ("cases run", "%d / %d" % (st["cases_run"], st["cases_total"]), "", "of the approved plan"),
        ("case pass rate", fmt_pct(pass_rate) if pass_rate is not None else NODATA, rate_cls,
         "%d of %d passed every assertion" % (st["cases_passed"], st["cases_total"])),
        ("total tokens (est., chars/4)", "<small>est.</small>%s" % fmt_tokens(st["est_tokens_total"]), "",
         "payload only, across %d call(s)" % st["n_calls"]),
        ("median latency (~, incl. hook overhead)",
         "<small>~</small>%s" % fmt_ms(st["median_latency"]) if st["median_latency"] is not None else NODATA, "",
         "wall clock between the two hooks"),
    ]
    out = '<div class="stats">'
    for label, val, cls, note in cells:
        out += (
            '<div class="stat"><div class="stat-label">%s</div><div class="stat-val %s">%s</div>'
            '<div class="stat-note">%s</div></div>' % (esc(label), cls, val, esc(note))
        )
    return out + "</div>"


def render_budget(m):
    st = m["stats"]
    window = m["context_window"] or DEFAULT_CONTEXT_WINDOW
    total = st["est_tokens_total"]
    errs = st["est_tokens_error"]
    useful = max(total - errs, 0)
    pct = (total / window) if window else 0
    over = pct > 1
    useful_pct = min(useful / window * 100, 100) if window else 0
    err_pct = min(errs / window * 100, 100 - useful_pct) if window else 0
    body = (
        '<div class="budget-header">'
        "<span>%d tool call(s) across %d case(s), payload only</span>"
        "<span><b>est. %s</b> / %s tokens (<b>%s</b> of context window)</span>"
        "</div>"
        % (st["n_calls"], st["cases_total"], fmt_tokens(total), fmt_tokens(window), fmt_pct(min(pct, 9.99)))
    )
    body += (
        '<div class="budget-track">'
        '<div class="budget-seg useful" style="width:%.1f%%"></div>'
        '<div class="budget-seg err" style="width:%.1f%%"></div>'
        "</div>" % (useful_pct, err_pct)
    )
    body += (
        '<div class="budget-legend">'
        '<span class="budget-legend-item"><span class="budget-dot" style="background:var(--bar)"></span>'
        "successful payloads (est. %s)</span>"
        '<span class="budget-legend-item"><span class="budget-dot" style="background:var(--red)"></span>'
        "error payloads (est. %s)</span>"
        '<span class="budget-legend-item"><span class="budget-dot" style="background:var(--track)"></span>'
        "window: %s tokens</span>"
        "</div>" % (fmt_tokens(useful), fmt_tokens(errs), fmt_tokens(window))
    )
    if over:
        body += (
            '<p class="note bad">These payloads together exceed the %s-token window '
            "(est.). Sub-agent containment is the only reason a single session survived them.</p>"
            % fmt_tokens(window)
        )
    return (
        '<h3 class="sub-title">Context budget <span class="hint">payload est. tokens vs a %s-token window</span></h3>'
        '<div class="budget">%s</div>' % (fmt_tokens(window), body)
    )


def render_glance(m):
    return (
        '<section class="sec">'
        + sec_head("02 &middot; the run at a glance", "Cases, headline numbers, context budget",
                   "One cell per case in plan order; click a cell to open its evidence.")
        + render_strip(m)
        + render_stats(m)
        + render_budget(m)
        + "</section>"
    )


def render_tool_table(m):
    cards = m["tool_cards"]
    out = '<section class="sec">' + sec_head(
        "03 &middot; per-tool", "Per-tool",
        "One row per tool, bars on a shared scale so the expensive one is visible without "
        "reading. Token figures est. (chars/4) · latency ~ (incl. hook overhead).",
    )
    if not cards:
        return out + '<div class="empty">No tools in plan.json and no tool calls in telemetry.</div></section>'

    max_tokens = max([as_number(c["est_tokens_median"]) or 0 for c in cards], default=0)
    max_latency = max([as_number(c["duration_median"]) or 0 for c in cards], default=0)

    head = (
        "<thead><tr>"
        "<th>Tool</th>"
        '<th class="num">Calls</th>'
        "<th>Payload economics<small>median est. tokens per call</small></th>"
        "<th>Latency<small>median, ~ wall clock</small></th>"
        "<th>Reliability<small>error rate</small></th>"
        "<th>Discoverability<small>found by the agent · L0/L1</small></th>"
        "<th>Grade<small>assertions passed</small></th>"
        "</tr></thead>"
    )
    rows = ""
    for c in cards:
        skipped = c["in_scope"] is False
        a = c["assertions"]
        graded_n = a["passed"] + a["failed"] + a["ungradable"]

        tags = []
        if skipped:
            tags.append('<span class="tag dashed">skipped &middot; %s</span>' % esc(str(c["skip_reason"] or "out of scope")))
        if c["write_capable"]:
            tags.append('<span class="tag warn">write-capable</span>')
        if not c["in_plan"]:
            tags.append('<span class="tag warn">not in plan (other server)</span>')
        tool_cell = '<td class="tool"><span class="tool-name">%s</span>%s</td>' % (
            esc(c["name"]), '<div class="tool-tags">%s</div>' % "".join(tags) if tags else "",
        )

        if c["n_calls"] == 0:
            calls_cell = '<td class="num">0<small>never called</small></td>'
            payload_cell = '<td class="bar-cell"><span class="mono">%s</span></td>' % DASH
            latency_cell = '<td class="bar-cell"><span class="mono">%s</span></td>' % DASH
            rel_cell = "<td><span class=\"st none\">%s</span></td>" % DASH
        else:
            calls_cell = '<td class="num">%d<small>in %d case(s)</small></td>' % (c["n_calls"], c["n_cases"])
            extra = "total est. %s" % fmt_tokens(c["est_tokens_total"])
            if c["bytes_median"] is not None:
                extra += " &middot; median payload %s" % fmt_bytes(c["bytes_median"])
            if c["capped"]:
                extra += ' &middot; <span class="warn">payload capture hit the 200 KB cap</span>'
            payload_cell = (
                '<td class="bar-cell"><div class="bar%s"><i style="width:%.1f%%"></i><b>est. %s</b></div><small>%s</small></td>'
                % (
                    "" if as_number(c["est_tokens_median"]) else " zero",
                    pct_of(c["est_tokens_median"], max_tokens), fmt_tokens(c["est_tokens_median"]), extra,
                )
            )
            latency_cell = (
                '<td class="bar-cell"><div class="bar%s"><i style="width:%.1f%%"></i><b>~%s</b></div>'
                "<small>slowest ~%s</small></td>"
                % (
                    "" if as_number(c["duration_median"]) else " zero",
                    pct_of(c["duration_median"], max_latency), fmt_ms(c["duration_median"]), fmt_ms(c["duration_max"]),
                )
            )
            err_rate = c["error_rate"]
            if not isinstance(err_rate, (int, float)):
                rel = '<span class="st none">%s</span>' % DASH
            elif not err_rate:
                rel = '<span class="st ok"><i>&#10003;</i>0% errors</span>'
            else:
                rel = '<span class="st %s"><i>&#10005;</i>%s errors</span>' % (
                    "bad" if err_rate >= 0.25 else "warn", fmt_pct(err_rate),
                )
            kinds = '<small>%s</small>' % esc(", ".join(c["error_kinds"])) if c["error_kinds"] else ""
            rel_cell = "<td>%s%s</td>" % (rel, kinds)

        if c["found_of"]:
            found_cls = "ok" if c["found_in"] == c["found_of"] else "bad"
            icon = "&#10003;" if found_cls == "ok" else "&#10005;"
            sub = []
            if c["calls_to_first"] is not None:
                sub.append("median %g call(s) to first correct" % c["calls_to_first"])
            if c["detours"]:
                sub.append("detours: %s" % esc(", ".join(sorted(set(c["detours"])))))
            disc_cell = '<td><span class="st %s"><i>%s</i>%d/%d case(s)</span>%s</td>' % (
                found_cls, icon, c["found_in"], c["found_of"],
                "<small>%s</small>" % " &middot; ".join(sub) if sub else "",
            )
        else:
            disc_cell = '<td><span class="st none">%s</span><small>no L0/L1 case targets it</small></td>' % DASH

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
        grade_cell = '<td class="tight">%s</td>' % grade

        rows += '<tr%s>%s%s%s%s%s%s%s</tr>' % (
            ' class="skipped"' if skipped else "",
            tool_cell, calls_cell, payload_cell, latency_cell, rel_cell, disc_cell, grade_cell,
        )
    return out + '<div class="tbl-wrap"><table class="tbl tools">%s<tbody>%s</tbody></table></div></section>' % (head, rows)


def render_trajectories(m):
    cases = [c for c in m["cases"] if c["level"] in ("L0", "L1")]
    out = '<section class="sec">' + sec_head(
        "04 &middot; discovery", "Discovery trajectory",
        "L0/L1 only. Did the agent find the right tool, and what did it touch first?",
    )
    if not cases:
        return out + '<div class="empty">No L0 or L1 cases in this plan &mdash; nothing to trace.</div></section>'
    for c in cases:
        traj = c["trajectory"]
        found = traj.get("found_tool")
        detours = [str(d) for d in dlist(traj, "detours")]
        ctf = traj.get("calls_to_first_correct")

        head = '<div class="traj-head"><span class="lvl">%s</span><span class="cid">%s</span><span class="tgt">%s</span></div>' % (
            esc(c["level"] or "?"), esc(c["id"]),
            "target: %s" % esc(c["tool"]) if c["tool"] else "no named target (server-level discovery)",
        )

        nodes = ['<li><span class="node start">task issued</span></li>']
        for call in c["calls"]:
            row = call["row"]
            cls = "err" if row.get("is_error") else ("hit" if call["on_target"] else "detour")
            nodes.append(
                '<li><span class="node %s">%s%s</span></li>'
                % (cls, esc(call["qualified"]), " &middot; error" if row.get("is_error") else "")
            )
        if len(nodes) == 1:
            for d in detours:
                nodes.append('<li><span class="node detour">%s</span></li>' % esc(d))
            if found is True and c["tool"]:
                nodes.append('<li><span class="node hit">%s</span></li>' % esc(c["tool"]))
        path = '<ol class="path">%s</ol>' % "".join(nodes)

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
        out += '<div class="traj">%s%s<p class="%s">%s</p></div>' % (head, path, note_cls, esc(" ".join(notes)))
    return out + "</section>"


STATE_CHIP = {
    "verified": '<span class="st ok"><i>&#10003;</i>verified</span>',
    "fabricated": '<span class="st bad"><i>&#10005;</i>NO &mdash; fabrication</span>',
    "unverifiable": '<span class="st warn"><i>?</i>unverifiable</span>',
}
STATE_ROW_CLASS = {"verified": "", "fabricated": "fabrication", "unverifiable": "unverifiable"}


def render_grounding(m):
    rows = m["grounding_rows"]
    fabs, unver = m["fabrications"], m["unverifiable"]
    out = '<section class="sec">' + sec_head(
        "05 &middot; grounding", "Grounding",
        "Every claim in a deliverable, checked against the captured payload of the call it cites.",
    )
    out += (
        '<div class="counts">'
        '<div class="fab-count"><span class="n %s">%d</span><span class="lbl"><b>fabrication(s)</b>'
        "claims contradicted by, or absent from, an intact payload</span></div>"
        '<div class="fab-count"><span class="n %s">%d</span><span class="lbl"><b>unverifiable</b>'
        "no intact payload to check against; not counted as fabrication</span></div>"
        "</div>"
        % ("zero" if fabs == 0 else "some", fabs, "none" if unver == 0 else "warn", unver)
    )
    if m["fabrication_reported"] != m["fabrication_listed"] and rows:
        out += (
            '<p class="note">grades_summary/grading reported %d fabrication(s); the claim '
            "rows list %d. The claim rows are authoritative per the workspace contract, so the "
            "count above comes from them.</p>"
            % (m["fabrication_reported"], m["fabrication_listed"])
        )
    if not rows:
        return out + '<div class="empty">No claims were recorded in any grading.json.</div></section>'
    body = (
        '<table class="tbl"><thead><tr><th>Case</th><th>Claim</th><th>Source tool call</th>'
        "<th>Grounded</th><th>Reason</th></tr></thead><tbody>"
    )
    for r in rows:
        if r["source_tool"]:
            src = '<span class="mono">%s</span><span class="claim-reason mono">%s</span>' % (
                esc(str(r["source_tool"])), esc(str(r["source_id"])),
            )
        elif r["source_id"]:
            src = '<span class="mono">%s</span>' % esc(str(r["source_id"]))
        else:
            src = '<span class="mono">no source cited</span>'
        row_cls = STATE_ROW_CLASS[r["state"]]
        body += (
            '<tr%s><td class="case">%s</td><td>%s</td><td>%s</td><td class="tight">%s</td><td>%s</td></tr>'
            % (
                ' class="%s"' % row_cls if row_cls else "", esc(r["case"]), esc(r["claim"]), src,
                STATE_CHIP[r["state"]], esc(r["reason"]) if r["reason"] else DASH,
            )
        )
    return out + '<div class="tbl-wrap">%s</tbody></table></div></section>' % body


def render_caveats(m):
    out = '<section class="sec">' + sec_head("06 &middot; caveats", "Caveats", "What this report does not claim.")
    body = "<div><h4>true of every mcp-eval report</h4><ul>%s</ul></div>" % "".join(
        '<li class="standing">%s</li>' % esc(c) for c in STANDING_CAVEATS
    )
    if m["caveats"]:
        body += "<div><h4>from this run</h4><ul>%s</ul></div>" % "".join(
            "<li>%s</li>" % esc(c) for c in m["caveats"]
        )
    else:
        body += '<div><h4>from this run</h4><div class="empty">No run-specific caveats were recorded.</div></div>'
    return out + '<div class="caveats">%s</div></section>' % body


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
    out = '<section class="sec">' + sec_head(
        "07 &middot; evidence", "Case detail", "Click a case to expand its task, deliverable, grading and telemetry.",
        '<span class="controls"><button data-all="open">expand all</button>'
        '<button data-all="close">collapse all</button></span>',
    )
    if not m["cases"]:
        return out + '<div class="empty">No cases found in plan.json or on disk.</div></section>'

    for c in m["cases"]:
        cls, label = OUTCOME_BADGE.get(c["outcome"], ("badge-neutral", c["outcome"]))
        tokens = sum(
            r["row"].get("est_tokens") or 0 for r in c["calls"]
            if isinstance(r["row"].get("est_tokens"), (int, float))
        )
        summary_line = (
            '<summary><span class="badge %s">%s</span>'
            '<span class="lvl">%s</span>'
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
            '<div class="case-block"><div class="run-line">status <b>%s</b> &middot; ran on <b>%s</b></div></div>'
            % (esc(str(c["status"])), esc(str(c["model"] or "unrecorded")))
        )
        if c["task"]:
            body += '<div class="case-block"><h4>Task given to the sub-agent</h4><blockquote class="quote">%s</blockquote></div>' % esc(c["task"])
        if c["deliverable"]:
            body += '<div class="case-block"><h4>Deliverable</h4><blockquote class="quote">%s</blockquote></div>' % esc(c["deliverable"])
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
                method = '<span class="assert-method">%s</span>' % esc(a["method"]) if a["method"] else ""
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
                    '<tr%s><td class="num">%d</td><td class="mono">%s</td>'
                    '<td class="mono">%s</td><td class="num">~%s</td><td class="num">%s</td>'
                    '<td class="num">est. %s</td><td class="tight">%s</td></tr>'
                    % (
                        ' class="err"' if err else "", i, esc(call["qualified"]),
                        esc(short_json(r.get("args"))), fmt_ms(r.get("duration_ms")),
                        fmt_bytes(r.get("payload_bytes")), fmt_tokens(r.get("est_tokens")),
                        '<span class="st bad"><i>&#10005;</i>%s</span>' % esc(str(r.get("error_kind") or "error"))
                        if err else '<span class="st none">none</span>',
                    )
                )
                rows += (
                    '<tr class="excerpt-row"><td></td><td colspan="6">%s</td></tr>'
                    % render_payload(call)
                )
            body += (
                '<div class="case-block"><h4>Tool calls (telemetry)</h4><div class="tbl-wrap">'
                '<table class="tbl calls"><thead><tr><th class="num">#</th><th>Tool</th><th>Args</th>'
                '<th class="num">~Latency</th><th class="num">Payload</th><th class="num">Tokens (est.)</th><th>Error</th></tr></thead>'
                "<tbody>%s</tbody></table></div></div>" % rows
            )
        else:
            body += '<div class="case-block"><h4>Tool calls (telemetry)</h4><div class="empty">No tool calls recorded for this case.</div></div>'

        out += '<div class="case-anchor" id="case-%s"><details class="case">%s%s</div></details></div>' % (
            esc(c["id"]), summary_line, body,
        )
    return out + "</section>"


def render_html(m):
    blob = json.dumps(m["raw"], ensure_ascii=False, default=str).replace("<", "\\u003c")
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>%s &middot; mcp-eval report</title>" % esc(m["server"]),
        "<style>%s%s</style></head><body>" % (font_faces(), CSS),
        '<div class="desk"><main class="sheet">',
        render_masthead(m),
        render_gaps(m),
        render_verdict(m),
        render_glance(m),
        render_tool_table(m),
        render_trajectories(m),
        render_grounding(m),
        render_caveats(m),
        render_cases(m),
        '<footer class="foot"><span>mcp-eval &middot; workspace: %s</span><span>generated %s</span></footer>'
        % (esc(m["workspace"]), esc(m["raw"]["generated"])),
        "</main></div>",
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
