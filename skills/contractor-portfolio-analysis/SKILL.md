---
name: contractor-portfolio-analysis
description: "Deep-dive a specific federal contractor's full contract portfolio — every award, expiration timeline, renewal risk assessment, and strategic insights. Uses USAspending.gov API as primary data source, supplemented by company website, news, and SAM.gov secondary sources. Produces self-contained HTML briefing with revenue trends, lost/expiring/at-risk contract tables, and renewal likelihood analysis."
triggers:
  - "analyze contractor portfolio"
  - "what contracts does [company] have"
  - "contract awards for [company]"
  - "what's expiring for [company]"
  - "contract renewal likelihood"
  - "contract intelligence briefing for [company]"
  - "competitive contractor analysis"
  - "federal contract portfolio"
  - "contract cliff analysis"
---

# Contractor Portfolio Analysis

## Overview

Systematic analysis of a specific federal contractor's complete contract portfolio using USAspending.gov API as the backbone. Discovers every contract award, maps expiration timelines, identifies lost/reduced/at-risk revenue, and assesses renewal likelihood for upcoming expirations. Delivers as a self-contained HTML briefing.

**Also handles brand-new entity research** — when USAspending returns zero results for all name variants, shift to Entity Establishment Intelligence Briefing covering registration status, website maturity, domain history, SBA/VA certifications, leadership credibility, and competitive positioning.

## When to Use

- User asks to analyze a specific company's federal contract portfolio
- Competitive intelligence on a rival contractor
- Due diligence before acquisition, partnership, or JV
- Assessing a company's revenue stability and growth trajectory
- "What contracts has [company] won/lost this year?"
- Renewal risk assessment for upcoming contract expirations
- Researching a newly registered GovCon LLC with no federal awards yet

## Prerequisites

- USAspending.gov API is public (no key needed)
- `~/govcon_research/raw/<company>/` for raw data
- HTML briefing output to `/data/nextcloud/data/amyn/files/briefings/`
- Python/jq for JSON parsing
- `ddgr` CLI as fallback when Firecrawl web_search/web_extract exhausts credits
- Wayback CDX API for domain history (`web.archive.org/cdx/search/cdx`)

## Workflow

### Phase 1: Company Identification

Identify the company's legal name and DBA. Federal records use the legal name, but the company may be known by a DBA.

```bash
# Search USAspending autocomplete to find exact legal entity name
curl -s -X POST "https://api.usaspending.gov/api/v2/autocomplete/recipient/" \
  -H "Content-Type: application/json" \
  -d '{"search_text": "Company Name", "limit": 10}' | jq '.results'
```

⚠ **Pitfall:** The DBA name may not appear in USAspending at all. Search using the legal name. For example, "Navaide" returns 0 results but "Red River Resources" returns 4 variants.

**Brand-new entity signal:** When autocomplete returns zero results for all name variants (legal name, DBA, shorthand), the entity either has no prime awards yet or is not yet SAM-registered. Immediately shift to Entity Establishment mode (see Phase 5e below).

### Phase 2: Contract Award Discovery

Pull all contract awards using `spending_by_award`. Use the legal name variant that matches USAspending records.

```bash
# All contract awards for a time period
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Legal Name"],
      "time_period": [{"start_date": "2020-01-01", "end_date": "2026-12-31"}],
      "award_type_codes": ["A", "B", "C", "D"]
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount", "Description",
               "Start Date", "End Date", "Awarding Agency", "Awarding Sub Agency",
               "Contract Award Type", "generated_internal_id"],
    "page": 1, "limit": 100, "sort": "Award Amount", "order": "desc"
  }' | jq '.results[] | {id: .generated_internal_id, amount: ."Award Amount",
         desc: ."Description", start: ."Start Date", end: ."End Date",
         agency: ."Awarding Sub Agency"}'
```

**Valid award_type_codes for contracts:** `A` (Definitive Contract), `B` (Purchase Order), `C` (Delivery Order), `D` (Task Order).

