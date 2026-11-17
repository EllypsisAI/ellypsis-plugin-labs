# Templates: INVENTORY, ACTION_MAP, FRICTION (the audit of an existing thing)

*One auditor, read-only. Click it, do not read it: every claim gets a screenshot and a code pointer. Count, do not opine. Taste is out of scope; flow, findability, hierarchy, feedback, dead ends, jargon and mobile are in.*

## Contents

1. How to capture (before writing anything)
2. `INVENTORY.md`
3. `ACTION_MAP.md` (counting convention, the table, the dependency graph, the chains with hunts)
4. `FRICTION.md` (severity scale, item format, the navigation section, the word scan)
5. Variants: website, slide deck

---

## 1. How to capture

- **Real viewports.** Desktop (1440 × 900) and phone (390 × 844 @2x, touch). Phone shots and every shot with a panel or dialog open are *viewport* shots (what the eye gets), followed by `-p2`, `-p3` when the page scrolls further. A full-page capture on a phone paints a fixed bottom bar in the middle of the page, which lies.
- **Every state.** First visit and returning; empty, first-run, error, expired, failed payment, the member role and the admin role, the 401/404/412/500 answers. States the demo cannot produce can be played at the network layer (rewrite the API answer; validate it against the real schema so you are still looking at the real UI).
- **Name shots by number and meaning**: `31-buy-4-412-bounce-to-account-desk.webp`. Dump the visible text of every shot alongside, so words can be grepped later.
- **Scripts, not hands**, when there are more than a dozen shots: a small Playwright script per scenario, re-runnable after the redesign for before/after.
- **Separate defects of the demo or environment from defects of the product.** Both matter; they go in different lists.

**The rig that produced 181 shots in an afternoon**, for reuse:
- Read the demo's README and scripts fully first; then start **one instance per fixture shape** on its own port (a four-person paying account, a solo owner who bought and never installed, a first-run account with nothing bought, no account at all, the same shapes with the legal step pending, the same with mail on and with mail failing). Eight instances covered every state the product has.
- A shared library: a browser context per viewport with locale and timezone set; a `returning` flag that seeds the product's "last visit" storage so the returning-user state appears; a `shot()` that waits for network idle, takes a viewport shot, pages the scroll container (`-p2`, `-p3`) when the page or the open panel scrolls further, and **dumps the visible text of every shot to a file** so the word scan is a grep later; a `rewriteAccount()` that intercepts the account API and answers with a modified payload for states the demo cannot produce (the member role, a broken permission, a failed payment, the 412 on checkout, 401/404/500), **validated against the product's real response schema** before it is served, so the UI in the shot is the real UI and only the wire answer was supplied; an `asMember` rewrite.
- One numbered script per scenario (`s1` the main account, `s2` the other shapes, `s3` the purchase flow, `s4` the played states, `s6` the entry screens, `s7` the checkout return, `s8` extras) plus a restart helper, because scripts mutate the in-memory demos and must run against fresh instances in order.
- When a shot looks wrong (a fixed bar painted mid-page), fix the rig, delete the shots, rerun; do not annotate around it.
- Where the product's own demo breaks the flow (accepting terms broke the demo's account validator), answer that one endpoint in the browser and say so in the inventory's defect list.
- Before handing back: **re-verify every `file:line` citation by grep** and fix the ones that moved (string files shift as you read them); copy the scripts into the run folder with paths made relative; kill the instances; report the size of the screenshot set and let the owner decide whether it is committed (39 MB of PNG became 7 MB of WebP).
- Say plainly what could not be reached (the external login, the payment provider, the third-party OAuth, the mail client) and that those were described from code.

## 2. `INVENTORY.md`

