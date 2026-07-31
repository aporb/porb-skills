# Opportunity Requirements Analysis — Deep-Dive Pattern

## When to Use

When the task is: "Analyze this Sources Sought / RFP / RFQ exhaustively — extract every requirement, assess whether [entity X] can realistically respond, and produce a go/no-go recommendation."

This is a step beyond new-work-vs-recompete classification. It's a full requirements decomposition + viability assessment + competitive landscape analysis + recommendation, typically producing a 400-600 line markdown document.

## Proven Workflow (6 Phases)

### Phase 1: Extract All Source Documents

Extract both the Sources Sought Notice AND the Draft SOW/Performance Work Statement using `pdftotext -layout`:

```bash
pdftotext -layout "<path to Sources Sought PDF>" /tmp/ss_notice.txt
pdftotext -layout "<path to Draft SOW PDF>" /tmp/sow.txt
```

The `-layout` flag preserves the field structure critical for government procurement documents. Always extract BOTH — the SS notice has format requirements and submission mechanics; the SOW has the actual scope.

### Phase 2: Extract Every Requirement from the SOW

Read the Draft SOW in full (even if it's 30+ pages). Catalog every:
- **Labor category** — name, key duties, certifications required (e.g., PMP, FAC-P/PM Level II)
- **Deliverable** — name, description, frequency (monthly, quarterly, as-required)
- **Task area** — structured tasks and subtasks
- **Additional requirements** — unique/modernization requirements (AI, emerging tech, specific tools)
- **Security/compliance** — background checks, clearances, HSPD-12, NIST, FedRAMP, CUI handling
- **Place of performance** — on-site vs hybrid vs remote, geographic constraints
- **Period of performance** — base + options

Organize these into a structured breakdown. This is the document's "single source of truth" for all subsequent analysis.

### Phase 3: Discover the Incumbent via USAspending

**Step 3a:** Search by topic keyword + awarding agency:

```bash
curl -s "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["A","B","C","D"],
      "keywords": ["<topic keyword 1>", "<topic keyword 2>"],
      "agencies": [{"type":"awarding","tier":"toptier","name":"<agency name>"}],
      "time_period": [{"start_date":"2020-01-01","end_date":"2026-12-31"}]
    },
    "fields": ["Award ID","Recipient Name","Description","Award Amount","Action Date","NAICS Code","Contract Award Type"],
    "limit": 10
  }'
```

**Crucial:** `award_type_codes` must be from a SINGLE group. Use `["A","B","C","D"]` for contracts, OR `["IDV_A","IDV_B",...]` for IDVs — never mix them. The API error body IS the authoritative reference for valid group members.

**Step 3b:** For the most relevant award, fetch the full detail via `/awards/{generated_internal_id}/`:

```bash
curl -s "https://api.usaspending.gov/api/v2/awards/CONT_AWD_<PIID>_<agcy>_<parent>_<office>/"
```

This endpoint returns critical fields NOT in the search results:

| Field | Location | What It Tells You |
|---|---|---|
| `type_set_aside` | `latest_transaction_contract_data` | **Incumbent's set-aside category** (WOSB, SDVOSB, 8a, etc.) |
| `type_set_aside_description` | `latest_transaction_contract_data` | Human-readable set-aside label |
| `naics` | `latest_transaction_contract_data` | **The NAICS the incumbent won under** |
| `naics_description` | `latest_transaction_contract_data` | NAICS description |
| `number_of_offers_received` | `latest_transaction_contract_data` | Competitive intensity (e.g., "7" means crowded field) |
| `extent_competed` | `latest_transaction_contract_data` | "A" = full and open, etc. |
| `product_or_service_code` | `latest_transaction_contract_data` | PSC code |
| `total_obligation` | Top-level | Current obligated amount |
| `base_and_all_options` | Top-level | Total ceiling |
| `period_of_performance.start_date` | Top-level | PoP start |
| `period_of_performance.potential_end_date` | Top-level | PoP end (all options) |
| `date_signed` | Top-level | Award date |

### Phase 4: Cross-Reference with SAM.gov and Aggregator Intel

- **SAM.gov listing:** Navigate to `https://sam.gov/opp/<hex-id>/view` (the hex ID from the SS notice's URL). Extract the notice type, PSC, NAICS, published date, and set-aside classification.
- **Washington Technology / GovConWire:** Search for news articles about the opportunity — these often include strategic context and agency intent.
- **HigherGov / GovTribe / GovConInABox:** Search for the incumbent's profile to get SBA certifications, size status per NAICS, GSA schedule data, and parent/subsidiary relationships.

### Phase 5: NAICS Shift Exclusion Analysis (Critical Strategic Pattern)

**This is one of the highest-value findings in a recompete analysis.** When the new Sources Sought uses a DIFFERENT NAICS code than the incumbent's award:

1. Check the incumbent's SAM registration for the NEW NAICS code's size status.
2. HigherGov's "Reported NAICS" section shows `[Small]` or `[Large]` per code.
3. **If the incumbent is registered as LARGE under the new NAICS, they may be excluded from a small business set-aside.**
4. Cross-reference with the Sources Sought's "recertify size status" language — this is often a deliberate signal that HHS expects the incumbent to be ineligible.

**Worked example (HHS VMO, July 2026):**
- Incumbent Summit/Allocore won under NAICS 541512 ($3.4M, PoP ending 09/06/2026)
- New Sources Sought: NAICS 541611, size standard $24.5M
- Summit/Allocore SAM registration: 541611 → **[Large]**, 541512 → **[Large]**, 541715 → **[Small]**
- Sources Sought explicitly states: "Language in any resultant RFQ will require all small businesses to recertify their size status at the submission of proposal. You are not required to respond to this sources sought notice if you cannot recertify your size as small."
- **Conclusion:** Summit/Allocore is likely ineligible for a small business set-aside under 541611. This is a MASSIVE competitive advantage for new SDVOSB entrants.

### Phase 6: Viability Assessment and Go/No-Go

Evaluate the bidding entity against EVERY requirement:

| Factor | Assessment |
|---|---|
| NAICS match | Is the NAICS in the entity's SAM registration? |
| Set-aside eligibility | SDVOSB/VOSB/8(a)/WOSB — does the entity qualify? |
| Past performance | Does the entity have relevant federal contract history? |
| Key personnel | Can the entity name qualified people for all labor categories? |
| Certifications | PMP, FAC-C, DAWIA, etc. held by proposed team members? |
| Location | Can the entity credibly perform at the required location? |
| Teaming needs | Is a partner required to fill gaps? |
| AI/tech differentiator | Does the entity have a unique capability the requirement explicitly asks for? |

Produce a Go/No-Go/Go-with-conditions recommendation with specific rationale for each condition.

## Deliverable Structure

A comprehensive requirements analysis should include:

1. **Executive Summary** — one-paragraph verdict
2. **Opportunity Overview** — table: Notice ID, type, dates, agency, NAICS, PSC, set-aside, PoP, POC
3. **Incumbent Analysis** — who holds the current contract, award details, PoP, set-aside, competitive intel
4. **Scope of Work Breakdown** — every labor category, deliverable, task area
5. **Capability Statement Requirements** — format, page limits, cover page elements
6. **Differentiator Analysis** — what makes this entity uniquely qualified (e.g., AI automation requirement)
7. **Gap Analysis** — past performance, personnel, location, certifications
8. **Competitive Landscape** — known competitors, their strengths/weaknesses, the NAICS exclusion angle
9. **Go/No-Go Recommendation** — with specific conditions and risk mitigations
10. **48-Hour Action Plan** (if deadline is tight) — timeline with concrete actions
11. **Open Questions** — decision points the entity leadership must resolve