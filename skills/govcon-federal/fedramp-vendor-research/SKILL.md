---
name: fedramp-vendor-research
description: Research a vendor/cloud service provider's FedRAMP authorization/certification status with concrete evidence from the FedRAMP Marketplace, press releases, and official documentation. Also covers product-level FIPS 140-2/140-3 compatibility research (NIST CMVP, architecture analysis, CMMC assessment) and integration compatibility under FIPS enforcement. Covers authorization paths (Agency, JAB, Direct), terminology changes (RFC-0020), equivalency, and cross-referencing vendor claims against Marketplace records.
category: research
---

# FedRAMP Vendor Research

## Trigger Conditions
- User asks about a specific vendor/product's FedRAMP status
- Need to verify a vendor's FedRAMP authorization claim
- Need to understand what authorization path a vendor used (Agency Auth, JAB, Direct, Equivalency)
- Need to find all FedRAMP authorized products from a parent company (e.g., Trimble, Microsoft, Oracle)
- Cross-referencing a vendor's marketing claims against actual FedRAMP Marketplace data
- **Need to understand ATO requirements for cloud services handling CUI under DFARS 7012 / NIST SP 800-171**
- **Need to understand when a contractor needs their own ATO vs. relying on CSP FedRAMP authorization**
- **Need to understand FedRAMP equivalency legal validity post-M-24-15 rescission**
- **Need to research the legal interplay between FedRAMP authorization, agency ATOs, DFARS 7012 cloud requirements, and NIST SP 800-171 compliance for contractor-operated systems**
- **Need to determine if a specific cloud service satisfies DFARS 7012(b)(2)(ii)(D) cloud requirements for handling CDI/CUI**
- **Need to research a product's FIPS 140-2/140-3 compatibility — can it run in a FIPS-enabled environment? What cryptographic modules does it use? What breaks if FIPS is enforced? See `references/fips-product-compliance-research.md` for the full methodology including NIST CMVP search, architecture analysis (`.NET`, `Java`, `REST`), and CMMC assessment framework.**
- **Need to investigate integration compatibility between two products when FIPS mode is enforced — e.g., a legacy desktop connector (`.NET Framework`) that uses non-FIPS algorithms vs. a modern REST API over TLS.**

## Research Sequence

### 1. Initial Search Strategy
Use ddgr or browser to find initial leads:
- `"<vendor> FedRAMP"` — general status
- `"<vendor> FedRAMP marketplace"` — Marketplace presence
- `"<vendor> FedRAMP authorized"` or `"FedRAMP certified"` (new terminology)
- `"<vendor> FedRAMP Ready"` — pre-certification status
- `"<vendor> FedRAMP Moderate Equivalency"` — Agency Auth path

### 1a. FIPS 140 Product Research (Distinct Sub-Methodology)
When the user asks about product-level FIPS 140-2/140-3 compatibility (as opposed to vendor-level FedRAMP status), consult **`references/fips-product-compliance-research.md`** first. The research sequence is: (1) check vendor security/compliance pages for FIPS mentions → (2) search NIST CMVP validated modules database for the product name → (3) check FedRAMP/equivalency pages for FIPS hints — note that FedRAMP Moderate requires FIPS but may be satisfied at the infrastructure layer only → (4) search vendor community forums and knowledge bases → (5) analyze product architecture for FIPS failure patterns (.NET Framework `FipsAlgorithmPolicy` registry key, Java JCE providers, REST API TLS cipher suites) → (6) check vendor integration pages for connector methods → (7) document what's absent (missing docs, missing NIST entries, missing vendor guidance). The reference file includes a worked field example: Oracle P6 EPPM + InEight N8 (NAESTIMATE) with CMMC assessment framework.

### 2. FedRAMP Marketplace — The Source of Truth
**Navigate to**: `https://marketplace.fedramp.gov/products/`

Search for the vendor/product in the search box. Key things to verify:

