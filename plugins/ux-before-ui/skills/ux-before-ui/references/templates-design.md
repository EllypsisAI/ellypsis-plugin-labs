# Templates: DESIGN (decisions), SCREENS (board spec), boards and the thinking row

*The lead writes both documents after reading everything. `DESIGN.md` is the argument; `SCREENS.md` is the instruction that lets several hands draw one design. Boards come after both.*

## Contents

1. `DESIGN.md`
2. `SCREENS.md`
3. Shared fictional data
4. Board format (HTML boards, sizes, the head, the render script)
5. The thinking row
6. Visual QA before anyone else sees it
7. Variants: website, landing page, slide deck

---

## 1. `DESIGN.md`

```markdown
# DESIGN — <thing> drawn from scratch (lead synthesis, <date>)

*Builds on AUDIENCE.md (who, jobs, fears), PATTERNS.md (<N> searches), ACTION_MAP.md +
FRICTION.md (what exists today). Customer words: <glossary path>. Design system: <name>.
Board: <link or folder>.*

## The one sentence
**<The thing everything follows from.>** e.g. "Nobody reads mail on this site. The owner comes
3–6 times in week one and then monthly; the colleague comes once. It is a place you pass
through on the way to something that happens elsewhere. Therefore it is drawn as corridors
with one next button, not as a dashboard to be learned."

## Why the current one feels wrong (the diagnosis, not taste)
1. **Actions that belong together are split apart.** <Where each piece lives today.> The
   customer assembles the chain themselves.
2. **The state that matters is not shown.** <"On" is a green dot; "does it work for me and
   for each of my people?" is nowhere.>
3. **It is designed for daily use** (<the daily-use features>) by people who come three times.
4. **The system is used as skin, not as logic.** <Where the design system's own rules were
   broken for effect.>

## The decisions
### D1 — <Title as a claim: "Three corridors, four places">
<What, in three lines.> Reason: <AUDIENCE §, FRICTION #, PATTERNS §>. Rejected: <the
alternative> because <the reason it lost>.
### D2 — <"The top bar is the system's own tab bar, full width, solid">
Reason: FRICTION shows text through the frosted pill, 10 px labels, no account name; the
system's README says not to stack frosted layers. Rejected: keep the frosted pill (PATTERNS §7
recommended it) because the audit's evidence outweighs the library's aesthetics.
### D3 — <"'Inbox' is called 'Overview'"> *(a proposal; the owner's name from v4, not decided)*
### D4 ... Dn

## The principles that governed the drawing (from AUDIENCE §5)
1. ... 10.

## What the design needs that does not exist today (honest, so nothing gets faked)
- `<route>` as a route, and the payment provider's success URL pointing there (today: billing page)
- "First email sorted" per person per mail client: data exists (<table>), no field in <endpoint>
- Sentences per action in the log: a static table in the client; no API
- Accept + checkout in one press: two existing calls in sequence; no new route
- A public page without login: `<json>` exists; the page does not
- <a real help link>: today "Ask us" appears four times with no link
- **<A truth the boards must respect>**: <e.g. "the reason is NOT stored by default;
  only 'explain my sorting' keeps it, with a snippet; the boards show it as it looks when the account has turned it on">

## Findings from the audit that changed the drawing
- <finding> → <decision it changed>
```

The "needs" list is the most valuable section for the builder and the easiest to skip. Every item is a promise the boards make that the system cannot keep yet; the boards must show it as *it will look*, labelled in the spec as needing X, and never as a pretend capability.

## 2. `SCREENS.md`

