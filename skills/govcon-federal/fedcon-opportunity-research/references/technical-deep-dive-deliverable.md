# Technical Deep-Dive Deliverable Pattern

## When to Use

Load this reference when you have already identified a specific solicitation (Sources Sought, RFP, or award) and need to produce a **structured multi-section technical analysis deliverable** — not just a go/no-go assessment, but a full BD research report covering incumbent, PWS reconstruction, modernization context, competitor landscape, and compliance framework.

This is the heavy-lift deliverable that lives in `~/repos/federal-bd-pipeline/<solicitation-slug>/research/technical-analysis.md`.

## What Makes This Different from Opportunity Research

| Dimension | Standard Opportunity Research | Technical Deep-Dive |
|-----------|------------------------------|---------------------|
| **Goal** | Discover + triage (which ones to pursue) | Evaluate + prepare (how to win one specific one) |
| **Output** | Briefing table or go/no-go card | Multi-section research report in BD pipeline repo |
| **Depth per section** | 2-3 sentences per opportunity | 3-5 pages of analysis |
| **PWS reconstruction** | Not needed | Required — labor categories, security, deliverables |
| **Strategic context** | Optional | Required — how this contract fits modernization |
| **Competitors** | List of names | Portfolio values, strengths, past relationships |
| **Compliance** | CMMC/Security check | Full DFARS clause + directive mapping |

## Workflow

### Phase 1: Incumbency Chain Reconstruction

When search tools fail (Tavily 432, Firecrawl unreachable, browser Google times out), use USASpending exclusively:

```bash
# Step 1: Search for awards matching the topic and agency
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{"filters":{"keywords":["DISTRIBUTION MANAGEMENT","MARINE CORPS"],"award_type_codes":["A","B","C","D"],"time_period":[{"start_date":"2018-01-01","end_date":"2026-12-31"}],"agencies":[{"type":"awarding","tier":"subtier","name":"Department of the Navy"}]},"fields":["Award ID","Recipient Name","Award Amount","Description","Start Date","End Date","generated_internal_id","Awarding Agency","Awarding Sub Agency","Recipient UEI"],"page":1,"limit":30,"sort":"Award Amount","order":"desc"}' | jq '.results[] | select(.Description | test("DISTRIBUTION MANAGEMENT|DMSS"; "i"))'
```

**Key fields to extract:**
- `Award ID` — The contract/order number (e.g., M67004-23-F-3000)
- `generated_internal_id` — Needed for full detail endpoint (e.g., `CONT_AWD_M67004-23-F-3000_9700_N0017819D8338_-NONE-`)
- `Recipient Name`, `Recipient UEI` — For entity lookup
- `Award Amount` — Total obligations
- `Start Date`, `End Date` — POP
- `Awarding Sub Agency` — Confirms correct office

**Step 2: Get full competitive intel from award detail:**
```bash
curl -s "https://api.usaspending.gov/api/v2/awards/CONT_AWD_M67004-23-F-3000_9700_N0017819D8338_-NONE-/" | \
  jq '{description: .description, naics: .naics, type_set_aside: .latest_transaction_contract_data.type_set_aside_description, n_offers: .latest_transaction_contract_data.number_of_offers_received, extent_competed: .latest_transaction_contract_data.extent_competed, psc: .product_or_service_code, idv_agency: .parent_idv.piid}'
```

**Critical intel from `latest_transaction_contract_data`:**
- `number_of_offers_received` — Competitive intensity gauge
- `extent_competed` — "A" = Full & Open, "D" = Competed under SAP, "C" = Not Competed
- `type_set_aside_description` — Set-aside status (or null/empty for none)
- `naics`, `naics_description` — Confirm NAICS
- `product_or_service_code` — PSC for scope alignment

**Step 3: Chain prior award history by searching for consecutive contracts:**

