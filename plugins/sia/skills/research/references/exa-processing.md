<!-- Curated from the Exa vendor plugin's extraction.md + filtering.md + source-quality.md (2026-07), combined:
all three cover the same moment — a subagent holding raw results, turning them into findings before returning. -->

# Processing results — extract, filter, tag

You hold search results; what you return gets merged with other subagents' output, so verbosity at this stage compounds. Compact, structured, judged — that's the contract.

## Extract

Snippets first. Titles, URLs, and highlights carry many fields (names, dates, rounds) — extract from what you have before fetching. Deep-read with `web_fetch_exa` when the snippet points at a value without containing it, when a judgment call needs body text, or when one rich page carries many fields. Batch 5–10 URLs per fetch; read full pages — truncating the page defeats the purpose of fetching it.

Field kinds, and how each is earned:
- **Literal** (name, date, amount): extract the stated value. Not present → "not found", never a guess — a guess contaminates downstream merging; a stated gap is information.
- **Categorical** (industry, stage, role level): map to the closest category; note ambiguity where the mapping is a stretch.
- **Semantic** (sentiment, "genuine opinion", relevance): read and judge, and include a one-line rationale — downstream synthesis needs to weigh your call, not just receive it.
- **Negation** ("no mention of X"): search for the positive case; absence is reported *with* a confidence tied to how thorough the coverage was. "Confirmed absent" (searched well, not there) and "not found" (limited coverage, paywalled) are different findings — say which.

Tag evidence strength: **direct** (source states it) · **inferred** (derived from context) · **uncertain** (single indirect signal).

## Filter

Hard filters first, soft second — hard checks are cheap and mechanical (dates, geography, thresholds, exclusions), so run them before spending judgment on rows that were never going to survive. Soft filters are judgment ("actually shipping" vs "just evaluating") — read what's needed, decide, and leave a one-line rationale per keep/drop so the reasoning stays visible.

- Temporal filters: exact date boundaries first, from today's date. An ambiguous date ("early 2025") gets flagged, never silently included or excluded.
- The ask sets the bias: "find every" → keep borderline cases, flagged; "top N" → precision, drop them. Default: keep flagged and let the orchestrator decide.

## Tag source quality

Quality tags are what let the orchestrator weight and rank — without them, a vendor blog and a practitioner post-mortem count the same.

Disqualify noise before deep-reading: no skin in the game (theorists without shipped work) · misaligned incentives (paid to sell, not to be right) · circular credentials (validated only inside their bubble) · positive-only advice (no tradeoffs, no failure modes) · temporal decay (moved from doing to teaching — check they still practice).

The distinction that matters most: **practitioners do the work, commentators write about the work.** Shipped products, specific numbers, "we built X and here's what happened" — versus roundups, top-10 lists, links to others' work.

Tag each source with a short free-form `quality` note describing what you actually observed ("shipped the product, writes from direct experience") — not a category. Categories crush signal; description preserves it for ranking.

Run verification searches (who cites them, track record, criticism) only when the task itself is about credibility — for normal research, tag what you see and move on.
