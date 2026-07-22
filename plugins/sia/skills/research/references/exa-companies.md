<!-- Curated from the Exa vendor plugin's company query patterns (2026-07), sales-intelligence lens. -->

# Exa query patterns — companies

Use `category:company` for structured company data (description, headcount, funding, location).

```
// By space + region
web_search_exa { "query": "category:company [space] companies [region]", "numResults": 10 }

// Similar to a known company
web_search_exa { "query": "category:company companies like [known player]", "numResults": 8 }
```

**Competitive / landscape sweeps** — layer angles in parallel, one subagent each or batched:

```
web_search_exa { "query": "category:company companies like [target]", "numResults": 10 }
web_search_exa { "query": "category:company [category] providers", "numResults": 15 }
web_search_exa { "query": "[category] contract awarded announcement recently", "numResults": 15 }
```

**Company deep-dive** — pair the structured record with news:

```
web_search_exa { "query": "category:company [company]", "numResults": 5 }
web_search_exa { "query": "[company] contract project announcement", "numResults": 10 }
```

The org's research brief supplies the domain vocabulary (segment phrasings, trigger terms, trade-press domains) — combine its phrasings with these shapes.
