# InEight Document — Session Case Study (July 10, 2026)

## Context

A full regulatory analysis was performed for Aecon Federal Services regarding InEight Document's "FedRAMP Moderate Equivalency" status. The analysis involved:
- Olivia Baer (Sr. Cybersecurity Analyst, Aecon) asking about DFARS 7012 compliance
- Habie Ng (Aecon) providing the A-LIGN SAR (319 KB, 19+ pages)
- Rodney Childress (Nuclear Federal Estimating) asking about risk inheritance
- Brian Gregorio (Sr. Dir Federal Compliance) advising on Letter of Attestation

## Key Agency Structure

- Aecon Federal Services Inc (AFSI) — 1ZYG1, pre-CMMC Level 2
- Aecon Technology Solutions Inc (ATSI) — 8B3S1, Jackson SC, already CMMC Level 2 certified
- Target: January 2027 for AFSI certification

## Errors Caught by Adversarial Review

### ERROR 1 — Fabricated CR26 Quote (Critical)
**Claim made in briefing:** "FedRAMP does not support or provide 'equivalency'" — attributed to the CR26 CSP page.

**What actually happened:** The CR26 CSP page at `fedramp.gov/2026/cloud-service-providers/` returned empty/JS-rendered content. The quote could not be verified. No evidence it exists on any accessible CR26 page.

**Root cause:** An earlier subagent research pass claimed to have seen this quote. It was accepted without independent verification.

**Fix:** Remove the quote. Reframe: CR26 doesn't address equivalency at all — the term doesn't appear in any CR26 definition or rule.

### ERROR 2 — "CR26 Eliminated Equivalency" Framing (Critical)
**Claim made:** CR26 "eliminated equivalency as a category" and equivalency was "abolished" under the new rules.

**What actually happened:** Equivalency was never a FedRAMP category or Marketplace listing type. It's a DoD-specific construct under the DoD's 2023 memo. CR26 is a forward-looking framework for new certifications — it doesn't address equivalency because equivalency was never part of FedRAMP.

**Fix:** Reframe: "Equivalency was never a FedRAMP category — it's a DoD construct under the 2023 memo. CR26 doesn't change this, but the agency path (which equivalency relied on) is now a legacy path with a June 2027 sunset."

### ERROR 3 — POA&M Conflation (Warning)
**Claim made:** The SAR shows "zero POA&Ms," implying this fully answers the POA&M question.

**What actually happened:** The SAR's Table 2-2 shows "zero open risks at the conclusion of the assessment" (point-in-time, Dec 17, 2025). The DoD memo requires BOTH zero at assessment conclusion AND maintained zero during continuous monitoring. The SAR only confirms the first.

**Fix:** Add a comparison table showing what the SAR confirms vs. what it doesn't. Recommend asking InEight for current continuous monitoring POA&M status.

### INFO — Multiple Additional Fixes
- "Final Draft" SAR status: noted but not flagged as a potential gap — added
- DoD memo Marketplace listing requirement: not initially addressed — added
- NIST 800-53 to 800-171 control mapping challenge: not mentioned initially — added
- ATO framing nuanced: "No ATO needed" was correct but the AO framework nuance was missing — added

## SAR Key Data Points

| Field | Value |
|---|---|
| FedRAMP Unique ID | FR2520254824 |
| 3PAO | A-LIGN |
| Assessment date | Sept 29 — Dec 17, 2025 |
| SAR version | Final Draft v1.0 |
| Impact level | Moderate |
| Cloud type | Government-Only Cloud |
| Underlying IaaS | Azure Government |
| Tenant model | Multi-tenant (gov clients only), separate from commercial |
| Controls assessed | 100% of FedRAMP Moderate baseline |
| SSP version | v3.6 |
| SAP version | v2.2 |
| Pen test date | October 31, 2025 |
| Assessment result | Zero open findings (all categories: High/Moderate/Low/Operational/VD) |
| A-LIGN recommendation | DoD FedRAMP Moderate Equivalency per DoD memo |
| Documentation | 17 auxiliary docs (incident response, BCP, vendor risk, clean desk, etc.) |

## DFARS 7012(b)(2)(ii)(D) — Exact Text

> "(D) If the Contractor intends to use an external cloud service provider to store, process, or transmit any covered defense information in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline [...]"

Key observations:
- Says "equivalent to" — not "authorized by" or "listed on the Marketplace"
- Contractor "shall require and ensure" — the obligation is on the contractor, not the CSP
- This is what makes equivalency a viable path: the standard is equivalence, not authorization

## DoD 2023 Equivalency Memo — Conditions

The memo (exact title: "DoD Memorandum for the Federal Risk and Authorization Management Program Moderate Equivalency for Cloud Service Provider's Cloud Service Offerings") requires:
1. Third-party assessment by a FedRAMP-recognized 3PAO (A-LIGN — confirmed)
2. Zero open or unresolved POA&Ms at time of authorization (confirmed from SAR)
3. Maintain zero POA&M posture during continuous monitoring (NOT confirmed — needs InEight)
4. CSP listed on FedRAMP Marketplace as "FedRAMP Ready" or better under pre-CR26 framework (tension: InEight is not on Marketplace)
5. Annual re-confirmation (first checkpoint: Dec 2026)
6. DoD contracts only (not applicable to civilian agencies)

## Three-Layer Analysis Framework

**Layer 1 — DFARS text:** "Equivalent to" FedRAMP Moderate, not "authorization." Legal foundation is solid.

**Layer 2 — DoD 2023 memo + 3PAO assessment:** Confirmed via A-LIGN SAR. But continuous monitoring POA&Ms and Marketplace listing conditions are open.

**Layer 3 — Azure infrastructure:** Azure Government is FedRAMP High authorized. This is the strongest layer — the infrastructure is fully certified even if the application layer is equivalency-only.

## Risk Register Summary

| # | Risk | Severity | Key Mitigation |
|---|---|---|---|
| R1 | CO rejects equivalency at award | High | 1-page DFARS summary, SAR, LOA |
| R2 | C3PAO flags SAR gap in CMMC | Medium | SSP documentation, LOA, NIST mapping |
| R3 | InEight has open POA&Ms (7-month gap) | Medium | Ask InEight (Q2) |
| R4 | CR26 sunset — equivalency framework ends | High | Ask InEight (Q5) |
| R5 | DCAA finds inadequate due diligence | High/Low | SAR is strong evidence |
| R6 | Civilian agency won't recognize equivalency | High | Depends on customer |
| R7 | InEight marketing creates bad faith impression | Medium | Be transparent upfront |

## Key Insight

**Aecon doesn't inherit more risk from equivalency than from full FedRAMP authorization.** DFARS puts the "require and ensure" obligation on the contractor regardless of the CSP's label. The risk is about *evidence* of due diligence, not the authorization path. With the A-LIGN SAR showing zero findings, Aecon has strong evidence.

## Sources for This Session

- A-LIGN FedRAMP SAR for InEight Inc. Document - US Government, v1.0, 12/17/2025 (19+ pages)
- DFARS 252.204-7012(b)(2)(ii)(D) via Cornell LII (law.cornell.edu/cfr/text/48/252.204-7012)
- FedRAMP.gov CR26 (fedramp.gov/2026) — Definitions and Important Dates pages
- FedRAMP Marketplace (fedramp.gov/marketplace/products/) — searched July 10, 2026
- InEight Security Page (ineight.com/company/security/)
- GLOBE NEWSWIRE press release (Jan 8, 2026) — InEight announces FedRAMP Moderate Equivalency
- Aecon internal emails — Olivia Baer, Habie Ng, Rodney Childress, Brian Gregorio correspondence