```markdown
# SCREENS — every board, with its content (lead, <date>)

*Specification for the drawers. Decisions and reasons are in DESIGN.md (read D1–Dn first).
Customer words: <glossary path> — binding. Reference board: `A1-<name>.html`; shared
stylesheet: `shared.css` (use its classes; invent no new colours or shadows).*

## Shared, fictional data (use exactly these — no real customers on a board)
- Company: **<Name Ltd>**. Owner: **<Name>** (<initials>, <email>). Colleagues: **<Name>**,
  **<Name>**, **<Name>**. Invited, not accepted: **<Name>** (sent 3 days ago).
- Products: **<Product>** (<price>/month ex. tax, per company) · **<Product>** ("coming soon").
- The address / the key string: `<value>`.
- Today: <weekday date>. Bought <date>. Next payment <date>. Price lines: <net · tax · total>.
- Team state (returning owner): <Name> ✓ ✓, last email sorted today 10:42 · <Name> ✓ ✓ · <Name> ✗
  missing permission · <Name> ✓ permission, not installed yet.
- Log: default stores sender, subject and label only — **never the message body** in sentences. Sentences:
  "<Name>'s inbox filed an invoice from <Sender> under Bills", ... Label chips: `<label_id>`, ... The reason (owners
  only) is the add-in's own words, e.g. *"Sender is a supplier; the subject mentions an invoice due Friday."*
- This week: **38 emails sorted** for 3 people.

## Words (a selection of the glossary — look up the rest)
<one word per thing> · **Never outward:** <banned words>. Button labels from §<x>: "<label>" ·
"<label>". The actor is **the customer's own tool** ("so your inbox sorts itself the way
you would"), never the product.

## Visual rules (the system, excerpt)
Buttons are **solid dark**, never accent. Accent only for links, badges, focus. Green/yellow/red
only with a word. Cards only for products and prices. One raised panel per page. One big
number per surface. Display face only for short, tall things. Mono for metadata, chips,
status. Corners 8 px, labels 12 px. No emoji, no icon packs. Touch targets ≥ 44 px.

## The rows
Sizes: desktop **1440 wide** (height by content: 900–1400), phone **390 × 844**. Filenames are fixed.

### Row A — <The owner buys and gets started> *(lead draws)*
- `A1-plans.html` — Plans, nothing bought ✅ (reference board)
- `A2-buy.html` — the buy dialog, first time (checkbox)
- `A3-return-permission.html` — back from payment: the product's page, ✓ Paid, step
  "Give permission" open
- ...

### Row B — <The colleague> *(drawer 1)*
Bar: quiet variant (no places). One narrow column (720).
- `B1-invitation.html` — before login. "<Owner> has invited you to <Company>." What it gives:
  "<one sentence>". Honest expectation: "About 3 minutes. You log in in three places: here,
  in <Microsoft or Google> and in <Outlook or Gmail> — that is by design." Primary button: **Continue**. Under: "Wrong
  person? Just close the page." Raised panel: the invitation as a short letter, not a card.
- `B2-corridor-permission.html` — after login. h1 "TWO STEPS AND YOU'RE READY". Step 1 open
  with the four facts (`.ui-facts`): *acts as you — can see what you can, no more* / *never
  deletes or sends mail* / *you log in at <Microsoft or Google>; we never see your password* / *revoke any time*.
  Button **Log in with <Microsoft or Google>**. Step 2 closed. Side note: "about 1 min".
- ...

### Row C — <The owner returns> *(drawer 2: C1–C4 · drawer 3: C5–C8)*
### Row D — <First time and edges> *(drawer 4)*
### Row E — <Phone 390 × 844> *(drawer 1)*

## Board format (for the drawers)
Copy the head and wrapper from the reference board **verbatim**. Root:
`<div class="ui" style="width: Wpx; height: Hpx;">` with the same W/H declared for the canvas.
Close every element, quote every attribute, no template expressions. Real `<button>`,
`<a href>`, `<input>` + `<label>`. No emoji, no SVG icon packs, no iframes.
```

Each board line is content in prose: what the heading says, which step is open, which facts sit at which button, what the status words are. The drawer's job is to render it in the system, not to invent the content.

## 3. Shared fictional data

- One plausible company with a name that could not be a real customer; three to five people with initials that do not collide; one product for sale and one or two "coming soon".
- Numbers that add up (net + tax = total; dates in order; "38 emails sorted for 3 people" matches the rows shown).
- Two moments in time when the design has them (row A is the first purchase on day one; row C is months later), stated so drawers do not mix them.
- Log sentences never contain the customer's data if the product does not store it by default; the fictional data must respect the account's real storage setting.
- Placeholders for third-party logos are marked as placeholders; the real product uses the service's own brand material.
- **The fictional data must obey the product's state model.** The first spec listed a colleague as "permission given, not installed yet" and, three lines later, had his inbox appear in the activity log. A drawer caught it; the lead ruled (none of that person's mail is sorted; the third person in the log is the one who installed the add-in but is blocked until an IT admin approves it; the returning owner bought in March, not today; here is the team state) and sent the ruling to every drawer it touched. Write the state of every person and every object once, check that every sentence in the data is possible in that state, and expect drawers to check it again.

## 4. Board format

A board is one HTML file, self-contained apart from a shared stylesheet and fonts. Works with any canvas that takes HTML, and without a canvas at all.

