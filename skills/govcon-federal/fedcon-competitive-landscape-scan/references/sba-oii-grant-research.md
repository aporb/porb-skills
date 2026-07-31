# SBA OII Grant & Prize Competition Research Methodology

## The Problem: USASpending Blind Spot

SBA Office of Investment and Innovation (OII) runs two major competitive funding streams:

1. **Growth Accelerator Fund Competition (GAFC)** — prize competition (2014–present), 566 prizes totaling $33M+
2. **SCALE Program** — traditional grant (FY 2026 debut), $9M, ~20 awards

**Neither appears meaningfully in USASpending.gov.** The `spending_by_award` endpoint cannot surface GAFC prize awards because they aren't standard federal assistance awards. The `cfda_numbers` filter is silently ignored, and `keywords` filters return empty for OII-specific terms. SCALE may appear once awarded but won't populate during the competitive research phase.

## Primary Data Sources

### 1. SBA.gov Press Releases (Highest Authority)
- **Pattern:** `sba.gov/article/<year>/<mm>/<dd>/sba-announces-...-growth-accelerator-fund-competition-...`
- **URL stability:** Older releases may return 404 if moved/archived; search SBA.gov search tool as fallback
- **Content quality:** Full winner lists by theme area, organization names, states, award amounts, administrator quotes, program details
- **Coverage:** 2023, 2024, 2025 GAFC stage one and stage two winners

### 2. America's Seed Fund (americasseedfund.us/accelerators)
- **What it provides:** Current-year GAFC public directory with clickable organization profiles
- **Format:** Contact directory + theme area + organization descriptions + award amount
- **Best for:** 2025 GAFC awardees; lab-to-market and capital formation tracks
- **Limitation:** Only shows current year; historical data via press releases

### 3. SSTI (State Science & Technology Institute — ssti.org)
- **What it provides:** Independent cross-referenced winner lists; identifies SSTI member awardees
- **Format:** Blog posts with full lists linked to Airtable directories
- **Best for:** Cross-referencing SBA press releases; identifying repeat winners; ecosystem analysis
- **Example:** ssti.org/blog/sba-announces-2024-growth-accelerator-fund-competition-stage-two-winners-over-3-million-prizes

### 4. Third-Party Grant Consulting Sites
- **What they provide:** Program parameter extraction (funding amounts, deadlines, scoring criteria, eligibility)
- **Example:** BW&CO Consulting (bwcoconsulting.com) — extracted SCALE program parameters from the NOFO
- **Caution:** These are commercial entities, not official sources; cross-reference with grants.gov

### 5. Grants.gov (for NOFO details)
- **What it provides:** Official Notice of Funding Opportunity, eligibility, deadlines, submission requirements
- **Limitation:** Grants.gov search results may be behind session walls; direct URL access works but requires knowing the opportunity ID
- **Pattern:** grants.gov/search-results-detail/<opportunity-id>

## Research Workflow for SBA OII Opportunities

### Phase 1: Gather Program Parameters
1. Search web for `"SCALE Program" SBA "SB-OIIGA-26-001"` (or equivalent opportunity number)
2. Check grants.gov for the official NOFO
3. Cross-reference with third-party grant consulting sites for parameter extraction
4. Extract: total funding, award count, per-award cap, period of performance, deadline, eligibility, scoring criteria, priority tracks

### Phase 2: Identify Prior Awardees
1. Search SBA.gov for the prior year's GAFC press releases: `site:sba.gov "Growth Accelerator Fund Competition" winners`
2. If SBA.gov returns 404, use web search: `"Growth Accelerator Fund Competition" SBA winners 2024`
3. Extract from press releases: organization names, states, theme areas, award amounts
4. Cross-reference with americasseedfund.us/accelerators for current-year directory
5. Cross-reference with SSTI for independent verification

### Phase 3: Map Competitive Landscape
1. Classify each prior awardee by: organization type, defense relevance, repeat winner status
2. Identify the subset most likely to bid on the target track
3. Tier competitors: Tier 1 (direct defense mission + GAFC history), Tier 2 (partial defense adjacency or GAFC history), Tier 3 (strong defense credentials but no GAFC history)
4. For each tier, assess: incumbency strength, organizational scale, geographic positioning, partnership network

### Phase 4: Differentiate
1. Identify weaknesses shared by the competitor pool (e.g., accelerators without operational experience, universities without small business delivery capability)
2. Map the client's unique positioning against those weaknesses
3. Build positioning pillars that exploit structural gaps in the competitive field
4. Recommend partnership architecture that fills gaps while reinforcing differentiators

## Pattern: SBA OII Awardee Demographics

From 2023–2025 GAFC data, the consistent demographic is:

| Type | Share | Characteristics |
|------|-------|-----------------|
| Nonprofit ecosystem builders | ~40% | Innovation hubs, tech councils, rural entrepreneurship orgs |
| University-affiliated entities | ~20% | Research parks, tech transfer offices, venture studios |
| For-profit accelerators/consultancies | ~20% | SBIR/STTR support, defense tech scouting, manufacturing support |
| Economic development organizations | ~15% | State/regional economic development, MEP-adjacent |
| Industry associations | ~5% | National reach, member networks, policy advocacy |

Key finding: 65% of 2024 Stage One winners were NEW to the program. SBA OII actively seeks fresh entrants.

## SBA OII Leadership (as of 2026)

- **Bailey G. DeVries** — Associate Administrator, Office of Investment and Innovation
- **Brittany Sickler** — Director of Ecosystem Development, OII
- Both have been quoted extensively in GAFC press releases; their language signals evaluation priorities: "ecosystem building," "underserved communities," "strategic partnerships," "national network"

## Known Footguns

1. **USASpending API will waste your time for SBA OII research.** Skip it entirely for GAFC/SCALE competitive intel. The awards don't exist in the system.
2. **SBA.gov article URLs are unstable.** Direct links from older press releases may 404. Always have a search-based fallback.
3. **Grants.gov session walls block content extraction.** The page loads but the content is behind a session timeout modal. Browser navigation may be required to bypass.
4. **SAM.gov blocks automated fetch.** The SAM.gov solicitation page (sam.gov/opp/...) returned fetch errors. Use grants.gov for NOFO parameters instead.
5. **web_search returns empty for specific program queries.** The web_search backend appears to have sparse indexing of SBA program pages. Rely on web_extract of known URLs rather than ad-hoc search.
