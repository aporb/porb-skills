# Common Fact-Check Targets for GovCon Adversarial Reviews

Recurring patterns of false/overstated claims encountered across reviews. Each entry describes the claim type, why it's commonly falsified, how to verify it, and the typical severity.

---

## Government Report Quotations

**Pattern:** A response quotes a real GAO, CBO, NIST, or IG report — but the quoted text is fabricated, paraphrased beyond recognition, or attributed to findings the report never made.

**Why it's common:** Writers want to cite a government authority to support their argument but haven't actually read the report. They invent a quote that sounds plausible and hope nobody checks.

**Verification:**
1. Search for the report number on the issuing agency's website (gao.gov, nist.gov, cbo.gov)
2. Read the "Highlights" or "What GAO Found" section — these summarize the actual findings
3. Search the report text for the quoted phrase verbatim
4. If the quote describes a finding materially different from the actual report findings, it's fabricated

**Severity:** P0. A single fabricated government quote makes the entire response non-credible. A CO can verify this in 30 seconds.

**Example from session:** `"GAO-25-107402 found that federal agencies' due diligence programs 'lack consistent risk assessment.'"` — The actual report found 3 of 11 agencies lacked documented processes for *SBIR/STTR* due diligence specifically. The quoted phrase does not appear anywhere in the report.

---

## DEA Registrant Database as Public API

**Pattern:** Claiming the DEA's Controlled Substances Act registration database as a free, publicly accessible API for automated screening.

**Reality:** The DEA registration database is **not publicly accessible via API.** It is restricted to authorized users (DEA registrants, law enforcement, state PDMPs). Public access is limited to single-registration lookups through the DEA's Registration Validation tool, which requires a DEA number to query — not batch-screening.

**Verification:** 21 CFR Part 1301 governs DEA registration data. No public API endpoint exists on DEA's website.

**Severity:** P0. This demonstrates either ignorance of the regulatory landscape or willingness to fabricate data source availability. Either is fatal.

**Applies to:** HHS, FDA, DOJ, pharmaceutical, medical supply chain, or any due diligence response involving controlled substances.

---

## "No New ATO Required" for M365 GCC High Custom Apps

**Pattern:** Claiming custom applications built on Microsoft 365 GCC High (Power Apps, Dataverse, SPFx web parts, Power Automate with custom connectors) "inherit FedRAMP High authorization" and require "no new ATO."

**Reality:** While M365 GCC High as a **platform** holds FedRAMP High authorization, custom applications change the security boundary. Every federal agency has its own SDLC/EPLC process (HHS has EPLC; DOD has RMF; Treasury has TLCM). Custom applications require:
- Security categorization (FIPS 199)
- Privacy impact assessment (PIA)
- Risk assessment (NIST 800-30)
- System Security Plan (SSP)
- Authorization to Operate (ATO) at the application level

**Verification:** Check the specific agency's IT governance policy. HHS OCIO Policy for IT Governance explicitly requires EPLC assessment for any system processing agency data, regardless of underlying infrastructure authorization.

**Severity:** P0. A CO who knows their agency's ATO process will immediately flag this as misleading. The claim signals either ignorance of federal IT governance or willingness to mislead about compliance burden.

**Applies to:** Any response proposing M365/Power Platform solutions on government tenants.

---

## DAWIA Certification Functional Series Mismatch

**Pattern:** Listing someone's DAWIA certification under the wrong functional area. E.g., "DAWIA III PM" for someone who holds "DAWIA Level III (1102 Contracting Officer)."

**Why it happens:** The response author sees "DAWIA Level III" and assumes all DAWIA certifications are equivalent, not understanding they're functional-area-specific.

**Reality:** DAWIA certification levels are tied to specific functional areas:
- 1102 = Contracting
- Program Management = different functional area
- Life Cycle Logistics = different functional area
- Engineering = different functional area

A DAWIA III in Contracting does NOT equal a DAWIA III in Program Management.

**Verification:** Cross-reference the claimed certification against team member resumes, bios, and DAU records. DAWIA certifications are always listed with their functional area designation.

**Severity:** P1. A CO may not catch this on a Sources Sought, but on a full proposal with key personnel requirements, misrepresenting a certification's functional area is protest bait.

