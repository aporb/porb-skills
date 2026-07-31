---
name: cmmc-l2-compliance-toolkit
description: Build a complete CMMC Level 2 compliance toolkit for federal contractors — reference documents, templates, SOPs per NIST SP 800-171 control family, evidence collection matrices, and operational procedures. Covers the full build pattern from research through gap analysis, parallel agent orchestration, and Nextcloud HTML briefing publication.
---

# CMMC L2 Compliance Toolkit

Build a complete CMMC Level 2 compliance toolkit for federal contractors — reference documents, templates, SOPs per NIST SP 800-171 control family, evidence collection matrices, and operational procedures. Covers the full build pattern from research through gap analysis, parallel agent orchestration, and Nextcloud HTML briefing publication.

## When to Use This Skill

Use this skill when:
- Building a CMMC L2 compliance toolkit from scratch for a federal contractor
- Creating SOPs, SSP templates, POA&M trackers, and evidence collection matrices
- Extracting the 110 NIST SP 800-171 Rev 2 controls programmatically
- Researching NIST SP 800-171 Rev 2 vs Rev 3 transition and its impact on CMMC L2
- Understanding CMMC L2 assessment requirements (currently Rev 2, not Rev 3)
- Determining recertification timelines and Rev 3 transition strategy
- Identifying new controls in Rev 3 that are NOT in Rev 2 (e.g., Supply Chain Risk Management, Planning, System and Services Acquisition)
- Researching C3PAO market and SPRS scoring methodology
- Orchestrating parallel build agents for distinct deliverables
- Conducting gap analysis and data integrity fixes on CSV/JSON data
- Publishing compliance briefings as self-contained HTML to Nextcloud
- Building a CMMC certification timeline PPTX deck for executive leadership — a 10-slide business-focused presentation covering current readiness, 7-phase Gantt timeline, Phase 2 deadline impact, acceleration opportunities, BD lead-time reference, and decisions required. Load references/cmmc-timeline-pptx-executive-deck-pattern.md for the deck structure, Midnight Executive palette, pptxgenjs Gantt gotchas, and the pre-build research workflow (review call recordings for executive context).
- Conducting gap analysis on bare-metal GPU infrastructure (Vast.ai/Lambda/RunPod) for CMMC L2 — load `references/vast-ai-gpu-cmmc-analysis.md` for the full 110-control gap mapping
- Building meeting-tasker deliverables from screenshots (meeting images → DOR matrices,
  timelines, compliance gate briefings) — see the "Meeting Tasker Deliverables" section below
  and load `references/meeting-tasker-deliverable-pattern.md` for the full workflow
- Answering SSP classification / legal-liability questions (Is the SSP CUI or CDI? Does it have
  to stay in the enclave? Liability if on commercial SharePoint? How do DIBCAC/C3PAOs access
  it?) — load `references/ssp-classification-and-assessment-access.md` for the full analysis
- Researching or defining federal laptop/endpoint hardware compliance standards across CMMC L2, NIST 800-171, DOD IL-4/IL-5, DISA STIGs, FedRAMP, and federal sustainability (EPEAT/Energy Star) — load `references/federal-laptop-hardware-compliance.md` for the condensed framework crosswalk, minimum hardware spec, recommended models, and deployment stack
- Researching or explaining the CMMC L2 assessment lifecycle and certification process
  (phase-in schedule, C3PAO engagement, scoring methodology, POA&M closeout, annual
  affirmation, recertification, subcontractor flow-down, Section 847/FOCI, C3PAO market) —
  load `references/cmmc-l2-assessment-lifecycle.md` for the condensed regulatory reference
- Researching the full CMMC/NIST 800-171 compliance methodology end-to-end — control families,
  assessment procedures, CMMC 2.0 model, SSP/POA&M structure, consultant lifecycle phases and
  artifacts, SPRS scoring methodology — load
  `references/cmmc-methodology-end-to-end-research.md` for the authoritative synthesis
- Defining Division of Responsibility (DOR) or RACI matrices between the contractor, JV
  partners, subcontractors, C3PAO, MSPs/MSSPs, and ESPs/CSPs — or researching how
  FOCI-mitigated entities (BAE Systems, Rolls-Royce model) structure compliance governance
  and the DFARS 7012/7020/7021 flow-down chain — load
  `references/cmmc-dor-raci-framework.md` for the full framework with verified regulatory
  citations, RACI matrix structure, and non-delegable responsibilities
- Researching what Microsoft tools and features are actually available in GCC High
  environments — Copilot timelines, Power Platform restrictions, Teams limitations, Fabric
  availability, and feature parity gaps versus commercial M365 — load the
  `m365-gcc-high-capability-research` skill for the full research methodology, source URLs,
  and pitfalls (complementary: use this before designing compliance workflows in GCC High)
- Researching or designing SharePoint Online / Teams / Power Automate / Purview compliance
  workflow architecture for a GCC High enclave (access requests, clearance verification,
  NDA recertification, audit trails) — load
  `references/m365-gcc-high-compliance-workflow-guide.md` for the condensed architecture
  reference covering three-list SharePoint schema, Power Automate sequential approval
  patterns, Forms vs Power Apps availability, Purview container-level labeling, Teams
  channel integration, multi-layer C3PAO audit strategy, and GCC High limitations matrix
- Researching the competitive landscape for a CMMC compliance product — pricing, features,\n  positioning of FutureFeed, PreVeil, and other commercial platforms — load\n  `references/cmmc-competitive-landscape-2026.md` for the full July 2026 competitive\n  analysis including pricing benchmarks, feature comparisons, GCC High vs lightweight\n  alternatives, and the Phase II suspension market window.\n- Researching the CMMC L2 self-assessment enablement competitive landscape specifically\n  targeting micro-businesses (1-10 employee federal contractors) — who sells compliance\n  packages, pricing, what's included, TAM size from SBA/SAM.gov data, Phase II suspension\n  impact on competitive dynamics, and underserved market gaps — load\n  `references/cmmc-l2-competitive-landscape-2026-07.md` for the condensed analysis\n  covering 6 competitors, TAM estimates, suspension impact, and strategic recommendations.

## CMMC L2 Compliance Toolkit Structure

```
compliance-toolkit/
├── reference-docs/              # Authoritative source documents
│   ├── NIST-SP-800-171-Rev2.pdf                    # The 110 controls (baseline)
│   ├── NIST-SP-800-171A-Rev2.pdf                   # Assessment procedures
│   ├── FAR-Complete.pdf                            # FAR Part 52.204-21
│   ├── 32-CFR-Part-170-CMMC-Final-Rule.html        # CMMC 2.0 regulation
│   ├── DFARS-HTML-Complete.zip                     # Full DFARS archive
│   ├── dfars-key-clauses/                          # Extracted CMMC/CDI clauses
│   └── [future: ScopingGuideL2v2.pdf, CAP-Level2.pdf]  # ⚠️ Manual download required
│
│├── templates/                   # Working templates (11 → 32 after mock assessment build)
│   ├── SSP-Template.md                           # System Security Plan (110 controls)
│   ├── POAM-Tracker.csv                          # Plan of Action & Milestones
│   ├── Control-Implementation-Matrix.csv         # 110 controls × status × evidence
│   ├── Cybersecurity-Program-Checklist.csv       # Monthly/annual procedures
│   ├── Asset-Inventory-Template.csv              # Hardware/software inventory
│   ├── Risk-Register-Template.csv                # Risk tracking
│   ├── Incident-Response-Plan.md                 # IR plan per NIST SP 800-61
│   ├── CMMC-L2-Scope-Determination.md            # Scope definition template
│   ├── Evidence-Collection-Matrix.csv            # What evidence proves each control
│   ├── CUI-Data-Flow-Register.md                 # Entry points, processing, storage, transmission, destruction
│   ├── TAA-Section889-Pre-Purchase-Checklist.md  # TAA, Section 889, prohibited vendors
│   │
│   ├── [Tech Config] GCC-High-Tenant-Baseline.md
│   ├── [Tech Config] AVD-Session-Host-Configuration-Baseline.md
│   ├── [Tech Config] Intune-Device-Compliance-Policy.md
│   ├── [Tech Config] FIPS-Cryptography-Validation-Register.md
│   ├── [Tech Config] Purview-DLP-Policy-Baseline.md
│   ├── [Tech Config] Conditional-Access-Policy-Register.md
│   ├── [Tech Config] Network-Segmentation-and-Tenant-Isolation.md
│   │
│   ├── [Governance] Annual-Affirmation-Template.md
│   ├── [Governance] Shared-Responsibility-Matrix.csv
│   ├── [Governance] ESP-CSP-Inventory.md
│   ├── [Governance] Subcontractor-CMMC-Flow-Down-Tracker.csv
│   ├── [Governance] Insider-Threat-Program.md
│   ├── [Governance] Tabletop-Exercise-Scenarios.md
│   ├── [Governance] Risk-Assessment-Methodology.md
│   ├── [Governance] Physical-Security-Plan.md
│   │
│   ├── [Built] Security-Awareness-Training-Curriculum.md
│   ├── [Built] Cryptographic-Key-Management-Plan.md
│   ├── [Built] CAB-Charter.md
│   ├── [Built] Vendor-Security-Questionnaire.md
│   ├── [Built] Evidence-Collection-Guide-GCC-High.md
│   ├── [Built] USB-Printer-Compensating-Control.md
│
├── control-families/            # One folder per NIST 800-171 family
│   ├── 0100-AC-Access-Control/              # 22 controls
│   │   └── CS-AC-0100.SOP.md
│   ├── 0200-AT-Awareness-Training/          # 3 controls
│   │   └── CS-AT-0200.SOP.md
│   ├── 0300-AU-Audit-Accountability/        # 9 controls
│   │   └── CS-AU-0300.SOP.md
│   ├── 0400-CM-Configuration-Management/    # 9 controls
│   │   └── CS-CM-0400.SOP.md
│   ├── 0500-IA-Identification-Authentication/# 11 controls
│   │   └── CS-IA-0500.SOP.md
│   ├── 0600-IR-Incident-Response/            # 3 controls
│   │   └── CS-IR-0600.SOP.md
│   ├── 0700-MA-Maintenance/                   # 6 controls
│   │   └── CS-MA-0700.SOP.md
│   ├── 0800-MP-Media-Protection/             # 9 controls
│   │   └── CS-MP-0800.SOP.md
│   ├── 0900-PS-Personnel-Security/            # 2 controls
│   │   └── CS-PS-0900.SOP.md
│   ├── 1000-PE-Physical-Protection/          # 6 controls
│   │   └── CS-PE-1000.SOP.md
│   ├── 1100-RA-Risk-Assessment/              # 3 controls
│   │   └── CS-RA-1100.SOP.md
│   ├── 1200-CA-Security-Assessment/          # 4 controls
│   │   └── CS-CA-1200.SOP.md
│   ├── 1300-SC-System-Communications-Protection/# 16 controls
│   │   └── CS-SC-1300.SOP.md
│   └── 1400-SI-System-Information-Integrity/ # 7 controls
│       └── CS-SI-1400.SOP.md
│
├── BUILD-PLAN.md               # Build documentation
├── GAP-ANALYSIS.md             # Build gaps, manual downloads, fixes
├── README.md                   # Full usage guide
├── Control-to-Document-Mapping.md  # All 110 controls mapped to SOP/evidence/data flow
└── nist_800_171_controls.json   # All 110 controls extracted programmatically
```

