# Image prompting — the construction method

The model is a draftsman, not a designer. All design thinking happens in the prompt; the
model executes a construction brief and you judge the execution.

## Two models, and what each one is for

The door ships exactly two generators. The founder never sees either name, and never sees
a parameter. You choose between them silently, by `kind`:

| | Marks — the default, leave `model` unset | Wordmarks — pass `model: "google/nano-banana-2-lite"` |
|---|---|---|
| Why | Draws marks that look like real logos. That is the whole reason it was chosen | Spells correctly. That is the whole of a wordmark |
| Its flaw | Writes lettering into marks unbidden, and misspells it | Obeys every construction rule and can still come out plain |

Recraft is an illustration model with text in its nature — a badge ring reading
`CORPENGEN COMPORTASSIITY` came out of a brief that said "no text". That trade is taken
knowingly: rule-following is the cheap problem, fixable in prompting, while a mark that
looks like a real logo is something a model either gives you or doesn't. Fixing it in
prompting is what this file is.

The corollary is the wordmark rule. A misspelled wordmark is worth nothing — there is no
iterating your way out of it — so a wordmark goes to the model whose headline strength is
legible text. Pass `model` for `kind: "wordmark"`, always, and say nothing about it.

## The shape of a mark prompt

Six parts, in this order. Lead with the style descriptor: the door never sends a `style`
parameter, so the model is sitting at its photorealistic schema default and the opening
words of the prompt are the only thing overriding it. "Flat vector logo mark" is not
decoration — it is the style control.

> **Flat vector logo mark.** [The construction, geometrically, in one or two sentences.]
> Exactly [N] colors, each rendered as one uniform solid fill of a single unvarying tone
> edge to edge: [names]. Plain white background. [Line discipline, and the one thing it
> must survive.] No text, no letters, no lettering, no wordmark, no badge, no ring, no
> seal, no emblem border, no gradients, no shading, no texture.

**Short beats long.** Specificity about geometry beats specificity about feeling, and a
prompt under a couple of hundred characters holds up as well as a long one. Length buys
nothing here; precision about what the shape *does* buys everything.

**Build one silhouette, never a relation.** This model cannot count parts or reason about
how two shapes meet. Measured 2026-08-28 on these exact prompts: *"two identical
rectangular bars, offset and overlapping, their intersection forming one perfect square"*
came back as four separate diamonds, and *"one continuous unbroken line forms a leaf that
curls inward into a closed circle"* came back as two leaves sitting inside a ring. The same
round's *"one solid amber hexagon with a single curved slot cut clean through it"* held,
twice. So state every construction as **one shape with something cut out of it or added to
it** — a silhouette, not an assembly, and never a count the model has to honour or an
intersection it has to compute.

**Never name the company in a mark prompt.** No name, no sector clause, nothing in
quotation marks. Quotation marks are how this vendor's own guide tells you to *request*
lettering — so "a logo mark for 'Vantage Ledger', reconciliation software" is a text
request wearing a no-text sign, and the bake-off got `VANTAGE LEDGER` set under the mark
for exactly that reason. The mark needs the construction idea; it has never needed the
name. *(Reasoned from the two bake-off rounds and the vendor's quoting convention, not
separately measured — if a live round still comes back with lettering, that is the thing
to say out loud.)*

**Say the exclusions out loud — but only for content.** This model's own guide uses direct
exclusion language throughout its worked examples, and negatives cost nothing on either of
the two models here. They work for things that shouldn't be *in* the picture: end every
mark prompt with the run above, including the form the model reaches for when it smuggles
letters in — **no badge, no ring, no seal, no emblem border.**

They do not work for how the picture is *rendered*. All three marks in the 08-28 round came
back with a soft gradient in a fill that the prompt had explicitly banned; re-running one of
them with the fill stated **positively** — "each rendered as one uniform solid fill of a
single unvarying tone edge to edge" — came back flat. Keep the negative, add the positive;
the positive is the half that holds. *(One re-run, not a study — but it costs nothing and
it is the one rule that decides whether the trace in `/vectorize` is clean.)*

**Never describe a surface.** No matte, glossy, fabric, grainy, brushed, embossed. Material
words pull the render toward photorealism on the way in, and there is nothing for them to
mean on the way out to SVG. Say what the shape does — curls inward, offsets, overlaps,
meets its own stem — never what it is made of.

**Name the background and the exact color count.** "Two flat colors only: deep soil brown
and moss green. Plain white background" holds. "Minimal palette" does not.

**Never set `style` or `colors`.** Both are live on this model and both are traps. The
bake-off followed the vendor's own recommendation — `style: "digital_illustration"` plus
`colors` — and got photographic soil texture and gradients against a brief that banned
both; the round that sent neither produced the flat, weighty marks that won. The palette
belongs in the prompt text, in words.

## The wordmark prompt

Same discipline, three changes: **quote the exact string**, spell it out, and say what
must not appear beside it.

> Flat vector wordmark. The single word "[EXACT STRING]" in capitals, set in a [type
> description], one uniform weight, even optical letter-spacing, on one horizontal
> baseline. Single flat color: [name]. Plain white background. Correct spelling
> [S-P-E-L-L-E-D O-U-T], one line, nothing else in the image. No symbol, no icon, no mark,
> no tagline, no second line, no border, no gradients.

