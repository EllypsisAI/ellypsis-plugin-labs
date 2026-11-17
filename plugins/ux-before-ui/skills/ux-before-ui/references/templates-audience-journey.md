# Templates: FRAME, AUDIENCE, JOURNEY, JOBS

*Copy the skeletons; keep the section order; delete what the frame says you do not need. Every claim carries a source path; every assumption carries `[A]`. Quote people only where a document holds the quote.*

## Contents

1. `FRAME.md`
2. `AUDIENCE.md` (who, mental models)
3. Journey and moments of truth (a section of AUDIENCE or its own `JOURNEY.md`)
4. Jobs and actions (a section of AUDIENCE or its own `JOBS.md`)
5. Design principles derived from the audience
6. Open questions only the owner can answer
7. Variants: website, landing page, slide deck

---

## 1. `FRAME.md`

```markdown
# FRAME — <thing>, <date>

## The sentence
<Thing> exists so that <who> can <understand / decide / do X> <when, how often>,
and we know it worked when <observable event>.

## Medium and starting point
Medium: <web app | website | landing page | deck | dashboard | other>.
Starting point: <nothing | rough idea | MVP | existing thing that feels wrong>.
The owner's own words for the problem: "<verbatim>" (<source path>).

## Sizing (the seven questions)
1. Exists? <answer> → audit <off | quick | full>
2. How often, how long? <numbers> → design target: <first sight | once learned>
3. Where does the value happen? <here | elsewhere: where> → finish line: <event, shown where>
4. Roles: <list> → corridors/rows: <list>
5. Riskiest moment: <moment> → exploration budget goes here; "before" row from here
6. Fixed: <design system, brand, words, platform, canvas, library> → verify: <what>
7. Cannot be true yet: <list> → needs list opened

## Phases and weights
| Phase | Weight | Who | Artifact |
|---|---|---|---|
| Audit | ... | ... | ... |
| Audience + journey + jobs | ... | ... | ... |
| Explore | ... (areas: ...) | ... | ... |
| Decide and draw | ... (rows: ...) | ... | ... |
| Critique | one gate on the full board | owner | REVISION_1.md |
| Handoff | ... | lead | HANDOFF.md |

## Inputs available
Reference library: <yes/no, which>. Canvas: <yes/no, which>. Design system: <path>. Locked words: <path>.
Existing screenshots / analytics / feedback: <paths>.

## Shared fictional data (for boards)
Company: <name>. People: <names, roles>. Prices, dates, states: <values>.
Never real customers on a board.

## Confirmed with the owner
<date, one line: what they confirmed or changed>
```

## 2. `AUDIENCE.md`

```markdown
# AUDIENCE — who opens <thing>, what they hire it for, what scares them

*<Author>, <date>. No code touched. Read before drawing a screen. Words used as the
customer reads them (<glossary path>). Each claim carries a path. [A] marks an
assumption: reasoned, not evidenced. Quotes only where a document holds them.*

## 0. The one thing to hold onto
<One paragraph: the customer's real errand, in their words, and what follows from it.
Example: "The errand is 'my mail should sort itself the way I would'. It is not 'use us'. The site is a
place people pass through on the way to something that happens elsewhere. Nobody reads mail
here; each visit has to finish in one go.">

## 1. Who
### 1a. <Role A> — <what they do here in five words>
- **Who in real life.** <job, company size, the archetype by name if there is one> (<path>)
- **What they already know.** <products, concepts, words; and what they do NOT know —
  the jargon that must never appear> (<path>)
- **Their vocabulary.** <their words for our things>. Not: <our internal words>.
- **Devices and context.** <laptop at work / phone between meetings / arriving from an email> [A]
- **How often they open it.** <numbers: week one, then per month>. Therefore the design
  target is <understood on first sight | efficient once learned>.
- **Success in their words.** <quote with path, or an inference marked as such>
### 1b. <Role B> ...
### 1c. <Role C> ...
### 1d. Present but not a design target: <the operator / the founder / support>
<Why they are excluded, and the one thing to watch (e.g. "if the founder clicks Buy for
a pilot customer, the payment rail is proven but the owner's journey is not").>

## 2. Mental models: what they map this onto, and where ours breaks theirs
| Role | Familiar model | Where our model breaks it | What the break sounds like [A] |
|---|---|---|---|
| <role> | <"a SaaS add-on an admin installs once"> | <"buying switches it on for the account but works for nobody until each person does their own step"> | <"I've paid, why does it say no access?"> |

**Implication for design.** <What cannot be removed (by design, by law), and what can be
made expected, ordered and visibly finished.>

## 3. Jobs to be done, ranked        (see §4 of this file)
## 4. Moments of truth, walked in order   (see §3 of this file)
## 5. Design principles for this audience  (see §5 of this file)
## 6. Open questions only the owner can answer  (see §6 of this file)

## Copy defects found in passing (for the copy owner, not design decisions)
- <banned word in a visible string, with path>
- <a document name that differs between the screen and the document itself>
```

