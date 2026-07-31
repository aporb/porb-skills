# NIST SP 800-171 Rev 2 vs Rev 3 Transition Research

## Executive Summary

NIST SP 800-171 Rev 3 was finalized on **May 14, 2024**, superseding Rev 2 (published 01/28/2021). However, **CMMC Level 2 assessments remain legally anchored to Rev 2** via 32 CFR Part 170 (CMMC Final Rule, October 15, 2024). The transition to Rev 3 is years away (realistically 2028 at earliest) and requires new federal rulemaking.

**Strategic Implication:** Organizations should build for Rev 2 compliance now. The legal and contractual reality is that CMMC L2 assessments, SPRS scores, and annual affirmations are all against Rev 2 controls. Rev 3 is worth understanding for forward planning (especially supply chain risk management), but not worth implementing ahead of your Rev 2 compliance program.

---

## What Changed from Rev 2 to Rev 3

### Control Families
- **Rev 2:** 14 control families
- **Rev 3:** 17 control families (+3 new families)

### New Control Families (Net-Add to Rev 2)

1. **Planning (PL)** — Elevated to separate family from Rev 2's Security Assessment family
   - Requires documented security plans describing system boundaries
   - Operational environment documentation
   - Control implementation documentation
   - Security strategy covering CUI system lifecycle

2. **System and Services Acquisition (SA)** — Net-new family
   - Secure system acquisition requirements
   - Developer security testing requirements
   - Supply chain security safeguards at acquisition level
   - Formal acquisition security requirements for CUI-impacting systems

3. **Supply Chain Risk Management (SR)** — Major net-new family
   - Establish supply chain risk management policies
   - Identify supply chain risks
   - Include security requirements in supplier contracts
   - Assess third-party providers before and after onboarding
   - Component authenticity and provenance tracking
   - Acquisition strategies for ICT/OT components
   - Reflects DoD's increasing concern about supply chain attacks post-SolarWinds 2020

### Control Count Discrepancy Explained

| Metric | Rev 2 | Rev 3 | Delta |
|--------|-------|-------|-------|
| Control requirements | 110 | 97 | -13 (apparent reduction) |
| Control families | 14 | 17 | +3 |
| Determination statements | ~320 | ~422 | +32% |
| Organization-Defined Parameters (ODPs) | 0 | ~40 | +40 |

**Why the apparent reduction?**
- 36 controls from Rev 2 were **withdrawn/moved** to "Non-Federal Organization" (NFO) category — NIST considers these basic hygiene any organization should already have
- ~23-24 **new requirements** were added (not in Rev 2)
- Some controls were split into more granular requirements
- Overall structure streamlined but assessment complexity increased

**Key Takeaway:** The 97 vs 110 count is misleading on paper. The 32% increase in determination statements (422 vs 320) and addition of ~40 ODPs make Rev 3 **meaningfully harder to assess** despite the lower headline control count.

### Organization-Defined Parameters (ODPs)

Rev 3 introduces ODPs that replace fixed spec values with organization-documented values. Examples:
- Password minimum length (NIST 800-63B says 8; most contractors set 12)
- Account lockout threshold and duration
- Audit log retention period (typical: 1 year; contracts may demand longer)
- Security training frequency (typical: annual)
- Vulnerability scan frequency (typical: monthly; quarterly is the floor)
- Patch deployment timeline (typical: critical within 30 days)

**Implementation Impact:** Every ODP must be specified in your System Security Plan (SSP). An assessor will ask "what are your defined values?" and you need a defensible answer tied to an authoritative source (e.g., NIST 800-63B). Leaving ODPs blank or copying spec defaults without justification is a common pitfall.

### Control Numbering Format Change

- **Rev 2:** `3.x.x` format (e.g., `3.1.1` for Access Control requirement 1)
- **Rev 3:** SP 800-53 Rev 5-aligned identifiers

**Operational Impact:** Documentation, SSP content, POA&M references, and training materials built around Rev 2's `3.x.x` control IDs will need reformatting when transitioning to Rev 3. This is not a substantive change to security requirements but creates rework.

### Enhanced Requirements in Existing Families

