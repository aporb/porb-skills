---
name: research-orchestration
description: Routing layer for all research skills — maps research tasks to the right skill, documents the full provider/API inventory, and defines chaining patterns. Load this when unsure which research skill to use.
tags: [research, orchestration, routing, meta]
related_skills: [deep-research, strategic-research, api-research, federal-contracting-research, government-disclosure-research, sbir-topic-pull, defense-policy-impact-briefing]
tier: B
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Research Orchestration

Routing layer for the 7 research skills. Use this when the task is
research-oriented but you're unsure which skill to load, or when a task
spans multiple research domains.

## Routing Map

### "Research this topic broadly"
→ **deep-research** — Multi-source fan-out engine. 5 search providers
(serper, brave-free, tavily, serpapi, perplexity). Quick mode (cheap
providers) or deep mode (iterative rounds). Output: HTML report.

### "Research this company" / "Research this person"
→ **strategic-research** — Company intelligence, professional profiling,
leadership analysis, partnership fit, outreach response drafting.
Output: HTML canvas (companies) or briefing document (people).

### "How does this API work?" / "Find a Python client for X"
→ **api-research** — API evaluation methodology: registration, auth,
rate limits, endpoints, client libraries. Includes reference docs for
federal APIs (USAspending, DSIP, NOAA, FBI, api.data.gov).

### "What contracts does X have?" / "What's coming up in Y agency?"
→ **federal-contracting-research** — USAspending awards (prime + sub),
SAM.gov entity data, procurement forecasts, LRAEs, vehicle access.
Backward-looking (awards) + forward-looking (forecasts).

### "What does this person/org earn?" / "LM-2" / "990" / "EDGAR"
→ **government-disclosure-research** — DOL LM-2 union filings, IRS 990
nonprofit compensation, SEC EDGAR corporate financials, FEC campaign
finance, lobbying LD-2/LD-1 disclosures.

### "Pull SBIR/STTR topics" / "Update sbir-portal data"
→ **sbir-topic-pull** — DSIP portal data pipeline. Pulls topic PDFs,
Q&A metadata, supplementary docs. Dedicated scripts for ingest into
the sbir-portal application.

### "How does this policy affect our portfolio?"
→ **defense-policy-impact-briefing** — Policy/budget/newsletter analysis
cross-referenced against HARBOR / Soal / SBIR Datascope. Ranked actions
with entity-specific impact assessment.

## Chaining Patterns

### Full company intelligence
1. **strategic-research** → leadership, products, market position
2. **federal-contracting-research** → awards, vehicles, forecasts
3. **government-disclosure-research** → if nonprofit/union/public company
4. **defense-policy-impact-briefing** → if defense-adjacent

### Opportunity pipeline
1. **federal-contracting-research** → backward awards + forward forecasts
2. **api-research** → if building integration with a federal API
3. **sbir-topic-pull** → if SBIR/STTR opportunities relevant

### Broad topic research
1. **deep-research** → multi-source sweep
2. **strategic-research** → if results mention specific companies/people
3. **defense-policy-impact-briefing** → if results are policy-driven

## Search Provider Inventory

### Deep-Research Engine Providers (fan-out, bypass Hermes web_search)

| Provider | Env Var | Cost/call | Capability |
|---|---|---|---|
| serper | SERPER_API_KEY | $0.001 | Search (Google SERP JSON) |
| brave-free | BRAVE_SEARCH_API_KEY | $0.00 | Search (Brave free tier) |
| tavily | TAVILY_API_KEY | $0.008 | Search (advanced, structured) |
| serpapi | SERPAPI_KEY | $0.015 | Search (Google via SerpAPI) |
| perplexity | PERPLEXITY_API_KEY | $0.010 | Synthesis (sonar model + citations) |

Engine CLI: `python3 ~/.hermes/skills/research/deep-research/scripts/engine.py`

### Hermes Runtime Providers (web_search / web_extract tools)

The tool now has a **built-in fallback chain** (`tools/web_fallback.py`). Each
provider is tried in order until one returns usable results; failed providers
are cooled down in `~/.hermes/cache/web_provider_cooldown.json` (15min for 429,
24h for 402/quota, 1h for auth, 5min for 5xx) so subsequent calls skip them
automatically.

Config in `~/.hermes/config.yaml`:
```yaml
web:
  backend: firecrawl
  extract_backend: tavily
  crawl_backend: tavily
  search_fallback_chain:
    - firecrawl
    - serper
    - brave-free
    - tavily
    - perplexity
  extract_fallback_chain:
    - firecrawl
    - tavily
```

Every response carries `_meta.attempts` describing which providers were tried
and which one answered. Inspect it when results look unexpected:

```json
{
  "success": true,
  "data": {"web": [...]},
  "_meta": {
    "provider": "serper",
    "attempts": [
      {"provider": "firecrawl", "outcome": "quota exhausted (402)", "cooled_for_s": 86400},
      {"provider": "serper",    "outcome": "ok", "results": 5}
    ]
  }
}
```

Provenance notes:
- **Firecrawl / Serper / Brave / Tavily** — raw SERP results.
- **Perplexity (last in chain)** — LLM-synthesized: row 1's `description` is
  the synthesized answer, subsequent rows are citation URLs. Treat differently
  from raw search snippets.

