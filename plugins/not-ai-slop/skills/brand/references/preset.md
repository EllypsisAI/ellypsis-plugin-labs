# The shipped preset

One preset, two grounds. Take unknown values from here rather than inventing them.

Three fields the preset must not supply unchanged: `brand`, `imagery`, and the first `dont`.

## Dark ground

```yaml
colors:
  canvas:  "#14181D"
  ink:     "#F2F4F6"
  muted:   "#98A2AE"
  accent:  "#E5484D"
  surface: "#1E242B"

safe_pairs:
  - ink on canvas
  - muted on canvas
  - accent on canvas
  - canvas on accent
  - ink on surface
```

## Light ground

```yaml
colors:
  canvas:  "#FFFFFF"
  ink:     "#12161B"
  muted:   "#5B6673"
  accent:  "#C1272D"
  surface: "#F1F3F5"

safe_pairs:
  - ink on canvas
  - muted on canvas
  - accent on canvas
  - canvas on accent
  - ink on surface
```

## Everything else, both grounds

```yaml
fonts:
  display: { family: "Space Grotesk", weight: 700, source: google }
  body:    { family: "Inter",         weight: 400, source: google }
  case: sentence

scale:
  hook: 108
  head: 76
  body: 40
  meta: 26
  pad:  90

geometry:
  radius: 0
  border: none
  shadow: none

logo:
  file: null
  placement: bottom-left
  height: 44

imagery: >
  Plain daylight on ordinary working surfaces. Desaturated, high contrast,
  no people, no lens flare, no stock-photo optimism.

donts:
  - Never a second accent — red is the only chroma in the system.
  - Never Space Grotesk under 700; there is no light display weight here.
  - Never a gradient; every surface is flat.
```

## Already measured

| Pair | Dark | Light |
|---|---|---|
| ink on canvas | 16.2:1 | 18.2:1 |
| muted on canvas | 6.9:1 | 5.8:1 |
| accent on canvas | 4.6:1 | 5.8:1 |
| canvas on accent | 4.6:1 | 5.8:1 |
| ink on surface | 14.2:1 | 16.3:1 |
| ink on accent | 3.6:1 — display only, so it is not listed | 3.1:1 — display only, so it is not listed |

Re-measure the moment a value changes. Nothing here stays true across a swap.

## When you swap the accent

**Step:** measure the user's accent against `canvas` in both directions. If `accent on canvas` clears 4.5:1, list it. If it only clears 3:1, list it with `# display sizes only` on the line. For text sitting on the accent, measure both `ink on accent` and `canvas on accent`, and list whichever is higher — only that one. Then rewrite the first `dont`, which names the accent by colour.

**Why:** the two grounds above carry different reds for exactly this reason — a colour that reads on white is often too dark to sit under white text, and the other way round. A preset colour belongs to nobody, so picking a ground-appropriate value is free. A user's colour is not free: never nudge their hex to make a pair pass. Change which pair is allowed. A brand whose colour is a hair off is a brand that has been quietly overruled, and they will see it before they can name it.

## Three looks to stay out of when you are guessing

1. Cream or off-white ground, a fat soft serif, a terracotta or burnt-orange accent.
2. Near-black ground with a single acid accent — lime, electric violet.
3. Broadsheet hairline rules with tiny letter-spaced caps kickers on everything.

These are the current signature of generated design. The constraint binds only values you *choose*: a brand that genuinely owns one of these keeps it — the file's job is to say whose this is, not whether it is in style.

None of the three go into `donts`. A don't that still makes sense after you swap the brand out is dead weight in a 45-line file; this list constrains your picking, not their brand.
