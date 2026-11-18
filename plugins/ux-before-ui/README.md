# ux-before-ui

The usual failure: a design system, three style words ("modern, clean, Apple-like") and straight into screens. It looks fine and works badly.

This skill reverses the order. Before anything is drawn it works out who arrives, in what state, how often, wanting and fearing what. Then it draws every screen, page or slide at once, side by side, so the design can be judged as a whole.

## What it does

| Phase | Output |
|---|---|
| Frame | One purpose sentence and seven sizing questions that decide which phases matter |
| Audit (if something exists) | Inventory, action map with click and screen counts, ranked friction |
| Audience, journey, jobs | Who comes, the moments of truth, ranked jobs and the actions they need |
| Explore | How expert teams solve the same jobs, as a recommended pattern per area |
| Decide and draw | Decision records, a board spec, every screen side by side |
| Critique | Owner feedback turned into rules for all boards |
| Hand off | A brief a builder can work from without being in the room |

It scales to the medium and starting point: a full run on an existing web app takes a day, a landing page takes hours, a deck half a day.

It is the process, not the visual craft. Typography, colour and layout come from your design system and the skills made for it.

## Use

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

It triggers on its own when you ask for a UI, page, flow or deck to be designed, redesigned or audited. You can also call it directly with `/ux-before-ui`.

It works best with real references to look at. On the first run it asks where they come from: the [Mobbin MCP](https://mobbin.com/mcp) (recommended, needs a paid Mobbin plan), screenshots from Mobbin, Mobbin open in a browser Claude can control, or your own references.

`scripts/render_boards.mjs` renders a folder of HTML boards to PNG and builds a contact sheet. It needs Node and Playwright.

## License

MIT
