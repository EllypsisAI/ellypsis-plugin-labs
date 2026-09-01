# Extracting a brand from a URL or from assets

## Reach

Reach the page with `~~fetch`. What you get back decides how far this can go:

| Reach | What you can read | Best confidence |
|---|---|---|
| Shell plus a headless browser | Computed styles on the rendered page, loaded font files, screenshots | `high` |
| Fetch-and-read only | HTML, inline styles, `<meta name="theme-color">`, `og:image` | `mixed` |
| No web reach | Nothing | Run the interview |

Say which one you had. A `high` claimed off a fetch-and-read is the same lie as an unmarked guessed hex.

## Read computed styles, never source CSS

**Step:** read the values the browser resolved for elements that actually painted on the rendered page. Do not read stylesheets, `:root` variable blocks, or a theme's CSS file.

**Why:** source CSS is the easier read and it answers the wrong question. A stylesheet ships every rule the theme could ever apply, including the CMS's own admin UI; computed styles are the subset a visitor actually saw.

## Pick roles by function, never by appearance

| Role | How it is chosen |
|---|---|
| `canvas` | the colour covering the largest painted background area |
| `ink` | the most-used text colour whose luminance differs from `canvas` by at least 64 |
| `muted` | the next most-used text colour that still clears 4.5:1 on `canvas`; if the site has none, mix `ink` toward `canvas` until it clears, and mark `confidence: mixed` |
| `accent` | the most-used interactive background — buttons, active states, filled links — with real chroma, above about 40 |
| `surface` | the second-largest painted background, when it differs from `canvas` by more than a hair; otherwise omit the field |

**Why:** chosen by appearance, the winner is whatever is most saturated, and an unstyled `<a>` at `#0000EE` beats a real brand accent on saturation alone. Frequency and function are what make a colour a brand's. Purity is what makes it an accident.

## Expect the junk — it is the normal case

Measured on one ordinary WordPress/Elementor site:

| Signal | What came back |
|---|---|
| CSS variables | 33 total, 21 of them `--wp-admin-*`, none of them brand |
| Font families | 7; four were icon fonts, two were real, one was a case-duplicate |
| Colours | the brand red present twice as two near-identical hexes, plus three CMS admin blues |
| Logo detection | 18 hits, 18 false positives — every one a Font Awesome glyph |
| Most-used text colour | a mid grey |

So filter before you pick anything:

- **Ban user-agent defaults** — `#0000EE`, `#0000FF`, `#551A8B`, `#EE0000`, `#000080`. An unstyled link is not a brand colour.
- **Drop CMS and framework variables** by prefix: `--wp-*`, `--bs-*`, `--elementor-*`, `--tw-*`, `--mui-*`.
- **Drop icon families** — anything matching `Font Awesome*`, `*-icons`, `Material Icons`, `swiper-icons`, single-letter families like `lg`, and any family used only inside `::before` content.
- **Merge near-identical hexes.** Within about 3 per channel is one colour typed twice. Keep the more-used one.
- **Merge case-duplicate families.** `montserrat` and `Montserrat` are one font.
- **Distrust logo detection completely.** Ask for the logo file, or write `logo.file: null`.

## Fonts you can see but cannot have

Cross-check every family in the computed styles against the font files that actually downloaded. A family that is used but absent from the loaded files is a licensed CDN font — Söhne, GT Walsheim, Graphik and their kind. Write the substitute as `source: fallback:<stack>` and name the substitution out loud in the confirmation.

## Confirm, then write

Show the accent as hex and in words, both fonts and where each came from, the one `imagery` sentence, and the first don't. Ask for corrections in the same message. This is the gate where a rebrand, a sub-brand's accent, or a two-year-old site gets caught — see SKILL.md step 4. Then write the file.

## From assets

| Asset | What it gives | What it does not |
|---|---|---|
| Logo SVG | exact brand hexes in the `fill` values, and often the display family outright | anything about `canvas` — light or dark still has to be asked |
| Logo PNG or JPG | a sampled hex — take it from a solid interior area, never an anti-aliased edge | precision; prefer an SVG when one exists |
| Brand guide PDF | the `donts`, nearly verbatim, and usually the only written pairing rules | current-ness; guides go stale quietly |
| A deck or template | theme colours and fonts | certainty that these are not the software's defaults |

A logo with two or more fills earns exactly one question: which is the primary. Everything else the assets do not cover comes from the interview, and `confidence` is `mixed` — part of this file was found and part of it was asked.
