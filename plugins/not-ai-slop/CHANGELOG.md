# not-ai-slop — Changelog

## 0.2.1 — 2026-09-01

Documentation pass: the changelog is written for people using the plugin, not for its
authors. No functional changes.

## v0.2.0 — 2026-08-28 — The rule that was unreachable

A real run produced the exact failure the plugin has a rule against. A post about
a conference event came back with pictures of empty conference rooms.

**The rule was not missing. It was optional.** `image-prompting/SKILL.md` §2 said
"read `references/prompt-craft.md` before writing a prompt" — a real instruction.
§1 only said "`references/image-idea.md` has both in full" — a pointer. The
anti-illustration rule lived in the ungated file, so the model read the one that
demanded it and skipped the one that mattered. Generalised:

> Load-bearing knowledge lives in reference files, reference files are optional,
> so the knowledge is optional.

The fix is not more rules. It is moving the rules that break the output when
skipped into the file that is always loaded, and putting real read gates on the
rest. `SKILL.md` went 90 → 166 lines deliberately, against the lean-skill
instinct, because a lean file that summarises what nobody opens teaches nothing.

**The second failure was worse, because the skill broke its own law.** The hook
rule read "cinematic, intriguing, good enough to stop a scroll" — three adjectives,
in the one skill whose thesis is that style adjectives are averaging instructions.
It told the model to *want* an intriguing picture and gave it no way to *invent*
one, so the model reached for the only concrete thing available: the topic.

Replaced with a mechanism. **Two emotional registers, chosen for not belonging
together, and the single image where they collide.** An astronaut kneeling in a
field of flowers — sterile against organic. A boulder where a man's head should
be — flesh against stone. A supercar alone in a wet moor — luxury against
desolation. Seven named operations are ways of staging a collision rather than a
menu of tricks, so an agent can reason from the principle when none of them fit.

Three parts do the work: **the ban list** (write down every noun the topic
suggests; none may appear), **five candidates from five different operations**
(the first idea is the literal one every time), and **a reject-check stated as
output** before anything is generated — banned nouns found, whether two registers
still collide or have collapsed into one, and what a stranger would guess the
caption to be.

This governs every image in a set, not the first. What is special about the first
is degree, not kind.

**Density is decided separately from content.** Feel or believe something gets a
constructed image; see or compare something gets a literal demonstration; memorise
a structure gets no picture. The variable is what the image is asked to do, not
where it sits. The literal carve-out matters as much as the anti-illustration
rule — when the claim *is* a claim about what an image should look like, a surreal
picture destroys the lesson.

**Restored verbatim from the original method**, which had been compressed rather than
ported: the four corollaries and the clinching example, the name *slot leakage* and
the layer table's lifetimes and edit-rights, Procedure 3 (expanding one block into
a consistent set), Block C with its ⚠ UNCALIBRATED flag and its self-critique — the
passage where the source catches itself writing "premium tech editorial look" and
names it an adjective posing as physics — and Block D's grammar rules.

**Ordering, made explicit.** The run table's third column was headed "Where the
knowledge is" and named files without requiring them; it now reads **Read first**,
and says plainly that it is not a bibliography. Step 5 no longer *hands off* to
`image-prompting` — it **invokes it by name**, the same distinction settled for
`~~present`, because "hand off the brief" is an instruction a model can satisfy by
doing the work itself.

**Four defects found by running it on a real Danish post**, all fixed here:

- **Gate 1 was showing scenes it had not invented yet.** The annotation under each
  string named "meeting-room table", "noticeboard wall" — the exact nouns the image
  method exists to ban, in the one artifact a human approves. Gate 1 is step 4; the
  image method runs at step 5. The annotation now carries tone only.
- **`imagery` in `design.md` contradicted the collision rule.** Its own example was
  a freight brand's loading docks — the brand's own working world, which is the
  topic. It now governs tone only and says so.
- **Procedure 1 assumed reference images exist.** With none, no fallback was stated.
  Now: name a real medium, derive from its documented physics, flag it uncalibrated.
- **Step 6 chose layouts without reading step 5's reserved quiet zones.** You cannot
  unwrite a background that has already been specified; the layout tree now reads
  the brief first.

