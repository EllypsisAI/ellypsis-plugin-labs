# Test plan guide

How to turn three interview answers into cases that measure something, and how to brief
the sub-agent that runs them. Read alongside `workspace-contract.md`, which fixes the
shapes; this file is about what goes inside them.

## What a case is

A case is **a task, phrased at a chosen information level, plus the assertions that
decide whether the joint system handled it**. Not a tool call with parameters — that
would test the server, and the server is not what's in question. The unit of measurement
is: given this much information, did the LLM get the user what they asked for.

Everything that makes a case good comes from the interview. The use case decides what
tasks are worth running, the audience decides the level, and the real inputs decide
whether the assertions can distinguish success from a polite empty response.

## The asymmetry ladder

Sub-agents don't act confused. They genuinely don't know what they weren't told — that
is why this measures anything at all. A persona instruction ("pretend you're a
non-technical user") produces theatre, because the agent still knows the answer and is
performing not knowing it.

| Level | The brief carries | Answers |
|-------|-------------------|---------|
| L0 blind | Task only. Server never named | Does Claude reach for this server at all, unprompted? |
| L1 civilian | Task + server name, phrased the way the audience talks | The real production condition for most integrations |
| L2 operator | Task + tool name + a precise ask | Does it work for someone who already knows the system? |
| L3 spec | Task + the exact arguments to pass | Ceiling check: does the tool work when called perfectly? |

L1 is the workhorse, because L1 is what production looks like: someone who knows the
system exists and describes their problem in their own words. L0 is worth one case per
server — it is the only measurement of whether the tool competes successfully against
everything else in the context. L2 is for tools whose users are genuinely power users
(the audience answer tells you). L3 is diagnostic, not a grade: run it after an L1
failure, never as the headline.

The gap between L1 and L3 is the most useful number this eval produces. L3 passes and L1
fails means the tool works and is undiscoverable — a description and naming problem. Both
fail means the tool is broken. Both pass means ship it.

## Default plan

One L1 case per in-scope tool, plus one L0 case for the server overall. Six to ten cases
for a typical server. Add, when the interview justifies it:

- **The empty case.** The input the user said should return nothing. Servers that answer
  "no results" badly cause more downstream fabrication than servers that error.
- **The chained case.** If the use case involves two tools in sequence (search then
  fetch), one L1 case for the sequence — the handoff is where argument fidelity breaks.
- **The neighbour case.** If two tools have similar descriptions, one L1 task that only
  one of them can satisfy. Selection failure between near-neighbours is invisible until
  you test for it.

Skip: cases that would pass for any server (does it return JSON), cases with no real
input behind them, and any case on a write-capable tool that the user has not approved
by name.

## Writing the task text

The task is what the sub-agent reads. It should read like a person asking for something,
not like a test.

| Level | Phrasing rule | Example |
|-------|---------------|---------|
| L0 | Name the goal, never the server or the tool | "Find out how many open deals we have with Contoso Fabrication and what stage they're at." |
| L1 | Name the server, keep the ask in the audience's words | "Check our Acme CRM — what's going on with Contoso Fabrication at the moment?" |
| L2 | Name the tool, state the ask precisely | "Use `search_contacts` on Acme CRM to find every contact at Contoso Fabrication, with their roles." |
| L3 | State the call | "Call `search_contacts` on Acme CRM with `{\"q\": \"Contoso Fabrication\", \"perPage\": 10}` and tell me what comes back." |

Use the user's real inputs verbatim. A task built on "Acme Corp" tests string handling; a
task built on the company the user actually named tests their integration.

Vagueness at L1 must be *natural* vagueness — the ambiguity a real person leaves in, not
an artificial riddle. "What's going on with Contoso Fabrication" is how people talk. "Retrieve
the entity associated with the industrial account" is a puzzle, and failing a puzzle tells
you nothing about production.

## Writing assertions

Three to five per case, each independently checkable, each pointing at a different
failure mode. Assertions are graded against the sub-agent's deliverable and the captured
telemetry — not against a raw JSON body — so they're written in those terms.

**Programmatic** — decidable from telemetry fields or the structure of the return:

| Pattern | What grading checks |
|---|---|
| "Calls `search_contacts` at least once" | A telemetry line for that tool under this case id |
| "No call returns an error" | `is_error` false across the case's lines |
| "Reaches the right tool within two calls" | `calls_to_first_correct` ≤ 2 |
| "Payload stays under 15k estimated tokens" | `est_tokens` on the relevant line |
| "Arguments are schema-valid on the first attempt" | First call's `args` against the input schema |

**Semantic** — needs judgment over the deliverable and the trajectory:

- "The deliverable answers the question as asked, not as the tool wanted it asked"
- "Every company and figure in the answer traces to a tool result"
- "A consultant who doesn't know the CRM's field names could act on this"
- "The empty result is reported as empty rather than filled in from general knowledge"

**Weak assertions to avoid**, and what they miss:

| Weak | Why it fails | Stronger |
|---|---|---|
| "Response looks correct" | Nothing to check against | "Names all three Contoso contacts the user listed" |
| "Server performs well" | No baseline | "Median call under 3s; no call over 10s" |
| "Has an ID field" + "ID present" | Same assertion twice; inflates the pass rate | Pick one |
| "Returns JSON with `data.items[0].name`" | Brittle; breaks on harmless schema changes | "Each result carries an identifier usable in a follow-up call" |
| "Finds the tool" on an L2/L3 case | The brief already named the tool | Reserve discovery assertions for L0/L1 |

The last one matters most: an assertion must be able to fail at the level it runs at.
Discovery assertions at L3 always pass and quietly inflate the score.

## Sub-agent briefs

The brief is the whole experiment. Everything the sub-agent knows, it knows because the
brief said it — so anything extra you add is a measurement you just destroyed.

Never in a brief: the tool schemas (beyond the level's allowance), the assertions, the
word "eval" or any hint that this is a test. The first two are obvious. The third is
easy to violate accidentally and is the most expensive: an agent that knows it is on a
discovery test will hunt through every available tool in a way no production agent does,
and `found_tool` comes back true for reasons the user will never reproduce.

Template — the only variable parts are the task and the one constraint line:

```
<task>
{case.task}
</task>

<context>
{level line — see below}
</context>

<report-back>
When you're done, reply with exactly these four sections and nothing else:

DELIVERABLE: your answer to the task, as you'd give it to the person who asked.
SOURCES: for each factual claim in the deliverable, which tool call produced it and
  a short verbatim excerpt from that result. If a claim came from your own knowledge
  rather than a tool, say so.
FRICTION: anything that got in your way — wrong guesses, retries, confusing field
  names, missing data, results you couldn't interpret. Leave empty if there was none.
STATUS: completed or blocked. If blocked, what blocked you.
</report-back>
```

Level lines:

| Level | `<context>` line |
|---|---|
| L0 | `Use whatever tools you have available.` (server never named, anywhere) |
| L1 | `The information lives in the <server> system, which you have access to.` |
| L2 | `Use the <tool> tool on the <server> server.` |
| L3 | `Call <tool> on <server> with these arguments: <json>.` |

The verbatim excerpt in SOURCES is the map grading follows, not the proof. Hooks write
each call's full payload to `payloads/<tool_use_id>.txt`, so grading looks the excerpt up
in the real payload rather than taking the sub-agent's word — see
`grading-guide.md § Grounding`. Asking for the excerpt is still what makes the check
cheap: it tells grading which file to search and what string to search for.

Spawn with `model: sonnet` unless `plan.json`'s `operator_model` says otherwise, and with
a general-purpose agent type that has real tool access — an agent restricted away from
MCP tools produces a clean-looking failure that has nothing to do with the server.
