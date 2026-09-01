# Changelog

## [0.3.0] - 2026-09-01

### Catalog
- Added `brand-kit` **v0.2.2** — takes a startup from nothing to a usable visual identity: an interview builds the brand foundation, visual brainstorming turns taste into something you can point at, and the kit assembles what you locked into files you can use.
- Added `not-ai-slop` **v0.2.1** — turns a post or article into a carousel whose visuals don't announce themselves as generated: a slide plan you approve first, backgrounds prompted by process rather than by style adjective, and an editable slide file alongside the PDF.
- `mcp-eval` **v1.0.3** — fully synthetic fixtures and worked examples; test suite moved out of the packaged plugin directory.

## [0.2.0] - 2026-08-18

### Catalog
- `mcp-eval` **v1.0.0** — full rebuild. Evaluates an MCP server *paired with the LLM that will drive it*: sub-agents run realistic tasks against the connected server while hooks capture the trajectory, then a verdict-first HTML dashboard reports discoverability, argument fidelity, payload economics, latency, reliability and grounding. Supersedes v0.2.0, whose bespoke Python MCP client measured a client that does not exist in production.
- Removed `scout` — no longer public.

### Architecture
Plugins now live **inline** at `plugins/<name>/` and are referenced with `"source": "./plugins/<name>"`. This supersedes the url-source hybrid described under 0.1.0.

The hybrid split development from publication: a plugin's working tree lived in one repo while the catalog lived in another, and the two drifted. One repo, one working tree, one truth — development happens where the plugin is published. This also matches the shape already proven for private per-client marketplaces.

Retired standalone repos (`EllypsisAI/mcp-eval`, `EllypsisAI/scout`) are private and archived.

## [0.1.0] - 2026-05-03

Initial public release. Ellypsis Plugin Labs marketplace established.

### Catalog
- Added `mcp-eval` (v0.2.0) - evaluate MCP servers for production readiness. Sourced from [EllypsisAI/mcp-eval](https://github.com/EllypsisAI/mcp-eval), tracking `main`.

### Architecture
The marketplace follows the hybrid pattern from `anthropics/claude-plugins-official`: each listed plugin lives in its own dedicated GitHub repo and is referenced from `marketplace.json` via the `url` source type. This keeps per-plugin issue trackers, READMEs, and release cadences independent while giving users a single curated install path.

Marketplace `name` is `ellypsis-labs` (the namespace users type with `@`); the repo is `EllypsisAI/ellypsis-plugin-labs`. The two diverge intentionally - the repo URL is descriptive, the namespace is brand-forward.
