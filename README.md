<p align="center">
  <img src="assets/banner.png" alt="Ellypsis Plugin Labs: expert methods for your AI agent" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-works-7c3f63?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Claude_Cowork-works-7c3f63?style=flat-square" alt="Claude Cowork">
  <img src="https://img.shields.io/badge/ChatGPT_Codex-works-7c3f63?style=flat-square" alt="ChatGPT Codex">
  <img src="https://img.shields.io/badge/license-MIT-191713?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <b>English</b> ·
  <a href="i18n/README.da.md">Dansk</a> ·
  <a href="i18n/README.de.md">Deutsch</a> ·
  <a href="i18n/README.sv.md">Svenska</a> ·
  <a href="i18n/README.no.md">Norsk</a> ·
  <a href="i18n/README.fr.md">Français</a> ·
  <a href="i18n/README.es.md">Español</a>
</p>

---

Ask your AI agent for a signup flow and it'll draw you one. It won't ask who's signing up, what they're nervous about, or why half of them leave at step two. It's good at everything and an expert at nothing.

**Plugin Labs gives it the expertise.** Each plugin is how a specialist actually works: the questions they ask first, the mistakes they've learned to avoid, the order they do things in. Install it once, and it kicks in whenever you ask for that kind of work. You talk to your agent the way you always do. It just stops winging it.

## What's inside

| | Plugin | What it does for you | Works in |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](plugins/ux-before-ui)** | Thinks like a design team before it draws anything. Who's coming, what they need, how the best products solve it. Then every screen side by side, critiqued, and handed off. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](plugins/not-ai-slop)** | Turns your post into a carousel that doesn't look AI-made. You sign off on every word first, and the images follow your brand. | **Codex** (images built in) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](plugins/mcp-eval)** | Finds out if Claude can actually use your MCP server, and gives you a straight ship or don't-ship verdict. | Claude Code |

More are on the way. Add the marketplace once and new plugins simply show up.

## Get it running in two minutes

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (the Claude desktop app)

Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → paste `EllypsisAI/ellypsis-plugin-labs` → install what you want.

**ChatGPT Codex** (app or CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Or don't bother.** Paste this into Claude Code or Codex and let it do the work:

> Add the plugin marketplace at github.com/EllypsisAI/ellypsis-plugin-labs and install ux-before-ui from it.

Then just ask for what you want, in your own words. The right plugin picks it up. You can also call one by name, like `/ux-before-ui`.

## Why this beats a good prompt

A prompt tells your agent what you want. A plugin teaches it how an expert would go about it, and that's the part you can't fit in a chat box.

- **Judgment, not checklists.** Your agent adapts the method to your case instead of filling in a template.
- **You stay in charge.** Plans, slide words and anything that changes the real world wait for your yes.
- **No made-up facts.** If it doesn't know, it says so.

## Who's behind this

We're [Ellypsis](https://ellypsis.dk), a small Danish AI studio. We build expert plugins for teams that work with AI every day. This marketplace is the part anyone can use, free and MIT-licensed.

Found a bug or have an idea? Open an issue and name the plugin in the title.
