# CMMC Division of Responsibility (DOR) & RACI Framework

**When to use this reference:** When a federal contractor needs to define ownership boundaries
between itself, JV partners, subcontractors, C3PAO assessors, MSPs/MSSPs, and ESPs/CSPs for CMMC
implementation, daily execution, and audit. Also when researching how FOCI-mitigated entities
(BAE Systems, Rolls-Royce model) structure their compliance governance, or when explaining the
DFARS 7012/7020/7021 flow-down chain and subcontractor verification obligations.

## Regulatory Flow-Down Chain (Verified Sources)

### DFARS 252.204-7012 ¶(b)(2)(ii)(D) — CSP FedRAMP Requirement

> If the Contractor intends to use an external cloud service provider to store, process, or transmit
> any covered defense information in performance of this contract, the Contractor shall require and
> ensure that the cloud service provider meets security requirements equivalent to those established
> by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate
> baseline... and that the cloud service provider complies with requirements in paragraphs (c)
> through (g) of this clause for cyber incident reporting, malicious software, media preservation
> and protection, access to additional information and equipment necessary for forensic analysis,
> and cyber incident damage assessment.

**Liability chain:** DoD → Prime → Subcontractor → CSP. The **contractor** (not the CSP) is
responsible for ensuring FedRAMP equivalence, incident reporting compliance, media preservation,
and forensic access.

### DFARS 252.204-7012 ¶(m) — Subcontractor Flow-Down

- Clause must flow to subs **without alteration** (except to identify parties)
- Prime determines whether information retains CDI identity when flowing to subs
- Subs must notify prime of NIST 800-171 variance requests (upward reporting)
- Subs must provide DoD incident report numbers to prime (upward reporting)

### DFARS 252.204-7020 ¶(g) — Assessment Flow-Down

- Prime inserts substance of clause in ALL subcontracts (excluding COTS)
- **Pre-award gate:** Prime cannot award a sub subject to NIST 800-171 unless sub completed Basic
  Assessment within last 3 years
- Prime must check SPRS for subcontractor's score **before** awarding

### DFARS 252.204-7021 ¶(f) — CMMC Flow-Down (NOV 2025)

- ¶(d)(1)(ii): Flow down correct CMMC level per 32 CFR § 170.23
- ¶(d)(4): Ensure subs complete annual affirmation **prior to subcontract award** and annually
- ¶(f)(1): Insert substance of clause (excluding ¶(e)(1)) in subcontracts with FCI/CUI requirement
- ¶(f)(2): **Pre-award gate:** Ensure sub has current CMMC certificate/status at appropriate level

### 32 CFR § 170.23 — Tiered Subcontractor CMMC Requirements

| Subcontractor Processes/Stores/Transmits | Prime Contract Level | Minimum Sub Level |
|---|---|---|
| FCI only (no CUI) | Any | **Level 1 (Self)** |
| CUI | Level 2 (Self) | **Level 2 (Self)** |
| CUI | Level 2 (C3PAO) | **Level 2 (C3PAO)** |
| CUI | Level 3 (DIBCAC) | **Level 2 (C3PAO)** |

Requirements apply at **all tiers** of the supply chain. "Prime contractors shall comply and shall
require subcontractors to comply with and to flow down CMMC requirements, such that compliance will
be required throughout the supply chain at all tiers."

## Prime Contractor Verification Obligations (Sequential)

**Pre-Award:**
1. Classify: Will sub process/store/transmit FCI or CUI?
2. Determine required CMMC level per § 170.23 tiering
3. Verify sub has current CMMC certificate/status at required level (DFARS 7021(f)(2))
4. Verify sub completed Basic NIST 800-171 Assessment within 3 years (DFARS 7020(g)(2))
5. Insert DFARS 7012 without alteration (DFARS 7012(m)(1))
6. Insert substance of DFARS 7020 and 7021 (DFARS 7020(g)(1), 7021(f)(1))
7. Ensure sub's affirming official completed annual affirmation (DFARS 7021(d)(4))

**Ongoing:**
1. Monitor sub CMMC status currency (not older than 3 years for Final L2 C3PAO)
2. Monitor sub annual affirmations
3. Receive/track sub NIST 800-171 variance requests (DFARS 7012(m)(2)(i))
4. Receive incident report numbers from sub incidents (DFARS 7012(m)(2)(ii))
5. Verify sub flow-down to their subs (multi-tier chain)

## FOCI-Mitigated Entity Governance (32 CFR § 117.11)

### Mitigation Instruments

