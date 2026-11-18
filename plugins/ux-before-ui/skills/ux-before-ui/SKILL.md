---
name: ux-before-ui
description: Design method to run BEFORE drawing or coding any screen, page or slide. Consult it first whenever someone wants a UI, frontend, website, landing page, dashboard, internal tool, mobile flow, onboarding, signup or checkout flow, or a slide or pitch deck designed, redesigned, restructured or audited - including "where do I start", "propose a new IA", "audit the UX", "make it convert", "people drop off", "users cannot find anything", "feels dated or clunky", "make it modern, clean or premium", "just make the screens, mockups or wireframes" - regardless of stack (Next.js, WordPress, Framer, React, Figma) and whether they have nothing yet, a rough idea, an MVP or a live product. It sizes a purpose-first method to the medium - audience, journey and moments of truth, jobs and actions, how expert teams solve the same jobs, everything side by side, critique, handoff. Not for implementing an approved spec, a one-component or CSS fix, charts, or producing .pptx/.docx files.
---

# UX before UI

*A working method for designing anything visual that must deliver an experience, done the way expert teams do it: understand who comes and why, map what they must do, see how good teams solve the same jobs, then draw everything side by side, critique it, and hand it off. The medium (app, site, deck) and the purpose decide how much of each step you do. The method is the constant; the steps are tailored.*

## Why this exists

The common failure, in the words of the founder whose product this method rebuilt: "you just want to make UIs right away, you don't think it over, and you leave it to the AI to figure it out as it goes." A design system plus three style words ("modern, Apple-like, glassmorphism") and straight into screens. The result looks fine and works badly. Related actions end up in different places, buying takes four screens and a detour, and nobody thought about the customer's psychology, because nobody asked who the customer is. The same failure produces landing pages that describe features to people who wanted a price, and decks that show everything and decide nothing.

Experts do it the other way round. They put the drawing last, because a screen is only an answer, and you cannot answer before you know the question: who arrives, in what state, how often, wanting what, fearing what, and what must be true before they can have it. Everything in this skill exists to make you ask that before you draw, and then to draw *everything* at once, side by side, so the design can be judged as a whole.

## The phases

One folder per run (for example `design/<date>-<slug>/`). Every phase writes its artifact there before the next starts. The folder is the memory: subagents read from it, the handoff points into it, and a crashed session leaves a readable trail.

| # | Phase | Question it answers | Artifact | Shrinks or disappears when |
|---|---|---|---|---|
| 1 | **Frame** | What must this thing make happen, for whom, and which analyses matter here? | `FRAME.md` | never |
| 2 | **Audit what exists** | What is there, what can you do, in how many steps, and where do people get lost? | `INVENTORY.md`, `ACTION_MAP.md`, `FRICTION.md` | nothing exists yet |
| 3 | **Audience** | Who comes, how often, knowing what, in which words, with which mental model? | `AUDIENCE.md` | one audience you know well |
| 4 | **Journey and moments of truth** | In what order do they meet it, and what do they think, fear and need at each moment? | `JOURNEY.md` (often a section of AUDIENCE) | never |
| 5 | **Jobs and actions** | What do they hire it for, ranked, and which actions must it support? | `JOBS.md` (often a section of AUDIENCE) | never |
| 6 | **Explore** | How do expert teams solve each of those jobs? | `PATTERNS.md` | strong precedent already in hand |
| 7 | **Decide and draw** | What do we decide, why, and what does every screen/page/slide look like next to the others? | `DESIGN.md`, `SCREENS.md`, `boards/` | never |
| 8 | **Critique and revise** | What does the owner see that we cannot, and which rule does each comment become? | `REVISION_n.md` | never |
| 9 | **Hand off** | What does a builder need to build it without us in the room? | `HANDOFF.md` | never |