| Field | What to check |
|-------|---------------|
| **Status** | "FedRAMP Certified" (was "Authorized"), "FedRAMP Ready", or "Agency Auth In Process" |
| **Cert Class** | Class C (Moderate), Class B (Low), Class D (High) — was "Impact Level" |
| **Package ID** | Unique identifier (format: FRXXXXXXXXXX or AGENCYXXXX or FXXXXXXXXXX) |
| **Authorization count** | Number of agency authorizations using this package |
| **Reuse count** | How many times agencies have reused it |
| **Certification Type** | Rev5 or 20x |
| **Path** | Agency, JAB, or Direct |
| **CSP (Provider)** | The legal entity that owns the authorization |

#### Marketplace Data Extraction via curl (Preferred for Bulk Research)

The Marketplace embeds ALL product data in the SSR HTML as inline JavaScript variable assignments. This means curl + regex is often FASTER and MORE RELIABLE than browser tools for bulk extraction.

**Pattern to extract:** The HTML contains blocks like:
```javascript
df.id="FR2226322745"; df.csp="Autodesk"; df.cso="Autodesk for Government (AFG)";
df.status="FedRAMP Certified"; df.phase="Ongoing Certification";
df.authorization=19; df.reuse=23;
df.service_desc="ArcGIS Online, hosted by Esri, is a secure and scalable SaaS...";
df.business_categories=["Analytics","Collaboration","Data Management",...];
df.filter_classes=" filter-status-FedRAMP-Authorized filter-impact-level-Moderate...";
```

**Extraction command template:**
```bash
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://www.fedramp.gov/marketplace/products/?search=<vendor>" \
  | python3 -c "
import sys, re
text = sys.stdin.read()
# Extract vendor/product references (case-insensitive)
for m in re.finditer(r'<vendor>', text, re.IGNORECASE):
    start = max(0, m.start()-200)
    end = min(len(text), m.end()+500)
    print(text[start:end])
    print('---')
"
```

**Key fields you can extract from the embedded data:**
- Package ID (FRXXXXXXXXXX format)
- CSP name and CSO (product) name
- Status: "FedRAMP Certified", "Agency Authorization In Process", "FedRAMP Ready"
- Impact level: "Moderate", "High", "Low", "LI-SaaS"
- Authorization count, reuse count
- Service description text
- Business categories array
- Agency names for authorizations and reuses
- Security email, sales email, website URL
- UEI number
- Service model: SaaS, PaaS, IaaS

**Why this beats the browser:** The browser can get stuck on `about:blank` after interactions, and the card view doesn't expose names in the AX tree. curl + regex on the raw HTML is stateless, fast, and gives you ALL data fields at once.

### 3. Check the Terminology Banner
The Marketplace page always shows a blue banner with the current FedRAMP terminology rules. This is critical context:
- **RFC-0020 (Feb 2026)**: "FedRAMP Authorization" → "FedRAMP Certification". Impact Levels → Classes A-D.
- The banner tells you the current effective date and any transition rules.

