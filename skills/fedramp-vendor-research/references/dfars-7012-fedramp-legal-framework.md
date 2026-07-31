# DFARS 7012 & FedRAMP Equivalency — Legal Framework

## Source: July 2026 Deep-Dive Research

Full research session produced `/home/amyn/dfars-7012-fedramp-equivalency-research.md` with complete citations and comparison tables.

---

## 1. The Regulatory Text

### DFARS 252.204-7012(b)(2)(ii)(D) — The Cloud Service Provider Requirement

> "If the Contractor intends to use an external cloud service provider to store, process, or transmit any covered defense information in performance of this contract, the Contractor **shall require and ensure** that the cloud service provider meets security requirements **equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline** and that the cloud service provider complies with requirements in paragraphs (c) through (g) of this clause for cyber incident reporting, malicious software, media preservation and protection, access to additional information and equipment necessary for forensic analysis, and cyber incident damage assessment."

**Source**: 48 CFR § 252.204-7012 (via Cornell LII eCFR mirror — the authoritative public copy, since eCFR.gov and acquisition.gov both block automated access)

---

## 2. The DoD CIO Memo (Dec 21, 2023)

**Title**: *Federal Risk and Authorization Management Program Moderate Equivalency for Cloud Service Provider's Cloud Service Offerings*

**Issued by**: DoD Chief Information Officer

**Effective**: Immediately upon release (Dec 21, 2023)

**Scope**: DFARS 252.204-7012 only (clarifies the meaning of "equivalent" in that clause)

### What it Requires — A CSP is FedRAMP Moderate Equivalent ONLY if:

1. **100% compliance** with ALL FedRAMP Moderate baseline security controls
2. **Assessment by a FedRAMP-recognized 3PAO** — self-attestation explicitly prohibited
3. **Zero control-related Plans of Action and Milestones (POA&Ms)** — all controls must be fully implemented before the assessment concludes. Only operational POA&Ms for routine maintenance are permitted.
4. **Complete Body of Evidence (BoE)** shared with the contractor, including:
   - System Security Plan (SSP) covering all control families
   - Control Implementation Summary (CIS) Workbook / Customer Responsibility Matrix (CRM)
   - Information Security Policies and Procedures
   - Information Security Contingency Plan
   - Incident Response Plan
   - Configuration Management Plan
   - FIPS 199 impact assessment
   - Separation of Duties Matrix
   - Security Assessment Plan (SAP)
   - Penetration testing plan and annual results (by 3PAO)
   - Database and web scanning results (validated annually by 3PAO)
   - Security Assessment Report (SAR) performed by 3PAO
   - Evidence and artifacts
   - POA&M including Continuous Monitoring Strategy and Executive Summary (validated by 3PAO)
5. **Annual reassessment** by a FedRAMP-recognized 3PAO
6. **Continuous monitoring**: monthly vulnerability scans, annual penetration tests, monthly executive summaries
7. **BoE submission to DIBCAC or C3PAO** upon request

### Key Source (secondary — primary PDF blocked by CDN):

- **Crowell & Moring Client Alert** (Jan 9, 2024): "No Longer Cloudy: DoD Issues New Guidance on FedRAMP Moderate Equivalency Cloud Security Requirements"
- **Ankura Consulting** (Jan 11, 2024): "DOD Issues Memo on FedRAMP Requirements for Defense Contractors"
- **Secureframe Blog** (Mar 3, 2026): "FedRAMP Equivalency for CMMC: The DoD Memo Explained [2026]"
- **CMMC Audit Prep** (Jan 4, 2024): "FedRAMP 'Equivalent' Memo released"

---

## 3. The FedRAMP Authorization Act & OMB M-24-15

The **FedRAMP Authorization Act** was passed 2023–2024, fundamentally restructuring FedRAMP. The Act defines a "FedRAMP authorization" as:

> *"a certification that a cloud computing product or service has completed a FedRAMP authorization process."*

**OMB Memorandum M-24-15** rescinded the original FedRAMP policy and established new authorities. Per FedRAMP's own RFC-0020 outcome statement:

> *"A fundamental lifecycle change for FedRAMP occurred when the FedRAMP Authorization Act was passed and OMB Memorandum M-24-15 was released. FedRAMP was not simply established in law or updated by these changes in statute and policy; instead, a very different program was established in its place with the same name."*

### Impact on Marketplace Listing

- The Act and M-24-15 established that only services completing a full FedRAMP authorization process (agency sponsorship + FedRAMP PMO review) qualify as "FedRAMP Certified" and thus appear on the Marketplace
- Equivalency services have never been Marketplace-listed — the CR26 rules (2026) simply reinforced this by formalizing "FedRAMP Certification" as the sole label

---

## 4. FedRAMP Consolidated Rules for 2026 (CR26)

### RFC-0020: FedRAMP Authorization Designations

- **Proposed**: Jan 13, 2026
- **Closed**: Feb 19, 2026
- **Outcome published**: Feb 25, 2026 (NTC-0004)

Key outcomes:
- Single official label: **"FedRAMP Certification"** or **"FedRAMP Certified"**
- Four certification classes: **A** (pilot), **B** (Li-SaaS/Low), **C** (Moderate), **D** (High)
- Transition period through Dec 31, 2026 (old impact levels shown in parentheses)
- Full transition by Jan 2027
- No separate "FedRAMP Validated" label for 20x vs Rev5 (filtered in Marketplace instead)