## 3. Journey and moments of truth

Walk it in the order the person meets it, from before they arrive to after the value. Include steps that happen in other products; mark them (↗). One row per moment.

```markdown
## Moments of truth, walked in order
Columns: what they think → what they fear → what reassures them → what happens today.

| # | Moment | Thinks | Fears | Reassured by | Today |
|---|---|---|---|---|---|
| 1 | Arrive (from <source>) | "Is this the thing X told me about?" | a phishing-looking login; an unknown company | our name and logo on our domain; a company behind it | <what exists, with screenshot + path> |
| 2 | Understand the offer | "What exactly will this do for me?" | vague promises; jargon | three plain lines: what it does, what it can change, what it cannot; one example | ... |
| 3 | Decide | "<price> against <what they pay today>" | commitment; per-seat surprises; lock-in | price per <unit>, no binding, cancel any time, the difference from the free alternative | ... |
| 4 | Pay | "Let me just pay." | the tax surprise; a total that differs; signing something unseen | one dialog: total with tax, the documents as links, one checkbox the first time, then straight to payment | ... |
| 5 | Back from payment | "Done?" | "did it go through, and what now?" | a receipt plus the real next step for this thing | ... |
| 6 | The scary click (a permission, a third-party login) ↗ | "Log in to X through a third party?" | "will it touch or delete my data?", "do you keep my password?", "can I undo this?" | four facts at the button: acts as you; can do only what you can; never deletes or sends mail; password never stored; revoke any time | ... |
| 7 | First proof of value | "It worked." | — | seeing it confirmed here: "your first email was sorted at 10:42" | ... |
| 8 | Month two | "Is it being used? Where is the invoice?" | the tool doing something odd unnoticed; service cut over a card glitch | who did what and why; a proper invoice; a grace period | ... |
```

The "Reassured by" column is the copy brief for that moment; the "Fears" column decides which facts belong next to which button. Facts, not comfort: each reassurance must be true and verified (the "never deletes or sends mail" claim was checked against the live permission list before it went on a board).

## 4. Jobs and actions

```markdown
## Jobs to be done, ranked
Frequency is per <account | visitor | room>. Importance = what breaks if the job fails.

### <Role A>
| # | Job | Frequency | Importance | Today (evidence) |
|---|---|---|---|---|
| A1 | **<verb the thing>** (<the three sub-questions they need answered>) | once | critical: <what breaks> | <screens and clicks today, with path> |
| A2 | ... | once, then per new hire | critical | ... |
| A3 | ... | weekly, then monthly | high: this is the retention argument | ... |
| A4 | ... | rare | medium | ... |

**Ruthless reading.** A1 and A2 happen in week one and decide whether there is a customer
at all. A3 is the only reason to ever come back. Everything else is housekeeping and can
live one level down.

### <Role B>
| # | Job | Frequency | Importance |
|---|---|---|---|
| B1 | ... | once | critical |

**Ruthless reading.** After week one this role has exactly one reason to open it: B4. Their
path should be a single guided corridor, not the main interface with parts greyed out.

## Actions (new thing: derived from the jobs; existing thing: see ACTION_MAP.md)
| # | Action | Who | How often | Starts at | Must be true first | Lands afterwards on |
|---|---|---|---|---|---|---|
| 1 | <action> | <role> | once | <place> | <precondition> | <the thing they were doing, not a list> |
```