**What `~~present` actually resolves to**, verified rather than assumed: Codex ships
the `Presentations` skill enabled by default; Claude Code ships **nothing** — there
is no pptx or presentation skill. The HTML/CSS fallback is conditioned accordingly.
It needs a real shell and a browser it can drive, which is why it worked on a laptop
and failed in a hosted sandbox during the v0.1.0 bake-off. In a sandbox with no
`~~present`, hand the spec over rather than pretending to render it.

## v0.1.0 — 2026-08-27 — Born: three skills, dual-runtime, no renderer

Two bodies of knowledge that already worked by hand — how to design a carousel,
and how to prompt images that don't read as AI — packaged so they can be
installed instead of pasted. A third skill emerged during design, and it turned
out to be the one that matters most.

**The thesis, carried over verbatim:** never prompt the look;
prompt the physical process that would have produced it. Style adjectives are
averaging instructions — they pull toward the mean of everything tagged that
way, which is exactly the generic-AI centre of mass you are trying to escape. A
process description is a constraint system.

**Look-agnostic, and that is the whole differentiator.** The plugin ships no
house aesthetic. Everything derives from a ~45-line `design.md` of colour roles,
two fonts, a scale and three to five don'ts. This was not obvious: the seed
method's own house palette (cream base, soft serif, one hot accent) is listed by
Claude's `frontend-design` skill as AI-slop cliché #1 — the seed's default look
was a named tell. So the craft rules stayed and the aesthetic went. Style blocks
now carry the *medium* (tool physics, substrate, negatives, how many colours the
process allows); `design.md` carries the *colour*. A block a brand has never seen
is a swap, not a re-calibration.

**No renderer, decided by test rather than by taste.** Four runs, same content,
same `design.md`, same image prompts, renderer as the only variable. HTML/CSS +
Playwright failed outright — no Chromium in the ChatGPT sandbox. A JS canvas
produced flat raster with no way back in. `pptxgenjs` gave a genuinely editable
file but stretched backgrounds by fitting width and height to the frame. The
runtime's **native presentation skill won on every axis** — correct
cover-crop, subtler scrim, both specified fonts genuinely embedded and verified
with `pdffonts`, an editable file plus a PDF — and won without any renderer
instruction at all. So the plugin hands over a spec via `~~present` and carries
no rendering engine. Two rules the spec may never break: cover-crop every
background and name the anchor; ship an editable file alongside every flattened
export, never a PDF alone.

**Gate 1 exists because of where edits actually hurt.** The obvious answer to
"I want to adjust this myself" is downstream: make the output more editable. The
cheaper answer is upstream — show the exact words before anything is generated,
when a change costs a keystroke rather than the whole run. Gate 2 shows
the layout but does not stop — and it is the real file with the pictures
missing, not a wireframe to rebuild.

**Three questions, then a gate.** A fourth means something upstream should have
defaulted. The two rules that replaced questions: backgrounds are mood, not
illustration — a brand about dossiers and files does *not* get backgrounds of
dossiers and files — and slide 1 is a hook picture, the least obligated to the
topic of anything in the set. Self-as-subject is asked once, up front, because it
changes every prompt after it. Culturally-specific plays (the comment-to-get-it
close) are opt-in and default off.

**It does not write.** Carousel from a finished post or from a rough idea, but
the caption is yours. It makes pictures for writing.

**Deliberately discarded:** everything assuming a whole slide or
whole carousel comes out of image generation. That included the entire carousel
architecture file, three of five style blocks (text-in-image layout grammars),
and the line "carousels are the same machinery with a different assembly." The
claims inside survived; the framing did not.

**Distribution.** One `skills/` tree, two catalogs — `.claude-plugin/` for Claude
Code, `.agents/plugins/` + `.codex-plugin/` for Codex and ChatGPT. Agent Skills
is an open standard, so nothing is generated from anything else. Install verified
end to end in Codex; the installed tree diffed byte-identical against source.

**No `.mcp.json`.** All four `~~categories` — `imagegen`, `present`, `brand`,
`fetch` — resolve to capabilities the runtime already has. Nothing to install,
nothing to authenticate, and every one has a degraded path written as a path
rather than an error.
