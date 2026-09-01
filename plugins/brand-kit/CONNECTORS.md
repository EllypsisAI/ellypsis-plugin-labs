# Connectors

Brand Kit has one connector: **the door** — Ellypsis's gateway endpoint carrying image
generation, storage and vectorization. `https://gateway.ellypsis.dk/brand-kit/mcp`.

**This file is documentation for people.** The runtime knowledge — which tool a skill calls
and what happens — lives inside each skill, self-contained. Root files are not reliably
findable at runtime; never make a skill depend on this one.

## The connector is added in Settings → Connectors. The plugin ships no `.mcp.json`.

This is deliberate. A door reached through a plugin-bundled `.mcp.json` is owned by an
engine that does not implement the MCP Apps extension — **the logo grid never renders on
that path**. Brand Kit's grid is not a garnish: it is where the founder reacts to the
images, and reacting is the product. So the connector path is the only path,
and `/brand-kit` surfaces it as a tappable card via the platform's connector directory
(`search_mcp_registry` → `suggest_connectors`).

Consequence to keep in view: installing the plugin alone gives a founder no door. The
onboarding skill assumes exactly that and starts there.

## The tools, as served

The gateway prefixes every backing tool with its MCP id: skills call **`core__brand_kit_*`**.
Every result carries a text half (what the skills read) and a structured mirror; the one
exception is `brand_kit_load`, where the document body travels only in the text.

| Tool | Params | What happens |
|------|--------|--------------|
| `core__brand_kit_status` | — | Free. Connection, run count, saved-document index, remaining allowance, model list. Storage is always ready once connected. |
| `core__brand_kit_generate` | `directions[]` (1–6 × `{prompt, label, note}`) or `prompt`+`count`, `kind`, `run_id?`, `model?` | Generates and stores. Images come back as image blocks in the same result. Per-direction failure is partial, not fatal — only what arrived is charged. **Never send `style` or `colors`** (see below). |
| `core__brand_kit_like` | `gen_id`, `note?`, `liked?` | Flags a stored image, with the founder's words. `liked: false` unlikes. |
| `core__brand_kit_liked` | `run_id?`, `limit?` (1–12, default 6) | Liked images with the exact prompt that produced each — the prompt is load-bearing for `/vectorize`. Empty is a normal answer, not an error. |
| `core__brand_kit_round` | `run_id?`, `limit?` | **Recovery. Free, read-only, generates nothing.** Returns a stored round as the same interactive grid. The answer whenever a round didn't arrive or a founder asks for last session's images. |
| `core__brand_kit_vectorize` | `gen_id`, `path?` | `vectorize` (default) traces the stored raster; `text-to-vector` generates a native vector from the same stored prompt. SVG returned in the text, truncated over 60,000 chars (the stored asset stays whole). Sanitized server-side. |
| `core__brand_kit_save` | `kind`, `content` (≤60,000 chars) | `foundation \| taste \| direction \| kit`. Never overwrites — writes version N+1. Over the cap is an in-band error naming the limit: shorten, never retry. |
| `core__brand_kit_load` | `kind?`, `version?` | No `kind` → index of what exists, with versions and dates, no bodies. A missing document is a normal answer, not an error. |
| `core__brand_kit_image` | `gen_id` | **App-only** — the widget's download button. Hidden from the model, and skills must not reach for it: a full-resolution image costs a fifth of the host's result budget to look at what the thumbnail already showed. |

## The two models

The allowlist is exactly two ids, and the skill picks between them by `kind` — silently,
because the founder never sees a model name.

| | id | Used for |
|---|---|---|
| Default | `fal-ai/recraft/v3/text-to-image` | Marks. Leave `model` unset |
| Second | `google/nano-banana-2-lite` | Wordmarks, always. And the next iteration of a mark that came back with lettering on it |

**"Fallback" is a named second model, not an automatic retry.** Nothing in core fails over
— the cap counts *generations*, so a silent server-side retry would burn a founder's
allowance twice per bad round. Passing `model` is the only path, and it is deliberate.

`style` and `colors` are live on the default model and both are traps: the 08-27 bake-off
sent Recraft's own recommended `style: "digital_illustration"` plus `colors` and got
photographic texture and gradients against a brief that banned both, while the round that
sent neither produced the marks that won. The door never sends `style`. Neither do the
skills. Palette goes in the prompt text — `references/image-prompting.md` carries the rest.

## Storage — core's own Postgres

Four document kinds, versioned, private per founder. **No Google authorization step
exists** — the console link the 0.1.0 skills sent founders to is gone. While the door is
down, skills fall back to a local `brand/` folder and say so.

## Spend — there is a cap, and refusals are written to be read aloud

Per founder, rolling 30 days: **60 generations, 10 vectorizations**. A shared daily service
ceiling applies on top of that. Every refusal comes back as a finished sentence. **Skills relay it and stop** — they never retry, and never quietly shrink a round
to squeeze under a cap.

Two rules the skills carry because money is involved:

- **Anything submitted and not confirmed cancelled is charged**, including a timeout. The
  result says so when it happened; the skill must not paper over it.
- **A round that was generated but not delivered is already paid for.** The recovery is
  `core__brand_kit_round`, never a second `generate`. Some hosts stop waiting before a
  four-image round finishes (ChatGPT at ~60 s; the gateway allows 120 s), which makes this
  a routine event rather than an edge case.

## The widget

`generate`, `liked` and `round` mount an interactive grid (`ui://brand-kit/grid.html`):
square tiles, captions over the image, heart / download / lock per tile. Likes go straight
to the tool and tell the model quietly afterwards; **locking is one deliberate message the
founder sends**, which is why `/brainstorm` tells them to send it on its own.

The founder-voiced sentences the grid emits ("I like … please record that", "I don't want
… after all", "Lock it — … is the direction") are a contract between the widget and the
skills: they arrive as ordinary user messages, and the same handling works on a host with
no grid at all. **A skill must never branch on whether the host supports widgets.**

## Which skill needs what

| Skill | Tools | Without the door |
|-------|-------|------------------|
| brand-kit (onboarding) | `status`; platform: `search_mcp_registry`, `suggest_connectors` | Explains the journey, sets up the local `brand/` fallback, offers to begin the interview; says plainly the visual track waits. |
| interview | `save`, `load`; platform: `visualize` (elicitation) | Fully functional (local `brand/` fallback). |
| brainstorm | `generate`, `like`, `liked`, `round`, `save`, `load` | Stops. Never generates through other tools — images made outside the door are lost to `/vectorize`. |
| vectorize | `liked`, `vectorize`, `save`, `load` | Stops. The liked images live behind the door. |
| kit | `save`, `load` | Fully functional; builds from local fallback or asks the founder for files. |

## Watermarking

Images from `google/nano-banana-2-lite` carry an invisible SynthID watermark. It is not
overridable and does not survive vectorization; the default model's images do not carry one.
