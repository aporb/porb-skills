# LFC OORAH — Full Worked Example

The complete proprietary methodology designed for Leatherneck Federal Consulting. This is the canonical reference for what a finished framework looks like — use it as a template when designing new frameworks for other firms, swapping domain, name, and phase content.

## Framework Identity

- **Name:** LFC OORAH Framework
- **Domain:** CMMC L2 / NIST 800-171 gap-to-audit compliance for defense contractors
- **Identity anchor:** "Oorah" — Marine Corps battle cry (the firm is Marine-veteran-led)
- **Tagline:** "From gap assessment to audit-ready. Oorah."
- **Trademark status:** Pending (not yet filed; footer says "(pending)")

## Acrostic

| Letter | Phase | Headline |
|---|---|---|
| **O** | ORIENT | Scope & Baseline |
| **O** | ORGANIZE | Plan & Architect |
| **R** | REMEDIATE | Implement & Document |
| **A** | ASSESS | Validate & Rehearse |
| **H** | HOLD | Certify & Sustain |

## Phase Details

### 01 — ORIENT: Scope & Baseline

**Objective:** Define the assessment boundary and establish an honest, evidence-based baseline before a single dollar is spent on remediation. Most failed assessments are lost here — to over-scoped enclaves and undocumented CUI flows.

**Key Activities:**
- CUI scoping & assessment-boundary determination (per CMMC L2 Scoping Guide)
- CUI data-flow mapping — entry, processing, storage, transmission, destruction
- Asset & External Service Provider (ESP/CSP) inventory
- Gap assessment against all 110 NIST SP 800-171 controls using 800-171A assessment objectives
- SPRS baseline score calculation (the −203 to +110 DoD scoring methodology)

**Deliverables:** Scope Determination, CUI Data-Flow Register, Asset/ESP inventory, Gap Assessment report (800-171A-referenced), SPRS baseline score

**Outcome:** A defensible scope, a true SPRS baseline, and a prioritized gap register — no surprises downstream.

### 02 — ORGANIZE: Plan & Architect

**Objective:** Turn the gap register into a costed, sequenced remediation program and an enclave architecture sized to your operation — not a template. This is where compliance becomes a project with an owner, a budget, and a date.

**Key Activities:**
- POA&M construction — severity, owner, due date, remediation plan per open control
- Remediation roadmap & milestone sequencing (cost + timeline)
- Enclave architecture design (GCC High / on-prem / hybrid) & shared-responsibility allocation
- SSP skeleton — system description, boundary, and control narrative structure
- Control Implementation Matrix baseline

**Deliverables:** POA&M (live tracker), Remediation roadmap with cost & schedule, Enclave architecture & Shared-Responsibility Matrix, SSP skeleton + Control Implementation Matrix

**Outcome:** A funded, scheduled remediation program and an enclave design that closes gaps by construction.

### 03 — REMEDIATE: Implement & Document

**Objective:** Execute the POA&M — implement controls and write the documentation that proves them. The single most common Day-1 failure is a structurally perfect SSP with zero implemented, documented controls.

**Key Activities:**
- Control implementation across all 14 families (AC, AT, AU, CM, IA, IR, MA, MP, PS, PE, RA, CA, SC, SI)
- Policy & SOP authoring per control family
- SSP section-by-section control implementation narratives (no placeholders)
- Evidence collection mapped to each control (Evidence Collection Matrix)
- POA&M burn-down and SPRS score uplift tracking

**Deliverables:** Completed SSP (all 110 control narratives), 14 control-family SOPs, Evidence repository (control-mapped), POA&M closed to assessable threshold (≥88/110, no open 3- or 5-point items >180 days), Updated SPRS score

**Outcome:** An implemented, documented, evidence-backed posture — the difference between a blank template and an assessable system.

### 04 — ASSESS: Validate & Rehearse

**Objective:** Prove readiness before the C3PAO does. A mock assessment against the official CMMC Assessment Process (CAP) finds the gaps your team can't see — while there's still time and budget to fix them.

**Key Activities:**
- Mock assessment / readiness review against the CMMC CAP (Level 2 v2.13)
- Evidence walk-through & artifact validation
- Tabletop exercises (incident response, insider threat)
- Residual POA&M adjudication — confirm each open item is POA&M-eligible
- Pre-assessment package assembly (SSP, POA&M, evidence index)

**Deliverables:** Readiness / mock-assessment report (findings + corrective actions), Corrective Action Program closure evidence, Tabletop exercise records, C3PAO-ready pre-assessment package

**Outcome:** Confidence — and the evidence — that the system will survive a C3PAO assessment on the first attempt.

### 05 — HOLD: Certify & Sustain

**Objective:** Pass the assessment and hold the objective. Certification is a milestone, not the finish line — CMMC is a continuous obligation with annual affirmations, SPRS upkeep, and POA&M discipline.

**Key Activities:**
- C3PAO assessment support (kickoff, evidence presentation, assessor Q&A)
- Findings response & limited POA&M closeout (180-day window)
- Certification & SPRS final reporting
- Annual affirmation & continuous-monitoring program
- Change control, periodic reassessment, and sustainment

**Deliverables:** Assessment-day support & findings responses, CMMC L2 certification (via C3PAO), Annual affirmation package (per 32 CFR §170.22), Continuous-monitoring / ConMon plan

**Outcome:** CMMC Level 2 certification — and a compliance posture that holds up year after year, not just on assessment day.

## Authoritative Source Grounding

| Source | Role in the Framework |
|---|---|
| NIST SP 800-171 Rev 2/3 | 110 controls, 14 families — the substance of Level 2 |
| NIST SP 800-171A | Assessment objectives & procedures the C3PAO actually uses |
| 32 CFR Part 170 | The CMMC Program final rule — levels, assessment, affirmation |
| DFARS 252.204-7019/7020/7021 | The contract clauses that make CMMC mandatory |
| CMMC CAP & Scoping Guide v2.13 | How the assessment is conducted and what's in scope |
| SPRS scoring (−203 → +110) | The DoD's own supplier-risk scoring methodology |

## Site Integration

**Shared data module:** `src/lib/oorah.ts` — exports typed `OorahPhase[]`, tagline, name constants, and grounding array. Imported by both the `/` landing teaser and the `/oorah` dedicated methodology page.

**Landing teaser (`/`):** Letter-tile strip (O-O-R-A-H) → info bar with phase run-on → "EXPLORE THE FRAMEWORK →" CTA to `/oorah`.

**Dedicated page (`/oorah`):** Hero with letter links → "Why OORAH" positioning → grounding strip → five full phase-detail cards with activities/deliverables/outcome callouts → "Request an OORAH Assessment" CTA.

**Silent-partner note:** One partner's AI/technology capability was folded into the firm's aggregate service offerings ("Secure Technology & AI Enablement") and a leadership pillar ("Secure Technology & AI") rather than attributed to a named individual. The framework belongs to the firm, not any single person.
