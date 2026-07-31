# CMMC / NIST 800-171 Compliance Methodology — End-to-End Research

Condensed authoritative reference covering the full NIST 800-171 / CMMC compliance methodology from gap assessment to passing a C3PAO assessment. Sourced from NIST publications, 32 CFR Part 170 (via Cornell LII), DFARS rules, and verified industry analysis. Use this when researching the methodology framework for a client engagement, building a compliance product, or answering deep regulatory questions that go beyond the toolkit-level SOPs and templates.

---

## 1. NIST SP 800-171 Rev 2 — 14 Control Families (110 Controls)

| # | Code | Family | Count | Key Focus |
|---|------|--------|-------|-----------|
| 1 | AC | Access Control | 22 | Least privilege, remote access, MFA, session lock, information flow |
| 2 | AT | Awareness and Training | 3 | Security awareness, role-based training, insider threat awareness |
| 3 | AU | Audit and Accountability | 9 | Audit log creation, review, retention, timestamps, protection |
| 4 | CM | Configuration Management | 9 | Baseline configs, change control, least functionality, software restrictions |
| 5 | IA | Identification and Authentication | 11 | Unique IDs, MFA, password policy, device auth, FIPS crypto |
| 6 | IR | Incident Response | 3 | IR capability, tracking/documenting/reporting, testing |
| 7 | MA | Maintenance | 6 | Authorized personnel, tool controls, remote maintenance logging |
| 8 | MP | Media Protection | 9 | Marking, sanitization, transport, removable media, disposal |
| 9 | PS | Personnel Security | 2 | Background screening, termination procedures |
| 10 | PE | Physical Protection | 6 | Facility access, visitor logs, access device management |
| 11 | RA | Risk Assessment | 3 | Risk assessments, vulnerability scanning, remediation |
| 12 | CA | Security Assessment | 4 | Control assessment, POA&M, continuous monitoring, SSP |
| 13 | SC | System and Communications Protection | 16 | Encryption (FIPS 140-3), segmentation, DoS, wireless, sessions |
| 14 | SI | System and Information Integrity | 7 | Flaw remediation, malware protection, monitoring, scanning |

**Four highest-weight families** (AC=22, SC=16, IA=11, AU=9) account for 55 of 110 controls.

### Rev 3 (May 2024) — Future State Only
- 97 requirements, 17 families (+3: Planning, System & Services Acquisition, Supply Chain Risk Management)
- 36 controls withdrawn (moved to NFO), 23 new controls, ~40 ODPs
- ~422 determination statements (32% more than Rev 2)
- **No current CMMC effect** — requires new federal rulemaking (~2028+)

---

## 2. NIST SP 800-171A — Assessment Procedures

Three assessment methods applied per-control:
- **Examine:** Review documentation, policies, configurations, access lists
- **Interview:** Talk to personnel (employees, admins, managers)
- **Test:** Exercise controls (attempt unauthorized access, verify MFA, check session lock)

~320 determination statements decompose the 110 controls into specific objectives. Each control scored:
- **MET:** All determination statements satisfied
- **NOT MET:** One or more statements not satisfied
- **N/A:** Control doesn't apply (treated as MET)

---

## 3. CMMC 2.0 Model

| Level | Controls | Assessment | Contract Trigger |
|-------|----------|------------|-----------------|
| L1 | 15 (FAR 52.204-21) | Self-assessment | FCI handling |
| L2 | 110 (NIST 800-171 R2) | Self OR C3PAO | CUI handling |
| L3 | 110 + NIST 800-172 | DIBCAC only | Critical programs |

### Phase-In Schedule
- Phase 1 (Nov 10, 2025): L1/L2 Self required; L2(C3PAO) at CO discretion
- **Phase 2 (~Nov 2026): L2(C3PAO) = condition of contract award**
- Phase 3 (~Nov 2027): All applicable contracts + options
- Phase 4 (~Nov 2028): Full implementation

### C3PAO Assessment Lifecycle
1. Engagement & Scoping (select C3PAO, define scope per §170.19)
2. Assessment (all 110 controls, Examine/Interview/Test)
3. Scoring (MET/NOT MET/N/A per §170.24)
4. eMASS Posting → SPRS (includes: date, level, C3PAO name, UID, all CAGE codes, SSP version, per-requirement results, artifact hashes)
5. Status: Conditional (POA&M allowed) or Final (passing, no gaps)
6. **POA&M closeout: 180 days** from Status Date; C3PAO must verify

### Annual Affirmation (§170.22)
- Required EVERY year for ALL levels
- Senior Affirming Official submits in SPRS
- Failure = loss of "Current" status = contract remedy

### Subcontractor Flow-Down (§170.23)
- Applies at ALL tiers
- Sub handling CUI where prime requires L2(C3PAO) → sub must have L2(C3PAO)
- Sub handling FCI only → L1(Self)

---

## 4. SSP & POA&M Structure