---

## SBIR Award Amounts Without Contract Numbers

**Pattern:** Stating a specific SBIR dollar amount ($307K, $1.2M) without providing the award number, phase designation, or verifiable source.

**Reality:** SBIR Phase I awards are typically capped at $150K (DoD FY2024-2025). Phase II awards are typically $750K-$1M. Amounts that don't align with these brackets need evidence (contract number on SBIR.gov or USAspending.gov).

**Verification:** Search SBIR.gov awards database by PI name, or check USAspending.gov for the specific contract.

**Severity:** P1. Without a contract number, the dollar figure is unverifiable. If the amount doesn't match SBIR phase norms, it's suspicious.

---

## Security+ Listed When Higher Certifications Are Held

**Pattern:** Listing CompTIA Security+ as a credential when the person holds substantially more rigorous certifications (CISA, CISSP, CASP+). This often happens because the verified background file explicitly states NOT to use Security+ — it "undersells" the person.

**Reality:** Security+ is an entry-level certification. Listing it alongside or instead of CISA/CISSP signals the person is junior. The user's own verified background files may contain explicit instructions about which certifications to use and which to suppress.

**Verification:** Check the verified background file for explicit "Do NOT use" instructions. Cross-reference all listed certifications against the verified background.

**Severity:** P1. Violating the user's own explicit directive while also underrepresenting the team's credentials.

---

## "Free Government API" Claims That Are Downloadable Files

**Pattern:** Claiming that OFAC, HHS OIG, BIS, or similar government data sources offer "free government APIs" that can be integrated via simple HTTP GET requests in a real-time screening workflow. The response may list 6+ sources under the blanket label "all free government APIs" accessible via "Power Automate HTTP connector."

**Reality:** Most government compliance data sources publish **downloadable flat files** (CSV, XML, TXT), not REST APIs. The integration pattern is batch ETL — scheduled download → parse → transform → store → query — not real-time API calls. This is a fundamentally different and more complex integration model.

| Source | Actual Access Method |
|---|---|
| OFAC SDN List | CSV/XML file download via Sanctions List Service. No REST API. |
| HHS OIG LEIE | Monthly CSV download from oig.hhs.gov. No query API. |
| BIS Denied Persons List | .TXT file download from bis.gov. No API. |
| SAM.gov | Authenticated REST API (requires API key registration via sam.gov). Not "free and open" — requires account. |
| SEC EDGAR | Free REST APIs, no authentication — legitimately free and open. |
| USAspending.gov | Free REST API — legitimately free and open. |

Only 2 of these 6 have true free REST APIs. The rest require file download + parsing + periodic refresh.

**Verification:** For each claimed "API:"
1. Navigate to the agency's developer/data access page
2. Check whether they offer a documented REST endpoint (not a download link) or a downloadable file
3. Check authentication requirements (API key = not "free and open")
4. Check whether the endpoint supports parameterized queries or only full-dataset downloads
5. Verify refresh cadence (daily CSV download vs. real-time query)

**Severity:** **P0** if the response's entire architecture depends on real-time API calls to sources that only publish downloadable files. This is the single most common false claim in GovCon due diligence/screening and supply chain vetting responses. If the integration pattern is ETL rather than API, the ROM cost estimate and timeline are likely wrong by a factor of 2-3x.

**Applies to:** Any response proposing automated screening or due diligence against government watchlists, exclusion lists, compliance databases, or entity registries.

---

## FDA Enforcement Database API Accessibility

**Pattern:** Claiming that FDA enforcement data — warning letters, Form 483 observations, consent decrees, import alerts — is available through openFDA or other free government APIs for integration into an automated screening workflow.

**Reality:** openFDA (open.fda.gov) provides APIs for drug/device **product recall** enforcement reports, adverse events, product labeling, and registrations. It does **NOT** provide APIs for:
- **Warning Letters** — confirmed by openFDA team: "The openFDA platform does not currently provide APIs for retrieving FDA-issued Warning Letters or Form 483 inspection reports" (Open Data Stack Exchange, May 2025)
- **Form 483 inspection observations** — no openFDA endpoint. The FDA Inspections Dashboard requires an OII Unified Logon authorization key — it is not a public API
- **Consent decrees** — no structured data source exists
- **Import alerts** — published as unstructured web pages, no API

