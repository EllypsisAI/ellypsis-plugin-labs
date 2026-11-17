# Templates: REVISION rules and HANDOFF

*The owner's critique is the one input the method cannot generate. Turn it into rules for every board, not patches to one; then hand the whole thing to a builder who was not in the room.*

## Contents

1. `REVISION_n.md`
2. The copy checklist
3. "The feeling": restraint and precision
4. Handling the owner's own warning
5. `HANDOFF.md`
6. Variants: website, slide deck

---

## 1. `REVISION_n.md`

```markdown
# REVISION <n> — the owner's <first> reading (<date>)

*Their comments on the board + their message. The lead's translation into rules. Applies to
all boards.*

## What they said
- **"<verbatim>"** → <the rule it becomes, one line>
- **"<verbatim>"** → <root cause found: e.g. "the display and text faces did not load on the
  board at all — the system bundle declares them with relative paths; the boards fell back to
  the system font. Fixed globally with our own font declarations.">
- **<Comment on a specific element>** → <the general rule: "the product's icon is the
  service's own logo; the rules icon is reserved for later team features; placeholders are fine on
  the board">
- **"<A sentence they called unnecessary>"** → delete, and delete its class: <counters
  without an action / legal requirements presented as benefits / lines that can be misread
  as X>
- **<A request to see a state>** → new board `<name>.html`

## <The feeling they asked for> — what it is, in words (lead)
<See §3 below; write it for this product and this system, with the system's actual knobs.>

## Rules for text (checklist per board)
<See §2 below, adapted.>

## <The one new mechanism they pointed at>
<Source, the exact behaviour, the UI for each case, what the builder must verify.>

## What each drawer does
- **Lead:** <rows>, the "before" row, the canvas.
- **Drawer 1:** <boards>. <Specific changes.>
- **Drawer 2:** ...
```

Keep their words verbatim at the top. The translation is yours; the words are theirs, and the next reader (or the next revision) needs both.

**The order of work in the round, as it ran:** (1) write this file; (2) find root causes before taste (render one board and look: were the fonts ever loading?); (3) the lead makes the global changes itself: the system's knobs, the font declarations in every board's head, the shared classes (a logo slot replacing the reserved icon), its own row, and the "Before" row from copies of the old boards with the old stylesheet; (4) re-brief each drawer with the owner's words, what is already done globally ("keep that"), the specific cuts per board with the owner's comment where there was one, and the same QA and return protocol; (5) review the hand-backs, answer the drawers' "please rule" items, put back what the checklist wrongly removed; (6) second truth pass; (7) publish as a new version of the same board.

