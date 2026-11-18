# Ellypsis Plugin Labs

Plugins for Claude Code and Cowork. Each one teaches Claude a way of working that a specialist would recognise: how to design before drawing, how to judge an MCP server by how a model actually uses it, how to make visuals that don't look generated.

## Install

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install <plugin>@ellypsis-labs
```

Add the marketplace once. `/plugin marketplace update ellypsis-labs` brings in new plugins and new versions.

## Plugins

| Plugin | Use it when you want to | Start with | Needs |
|---|---|---|---|
| [`ux-before-ui`](plugins/ux-before-ui) | Design or redesign an app, site, landing page or deck, and work out who it is for and what they must do before anything is drawn | `/ux-before-ui` | Nothing to start. Best with a UI reference library: the [Mobbin MCP](https://mobbin.com/mcp) (paid plan), or screenshots. Node and Playwright to render boards |
| [`mcp-eval`](plugins/mcp-eval) | Know whether an MCP server works in the hands of Claude: whether it finds the right tool, calls it well, survives the payload and grounds its answer | `/eval` | Claude Code, the server you want to test connected, `python3` |
| [`not-ai-slop`](plugins/not-ai-slop) | Turn a post or article into a carousel that looks like your brand, not like a generator | `/carousel` | Nothing to install. Where the runtime has no image generation (Claude Code today), you get the image prompts to run elsewhere |

Every skill also triggers on its own when you ask for the thing in plain words. Each plugin's README and CHANGELOG has the detail and the current version.

## How they are built

- **Judgment over checklists.** Skills teach how to think about the domain and keep the expertise in reference files, so Claude adapts to your case instead of following a script.
- **You decide before anything costly happens.** The design frame, the carousel's slide plan and any write call an eval would make each wait for your yes.
- **Nothing is made up.** No invented numbers, quotes or examples presented as fact; a gap is stated as a gap.

## About

[Ellypsis](https://ellypsis.dk) is a Danish AI consultancy that builds knowledge-work plugins for Claude. This catalog is the part of that work that is useful to anyone.

## Contributing

Issues and PRs are welcome. Name the plugin in the title.

Tests live in `tests/<plugin>/`, never inside `plugins/<name>/`: an install copies the plugin folder to every user.

## License

MIT. See [LICENSE](LICENSE).
