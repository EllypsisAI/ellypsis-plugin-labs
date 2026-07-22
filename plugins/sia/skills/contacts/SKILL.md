---
name: contacts
description: "This skill finds decision-makers and contacts at target companies. Use when the user asks to find people, look up who works somewhere, or identify who to reach out to. Trigger on: 'find contacts at X', 'who should we reach out to at X', 'find the right person', 'get me contacts', 'who's the fleet manager at X', 'look up people at X', 'find their procurement team', 'who can we talk to there'. Also use after company research when the natural next step is identifying people to contact. Do NOT use for writing emails (that's outreach) or logging contacts to CRM (that's the crm skill)."
---

# Find Contacts

Finds people who can say yes — or connect us to someone who can. If decision-makers aren't findable, find a path to them.

## Before starting

1. Research should already exist for this company — trigger the research skill first if not. Contact-finding without research produces names without reasons.
2. Fetch the CRM pack through the Ellypsis gateway (skip if already fetched this session) and run its Complete CRM Lookup: existing person contacts, their entries, linked opportunities. The lookup is the duplicate-prevention mechanism — "finding" someone we already know wastes the relationship we already have.
3. Fetch the research brief (skip if already fetched this session). Its **People asks** section carries the priority framework, the roles that matter per segment, the strategy classifications, and the per-contact output format.

In the normal arc — research, then contacts — both bodies are already in context and this skill adds zero new fetches.

## Searching

- Run search batches in subagents that return distilled contact lists, never raw results. Point each subagent to `skills/research/references/exa-searching.md` and `exa-people.md` — these are files the subagent reads directly; the research skill itself is never invoked.
- Start with a company directory or domain search — who works there, in what roles. Directories miss senior people; if decision-makers don't surface, search them directly by title. Conference speaker lists, industry associations, and press releases also carry names.
- A name without an email is still a path — include the LinkedIn profile.

## The lines that never bend

- Never fabricate email addresses. Guess formats only when explicitly asked, and mark them clearly as guesses.
- Web-sourced details are marked unverified until confirmed — a wrong contact detail logged to the CRM misroutes everything downstream.

## What usually follows

Contacts exist to be written to — outreach drafts the messages. The crm skill logs approved people, on an explicit go.
