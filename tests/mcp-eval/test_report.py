#!/usr/bin/env python3
"""
Tests for scripts/report.py.

Run:  python3 tests/mcp-eval/test_report.py
  or: python3 -m unittest discover -s tests/mcp-eval -v
"""

import html
import html.parser
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[1] / "plugins" / "mcp-eval"
REPORT_PY = PLUGIN / "scripts" / "report.py"
FULL_WS = HERE / "fixtures" / "full-workspace"
PARTIAL_WS = HERE / "fixtures" / "partial-workspace"

_spec = importlib.util.spec_from_file_location("mcp_eval_report", REPORT_PY)
report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(report)

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class TagBalanceParser(html.parser.HTMLParser):
    """Collects any element left open or closed out of order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("</%s> with nothing open" % tag)
        elif self.stack[-1] != tag:
            self.errors.append("</%s> closes <%s>" % (tag, self.stack[-1]))
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def close(self):
        super().close()
        if self.stack:
            self.errors.append("never closed: %s" % ", ".join(self.stack))


def run_report(workspace, *extra):
    """Run the CLI; return (returncode, stdout, stderr, html_text_or_None)."""
    tmpdir = tempfile.mkdtemp()
    out = Path(tmpdir) / "eval-report.html"
    proc = subprocess.run(
        [sys.executable, str(REPORT_PY), str(workspace), "--output", str(out), *extra],
        capture_output=True, text=True,
    )
    text = out.read_text(encoding="utf-8") if out.exists() else None
    return proc.returncode, proc.stdout, proc.stderr, text


class ReportTestCase(unittest.TestCase):
    """Substring assertions that report the needle, not the whole 60 KB page."""

    def has(self, text, *needles):
        for needle in needles:
            self.assertTrue(needle in text, "missing from report: %r" % needle)

    def lacks(self, text, *needles):
        for needle in needles:
            self.assertFalse(needle in text, "unexpectedly present: %r" % needle)

    def well_formed(self, text):
        parser = TagBalanceParser()
        parser.feed(text)
        parser.close()
        self.assertEqual(parser.errors, [], "malformed HTML")


class FullWorkspaceTests(ReportTestCase):
    """A complete workspace: an L0 case with a detour, a failed sub-agent,
    an ungradable assertion and a fabrication."""

    @classmethod
    def setUpClass(cls):
        cls.code, cls.stdout, cls.stderr, cls.html = run_report(FULL_WS)
        assert cls.html is not None, "report was not written: %s" % cls.stderr

    def test_generates_successfully(self):
        self.assertEqual(self.code, 0, self.stderr)
        self.assertGreater(len(self.html), 5000)
        self.assertTrue(self.html.startswith("<!DOCTYPE html>"))

    def test_html_is_well_formed(self):
        self.well_formed(self.html)

    def test_self_contained(self):
        self.lacks(self.html, "http://", "https://", "cdn.", "<link ", "<img ")

    def test_no_double_escaped_entities(self):
        self.lacks(self.html, "&amp;middot;", "&amp;mdash;", "&amp;rarr;")

    def test_verdict_is_first_and_verbatim(self):
        self.has(
            self.html,
            "Ship with caveats",
            "Sonnet finds all three read tools and recovers from a bad argument name",
        )
        self.assertLess(self.html.index("verdict-word"), self.html.index('class="stats"'),
                        "verdict must precede the stat row")
        self.assertLess(self.html.index('class="stats"'), self.html.index("Per-tool"),
                        "stat row must precede the tool cards")

    def test_stat_row(self):
        self.has(self.html, "cases run", "case pass rate", "5 / 5", "40%", "median latency")

    def test_token_figures_are_labelled_estimates(self):
        self.has(
            self.html,
            "total tokens (est., chars/4)",
            "Tokens (est.)",                 # telemetry table header
            "est. 88.3k",                    # 534 + 11975 + 11975 + 45 + 2321 + 61428
            "est. 12.0k",                    # per-tool median
        )
        self.lacks(self.html, "total tokens (measured")

    def test_latency_figures_are_labelled_approximate(self):
        self.has(self.html, "median latency (~, incl. hook overhead)", "~Latency", "~1.5s", "~1.1s")

    def test_context_budget_bar(self):
        self.has(self.html, "Context budget", "200.0k", "budget-track", "of context window",
                 "successful payloads", "error payloads")

    def test_context_window_override(self):
        _, _, _, text = run_report(FULL_WS, "--context-window", "20000")
        self.has(text, "20.0k", "Sub-agent containment")   # 26.9k est. exceeds a 20k window

    def test_per_tool_cards(self):
        self.has(self.html, "search_contacts", "list_deals", "fetch_attachment", "create_entry",
                 "Payload economics", "Latency", "Reliability", "Discoverability",
                 "error rate", "write-capable, not approved", "mcp_error")

    def test_tool_never_called_says_so(self):
        self.has(self.html, "never called")   # create_entry was skipped

    def test_trajectory_renders_detour_tool_names(self):
        self.has(
            self.html,
            "Discovery trajectory",
            "mcp__notes__search_notes",
            "Detoured into: mcp__notes__search_notes.",
            "Found the target tool.",
            "2 call(s) before the first correct one.",
            "1 call(s) returned an error.",
        )

    def test_trajectory_covers_l0_and_l1_only(self):
        traj = self.html[self.html.index("Discovery trajectory"):self.html.index("Grounding")]
        self.has(traj, "l0-blind-research", "l1-search-contacts", "l1-list-deals",
                 "l1-fetch-attachment")
        self.lacks(traj, "l3-list-deals-spec")

    def test_grounding_table_flags_the_fabrication(self):
        self.has(
            self.html,
            "Dana Whitfield signs off on capital purchases",
            '<tr class="fabrication">',
            "fabrication(s)",
            '<span class="n some">1</span>',   # prominent count
            "NO &mdash; fabrication",
            "no field in payloads/toolu_b1.txt carries sign-off authority",   # reason visible
        )

    def test_unverifiable_claim_is_amber_and_not_a_fabrication(self):
        self.has(
            self.html,
            '<tr class="unverifiable">',
            "The report recommends a re-inspection in 24 months",
            '<span class="n warn">1</span>',                    # unverifiable count
            "not counted as fabrication",
            "truncated at the 200 KB cap",                      # the reason, visible
            "unverifiable claims <b>1</b>",                     # surfaced next to the verdict
        )
        # the fabrication headline stays at 1: the null claim is not counted
        self.lacks(self.html, '<span class="n some">2</span>')

    def test_legacy_boolean_false_without_reason_is_still_a_fabrication(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(FULL_WS, ws)
            gpath = ws / "cases" / "l1-search-contacts" / "grading.json"
            grading = json.loads(gpath.read_text())
            grading["grounding"]["claims"][2] = {
                "claim": "Dana Whitfield signs off on capital purchases",
                "source": None, "grounded": False,
            }
            gpath.write_text(json.dumps(grading))
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, '<tr class="fabrication">', "NO &mdash; fabrication",
                     "no reason recorded", '<span class="n some">1</span>')

    def test_claim_rows_beat_a_disagreeing_reported_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(FULL_WS, ws)
            gpath = ws / "cases" / "l1-search-contacts" / "grading.json"
            grading = json.loads(gpath.read_text())
            grading["grounding"]["fabrications"] = 3      # disagrees with the one false row
            gpath.write_text(json.dumps(grading))
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, '<span class="n some">1</span>',
                     "reported 3 fabrication(s); the claim rows list 1",
                     "claim rows are authoritative")

    def test_grounded_claims_carry_their_source_call(self):
        self.has(self.html, "toolu_b1", "mcp__acme-crm__search_contacts")

    def test_ungradable_assertion_is_not_a_failure(self):
        self.has(self.html, "UNGRADABLE", "the payload carries no currency field")

    def test_failed_subagent_case_renders(self):
        self.has(self.html, "l3-list-deals-spec", "sub-agent failed",
                 "The sub-agent failed; no deliverable was returned.")

    def test_case_detail_is_expandable_and_complete(self):
        self.has(
            self.html,
            '<details class="case">',
            "Deliverable",
            "Contoso Fabrication has 3 open deals worth 1,240,000",    # deliverable verbatim
            "Assertions",
            "Tool calls (telemetry)",
            "Friction the sub-agent reported",
            "Task given to the sub-agent",
        )

    def test_caveats_render_verbatim_plus_standing_labels(self):
        for caveat in json.loads((FULL_WS / "grades_summary.json").read_text())["caveats"]:
            self.has(self.html, html.escape(caveat))
        for standing in report.STANDING_CAVEATS:
            self.has(self.html, html.escape(standing))

    def test_model_under_test_is_stated(self):
        self.has(self.html, "operator model: sonnet", "ran on")

    def test_unanswered_interview_fields_are_badged_as_assumed(self):
        self.has(
            self.html,
            "Run parameters",
            "Non-technical consultants who describe what they want in plain language.",
            '<div class="param assumed">',                       # the audience row
            '<span class="chip">assumed</span>',
            "1 assumed, not answered by the user",
            '<span class="chip">1 interview answer(s) assumed</span>',
        )
        # the assumed chip sits inside the verdict card, above the stat row
        self.assertLess(self.html.index("Run parameters"), self.html.index('class="stats"'))

    def test_answered_interview_fields_are_not_badged(self):
        params = self.html[self.html.index("Run parameters"):self.html.index('class="stats"')]
        use_case = params[params.index("Use case"):params.index("Audience")]
        self.assertNotIn("chip", use_case, "an answered field must not be badged assumed")

    def test_payload_excerpt_and_capture_path_per_call(self):
        self.has(
            self.html,
            '<pre class="box excerpt">',
            "EQUIPMENT INSPECTION REPORT",                                # excerpt text
            "full payload:",
            "payloads/toolu_d1.txt",
            "truncated at the 200 KB cap",
        )
        # full payload files are never inlined, only pointed at
        self.lacks(self.html, "point 059")

    def test_capped_payload_shows_on_the_tool_card(self):
        self.has(self.html, "payload capture", "hit the 200 KB cap")

    def test_data_blob_is_inlined_and_parses(self):
        match = re.search(
            r'<script type="application/json" id="eval-data">(.*?)</script>', self.html, re.S
        )
        self.assertIsNotNone(match, "inline data blob missing")
        blob = json.loads(match.group(1))
        self.assertEqual(blob["plan"]["server"], "acme-crm")
        self.assertEqual(len(blob["telemetry"]), 6)
        self.assertEqual(blob["context_window"], 200000)

    def test_stdout_summarises_the_run(self):
        self.has(self.stdout, "verdict: ship-with-caveats", "est. 88.3k tokens")


class PartialWorkspaceTests(ReportTestCase):
    """Degrade section by section; never crash."""

    def test_missing_grading_telemetry_and_summary(self):
        code, _, stderr, text = run_report(PARTIAL_WS)
        self.assertEqual(code, 0, stderr)
        self.assertIsNotNone(text)
        self.has(
            text,
            "No verdict recorded",
            "ungraded",
            "grades_summary.json is missing",
            "telemetry.jsonl is missing",
            "No tool calls recorded for this case.",
            "No claims were recorded",
            "Assertions (planned, not graded)",
            "No run-specific caveats were recorded.",
        )
        self.well_formed(text)

    def test_empty_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, stderr, text = run_report(tmp)
            self.assertEqual(code, 0, stderr)
            self.has(text, "No verdict recorded", "No cases found", "plan.json is missing")
            self.well_formed(text)

    def test_malformed_files_do_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(FULL_WS, ws)
            (ws / "plan.json").write_text("{ not json at all")
            (ws / "telemetry.jsonl").write_text(
                '{"case_id": "l1-search-contacts", "tool_name": "x", "est_tokens": 10}\n'
                "garbage line\n"
            )
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, "plan.json could not be read", "1 malformed line(s) skipped",
                     "l0-blind-research")   # cases survive from disk with no plan
            self.well_formed(text)

    def test_missing_payloads_directory_does_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(FULL_WS, ws)
            shutil.rmtree(ws / "payloads")
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, "excerpt only &mdash; no payload file captured", "EQUIPMENT INSPECTION REPORT")
            # the grading reason still names the file; only the capture pointer goes away
            self.lacks(text, '<span class="path">payloads/toolu_d1.txt</span>')
            self.well_formed(text)

    def test_telemetry_without_excerpt_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(FULL_WS, ws)
            shutil.rmtree(ws / "payloads")
            lines = [
                json.dumps({k: v for k, v in json.loads(line).items() if k != "payload_excerpt"})
                for line in (ws / "telemetry.jsonl").read_text().splitlines() if line.strip()
            ]
            (ws / "telemetry.jsonl").write_text("\n".join(lines) + "\n")
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, "no payload captured for this call")

    def test_interview_without_unanswered_badges_nothing(self):
        code, _, stderr, text = run_report(PARTIAL_WS)
        self.assertEqual(code, 0, stderr)
        self.has(text, "Run parameters", "Sales consultants pulling contact context")
        self.lacks(text, '<span class="chip">assumed</span>', "interview answer(s) assumed")

    def test_case_dir_absent_from_plan_is_still_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            shutil.copytree(PARTIAL_WS, ws)
            extra = ws / "cases" / "l2-operator-extra"
            extra.mkdir(parents=True)
            (extra / "result.json").write_text(json.dumps(
                {"case_id": "l2-operator-extra", "status": "completed", "deliverable": "orphan case"}
            ))
            code, _, stderr, text = run_report(ws)
            self.assertEqual(code, 0, stderr)
            self.has(text, "l2-operator-extra", "not in plan.json")

    def test_missing_workspace_directory_exits_nonzero(self):
        proc = subprocess.run(
            [sys.executable, str(REPORT_PY), "/nonexistent/eval-workspace"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not a directory", proc.stderr)

    def test_default_output_lands_in_the_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "eval-workspace"
            shutil.copytree(FULL_WS, ws)
            proc = subprocess.run([sys.executable, str(REPORT_PY), str(ws)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((ws / "eval-report.html").exists())


class UnitTests(unittest.TestCase):
    """The judgement calls that must not drift."""

    def test_qualified_tool_names_match_plan_names(self):
        self.assertTrue(report.tool_matches("mcp__acme-crm__search_contacts", "search_contacts"))
        self.assertTrue(report.tool_matches("search_contacts", "search_contacts"))
        self.assertFalse(report.tool_matches("mcp__notes__search_notes", "search_contacts"))
        self.assertFalse(report.tool_matches("mcp__crm__contacts_search", "search"))

    def test_nothing_defaults_to_failure(self):
        self.assertEqual(report.case_outcome("completed", [{"passed": None}], True), "partial")
        self.assertEqual(report.case_outcome("completed", [], False), "ungraded")
        self.assertEqual(report.case_outcome("subagent_failed", [], False), "failed-to-run")
        self.assertEqual(report.case_outcome("completed", [{"passed": True}], True), "pass")
        self.assertEqual(
            report.case_outcome("completed", [{"passed": True}, {"passed": False}], True), "fail"
        )

    def test_latency_rounds_half_up(self):
        self.assertEqual(report.fmt_ms(1450), "1.5s")
        self.assertEqual(report.fmt_ms(310), "310ms")
        self.assertEqual(report.fmt_ms(None), report.DASH)

    def test_formatters_survive_junk_telemetry_values(self):
        for junk in (None, "n/a", {}, [], True):
            self.assertEqual(report.fmt_ms(junk), report.DASH)
            self.assertEqual(report.fmt_tokens(junk), report.DASH)
            self.assertEqual(report.fmt_bytes(junk), report.DASH)


if __name__ == "__main__":
    unittest.main(verbosity=2)
