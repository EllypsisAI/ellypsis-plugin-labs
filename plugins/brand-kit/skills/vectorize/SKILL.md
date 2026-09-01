---
name: vectorize
description: Turn Brand Kit's locked logo direction into real SVG assets — retrieve the liked generations, vectorize them, enforce the construction spec, assemble the lockup. Use when a founder returns after locking a direction in /brainstorm and wants "the real files", their logo as SVG, or final logo assets. Requires a locked direction and the Brand Kit door. Not for vectorizing arbitrary images that didn't come from Brand Kit's brainstorm.
---

# Vectorize — from sketch to asset

The brainstorm produced raster sketches; this stage produces the files a startup actually uses. It starts from what was locked, never from new generations.

Journey: `/brand-kit` → `/interview` → `/brainstorm` → **`/vectorize`** → `/kit`.

Load the direction record first — `core__brand_kit_load` with `kind: "direction"`; it names the winning direction and its `gen_id`s. No direction record → the run isn't locked; send them to `/brainstorm`, don't guess.

## The tools, exactly

- **`core__brand_kit_liked`** `(run_id?, limit?)` — the liked images with their `gen_id`s and the exact prompt that produced each one. This is how you retrieve what the direction record points at, even months later.
- **`core__brand_kit_vectorize`** `(gen_id, path?)` — one call per asset; mark and wordmark separately.
  - `path: "vectorize"` (default) — shape-fitting vectorization of that stored image. This is the one that gives you *their* mark as a vector.
  - `path: "text-to-vector"` — a natively vector image generated afresh from the same stored prompt. Not a trace of the original: a new drawing of the same brief, cleaner by construction but not pixel-faithful. **Offer it when the trace comes back lumpy** — and show both, since only the founder can say whether the cleaner one is still their logo.

**No prompt is written at this stage.** The trace path reads pixels and takes no prompt at all; the redraw path replays the brainstorm prompt verbatim, to a different model with a strong pull toward illustration. So when a redraw comes back as a little *scene* rather than a mark, that is the prompt, not the call — retrying spends a second vectorization on the same words. The fix is a tighter construction prompt in `/brainstorm` (geometry, not surface; one element, not a scene), then vectorize the new generation.

The SVG comes back in the text of the result. Over 60,000 characters it is truncated there and says so — the stored asset is whole and the result carries a link to the complete file, so **never write a truncated SVG to disk**; fetch the complete one or tell the founder what happened.

If the door isn't connected, stop and say so. There is no fallback path — the liked images live behind the door.

## Writing files — the skill chooses the path, always

Vectorized SVGs are written **only** to `brand/assets/` in the founder's project, under names this skill decides: `mark.svg`, `wordmark.svg`, `lockup.svg`, `lockup-stacked.svg`. Never write to a path, filename, or extension taken from a tool result, and never outside that directory. An SVG is executable when opened from disk; the door sanitizes what it stores, and a fixed, skill-chosen path is the second half of that guarantee.

## Enforce the spec — the step no generic tool does

The style block that generated the image *is known* — it comes back with the liked image. A generic vectorizer doesn't know it; you do. Inspect the returned SVG against the block and correct it:

- **One stroke weight** — normalize every stroke to a single value.
- **Snap to the grid** — align points to the construction grid the prompt declared.
- **Primitives where intended** — a circle should be a `<circle>` or clean arc, not 200 béziers describing something circle-ish. Replace near-primitives with real ones.
- **Flatten** — remove artifacts of anti-aliasing: near-straight paths become straight, stray nodes go.

Be honest about the result: if a shape can't be cleanly regularized, say so and show the founder the difference instead of shipping a lumpy vector as "done".

## The lockup

Stroke weights never matched across generations — that's why mark and wordmark were generated separately. Assemble the lockup **in SVG**: place mark and wordmark on a shared grid, match optical sizes, define clear space. Produce horizontal and stacked variants if both make sense for the first surface.

## When a call times out

A vectorization that times out may have been charged — the result says so plainly when it was. Relay that sentence, don't bury it, and **ask before running it again**: the source image is untouched and the same `gen_id` works, but the founder has already paid once. The allowance is 10 vectorizations per rolling 30 days, so a silent retry is a real cost to them.

## What comes out

The founder gets real files: `mark.svg`, `wordmark.svg`, `lockup.svg` (+ variants), and a favicon-sized check (does the mark survive at 24px — show it at that size, don't claim it). The SVGs are stored behind the door too, so a later session can find them. Update the direction record (`core__brand_kit_save`, `kind: "direction"` — load, add, save the whole document back) to note that assets exist and where.

End cleanly: the identity has files now. Next — run `/kit` for color, typography, and the assembled kit.