- **Identical head** on every board (the reference board's), so fonts, tokens and the stylesheet load the same way everywhere. Drawers copy it; a format check compares it.
- **Explicit size on the root** (`style="width: 1440px; height: 1160px;"`), also declared wherever the canvas expects it, so the render is exact and the canvas layout is predictable.
- **The shared stylesheet** is a reference implementation of the design system's tokens and components (`shared.css`): every colour, radius, shadow, type size comes from the system's tokens; drawers use its classes and invent nothing.
- **Fonts served locally** or from an origin you control. Fonts declared with relative paths inside a design-system bundle can fail silently on the canvas; the boards fall back to the system font and the whole design looks generic. Declare your own `@font-face` with absolute URLs and verify one render before drawing thirty.
- **Real elements** (`button`, `a`, `input`, `label`), because the builder will read the board as intent.
- **Render**: `node scripts/render_boards.mjs boards/ --out preview/` screenshots every board at its declared size, writes `preview/contact-sheet.html`, and prints a `!! font not loaded` flag for any declared font that fell back (the silent failure that makes a whole board look generic). Needs Node and Playwright (`npm i playwright` + a Chromium; set `PW_CHROMIUM=/path/to/chrome` if Playwright's own browser is missing). Without Playwright: open each board in a browser at the declared width and screenshot it, and check the fonts in the inspector.
- **Format check** (a 30-line script pays for itself with more than one drawer): balanced tags, quoted attributes, the head identical to the reference, no forbidden content (iframes, inline SVG packs, emoji, template braces), root size equal to the declared size, a title.
- **Derive dependent boards by script.** A panel over a page is generated from the page board; an upgrade dialog from the purchase dialog; a home page with one extra item from the home page; the public pricing page from the owner's plans page. Every drawer's generator copies the reference board's head, helmet and bar from disk at build time. Then a change to the reference or to the page underneath is a rerun, not a redraw, and twins cannot drift. In the run this is what made revision two take one turn per drawer.
- **The harness trap.** A render script that takes the viewport from the first `width: Npx; height: Npx` it finds anywhere in the file will pick up a small element's CSS rule written in that order and produce a 1 × 1 or 20 × 20 image. Anchor the size detection on the root (or a `data-size` attribute), as `scripts/render_boards.mjs` does; when a drawer reports a trap like this, fix the shared tool for everyone rather than letting each drawer work around it.

## 5. The thinking row

Four boards that sit above the screen rows on the same canvas, so the owner sees the reasoning next to the screens and comments on the design instead of the pixels:

- **R1 — Who comes.** The roles, their visit frequency, their one job each, the one sentence. (From AUDIENCE §0–2.)
- **R2 — The journey.** The moments in order, with the fear and the answer at each, including the steps in other products. (From AUDIENCE §4.)
- **R3 — Before → after, in numbers.** Signup → first value: 22 screens → 13, 30 clicks → 17, 5 hunts → 0; the three top friction items and what replaced them. (From ACTION_MAP and DESIGN.) For a new thing: the target counts.
- **R4 — Where things live.** The information architecture: places, what each holds, which role sees which. (From DESIGN D1–D3.)

Each row of screens also gets a short note beside it (what this row is, which references it draws on), so a stranger can read the board top to bottom.

## 6. Visual QA before anyone else sees it

1. Render every board locally; look at every PNG, not a sample. Fonts, alignment, overflow, a button that fell off the bottom of a phone board.
2. Contact sheet per row; compare siblings: same bar, same spacing, same status words, same fictional data.
3. Truth pass: read every sentence on every board against `DESIGN.md`'s needs list and the real system. Fix on the board; note the catch in the run log.
4. Word pass: grep the boards for the banned words and for each locked term's forbidden synonyms.
5. Format check by script.
6. Publish once, in rows, at real sizes, with the thinking row and the notes. Republish as versions, never as a new board, so the owner's comments stay attached.

## 7. Variants

**Website.** Boards per page and per fold in scroll order; a horizontal rule on the board marks the fold at 900 (desktop) and 844 (phone). Rows per visitor path. The thinking row's R3 shows scroll depth to the action and the number of asks per page, before and after.

**Landing page.** One row: the folds in order at phone width first, then desktop; a second row with two or three hero alternates; R2 is the scroll journey with the objection each fold answers.

**Slide deck.** Boards at 1920 × 1080 in reading order in one row (or one row per act); alternates of the key slide in a second row; the thinking row is who is in the room · the arc with the beat each slide serves · the ask. `SCREENS.md` gives per slide: the claim as the title, what the room must take away, the words allowed on the slide, the speaker's line. A slide sorter view in the deck tool is an acceptable board if all slides fit on one screen; otherwise render to PNG and make the contact sheet.
