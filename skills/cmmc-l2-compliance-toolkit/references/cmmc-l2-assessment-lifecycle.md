# CMMC Level 2 Assessment Lifecycle — Condensed Regulatory Reference

Verified against 32 CFR Part 170 (via Cornell LII), DFARS Final Rule (Fed. Reg.
Sept 10, 2025, Doc 2025-18764, effective Nov 10, 2025), and NIST SP 800-171 Rev 2.
All citations are to the binding regulation unless noted "(guidance)" or "(industry)".
Market/cost data sourced from 2026 industry analysis.

Load this when answering: "how does the CMMC L2 assessment work," "what's the
certification lifecycle," "scoring methodology," "annual affirmation," "POA&M
closeout window," "recertification timeline," "Phase 2 deadline," "flow-down to
subcontractors," "Section 847 and CMMC," or "C3PAO engagement process."

## 1. Governing Regulatory Framework (Current as of 2026)

| Instrument | Status | Key Date |
|---|---|---|
| **32 CFR Part 170** (CMMC Program Rule) | Effective | Dec 16, 2024 |
| **DFARS CMMC Final Rule** (48 CFR Part 204) | Effective | Nov 10, 2025 |
| **DFARS Clause 252.204-7021** (CMMC Requirements) | Prescribed per §204.7504 | Phase-in Nov 10, 2025 – Nov 9, 2028 |
| **NIST SP 800-171 Rev 2** (110 controls) | Current for CMMC L2 | Per §170.14(c)(3) |
| NIST SP 800-171 Rev 3 (May 2024) | NOT mandatory for CMMC | Requires rule amendment (~2028+) |

§170.14(c)(3): "The security requirements in CMMC Level 2 are identical to the
requirements in **NIST SP 800-171 R2**." Rev 3 has no firm CMMC transition date.
Build to Rev 2 (110 controls); track Rev 3 deltas for future migration.

## 2. Phase-In Schedule (§170.3(e))

| Phase | Begins | What Triggers |
|---|---|---|
| **Phase 1** | Nov 10, 2025 (DFARS rule effective date) | L1(Self)/L2(Self) as award condition. DoD *may* include L2(C3PAO) at discretion. |
| **Phase 2** | ~Nov 10, 2026 (1 yr after Phase 1) | L2(C3PAO) becomes a **condition of contract award** for applicable solicitations. |
| **Phase 3** | ~Nov 2027 (1 yr after Phase 2) | L2(C3PAO) for ALL applicable contracts + option periods. L3(DIBCAC) for critical contracts. |
| **Phase 4** | ~Nov 2028 | Full implementation — CMMC in all applicable solicitations/contracts. |

DFARS clause prescription (§204.7504):
- Until Nov 9, 2028: Clause 252.204-7021 used at CO discretion during phase-in
- On/after Nov 10, 2028: Mandatory whenever systems process/store/transmit FCI or CUI

**Practical impact:** Phase 2 (~November 2026) is the hard deadline — L2(C3PAO)
cert must be posted in SPRS before contract award for applicable solicitations.

## 3. Assessment Types

- **L2(Self):** OSA self-assesses, posts score to SPRS (e.g., "105 out of 110").
  Self-assessment every 3 years to maintain compliance (§170.16).
- **L2(C3PAO):** Certified Third-Party Assessment Organization conducts formal
  assessment, posts results to CMMC eMASS → auto-transmits to SPRS. Valid 3 years.

## 4. C3PAO Assessment Lifecycle (§170.17)

**Step 1 — Engagement & Scoping:**
- Select a C3PAO from Cyber AB Marketplace (must be "Authorized," not "Candidate")
- C3PAO defines the CMMC Assessment Scope per §170.19
- C3PAO must be independent (no consulting relationship with the OSC)

**Step 2 — Assessment:**
- C3PAO evaluates all 110 NIST SP 800-171 Rev 2 requirements
- Each requirement objective scored: MET / NOT MET / N/A
- Scoring per §170.24 (see §5 below)

**Step 3 — Results Posting:**
- C3PAO posts results to CMMC eMASS → auto-transmits to SPRS
- eMASS record (§170.17(a)(1)(i)) includes: Date/level, C3PAO name, Assessment UID,
  Assessor names/contacts, **all CAGE codes** (plural), SSP name/date/version,
  CMMC Status Date, per-requirement results, POA&M status, artifact hashes

**Step 4 — Status Determination:**

| Status | Condition |
|---|---|
| **Conditional L2(C3PAO)** | Assessment has a POA&M meeting §170.21(a)(2) requirements |
| **Final L2(C3PAO)** | Passing score achieved (no unmet requirements, or POA&M closed out) |

