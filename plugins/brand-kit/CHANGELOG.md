# Changelog

What changed in each release, and why it is better. This file ships inside the plugin and
is published, so it is written for people using Brand Kit — not for its authors. Internal
design notes, and anything about who the tool was built with, belong in the workshop.

## 0.2.2 — 2026-09-01

**No bundled `.mcp.json`.** 0.2.1 shipped one as a short-lived experiment; the plugin's own
documentation said the opposite in three places, so an installer got contradictory
instructions on day one. The connector is added once in **Settings → Connectors**, which is
the path that renders the interactive grid — and reacting to the grid is the product.

Nothing else changed. Version bumped because `plugin update` only re-copies when `version`
changes.

## 0.2.0 — 2026-08-28

Reconciled against the live door. Every skill now calls the tools that actually exist, with
the arguments they actually take.

### What changed in the tools

- **Every call site is `core__brand_kit_*`.** The gateway prefixes backing tools with the
  MCP id; the bare names 0.1.0 used exist nowhere.
- **Eight model-callable tools, not five.** `brand_kit_save` / `brand_kit_load` are the
  storage verbs the skills had been describing without naming, and `brand_kit_round` is new
  (below). A ninth is app-only — the grid's download button — and is deliberately not named
  in any skill.
- **`directions[]` over a bare prompt.** Each direction carries its own `label` and `note`,
  which is what you read on the card. A bare prompt yields "Direction 1…N" and nothing to
  react to.
- **Images arrive as images.** 0.1.0's skills said "returns a viewable URL … render results
  inline". There is nothing to render, and re-describing pictures you are already looking at
  doubles both your reading and the token bill. Both instructions are gone.
- **No Google consent step.** Storage is the door's own. The console link 0.1.0 sent
  first-time users to is gone from onboarding — it cost something before you had seen any
  value.
- **A spend cap ships**: 60 generations and 10 vectorizations per rolling 30 days. Refusals
  come back as finished sentences; the skills relay them and stop, and never quietly shrink
  a round to get under a cap.

### The prompting is the deliverable

The image model changed twice in two days, which settled something: the prompt shape matters
more than the model behind it. What the rewritten `image-prompting.md` does, with five live
generations behind it rather than reasoning alone:

- **Never name the company in a mark prompt.** Quotation marks around a name are how these
  models are *asked* for lettering — a quoted name in a "no text" brief is a text request
  wearing a no-text sign. A mark needs the construction idea; the name lives on the card.
- **Lead with the style descriptor.** No `style` parameter is sent, so the model sits at its
  photorealistic default and the opening words are the only thing overriding it. "Flat vector
  logo mark" is a control, not decoration.
- **Say the exclusions out loud**, and state fills positively. "No gradients" as a negative
  failed 3 of 3; the same prompt with the fill stated positively came back flat.
- **Never set `style` or `colors`.** Following the vendor's own recommendation produced
  photographic texture and gradients against a brief banning both; sending neither produced
  the marks that won.
- **Describe geometry, never surface.** Material words (matte, glossy, fabric) pull the
  render toward photorealism and mean nothing as SVG. This also protects the replay:
  `/vectorize`'s `text-to-vector` path hands your original prompt back verbatim, and scene
  language that survived the generator collapses there.
- **Relational constructions fail** — "two bars whose intersection forms a square" came back
  as four diamonds, 2 of 2. Keep the archetype for divergence, then restate the prompt as one
  silhouette with a cut, which held 2 of 2.

### Wordmarks go to the second model

Which model runs is decided by `kind`, not judgement. **Every wordmark** uses the model with
the stronger lettering, because a misspelled wordmark cannot be iterated into a correct one —
the spelling is the whole artifact. Marks stay on the default and are **never silently
re-rolled**: a skill that judges its own output and generates again spends your allowance on
a problem you may not have minded. When lettering appears in a mark, the next iteration *you
ask for* runs on the other model.

### Never generate to recover

Some hosts stop waiting before a four-image round finishes. You see a transport error and do
the natural thing — generate again. But the images were already made, stored and **charged**,
so the retry pays twice for pictures you already own. `core__brand_kit_round` returns that
round, free, as the same grid. `/brainstorm` carries this as a named section, because it has
to fire in exactly the case where a reference went unread: a missing round, a request for
last session's images, or a result saying images were generated but not stored.

### Vectorizing writes to a fixed path

`/vectorize` writes returned SVGs **only** to `brand/assets/`, under names the skill chooses
(`mark.svg`, `wordmark.svg`, `lockup.svg`) — never a path, filename or extension taken from a
tool result. An SVG opened from disk executes its own script; the door sanitizes what it
stores, and a fixed skill-chosen path is the other half of that guarantee. A truncated SVG is
never written to disk; the stored asset stays whole and the result links it.

### Smaller corrections

- `/vectorize` gained `path: "text-to-vector"` — a native vector redraw from your stored
  prompt, offered when the trace comes back lumpy. Shown alongside the trace, never instead
  of it: only you can say whether the cleaner drawing is still your logo.
- `/kit` states the trademark limitation out loud and writes it into the kit document — the
  image vendor's terms disclaim originality and non-infringement.
- Onboarding reads status instead of asking questions: the document index says where you left
  off, and runs-without-documents means an unlocked brainstorm to recover rather than a fresh
  start.
- A timed-out vectorization that could not be confirmed cancelled **is charged**, and the
  skill says so before offering to retry.
- Saves are versioned and capped; over the cap means shorten or split, never retry the same
  body.

## 0.1.0 — 2026-08-21

First version: a free tool that takes a founder from nothing to a usable visual identity —
interview → brainstorm → vectorize → kit.

### The reasoning that shaped it

- **The interview is the product; the generator is a draftsman.** A capacity test showed the
  model executes a tight construction brief well — correct spelling, true circles, overshoot —
  but every piece of design thinking lived in the prompt, stroke weights did not match across
  elements, and relational instructions were ignored. Hence: mark and wordmark are separate
  generations, the lockup is assembled in SVG, style blocks are vectorizable by construction,
  and success criteria are written before anything is generated.
- **Rejections over preferences.** The taste profile logs what you pushed away and your words
  for why. That is a promptable rule; a list of likes is only a moodboard.
- **Divergence is engineered.** Round one comes from deliberately incompatible style blocks.
  Otherwise you choose between variations of the model's middle, and the choice carries no
  information.
- **Stop rules are law** — at most two divergent rounds, then at most three iterations, then
  back to the interview. Enforced through the deliverable, since a hard stop is a convention
  rather than a mechanism.
- **Locking is explicit.** Ambiguous affirmatives never lock. The word is "lock it".
- **No bring-your-own-key.** Friction before value kills a free tool. The door holds the key;
  you never see a prompt, parameter, or model name. The narrow surface is the product.
- **The design system is a hand-off.** Brand Kit ends at `brand/kit.md`; components and tokens
  go to Claude's design tooling with the kit as input.
- **`/kit` ships `tokens.css`** — paste-ready tokens beat prose for website-first founders.

### Known limits

- **The vector track is unproven end to end.** Nobody has run a locked mark through
  `vectorize` and inspected the anchor points.
- **Application runs** (deck, landing page) are not designed yet. `kit.md` is written to be
  their input.
