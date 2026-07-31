---
name: fedcon-opportunity-research
description: "Exhaustive federal contracting opportunity research by date window — discover solicitations, contract awards, SBIR/STTR topics, and GWAC/IDIQ task order pipelines across SAM.gov, SBIR.gov, GovCon Wire, Federal News Network, and agency sites. Extract complete opportunity details (agency, solicitation number, title, value, deadline, capabilities sought, set-aside status, source URL) and flag opportunities relevant to specific capability areas (AI, cybersecurity, data analytics, cloud, technology)."
triggers:
  - "research federal contract opportunities"
  - "find GovCon opportunities"
  - "search SAM.gov solicitations"
  - "SBIR/STTR topic research"
  - "federal contracting pipeline analysis"
  - "find opportunities between [dates]"
  - "HARD date constraint opportunities"
  - "look up a SAM.gov opportunity"
  - "evaluate this contract opportunity"
  - "what's the size of this contract"
  - "incumbent on this solicitation"
  - "recompete or new work"
  - "SAM.gov notice detail"
---

# Federal Contracting Opportunity Research

## Overview

Systematic, exhaustive research to discover federal contracting opportunities within a hard date window. Covers active solicitations, contract awards, SBIR/STTR topics, and GWAC/IDIQ vehicle activity. Extracts complete opportunity details and flags items relevant to specific capability areas.

## When to Use

- User asks to research opportunities between specific dates with a HARD date constraint
- Preparing for business development outreach
- Analyzing federal spending trends in a time period
- Building opportunity pipelines for a GovCon firm
- Identifying small business set-asides in a date range
- Evaluating a batch of grants.gov / simpler.grants.gov NOFO opportunities (this is a different class from SAM.gov contract solicitations — see "Grants.gov & NOFO Analysis" section below)
- Multi-opportunity pipeline assessment: user drops 3-5+ links and wants them all evaluated, ranked, and turned into a decision briefing
- Rapid assessment from a forwarded solicitation — someone sends you a SAM.gov notice (Sources Sought, presolicitation, RFP) and you need a go/no-go with incumbent analysis, competitive landscape, and teaming strategy. This is different from discovery: you start WITH the opportunity details and work backward through predecessor history.
- Building or seeding a BD pipeline repo with sub-module directory structure — creating a federal-bd-pipeline repository with per-opportunity sub-modules containing source-docs, research, and deliverables folders

## User-Specific Conventions (Amyn / HARBOR / Leatherneck)

These conventions apply when researching opportunities for Amyn Porbanderwala's entities (HARBOR Initiative LLC, Leatherneck Federal Consulting LLC, or partnership assessments):

