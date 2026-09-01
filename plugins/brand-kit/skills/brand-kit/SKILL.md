---
name: brand-kit
description: Onboard a founder into Brand Kit — surface and connect the Brand Kit connector, verify the door, pick up where they left off, explain the journey. Use when Brand Kit was just installed, on a founder's first session, when the user says "get started with brand kit" or asks how Brand Kit works, or when core__brand_kit_* tools turn out to be missing mid-journey.
---

# Brand Kit — onboarding

Brand Kit takes a startup from nothing to a usable visual identity: logo, color palette, typography. The founder needs no design vocabulary — the whole thing runs on their words. This skill connects the machinery before any creative work begins.

## The journey (know it, tell it)

`/brand-kit` → `/interview` (build the brief) → `/brainstorm` (see directions, react, lock one) → `/vectorize` (turn the locked mark into real SVG) → `/kit` (palette, typography, the assembled kit). Each stage ends by naming the next command. After the kit, a design system is a separate hand-off — not this plugin's job.

## What to do

1. **Welcome in one breath.** What Brand Kit does, and that they'll never be asked for design jargon or shown a prompt.

2. **Connect through Settings → Connectors — assume they are NOT connected yet.** Installing the plugin does not connect the door, and the plugin deliberately ships no bundled server: the interactive logo grid only renders when Brand Kit is added as a connector. Hand them a tappable card rather than prose instructions: `search_mcp_registry` to find the Brand Kit connector, then `suggest_connectors` to render it with its Connect button (or Use, if already connected). If those tools aren't available, or the directory doesn't have it, give the step in plain words with the address they need: **Settings → Connectors → Add custom connector**, URL `https://gateway.ellypsis.dk/brand-kit/mcp`, named `brand-kit`. Never send a founder looking for a connector without handing them that URL.

3. **Verify the door.** Call `core__brand_kit_status` (hosts may show it under a connector prefix). It costs nothing and does nothing creative — it reports the connection, the founder's run count, which brand documents they have saved, and how much of their image allowance is left. First use may open a login window; say so **before** it appears: use the account they want their brand work tied to, nothing is published anywhere.

4. **Read the answer instead of asking questions.** Storage is always ready once connected — never ask a founder to authorize anything else.
   - `documents` empty and `runs: 0` → first session. Say the allowance in plain words once (60 image generations and 10 vectorizations per rolling 30 days, which is more than any one identity needs), then go to `/interview`.
   - `documents` lists a foundation → they've been here. Say what exists and send them to the stage that follows it, not back to the start.
   - `runs` above zero with nothing saved → a brainstorm that never got locked. Their images are still there: `/brainstorm` picks it up with `core__brand_kit_round`.
   - `image_service: "not_configured"` → everything except generating and vectorizing still works. Say that plainly; the interview is unaffected.

5. **Hand off.** End with the one command that comes next — usually: run `/interview`.

## If the door can't connect

Say so plainly and never fake the visual track. The interview works fully without the door — offer to start there, keep the founder's work in a local `brand/` folder as the fallback, and say that's what's happening; it moves behind the door once the connector is added. `/brainstorm` and `/vectorize` genuinely require the door — images made anywhere else are lost to the later stages.
