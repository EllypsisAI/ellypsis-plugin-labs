# Composition — what goes where

Read after Gate 1, before writing the spec. Values come from `design.md`; this file
decides how they are arranged. Where more than one treatment exists, all of them are
here — choose per slide, and choose differently across the set.

- [1. Canvas](#1-canvas)
- [2. The eight layouts](#2-the-eight-layouts)
- [3. Rhythm — the set, not the slide](#3-rhythm--the-set-not-the-slide)
- [4. Numeral treatments](#4-numeral-treatments)
- [5. The save slide](#5-the-save-slide)
- [6. Furniture](#6-furniture)
- [7. Type discipline](#7-type-discipline)
- [8. Colour discipline](#8-colour-discipline)
- [9. The background brief](#9-the-background-brief)
- [10. Looks that read as generated](#10-looks-that-read-as-generated)

---

## 1. Canvas

**4:5 portrait, 1080 × 1350. Every slide, no exceptions.** Absolute px throughout: no rem
units, no breakpoints, nothing fluid in the spec.

Margin is `pad` from `design.md`, uniform on all four sides. Type never touches the edge
except where a treatment is deliberately full-bleed.

Platform masters: LinkedIn carousels are PDFs, Instagram takes PNGs. Both come off the
same 1080 × 1350 slides — see `handoff.md`.

## 2. The eight layouts

Same cover, eight layouts. Nothing changes but where the words sit.

Most people redesign the whole cover — new photo, new colours, new fonts — when the cover
was never the problem. The image was fine; the type was in the wrong place. Once a layout
has a name you stop designing and start choosing, and choosing takes about four seconds.

| # | Name | Mechanics | Use when |
|---|------|-----------|----------|
| 01 | **THE STACK** | Everything in one column, bottom left. Type sits low, image breathes above it | Any cover you're not sure about. If you cannot decide, it is this one |
| 02 | **THE BAND** | A solid block of colour across the middle holding all the type. Image above and below | The image is too busy to read over. When the photo will not shut up, stop fighting it |
| 03 | **THE SPLIT** | Image takes one half of the frame, flat colour the other. **All type lives in the colour half** | No clean space anywhere in the image. Stop fighting the photo for room — take half |
| 04 | **THE OVERLAP** | Type sits over the image with intention; contrast carries it | Clean space already exists and you can use it with confidence. Best for anything with a person in it |
| 05 | **THE CORNER** | All type in one corner; the rest of the frame left undisturbed | The image is the hook. Balance and breathing room |
| 06 | **THE LOW LINE** | A thin line of type along the bottom. The image gets the spotlight | The image leads. Subtle does not mean weak |
| 07 | **THE FRAME** | Type sits inside a frame or container box | Busy or dynamic images. Boundaries make things stronger |
| 08 | **THE PUNCH** | The hero word gets huge; everything else gets small | One word carries it. When in doubt, punch it out |

```
Is the image busy / no clean space?
├─ Busy but usable ──────────────▶ 02 BAND  or  07 FRAME
├─ No clean space at all ────────▶ 03 SPLIT
└─ Clean space exists
   ├─ Image is the hook ─────────▶ 05 CORNER  or  06 LOW LINE
   ├─ Person in the image ───────▶ 04 OVERLAP
   ├─ One word carries it ───────▶ 08 PUNCH
   └─ Don't know ────────────────▶ 01 STACK
```

**Read the background brief before running this tree, not after.** Step 5 already told
`image-prompting` where each image keeps its quiet zone, and that promise was made before
this decision existed. The tree picks where the type sits; if it picks a region the brief
reserved for something else, the layout is wrong, not the brief — you cannot unwrite a
background that has already been specified. Check the slide's reserved region first and
let it eliminate branches.

Name the layout in the spec, per slide. A layout chosen by name is auditable; a layout
improvised is not, and the audit in `audit.md` checks for exactly this.

## 3. Rhythm — the set, not the slide

**Vary composition and scale across slides.** Uniform framing reads as a slideshow, and a
slideshow is the failure state — pleasant, consistent, forgettable. Never two identical
treatments in a row.

Rotate the ground:

1. A textured light ground — the dominant surface
2. Near-black with a fine directional texture
3. Full-bleed photograph with type laid over it
4. A flood of one saturated colour
5. A quiet ground, reserved for the summary or filter slide

Alternate density in the same pass: one-word slide → dense slide → image slide → colour
flip. Same energy on every slide reads as one long slide.

**Content bleeds into the next slide's edge** — a fragment of the next image visible at
the boundary. Swipe bait, and it only works if it is deliberate: name the bleed in the
spec with the px offset, or it will not survive the export.

## 4. Numeral treatments

Three, rotated across the set. The choice is part of the rhythm, not a house style.

- **(a) Badge** — a filled circle or starburst holding the numeral, sitting left of a
  large bold title, with an italic subtitle underneath.
- **(b) Giant rotated word-numeral** — `ONE` `TWO` `THREE` set in huge accent type,
  rotated 90°, running down the left edge; the title sits to its right.
- **(c) Rotated tag** — a small accent rounded rectangle, tilted 3–5°, holding the word
  `ONE`…`SIX`, sitting on top of a huge all-caps title word, with an italic subtitle
  line beneath.

Separate from these, **the slide number is always visible** — a small `01`/`4/8` in the
meta size, same position on every slide. That is furniture, not a treatment, and it does
not rotate.

## 5. The save slide

The one slide worth saving on its own. Treatments, in descending order of how usable the
thing on it is:

| Treatment | What it holds |
|-----------|---------------|
| **The object card** | A card styled as the thing itself, so it reads as a ready-to-paste object rather than text on a slide. Rounded corners, its own chrome, the asset set in mono |
| **The framework** | A named structure the reader can hold — a numbered spine, a 2×2, a chain of steps |
| **The fill-in** | A template with blanks. Not a post they read, a thing they use |
| **The quotable** | One line, huge, alone on the slide. The screenshot |

The object card is the strongest when there is a literal asset — a prompt, a snippet, a
checklist. It is also the narrowest: it only works when the thing on the card can be
taken away and used as-is. A card wrapped around a paragraph of advice is a card lying
about what it holds.

## 6. Furniture

What repeats is what they remember. A three-part rail at the top of every slide, small
caps, wide letterspacing, at the meta size:

```
[LEFT]              [CENTER]           [RIGHT]
AUG ©2026           HANDLE             ROLE OR TAGLINE
```

Optional bottom rail: a hairline with the slide index, current one highlighted. It gives
the reader a progress bar and a reason to keep going.

Fill it from `design.md` — `brand`, `logo.file`, `logo.placement`. Never invent a handle,
a tagline, or a logo path; a `null` logo means no logo, not a placeholder.

**The handle test:** cover the handle, screenshot any slide, and ask whether a stranger
would still know whose it is. If the only thing identifying the set is the name on it,
there is a template here but no brand.

Design the rail once, then never change it across the set — and, if the user posts a
series, across the series.

## 7. Type discipline

**Max two font families per slide.** One loud, one quiet, the same two every time.
Contrast is the whole mechanic: a heavy display face next to a plain one does ninety
percent of the work, which is why you never need to collect fonts.

| Role | From `design.md` | Used for |
|------|------------------|----------|
| LOUD | `fonts.display` | The hero word. Headlines |
| QUIET | `fonts.body` | Body, labels, header furniture, meta |

A third style may appear in one restricted role — an italic used exclusively for
subtitles and the signature line. It is not a third family used freely; it is one style
with one job, and if it starts appearing anywhere else it has become a third font.

Sizes come from `scale` in `design.md` — `hook`, `head`, `body`, `meta`. `body` is the
minimum legible size in-feed; never go under it to make a long line fit. Cut the line
instead, or come back to Gate 1.

## 8. Colour discipline

Three roles, from `design.md`: `canvas` carries most of the surface, `ink` is the text,
`accent` appears **once, maybe twice per slide**.

- **Never 50/50.** Base and accent are not equal. Used equally, it stops looking like a
  brand and starts looking like a flag.
- **Nothing at full saturation, and darks are off-black, never pure black.** Cheap is
  maximum saturation; expensive is the same colour pulled back. If `design.md` hands you
  a pure `#000000` canvas, use it — it is the brand's call, not yours — but do not
  generate one.
- **Only `safe_pairs` from `design.md`.** An agent that faithfully reproduces a brand's
  3.1:1 pairing ships unreadable slides; the pair list exists so that cannot happen.
- **Functional colours are functional only.** A red ✗ and a green ✓ on a comparison slide
  are semantics. They are never decoration, and they do not count as a second accent.

## 9. The background brief

`image-prompting` writes the prompts. This is what it gets handed, per slide.

**Backgrounds are mood, not illustration.** The picture does not depict what the slide
says. A brand built on dossiers and files does *not* get backgrounds of dossiers and
files. The image carries atmosphere; the words carry meaning. This is the fix for the
literal-minded failure, and it is the single most common way a slide set announces itself
as generated.

**Slide 1 is a hook picture.** Cinematic, intriguing, good enough to stop a scroll on its
own. It has the least obligation to the topic of any slide in the set.

Hand over, per image:

| Field | Value |
|-------|-------|
| Mood | One sentence, from `imagery` in `design.md` plus the user's one-line answer |
| Light | Warm invites, cold keeps distance. Pick deliberately — it is the fastest dial there is and the one nobody touches |
| Subject | One. Two competing focal points cancel each other out |
| Negative space | Where the type will sit, named by region — pre-planned, not hoped for |
| Grade | Muted, one dominant colour per image, consistent across the set |
| Never | Baked-in text, logos, watermarks, or a depiction of the slide's claim |

**Self-as-subject** only when the user said yes to the second question. It opens
treatments — a period version, an age-shifted version, a stylised version — and it
changes every prompt after it, which is why it is asked once, up front.

Not every slide needs an image. Flat `canvas` slides are part of the rhythm, and a set
where every slide is a photograph has no rhythm left to spend.

Degraded path — no image generation available: write the prompts out for the user to run
elsewhere, and compose against flat `canvas` grounds so the slides ship complete either
way.

## 10. Looks that read as generated

Three combinations are so common in generated work that they now read as the tell,
regardless of how well they are executed:

- Cream ground + soft serif + terracotta accent
- Near-black + one acid accent
- Broadsheet hairlines and thin rules everywhere

None of these are banned. They are banned **as defaults**. If `design.md` specifies cream
and a serif, that is the brand and it ships. If nothing specifies it and it appears
anyway, it arrived because it is the average of everything, which is exactly the thing
this plugin exists to avoid.

The general form of the rule: every visual decision on a slide should be traceable to
`design.md` or to a named layout. Ask what the slide makes the reader feel, then point at
the decision that produced it. If you cannot point at one, you decorated.
