---
name: kit
description: Build the brand color palette and typography and assemble the kit document — Brand Kit's final stage. Use when a founder needs colors, fonts, brand guidelines, or the assembled kit for their company's identity — "what fonts/colors should our brand use", "put it all together". Works from the brand foundation and logo assets. Not for styling questions outside a company's brand identity.
---

# Kit — palette, typography, assembly

The last stage: turn a logo plus a foundation into a kit a startup can actually run on — colors with roles, fonts that exist, and one document that keeps every future deck and page consistent.

Journey: `/brand-kit` → `/interview` → `/brainstorm` → `/vectorize` → **`/kit`**.

Load the foundation, the taste log and the direction record first — `core__brand_kit_load`, one call per `kind`, or with no argument for an index of what exists. Honor every rejection in them. If no logo assets exist yet, the kit can still be built around the wordmark string — but say what's missing rather than pretending.

## Palette

Colors get **roles, not just swatches**: background, ink (text), primary, accent — light and dark variants of each. Derive from the foundation's adjectives and the locked mark; respect stated color aversions absolutely. Check real contrast (WCAG AA for text roles) and say the ratios — never claim "accessible" without the numbers. Two to four colors plus neutrals; a startup with nine brand colors has none.

## Typography

Only fonts that exist. Default source is Google Fonts (free, licensable, everywhere) unless the founder brings a license. One face for headings, one for body — or one family doing both jobs through weight. Explain each choice in one sentence tied to the foundation ("geometric sans because you rejected anything soft"), not with invented typographic lore. Never attribute qualities to a font it doesn't have.

## Say the trademark line — once, out loud

When the kit is assembled, say this in the conversation. It is not a footnote and not a disclaimer to bury in the document:

> These marks are generated, not trademark-cleared. Before you register anything or put it on a product, run a trademark search in the classes and countries you actually trade in — that step is yours, and it is the one thing here nobody can do for you.

## Assemble the kit

One kit document, saved through the door with `core__brand_kit_save` and `kind: "kit"`, and handed to the founder as a file. Usable by a human or a machine:

- The logo: the asset files, clear-space rule, minimum size, don'ts (no stretching, no recoloring outside the palette, no busy backgrounds).
- The palette: each role with hex values, light/dark, contrast ratios.
- The typography: families, weights, the heading/body split, where to get them.
- The voice of the visuals: the foundation's three adjectives and the standing rejections — so the next deck is made *against* something, not from memory.
- The trademark line above, in writing as well as said.

A saved document is capped at 60,000 characters — far more than a kit needs. If a save is refused for length, shorten or split it; never retry the same body.

Also give the founder the palette and font imports as a drop-in `tokens.css` — their first surface is usually a website, and paste-ready tokens are worth more there than prose.

The creative work here needs no door tools beyond loading and saving; if the door is down, build from the local `brand/` folder (or ask the founder for their files) and say so.

## After the kit

A full design system — components, tokens in code, applied templates — is the natural next step and a **hand-off, not this plugin's job**: the kit document is written to be the input for Claude's design tooling. Say that plainly, and end: the kit is done, everything future materials need is in it.
