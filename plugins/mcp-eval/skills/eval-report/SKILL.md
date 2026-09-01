---
name: eval-report
description: Re-renders the mcp-eval HTML dashboard from artifacts already on disk in an eval workspace, running no tests and grading nothing. Use only when an eval workspace already exists and the user wants the report rebuilt, reopened, or regenerated — after hand-editing a verdict, after re-running a case, or to look again at a report from an earlier session. Not for running an evaluation and not for repeating a test case.
argument-hint: "[workspace-path]"
---

# Re-render the eval dashboard

`$ARGUMENTS` — workspace path, default `eval-workspace`.

Re-render only. This spends no tokens on the target server and makes no judgments: it
turns artifacts already on disk into the dashboard. Use it after editing a verdict, after
a case re-run, or to reopen a report from an earlier session.

## Steps

1. Check the workspace exists and holds `plan.json` and `grades_summary.json`.
2. Render and open:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/report.py <workspace>
   open <workspace>/eval-report.html    # xdg-open on Linux
   ```

3. Tell the user the verdict and the path.

## When artifacts are missing

Say what is missing and what produces it. Do not fill the gap.

| Missing | What it means |
|---|---|
| `plan.json` | No eval has run here — start with `/eval` |
| `grades_summary.json` | Cases ran but grading never finished — grade the existing `cases/`, `telemetry.jsonl`, and `payloads/` per `${CLAUDE_PLUGIN_ROOT}/references/grading-guide.md`, then render |
| Some `cases/<id>/grading.json` | Those cases are ungraded. Grade them or render without them — the dashboard will show them as ungraded, which is the truth |
| `telemetry.jsonl` empty or absent | The hooks never fired. Grading built on that is trajectory-blind; the report should say so rather than imply the calls were clean |
| `payloads/` empty while telemetry has lines | Trajectory is measurable, grounding is not. Grounding claims stay ungradable rather than being taken on the sub-agent's word |

Rendering a partial workspace is fine. Inventing the missing part to make the dashboard
look complete is not — an eval that quietly reports grades it never computed is worse
than one that reports a gap.
