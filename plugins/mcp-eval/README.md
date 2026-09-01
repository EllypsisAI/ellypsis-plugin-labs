# mcp-eval

Evaluate an MCP server **in the hands of an LLM**.

A deterministic client can verify your server works. It cannot tell you whether Claude
*finds* your tool, *selects* it over its neighbors, *calls* it with sane arguments,
*survives* the payload, and *grounds* its answer in what came back. That joint system —
your server paired with the model — is what actually ships to users. It is the only
thing this plugin measures.

## How it works

One entry point: `/eval`. It runs a six-stage arc inside your live Claude Code session:

1. **Preflight** — picks the connected server, probes that sub-agents can reach it,
   warns about token cost and context headroom, and classifies tools: write-capable
   tools are **skipped by default** (this runs against live systems).
2. **Interview** — three questions, always asked: what is the server for, who will be
   driving the LLM, and real inputs from your world (including one that should return
   nothing — empty results are where servers induce downstream fabrication).
3. **Test plan** — cases per tool at graded information-asymmetry levels, shown for
   your approval before anything runs.
4. **Run** — sub-agents execute each case as a *task*, not a tool instruction. They
   run on Sonnet by default (an integration worth shipping should be operable by
   Sonnet) and are never told they're in an eval. Plugin hooks capture every MCP call:
   timing, arguments, payload sizes, payload contents.
5. **Grade** — every assertion scored against captured evidence. Grounding is verified
   against the actual payloads on disk, not the sub-agent's word. Verdicts are
   trinary: nothing ever defaults to FAIL.
6. **Report** — a self-contained HTML dashboard, verdict first.

### The asymmetry ladder

Sub-agents receive only what a real user would say:

| Level | Sub-agent knows | Simulates |
|-------|-----------------|-----------|
| L0 | The task only — server never named | Cold discovery |
| L1 | Task + server name, vague human phrasing | An end user (default) |
| L2 | Task + tool name | A power user |
| L3 | Task + exact arguments | Ceiling control |

When L1 fails, an L3 control separates "tool is broken" from "tool is undiscoverable" —
opposite verdicts for a server author.

## What it measures

| Family | Examples | Label |
|--------|----------|-------|
| Discoverability & selection | Found the right tool? Detours, calls-to-first-correct | measured |
| Argument fidelity | Schema-valid, semantically sane, retries needed | measured / graded |
| Payload economics | Bytes, estimated tokens, field inventory, context impact | **estimated** (chars/4) |
| Latency | Wall clock per call from hook timestamps | **approximate** (~ms hook overhead) |
| Reliability | Error rates, timeouts, determinism across reruns | measured |
| Grounding | Claims traced to captured payloads; fabrications flagged | graded, payload-verified |

What it does **not** claim, because it isn't honestly capturable in-session: exact
per-call token cost, isolated schema overhead, per-tool memory/CPU, concurrency
behavior. The dashboard says so in its own caveats block.

## Install

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install mcp-eval@ellypsis-labs
```

Requires Claude Code with your target MCP server connected, and `python3` (stdlib only).

## Invocations

Three skills, each usable as a slash command or triggered by asking in plain language:

| Invocation | Does |
|------------|------|
| `/eval [server-name]` | The full arc |
| `/eval-rerun <case-id>` | Repeat one case — determinism checks. Always runs against `eval-workspace/`; restore an archived workspace there first |
| `/eval-report [workspace-path]` | Re-render the dashboard from an existing workspace |

## Notes

- Everything lands in `eval-workspace/` in your working directory — plans, per-call
  telemetry, captured payloads, grades, report. Re-runs archive rather than overwrite.
- The eval is token-heavy by design (it spawns real sub-agents). `/eval` warns you
  up front and estimates the cost band before starting.
- Nothing is sent anywhere. The HTML report is the artifact.

MIT © Ellypsis