FDA Warning Letters are published on fda.gov as an unstructured web database — integration requires web scraping (fragile, possibly against ToS) or FOIA requests. This is the exact data the response typically claims as its competitive differentiator over commercial platforms like Dow Jones or LexisNexis.

**Verification:**
1. Check open.fda.gov/apis/ — the complete endpoint list. If Warning Letters or 483s aren't listed as endpoints, they're not available via API
2. openFDA endpoints include: drug adverse events, drug labeling, NDC Directory, drug recall enforcement, drug Orange Book, Drugs@FDA, drug shortages; device 510(k), classification, recall enforcement, adverse events, PMA, recalls, registration/listing, UDI; food enforcement. **No Warning Letter endpoint. No 483 endpoint.**
3. Check open.fda.gov/about/status/ for the definitive list of all available endpoints

**Severity:** **P0.** This is often the core differentiator the response uses to claim superiority over commercial platforms (e.g., "Dow Jones does not natively integrate FDA enforcement databases… Neither do its competitors."). If the data source doesn't have an API, the proposed solution faces the exact same integration barrier as the commercial platforms it criticizes — the claim is hollow.

**Applies to:** HHS, FDA, pharmaceutical, medical device, biologics, food safety, or any response involving FDA-regulated entity screening. Particularly relevant for ASPR, BARDA, and medical countermeasure supply chain responses.

---

## Commercial API Integration Guide Cited as Architecture Validation

**Pattern:** Citing a commercial vendor's integration guide (e.g., sanctions.io's Power Automate + Dynamics 365 guide) as published "validation" for a proposed custom architecture that deliberately avoids commercial dependencies.

**Reality:** The cited guide demonstrates connecting to a **commercial, paid API** — the exact kind of SaaS dependency the response's build-vs-buy argument rejects. This citation undermines rather than supports the argument. It proves that commercial screening APIs integrate with Power Platform, which supports the COTS procurement path the response argues against.

**Verification:** Read the cited guide/article in full. Ask:
1. Does it demonstrate the specific architecture pattern the response proposes? (Usually no — it's a single-vendor API connection, not multi-source government data stitching)
2. Does it connect to free government data sources? (Usually no — these are vendor marketing pieces for their paid products)
3. Would a CO who reads the cited source conclude it validates the response's architecture? (Usually no — they'd conclude commercial APIs work fine with Power Platform)

**Severity:** **P1.** The CO or technical evaluator who actually reads the cited source will see it doesn't support the claimed architecture. At best, it looks sloppy. At worst, it looks like deliberate misdirection — citing a source the evaluator won't check, hoping the citation alone carries weight.

**Applies to:** Any response that cites third-party integration guides, whitepapers, or blog posts as evidence for a custom-build approach, especially when those sources demonstrate commercial SaaS integration patterns.

---

## Power Automate HTTP Connector as Real-Time Multi-Source Screening Engine

**Pattern:** Proposing Power Automate cloud flows with HTTP connectors as a real-time, multi-source screening engine against 6+ government data sources, without acknowledging platform operational limits or the batch-ETL nature of most government data sources.

**Reality:** Power Automate has significant operational constraints:
- Standard license: HTTP connector throttled at ~300 requests per 60 seconds (connector throttling)
- 24-hour API request limits per tenant across all flows
- Flows idle >90 days may be automatically disabled
- Premium Power Automate Process licenses add 250,000 PPR per license (stackable), but this represents additional per-user cost
- Most "government APIs" in these proposals are actually downloadable files requiring scheduled ETL with file parsing — fundamentally different from and more complex than HTTP connector calls

**Verification:** Check Microsoft Learn documentation:
- https://learn.microsoft.com/en-us/power-automate/limits-and-config (flow limits)
- https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/understand-limits (throttling)
- https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations (request limits)

**Severity:** **P1.** The response presents a real-time screening architecture when the operational reality is scheduled batch processing with file downloads, parsing, and platform throttling. The complexity gap between what's described and what's buildable is significant enough to affect the ROM cost estimate (likely 2-3x understated) and timeline.

