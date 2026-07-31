# Sources Sought Classification Deep-Dive

## When to Use This Pattern

When the user asks about a single Sources Sought opportunity and wants:
- Incumbent chain verification (not just current contract — the full history)
- Competitive classification (sole source vs competitive, single-OEM vs reseller market)
- Strategic assessment (should we respond? how?)
- Corporate/OEM relationship analysis (when the solicitation product name doesn't match any recipient name)

This is the **single-opportunity deep-dive** pattern, distinct from the batch recompete classification in `usaspending-new-work-vs-recompete.md`.

## Workflow (7 Steps)

### 1. Extract SAM.gov Listing
Navigate the SAM.gov detail page via browser (`browser_navigate` + `browser_snapshot` with `full=true`). Capture:
- Notice ID, title, type (Sources Sought / Combined Synopsis / RFI), status
- Agency, office, PSC, NAICS, set-aside
- Description (verbatim)
- Response deadline, published date
- Attachments (count, sizes, filenames — note which are PWS vs RFI vs cover)
- POC email and phone

**Pitfall:** SAM.gov SPA attachments require authenticated session cookies to download. In headless browser mode, the attachments table is visible but individual file downloads typically fail (links resolve to JavaScript handlers, not direct URLs). Note the attachment names/sizes and advise manual download. Do not burn 5+ tool calls retrying — the listing content is sufficient for classification.

**Browser-click download warning:** Clicking the "Download All" button or individual PDF links via `browser_click` on the SAM.gov detail page does NOT trigger a file download in headless browser mode — the page may show no visible reaction, and no file appears on disk. The only reliable method for automated download is the API interception technique documented in `samgov-attachment-download.md` (monkey-patch XHR/fetch → click → extract S3 presigned URL → curl download). If that's not feasible within the time budget, accept the attachment as gated and proceed with the listing-level data.

### 2. Search USASpending by Product/Topic Keywords
Use `spending_by_award` with topic keywords (the product name, the requirement type):
```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "keywords": ["Corepoint"],
      "award_type_codes": ["A","B","C","D"]
    },
    "fields": ["Award ID","Recipient Name","Award Amount","Base Obligation Date",
               "Description","Start Date","End Date","Awarding Agency",
               "Contract Award Type"],
    "limit": 20, "page": 1,
    "sort": "Base Obligation Date", "order": "desc"
  }'
```

**Critical:** `award_type_codes` must all be from ONE group. Contracts: `["A","B","C","D"]`. IDVs: `["IDV_A","IDV_B","IDV_B_A","IDV_B_B","IDV_B_C","IDV_C","IDV_D","IDV_E"]`. Mixing groups returns 400.

**Sort field:** Use `"Base Obligation Date"` for contracts, not `"Action Date"` (that's transaction-level). If wrong, the error body lists all valid fields.

**Alternative: `recipient_search_text` + `agency` for broad contractor searches.** When you know the contractor name but not the specific award IDs, use `recipient_search_text` (array of entity-name substrings) paired with `agency` (toptier agency code, e.g. `"036"` for VA). This is faster and cleaner than keyword search when the recipient is a well-known entity with many contracts:
```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["MedBridge"],
      "award_type_codes": ["A","B","C","D"],
      "agency": "036"
    },
    "fields": ["Award ID","Recipient Name","Start Date","End Date",
               "Award Amount","Description"],
    "limit": 50
  }'
```
Run separate queries for contracts (`["A","B","C","D"]`) and IDVs to get the complete picture. This avoids the noise of DoD/other-agency awards that a pure keyword search picks up.

Filter results to the relevant agency (VA) and office (matching prefix pattern — e.g., 36C263 for VISN 23, 36C10B for TAC NJ). The most recent same-agency award with matching product description is the incumbent.

### 3. Search by Incumbent Recipient Name
Once you identify the incumbent recipient name, run a second query by recipient to get their full history:
```bash
# Use keywords matching the recipient entity name
curl ... -d '{"filters":{"keywords":["Interoperability Bidco"],"award_type_codes":["A","B","C","D"]}, ...}'
```

Also query for the prior incumbent if there was a transition (e.g., Corepoint Health → Interoperability Bidco).

### 4. Pull the Base IDV
If delivery orders reference a parent IDV (e.g., "36C26320D0009"), query it separately using IDV award types to get the ordering period and ceiling:
```bash
curl ... -d '{"filters":{"award_ids":["36C26320D0009"],"award_type_codes":["IDV_B_B"]}, ...}'
```

### 5. Resolve Corporate/OEM Relationships
When the solicitation mentions a product name but the incumbent is a different-named entity:
- The product name is usually the OEM product brand (e.g., "Corepoint Integration Engine")
- The incumbent entity name may be an acquisition vehicle (e.g., "Interoperability Bidco, Inc.")
- Search for: `"[product] [incumbent] acquisition"`, `"[product] merger"`, `"[incumbent entity] dba"`
- Common signals: "BidCo" or "Bidco" in entity name = private equity acquisition vehicle
- Check company policy pages (footer copyright line often reveals legal entity name)
- Check LinkedIn and press releases for rebranding announcements

**Key insight:** In healthcare IT, products are often acquired and rebranded multiple times while the federal contracts continue under the original or intermediate legal entity name. The solicitation title often uses the product brand name (e.g., "Corepoint") but the award recipient is the acquiring entity's legal name.

### 6. Classify the Competitive Landscape
Based on the OEM analysis and incumbent chain:

| Classification | Signal | Example |
|---|---|---|
| **Sole Source / Single OEM** | Proprietary product, one manufacturer, 10+ year incumbent, no reseller network found | Corepoint Integration Engine |
| **Brand-Name with Resellers** | Proprietary product but authorized reseller channel exists (e.g., Cisco, Microsoft) | GSA Schedule software |
| **Competitive** | Multiple awardees, non-proprietary requirement, generic PSC | IT support services |

**Set-aside assessment:**
- Blank set-aside on a Sources Sought = acquisition strategy TBD
- If sole-source, FAR 6.302-1 applies (no set-aside possible)
- If competitive and VA, SDVOSB set-aside may apply per VAAR 819.70 (Veterans First)

### 7. Assess Strategic Fit and Recommend Response
For each entity (e.g., Leatherneck + HARBOR):
- **Can we provide this?** (direct product, reseller, or alternative)
- **Set-aside advantage?** (SDVOSB prime preference at VA)
- **Past performance gap?** ($0 contracts = neutral per FAR 15.305(a)(2)(iv), but a weakness)
- **Timeline urgency:** Days to response deadline, months to contract end
- **Response recommendation:** Submit capability statement? Wait for RFP? Partner? Skip?

## Worked Example: VA Rhapsody Corepoint Sustainment (36C10B26Q0658)

### SAM.gov Extraction
- **Notice ID:** 36C10B26Q0658
- **Title:** DA01--NTP Rhapsody Corepoint Sustainment Contract (VA-26-00070018)
- **Type:** Sources Sought
- **Agency:** VA, TECHNOLOGY ACQUISITION CENTER NJ (36C10B)
- **PSC:** DA01 | **NAICS:** 541519 | **Set-Aside:** (blank)
- **Response:** Jul 23, 2026 (6 days from posting)
- **Attachments:** PWS (114 KB), RFI instructions (27 KB), cover doc (14 KB) — all Public, all undownloadable via headless browser

### USASpending Incumbent Chain (verified via API)
```
Current:  Interoperability Bidco, Inc.  — $141,128  (Nov 2024–Oct 2026)  36C26325C0018
Prior:    Corepoint Health, LLC (IDIQ)  — ~$62K/yr   (FY20–FY24, 5 DOs)   36C26320D0009
Earlier:  Corepoint Health, LLC         — $294,277   (FY15–FY19, license)  VA26314P1320
Earliest: Corepoint Health, LLC         — $59,000    (FY14)                VA26314P0079
```

### Corporate Resolution
- Corepoint Health, LLC → acquired by Lyniate (2019) → legal entity "Interoperability Bidco, Inc."
- Lyniate rebranded to Rhapsody (Apr 2023)
- Interoperability Bidco, Inc. = legal entity name, doing business as Rhapsody
- **Verdict: Single OEM** — Interoperability Bidco is the sole manufacturer of Corepoint Integration Engine. No authorized federal reseller network found.

### Classification
- **Sole Source / Single OEM**
- Competitive barrier: EXTREMELY HIGH (proprietary engine, 13-year VA lock-in, clinical system dependencies)
- Likely acquisition path: FAR 6.302-1 sole-source justification, or brand-name with competition limited to authorized resellers

### Strategic Assessment
- Leatherneck is NOT an authorized Corepoint reseller
- No set-aside means SDVOSB provides no preference advantage
- $0 past performance is a weakness (neutral rating, but still missing)
- 6-day response window is aggressive
- **Recommendation:** Submit capability statement positioning AI-augmented HL7 sustainment generally (not Corepoint-specific). Advocate for SDVOSB set-aside if competitive. Explore Rhapsody partnership channel in parallel.

## Output Template

For single-opportunity research, deliver a markdown file at:
`~/sources-sought-responses/research/<Notice-ID>-research.md`

Sections:
1. Solicitation Snapshot (table)
2. Incumbent Chain — Verified via USASpending (table with all awards, periods, amounts)
3. Incumbent Chain Summary (ASCII timeline)
4. Corporate / OEM Relationship Analysis
5. Competitive Landscape Classification
6. Incumbent Federal Footprint (if relevant)
7. Key Dates & Urgency
8. Strategic Implications (entity-specific)
9. Data Sources (table: source × method × verification status)
10. Next Actions (checklist)

**RUSH variant (≤4-day deadline):** When the user says "RUSH" or the response deadline is within 4 days, prioritize actionability over exhaustiveness. Use this section structure instead:

1. **Opportunity Summary** — full table with all SAM.gov fields + POC email
2. **Incumbent Chain — Verified** — full DO chain table + parent IDV details + current DO deep-dive
3. **Full Landscape** (when incumbent has 30+ contracts) — comprehensive table of all same-agency awards, grouped by VISN/NCO, with amounts and periods. This establishes entrenchment at a glance.
4. **Classification & Competitive Assessment** — competition profile table, Sources Sought signal analysis (what NCO is really testing), competitive position matrix (strength/weakness/mitigation), past performance flag
5. **Response Strategy (RUSH)** — minimum deliverable, key questions to resolve, pre-drafted CO email
6. **Data Sources** — table: source × status × verification
7. **Attachments & Raw Files** — paths to supporting data
8. **Verdict** — decision table: Pursuit Viability / Effort Required / Strategic Value / Deadline Risk, each rated LOW/MEDIUM/HIGH, plus a one-line RECOMMENDATION

The Verdict table is the key addition — it forces a go/no-go recommendation in one glance. The pre-drafted CO email saves the user from drafting from scratch on a tight clock. See `36C24426Q0800-research.md` (VISN 04 MedBridge Sources Sought, 4-day window) for a worked RUSH example.