The DOI in the award description (scope text) is usually stable across recompetes even when the contract number changes. Search narrower keywords from the description across a wider date window (8+ years) and sort by Start Date:

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" ... -d '{"filters":{"keywords":["DISTRIBUTION MANAGEMENT SUPPORT"],"time_period":[{"start_date":"2015-01-01","end_date":"2026-12-31"}]},"fields":["Award ID","Recipient Name","Award Amount","Start Date"],"page":1,"limit":100,"sort":"Start Date","order":"asc"}'
```

Build the incumbency chain as a table:

| Contract | Period | Incumbent | Award Value | Vehicle | Offers |
|----------|--------|-----------|-------------|---------|--------|
| M67004-18-F-4044 | 2018-2020 | PAI | $5.36M | GSA MAS | 4 |
| M67004-20-F-4104 | 2020-2022 | Cervello Global | $10.93M | GSA | 3 |
| M67004-23-F-3000 | 2022-2026 | PAI | $11.35M | SeaPort-NxG | 7 |

**Signal: losing and winning back.** If the same contractor held the scope, lost it, then won it back, that's important — it proves the incumbent IS beatable but also knows how to win recompetes.

### Phase 2: Competitor Profile Construction

Build competitor profiles by chaining USASpending endpoints:

```python
# Per competitor workflow:
for company in ["CHEROKEE NATION MANAGEMENT", "CORPS SOLUTIONS LLC", "RIVET OPERATIONS COMPANY"]:
    # Step 1: Get all awards to this recipient across relevant agencies
    search = POST /v2/search/spending_by_award/
    filters = {
        recipient_search_text: [company],
        award_type_codes: ["A", "B", "C", "D"],
        time_period: [{start_date: "2020-01-01", end_date: "2026-12-31"}]
    }
    
    # Step 2: Identify those at the TARGET agency (e.g., MARCORLOGCOM, Department of the Navy)
    for award in results:
        if contracting_office from NO_MARINE_CORPS_ID_prefix_regex:
            fetch detail via /v2/awards/{generated_internal_id}/
            record: contract, value, description, POP
    
    # Step 3: Assess relevance — same NAICS, same office, same PSC
