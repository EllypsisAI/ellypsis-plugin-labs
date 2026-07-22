# Connectors

`.mcp.json` declares both servers by URL. The gateway authenticates per user via OAuth at
connect time. Exa's endpoint is keyless in the manifest by design — the API key is each
client's own, added at workspace connect time (BYO key vs proxy is the per-client auth
variance, pinch #11); a key never belongs in a public plugin manifest.

## Ellypsis gateway — required

The one connection this plugin depends on. It brings:

- Core tools: brain logging/search, workspace status.
- The served bodies the skills fetch: research brief, CRM pack, company voice guide, org context.
- The per-company CRM satellite (each org's own CRM), via per-user OAuth.

**Degraded mode (gateway not connected):**

| Skill | Behavior |
|-------|----------|
| crm | Stop before any read or write. Never improvise CRM operations from raw tool schemas. |
| outreach | Never draft — the voice guide is a precondition, not an enhancement. |
| contacts | Searching may proceed; say clearly that results are unchecked against the CRM (no dedup, no history). |
| research | Say the brief is unavailable; offer method-only research explicitly labeled as generic. |

## Exa — research engine

Research runs on Exa (standardized fleet-wide; per-client variance is auth/billing only —
BYO key vs proxy, pinch #11). Connected per workspace by the client.

**Degraded mode:** fall back to whatever search tools the surface provides and say the
research craft references don't fully apply; if none exist, report the gap instead of guessing.