⚠ **Critical Pitfall:** `"IDV"` is NOT a valid award_type_code for the `spending_by_award` endpoint. It will return a validation error. Use the granular codes: `IDV_A`, `IDV_B`, `IDV_B_A`, `IDV_B_B`, `IDV_B_C`, `IDV_C`, `IDV_D`, `IDV_E` if you need IDV data, or simply use `A`, `B`, `C`, `D` for contract awards.

### Phase 3: Revenue Trend Analysis

Get year-by-year obligation totals to see growth/decline trajectory:

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_over_time/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2019-01-01", "end_date": "2026-12-31"}],
      "award_type_codes": ["A", "B", "C", "D"]
    }, "group": "fiscal_year"
  }' | jq '.results[] | {fy: .time_period.fiscal_year, amount: .aggregated_amount}'
```

### Phase 4: Spending Breakdown by Category

Get revenue distribution by agency and NAICS code:

```bash
# By agency
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_category/awarding_agency/" \
  -H "Content-Type: application/json" \
  -d '{"filters": {"recipient_search_text": ["Company Name"],
    "time_period": [{"start_date": "2019-01-01", "end_date": "2026-12-31"}],
    "award_type_codes": ["A", "B", "C", "D"]}, "limit": 10}' \
  | jq '.results[] | {name: .name, amount: .amount}'

# By NAICS code
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_category/naics/" \
  -H "Content-Type: application/json" \
  -d '{"filters": {"recipient_search_text": ["Company Name"],
    "time_period": [{"start_date": "2019-01-01", "end_date": "2026-12-31"}],
    "award_type_codes": ["A", "B", "C", "D"]}, "limit": 15}' \
  | jq '.results[] | {code: .code, name: .name, amount: .amount}'
```

### Phase 5: Contract Detail Extraction

For each significant contract, get detailed POP dates, recipient info, and business categories:

```bash
curl -s "https://api.usaspending.gov/api/v2/awards/<generated_internal_id>/" | jq '{
  description: .description, total_obligation: .total_obligation,
  date_signed: .date_signed,
  pop_start: .period_of_performance.start_date,
  pop_end: .period_of_performance.end_date,
  recipient: .recipient.recipient_name,
  recipient_uei: .recipient.recipient_uei,
  business_categories: .recipient.business_categories,
  recipient_location: .recipient.location
}'
```

⚠ **Pitfall:** The `/api/v2/awards/<id>/` endpoint is the BEST source for UEI and business categories (8(a), SDVOSB, WOSB, etc.). The `/api/v2/recipient/` endpoint with `recipient_search_text` returns ALL entities in the database sorted by amount — it does NOT filter by search text. However, the `/api/v2/recipient/<UUID>/` endpoint DOES work when you pass the UUID-based `recipient_id` from award results (format: `942a2bde-c189-6421-6a4d-a9b1c2f00d41-C` with `-C`/`-P`/`-R` suffix for child/parent/root level). See `references/usaspending-api-patterns.md` §7 for the proven pattern.

### Phase 5b: Transaction-Level Extraction

Awards aggregate multiple modification transactions (Mods). For granular spending detail — each obligation action, its date, amount, and description — use `spending_by_transaction/`. This is essential for understanding spending velocity, identifying specific work performed under each award, and building accurate revenue-by-year analysis.

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_transaction/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2019-10-01", "end_date": "2026-09-30"}],
      "award_type_codes": ["A", "B", "C", "D"]
    },
    "fields": ["Award ID", "Recipient Name", "Transaction Amount", "Action Date",
               "Action Type", "Transaction Description", "Mod",
               "Awarding Agency", "Awarding Sub Agency",
               "generated_internal_id", "recipient_id", "Recipient UEI",
               "naics_code", "naics_description"],
    "page": 1, "limit": 100, "sort": "Transaction Amount", "order": "desc"
  }'
```

