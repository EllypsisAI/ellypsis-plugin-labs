# The design.md schema

One file. One YAML frontmatter block. Every value literal — a hex, a pixel number, a family name — so that nothing has to be resolved at runtime by anything. Roughly 45 lines. Use it as given.

## The shape

```yaml
---
brand: Acme Freight                     # names the voice; used in alt text and the footer slide
source: https://acmefreight.com (captured 2026-08-27)
confidence: high                        # high | mixed | asked

colors:                                 # ROLES, not names. The composer maps role to CSS.
  canvas:  "#14181D"                    # slide background; also tells image generation light vs dark
  ink:     "#F2F4F6"                    # primary text on canvas
  muted:   "#98A2AE"                    # secondary text — must clear 4.5:1 on canvas
  accent:  "#E5484D"                    # ONE loud colour: numbers, rules, the one word
  surface: "#1E242B"                    # inset panel or quote card; omit when the brand is flat

safe_pairs:                             # the only combinations the composer may use
  - ink on canvas
  - accent on canvas
  - canvas on accent
  - muted on canvas
  - ink on surface

fonts:
  display: { family: "Space Grotesk", weight: 700, source: google }
  body:    { family: "Inter",         weight: 400, source: google }
  # source: google | file:<path> | fallback:<stack> — fallback means DON'T claim the brand font
  case: sentence                        # sentence | upper | title — a cheap, strong brand tell

scale:                                  # px at 1080x1350. Absolute — no rem, no breakpoints
  hook: 108                             # slide-1 headline
  head: 76                              # body-slide headline
  body: 40                              # minimum legible in-feed; never go under
  meta: 26                              # kicker, slide number, handle
  pad:  90                              # uniform slide margin — the whole spacing system

geometry:
  radius: 0                             # px, or "pill"
  border: none                          # CSS shorthand, or none
  shadow: none                          # none | soft | hard-offset

logo:
  file: assets/logo-white.svg           # a real path, or null — never invent one
  placement: bottom-left
  height: 44

imagery: >                              # the TONE of background images: light, grade, what to keep out.
                                        # Never the subject — that is decided per image, elsewhere.
  Cold overcast daylight. Desaturated, high contrast, no people,
  no lens flare, no stock-photo optimism.

donts:                                  # 3-5, each naming a value this brand actually has
  - Never a second accent — red is the only chroma in the system.
  - Never Space Grotesk under 700; there is no light display weight here.
  - Never a gradient; every surface is flat.
---
```

Values above are illustrative. `source` is one of a URL with its capture date, `interview`, or `assets` — joined with ` + ` when more than one contributed.

## Colours are roles, not names

Five slots, named for the job they do — canvas, ink, muted, accent, surface — one hex in each. Never `brand_blue`, `sea_green`, `primary_2`. Never a sixth slot. `surface` is the only one that may be omitted, and only when the brand has no inset panel.

## safe_pairs is computed, not copied

**Step:** once the palette is fixed, measure contrast for every foreground/background combination you intend to allow. List only the ones at or above 4.5:1. Keep a pair that only clears 3:1 solely for display sizes, and mark it inline: `- accent on canvas   # display sizes only`. Write pairs as `<role> on <role>`. In a light brand the readable pair on accent is usually `canvas on accent`, not `ink on accent` — compute it, don't copy the example.

**Why:** the measuring is mechanical; overruling the brand is not. An agent handed a brand's colours will faithfully reproduce that brand's unreadable pairing, because reproducing it looks like fidelity. Plenty of real brands ship 3.1:1 grey-on-white and get away with it at 16px on a desktop; the same pair at feed size on a phone is a grey rectangle. This is the one place the palette gets overruled, and it gets overruled once so that no slide has to decide it again.

## Fonts carry a source

**Step:** every font records where it comes from. `google` means loadable by name. `file:<path>` means present on disk at that path. `fallback:<stack>` means the brand's real font could not be obtained and this stack is standing in for it. When you substitute, name the substitution in the confirmation rather than only in the file.

**Why:** deciding you can honestly claim a font is the same judgment as `confidence`, and it fails the same way. Licensed CDN fonts appear in a site's computed styles and never download, so the family name is right there, free to copy, and wrong. What follows is slides that miss by a hair everywhere with nothing in the file to explain why, and a client told "here is your brand font" about type they do not own.

## Deliberately not in this file

Component CSS for buttons, cards, nav (a carousel has none) · a spacing scale table (`pad` plus `scale` is the entire rhythm) · an 8-to-12 colour palette (five roles force the hierarchy decision; twelve colours defer it) · a full WCAG matrix (`safe_pairs` is the answer, not the data) · light and dark variants of one brand (pick one `canvas`) · motion, interaction states, breakpoints, responsive anything · a prose "visual theme" section (`imagery` and `donts` carry it in a form a machine can use).

If something genuinely cannot be expressed, say so to the user and leave it out. Every field added here is a field every future brand has to answer for.

## Before you write

- Every hex literal, quoted, six digits. No variables, no design tokens, no `var(--x)`.
- `muted` clears 4.5:1 on `canvas`, and every listed pair has actually been measured.
- Both fonts have a `source`, and nothing claims a font it cannot load.
- `logo.file` is a path that exists, or `null`.
- Three to five `donts`, each naming a value present elsewhere in the file. Swap the brand out and a good don't stops making sense; one that still reads fine is dead weight — cut it.
- `imagery` is one sentence, concrete, and says what to keep out as well as what to show.
  It governs **tone only** — light, grade, exclusions. It must not name a subject, a place,
  or the brand's own working world: a freight brand does not get loading docks here. What
  the picture is *of* is decided per image by the image skill, which requires the subject
  to have no relation to the topic. An `imagery` line that names a scene overrides that
  rule by accident and quietly reintroduces the literal picture.
- The file is self-contained: no relative links to these references, nothing to resolve. It gets pasted into another tool and still works on its own.
