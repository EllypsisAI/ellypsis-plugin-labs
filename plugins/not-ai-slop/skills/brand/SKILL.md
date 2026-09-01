---
name: brand
description: Produces and refreshes design.md — the small file of colour roles, fonts, sizes and don'ts that makes generated visuals look like one particular brand instead of nobody's. Use it whenever someone wants slides, carousels or generated images to look like their brand, asks to pull a brand or design system out of a website URL, a logo, or a brand guide PDF, says the output "doesn't look like us" or "looks generic", wants to change their accent colour or fonts, or has no design.md yet. Run it before composing anything visual — the carousel skill calls it first when design.md is missing.
argument-hint: "[website url | path/to/assets | refresh]"
---

# brand

`design.md` is about 45 lines of literal YAML: five colour roles, two fonts, a pixel scale, three to five don'ts. A composer reads it and maps values straight onto CSS with no taste required. It is the whole difference between a slide made for someone and a slide made for no one.

The schema is fixed and small. **Read `references/schema.md` before writing a file**, and use it as given. If a field seems to be missing, tell the user what you could not express and leave the schema alone — the smallness is the design.

`$ARGUMENTS`: a URL means extract. A file or folder means assets. `refresh`, or nothing, means resolve first and then produce or amend.

## 1. Resolve before you produce

Stop at the first hit:

1. `~~brand` — the brand-custody connector, when one is configured. It hands back the same YAML this skill writes.
2. `design.md` in the working directory, or at the path the user named.
3. Neither — produce one.

Write back through whatever answered: the connector when it is configured and writable, the file otherwise — `design.md` in the working directory when there was nothing to find. The two carry identical YAML. Everything downstream reads the resolved values, never a path.

## 2. Take the path their material allows

| They have | Path | Read |
|---|---|---|
| Only themselves | Five questions, once | `references/interview.md` |
| A website URL | Computed styles → roles → confirm | `references/extraction.md` |
| A logo, brand guide, or deck | Assets, then interview for the gaps | `references/extraction.md`, *From assets* |

Every path degrades to the interview: no `~~fetch`, a page that will not render, a capture that comes back as CMS junk, a logo that turns out to be an icon glyph. Drop to the questions instead of guessing harder.

**Why:** a complete preset beats a half-extracted brand, because the fields hold each other up — `safe_pairs` is only true relative to the palette it was computed against, and a `dont` only means something next to the value it names. Half found and half invented reads worse than honestly borrowed, and it does so without telling anyone.

## 3. Fill every field, and mark what you guessed

Every field gets a value or an explicit `null`; nothing is left blank. The preset in `references/preset.md` supplies whatever the user did not. A substituted font carries `source: fallback:<stack>`, a logo you never saw is `logo.file: null`, and `confidence` is `high` only when the colours and fonts came from the brand's own material.

**Posture:** the drift is quiet confidence — a value that arrived by inference gets recorded as though it arrived by evidence, because the file looks unfinished otherwise and the inference was a good one. A guessed value that is marked guessed stays cheap to correct forever. An unmarked one gets composed, exported and published, and nobody ever finds out which line was the invention.

## 4. Confirm once, in about thirty seconds

Show the accent as hex and in words, both fonts and where each came from, the one `imagery` sentence, and the first don't. Invite corrections in the same message. One exchange, then write the file.

**Why:** extraction reads the site as it is today, and cannot know that the rebrand shipped last month or that the accent belongs to a sub-brand. This is the only place a wrong brand is caught before it is baked into every slide from here on.

## What this skill never asks

- **Anything already in `design.md`.** A refresh touches the fields in question and leaves the rest alone, including their `source` and `confidence`.
- **Layout, type sizes, or positions.** `scale` and `geometry` come from the preset and get nudged by *loud or quiet*. The renderer's constraints are ours to set, not the user's to specify.
- **Permission to continue.** When `carousel` called this, write the file and let the run go on.

The plugin's budget is three questions before the first gate. The interview's five is the one place it is exceeded, and it is exceeded exactly once, because the answers get written down and are never asked again. A sixth question is not available — derive it, default it, or ask it later when the answer actually changes something.
