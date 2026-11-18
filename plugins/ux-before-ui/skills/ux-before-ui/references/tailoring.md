# Tailoring the method from the purpose

*Read this after writing the purpose sentence and before writing `FRAME.md`. It answers "which of the phases matter here, and how much of each". The method is the constant; the size of each step is what you tailor.*

## Contents

1. What the purpose sentence decides
2. The seven sizing questions, in depth
3. Medium × phase, in full
4. Starting point × phase, in full
5. Five worked frames (app, agency site, landing page, investor deck, ops dashboard)
6. Signs you sized it wrong, and mid-run corrections

---

## 1. What the purpose sentence decides

> **[Thing] exists so that [who] can [understand / decide / do X] [when, how often], and we know it worked when [an observable event].**

Each slot steers a phase:

| Slot | Steers | If you cannot fill it |
|---|---|---|
| **who** | Phase 3 (Audience). More than one "who" = more than one corridor and row. | You are designing for yourself. Stop and find out who. |
| **understand / decide / do** | The verb tells you the medium's real job. *Understand* → the deck and the landing page; *decide* → the deck's ask, the pricing page; *do* → the app. Many things mix them; name the dominant one. | The thing has no job and will become a feature list. |
| **when, how often** | Phase 2 depth and the whole design target: once → "understood at first sight"; daily → "efficient once learned". | Assume once. Designing for once and being wrong costs little; the reverse costs the customer. |
| **worked when** | The finish line of the journey (Phase 4), which the design should show to the user. If the event happens somewhere else (in another product, after the meeting), the journey includes that place. | You cannot tell success from silence, and neither can the user. |

## 2. The seven sizing questions, in depth

1. **Is there something already?**
   - *Nothing*: Phase 2 off. Actions are derived from jobs in Phase 5 and drawn as the first journey sketch.
   - *A prototype or MVP*: a quick audit: action map with counts, the chains with hunts, a ten-line friction list. Skip the full inventory.
   - *An existing product*: the full audit first. The action map's counts become the before/after the owner judges by. Do not let the audience research start from the existing screens' assumptions; run the two in parallel and let the synthesis reconcile them.
2. **How often, how long?** Ask for numbers, not adjectives: visits in week one, visits per month after, minutes per visit. If nobody knows, reason it out from the jobs (a person who has exactly one job here comes once). Write the number in `FRAME.md`; every later argument about density, navigation and shortcuts refers to it.
3. **Where does the value happen?** If elsewhere: the journey has a hand-off out and (ideally) a signal back; the design's finish line is the first proof of value shown here; instructions must follow the *other* product's real interface, verified against its current help pages. If here: the finish line is the first completed job.
4. **How many roles?** One row per role on the board. A role that comes once gets a corridor (one column, one next button, no navigation), never the main interface with greyed-out parts. A role that administers gets a "who is ready" view, never a switch that implies everyone is.
5. **The riskiest moment.** Money (the price with tax before the payment provider says it), trust (a login through a third party, a permission), a decision (the ask slide), a first impression (the hero, slide one). The exploration budget goes here; the "before" row on the board comes from here.
6. **What is fixed?** Design system, brand, vocabulary, platform, canvas, reference library. Fixed things reduce Phase 7's freedom and increase its verification duties: render the system once before trusting it; look up the vocabulary before writing copy.
7. **What cannot be true yet?** Data not collected, routes that do not exist, content not written, numbers you do not have, a help link nobody has decided. Open the needs list in `FRAME.md` and carry it through `DESIGN.md` to `HANDOFF.md`. A board that shows a capability that does not exist is a lie the builder will discover.

## 3. Medium × phase, in full

Weights: **S** = an hour or less, a page; **M** = a few hours, several pages; **L** = a session, a substantial document.

### Web app, console, internal tool