| Instrument | When Applied | Governance Impact |
|---|---|---|
| **Board Resolution** | Foreign interest lacks board representation | Minimal structural change |
| **Security Control Agreement (SCA)** | Foreign interest has board representation but doesn't control entity | ≥1 cleared US citizen outside director |
| **Special Security Agreement (SSA)** | Foreign interest effectively owns/controls entity | **Standard for Five Eyes allies** (BAE, Rolls-Royce model) |
| **Proxy Agreement (PA)** | Higher-risk foreign ownership | US citizen proxy holders exercise voting rights |
| **Voting Trust (VT)** | Single controlling foreign shareholder | Foreign owner transfers legal title to US trustees |

### SSA Required Documents (The "Four-Document Stack")

These documents directly shape the CMMC DOR:

| Document | CFR Citation | CMMC DOR Role |
|---|---|---|
| **Special Security Agreement (SSA)** | § 117.11(d)(2)(iii) | Defines board composition, GSC authority, foreign parent insulation |
| **Technology Control Plan (TCP)** | § 117.11(h)(1) | Physical/logical access controls for non-US persons → maps to AC, PE controls |
| **Electronic Communications Plan (ECP)** | § 117.11(h)(2) | Network separation → maps to SC controls; **regulatory basis for GCC High/commercial tenant isolation** |
| **Affiliated Operations Plan** | § 117.11(h)(3) | Controls for services shared with foreign parent → affects vendor management |

### Government Security Committee (GSC) — § 117.11(g)

- Permanent committee of the board of directors
- Composed of outside directors/proxy holders/trustees (cleared US citizens)
- **FSO is principal advisor to GSC**; GSC chairman concurs with FSO appointment
- FSO functions carried out under GSC authority
- GSC ensures adherence to security laws/regulations; investigates violations
- **Annual review** with CSA (DCSA); annual certification by GSC chairman

### Electronic Communications Plan (ECP) — § 117.11(h)(2)

The ECP is the **regulatory basis** for requiring network separation between the US subsidiary and
foreign parent. It requires:
- Technical and logical separation of electronic communications and networks
- Detailed network description and configuration diagram
- Delineation of shared vs. protected networks
- Firewalls, remote administration, monitoring, maintenance, separate email servers

**For GCC High enclaves:** The ECP is what makes the GCC High/commercial tenant split a regulatory
requirement under FOCI mitigation, not just a best practice. This should be cited when justifying
the enclave architecture to C3PAOs or DCSA.

## BAE Systems / Rolls-Royce Model (Five Eyes FOCI Pattern)

All major Five Eyes-origin defense contractors operating in the US share these DOR characteristics:

1. **Independent US legal entity** with own CAGE code
2. **US-citizen board majority** with GSC oversight
3. **Segregated IT infrastructure** for federal work (separate from parent's commercial IT)
4. **US-citizen KMP** for all security roles (FSO, ITPSO, CISO/CICS)
5. **SSA + TCP + ECP** document stack enforced by DCSA
6. **Annual DCSA review** of FOCI mitigation effectiveness
7. **Independent CMMC assessment** of the US entity's enclave (not the parent's systems)
8. **Flow-down to subcontractors** managed by the US entity, not the foreign parent

**BAE Systems Inc.** (UK parent → US sub under SSA): Independent US-citizen board, separate IT
infrastructure, US-citizen KMP, GSC with outside directors.

**Rolls-Royce North America** (UK parent → US sub under SSA): Same structure; operates DOE/NNSA
nuclear contracts — directly relevant to Aecon's SRS/SRPPF scope.

## Microsoft Shared Responsibility Model (GCC High Context)

| Responsibility Area | On-Prem | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Customer data | Customer | Customer | Customer | Customer |
| Configurations/settings | Customer | Customer | Customer | Customer |
| Identities/users | Customer | Customer | Customer | Customer |
| Client devices | Customer | Customer | Customer | Shared |
| Applications | Customer | Customer | Shared | Shared |
| Network controls | Customer | Customer | Shared | Microsoft |
| Operating system | Customer | Customer | Microsoft | Microsoft |
| Physical hosts | Customer | Microsoft | Microsoft | Microsoft |
| Physical network | Customer | Microsoft | Microsoft | Microsoft |
| Physical datacenter | Customer | Microsoft | Microsoft | Microsoft |

**Customer-retained (regardless of service model):** Data, endpoints, accounts, access management.

## Key DOR Principles

### Non-Delegable Responsibilities

The following CANNOT be outsourced or delegated — the OSA retains accountability:

1. **CMMC Affirmation** — Affirming Official (within OSA) personally attests. Cannot delegate to C3PAO/MSP.
2. **72-hour DIBNet incident reporting** — OSA owns the clock. MSP can detect/escalate; OSA reports.
3. **DFARS 7012/7021 flow-down** — OSA accountable for subcontractor clause compliance.
4. **FOCI mitigation compliance** — GSC, TCP, ECP compliance is the OSA's obligation to DCSA.
5. **Scope determination** — Defining the assessment boundary is the OSA's responsibility.

### Shared Responsibility ≠ Shared Liability

Operational responsibility can be shared or outsourced. **Regulatory liability cannot** — it stays
with the contractor (OSA). If Microsoft's GCC High has a breach exposing CUI, DoD pursues the OSA,
not Microsoft. The OSA's recourse is through its contractual relationship with the CSP (BAA, SLA).

### Foreign Parent Firewall

For FOCI-mitigated entities, the DOR must establish an absolute firewall:

1. **Architectural** — GCC High enclave technically inaccessible to foreign personnel (Entra ID conditional access)
2. **Organizational** — GSC with US-citizen majority oversees security decisions
3. **Procedural** — TCP and ECP define and enforce separation
4. **Audit** — DCSA annual review verifies firewall effectiveness
5. **Incident** — Any attempt by foreign personnel to access CUI is reportable under FOCI + DFARS 7012

## RACI Matrix Structure

A complete DOR matrix for a CMMC L2 contractor should include these RACI dimensions:

1. **Implementation RACI** — who builds/configures/implements each control family
2. **Operations RACI** — who runs/monitors/responds day-to-day
3. **Audit RACI** — who prepares evidence, who assesses, who affirms
4. **Incident RACI** — who detects, who reports, who responds, who notifies
5. **Flow-down RACI** — who verifies subs, who flows clauses, who tracks affirmations
6. **FOCI Firewall RACI** — what the foreign parent can/cannot do, how it's enforced

**Party definitions for RACI:**
- **OSA** (Organization Seeking Assessment) — the entity being certified
- **JV Partners** — other companies accessing CUI through the OSA's enclave
- **Subcontractors** — Tier 1+ subs processing FCI/CUI
- **C3PAO** — independent assessor (cannot be implementer — conflict of interest)
- **MSP/MSSP** — managed service/security provider (if engaged)
- **ESPs** — External Service Providers (Microsoft GCC High, Box, InEight)
- **DCSA** — FOCI mitigation oversight authority
- **Foreign Parent** — must be insulated from CUI

## Research Technique: Cornell LII for Regulatory Text

Government regulatory sites (eCFR, Federal Register, acquisition.gov, dodcio.defense.gov) and
search engines (Google, Bing, DuckDuckGo) all block automated access. **Cornell LII**
(law.cornell.edu) reliably serves the full eCFR text and is curl/browser-accessible.

**URL patterns:**
- DFARS clauses: `https://www.law.cornell.edu/cfr/text/48/252.204-7012` (or -7020, -7021)
- CMMC rule: `https://www.law.cornell.edu/cfr/text/32/170.NN` (any section)
- NISPOM/FOCI: `https://www.law.cornell.edu/cfr/text/32/117.11`

**Extraction technique for JS-rendered pages:**
```javascript
document.querySelector('main').innerText  // via browser_console
// or for long pages, paginate with substring:
document.querySelector('main').innerText.substring(0, 12000)
document.querySelector('main').innerText.substring(12000, 24000)
```

## Regulatory Citations Index

| Citation | Key DOR Provision |
|---|---|
| DFARS 252.204-7012 ¶(b)(2)(ii)(D) | CSP FedRAMP Moderate equivalence requirement |
| DFARS 252.204-7012 ¶(m) | Subcontractor flow-down without alteration |
| DFARS 252.204-7020 ¶(g) | Pre-award Basic Assessment verification for subs |
| DFARS 252.204-7021 ¶(d)(4) | Annual affirmation of subcontractors |
| DFARS 252.204-7021 ¶(f) | Pre-award CMMC status verification for subs |
| 32 CFR § 170.23 | Tiered CMMC level requirements by FCI/CUI processing |
| 32 CFR § 117.11(d)(2) | FOCI mitigation instruments (SSA, PA, VT, SCA) |
| 32 CFR § 117.11(g) | Government Security Committee requirements |
| 32 CFR § 117.11(h)(1) | Technology Control Plan |
| 32 CFR § 117.11(h)(2) | Electronic Communications Plan |
| Microsoft Shared Responsibility | IaaS/PaaS/SaaS responsibility matrix |