## Build Process

### 1. Research and Plan

**Set up a todo list for the full build:**
- RESEARCH: Find exact download URLs for all CMMC/NIST/DFARS source documents
- PLAN: Write detailed implementation plan for the compliance toolkit
- DOWNLOAD: Fetch all reference PDFs
- BUILD: Directory structure — all 14 control families
- BUILD: SSP template mapped to 110 controls
- BUILD: POA&M tracker template
- BUILD: SOP templates for each control family (14 families)
- BUILD: Cybersecurity Program Checklist (improved from existing version)
- BUILD: Evidence collection templates + scoping document template
- BUILD: Asset inventory, risk register, incident response plan templates
- GAP ANALYSIS: Compare built toolkit against plan — identify and fix gaps
- SUMMARIZE: Create HTML briefing and publish to Nextcloud

**Write the plan document (`BUILD-PLAN.md`):**
- Objective statement
- Deliverables list
- Directory structure
- Naming conventions (align with organizational conventions)
- Roles and responsibilities
- Timeline and milestones

### 1.5. Comprehensive Verification Workflow (User-Required)

The user expects a multi-verification workflow for ALL deliverables:

1. **Full audit against requirements** — Verify each document meets the requirements criteria
2. **Generate detailed remediation plan** — Write `REMEDIATION-PLAN.md` documenting all gaps
3. **Dispatch parallel fix agents** — Use `delegate_task` with `tasks=` for parallel workstreams
4. **Dispatch reviewer agent** — Audit the fixed work against the requirement criteria
5. **Second fix pass** — Address any gaps found by the reviewer
6. **Final review** — Check everything one last time, fix any minor issues, report complete

**Verification audit approach:**
- For SOPs: Check for required sections (Document Control, Purpose, Scope, References, Roles, Controls Covered, Procedures, Evidence Collection, Revision History, Exceptions, Review and Maintenance)
- For CSVs: Check row counts, header presence, control ID format
- For templates: Verify bracketed placeholders and required subsections
- Run `execute_code` with grep/awk for structured verification
- Write `REMEDIATION-PLAN.md` with specific file paths and required fixes

### 2. Download Reference Documents

**Download programmatically (where possible):**
- NIST SP 800-171 Rev 2: `curl -sL https://csrc.nist.gov/pubs/sp/800-171/rev/2/final`
- NIST SP 800-171A Rev 2: `curl -sL https://csrc.nist.gov/pubs/sp/800-171a/rev/2/final`
- 32 CFR Part 170: **eCFR and Federal Register BLOCK automated access** (return a "Request
  Access" page; the local `32-CFR-Part-170-CMMC-Final-Rule.html` captured by the command
  below is that blocked page, NOT the real regulation). Use **Cornell LII**, which mirrors
  the official eCFR text and is curl-accessible: `curl -sL "https://www.law.cornell.edu/cfr/text/32/170.NN"`
  for any section (e.g., 170.3, 170.4, 170.14–170.19, 170.23). Fetch per-section; the part
  index is at `https://www.law.cornell.edu/cfr/text/32/part-170`. Do NOT use the
  `https://www.ecfr.gov/current/...` URL.
- FAR Complete: `curl -sL -o FAR-Complete.pdf https://www.acquisition.gov/far/part-52#subpart-52.2` (extract 52.204-21)
- DFARS Complete: `curl -sL -o DFARS-HTML-Complete.zip https://www.ecfr.gov/current/title-48/subtitle-A/chapter-2/subchapter-I/part-252?download=zip`

**Extract DFARS key clauses:**
- Unzip DFARS archive to `dfars-extracted/dita_html/`
- Copy standalone HTML files for:
  - `DFARS-252.204-7012-Safeguarding-CDI.html`
  - `DFARS-252.204-7019-NIST-800-171-Requirements.html`
  - `DFARS-252.204-7020-DoD-Assessment-Requirements.html`
  - `DFARS-252.204-7021-CMMC-Requirements.html`
  - `DFARS-252.204-7008-Compliance-with-CDI-Controls.html`
  - `DFARS-252.204-7009-Limitations-CUI.html`
  - `DFARS-252.204-7014-Procedures-Safeguarding-CDI.html`

**Manual downloads required (DoD CIO blocks bots):**
- CMMC L2 Scoping Guide v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/ScopingGuideL2v2.pdf`
- CAP Level 2 v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/CAP-Level2-Version-2-13.pdf`
- Document this in `GAP-ANALYSIS.md` as a manual action item

### 3. Extract the 110 Controls

**⚠️ The old extraction method produces truncated text.** The original `scripts/nist-controls-extraction.py` extracts from the PDF table of contents, which only has the first sentence of each control. For the FULL control text (needed for SSP and Control Implementation Matrix), use the method in `references/nist-control-text-extraction.md`.

**For NIST SP 800-171 Rev 2 (PDF):** Use `pdftotext -raw` with a DISCUSSION-header stop condition (see reference file).

**For NIST SP 800-171 Rev 3 (HTML, May 2024):** The HTML version at `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html` is browser-accessible. Use `browser_console` with JavaScript to extract specific control requirements by heading ID — this is faster than PDF extraction and gives you the exact control text with DISCUSSION and REFERENCES sections. Pattern:
```javascript
const sections = ['03.13.11', '03.05.02']; // desired control IDs
sections.forEach(id => {
  const h3 = Array.from(document.querySelectorAll('h3')).find(h => h.textContent.includes(id));
  if (h3) {
    let content = ''; let el = h3.nextElementSibling; let count = 0;
    while (el && !['H3','H2'].includes(el.tagName) && count < 20) {
      content += el.textContent.trim() + '\n';
      el = el.nextElementSibling; count++;
    }
    console.log(id + ': ' + content.substring(0, 2000));
  }
});
```
See the "Government Website Blocking for Research" pitfall (Resolution item 6) for the full technique.

**Use `pdftotext -raw` with a DISCUSSION-header stop condition:**

```bash
cd compliance-toolkit
pdftotext -raw reference-docs/NIST-SP-800-171-Rev2.pdf -
```

Then parse with the Python script pattern in the reference file. This captures complete control text including trailing phrases like "devices (including other systems)" that the TOC-only method misses.

**Verification:**
```python
# Should end with a full phrase, not be cut off mid-sentence
"3.1.1: Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems)."
```

**Reference:** See `references/nist-control-text-extraction.md` for the full extraction script and verification steps.
```bash
cd compliance-toolkit
python3 references/nist-controls-extraction.py
```

This extracts all `3.x.x` controls from NIST SP 800-171 Rev 2 PDF and saves to `nist_800_171_controls.json`.

**Verify extraction:**
```bash
python3 -c "
import json
with open('nist_800_171_controls.json', 'r') as f:
    data = json.load(f)
print(f'Total controls: {data[\"total\"]}')
print(f'Families: {len(data[\"families\"])}')
"
```

Should output: `Total controls: 110, Families: 14`.

### 4. Build Directory Structure

```bash
mkdir -p compliance-toolkit/{reference-docs,templates,control-families}
for family in 0100-AC-Access-Control 0200-AT-Awareness-Training 0300-AU-Audit-Accountability 0400-CM-Configuration-Management 0500-IA-Identification-Authentication 0600-IR-Incident-Response 0700-MA-Maintenance 0800-MP-Media-Protection 0900-PS-Personnel-Security 1000-PE-Physical-Protection 1100-RA-Risk-Assessment 1200-CA-Security-Assessment 1300-SC-System-Communications-Protection 1400-SI-System-Information-Integrity; do
  mkdir -p "compliance-toolkit/control-families/$family"
done
```

### 5. Build Templates

**SSP Template:**
- Pre-structure with all 110 controls in Section 5
- Use the control IDs and text from `nist_800_171_controls.json`
- Include columns for: Implementation Description, Responsible Role, Evidence Artifact, Last Assessed Date, Next Assessment Date

**POA&M Tracker CSV:**
- Use the script `scripts/generate_poam_tracker.py` (or build inline with execute_code)
- Columns: POAM_ID, Control_ID, Finding_Description, Severity, Discovery_Date, Owner, Due_Date, Remediation_Plan, Status, Evidence_Artifact, Last_Updated
- Pre-populate with 110 rows, one per control

**Control Implementation Matrix CSV:**
- Use the script `scripts/generate_control_matrix.py` (or build inline with execute_code)
- Columns: Control_ID, Control_Family, Control_Text, Implementation_Status, Responsible_Role, Implementation_Description, Evidence_Artifact, Last_Assessed_Date, Next_Assessment_Date
- Pre-populate with 110 rows

**Other templates:**
- Asset Inventory Template CSV
- Risk Register Template CSV
- Incident Response Plan MD (per NIST SP 800-61, include 72-hour DFARS 252.204-7012 reporting)
- CMMC L2 Scope Determination MD
- Evidence Collection Matrix CSV (map all 14 families to evidence types)
- CUI Data Flow Register MD
- TAA & Section 889 Pre-Purchase Checklist MD

### 6. Build Control Family SOPs

**Use parallel agent orchestration:**
- Dispatch 1-3 agents to build SOPs in parallel
- Each agent gets a specific subset of control families
- Provide context: company name, CAGE code, platform (GCC High, AVD, InEight, Box.com), roles, locations
- Provide the controls JSON path for accurate control text extraction

**SOP structure (per family):**
1. Document Control table (Document ID, Version, Effective Date, Last Reviewed, Next Review Date, Owner, Approved By)
2. Purpose — what the SOP accomplishes and why it matters for CMMC L2
3. Scope — systems, personnel, and processes covered
4. References — NIST 800-171 section, CMMC 2.0, organizational policies
5. Roles and Responsibilities — at least: Sr Cybersecurity Analyst, Sr Manager Security GRC, Federal Compliance Project Director
6. Procedures — numbered, actionable steps for implementing each control in the family
7. Exceptions and Variance
8. Review and Maintenance
9. Change Log

**Naming convention:**
- Align with organizational conventions (e.g., `CS-[FAMILY]-####.SOP.md`)
- Use folder naming: `####-[FAMILY]-[Full Name]/`

### 7. Gap Analysis and Data Integrity Fixes

**Always verify:**
- CSV row counts: POAM Tracker and Control Matrix should have 111 lines (header + 110 controls)
- Control IDs in CSVs should match `3.x.x` format, not truncated or corrupted
- All 14 SOP files exist in their respective folders

