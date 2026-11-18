# not-ai-slop

Visuals for your writing that don't announce themselves as generated.

Give it a post, an article or a newsletter and get back a carousel. You see the exact words for every slide before a single image is made, so the edits happen while they're free. Backgrounds are prompted by how a photographer, printer or painter would have made them, not by "modern, clean, minimal", and that is what keeps them off the generic AI look. Everything follows your brand, and you always get an editable slide file next to the PDF.

## Skills

| Skill | What it does |
|---|---|
| `/carousel` | Turns something you wrote into a carousel: slide plan for your approval, backgrounds, layout, export |
| `/brand` | Pulls your colours, fonts and rules from your website or files into one small `design.md` |
| `/image-prompting` | Writes image prompts that don't read as AI output. Used by the carousel, and on its own |

They also start on their own when you ask in plain words: "turn this post into a LinkedIn carousel".

## Where it shines

| | Images | Slide file |
|---|---|---|
| **ChatGPT Codex** | Made for you, built in | Codex's presentation skill |
| Claude Cowork | Finished prompts to run in any image tool | Built-in document creation |
| Claude Code | Finished prompts to run in any image tool | HTML at 1080×1350, printed to PDF |

## Install

**Codex**

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install not-ai-slop@ellypsis-labs
```

**Claude Cowork:** Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → `EllypsisAI/ellypsis-plugin-labs`.

Nothing else to set up: no API keys, no connectors.

## License

MIT