```

**Profile structure:**
```markdown
| Rank | Contractor | HQ | Size | Key Strengths | MARCORLOGCOM Presence | Est. Portfolio |
|------|-----------|-----|------|--------------|----------------------|----------------|
| **N** | **Name** | City, State | Small/Large | Bullet capabilities | Specific contract names | ~$XXM+ |
```

For teammates / subtiers, also check acquisition-vehicle-level dollar concentration (how much of their total DoD portfolio depends on this specific IDIQ or office).

### Phase 3: PWS Reconstruction from Scope Areas

The Sources Sought scope areas ARE the PWS skeleton. Reconstruct the PWS by:

**3a. Systems Mapping**

For each scope area, identify the specific DoD IT systems involved:

| Scope Area | Primary Systems | Secondary Systems |
|-----------|----------------|-------------------|
| Distribution Analytics | GCSS-MC (SAP ERP), DPAS | DLA Transaction Services, IUID |
| Nodal Expediting | TMS, GATES, DSS | WebLDMIS, TC-AIMS II |
| Financial Mgmt | GFM, PowerTrack, WAWF | G-Invoicing, DTS |
| Freight Operations | GCSS-MC, IGC, Container Mgmt | DLA DIS |

Map to mission context:
- **GCSS-MC** = Marine Corps' SAP-based logistics ERP (supply, maintenance, transportation, financial)
- **IGC** = Integrated Global Combat — supply chain/inventory for prepositioning
- **TMS** = Transportation Management System
- **DLA DIS** = DLA Distribution Standard System

**3b. Labor Category Estimation**

Estimate FTE levels from scope breadth and location count:

| Labor Category | Estimated FTEs | Clearance | Rationale |
|---------------|---------------|-----------|-----------|
| Program Manager | 1 | Secret | COR interface, govt facility access |
| Logistics/Data Analysts | 5-8 | Secret | GCSS-MC system access |
| Field-Node Personnel | 8-12 | Secret (some) | Military installation access at 15+ nodes |
| Freight Specialists | 4-6 | NACLC/T1 | Port/depot operations |
| Financial Analysts | 2-3 | NACLC/T1 | TAC management, WAWF |
| HAZMAT Specialist | 1-2 | Varies | 49 CFR / IMDG / IATA certification |
| **Total** | **24-37** | — | — |

**3c. Security Requirements Estimation**

Key signal from Sources Sought: if the solicitation asks respondents to "disclose current security clearance level or company's eligibility for obtaining one," then **Secret FCL is required**. Map from scope:

| Condition | Requirement | Rationale |
|-----------|-----------|-----------|
| Military installation access | Secret FCL | Base access requires clearance or CAC sponsorship |
| GCSS-MC access | IT-II, Secret | Logistics ERP contains CDI and PII |
| OCONUS nodes (Japan, Guam, Germany) | Secret + host-nation agreements | SOFA-dependent |
| Port/depot operations only | TWIC + NACLC | Physical freight handling |
| Contract admin / data only | Tier 1 (NACLC) | No system access or classified handling |

**3d. Deliverable Schedule Reconstruction**

From the predecessor contract description on USASpending (e.g., "DMSS Transportation Support") and the scope areas, infer deliverable cadence:

| Deliverable | Frequency |
|------------|-----------|
| Monthly Status Report | Monthly |
| Distribution Performance Dashboard | Quarterly |
| Container/Asset Visibility Report | Weekly |
| Financial Reconciliation | Monthly |
| Freight Bill Audit | Monthly (within 30 days) |
| Process Improvement Recommendations | Quarterly |
| Transition Plan | Once (phase-in/phase-out) |

**3e. Applicable Directives Mapping**

Use agency type (Marine Corps, Navy, Army, etc.) to infer governing directives:

- **Marine Corps:** MCO P4610.19D (Distribution Mgmt), MCO P4400.150 (Supply Policy), MCO 4450.12A (HAZMAT)
- **Navy:** NAVSUP P-485 (Supply Procedures)
- **All DoD:** DTR 4500.9-R (Defense Transpo Regulation), 49 CFR 100-185 (HAZMAT)

**DFARS clauses** by category:

Category: Cybersecurity
- 252.204-7012 (Safeguarding CDI)
- 252.204-7019/7020 (NIST SP 800-171 Assessment)
- 252.204-7021 (CMMC)

Category: Service Continuity
- 252.237-7023 (Essential Contractor Services)
- 252.237-7024 (Notice of Essential Contractor Services)

Category: Payment
- 252.232-7003 (WAWF)
- 252.232-7006 (Wide Area Workflow)

Category: Security
- 252.239-7001 (IA Contractor Training)
- 252.204-7000 (Disclosure of Information)

Category: Contract Admin
- 252.243-7001 (Pricing Modifications)
- 252.246-7003 (Safety Notification)

### Phase 4: Strategic Context Mapping

Connect this specific contract to the agency's modernization initiatives. This adds depth that differentiates the analysis from a simple data dump.

**Marine Corps example — Force Design 2030:**

| Initiative | Contract Relevance |
|-----------|-------------------|
| Littoral Regiments | More distributed logistics nodes → more complex distribution |
| Pacific Pivot | Nodal expediting at Guam, Darwin, Okinawa becomes critical |
| MCPP-N Expansion | Container/freight operations for prepositioned equipment |
| GCSS-MC Modernization | Contractors will use and adapt to the evolving system |

**Other DoD modernization context sources:**
- Agency command plans (MARADMINs, ALNAVs, ALARACTs)
- Service-level logistics modernization pages (marines.mil, army.mil)
- Historical CBO/DOT&E reports on logistics posture
- PEO/PMO program briefings (PACOM/INDOPACOM logistics, etc.)

**Template:**
```markdown
### 4.1 [Agency's] Modernization Initiative
Force Design (formerly "2030") is the Commandant's restructuring for great-power competition:
- [Structural changes affecting logistics]
- [How this contract directly supports execution]
- [Key locations impacted by modernization]