**Fix CSV data integrity:**
If CSV files have wrong control IDs or wrong row counts, rebuild programmatically from `nist_800_171_controls.json`:
```python
import json
with open('nist_800_171_controls.json', 'r') as f:
    data = json.load(f)

family_codes = {...}  # Map 3.x to family name

# Rebuild POAM Tracker
poam_lines = ['POAM_ID,Control_ID,Finding_Description,Severity,Discovery_Date,Owner,Due_Date,Remediation_Plan,Status,Evidence_Artifact,Last_Updated']
poam_idx = 1
for family, controls in data['families'].items():
    for control in controls:
        poam_lines.append(f'POAM-{poam_idx:03d},{control["id"]},,,Open,,,Incomplete,,')
        poam_idx += 1

with open('templates/POAM-Tracker.csv', 'w') as f:
    f.write('\n'.join(poam_lines))
```

**Document gaps:**
- Write `GAP-ANALYSIS.md` documenting:
  - Planned vs actual deliverables
  - Gaps requiring manual action (DoD CIO downloads)
  - Gaps fixed during build (CSV data integrity)
  - Gaps in progress (missing SOPs)
  - Optional enhancements not in original plan

### 8. Publish HTML Briefing to Nextcloud

**Build self-contained HTML briefing:**
- Use Thariq/html-effectiveness aesthetic (ivory #FAF9F5, clay #D97757, slate #141413)
- Include: executive summary, deliverables list, directory structure, usage guide, gaps, next steps
- Self-contained (no external CSS/JS)

**Save and scan:**
```bash
# Write to briefings directory
cat > /data/nextcloud/data/amyn/files/briefings/[filename].html << 'EOF'
[HTML content]
EOF

# Scan with Nextcloud
sg www-data -c "docker exec --user www-data nextcloud php occ files:scan --path='/amyn/files/briefings/[filename].html'"
```

**URL pattern:** `https://brief.h.porb.dev/[filename].html`

## User-Required Verification Workflow

The user requires a multi-verification workflow for ALL deliverables:

1. **Full audit against requirements** — Verify each document meets the requirements criteria
2. **Generate detailed remediation plan** — Write `REMEDIATION-PLAN.md` documenting all gaps
3. **Dispatch parallel fix agents** — Use `delegate_task` with `tasks=` for parallel workstreams
4. **Dispatch reviewer agent** — Audit the fixed work against the requirement criteria
5. **Second fix pass** — Address any gaps found by the reviewer
6. **Final review by the orchestrator (you), not another agent** — The orchestrator is the last gate. Run verification commands directly, fix any minor issues inline, and only declare complete after personal inspection. The user's exact words: "you do the final review and any minor fixes or anything else that's left."

Do not shortcut verification. Do not declare work complete without this full workflow. The orchestrator must personally run the final verification pass — delegating the final review to another agent is not acceptable.

## Structured QA Review (Review-Only Mode)

When asked to perform a **QA review** (as opposed to the build+verify workflow above), the user
wants a **structured pass/fail report with specific gaps, file paths, and what's missing** —
typically with an explicit "DO NOT modify any files" constraint. This is a read-only audit class
of work. Use the reusable verification script `scripts/qa-review-toolkit.sh` to run the full
audit in one shot, then translate raw output into a structured report.

### Review Deliverable Format

A QA review should produce a report with:
- **Per-criterion PASS/FAIL** with evidence (counts, line numbers)
- **Specific gaps** with exact file path and what's missing
- **Overall verdict**: READY FOR COMMIT or GAPS FOUND
- A **gaps summary table** at the end (#, severity, file, issue, fix)

### What to Check (Full Audit Matrix)

Beyond the build-time CSV/SOP checks below, a thorough review should verify:

**SOPs (14 files):** Each has all 7 Document Control fields (Document ID, Version, Effective Date,
Last Reviewed, Next Review, Owner, Approved By); all 10 required sections (Purpose, Scope,
References, Roles, Controls Covered, Procedures, Evidence Collection, Exceptions and Variance,
Review and Maintenance, Revision History); control count per family matches expected (AC=22, AT=3,
AU=9, CM=9, IA=11, IR=3, MA=6, MP=9, PS=2, PE=6, RA=3, CA=4, SC=16, SI=7; total=110).

**Templates (11 files):**
- SSP-Template.md: 110 unique control IDs (grep `3\.[0-9]+\.[0-9]+` | sort -u | wc -l)
- POAM-Tracker.csv & Control-Implementation-Matrix.csv: 111 total lines = 1 header + 110 data rows
- Cybersecurity-Program-Checklist.csv: ≥30 procedures; contains SPRS, C3PAO, awareness, vulnerability, access review, IR, backup, POAM
- Asset-Inventory-Template.csv: header + ≥5 example rows
- Risk-Register-Template.csv: header + ≥3 example rows
- Incident-Response-Plan.md: 72-hour DIBNet reporting, severity matrix, Containment/Eradication/Recovery, lessons learned, escalation chain
- CMMC-L2-Scope-Determination.md: enclave boundary, in/out-of-scope, CUI data flow, ESPs, GCC High, facilities, mobile/printing/removable
- Evidence-Collection-Matrix.csv: covers all 14 families
- CUI-Data-Flow-Register.md: entry points, processing, storage, transmission, destruction
- TAA-Section889-Pre-Purchase-Checklist.md: TAA, Section 889, 5 prohibited companies (Huawei/ZTE/Hytera/Hikvision/Dahua), False Claims Act, FAR citations

**Index docs:** README directory tree matches actual files; Control-to-Document-Mapping.md has 110 controls; nist_800_171_controls.json has 14 families, total=110.

**Reference docs:** NIST SP 800-171 Rev 2 PDF (≥1 MB), NIST SP 800-171A Rev 2 PDF (≥1 MB), 7 DFARS key clauses, 32 CFR Part 170.

**Overall quality:** No stub files (<20 lines except intentional example-row CSVs); no stray `*.py`/`.tmp`/`.bak`/`.swp`; no broken cross-references; no empty undocumented directories.

### SOP Files — Required Sections

Each SOP must have (in order): Document Control, Purpose, Scope, References, Roles, Controls Covered, Procedures, Evidence Collection, Revision History, Exceptions, Review and Maintenance.

**Verification command:**
```bash
for f in control-families/*/CS-*.SOP.md; do
  name=$(basename "$f" .SOP.md)
  has_exceptions=$(grep -ci 'exception' "$f")
  has_review=$(grep -ci 'review.*maintenance\|maintenance.*review\|##.*Review\|##.*Maintenance' "$f")
  echo "$name: Exceptions=$has_exceptions Review=$has_review"
done
```

### CSV Files — Row Counts

- `POAM-Tracker.csv`: 111 lines (header + 110 controls)
- `Control-Implementation-Matrix.csv`: 111 lines
- `Cybersecurity-Program-Checklist.csv`: 35+ lines (header + 30+ procedures)
- `Asset-Inventory-Template.csv`: 6+ lines (header + 5+ example rows)
- `Risk-Register-Template.csv`: 4+ lines (header + 3+ example rows)
- `Evidence-Collection-Matrix.csv`: 107 lines

**Verification command:**
```bash
for csv in templates/*.csv; do
  wc -l "$csv"
done
```

### Remediation Plan Pattern

Write `REMEDIATION-PLAN.md` with:
- Documents That PASS (table)
- Documents Requiring Remediation (grouped by gap type)
- Specific fixes per file (exact text to insert)
- File paths and section numbers

### Reviewer Agent Criteria

Reviewer agent must:
1. Re-run verification audit commands
2. Compare against original gaps in REMEDIATION-PLAN.md
3. Check for new issues introduced by fixes
4. Report structured findings (what was fixed, what passed, remaining gaps with specific file paths and line numbers)

## Git Commit and Push Workflow

When the toolkit is complete and all QA passes, commit to the repo using a clean PR workflow:

### 1. Exclude Bulk Extracted Archives

Compliance toolkits download large reference archives (e.g., DFARS HTML Complete ZIP = 3.9 MB). When extracted, these produce thousands of individual files (the DFARS archive alone = 2,874 HTML files). **Always gitignore the extracted directory; keep only the ZIP.**

```bash
echo "# DFARS full extracted archive — too many files, use the ZIP instead
compliance-toolkit/reference-docs/dfars-extracted/" >> compliance-toolkit/.gitignore

# If already staged, unstage:
git rm -r --cached compliance-toolkit/reference-docs/dfars-extracted/
```

A clean toolkit should be ~47 files, not ~2,920.

### 2. Feature Branch + Squash Merge

```bash
git checkout -b feat/cmmc-l2-compliance-toolkit
git add compliance-toolkit/
git diff --cached --name-only | wc -l  # Verify count is reasonable (~47, not thousands)
git commit -m "feat: add complete CMMC L2 compliance toolkit for [Company]

[Detailed body listing contents: 14 SOPs, 11 templates, reference docs]
[QA status: reviewer agent passed all criteria]"

git push -u origin feat/cmmc-l2-compliance-toolkit
gh pr create --title "feat: CMMC L2 Compliance Toolkit" --body "..." --base main
gh pr merge --squash --delete-branch
git checkout main && git pull origin main
```

### 3. Large PDF Files

The FAR-Complete.pdf is ~13 MB — under GitHub's 100 MB hard limit but above the 50 MB warning threshold. No Git LFS needed for compliance reference PDFs (all under 15 MB). If a PDF exceeds 50 MB, consider Git LFS or storing externally.

### Meeting Tasker Deliverables — From Screenshots to SteerCo Briefings

**Problem:** The user walks out of a meeting, dumps 10-15 screenshots (Teams invite, Copilot/
M365 summary, task list, presentation slides) into Discord, and says "Taskers [client]." They
expect: every image visually inspected in detail → action items extracted → deliverables built
for each → judge-gated → published as HTML.

**Resolution:**

1. **Batch vision_analyze on ALL images** — dispatch `vision_analyze` on every image
   simultaneously in one assistant turn. Don't skip any. Some may fail with 429 rate limits
   on the vision model — retry those individually after the batch completes. Keep a structured
   log of what each image contains.

2. **Document image contents** — before building deliverables, create a mental (or working-file)
   summary of what each image contains. This becomes source-of-truth for the deliverable
   content. Key extraction targets:
   - Meeting metadata (title, date, organizer, attendees, responses)
   - Action items with assignees and descriptions (exact wording)
   - Presentation slide content (topic / description / expected outcome tables)
   - Strategic frameworks and visual models (e.g., the "Compliance Gate" concept)
   - Org charts, timelines, phase diagrams
   - Process maps and decision flows

3. **Cross-reference with local repo** — before building, search the local repo for existing
   materials that inform the deliverable. For Aecon this includes the enclave deployment plan,
   shared responsibility matrix, subcontractor flow-down tracker, FOCI pathway, process maps.
   Pull control-level detail (CSV templates, deployment phases) into the deliverable.

4. **Build the deliverable** — synthesize images + repo context into the specific action items
   assigned. For meeting taskers, the user's exact wording of the action item IS the deliverable
   requirement — don't paraphrase or generalize it.

5. **Judge-gate** — dispatch a judge agent to review the deliverable against the original action
   items. Use the HTML file path as the input, not inline content.

**Deliverable types from meeting taskers:**

- **DOR (Division of Responsibility) matrix** — three lifecycle phases (Setup / Implementation /
  Daily Execution) × multi-party R/A/C/I matrix. Parties typically include: the contractor
  entity, compliance team, C3PAO, platform provider (Microsoft), ESPs, subcontractors, JV
  partners, DCSA, BD. Each cell has an R/A/C/I tag. Include a cadence column for daily
  execution activities (Continuous / Monthly / Quarterly / Annually).

- **CMMC timeline (JV formation → audit)** — seven-phase Gantt from entity formation through
  certification posting. Include: (a) greenfield timeline (7-10 months), (b) client-specific
  acceleration track, (c) BD lead-time reference card (scenario → minimum lead time table),
  (d) BD bid eligibility check embedded at opportunity intake. Use Gantt-style bars in HTML/CSS.

- **Compliance Gate briefing** — the FOCI × CMMC × CAS three-gate model where any single gate
  failure blocks the pursuit. Present as a visual with Go/No-Go cards. This is the executive-
  level framing that connects compliance work to business development strategy.

**Reference:** See `references/meeting-tasker-deliverable-pattern.md` for the full workflow\nwith the July 2026 Aecon example (15 images → DOR matrix + timeline HTML briefing). Key\nlessons from that session:\n- **CMMC scoring model confusion** — see the \"CMMC 1.0 vs 2.0 Scoring Methodology\" pitfall\n  above. ALWAYS load `references/cmmc-l2-assessment-lifecycle.md` before writing scoring details.\n- **FOCI transition DOR** — for foreign-owned contractors, include a pre-mitigation vs.\n  post-mitigation ownership table (CMMC assessment and FOCI mitigation are parallel tracks).\n- **Decisions Required table** — make the briefing actionable with named owners and deadlines.\n- **Timeline realism** — always include a readiness reality check and best/likely/worst-case\n  range, not a single optimistic date.\n- **Internal mock assessment framing** — never represent internal analysis as external C3PAO\n  findings in client-facing deliverables.

### Meeting Prep Briefings from Toolkit Intelligence

**Problem:** After completing the toolkit and mock assessment, the user needs executive meeting prep — a one-page HTML briefing for a 1-on-1 with leadership (e.g., Compliance Director). This is a different deliverable from the technical mock assessment briefing.

**Resolution:**

1. **Clarify meeting objective first** — ask the user: status update? strategy alignment? resource ask? scope expansion? This determines the entire briefing structure.
2. **Produce as self-contained HTML** using the Thariq/html-effectiveness aesthetic with:
   - TL;DR with recommended position (not neutral — be opinionated)
   - Stat cards for where the company stands
   - Decision matrix for the key strategic question (e.g., scope expansion vs delta assessment vs standalone cert — with pros/cons and a recommendation)
   - Timeline to deadline
   - Resource asks (IT hours, budget, decisions needed)
   - Top 5 discussion points ranked by importance, each with: recommended position, counterarguments to anticipate, and response
   - "What could go wrong" section (top 3 risks + mitigations)
   - Decision log: what needs to be decided in-meeting vs what can wait
3. **NO personal names** — use role titles throughout
4. **Save to Nextcloud briefings/** and send the link

### Podcast-Style Audio Briefings from Toolkit Intelligence

**Problem:** The user may request a Freakonomics/Planet Money-style podcast to get up to speed on the compliance situation — an audio narrative that tells the story of where the company stands, what's at stake, and the path forward.

**Resolution:**

1. **Dispatch a writer agent** to produce a ~2,500-word script from the gap reports and toolkit docs. Structure: cold open hook → Act 1 (explain the domain) → Act 2 (where this company stands) → Act 3 (path forward) → closing (what's at stake). Include `[PAUSE]`, `[MUSIC]`, `[SOUND EFFECT]` production cues. NO personal names.
2. **Clean the script for TTS** — strip all `[BRACKETED]` cues, `NARRATOR:`/`EXPERT:` labels, and `---` separators using regex before feeding to TTS.
3. **Split into ≤4,000-character chunks** at paragraph boundaries (TTS providers have character caps: xAI 15,000, OpenAI 4,096, edge ~unlimited but shorter chunks = more reliable).
4. **Generate each chunk via `text_to_speech`**, then **concatenate with ffmpeg:**
   ```bash
   # Create concat list
   for f in /tmp/podcast-part-*.mp3; do echo "file '$f'" >> /tmp/concat-list.txt; done
   # Concatenate without re-encoding
   ffmpeg -f concat -safe 0 -i /tmp/concat-list.txt -c copy /tmp/podcast-full.mp3
   ```
5. **Deliver** the final MP3 directly (MEDIA: path) + script location for reference.

**Key TTS pitfall:** The edge TTS provider (default) produces 48 kbps audio — fine for voice but lower quality. If the user wants broadcast quality, use xAI or OpenAI TTS if available. The edge voice is the reliable fallback.

## Pitfalls

### DoD CIO Website Bot Detection Blockade

**Problem:** The DoD CIO website (`dodcio.defense.gov`) blocks all automated downloads (both `curl` and `browser_navigate`) with 403 Access Denied due to aggressive bot detection.

**Impact:** Two critical reference documents cannot be downloaded automatically:
- CMMC L2 Scoping Guide v2.13
- CMMC Assessment Process (CAP) Level 2 v2.13

**Resolution:**
1. Document this gap in `GAP-ANALYSIS.md` as a manual action item
2. Provide URLs to user for manual download from corporate browser
3. Instructions: Save to `compliance-toolkit/reference-docs/` and scan into Nextcloud

**Reference:** See `references/dod-cio-bot-detection.md` for full details.

### Client-Specific Content for Implementation Descriptions

**User requirement:** The Control Implementation Matrix should have client-specific implementation descriptions, not generic "See the SOP" text. The user corrected this explicitly.

**Resolution:**
1. For the first 10-20 controls (AC, IA, SC families — the most technically significant), write Aecon-specific descriptions referencing their actual stack, named personnel, and site locations
2. For the remaining controls, a brief one-liner is acceptable but should still reference the client environment when possible
3. Use the client's onboarding documents, transcript insights, and existing analysis files to extract specifics: vendor names (InEight, Box.com), platform versions (GCC High, Windows 11), named personnel (Olivia, Joe), site details (Charlotte FCS office, SRS), and known technical decisions (USB-only printers, Intune device compliance)
4. When dispatching the control matrix build agent, pass context-rich client specifics so the agent can produce better implementation descriptions the first time

**Reference:** See `references/client-specific-implementation-examples.md` for the Aecon examples used after this correction.

### SOP Section Consistency (Parallel Builds)

**Problem:** When dispatching multiple agents to build SOPs in parallel, some agents will include all required sections (Exceptions, Review and Maintenance, Evidence Collection, Revision History) and some will not. After all SOPs are built, run a section-presence audit:

```bash
for f in control-families/*/CS-*.SOP.md; do
  name=$(basename "$f" .SOP.md)
  has_exc=$(grep -c 'Exceptions and Variance' "$f")
  has_rev=$(grep -c 'Review and Maintenance' "$f")
  echo "$name: Exceptions=$has_exc Review=$has_rev"
done
```

For any SOP missing sections, insert them before the Revision History section with correct sequential numbering. Use a Python script to automate insertion and renumbering — do NOT manually edit each file.

### nist_800_171_controls.json Truncation

**Problem:** Even after the `pdftotext -raw` extraction method is documented, the `nist_800_171_controls.json` file itself may still contain truncated control text if it was built with the old TOC-based method and never rebuilt. The JSON will have the first sentence only (e.g., "Limit system access to authorized users, processes acting on behalf of authorized users, and" — cut off mid-sentence).

**Detection:** Spot-check 3 controls for complete text:
```bash
python3 -c "
import json
with open('nist_800_171_controls.json') as f: data=json.load(f)
for fam in ['3.1']:
  for c in data['families'][fam][:3]:
    print(f'{c[\"id\"]}: {c[\"text\"][-60:]}')"
```
If any text ends mid-phrase (no period, cut-off clause), the JSON is truncated.

**Resolution:** Re-extract using the `pdftotext -raw` method in `references/nist-control-text-extraction.md`, then rebuild the JSON. If the Control Implementation Matrix CSV was built from the truncated JSON, rebuild the CSV too — see `scripts/rebuild-control-matrix.py` for a one-shot script that extracts full text from PDF, rebuilds the CSV with all 110 controls, and optionally applies client-specific implementation examples.

### CSV Data Corruption
- Wrong control IDs (e.g., `a1c` instead of `3.1.1`)
- Wrong row counts (e.g., 14 rows instead of 110)
- Missing headers

**Resolution:**
1. Rebuild CSV files programmatically from `nist_800_171_controls.json`
2. Verify row counts: 111 lines (header + 110 controls)
3. Verify control IDs match `3.x.x` format
4. Prepend header row if missing

### Naming Convention Mismatch

**Problem:** SOP files or folders may not match organizational naming conventions.

**Resolution:**
1. Align with existing organizational conventions (e.g., `CS-[FAMILY]-####.SOP.md`)
2. Use folder naming: `####-[FAMILY]-[Full Name]/`
3. Document the naming convention in `README.md`

### Duplicate CSV Header Rows

**Problem:** When CSVs are rebuilt or concatenated programmatically, the header row may be
duplicated (lines 1 and 2 are byte-identical). This passes a naive `wc -l` count (still 111
lines) but will break spreadsheet import and any consumer expecting exactly one header.

**Detection:**
```bash
# Both lines identical → duplicate header present
sed -n '1p' templates/POAM-Tracker.csv
sed -n '2p' templates/POAM-Tracker.csv
[ "$(sed -n '1p' file.csv)" = "$(sed -n '2p' file.csv)" ] && echo "DUPLICATE HEADER"
```

**Resolution:** Delete line 2. Always include a duplicate-header check in QA review alongside
the row-count check — a correct line count does NOT prove a clean header.

### README Directory Tree Drift

**Problem:** After building templates, the README directory tree is not updated and omits
newly-added files. In the July 2026 build, `CUI-Data-Flow-Register.md` and
`TAA-Section889-Pre-Purchase-Checklist.md` existed in `templates/` but were absent from the
README tree.

**Detection:** Compare actual files vs README-listed files:
```bash
for f in templates/*; do
  base=$(basename "$f")
  grep -q "$base" README.md || echo "MISSING FROM README: $base"
done
```

**Resolution:** After every build/fix pass, regenerate the README directory tree or run the
drift check above. Treat README as a contract with the file system.

### CSV Trailing Newline and `wc -l` Miscounting

**Problem:** `wc -l` counts newline *characters*, not lines. A CSV file with no trailing newline after the last data row will report N-1 lines even though it has N logical lines (header + N-1 data rows). This caused QA confusion where a CSV appeared to have 109 data rows when it actually had 110.

**Detection:**
```bash
# Check if file ends with a newline
[ -n "$(tail -c 1 file.csv)" ] && echo "MISSING TRAILING NEWLINE"

# Fix: append newline if missing
[ -n "$(tail -c 1 file.csv)" ] && echo "" >> file.csv
```

**Resolution:** Always ensure CSV files end with a trailing newline before running `wc -l`. When building CSVs programmatically with `'\n'.join(lines)`, add a trailing `'\n'` explicitly:
```python
with open('file.csv', 'w') as f:
    f.write('\n'.join(lines) + '\n')
```

### Evaluating Non-Existent Deliverables

**Problem:** User asks to "evaluate this section" or "review this document" but the content doesn't exist in the workspace. Searching with `search_files`, `find`, and `read_file` returns nothing. The agent cannot evaluate against criteria without the actual content.

**Example from practice:** User requested evaluation of a "Where to Find Compliance Documentation" section against 5 criteria (answers Joe's question, generality, logical positioning, operational tone, IT/utility). The section didn't exist in `/home/amyn/repos/aecon-fcs/` or anywhere in the repo. Agent wasted cycles searching and had to report inability to evaluate.

**Detection pattern:**
```bash
# 1. Broad search by title/keywords
search_files(path="/path/to/workspace", pattern="Where to Find Compliance Documentation", target="content")

# 2. File pattern search
find /path/to/workspace -type f -name "*where*find*" -o -name "*compliance*doc*"

# 3. Session search if content might be from recent work
session_search(query="Where to Find Compliance Documentation")

# 4. If all three return empty/null → content doesn't exist
```

**Resolution:**
1. **Search systematically** using the three-pronged approach above before concluding "not found"
2. **Report clearly** if content is missing: "I've searched [workspace] and cannot locate [title]. To proceed with the evaluation, please provide: [file path OR actual content]"
3. **Check session_search** for context — the user may be referencing work from a recent session that hasn't been committed yet
4. **Don't fabricate evaluation** — attempting to evaluate criteria against non-existent content leads to hallucination
5. **Offer to create** if appropriate: "This section appears to be missing. Would you like me to draft it based on your criteria?"

**Key lesson:** When the user says "evaluate X" but X doesn't exist, the workflow is: search → report missing → request content or offer to create. Do not attempt to evaluate criteria against a phantom.

### Empty Scaffold Directories

**Problem:** Build scripts create placeholder directories (`sop-templates/`, `tracking/`,
`Graphics/`) that never get populated but remain in the tree, making the repo look unfinished.

**Resolution:** Run `find . -type d -empty` as part of every QA review. Either populate the
directory, remove it, or add a `.gitkeep` with a documented purpose.

### Grep Alternation Escaping — `\|` vs `|`

**Problem:** When using `grep -qiE "$term"` where `$term` contains `term1\|term2`, the `\|`
is treated as a **literal backslash-pipe** in Extended Regular Expression mode, NOT as
alternation. This produces silent false-negative FAILs in verification checks — every section
that uses alternation appears "missing" even though it's present.

**Example that FAILS (false negative):**
```bash
# WRONG: \| is literal in ERE mode
grep -qiE "Purpose\|Scope" file.md   # returns non-zero even when both exist
```

**Correct patterns:**
```bash
# Option A: bare pipe with -E
grep -qiE "Purpose|Scope" file.md

# Option B: escaped pipe WITHOUT -E (BRE mode)
grep -qi "Purpose\|Scope" file.md

# Option C: multiple separate checks (safest for verification scripts)
for section in Purpose Scope; do grep -qi "$section" file.md && echo "PASS: $section"; done
```

**Impact:** During the July 2026 QA review, this escaping bug caused every SOP to report
"## Purpose" as FAIL when all 14 SOPs actually had `## 1. Purpose`. It also caused false FAILs
in template content checks (DIBNet, lessons learned, in-scope, etc.). Always double-check
failing grep results with a simpler pattern before reporting a gap.

**Resolution for verification scripts:** Use the reusable `scripts/qa-review-toolkit.sh`,
which uses correct escaping throughout. If hand-writing checks, prefer separate per-term grep
calls over alternation to avoid this class of bug entirely.

### CMMC 1.0 vs 2.0 Scoring Methodology — Critical Confusion

**Problem:** The CMMC 1.0 scoring model (1000-point scale, 17 weighted requirements ×10,
93 requirements ×1, ≥883 pass threshold) is widely cited in older industry sources and LLM
training data. The CMMC 2.0 final rule (32 CFR Part 170, effective Dec 2024) uses a completely
**different** model. If you build deliverables from general knowledge without loading the
`references/cmmc-l2-assessment-lifecycle.md` reference file, you WILL use the wrong methodology.

**Correct CMMC 2.0 scoring (§170.24):**
- Maximum score: **110** (not 1000)
- Per-requirement value: **1, 3, or 5** points (based on NIST FIPS 200 / NIST 800-53 R5 designation)
- Each requirement scored: **MET / NOT MET / N/A** (not weighted multiplication)
- Score = 110 minus sum of NOT MET values
- Negative scores possible
- POA&M allowed per §170.21 for eligible requirements (Conditional status); 180-day closeout window
- NOT all requirements are POA&M-eligible; do not cite a specific "5-item maximum" without verifying current CAP guidance

**Resolution:** ALWAYS load `references/cmmc-l2-assessment-lifecycle.md` before writing any
deliverable that references CMMC assessment scoring, pass thresholds, or POA&M rules. The
reference file has been verified against Cornell LII regulatory text and is authoritative.

### Internal Mock Assessment ≠ External Assessment Finding

**Problem:** When writing deliverables that cite readiness gaps or assessment findings from an
internal mock C3PAO assessment (the persona-based exercise documented in this skill), the
language must NOT imply these are findings from an actual C3PAO or external assessor.

**User correction (July 2026):** "the mock c3pao assessment was just something i had you run
internally not an actual assessment." The deliverable had language like "the C3PAO would pause
the assessment on Day 1" and "C3PAO gap assessment dated July 6" which implied external
engagement.

**Resolution:** In deliverables, always frame internal mock assessment output as "an internal
mock assessment identified..." or "internal analysis found..." — never as "the C3PAO found..."
or "assessment findings from [date]." Distinguish clearly between internal preparatory work and
actual C3PAO engagement output. This applies to readiness percentages, gap counts, and severity
ratings — all are internal estimates until a real C3PAO validates them.

### Toolkit vs. Strategic Roadmap Confusion

**Problem:** Once the tactical toolkit is built, the user may shift focus to strategic architecture questions — entity structure, CAGE code strategy, FOCI, multi-CAGE scope expansion, certification timeline, Recert roadmap. The toolkit SOPs don't answer these questions.

**Resolution:**
1. Recognize the difference: The toolkit is the tactical foundation; the roadmap is the corporate architecture.
- **Entity structure:** CMMC certification is granted at the **information system level**, NOT entity-level. Per § 170.4: *"CMMC Status...of an OSA information system is officially stored in SPRS."*
- **Multiple CAGE codes per scope:** Multiple CAGE codes CAN share one Assessment Scope. Per § 170.17(a)(1)(i)(E), SPRS must list *"All industry CAGE codes associated with the information systems addressed by the CMMC Assessment Scope"* — plural. One GCC High tenant / one Assessment Scope can cover multiple CAGE codes.
- **The word "enclave" does NOT appear in the regulation.** 32 CFR Part 170 uses "information system," "CMMC Assessment Scope" (§ 170.19(a)), and "OSA's environment."
- **Scope expansion = delta assessment required:** Adding a new CAGE code to an existing certified scope is a material change. Per DFARS 204.7501, "Current" status requires *"No changes in compliance...since the [Status] date."* A C3PAO delta assessment is needed before the new CAGE can rely on the expanded certificate.
- **CMMC reciprocity:** A CMMC L2 certification carries across ALL contracts that use the same certified information system, regardless of CAGE code. Per DFARS 252.204-7021(c): *"CMMC assessments will not duplicate efforts from any other comparable DoD assessment."*
- **FOCI vs CMMC:** CMMC does NOT consider FOCI. FOCI only gates Facility Security Clearance (FCL) for classified work. A foreign-owned company can get CMMC L2 certified without FOCI mitigation.
- **NIST Rev 3 transition:** Rev 3 published May 14, 2024; DoD still assesses Rev 2 (§ 170.14(c)(3)). Transition requires new federal rulemaking — earliest ~2028. Build for Rev 2, design for Rev 3.

**Reference:** See `references/cmmc-entity-scope-and-structure.md` for full regulatory citations, scope expansion process, phase-in timeline dates, and authoritative source access notes.

### HTML Briefing Design — Avoid Wall-of-Text

**Problem:** Strategic briefings produced as long-form documents with dense paragraph blocks instead of visual, scannable interfaces.

**User feedback:** "There are big old text blocks instead of clear concise visuals."

**Resolution:** When producing HTML briefings (especially multi-section strategic documents), use the html-effectiveness visual vocabulary:
- **Stat cards / summary bands** — 4-column grids with key numbers at the top for executive scan
- **Milestone timelines** — date column + dot + connecting line + concise body with tags (NOT stacked divs with bullet lists)
- **Collapsible `<details>`** — put dense regulatory citations behind expandable sections; show the key point, hide the full text
- **Side navigation** — sticky nav for any document with 5+ sections
- **TL;DR box** — executive summary at the top before diving into detail
- **Section number badges** — numbered badges (01, 02, etc.) next to section headers
- **Callout boxes** — for warnings, critical findings, and action items (not inline bold text)
- **Compact tables** — for comparison data, not multi-paragraph descriptions

**Anti-pattern:** Five consecutive `<li>` items each containing a full paragraph of regulatory citation. This is a document, not a briefing.

**Reference:** Study `/home/amyn/repos/html-effectiveness/` (20 examples). Key files:
- `11-status-report.html` — stat cards, summary bands, compact tables
- `16-implementation-plan.html` — milestone timeline with dots/lines/tags, section badges
- `14-research-feature-explainer.html` — sticky side nav, TL;DR box, collapsible details, callouts

**Reference:** See `references/cmmc-infrastructure-required-pitfall-2026-07.md` for the full analysis of three infrastructure delivery paths (PreVeil, M365 BP GCC High, Cuick Trac), the NIST 800-171 technical controls that require infrastructure, and market context ($6.8B market, 300K+ DIB organizations).

### Government Website Blocking for Research

**Problem:** Multiple government websites block automated research access:
- **acquisition.gov** — Returns empty/JS-redirected content for DFARS clauses
- **sam.gov** — Returns minimal content, blocks SPRS scoring methodology access
- **cyberab.org** — Returns empty content, blocking C3PAO directory access
- **dodcio.defense.gov** — 403 Access Denied for CMMC CAP and scoping guides

**Also blocked (confirmed July 2026):**
- **Search engines** — Google (403/captcha), Bing (Cloudflare challenge), DuckDuckGo (empty
  results page) all block automated browser_navigate queries
- **web_search tool** — Consistently returns empty results (`"web": []`) for CMMC/NIST
  compliance queries. Do not rely on this tool for compliance research; use web_extract
  on known-good industry sources instead.
- **firecrawl_search** — Unreliable for government/compliance queries; MCP server may be
  unreachable. Fall back to web_extract on known-good URLs.
- **CMMC Command (cmmccommand.org)** — Next.js site with client-side routing. Direct URL
  extraction via web_extract returns 404 for individual blog posts. Browser navigation to
  listing pages works, but individual post content is only accessible through click-through
  navigation from the listing page, not via direct URLs.
- **Corporate sites** — BAE Systems (baesystems.com) uses Imperva/hCaptcha bot protection;
  Rolls-Royce and other defense contractor sites similarly protected
- **acquisition.gov / sam.gov / cyberab.org / dodcio.defense.gov** — Return empty content,
  JS-redirected content, or 403 Access Denied for automated access

**Reliable industry sources (confirmed working with web_extract):**
- **cmmc-hub.com** (Ghost CMS) — Reliable for NIST 800-171 control families, CMMC Level 2,
  SPRS scoring, regulatory stack, SSP writing, and Rev 2 vs Rev 3 articles. Use web_extract
  directly on article URLs. Primary go-to source when government sites are blocked.
  **⚠️ July 2026:** Several previously-working article URLs returned 404s (e.g.,
  `/nist-800-171-self-assessment/`, `/cmmc-level-2/`). The site may have restructured.
  Fall back to the root domain or use browser_navigate + browser_snapshot to discover
  current article URLs.
- **fieldledger.us** — Reliable for Rev 2 vs Rev 3 comparison, ODP analysis, and control
  count details.
- **secureframe.com** — Reliable for NIST 800-171 and CMMC framework guides.
  **⚠️ July 2026:** Previously-working article URL `/blog/cmmc-20-self-assessment-guide`
  returned 404. Use browser_navigate to discover current URLs.
- **learn.microsoft.com** — Reliable for Windows security documentation (TPM, BitLocker,
  hardware security, Intune, GCC High). Use web_extract or browser_navigate directly.
- **epeat.net** — Electronic Product Environmental Assessment Tool registry; accessible
  via web_extract for sustainability/EPEAT research.
- **epa.gov** — Accessible via web_extract for EPP Recommendations and federal
  sustainability standards (FAR 23.1 compliance).
- **cyber.mil (public.cyber.mil)** — DISA STIGs Document Library: browser_navigate to
  `/stigs/downloads/`, browser_type + browser_press to search for specific STIGs
  (Windows 11, GPOs, Intune policies). Publicly accessible without CAC login.
- **nvlpubs.nist.gov** — NIST HTML publications accessible via browser_navigate.
  Use browser_console for structured control text extraction (see pitfall Resolution #6).

**Competitive intelligence sources — CMMC commercial product research:**
For researching the commercial CMMC compliance product landscape (pricing, features,
positioning), use these browser-navigable commercial sites. Unlike government/industry
blog sites, these are fully accessible via browser_navigate and render their pages
completely (no JS-shell blocking, no 404s on key pages):
- **futurefeed.co** — CMMC SaaS platform (4,086 users, 1,400+ companies, 447 CAGE codes).
  `/pricing/` shows full pricing: $100/mo Innovator (≤25 FTEs), $400/mo Standard (26-999
  FTEs). Features: live SSP, POA&M, CMMC L1, project management. AWS GovCloud FedRAMP High.
- **preveil.com** — Encrypted CUI enclave + compliance platform (3,000+ contractors).
  `/new-pricing-page/` shows pricing: Gov Community custom → PreVeil Pass $450/mo for SMEs
  (3 licenses + Compliance Accelerator + pre-filled docs). Claims 75% savings vs GCC High.
  `/cmmc-compliance/` has feature overview. Also has a CMMC Cost Calculator tool.
- **NIST CPRT** (csrc.nist.gov/projects/cprt/catalog) — Free reference tool for browsing
  NIST SP 800-171 control data in Excel/JSON. JS-heavy (shows "Loading..."); use
  browser_navigate and wait. This is the canonical free alternative any commercial product
  competes against.

`references/cmmc-l2-competitive-landscape-2026-07.md` for the condensed analysis
  covering 6 competitors, TAM estimates, suspension impact, and strategic recommendations.
- Researching or designing software procurement governance intake checkpoints for a GCC
  High / CMMC enclave — FAR Part 12 vs Part 8 applicability, DFARS clause triggers
  (7012/7019/7020/7021/7024/239-7010), FedRAMP vs DoD Impact Level mapping, SPRS
  verification, compliance checks for CUI-touching software, MVP vs over-engineering
  for sub-$100K purchases — load `references/software-procurement-governance-checklist.md`
  for the full intake gate framework with threshold routing, Light/Full check matrices,
  and FAR/DFARS regulatory quick reference
positioning strategies, and the GCC High vs lightweight-alternative analysis.

**Impact:** Cannot verify official C3PAO counts, SPRS scoring methodology, or DFARS 252.204-7012 clause language directly via curl or browser tools during automated research sessions. Cannot use search engines to discover BAE/FOCI case studies or corporate governance structures.

**Resolution for Regulatory Research (Verified Working):**
1. **Cornell LII (law.cornell.edu) is the reliable primary source for all CFR text.** It serves
   full eCFR content and is accessible via both curl and browser tools. URL patterns:
   - DFARS: `https://www.law.cornell.edu/cfr/text/48/252.204-NNNN`
   - CMMC rule: `https://www.law.cornell.edu/cfr/text/32/170.NN`
   - NISPOM/FOCI: `https://www.law.cornell.edu/cfr/text/32/117.NN`
   - Part index: `https://www.law.cornell.edu/cfr/text/32/part-170`
2. **For JS-rendered pages**, extract text via browser_console:
   `document.querySelector('main').innerText` (paginate with `.substring(N, M)` for long pages)
3. **Microsoft Learn (learn.microsoft.com)** is accessible and reliable for shared responsibility
   models, GCC High documentation, and Azure security documentation
4. **For corporate/FOCI research** where search engines and corporate sites are blocked: rely on
   the regulatory text (32 CFR § 117.11 defines the SSA structure that BAE/Rolls-Royce follow),
   SEC filings (EDGAR is accessible), and existing reference files (`references/foci-and-cmmc-strategy.md`)
5. **DISA STIG site (public.cyber.mil) works with browser tools** — use `browser_navigate` to the
   STIGs Document Library, `browser_type` into the search box, `browser_press('Enter')` to search.
   The site returns STIG results (Windows 11, GPOs, Intune policies) without requiring CAC login.
   This is the authoritative source for current STIG versions and automation content.
6. **NIST 800-171 control text extraction via browser_console** — when the NIST HTML publication
   is loaded in the browser (`browser_navigate` to the nvlpubs.nist.gov HTML URL), use
   `browser_console` with JavaScript to extract specific control requirements by their heading
   IDs. Pattern:
   ```javascript
   const sections = ['03.13.11', '03.05.02', '03.13.08'];
   sections.forEach(id => {
     const h3 = Array.from(document.querySelectorAll('h3')).find(h => h.textContent.includes(id));
     if (h3) {
       let content = ''; let el = h3.nextElementSibling; let count = 0;
       while (el && !['H3','H2'].includes(el.tagName) && count < 20) {
         content += el.textContent.trim() + '\\n';
         el = el.nextElementSibling; count++;
       }
       console.log(id + ': ' + content.substring(0, 2000));
     }
   });
   ```
   This is faster and more reliable than `pdftotext` for Rev 3 control text extraction.
7. **EPA, EPEAT, and FedRAMP sites are accessible** via `web_extract` — use these for
   sustainability (EPA Recommendations, EPEAT Registry) and cloud authorization (FedRAMP
   Marketplace) research. Energy.gov and sustainability.gov may return minimal content.

**Resolution for Rev 3 Transition Research:**
1. **Primary Sources (accessible):** NIST websites (csrc.nist.gov) reliably return content. Use official NIST documentation as your primary source of truth for control counts, family structures, and publication dates.
2. **Industry Analysis (accessible):** Multiple industry sources (cmmc-hub.com, CMMC Command, Secureframe, Field Ledger, Cybriant) provide detailed analysis of Rev 2 vs Rev 3 changes and transition timelines.
3. **Government Sources (blocked):** For C3PAO counts, SPRS scoring, and DFARS clause verification:
   - Document the limitation explicitly in your research output
   - Provide citations for accessible sources
   - Note which data points require manual verification via corporate browser
   - Do not fabricate numbers or cite blocked sources
4. **Verification Strategy:** When presenting findings to stakeholders, distinguish between:
   - **Verified via primary/industry sources:** Control counts, family structures, new requirements, timeline estimates
   - **Requires manual verification:** C3PAO counts, SPRS scoring thresholds, DFARS exact clause language

**Reference:** See `references/rev-3-transition-research.md` for full details on Rev 2 vs Rev 3 differences and research approach.

## C3PAO Persona-Based Mock Assessment

After building the toolkit, run a **simulated C3PAO assessment** using 5 assessor personas to identify gaps a real assessment would find. This is a reusable validation technique that catches what a generic QA review misses.

### When to Run

- After the initial toolkit build + QA verification cycle is complete
- Before the company engages a real C3PAO
- When the user asks for a "mock assessment" or "act like the auditor"
- When the user says things like "creep right down" and "figure out what's missing"

### How to Run

1. **Create a C3PAO-PERSONAS.md** file in the toolkit root (see `references/c3pao-assessment-personas.md` for the full persona framework — copy and customize per client)

2. **Dispatch 3 parallel persona agents** (not more — 3 is the sweet spot for coverage without overlap):
   - Agent 1: Lead Assessor + Documentation Specialist — reviews SSP, scope, POA&M, evidence cross-references
   - Agent 2: Technical Assessor — reviews AC/IA/SC/CM/AU SOPs against actual platform configuration
   - Agent 3: Compliance/Governance + Supply Chain Assessor — reviews governance SOPs, IR plan, ESP inventory, TAA compliance

3. **Each agent must have full context** — the user is explicit about this:
   - Company entity structure (parent/subsidiary, CAGE codes, FOCI status)
   - Complete technical stack (GCC High, AVD, InEight, Box.com, Intune, Defender, Purview)
   - Named personnel and their roles
   - Known technical decisions and compromises (e.g., USB-only printers)
   - Meeting intelligence / transcript insights (if available from the repo)
   - Existing analysis documents (ATCP, Playbook, Enclave Plan)
   - All relevant file paths in the repo
   - The specific persona description they embody

4. **Compile findings** into a unified gap report categorized CRITICAL / MAJOR / MINOR

5. **Build all missing artifacts** identified by the reviewers — do not stub, do not defer

6. **Publish HTML briefings** explaining what the mock assessment found, why specific documents were added, and what the team needs to do next

### Agent Model Selection

The user has a model preference for delegated compliance agents: **use a capable model** (user specified "deep seek v4pro" — use whatever the strongest available model is for deep regulatory analysis work). If using `delegate_task`, the model is inherited from the parent session; if a specific model is needed, ensure the session is configured accordingly before dispatching.

### Standard Template Categories for GCC High Enclaves

When building the missing artifacts after a mock assessment, these are the standard document categories for a Microsoft GCC High enclave:

**7 Technical Config Documents:**
- `GCC-High-Tenant-Baseline.md` — tenant name, regions, admin roles, password/MFA policy, SharePoint sharing, Teams federation
- `FIPS-Cryptography-Validation-Register.md` — all FIPS 140-2/3 modules with CMVP cert numbers
- `AVD-Session-Host-Configuration-Baseline.md` — OS image, FSLogix, session timeouts, clipboard/drive redirection, RDP properties
- `Intune-Device-Compliance-Policy.md` — compliance settings, conditional access integration, USB device restrictions
- `Purview-DLP-Policy-Baseline.md` — sensitivity labels, DLP policies, endpoint DLP
- `Conditional-Access-Policy-Register.md` — all CA policies with users/apps/conditions/grants
- `Network-Segmentation-and-Tenant-Isolation.md` — VNet structure, NSG rules, Azure Firewall, commercial tenant isolation

**8 Governance Documents:**
- `Annual-Affirmation-Template.md` — per 32 CFR § 170.22, AO designation, attestations, review checklist
- `Shared-Responsibility-Matrix.csv` — control-level inheritance (Microsoft GCCH, Box, InEight)
- `ESP-CSP-Inventory.md` — all External Service Providers with FedRAMP level, CUI exposure, agreement status
- `Subcontractor-CMMC-Flow-Down-Tracker.csv` — subcontractor compliance flow-down tracking
- `Insider-Threat-Program.md` — NITTF guidelines, behavioral/technical detection, reporting procedures
- `Tabletop-Exercise-Scenarios.md` — 3+ scenarios specific to the enclave risk profile
- `Risk-Assessment-Methodology.md` — 5x5 matrix, vulnerability scanning, acceptance criteria
- `Physical-Security-Plan.md` — office/facility descriptions, access control, clear desk, environmental protections

**5+ Additional Documents (may overlap with above, build as needed):**
- `Security-Awareness-Training-Curriculum.md` — annual training content, phishing, CUI handling
- `Cryptographic-Key-Management-Plan.md` — key generation, storage, rotation, destruction
- `CAB-Charter.md` — Configuration Advisory Board, change management process
- `Vendor-Security-Questionnaire.md` — procurement security assessment
- `Evidence-Collection-Guide-GCC-High.md` — step-by-step evidence collection per service (Azure, SharePoint, Purview, Intune, Defender, Sentinel)

### Assessment Readiness Scoring

After the mock assessment and artifact build, assess readiness as a percentage. The July 2026 Aecon FCS assessment went from ~15% to ~25% after adding all config and governance docs. The biggest single gap determining this score:

- **~70% of the score** is SSP control descriptions (110 controls × [INSERT] placeholders)
- **~15%** is actual evidence artifacts collected from live systems (GCC High screenshots, config exports)
- **~10%** is SOP procedure step detail
- **~5%** is POA&M/Gap closure

So adding governance and technical config docs moves the needle from ~15% to ~25% because it covers ~10% of the readiness picture. The SSP is the real blocker.

**Remediation effort estimate for a 2-person IT + part-time lead team:**
- SSP description fill for 110 controls: ~250-350 hours (2-3h per control for good client-specific content)
- Evidence collection: ~80 hours (walk through each control and capture/screenshot)
- SOP refinement: ~40 hours
- Tabletop execution: ~20 hours
- Pre-assessment dry run: ~16 hours
- **Total: ~400-500 hours = 10-13 weeks at 1 FTE, or ~16 weeks with shared team**

### HTML Briefing After Mock Assessment

After the mock assessment, create a self-contained HTML briefing. The July 2026 `c3pao-mock-assessment-2026-07-06.html` (25KB, 567 lines) is a good template. Structure:

1. TL;DR stat band — readiness %, critical count, total templates, estimate to close
2. Assessment Team — all 5-7 personas with names and review focus
3. Assessment Scoring — stat cards: CRITICAL/MAJOR/MINOR, files, templates, hours
4. Timeline diagram — milestone timeline from today through CMMC Phase 2 deadline
5. Top 10 Fixes — ranked by impact, with brief description
6. Remediation Plan — phased approach with weeks, effort, owners
7. Decision Points — questions for executive leadership (C3PAO selection, IT capacity, budget)
8. Key Gaps by Persona — table showing each persona's critical findings

Use collapsible `<details>` for detailed findings, not inline paragraph walls. Side nav for sections.

### Clean Role-Based Export for SharePoint Distribution

**Problem:** After completing a toolkit, the user needs to "package this all as if it was a means work that he put together and have it in one folder" — a clean, self-contained folder ready to drop into a company SharePoint. The internal C3PAO methodology docs (persona files, gap reports) must NOT be included, and all personal names must be replaced with role titles.

**Resolution:**

1. **Create a sibling export directory** (e.g., `cmmc-l2-toolkit/` alongside the `compliance-toolkit/` working directory)
2. **Copy ONLY the deliverable files:** templates/, reference-docs/ (PDFs + key clause HTML, NOT extracted archives)
3. **Strip all personal names** using `sed` batch replacement. Map every individual's name to their role title:
   ```bash
   for name_map in "Enzo Zoratto|FBU Head" "Brian Gregorio|Compliance Director" ...; do
       name="${name_map%%|*}"; role="${name_map##*|}"
       find export_dir/ -type f \( -name '*.md' -o -name '*.csv' \) -exec sed -i "s/$name/$role/g" {} +
   done
   ```
4. **Verify zero names remain:** grep for each name across all `.md` and `.csv` files — must return 0 hits
5. **Write a comprehensive README.md** as the SharePoint landing page with:
   - Purpose & scope
   - Document index table (all templates with descriptions)
   - CMMC Phase 2 timeline
   - Role-based naming convention key (so the team knows which role maps to their actual seat)
   - Directory structure
   - Next steps for the team
6. **Gitignore heavy extracted archives** in the export directory (dfars-extracted/ = 2,874 files, 40MB — keep the ZIP only)
7. **Zip the folder** for upload: `zip -r /tmp/cmmc-l2-toolkit.zip cmmc-l2-toolkit/ -x '*/.git/*'`

**Critical pitfall — the README itself:** When writing the landing page README, the agent may inadvertently include personal names from context. ALWAYS run the name verification pass AFTER writing the README, not just after copying templates.

**Reference:** See `references/toolkit-export-sanitisation.md` for the full name-to-role mapping table and the SharePoint export workflow.

## Recurring Legal/Regulatory Questions (Common During Compliance Engagements)

During CMMC L2 engagements, compliance officers and legal counsel repeatedly raise a cluster of
questions about the **System Security Plan (SSP)** that are not answered by the SOPs, templates,
or scoping guidance alone. These are legal-analysis questions requiring direct citation to
DFARS, 32 CFR Part 170, and the CUI Registry.

### "Is the SSP CUI or CDI? Does it have to stay in the enclave?"

**Answer framework (full analysis in `references/ssp-classification-and-assessment-access.md`):**

- **CDI?** No, by default. The SSP fails the DFARS 7012 provenance prong (DoD does not provide
  it; the contractor creates it) and is not "controlled technical information."
- **CUI?** Not automatically, but a sufficiently detailed SSP maps to the CUI Registry category
  **"Information Systems Vulnerability Information."** And critically — **DFARS 252.204-7020(g)(3)
  explicitly designates DoD's copies of assessment documentation (including the reviewed SSP) as
  CUI.** If DoD treats its copy as CUI, the contractor's copy warrants the same treatment.
- **Must it stay in the enclave?** No statute explicitly says so (the word "enclave" does not
  even appear in 32 CFR Part 170), but the **enclave-description paradox** creates strong
  pressure: the document proving you protect CUI should not itself be unprotected.

### "What's the liability if the SSP is on commercial SharePoint?"

Severe if the SSP is CUI (reportable cyber incident, 72-hour DIBNet, SPRS damage, contract
suspension risk). Moderate if non-CUI but exfiltrated (False Claims Act exposure, control
failure finding). See the liability matrix in the reference file.

### "How do DIBCAC assessors and C3PAOs actually access the SSP?"

Per DFARS 252.204-7020(c), contractors provide access to facilities, systems, and personnel.
Assessors receive the SSP via secure file exchange under NDA — **they do NOT need the SSP to
live on commercial SharePoint.** This undercuts any "but consultants need access" justification
for storing the SSP outside the enclave. See the reference file for the full access mechanics.

**When these questions arise, load `references/ssp-classification-and-assessment-access.md` for
the full dual-perspective analysis with citations, liability matrix, and compliance officer
recommendations.** Do not attempt to answer from memory — the regulatory citations must be
quoted accurately.

## Support Files

- **`references/cmmc-l2-assessment-lifecycle.md`** — Condensed regulatory knowledge bank of
  the CMMC L2 assessment lifecycle, verified against 32 CFR Part 170 (via Cornell LII) and
  DFARS Final Rule (Fed. Reg. Sept 10, 2025). Covers: governing framework, phase-in schedule
  (Phase 2 ~Nov 2026 = L2(C3PAO) award condition), C3PAO assessment process (§170.17),
  scoring methodology (§170.24), POA&M 180-day closeout, 3-year validity + annual
  affirmation (§170.22), subcontractor flow-down (§170.23), Joint Ventures/CAGE codes,
  Section 847/FOCI interaction, C3PAO market & cost (2026), reciprocity/scope expansion,
  and the Cornell LII text-extraction technique for parsing JS-rendered CFR pages. Load this
  when answering "how does the L2 assessment work," "what's the certification lifecycle,"
  "Phase 2 deadline," "scoring methodology," "annual affirmation," "flow-down," or
  "Section 847 and CMMC."
- **`references/cmmc-methodology-end-to-end-research.md`** — Authoritative synthesis of the full
  CMMC/NIST 800-171 compliance methodology from gap assessment to C3PAO certification. Covers
  all six dimensions: (1) NIST SP 800-171 Rev 2 14 control families with counts, (2) NIST
  SP 800-171A assessment procedures (examine/interview/test) and determination statements,
  (3) CMMC 2.0 model levels, phase-in schedule, C3PAO assessment lifecycle, annual affirmation,
  and subcontractor flow-down, (4) SSP per NIST SP 800-18 and POA&M required fields, (5) the
  7-phase consultant lifecycle with canonical phase names, deliverables, timelines, and budget
  ranges, (6) SPRS scoring formula (−203 to +110), weight assignments, and score tiers.
  Compiled from NIST, 32 CFR Part 170, DFARS, and verified industry sources. Load this when
  researching the methodology framework for a client engagement, building a compliance product,
  or answering deep regulatory questions that span multiple dimensions.
- **`references/m365-gcc-high-compliance-workflow-guide.md`** — Condensed M365 GCC High
  compliance workflow architecture reference from July 2026 Aecon session. Covers:
  three-list SharePoint architecture (Personnel Roster + Access Requests + Audit Log) with
  specific column types and permission models; Power Automate sequential approval pattern
  with parallel NDA/clearance branches and GCC High connector availability; Forms vs Power
  Apps availability and recommendation (customized SharePoint form); Purview container-level
  labeling approach and DLP integration for list data; Teams channel + SharePoint tab
  integration with adaptive cards; multi-layer C3PAO audit strategy (UAL + versioning +
  flow run history + Purview Premium); GCC High limitations matrix (✅ available, ⚠️ limited,
  ❌ not available). Load this when asked about SharePoint list design for clearance
  management, Power Automate approval workflows in GCC High, Purview sensitivity labeling
  for compliance sites, Teams integration patterns, or C3PAO audit evidence collection.
- **`references/cmmc-dor-raci-framework.md`** — Division of Responsibility and RACI framework
  for multi-party CMMC compliance. Covers: DFARS 7012/7020/7021 flow-down chain (with exact
  paragraph citations for CSP FedRAMP requirement, subcontractor pre-award verification gates,
  and tiered CMMC level requirements per 32 CFR § 170.23), FOCI-mitigated entity governance
  (SSA/SCA/PA/VT instruments, four-document stack: SSA+TCP+ECP+Affiliated Ops Plan, GSC
  requirements from 32 CFR § 117.11), BAE Systems/Rolls-Royce Five Eyes model, Microsoft
  shared responsibility matrix, non-delegable responsibilities, "shared responsibility ≠
  shared liability" principle, foreign parent firewall enforcement layers, and RACI matrix
  structure for implementation/operations/audit/incident/flow-down/FOCI dimensions. Load
  this when asked about DOR, RACI, who owns what in CMMC, subcontractor flow-down
  obligations, CSP/ESP shared responsibility, or how foreign-owned contractors structure
  their compliance governance.
- **`references/ssp-classification-and-assessment-access.md`** — Dual-perspective (DIBCAC
  regulatory + Legal/Compliance) analysis: SSP CUI/CDI classification, DFARS 7020(g)(3) CUI
  designation smoking gun, enclave-description paradox, liability matrix for commercial
  SharePoint exposure, and how DIBCAC/C3PAO assessors actually access the SSP during
  assessments. Load this when asked "is the SSP CUI?", "does it have to stay in the enclave?",
  or "what's the liability if it's on SharePoint?"
- **`references/c3pao-assessment-personas.md`** — Full C3PAO mock assessment framework: 5 assessor personas (Lead, Technical, Compliance, Documentation, Supply Chain), how to run a mock assessment, what each persona looks for, and how to compile findings into remediation
- **`references/dod-cio-bot-detection.md`** — Full details on the DoD CIO 403 blockade and manual download workaround
- **`references/nist-control-text-extraction.md`** — Correct method for extracting full NIST SP 800-171 control text using pdftotext -raw with DISCUSSION-header stop condition. Use instead of the incomplete TOC-based extraction.
- **`references/client-specific-implementation-examples.md`** — Real Aecon examples for 31 controls with named personnel, platforms, and locations. Demonstrates the level of specificity the user expects for client-facing content.
- **`references/toolkit-export-sanitisation.md`** — How to create a clean role-based export of a completed toolkit for SharePoint/corporate distribution, stripping personal names to role titles.
- **`references/meeting-tasker-deliverable-pattern.md`** — Workflow for building meeting-tasker deliverables (DOR matrices, timelines, compliance gate briefings) from dumped meeting screenshots. Includes image extraction strategy, deliverable type catalog, and the July 2026 Aecon example (15 images → 2 action items → HTML briefing with DOR matrix + JV-to-audit timeline + BD lead-time reference card).
- **`references/cmmc-timeline-pptx-executive-deck-pattern.md`** — Complete 10-slide PPTX deck pattern for CMMC certification timeline presentations to executive leadership (Sr. Director level). Covers: slide-by-slide structure, Midnight Executive dark palette with hex codes, Gantt chart pptxgenjs gotchas (text-on-bar minimum widths, deadline marker placement, bar color visibility), BD lead-time reference card pattern, decisions-required table with status badges, and the pre-build research workflow (parallel agent review of call recordings for executive context before building). From the July 2026 Brian Gregorio Aecon FCS deck.
- **`references/compliance-methodology-naming-research.md`** — Industry analysis of how leading CMMC consultants, Big 4 advisory firms (Deloitte, KPMG, Accenture, PwC, EY), major compliance assessors (Coalfire, Schellman), and standards bodies (NIST CSF 2.0 Govern/Identify/Protect/Detect/Respond/Recover, ISO 27001 PDCA, NIST RMF, SOC 2) name their gap-to-audit methodology phases. Covers recurring phase vocabulary ranked by industry adoption, common modifiers (Readiness, Gap, Pre-, Continuous, Mock, Self-), branded framework names, differentiation strategies, and naming patterns by firm type. Load this when naming a compliance methodology, choosing phase names for a client framework, competitively positioning a compliance offering, or writing marketing/proposal language about a methodology.
- **`references/cmmc-competitive-landscape-2026.md`** — Full competitive analysis of the CMMC
  compliance product market as of July 2026. Covers: FutureFeed (pricing, feature set, user
  base), PreVeil (pricing tiers, GCC High alternative positioning, PreVeil Pass for SMEs),
  the GCC High vs lightweight approach analysis (three infrastructure tiers), Phase II
  suspension market window, competitive pricing benchmarks ($100-450/mo range), and HARBOR
  portfolio mapping to CMMC product opportunity. Load this when researching the CMMC
  product market, pricing a CMMC SaaS offering, evaluating build-vs-buy, or positioning
  against FutureFeed/PreVeil.
- **`references/cmmc-l2-competitive-landscape-2026-07.md`** — Condensed competitive landscape
  analysis for CMMC L2 Self-Assessment compliance enablement targeting 1-10 employee federal
  contractors. Covers 6 competitor profiles (PreVeil $450/mo, Cuick Trac, Summit 7 NCODE,
  Exostar, FutureFeed, Totem), TAM estimates from SBA data (120K DIB small businesses,
  30K-50K micro-contractors), Phase II suspension impact analysis (July 13, 2026), and 6
  underserved market gaps. Also includes confirmed-accessible competitor URLs for web_extract
  research, SBA cost estimates ($388K-$594K), and strategic recommendations. Load this when
  researching the CMMC self-assessment vendor market or evaluating competitive positioning
  for a micro-business compliance product.
- **`references/federal-laptop-hardware-compliance.md`** — Condensed framework crosswalk for federal laptop hardware compliance: CMMC L2, NIST 800-171 Rev 3 controls (verified via NIST HTML extraction), DOD IL-2/4/5 requirements, DISA Windows 11 STIG v2r8, FedRAMP customer responsibility, Intune/Autopilot management, EPEAT/Energy Star sustainability, minimum hardware spec, recommended secured-core models (Dell/HP/Lenovo/Microsoft), and deployment stack build order. Load this when researching hardware standards for federal contracts, answering "what laptop should we buy for CMMC," or building procurement specs for GCC High endpoints.
- References directory also contains: `rev-3-transition-research.md`, `cmmc-entity-scope-and-structure.md`, `cmmc-competitive-landscape-2026.md`, `c3pao-assessment-personas.md`, `foci-and-cmmc-strategy.md`, `dod-cio-bot-detection.md`.
- **`scripts/qa-review-toolkit.sh`** — Reusable full-audit QA review script for review-only mode.\n- **`references/vast-ai-gpu-cmmc-analysis.md`** — Vast.ai GPU infrastructure CMMC L2 gap analysis (July 2026). 110-control mapping for bare-metal GPU rentals. 50 GAP controls, 6 infrastructure options, hybrid architecture recommendation.
- **`scripts/rebuild-control-matrix.py`** — One-shot script: extracts full control text from NIST 800-171 Rev2 PDF via `pdftotext -raw`, rebuilds `Control-Implementation-Matrix.csv` with all 110 controls (fixing truncation), and optionally applies client-specific implementation examples from a dict. Usage: `python3 scripts/rebuild-control-matrix.py`
- **`templates/control-mapping-template.md`** — Template for control-to-document mapping (110 controls mapped to SOP/evidence/data flow)

## Usage Example

**For a new CMMC L2 effort:**

1. **Start with the Scope Determination** — Open `templates/CMMC-L2-Scope-Determination.md` and define the enclave boundary, in-scope systems, CUI data flow, and external service providers.

2. **Populate the SSP** — Open `templates/SSP-Template.md` and fill Section 5 for all 110 controls with implementation descriptions, responsible roles, evidence artifact locations, and last assessed dates.

3. **Run a Gap Assessment** — Use `templates/Control-Implementation-Matrix.csv` to mark each control's implementation status. This becomes your baseline POA&M.

4. **Create Your POA&M** — Open `templates/POAM-Tracker.csv` and create entries for all "Not Implemented" or "Partially" controls.

5. **Implement Controls per SOPs** — Go into each `control-families/####-[FAMILY]/` folder and follow the procedures in the SOP. Collect evidence artifacts as specified.

6. **Operate the Program** — Use `Cybersecurity-Program-Checklist.csv` to track monthly/annual procedures. Update POA&M and evidence continuously.

## References

### NIST & CMMC Official Sources
- NIST SP 800-171 Rev 2 — https://csrc.nist.gov/pubs/sp/800/171/rev/2/final
- NIST SP 800-171A Rev 2 — https://csrc.nist.gov/pubs/sp/800-171a/rev/2/final
- NIST SP 800-171 Rev 3 (final, May 14, 2024) — https://csrc.nist.gov/pubs/sp/800/171/r3/final
- 32 CFR Part 170 (CMMC Final Rule, October 15, 2024) — eCFR blocks bots; use Cornell LII mirror:
  `https://www.law.cornell.edu/cfr/text/32/part-170` (per-section: `.../32/170.NN`)
- CMMC 2.0 — https://www.acquisition.gov/cmmc

### CMMC Assessment & Marketplace
- CMMC Assessment Process (CAP) — DoD CIO website (may block automated access)
- CMMC Accreditation Body (CyberAB) — https://www.cyberab.org (may block automated access)
- CMMC Marketplace — https://www.cmmcmarketplace.org
- SAM.gov (SPRS) — https://sam.gov (may block automated access)

### Industry Analysis (for Rev 3 transition research)
- cmmc-hub.com — CMMC analysis with Rev 2 vs Rev 3 comparison
- CMMC Command (cmmccommand.org) — Transition timeline and analysis
- Secureframe (secureframe.com) — Rev 2 vs Rev 3 changes
- Field Ledger (fieldledger.us) — Control count and ODP analysis
- Cybriant (cybriant.com) — Determination statement analysis

### Design
- Thariq/html-effectiveness aesthetic — https://github.com/Thariq/html-effectiveness