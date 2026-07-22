# Connectors

`.mcp.json` declares all three servers by URL. The gateway and the CRM satellite
authenticate per user via OAuth at connect time. Exa's endpoint is keyless in the manifest
by design — the API key is each client's own, added at workspace connect time (BYO key vs
proxy is the per-client auth variance, pinch #11); a key never belongs in a public plugin manifest.

## Ellypsis gateway — required

The connection this plugin's knowledge depends on. It brings:

- Core tools: brain logging/search, workspace status.
- The served bodies the skills fetch: research brief, CRM pack, company voice guide, org context.

**Degraded mode (gateway not connected):**

| Skill | Behavior |
|-------|----------|
| crm | Stop before any read or write. Never improvise CRM operations from raw tool schemas. |
| outreach | Never draft — the voice guide is a precondition, not an enhancement. |
| contacts | Searching may proceed; say clearly that results are unchecked against the CRM (no dedup, no history). |
| research | Say the brief is unavailable; offer method-only research explicitly labeled as generic. |

## CRM satellite — the CRM toolset

The CRM's tools arrive through a dedicated satellite server, per-user OAuth **direct** —
deliberately not gateway-proxied, so every write lands as the logged-in salesperson. The
declared satellite serves Capsule; a client on a different CRM gets that CRM's satellite
here instead. The crm skill stays CRM-agnostic — the gateway-served CRM pack teaches
whichever CRM the satellite exposes.

**Degraded mode (satellite not connected):** the crm skill stops before any read or write;
contacts flags results as unchecked against the CRM; outreach skips the history lookup and
says follow-up context may be missing.

## Exa — research engine

Research runs on Exa (standardized fleet-wide; per-client variance is auth/billing only —
BYO key vs proxy, pinch #11). Connected per workspace by the client.

**Degraded mode:** fall back to whatever search tools the surface provides and say the
research craft references don't fully apply; if none exist, report the gap instead of guessing.