### 4.2 How This Contract Supports [Initiative]
1. **[Scope area]** provides [specific capability needed for modernization]
2. **[Scope area]** supports [specific modernization objective]
3. **[Scope area]** enables [specific modernization outcome]
```

### Phase 5: Compliance Framework

Map all anticipated DFARS clauses, military orders, and regulatory requirements into a structured table:

```markdown
| DFARS Clause | Title | Relevance |
|-------------|-------|-----------|
| 252.204-7012 | Safeguarding CDI | GCSS-MC access |
| 252.204-7021 | CMMC Requirements | Cybersecurity maturity |
```

Separate table for military-specific requirements:

| Requirement | Reference | Impact |
|------------|-----------|--------|
| NISPOM | DoD 5220.22-M | Facility clearance |
| DTR | 4500.9-R | All cargo movement |
| Supply Policy | MCO P4400.150 | Class II/IX procedures |

Include compliance edge cases:
- **CMMC status** at time of writing (Phase II suspension, self-assessment vs C3PAO)
- **SCA wage determinations** for each work location (include note that multiple locations = multiple wage dets)
- **International SOFAs** (Japan SOFA, Germany NATO SOFA, Singapore MOU)
- **Small business limitations on subcontracting** (50% personnel cost rule for NAICS 541614)
- **ITAR/export control** if handling technical data for military equipment

### Phase 6: Location-Strategic Analysis

For solicitations with multiple performance locations, analyze the strategic significance of each:

```markdown
| Location | Type | Strategic Significance |
|----------|------|----------------------|
| Albany, GA | MCLB HQ | MARCORLOGCOM command; depot maintenance |
| Guam | Pacific Hub | Force Design Pacific pivot; emerging logistics node |
| Singapore | Strategic Port | SEA logistics hub; MRO capability |
```

This signals to the BD team which locations are high-value (and thus need their strongest personnel) vs. routine.

### Phase 7: Win Probability / Competitive Assessment

Quantify:
- **Number of offers on prior award** — 3-4 = moderate competition, 7+ = intense
- **Incumbent recompete history** — has scope been lost before? (beatable signal)
- **Set-aside change risk** — Sources Sought suggesting small business? Large primes excluded
- **NAICS shift** — new NAICS may disqualify incumbent (SR/MSB recertification check)
- **Past performance barrier** — 5 year / 2 project minimum blocks new entrants
- **Location breadth** — 15+ nodes across 7 countries favors incumbent with existing footprint

### Phase 8: Deliverable Structure

Save to `~/repos/federal-bd-pipeline/<solicitation-slug>/research/technical-analysis.md`

Sections:
1. Executive Summary
2. Incumbent Identification
3. Scope Deep-Dive (with systems map)
4. PWS Reconstruction
5. Agency Modernization Context
6. Industry Standards & Table Stakes
7. Competitor Profiles
8. Regulatory & Compliance Framework
9. Opportunity Assessment (Win Probability)
10. Research Methodology & Sources
11. Appendices (timeline, locations, maps)

## Tools and Workarounds

### When Search Tools Fail (Tavily 432, Firecrawl unreachable)

| Failed Tool | Replace With |
|-------------|-------------|
| Tavily search (`web_search`) | USASpending API for award data; Wikipedia for agency/modernization context; acquisition.gov (curl) for DFARS clauses |
| Firecrawl scrape | `web_extract` for known URLs; `curl -s` for government .gov/.mil pages (many work with browser UA) |
| Browser Google search | Google via curl + regex (snippets only — rate-limited); Wikipedia directly |
| SAM.gov detail page (when 404s) | USASpending award detail for prior award chain; skip SAM.gov entirely for the deep-dive |

### USASpending Endpoints Summary

| Endpoint | Purpose | Key Fields |
|----------|---------|------------|
| `POST /v2/search/spending_by_award/` | Find awards by keyword + agency + date | Award ID, Recipient Name, Award Amount, Start/End Date, generated_internal_id |
| `GET /v2/awards/{generated_internal_id}/` | Full award detail | description, naics, psc, latest_transaction_contract_data.* |
| `POST /v2/search/spending_by_recipient/` | Recipient-level rollup | Total obligations, award count, agency breakdown |

## Worked Example

Full worked example: `~/repos/federal-bd-pipeline/marcorlogcom-m67004-26-r-0008/research/technical-analysis.md`

This was produced by the session that created this reference. Key data points:
- Incumbent: PAI ($11.35M, 7 offers, F&OC, SeaPort-NxG)
- Incumbency chain: PAI(2018)→Cervello Global(2020)→PAI(2022)→Recompete(2026)
- Scope: 4 areas across 15 locations in 7 countries
- PWS: 7 sections, 9 labor categories (24-37 FTEs), Secret FCL
- Top competitor: Cervello Global (previous incumbent, could re-bid)
- 13 DFARS clauses, 10 military-specific requirements