⚠ **Critical:** The `fields` and `sort` parameters for `spending_by_transaction/` use DIFFERENT field names than `spending_by_award/`. Invalid field names cause 422 errors. Valid fields include: `"Transaction Amount"` (NOT `"amount"`), `"Action Date"`, `"Action Type"`, `"Transaction Description"`, `"Mod"`, etc. The `sort` parameter is REQUIRED. See `references/usaspending-api-patterns.md` §8 for the complete valid field list.

### Phase 5c: DBA/Project Name Discovery (Keyword Search)

If the company operates under a DBA or has a product/project name that doesn't appear as a registered recipient, use keyword search to find awards mentioning it in descriptions:

```bash
# Find awards mentioning a product/DBA name (e.g., "Navaide")
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_transaction/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "keywords": ["Navaide"],
      "award_type_codes": ["A", "B", "C", "D"],
      "time_period": [{"start_date": "2019-10-01", "end_date": "2026-09-30"}]
    },
    "fields": ["Award ID", "Recipient Name", "Transaction Amount",
               "Transaction Description", "Action Date"],
    "page": 1, "limit": 100, "sort": "Transaction Amount", "order": "desc"
  }'
```

The `keywords` filter searches award descriptions and transaction descriptions. This is how you connect a DBA/product name to the actual legal entity that holds the contracts.

### Phase 5d: Brand-New Entity Handling (No Federal Awards Exist)

When all USAspending queries return **zero results** (autocomplete, spending_by_award, spending_by_transaction, keyword search), immediately shift from contract-portfolio analysis to **Entity Establishment Intelligence Briefing**.

A brand-new GovCon entity (<6 months since state registration) has no federal awards to analyze. The intelligence value shifts to registration completeness, SBA/VA certification status, and leadership credibility.

**Decision rule:** If USAspending autocomplete returns empty for all name variants (legal name, DBA, shorthand) AND `spending_by_transaction` keyword search returns empty — you have a brand-new or unregistered entity. Do not produce a revenue-trend or contract-cliff briefing. Produce an Entity Establishment Briefing instead.

**Research checklist for brand-new entities:**

| Check | Source | What It Reveals |
|-------|--------|----------------|
| Website "Coming Soon" vs commercial content | Direct HTTP response | SAM registration status inference, operational maturity |
| Domain age & prior ownership | Wayback CDX API | Brand continuity signal, domain repurposing |
| EIN prefix cross-check | Public EIN prefix tables | State of principal owner vs stated entity state |
| SAM.gov HTTP probe | `curl -sL -o /dev/null -w "%{http_code}"` | 200 SPA shell ≠ confirmed entity (see Pitfall below) |
| State business registry | TX Comptroller, SOS search by File Number | Confirms entity legal existence; reveals Taxpayer Number, formation date (see `references/state-entity-verification.md`) |
| SBA DSBS / certifications portal | `search.certifications.sba.gov` | SDVOSB / 8(a) / WOSB status (503 = system down, not absence) |
| cage.report direct URL | `cage.report/` search | UEI-linked entity data |
| Named contacts on Coming Soon page | Source-code extraction | Operational sophistication signal |

**Critical framing:** When no federal records exist, the briefing must honestly report **confirmations of absence** — not imply capability that cannot be verified. Lead with what is NOT found. Reserve "plausible" or "unverified" language for inferences only, not claims.

**Briefing section order for brand-new entities:**
1. Entity Profile + Gap Warning (red callout)
2. Socio-Economic / Certifications (self-declared vs verified)
3. Services (inferred from GovTribe descriptions; flag credibility risks like "offering CMMC L2 without own L2")
4. Leadership (honest zero-profile findings; do not fabricate)
5. SAM.gov probe results (HTTP response analysis)
6. NAICS plausibility table (inferred, NOT confirmed)
7. Competitive Landscape (brand-name signal, Flying Leatherneck distinction)
8. Domain History Timeline (Wayback CDX + prior entity identification)
9. Notable Observations (EIN prefix anomaly, domain brand value, contact infrastructure quality)
10. Intelligence Gap Summary (table: category × status × priority × next step)
11. Sources & Research Scope Boundary