Take the string from the foundation, character for character. Spelling it out letter by
letter is cheap insurance on the one thing that has to be right.

## The prompt outlives the round

Whatever you write is stored with the image, and `/vectorize`'s `text-to-vector` path
hands it **back to a model verbatim** — no style parameters, nothing added, months later,
with nobody around to rewrite it. A prompt built from one geometric construction survives
that. A prompt that describes a scene does not: the 08-27 bake-off handed scene-shaped
mark briefs to Recraft's vector side and got back a man with a building, a compost pile,
and a cartoon tooth on a rainbow. One construction, stated geometrically, is the guard.

## What every prompt decides before generating

1. **Construction grid** — e.g. "constructed on a 12-unit grid".
2. **One stroke weight** — named explicitly, e.g. "a single uniform stroke weight throughout".
3. **Terminals and joins** — flat/rounded terminals, mitred/rounded joins. Pick, state.
4. **Letterfit** — "optical letter-spacing" for wordmarks.
5. **Exactly one subject** — one mark, or one text string. Never both in one image; that
   is what `kind` separates.
6. **Color budget** — two flat colors maximum at this stage, named.
7. **Vectorizable by construction** — flat solid fills, no gradients, texture, shadow or
   3D, plain background. This is what makes the output convertible to real SVG later.
   Non-negotiable, invisible to the founder.
8. **A single graphic element** — "the mark filling most of the frame, no background
   scene, no extra decorative elements".

## Label and note — the two fields the founder actually reads

Each entry in `directions` carries a `label` and a `note` alongside its prompt, and those
are what appear on the card. Write them for the founder, never for the model:

- **`label`** — two or three words naming the idea: "negative space", "one continuous line",
  "the wordmark alone". Not "Direction A", not the archetype's jargon.
- **`note`** — one line of *why this direction exists*, in their language: "the cycle
  closes on itself, like you described the compost route". This is what makes a round
  readable and a reaction meaningful.

The company name lives here, in the founder's own words on the card — not in the prompt.

## Success criteria before, not after

Write the pass/fail list before generating — e.g.: exact spelling; consistent stroke
weight; no artifacts; survives as a favicon at 24px (if an app icon is the first surface).
Judge the output against the list, not against vibes. First generations count — no silent
cherry-picking.

## Known failures — verify, don't assume

Measured 2026-08-28 by running this file's own prompt shape through the live door (five
images, both models), on top of the two bake-off rounds of 08-27 and one earlier model on
08-21. Small numbers: treat these as things to check in the output, not settled facts.

- **Lettering in a mark — did not recur.** Five images, no letters anywhere, including on
  the model that put `VANTAGE LEDGER` and a misspelled badge ring into the bake-off's
  marks. That is the no-name rule plus the exclusion run doing their job on this prompt
  shape, which is the thing the bake-off never tested. If it comes back anyway, see
  `/brainstorm` — it changes which model the next iteration uses, and it gets reported.
- **Relational and counted constructions fail.** Two of two, above. Build one silhouette.
- **Gradients survive a negative.** Three of three. State the fill positively.
- **A banned "ring" still became a circular container.** The exclusion stops a *badge* with
  lettering, not an enclosing circle. If the construction shouldn't sit inside anything,
  say what it sits on instead.
- **Spelling held on the wordmark model.** `ELLYPSIS` came back correct, one line, no
  symbol beside it — the reason wordmarks always pass `model`.
- **Stroke weight across elements** did not hold on the 08-21 model. The rule stands
  regardless: mark and wordmark are always separate generations, and the lockup is
  assembled in SVG later.
- **Fine double-lines and thin overlaps die at small sizes.** If the first surface is an
  app icon, the concept must be bold enough to survive 24px.
- **Output is raster.** It is a sketch. The deliverable comes from `/vectorize`.

## Engineering divergence (round one)

Four to six directions from **deliberately incompatible** style blocks. Vary construction
logic, not adjectives:

| Direction archetype | What changes |
|---------------------|--------------|
| Geometric-modular | strict grid, circles/squares as primitives, mitred joins |
| Organic-continuous | one continuous line, rounded terminals, no grid visible |
| Typographic-only | no mark at all; the wordmark IS the identity, weight does the talking |
| Negative-space | the figure lives in what's left out; solid block + cutout |
| Heavy-reduction | one bold silhouette shape, no line work at all |

Pick the 4–6 that the foundation's adjectives and rejections allow. Two directions the
founder can't tell apart are one direction — merge or replace before generating.

**Then restate each one as a silhouette.** Geometric-modular and organic-continuous are
relational archetypes — "primitives on a grid", "one continuous line" — and those are
exactly the phrasings that came back as four diamonds and two leaves. The archetype is how
you keep the round *divergent*; the prompt still has to name one shape with something cut
from it. Negative-space and heavy-reduction survive the translation unchanged, which is why
they are the safest openers for a first round.

## Iterating after a lock (max three)

Change **one variable per iteration** — weight, or terminal treatment, or proportion.
Never "try again" with the same prompt; identical prompts produce lottery tickets, not
iterations. Re-state the full prompt every time (the model has no memory of the last
generation), with the one change applied. Check every iteration against the rejections in
the taste log before showing it.
