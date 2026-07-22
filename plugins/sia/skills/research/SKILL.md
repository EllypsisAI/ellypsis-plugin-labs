---
name: research
description: "This skill is the research method — deep research on anything without flooding the main context. Use for any research request: 'research X', 'look into X', 'what do we know about X', 'find everything about', 'deep dive on', 'find me all', 'is X a good fit', competitive analysis, market scans, or when the user shares a company name or URL and expects intelligence gathering. Also use when a task needs research as context. Do NOT use for finding people (that's the contacts skill), writing messages (that's outreach), or logging results (that's the crm skill)."
---

# Research Orchestrator

Research is finding information if it exists. The orchestrator's job is to protect the space where judgment happens: subagents search, read, and distill; the main context plans, weighs, and concludes. Raw search output never enters the main context — once it does, it crowds out the thinking it was gathered for.

## The brief comes first

Fetch the **research brief** from the Ellypsis gateway before any research (once per session — skip if it's already in context). This method is deliberately generic — the brief is what makes it this company's research: what to hunt, which systems to check first, what counts as a signal, what shape the output takes. It may route you to other gateway bodies; follow it. Research on the method alone produces generic findings, which is exactly what a coworker exists not to do.

If the ask involves time ("recent", "past 6 months"), calculate exact dates from today's date before anything else. Eyeballed dates silently corrupt every filter downstream.

## Size the job before starting it

Both sizing failures are real: fanning out on a fact lookup burns time and tokens; answering a four-constraint sweep with one search produces a shallow answer that looks complete.

- **A fact, a page or two** → handle it yourself. Search, read, answer.
- **One clean angle** → one subagent, so the main context stays clean.
- **Several independent angles** → one round of parallel subagents, then compile.
- **Cross-referencing, multi-hop, exhaustive coverage** → multiple passes, compiling between them: find entities → find what relates to them → enrich; or scout broadly → dig where it's promising.

When the ask could honestly be read two sizes apart ("find competitors to X" — quick list or deep sweep?), describe both and let the user choose. Don't ask when it's clearly one size, or when the user already set the depth. A named number ("find 100") is a commitment — keep working until it's met.

## Dispatch

Search runs on Exa. Point every subagent to this skill's references — `exa-searching.md` always, the pattern file matching the work (`exa-companies`, `exa-people`, `exa-relationships`, `exa-news`), and `exa-processing.md` when it will extract, filter, or judge sources. Subagents read them; the main context doesn't.

Give every subagent three things: the task, the qualifying criteria, and the output format. The criteria go *to* the subagent because filtering must happen at the edge — a subagent that returns unfiltered results has moved the raw output problem into your context instead of solving it. Returns are compact and structured; they'll be merged with other subagents' output, and verbosity at that stage compounds.

- Decompose by **angle** — genuinely different questions (the skeptic's, the builder's, the practitioner's) — not synonyms, which land in the same place.
- 3–5 searches per subagent; independent workstreams dispatched in parallel, in one message; 3–5 seeds per subagent when enriching a list.
- Subagents don't need the strongest model.
- Empty returns → change the angle. Still empty → limited coverage is itself a finding; report it, never pad it. Off-topic returns → the query was too vague; longer and more specific.

## Compile

Deduplicate before anything else — synthesis over duplicates double-counts evidence. Same URL: drop. Same entity from different sources: merge, keep the best data.

Then check coverage: missing time periods, regions, entity types get targeted follow-ups. Heavy overlap between subagents is a good sign — independent angles converging. Fully disjoint results usually mean angles were missed, not that coverage is complete.

## Weighing what came back

- Convergence only counts across **independent, high-signal** sources. Three low-quality sources agreeing is shared noise, not confirmation.
- Practitioners over commentators — the people doing the work over the people writing about it. Skin in the game is the strongest quality signal there is.
- Decide who to *exclude* before synthesizing: misaligned incentives, unfalsifiable claims. Filtering out noise reliably beats hunting for brilliance.
- Red-team the compiled result: whose perspective is missing, what bias distorts the aggregate? A gap found here is one targeted follow-up, not a rerun.

## Evidence

A result appearing in search output does not mean it meets the criteria — Exa returns the pages most *similar* to your description, and similarity is not validation. Every result earns its place by being checked against the criteria. Cite sources for key claims; use the brief's recency window for anything presented as a signal; state gaps explicitly — "nothing found" is information, silence is not. Never fabricate a finding.

## Output

Follow the brief's output shape. Keep the main answer tight; tables when fields are uniform. If the full result doesn't fit readably, write it to a file (when the surface has one) and summarize above the pointer.