**Deliverable format:** Self-contained HTML briefing at `/data/nextcloud/data/amyn/files/briefings/` → `https://brief.h.porb.dev/<filename>.html`. Thariq/html-effectiveness design tokens (ivory #FAF9F5, clay #D97757, slate #141413, oat/olive). After writing: `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`. Send link only in Discord, never attach the file.

**HTML quality check — mandatory before delivery:** Open `~/repos/html-effectiveness/index.html` and load the reference gallery. Find the example closest to your deliverable type (status report #11, research explainer #14-15, implementation plan #16, code review #03). Compare your output against its visual rhythm, spacing, typography hierarchy, and card/table styling. If your HTML looks materially worse than the gallery equivalent, rewrite it. The gallery is the minimum quality bar — passing validation is not enough. The user will notice and ask for a fix if you skip this step.

**Teaming structure — Leatherneck primes 100%, HARBOR is internal.** When analyzing opportunities for joint Leatherneck/HARBOR pursuit, the structure is NOT a formal prime-subcontract: Leatherneck is the sole applicant and Amyn is named as Leatherneck key personnel. HARBOR's product stack and methodology are internal delivery capabilities of the Leatherneck team — not a disclosed subcontract. This avoids 49% subcontract caps, simplifies the budget, and keeps the narrative clean. The internal arrangement between HARBOR and Amyn is separate and not disclosed in applications.

**Scope broadening mandate — do NOT default to federal/compliance-only.** When the user says "anything and everything" or "don't just think about LFC," drop the federal/compliance filter immediately. Assess ALL capabilities across the combined team — technology advisory, AI strategy, smart city planning, commercial cybersecurity, program management advisory — not just FAR-based GovCon compliance work. This is especially critical when evaluating a large commercial prime (Bechtel, KBR, Fluor, AECOM) where entry points cross federal/commercial/procurement lines. Default to the broadest-possible assessment across every project in the target's pipeline and let the user trim. The July 2026 Bechtel session: I filtered to federal compliance only, the user pushed back, and the corrected assessment included technology advisory, smart city planning, digital engineering, and AI strategy across 18 commercial/energy/infrastructure projects.

**Entity data sources of truth:**
- HARBOR: `~/repos/2026_books/operations/harbor-initiative-llc/00-canonical-facts.html` (UEI, EIN, NAICS, formation, compliance calendar). UEI K4CVRY71WQZ8.
- Leatherneck: SAM.gov entity record (UEI VU2HV8458J93) + SBA DSBS profile. Partnership/LLP entity structure (not single-member LLC — flag this).
- Portfolio: `~/repos/2026_books/HARBOR_portfolio/` for member capabilities and past engagement intel.

**Prime entity mandate:** Leatherneck Federal Consulting LLC primes everything. Amyn Porbanderwala serves as a named Leatherneck key personnel (Technology Lead). The HARBOR relationship is an internal agreement between Amyn and Leatherneck — not a disclosed subcontract. This structure is cleaner for applications: no 49% subcontract cap, simpler budget (all personnel under Leatherneck), and a coherent single-entity narrative. When assessing opportunities, evaluate with Leatherneck as the 100% bidding entity and HARBOR's product stack as an internal delivery capability. The only exception is SBIR/STTR Phase I topics where HARBOR can submit directly once its own SAM registration completes (bank account bottleneck). Until then, Leatherneck primes all submissions.

**Team-role distribution — DO NOT put everything on two people.** When building pursuit plans, capability statements, or submission timelines, distribute tasks across ALL team members. Leatherneck has four co-founders: Douglas Henderson (BD/Capture, PMP/DAWIA III, $20B SRNS portfolio), Mark Payne (Contracts/Budget, DAWIA III Contracting, 15yr USMC), Justin Frawley (Risk/Compliance, MBA, 15yr commercial), and Amyn Porbanderwala (Technical Lead, DAF SBIR PI, Secret clearance, USMC cyber). Budget/forms → Mark. Risk/compliance → Justin. Technical/narrative → Amyn. BD/teaming/submission → Douglas. Never assign SF-424s to Amyn or technical approach to Mark — roles map to the person with that expertise. If a pursuit plan shows only Douglas and Amyn as owners, it's wrong — fix it before presenting to the team.

**Cross-contamination rule:** Briefings and deliverables prepared for Leatherneck Federal Consulting LLC (or any external partner) MUST NOT contain HARBOR portfolio intel — no reference to specific portfolio companies (AXOLTL, Ecotronics, Chandler, etc.), no drone-dominance competitive assessment sourced from portfolio work, no internal HARBOR methodology details. Strip all portfolio references before sharing externally. The briefing is Leatherneck's document; include only what Leatherneck needs to know.

**"Cast wide net → CSV → filter locally" pattern:** When the user asks to pull everything and find the 5-10% that applies, the correct workflow is: (1) USASpending API — small-dollar awards by NAICS + keyword, dump to CSV; (2) SBIR portal — full topic dump, score locally; (3) SAM.gov browser — Sources Sought keyword searches only (set-aside filter returns hardware noise). Do not do one-at-a-time detail-page verification for broad scans. Process locally with Python scripts, then brief the user on top hits.

**Extended — "Pull everything → interactive dashboard" pattern:** When the user says "pull ALL of it" (no limits, unfiltered, full dataset), escalate to a multi-NAICS bulk sweep (16+ codes with pagination) + agency rollups + unified analysis + interactive HTML dashboard with embedded ~60KB JSON. This is a different workload from the CSV-for-filtering pattern — the output is an interactive briefing, not a CSV for local filtering. The full technical recipe (USASpending bulk query recipes, field name mapping for UI, skeleton+data+patch assembly, Nextcloud deployment) is in `references/usaspending-bulk-pull-to-dashboard.md`. Trigger: user explicitly says "everything," "all of it," "don't limit to anything."

**Dual-track B2B/B2G framing:** HARBOR is B2B today (18 portfolio members, productized engagements) but built for B2G (UEI assigned, engagement packet ready, roadmap includes federal activation). Never say "B2B not B2G" — it's "B2B today, B2G tomorrow." The Leatherneck play is the bridge: subcontract through Leatherneck's active SAM now while HARBOR's own SAM completes.

**Drone dominance / counter-UAS lane:** The Hegseth DDP, Replicator 2/DAWG, and $1.5B DHS C-UAS vehicle represent a major spending wave. HARBOR/Leatherneck don't compete on hardware — the play is the software/services layer (AI/ML orchestration, CMMC compliance, program management, training) on top of hardware primes. Key intel: `HARBOR_portfolio/axoltl_chandler/05-assessment-rebuild/00-inputs/federal-acceleration-intel.md` (18-row opportunities table).

**SBIR portal:** sbir.porbanderwala.cloud has 75 active SBIR/STTR topics with AI-powered search. Use for SBIR-specific research. Filter by component (ARMY, USAF, NAVY, DARPA, DLA, etc.), phase, status.

**SBIR topic PDF extraction:** DoD SBIR topic PDFs (from DSIP or attached by user) extract cleanly with `pdftotext -layout <file> -`. The `-layout` flag preserves the field structure (OBJECTIVE, DESCRIPTION, PHASE I/II/III, KEYWORDS, CMMC level, ITAR flags). All 8 topic types (xTech competitions, open topics, DP2, DIU challenges) follow the same format. Fields to capture: topic number, title, agency, component, modernization priorities, CMMC level, phase structure, deadline, DP2 vs Phase I, ITAR restrictions.

**Briefing table columns (Leatherneck-prime standard):** Every opportunity table must include these columns as a minimum: Notice ID, Title/Agency, Deadline, Set-Aside, Work description (1-2 lines), New-or-Recompete classification, Past Performance Required? (YES/NO), and Fit score. Group by urgency: 🔴 URGENT (this week), 🟡 ACTIVE (this month), 🟢 FORWARD-LOOKING (next month). For SBIR topics, add Topic Number, Relevance (1-5 score), and Phase I award estimate. Agency spending section: Rank, Agency, 90-Day Spend, Target? (PRIMARY/SECONDARY/MONITOR).

## Prerequisites

- Research workdir: `~/govcon_research/`
- Output directory structure: `~/govcon_research/raw/<date>/` and `~/govcon_research/analysis/`
- Python 3 available for XML parsing
- curl available for API and RSS feeds
- No API keys required (uses public RSS feeds and site scraping)

## Workflow Steps

### Phase 0: Rapid Assessment of a Forwarded Solicitation

Use this phase when someone sends you a specific SAM.gov notice (Sources Sought, presolicitation, RFP) and you need a go/no-go assessment. You start WITH the opportunity details known — this is NOT a discovery workflow.

**⚠️ Critical: hit USAspending API directly from your own tool calls, do not delegate.** The user will say "do not be lazy" if you dispatch sub-agents for research that you could execute yourself. Direct API calls are faster, avoid intermediary rate limits, and let you steer the analysis in real time as findings emerge. Reserve sub-agent delegation only for parallel workstreams after the core API research is done (e.g., one agent per competitor deep-dive).

**Step 0.1: Extract source document.** If the solicitation came as an email attachment (.docx, .pdf), extract the text. For .docx use `python3 -c "import docx; print(docx.Document('file.docx').text)"`. For PDFs use `pdftotext -layout file.pdf -`. Collect: Notice ID, agency/subtier/office, title, NAICS code, set-aside language, response deadline, contract type, period of performance, PWS scope areas, POC/CO names.

**Step 0.2: Look up predecessor contract via USAspending.** The Notice ID is a solicitation identifier (pre-award), NOT an award ID. Search USAspending by:
- Topic keywords from the PWS (single tokens only — `spending_by_award` keywords don't do phrase matching)
- Contracting-office prefix from the Notice ID (chars before the fiscal-year segment)
- Agency + NAICS combination

From each award result, grab `generated_internal_id` and fetch full detail via GET `https://api.usaspending.gov/api/v2/awards/{generated_internal_id}/` (note: this is a GET, not POST). Read `description`, `total_obligation`, `period_of_performance`, and `latest_transaction_contract_data` (contains `number_of_offers_received`, `extent_competed`, `type_set_aside`, `naics`, `naics_description`).

**Step 0.3: NAICS shift analysis — the critical competitive intel signal.** Compare the predecessor's NAICS code to the new solicitation's NAICS. If different:
- Note the size standard difference (e.g., 541330 $25.5M → 541614 $20M)
- Check if the incumbent is registered as LARGE under the new NAICS (use HigherGov, SAM.gov entity lookup, or cage.report)
- If the incumbent is large under the new NAICS and the solicitation is small business set-aside, this is a **game-changing competitive opening** — flag immediately

**Step 0.4: Incumbent portfolio deep-dive.** Search USAspending by the incumbent's legal name. Collect ALL contracts under the same contracting office/agency. Identify:
- Total dollar value across all MARCORLOGCOM-related contracts
- Whether the incumbent holds adjacent scopes (same office, different PSCs)
- POP end dates of related contracts (reveals if multiple contracts are coming up for recompete)
- Personnel deployment pattern (global locations, hiring signals — look for active job postings for the exact labor categories)

**Step 0.5: Competitive landscape via contracting-office prefix.** Search USAspending `spending_by_award` filtering by:
- The contracting-office prefix (e.g., `M67004` for MARCORLOGCOM)
- Award type codes `A,B,C,D`
- Broad date range (5+ years)

This reveals every contractor that has worked with that office. Tier the results: Tier 1 = direct DMSS/Distribution incumbents, Tier 2 = adjacent scope under same office, Tier 3 = large primes with logistics capability. See `references/competitive-landscape-via-contracting-office.md` for the full tiered classification framework.

**Step 0.6: Go/No-Go with teaming strategy.** Assess:
- Can you prime? (Only if you have past performance in the exact scope area. If $0 prime awards, answer is NO.)
- Can you sub to the incumbent? (Highest probability if they need SDVOSB/small business partners. Reach out within 72 hours.)
- Can you sub to a challenger? (Lower probability — they need a full new team. HARBOR's AI analytics could be a discriminator.)
- Can you sub to a large prime entering? (Lowest — large primes build their own analytics. Only leverage point is small business set-aside status.)

**Step 0.7: Deliverable.** Self-contained HTML briefing at `/data/nextcloud/data/amyn/files/briefings/`. Thariq/html-effectiveness design tokens. Key sections: Executive Summary, Opportunity at a Glance table, Incumbent Analysis, NAICS Shift Analysis, Competitive Landscape, Fit Assessment (capability matrix), Go/No-Go Recommendation, Teaming Strategy, Immediate Action Plan (72 hours), Key Risks, Sources.

### Phase 1: Date Window Definition

Confirm the exact date window with the user. The user may specify "HARD date constraint" which means:
- Only opportunities posted or updated within the window
- No opportunities outside the window
- Be explicit about the range (e.g., "June 30 and July 7, 2026")

**Thoroughness mandate:** When the user says "do not be lazy," exhaustive means exhaustive. Every SAM.gov result page must be opened. Every detail page with a deadline in range must be verified for set-aside, PSC, description, and past performance attachments. Every SBIR topic must be scored for fit. Multi-source cross-checking (SAM.gov + USASpending + SBIR.gov + the local portal) is the minimum — not optional. Do not stop after one data source.

### Phase 2: Multi-Source RSS Discovery

Run Google News RSS queries in parallel for comprehensive coverage. Use the queries in `references/fedcon-rss-queries.md`:

```bash
# Run in parallel for efficiency
mkdir -p /tmp/govcon
curl -sL "<RSS_URL_1>" -o feed1.xml
curl -sL "<RSS_URL_2>" -o feed2.xml
# ... continue for all feeds
```

**Source Categories:**
1. **SAM.gov & Federal Solicitations** (5 queries)
2. **SBIR/STTR Open Solicitations** (5 queries)
3. **Major GWAC/IDIQ Vehicle News** (5 queries)
4. **FedScoop, GovConWire, Federal Times** (3 queries)
5. **Defense Innovation Programs** (3 queries)

### Phase 3: Parse and Filter RSS Results

Use Python to parse RSS XML and filter by date window:

```python
import re

xml = open('feed.xml').read()
items = re.findall(r'<item>(.*?)</item>', xml, re.S)
for it in items:
    title = re.search(r'<title>(.*?)</title>', it, re.S)
    pub = re.search(r'<pubDate>(.*?)</pubDate>', it, re.S)
    link = re.search(r'<link>(.*?)</link>', it, re.S)
    src = re.search(r'<source[^>]*>(.*?)</source>', it, re.S)
    # Filter items within date window
    # Extract and store title, date, link, source
```

### Phase 4: Full Content Extraction

For relevant articles (within date window), fetch full content from source sites:

**GovCon Wire** (highly reliable, full content):
```bash
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://www.govconwire.com/articles/<slug>" > article.html
```

Parse with Python extraction script:
```python
# Extract title, meta description, article paragraphs
title = re.search(r'<title>(.*?)</title>', html)
meta = re.search(r'<meta name="description"[^>]*content="([^"]*)"', html)
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
```

**⚠️ Pitfall: Google News Redirects**
Google News RSS links use JavaScript redirects that curl cannot resolve:
- The `curl -L` and `location` header methods don't work
- Redirect URLs contain encoded article IDs that require JavaScript execution
- **Solution:** Use the RSS feed to discover articles, then fetch from the source site directly (e.g., `www.govconwire.com`, `www.fedscoop.com`)

### Phase 5: SAM.gov Public UI Search (Primary Method — No Login Needed)

The SAM.gov contract-opportunities search UI works **anonymously** (no login.gov account needed) at `https://sam.gov/search?index=opp`. When the request is "find opportunities by NAICS / set-aside / deadline," this is the most reliable path — far better than RSS for structured filters.

**Applying filters via the browser tool:**

1. Navigate to `https://sam.gov/search?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm%5Bstatus%5D%5Bis_active%5D=true`
2. **⚠️ URL `sfm[]` params are unreliable** — NAICS params in the URL are silently ignored on first load (you'll see ~16,008 unfiltered results). Set-aside params in the URL DO tend to stick. Always verify the filter chips in the left panel before trusting result counts.
3. **NAICS codes must be added through the filter widget:**
   - Click the "Product or Service Information" heading to expand it (may take 2 clicks — the first click sometimes collapses instead).
   - Click the NAICS combobox, type the code (e.g. `541611`), wait ~2s for the typeahead, press **Enter**. The code appears as a chip under "NAICS results" and the result count updates.
   - Repeat for each additional NAICS code — multiple codes are OR'd. Element refs change after each search; re-snapshot to find the combobox's new ref each time.
4. **Set-aside for "small business or unrestricted" requests:** add BOTH `Total Small Business` AND `No set aside used` chips (OR'd; SB-only alone misses unrestricted opps).
5. **Status:** check "Active" only.

**⚠️ Do not type NAICS *expressions* into the keyword textbox** — `541611 OR 541519` as a keyword returns "No matches found". **However, a SINGLE bare NAICS code in the keyword-text box works and is the fastest path** (verified 2026-07-18: 541611 → 762, 541519 → 1,450, 611430 → 283 active results — keyword match, likely slightly broader than the NAICS-field widget). When volume per code is low enough that one 25-card page covers the freshest slice, prefer: type code into `keyword-text` + Enter → extract → repeat per code from a FRESH page load. Use the NAICS filter widget when you need exact NAICS-field matching or multi-code OR. If the two methods' counts diverge wildly, trust the widget and note the keyword count as an upper bound.

**Fast keyword-path details:** navigate to `https://sam.gov/search/?index=opp&sfm%5Bstatus%5D%5Bis_active%5D=true` (the `keywords=` URL query param does NOT populate the simple-search box — you must type + Enter). After Enter, wait ~5s and confirm render via `document.body.innerText.match(/Showing [\d,\s-]+ of [\d,]+ results/)`. Then extract with JS (below). Re-navigate fresh between codes — re-typing into a stale page is unreliable.

**Extraction JS** (works for both paths — verified): walk from each `h3 a` up ≤12 parents to the container whose innerText includes both `Notice ID:` and `Contract Opportunities`; capture `{title, url, raw: innerText.replace(/\s+/g,' ').slice(0,800)}`. `raw` carries deadline, notice type, agency/subtier/office, published/updated dates, awardee (award notices only). Full snippet in `references/sam-gov-ui-search.md`.

**Extracting results:** SAM.gov renders ~25 results/page as cards with an h3 title link (`/workspace/contract/opp/<id>/view`), Notice ID, deadline ("Current Response Date" / "Current Date Offers Due"), notice type, agency/subtier/office, and published/updated dates. A working JS extraction snippet for `browser_console` is in `references/sam-gov-ui-search.md`. Paginate with the "Next Page" button and re-extract per page. **Estimated value is NOT shown in list view** — open individual notices for dollar figures when filtering by contract value. Many results are Award Notices or sole-source presolicitations; filter by `notice_type` (Solicitation / Combined Synopsis / Sources Sought are the biddable ones).

**Detail-view URLs:** `https://sam.gov/workspace/contract/opp/<32-char-hex-id>/view`

**Aggregator access notes:**
- **HigherGov** gates anonymous users after a handful of free views ("You've used all of your free views") — expect a login/trial wall; treat it as a paid-only source unless the user has credentials.
- **State portals** (e.g. SC SCBO at web.casm.sc.gov, TX ESBD at txsmartbuy.com) reject bare curl (0 bytes/redirects) — drive them with the browser tool, not curl.

### Phase 6: SBIR.gov /topics Scraping + Direct API Attempts (Optional/Backup)

- **SBIR.gov `/topics` HTML pages ARE curl-able with a browser UA** — this is the most reliable way to enumerate all open SBIR/STTR topics with close dates. The dead parts are `/sbirsearch/*` (404) and the API:
- **DOE SBIR is structurally different from DoD SBIR.** DOE uses FOA numbers (DE-FOA-000XXXX) instead of topic numbers, a **pitch-first** Phase I (700 words, 4 criteria), and concurrent Phase I/Phase II releases. The program is administered by the Office of Science at `science.osti.gov/sbir`, not through DSIP. Phase I awards are ~$200K (vs DoD's ~$150K). See `references/doe-sbir-research.md` for the complete DOE-specific workflow.
```bash
# SAM.gov API — 403 / 401 without a key; do not rely on it
curl "https://api.sam.gov/entityapi/v2/opportunities?api_key=DEMO&..."
# /api/prod/opps/v2/opportunities returns 401 "Bad credentials" without a key

# SBIR.gov /sbirsearch/* — 404/stale; do NOT use
curl "https://www.sbir.gov/sbirsearch/solicitations?latest=open"

# SBIR.gov /topics — WORKS with UA; paginate ?page=0..N (~46 topics, 10/page)
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" \
  "https://www.sbir.gov/topics?page=0"
```

Full SBIR.gov listing+detail parser and DoD-portal notes are in `references/sbir-topic-scraping.md`.

**⚠️ Cross-check a second SBIR portal before declaring a deadline picture complete.** SBIR.gov `/topics` shows only the NEWEST DoD batch. An older still-open batch (which may close within days) drops off SBIR.gov but stays open on the DoD portal `www.dodsbirsttr.mil` (DSIP) and aggregators. DoW releases topics the first Wednesday of each month, closing the last Wednesday of the following month — so the urgent batch is often the one SBIR.gov no longer lists.

### Phase 7: Opportunity Data Extraction

For each relevant opportunity, extract:

| Field | Source |
|-------|--------|
| Agency | Article content, SAM.gov, solicitation header |
| Solicitation Number | Article content, SAM.gov |
| Title | Article headline, solicitation name |
| Estimated Value | Article, solicitation, announcement |
| Response Deadline | Article, SAM.gov, solicitation notice |
| Capabilities Sought | Performance work statement, article description |
| Set-Aside Status | Article, solicitation text (small business, SDVOSB, 8(a), HUBZone) |
| Source URL | Article permalink, SAM.gov link |
| Posted Date | RSS pubDate, article publication date |

### Phase 8: AI/Cyber/Data Relevance Flagging

Manually assess each opportunity for relevance to AI/cyber/data capabilities:

**High Relevance (⭐⭐⭐⭐⭐):**
- AI-specific solicitations (machine learning, autonomy, computer vision)
- Cybersecurity contracts (zero trust, threat detection, incident response)
- Data analytics platforms (big data, analytics, insights)
- Cloud services supporting AI workloads

**Medium Relevance (⭐⭐⭐):**
- Network security, IT modernization
- Research and development contracts
- Engineering with technology integration potential

**Low Relevance (⭐⭐):**
- Facilities, logistics, construction, staffing
- Pure services without technology component

### Phase 9: Grants.gov & NOFO Analysis (Cooperative Agreements, Grants, BAAs)

When the user provides grants.gov / simpler.grants.gov links, you are dealing with a different class of opportunity from FAR-based SAM.gov contracts. Key differences:

**Vehicle Types on Grants.gov:**
- **Grant:** Minimal government involvement. Awarded to accomplish a public purpose.
- **Cooperative Agreement:** Substantial government involvement (reviews/approves deliverables, training materials, participant lists). Most common for State Dept, USAID, HHS.
- **BAA (Broad Agency Announcement):** FAR 6.102(d)(2), 35.016. Used by DARPA, service labs for R&D. Can result in Procurement Contracts, OT Agreements, or Cooperative Agreements.

**Evaluation Structures (different from FAR 15):**
- Grant NOFOs typically use weighted merit review criteria (e.g., Quality 30%, Experience 30%, Cost 20%, Impact 15%, M&E 5%)
- DARPA BAAs use a two-step process: Step 1 mandatory conformance (originality check) → Step 2 comprehensive evaluation (scientific merit > qualifications > contribution to mission > transition > cost realism)
- No LPTA or tradeoff — these are peer/merit reviews by evaluation panels

**Eligibility Quirks:**
- Some grants are limited to state governments, nonprofits, or educational institutions — check eligibility FIRST before deep-diving
- For-profits may be eligible but with restrictions (e.g., State Dept prohibits profit/fee — cost recovery only)
- "All responsible sources" language in a BAA means truly open — but the evaluation favors established researchers with publication records

**Submission Systems:**
- Grants.gov Workspace (most common) — requires SAM.gov registration + Grants.gov account
- MyGrants (State Dept) — separate system, requires its own registration
- DARPA BAAT (Broad Agency Announcement Tool) — separate from Grants.gov, requires registration

**Required Forms (Grant NOFOs):**
- SF-424 (Application for Federal Assistance)
- SF-424A (Budget Information — Non-Construction)
- SF-424B (Assurances — Non-Construction)
- SF-LLL (Disclosure of Lobbying Activities)
- Detailed Budget (agency-specific Excel templates)
- Budget Narrative (justification for every line item)

**Format Requirements Vary Wildly:**
- DARPA BAAs: Typically 12pt font, specific templates for Vol I/II
- State Dept NOFOs: 15pt Open Sans (!), single-spaced, 1" margins, 20-page proposal + 2-page SOW
- DoD NFOs: 12pt Times New Roman, 10-page project narrative
- Always extract the formatting section from the NOFO — non-compliant formatting = disqualified

**Nested Attachments:**
- Grants.gov opportunities often bundle supporting documents in .zip files
- Some zips contain nested zips — unzip recursively until you reach PDFs/DOCX/XLSX
- Use `unzip -o <file> -d <dir>` for each layer

**Proactive adversarial review — required for complex NOFO analyses:** After completing a multi-source NOFO analysis (2+ entities, $0 past performance, teaming structure), run the adversarial gate from `quality-gate-pipeline` before the user asks for it. Dispatch a subagent with ALL source files (NOFO docs, entity dossiers, research artifacts, proposal drafts) and instruct it to cross-reference every claim. The subagent should produce its own structured HTML output saved to the briefings directory. The key value is cross-source credential contradiction detection — no single agent can catch every inconsistency in its own output. Do not wait for the user to demand this — common signals that an adversarial review is needed: first-time grant applicant, multi-entity teaming, conflicting personnel sources (e.g., internal dossiers vs. proposal resumes), untested budget assumptions, or NOFO-required elements not yet addressed. After the review, fix all P0 findings before delivering the analysis to the user.

**Forecast vs. Live:**
- Grants.gov distinguishes between Forecast (planned, not yet accepting applications) and Posted (live)
- Forecast listings show "Estimated Post Date" and "Estimated Application Due Date" — these can slip
- Before investing time in a forecast, check Grants.gov for the live posting

### Phase 10: Compile Report

Generate a markdown report at:
`~/govcon_research/raw/<date>/opportunities.md`

Structure:
1. Executive Summary (total value, key highlights)
2. Active Solicitations (open for bid, with deadlines)
3. Recent Contract Awards (task order opportunities)
4. GWAC/IDIQ Vehicle Awards (task order pipeline)
5. Major Programs (long-term opportunities)
6. Small Business Set-Aside Summary table
7. Recommended Actions for AI-focused firms
8. Search Strategy Notes
9. Disclaimer

## Output Format

### Opportunity Entry Template

```markdown
### 1. **[Solicitation Title] - $[Value]**

| Field | Details |
|-------|---------|
| **Agency** | [Agency name] |
| **Solicitation #** | [Number or "Check SAM.gov"] |
| **Title** | [Full title] |
| **Est. Value** | **$[value]** |
| **Response Deadline** | **[date]** |
| **Source URL** | [URL] |
| **Posted** | [date] |
| **Capabilities Sought** | [description] |
| **Set-Aside Status** | [status] |
| **AI Relevance** | ⭐[1-5] [explanation] |

**Key Details:**
- [bullet points of important specifics]
- [contract vehicle type, ordering period, requirements]
```

### Recommended Actions Section

Group by urgency:
- **Immediate (This Week)** - Opportunities with deadlines within 7 days
- **This Month** - Opportunities with deadlines within 30 days
- **Ongoing** - Continuous pipelines (SBIR, GWAC task orders)

## Source Patterns

### Google News RSS Query Pattern

```
https://news.google.com/rss/search?q=<query>&hl=en-US&gl=US&ceid=US:en
```

**Common Query Patterns:**
- `SAM.gov+solicitation+RFP+[year]`
- `federal+contract+opportunity+RFP+[month]+[year]`
- `SBIR+STTR+solicitation+[year]`
- `DoD+SBIR+open+topic+[year]`
- `AFWERX+SBIR+[year]`
- `GWAC+IDIQ+RFP+[year]`
- `site:fedscoop.com+RFP+solicitation`
- `site:govconwire.com+opportunity+solicitation`
- `DIU+defense+innovation+contract+[year]`
- `NSIN+opportunity+[year]`
- `SOFWERX+[year]`

### GovCon Wire Direct Scraping

GovCon Wire provides complete solicitation details in articles:
- Full PWS descriptions
- Exact deadlines
- Set-aside status
- Value estimates
- Agency information

**Reliable source for:** TSA, DOI, DIA, DMEA, DISA, LOC, MDA, SEWP announcements

## Critical: getting award descriptions (third-batch lesson, 2026-07-18)

**The `Description of Requirement` field returned by `spending_by_award` keyword search is NULL** for almost all awards. The search endpoint exposes the field name but the field is empty in the result rows. To get the actual scope text you MUST fetch each award's full detail via the `/awards/{generated_internal_id}/` endpoint:

1. Run the keyword search (single token or 2-word entity name).
2. From each result row, grab the `generated_internal_id` (format: `CONT_AWD_<PIID>_<agcy_code>_<parent_idv_or_-NONE->_<office_code>`, e.g. `CONT_AWD_7571PS26F00305_7571_75D30124D18711_7523`).
3. GET `https://api.usaspending.gov/api/v2/awards/{generated_internal_id}/` (note trailing slash).
4. Read `description`, `naics.code`, `naics.description`, `awarding_agency.subtier.subtier_name`, `awarding_agency.office_agency_name` from the response. The `description` field is populated and runs 1–10 lines — this is the scope text that reveals whether a prior award matches the new solicitation.

- `scripts/usaspending-detail-fetch.py` — Loops a list of PIIDs, fetches each award's full detail via generated_internal_id, and prints PIID, recipient, POP, amount, office, and description. Put this helper in front of the office-prefix matching step whenever the award topic is not obvious from the recipient name alone.
- `scripts/convert-markdown-proposal-to-docx.py` — Converts markdown proposal artifacts to properly formatted .docx per federal NOFO specs. Handles 15pt Open Sans body, Calibri 10pt tables, 1" margins, headings, tables, bullets, and inline formatting. Use when the user needs Word documents for final submission (e.g., MyGrants, Grants.gov). Run from the dfop/ directory: `python3 convert_to_docx.py` after modifying the __main__ block with source .md paths and output .docx paths.

## SAM.gov Notice-ID search unreliability (third-batch lesson, 2026-07-18)

The existing pitfalls section warns that `/opp/<notice-id>/view` 404s and that W-prefix notices drop out of active search. The third batch (8 Notices: 7571TE26Q00092, 7571PS26Q00058, 2032H326N00011, PANMCC25P0000017585, 15F06726Q0000322, 36C10D26Q0134, FA940126Q0022, 47QACA26Q0350) showed a broader failure: typing the Notice ID verbatim into the SAM.gov search box returned "No matches found" for ALL 8, even with both Active and Inactive status checkboxes ticked. This affected Q-prefix (RFQ), N-prefix (RFP), and P-prefix (Purchase) Notice IDs alike — not just W-prefix Special Notices.

**Implication:** do NOT burn browser tool calls trying to open the SAM.gov notice detail page for a batch of Notice IDs. Treat the user-provided title + the USAspending prior-award chain as the primary evidence and only fall back to SAM.gov browser search for the 1–2 notices where the title alone is genuinely ambiguous. The SAM.gov search box appears to require the notice's internal 32-char hex opportunity ID, not the human-readable Notice ID; the search box sometimes resolves a Notice ID via fuzzy match but it is unreliable and should not be the default path for batch research.

## Worked examples

All worked examples (per-batch tables with Notice ID, title, verdict, incumbent, prior award value, and work covered) live in `references/usaspending-new-work-vs-recompete.md` — three batches as of 2026-07-18 (8-example IT/kiosk/SIEM batch, 7-example medical/training/curriculum batch, and 8-example HHS/Treasury/Army/DOJ/VA/AF/GSA batch).

## Pitfalls

- **Never dismiss opportunities without fully reading eligibility AND attached documents.** When the user provides 3-5 links, evaluate EVERY one. What looks like "wrong domain" on first glance (e.g., DoD environmental program, HHS social services) may have cross-cutting priorities — "emerging technologies," "data/information management" — that make it viable. Read the full NOFO description, eligibility section, AND attached PDFs before classifying as "dead." Only hard-kill when eligibility explicitly excludes the entity (e.g., "state governments only").
- **Brief before deep-diving.** For multi-opportunity batches (3+ links), extract the basics from all links first (title, agency, due date, value, eligibility), create a summary table, and share with the user. Then interview for prioritization before spinning up research agents. The user wants to see the landscape and make go/no-go calls, not wait for exhaustive analysis on something they'll dismiss. However, do NOT hard-kill at this stage — flag all opportunities with a provisional assessment and let the user confirm drops. A July 2026 session prematurely killed 3 of 5 by title ("RESTORE = environmental", "CSBG = social services", "DoD EIE = natural resources") and the user pushed back. Present a full table with reasons for every proposed drop.
- **When updating an existing HTML briefing for a business stakeholder, rewrite the file ONCE.** A July 2026 session attempting to patch an existing Douglas briefing via multiple `patch(mode=replace)` calls produced broken CSS (duplicate `tr:nth-child` rules, wiped table styles). For significant content additions (new opportunities, new sections), rewrite the complete HTML file with `write_file` rather than incrementally patching. Patching is fine for small text fixes; content restructure = full rewrite.
- **Audience-appropriate briefing format.** When the briefing is for a business/contracts stakeholder (Douglas Henderson — PMP, DAWIA III, JD), strip all technical AI/architecture detail, agent methodology narrative, and version history. Focus on: vehicles, evaluation criteria weights, competitive landscape, past performance gaps, compliance requirements, risk matrix, and recommended actions by week. Use BD language: "winnability," "teaming strategy," "discriminator," not "model architecture" or "agent orchestration." Format: BLUF card → one large executive pipeline table (`.wrap` at 1200px, 12+ columns including Solicitation #, Due+countdown, Ceiling+PoP, Winnability badge, Key Risk, Strategy; `white-space:nowrap` headers; no horizontal scroll) → deep-dive per actionable opportunity (vehicle & terms, scope/workstreams, evaluation criteria with weights, competitive landscape, teaming strategy, submission checklist) → regulatory updates (CMMC, etc.) → risk matrix with severity badges → action items grouped by week with owners.
- **Grants.gov pipeline batches (3+ simpler.grants.gov links) follow a fixed orchestrator pattern.** (1) `web_extract` all links in parallel + unzip/extract all attached docs recursively (`unzip -o` each layer — grants.gov zips often nest zips); (2) quick-assess ALL opportunities in a table before any deep-dive — never dismiss by title alone; (3) interview user on which to pursue and in what order; (4) dispatch parallel sub-agents per opportunity for full requirements analysis (one agent per opportunity, each given ALL extracted docs as context, each writing `~/govcon_research/leatherneck-pipeline/<slug>/01-requirements-analysis.md`); (5) one competitive-landscape agent across all opportunities (incumbents, prior awards via USAspending, teaming landscape); (6) compile a master HTML briefing with executive table + per-opportunity deep-dive + risk matrix + weekly action items. Use the Douglas-format spec above. See `references/grants-pipeline-batch-workflow.md` for the full workflow and a worked 5-opportunity example.
- **Audience-appropriate briefing format.** When the briefing is for a business/contracts stakeholder (Douglas Henderson — PMP, DAWIA III, JD), strip all technical AI/architecture detail, agent methodology narrative, and version history. Focus on: vehicles, evaluation criteria weights, competitive landscape, past performance gaps, compliance requirements, risk matrix, and recommended actions by week. Use BD language: "winnability," "teaming strategy," "discriminator," not "model architecture" or "agent orchestration."
- **Empty results ≠ no incumbent.** The Notice-ID keyword search will always be empty; that's the trap. Switch to topic + agency.
- **The USAspending `/api/v2/recipient/` endpoint does NOT filter by search text.** It returns ALL entities sorted by total amount. However, the UUID-based `recipient/<recipient_id>/` GET endpoint DOES work — pass the `recipient_id` from award/transaction results (format: `<UUID>-C` for child level). For a full USAspending API reference, see `contractor-portfolio-analysis` skill's `references/usaspending-api-patterns.md`. For market-level competitive landscape scanning across NAICS codes (agencies, competitors, SDVOSB patterns), use `fedcon-competitive-landscape-scan`.
- **FPDS.gov has been consolidated into SAM.gov.** The FPDS ezsearch endpoint now redirects to SAM.gov search. All FPDS-sourced contract data is accessible through USAspending.gov's API. The `api.sam.gov/prod/federalaccounts/` endpoint requires an API key.
- **SAM.gov API blocks direct access.** Returns 403 Forbidden. Do not rely on API queries. Use Google News RSS and site scraping instead.
- **Firecrawl credits may exhaust mid-research.** When `firecrawl_scrape` returns 402/insufficient-credits, the MCP server auto-retries then fails. Do NOT keep retrying Firecrawl tools — use the browser tool (navigate + scroll + snapshot) for SAM.gov detail pages, USASpending API (api.usaspending.gov, free, no key) for award history, and `ddgr` CLI for web search. The `mcp__firecrawl__firecrawl_search` is credit-gated too; fall back to `web_search` when credits are empty.
- **Firecrawl MCP server can be unreachable** (not just credit exhaustion — the server itself may be down). When `mcp__firecrawl__firecrawl_search`, `firecrawl_scrape`, or `firecrawl_parse` return "MCP server unreachable" / "unreachable after 3 consecutive failures," do NOT retry — the server has been down for the session. Fall back to `web_search` for search queries and `web_extract` for page content extraction. These are faster and free for known URLs. For PDFs, `pdftotext -layout <file> -` reliably extracts text. Only attempt Firecrawl tools again in a subsequent session. Do not burn multiple turns retrying Firecrawl tools — one failure is definitive.
- **SAM.gov API v2 endpoint filters are BROKEN.** The API key authenticates correctly and the endpoint returns HTTP 200 with data, but EVERY content filter — `naicsCode`, `setAside`, `pscCode`, `noticeType` — is silently ignored. The response always contains the full unfiltered corpus (typically 27,925–45,624 results depending on date range). Only `postedFrom`/`postedTo` date parameters actually constrain results. Verified 2026-07-18 with a working API key: querying `naicsCode=541519&setAside=SDVOSBC` returned the same 29,583 results as an unfiltered query. **Do not design workflows around SAM.gov API filtering** — use the browser-based UI search (which DOES honor filters) or fall back to USASpending award data for competitive intelligence.
- **SAM.gov set-aside filter shows hardware, not services.** Searching SAM.gov by SDVOSB + Small Business set-aside returns overwhelmingly DLA/DoD hardware parts (valves, pumps, carpet, propulsion shafts). Federal consulting/cyber/training services with set-aside tags rarely appear in standalone SAM.gov solicitations — they flow through GSA Schedules, VA IDIQs, and GWAC task orders that don't surface publicly. For services opportunities, prefer: (a) USASpending competitive-intel approach (small-dollar award patterns by agency, identify SDVOSB-friendly offices), (b) browser-based Sources Sought keyword search (these DO appear with set-aside tags), (c) state procurement portals for sub-federal set-asides. See `references/samgov-api-reality-check.md`.
- **"Cast wide net → CSV → filter locally" is the preferred pattern.** When the user says to pull everything and sift, do not do one-at-a-time detail-page verification. Pull all available data from USASpending API (small-dollar awards by NAICS + keyword), SBIR portal (all topics), and SAM.gov browser search (Sources Sought only — the only filter that surfaces services). Dump to structured CSVs in `~/govcon_research/csv/` and process with Python scripts afterward. The user wants the raw data locally to find the 5-10% that actually applies.
- **USAspending keyword search matches too broadly for pinpoint queries.** The `keyword` parameter in `search/spending_by_award` matches anywhere in award descriptions, returning unrelated giant primes alongside relevant awards. For targeted incumbent discovery, filter by `awarding_agencies` (toptier agency name) + NAICS + `award_type_codes: ["A","B","C","D"]` + `award_amounts` band, then scan results for the contracting-office prefix match.
- **"SIEM" keyword matches Siemens, not Security Information Event Management.** Searching for `SIEM` in USASpending returns results dominated by Siemens Healthcare/Industry/Government — all large contractors with much higher dollar values than actual SIEM contracts. The five-letter substring `SIEM` appears in every Siemens award. Fix: use `"Security Information and Event Management"` as exact phrase, use `QRadar` as keyword surrogate (IBM's product used by VA), or combine program names (`GenISIS` + `SIEM`) and manually filter. For multi-query disambiguation, run separate searches per keyword combination and intersect results. Full GenISIS domain intel: `references/va-genisis-program-intel.md`.
- **SBIR.gov's `/sbirsearch/*` endpoints are dead (404) and its API is blocked — but `https://www.sbir.gov/topics` HTML pages scrape fine with curl + a browser UA.** Detail pages are server-rendered Drupal: title in `<h2>`, fields as pipe-delimited text (`Funding Agency | DOW | MDA |`, `Close Date | August 19, 2026 |`). Full parser in `references/sbir-topic-scraping.md`.
- **Porbanderwala SBIR API `?search=` and `?status=` params are no-ops.** The `/api/opportunities?search=cybersecurity&status=open` endpoint ignores filter params and always returns all 413 topics (sorted by recency). Pull the full dataset with paginated curl (`?page=1..22&pageSize=50`) and filter + score in Python. The API returns exactly the requested pageSize.
- **Porbanderwala API `abstract` field is empty for ~90% of topics.** Only ~40 of 413 topics have a non-empty abstract. When `abstract` is `""`, score on the `title` field alone. The `sourceUrl` in each result points to the DSIP topic page — use that for full descriptions when the title isn't enough to classify. DSIP pages are JS-heavy and 403 from direct curl; open with browser_navigate.
- **`sbir.defensebusiness.org` is a hijacked/parked domain serving gambling spam — never use it.** The real DoD SBIR/STTR portal is `www.dodsbirsttr.mil` (DSIP, "DoW SBIR/STTR Innovation Portal"). Treat unexpected content (casino, e-commerce, non-English storefront) on a GovCon-looking domain as a hijack signal: bail out and find the canonical .mil/.gov.
- **DoD SBIR batches overlap; SBIR.gov only lists the newest.** DoW releases topics the first Wednesday of each month, closing the last Wednesday of the following month. When a new batch goes live, the prior batch (often with only days left) drops off SBIR.gov `/topics` but stays open on DSIP/aggregators. Scans limited to SBIR.gov miss the most urgent deadlines — always cross-check `dodsbirsttr.mil` or an aggregator for "closing soon" topics.
- **Google News redirects require JavaScript.** Cannot resolve via curl. Use RSS for discovery, then fetch from source site directly.
- **Some sources return 404s.** FedScoop, DefenseScoop articles may 404. Work with available sources (GovCon Wire is most reliable for solicitation details).
- **Date filtering must be strict.** When the user specifies "HARD date constraint," only include items posted or updated within that window. Related announcements slightly outside window can be noted in "Additional Monitoring" section but not in main opportunity count.
- **SAM.gov page scraping requires browser.** The SAM.gov site uses heavy JavaScript. Do not attempt to scrape it directly with curl. Use the browser workflow in Phase 5 or secondary sources (GovCon Wire, Federal News Network) that report on SAM.gov postings.
- **GovCon Wire canonical URLs live at `/articles/<slug>`, not `/YYYY/MM/<slug>`.** Guessing a date-based slug from the RSS title 404s. Resolve the real URL via `curl -s "https://www.govconwire.com/?s=<keywords>"` and pull the `<a rel="bookmark">` href, then fetch that. Article body extraction: `<title>`, `<meta name="description">`, and paragraphs inside `div.entry-content` — full text, deadlines, set-aside, and ceiling are usually all in the first 15 `<p>` tags.
- **USAspending `business_categories` matches recipient SAM registration status, NOT award size.** Base IDV ceilings of $100M-$1B+ awarded to small-business-registered holders pass the filter. Always pair with an `award_amounts` band when hunting genuinely small actions. Sub-$250K-band queries also double as competitive intel: they name the incumbent small-biz winners. See `references/usaspending-opportunity-patterns.md`.
- **Searching USAspending by a SAM.gov Notice ID returns empty.** A Notice ID identifies a solicitation (pre-award), and USAspending only holds awards. To determine whether a Notice is new work or a recompete, search by topic keyword + awarding agency/subtier + NAICS, then match the contracting-office prefix on the Notice ID (chars before the fiscal-year segment, e.g. 36C262, FA3030, 75N98, 75H710) against prior Award ID prefixes. The most recent same-prefix same-topic recipient is the incumbent. Full method, title-signal table, and 15 worked examples in `references/usaspending-new-work-vs-recompete.md`.
- **USAspending `spending_by_award` keywords do NOT do phrase matching.** Multi-word topic queries like `"Civilian Guardian Course"` or `"NAVSUP WSS OJT"` return 0 results — this is a query-shape failure, not "no awards exist". Use single-token keywords (`"RFID"`, `"MedBridge"`, `"TCCC"`, `"Guardian"`) or two-word entity names (`"Templar Medical"`, `"Purdy Group"`) which work because the recipient-name field is one logical token. See the Keyword strategy section in `references/usaspending-new-work-vs-recompete.md`.
- **W-prefix Notice IDs (position-7 = W) are Special Notices / Sources Sought** and often disappear from SAM.gov active+inactive search after their response date. Don't burn tool calls retrying the SAM.gov page; infer scope from the user-provided title + the prior-award chain (same office prefix + same topic keyword on USAspending). See `references/usaspending-new-work-vs-recompete.md`.
- **SAM.gov `/opp/<notice-id>/view` URLs 404.** The Notice ID is not the URL slug; SAM.gov uses an internal 32-char hex opportunity ID. To open a notice: navigate to `sam.gov/search/`, click the Contracting domain button, type the Notice ID into the New Search box, click New Search, then click the h3 link in the results. The detail page's Description field is often truncated to amendment text (e.g. AMENDMENT ONE SITE VISIT); extract the surrounding fields via `browser_console` JS (slice `document.body.innerText` from `Description` to +3500 chars). The real SOW lives in the .docx/.pdf attachments (some gated).

- **Stop after 3-4 failed SAM.gov attachment download attempts.** The SOW/PDF download endpoints gate behind authentication even for attachments marked \"Public\". The resources LIST API (`/api/prod/opps/v3/opportunities/{oppId}/resources?api_key=null`) returns metadata (resource IDs, filenames, sizes) without auth, but the file download itself returns HTTP 200 with 0-byte body whether called from curl or browser fetch. The documented zip endpoint (`/resources/download/zip`) is the reliable path — if it also fails, STOP. For opportunity size/timeline questions, cross-reference with OrangeSlices (incumbent name/value/bidders), GovTribe (award date/PoP/ceiling), HigherGov (NAICS/duration), and USASpending (prior award chain). These four sources together can answer value and period-of-performance questions without the SOW PDF. Burning 10+ tool calls when the answer is triangulable from aggregator data is a net loss.
- **Office-prefix matching fails when the recompete moves to a different contracting office.** The new Sources Sought may carry a different office prefix than the incumbent contract because the agency consolidated procurement under a strategic buying center. E.g., HHS VMO support was awarded through 75P001 (OAS/ASA) but the recompete Sources Sought is issued by 7571TE (OMAS SBC-IT). Office-prefix-only searches will return "no matching prior award" and incorrectly classify the opportunity as NEW WORK. **Always run a topic-keyword + agency-wide search as a fallback** when prefix matching finds nothing — the incumbent is often sitting under a different office code. For Sources Sought with zero prefix hits, flag as LOW CONFIDENCE until the agency-wide keyword search confirms.
- **USAspending `Start Date` is period-of-performance start and can be in the FUTURE on modifications** — a descending sort surfaces far-future dates (2027+) first. Not a data error; don't filter on it as "award recency".

- **USAspending `spending_by_award` `sort` field names differ from `spending_by_transaction`.** Contracts use `"Base Obligation Date"` (not `"Action Date"` — that's a transaction-level field). IDV awards use their own field mapping (no `End Date`, has `Last Date to Order`). If the sort field is invalid, the API returns a 400 with the complete list of valid field names for that award-type group — the error body IS the authoritative reference. Start with `"Base Obligation Date"` for contracts and the error will correct you if needed.

- **USAspending `cfda_numbers` filter can be silently ignored or return non-matching data.** When filtering `spending_by_award` by `cfda_numbers: ["19.317"]` or `["19.901"]`, the API sometimes returns awards with completely different CFDA numbers (observed: HHS Medicaid awards under 93.778 returned when querying State Dept 19.317, and general State Dept awards under 19.xxx returned when querying 19.901). This is NOT a syntax error — the API returns 200 with `total` reflecting the unfiltered result count. **Workaround:** Combine `agencies` filter (by `toptier` name, e.g., `"Department of State"`) + `keywords` filter for program-specific terms (e.g., `"EXBS"`, `"Export Control"`). CFDA numbers can also differ between legacy awards and new opportunities (e.g., EXBS uses 19.901 in USASpending for existing awards but 19.317 on new DFOP NOFOs) — always verify first-page results to confirm the actual CFDA in use.

- **`spending_by_award` `fields` parameter is REQUIRED.** Omitting it returns 422 with `"Missing value: 'fields' is a required field"`. The `fields` array must use exact field names from the API's contract/IDV mapping (e.g., `"Award ID"`, `"Recipient Name"`, `"Description"`, `"Award Amount"`, `"Start Date"`, `"End Date"`, `"Awarding Agency"`, `"Awarding Sub Agency"`, `"Contract Award Type"`, `"Last Modified Date"`, `"Base Obligation Date"`, `"naics_description"`, `"psc_description"`, `"Recipient UEI"`). Invalid field names return 400 with the full valid-field list — use the error body as the authoritative reference.

- **USAspending sort-field discovery pattern:** when you need a specific sort, start with the most likely field name (e.g., `"Award Amount"` for value-based, `"Base Obligation Date"` for recency). If the API returns 400, the error body contains the complete valid-field mapping for that award-type group. Read it, pick the exact match, and retry. This is your fastest path — the error IS the documentation.

- **Sources Sought classification: the solicitation product name may not match the incumbent recipient name.** When the solicitation mentions a product (e.g., "Corepoint") but USASpending returns an unfamiliar incumbent (e.g., "Interoperability Bidco"), the product is proprietary and the entity is an OEM acquisition vehicle. Search the corporate merger/acquisition trail — acquisition-entity names (e.g., "BidCo") are common in healthcare IT private-equity rollups. The solicitation is for the same product even though the legal entity name changed after a merger or rebranding. See `references/sources-sought-classification-deep-dive.md` for the classification workflow and a worked VA Corepoint example.

- **Deadlines change.** Always verify deadlines on SAM.gov before acting. Article reports may be delayed or outdated.
- **Set-aside status may be ambiguous.** Some solicitations don't explicitly state set-aside. Mark as "Not specified" rather than guessing.
- **Past performance requirements are hidden in attachments, not the description.** SAM.gov detail pages don't surface "past performance required" in the text body — scan the Attachments table for filenames containing "Past Performance Questionnaire", "Relevant Past Performance Template", "Past Performance Information", or "CPARS". A Sources Sought (pre-RFP) won't have them; a Combined Synopsis/Solicitation with a past-perf attachment is a re-compete with an incumbent evaluation. For entities with $0 contracts, this is a mandatory filter — flag the opportunity as BLOCKED unless teaming with a prime that has past performance.
- **NAICS shift can exclude the incumbent from a small business recompete.** When a Sources Sought changes the NAICS code from the incumbent's prior award, check the incumbent's SAM registration for the NEW NAICS. Use HigherGov or SAM.gov entity lookup to check if the incumbent is registered as LARGE under the new NAICS — if so, they become ineligible for a small business set-aside. This is a massive competitive advantage for small business entrants. Cross-reference with any recertify-size-status language in the Sources Sought — that clause is often a deliberate signal from the CO that the incumbent may not qualify. Worked example: HHS VMO (July 2026) — incumbent Summit/Allocore held the award under NAICS 541512 but is registered LARGE under the new NAICS 541611, making them ineligible for a small business set-aside recompete.
- **USAspending awards detail endpoint has critical competitive intel beyond descriptions.** Always fetch the full award detail via `/awards/{generated_internal_id}/` and read `latest_transaction_contract_data` — it contains `type_set_aside`, `type_set_aside_description`, `naics`, `naics_description`, `number_of_offers_received`, `extent_competed`, and `product_or_service_code`. These fields paint the full competitive picture of the prior award and are NOT available in `spending_by_award` search results.
- **Delegation agent results DO NOT land in `~/.hermes/cache/delegation/` — they write to THIS SKILL'S reference files.** When you dispatch parallel delegation agents for per-opportunity USAspending history research and later need to check whether they completed: do NOT stop after checking `~/.hermes/cache/delegation/` for subagent-summary files. The agents dump their findings into `references/usaspending-new-work-vs-recompete.md` (incumbent, award values, verdicts) and `references/samgov-detail-page-verification.md` (set-aside, past-perf attachments, POC emails). Check `ls -la` on those reference files for modification timestamps NEWER THAN the briefing file, then read them directly. Also check for still-running USASpending processes (`ps aux | grep usaspending`) — if they're active, the research is still in-flight.

## Related Reference Files

- `references/fedcon-rss-queries.md` — Full list of Google News RSS query patterns for federal contracting research across 5 source categories.
- `references/sam-gov-ui-search.md` — Proven anonymous SAM.gov UI search workflow: NAICS/set-aside filter widget steps, result-count sanity checks, and a copy-paste JS snippet for extracting structured opportunity data (title, notice ID, deadline, type, agency, permalink) from result pages.
- `references/samgov-browser-extraction.md` — Fast single-NAICS keyword-box variant of the SAM.gov browser workflow: interaction sequence, verified card-extraction JS, list-view field inventory, and result-volume snapshots.
- `references/samgov-detail-page-verification.md` — Proven browser workflow for opening individual SAM.gov notice detail pages to extract set-aside, PSC, description, past performance requirements, and new-vs-recompete classification signals. Includes 3 worked examples from the 2026-07-18 scan.
- `references/competitive-landscape-via-contracting-office.md` — Tiered competitive landscape via contracting-office prefix search. Multi-cycle contract lineage reconstruction, NAICS shift analysis with size-standard comparison table, and Tier 1/2/3 classification framework for identifying teaming partners beyond the incumbent. Worked example: MARCORLOGCOM DMSS 4-cycle chain (PAI→Cervello→PAI→recompete).
- `references/usaspending-opportunity-patterns.md` — USAspending curl recipes for opportunity research: sub-$250K awards by NAICS, awarding-agency spend rollups, and filter pitfalls (small_business trap, future Start Dates).
- `references/usaspending-new-work-vs-recompete.md` — NEW WORK vs RECOMPETE classification from a batch of SAM.gov Notice IDs. Covers the Notice-ID-isn't-an-award trap, the single-group `award_type_codes` constraint, the **single-token keyword strategy** (multi-word phrases return 0), contracting-office prefix matching for incumbent discovery, title-signal table, W-prefix Sources Sought visibility trap, batch-efficiency guidance, the expected pipe-delimited output format, and **15 worked examples** across two 2026-07-18 batches (IT/kiosk/SIEM + medical/training/curriculum). Pair with `templates/usaspending-batch-research.py`.
- `references/usaspending-third-batch-examples.md` — Third batch (2026-07-18) of 8 worked NEW-vs-RECOMPETE examples across HHS/Treasury/Army/DOJ/VA/AF/GSA. Includes the procedural notes on SAM.gov Notice-ID search returning "No matches found" for all 8 (broader than the W-prefix trap), USAspending `Description of Requirement` being NULL in keyword results (must fetch detail via `/awards/{generated_internal_id}/`), and prefix-only office search returning 20+ awards per office. Pair with `scripts/usaspending-detail-fetch.py`.
- `references/usaspending-bulk-pull-to-dashboard.md` — **USASpending bulk "pull everything" pipeline.** Multi-NAICS sweep (16+ codes with pagination), agency rollup via `/api/v2/awards/aggregate/`, USASpending→compact field name mapping for UI, dashboard assembly pattern (skeleton → generate data → patch → deploy), browser console debugging for field name mismatches, and Nextcloud deployment. Use when the user says "pull ALL of it" with no filters — this builds an interactive dashboard, not a CSV for filtering.
- `references/zero-dollar-entity-grant-nofo-analysis.md` — Grant NOFO analysis for $0-revenue entities: NICRA vs 15% de minimis (2 CFR 200.414(f)), MTDC calculation (2 CFR 200.1), fringe benefits without payroll history, two-$0-org teaming strategy, personnel budget reconciliation, SBA risk assessment readiness, cross-source credential verification workflow, and common pitfalls from a worked SCALE Program example.
- `references/opportunity-requirements-analysis.md` — Full single-opportunity deep-dive pattern (go/no-go focused)
- `references/technical-deep-dive-deliverable.md` — Heavy-lift technical analysis deliverable (PWS reconstruction, systems mapping, competitor profiling, compliance framework). Use when the output is a multi-section research report for the BD pipeline, not just a go/no-go card.: extract SS notice + Draft SOW with `pdftotext -layout`, catalog every labor category and deliverable, discover incumbent via USAspending keyword search + full award detail endpoint (use `latest_transaction_contract_data` for set-aside/NAICS/offers/competition), run NAICS shift exclusion analysis, cross-reference with aggregator intel (HigherGov, Washington Technology), and produce a structured Go/No-Go viability assessment with a 48-hour action plan. Pair with `references/usaspending-new-work-vs-recompete.md` for incumbent classification.
- `references/sbir-topic-scraping.md` — Working SBIR.gov `/topics` curl+parse recipe (Drupal pipe-delimited fields, pagination), DoD portal map (DSIP at dodsbirsttr.mil; hijacked-domain warning), the two-overlapping-batches deadline trap, and the browser-tool pattern for Next.js/RSC SBIR aggregators that resist curl.
- `references/doe-sbir-research.md` — DOE SBIR/STTR research patterns: key differences from DoD SBIR (FOA-based, pitch-first, OSTI-managed), DOE site map (science.osti.gov/sbir, PAMS), Phase I→Concept Stage / Phase II→Development Stage redesign, concurrent Phase I/Phase II release cycles, SBIR Reauthorization Act impact on DOE, and worked example (DE-FOA-0003548 Genesis Mission). Load when researching DOE-specific SBIR opportunities.
- `references/subcontracting-prime-directories.md` — SBA/DoD/DOT/GSA subcontracting directories, registration process, SDVOSB value to primes, and GSA API setup. Fastest revenue path without past performance.
- `references/drone-dominance-cuas-lane.md` — Hegseth DDP / Replicator 2 / DAWG / DHS $1.5B C-UAS landscape. Software/services play (AI/ML, CMMC, PM, training) for entities without hardware. SBIR topic type patterns from 8 analyzed PDFs.
- `references/samgov-api-reality-check.md` — What actually works (and doesn't) with the SAM.gov v2 API. Filters are broken, set-aside searches return hardware not services. Use browser UI for filtering, USASpending for competitive intel.
- `references/sources-sought-pipeline.md` — 6-phase, 8-persona, 3-quality-gate multi-agent orchestrator pattern for producing submission-ready Sources Sought responses at scale. Includes full persona library, gap severity levels, workspace structure, and entity factsheet template.
- `references/sources-sought-response-drafting.md` — Proven 11-section Sources Sought response template with mandatory element checklist, PD sufficiency (YES/NO) pattern, ROM estimation methodology, SDVOSB cert gap disclosure pattern, Section 508 compliance pattern, transparency (what-we-are-not) pattern, multi-patch file construction technique, and the worked VA SIEM example (36C10B26Q0650).
- `references/sources-sought-classification-deep-dive.md` — Single-opportunity Sources Sought classification workflow: SAM.gov extraction → USASpending incumbent chain verification → OEM/corporate merger resolution → competitive landscape classification → strategic assessment → response recommendation. Includes a worked VA Corepoint (36C10B26Q0658) example with sole-source/single-OEM finding.
- `references/samgov-attachment-download.md` — SAM.gov attachment download via browser API interception: monkey-patch XHR/fetch, click "Download All", extract S3 presigned URL from JSON redirect, curl download + unzip + pdftotext. The only reliable method for downloading PWS/SOW PDFs from SAM.gov without an API key.
- `references/leatherneck-harbor-entity-factsheet.md` — Self-contained entity factsheet for Leatherneck + HARBOR to dispatch as context to every sub-agent in a response pipeline. Includes teaming structure, past performance strategy, capabilities matrix, and confidential-items exclusion list.
- `references/cmmc-phase2-suspension-2026-07-13.md` — CMMC Phase II (C3PAO) suspended July 13, 2026. Only self-assessments required. What stays, what's suspended, what it means for DoD proposals. Primary source citations. Critical for any DARPA BAA or DoD contract requiring CMMC.
- `references/sdvosb-product-procurement-patterns.md` — SDVOSB product procurement compliance: non-manufacturer rule (13 CFR 121.406), VAAR 852.219-73 \"cost of materials\" exclusion for supply contracts, limitations on subcontracting for SDVOSB resellers, the proven VA SDVOSB SIEM reseller model (ThunderCat, Four Points, Merlin, Alvarez), and a go/no-go checklist for product procurement opportunities.
- `references/va-genisis-program-intel.md` — Domain intelligence for the VA GenISIS program (Genomic Information System for Integrative Sciences): full contractor ecosystem, SIEM component history, incumbent chain for task orders, and the critical "SIEM matches Siemens" keyword disambiguation pitfall.
- `references/grants-pipeline-batch-workflow.md` — End-to-end orchestrator pattern for multi-opportunity grants.gov batches: parallel extraction, provisional triage without hard kills, parallel sub-agent requirements analysis, competitive landscape, master HTML briefing assembly with the Douglas-format executive table, and a worked 5-opportunity example from the July 2026 DICE/DFOP/EIE/CSBG/RESTORE + HHS-VMO/Treasury-FMBSS/VA-SIEM session.
- `references/exbs-program-intelligence.md` — EXBS domain knowledge bank: CFDA mapping (19.901 vs 19.317), USASpending award query recipe, major EXBS cooperative agreement recipients with award ranges and roles, five core assistance areas, SSTMA Academy profile, trade data sources for export control analysis, diversion detection methodologies, competitive landscape for the DFOP0018157 opportunity, and C4ADS methodology notes.
- `references/harbor-framework-opportunity-analysis.md` — **HARBOR 6-stage analytical framework applied to single-opportunity analysis.** How to run a SAM.gov opportunity through H-A-R-B-O-R (Harvest → Architect → Risk-Proof → Build → Operate → Replicate) to identify productization angles, produce a strategic briefing, and determine whether/how to respond. Covers the 3-agent parallel research pattern (Incumbent / Market / Build-vs-Buy), the M365 productization alternative for SaaS replacement opportunities, the HARBOR-structured briefing template with worked example (HHS ASPR due diligence, July 2026), and the 48-hour action plan pattern for tight deadlines. Distinct from standard opportunity discovery (this is single-opportunity deep analysis, not date-window pipeline scanning).
- `references/state-dept-cooperative-agreement-mechanics.md` — Complete State Department cooperative agreement submission mechanics: MyGrants attachment order, SF-424 form-by-form field mapping, 15% de minimis indirect cost rate methodology with MTDC calculation (2 CFR 200.414(f) + 200.1), PHFFA compliance (2 CFR 602-604), Trafficking in Persons certification trigger ($500K threshold, 2 CFR 175), branding requirements (brand.america.gov), reporting cadence (PMS quarterly + PPR), audit requirements, substantial involvement provisions, for-profit cost rules (FAR 48 CFR 30/31 precedence over 2 CFR 200 Subpart E per 2 CFR 600.101(b)), and research methodology with web-extraction pitfalls. Load when any State Department NOFO requires a submission compliance guide.