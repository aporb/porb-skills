# NIST RMF + FedRAMP Authorization Lifecycle Reference

> Compiled from NIST CSRC (csrc.nist.gov), FedRAMP Consolidated Rules for 2026 (fedramp.gov/2026), FedRAMP GitHub rules repo (github.com/FedRAMP/rules), NIST SP 800-37 Rev 2, SP 800-53 Rev 5, SP 800-171 Rev 2. July 2026.

## NIST RMF 7-Step Lifecycle (SP 800-37 Rev 2)

Rev 2 added "Prepare" as a preparatory step — it's 7 steps, not 6.

| # | Step | Purpose | Key Outcomes |
|---|------|---------|-------------|
| 0 | **PREPARE** | Prepare the organization to manage security and privacy risks | Risk management roles identified; org-wide risk strategy established; org-wide risk assessment done; org-wide ConMon strategy developed; common controls identified |
| 1 | **CATEGORIZE** | Determine adverse impact from loss of CIA | System characteristics documented; FIPS 199 categorization (Low/Moderate/High); categorization approved by AO |
| 2 | **SELECT** | Select, tailor, and document controls | SP 800-53B baseline selected; controls tailored; controls designated as system-specific / hybrid / common; ConMon strategy developed; SSP reviewed/approved |
| 3 | **IMPLEMENT** | Implement the controls | Controls implemented per plans; SSP updated to reflect as-implemented state |
| 4 | **ASSESS** | Determine if controls are correctly implemented and operating | Assessor selected; SAP developed per SP 800-53A; control assessments conducted; **SAR** produced; remediation actions taken; **POA&M** developed; SSP updated |
| 5 | **AUTHORIZE** | Senior official determines if risk is acceptable | Authorization package assembled (SSP + SAR + POA&M); risk determination rendered; **ATO** approved or denied |
| 6 | **MONITOR** | Maintain ongoing situational awareness | System monitored per ConMon strategy; ongoing assessments (SP 800-137/137A); outputs analyzed and responded to; posture reported to management; ongoing authorization |

**Key RMF artifacts:** SSP (System Security Plan), SAP (Security Assessment Plan), SAR (Security Assessment Report), POA&M (Plan of Action and Milestones), ATO Letter.

## NIST SP 800-53 Rev 5 Control Catalog — 20 Families

| # | ID | Family | Focus |
|---|----|--------|-------|
| 1 | AC | Access Control | Who can access what |
| 2 | AT | Awareness and Training | Security training |
| 3 | AU | Audit and Accountability | Logging, monitoring |
| 4 | CA | Assessment, Authorization, and Monitoring | RMF governance |
| 5 | CM | Configuration Management | Baselines, change control |
| 6 | CP | Contingency Planning | Disaster recovery |
| 7 | IA | Identification and Authentication | User/device identity |
| 8 | IR | Incident Response | IR planning, handling |
| 9 | MA | Maintenance | System maintenance |
| 10 | MP | Media Protection | Media handling, sanitization |
| 11 | PE | Physical and Environmental Protection | Physical security |
| 12 | PL | Planning | Security planning |
| 13 | PM | Program Management | Enterprise-level program |
| 14 | PS | Personnel Security | Personnel screening |
| 15 | PT | PII Processing and Transparency | Privacy (NEW in Rev 5) |
| 16 | RA | Risk Assessment | Risk assessment |
| 17 | SA | System and Services Acquisition | SDLC, supply chain |
| 18 | SC | System and Communications Protection | Network, crypto |
| 19 | SI | System and Information Integrity | Malware, alerts |
| 20 | SR | Supply Chain Risk Management | SCRM (NEW in Rev 5) |

**Baselines:** Low (~125 controls), Moderate (~325), High (~425), Privacy (all systems). Per SP 800-53B.

## SP 800-53 → SP 800-171 Mapping

SP 800-171 Rev 2: **110 requirements** in **14 families**, all derived from 800-53. SP 800-171 is a subset at the "moderate confidentiality" CUI impact level.

- CMMC 2.0 maps directly to SP 800-171 Rev 2 (three levels)
- DFARS 252.204-7012/7019/7020 mandate 800-171 compliance
- SP 800-171A provides assessment procedures per requirement

## FedRAMP Authorization Paths (2026 Consolidated Rules)

### Two Certification Paths

| Path | Description | Rule |
|------|-------------|------|
| **FedRAMP Program Certification** | Direct certification by FedRAMP. Provider applies via Certification Application Form, supplies fresh Certification Package, undergoes FedRAMP-managed assessment. Primary path for 20x certs. Replaces old JAB/P-ATO. | FRC-APP-AFC, FRC-APP-FCP |
| **FedRAMP Agency Certification** (Rev5 only) | Provider completes ATO process with agency sponsor, concluding with formal signed ATO letter sent over official government channels to FedRAMP. FedRAMP reviews and lists. | FRC-APS-ATO |

### Terminology Changes (2026)

| Legacy | 2026 |
|--------|------|
| FedRAMP Authorization | FedRAMP Certification |
| JAB/PMO P-ATO | FedRAMP Program Certification |
| Agency ATO | FedRAMP Agency Certification (legacy, Rev5 only) |
| 3PAO | FedRAMP Recognized independent assessor |
| Low / Moderate / High impact | Class A / B / C / D |
| SSP (System Security Plan) | SDR (Security Decision Record) for 20x |