```markdown
# SCREEN_INVENTORY — <thing> as it stands, <date>

*Every screen, panel, dialog and full-screen state, what it shows in order of visual
weight, what you can do there, and the screenshots. Flow analysis is in ACTION_MAP.md;
problems are ranked in FRICTION.md. Nothing in product code was changed.*

## How the screenshots were made
- Source: <demo / staging / production account>, <fixtures or accounts used>
- Viewports: <as above>
- States played at the network layer: <list, marked [net] below>
- Scripts: <path>

### Demo/environment defects found while capturing (not product defects)
1. <what breaks, where (file:line), what it blocks>

## 0. The shell (on every place)
**File:** <path:lines>
### 0.1 Top navigation — desktop
- **What you see, by weight:** <the elements in the order the eye meets them, with sizes>
- **Behaviour:** <sticky? translucent? badges? what it signals and what it does not>
- **Actions:** <what you can do from here>
- **Shots:** <files>
### 0.2 Navigation — phone
### 0.3 Banners that appear everywhere

## 1. <Place / page>
### 1.1 <State: returning owner>
- **File:** <path:lines>
- **What you see, by weight:** ...
- **Behaviour:** ...
- **Actions:** ...
- **Shots:** ...
### 1.2 <State: first visit>
...
## N. Panels and dialogs
## N+1. Full-screen states (not found, no account, expired link, past due)
```

## 3. `ACTION_MAP.md`

