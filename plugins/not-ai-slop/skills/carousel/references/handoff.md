# Handoff — the spec `~~present` receives

This skill does not build a renderer. It writes a spec and hands it to `~~present`, the
runtime's own **presentation skill** — a named skill to invoke, not a rendering approach to
describe. Settled by a controlled test: the presentation skill produced correct
cover-cropping, a subtle scrim, both specified fonts genuinely embedded, an editable file
and a PDF. Every run that specified a renderer did worse.

## The two rules the spec may never break

**Cover-crop, never stretch.** Cover-crop every background image to the frame. Never set
an image's width and height to the frame's dimensions. State the anchor in the spec, so
the sacrificed edge is named — `crop: cover, anchor: top` / `anchor: center` /
`anchor: bottom-left`. Anchor toward the region `image-prompting` was asked to keep clear.

**The editable file is the deliverable.** Ship an editable slide file alongside every
flattened export. Never a PDF alone, never PNGs alone.

## What the spec contains

Per set:

```yaml
canvas: { w: 1080, h: 1350 }
fonts:
  display: { family: "Space Grotesk", weight: 700, source: google }
  body:    { family: "Inter",         weight: 400, source: google }
colors:  { canvas: "#0E1116", ink: "#FFFFFF", muted: "#9AA3AE", accent: "#E4572E" }
scale:   { hook: 108, head: 76, body: 40, meta: 26, pad: 90 }
geometry: { radius: 0, border: none, shadow: none }
furniture:
  top_rail: { left: "AUG ©2026", center: "@handle", right: "<role or tagline>" }
  slide_number: { position: top-right, style: "01", size: meta }
```

Per slide:

```yaml
- n: 1
  layout: 04-OVERLAP
  ground: image
  image: { file: bg-01.png, crop: cover, anchor: center, scrim: "linear, #0E1116 0%→60%, bottom" }
  strings:                    # verbatim from Gate 1 — not re-derived, not re-cased
    - { text: "I took Canva out of the equation.", role: hook, color: ink }
  accent_used: none
  bleed: { next: bg-02.png, edge: right, offset_px: 24 }
```

Field rules:

- `strings` are the Gate 1 strings, character for character. Instruct `~~present` not to
  rewrite, retitle, re-case or otherwise clean up copy.
- Every colour is a literal hex from `design.md`. Never a role name the renderer resolves,
  never a colour the renderer picks.
- `scrim` is named explicitly wherever type sits on an image: a gradient in the canvas
  colour. The type does not move or resize to accommodate it.
- `accent_used` is stated per slide, so the once-or-twice rule is checkable at export.
- `bleed` carries the neighbouring file, the edge and the px offset. Unnamed bleed does not
  survive export.

## Fonts

Name the source for every family: `google`, `file:<path>`, or `fallback:<stack>`. After
export, check what actually rendered. If a font fell back, name the substitute in the
handback note and do not claim the brand font.

## Deliverables

| Artifact | For |
|----------|-----|
| The editable slide file | Opening and changing one thing without an agent |
| A combined PDF | LinkedIn |
| Per-slide PNGs | Instagram and everywhere else |
| A contact sheet | Checking the set at a glance |
| A short note | Which tool built it, what failed and what it fell back to, whether both fonts rendered or were substituted |

## Degraded path — no `~~present`

Compose the slides as HTML/CSS at a fixed 1080 × 1350 canvas: absolute px, no responsive
units, one file per slide or one file with page breaks. Print to PDF from a browser. The
HTML file is then the editable deliverable, with named knobs at the top — a `:root` block
holding the same colours, sizes and padding the spec carried, so a change is one value in
one place.

Say plainly that this is the fallback, and which fonts loaded. The rules above do not
relax here: `background-size: cover` with an explicit `background-position`, never
`width: 100%; height: 100%` on the image; and the HTML ships beside the PDF, not instead
of it.