### 4. Check Agency Authorization (Equivalency) Products
If the vendor claims "Equivalency Authorization" or "Agency Authorization":
- Search by product name on the Marketplace
- Filter by "Agency Auth In Process" (but note: this filter may show 0 results if the vendor isn't listed)
- **Key fact**: Under the new RFC-0020 rules, "Agency Auth" is NOT a visible filter category on the current Marketplace for certified products. Products authorized via the agency path before the rule change (like InEight Document) may NOT appear on the new Marketplace at all.

### 5. Check Parent Company Products
To find ALL FedRAMP products from a parent company (e.g., all Trimble brands):
1. Search each known brand/subsidiary individually
2. Try: `site:marketplace.fedramp.gov <companyname>`
3. Look for "A [Parent] Company" in CSP names (e.g., "e-Builder, A Trimble Company")

### 6. Verify Against Press Releases
Cross-reference Marketplace data with official press releases:
- GLOBE NEWSWIRE / BusinessWire press releases are authoritative
- Check the vendor's own `/fedramp/` or `/security/` page
- Look for the specific authorization language: "FedRAMP Moderate" vs "FedRAMP Moderate Equivalency" vs "FedRAMP Certified" — these are DIFFERENT statuses

### 7. Concrete Evidence to Capture
For every finding, capture:
- **Marketplace URL** with the search/product result
- **Package ID** (e.g., F1603307884)
- **Exact status text** from the page
- **Excerpts** from press releases with dates
- **Negative evidence** when a product is NOT on the Marketplace (this is often the most important finding)

## Reading a 3PAO Security Assessment Report (SAR)

When a vendor shares their 3PAO SAR (typically from a FedRAMP-recognized assessor like A-LIGN, Coalfire, or Schellman), here's what to look for and what to be careful about:

### Key Pages to Extract

| Page/Section | What It Tells You | Key Questions |
|---|---|---|
| **Cover page** | CSP name, CSO name, version, date, preparer (3PAO), status (Draft/Final) | Is this a final report or work-in-progress? |
| **Table 2-1 (Executive Summary)** | FedRAMP Unique ID (FR-XXXXXXXXXX), Impact Level, Service Model, Deployment Model | Does the deployment model match what the vendor told you? (Government-Only vs. Community vs. Public) |
| **Table 2-2 (Risk Summary)** | Open risks at each severity level (High, Moderate, Low) across all testing types (OS scans, web scans, DB scans, container scans, pen test, CM-6) | Are there zeros across the board? Any vendor dependencies (VDs)? |
| **Page 5 / Strengths & Weaknesses** | Specific controls tested, weaknesses found, and their remediation status | Were weaknesses remediated "following post-interview testing"? |
| **Page 9 / Recommendation** | The 3PAO's formal recommendation and whether it references a specific framework (DoD equivalency memo vs. standard FedRAMP authorization) | Does the 3PAO explicitly reference the right framework? |
| **Appendix A** | Risk Exposure Table (RET) — detailed breakdown of any risks | Only needed if Table 2-2 shows non-zero values |
| **Appendix C** | Vulnerability scan summaries (infrastructure, web, database, container) | Was 100% of inventory scanned? Any discrepancies? |
| **Appendix F** | Penetration test report (or reference to a separate file) | What date was the pen test conducted? |

### The Critical Finding: Table 2-2 (Risk Summary)

This is the single most important page for a contractor evaluating a CSP. It shows the complete risk posture at the conclusion of the assessment.

**When it shows ALL ZEROS** (the cleanest possible result):
- Zero open risks at every severity level
- Zero findings across all testing categories
- Zero operational requirements (ORs)
- Zero vendor dependencies (VDs)
- This means the initial assessment closed with no Plan of Actions and Milestones (POA&Ms)
- **This meets the strictest condition of the DoD's Dec 2023 equivalency memo**

**When it shows non-zero values:**
- Any non-zero value means there are open risks that must be tracked in a POA&M
- Vendor dependencies (VDs) mean the CSP is waiting on a downstream vendor to patch
- Operational Requirements (ORs) mean the finding was accepted as-is with agency approval
- Each non-zero cell needs to be evaluated for severity and remediation plan

### ⚠️ Critical Distinction: Initial Assessment POA&Ms vs. Continuous Monitoring POA&Ms

**This is one of the most common misunderstandings in SAR interpretation.**

- **Table 2-2 shows risks that remained open at the conclusion of the INITIAL ASSESSMENT.** This is a point-in-time snapshot. If it shows zeros, it means the initial assessment closed clean — no findings were carried forward.

- **Continuous monitoring POA&Ms** are separate, ongoing, and LIVING documents. FedRAMP requires CSPs to perform ongoing scanning and vulnerability management after the initial assessment. Findings from periodic scans since the assessment date would be tracked in a continuous monitoring POA&M.

**What this means for your analysis:**
- "Zero findings at initial assessment conclusion" = the system was built correctly and passed all controls. This is very strong evidence.
- "Current continuous monitoring state" = unknown without current scan data. The SAR alone does NOT guarantee zero findings today.
- When a contractor asks "does this CSP have open POA&Ms?", you need to clarify: "Do you mean at the time of initial assessment (we can answer from the SAR) or currently (we need the CSP's continuous monitoring data)?"

### Embedded Artifacts (Not Included in Most SAR PDFs)

SAR documents often reference supporting files that are NOT included in the PDF itself:

| Artifact | What It Contains | How Critical |
|---|---|---|
| **SRTM Workbook** | Control-by-control testing results, evidence, and assessor notes | Needed for CMMC SSP if the C3PAO asks for evidence |
| **Scan result zip files** | Raw vulnerability scan output (Nessus, etc.) | Supporting evidence; findings already summarized in Table 2-2 |
| **Penetration test report** | Detailed exploitation results, methodology, findings | Important for due diligence but findings already in Table 2-2 |
| **False positive reports** | Validated false positives from scans | Low — already accounted for in the SAR findings |
| **Raw scan data** | Machine-readable CSV/Nessus output | Typically only needed for C3PAO or agency audit |

**Bottom line for contractors:** The SAR summary (Table 2-2 + strengths/weaknesses + recommendation) is usually sufficient for CSP due diligence. The embedded zip files are supporting evidence that backs up those findings. You only need to request them if:
1. A C3PAO asks during a CMMC assessment
2. A contracting officer requests the full evidence package
3. You want to verify something specific that the summary doesn't cover

### Practical SAR Analysis Example: What to Tell a Client

When a client/coworker sends you a SAR and asks for analysis, structure the response as three buckets:

**What we can ANSWER right now from the SAR:**
- Whether the initial assessment found open POA&Ms (Table 2-2)
- Whether the 3PAO assessed 100% of controls
- Which testing was performed (pen test, vuln scans, container scans, STIG compliance)
- Which deployment model (Government-Only, Community, Public) — from Table 2-1
- The specific framework the assessment was conducted under (DoD equivalency memo vs. JAB path)
- Weaknesses found during testing and whether they were remediated
- Documentation artifacts reviewed (training, incident response, DR/BCP, vendor risk analysis)

**What the SAR alone CANNOT tell you:**
- Current continuous monitoring state (findings since the assessment date)
- The sponsoring agency (the SAR documents the assessment, not the authorization)
- CR26 transition plans (if SAR predates CR26)
- Contract-specific requirements (whether a specific solicitation requires Marketplace listing)

**What supporting files the SAR references but doesn't include:**
- Raw scan result zip files (Nessus output, etc.)
- SRTM workbook
- Penetration test report
- These are supporting evidence — findings already in Table 2-2

## FedRAMP Authorization Paths (pre-RFC-0020)

| Path | Old Name | New Name (post RFC-0020) | On Marketplace? |
|------|----------|--------------------------|-----------------|
| JAB | FedRAMP Joint Authorization Board | FedRAMP Certified (JAB path) | Yes, visible |
| Agency | FedRAMP Agency Authorization | FedRAMP Certified (Agency path) | Yes, visible |
| **Agency Equivalency** | FedRAMP Moderate Equivalency Authorization | No direct mapping — was an Agency Auth deemed "equivalent" | **May NOT appear** on new Marketplace |
| Direct | FedRAMP Direct Authorization | FedRAMP Certified (Direct path) | Yes |
| Ready | FedRAMP Ready | FedRAMP Ready (being retired per RFC-0023) | Yes, but retiring |

## Terminology Timeline

- **Pre-Jan 2026**: "FedRAMP Authorization" at "Moderate Impact Level"
- **Jan 13 – Feb 19, 2026**: RFC-0020 comment period
- **Feb 19, 2026**: RFC-0020 closed; outcome published
- **After Feb 2026**: "FedRAMP Certification" at "Class C (Moderate)"
- **Until Dec 31, 2026**: Legacy impact levels shown in parentheses
- **Jan 2027**: Fully transitioned to class structure only

## Regulatory Compliance: DFARS 7012 & ATO Requirements

### Context
DFARS 252.204-7012 governs contractor handling of Covered Defense Information (CDI) / Controlled Unclassified Information (CUI) in cloud services. The key requirement for cloud use is at **paragraph (b)(2)(ii)(D)**.

### Key Distinctions

| Concept | What it is | Who issues it | Contractor relevance |
|---------|-----------|---------------|---------------------|
| **FedRAMP Authorization (Certification)** | Assessment that a CSP meets security baselines; creates "Presumption of Adequacy" (M-24-15 §IV.a) | FedRAMP Director (Program Auth) or Agency AO (Agency Auth) | Contractor must acquire cloud services ONLY from CSPs with FedRAMP Moderate or High (Class C or D) |
| **Agency ATO/ATU** | Authorization to Operate for the agency's information system that *uses* the CSP | Agency Authorizing Official | Contractor does NOT issue or receive an ATO. The agency AO reuses the FedRAMP package to issue their own ATO |
| **Contractor NIST SP 800-171 Compliance** | Contractor implements security controls equivalent to NIST SP 800-171 on their own systems (including CUI environment) | Contractor self-assessment (or third-party assessment per CMMC) | Required by DFARS 7012(b)(2)(i); separate from cloud authorization requirement |

### When does a contractor need an ATO?
**Never.** A contractor's obligation under DFARS 7012 is:
1. **Cloud requirement**: Acquire cloud services handling CDI/CUI only from a CSP with FedRAMP Moderate or High authorization (FedRAMP Certified Class C or D). See DFARS 7012(b)(2)(ii)(D).
2. **System requirement**: Implement NIST SP 800-171 security controls on their own systems (self-assessment). See DFARS 7012(b)(2)(i).
3. **ATO**: Issued by federal agency AOs for federal information systems. Contractor-operated systems handling CUI under a DoD contract do not receive a federal ATO unless the system is designated as a federal information system by the contracting agency.

### ⚠️ CRITICAL: DFARS 7012(b)(2)(ii)(D) — Exact Text

**DO NOT MISQUOTE THIS.** This is the single most common error in FedRAMP/DFARS compliance analysis and it changes the entire legal meaning.

The **correct** text (verified via Cornell LII / eCFR):

> *(D) If the Contractor intends to use an external cloud service provider to store, process, or transmit any covered defense information in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets **security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline**.*

⚠️ The DFARS does **NOT** say "FedRAMP authorization at the Moderate or High baseline." That is a fabricated paraphrase. The actual text requires **"security requirements equivalent to"** FedRAMP Moderate — which is a fundamentally different standard that **supports** the concept of equivalency. If you see the incorrect phrasing in a briefing you're reviewing, flag it as a critical error.

Verify with:
```
curl -sL -A "Mozilla/5.0" "https://www.law.cornell.edu/cfr/text/48/252.204-7012" | grep -i -A2 -B2 "equivalent to"
```

**Why this matters for analysis:** Since the DFARS requires security controls *equivalent to* FedRAMP Moderate (not FedRAMP *authorization* itself), a CSP with properly-documented FedRAMP Moderate Equivalency (3PAO-assessed, zero POA&Ms) is arguably closer to the actual regulatory requirement than one that merely has "FedRAMP authorized" with open POA&Ms. The misquote makes the regulation appear hostile to equivalency when the actual text supports it.

### OMB M-24-15 (July 25, 2024) — Key Provisions
- **Rescinded** the 2011 FedRAMP founding memo in its entirety (§X).
- **Created "Presumption of Adequacy"** (§IV.a): Agencies must presume a FedRAMP-authorized CSO's security assessment is adequate for issuing their own ATO at or below that FIPS 199 impact level.
- **Two authorization paths** (§IV.c): Agency Authorization (signed by agency AO) and Program Authorization (signed by FedRAMP Director).
- **Temporary authorizations** (§IV.e): Up to 12 months for piloting new services without full authorization; extendable if full authorization is in progress.
- **Marketplace is authoritative** (§IV.e): The FedRAMP Marketplace is the source of truth for which CSOs are authorized.
- **Agency ATOs still required**: M-24-15 footnote 5: *"the appropriate agency authorizing officials must issue an authorization when reusing artifacts (such as system security plans and assessments) in the FedRAMP repository."*

### FedRAMP Equivalency — Post-M-24-15 Status
- The 2011 memo that authorized the equivalency framework was formally rescinded.
- M-24-15 did NOT include a blanket grandfather clause, sunset date, or transition period for equivalency authorizations.
- CSPs with pre-2024 equivalency authorizations that were NOT re-designated by the FedRAMP PMO face legal uncertainty for DFARS 7012 compliance.
- The safest path: verify the CSP appears on the FedRAMP Marketplace with a current authorization designation.
- The FedRAMP 2026 Consolidated Rules site (fedramp.gov/2026) explicitly warns: *"Historical FedRAMP information is now often wrong! Nearly all of that historical information no longer applies after FedRAMP was rescinded and replaced in 2024."*

### Sources for Regulatory Research
- **DFARS 7012**: eCFR API (use versioner to bypass browser blocks) — eCFR.gov blocks browser navigation for DFARS sections; the API versioner works.
- **OMB M-24-15**: Full text at fedramp.gov/2026 (Consolidated Rules, "OMB Memorandum M-24-15" page). The original PDF at whitehouse.gov may 404.
- **NIST SP 800-171 Rev. 3**: nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf — download as PDF for offline text extraction.
- **FedRAMP 2026 Consolidated Rules**: fedramp.gov/2026 — SPA site; use browser tools, not curl. To extract article content, use `browser_console` with JS: `document.querySelector('article').innerText`.

## Pitfalls

- **SvelteKit SPA renders empty pages for browser — curl + regex can actually work BETTER**: The Marketplace runs on client-side JavaScript. The browser approach can get stuck on `about:blank` states after interactions. However, the SSR HTML contains all product data serialized in inline `<script>` variable assignments using patterns like `df.id="FR2226322745"; df.csp="Autodesk"; df.cso="Autodesk for Government (AFG)"; df.status="FedRAMP Certified"`. You can extract this with curl + Python regex on the HTML body — this is often MORE reliable than browser tools for bulk data extraction. See \"Marketplace Data Extraction via curl\" below.
- **"Equivalency" products may be invisible**: Vendors with "Equivalency Authorization" through a sponsoring agency (not JAB) may not appear on the Marketplace under the new RF-C0020 terminology. The press release may say "check the Marketplace" but the product won't be there. Capture this as evidence.
- **Partial-name matches pollute search results**: Searching a product name like "InEight" returns false positives containing substrings ("Insight", "Contract Insight", "Eightfold"). The actual product may not be in the results at all. Verify each result card individually — don't assume a non-zero result count means the product was found. Use `browser_vision` to visually inspect the card area, or extract all H3 text elements to confirm your target product is actually present in the results.
- **"Equivalency" is not a Marketplace listing category and never was**: The Marketplace has always listed FedRAMP Authorized/Certified services only. If a user asks "why does my equivalency CSP not appear on the Marketplace?", the answer is: equivalency services were never listed there. The CR26 rules (Feb 2026) simply reinforced this by formalizing "FedRAMP Certification" as the sole label.
- **Equivalency requires contractor validation of full BoE**: If you identify a CSP claiming equivalency, you MUST also check whether the contractor has obtained and validated the 3PAO's Body of Evidence. Without that, the equivalency claim has not been satisfied under the DoD CIO memo.
- **A suite-level authorization does NOT authorize individual modules**: If a Full Suite is FedRAMP authorized but a specific module only has "equivalency," the module's CUI processing is governed by the equivalency rules, not the suite's ATO. Verify what specific product name appears on the authorization document.
- **Marketplace filter count ≠ actual results**: On the new Marketplace, the filter count shows numbers for each status, but the actual results list may be paginated or differently filtered. Always check the text below the search bar for the actual result count.
- **ddgr rate limits aggressively**: After a few queries, ddgr returns empty results ([ERROR] HTTP Error 202). Use browser navigation directly when ddgr starts failing.
- **DuckDuckGo "I'm Feeling Duck" URLs**: If ddgr is failing, try using the browser to search directly.
- **Vendor claims "FedRAMP Authorized" but it's "Ready"**: "FedRAMP Ready" is NOT authorization — it means the vendor completed a readiness assessment but has NO authorization. The product cannot be used by federal agencies under FedRAMP. Press releases often blur this line.
- **Multiple products, one authorization**: A suite authorization covers the suite, not each module. A vendor may claim their "Suite" is authorized but only one module actually went through the process. Verify the authorized product name exactly.
- **Vendor sites block automated access**: Some vendors (notably Autodesk) prevent all programmatic access to their sites. When a vendor's site returns "Access Denied" to browser and 402s to curl, pivot to the FedRAMP Marketplace (government site — not blocked) and/or use meeting transcripts. See `references/autodesk-research-block.md` for the full Autodesk pattern.

## Verification Checklist
- [ ] Product found on Marketplace? → Yes/No (document which)
- [ ] Status listed as: ___________
- [ ] Class/Impact Level: ___________
- [ ] Package ID: ___________
- [ ] Path (Agency/JAB/Direct): ___________
- [ ] Press release date matches Marketplace entry? → Yes/No
- [ ] Company has other authorized products? → List
- [ ] Negative evidence captured (product NOT found)? → Yes
- [ ] **For CUI/CDI use: CSP has FedRAMP Moderate or High (Class C or D)? → Yes/No (DFARS 7012(b)(2)(ii)(D) requirement)**
- [ ] **CSP authorization obtained under pre-2024 equivalency? → If so, verify re-designation status**
- [ ] **Contractor system boundary identified? → Contractor does NOT need ATO; verify NIST SP 800-171 compliance path**
- [ ] **SAR Table 2-2 reviewed? → All zeros / non-zero findings documented**
- [ ] **SAR recommendation framework identified? → DoD equivalency memo / JAB / Agency path**
- [ ] **Initial assessment POA&Ms vs. continuous monitoring clarified? → Distinction made clear in analysis**
- [ ] **Underlying CSP authorization checked? → If CSP runs on Azure/GovCloud, check that layer's FedRAMP status separately**
- [ ] **Embedded artifacts catalogued? → Zip files, SRTM, pen test report identified as not included**

## Reference Files

- `references/fedramp-construction-landscape-2026-07-21.md` — **Comprehensive construction + adjacent FedRAMP Moderate SaaS landscape catalog.** Covers all parent companies (Autodesk AFG confirmed FedRAMP, Oracle Primavera In Process, Trimble GovRAMP+CMMC, Bentley/Hexagon/Topcon status), adjacent categories (Esri ArcGIS Online FedRAMP, DocuSign Federal IL4, Box High, Power BI), and equivalency candidates with 3PAO/SOC 2 evidence (InEight A-LIGN, Trimble SafeBase). Use as quick-reference when evaluating CSP options for federal construction contracts.
- `references/ineight-sar-analysis-2026-07-10.md` — Detailed analysis of the A-LIGN SAR for InEight Document. Example case study for reading a 3PAO SAR, interpreting Table 2-2 (all zeros), identifying weaknesses and remediation, distinguishing initial assessment from continuous monitoring POA&Ms, and mapping embedded artifacts to contractor needs.
- `references/ineight-trimble-fedramp.md` — InEight/Trimble FedRAMP research
- `references/ineight-document-fedramp-2026-07-10.md` — InEight Document specific findings: CR26 quotes, DFARS misquote correction, Marketplace absence evidence, press release disconnect
- `references/dfars-ato-regulatory-research.md` — Regulatory compliance research: DFARS 7012, OMB M-24-15, NIST SP 800-171, contractor ATO requirements, FedRAMP equivalency post-rescission questions
- `references/fedramp-construction-platforms.md` — Quick-reference table of FedRAMP-authorized construction platforms (Autodesk, ProjectTeam, Kahua, e-Builder) with notable non-authorized (Procore, OST). Use when evaluating OST alternatives.
- `references/ost-constructconnect-vendor-assessment-2026-07-16.md` — Worked example: full CMMC/FedRAMP vendor compliance assessment for a non-FedRAMP desktop application (ConstructConnect OST). Demonstrates the cross-reference methodology (assessment claims → vendor public pages → gap analysis → meeting prep), Firecrawl fallback pattern, and internal Thariq ivory/clay compliance briefing format.
