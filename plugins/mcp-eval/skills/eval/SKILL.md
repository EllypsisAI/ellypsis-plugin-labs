---
name: eval
description: Evaluates whether an MCP server is production-ready with the LLM that will actually drive it — tool discoverability, argument fidelity, payload economics, reliability, and grounding — then writes an HTML dashboard with a ship / don't-ship verdict. Use this whenever the user wants to evaluate, test, benchmark, audit, vet, or review an MCP server or its tools; asks whether an MCP is good, production-ready, or worth shipping; wonders why Claude isn't finding or using a connected server's tools; asks what a server's responses cost in tokens or context; or is comparing two MCP servers. Use it even when the request sounds casual ("can you take a quick look at this MCP", "does this server actually work with Claude") — the shortcut version of this work produces a confident score of nothing.
argument-hint: "[server-name]"
---

# Evaluate an MCP server

`$ARGUMENTS` — the MCP server to evaluate. Optional; detect and ask when absent.

## What this measures

A deterministic client can prove a server responds. It cannot tell you whether an LLM
**finds** the tool, **picks** it over its neighbours, **calls** it with sane arguments,
**survives** the payload, and **grounds** its answer in what came back. That joint
system — server plus LLM — is what actually ships, and it is the only thing scored here.

Which is why every measured tool call happens inside a sub-agent and never in this
session. Two reasons, both structural rather than stylistic. A 50k-token result that
lands in a sub-agent dies there; the same result here would eat the context that
grading needs. And discovery cannot be measured from a context that already knows the
answer — once you have read the schemas, you can no longer tell whether they were
findable.

## Invariants

| Rule | Why |
|------|-----|
| Never call the target's tools yourself | You are the instrument, not the subject |
| Stages are gates, in order, none skipped | Each one's output is the next one's input; skipping produces a confident eval of nothing |
| Cases run one at a time | Telemetry is attributed by a single marker file — two live cases corrupt every metric silently |
| Write-capable tools are skipped unless individually approved by name | These calls hit live business systems |
| Nothing defaults to false | Ungradable is a real outcome with a reason; a fabricated FAIL is worse than a gap |

### What survives a request to go faster

Users ask for the quick version. These three are what make the result mean anything, so
they hold even then — say what you're skipping instead of skipping it silently.

**The interview is a gate.** Three questions, asked every time: what the server is for,
who will be driving the LLM, and real inputs from the user's world. Schemas and READMEs
describe what a server *can* do; they say nothing about what it is for or in whose words
it will be asked. An eval built on inferred answers scores your imagination.

**Write-capable tools are skipped by default.** They run only on approval that names the
tool. "Looks good" and "ok" are not that approval — these calls land in live business
systems, and a corrupted record outlives the eval.

**Nothing defaults to false.** An assertion that can't be judged is reported ungradable
with its reason. A fabricated FAIL in a dashboard is worse than a stated gap.

Read `${CLAUDE_PLUGIN_ROOT}/references/workspace-contract.md` before writing any
artifact. It is the shared shape between hooks, this skill, and the report generator;
inventing a field breaks the dashboard.

---

## Stage 1 — Preflight

**Workspace.** The hooks resolve a fixed path, so the workspace is always
`eval-workspace/` in the session cwd — not a custom location. If one already exists with
a `plan.json`, stop and ask: archive it to `eval-workspace-<YYYYMMDD-HHMM>/` and start
fresh, or leave it alone and use `/eval-report`. Never overwrite a previous run's
evidence. Once decided, create `eval-workspace/` and `eval-workspace/cases/` — the hooks
create their own directories (`.pending/`, `payloads/`).

**Target.** List connected MCP servers. If `$ARGUMENTS` names one, use it. If several are
connected and no argument was given, ask which — do not guess from the conversation.

**Access probe.** Spawn one throwaway sub-agent (`model: sonnet`) whose only job is to
report whether it can see and call the target's tools:

> List the tools available to you from the `<server>` MCP server. Then call the one
> that looks most obviously read-only (a list, search, or get) with minimal arguments.
> Report back: the tool names you could see, whether the call succeeded, and the exact
> error text if it did not. If you cannot see any tools from that server, say so
> explicitly — including whether tools appear to be available but not yet loaded.

Do not write a marker for the probe; it is not a case and its calls must not land in
telemetry. If the probe fails, stop the eval and give the user the specific fix:

| Probe symptom | Fix to hand the user |
|---|---|
| No tools from that server visible at all | Server isn't connected in this session — check `/mcp`, reconnect, then re-run `/eval` |
| Tools visible, call returns auth error | Re-authenticate the server; OAuth tokens expire silently |
| Tools visible only after the sub-agent searched for them | Not a failure — deferred tool loading is active. Note it in the plan; the search query the agent used becomes part of the discoverability measurement |
| Call returns a transport/timeout error | The server itself is down or unreachable; nothing here can be measured until it responds |

No eval spend happens before this passes.

**Cost warning and headroom.** This is token-heavy work. A sub-agent case typically
spends 15k–60k tokens depending on how large the payloads are, and grading each case
costs this session another 5k–15k. State the band for the plan you are about to
propose — a default six-case plan lands around 120k–450k tokens — and say plainly that a
server returning 50k-token results sits at or above the top of that range. If less than
roughly 40% of this session's context window remains, recommend starting `/eval` in a
fresh session: grading has to hold telemetry and results for every case at once, and a
run that dies at Stage 5 has spent the money without producing a verdict.

**Tool classification.** Read every tool's name, description, and input schema and sort
them into read-only and write-capable. Verbs give it away (`create`, `update`, `delete`,
`send`, `post`, `archive`, `move`, `merge`, `pay`), as do schemas that take a body or a
record to mutate. When a tool is ambiguous, classify it write-capable — the cost of
wrongly skipping a read tool is a thinner eval; the cost of wrongly calling a write tool
is a corrupted production record.

Show the classification as a table and mark write-capable tools skipped. They run only
when the user names them: "run `create_entry`", "test `create_entry` and `update_deal`,
that account is a sandbox". "Looks good", "ok", "yes", and "go ahead" are not approval
to call a write tool, no matter what they follow. When the user does approve a set, echo
the exact tool list back and get one confirmation before anything runs.

---

## Stage 2 — Interview

Three questions. Ask them every time, in one message, verbatim, and wait for the
answers before doing anything else.

```
Three questions before I build the test plan.

1. What is this server for? Describe the job it does in your product or workflow.

2. Who will be driving the LLM that uses it — what do they know, and how do they
   phrase things? ("sales consultants who don't know the CRM's field names" tells
   me more than "internal users".)

3. Give me real inputs from your world: actual IDs, company names, queries, or
   record names you expect to work. And one that should return nothing.
```

Do not answer these from the server's README, its schemas, or a repo you can see. Those
describe what the server *can* do; the eval needs to know what it is *for*, who is
asking, and in whose words. An eval built on inferred answers measures your imagination
and reports the score as if it were the user's.

The third answer is the one that decides whether this is an eval or a smoke test.
Without real inputs, every case degrades into "does the tool return 200". If the answer
is vague, ask again for specifics — once, plainly. If the user genuinely declines, put
that field's name in `plan.interview.unanswered` and its value becomes your stated
assumption, so the dashboard badges it and no guess passes as a requirement.

**Model is not a question.** Sub-agents run on Sonnet. An MCP integration worth shipping
should be operable by Sonnet, so Sonnet is the honest test condition — and it is the
cheap one. Set `operator_model` to something else only if the user has explicitly said
their production path runs on Opus or Fable.

---

## Stage 3 — Test plan

Read `${CLAUDE_PLUGIN_ROOT}/references/test-plan-guide.md` now. It carries the case
recipe, the asymmetry ladder, how to phrase a task at each level, how to write
assertions that can actually be graded, and the sub-agent brief template you will need
in Stage 4.

Default plan: one L1 case per in-scope tool, plus one L0 server-level case. L3 enters
later as a control, not up front — it is only interesting once an L1 case has failed.

