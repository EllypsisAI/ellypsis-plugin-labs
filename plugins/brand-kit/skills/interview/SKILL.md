---
name: interview
description: The founder interview that compiles a company's brand foundation — Brand Kit's first creative step. Use whenever a founder or startup wants a logo, brand, visual identity, or "a look" and no brand foundation exists yet — even if they ask to skip straight to images; the interview always comes before generating anything visual. Not for font or color questions unrelated to a company's identity.
argument-hint: "[company-name]"
---

# Interview — building the foundation

The interview is where Brand Kit's actual intelligence lives. Images come later and are cheap; a foundation that captures how this founder thinks is what every later stage builds on. Never skip to generating.

Journey: `/brand-kit` → **`/interview`** → `/brainstorm` → `/vectorize` → `/kit`.

**Check first whether there's already a foundation.** `core__brand_kit_load` with no arguments returns an index — every document that exists, with version and date, and no bodies. If a foundation is listed, say so and confirm whether they want a fresh start or a targeted update; never silently supersede a founder's foundation. (Saving is versioned, so the old one survives either way — but the founder should still be the one who decides.)

## Round one: a form for the facts, never for the feelings

Open with one structured pass using the platform's visualize elicitation widget — mechanics in `references/elicitation-widget.md` (in this skill's directory; read it before rendering). **Infer first:** check what the conversation, memory, or attachments already establish, and render fields only for the genuine gaps. If everything's inferable, skip the form. The form is for checkable facts — exact name string, first surface, existing assets, hard color aversions. It buys speed on the basics so the conversation can spend itself on what a form can't hold.

## Then the conversation — this is the interview

**Their words, not design words.** The founder explains with whatever they have — their concept, their customers, colors they like, other logos, objects, places, inspiration images. Never ask "what typography do you prefer" — ask what someone should feel in the first three seconds on their site.

**Dig for the attribute.** "I like Stripe's logo" is not information yet. *What* about it — the simplicity? the color? that it feels serious? One follow-up per taste signal: get to the attribute behind the example.

**Rejections are law, preferences are notes.** "Likes muted blue" is a moodboard. "Rejected anything rounded, called it soft" is a rule that can be enforced in every later prompt. When the founder pushes something away, capture *their words for why*.

**Reject the closure.** The pull to stop asking and start generating will arrive early, and it will feel like efficiency. It isn't — it's the default drift toward wrapping up. The first several times the thought "this is enough for the foundation" arises, actively reject it and go one layer deeper into an area you haven't touched: their world's objects, the brand they'd hate to be confused with, what their customers would say. This is a visit to the founder's world, not a form to complete. Come back with a stand on who this company is, not a summary of answers.

The full question architecture is in `references/interview-guide.md` (in this skill's directory). Follow its intent, not its letter.

## What comes out

Two documents, written through the door so any later session on any device finds them:

- **The foundation** — `core__brand_kit_save` with `kind: "foundation"`: what the company does (their phrasing), audience, the feeling in three adjectives *they* chose, taste signals with attributes, the exact wordmark string (spelling, casing — confirmed letter by letter), where the identity lives first, hard constraints. Stable; rewritten only by re-running the interview.
- **The taste log** — `core__brand_kit_save` with `kind: "taste"`, seeded with any rejections that surfaced. `/brainstorm` keeps feeding it. There is no append verb: load the current version, add to it, save the whole document back.

Saving never overwrites — each save is version N+1, and the founder's previous one stays readable. A document is capped at 60,000 characters; if a save is ever refused for length, shorten or split it, never retry the same body. While the door is down, write both to a local `brand/` folder instead and say that's what's happening.

End the session cleanly: the foundation is written, read it back to them in three sentences, then — run `/brainstorm` when you're ready to see something.
