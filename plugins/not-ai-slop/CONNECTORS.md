# Connectors

Skills never name tools. They use `~~category` placeholders, resolved here.
Every category states what happens when nothing fills it — degraded mode is a
path, not an error.

**No `.mcp.json` ships with this plugin.** All four categories resolve to
capabilities the runtime already has. Nothing to install, nothing to
authenticate.

| Category | Resolves to | Used by |
|----------|-------------|---------|
| `~~imagegen` | The runtime's image generation | `image-prompting` |
| `~~present` | The runtime's native presentation skill | `carousel` |
| `~~brand` | Brand custody, when configured | `brand` |
| `~~fetch` | Web reach for brand extraction | `brand` |

## `~~imagegen`

| Runtime | Resolves to |
|---------|-------------|
| Codex | Built-in `image_gen`, exposed as `$imagegen` |
| ChatGPT | Built-in image generation |
| Claude Code | Nothing native today |

**Degraded:** write the prompts out in full, labelled per image, for the user to
run elsewhere. This is a complete deliverable, not a failure — the prompts are
the hard part.

## `~~present`

| Runtime | Resolves to |
|---------|-------------|
| ChatGPT | The built-in presentation skill |
| Claude Code | **Nothing native.** No presentation or pptx skill ships — verified 2026-08-28 |
| Cowork | Native document creation |
| Codex | The `Presentations` skill, from the `presentations` plugin — installed and enabled by default |

It is a **skill**, not a loose capability. Invoke it by name and let it pick the
rendering — every run that specified a library or approach did worse.

Settled by a controlled test on 2026-08-27: the presentation skill beat every
hand-specified renderer on cover-cropping, scrim, embedded fonts, and gave back
an editable file. **Do not build a renderer.**

**Degraded:** compose as HTML/CSS at a fixed 1080×1350 canvas, absolute px, no
responsive; print to PDF from a browser. The HTML file is then the editable
deliverable. Say which fonts actually loaded and that this was the fallback.

This path needs a real shell and a browser it can drive. It works on a normal
machine and it does **not** work in a hosted sandbox — the controlled test's
HTML run failed for exactly that reason, no Chromium to install. In a sandbox
with no `~~present`, write the spec out and hand it over rather than pretending
to render it.

## `~~brand`

Brand custody may later live in a hosted service. Nothing fills this today.

**Degraded — and this is the normal case:** `design.md` in the working
directory. The local file is both today's v1 and the permanent fallback, so a
hosted service arriving later is a connector change, not a skill rewrite.

## `~~fetch`

Web reach for reading a site's computed styles during brand extraction.
Resolves to whatever browsing or fetching the runtime has.

**Degraded:** the five-question interview. Extraction is the differentiator;
the interview is the thing that cannot fail. Drop to it rather than guessing
harder — a complete preset beats a half-extracted brand.
