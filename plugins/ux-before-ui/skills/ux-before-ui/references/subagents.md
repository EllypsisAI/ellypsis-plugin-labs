# Running the method with subagents (and alone)

*The lead keeps the synthesis and protects its own context; agents do the substantial reading, counting, searching and drawing. This file records the working pattern as it actually ran between a lead and seven agents in one day: the brief anatomy, the mid-run messages, the hand-backs, and what the lead did in between. Brief with pointers into the run folder; do not pre-read to write a brief; verify claims before the owner sees them.*

## Contents

1. Roles
2. Brief anatomy (research briefs and drawer briefs, as they were written)
3. The research stage: three agents in one turn, and what the lead does while they run
4. The drawing stage: reference board, shared stylesheet, partitions, generators
5. Mid-run messages: notice, spec change, ruling, twin, re-brief
6. Truth-checks
7. Hand-backs and the lead's review
8. Revision rounds
9. Running it alone
10. Time and budget

---

## 1. Roles

| Role | Weight | Reads | Writes | Must | Never |
|---|---|---|---|---|---|
| **Lead** | strongest model | reports and boards; the design system; everything at the end of each stage | `FRAME.md`, `DESIGN.md`, `SCREENS.md`, the reference board, the shared stylesheet, `REVISION_n.md`, `HANDOFF.md`, the run log | frame, brief, prepare the fixed things, synthesise, decide with reasons, rule on shared data, review every board, talk to the owner | delegate the synthesis; pre-read code to write a brief; let an agent talk to the owner; ask the owner anything mid-run that can be queued |
| **Auditor** | strong (judgment on severity) | the running product at both viewports, its code for pointers, the glossary | `INVENTORY.md`, `ACTION_MAP.md`, `FRICTION.md`, `shots/`, `capture/` | click everything; count; give every claim a shot + file:line and re-verify the citations before handing back; separate demo defects; say what could not be reached | change product code; opine on taste; propose designs |
| **Audience researcher** | strong | human sources first (the owner's words, feedback, sales notes, canon, legal), the products the customers already use (their current help pages), and **last** the product's own copy and behaviour, to fill the "Today" column | `AUDIENCE.md` (with journey and jobs) | mark `[A]`; quote only from documents; verify third-party claims live (one web fetch settled who may approve the add-in on a Microsoft 365 work account); derive principles; list owner-only questions | start from the screens (they carry the maker's assumptions); invent quotes; change code |
| **Explorer** | strong | the reference library or its substitutes; the owner's words and two current screenshots for context | `PATTERNS.md`, `refs/` (or a manifest + download script) | look at every image; keep running notes per search; mechanism / steal / doesn't fit; one pattern per area; flag open questions | recommend visual style when a system is fixed; resolve the owner's calls |
| **Drawers** (2–4, parallel) | strong (they check truth against code) | `DESIGN.md`, `SCREENS.md` (their rows), the named sections of `AUDIENCE.md` and `PATTERNS.md` by line range, the reference board, the stylesheet, the glossary, the design system's own component sources, today's screenshots of what they replace, and the code behind every claim on their boards | their row's boards only, and their own generator scripts in scratch | copy the head verbatim; use only the stylesheet's classes; truth-check every sentence; render, look, fix, repeat; measure and trim; report catches, conflicts and tool traps | touch another drawer's files or the stylesheet; invent colours, shadows or words; use real customers; publish |
| **Blind tester** (build stage, later) | strong | the boards and the spec, before the code | expectations | write what the built thing must do from the boards before reading code | read the implementation first |

Model choice by task weight, set explicitly per agent. In the run every agent ran on the strongest model, because each one judges (severity, fit, truth); a pure file-lister could run lighter.

## 2. Brief anatomy

The research briefs and the drawer briefs had the same skeleton and different middles. Both fit on one screen; both carry paths, not pre-read content.

**Research or audit brief** (auditor, researcher, explorer):
1. **One line of role and scope**: "You are the AUDITOR in a UX redesign run for X. Research task: do NOT change any product code. Run dir (write everything here): `<path>`."
2. **Why this run exists**: the owner's complaint in two or three sentences, and the path to his sharpest example, marked "read it first". For the explorer, the product in plain words (what is sold, to whom, the flow, the money) in one paragraph, because the library agent knows nothing about the product.
3. **What to produce**: numbered deliverables with filenames and exact contents: table columns spelled out ("action · who · how often · where it starts · exact click path (count clicks and screen changes) · prerequisites · where it dead-ends · file:line"), the section list for a document, the pattern areas with two lines each and the three lines per reference (mechanism, steal, doesn't fit), the naming scheme for screenshots.
4. **Tools and environment traps**: how to run the thing (demo mode, its README and scripts, fixtures), the browser binary path and "never run `playwright install`", how to load the library tool and the parameters to use on every call, limits ("screens 8–12, flows 3–5, ~20–30 searches"), "look at the images, don't describe from metadata", "download the images, URLs expire". If a state cannot be reached: "say so and describe it from code rather than faking it."
5. **The locked words** (path) and the things not to reach for (parked assets, other products in the repo).
6. **Return protocol**: "Your final message is your report to me: ≤N words (the five worst friction points, the signup → first-value chain in one line with its screen count, what you could not reach), plus a **journal notes** section: what happened, what was contested, what you verified yourself vs. took on faith. All details live in the files."

**Drawer brief** adds, in this order:
1. The completeness mindset block, verbatim, at the top (drawers build; researchers get scope, not the ocean).
2. **Read first, in this order**, with line ranges: `DESIGN.md` (which decisions matter most for this row), `SCREENS.md` ("your screens: row B and row E"), the named sections of `AUDIENCE.md` ("§1b, §3, §4 moments 7–10 — you are drawing for the member"), the named sections of `PATTERNS.md`, the glossary, the reference board and the stylesheet ("copy A1's head, helmet and wrapper VERBATIM; move `aria-current` to your place; do NOT edit shared.css or A1; a genuinely new shared class goes in your own board's style block and into your report"), the design system's README for intent.
3. **Write**: the exact filenames, into the exact folder, and "do not touch any other file in that folder (siblings are drawing A*, C*, D* in parallel)".
4. **Format rules that fail silently**: the one script line to keep exactly, closed elements, quoted attributes, the root's fixed size and the same numbers in the canvas declaration, the required script stub, no template expressions, no innerHTML, no emoji, no icon packs, no iframes, real buttons and inputs and labels, the language attribute, a unique title, the sizes (desktop 1440 wide, height to content, phone 390 × 844 exactly). Overlays: "draw the page underneath fully, then the scrim and the floating window on top, inside the same root."
5. **Quality bar**: what the owner will judge these screens by, in the row's own terms ("Overview must read in five seconds: what waits for me, does it work for everyone, what got sorted"), exactly one raised panel, one obvious primary action, sober copy, and "match A1's look exactly (same bar, type scale, spacing rhythm). Where the spec leaves room, decide like a senior product designer and say what you decided in your report."
6. **QA your own boards visually**: the render command, "open the PNG with your Read tool and fix what is off (overflow, clipping, wrapping, misalignment, dead space; trim the board height to content + ~64 px). Iterate until clean. Do not publish anything; the lead assembles and publishes."
7. **Return protocol**: per file its final W × H and one line on what it shows and any decision beyond the spec; any spec or glossary conflict; the journal notes.

Where two drawers' boards are twins (the upgrade dialog and the purchase dialog), the brief says so and names who draws which, and the lead follows up with the reference as soon as it exists (§5).

## 3. The research stage

The three research agents were launched **in the same turn**, in the background, before anything else was written, each blind to the others' conclusions:

- The auditor must not read `AUDIENCE.md` first, or the friction list inherits the researcher's theory instead of the clicks.
- The researcher must not start from the existing screens, or the audience inherits the maker's assumptions; it reads the product's copy last, to fill "Today".
- The explorer gets the owner's words and two screenshots for context and the pattern areas from the frame; it does not wait for the audience document.

**What the lead does while they run** (about three hours in the run): prepares the fixed things. Uploads the fonts to the canvas, reads the design system's building blocks and finds the component that answers the owner's constraint (the system's own menubar was the full-width top bar without the frosted effect), writes the shared stylesheet from the tokens, learns the board format, and renders one test board. This is the moment to discover that a font declared with a relative path does not load; in the run it was discovered a revision later, after the owner said the boards lacked elegance. Status to the owner during this time is one short paragraph, no questions: "the three agents are still working; the fonts are on the canvas; I continue on my own when they report back."

As each report arrives, the lead reads it, says the one sentence that matters back to the owner ("nobody reads mail on this site"), and folds it in, but **does not fix the information architecture until the audit and the exploration are both in**. When they conflict (the explorer recommends the frosted pill; the audit shows text through it, 10 px labels and no account name), the lead writes the decision and the loser's reason in `DESIGN.md`.

## 4. The drawing stage

1. **The lead draws first**: the reference board (the most representative screen: the plans page, the home, slide one) and the shared stylesheet from the system's tokens. Render it locally; look at it; fix what is off (in the run: the wordmark and one bar item had picked up the accent colour). Nothing is briefed until the reference board renders correctly, because every drawer copies its head.
2. **Then the spec.** `SCREENS.md` is written after the reference board, so its board format section describes a file that exists.
3. **Partition by row.** One drawer per row or half row. Each brief names the drawer's files and the siblings' files as do-not-touch. Filenames and sizes are fixed in the spec; a drawer that needs a new board asks.
4. **Shared things are the lead's**: the stylesheet, the head, the fictional data, the words. A drawer that needs a class puts it in its own board's style block, prefixed, and lists it in the report as "worth promoting"; the lead promotes once, for everyone.
5. **The lead draws in parallel**, its own row (the money path) and the thinking row, while the drawers draw theirs, and answers messages between boards.
6. **Drawers build generators.** Every drawer in the run ended up with a small script: one that assembles its boards from the reference board's head, helmet and bar read from disk at build time ("so the font block can never drift"); one that derives the side-panel board from the page board underneath it ("so the two can't drift apart"); one that derives the upgrade dialog from the purchase dialog, the failed-payment home from the sibling's home, the public pricing page from the owner's plans page. When the reference changes, the board is regenerated, not redrawn. Say this in the brief so they start that way.
7. **Each drawer renders its own boards**, reads the PNG, fixes, and repeats (three to eight rounds per board in the run), measures the real content bottom with a script and trims the board to content plus ~64 px, runs the format check, diffs its head, helmet and bar against the reference to prove they are verbatim, and sweeps the visible text (tags stripped) for banned words.

## 5. Mid-run messages

Five shapes, all short, all to a named agent, all sent the moment the need appears rather than batched:

- **Notice** (a shared thing changed): "shared.css updated (lead): base resets now sit in `:where(.ui)`, so button text renders light-on-dark correctly (before, it was invisible). New class `.ui-well` = a panel-coloured well to lay a raised panel on. Re-render your boards before you finish; no action needed if they already look right." Sent to all four drawers at once.
- **Spec change** (from a finding): "One spec change for C5 + C8 (from the auditor's findings): the 'explain my sorting' setting moves to where it governs. On C5 add one quiet owner-only line under the lede: '…'. On C8 drop the line from the account section. Everything else as SCREENS.md."
- **Ruling** (shared data or a conflict a drawer raised): "Lead ruling on shared data (found by drawer 2, applies to C5–C8): (1) Peter has given permission but has NOT installed the add-in, so none of Peter's mail is sorted: no 'Peter's inbox …' rows anywhere. The third person in the log is Jonas: installed, every sort blocked until his IT admin approves the add-in. Keep 38 emails / 3 people. (2) The returning owner bought on 3 March, not 18 April, so … (3) Team state: … If you already drew otherwise, fix and re-render." Numbered facts, the source of the catch named, the consequence for each board, one closing instruction.
- **Twin** (a reference the brief promised): "My first-time purchase dialog is now at `A2-buy.html`: build D4 as its twin (same frame, same two-column body with the receipt in a well on the right, same button and fine line), differing only where SCREENS.md D4 says."
- **Re-brief** (a revision round): the owner's words in one sentence · "read `REVISION_n.md` first" · **already done globally by me** (fonts, knobs, dividers, the logo slot, and "keep that") · **your specific changes**, per board, with the owner's comment where there was one · "no dashed dividers in UI, less mono, re-render, QA, trim heights, only touch your files" · "report: per board one line on what you cut or changed, plus journal notes." Where a sibling's board is the drawer's reference, say "I'm editing A2 now" so the drawer knows to wait or check.

Drawers, for their part, noticed the changes by re-reading the shared files from disk, checked file times to see whether a reference had been revised before mirroring it, applied the rules directly when it had not, and re-aligned wording when it landed.

## 6. Truth-checks

Mockups lie effortlessly, and the builder will find out. Every drawer checks every claim on its boards against the real system before returning, and reports what it found. In the run the drawers did this on their own initiative, before drawing: one read the storage defaults, the 'explain my sorting' setting, the schema and the retention policy "to keep the fiction honest"; one checked the billing code before writing a field note that the company's VAT number appears on the receipt ("I don't want a false fact on the screen"); one removed a timestamp it could not vouch for ("DESIGN.md asks us not to fake data"); one searched the repo for a verified third-party UI path and, finding none, used generic wording flagged as unverified. Catches, all fixed on the boards before publication:

- A person shown in the activity log who could not appear there (not installed yet) → replaced by someone who could, with blocked sorts shown as blocked; the lead ruled and broadcast.
- "We keep the sender, the subject and why" → the *why* is not stored by default (a decision record said so) → "by default only sender, subject and label", everywhere it appeared.
- Only emails the add-in moved carry a reason → the log-row board opens a moved email, not one left in the inbox.
- The company's VAT number promised on the receipt → the payment provider does not print it → the claim removed.
- A plan upgrade through the same dialog → today the billing endpoint returns a manage-subscription link, not a checkout → listed in the needs, the button labelled honestly.
- A cancel URL pointing at the billing page, not the object → in the needs.
- A locked sentence about the third-party install step → used verbatim on the two boards where it applies; when the copy checklist dropped it from the member's corridor, the lead put it back.

The rule for drawers: **if a sentence on your board asserts something about the system, find the code or the record that makes it true; if you cannot, change the sentence and tell the lead.** The rule for the spec: **the fictional data must obey the product's own state model** (who can appear where, what exists at which date); when a drawer finds it does not, the lead rules for everyone.

## 7. Hand-backs and the lead's review

The hand-back shape that made the lead's review fast (drawers):

1. One line: all boards drawn, rendered, checked by eye, format check passed, only my files touched.
2. How they are built (the generator, what it copies from where, how to re-sync).
3. **Per board**: W × H, what it shows in one line, and the decisions beyond the spec, each with its reason.
4. **Where I departed from the spec or the shared data, please rule**: numbered, with the evidence (the Peter/Jonas catch arrived this way).
5. **Board-local classes worth promoting.**
6. **Tool traps for the siblings** (the harness reading the first width/height it found).
7. **Journal notes**: what happened · what was contested · verified myself · taken on faith.

Researchers and the auditor: the headline items the brief asked for (the five worst friction points; the roles and top principles and the three losing moments; one recommended pattern per area and the three findings), the file paths, what could not be reached or downloaded and what the owner can do about it, and the same journal notes.

The lead, on each hand-back: reads it, looks at the boards (or the report's evidence), relays any catch to the siblings it touches **immediately** (not after all reports are in), answers the "please rule" items, fixes a shared tool if a trap was reported, and tells the owner in one paragraph what landed. **Trust but verify** before the owner sees anything: render the claimed boards, `ls` the claimed files, grep the claimed fix. A hand-back describes intent.

## 8. Revision rounds

- The owner's comments come in on the board and in a message. The lead writes `REVISION_n.md` (their words verbatim → rules) before anyone redraws, and finds root causes first (the fonts).
- The lead makes the **global changes itself**: the system's knobs, the font declarations in every head, the shared classes (the logo slot), the reference row, the "Before" row from copies of the previous boards with the previous stylesheet.
- Then the **re-brief** (§5) to the same drawers, resumed with their context. New boards the owner asked for go to the drawer whose row they belong to.
- Drawers regenerate rather than redraw, re-align to references as they land, and flag the calls that are the lead's: a dashed ring that marks a state rather than a divider; a locked sentence dropped by the checklist; a rule the lead added last round that the drawer now cuts, with the reason. The lead answers each, and the ones that are the owner's (a page with no raised panel, against a system rule, kept for calm) go to the owner's list.
- A second truth pass after the rebuild: revisions introduce new sentences (one drawer changed "we never store your mail" because, with 'explain my sorting' switched on, the system does store a snippet).
- Ideas that arrive during the round go on a **separate page or row** as an exploration; the approved page is not touched unless the owner says so.

## 9. Running it alone

Same phases, same order, same artifacts. Differences:

- Write each artifact to disk **before** starting the next; your context will not hold the audit and the audience and the patterns at once, and the folder is the memory a later session (or a crash) reads.
- Do the audit before the audience document, then reread the audit after writing the audience document, and write down what changed your mind (that is the reconciliation the lead does in `DESIGN.md`).
- The caps matter more: exploration in hours, one pass per pattern area; the reference board before any other board; render after every three boards, not at the end.
- Truth-check as you draw, board by board; you do not have a drawer reporting catches. Keep your own "please rule" list and answer it in `DESIGN.md`.
- Keep the owner's gates the same: the frame in one message; the full board once; the open calls queued.

## 10. Time and budget

- A full run on an existing web app with three roles: one long day. Research stage ~3 hours in parallel (auditor, researcher, explorer). Synthesis and reference board ~2 hours. Drawing 32 boards with four drawers ~2 hours. Publication, the owner's reading, revision two with the same drawers ~3 hours. Handoff ~1 hour.
- Per agent in that run: roughly 190K–360K tokens, 25–52 tool calls, 6–8 minutes of wall time per turn (a drawer's revision turn was the same size as its first turn).
- A landing page: hours end to end; one drawer or none.
- A deck: half a day; the outline-as-decisions is most of the work.
- If the research stage passes a day, the frame was too wide or research became the hiding place. Cut to the riskiest moment and move.
