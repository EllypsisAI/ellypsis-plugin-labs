# Grading guide

How to score a case against what was actually captured. Read at grading time, once,
before writing the first `grading.json`. Shapes come from `workspace-contract.md`; this
file is about how to reach the values honestly.

Grading happens in this session rather than in a sub-agent because it is judgment work,
and judgment is the one thing that shouldn't be delegated to the cheap model running the
tests. It is also the stage where the eval can most easily lie — by scoring what it
hoped happened rather than what the artifacts show.

## Inputs per case

| Source | Carries |
|---|---|
| `cases/<id>/result.json` | The deliverable, the sub-agent's claimed sources, self-reported friction |
| `telemetry.jsonl` lines with this `case_id` | Every call: tool, args, timing, size, error state, first 500 chars of payload |
| `payloads/<tool_use_id>.txt` | The full payload (200 KB cap, truncation marked) |

**Context discipline.** Payload files run to 200 KB. Never `Read` one whole — search it
(`grep -c`, `grep -o`, a short Python check) for the string you're verifying and read
only the hit. A grading pass that pulls six payloads into context wholesale will run out
of window before the verdict, which is exactly the failure the sub-agent architecture
exists to prevent. And check `payload_excerpt` on the telemetry line first: it's already
in context and it settles a good share of claims for free.

## Assertions

Pick the method the assertion actually needs.

**Programmatic** — decidable from telemetry fields without interpretation: a call to the
expected tool exists, `is_error` is false, `est_tokens` sits under a threshold, the first
call's `args` validate against the input schema, `calls_to_first_correct` ≤ N. Record
`"method": "programmatic"` and cite the telemetry line in `evidence`.

**Semantic** — anything about usefulness, phrasing, or fitness for the audience the
interview named. Reason over the deliverable and the trajectory, then write the reasoning
into `evidence`, naming the specific call or sentence you relied on. Evidence that
doesn't point at something specific isn't evidence; "the answer was good" is a second
opinion, not a grade.

**The null rule.** `passed` is `true`, `false`, or `null`. Use `null` when the assertion
genuinely cannot be judged from what was captured, and put the reason in `evidence`:

| Situation | Why it's null, not false |
|---|---|
| No telemetry lines for the case | The hooks didn't fire. Nothing was observed, so nothing failed |
| Sub-agent blocked before reaching the tool | The case never tested what the assertion is about |
| Assertion needs a domain input the user declined to give | The gap is in the plan, not the server |
| Payload truncated at the 200 KB cap past the point of interest | The evidence exists; it just isn't on disk |

A null is information — it tells the user their eval has a hole and where. A false
invented to fill the field is a lie that ships in a dashboard and gets quoted in a
go/no-go decision.

## Grounding

Walk each factual claim in the deliverable and try to break it. The sub-agent's SOURCES
section is the map, not the proof — it says which call it believes produced each claim.
Verification is against the captured payload.

`grounded` is trinary, for the same reason `passed` is. `false` means **fabricated** and
nothing else; `null` means **not payload-verifiable** — the evidence isn't on disk, or
the claim was never offered as tool-sourced. Collapsing the second into the first is the
fail-closed default sneaking in through the back door: it would invent fabrications on
exactly the servers whose payloads are too big to capture whole.

| Check, in order | `grounded` | `reason` |
|---|---|---|
| Excerpt appears in `payload_excerpt` or in `payloads/<tool_use_id>.txt` | `true` | — (omit) |
| Cited call has no telemetry line | `false` — the strongest fabrication signal there is: the agent sourced a claim to a call it never made | `"cited call not in telemetry"` |
| Cited call exists but `is_error` is true | `false` — an error payload didn't supply the fact | `"cited call returned an error"` |
| Excerpt absent from an intact payload | `false` — the call happened and the content isn't in it | `"not present in the captured payload"` |
| Claim reads as tool-sourced but cites nothing, and no captured payload plausibly carries it | `false` | `"presented as tool-sourced with no plausible source"` |
| Excerpt absent, payload hit the 200 KB cap | `null` | `"payload truncated at the 200 KB cap; evidence may lie beyond it"` — also add a caveat to `grades_summary.json` |
| Payload file missing for a call that has a telemetry line | `null` | `"payload artifact missing"` |
| Claim openly attributed to the agent's own knowledge | `null`, `source: null` — honestly declared, so not a fabrication, and there is no payload it could be checked against | `"agent's own knowledge, declared as such"` |

The **value** carries the semantics, not the prose beside it: `null` versus `false` is
what separates unverifiable from fabricated, and `reason` only says which flavour of
each. That split matters because `fabrications` is computed from the claim rows — a row
marked `false` with a note reading "not really a fabrication" gets counted as one by
anything aggregating the data, including the dashboard. `reason` is required whenever
`grounded` is not `true`.

A declared own-knowledge claim is `null` rather than `false` because the agent did the
honest thing by labelling it. That said, it still deserves a mention in the verdict when
the deliverable leaned on it — an answer that reads as CRM data but rests on the model's
priors is a real finding, just not a fabrication.

Match on substance, not characters. A payload holding `"name":"Contoso Fabrication"` grounds
the claim "Contoso Fabrication is in the CRM"; a rephrasing is fine, an invented number is not.
Numbers deserve the strictest reading — "three open deals" needs three deals in the
payload, not an unspecified list the agent counted optimistically.

`fabrications` counts `grounded: false` claims only — never the nulls. It carries real
weight in the verdict: a server whose payloads are easy to misread produces confident
wrong answers in production, and that is worse than a server that errors. Which is
exactly why the count has to stay clean. A pile of nulls means the eval couldn't see;
a non-zero `fabrications` means the joint system made something up, and the two must
never be confusable in a number someone ships on.

## Trajectory

From telemetry alone, for the case's tool:

| Field | How |
|---|---|
| `found_tool` | Any successful (`is_error: false`) call to the case's tool. `false` if it never landed |
| `detours` | Tool names called before the first correct call — including other servers' tools. This is the selection-failure signal |
| `calls_to_first_correct` | 1-based index of the first correct call in the case's call sequence; `null` if it never came |

On an L0 case the tool is `null` in the plan, so "correct" means any call to the target
server. Detours at L0 are the interesting number — they show what Claude reached for
instead.

## Aggregating and the verdict

Fill `grades_summary.json` per the contract, then reason to one of three verdicts in a
paragraph that names the cases it rests on. A verdict without case ids in it isn't
reviewable.

| Verdict | The shape of the evidence |
|---|---|
| `dont-ship` | L1 fails while L3 passes on core tools — the tools work and nobody will find them. Or errors on the main path, or fabrications across multiple cases, or routine calls that blow the context budget |
| `ship-with-caveats` | The main path works at L1, with specific named holes the user can route around |
| `ship` | L1 passes across in-scope tools, deliverables trace to payloads, payloads and latency are sane |

The L1-versus-L3 gap is usually the finding. Both failing means the tool is broken; L3
passing alone means it is undiscoverable; those have opposite fixes and the verdict
should say which one this is.

State the coverage inside the reasoning, not as a footnote: write-capable tools that
were skipped, cases that came back ungradable, and any interview field in
`plan.interview.unanswered` all bound what the verdict can claim. A verdict that reads
as if it covered everything, when half the surface was never tested, is the one way this
report can do real damage.

Carry into `caveats` at minimum: `est_tokens` are chars/4 estimates, latency includes
hook overhead, plus any truncated payload and any grounding claim it blocked.