**Applies to:** Any response proposing Power Automate as the integration backbone for multi-source government data screening or due diligence workflows.

---

## Sources Sought Response as Mini-Proposal

**Pattern:** A Sources Sought response spends 50%+ of its content describing a technical solution, architecture, and implementation approach — effectively submitting a proposal for a requirement that hasn't been solicited.

**Reality:** A Sources Sought is market research. The agency wants to know: who are you, what can you do, are you a viable competitor. They do NOT want a technical proposal. The standard SSN asks for: company profile, capability statement, contract vehicles, optional pricing, optional NAICS/PSC.

**Verification:** Compare the SSN's stated requirements against the response's content allocation. If Sections 1-3 are unsolicited technical narrative, flag the disproportionate emphasis.

**Severity:** P1. A CO may interpret this as the respondent not understanding the acquisition vehicle, or trying to steer the acquisition strategy. Either impression is negative.

---

## Wrong-Notice Gap Analysis Cross-Reference

**Pattern:** Loading a team credential gap analysis that was built for a different notice ID and applying its PWS-specific findings to the current response.

**Reality:** Team credential facts (certifications, employment history, clearances) are transferable across notices. But PWS line-item gaps ("C.5.1.3 requires PMP"), deliverable assignments, and section-specific recommendations are tied to a specific PWS. A gap analysis built for HHS OCIO VMO (7571TE26Q00092) cannot be applied to HHS ASPR Sources Sought (ACQ-OMAS-2026-SAT-0015).

**Verification:** Check the notice ID on any gap analysis loaded. If it doesn't match the current notice, use credential facts only — discard PWS-specific findings.

**Severity:** P2 for the review process (wrong PWS findings waste time). P0 if the review then makes incorrect PWS alignment claims.

---

## Stale/Expired Bid Protests Represented as Current

**Pattern:** A pre-sales strategy deck or capability statement characterizes a contract dispute or bid protest as "recent" or "current" when it was resolved years ago. The deck may use a status label like "HALTED — bid protests filed" to justify monitoring a contract as a potential entry point.

**Why it happens:** The author researched the contract at one point, noted "bid protests filed," and never refreshed the research. The protest status was accurate at the time of initial research but became stale after GAO ruled on it.

**Verification:**
1. Search for the specific program name + "bid protest" + "GAO" with a date range
2. Check GAO's public bid protest database (gao.gov/legal/bid-protests) for the decision
3. Check the prime contractor's press releases or procurement website for contract status updates
4. If the protest was resolved >1 year ago, the characterization as "recent" or "current" is misleading

**Severity:** **P0** if the deck uses the stale protest as a justification for outreach strategy or positions the contract as "at risk." Bechtel's WIPP contract is the canonical example: protests were filed in November 2022 and **denied by GAO the same month**. Bechtel received a 3-year extension in 2025. The contract is fully operational with no active protests. A deck calling this "HALTED" and "Recent" in 2026 is factually wrong by 3.5 years.

**Resolved protest patterns:** When a protest was filed and denied:
- Contract continues operating under the incumbent or awardee
- The protest filing date is the only date that matters — not the "recent" label
- If the deck's outreach angle is "we can help mitigate protest risk," and the protest was resolved years ago, the pitch has no foundation

**Applies to:** Any pre-sales deck targeting DOE, DoD, or civilian agency contracts that references bid protests or contract disputes as justification for outreach.

---

## ITAR/Export Control Penalty Citation Errors

**Pattern:** Claiming an ITAR civil penalty with a wrong dollar figure and/or wrong regulatory citation. Common in compliance-focused pitch decks and capability statements where ITAR exposure is used as a selling point for export control services.

**Why it's common:** Writers find a vaguely remembered penalty amount and regulation number without verifying against the current Federal Register inflation adjustment or the correct CFR subpart.