### Strategic-Research Direct APIs
- **Tavily** — used inline via urllib (bypasses both engine and Hermes tools)
- **ddgr CLI** — DuckDuckGo fallback (`/opt/homebrew/bin/ddgr`)

### Federal APIs (documented in api-research + federal-contracting-research)
- USAspending.gov `/api/v2/` — awards, recipients, trends
- SAM.gov — entity registration (rate-limited, 10/day free)
- DSIP `dodsbirsttr.mil/topics/api/public/` — SBIR/STTR topics
- SBA DSBS — small business certifications (no API)
- GSA eLibrary — Schedule/SIN verification
- NOAA CDO — climate data
- FBI UCR — crime statistics
- api.data.gov — federal API gateway
- ProPublica Nonprofit Explorer — IRS 990 compensation

## Fallback Behavior

**Tool-layer fallback is now automatic** (since 2026-05). The old "Firecrawl
fails → manually try ddgr → browser → Wikipedia" ladder no longer applies for
the first failure. Just call `web_search` and `web_extract` — the dispatcher in
`tools/web_fallback.py` walks the chain (firecrawl → serper → brave-free →
tavily → perplexity for search; firecrawl → tavily for extract) and cools down
providers that 429 or run out of credits.

### Reading `_meta.attempts`

Every response has a `_meta` block. Use it to:
- **Sanity-check provenance** — if `_meta.provider == "perplexity"`, expect
  synthesized prose in result[0].description, not raw snippets.
- **Diagnose slowdowns** — multiple `attempts` with non-ok outcomes means the
  first providers were tried and failed; cumulative latency adds up.
- **Decide whether to escalate** — if you see Firecrawl cooled for 86400s, the
  monthly quota is exhausted. Top up credits or wait.

### Inspecting / resetting cooldown state

```bash
cat ~/.hermes/cache/web_provider_cooldown.json   # see active cooldowns
rm  ~/.hermes/cache/web_provider_cooldown.json   # nuke all cooldowns
```

Edit the JSON to remove a single provider's entry if you've topped up credits
and want to retry it immediately.

## Last-Resort Ladder (only when ENTIRE chain exhausts)

If `web_search` returns `success: false` AND `_meta.attempts` shows every
provider in the chain failed, the chain itself is exhausted. Only then escalate:

1. **Direct URL extraction** — `web_extract` on URLs you already know.
2. **DuckDuckGo HTML via browser** — `browser_navigate` to
   `https://html.duckduckgo.com/html/?q=<query>`, click results, `browser_snapshot`.
3. **ddgr CLI** — text or image search via `ddgr --json --num N "query"`. Pipe
   to Python for structured URL extraction. See "ddgr Image & Reference Search"
   below for techniques.
4. **Google via browser** — often captchas, skip to DDG if blocked.
5. **Wikipedia raw** — `https://en.wikipedia.org/w/index.php?title=Topic&action=raw`.

Historical note: before the 2026-05 tool refactor, the agent had to climb this
ladder manually on Firecrawl's first 402. Now the chain absorbs that — only
climb when the chain itself reports total exhaustion in `_meta.attempts`.

## ddgr Image & Reference Search

Use `ddgr` for image and reference searches when visual content is the primary
goal (reference galleries, character designs, tattoo flash, product shots). The
user explicitly prefers ddgr over browser-based Bing/Google image search.

### Text search to find relevant pages

```bash
ddgr --json --num 10 "Harley Quinn Batman TAS production cel" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data[:10]:
    print(r.get('url',''))
"
```

### Extract image URLs from discovered pages via browser console

Once you find a page with good images, open it via `browser_navigate` and
extract the image URLs:

```javascript
// Unique image URLs above minimum size
JSON.stringify(Array.from(document.images)
  .filter(i => i.naturalWidth > 200)
  .map(img => img.src.substring(0,200))
  .filter((v,i,a) => a.indexOf(v)===i)
)
```

For gallery/product pages with link-based media URLs:
```javascript
JSON.stringify(Array.from(document.querySelectorAll('a[href*="mediaurl"]'))
  .slice(0,20)
  .map(a => new URL(a.href).searchParams.get('mediaurl'))
  .filter(Boolean)
  .map(u => u.substring(0,200))
)
```

### Download found images via terminal

```bash
curl -sL "<image_url>" -o ref-01.jpg
```

Or batch via Python with proper headers:
```python
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
data = urllib.request.urlopen(req, timeout=30).read()
with open(path, "wb") as f: f.write(data)
```

### Pitfalls
- **User prefers ddgr over browser** — for research searches, always try ddgr
  first. The user explicitly corrected: "why are you using bing search use
  bash 'ddgr --help'"
- **ddgr --json output is valid JSON** — pipe directly to `python3 -c "import
  sys,json;..."` for URL extraction
- **Page image selectors vary** — some sites lazy-load images. Use
  `document.images` + `naturalWidth` filter as a reliable universal approach
- **Auction sites often block curl** — use the browser to open the page, then
  extract image URLs via console
- **Production cels > fan art** — when gathering character references, original
  animation cels and official model sheets are more accurate than fan art.
  See `references/visual-reference-gathering.md` for the full workflow.
