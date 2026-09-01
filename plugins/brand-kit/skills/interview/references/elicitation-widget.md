# The visualize elicitation widget — mechanics

How to render the interview's structured pass as a tappable form instead of a wall of
questions. Platform tools; if `visualize` isn't available in this environment, ask in
plain conversation instead.

## The two-step call

1. `visualize:read_me(modules=["elicitation"])` — loads the design spec (CSS classes,
   layout rules, locked chrome). **Silent** — never mention this call to the user.
2. `visualize:show_widget` — renders the actual form as HTML.

## Infer first — the design principle

Before rendering anything, check what's already known from the conversation, memory, or
attachments. Render a field only for what genuinely can't be determined otherwise. If
everything's inferable, skip the form entirely. Default is "check what's missing, then
form only for the gaps" — never "always show the form."

## Shell is locked, inputs are open

The form wrapper, header (title always "[subject] details", e.g. "Brand details"), the
`.elicit-question` label styling, and footer (Skip / Continue buttons) are fixed — don't
restyle them. There's a required header SVG and (if using file upload) a required
dropzone SVG — both emitted byte-for-byte, never redrawn. What's open is how each
`.elicit-group` renders its input.

## Choice inputs — one mechanism, three shapes

Every option is a `<button class="elicit-pill" data-value="...">` inside a
`.elicit-pills` container with `data-name` (what it maps to in the output) and
`data-multi` (true/false). The shell wires selection state automatically — no onclick,
no `<script>` anywhere in the form. Presentation varies:

- **Plain pills** — short text-only options (≤4 words)
- **Cards** — options with an icon + one-line subtitle
- **Preview tiles** — small illustrated previews, for output-format choices

Other input types: sliders (`<input type="range">`) for quantities/scales,
`<input type="date">` for dates, `<textarea class="elicit-textarea">` for free text, and
a dropzone+textarea pair for file uploads (inspiration images belong here).

**Color:** selection state is locked to blue unless there's a real semantic reason
(amber=cost, red=risk, green=success), set via `data-accent` on the pill — never inline
color overrides; they break the selected-state styling. (Note: green-as-success in the
form chrome is the platform's semantics, not a brand choice — it says nothing about the
founder's palette.)

## The output contract — what matters most

On submit, the answers arrive as the user's **next chat message** — not a tool result —
compiled onto one line: `[Subject] details — Question: answer · Question: answer`.
Field labels are auto-derived from `data-name` (humanized to sentence case).
Multi-select values are comma-joined. Long text (81–200 chars) gets quoted; over 200
chars shows a `(N chars — see below)` placeholder with the full text repeated verbatim
underneath. If the user hits Skip, the message is literally
`(Skipped the form — proceed with defaults or ask me in plain text)` — honor it: continue
conversationally, don't re-render the form.

## What belongs in Brand Kit's form (and what doesn't)

Form-worthy: exact company name string (free text — it will be confirmed letter by
letter in conversation anyway), first surface (cards: deck / website / app icon /
packaging), existing assets yes/no + upload, hard color aversions (pills), rough timeline.
NOT form-worthy: anything about feeling, taste, admired brands, or the company's world —
those need the follow-up question, the "what about it?", the digging. A form can't dig.
