---
name: image-prompting
description: Writes image prompts that produce pictures nobody reads as AI output, by prompting the physical process that would have produced the look instead of the look itself. Use whenever an image, background, texture, or visual element is being generated or a prompt for one is being written; whenever generated images come back looking generic, smooth, stocky, or "AI"; whenever a set of images has to hold one style across all of them; and whenever slide or post backgrounds are needed. Use it even when the ask is casual ("make me a picture of...", "what prompt should I use for this", "can you generate a background") — a prompt written without it names a style instead of a process and averages straight to the AI mean. For a whole carousel or slide set, the carousel skill owns the run and calls this one for the pictures — this skill is for the image itself, not the deck.
argument-hint: "[what the image is for]"
---

# Image prompting

**Never prompt the look. Prompt the physical process that would have produced the look.**

Style adjectives ("retro", "grainy", "cinematic", "editorial") are averaging
instructions — they pull the model toward the mean of everything tagged that
way, which is exactly the generic-AI center of mass you are trying to escape.
A process description is a *constraint system*: it removes the model's escape
routes. A prompt that says "halftone dots on a 45° grid, 10–18px in shadows,
zero in highlights, layers misregistered 1–3px" cannot drift into smooth
digital rendering, because smooth digital rendering violates the stated
physics.

Corollaries that shape every procedure below:

1. **Numbers beat adjectives.** "Thick lines" is a vibe; "a 20mm chisel tip,
   no stroke thinner than the tip allows" is physics.
2. **Constraints beat descriptions.** Say what is *forbidden* (negative
   prompt) with the same care as what is wanted. The negative prompt's job is
   to list the model's defaults: clean edges, gradients, perfect registration,
   stock-photo lighting, "digital look".
3. **Every distinctive style has an imperfection signature.** Ink bleed,
   misregistration, dry-drag, scan softness, paper aging. The imperfection is
   not decoration — it is the *evidence of the process*, and it is what reads
   as human. Identify it first when analyzing any reference.
4. **One tonal mechanism per style.** Real processes render tone one way
   (dot size, hatching density, ink layering, exposure). Find it in the
   reference and declare it exclusive: "dot size is the only tonal tool."

Three moves: decide what the picture should be, write the prompt, judge it and
iterate. The first two open with a file to read before doing anything. Both
gates are real — what is kept here is the floor, not the method.

## 1. Decide what the picture should be

**Read `references/image-idea.md` before deciding what any picture is.** It
carries the principle the recipe implements, the seven operations that stage it,
and the rule for which images get a picture at all. The idea is where this skill
fails when it fails, and it fails by defaulting to the topic.

**Step:** Get to the idea in one line of conversation. Ask two things and only
these two: whether the pictures should feel like anything in particular, and
whether they want to be in them (default: no). Self-as-subject is asked up
front because it changes every prompt after it — a late yes means rewriting the
whole set.

**Step: the picture does not depict what the words say.** A brand built on
dossiers and files does *not* get backgrounds of dossiers and files. The image
carries atmosphere; the words carry meaning. The subject of the words never
enters the scene slot as a noun — what enters is a physical situation with a
temperature.

**Step: write the ban list before inventing anything.** Write down every noun a
reader would expect from the topic. Conference → room, stage, badge, lanyard,
audience, podium, microphone, seats, slides, name tag. **None of these may
appear in the image.** The topic supplies the feeling and one word; it never
supplies the objects. Skipping this step is what produces empty conference
rooms.

**Step: name two registers that collide.** This is the mechanism, and it is what
an agent has instead of "make it intriguing". One register is the feeling the
words need — reverence, exposure, futility, solitude, menace. The other is
chosen for *not belonging with it*. Then find the single image where the two
collide: an astronaut kneeling in a field of flowers, sterile against organic; a
boulder where a man's head should be, flesh against stone; a supercar parked
alone in a wet empty moor, luxury against desolation. This runs on every image
in the set, not only the first — the first one gets the strongest collision, the
rest are not decoration waiting for a topic.

**Step: generate five candidates from five different ways of staging that
collision** — the operations table in `image-idea.md` — then pick the one
furthest from the topic that still carries both registers. One candidate is not
a choice — the first idea is the literal one every time, which is why the count
is part of the rule.