**Reference:** See `leatherneck-federal-consulting-intel-2026-07-18.html` for a complete worked example.

### Phase 6: Company Intelligence Gathering

Supplement federal data with company website and news:

```bash
# Company website - get capabilities, partnerships, recognitions
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://company-website.com" | python3 -c "
import sys, re
html = sys.stdin.read()
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.S)
clean = re.sub(r'<[^>]+>', ' ', clean).strip()
clean = re.sub(r'\s+', ' ', clean)
print(clean[:5000])
"
```

Look for on company website:
- SBA designations (8(a), EDWOSB, SDVOSB, HUBZone, ISBEE) in footer or About page
- Contract vehicles (GSA MAS numbers, SeaPort-NxG, 8(a) STARS, etc.)
- Strategic partnerships and JVs
- Inc. 5000 rankings, awards
- SBIR/STTR awards
- Leadership team, HQ location
- **"Coming Soon" status** — indicates mid-registration or pre-launch
- **Email-protection wrappers** (Cloudflare) on contact page — confirms domain is active but protected

**Firecrawl credit exhaustion fallback:** If `web_search` or `web_extract` returns "Payment Required / Insufficient credits," immediately switch to `ddgr` CLI for search and raw `curl` for direct site scraping. Do not retry Firecrawl — switch tools, don't block.

### Phase 7: Contract Lifecycle Classification

Categorize every contract into one of four buckets:

| Bucket | Criteria | Action |
|--------|----------|--------|
| **Secure** | POP end date > 12 months out | Revenue floor calculation |
| **At Risk** | POP end date within 90 days | Renewal likelihood assessment |
| **Expired/Lost** | POP end date in past, no replacement found | Revenue loss quantification |
| **Reduced** | Expired but rebid at lower value | Calculate delta |

### Phase 8: Renewal Likelihood Assessment

For each at-risk contract, assess renewal probability based on:

1. **Vehicle type** — GSA MAS task orders are easy to recompete; definitive contracts need full RFP
2. **Set-aside status** — 8(a) sole-source threshold is $7M (STARS III); above that requires competition
3. **Historical pattern** — Has the company held similar contracts before? (e.g., recurring commodity supply = high renewal)
4. **Market dynamics** — Is the agency consolidating work under a larger prime? Are there known large vehicles that absorbed the scope?
5. **Option periods** — Does the contract description mention option years? "Base Year Labor" suggests option periods exist
6. **New awards** — Has the same agency awarded the company new contracts recently? (positive signal)

### Phase 9: HTML Briefing

Compile into self-contained HTML briefing using the Thariq aesthetic (ivory `#FAF9F5`, clay `#D97757`, slate `#141413`). Key visual elements vary by briefing type:

**For established contractors (has awards):**
- **Stat cards** — lost revenue, at-risk amount, total negative impact, secured floor
- **Revenue trend bar chart** — FY-by-FY obligations showing growth then cliff
- **Contract tables** — color-coded by status (red=lost, amber=at-risk, green=secure)
- **Expiration timeline** — visual timeline with colored dots showing when contracts expire
- **Renewal likelihood table** — each at-risk contract with assessed probability and reasoning

**For brand-new entities (no awards):**
- **Dark snapshot box** — key entity facts (legal name, formation date, EIN, DVOSB claim, website status)
- **Red gap warning callout** — "BRAND-NEW ENTITY — HIGH INTELLIGENCE GAPS"
- **Domain history timeline** — Wayback CDX dots showing prior entity transitions
- **Certifications table** — claimed vs verified vs not found
- **SAM probe results** — HTTP response analysis table
- **Services assessment** — claimed vs inferred vs implausible
- **Leadership cards** — zero-profile findings honestly reported
- **Intelligence gap table** — category × status × priority × next step

Save to `/data/nextcloud/data/amyn/files/briefings/<company>-contract-intelligence-<date>.html`, then:
```bash
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"
```
Deliver as `https://brief.h.porb.dev/<filename>.html`

