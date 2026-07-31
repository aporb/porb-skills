# PWS Role & Deliverable Mapping Template

> Use this template BEFORE writing any capability section. Fill it out from the PWS text, then build the response's Capabilities section from the filled-out template.

## Step 1: Extract All PWS Specialist Roles

List every role the PWS explicitly names. For each, classify as Covered, Gap, or Subcontract.

| # | PWS Role | Key Duties | Covered? | Who / How |
|---|---|---|---|---|
| 1 | Program Manager/Project Manager | Overall execution, stakeholder engagement, schedule/risk, KPIs, SOPs | Covered | [Name], [qualification], PMP/FAC-P/PM commitment |
| 2 | Acquisition Specialist | SOWs, IGCEs, acquisition plans, FAR/HHSAR compliance | Subcontract | Former 1102 series, FAC-C certified |
| 3 | Finance Specialist | Billing, budget tool, financial reports, cost analysis | Gap/Covered | [Name if covered, or "Seeking subcontract"] |
| 4 | Program Outreach & Communication Specialist | Newsletters, briefings, training, surveys, vendor days | Gap/Covered | [Name if covered, or mitigation plan] |
| 5 | Emerging Technology Specialist | Tech evaluation, market research, licensing strategies | Covered | [Name], [qualification] |
| 6 | License Specialist | Full lifecycle, portals, GSA pricing, license consolidation | Subcontract | 10+ yr enterprise licensing, Microsoft/Oracle |
| 7 | VMO Application/Site Administrator | Maintain VMO app and site, data accuracy | [Status] | [Mitigation] |
| 8 | SAM Team Coordinator | Work with SAM team for license inventory/utilization | [Status] | [Mitigation] |

**Coverage check:** Count rows marked "Covered" vs total. If >50% are Gap/Subcontract, the response's team section needs explicit staffing plans with named candidates or firms.

## Step 2: Extract All PWS Task Areas

| # | PWS Section | Task Area | Key Sub-Requirements | Addressed How |
|---|---|---|---|---|
| 1 | C.5.1 | Program Support | Admin mgmt, kickoff, PM, financial control, data analytics, outreach | [Brief description] |
| 2 | C.5.2 | Enterprise & Acquisition Management | Acquisition support, BPA/ELA/order management, contract sustainment | [Brief description] |
| 3 | C.5.3 | Out-Going Transition Support | 30-day transition-out plan, train successor contractor | [Brief description] |
| 4 | C.5.4 | Deliverables | 13 specific recurring deliverables (see Step 3) | [Brief description] |
| 5 | C.5.8 | Security Requirements | FIPS 199, NIST 800-53, CUI, Privacy Act, PIV/HSPD-12 | [Brief description] |

## Step 3: List All Deliverables

| # | Category | Deliverable | Frequency | Addressed How |
|---|---|---|---|---|
| 1 | Contract & Vendor Mgmt | BPA/ELA Tracking Report | Monthly | |
| 2 | Contract & Vendor Mgmt | Vendor Performance Report | Quarterly | |
| 3 | Financial Management | Software Spend & Cost Analysis | Monthly/Quarterly | |
| 4 | Financial Management | Cost Savings & Avoidance Report | Quarterly | |
| 5 | Compliance & Audit | Audit Readiness Package | As Required | |
| 6 | Compliance & Audit | Compliance Status Report | Quarterly | |
| 7 | Renewal & Strategic Planning | Software Renewal Plan (12-24 mo) | Quarterly | |
| 8 | Renewal & Strategic Planning | Pre-Renewal Assessment | As Required | |
| 9 | Reporting & PM | Program Status Report | Monthly | |
| 10 | Reporting & PM | Executive Briefings | Monthly/Quarterly | |
| 11 | Reporting & PM | Dashboards & Metrics Reporting | Continuous/Monthly | |
| 12 | Process & Governance | Standard Operating Procedures | Initial + Updates | |
| 13 | Transition | 30-Day Transition-Out Plan | At Contract End | |

## Step 4: Check Emphasis Proportions

Before writing, estimate:
- % of PWS requirements that are about [Topic A]: ___%
- % of PWS requirements that are about [Topic B]: ___%
- % of PWS requirements that are about AI/automation: ___%

The response's page allocation should roughly mirror these proportions. If AI is 2% of PWS requirements, it should be ~10% of the response at most — not 80%.

## Anti-Pattern (from real session)

**HHS VMO v3 (score: 42/100 — FAIL):**
- PWS: 8 specialist roles, 13 deliverables, 5 task areas. AI = 1 sentence in "Additional Requirements."
- Response: 80% about AI agent infrastructure. ~30% PWS coverage. 6 of 8 roles unaddressed. 12 of 13 deliverables missed.
- Fix (v4): Led with management consulting understanding. Mapped all 8 roles and 13 deliverables explicitly. AI described as augmentation, not replacement. Score would land in 65-75 range.

## Post-Response Verification

After writing, run `grep` against the draft for:
- Every PWS role name → should appear at least once
- Every deliverable name → should appear in a table or paragraph
- Every task area reference (C.5.1, C.5.2, C.5.3, C.5.4, C.5.8) → should be addressed
- False claims from the overstatement checklist → should return zero matches