Present the plan as a table (case id, level, tool, the task in one line, what is
asserted), then require explicit approval before any case runs. A clear yes approves the
read-only plan. Write-capable cases carry their own per-tool approval from Stage 1 and
never inherit this one.

On approval, write `plan.json` exactly as the contract specifies, including every tool
you classified — in-scope and skipped, with the skip reason. The dashboard reports what
was *not* tested, and that is half the honesty of the thing.

---

## Stage 4 — Run

Sequentially, for each case in `plan.json`:

1. Write `eval-workspace/.eval-active` — `{"case_id": "<id>", "started": "<ISO8601 Z>"}`.
2. Spawn the sub-agent with `model: <plan.interview.operator_model>` (Sonnet by default)
   and a brief built per the guide's template for that case's level.
3. Parse its four-section return into `cases/<id>/result.json` per the contract.
4. Delete `.eval-active`.

The marker is the whole attribution mechanism: hooks exit instantly when it is absent
and stamp the case id on every call when it is present. So delete it even when a case
blows up — a stale marker silently bills the next case's calls to the last one, and
nothing downstream can detect that. If a sub-agent returns prose instead of the four
sections, ask it once for the structured form; if it still doesn't, write the case with
`"status": "subagent_failed"` and whatever it did return in `deliverable`.

Two things never enter a brief: the tool schemas (beyond what the level allows) and the
assertions. Handing over the schemas measures nothing, since production won't; handing
over the assertions teaches to the test. Don't tell the sub-agent it is being evaluated
either — an agent that knows it is on a discovery test performs discovery it would never
otherwise attempt, and `found_tool` goes up for reasons the user will never see in
production.

When an L1 case fails, add its L3 control (same tool, exact arguments) to `plan.json`
and run it — announce it, no fresh approval needed, since it is the same read-only tool.
It is the only thing that separates "the tool is broken" from "the tool is invisible",
and those two findings have opposite fixes. If the failed tool is write-capable, the
control never runs automatically.

Do not pull tool payloads into this session while the run loop is going. The hooks are
already capturing them to `payloads/`, and grading reads them later by targeted search —
that split is the whole reason a 50k-token result can be measured without being paid
for twice.

---

## Stage 5 — Grade

Read `${CLAUDE_PLUGIN_ROOT}/references/grading-guide.md` now. It carries the method:
programmatic versus semantic assertions, when an outcome is `null`, the grounding
verification ladder, trajectory computation, and the verdict rubric.

Mandatory, in-session, every assertion of every case. The gates:

- Score against artifacts, never against memory of the run. Inputs are the case's
  `result.json`, its `telemetry.jsonl` lines, and the `payloads/<tool_use_id>.txt` files.
- Grounding is verified against the payload files, not against the sub-agent's word.
  Its SOURCES section says where it believes each claim came from; the payload says
  whether it was there. Search those files for the claimed excerpt — don't read them
  whole, they run to 200 KB and grading needs the context more than you need the prose.
- Both verdict fields are trinary and neither ever defaults to false. `passed` is
  `true | false | null`, with `null` carrying its reason in `evidence`. `grounded` is
  `true | false | null`, where `false` means fabricated and nothing else, `null` means
  not payload-verifiable (truncated payload, missing artifact, or a claim the agent
  openly declared as its own knowledge), and `reason` is required whenever it isn't
  `true`. `fabrications` counts only the `false` ones, computed from the claim rows —
  so the value has to carry the meaning, never a note beside it.
- Write `cases/<id>/grading.json` per case, then aggregate `grades_summary.json` with a
  verdict paragraph that names the cases it rests on and states what was never tested —
  skipped write tools, ungradable cases, and anything listed in
  `plan.interview.unanswered`.

---

## Stage 6 — Report

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/report.py eval-workspace
open eval-workspace/eval-report.html    # xdg-open on Linux
```

Then give the user the verdict and the two or three findings that drove it, in prose, in
the session. The dashboard is the evidence; your paragraph is the answer.