Phases 3 to 5 usually run as one research brief for one agent and land in one document with three sections; the order matters more than the file count. Phase 2 runs in parallel with them when there is something to audit, and so does Phase 6. While they run, the lead prepares the **fixed things**: verifies that the design system actually renders (fonts, tokens), writes the shared stylesheet, learns the canvas or board format, and renders one test board. In the run this skill comes from, the fonts had silently fallen back to the system face and nobody noticed until the owner said the boards lacked elegance; the check belongs here, not in revision two.

## First run: choose where the references come from

Without real screens to look at, a model draws the average of what it remembers, and that average is what makes generated UI look generated. Screens from shipped products give it mechanisms real teams have already tested. In the experience of the people who built this method, the runs with a reference library came out clearly better than the runs without one. That is their observation, not a measured result.

The first time the skill runs in a project (there is no earlier run folder with a `FRAME.md`, and the user has not said where references come from), tell the user this in a few lines before Phase 1 and let them choose:

| Option | How | Trade-off |
|---|---|---|
| **Mobbin MCP** (recommended): [mobbin.com/mcp](https://mobbin.com/mcp) | Add the connector and sign in once | Best results: the explorer searches flows and screens itself and looks at every image. Needs a paid Mobbin plan |
| **Screenshots from Mobbin** | The user searches [mobbin.com](https://mobbin.com) and drops screenshots into the run folder | No connector needed; coverage depends on what the user picks |
| **Mobbin in the browser** | The user signs in to Mobbin in a browser Claude can control and gives Claude access to it | No connector needed; slower than the MCP; uses the user's own account |
| **Your own references** | The user gives Claude screenshots, links or files of products they admire or compete with | No Mobbin at all; Claude only knows what it is given, so give it plenty |

Record the choice in `FRAME.md`; later runs read the latest one and do not ask again. If the user chooses none, run Phase 6 on the fallbacks and say in `FRAME.md` that exploration ran without a reference library.

## Phase 1: Frame. The purpose decides the method

Do not start from the medium ("we need an app"). Start from what it must make happen. Write one sentence:

> **[Thing] exists so that [who] can [understand / decide / do X] [when, how often], and we know it worked when [an observable event].**

Examples: *"The console exists so a company owner can buy the add-in for the company and get it sorting each colleague's inbox inside their own mail client within a day; it worked when each person's first email is sorted."* · *"The landing page exists so a stranger from a LinkedIn post understands what we sell, what it costs and why to trust us in under a minute, and books a call."* · *"The deck exists so four investors, live, in twelve minutes, believe the problem is real and this team can win, and agree to a second meeting."*

Then answer seven sizing questions; each one turns a phase up or down:

1. **Is there something already?** → Phase 2 on or off, and how deep. What exists is evidence of what its maker thought mattered, so audit it before you trust it.
2. **How often do they come, and how long do they stay?** Once, three times, daily? This decides whether you design for "understood at first sight" or "efficient once learned". Most products are designed as if for daily use by people who come three times.
3. **Where does the value happen, here or somewhere else?** If the value happens elsewhere (inside another product, after the meeting, at the checkout of a third party), the journey must include those steps, and the finish line is the first proof of value, shown *here*.
4. **How many distinct people or roles?** Each gets its own corridor and its own row on the board. A role that visits once must never inherit the daily user's interface with parts greyed out.
5. **Which moment carries the most risk?** Money, trust, a decision, a scary click (a login, a permission, a signature). That moment gets the exploration budget.
6. **What is fixed?** A design system, a brand, a locked vocabulary, a platform, a tool. Fixed things shape Phase 7; they also need verifying (a design system that silently fails to load its fonts will make everything look generic).
7. **What cannot be true yet?** Data, capabilities, content that does not exist. Start the "needs" list now, and never fake it on a board.

Write `FRAME.md`: the sentence, the medium, the starting point, the answers, which phases grow and shrink, the inputs available (reference library? canvas? system?), the fictional data you will use, and the words that are locked. It is a page, not a study: it steers the research, it does not replace it. **Confirm the frame with the owner in one message**, with your recommendation and reasons, before spending anything. Read `references/tailoring.md` for the full medium × phase and starting-point × phase tables; the short versions:

**Starting points.**

| You have | Enter at | Grows | Shrinks |
|---|---|---|---|
| Nothing yet | Frame → Audience | audience, journey, exploration (you have no evidence, so borrow it from how experts solved the same jobs) | audit (none); actions are derived from jobs, not counted |
| A rough idea | Frame → Audience, then sketch the journey early to test whether the idea survives contact with the moments of truth | journey and moments (the idea lives or dies there) | audit; exploration narrows to the two or three moments the idea depends on |
| An MVP | Frame → quick audit (counts and hunts) → Audience | action map; audience (usually never done for an MVP) | inventory (few screens) |
| An existing thing that feels clunky | Frame → **full audit first** → Audience | audit; the "before" row on the board | exploration narrows to the top friction areas |

**Media.**

| Medium | Audience means | Journey means | Actions mean | Side by side means |
|---|---|---|---|---|
| Web app, internal tool | roles, visit frequency, what they already use | entry → first value, including steps in other products | every action: who, how often, clicks, screens, prerequisites, dead ends | every screen and state, desktop and phone, one row per corridor |
| Website, landing page | where they come from, what they know, what they compare with | arrive → recognise → understand → trust → act → after | the few things a visitor can do; one job per page | every page and fold, desktop and phone, one row per visitor path |
| Slide deck | who is in the room, live or read alone, who decides | the narrative arc: where they doubt, where they decide | what the room must understand or decide, slide by slide; the ask | every slide in order on one board, alternates of the key slide beside it |
| Anything else (email sequence, kiosk, print, dashboard) | derive from the purpose sentence | the order they meet it | what they must do or see at each point | every piece in the order it is met |

## Phase 2: Audit what exists

Only when something exists. Three artifacts, one auditor, no code changed.

- **`INVENTORY.md`**: every screen, panel, dialog and state (empty, first-run, error, failed payment, expired link), what it shows in order of visual weight, what you can do there, and a screenshot at real viewports (desktop and phone). Click it, do not read it: screenshots of what the eye gets, not full-page captures that paint a fixed bar in the middle. Record defects of the demo or environment separately from defects of the product.
- **`ACTION_MAP.md`**: every action as a row: who · how often · where it starts · exact click path · **clicks / screen changes** · prerequisites · dead ends and bounces · code pointer. Then the dependency graph (what must be true before what, and who enforces it), and the **dependency chains** from entry to first value, screen by screen, with every **hunt** marked (a place where the user must find the next step themselves). Close with "where each hunt could have been a handoff": what the system already knew at that moment versus where it sent the user.
- **`FRICTION.md`**: problems ranked, with a severity scale tied to the purpose (Critical = blocks the path to the purpose; High = costs a real user minutes on a path they must take; Medium = confusing but recoverable; Low = polish). Each: what happens, why it hurts, evidence (screenshot + file:line), severity. Flow, findability, hierarchy, feedback, dead ends, jargon, mobile. Not taste. Add a scan of every visible word against the locked vocabulary.

Counting is the point: "signup → first value = 22 screens, 30 clicks, 5 hunts" is an argument nobody can wave away, and it becomes the before/after the owner can judge. When you cannot reach the thing (no URL, no code, no account), do not pretend: say so at the top, audit from what you were given, mark every inference `[A]`, make access the first item on the needs list, and redo the audit against the real thing before any board is built on it. For a deck, the inventory is slide by slide (claim, what the room must take away, words, seconds), the hunts are the places where the audience has to make the connection themselves, and the count is slides to the ask. For a site, count the paths to the action and the fold at real widths. Templates: `references/templates-audit.md`.

## Phase 3: Audience

Per role: who they are in real life · what they already know and do not (which words are jargon to them) · their vocabulary versus ours · devices and context · **how often they come and how long they stay** · what success is in their own words (quote only where a document holds a quote; otherwise infer and say so). Then **mental models**: the familiar thing they map this onto · where our model breaks it · what the break sounds like. Mark every assumption `[A]`; give every other claim a source path. End with numbered **design principles derived from the audience** (each traceable to a finding) and **open questions only the owner can answer** (list them, recommend a default, do not block on them).

Sources, in this order: everything written about these people (feedback, support mail, sales notes, the owner's own words in past notes), the products they already use (verify claims about those products against their current help pages; one such check found that on a Microsoft 365 work account only an IT admin can approve the add-in, which the product's instructions got wrong), and only then the product's own copy and behaviour, to fill the "Today" column. The researcher never starts from the screens, because the screens carry the maker's assumptions about the user; but the researcher does read them last, and that is where several of the sharpest findings came from (an install card that colleagues invited after the purchase never saw; a post-payment message that skipped the permission step). Visit frequency is the single most consequential number in the whole run; get it right. Template: `references/templates-audience-journey.md`.

## Phase 4: Journey and moments of truth

Walk the whole path in order, from before they arrive to after the value, including the steps that happen in other products. Each moment is a row: **Thinks · Fears · Reassured by · Today** (the last column only when something exists). The fears are what the screens must answer, at that moment, with facts, not comfort. The riskiest moments (from Frame Q5) are where the exploration budget goes. The finish line is the first proof of value, and the design should show it to them ("your first email was sorted at 10:42"), because "did it work?" is the anxiety at the end of every setup.

For a deck, the moments are the arc: why should I listen · do I recognise the problem · do I believe the claim · the proof · the ask · the objections. For a site: source → hero → what is it → price → proof → trust → act → confirmation.

## Phase 5: Jobs and actions

**Jobs ranked**: `# · job · frequency · importance (what breaks if it fails) · today`. Then the ruthless reading: which one or two jobs decide whether there is a customer or a decision at all; which single job is the only reason to come back; everything else lives one level down. **Actions**: every action the thing must support, derived from jobs (new) or counted in the audit (existing), each with who, how often, where it starts, what must be true first, and where it lands afterwards. Two rules fall out of this table every time: related actions live together, and a precondition is a step *inside* the flow, never a detour that leaves the user somewhere else. For a deck, the actions are what the room must understand or decide on each slide, and the ask.

## Phase 6: Explore how expert teams solve the same jobs

From the jobs and the risky moments, derive 5 to 10 **pattern areas**, each a job good teams have solved many times ("buying an add-on inside a product", "setup that finishes in another product", "a home page for someone who comes monthly", "a pricing section", "the proof slide"). Per area, 3 to 6 references; per reference three lines: **Mechanism** (why it works, one sentence) · **Steal** (what transfers, in our words) · **Doesn't fit** (and why: scale, tone, constraint). One **recommended pattern per area**, in our words. Open with the two to four findings that most change the design; close with open questions flagged, not resolved.

Scope is interaction, information architecture, flow and copy structure. Visual style is out of scope whenever a design system is fixed; the library must not restyle you. Use the reference source chosen on the first run (Mobbin or equivalent; look at every image, never metadata alone): real screens are what lift the result above the average of memory. Without one: the products your audience already uses (screenshot them), public help centres and design docs, well-known decks and talks, and your own memory only with the claim marked as memory. Cap it in hours. Research is the comfortable hiding place; decide with cited sources and move. Template: `references/templates-explore.md`.

## Phase 7: Decide, then draw everything side by side

**7a. `DESIGN.md`**, the synthesis, written by the lead who read everything:
- **The one sentence** everything follows from ("nobody reads mail on this site", "the room decides on slide 4").
- **The diagnosis**: why the current thing feels wrong, as mechanisms ("related actions are split across four places"), never as taste.
- **Decisions D1..Dn**, each with what, why (pointing at audit, audience, patterns) and the rejected alternative with the reason it lost.
- **Information architecture**: the places, pages or acts, and what lives where.
- **What the design needs that does not exist yet**: routes, data, capabilities, content, a real help link. Honest, so nothing gets faked on a board.
- **Audit findings that changed the drawing.**

**7b. `SCREENS.md`**, the board spec, so several hands draw one design:
- **Shared fictional data**: a named, plausible company, people, prices, dates, states. Never real customers on a board.
- **Word rules**: the customer's words, one word per thing, the banned words.
- **Visual rules**: the system's own rules restated in ten lines, and what is allowed (buttons are solid dark, one accent use, one big number per surface, touch targets).
- **Rows**: one row per corridor, path or act; every board with a fixed filename, a fixed size and its content in prose.
- **The thinking row**: four boards that show the reasoning next to the screens (who comes · the journey · before → after in numbers · where things live). The owner judges the screens better with the reasoning in view.
- **Board format**: identical head and wrapper for every board; sizes at the medium's real dimensions (desktop 1440 wide, phone 390 × 844, slides 1920 × 1080).

**This skill is the process, not the visual craft.** It decides *what* each screen, page or slide must do; it does not teach typography, colour, layout, contrast, accessibility or component use. When you reach the drawing, let the craft be governed by the design system you were given and by the skills made for it (e.g. `artifact-design`, a design canvas type's own references, `dataviz` for charts). Load them before the first board, and let them win on every visual question this skill does not answer.

**7c. Draw.** The lead draws the **reference board** and the **shared stylesheet** first; drawers take rows in parallel and copy the reference board's head verbatim. Two checks every drawer owns:
- **Truth-check every sentence** on a board against the real system. Mockups lie effortlessly ("we keep the sender, the subject and why" when the why is not stored by default; a person shown in a log they cannot appear in; a VAT number promised on a receipt the payment provider does not print). Each catch is fixed on the board and reported.
- **Verify the system renders**: render one board locally and look. Fonts declared with relative paths fall back silently, and the whole board turns generic without an error.

Two more things the run taught about drawing with several hands:
- **The fictional data must obey the product's own state model.** A drawer noticed that a person listed as "not installed yet" could not appear in the activity log; the lead ruled (who has installed, who is blocked, when the plan was bought) and broadcast the ruling to every drawer it touched. Rulings on shared data are the lead's, they are numbered facts, and they end with "if you already drew otherwise, fix and re-render".
- **Derive, do not copy.** Boards that are variants of another board (a side panel over a page, an upgrade dialog that twins the purchase dialog, a home page with one extra item) are generated from their source board by a small script, and every drawer's script copies the reference head at build time. Revision two then becomes a rerun, not a redraw. When a drawer reports a trap in a shared tool (the render harness read the first `width/height` it found and produced a 1 × 1 image), the lead fixes the tool for everyone.

Then render every board, make a contact sheet, and look at it with your own eyes before anyone else does. A design canvas is optional: a folder of HTML boards plus `scripts/render_boards.mjs` gives you PNGs and a contact sheet; a slide sorter is a deck's board. Templates: `references/templates-design.md`; running drawers in parallel, with the brief, notice, ruling and hand-back shapes as they were actually written: `references/subagents.md`.

## Phase 8: Critique and revise

The board is the owner's gate: it is what they can judge that no text can convey. Collect every comment, then **translate each into a rule for all boards**, never a patch to one. "Many sentences try to have a conversation with the user" became a copy checklist:

*Delete*: sentences that explain the UI · reassurance without a fear at that moment · repetitions of something elsewhere on the screen · legal requirements presented as benefits · counters without an action · "you will come back here" sentences · footnotes that change no decision. *Keep*: the price (with tax wherever money changes hands) · the fact that answers the real fear · at most three short facts at the scary click · status words · the one sentence to try.

**The feeling.** Owners ask for "modern", "elegant", "premium", "like that other site". Define the feeling in words (usually restraint and precision) and reach it only by **subtracting and turning the system's own knobs** (radius, shadow depth, dividers, spacing, type sizes), never by adding effects (glass, blur, gradients, shadows). The previous design chased the feeling by adding and broke the system. Keep a **"before" row** of two or three boards so the owner can compare and say stop. When the owner warns you they may be chasing someone else's feeling and could ruin the work, do not refuse and do not comply blindly: name the feeling, find its mechanism, apply it by subtraction, and show before and after.

How the revision actually ran: the lead wrote the rules first, made the **global changes itself** (the system's knobs, the fonts, the shared classes, every board's head), and only then re-briefed each drawer with four things: the owner's words, what was already done globally, the specific cuts per board, and the same QA and return protocol as before. Drawers checked whether their reference boards had been revised yet before mirroring them, applied the rules directly when they had not, and re-aligned when they landed. **Locked words outrank the copy checklist**: a locked sentence is used verbatim or not at all, and when "fewer words" drops it from the one place it belongs, the lead puts it back. When the owner hands you a mechanism vaguely ("there is a link that opens the dialog pre-filled; the details are in the repo somewhere"), find the source, and write the exact behaviour with its source into the rules and the handoff.

Root-cause visual defects (the fonts) instead of compensating. Run a second truth pass after the rebuild. Ideas that arrive during critique go on a separate page or row; the approved page is not touched. Template: `references/templates-revision-handoff.md`.

## Phase 9: Hand off

`HANDOFF.md` stands alone for a builder who was not in the room: a **kickoff prompt** the owner pastes · **where truth lives** (board, sources, DESIGN, REVISION rules, AUDIENCE, audit, locked words) · the IA in ten lines · **chunks in business-value order**, each ending in something the owner can click (the money path first) · **what the backend, data or producer must provide** (need · today · where, with file:line) · the one novel mechanism spelled out · visual rules · **truths the design rests on** (verify before shipping; never claim beyond them) · the owner's **open calls with build-so-they-don't-block defaults** · blockers to clear before starting. For a deck, the handoff is the outline, speaker notes, data sources and open calls, to whoever produces the file. For a site, page map plus copy plus needs go to the builder, and art direction comes after the structure and words are settled. Template: `references/templates-revision-handoff.md`.

## Rules that made it work

- **Evidence on every claim, `[A]` on every assumption.** Design arguments without paths turn into taste debates.
- **Count, do not opine.** Clicks, screens, hunts, visits per month. Numbers survive the owner's review; adjectives do not.
- **Design for the real visit frequency.** "Understood on first sight" and "efficient once learned" are different products.
- **The next step is one real button where the eye lands.** People who do a thing once will not hunt for it.
- **A flow never sends you away to satisfy a precondition and leaves you there.** Terms, account creation, a login: a step in the same dialog, then straight back.
- **Show the state that matters, per person.** "Paid" is not "works for me"; show both.
- **Answer the fear at the scary click, with facts.** What it can do, what it cannot, what you never store, how to undo.
- **The actor in every sentence is the customer or their own tool.** Your brand name recedes.
- **Words are locked**: one word per thing, a list of banned words, checked on every board.
- **Shared fictional data**, never real customers.
- **Truth-check every sentence against the real system.**
- **Never fake what does not exist**; keep the needs list and hand it over.
- **Verify the fixed things actually work** (fonts, tokens, components).
- **The board is not the product.** It is handed to a builder, in chunks, with tests.
- **Finish each phase's artifact completely before the next.** Half an audience document is worth nothing to the drawer.

## Traps

- **Jumping to UI.** It feels productive and it is how the bad version got built.
- **Style words instead of jobs.** "Modern, clean, Apple-like" describes no user and decides nothing.
- **Daily-use design for three-visit people.** Command palettes, side panels, dense lists and material metaphors for someone who comes once.
- **Flows that send you away** to satisfy a precondition, then forget why you left.
- **Copy that converses instead of informing.** Say the right thing at the right time; the screen is not a chat.
- **Chasing a feeling by adding effects.** Glass and blur are how systems get broken; restraint is how they get elegant.
- **Faking data or capabilities on a board.** The builder will discover it and lose trust in everything else.
- **Trusting that the design system renders.** Look at one board before drawing thirty.
- **Research as a hiding place.** Cap exploration; decide with sources.
- **Letting the reference library overrule the audit.** The explorer will recommend the pattern that looked best; the audit knows which one the users tripped over. The lead decides, with reasons written down.
- **Resolving the owner's tensions silently.** Name them, recommend, queue them.

## When to involve the human

Only for strategic calls, and always by showing something to react to rather than listing options they cannot evaluate. Recommend, with reasons.

- **At the frame**: purpose, in and out of scope, the tools and systems they give you. One message.
- **Questions only they can answer** (who really clicks the buy button, whether a named human belongs on the site, whether two categories or one): list them with a recommended default, proceed, queue them.
- **The visual gate**: the side-by-side board, once, with the thinking row in view. Not screen by screen and not a standing dashboard.
- **Strategic calls only**: scope, money, legal, customer-facing names and claims. Never code, never pixels, never "does this look right to you" on a single component. In the whole run the lead asked the owner nothing mid-run; status went to him in one short paragraph at a time, and every question was queued for the end.
- **Their critique becomes rules; their feeling becomes a mechanism.**
- **The message that presents the board** has a shape that worked: how it was done (four numbered lines) · how to read the board, top to bottom · the decisions waiting, numbered, each with the reason it matters · the things to know (what could not be verified, what does not exist yet, where the files are) · the next step. No questions inside the walkthrough; the questions are their own list.
- **When a new idea arrives during critique**, run this: restate it in your own words · give a recommendation as a starting point for the conversation, not a decision · ask one question back if one thing decides the shape · name the biggest risk · leave the approved board untouched · write their words to a note in the run folder · offer a separate page with two or three variants. That is how "shared team rules across inboxes" became a four-board exploration page instead of a change to the approved design.

## Running it

With subagents, the lead frames, briefs, synthesises, draws the reference board, reviews the contact sheet and writes the handoff; auditor, audience researcher, explorer and parallel drawers do the substantial work, partitioned so no two touch one file. Each agent in the run used roughly 200–350K tokens and 25–50 tool calls over six to eight minutes of wall time; the lead's own context is the scarce resource, which is why the lead reads reports and boards, not code. Read `references/subagents.md` before the first spawn; it holds the brief anatomy, the four mid-run message shapes and the hand-back shape as they were actually written. Alone, do the phases in the same order and write each artifact to disk before starting the next; the folder is your memory, and the caps still apply (exploration in hours). A full run on an existing web app took one long day with a lead and seven agents; a landing page is hours; a deck is half a day.

## References

- `references/tailoring.md`: choosing and sizing the method from the purpose; medium × phase and starting point × phase in full, with worked purpose sentences for an app, a site, a landing page, a deck and a dashboard.
- `references/templates-audience-journey.md`: FRAME, AUDIENCE, JOURNEY and moments of truth, JOBS.
- `references/templates-audit.md`: INVENTORY, ACTION_MAP with counting convention and hunts, FRICTION with the severity scale.
- `references/templates-explore.md`: PATTERNS entries and how to explore without a reference library.
- `references/templates-design.md`: DESIGN decision records, SCREENS board spec, fictional data, board format, the thinking row.
- `references/templates-revision-handoff.md`: REVISION rules, the copy checklist, the elegance rules, HANDOFF.
- `references/subagents.md`: roles, briefs, partitioning, shared stylesheet and reference board, truth-checks, visual QA, return protocol, and how to run alone.
- `scripts/render_boards.mjs`: renders a folder of HTML boards to PNG at their declared sizes and writes a contact sheet (needs Node and Playwright).