Two rules fall out of the table: related actions live together (if three rows share a precondition, they are one flow), and a precondition is a step inside the flow, never a detour that leaves the user somewhere else.

## 5. Design principles derived from the audience

Numbered, each traceable to a finding above. The pattern is *rule → because → therefore on the screen*. Examples that recur across products:

1. **Design for N visits, not for daily use.** Because the owner comes five times in week one and then monthly, and the colleague comes once. Therefore every screen says "what do I do now" to someone who has not learned the model: no shortcut-only paths, no meaning carried by materials.
2. **The next step is always one real button, where the eye lands.** Because people who do a thing once will not hunt for it.
3. **A flow never sends you away to satisfy a precondition and leaves you there.** Because the audit counted what the detour costs.
4. **Separate "the account has paid" from "it works for me", and show both per person.** Because the mental model "bought = on" breaks here.
5. **Money is stated in the local convention, flat, before the payment provider says it.** Because the tax surprise is the fear at the pay moment, and our number and theirs must never disagree.
6. **Answer the data fear at the moment of permission, with facts.** Because that click is the scariest in the product and today one fact sits next to it.
7. **The actor in every sentence is the customer's own tool; our name recedes.** Because each extra appearance of our brand is another brand in a flow that already has three.
8. **Every link from elsewhere lands on the exact fix.** Because a person arriving mid-task should be back within twenty seconds.
9. **Instructions follow the customer's real plan or platform.** Because one instruction for everyone is wrong for half of them.
10. **The finish line is the first proof of value, shown here.** Because "did it work?" is the anxiety at the end of every setup, and the answer is already in our data.

*Tone line at the end: state facts, name the thing, no adjectives selling a feeling.*

## 6. Open questions only the owner can answer

Format: the question, why it matters for the design, the two shapes it could take, your recommended default. Proceed with the default; do not block.

```markdown
1. **Who actually clicks Buy for a pilot customer: the owner, an office manager, or you?**
   If you do, the payment rail is proven but not the owner's journey, and the redesign's
   priority order should follow. Default: design for the owner; you are not a role.
2. **Should the owner come back, or should the site go quiet after setup?**
   Two different front pages. Default: <recommendation and why>.
3. **Does a named human belong on the site?** A contact person is a brand and service
   decision, not a UI detail, and the cheapest trust signal for a stranger. Default: yes,
   as a configuration value, no hard-coded address.
```

## 7. Variants

**Website.** §1 becomes segments by traffic source ("from a referral", "from search for X", "returning client looking for the phone number"), each with what they already believe and what they compare with. §3 is the scroll: arrive → recognise → understand → price → proof → trust → act → after. §4 lists the three or four things a visitor can do and assigns one job per page.

**Landing page.** One segment per traffic source; the ad or post is part of the journey (what it promised is what the fold must confirm). Jobs collapse to one; every other element is a candidate for removal.

**Slide deck.** §1 is who is in the room (what they have funded or bought, what they fear, who decides, whether it is spoken live or read alone). §3 is the arc, one row per beat: *why should I listen · do I recognise the problem · do I believe the claim · the proof · the ask · the objections*, with Thinks / Fears / Reassured by per beat. §4 is one line per slide, "what the room must understand or decide here", and the ask as the deck's action. The visit-frequency question becomes "seen once, live, in N minutes", which decides words per slide.