```markdown
# ACTION_MAP — every action <thing> supports, and the order a user is forced through

*Auditor's map, <date>. Click paths were clicked unless marked "code" (read, not clicked)
or "external" (outside the product).*

**Counting convention.** **C** = clicks/taps (typing not counted; ticking a box counts).
**S** = screen changes: a route change, a panel opening, a dialog opening, or a page
outside the product. Paths start from the most natural starting point and include the
navigation click to get there. Roles: <list, with the code that defines them>.

## 1. The table
### A. <Group: getting in and the account>
| # | Action | Who | How often | Starts at | Exact click path | C / S | Prerequisites | Dead-ends / bounces | Code |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Sign up and create the account | owner-to-be | once | <url> | <step → step → step> | 3 / 3 | none | <where it drops you without a next step> | <path:lines> |
| A2 | Join from an invitation | invitee | once | mail | ... | 2+login / 4 | valid token | lands on the home page with no personal setup guide | ... |
### B. <Group: money>
| B1 | **Buy — terms already accepted** | owner | once per product | any | ... | 5 / 5 | ... | after paying you land on the billing page, not the product | ... |
| B2 | **Buy — first time (terms pending)** | owner | once | any | ... | **12 before payment** / **8 before payment** | ... | bounce to another page; accept does not resume; the toast points to a Terms section that does not exist | ... |
### C. <Group: setup>
### D. <Group: seeing what happened>
### E. <Group: personal>
| E3 | Get help | anyone | — | — | **Not possible from the UI.** "Ask us" appears four times with no link (grep for a help link → nothing) | — | ... |

## 2. The dependency graph (what must be true before what)
Read top to bottom; every arrow is enforced somewhere, and the right column says who enforces it.
```
account ─────────────────────────── session (401 → login)
  └─ organisation exists ────────── /account 404 → /start
      └─ role = owner ──────────── every write below is owner-gated
          └─ terms accepted ────── 412 BEFORE payment
              └─ paid ──────────── (+ VAT number required, + the payment provider's own terms tick)
                  └─ switched on ── automatic after purchase
                      ├─ [per PERSON] permission given ── gate: org entitled
                      └─ [per PERSON] installed in their own mail client
                            └─ first email sorted
```
<Note which nodes are per person, not per account, and whether the product's only
checklist is per account (it usually is).>

## 3. Dependency chains — the real order, screen by screen
Legend: **[S]** a screen change · **⟂ HUNT** a place where the product leaves the user to
find the next step themselves.

### Chain 1 — a new customer, signup → first value
| # | Screen | What the user does | C | Notes |
|---|---|---|---|---|
| 1 | Login (external) **[S]** | sign up | 2 | |
| 2 | /start **[S]** | company name, **Create** | 1 | shot |
| 7 | Billing page **[S]** (thrown there by a 412 + toast) | ⟂ **HUNT** — the toast points to a Terms section that does not exist; tick 3 documents | 3 | shots |
| 8 | Billing page | **Approve and continue** → the box disappears; nothing else | 1 | ⟂ **HUNT** |
| ... |
**Totals: ≈ 22 screens (14 inside, ≥ 8 outside), ≈ 30 clicks, 5 hunts.** Steps 6–10 exist
only because <the precondition is a detour instead of a line in the dialog>; the hunts at
12 and 15 exist because the two returns from external services land on a page that is not
the thing being set up.

### Chain 2 — the same customer, second purchase
### Chain 3 — an invited colleague, link → first value
### Chain 4 — <a product that needs no permission>

### Where each hunt could have been a handoff (observation, not design)
| Hunt | What the product already knew at that moment | Where it sends you instead |
|---|---|---|
| after the 412 | which documents are missing (in the refusal and in /account before the click) | the billing page, with a toast pointing to a non-existent section |
| after paying | the purchased item names | billing page, banner text without a link |
| a new colleague | that this person has no permission and no install | home page with no card |
```

The totals line is the sentence the owner will repeat. Make it exact and make it reproducible.

## 4. `FRICTION.md`

```markdown
# FRICTION — what gets in the user's way, ranked

*Auditor's list, <date>. Flow, findability, hierarchy, feedback, dead ends, jargon and
mobile — not visual taste. Each item: what happens, why it hurts, evidence (screenshot +
file:line), severity.*

Severity: **Critical** = blocks or nearly blocks the path to <the purpose: a paying,
working customer> · **High** = costs a real user minutes or a support mail on a path they
must take · **Medium** = confusing or wasteful, but recoverable · **Low** = polish,
wording, edge states.

## The ranking
### 1. <The owner's complaint, reproduced click for click> — **Critical**
<One paragraph: what happens.> **12 clicks and 8 screen changes before payment**
(ACTION_MAP B2), against 3 and 3 when the precondition is already met.
- <Mechanism 1, with path: e.g. "the product knows before the first click that the
  request will be refused (`readyToPay: false` in /account) and nothing reads it">
- <Mechanism 2: "the button says 'Approve and continue' and does not continue anything">
- <Mechanism 3: "the payment provider then asks for the same consent again">
- <Phone-specific: "the jump lands scrolled mid-page, the heading above the fold">
- Evidence: <shots in order>

### 2. <There is no primary button — the call to action is 12 px text, and one act has three names> — **High**
### 3. <Every return from outside lands somewhere other than the thing you were doing> — **High**
### 4. <"Does it work?" ignores the state that matters, and the setup guide is per account instead of per person> — **High**
### 5. <The setup order is scattered across three places with three vocabularies> — **High**
### 6. <A link leads to a page that cannot answer the question> — **High**
### 7. <Phone: panels are full-screen under a floating dock; the primary button is a screen away> — **High**
### 8. <One page is a drawer for everything, including a step of the purchase> — **Medium**
### 9. <Dead ends with no way to reach a human> — **Medium**
### 10. <Empty states teach steps that cannot be taken yet> — **Medium**
### 11. <Failures say what, never why or what to do> — **Medium**
### 12. <A toggle reads as an instruction, not a state> — **Low**
### 13. <Engineering leaks onto the surface (raw identifiers, "URL", "checked now" with no check)> — **Low**

## The navigation — what it is, how it behaves, where it hurts
<Desktop and phone, with sizes and behaviour; what it signals and what it does not
(setup debt? a pending legal step? the account name? help?).>

## W. Vocabulary violations and tensions (against <glossary path>)
Scanned over the text of all <N> screenshots plus <string file>.
| # | Where the user sees it | Word | Rule | Evidence |
|---|---|---|---|---|
| W1 | not-found screen | "<banned word>" | <rule> | <shot; path> |
Checked and clean: <list>. Dead strings still carrying banned words (not rendered): <list>.
```

## 5. Variants

**Website.** Inventory: every page and state at both widths, with the fold marked. Action map: every path to the action (contact, book, buy, sign up, download) with clicks and screen changes from the home page and from a deep link; forms field by field. Chains: "from search for X → booked" and "returning client → phone number". Friction: the same scale with Critical = blocks the action.

**Slide deck.** Inventory: one row per slide: number · title · the claim · what the room must take away · words on the slide · seconds when spoken · the shot. Action map: slides to the ask; per beat of the arc, which slides serve it; "hunts" = places where the audience must make a connection the deck does not make for them (a chart with no stated takeaway, a jump from problem to product with no bridge). Friction: Critical = the room loses the thread or the ask is unclear; High = a slide that says two things; Medium = text nobody can read at the back; Low = inconsistency.