**Locked words outrank the checklist.** A locked sentence (a glossary line the owner has fixed) is used verbatim or not at all. When "fewer words" removes it from the one place it belongs (the sentence about being sent to the product's login page, at the step where that login appears), the lead puts it back and says so to the owner. Drawers flag every locked line they dropped; the lead decides where "nothing" was wrong.

## 2. The copy checklist

Run it on every board, every revision. It exists because the first version of every screen tries to have a conversation with the user, and screens are not chats: say the right thing at the right time, not many things everywhere.

**Delete:**
- sentences that explain the UI ("click the button below to…")
- reassurance where no fear exists at that moment
- repetitions of something already visible elsewhere on the screen
- legal requirements presented as benefits ("invoice with VAT number" is the law, not a feature)
- counters without an action ("3 plans · 1 for sale now")
- "you will come back here" sentences (the flow does that itself)
- footnotes that do not change a decision
- lines that can be misread in a way that costs you ("everyone in the account gets access" read as "one login for all")

**Keep:**
- the price, with tax wherever money changes hands
- the fact that answers the real fear ("never deletes or sends mail")
- the facts at the scary click, **at most three short lines**
- status words
- the one sentence to try (the first thing to do in the other product)
- the honest expectation ("three logins in three places; that is by design")

**Per board:** heading + at most one line. Per section: at most one help line, and only if it is needed *now* to act.

## 3. "The feeling": restraint and precision

Owners ask for *modern*, *elegant*, *premium*, *clean*, *like that site*. The previous design usually chased it by **adding** (glass, blur, gradients, floating panels) and broke the system's own logic. Define the feeling in words, then reach it only by **subtracting** and by turning the system's own knobs. A version of the rules that worked:

1. **Fewer words.** Heading plus at most one line per screen; one help line per section, only if needed now.
2. **Fewer lines.** Air is the divider. No dashed dividers in the UI (only on raised panels). Rows: a hairline or nothing. Only product cards get the heavy border.
3. **Less mono.** The monospace face only for addresses, identifiers, times, status words, kickers and numbers in tables. Everything else secondary in the text face, muted.
4. **More air.** Sections 72–96 px apart. One focus per screen.
5. **Softer geometry, through the system's knobs**, not new CSS: e.g. radius scale ×1.5 (buttons 12, cards 15, dialogs 18), shadow depth halved, dashed → solid.
6. **Badges and ornaments only where they mean something**: at most one per screen; many screens need none.

Keep two or three boards from before the revision in a **"Before" row** with the previous stylesheet, so the owner can compare side by side and say stop if something old was better.

## 4. Handling the owner's own warning

Sometimes the owner says it themselves: *"tell me if I'm getting too much … I can ruin everything we've made because I want a feeling I get from other people's websites."* Neither refusal nor compliance is right.

- **Name the feeling.** "What you're missing is calm and precision, not effects."
- **Find the mechanism.** What in the admired sites produces it? Almost always: fewer elements, more space, one type scale, consistent geometry.
- **Apply it by subtraction**, with the system's knobs, on every board.
- **Show before and after** in the same row, and say: "the old console chased this by adding and broke the system; this chases it by removing. Here is the version before; say stop if you prefer any of it."
- **Root-cause anything that looked generic** (the fonts) before touching taste.

The answer that was given, for the record: *"You are not too much. The feeling you miss is real, and it can be said in words: calm and precision. The risk you describe arises when one chases the feeling by adding things. That is what the old console did with glass and blur, and it broke the system. So I have only subtracted and turned the design system's own three settings: rounder corners, shadows half as deep, dividers are solid instead of dashed. Nothing new was added."* Followed by the font finding, the list of what changed, the "Before" row, and the three things still open.

**When a new idea arrives during the round** ("in future there will also be shared team rules across inboxes; we must not decide now; we must not harm this canvas"): restate the idea in your own words · give a recommendation as a starting point for the talk, not a decision ("one rulebook per company, personal rules on top") · ask back the one question that decides the shape ("you reserved the rules icon for later team features; are the shared rules those features?") · name the biggest risk ("a shared rulebook for people who never wrote a filter: the word appears once, at the moment it applies, to the person it applies to") · leave the approved board untouched · write their words and your reading to a dated note in the run folder · offer a separate page with two or three variants. When they say yes "provided we are ready for the handoff", the variants go on their own page of the same board, the main page stays as approved, and the handoff says the exploration is not in scope.

**When the owner hands you a mechanism vaguely** ("there is a link that opens the dialog pre-filled; there is information in the repo; I don't know how important it is that you know exactly how it works, as long as the agent that builds it does"): find the source, write the exact behaviour per case with the source path into the revision rules, put it on the boards where it belongs, and carry it into the handoff with what the builder must verify. The vagueness is theirs to have; the precision is yours to supply.

## 5. `HANDOFF.md`

```markdown
# HANDOFF — build <thing> from the board

*For the agent or team that builds it. Written by the lead <date> after <n> revision rounds with
<owner>. Read the whole file before touching code. It stands alone.*

## Kickoff prompt (the owner pastes this into the new session)
> Build <thing>'s front end from the approved design. Everything you need is in
> `<run folder>/HANDOFF.md` — read it first. Start from branch `<branch>`. Work in the chunks
> the handoff describes, maker ≠ tester, and end each chunk with a PR I can click.
> <The business condition: "the pilot customers must be able to buy through the new front.">

## 1. What is being built, and where the truth lives
- **The board (approved direction):** <link>. Source of every board: `<folder>/*.html` +
  `<folder>/shared.css` (a *reference implementation* of the system's components, not code to copy
  blindly). Render one locally: `<command>`.
- **Why each decision:** `DESIGN.md` (D1–Dn + "what the design needs that does not exist").
  **Text and elegance rules:** `REVISION_n.md` — they apply to every screen you build.
- **The people:** `AUDIENCE.md`. **What exists today:** `INVENTORY.md`, `ACTION_MAP.md`,
  `FRICTION.md` + `shots/`.
- **The customer's words (binding):** <glossary path>. New words the design introduces, pending
  the owner's yes: <list>.
- **Not in scope:** <the exploration page, hidden features, parked assets>.
- **The boards' data is fictional** (<company, people>). <Which products are illustrative.>

## 2. The information architecture (D1–D3, R4)
<Ten lines: the bar and its places; who has no places; the object page that replaces the side
panel as a destination; what side panels are still for.>

## 3. Chunks (in this order — <the money path> first, because <business reason>)
1. **<Shell + the money path + setup>** — <boards>. <The one integration detail: "accept +
   checkout in one press: two existing calls in sequence; read `readyToPay` before the click so
   the checkbox appears only when documents are missing".>
2. **<The second role's corridor>** — <boards>. <Deep link from the other product lands here.>
3. **<The returning user's places>** — <boards>.
4. **<Phone + edges>** — <boards>.
Each chunk: branch → PR → the owner's click → merge. A blind tester writes expectations from
the boards before reading the code.

## 4. What the backend / data / producer must provide (from DESIGN.md)
| Need | Today | Where |
|---|---|---|
| success URL → `/<object>/:id?checkout=success` | lands on the billing page | `<file>:<line>` |
| cancel URL → `/<object>/:id?checkout=cancel` | `/billing` | `<file>:<line>` |
| return from third-party login → the step | the billing page | `<file>:<line>` |
| "first email sorted" per person per mail client | data exists (<tables>), no field in /account | `<file>` |
| per-person permission on the team page | roster exists, shown only as a count | `<file>:<lines>` |
| invitation email | not built; fallback = copy link (primary button until invitations send) | <decision ref> |
| sentences per action in the log | static table, <N> actions | new |
| the one novel mechanism | new, client-side | §5 |

## 5. <The one novel mechanism>
<Exact URLs/behaviour per case; the source; what the builder must verify against the real
third-party product; what remains unverified.>

## 6. Visual rules (the system + REVISION n)
- Buttons are solid dark, never accent. Colours only with a word. Cards only for products and prices.
  At most one badge per screen.
- The system's knobs set to: <values>. Dashed lines only on raised panels.
- **Fonts:** the system bundle declares them with relative URLs that do not always resolve —
  serve the font files yourself and verify the display face actually renders.
- **Logo slots:** each third-party product shows *its own* logo; our own get their icon; the
  <reserved icon> is never a product icon. Real logo files must be obtained.

## 7. Truths the design rests on (check them; never claim beyond them)
- <"Tidy never deletes or sends mail on its own (verify in the live permission list before 'cannot delete' goes live).">
- <"The log stores sender, subject and the label it chose by default, not the message body; with 'explain my sorting' switched on it does store a snippet and the reason. Screen text follows the account's actual setting.">
- <"The company's VAT number is not printed on the payment provider's receipt.">
- <"On a Microsoft 365 work account only an IT admin can approve the add-in.">

## 8. The owner's open calls — build so they do not block
| Call | Build like this until they answer |
|---|---|
| <Switch 'explain my sorting' on by default?> | UI shows the reason when present; text follows the setting. Do not touch the default. |
| <Turn off the provider's extra consent tick?> | Unchanged — legal is theirs. |
| <"Inbox" → "Overview"; Team as its own place> | Build as drawn; write it at the top of the PR so they can say no. |
| <Help link for "Ask us"> | A configuration value; no hard-coded link. |

## 9. Before you start
- <Fix the demo defect that blocks exactly the flow being built (file:line).>
- <The capture scripts take the same screenshots again after the redesign: use them for before/after in the PR.>
```

The kickoff prompt is one paragraph the owner pastes without editing. Section 4's "where" column is what makes the handoff buildable without the lead: a need without a file:line is a wish.

## 6. Variants

**Website.** Chunks are pages in the order visitors need them (home and the action page first). Section 4 becomes the assets and content needed (photos, three case studies, testimonials with permission, legal texts, tracking events). Art direction (custom imagery, motion) is a separate step after the structure and copy are approved, briefed with the board and the audience document.

**Slide deck.** The handoff is the outline as a numbered list (title = the claim, the takeaway, the words allowed, the speaker's line), the data source for every number, the alternates that lost and why, the open calls (which pilot customer may be named), and the production notes (aspect, brand, the file format the room needs). It goes to whoever produces the file, with the board attached so they can see the whole arc at once.