### SSP (per NIST SP 800-18)
| Section | Content |
|---------|---------|
| System Identification | Name, ID, owner, CAGE code(s), system type, status |
| System Environment | Description, purpose, scope, boundary, HW/SW inventory |
| System Interconnections | Connections, data flows, ESPs/CSPs |
| Security Requirements Traceability | All 110 controls → implementation mapping |
| Control Implementation | Per-control: description, responsible role, evidence artifact, assessed date |
| Roles and Responsibilities | System owner, ISSO/ISSM, users, admins |
| Plan Maintenance | Review cadence, update procedures, version control |

### POA&M Required Fields
POA&M ID, Control ID, Finding Description, Severity, Discovery Date, Owner, Due Date, Remediation Plan, Resources, Status, Evidence Artifact, Last Updated

---

## 5. Consultant Lifecycle — 7 Canonical Phases

### Phase 1: Scoping & Discovery (Weeks 1–4)
**Artifacts:** Assessment Scope Document, Asset Inventory, CUI Data Flow Register, ESP/CSP Inventory

### Phase 2: Gap Assessment (Weeks 3–8)
**Artifacts:** Gap Assessment Report, Baseline SPRS Score, Gap Findings Matrix, Initial POA&M

### Phase 3: Remediation Planning (Weeks 6–10)
**Artifacts:** Remediation Roadmap, Resource Plan, Updated POA&M

### Phase 4: Implementation & Evidence Collection (Weeks 8–36+)
**Artifacts:** 14 Control Family Policies, SSP (fully populated), Evidence Repository, Cybersecurity Program Checklist, Incident Response Plan, Configuration Baselines, Key Management Plan, Insider Threat Program

### Phase 5: Internal Mock Assessment / Readiness Review (Weeks 30–40)
**Artifacts:** Readiness Assessment Report, Evidence Readiness Checklist, Expected SPRS Score, Staff Interview Prep Briefing

### Phase 6: C3PAO Engagement & Assessment (Weeks 36–48)
**Artifacts:** C3PAO Assessment Report, Final SPRS Score, CMMC Status/Certificate, POA&M Closeout Evidence

### Phase 7: Continuous Monitoring & Sustainment (Ongoing)
**Artifacts:** Annual Affirmation, Updated SSP, Continuous Monitoring Reports, Training Records, Annual Risk Assessment

### Typical Timelines
| Starting SPRS | Timeline |
|---------------|----------|
| Below −100 | 18–24 months |
| −100 to 0 | 12–18 months |
| 0 to 50 | 9–12 months |
| 50+ | 6–9 months |

### Budget Range: $75K–$500K+ total program cost ($30K–$200K C3PAO fee alone)

---

## 6. SPRS Scoring

**Formula:** SPRS Score = 110 − Σ(value of all NOT MET requirements)

- Each of 110 controls weighted at **1, 3, or 5 points** (NIST FIPS 200 / NIST 800-53 R5)
- **Range: −203 to +110**
- −203 = all 110 NOT MET at their assigned weights (sum of deductions = 313)
- +110 = all 110 MET

### Score Tiers
| Score | Interpretation |
|-------|---------------|
| +110 | Perfect |
| +50 to +99 | Good |
| 0 to +49 | Moderate gaps |
| −50 to −1 | Poor |
| −100 to −51 | Very poor |
| Below −100 | Severe (foundational controls missing) |

---

## 7. Regulatory Stack

| Layer | Instrument | Enforces |
|-------|-----------|----------|
| 1 | FAR 52.204-21 | Baseline for all federal contractors (FCI) |
| 2 | DFARS 252.204-7012 | NIST 800-171 + 72-hr incident reporting + cloud FedRAMP |
| 3 | DFARS 252.204-7019/7020 | Self-assess, post SPRS score |
| 4 | DFARS 252.204-7021 (CMMC) | Independent third-party verification via C3PAO |
| Tech | NIST SP 800-171 Rev 2 | Made binding via DFARS |
| Assess | NIST SP 800-171A Rev 2 | Assessment procedures used by C3PAOs |

---

## Key Distinctions

- **SPRS score ≠ CMMC status.** SPRS score is a self-attested gap metric posted per DFARS 7020. CMMC L2(C3PAO) is an independent certification per DFARS 7021.
- **NIST 800-171 is not a regulation.** It's a NIST publication. DFARS makes it contractually binding.
- **CMMC keys on the information system, not the legal entity.** One Assessment Scope can cover multiple CAGE codes (§170.17(a)(1)(i)(E)).
- **CMMC does NOT consider FOCI.** Foreign-owned companies can get CMMC L2 certified. FOCI only gates Facility Security Clearance for classified work.
- **The word "enclave" does not appear in 32 CFR Part 170.** The regulation uses "information system," "CMMC Assessment Scope," and "OSA's environment."

---

*Sources: NIST SP 800-171 Rev 2, NIST SP 800-171A Rev 2, 32 CFR Part 170 (via Cornell LII), DFARS Final Rule (Sept 2025), cmmc-hub.com, cmmccommand.org, fieldledger.us, secureframe.com. Compiled July 2026.*