**Zero Trust and Cloud:**
- Zero-trust architecture principles and microsegmentation
- Cloud service provider oversight and shared responsibility documentation
- FedRAMP alignment for cloud-hosted CUI environments
- Software supply chain integrity including SBOM requirements

**Configuration Management:**
- More specific requirements for development environment configuration management
- Defined configuration management baselines

**System and Communications Protection:**
- Expanded network boundary protection
- Additional controls for cloud environments

**Risk Assessment:**
- Threat intelligence integration
- Risk response documentation

**Incident Response:**
- Enhanced supply chain incident handling (coordinating with Rev 3's new SR family)

---

## CMMC Level 2 Current Assessment Baseline

### CMMC L2 Assesses Against: Rev 2

**Legal Basis:** 32 CFR Part 170, the CMMC Final Rule published **October 15, 2024**, explicitly specifies in the assessment methodology that CMMC Level 2 requires implementation of security requirements in **NIST SP 800-171 Rev 2** (dated February 2020).

**What This Means:**
- C3PAO assessments are conducted against Rev 2 requirements
- SPRS scores are calculated on 110 Rev 2 controls
- Annual affirmations certify compliance with Rev 2
- Full stop — your assessor, your SPRS score, and your affirmation are all Rev 2

### CAP (CMMC Assessment Process) Status

The CMMC Assessment Process (CAP) is currently aligned with Rev 2 controls. DoD has not updated CAP methodology to require Rev 3.

---

## Rev 3 Transition Timeline

### Federal Rulemaking Requirement

For CMMC to transition from Rev 2 to Rev 3, DoD must:
1. Publish notice of proposed rulemaking (NPRM)
2. Open public comment period (typically 60-90 days)
3. Review and address public comments
4. Publish final rule
5. Implement with specified effective date

**Rulemaking Timeline:** 18-36 months under favorable conditions.

### Key Dates

| Date | Event |
|------|-------|
| May 14, 2024 | NIST publishes SP 800-171 Rev 3 (final) |
| October 15, 2024 | CMMC 32 CFR Final Rule takes effect — references Rev 2 |
| November 10, 2025 | Phase 1 begins — Select contracts require CMMC self-assessments |
| November 10, 2026 | Phase 2 begins — C3PAO Level 2 assessments broadly required |
| November 10, 2027 | Phase 3 begins — Level 2 and Level 3 broadly required |

### DoD Official Position on Rev 3 Adoption

**Status:** No official timeline or guidance announced for transitioning CMMC to Rev 3.

**Analysis:** Given that the CMMC rule just went through a multi-year development process and published in late 2024, a transition rule modifying the technical standard reference is not coming quickly. Realistically, Rev 3 transition to CMMC is **2028 at earliest** before any contractual effect.

---

## Strategic Recommendations for 5-10 Year Planning

### For Aecon (or any federal contractor)

1. **Certify Against Rev 2 First**
   - CMMC L2 certifications are valid for 3 years from certification date
   - If certifying now (2026), certification valid until 2029
   - Rev 3 transition not expected before certification expires

2. **Document ODP Values Strategically**
   - When building SSP for Rev 2, document ODP-style parameter values even though Rev 2 doesn't require them
   - Pick values aligned with best practices (NIST 800-63B, CIS benchmarks)
   - Cite authoritative sources in documentation
   - This positions you for smoother Rev 3 transition

3. **Start Building Supply Chain Risk Management Practices**
   - Supply Chain Risk Management (SR) is the biggest net-new area in Rev 3
   - Begin building vendor assessment workflows, supplier contract security clauses, and provenance tracking now
   - This is forward-looking work that doesn't require Rev 3 certification but pays off in resilience

4. **Document Cloud Architecture Thoroughly**
   - Rev 3 strengthens cloud and zero-trust requirements
   - Document shared responsibility models, CSP oversight, and FedRAMP alignment
   - This documentation will carry forward to Rev 3 assessments

5. **Follow DoD Rulemaking for Transition Signals**
   - Watch Federal Register for CMMC rulemaking notices
   - DoD must publish NPRM before changing Rev 2 reference to Rev 3
   - No NPRM = no transition timeline = stay Rev 2

---

## Research Approach for Blocked Government Sites

### Problem Sites

The following government sites block automated research access during this session:
- **acquisition.gov** — Returns empty/JS-redirected content for DFARS clauses
- **sam.gov** — Returns minimal content, blocking SPRS scoring methodology access
- **cyberab.org** — Returns empty content, blocking C3PAO directory access
- **dodcio.defense.gov** — 403 Access Denied for CMMC CAP and scoping guides

### Research Strategy

1. **Primary Sources (Accessible)**
   - NIST websites (csrc.nist.gov) reliably return content
   - Use official NIST documentation as source of truth for control counts, family structures, publication dates

2. **Industry Analysis (Accessible)**
   - cmmc-hub.com — Detailed Rev 2 vs Rev 3 comparison, transition timeline analysis
   - CMMC Command (cmmccommand.org) — Control family changes, new requirements
   - Secureframe (secureframe.com) — Structural changes, ODPs, control count
   - Field Ledger (fieldledger.us) — Control count discrepancy resolution, NFO category
   - Cybriant (cybriant.com) — Determination statement analysis

3. **Government Sources (Blocked)**
   - For C3PAO counts, SPRS scoring, DFARS verification:
     - Document the limitation explicitly in research output
     - Provide citations for accessible sources
     - Note which data points require manual verification via corporate browser
     - Do not fabricate numbers or cite blocked sources

4. **Verification Framework**
   When presenting findings, distinguish between:
   - **Verified via primary/industry sources:** Control counts, family structures, new requirements, timeline estimates
   - **Requires manual verification:** C3PAO counts, SPRS scoring thresholds, DFARS exact clause language

### Tool-Specific Patterns

- **ddgr search tool** — Experiences rate limiting; switch to direct curl requests after initial discovery
- **curl on government sites** — Returns empty/JS-redirected content; fallback to industry analysis
- **browser_navigate on government sites** — Returns JS shell; not effective for automated extraction

---

## Citations

### NIST Official
- NIST SP 800-171 Rev 3 Final Publication: May 14, 2024 — https://csrc.nist.gov/pubs/sp/800/171/r3/final
- NIST News Release: "NIST Issues Updated Security Requirements and Assessment Procedures," May 14, 2024 — https://www.nist.gov/news-events/news/2024/05/nist-issues-updated-security-requirements-and-assessment-procedures

### CMMC Regulatory
- CMMC Final Rule: 32 CFR Part 170, published October 15, 2024 — https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XII/part-170

### Industry Analysis
- cmmc-hub.com — "NIST 800-171 Rev 3: What Changed and Why It Doesn't Matter Yet" — https://www.cmmc-hub.com/nist-800-171-rev-3-what-changed-and-why-it-doesnt-matter-yet/
- CMMC Command — "NIST SP 800-171 Rev 3: What Changed and What It Means for CMMC" — https://cmmccommand.org/blog/nist-800-171-rev-3-changes
- Secureframe — "NIST 800-171 Rev 2 vs Rev 3: What Changed and What It Means for CMMC" — https://secureframe.com/blog/nist-800-171-rev2-vs-rev3
- Field Ledger — "NIST 800-171 Rev 3: What Changed, Why, and When You Need to Care" — https://fieldledger.us/blog/nist-800-171-rev-3-changes
- Cybriant — "NIST SP 800-171 Rev 3: What Changed and How to Comply" — https://cybriant.com/feeds/blog/nist-sp-800-171-rev-3

---

## Key Takeaways for Aecon 5-10 Year Strategic Roadmap

1. **Build for Rev 2 now.** The legal and contractual reality is that CMMC L2 assessments, SPRS scores, and annual affirmations are all against Rev 2 controls.
2. **Rev 3 transition is years away.** Realistically 2028 at earliest before any contractual effect. Requires new federal rulemaking (18-36 months).
3. **Document ODP values strategically.** When building SSP for Rev 2, document parameter values aligned with best practices for smoother future transition.
4. **Start building supply chain risk management practices.** SR is the biggest net-new area in Rev 3 — begin vendor assessment workflows and supplier contract security clauses now.
5. **Follow DoD rulemaking for transition signals.** Watch Federal Register for CMMC NPRM. No NPRM = no transition timeline = stay Rev 2.