### Readiness Assessment (RAR)

Legacy pre-assessment where a FedRAMP-recognized assessor evaluates CSP organizational processes and security capabilities before full assessment. In 2026 rules, absorbed into: Marketplace listing first (FRC-APP-MLF), fresh Certification Package (FRC-APP-FCP), and fresh Independent Assessment (FRC-APP-FIA).

## FedRAMP Phases & Key Artifacts

| Phase | CSP Produces | Assessor Produces | FedRAMP/Agency Produces |
|-------|-------------|-------------------|------------------------|
| **Readiness** | Documentation, architecture, control narratives | RAR | Readiness determination |
| **Assessment** | Evidence, interviews, POA&M responses | SAP, SAR + RET + SRTM | SAP approval |
| **Authorization** | SSP + POA&M + Executive Summary | — | ATO Letter / Certification |
| **ConMon** | Vulnerability scans, POA&M updates, Ongoing Certification Report (quarterly), Incident reports | Annual assessment SAR | Quarterly Review, Annual review |

### Key Artifacts

- **SSP**: Comprehensive security posture description, architecture, data flows, control implementations. Multiple appendices (CIS/CRM workbook, ISCP, crypto modules, Rules of Behavior, inventory).
- **SAP**: Assessor-authored plan — methodology, scope, sampling, test procedures per SP 800-53A.
- **SAR**: Assessor findings — control pass/fail, Risk Exposure Table (RET), Security Requirements Traceability Matrix (SRTM).
- **POA&M**: CSP-maintained register of all weaknesses, with remediation actions, milestones, responsible parties, dates. Updated continuously.
- **RAR**: Pre-assessment readiness confirmation.

## Continuous Monitoring / ConMon

### Legacy ConMon (Rev5)

- **Monthly:** Vulnerability scans, POA&M updates, ConMon Executive Summary
- **Annual:** Assessment (subset of controls), penetration test, updated SSP/SAR/POA&M
- **On-change:** Significant Change Requests (SCRs)
- **Vuln SLAs:** Critical/High: 30 days; Moderate: 90 days

### 2026 CCM (Collaborative Continuous Monitoring) — Key Rules

**CCM Ruleset** (`obj['FRR']['CCM']['data']['all']` in machine-readable JSON):

- **AGM (Agency Monitoring)** — Agency responsibilities: review Ongoing Certification Reports, consider security category for resource allocation
- **OCR (Ongoing Certification Reports)** — Provider MUST supply quarterly report to all necessary parties (CCM-OCR-AVL); MUST supply next report date publicly (CCM-OCR-NRD); MUST provide async feedback mechanism (CCM-OCR-FBM); MUST supply anonymized feedback summary (CCM-OCR-AFS)
- **QTR (Quarterly Reviews)** — Provider MUST supply registration/calendar info (CCM-QTR-REG); MUST publicly supply next review date (CCM-QTR-NRD); SHOULD schedule 3 business days after report release (CCM-QTR-SAR); SHOULD record/transcribe (CCM-QTR-RTR)

**Other 2026 rulesets for ConMon:**
- **VDR** (Vulnerability Detection and Response) — vuln detection/remediation timelines, IRV/KEV/LEV classifications
- **VER** (Vulnerability Evaluation and Reporting) — vuln reporting requirements
- **SCN** (Significant Change Notification) — Adaptive, Certification Class, Routine Recurring, Transformative change types
- **IEC** (Incident Evaluation and Communication) — IIR → OIR → FIR reporting chain

### FedRAMP Rulesets Reference (from GitHub JSON)

List all rulesets with `curl -sL https://raw.githubusercontent.com/FedRAMP/rules/main/fedramp-consolidated-rules.json | python3 -c "import json,sys; obj=json.load(sys.stdin); frr=obj['FRR']; [print(f\"{k}: {frr[k]['info']['name']}\") for k in frr if k != 'info']"`

| Key | Ruleset | Purpose |
|-----|---------|---------|
| FRC | FedRAMP Certification | How CSOs obtain and maintain certification |
| CCM | Collaborative Continuous Monitoring | Agency/provider shared monitoring responsibility |
| IVV | Independent Verification and Validation | Expectations for independent assessments |
| MAS | Minimum Assessment Scope | Scope definition for assessment |
| VDR | Vulnerability Detection and Response | Vulnerability management timelines |
| VER | Vulnerability Evaluation and Reporting | Reporting requirements |
| SCN | Significant Change Notification | Change classification and notification |
| IEC | Incident Evaluation and Communication | Incident reporting chain |
| CDS | Certification Data Sharing | Data sharing requirements |
| MKT | Marketplace Listing | Marketplace rules |
| REC | FedRAMP Recognition | Assessor recognition program |
| SCG | Secure Configuration Guide | Secure config documentation |
| SDR | Security Decision Record | Decision documentation |
| AFC | Addressing FedRAMP Communication | Communication protocols |
| AGU | Agency Use | Agency responsibilities |