**Step: state the reject-check in the output, before generating.** Write the
scene slot, then say three things: which banned nouns it contains (none is the
only passing answer), whether it still holds two colliding registers or has
collapsed into one, and what a stranger reading the slot without the caption
would guess the caption to be. If they could guess it, it is illustrating — go
back and pick another candidate. The correct answer to *"what does this picture
have to do with the post?"* is *"nothing, until you read the headline."*

**Carve-out:** when the claim *is* a claim about what an image should look like
— a slide teaching scale, or light, or one subject per frame — the image must
demonstrate it, literally, and none of the above applies. A surreal picture
there destroys the lesson. `image-idea.md` has the rule for telling the two
cases apart.

## 2. Write the prompt

**Read `references/prompt-craft.md` before writing a prompt.** Deriving a block
costs seven questions about process and a calibration loop; the file also has
the diagnosis table for when output comes back wrong.

**Step:** Assemble in layers with different lifetimes. Keeping the layers
separate is what makes output consistent across a set and across a content
pipeline:

| Layer | Contains | Lifetime | Who may edit |
|---|---|---|---|
| **STYLE BLOCK** | medium, tool physics, tonal mechanism, texture/substrate, negative prompt | frozen per project; versioned in a file | only via the test-diff-patch loop, never mid-production |
| **WORLD BLOCK** | palette (hex-locked, from `design.md` when one is resolved), lighting logic, recurring characters/sets/props described once and verbatim-reused, camera language | frozen per set/campaign | locked after the plan is approved |
| **SCENE SLOT** | subject, composition | changes every generation | freely |

The style block's sixth part is PALETTE — how many colors the process allows and
where each may go. That much is physics and stays in the block; the values
themselves come from `design.md` and sit in the world block.

Take a block from `references/style-blocks.md` if one fits; derive a new one
with Procedure 1 in `references/prompt-craft.md` if none does.

**Step:** Paste the STYLE and WORLD text verbatim, character-for-character, into
every prompt in the set. The single most common failure in multi-image work is
**slot leakage**: style or world vocabulary drifting into the scene slot,
getting paraphrased per image, and slowly mutating the look. Paraphrasing counts
as editing. If an image needs something the world block lacks, change it in the
world block, once, and re-freeze — never in the individual prompt.

**Step:** Never ask for text inside the image. Generated images supply
backgrounds and elements; every word a reader will read is set as live text by
whatever renders the surface.

## 3. Judge it and iterate

**Step:** Generate once with `~~imagegen`, using a neutral subject if you are
calibrating a new block. Put the output beside the reference or the intent.
Name each delta in process terms — "dots too uniform", not "looks too clean";
"registration too perfect", not "too digital". Patch exactly one block section,
regenerate. Two to four loops is normal; if it has not converged in five, the
medium hypothesis is wrong — go back to Procedure 1 and try the other candidate.

**Why:** A delta named as a feeling gives you nothing to change; named as a
process fault it points at one line of the block. Patching several sections at
once destroys the only thing the loop produces — knowledge of which change did
what.

**Posture:** The first generation is a probe, not a candidate. "Close enough"
arrives long before the picture stops improving — treat its arrival as the cue
to name one more delta, not as permission to stop.

**Step:** Human approves vibe → blocks are FROZEN and versioned. From here on,
edits require re-approval.

When output is wrong in a way you can name, the symptom→cause→fix table in
`references/prompt-craft.md` (Procedure 4) comes before touching any prompt.

## Tools

`~~imagegen` is the image-generation category, resolved by the plugin's
connector configuration. Nothing connected is not a blocker: write the prompts
out in full, labelled per image, for the user to run elsewhere.

## References

| File | Read when |
|---|---|
| `references/image-idea.md` | **Before deciding what any picture is.** The collision principle, the recipe, the seven operations, the constants, which images get a picture at all, self-as-subject |
| `references/prompt-craft.md` | **Before writing any prompt.** Deriving a block from references, using references at generation time, holding one look across a set, the diagnosis table |
| `references/style-blocks.md` | Choosing a look. Calibrated blocks ready to paste, each with notes on why it works |