## 5. Scoring Methodology (§170.24)

| Element | Rule |
|---|---|
| **Maximum score** | 110 (total L2 security requirements) |
| **Per-requirement value** | 1, 3, or 5 points (based on NIST designation: basic=5 from FIPS 200; derived=3/1 from NIST 800-53 R5) |
| **MET** | All objectives satisfied |
| **NOT MET** | One or more objectives unsatisfied; requirement value subtracted from max |
| **N/A** | Requirement doesn't apply (treated as MET for scoring) |
| **Negative scores** | Possible — if NOT MET values exceed remaining points |
| **POA&M at L2** | Allowed per §170.21; NOT all requirements are POA&M-eligible |

L1 has NO POA&M permitted — all requirements must be MET (§170.24(c)(1)).

## 6. POA&M Closeout (§170.17(a)(1)(ii)(B))

- If Conditional: POA&M items must be remediated within **180 days** of CMMC Status Date
- POA&M closeout certification assessment by C3PAO required
- C3PAO posts closeout results to eMASS within 180 days
- **Failure = Conditional status expires** → standard contractual remedies apply →
  ineligible for new L2(C3PAO)+ awards until new CMMC Status achieved

## 7. Validity Period & Recertification

- **L2(C3PAO) certification valid 3 years** from CMMC Status Date (§170.17)
- Recertification assessment by C3PAO required within 3 years
- Annual affirmation required every year (see §8 below)
- **DIBCAC override (§170.17(a)(1)(iv)):** DoD reserves right to conduct DCMA DIBCAC
  assessment at any time. If DIBCAC finds non-compliance, **DIBCAC results take
  precedence** over C3PAO status → contractual remedies + award ineligibility

## 8. Annual Affirmation (§170.22)

Required for ALL levels — both self-assessment and C3PAO certification.

| Trigger | When |
|---|---|
| Achievement of Conditional Status | At assessment |
| Achievement of Final Status | At assessment |
| **Annual affirmation** | Every year following Final Status Date |
| POA&M closeout | At closeout assessment |

**Affirming Official requirements:**
- Senior-level representative of the OSA with authority to affirm continuing compliance
- Submits electronically in SPRS
- Includes: name, title, contact info, affirmation statement
- **Both prime AND subcontractor** must affirm their own compliance (§170.22(a))
- DoD verifies affirmation in SPRS before contract award (§170.22(b))

**Failure to affirm = loss of "Current" status = contract remedy / award ineligibility.**

## 9. Subcontractor Flow-Down (§170.23)

CMMC applies to **primes and subcontractors at ALL tiers** processing/storing/
transmitting FCI or CUI.

| If subcontractor handles... | And prime requires... | Subcontractor minimum status |
|---|---|---|
| **FCI only** | (any) | **L1(Self)** |
| **CUI** | L2(Self) | **L2(Self)** |
| **CUI** | **L2(C3PAO)** | **L2(C3PAO)** |
| **CUI** | L3(DIBCAC) | **L2(C3PAO)** |

- Prime contractors **must flow down** CMMC requirements contractually (§170.23(a))
- Each subcontractor affirms its own compliance in SPRS
- Flow-down applies at every tier of the supply chain

## 10. Joint Ventures & Multiple Entities

### Multiple CAGE Codes — One Cert Covers Many
§170.17(a)(1)(i)(E) requires SPRS to list **"All industry CAGE codes associated
with the information systems addressed by the CMMC Assessment Scope"** — plural.
One Assessment Scope (one certified system/enclave) can cover multiple CAGE codes.
Identical plural language at §170.15(a)(1)(i)(D) [L1] and §170.16(a)(1)(i)(D) [L2 self].

### Joint Ventures
The DFARS CMMC Final Rule (Sept 2025) confirms CMMC applies to joint ventures,
including mentor-protégé JVs. Per Arnold Porter analysis of the rule: *"Each
individual entity that has a requirement for CMMC would be required to comply with
the requirements related to the individual entity's information systems."*

**Practical rule:** If the JV has its own CAGE code and systems processing CUI,
that boundary must be certified. JV partners' separate systems need separate
certification if they touch CUI independently.

### Foreign Entities Sharing One Enclave
- Permitted — CMMC keys on systems + CAGE codes, not legal-entity boundaries
- Foreign ownership is NOT a CMMC bar (but triggers FOCI/ITAR review separately)
- Assessors may examine foreign-national access under AC/IA controls

## 11. Section 847 (FY2020 NDAA) Interaction with CMMC

