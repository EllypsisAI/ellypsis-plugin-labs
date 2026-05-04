# Changelog

## [0.1.0] - 2026-05-03

Initial public release. Ellypsis Plugin Labs marketplace established.

### Catalog
- Added `mcp-eval` (v0.2.0) - evaluate MCP servers for production readiness. Sourced from [EllypsisAI/mcp-eval](https://github.com/EllypsisAI/mcp-eval), tracking `main`.

### Architecture
The marketplace follows the hybrid pattern from `anthropics/claude-plugins-official`: each listed plugin lives in its own dedicated GitHub repo and is referenced from `marketplace.json` via the `url` source type. This keeps per-plugin issue trackers, READMEs, and release cadences independent while giving users a single curated install path.

Marketplace `name` is `ellypsis-labs` (the namespace users type with `@`); the repo is `EllypsisAI/ellypsis-plugin-labs`. The two diverge intentionally - the repo URL is descriptive, the namespace is brand-forward.
