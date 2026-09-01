# Reference: Process-physics prompting

`SKILL.md` carries the thesis, the four corollaries and the three-layer model,
and it is already loaded by the time you are here. This file is the rest of the
method: what the palette and the live text do to a block, and the four
procedures.

## The palette carries the brand

The style block is how the image is *made* — medium, tool physics, tonal
mechanism, substrate, negative prompt. None of that is brand-specific, and it
ships fixed. The palette is what makes an image belong to one brand rather than
another, so it sits in the world block and is populated from `design.md`: the
colour roles there (canvas, ink, muted, accent, surface) become the hex-locked
palette for the set.

Changing those values is a swap, not a re-calibration — no new version slug, no
calibration pass. The style block hasn't moved, which is precisely why one block
serves every brand. What the style block still owns is how many colors the
process allows and where each may go: "max 4 inks, highlights are raw paper" is
physics; `#1A65FF` is not.

With no `design.md` resolved, the block's shipped palette is the fallback — say
that it is one, because a fallback palette is someone else's brand.

## Generated images sit behind live text

Nothing generated here carries a word. Images supply backgrounds and elements;
the text is set live by whatever renders the surface. That changes one thing
about the style block: texture that would be a virtue in a standalone print
becomes noise under a headline. A background carrying live text needs a low-ink
zone — raw paper, an unbroken flat field, a soft area of the gradient — large
enough for the text to sit in, and that zone belongs in the prompt as a
composition instruction, not as a hope. Each block in `style-blocks.md` states
where its text zone comes from under **Legibility**.

The vocabulary for saying so is placement language, and it is written into the
prompt the same way tool physics is: *placement language throughout (top-left,
full-width bottom, center panel, bleeding beyond edges)*. A quiet zone that is
not placed is not prompted.

---

## Procedure 1 — Deriving a style block from reference images

Use when: the aesthetic is new, no existing block covers it. Input: 1–5
reference images (the fewer, the more you must interrogate each). Output: a
frozen style block in the six-part anatomy.

**With no reference images at all:** name a real medium and derive the block from
that medium's documented physical properties instead of from pictures — the seven
questions below are answerable about 35mm colour negative, letterpress or riso from
what the process actually does. Mark the result `⚠ UNCALIBRATED`, the same flag
`style-blocks.md` uses, and say so in the handback. It is a hypothesis that has not
been tested against anything, and the calibration loop still owes it two to four
passes before it can be trusted.

Interrogate the references in this order — these are *questions about
process*, not appearance:

1. **Medium hypothesis.** What machine or hand made this? (Risograph,
   letterpress, screenprint, 35mm film, marker, gouache, CRT capture,
   xerox generation-loss, cel animation...) If unsure, name the two
   candidates and pick by the tonal mechanism (step 3).
2. **Edge quality.** Zoom mentally into any boundary between two colors.
   Crisp die-cut? Fuzzy capillary bleed? Halo of misregistration? Anti-aliased
   digital smoothness (→ your reference may itself be digital-imitating-print;
   still prompt the imitated process)?
3. **Tonal mechanism.** How does the image get from light to dark? Dot size?
   Line density? Solid ink vs. bare paper (no midtones at all)? Layered
   translucent inks? Photographic continuous tone? Declare ONE as exclusive.
4. **Color logic.** Count the actual inks/colors — not the apparent colors
   (overprints create extras). Where is each allowed? Is white "paper showing
   through" or "white ink"? Extract hexes from the reference if possible;
   otherwise name colors in print vocabulary (fluorescent pink, cobalt,
   vermillion) which anchors better than generic names. What you are deriving
   here is the *count and the placement rules* — how many colors the process
   allows and where each one may go. The hex values themselves come from
   `design.md` when one is resolved — see *The palette carries the brand*.
5. **Substrate.** What is it printed/drawn on, and what has time done to it?
   Paper grain, coating, aging, folds, tape, scan artifacts.
6. **Imperfection signature.** The 1–2 flaws that appear in *every*
   reference. These go in the block as mandatory, with magnitudes
   ("misregistered 1–3px", "dry-drag where the marker moved too fast").
7. **Invariants vs. variables.** With multiple references: what repeats in
   all (→ style block), what differs (→ that's the scene slot's freedom;
   explicitly do NOT constrain it).

The process signature from step 6 is not the same thing as a composed
imperfection — an arrow, a torn edge, a piece of tape — and the composed one has
a hard count: *exactly ONE imperfection element per poster (swooping hand-drawn
arrow, misaligned stamp, torn edge, fold crease, tape)*. Two read as a filter.

Then write the block using the six-part anatomy:

```
1. CORE DIRECTIVE   — one line naming the medium ("authentic risograph print")
2. TOOL PHYSICS     — how the tool behaves, with numbers
3. TONAL RULE       — the one allowed tonal mechanism; forbid the rest
4. PALETTE          — max N colors, per-color placement rules; values from design.md
5. SUBSTRATE/TEXTURE— paper, grain, aging, scan quality
6. NEGATIVE PROMPT  — the model's defaults this style forbids, listed explicitly
```

