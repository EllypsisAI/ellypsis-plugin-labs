<!-- Curated from the Exa vendor plugin's patterns-news.md (2026-07), trigger-hunting lens. -->

# Exa query patterns — news and recent events

News is trigger-hunting: contracts awarded, newbuilds announced, procurement windows opening. The org's research brief carries the domain trigger phrasings — combine them with these shapes. Encode time semantically ("[month year]"), calculated from today's date.

```
web_search_exa { "query": "category:news [topic] announcement", "numResults": 15 }
web_search_exa { "query": "[topic] news update latest development [month year]", "numResults": 15 }
```

**Reactions / sentiment on a recent event** — sweep angles in parallel:
```
web_search_exa { "query": "[event] reaction analysis commentary", "numResults": 12 }
web_search_exa { "query": "[event] criticism concerns issues", "numResults": 15 }
```