**Verification:**
1. Check the correct regulation: 22 CFR §127.10(a)(1)(i) — NOT 22 CFR 126.13. Part 126 is "General Policies and Provisions" (visitor controls, proscribed countries). Part 127 is "Violations and Penalties."
2. Check the current maximum penalty from the annual inflation adjustment published in the Federal Register. For 2025: $1,271,078 (the greater of this amount or twice the transaction value). Do NOT use memory — look up the current year's figure.
3. The claim should reference 22 CFR §127.10(a)(1)(i) specifically — not a nearby subpart or a Part 126 reference

**Severity:** **P0.** If the pitch deck's compliance imperative is built on ITAR risk, having BOTH the wrong dollar amount AND the wrong regulation citation undermines the entire compliance credibility proposition. The counterparty's compliance officer will catch this.

**Example from the Westerman engagement (Jul 2026):** "$1,448,000 (2025 adjusted, 22 CFR 126.13)" — wrong on both counts. Correct: $1,271,078 under 22 CFR §127.10(a)(1)(i). Two errors on the same factual claim in a compliance-focused pitch destroyed the credibility of the compliance risk section.

**Applies to:** Any compliance pitch deck, SOW, or capability statement that references ITAR, EAR, or OFAC penalty amounts. Particularly relevant for defense, nuclear, aerospace, and export-controlled manufacturing contractors.

---

## Fabricated AI/Technology Statistic — Attributed to Prestigious Source

**Pattern:** Claiming a specific percentage with a precise range attributed to prestigious institutions (MIT, McKinsey, Harvard Business Review, Gartner) where the attributed source has no record of making that claim.

**Why it's common:** The writer needs a startling statistic to make the case for intervention but can't find a real one that fits. They create one and attribute it to a source unlikely to be challenged.

**Verification:**
1. Search for the specific phrase (e.g., "88-95% AI pilots never reach production") with the attributed source
2. Search for the attributed source's actual publications on the topic during the stated timeframe
3. Check for related-but-different statistics from the same genre (e.g., Gartner reports "70-87% AI project failure rates" from various years — close but not the same)
4. If the claim has a precise range (88-95%) AND prestigious attribution (MIT + McKinsey) AND a specific timeframe (2025-2026) AND cannot be found in any search result across multiple search engines — it's fabricated

**Severity:** **P0.** A fabricated statistic with specific attribution destroys credibility with any sophisticated reader who decides to verify. The precision of the range combined with the prestige of the source is itself suspicious — real studies rarely produce such neat ranges.

**Example from the Westerman engagement (Jul 2026):** "88-95% AI pilots never reach production (MIT/McKinsey 2025-2026)" — no evidence found for this specific statistic from either source. Related stats exist (Gartner, various consulting surveys at 70-87%) but the claimed range and combined attribution are fabricated.

**Applies to:** Any pitch deck, proposal, or capability statement that cites technology adoption failure rates, particularly AI-related statistics. Common in digital transformation and AI consulting pitches.

---

## Customer Relationship Mislabeled as Acquirer Relationship

**Pattern:** Labeling a major customer as the "acquirer" of a company when the relationship is actually supplier-customer. Common in pitch decks where the author is trying to signal strategic momentum.

**Why it's common:** The author knows "Company A" and "Company B" are closely related and assumes "Company A must have acquired Company B" without checking. The actual acquirer is a less-well-known holding company or private equity firm.

**Verification:**
1. Search for "[Company A] acquires [Company B]" or "[Company A] acquisition of [Company B]"
2. Check the target company's "About" page or press releases for ownership history
3. Check Crunchbase, PitchBook, or SEC filings for acquisition records
4. If no acquisition record exists but the companies have a known supplier relationship, the claim is false

**Severity:** **P0.** The counterparty's management will immediately know the correct acquirer. This is the fastest way to demonstrate you haven't done your homework on the target company itself.

**Example from the Westerman engagement (Jul 2026):** The pitch deck labeled Centrus HALEU as "your acquirer" — suggesting Centrus Energy acquired Westerman Inc. In reality, Worthington Industries acquired Westerman in 2012. Centrus is a supply chain customer that purchases UF₆ cylinders from Westerman. The false claim was caught by the adversarial review on the first substantive slide, undermining the deck's credibility from the outset.

**Applies to:** Any pitch deck, capability statement, or proposal that references a counterparty's ownership history, acquisition trajectory, or strategic partnerships.
