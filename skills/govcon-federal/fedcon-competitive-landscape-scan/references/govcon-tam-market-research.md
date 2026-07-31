# GovCon Market Sizing & TAM Research Pattern

## When to Use
"Size the federal contracting enablement market," "what's the TAM for X in GovCon," "how big is the CMMC compliance market," "total federal contract spending broken down by X," "market landscape report for GovCon services."

## Overview
Combines USASpending.gov API queries + `firecrawl_agent` for autonomous multi-source research + browser navigation for supplemental data. Produces a structured markdown TAM report with cited numbers.

## Tool Reliability Matrix for GovCon Research

| Tool | Reliability | Notes |
|------|------------|-------|
| `web_search` | ⛔ **Dead** — returns `{data: {web: []}}` consistently for GovCon queries | Do not rely on |
| `web_extract` | ⛔ **Mostly dead** — fails on Bloomberg, Govtribe, LinkedIn, USASpending recipient pages, many .gov SPAs | Some Wikipedia pages work |
| `firecrawl_search` | ⚠️ **Unreliable** — 402 credit exhaustion common | Test once, fall back if fails |
| `firecrawl_agent` | ✅ **Hero tool** — works when all simpler tools fail | Autonomous browser stack, handles multi-source research, returns structured data |
| `browser_navigate` | ⚠️ **Useful for navigation pages, not data-heavy pages** | SBA, USASpending explorer, Wikipedia work; LinkedIn/SAM.gov gate content |
| USASpending API (`curl -X POST`) | ✅ **Gold standard** — always works, no auth needed | `spending_over_time`, `spending_by_award` |
| DuckDuckGo API (`api.duckduckgo.com`) | ⚠️ **Often empty** | Try once, don't rely on |

## Primary Research Workflow

### Phase 1: USASpending API — Aggregate Spending Data
Get the top-line numbers first. These endpoints are fast, reliable, and free:

```bash
# Total contract obligations by fiscal year
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_over_time/" \
  -H "Content-Type: application/json" \
  -d '{"group":"fiscal_year","filters":{"time_period":[{"start_date":"2019-10-01","end_date":"2024-09-30"}],"award_type_codes":["A","B","C","D"]}}'

# Professional services spending by NAICS 5416
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_over_time/" \
  -H "Content-Type: application/json" \
  -d '{"group":"fiscal_year","filters":{"time_period":[{"start_date":"2019-10-01","end_date":"2024-09-30"}],"award_type_codes":["A","B","C","D"],"naics_codes":["5416"]}}'
```

**Key endpoints for market sizing:**
- `spending_over_time` — aggregate spending by fiscal_year, quarter, or month. Supports NAICS, PSC, agency, and award type filters.
- `spending_by_award` — individual award rows. Use for recipient/competitor research. Requires `fields` parameter.
- `spending_by_category` — spending grouped by NAICS, PSC, agency, or recipient. Returns ranked results.

**API quirks for market sizing:**
- `award_type_codes` is REQUIRED — contracts: `["A","B","C","D"]`, IDVs: `["IDV_A"..."IDV_E"]`, grants: `["02"...]`
- `fields` is REQUIRED on `spending_by_award` — use `["Award ID"]` as minimal field for count-only queries
- NAICS filter uses 2-6 digit codes — `"5416"` matches the entire 5416xx family
- `time_period` uses `action_date` (not award start date) — this is correct behavior
- ALL USASpending endpoints require POST — GET returns 405

### Phase 2: Firecrawl Agent — Multi-Source Market Research
When web_search, web_extract, and firecrawl_search are all failing, dispatch `firecrawl_agent`:

```json
{
  "name": "mcp__firecrawl__firecrawl_agent",
  "arguments": {
    "prompt": "Detailed research prompt with specific data requests...",
    "urls": ["list", "of", "seed", "URLs"],
    "schema": { /* optional JSON schema for structured output */ }
  }
}
```

**Best practices:**
1. **Write a detailed prompt** — specify exactly what data points you need, with tables and categories
2. **Provide seed URLs** — the agent does better when directed to specific high-value sources
3. **Set a JSON schema** — for structured data extraction (optional, but helps with multi-firm comparisons)
4. **Poll every 15-30s** for 2-5 minutes — complex research takes time
5. **Run a second agent** for follow-up questions with different seed URLs if the first misses something

**Firecrawl agent is the primary fallback** when simpler tools fail. Don't try to manually scrape each source with browser/curl — one agent call can replace 10+ manual tool calls.

### Phase 3: Compile & Synthesize
Combine API data + agent results + browser-verified facts into a structured report. Standard sections for GovCon TAM reports:

1. **Total federal contract spending** — USASpending API data by fiscal year
2. **SBA procurement scorecard** — small business set-aside data from SBA.gov
3. **Specific compliance market TAM** — CMMC, CAS, FOCI, DCAA from agent research
4. **Professional services spending** — NAICS 5416 breakouts from USASpending API
5. **Comparable firms** — revenue, employees, capabilities from agent research
6. **Synthesis** — combined TAM, addressable slice, competitive positioning
7. **Market tailwinds** — regulatory catalysts, growth drivers, certification gaps

**Format:** Self-contained markdown file with tables, dollar figures (use `$` and `B`/`M` units), and source citations for every data point. Save to a durable location (`~/govcon_research/` or user-specified path).

### Phase 4 (Optional): SBA Scorecard Detail
The SBA scorecard page URLs change frequently (CMS migration). Instead of guessing PDF URLs:

1. Navigate to `https://www.sba.gov/federal-contracting/contracting-data/small-business-procurement-scorecard`
2. The page's "Scorecards" section links to "FY 2021-2025 scorecard details" — but these are anchor links that don't navigate
3. **Use firecrawl_agent** with the SBA scorecard URL as a seed — it discovered the working URL pattern: `sba.gov/.../scorecard-details?agency=GW&year=2024`

## Pitfalls

- **Don't waste time on SBA scorecard PDF URLs.** The CMS has migrated and old URLs return 404. Use the firecrawl_agent or browser-based discovery.
- **USASpending and SBA use different methodologies.** USASpending API returned $740.8B FY2024 contracts; SBA scorecard reported $638B eligible. Both are correct — they filter differently (SBA excludes non-small-business-eligible contracts).
- **`web_extract` fails silently on many .gov and commercial sites.** Bloomberg, Govtribe, USASpending recipient pages — all return "Failed to fetch url." Don't retry more than twice.
- **`firecrawl_agent` is subject to the same rate limits but has its own browser stack.** It sometimes works when `firecrawl_scrape` fails. Try it before giving up on a data source.
- **Typewriter NYT vs `hermes` spelling.** The user's firm is "HARBOR" not "Harbor" — always check entity names from canonical sources.

## Worked Example
July 2026 GovCon enablement TAM research: [govcon-enablement-tam-research.md](../../../../govcon-enablement-tam-research.md) — combined USASpending API (5 endpoints), two firecrawl_agent calls, and browser navigation to produce an 8-section market report covering $741B federal contracts, $7-13B compliance TAM, and 10+ comparable firms.