| Phase | Becomes | Weight |
|---|---|---|
| Audit | Every screen and state at desktop and phone; every action counted; chains from signup to first value with hunts; friction ranked | L (existing), S (MVP), off (new) |
| Audience | Roles with visit frequency, prior knowledge, vocabulary, devices; mental models vs yours | L |
| Journey | Signup → setup → first value, including steps in other products; return visits as their own journey | M |
| Jobs and actions | Jobs ranked per role; every action with prerequisites and landing place | M |
| Explore | Pattern areas from the jobs (buying inside a product, setup that finishes elsewhere, home for an occasional visitor, activity log, account and billing, navigation, first-run) | M |
| Decide and draw | Corridors and places; every screen and state as a board, desktop + phone rows; thinking row | L |
| Critique | The owner on the board; copy checklist; elegance by subtraction; before row | M |
| Handoff | Chunks by business value (the money path first); backend needs with file:line; truths; open calls | M |

### Website (several pages)

| Phase | Becomes | Weight |
|---|---|---|
| Audit | Pages and states; paths to the action (contact, buy, sign up) with click counts; the fold at 1440 and 390; forms; load time | M |
| Audience | Where visitors come from (search, a post, a referral), what they already believe, what they compare you with; one visit | M |
| Journey | Arrive → recognise ("is this for me?") → understand → price → proof → trust → act → confirmation and what happens after | M |
| Jobs and actions | The three or four things a visitor can do; one job per page, written above the page | S |
| Explore | Hero, what-it-is section, pricing, proof, trust signals, forms, navigation for a small site | M |
| Decide and draw | Page map; every page and every fold as a board, desktop + phone; one row per visitor path (stranger from search, returning, from a specific campaign) | L |
| Critique | On the board; the copy checklist matters most here | M |
| Handoff | Page map, copy, needs (photos, testimonials, legal texts), then art direction as a separate step after structure and words are settled | M |

### Landing page (one page, one action)

| Phase | Becomes | Weight |
|---|---|---|
| Audit | Only if one exists: the fold, the scroll depth to the action, the number of asks | S |
| Audience | One or two segments, by traffic source; what the post or ad promised them | S |
| Journey | The scroll: promise → recognition → proof → objections → the action; the after (thank-you, email) | S |
| Jobs and actions | One job, one action; everything else is a distraction to remove | S |
| Explore | Heroes, proof sections, pricing blocks, forms, in the same category | S–M |
| Decide and draw | The folds as boards in scroll order, desktop + phone; two or three alternates of the hero side by side | M |
| Critique | On the board; be ruthless with copy | S |
| Handoff | Copy, section order, assets needed, tracking events, then art direction | S |

### Slide deck

| Phase | Becomes | Weight |
|---|---|---|
| Audit | Existing deck: slide · claim · what the room must take away · words on slide · seconds; hunts = where the audience must connect the dots themselves; count slides to the ask | S–M |
| Audience | Who is in the room, what they already believe, what they fear (looking foolish, wasting money), who decides, and whether the deck is spoken live or read alone as a PDF (two different decks) | M |
| Journey | The arc: why listen · do I recognise the problem · do I believe the claim · the proof · the ask · objections; where doubt arises and where the decision is actually made | M |
| Jobs and actions | Per slide, the one thing the room must understand or decide (the "so what"); the ask as the deck's action | M |
| Explore | How expert decks do the same jobs: opening, problem framing, the proof slide, the ask; structure references, not template galleries | S–M |
| Decide and draw | The outline as decisions (why this order, which order lost); every slide on one board in reading order; alternates of the key slide beside it; a thinking row (who is in the room, the arc, the ask) | M–L |
| Critique | The owner reads it in order at speaking pace; comments become rules ("less text" becomes a words-per-slide rule for all) | S–M |
| Handoff | Outline, speaker notes, data sources for every number, open calls, to whoever produces the file | S |

### Dashboard or ops view

