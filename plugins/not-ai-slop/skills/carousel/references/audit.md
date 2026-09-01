# Audit — run before export

Between the backgrounds landing and the export. Fast, and it catches the failures that
are expensive after a PDF exists.

Run it against the contact sheet, not slide by slide — half of these are set-level and
invisible one slide at a time.

## Structure

- [ ] The outcome was named first, and the archetype picked wins that outcome
- [ ] Slide 1 opens at the most interesting moment, not with a title
- [ ] Cover is 8 words or fewer, big type, high contrast, a promise or a number
- [ ] Slide 2 sets up the problem and creates stakes — it earns the rest of the set
- [ ] **Spine test:** cover any slide; if the next one still makes sense without it, the spine is broken
- [ ] One idea per slide, max two supporting sentences. No paragraphs
- [ ] At least one slide is genuinely save-worthy on its own
- [ ] The close flips a belief and names one specific action

## Words

- [ ] Every string on every slide is character-identical to what was approved at Gate 1
- [ ] Every claim traces to the piece. No invented numbers, proof, or case studies
- [ ] Proof is shown, not claimed
- [ ] No hedging, no throat-clearing, no slide that announces the next slide
- [ ] Emphasis is one or two words per headline, never more
- [ ] No credit lines, no attribution, no provenance anywhere on the slides

## Design

- [ ] Every slide survives being screenshotted alone
- [ ] Max two font families per slide — one loud, one quiet, the same two throughout
- [ ] Three colour roles; accent appears once or twice per slide, never 50/50
- [ ] Nothing at full saturation unless `design.md` says so; darks are off-black
- [ ] Only `safe_pairs` combinations are used
- [ ] Visual weight changes on every slide — no two consecutive treatments alike
- [ ] Layout was chosen by name from the eight, per slide, not improvised
- [ ] Furniture present and identical on every slide; slide numbers visible
- [ ] No background depicts what its slide says
- [ ] Every background is cover-cropped with a named anchor. Nothing is stretched
- [ ] Type on an image is readable, and the scrim reads as a gradient rather than a grey box
- [ ] `pad` is actually `pad` on all four sides of every slide

## Handback

- [ ] An editable file ships alongside the PDF
- [ ] Both fonts actually rendered — or the substitution is named in the note
- [ ] The note says which tool built it and what fell back

## Kill criteria

Not warnings. Any of these means going back, not shipping with a caveat.

| Finding | Go back to |
|---------|------------|
| Cover over 8 words | The cover. Rebuild it |
| Nothing on the set is save-worthy | The shape. The carousel won't be saved either |
| A string differs from the approved one | The spec. Restore it, or return to Gate 1 |
| A claim with no source in the piece | The plan. Cut it |
| A personal story with no transferable lesson | Hold the post. It is a journal entry |
| "Does it look good?" is the only defence for a slide | You decorated. Point at a decision or change it |
