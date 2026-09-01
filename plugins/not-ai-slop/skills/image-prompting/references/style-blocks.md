# Reference: Calibrated style blocks

Worked examples of the six-part anatomy (see `prompt-craft.md`). A and B are
transcribed as written and battle-tested at scale; C is reconstructed and
carries the flag to prove it. They describe **backgrounds and elements only** —
nothing here asks for text inside the image.

Usage: paste a block verbatim as the STYLE BLOCK layer. Swap only the
subject/scene slot. To adapt a block ("keep the exact style tags, change the
subject to X") let an LLM do the swap — never hand-edit the block itself.

Versioning: if a block gets patched, bump the version suffix and note what
the patch fixed. Never patch mid-production.

The palette is the exception to "never hand-edit the block". Each block ships
with a palette, but those values are a **fallback** — when a `design.md` is
resolved, its colour roles (canvas, ink, muted, accent, surface) supply the hexes
instead, in the WORLD block. That is a swap: no new version slug, no calibration
pass. The style block still owns how many colors the process allows and where
each may go; `design.md` owns what they are. See *The palette carries the brand*
in `prompt-craft.md`.

With no `design.md` at all, the formula to fall back on is *cream/white base +
cobalt + one hot accent (vermillion, hot pink, or chartreuse)* — a base, a cold
structural colour and one heat, which is the shape a two-plus-one palette wants
whatever the actual hues turn out to be.

---

## Block A — RISOGRAPH / HALFTONE  `riso-v1`

Best for: full-frame backgrounds with weight, hero imagery behind a headline,
single elements dropped onto a flat field.
Mode: image-to-image (drop content image + this text) or text-only.
Palette: max 4 inks is process, the named inks are the fallback. From
`design.md`: accent and ink take the two heaviest inks, muted and surface the
remaining two, canvas is the raw paper the highlights drop out to.
Legibility: hostile by default — dot size varies across the whole frame, so
local contrast changes everywhere. The block's brightest zones carry zero ink
and read as raw paper — that is the text zone. Say where it is and how big:
"upper-left third stays raw paper, no dots".

```
Recreate the input image as an authentic risograph print. Max 4 ink colors
from classic riso palette: fluorescent pink, red, yellow, teal, cobalt blue,
black, forest green. Highlights are raw off-white paper — no ink. Bold flat
shapes, no photographic detail. Halftone dots on a 45° grid: large (10–18px)
in shadows, medium (5–9px) in midtones, small (1–4px) near highlights, zero
in brightest zones. Dot size is the only tonal tool. Overlapping colors
overprint. Layers misregistered 1–3px. White highlights sprayed and
irregular, never a clean fill. Paper grain, ink speckle, dropout, and scan
softness throughout.

NEGATIVE PROMPT: random dot scatter, uniform dot size, gradients, clean
digital look, perfect registration, more than 4 colors, no paper texture,
watermarks.
```

Anatomy notes (why it works): tonal mechanism declared exclusive ("dot size
is the only tonal tool"); imperfection signature quantified ("misregistered
1–3px"); white defined as *absence of ink*, which kills digital white fills;
negative prompt enumerates exactly the model's defaults.

---

## Block B — HEAVY CHISEL MARKER  `marker-v1`

Best for: spot illustrations, punk-zine energy, "human imperfection" themes.
As a background it works when the black masses are pushed to one side and the
rest is left as negative space.
Palette: black-and-white plus one spot colour is process; `#1A65FF / #FFCD2E /
#FE342C` are the fallback for that spot. From `design.md`: accent is the spot
colour, ink the black masses, canvas the negative space.
Legibility: excellent, but binary. Text sits either in the pure white negative
space or reversed out of a solid black mass — never across the fuzzy edges,
where jagged bleed eats letterforms. Decide which of the two before generating
and prompt the masses to leave that side open.

```
PROMPT: HEAVY CHISEL MARKER. CORE DIRECTIVE: BOLD BLOCKY MARKER ILLUSTRATION.
Render the subject using exclusively an ultra-wide chisel-tip permanent
marker. The style must be heavy, clunky, and aggressive.

STEP 1: THE "HEAVY HAND" TECHNIQUE. Tool Physics: Simulate a marker with a
20mm wide tip. No Fine Lines: Do NOT draw thin outlines. Every stroke must
be thick and massive. Blocky Shapes: Simplify the subject into bold, solid
black shapes. Instead of outlining an arm, draw it as one thick black
stroke. High Contrast: Eliminate all details. Eyes might just be black dots.
Hair is a solid black mass. Imperfection: The edges of the strokes must be
rough and jagged (bleeding ink). Show the "dry drag" texture where the
marker moved too fast and didn't cover the paper 100%.

STEP 2: NAIVE FILLING (NO SHADING). Solid Black: Fill areas completely with
black ink. Do not hatch. Negative Space: Leave the rest pure white. Look: It
should look like a punk-zine graphic or a crude stamp, not a refined drawing.

STEP 3: SINGULAR SPOT COLOR (OPTIONAL). Black & White dominates. Accent: Use
ONE of the strictly defined colors (#1A65FF, #FFCD2E, #FE342C) for a single
element (e.g., a background shape or one clothing item). Style: Apply the
color as a solid, flat block, slightly misaligned with the black contours
(offset printing error look).

STEP 4: TEXTURE. Paper: Rough, absorbent paper texture. The ink edges should
look "fuzzy" (capillary action).

NEGATIVE PROMPT: thin lines, ballpoint pen, sketching, gray shading,
gradients, fine details, realistic proportions, smooth vector edges, clean
art, digital look, cross-hatching, pencil.
```

Anatomy notes: tool physics as a physical spec (20mm tip → minimum stroke
width follows); the imperfection signature ("dry drag") is *named as a
physical phenomenon*, not an effect; spot color misalignment ties even the
accent to a printing-process story.

---

## Block C — CHROME GRADIENT / THERMAL  `chrome-v0` ⚠ UNCALIBRATED

Best for: tech/AI content, modern SaaS-feel slides. Reconstructed from
observation, not a production-tested prompt. Run one test-diff-patch cycle
(`prompt-craft.md`, Procedure 1) before relying on it.
Mode: text-only, or image-to-image over a flat field.
Palette: two hues meeting in one soft gradient is the process; the bracketed
pair is the fallback. From `design.md`: accent and one of muted/surface make the
field, canvas is the quiet area the text sits in.
Legibility: the easiest of the three — the field is soft-focus everywhere, so
almost any part of it takes text. The blob is the one thing that doesn't. Say
which side it sits on, and the negative space the block already asks for becomes
the text zone.
Abridged: the lines that prompted a headline, a subline and an arrow-link
*inside* the image are cut, because nothing here asks for text in the image.
The background they sat on is below, intact.

```
Soft-focus thermal gradient background, blurred iridescent color field
[orange-to-blue / pink-to-teal], heavy 35mm film grain overlay, one glossy
chrome-glass 3D abstract blob floating center-right with iridescent
reflections, shallow depth of field, generous negative space, premium tech
editorial look.

NEGATIVE PROMPT: clutter, more than one 3D object, saturated flat colors,
hard edges in background, stock-photo look, missing grain.
```

Known weakness: "premium tech editorial look" is an adjective, not physics —
exactly the kind of phrase Procedure 1 exists to replace. Candidate process
framing for the calibration pass: "large-format studio photograph of a
blown-glass/chromed object, projected gradient lighting, shot on 35mm film,
push-processed grain."

That last paragraph is the block's own confession, and it is worth more than the
block. A prompt written from inside this method still ended on an adjective,
and the fix is not to soften it — it is to name the photograph that would have
produced the look. Its negative prompt is also the only one in this
library that negates the smooth-3D-render default (`more than one 3D object`,
`hard edges in background`, `stock-photo look`, `missing grain`), which is the
nearest thing there is to what a model produces unprompted for a tech slide.

---

Three blocks is the library, not the method. When none of them fits, run
Procedure 1 in `prompt-craft.md` and derive a fourth — that is the skill these
three are here to teach.