| Phase | Becomes | Weight |
|---|---|---|
| Audit | Existing views; the questions each answers; what people actually look at (ask them); exports | M |
| Audience | Roles; the questions they arrive with; how often; in what situation (a meeting, a morning check, an incident) | M |
| Journey | The glance → the question → the drill-down → the action taken elsewhere | S |
| Jobs and actions | The questions ranked; per question the decision it feeds; the actions available from the view | M |
| Explore | How expert tools answer the same questions (this is where a charting skill or guideline enters, after the questions are known) | S–M |
| Decide and draw | One board per view and state (empty, loading, incident) per role | M |
| Critique | On the board; "one number per surface" is usually the rule that emerges | S |
| Handoff | Views, data needs per tile, refresh rules | S |

### Anything else (email sequence, kiosk, print, voice)

Derive the four columns from the purpose sentence: the audience is *who*, the journey is *the order they meet it*, the actions are *what they must do or see at each point*, and side by side is *every piece in the order it is met*. Then size with the seven questions.

## 4. Starting point × phase, in full

### Nothing yet

- **Enter at** Frame, then Audience. There is nothing to audit, so borrow evidence: what your audience already uses (audit *that* lightly), and how expert teams solved the same jobs.
- **First board**: the journey sketch, before any screen. Draw the moments in order with the fears next to them; if the owner disagrees here, you have lost an hour instead of a week.
- **Grows**: Audience, Journey, Explore.
- **Shrinks**: Audit (off). Actions come from jobs; count them anyway once drawn (clicks and screens from entry to first value), because the count is what you will compare the built thing against.
- **Trap**: inventing constraints to feel grounded. The needs list is where invented data goes.

### A rough idea

- **Enter at** Frame, then Audience, and sketch the journey early to test the idea. An idea usually depends on two or three moments of truth ("will they give us that permission?", "will they pay before they see it work?"). Find those, explore only those, and draw them first.
- **Grows**: Journey and moments.
- **Shrinks**: Audit (off), Explore (narrowed to the moments the idea depends on).
- **Owner gate**: after the journey sketch, before screens. This is the one time the human sees something before the full board.

### An MVP

- **Enter at** Frame, then a quick audit: action map with counts, the chains with hunts, ten friction lines. Then Audience, which has usually never been done for an MVP; the MVP embodies the maker's assumptions about the audience, so audit and audience run in parallel and are reconciled in `DESIGN.md`.
- **Grows**: Action map, Audience.
- **Shrinks**: Inventory (few screens), Explore (aim it at the top three friction areas).
- **Trap**: keeping the MVP's information architecture because it exists. The audit shows what it costs; the audience shows whether it matches anyone's mental model.

### An existing thing that feels clunky

- **Enter at** Frame, then the **full audit first** (inventory, action map, friction), in parallel with Audience. The owner's complaint ("buying is awful", "the deck loses them on slide 6") is the first friction item; reproduce it click by click and count it.
- **Grows**: Audit, the "before" row on the board, the before/after numbers in the thinking row.
- **Shrinks**: Explore narrows to the top friction areas and the riskiest moment.
- **Owner gate**: the full board with the before row.
- **Trap**: treating the complaint as the scope. The complaint is a symptom; the action map shows the disease (usually: related actions split across places, the state that matters not shown, a flow that sends you away).

## 5. Five worked frames

### A. B2B web console for a mail add-in (an existing thing that feels clunky)

*Sentence:* the console exists so a company owner can buy the add-in for the company and get it sorting each colleague's inbox inside their own mail client within a day; it worked when each person's first email is sorted.
*Sizing:* exists (full audit) · owner 3–6 visits in week one then monthly, colleague once or twice ever · value happens inside another product (the mail client) · three roles (owner, colleague, stranger) · riskiest moments: paying with tax shown honestly, and a permission given through a third-party login · fixed: design system, locked vocabulary, a canvas, a reference library · not yet: per-person "first email sorted" signal, a public page, a help link.
*Plan:* Audit L ∥ Audience L (with journey and jobs inside) → Explore M (8 areas) → DESIGN + SCREENS → 32 boards in 5 rows + thinking row + before row → critique → handoff in 4 chunks, the money path first.

