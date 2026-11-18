# Ellypsis Plugin Labs

**Your AI agent can do almost anything. These plugins make it do one thing the way a specialist would.**

Each plugin hands your agent a working method: the questions a senior designer asks before drawing, the way an image director thinks about a picture, the tests a platform team runs before shipping an integration. You keep talking to your agent the way you always do. It just stops guessing.

Works with **Claude Code**, **Claude Cowork** and **ChatGPT Codex**. Install in two minutes, below.

---

## ux-before-ui
### Stop getting interfaces that look fine and work badly

Ask an AI for a screen and you get a screen: a design system, three style words, straight to pixels. Nobody asked who arrives, what they fear, or why they leave.

ux-before-ui makes your agent work like a design team. It frames the purpose, maps your audience and their journey, ranks the jobs they came to do, and studies how the best products solve those same jobs, from real product screens. Then it draws **every screen, page or slide side by side**, critiques them with you and hands off a brief a developer can build from.

- Apps, websites, landing pages, onboarding, checkout, pitch decks
- From a blank page, a rough idea, an MVP or a live product that feels clunky
- Pairs with [Mobbin](https://mobbin.com/mcp) for real-world references. The first run walks you through the options

> *Try:* "Redesign our onboarding, people drop off after signup" · "Plan a landing page before we build it" · "Audit this app and propose a new structure"

**Runs on:** Claude Code · Claude Cowork · ChatGPT Codex

---

## not-ai-slop
### Visuals for your writing that don't look generated

Turn a post or article into a carousel people stop scrolling for. You approve the words on every slide before anything is made. Backgrounds are prompted by how a photographer, printer or painter would have made them, not by "modern, clean, minimal", which is exactly what keeps them off the generic AI look. Everything follows your brand, pulled from your website into one small file, and you always get an editable slide file next to the PDF.

> *Try:* "Turn this post into a LinkedIn carousel" · "Write an image prompt that won't look AI-generated" · "Pull our brand out of our website"

**Best in ChatGPT Codex**, where image generation is built in, so the backgrounds are made for you in the same run. In Claude you get the slide file and finished image prompts to run in any image tool.

---

## mcp-eval
### Find out if Claude can actually use your MCP server

Your server passes its tests. That doesn't mean a model finds the right tool, calls it with sane arguments, survives the payload and grounds its answer in what came back. mcp-eval sends sub-agents through realistic tasks against your connected server, records every call, and hands you a dashboard with a ship or don't-ship verdict.

> *Try:* "Is this MCP server production-ready?" · "Why isn't Claude using my tools?"

**Runs on:** Claude Code. Needs the server you want to test connected, and `python3`.

---

## Install

Add the marketplace once, then install whichever plugins you want. New plugins and updates arrive through the same marketplace.

### Claude Code

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

Swap in `not-ai-slop` or `mcp-eval` for the others. Update later with `/plugin marketplace update ellypsis-labs`.

### Claude Cowork (Claude desktop app)

1. Open **Customize** → **Browse plugins**.
2. On the **Personal** tab, click **+** → **Add marketplace from GitHub**.
3. Paste `EllypsisAI/ellypsis-plugin-labs`.
4. Pick the plugins you want and install.

### ChatGPT Codex (app or CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

Or `codex plugin add ux-before-ui@ellypsis-labs`. In the Codex app, type `/plugins` to browse and install.

### Or let your agent do it

Paste this into Claude Code or Codex:

> Add the plugin marketplace at github.com/EllypsisAI/ellypsis-plugin-labs and install ux-before-ui from it.

### Then just ask

Every plugin wakes up on its own when you ask for what it does, in plain words. You can also call it by name: `/ux-before-ui`, `/carousel`, `/eval`.

| | Claude Code | Claude Cowork | ChatGPT Codex |
|---|---|---|---|
| ux-before-ui | ✓ | ✓ | ✓ |
| not-ai-slop | ✓ prompts for images | ✓ prompts for images | ★ images built in |
| mcp-eval | ✓ | | |

---

## Why they work

- **A method, not a checklist.** Each plugin teaches your agent how a specialist thinks, so it adapts to your case instead of filling in a template.
- **You stay in charge.** The design frame, the slide words and anything an eval would write all wait for your yes.
- **No made-up facts.** No invented numbers, quotes or examples dressed up as real.

## About

Built by [Ellypsis](https://ellypsis.dk), a Danish AI consultancy that builds expert plugins for teams who work with AI every day. This marketplace is the part of that work anyone can use, free and MIT-licensed.

Issues and pull requests are welcome. Name the plugin in the title.

## License

MIT. See [LICENSE](LICENSE).
