# Brand Kit

Takes a startup from nothing to a usable visual identity — logo, color palette,
typography — in conversation. No design vocabulary needed; you explain your company with
whatever words you have, react to what you see, and walk away with real files.

## The journey

| Command | What happens |
|---------|--------------|
| `/brand-kit` | Onboarding: connects Brand Kit's door, checks where you left off, explains the road. |
| `/interview` | ~20 minutes of questions about your company, in your words. Compiles your brand foundation. |
| `/brainstorm` | Genuinely different logo directions to react to. You lock one when it's right. |
| `/vectorize` | Turns the locked direction into real SVG assets — mark, wordmark, lockup. |
| `/kit` | Color palette with roles, fonts that exist, drop-in CSS tokens, and the kit document that keeps every future deck consistent. |

Your brand work — foundation, taste notes, liked images, the kit — is stored behind
Brand Kit's own backend, so any later session on any device can find it. Nothing is
published anywhere, and you never need an API key.

## Install

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install brand-kit@ellypsis-labs
```

Then add the **Brand Kit connector** in Settings → Connectors — the plugin is the
know-how, the connector is the door, and you need both:

```
Settings → Connectors → Add custom connector
name: brand-kit
url:  https://gateway.ellypsis.dk/brand-kit/mcp
```

`/brand-kit` walks you through it and through the one login moment. Use the account you
want your brand work tied to.

Logo directions arrive as an interactive grid you can react to directly: heart the ones
that land, download any of them, lock the one that's right. That grid is why the
connector is added in Settings rather than bundled into the plugin — it doesn't render
on the bundled path.

## What it is not

Brand Kit ends at the kit. A full design system (components, code tokens, applied
templates) is a hand-off to Claude's design tooling, with the kit document as its input.

Built by [Ellypsis](https://ellypsis.dk). MIT-licensed.