### B. Agency website (existing, four pages)

*Sentence:* the site exists so a prospective client sent by a referral understands what we do, sees we have done it for people like them, and books a call; it worked when a call is booked.
*Sizing:* exists (M audit: paths to "book", the fold) · one visit · value happens on the call, later · two roles (referred prospect, returning client looking for contact details) · riskiest moment: "is this for people like me?" on the home page · fixed: brand · not yet: three case studies written, permission to name clients.
*Plan:* Audit S–M → Audience M (what the referral told them; what they compare with) → Journey S → Explore M (hero, proof, booking) → page map → boards: home, work, about, contact × desktop/phone + a row for the returning client → critique → handoff to builder, then art direction.

### C. Landing page for a booking service (nothing yet)

*Sentence:* the page exists so a homeowner who clicked an ad understands they can book a plumber for a fixed price today and books; it worked when a booking with a time slot is made.
*Sizing:* nothing · one visit, on a phone, in a hurry · value happens when the plumber arrives, days later · one role · riskiest moment: the price and "can I trust this?" · fixed: nothing yet · not yet: real prices per job type, reviews.
*Plan:* Audience S (ad copy decides their expectations) → Journey S (promise → price → trust → slot → confirmation) → Explore S–M (fixed-price service pages, booking flows on phones) → boards: five folds on phone first, desktop second, plus three hero alternates → critique → handoff: copy, sections, tracking, assets; then art direction.

### D. Investor deck (a rough idea)

*Sentence:* the deck exists so four seed investors, live, in twelve minutes, believe the problem is real and this team can win, and agree to a second meeting.
*Sizing:* nothing to audit (a rough outline) · seen once, live; a PDF version read alone afterwards is a second deliverable · value happens after the meeting · one audience with one decider · riskiest moments: slide 2 (do I recognise the problem) and the ask · fixed: brand · not yet: traction numbers for the last month, a named pilot customer.
*Plan:* Audience M (what these four have funded, what they fear) → Journey M (the arc, where doubt arises) → Jobs M (one "so what" per slide) → Explore S (how strong decks open, prove, ask) → outline as decisions → all slides on one board, three alternates of the problem slide → read-through critique at speaking pace → handoff: outline, notes, data sources, open calls, to the deck producer.

### E. Ops dashboard (an MVP)

*Sentence:* the view exists so the on-call operator can see within ten seconds whether anything needs them and what to do first; it worked when the first action after opening is the right one.
*Sizing:* MVP (quick audit: which tiles are looked at) · several times a day, seconds each · value happens in the systems they act on · two roles (operator, manager weekly) · riskiest moment: an incident at 3 a.m. · fixed: the data available, a charting guideline · not yet: a priority signal that combines three sources.
*Plan:* Audit S (ask the two operators what they look at) → Audience M → Jobs M (questions ranked) → Explore S → boards: normal, incident, empty, per role → critique → handoff with data needs per tile.

## 6. Signs you sized it wrong

- **The drawer asks "what does this person actually do here?"** Audience or Jobs was too thin. Stop drawing; answer it; write it down.
- **Two boards show the same action in two places.** Actions were never mapped or the IA decision was not written. Back to `DESIGN.md`.
- **The explorer's document is longer than the audience document.** Research became the hiding place. Cut to the recommended patterns and move.
- **The owner comments on pixels.** They were shown screens without the thinking row, or shown them one at a time. Put the reasoning next to the screens and show the whole board.
- **The builder asks where a number comes from.** The needs list was skipped or a board faked it. Fix the board and the handoff.
- **A role's flow is the main interface with things greyed out.** Frame Q4 was answered "one role" when there were two.
- **Every screen has a help sentence.** The design is compensating for structure with copy. Back to the action map: which precondition is being explained instead of built in?