### RFC-0021: Expanding the FedRAMP Marketplace

- **Outcome published**: Feb 25, 2026 (NTC-0005)
- FedRAMP will NOT store/publish pricing on Marketplace
- Advisory services listing made optional
- Independent assessors must complete ≥2 assessments every 2 years to maintain recognition
- CR26 rules valid through Dec 31, 2028

---

## 5. Contractor Obligations Under DFARS 7012 — Complete Citation

### DFARS 7012 paragraphs (c) through (g) — the full incident response requirements the CSP must comply with:

**(c) Cyber incident reporting requirement:**
- (c)(1) When contractor discovers a cyber incident affecting CDI or ability to provide operationally critical support:
  - (i) Conduct review for evidence of compromise
  - (ii) Rapidly report (within 72 hours) at https://dibnet.dod.mil
- (c)(2) Cyber incident report shall include required elements at dibnet.dod.mil
- (c)(3) Contractor must have or acquire a DoD-approved medium assurance certificate

**(d) Malicious software:**
- Submit isolated malicious software to DoD Cyber Crime Center (DC3) in accordance with their instructions

**(e) Media preservation and protection:**
- Preserve and protect images of all known affected information systems and relevant monitoring/packet capture data for at least 90 days

**(f) Access to additional information or equipment necessary for forensic analysis:**
- Upon DoD request, provide access to additional information or equipment

**(g) Cyber incident damage assessment activities:**
- If DoD elects a damage assessment, provide all relevant information gathered per (e)

### Flow-down (m):
- Contractor must include the clause in all subcontracts for operationally critical support or where subcontract performance involves CDI
- Subcontractors must notify the prime contractor when submitting NIST SP 800-171 variation requests
- Subcontractors must provide the incident report number to the prime contractor

---

## 6. Complete Comparison: FedRAMP Authorized vs. FedRAMP Moderate Equivalency

| Dimension | FedRAMP Moderate Authorization | FedRAMP Moderate Equivalency |
|---|---|---|
| **Listed on FedRAMP Marketplace** | ✅ Yes | ❌ No |
| **Agency sponsorship required** | ✅ Yes | ❌ No |
| **3PAO assessment required** | ✅ Yes | ✅ Yes |
| **Open POA&Ms permitted** | ✅ Yes (with AO risk acceptance) | ❌ No — zero control-related POA&Ms |
| **Body of Evidence** | ✅ Yes (held by FedRAMP/agency, available via PMO) | ✅ Yes (shared directly with contractor) |
| **Contractor must validate BoE** | ❌ No (FedRAMP does it) | ✅ Yes (contractor's obligation) |
| **Satisfies DFARS 252.204-7012** | ✅ Yes (automatically) | ✅ Yes (if memo requirements met) |
| **ATO from an AO** | ✅ Yes (Agency ATO required) | ❌ No ATO — equivalency is a contractor-facing validation |
| **Annual reassessment** | ✅ Yes | ✅ Yes |
| **Continuous monitoring** | ✅ Yes (via agency/FedRAMP PMO) | ✅ Yes (validated by 3PAO, monitored by contractor) |

---

## 7. Access Pattern: Government Sites That Block Automated Access

| Site | Blocking Mechanism | Alternative Access |
|------|-------------------|-------------------|
| dodcio.defense.gov | CDN Edge/GeoTrust — returns Access Denied | Law firm secondary analysis (Crowell, Ankura, Secureframe) |
| eCFR.gov | Cloudflare bot detection + CAPTCHA | Cornell LII (law.cornell.edu/cfr/text/48/252.204-7012) |
| acquisition.gov | Drupal redirect to OOPS page | Full DFARS download (PDF/Word/DITA) from /dfars page |
| fedramp.gov | SvelteKit SPA (curl returns empty shell) | Browser tools required; RFC pages work with browser |
| federalregister.gov | Bot detection + CAPTCHA | FR API (api.federalregister.gov) or Cornell LII |

---

## Primary Source Citations

1. **DFARS 252.204-7012** — 48 CFR § 252.204-7012, Cornell LII: https://www.law.cornell.edu/cfr/text/48/252.204-7012
2. **DoD CIO Memo (Dec 21, 2023)** — Originally at dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf (CDN-blocked); content verified via Crowell, Ankura, Secureframe, CMMC Audit Prep secondary sources
3. **OMB Memorandum M-24-15** — whitehouse.gov/omb/information-resources/guidance/memoranda/
4. **FedRAMP RFC-0020 Outcome** (Feb 25, 2026) — https://www.fedramp.gov/notices/0004/
5. **FedRAMP RFC-0021 Outcome** (Feb 25, 2026) — https://www.fedramp.gov/notices/0005/
6. **FedRAMP Consolidated Rules for 2026** — https://www.fedramp.gov/2026/
7. **Crowell & Moring** (Jan 9, 2024): https://www.crowell.com/en/insights/client-alerts/no-longer-cloudy-dod-issues-new-guidance-on-fedramp-moderate-equivalency-cloud-security-requirements
8. **Ankura Consulting** (Jan 11, 2024): https://ankura.com/insights/dod-issues-memo-on-fedramp-requirements-for-defense-contractors
9. **Secureframe** (Mar 3, 2026): https://secureframe.com/blog/fedramp-equivalency-cmmc
10. **CMMC Audit Prep** (Jan 4, 2024): https://www.cmmcaudit.org/fedramp-equivalent-memo-released/