## Pitfalls

- **"IDV" is not a valid award_type_code.** The spending_by_award endpoint rejects it. Use `A`, `B`, `C`, `D` for contracts, or granular `IDV_A` through `IDV_E` for IDVs.
- **The `/api/v2/recipient/` endpoint does not filter by search text** — BUT the UUID-based `recipient/<recipient_id>/` GET endpoint DOES work. Pass the `recipient_id` from award/transaction results (format: `<UUID>-C` for child, `-P` for parent, `-R` for root). Numeric `internal_id` values fail with 400; only UUID-based IDs work. See `references/usaspending-api-patterns.md` §6.
- **`spending_by_transaction/` uses different field names than `spending_by_award/`.** It requires `"Transaction Amount"` (not `"amount"`), `"Transaction Description"`, `"Action Date"`, `"Mod"`, and the `sort` parameter is REQUIRED. Invalid field names cause 422. See §7 of the API reference for the complete valid field list.
- **FPDS.gov has been consolidated into SAM.gov.** The FPDS ezsearch endpoint (`fpds.gov/ezsearch`) now redirects to SAM.gov. All FPDS-sourced contract data is accessible through USAspending.gov's API. The `api.sam.gov/prod/federalaccounts/` endpoint requires an API key (returns 404 without one).
- **Defense.gov returns 403 for curl.** Cannot scrape DoD contract announcement pages directly. Use ClearanceJobs (news.clearancejobs.com/category/defense-contracts/) or Google News RSS as fallback.
- **SAM.gov API requires an API key.** No SAM.gov API key means no live solicitation searches. Use Google News RSS and secondary sources for recompete intelligence.
- **SAM.gov UI returns HTTP 200 SPA shell.** Both `/api/sam.gov/entity/<search>` and `sam.gov/entity/<search>` return HTTP 200 even with zero results — they render search results client-side via JavaScript. A 200 from these paths does NOT confirm entity existence; absence from cage.report + USAspending + direct keyword search is the stronger signal.
- **SAM.gov entity search requires sign-in (as of July 2026).** The entity search page (`sam.gov/search/?index=entity`) now displays "Sign in to Access Full Features. Sign in to your SAM.gov account to search, download, save searches, and follow records." The `sfm[domains][entity]=true` URL parameter is ignored — the search results area never populates without authentication. Typing a UEI into either the keyword-text filter box or the main search bar and pressing Enter/submit produces no results. **Do not spend time trying to scrape or interact with the SAM.gov entity search UI — it is gated behind login.** Fall back to: state business registries (see `references/state-entity-verification.md`), USAspending.gov API (Phase 1), cage.report, and the SBA Certifications portal.
- **`spending_by_award` does NOT return set-aside fields in results.** The `Set Aside`, `Type of Set Aside`, and `Extent Competed` fields are ALWAYS null in `spending_by_award` responses — this is a USASpending API design decision, not a data error. The API supports `set_aside_type_codes` as an INPUT filter (and it works correctly) but does not expose the matched values in the OUTPUT. For SDVOSB/8(a)/WOSB detection: (a) run a separate query with the set-aside filter and cross-reference returned award IDs against your dataset, OR (b) use the `/awards/{generated_internal_id}/` detail endpoint which includes `recipient.business_categories`. See `references/usaspending-api-patterns.md` §"Field Naming and Response Format Quirks" for the proven cross-reference pattern.
- **NAICS and PSC are nested objects in `spending_by_award` responses.** They return as `{code: "541611", description: "ADMINISTRATIVE MANAGEMENT..."}` objects, not flat strings. The field names in the `fields` array are `NAICS` and `PSC` (NOT `NAICS Code` or `Product or Service Code (PSC)`). Extract with `naics.get("code", "")` and `naics.get("description", "")`.
- **`page_metadata.total` is unreliable — may show 0 with valid results.** The API returns `"total": 0, "hasNext": true` on many queries. Always paginate by `hasNext` — stop when it's `false` or the results array is empty. Do not trust `total` for page-count logic or early termination decisions.
- **`award_type_codes` is REQUIRED and award-type groups cannot mix.** Omitting it returns 422. Contract types (A–D) and IDV types (IDV_A–E) are separate groups — mixing them in one query also returns 422. Always query contracts and IDVs in separate API calls.
- **`time_period` uses `action_date` (most recent action), not award start date.** Competitor searches may return old contracts with recent modifications — these ARE currently active. The `End Date` field tells the real expiration, not the filter window. Do not discard results because their `Start Date` predates your filter window.
- **Obligation ≠ Revenue.** USAspending reports total obligations, which may include unexercised option periods. Actual revenue may differ. Always note this caveat.
- **Subcontract revenue is invisible.** If the company is a subcontractor on a large prime, that work does not appear in USAspending prime award data. This can significantly understate the company's actual activity.
- **FY2026 data is partial.** Federal fiscal year runs Oct 1 – Sep 30. If analyzing mid-year, obligation totals will be incomplete.
- **DBA vs legal name mismatch.** Company DBAs often don't appear in USAspending as registered recipients. Always search using the legal entity name from SAM.gov or the company's website footer. If you know a DBA/product/project name (e.g., "Navaide") but not the legal entity, use the `keywords` filter in `spending_by_transaction/` to find awards mentioning it in descriptions — this reveals the actual legal entity that holds the contracts.
- **Task order ceiling ≠ obligation.** USAspending's `total_obligation` is the funded amount, NOT the ceiling. For IDIQ/task orders, the ceiling can be 50x+ the current obligation (e.g., Navaide's CEBO: $655K obligated vs $104M ceiling). Always check OrangeSlices AI or company press for ceiling values on competitive task orders. Reporting the obligation as the contract value is a catastrophic error.
- **SBA certification suspension is the #1 cause of portfolio erosion.** Always check `search.certifications.sba.gov/profile/<UEI>/<CAGE>` early in the analysis. A suspended 8(a) or expired set-aside designation explains why sole-source contracts expire without replacement. This is often the root cause — don't discover it last.
- **Stale facts across iterative briefing updates.** When updating a briefing with new information (e.g., protest outcome, SBA status), search the entire HTML for every reference to the old fact. Common stale references: "8(a) certified" in the company profile, "protest filed" in stat cards, old obligation amounts presented as total values, wrong POP end dates for multi-year task orders. After each major fact update, re-read the full HTML and grep for contradictions.
- **OrangeSlices AI is the best source for Navy/SeaPort-NxG contract details.** They report full ceiling values, number of competitors, protest filings, and GAO decision outcomes. Free articles cover award announcements; protest outcome articles are also free. Use `orangeslices.ai` in Google News RSS queries alongside the company name.
- **GAO.gov blocks curl with Akamai.** Use OrangeSlices AI articles (which report GAO digests, file numbers, and decision dates) or Google News RSS as alternatives. The GAO bid protest search URL is `https://www.gao.gov/legal/bid-protests/search?processed=1&file=<number>&outcome=all` but requires a browser.
- **Domain repurposing can mask entity history.** A domain registered before the current entity's formation date indicates acquisition, not continuity. The prior owner's business type, industry, and name may be entirely unrelated — but the prior registration date can be misread as "company has been around since [year]." Always check Wayback Machine CDX for the domain's first archive date and compare to the entity's registration date. If the domain predates the entity by years, it was repurposed, not inherited.
- **EIN prefix indicates state of issuance, not entity state.** EIN prefix `42` = Pennsylvania. A South Carolina LLC with a Pennsylvania-issued EIN suggests an out-of-state principal owner. Flag as a clarifying question; do not treat it as a registration error.
- **GovTribe auto-generates NAICS for unregistered entities.** GovTribe descriptions for entities without completed SAM registrations may include auto-suggested NAICS codes. Treat them as inferred, not confirmed, until SAM registration is complete.
- **Firecrawl credits can exhaust mid-research.** If `web_search` or `web_extract` returns "Payment Required / Insufficient credits," immediately fall back to `ddgr` CLI (DuckDuckGo) for search and `curl` for direct site scraping. Do not retry Firecrawl after credit exhaustion — switch tools, don't block.
- **Self-declared socio-economic status ≠ certified status.** A "DVOSB" or "SDVOSB" claim on a company website footer is self-declared only. VA VETS verification or SBA DSBS certification is required before the status is actionable for set-aside contracts. Always flag self-declared status as "ⓘ UNVERIFIED."
- **Indirect SAM.gov evidence is unreliable for brand-new entities.** USAspending returning zero + cage.report returning zero + SAM.gov returning HTTP 200 SPA shell ≠ "no SAM registration exists." The entity may be fully registered and active but invisible to indirect sources because: (a) it has no awards yet (nothing for USAspending to index), (b) cage.report lacks a historical crawl of the new UEI, (c) SAM.gov's JS-rendered entity pages don't expose records to curl. **Only a direct SAM.gov entity PDF export or a logged-in SAM.gov lookup resolves this ambiguity.** When the user has access to SAM.gov/SBA portals, request entity PDF exports as a follow-up step after the initial OSINT sweep returns empty. The SBA Certifications portal (`search.certifications.sba.gov/profile/<UEI>/<CAGE>`) is also JS-rendered — request a PDF export rather than attempting to scrape it.

