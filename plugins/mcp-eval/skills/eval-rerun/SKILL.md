---
name: eval-rerun
description: Re-runs one case from an existing mcp-eval test plan with a fresh sub-agent, then compares the two runs. Use only when an eval has already been run against an MCP server and the user wants a single case repeated — checking whether a result is stable or flaky, asking whether the eval is deterministic, or verifying that a fix to a tool description or schema actually worked. Not for starting a new evaluation and not for re-rendering the dashboard.
argument-hint: "<case-id>"
---

# Re-run one eval case

`$ARGUMENTS` — the case id from `eval-workspace/plan.json`.

Re-running a single case answers two questions that a full eval cannot. **Is this result
stable?** An MCP integration that passes once and fails once is not a passing
integration, and the only way to see that is to run the same brief twice. **Did the fix
work?** After the user changes a tool description or a schema, one case re-run is the
cheap confirmation — a full eval is not.

Always operates on `eval-workspace/` in the session cwd. There is no workspace argument
on purpose: the hooks resolve that fixed path when deciding whether to record telemetry,
so a rerun pointed at an archived workspace would write its marker somewhere the hooks
never look, capture nothing, and hand back an ungradable case that looks like a server
failure. To re-run against an archived workspace, restore it to `eval-workspace/` first.

## Steps

1. Load `eval-workspace/plan.json` and find the case by id. Not found → list the
   available ids and stop.
2. Read the existing `cases/<id>/result.json`, `cases/<id>/grading.json`, and that
   case's `telemetry.jsonl` lines **before** anything is overwritten. They are the
   comparison baseline and the two JSON files are about to be gone. (Telemetry appends
   and payload files are keyed by `tool_use_id`, so both runs' raw evidence survives.)
3. If the case's tool is write-capable, get fresh approval naming that tool. A rerun is a
   new live call — the earlier approval covered the earlier call, not this one.
4. Build the brief exactly as before: same task text, same level, template and level
   line from `${CLAUDE_PLUGIN_ROOT}/references/test-plan-guide.md`. Changing the brief
   turns a determinism check into a different experiment.
5. Write `eval-workspace/.eval-active` with the case id and current timestamp, spawn the
   sub-agent with `model: <plan.interview.operator_model>`, then delete the marker —
   including on failure. A stale marker bills later calls to this case.
6. Overwrite `cases/<id>/result.json`, re-grade the case against the new telemetry and
   payload files following `${CLAUDE_PLUGIN_ROOT}/references/grading-guide.md`, and
   overwrite `cases/<id>/grading.json`.
7. Re-aggregate `grades_summary.json` so the dashboard doesn't show a stale total, and
   fold the determinism observation into its `reasoning`.

## Reporting the comparison

Telemetry appends, so both runs remain in `telemetry.jsonl`; distinguish them by
timestamp. Compare and report in the session:

| Dimension | What a difference means |
|---|---|
| Same tool found? | Discovery is non-deterministic — the most serious instability, and invisible in a single run |
| Call count / detours | The path varies even when the destination doesn't |
| Payload size | The server's response varies for the same input |
| Latency | Load-dependent; only interesting at large deltas |
| Assertions that flipped | Name each one — a flipped assertion is the finding |

Identical results across a rerun are worth stating explicitly. "Stable across two runs"
is a claim the single-run dashboard cannot make.

Re-render the dashboard with `/eval-report` when the user wants the HTML updated.
