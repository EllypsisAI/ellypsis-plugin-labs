---
name: crm
description: "This skill handles all CRM operations — creating records, logging data, and helping salespeople execute their task queues. Use when the user wants to persist anything to the CRM or work through their sales tasks. Trigger on: 'log it', 'save to CRM', 'create the org', 'add them to the CRM', 'create the opportunity', 'push to CRM', 'log the contact', 'save this', 'save the draft', 'save that draft for later'. Also use when the user brings up their task list and wants help working through follow-ups, or says 'mark it done', 'what tasks do I have', 'help me with my follow-ups'. This is the only skill that writes to the CRM — research, contacts, and outreach produce the content, this skill persists it. Do NOT use for researching companies (that's research), finding people (that's contacts), or drafting emails (that's outreach)."
---

# CRM Operations

Handles data entry to the connected CRM and helps execute tasks from the salesperson's queue.

This skill is deliberately CRM-agnostic. The operating manual for your company's actual CRM — which tools to call, creation workflows, lookup procedures, field conventions — is the **CRM pack**, served through the Ellypsis gateway. Your company's pack teaches the CRM your company runs.

## Before starting

1. Fetch the CRM pack: the gateway tool whose description names your company's CRM. Fetch it once per session, before the first CRM read or write. Tool schemas alone are not enough — the pack carries the workflows and constraints the schemas can't.
2. If the gateway is not connected, stop and say so. Never improvise CRM operations from raw tool schemas without the pack.

## Two modes

### Mode 1 — Data entry
The user has research, contacts, or drafts ready and wants them logged. Follow the pack's creation workflow. Always search before creating — duplicates are worse than a moment's delay.

### Mode 2 — Task execution (daily driver)
The salesperson wants to work through their active and overdue tasks. However the list arrives — fetched through the CRM tools or pasted in — group tasks by organisation.

**One org per thread.** If the list spans multiple orgs, pick one org, handle all its tasks, then say: "Done with [org]. Take the remaining tasks to a new chat so we start fresh." Multiple tasks on the same org share CRM context and belong together; switching orgs mid-thread bleeds details between companies.

For the selected org, run the pack's full-lookup procedure once, then process its tasks sequentially.

## Standing rules

- Nothing is written without the user's explicit go: "log it", "save it", "create it", "push it", "approved". "Looks good" / "ok" / "yes" is not a go. Writes execute immediately — there is no undo.
- Deletion is never part of any workflow. A wrong record gets corrected with a follow-up note, not removed.
- Never invent data to fill a CRM field. A field you don't have goes empty or gets asked about — a plausible guess in a CRM is a lie with a timestamp.
- Always search before creating. Surface what was created and which IDs were assigned.
- If a dependency is missing (logging a contact but no org exists), say so and offer to create it first.
- When something is learned that outlives the session — a correction, a preference, a dead end — log it to the brain before moving on.