**What Section 847 is:** Requires DoD to improve risk assessment and mitigation of
**Foreign Ownership, Control, or Influence (FOCI)** of contractors/subcontractors.
Requires beneficial ownership disclosure and foreign control assessment.

**Relationship to CMMC:**
- Section 847 governs FOCI risk — **separate from CMMC**, which governs cybersecurity maturity
- Does NOT affect CMMC level determination or assessment
- A company can be CMMC L2 certified regardless of FOCI status
- FOCI mitigation (if required for Facility Security Clearance) runs in parallel
- For JVs with foreign partners: Section 847 disclosure may be required; CMMC still
  applies to the JV's CUI systems

**Key distinction:** FOCI only gates Facility Security Clearance (FCL) for classified
work. CMMC is unclassified cybersecurity and does not consider FOCI.

## 12. C3PAO Market & Cost (2026 Industry Data)

### Accredited C3PAO Count
- **60+ C3PAOs authorized** as of April 2026 (CMMC Ready Now intelligence report)
- Listed on Cyber AB Marketplace (cyberab.org/marketplace)
- Statuses: "Authorized" (can assess) vs. "Candidate" (in process, cannot assess)
- ⚠️ CyberAB.org blocks automated access — count requires manual browser verification

### Assessment Cost (2026 ranges, industry)
| Component | Range |
|---|---|
| C3PAO assessment fee | $30K – $200K+ (varies by org size/scope) |
| Total L2 program cost | $75K – $500K+ (incl. remediation, tooling, consulting) |
| Ongoing annual maintenance | $20K – $75K/year |

**Cost drivers:** scope size (asset count), CUI complexity, remediation backlog,
consulting support, evidence collection maturity.

⚠️ These ranges are from industry analysis (Cabrilloclub, PolicyCortex, C3PAO cost
guides), not DoD-published figures. Verify with actual C3PAO quotes.

## 13. Reciprocity & Scope Expansion

### Certification Portability
- CMMC certification is **system/scope-specific, NOT contract-specific**
- A cert carries across ALL contracts using the same certified information system
- DFARS 252.204-7021(c): *"CMMC assessments will not duplicate efforts from any
  other comparable DoD assessment."*
- Contracting officers verify by CMMC UID in SPRS (DFARS 204.7503)
- §170.17(a): L2(C3PAO) "also satisfies...Level 1 (Self) and Level 2 (Self) for
  the same CMMC Assessment Scope."

### Scope Expansion (Adding CAGE Codes/Business Units)
- Adding systems/CAGEs to a certified environment = **material scope change**
- "Current" status requires "no changes in compliance" since Status Date (DFARS 204.7501)
- **Process:** Update SSP → update Assessment Scope → C3PAO delta/supplemental
  assessment → C3PAO posts updated results to eMASS → SPRS with expanded CAGE list
- Unassessed expansion likely invalidates "Current" status

### Acquisitions/Mergers
- Cert attaches to the information system + Assessment Scope, not the corporate entity
- If systems remain operationally unchanged, cert MAY remain valid
- New parent becomes OSA, assumes annual affirmation obligations (§170.22)
- Material architecture/personnel/policy change = reassessment typically required

## Research Technique — Extracting Cornell LII Text

Cornell LII (`law.cornell.edu/cfr/text/32/170.NN`) reliably serves 32 CFR Part 170
content, unlike eCFR/Federal Register which block bots. However, the page is
partially JS-rendered and the raw HTML has heavy metadata/schema in the first
~5000-10000 characters before the actual regulatory text appears.

**Working extraction pattern (Python via terminal):**
```bash
curl -sL "https://www.law.cornell.edu/cfr/text/32/170.17" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
# Regulatory text appears AFTER the JSON-LD schema block (~5000+ chars in)
# Search for a known regulatory marker to skip metadata
for marker in ['(a) General', 'The Level 2', 'CMMC Level', 'three years']:
    idx = text.find(marker)
    if idx > 5000:  # skip metadata section
        print(text[idx:idx+3000])
        break
"
```

**Key insight:** The threshold `> 5000` (or `> 7000` for some sections) filters
out the breadcrumb/schema/metadata matches and lands on the actual CFR body text.
Without this threshold, the marker matches the page title/metadata and returns
JSON-LD garbage instead of regulation text.

**Sections verified accessible via this method (July 2026):**
§170.3 (phase-in), §170.4 (definitions), §170.14 (CMMC model/levels),
§170.16 (L2 self-assessment), §170.17 (L2 C3PAO assessment), §170.22 (affirmation),
§170.23 (subcontractors), §170.24 (scoring).
