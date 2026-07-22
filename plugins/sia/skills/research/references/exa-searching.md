<!-- Curated from the Exa vendor plugin's searching.md (2026-07, pasted verbatim by Sewar) + Ellypsis production learnings.
Sibling files: exa-companies, exa-people, exa-relationships, exa-news (query patterns), exa-processing (extract/filter/tag).
All vendor reference files are now folded. -->

# Searching with Exa

Subagents read this file before searching; it never loads in the orchestrator's context.

## The two tools

- **`web_search_exa`** — search by query. Params: `query`, `numResults`. Category filtering rides inline in the query string: `category:<type>`.
- **`web_fetch_exa`** — read full content from known URLs, after search, when snippets aren't enough. If it fails, fall back to any other fetch tool; if that fails too, skip and work with remaining sources.

Do NOT use `web_search_advanced_exa` or any other Exa tools. Filter and summarize results inline — no file juggling to process them.

## How Exa thinks

Vector embeddings, not keywords. You are describing a target page; Exa returns its nearest neighbors in embedding space. It does not match keywords exactly, does not understand boolean logic, and does not validate results against your criteria.

**Describe the page you want to find, not the fact you want to know:**

| Looking for | Bad query | Good query |
|---|---|---|
| Posts about X | "X" | "detailed blog post about X written by a practitioner" |
| Company doing Y | "Y company" | "category:company company building Y for [buyer]" |
| Person at company | "person at company" | "category:people senior [role] at [company]" |

Write queries as natural grammatical phrases. Inline categories: `company`, `research paper`, `news`, `personal site`, `people`.

## Sizing — match numResults to query precision

| Query precision | numResults |
|---|---|
| Named entity (specific person/company) | 5 |
| Precise filter (narrow category + constraints) | 10 |
| Broad discovery (wide category, few constraints) | 15 |

Never above 25. More coverage = more queries from different angles at 10–15, never one query at 50.

## Query diversity

- **Angles are different questions** — a skeptic angle, a builder angle, a practitioner angle. Synonym swaps ("overhyped" vs "overrated") are the same angle and waste calls.
- **Word order shifts embeddings** — for coverage on one angle, run 2–3 phrasings in parallel and merge.

## Encoding time

Calculate exact dates FIRST from the current date. Then encode them semantically in the query — "published in March 2026" — rather than relying on date filters. Never reuse dates from examples.

## Anti-patterns

- Boolean operators ("AND", "NOT") are just words to Exa.
- Quotes don't force exact phrase matching.
- 1–2 word queries scatter.

## When nothing comes back

Longer and more specific → different angle (not a synonym) → if multiple angles return nothing, the topic likely has limited web coverage: report that. Never fabricate.

## After getting results

Exa returns similarity, not validation — review titles and snippets, discard what doesn't meet the criteria, and `web_fetch_exa` the most promising URLs for full content. Deduplicate before returning: URL is canonical; for people, LinkedIn URL first, then name + current company.
