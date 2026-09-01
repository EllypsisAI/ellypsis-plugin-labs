---
name: brainstorm
description: Brand Kit's visual brainstorm — generate deliberately different logo directions from the brand foundation, collect reactions, and lock one. Use when a founder wants to see logo ideas, directions, or drafts for their company's identity, says "show me something", or asks to see the images from an earlier round. Requires a completed interview (a brand foundation — else run /interview first) and the Brand Kit door. Not for general-purpose brainstorming or image generation outside brand identity.
argument-hint: "[reaction — e.g. \"B but warmer\"]"
---

# Brainstorm — seeing directions

Image generation here is brainstorming, not delivery. People cannot see an image from a text description — renders exist to externalize thought and provoke reactions. Chase reactions, not perfection. The finished logo is `/vectorize`'s job, later.

Journey: `/brand-kit` → `/interview` → **`/brainstorm`** → `/vectorize` → `/kit`.

Load the foundation and taste log first with `core__brand_kit_load` (the document body is in the text of the result). No foundation → run `/interview` first, no exceptions. How to construct every prompt lives in `references/image-prompting.md` (in this skill's directory) — read it before the first generation. If the founder passed a reaction as an argument (e.g. "B but warmer"), that's the iteration instruction — log it and act on it.

## Never generate to recover — ask for the round

**If a round doesn't appear, it was still made, still stored, and still paid for.** Some hosts stop waiting before four images finish; the images are already in the founder's storage. The same is true when a founder returns and asks for "the ones from last time", or when a result says images were generated but couldn't be stored.

Every one of those is `core__brand_kit_round` — free, generates nothing, and returns the round exactly as interactive as a fresh one. `run_id` for a specific run, no argument for their latest. **Generating again is the one move that turns a display problem into a double charge.** It is never the answer to a missing round.

## The tools, exactly

All generation goes through the Brand Kit door (hosts may show these names under a connector prefix). The founder never sees a prompt, a parameter, or a model name.

- **`core__brand_kit_generate`** — **always pass `directions`**: 1–6 objects of `{prompt, label, note}`, where `label` is the direction's name and `note` is the one line of *why this direction*, in the founder's language. Those two are what the founder sees on each card; a bare `prompt` yields "Direction 1…N" with nothing to react to. Plus `kind: "mark" | "wordmark"`, and `run_id` — omit it to start a run, pass it back to keep adding to the same one. **Never set `style` or `colors`** — both are live on the default model and both were measured making it worse; the palette goes in the prompt text.
- **`core__brand_kit_like`** `(gen_id, note?, liked?)` — flags one image so any later session can find it. Call it the moment the founder reacts positively and pass their words as the note. `liked: false` unlikes.
- **`core__brand_kit_liked`** `(run_id?, limit?)` — the liked images with their exact prompts. Default 6; ask for more when the headline says the list was trimmed.
- **`core__brand_kit_round`** `(run_id?, limit?)` — recovery, above. Free.

**Two models, chosen by `kind`, silently.** Marks go to the default — leave `model` unset.
Wordmarks pass `model: "google/nano-banana-2-lite"`, every time: the default model
misspells lettering, and a misspelled wordmark cannot be iterated into a right one. The
founder never hears either name.

**If a mark comes back with letters on it** — the default model's known flaw — don't
re-roll it silently. A re-roll the founder didn't ask for spends their allowance on a
problem they may not have minded. Carry on with the round; when they ask for an iteration
on that direction, run *that* one with `model: "google/nano-banana-2-lite"`.

**The images come back as images.** Each generation arrives as a picture in the same result — there is nothing to render, link, or fetch. **Never describe them back to the founder**; they are looking at them. Say what you'd say next to someone holding a sheet of prints: which one to look at first, what separates them.

Four directions is the default and the right number. Partial failure is normal — if two of four fail, two arrive, the result names the other two, and only the two that arrived were charged. Show what came and offer the missing ones as a smaller ask.

## Reactions arrive as sentences — answer them, don't classify them

The founder may be looking at an interactive grid where hearting is one click. **Never branch on whether the host supports it** — you cannot know, and one behavior covers both.

| What arrives | What to do |
|---|---|
| "I like "geometric" (gen_…) — please record that." | `core__brand_kit_like` with that `gen_id`. |
| "I don't want "anchor" (gen_…) after all — please unlike it." | Same tool, `liked: false`. |
| "Lock it — "…" (gen_…) is the direction…" | The explicit lock, below. |
| A quiet note that a like *has already been recorded* | Don't call the tool again. Acknowledge and move on. |
| Nothing — they just talk | Read the numbered list aloud and ask which ones land. |

Locking is one deliberate message, so tell the founder to **send it on its own** — an empty composer, then the Lock button — or the host will ask them about replacing text they'd already typed.

## The rounds

**Round one is divergence, engineered.** Four to six directions from deliberately incompatible style blocks — different construction logic, weight, figure/type balance (recipes in the reference). Asking one prompt for "different directions" yields variations of the model's middle, and the founder's choice carries no information. Marks and wordmarks are separate generations — never one combined image.

**Log rejections as they happen.** Every "no" goes to the taste log (`core__brand_kit_save`, `kind: "taste"` — load it, add, save the whole document back) with the founder's words for why. "Rejected both round ones, called them soft" is a rule every following prompt obeys.

## Stop rules — these are law

- Maximum **two rounds** of divergent generation before a preference is locked.
- After a lock, maximum **three iterations** on the chosen direction — one variable changed per iteration, never regenerate hoping.
- Then hard stop: more generations will not help; the foundation needs another look. Point back to `/interview` — not to another round.
- If *everything* is rejected, that is a finding about the foundation, not the generator. Same exit.
- Checking the taste log before showing any iteration is part of the round, not optional.

**Locking is an explicit act.** "Looks good", "ok", "yes" never lock. The word is "lock it" — or the founder's unmistakable equivalent, confirmed back. On lock: `core__brand_kit_like` the winners and save the direction record (`core__brand_kit_save`, `kind: "direction"`) — which direction, which `gen_id`s, the run, and why, in their words. That record is what makes a run *finished*, and what `/vectorize` starts from.

## When the door says no

Brand Kit has a spend allowance, and a refusal comes back as a finished sentence written to be read to the founder. **Relay it and stop — never retry the same call, and never quietly generate a smaller round to get under a cap.** If the answer names a number that's left, offer that number. If it says images were generated but not stored, that is the recovery case above: ask for the round. If the door isn't connected at all, stop and say so — never generate through other tools, since images made outside the door are invisible to `/vectorize` and are lost.

End cleanly: "Thanks for today — when you're ready, run `/vectorize`."
