# FOCI and CMMC Strategic Analysis Patterns

**When to use this reference:** When a federal contractor has a foreign parent, multiple legal entities, and needs both CMMC L2 certification (CUI work) and FCL (classified work). This is the strategic layer above the tactical compliance toolkit.

## Core Strategic Insight

**You are not building a CMMC enclave. You are building a US federal subsidiary** with three pillars:
1. **Entity formation** — FOCI-mitigated legal entity with proper CAGE code
2. **FOCI mitigation** — SSA/Proxy Agreement for classified work access
3. **CMMC L2 certification** — Entity-level cybersecurity assessment

The compliance toolkit is tactical execution. The strategic roadmap determines whether that execution even matters.

## Key Distinctions

| Dimension | CMMC Level 2 | FCL (Facility Clearance) |
|-----------|--------------|--------------------------|
| **Protects** | CUI / CDI / FCI | Classified information (Confidential, Secret, TS) |
| **Authority** | DoD CIO / CMMC PMO | DCSA (Defense Counterintelligence and Security Agency) |
| **Assessment** | C3PAO certification | DCSA facility clearance investigation |
| **Required for** | All DoD contracts with CUI | Contracts requiring access to classified information |
| **FOCI trigger** | **No** — CMMC does not consider FOCI | **Yes** — FCL cannot be granted to FOCI entities without mitigation |
| **Timeline** | ~3–6 months for C3PAO assessment | 6–18 months for DCSA FCL + SSA negotiation |

**Critical:** A foreign-owned company can get CMMC L2 certified without FOCI mitigation. You can win CUI-bearing contracts with CMMC L2. But classified work (Sentinel, Top Secret) needs FCL → needs FOCI mitigation.

## FOCI Mitigation Instruments

For foreign-owned companies (Canadian, UK, Australian, EU):

| Instrument | When to Use | Key Requirements | Aecon Case |
|------------|-------------|------------------|------------|
| **Special Security Agreement (SSA)** | Five Eyes allies, dispersed ownership | Independent US-citizen board, US-citizen KMP, operational control over classified work | **Recommended** — BAE Systems model |
| **Proxy Agreement** | Higher-risk foreign ownership (China, Russia), significant parent influence | Three US-citizen proxy holders exercise foreign owner's voting rights, majority US-citizen board | Unlikely overkill for Canadian parent |
| **Voting Trust Agreement** | Single controlling foreign shareholder | Foreign owner transfers voting rights to US-citizen trustees | Unlikely — Aecon is publicly traded with dispersed ownership |
| **Board Resolution** | Minimal FOCI, small foreign investment | Board resolves to exclude foreign influence from classified contracts | Insufficient — Aecon's FOCI is too extensive |

**Favorable factors for Aecon:**
- Canada = Five Eyes ally (lowest-risk foreign ownership category)
- 2018 CCCC block precedent — Canadian government blocked Chinese state-owned CCCC acquisition of Aecon on national security grounds
- Existing US segregated entity (ATSI holds CMMC cert)
- Active CUI-bearing contracts (SRPPF, Howard Hanson Dam)

**Timeline:** 6–18 months from DCSA engagement to executed SSA

**Cost:** $100K–$500K in legal/counsel fees

**KMP Requirements under SSA:**
- SMO (Senior Management Official): US citizen (candidate: Henderson)
- FSO (Facility Security Officer): US citizen (not appointed — could combine with compliance role)
- ITPSO (Insider Threat Program Senior Official): US citizen (not appointed)
- AFSI Board: Majority US citizens (not constituted)

## CMMC Scope Rules

### Entity-Level Certification

**CMMC certification is granted at the entity level, scoped to a specific CAGE code.**

