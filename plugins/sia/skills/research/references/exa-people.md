<!-- Curated from the Exa vendor plugin's people query patterns (2026-07), contact-finding lens. -->

# Exa query patterns — people

Use `category:people` for LinkedIn-weighted results. Be specific — a vague people query ("category:people founder CEO startup") matches thousands of irrelevant profiles. Anchor with a company, role, or region.

```
// By company + role
web_search_exa { "query": "category:people [role] at [company]", "numResults": 10 }

// By role + region (no known company)
web_search_exa { "query": "category:people [role] [industry] [region]", "numResults": 12 }

// Specific person
web_search_exa { "query": "category:people [name] [company] [specialty]", "numResults": 5 }
```

**Comprehensive company coverage** — sweep departments and seniority in parallel:

```
web_search_exa { "query": "category:people operations fleet at [company]", "numResults": 10 }
web_search_exa { "query": "category:people procurement technical at [company]", "numResults": 10 }
web_search_exa { "query": "category:people management director at [company]", "numResults": 10 }
```

**Supplement beyond LinkedIn** — directories miss senior people:

```
web_search_exa { "query": "[company] team page employees about us", "numResults": 5 }
web_search_exa { "query": "joined [company] recently hired new role announcement", "numResults": 5 }
```

Conference speaker lists, industry associations, and press releases also surface names the directory hides.

**Role adjacency** — organizations title the same job differently. If the named role misses, sweep adjacent titles in parallel (fleet manager ↔ operations director ↔ technical superintendent; procurement manager ↔ purchasing ↔ supply chain) rather than concluding the role doesn't exist.

**Verify a specific person** — LinkedIn-weighted results go stale; confirm current employment before the person counts:

```
web_search_exa { "query": "category:people [name] [current company]", "numResults": 5 }
web_search_exa { "query": "[name] [company] interview appointed joins", "numResults": 5 }
```

**Where emails actually live:** team pages, press releases, conference programs and PDFs, signature blocks in published correspondence. An email is evidence-backed or it's absent — never constructed from a name pattern unless explicitly asked, and then clearly marked a guess. Carry a confidence level with every address.

**Deduplicate** by LinkedIn URL (canonical), else name + current company. The org's research brief and segment guides name which roles matter — weight the sweep accordingly.
