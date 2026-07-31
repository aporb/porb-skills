---
name: fedcon-competitive-landscape-scan
description: "Federal market landscape scan across target NAICS codes — map agencies spending, identify competitors, flag SDVOSB patterns, surface recompete opportunities, and benchmark competitive positioning. Uses USASpending.gov API with enriched SDVOSB detection via set_aside_type_codes filter. Outputs structured CSVs (awards + agency summary) and an analytical briefing."
triggers:
  - "scan federal market by NAICS"
  - "competitive landscape analysis GovCon"
  - "map small-dollar awards by NAICS"
  - "who's winning contracts under NAICS [codes]"
  - "SDVOSB patterns in federal spending"
  - "competitive intelligence sweep federal"
  - "USASpending market scan"
  - "agency spending breakdown by NAICS"
  - "recompete opportunities by NAICS"
  - "research competitive landscape for [solicitation number]"
  - "who are the incumbents for [opportunity]"
  - "find competitors for [RFP/BAA/NOFO]"
  - "competitive intel on [DARPA BAA / State NOFO / solicitation]"
  - strategic intelligence for federal opportunity
  - nuclear fabrication market landscape
---

# Federal Competitive Landscape Scan

## Overview

Systematic multi-NAICS competitive landscape analysis using the USASpending.gov API. Discovers which agencies are buying under target NAICS codes, which competitors are winning, what SDVOSB patterns exist, and which contracts are expiring (recompete opportunities). Produces two structured CSVs plus an analytical briefing.