- **One company can have multiple enclaves** under the same CAGE code. ATSI's Jackson/SC enclave and a future Charlotte enclave could both fall under one CMMC certification if they're under the same CAGE.
- **Different CAGE codes = different certifications.** If AFSI gets its own CAGE code (separate from ATSI's 8B3S1), it needs its own CMMC assessment.
- **CMMC reciprocity:** CMMC L2 certification does carry across contracts under the same CAGE code. It is not contract-specific — it's entity-scoped.
- **Enclave expansion:** Adding systems to an existing enclave doesn't require re-certification, but it does require updating the SSP, scope determination, and evidence.

### CAGE Code Strategy

| Option | Approach | Pros | Cons |
|--------|----------|------|------|
| **A: Single CAGE, expand enclave** | Keep ATSI's CAGE 8B3S1, expand Jackson cert to cover Charlotte/Sentinel | One certification, leverage existing cert, faster | ATSI is being phased out; CAGE may not map to AFSI's corporate structure |
| **B: AFSI gets own CAGE + cert** | AFSI (CAGE 1ZYG1) gets its own CMMC L2 assessment from scratch | Clean entity alignment, right for FOCI/SSA structure | Full new assessment (~3-6 months, $30K-$100K) |

**Recommendation:** Option B. The FOCI mitigation and entity formation are going to create AFSI as a separate legal entity anyway. Build AFSI's certification clean from the start.

## NIST SP 800-171 Rev 3 Transition

### What Changed

| Dimension | Rev 2 (Current) | Rev 3 (Future) |
|-----------|----------------|----------------|
| **Control count** | 110 controls (3.1–3.14) | 97 controls (reorganized), but **more requirements within each** — net increase |
| **Structure** | 14 families, paragraph-level (3.1.1) | Reorganized into logical groups, requirement-level numbering |
| **New areas** | No supply chain risk management | **Supply chain risk management (SCRM)** — new requirements |
| **Authentication** | MFA for privileged accounts | **Phishing-resistant MFA, passwordless options** |
| **Assessment** | SPRS self-assessment (basic/medium/high) | Refined scoring with new point values per requirement |

### Timeline

- **NIST published SP 800-171 Rev 3:** January 2024
- **NIST published SP 800-171A Rev 3:** May 2024 (assessment procedures)
- **DoD CMMC currently assesses against Rev 2.** The CMMC Final Rule (32 CFR Part 170) references NIST SP 800-171 Rev 2.
- **DFARS 252.204-7012 currently requires Rev 2.** DoD has not yet updated the clause.
- **Expected transition:** DoD will likely update DFARS 252.204-7012 to reference Rev 3 in a future rulemaking (likely 2027–2028). Contractors will get a transition period (typically 6–12 months).
- **Practical deadline:** If certifying against Rev 2 in 2026/2027, re-assess against Rev 3 by ~2028–2029.

### Build Strategy

**Build for Rev 2, design for Rev 3.**

- Implement phishing-resistant MFA now (Rev 3 requirement, best practice regardless)
- Start a vendor/supplier risk management process (Rev 3 SCRM requirement)
- Document controls at the requirement level, not just the family level (Rev 3 is more granular)

## 5-Phase Strategic Roadmap Template

### Phase 1: Foundation (Now–12 months)

**Objective:** CMMC L2 certification + entity formation

**Deliverables:**
- CMMC L2 certification (C3PAO assessment complete)
- AFSI incorporation (Delaware)
- CAGE 1ZYG1 certification (separate from ATSI's 8B3S1)
- GCC High enclave operational
- SSP, POA&M, evidence collection complete
- SPRS score posted
- FOCI counsel engaged

**Cost:** $200K–$500K

### Phase 2: FOCI Mitigation + FCL Pursuit (12–24 months)

**Objective:** SSA executed, FCL granted

**Deliverables:**
- SSA filed to DCSA
- AFSI board formed (majority US citizens)
- FSO/ITPSO designated (US citizens)
- Facility Security Clearance process initiated
- Insider threat program operational
- Monitor for NIST Rev 3 transition signal

**Cost:** $100K–$500K

### Phase 3: Scale (24–36 months)

**Objective:** Contract award(s) + classified operations

**Deliverables:**
- Sentinel or similar classified contract execution
- Classified work under FCL
- NIST Rev 3 re-assessment (if DoD signals transition)
- Enclave expansion for new programs
- CMMC triennial re-assessment

**Cost:** $100K–$200K

### Phase 4: Maturity (36–60 months)

**Objective:** Prime contractor positioning

**Deliverables:**
- Supply chain CMMC flow-down requirements operational
- Automated compliance operations
- Multi-site expansion
- Ongoing compliance operations

**Cost:** $200K–$500K/year

### Phase 5: Market Leadership (60+ months)

**Objective:** Top-tier federal contractor positioning

**Deliverables:**
- Potential CMMC L3 positioning
- Ongoing SSA compliance and FCL renewal
- AI/ML security framework (FY2026 NDAA §1513)
- Second FCL renewal

**Cost:** $200K–$500K/year

## Key Decision Points

| # | Decision | Options | Recommendation | Deadline |
|---|----------|---------|----------------|----------|
| 1 | CAGE code strategy | Expand ATSI's 8B3S1 cert, OR new cert for AFSI/1ZYG1 | New cert (clean entity alignment) | Before contract bid |
| 2 | FOCI instrument | SSA vs Proxy vs Board Resolution | SSA (BAE Systems model) | Phase 2 |
| 3 | C3PAO selection | Which authorized assessor | Research cmmcab.org marketplace | Phase 1 |
| 4 | Enclave tenant strategy | Single GCC High tenant vs separate tenants per program | Single tenant, logically partitioned | Phase 1 |
| 5 | FSO role | Dedicated hire, or combined with compliance role | Combined initially, dedicated by Phase 2 | Phase 2 |
| 6 | Rev 3 preparation | Build for Rev 2 only, or dual-track Rev 2 + Rev 3 | Build for Rev 2 (tested), design for Rev 3 | Ongoing |

## Blocked Resources (Manual Download Required)

DoD CIO and DCSA block all automated downloads (403). These are the strategic gaps:

**DoD CIO:**
- Scoping Guide v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/ScopingGuideL2v2.pdf`
- CAP Level 2 v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/CAP-Level2-Version-2-13.pdf`
- Environment Assessment Guide L2: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/EnvironmentAssessmentGuideL2v2.pdf`
- CMMC Documentation Landing: `https://dodcio.defense.gov/CMMC/`

**DCSA:**
- FOCI Information Page: `https://www.dcsa.mil/mc/ctp/foci/`
- DCSA Main Site: `https://www.dcsa.mil/`

**Manual download required:** Open corporate browser, navigate to URLs, save to `compliance-toolkit/reference-docs/`.

## Aecon FCS Specific Context

**Corporate structure:**
- Aecon Group Inc. (Canadian, TSX:ARE) — Parent
- AEGI (Aecon Energy Group Inc., Delaware) — Amyn's employer
- FCS (Federal Contract Solutions) — Operating division, not a legal entity
- ATSI (Aecon Technical Services Inc.) — CAGE 8B3S1, holds Jackson CMMC cert, being phased out
- AFSI (Aecon Federal Services Inc.) — CAGE 1ZYG1, planned FOCI-mitigated entity, not yet incorporated

**Favorable factors:**
- Canada = Five Eyes ally (lowest-risk FOCI category)
- 2018 CCCC block precedent demonstrates Canadian government protects Aecon from adversarial ownership
- Existing US segregated entity (ATSI) and GCC High enclave
- Active CUI-bearing contracts (SRPPF, Howard Hanson Dam)

**Comparable model:** BAE Systems plc (UK) → BAE Systems Inc. (US) under SSA. Independent US-citizen board, separate IT infrastructure, US-citizen KMP.

**Strategic target:** Position Aecon as a top-3 Canadian-origin federal defense/nuclear construction contractor by 2036.

## References

- NIST SP 800-171 Rev 3: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf
- NIST SP 800-171A Rev 3: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171Ar3.pdf
- 32 CFR Part 170 (CMMC Final Rule): https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XII/part-170
- 32 CFR Part 117 (NISPOM / FOCI authority): https://www.ecfr.gov/current/title-32/subtitle-B/chapter-I/subchapter-G/part-117
- BAE Systems Inc. public filings: SSA structure, US-citizen board composition