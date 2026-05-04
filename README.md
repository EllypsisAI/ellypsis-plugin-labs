# Ellypsis Plugin Labs

The public marketplace for plugins from Ellypsis Labs. One install, every Ellypsis plugin available on demand — for Claude Code and Cowork.

## What's in here

This repo is a thin catalog. The plugin code itself lives in dedicated repos under `EllypsisAI/`; this marketplace.json points to each of them. Each plugin is independently installable, separately versioned, and has its own README and issue tracker.

| Plugin | Repo | What it does |
|---|---|---|
| `mcp-eval` | [EllypsisAI/mcp-eval](https://github.com/EllypsisAI/mcp-eval) | Evaluate MCP servers for production readiness — test tools, measure token costs, grade responses, generate visual reports. |

More plugins shipping over time as Ellypsis Labs builds them.

## Install

In Claude Code:

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install mcp-eval@ellypsis-labs
```

After adding the marketplace once, browse and install any plugin in the catalog with `@ellypsis-labs`. Run `/plugin marketplace update` to pull new additions.

## Why a marketplace at all

A single-plugin repo can be installed directly via `/plugin marketplace add EllypsisAI/<plugin>`. The marketplace layer exists to make a *suite* discoverable: one command adds every Ellypsis Labs plugin at once, current and future. As the catalog grows, you don't need to know each plugin's repo URL — just `/plugin install <name>@ellypsis-labs`.

The pattern follows Anthropic's own [`claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) marketplace: one curated catalog, plugins live in their own repos, marketplace.json references them via `git-subdir`/`url` sources.

## What is Ellypsis Labs

Ellypsis is a Danish AI consultancy that ships knowledge-work plugins for Claude — content strategy, sales intelligence, ERP consulting, productivity. Plugin Labs is the public surface for the generic, reusable parts of that work.

Client-specific plugins (custom CRM integrations, proprietary domain knowledge) stay in private repos by design. What you see here is what's general enough to ship publicly, MIT-licensed, and intended for anyone doing similar work.

Site: [ellypsis.dk](https://ellypsis.dk)

## License

Marketplace metadata: MIT — see [LICENSE](LICENSE).

Each linked plugin has its own license; check the plugin's repo. All plugins currently in this catalog are MIT.

## Contributing

Issues and PRs about a specific plugin go on that plugin's own repo. Issues about the marketplace itself (catalog metadata, install flow, missing plugins you want listed) go here.