Unlike `fedcon-opportunity-research` (which finds open solicitations in a date window) or `contractor-portfolio-analysis` (which analyzes one contractor's portfolio), this skill maps the ENTIRE competitive landscape across multiple NAICS codes — it answers "who's playing in this space and where should we focus?"

## When to Use

- Building a federal BD pipeline: "Show me everything under 541611 and 541519 from the last 6 months"
- **DOE/NNSA nuclear fabrication supply chain research:** "Map the nuclear fabrication market for Westerman Inc." — TerraPower Natrium, X-energy TRISO-X, Centrus enrichment, HALEU supply chain, SMR/microreactor deployment. See Mode C for web-search-based methodology (these markets are NOT in USASpending)
- **Pre-production supply chain landscape:** "What companies supply UF6 cylinders for the HALEU market?" or "Who fabricates nuclear-grade components for advanced reactors?" — markets where the spending is through DOE cooperative agreements, cost-share arrangements, and private investment, not procurement contracts
- Competitive benchmarking: "Who's winning small-dollar awards in our NAICS?"
- SDVOSB market sizing: "Which agencies award SDVOSB set-asides in our space?"
- Recompete targeting: "What contracts are expiring soon that we could chase?"
- Agency prioritization: "Which agencies spend the most in our NAICS codes?"
- Partnership/JV due diligence: "What's the competitive density in this NAICS cluster?"
- **Opportunity-specific competitive analysis:** "Research the competitive landscape for [solicitation number]" — who are the incumbents, likely competitors, and related prior awards for a KNOWN opportunity (BAA, RFP, cooperative agreement, or grant NOFO). See "Two Modes" below.

## Two Modes

### Mode A: NAICS-Wide Market Sweep (Phases 1–8)
The original pipeline — scan all awards across target NAICS codes to map the full market. Use when the question is "what's out there?" or "map our NAICS space." Follow Phases 1 through 8 below.

### Mode B: Opportunity-Specific Competitive Scan
Use when the user gives you specific solicitation numbers (e.g., "HR001126S0010" or "DFOP0018157") and wants to know who's competing for THOSE opportunities. This mode skips the NAICS sweep and instead:

1. **Extract opportunity details** — scrape the solicitation page (SAM.gov, Grants.gov, agency program page) for scope, agency, office, PM name, funding amount, vehicle type, due date, and technical areas. DARPA BAA program pages are particularly rich sources
2. **Research the PM** — search the PM's name + agency; pull their bio page; map their prior affiliations (former employers are often bidders), research interests, and professional network. For DARPA BAAs, this is the single highest-signal competitive intel source
3. **Map related/recent programs** — search for sibling/similar programs at the same agency office; identify their known performers. These groups almost always bid again. Check for proposers day attendee lists if publicly posted
4. **USAspending keyword + agency queries** — use the `keywords` filter with the agency constraint to find awards containing the program's domain terms. **Query both contract AND grant award types in separate calls** since BAAs and cooperative agreements can use either instrument. Contract codes: `["A","B","C","D"]`. Grant/cooperative agreement codes: `["02","03","04","05"]`. See "Award Type Codes Reference" below
5. **Incumbent identification** — from USAspending results and web research, identify recurring awardees in the relevant program area. Cross-reference with trade press (OrangeSlices, GovCon Wire, Shephard Media, FedScoop) and company websites for contract vehicle details (ceiling values are often 50x+ the obligation amount)
6. **Parallel web search** — run 4–6 simultaneous searches for: (a) program performers/contractors, (b) PM background and prior affiliations, (c) related program awardees, (d) small business/SDVOSB award patterns at the agency office, (e) trade press coverage, (f) Proposers Day / industry day announcements
7. **Competitive assessment** — tier the likely competitors. For each: classify as large prime, university, FFRDC/UARC, mid-tier R&D firm, small business, or nonprofit; assess their incumbency strength; note their likely teaming posture (primes, subs, 1099 SMEs)
8. **Strategic recommendation** — assess winnability on a VERY LOW → LOW → MODERATE → GOOD scale; recommend prime vs subcontractor posture; identify concrete teaming partner targets and JV structures; flag timeline pressure (e.g., 35-day window from posting to deadline)

**Mode B output:** A structured markdown briefing (not CSVs) saved to `~/govcon_research/<project>/competitive-landscape.md` covering: opportunity summary table, PM intelligence, competitive landscape with tiered threat assessment, related programs table, USAspending award data, teaming opportunity matrix, and strategic assessment with concrete next steps.

**Mode B pitfall — DARPA BAAs are NOT standard federal contracts:** DARPA selects performers based on scientific merit and PI credentials, not past performance or price. A small business without published AI research or a named PI with DARPA credentials has near-zero chance of winning TA1+TA2 prime on a first DARPA BAA. Be honest about this. The realistic play is TA3 (T&E, competed separately), subcontractor to a university prime, or SBIR/STTR as a credential-building step.

### Mode C: Pre-Production Supply Chain Landscape Scan (Web-Search Based)

Use this mode when the target market does not flow through standard federal procurement contracts tracked by USASpending.gov — i.e., **pre-production supply chains, DOE/NNSA nuclear fabrication, advanced reactor fuel supply, ARDP cost-share agreements, DOE cooperative agreements, private investment-driven buildout, and military installation procurement through DIU/ANPI** rather than traditional contracting vehicles.

This market is **not captured by USASpending API awards** because most spending is:

- DOE cooperative agreements and cost-share arrangements (ARDP) — not standard contracts
- Private capital raising (Centrus $1.2B convert notes, Amazon $500M in X-energy, Anduril $61B valuation)
- NNSA direct M&O contracts to primes (Bechtel/Floor at SRS, Hanford, Y-12)
- DIU/ANPI OTA awards for military microreactors
- Pre-revenue venture-funded companies (Radiant Nuclear)

**Methodology:**

1. **Identify market scope** — List the key programs, entities, and DOE/NNSA initiatives in the target space (e.g., TerraPower Natrium, X-energy TRISO-X, Centrus enrichment, HALEU allocation, SRPPF, Sentinel, WTP)
2. **Split into 5-7 parallel subtopic searches** — Each subtopic gets its own `web_search` call. Use company names + program names + data points (cost, date, milestone). Run all searches concurrently
3. **Extract structured data per entity** — For each company/program: program details, cost figures, timeline, key personnel, supply chain position, certifications, and subcontracting channels (see `references/doe-nnsa-nuclear-market.md` for the full entity/domain reference)
4. **Cross-reference claims** — "DOE awarded $2B" may actually mean "$2B cost-share (50% DOE + 50% private)" — check the source document
5. **Map supply chain position** — Identify where prime contractors (Bechtel, Fluor, Northrop Grumman) need subcontractors/vendors; identify sole-source positions (Westerman = only domestic UF6 cylinder manufacturer)
6. **Compile structured report** — Multi-section markdown with: landscape overview, per-project deep dives, prime contractor analysis, supplier positioning, strategic implications, key contacts. For internal intelligence, markdown is acceptable. For client-facing deliverables, convert to self-contained HTML (see `html-briefing` skill)

**Pitfalls:**
- DOE cooperative agreements DO NOT appear in USASpending.gov — don't waste time querying the API
- "Billion" vs "million" rounding in trade press — always verify from the primary source
- Program delays are the norm — assume advanced reactor timelines will slip 2-4 years from initial announcements
- Private companies (Westerman, Radiant) have no SEC filings — all data comes from press releases, LinkedIn, DOE RFI responses
- Some company names have heavy search noise — use "Westerman Inc" not "Westerman" (which returns a UK musician)

**Domain reference:** See `references/doe-nnsa-nuclear-market.md` for the complete DOE/NNSA nuclear fabrication market entity database, key contacts, supply chain matrix, and research methodology.

### Award Type Codes Reference

| Category | Codes | Use For |
|----------|-------|---------|
| Contracts | `A`, `B`, `C`, `D` | Standard federal contracts, task orders, delivery orders, purchase orders |
| IDVs | `IDV_A`, `IDV_B`, `IDV_B_A`, `IDV_B_B`, `IDV_B_C`, `IDV_C`, `IDV_D`, `IDV_E` | Indefinite delivery vehicles (GWACs, IDIQs, BPAs) |
| Grants | `02`, `03`, `04`, `05` | Block grants, formula grants, project grants, cooperative agreements |
| No `G` or `IDV` | These literal strings are INVALID — the API returns 422 |

⚠ **Critical:** When researching an opportunity that could be either a contract OR a cooperative agreement (DARPA BAAs, State Dept NOFOs), query ALL applicable types in separate calls. A program may have prior awards as contracts even if the current opportunity is a cooperative agreement, or vice versa. Querying only one type produces an incomplete competitive picture.

## Prerequisites

- USASpending.gov API is public (no key needed)
- `~/govcon_research/` as workdir with `csv/` subdirectory for outputs
- Python 3 with `requests` library (available by default)
- No SAM.gov or Firecrawl credits needed — pure API pipeline

## Workflow

### Phase 1: Define the Scan Parameters

```
NAICS codes: ["541611", "541519", "611430", "541618", "541690"]
Competitors: ["GOVSMART", "V3GATE", "FCN", ...]
Date window: last 180 days
Award band: $0–$500K
```

Confirm each parameter with the user. The date window is a HARD constraint — only awards with action dates inside it.

### Phase 2: Query by NAICS Codes

For each target NAICS code, query `spending_by_award` separately for contracts (`A`, `B`, `C`, `D`) and IDVs (`IDV_A` through `IDV_E`). The API REQUIRES `award_type_codes` and does NOT allow mixing contract types with IDV types in a single query.

See `scripts/sweep-by-naics.py` for the reusable query script.

**Critical API quirks (all discovered 2026-07-18):**

- `award_type_codes` is REQUIRED — the API returns 422 without it. Contracts and IDVs are separate award groups; query each with its own call.
- The field name for NAICS in the response is `NAICS` (not `NAICS Code`), and for PSC it's `PSC` (not `Product or Service Code (PSC)`). These return as OBJECTS `{code: "541611", description: "ADMINISTRATIVE MANAGEMENT..."}`, not flat strings.
- `time_period` uses `action_date` (most recent modification date), NOT award start date. This means competitor searches return old contracts that had recent mods. This is correct behavior — they're active.
- `page_metadata.total` may show 0 even when results exist — rely on `hasNext` for pagination, not `total`.
- `spending_level` defaults to `"awards"` — set it explicitly if needed.

**Pagination:** The API returns max 100 results per page. Loop pages until `hasNext` is `false`. Use `max_pages=15` per NAICS code and `max_pages=5` per competitor to keep queries bounded while catching the tail.

### Phase 3: Query by Competitor Names

Search for each known competitor using `recipient_search_text`. The same contract/IDV split applies. Competitor searches use the same `time_period` and `award_amounts` filters if you want bounded results, or leave them open for full portfolio discovery.

**⚠ Competitor searches return awards across ALL NAICS, not just target ones.** This is intentional — you want the full competitive picture. The resulting CSV will contain non-target NAICS codes (e.g., 334111 Electronic Computer Manufacturing, 513210 Software Publishers) from competitor work. Tag the `source_query` field so you can filter later.

### Phase 4: SDVOSB Enrichment

**⚠ PITFALL: `spending_by_award` does NOT return set-aside fields in results.** The `Set Aside`, `Type of Set Aside`, and `Extent Competed` fields are ALWAYS null in the response. The API supports `set_aside_type_codes` as an INPUT filter but does not expose these fields in the OUTPUT.

**Workaround:** Run a SEPARATE sweep for each NAICS with `"set_aside_type_codes": ["SDVOSBC", "SDVOSB"]` in the filter. Collect all returned award IDs, then cross-reference against the master dataset. Any award that appears in the SDVOSB-filtered query is an SDVOSB award.

This requires running the full NAICS query pipeline TWICE — once without set-aside filter (all awards), once with (SDVOSB awards only). Use `max_pages=10` for the SDVOSB sweep since the volume is lower.

See `scripts/enrich-sdvosb.py` for the cross-referencing script.

### Phase 5: Extract and Structure

Flatten the API response into a CSV with these columns at minimum:

```
award_id, recipient_name, recipient_uei, award_amount, awarding_agency,
awarding_sub_agency, naics_code, naics_description, psc_code, psc_description,
start_date, current_end_date, last_date_to_order, description,
award_type, contract_award_type, is_sdvosb, source_query
```

Extract NAICS and PSC from their nested objects: `naics.get("code", "")` / `naics.get("description", "")`.

See `templates/landscape-scan-script.py` for the full extraction template.

### Phase 6: Build Agency Summary

Roll up by awarding agency:

| agency_name | total_spending | num_awards | avg_award_size | sdvosb_award_count | sdvosb_spending | sdvosb_pct | naics_codes | psc_codes |
|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | $132.8M | 895 | $148K | 442 | $57.9M | 49.4% | 541519,541611,... | R408,R425,... |

Sort by `total_spending` descending. Add PSC codes (top 10 per agency) for additional targeting context.

### Phase 7: Surface Key Patterns

From the structured data, extract actionable intelligence:

1. **Top agencies by spending** — where's the money concentrated?
2. **Top recipients (competitors)** — who's winning the most?
3. **SDVOSB distribution** — which agencies are SDVOSB-friendly? (VA leads heavily at ~49%)
4. **SDVOSB competitors** — which known competitors hold SDVOSB status? (REDHAWK, THUNDERCAT, V3GATE)
5. **Recompete opportunities** — awards with `current_end_date` before Dec 2026, filtered to ≥$100K for actionable targets
6. **Competitor recompete exposure** — which competitors have contracts expiring soon?

### Phase 8: Output

Deliver two files to `~/govcon_research/csv/`:

1. `usaspending_small_dollar_awards.csv` — every award row (typically 10K–15K rows for 5 NAICS + 11 competitors)
2. `usaspending_agency_summary.csv` — agency-level rollup (typically 50–70 agencies)

Present findings as a structured summary covering agencies, competitors, SDVOSB patterns, and recompete opportunities. The CSV files are self-service for filtering and deeper analysis.

## Pitfalls

- **`award_type_codes` is REQUIRED.** The API returns 422 without it. Mixing contract types (A–D) with IDV types (IDV_A–E) in one query also returns 422 — use separate queries. The literal strings `"G"` and `"IDV"` are INVALID — grants use numeric codes `"02"` through `"05"` (see Award Type Codes Reference above)
- **NAICS and PSC are nested objects, not strings.** `award["NAICS"]` → `{code: "541611", description: "..."}`. Extract with `.get("code")`, not as a raw field.
- **Set-aside fields are always null in `spending_by_award` responses.** SDVOSB detection requires a separate query with `set_aside_type_codes` filter and cross-referencing award IDs. This is a USASpending API design limitation, not a data error.
- **`page_metadata.total` is unreliable.** It may show 0 even when results exist and `hasNext` is true. Always paginate by `hasNext` — stop when it's `false` or when the results array is empty.
- **`recipient_search_text` returns all awards for those recipients across ALL NAICS.** Expect non-target NAICS codes in the output. Tag rows with `source_query` to distinguish NAICS-filtered results from competitor-name results.
- **`time_period` uses `action_date`, not award start date.** Competitor searches will return old contracts that had recent modifications (e.g. 2012 awards with 2026 mods). These ARE active contracts — do not filter them out based on old `current_end_date`. The real signal is the expiring list (end date in 2026).
- **Competitor name matching is fuzzy.** `recipient_search_text: ["BLUE TECH"]` matches "BLUE TECH INC." but also "BLUE TECHNOLOGY SOLUTIONS LLC". Scan results for false positives and exclude them if needed.
- **NASA SDVOSB spending may show $0.** IDV ceiling values are not captured as award amounts. Don't disregard NASA as an SDVOSB buyer just because the spending column is empty — the award count tells the real story.
- **`award_amounts` filter combined with `naics_codes` + `time_period` returns 0 results.** The USASpending API's amount filter is too restrictive when combined with NAICS and date filters — querying NAICS 541519 + sub-$500K + last 180 days returned 0 results, but removing the amount filter returned 50. **Fix:** Query without amount caps, then filter locally in Python (`[r for r in results if (r.get('Award Amount') or 0) < 500000]`). Sort ascending (`order: \"asc\"`) to surface the smallest awards first rather than pulling page after page of top-dollar results. For targeted small-award discovery across multiple NAICS, use the single-token keyword strategy from `fedcon-opportunity-research` — keyword queries return smaller, more relevant result sets.
- **Don't use `firecrawl_scrape` on the USASpending API.** It's a POST endpoint and firecrawl GETs it, returning empty. Always use `requests.post()` in Python or `curl -X POST` in terminal.
- **`cfda_numbers` filter is SILENTLY IGNORED on `spending_by_award`.** The API accepts the filter but drops it (the response message logs: "The following filters from the request were not used: {'cfda_numbers'}") and returns ALL awards for the agency, not just the targeted assistance listing. This is particularly dangerous because it LOOKS like it worked — you get results, but they're the wrong results. **Fix:** Use `agencies` filter by toptier name (e.g., `{"type": "awarding", "tier": "toptier", "name": "Small Business Administration"}`) instead of `cfda_numbers`. You may still need to filter by award amount or description keywords locally after retrieval.
- **`keywords` filter is unreliable for grant/prize award searches on `spending_by_award`.** SBA OII's Growth Accelerator Fund Competition (GAFC) prizes are NOT standard federal awards — they're prize competitions, not grants/contracts. The `keywords` filter returned zero results for "Growth Accelerator", "GAFC", "OII", and "accelerator" when querying SBA grants. If a keyword search returns empty or unrelated results, the award type may not be in USASpending at all. **Fix:** For SBA OII prize competitions, GAFC, and similar non-standard awards, abandon USASpending and research via (a) SBA.gov press releases (search "SBA announces Growth Accelerator Fund Competition winners"), (b) americasseedfund.us/accelerators (the SBA OII public directory), (c) third-party aggregators like SSTI (ssti.org) that maintain independent winner tracking. See `references/sba-oii-grant-research.md` for the full alternative-source methodology.

## Output Files

- `~/govcon_research/csv/usaspending_small_dollar_awards.csv` — individual awards (12K+ rows)
- `~/govcon_research/csv/usaspending_agency_summary.csv` — agency rollup (60+ rows)
- `~/govcon_research/query_usaspending.py` — primary extraction script (see `scripts/sweep-by-naics.py` for reusable version)
- `~/govcon_research/enrich_sdvosb.py` — SDVOSB cross-referencing script

- **For SBA OII grant/prize competition intelligence (GAFC, SCALE, etc.), skip USASpending entirely.** See `references/sba-oii-grant-research.md` for the full alternative-source methodology — USASpending does not index these awards.

## Related Skills

- **`fedcon-opportunity-research`** — Finding open solicitations and new opportunities. Complementary: this skill maps the existing competitive landscape; that skill finds what's available to bid NOW.
- **`contractor-portfolio-analysis`** — Deep-dive a single contractor's portfolio. This skill does the opposite: maps all competitors across NAICS codes at once.
- **`govcon-partnership-assessment`** — Side-by-side GovCon entity comparison. Use after this scan when you've identified specific competitors/partners.
- **`references/content-competitive-intel.md`** — Content/voice competitive intelligence methodology (sibling to this skill). Use when the task is analyzing who covers what in a thought-leadership topic space, identifying coverage gaps, and positioning — NOT federal contract data. Covers JSON-LD extraction from known URLs, voice landscape mapping, coverage gap analysis, structured 8-question report format, and competitive risk assessment.

## GovCon TAM & Market Sizing

When the user asks "size the market," "what's the TAM," or "how big is X in federal contracting," this is a different workflow from opportunity discovery or competitive scanning. Load `references/govcon-tam-market-research.md` for:

- **Tool reliability matrix** — which tools work (USASpending API, firecrawl_agent, browser) and which don't (web_search, web_extract, firecrawl_search) for GovCon data
- **USASpending `spending_over_time` endpoint** — aggregate spending by fiscal year with NAICS/PSC/agency filters
- **Firecrawl agent as primary fallback** — when simpler tools fail, one agent call replaces 10+ manual scrape attempts
- **SBA scorecard data extraction** — CMS URLs change; use agent for discovery
- **Synthesis report format** — 8-section markdown: spending data, scorecards, compliance TAM, professional services, comparable firms, synthesis, tailwinds

## Worked Example

See `references/naics-sweep-example-2026-07-18.md` for the full 12,454-award scan across 5 NAICS codes and 11 competitors that produced the patterns above.