---
name: carousel
description: Turns something already written — a finished post, a blog article, a newsletter, or a rough idea — into a carousel. Produces a slide plan you approve before anything is generated, background images, and an editable slide file alongside a PDF. Use this whenever someone asks for a carousel, slides, a swipe post, a LinkedIn or Instagram PDF, or 'pictures for this post'; when they want an article, draft or transcript turned into slides; or when they say 'make this look good' about something they wrote. It owns the whole run and calls the image-prompting skill for the pictures and the brand skill for the look, so start here for anything deck-shaped. It makes pictures for writing — it does not write the post and does not write the caption.
argument-hint: "<what you wrote — file path, URL, or pasted text>"
---

# Carousel

Slides for something already written. The words come out of the piece — this skill
picks which ones, cuts them to fit, and builds the pictures around them.

It does not write the post. It does not write the caption. Asked for either, say so
and hand back slides.

## The run

| # | Step | Read first |
|---|------|------------|
| 0 | Brand — read `design.md`. None exists? the `brand` skill writes one first | — |
| 1 | Read the piece — find the one idea, the proof, the thing worth keeping | — |
| 2 | Pick the shape — outcome first, then archetype, then beat sequence | `references/structures.md` |
| 3 | Slide plan — the exact strings, in order, one idea per slide | `references/voice.md` |
| 4 | **Gate 1 — the words. Hard stop** | below |
| 5 | Backgrounds — **invoke the `image-prompting` skill by name** | `references/composition.md` |
| 6 | Compose — approved words in, placeholder blocks where backgrounds land | `references/composition.md` |
| 7 | **Gate 2 — the layout. Soft look** | below |
| 8 | Backgrounds in, audit, export, hand back the editable file | `references/audit.md`, `references/handoff.md` |

Work the steps in that order, and open the file in the last column **before** doing the
step rather than after. The third column is not a bibliography. A step worked from
memory is the failure this table exists to prevent: the rules that stop bad output live
in those files, and a rule that was not read is a rule that was not applied.

## Gate 1 — the words

**Step:** Show the exact strings that will appear on each slide, in order, one line
each, with one short line under each naming what sits behind it. Then stop. Wait for
the user. Generate no image, open no slide file, and do not read silence as go.

That short line names **whether there is a picture and what temperature it carries** —
"hook picture, cold daylight", "flat canvas". It never names a scene. The scene does not
exist yet: it is invented at step 5, by a method that has not run when this gate is
shown. Guessing one here means guessing literally — "meeting-room table", "noticeboard
wall" — and putting the exact nouns the image method exists to ban in front of the one
person whose approval you are asking for.

```
1  I took Canva out of the equation.              · hook picture, cold daylight
2  Every time, the format had to be found again.  · flat canvas
3  All of it is written in code now.              · screen glow, dark
4  A design system and a few templates.           · flat canvas
5  You still make the last small edits yourself.  · flat canvas
```

**Why:** Everything after this bakes the words into something — a background composed
around a line length, a type size chosen for a word count, an exported PDF. Changing a
line here costs a keystroke; the same change after export costs the run. The habit this
gate defeats is real and named: people hold their small edits until the end, which is
the most expensive place there is to make them.

**Posture:** A plan that looks finished is not consent. This is not a checkpoint to
narrate on the way past — it is the one moment where the words are still free, and
your own sense that everything reads fine is exactly the drift it was built to catch.
Silence is not approval. It is a question nobody has answered yet.

The approved strings then go into the slides **verbatim** — never re-derived from the
piece, never improved in passing, never re-cased or re-punctuated. If a string will not
fit the layout, that is a layout problem; change the layout, or come back and ask.

## Step 5 — the backgrounds

**Step:** Invoke the `image-prompting` skill by name. Hand it the brief from
`references/composition.md` and use the prompts it returns, unedited.

**Why:** It is a skill, not a description of one — the same distinction as `~~present`.
"Hand off the brief" is an instruction you can satisfy by writing the prompts yourself,
and writing them yourself is how a post about a conference ends up with pictures of
empty conference rooms. The rules that prevent that live inside that skill, and they
only apply if it runs.

Do not write image prompts here. Not a first draft, not a starting point, not "the brief
is basically the prompt already."

## Gate 2 — the layout

Show the real slide file with the approved words in it and placeholder blocks where the
backgrounds will land. Say what it is in one line. Then keep going — silence means
continue.

It is the actual artifact with the pictures missing, not a wireframe to be rebuilt once
approved. The backgrounds drop into this same file.

## Questions — the budget is three

Never more than three questions before Gate 1. A fourth means something upstream should
have defaulted instead.

| Question | Default | When to ask |
|----------|---------|-------------|
| "Should the pictures feel like anything in particular?" | `imagery` from `design.md`, or the hook-picture rule | Always. One line, not a briefing |
| "Do you want to be in them?" | No | Always. It is cheap and it changes every prompt after it |
| "Want a comment-to-get-it close?" | **No** | Only when the piece actually has something to give away |

Never ask: anything already in `design.md`; permission to proceed between steps that
cost nothing; which layout, which type size, where things sit — that is the composer's
job to decide and this skill's job to constrain; or the same thing twice in new words.

## Where the words come from

Pull them from the piece. Cut them, shorten them, drop them — but never introduce a
claim the piece does not make. No invented statistics, no invented before/after, no
"industry standard". If the piece has no proof, the proof beat says so or gets dropped;
a stated gap beats a plausible-sounding invention. See `references/voice.md`.

## Rendering

Hand a **spec** to `~~present` — the runtime's own **presentation skill**. It is a skill,
not a vague capability: invoke it by name and let it choose the rendering. Do not name a
library, do not describe a rendering approach, do not build a renderer. A controlled test
settled this: the presentation skill produced correct cover-cropping, a subtle scrim, both
specified fonts genuinely embedded, an editable file and a PDF — and it won when it was
given no renderer instruction at all. Every run that specified one did worse.

Two rules the spec is never allowed to break:

- Cover-crop every background, and name the anchor. Never set a background's width and
  height to the frame.
- Ship an editable slide file alongside every flattened export. Never a PDF alone.

Degraded path — no `~~present` available: compose the slides as HTML/CSS at a fixed
1080×1350 canvas, absolute px, no responsive, and print to PDF from a browser. The HTML
file is then the editable deliverable. Say which fonts actually loaded, and that this was
the fallback. Full spec format and deliverables: `references/handoff.md`.