## Output Files

- HTML briefing: `/data/nextcloud/data/amyn/files/briefings/<company>-contract-intelligence-<date>.html`
- Raw API data: `~/govcon_research/raw/<company>/` (JSON files per query)
- Briefing URL: `https://brief.h.porb.dev/<filename>.html`

## Related Skills

- **`fedcon-opportunity-research`** — Finding open solicitations and new opportunities by date window. Complementary: this skill analyzes a company's existing portfolio, that skill finds what's available to bid.
- **`fedcon-competitive-landscape-scan`** — Multi-NAICS competitive landscape mapping: agencies, competitors, SDVOSB patterns, and recompete opportunities. Use when you need the full market picture before zooming into a single contractor.
- **`contact-intelligence`** — Researching a person/company for outreach and networking. This skill goes deeper on the federal financial data side.

## CGO/CRO Judge Review Pattern

After building the initial briefing, dispatch a `delegate_task` judge agent to review the HTML against all raw research files from a Chief Growth Officer perspective. The judge should check:

1. **Factual accuracy** — Are all numbers, dates, contract IDs, and percentages correct across the entire HTML?
2. **Contradiction check** — Do any sections reference stale facts that were updated elsewhere? (e.g., "8(a) certified" when the certification is only self-declared)
3. **Strategic framing** — Is the root cause properly connected to the symptoms? For brand-new entities, is the absence of records honestly framed rather than implied?
4. **Completeness** — Are all gap-analysis cells populated? Are all "empty" flags consistent with the actual research scope?
5. **Stylistic consistency** — Do flag icons match their semantic meaning? Are verbiage choices consistent (e.g., "probe" vs "search" vs "query")?
6. **CGO priorities** — Competitive threats, size standard proximity, JV strategy implications, pipeline health, BD priorities

Pass all raw research file paths and the HTML briefing path to the judge. Have it write its review to `~/govcon_research/raw/<company>/cgo_judge_review.md`, then apply all fixes before re-publishing.

## Reference Files

- `references/usaspending-api-patterns.md` — Detailed API endpoint reference, exact curl commands, response parsing patterns, and field mappings.
- `references/external-data-sources.md` — SBA Certifications portal, OrangeSlices AI (task order ceilings, protests), GAO bid protest docket, cage.report, HigherGov, company website scraping targets, brand-new entity detection checklist.
- `references/state-entity-verification.md` — State business registry search patterns (TX Comptroller, SOS) for cross-verifying entity existence when SAM.gov is inaccessible.