On part 5, aging is a string with a position: *when vintage: add substrate aging
at the end ("warm cream background, heavily distressed, staining, fold creases,
scotch tape corners")*. At the end, because everything before it describes a
fresh print and the aging is what happened to it afterwards.

**Calibrate before freezing (test-diff-patch loop):**
Generate once with a neutral subject (an everyday object — a can, a chair —
never a person, faces hide style errors). Put output beside reference. Name
each delta *in process terms* ("dots too uniform" not "looks too clean";
"registration too perfect" not "too digital"). Patch exactly one block section
per iteration. Two to four loops is normal; if it doesn't converge in five,
your medium hypothesis is wrong — return to step 1. Freeze, version
(`style-block-riso-v3`), and log what each patch fixed.

## Procedure 2 — Using reference images at generation time

Three distinct modes; choosing wrong wastes runs:

- **Image-to-image style transfer** — you already have the *content* (a
  photo, a product shot, a frame) and want it re-rendered. Drop the image +
  the style block as instruction ("Recreate the input image as..."). This is
  the highest-fidelity mode.
- **Reference as style anchor** — you have vibe references but generate new
  content. Attach 1–3 references AND the derived style block; the block does
  the heavy lifting, references resolve ambiguity the text can't carry
  (exact grain frequency, exact palette temperature). Attach references with
  "match the rendering style of the attached images, subject as described";
  where the tool exposes a style-reference parameter, use it with stylisation
  turned down, so the prompt's process language dominates instead of the
  tool's house style.
- **Text-only from frozen block** — production mode once calibrated. Fastest,
  most repeatable, and the only mode that scales across an agent pipeline
  without shipping reference files around.

The two chain, and chaining them beats asking one generation to do both jobs:
generate the flat stamp/label first, then a second image-to-image pass wraps it
onto a real product ("product photo, this design as the label, fridge/table
context"). The flat pass runs under full process control; the second pass only
has to place it.

Rule of thumb: derive with references, produce without them.

## Procedure 3 — Expanding one block into a consistent set

This implements the handoff: approved base prompt + the plan → per-image
prompts → image gen.

1. **Split the approved base prompt** into STYLE BLOCK and WORLD BLOCK if not
   already separated. Everything palette/lighting/character goes to world.
2. **Write character/set sheets inside the world block.** Each recurring
   character or set gets ONE canonical description (clothing, colors by hex,
   distinguishing features, ~30–50 words). This exact text appears verbatim
   in every scene where they appear. Consistency across shots comes from
   verbatim repetition + locked palette, not from hoping the model remembers.
3. **Per-image prompt = STYLE BLOCK ⊕ WORLD BLOCK ⊕ scene slot.** The scene
   slot contains ONLY: subject, composition/camera (from a fixed camera
   vocabulary you define once — e.g. "static wide", "close-up, subject
   right-third").
4. **Set-level variation discipline:** vary shot distance and composition
   across images (wide → medium → close reads as an edited sequence; ten
   medium shots reads as a slideshow), but never vary style/world language.
5. **Batch-generate, then review the set side-by-side** before assembling
   anything. Check: palette identical? Recurring element consistent? Any image
   where style visibly drifted → regenerate that image, same prompt (variance
   is cheaper to fix by re-roll than by re-prompt).

Step 5 is the one an agent gets wrong by instinct: when one image in a set comes
back off-style, the reflex is to edit its prompt, which breaks the verbatim rule
and mutates the set to fix one frame. Re-roll first. Step 2 is the same
machinery `image-idea.md` applies to the self-as-subject case — one sheet, one
person, reused verbatim.

## Procedure 4 — Diagnosis (when output is wrong)

Name the symptom, apply the matching fix. Never shotgun-edit the prompt.

| Symptom | Cause | Fix |
|---|---|---|
| Looks "AI-generic", smooth, stocky | style block is adjectives not physics; or negative prompt missing/weak | rewrite offending section as process constraints; enumerate the model's defaults in the negative prompt |
| Style drifts across a set | slot leakage — style/world text paraphrased per image | restore verbatim blocks; diff the prompts to find the mutation |
| Every output looks the same when it shouldn't | over-frozen — scene-slot freedoms got written into the block | move compositional/subject language back to the slot |
| Reference match plateaus below "close enough" | wrong medium hypothesis | back to Procedure 1 step 1; try the second candidate medium |
| A recurring element changes between images | description paraphrased or too short | canonical 30–50 word sheet, verbatim everywhere, include hexes |
| Text placed on it disappears into the picture | no low-ink zone was prompted; texture is competing across the whole frame | prompt the quiet area explicitly (where it sits, how large); drop dot/grain magnitudes in that zone, not globally |
| The picture illustrates the caption | the slide's subject entered the scene slot as a noun | see `image-idea.md` — the scene slot takes a physical situation, not the topic; rebuild the ban list and pick another candidate |

---

The blocks are the vocabulary. This file is the grammar. An agent that only
copies the blocks has learned nothing; an agent that can run Procedure 1 on
three screenshots of any aesthetic it has never seen — and freeze a block that
holds across a whole set — has the skill.
