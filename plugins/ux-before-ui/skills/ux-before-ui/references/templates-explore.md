# Template: PATTERNS (how expert teams solve the same jobs)

*One explorer. Scope: interaction, information architecture, flow structure and copy structure. Visual style is out of scope whenever a design system is fixed. Look at every image; nothing comes from metadata alone. Cap it in hours.*

## Contents

1. Deriving the pattern areas
2. `PATTERNS.md`
3. With a UI reference library
4. Without a library
5. What the lead does with it

---

## 1. Deriving the pattern areas

A pattern area is a job that good teams have solved many times, phrased so that a search finds it. Derive 5 to 10 from the jobs table and the risky moments:

| Job or moment (yours) | Pattern area (searchable) |
|---|---|
| O1 buy the add-in once for the whole team | buying an add-on inside a product: one dialog, then payment, then return |
| O2 invite the team, see whose inbox is sorting | home for a small-team admin, first time vs returning; per-person readiness |
| M3 install it in their own mail client | setup that finishes in another product; client-specific instructions |
| O4 see that mail is being sorted | activity or audit log for a non-technical owner |
| O5 receipts, cancel | account: billing, members, legal |
| navigation for four places | top navigation that survives a phone |
| S1 understand what it does to their mail before login | an add-in's store page; first-run when the value happens elsewhere |
| deck: slide 2 | framing a problem so the room recognises it |
| landing: the fold | fixed-price service hero with the price visible |

Name the areas so that each maps to at least one board row later.

## 2. `PATTERNS.md`

```markdown
# PATTERNS — how expert teams handle the jobs <thing> does

*Explorer output, <date>. Source: <library / products screenshotted / documents>. <N> searches
(<M> screen searches, <K> flow searches). I looked at every preview image; nothing here comes
from metadata alone. Scope: interaction, IA and flow structure. Visual style is out of scope
because our design system is fixed.*

**Images:** <downloaded to refs/ | not downloadable from here: URLs and a download script in
refs/download.sh; URLs expire <date>; every reference also links to its permanent page>.

Context I checked before writing: <the owner's words (path)>, <two current screenshots (paths)>.

---

## The <two to four> findings that most change <the riskiest job>
1. **<Finding as a rule.>** <Which references show it, and the mechanism in one sentence.>
   <How it applies to us, in our words.> (e.g. "Payment is step 1 of setup, not the end of
   buying. NordVPN, Asana, Cursor and Square show the purchase as an already-ticked row in a
   setup checklist. The return from payment should land on that product's setup card with
   ✓ Paid ticked, not on a thank-you page. A list that starts partly done gets finished.")
2. **<Finding.>** ...
3. **<Finding.>** ...

---

## 1. <Pattern area>
- **[<Product — screen name>](<permanent link>)**. <What is on the screen, factually.>
  *Mechanism:* <why it works, one sentence.>
  *Steal:* <what transfers, phrased in our words and our data.>
  *Doesn't fit:* <what does not, and why: scale, tone, a constraint we have.>
- **[<Product>](<link>)**. ...
- Also seen: <two or three more in one line each, confirming or contradicting>.

**Pattern we recommend:** <One paragraph in our words: the structure, the controls, what the
button says, where the state lives, what happens after. No adjectives.>

## 2. <Pattern area>
...

## Open questions I flag but don't resolve
- **<Checkbox vs "by clicking" sentence.>** <Which references do which; my read; whose call it
  is (legal, product, brand).>
- **<Default access after purchase.>** ...

## Image manifest (`refs/`)
| file | reference |
|---|---|
| a2-trello-tax-line-checkbox | [Trello](<link>) |
```

Per reference, three lines and no more. The *Doesn't fit* line is what keeps the library from restyling you: "132,772 installs last week" does not fit a twelve-person team with forty customers; confetti does not fit B2B; eight developer-tool tabs do not fit an office team.

## 3. With a UI reference library

Mobbin or an equivalent (screen and flow search across real products), used through its tool or its site:

- Search **flows** for multi-step jobs (purchase, onboarding, connect) and **screens** for single moments (a pricing block, an audit log row, a top bar). One phone search for the mobile navigation even when the product is desktop-first.
- Open every preview image. Descriptions and tags are not evidence.
- Record the permanent page link, not the image URL; image URLs expire. If images cannot be downloaded from the current environment (network policy), write the manifest and a download script and say so at the top of the document.
- Prefer products your audience already uses, then products in the same price and trust band, then anything with the mechanism. Say which band each reference is in when it matters.

**Query craft, from the 22 searches that worked.** Describe the *mechanism* you are looking for, not a product name and not an adjective: "modal dialog to confirm subscribing to a paid add-on, showing monthly price, VAT line, total, a checkbox agreeing to terms of service with links, and a continue to payment button"; "setup instructions card with an install link in a copy field, numbered steps to add it in the mail client, and a status indicator waiting for the first sorted email"; "audit log page listing events with who did what and when, filters for member, action type and date range, readable sentence rows". One to three queries per area; flows for anything multi-step; one phone search even for a desktop product, for the navigation. Keep the same task intent on every call. Keep a **running notes file** and append after each search: the permanent page URL, the image URL, and what is on the screen in one line; the document is written from the notes, not from memory. When a search fails with a tool error, retry once with a simpler query. When the images cannot be downloaded from the environment, write the manifest and a download script, say at the top of the document when the URLs expire, and tell the owner exactly where to allow the domain; then look at two current screenshots of the product so the recommendations map onto what exists.

## 4. Without a library

The method does not depend on the library; it depends on looking at real solutions before drawing. Substitutes, in order of value:

1. **The products your audience already uses**, screenshotted by you (their mail client, their chat tool, their payment provider's own checkout, their mail client's add-in settings). These carry the mental models the audience will bring.
2. **Public help centres and design documentation** of those products (setup articles show the real flow step by step, with screenshots; verify against the current version, since interfaces move).
3. **Your own past runs** and their pattern documents.
4. **Well-known decks and talks** for a deck; category leaders' pages for a landing page; competitor sites for a website.
5. **Memory**, last, with the claim marked as memory ("from memory: Trello puts one checkbox above the button; not verified today"). A memory claim that decides a design must be verified before the board is drawn.

The document format is the same. The *Mechanism / Steal / Doesn't fit* discipline matters more without a library, because the temptation to write from taste is higher.

## 5. What the lead does with it

- The explorer recommends; the lead decides, in `DESIGN.md`, with the reason written next to the rejected alternative. The explorer will recommend the pattern that looked best in the library ("keep the frosted pill"); the audit knows which one the users tripped over (text showing through the pill, 10 px labels, no account name). When they conflict, the audit's evidence wins unless the lead can say why not.
- The top findings go into the thinking row on the board (the "before → after" board cites them), so the owner sees where the design came from.
- The open questions join the owner's queue with a recommended default.
- The image manifest and links go into the handoff so the builder can look at the same references.
