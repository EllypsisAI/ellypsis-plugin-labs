<!-- Curated from the Exa vendor plugin's patterns-relationships.md (2026-07), sales-intelligence lens. -->

# Exa query patterns — hidden relationships

Who they build for, buy from, partner with. Direct queries ("[company] clients") return articles *about* them, not actual connections — use indirect signals.

**Start with the subject's own platforms:**
```
web_search_exa { "query": "[subject] official website blog podcast", "numResults": 5 }
web_search_exa { "query": "[subject] conversation interview testimonial guest", "numResults": 8 }
web_fetch_exa { "urls": ["https://subject.com/blog", "https://subject.com/about"] }
```

**B2B, company → customers:**
```
web_search_exa { "query": "[company] case study customer success story", "numResults": 5 }
web_fetch_exa { "urls": ["https://company.com/customers", "https://company.com/case-studies"] }
```
In industrial B2B the case-study equivalents are reference lists and delivery announcements — "delivered to", "in service with", "built for" — plus the partner/supplier mentions on the *end client's* project news (the org's research brief carries the domain phrasings).

**Indirect signals:**
```
// Testimonials
web_search_exa { "query": "personal blog [subject] changed my life testimonial", "numResults": 15 }

// Duration markers — high confidence; people don't fabricate decades
web_search_exa { "query": "[subject] years decades longtime worked with known since", "numResults": 10 }

// Terminology detection: find insider terms, then search for people using them
web_search_exa { "query": "[subject] method terminology concepts framework", "numResults": 5 }
web_search_exa { "query": "[unique term 1] [unique term 2] personal story", "numResults": 10 }
```
