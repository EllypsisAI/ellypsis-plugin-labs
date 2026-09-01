# Ellypsis Plugin Labs

The public marketplace for plugins from Ellypsis Labs — for Claude Code and Cowork. One install, every public Ellypsis plugin.

## Install

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install <name>@ellypsis-labs
```

Add the marketplace once, then install anything in the catalog with `@ellypsis-labs`. `/plugin marketplace update` pulls new additions and updated versions.

## What's in here

Plugins live inline in this repo under `plugins/<name>/` — one repo, one working tree, so what ships is what's developed.

| Plugin | What it does |
|---|---|
| [`brand-kit`](plugins/brand-kit) | Takes a startup from nothing to a usable visual identity. An interview builds the brand foundation, visual brainstorming turns taste into something you can point at, and the kit assembles what you locked into files you can use. |
| [`mcp-eval`](plugins/mcp-eval) | Evaluates an MCP server in the hands of an LLM. Sub-agents run realistic tasks against your connected server while hooks capture the trajectory — discoverability, argument fidelity, payload economics — and grade it. |
| [`not-ai-slop`](plugins/not-ai-slop) | Visuals for things you've written that don't announce themselves as generated. Turns a post or article into a carousel: a slide plan you approve before anything is made, then images prompted against a design system. |

Current versions live in each plugin's `.claude-plugin/plugin.json` and its CHANGELOG.

More shipping over time.

## Why a marketplace

A marketplace makes a *suite* discoverable: one command adds every public Ellypsis plugin, current and future, and you never need to know an individual plugin's path. It is also the only route — installing a plugin repo directly no longer works, since the CLI requires a marketplace manifest on the source's default branch.

The shape follows Anthropic's own [`claude-plugins-official`](https://github.com/anthropics/claude-plugins-official): one curated catalog, `marketplace.json` at `.claude-plugin/`, a plugin listed only once it is on `main`.

## What is Ellypsis Labs

Ellypsis is a Danish AI consultancy building knowledge-work plugins for Claude. Plugin Labs is the public surface for the parts of that work that generalise — what is useful to anyone doing similar work, rather than to one organisation.

Work built for a specific client stays private, and nothing in this catalog carries a client's data, context, or identity.

Site: [ellypsis.dk](https://ellypsis.dk)

## License

MIT — see [LICENSE](LICENSE). Each plugin carries its own license file where it differs; all plugins currently in this catalog are MIT.

## Contributing

Issues and PRs are welcome here — this is the repo for both the catalog and the plugins in it. Say which plugin you mean in the title.

Test suites live at `tests/<plugin>/`, never inside `plugins/<name>/`. A plugin install copies the plugin directory verbatim, so anything kept in there ships to every user.
