---
name: federal-grant-budget
description: Build precise, regulation-compliant budgets for federal assistance awards (grants and cooperative agreements). Covers MTDC calculation with the 15% de minimis indirect rate, line-item structuring for DOS/agency Excel templates, budget narrative writing, SF-424A mapping, and exact-total solving via iterative computation. For any federal NOFO/NOFA requiring a detailed budget under 2 CFR 200.
---

# Federal Grant Budget Building

Build complete, regulation-compliant budget packages for federal assistance awards — cooperative agreements and grants under 2 CFR 200 Uniform Guidance. The deliverable is always three components: a **detailed line-item budget** (Excel structure), a **budget narrative** (Word structure, justifying every line), and an **SF-424A mapping** (matching OMB cost categories A–K).

## When to Use

- Any federal NOFO/NOFA that requires a detailed budget, budget narrative, and SF-424A
- Cooperative agreements (substantial involvement) as well as standard grants
- For-profit recipients (cost recovery only, no profit/fee) using the 15% de minimis indirect rate
- Non-profit recipients with or without NICRA
- Any budget where Modified Total Direct Cost (MTDC) calculations are required

## Core Methodology: Solve Exact Total via MTDC Equation

The hardest part of federal grant budgeting is making the total hit exactly the NOFO ceiling while respecting MTDC exclusions (equipment, participant support, subaward portions over $50K) and the 15% de minimis rate. Manual iteration is error-prone. Use the solver.

### Step 1: Set Fixed (Non-Personnel) Budget Categories

Fix all categories except Personnel first. Personnel becomes the dependent variable solved from the total constraint.

**Fixed categories (choose defensible numbers):**
- **Travel:** Based on real trip counts × per-trip cost estimates (airfare per Fly America Act, lodging/M&IE per published per diem rates)
- **Equipment:** Items ≥$10,000/unit with useful life >1 year. Justify each purchase. Excluded from MTDC.
- **Supplies:** Items <$10,000/unit. Included in MTDC.
- **Contractual (subawards):** Three subawards is a good default pattern. Only the first $50,000 of EACH subaward counts toward MTDC.
- **Other Direct — Services:** Cloud, software, translation, venues, audit. Included in MTDC.
- **Other Direct — Participant Support:** Travel/stipends for foreign officials or program participants. Excluded from MTDC.

**Default split (for a ~$6M cooperative agreement):**
| Category | Typical % of Direct | Notes |
|---|---|---|
| Personnel | 30–35% | Solve from total equation |
| Fringe | 8–10% | 28% of personnel is common for small businesses |
| Travel | 7–10% | International-heavy programs |
| Equipment | 2–4% | Front-load Year 1 |
| Supplies | 2–4% | Laptops, devices, office, sub-$10K software |
| Contractual | 30–40% | Largest for tech-heavy programs (app dev, etc.) |
| Other Direct | 10–12% | 500K services + 120K participant support common |
| Indirect | 8–10% | 15% of MTDC typically falls in this range |

### Step 2: Solve for Personnel Using the MTDC Equation

The relationship:
```
Total = Direct + Indirect
Direct = P + F + T + S + E + C + O
Fringe = rate × P  (typically 0.28)
Indirect = 0.15 × MTDC
MTDC = P + F + T + S + (num_subs × 50,000) + OD_services
```

This resolves to:
```
Total = 1.472P + fixed + 0.15 × mtdc_fixed
P = (Total - fixed - 0.15 × mtdc_fixed) / 1.472
```

Where:
- `fixed` = T + S + E + C + O_total (everything that doesn't depend on P)
- `mtdc_fixed` = T + S + (num_subs × 50,000) + OD_services

Run `scripts/solve-budget.py` with the fixed values to find exact P. The script handles rounding to whole dollars.

### Step 3: Allocate Personnel Across Positions

Distribute solved P across reasonable positions. Typical structure for a ~$1.7M personnel pool over 24 months:

- 1× Program Director (1.0 FTE, ~$140K/yr)
- 1× Technical Lead per workstream (1.0 FTE, ~$110–125K/yr)
- 1–2× Analysts/Specialists (1.0 FTE, ~$80–105K/yr)
- 1× Technical PM (1.0 FTE, ~$110–120K/yr)
- 0.5× Finance/Grants Manager
- 0.5× IT/Infrastructure Engineer
- 0.5× Training Specialist
- 0.5× Domain SME

Total FTE: 8.0–10.0. The last position absorbs the residual to make the sum exact.

### Step 4: Build the Budget Narrative

Every line item needs: **what it is, how the amount was derived, what specific activities it supports, and what regulation authorizes it.** Structure:

1. **Personnel:** Position-by-position with BLS salary justification and 2 CFR 200.430 citation
2. **Fringe:** Component breakdown (FICA, health, workers' comp, etc.) with effective rate calculation
3. **Travel:** Trip counts × per-trip costs, Fly America Act compliance
4. **Equipment:** Per-item justification over $10K threshold
5. **Supplies:** Sub-$10K items with quantities
6. **Contractual:** Each subaward's scope, deliverables, selection method, and MTDC impact
7. **Other Direct:** Separate services (MTDC-eligible) from participant support (excluded)
8. **Indirect:** MTDC base calculation table, 2 CFR 200.414(f) citation, tiebreaker advantage per EO 14332

### Step 5: Map to SF-424A

Populate Sections A–F. Key mappings:

| SF-424A Section | What Goes There |
|---|---|
| Section A | One row: program title, CFDA 19.317, federal amount, $0 non-federal |
| Section B (6a–6k) | Direct mapping from budget categories A–K |
| Section C | All zeros (no cost share unless voluntarily offered) |
| Section D | Quarterly cash needs (Year 1 = ~48% of total, split across 4 quarters) |
| Section E | Year 2 quarterly cash needs (~52% of total) |

## Critical Rules to Encode

### MTDC Exclusions (2 CFR 200.1)
**ALWAYS excluded from MTDC base:**
- Equipment (Category D) — ALL of it
- Participant support costs — ALL of it (portion of Category H)
- Portion of each subaward exceeding $50,000
- Capital expenditures, rental costs, tuition, scholarships

**ALWAYS included in MTDC base:**
- Personnel, Fringe, Travel, Supplies — ALL
- First $50,000 of each subaward
- Services portion of Other Direct Costs

### For-Profit Restrictions
- No profit or fee in ANY line item — cost recovery only
- 15% de minimis available if no NICRA (2 CFR 200.414(f))
- If no NICRA AND not using de minimis: allocate indirect costs directly to categories
- All subrecipients AND contractors subject to same no-profit rule
- Cost accounting per 48 CFR Part 30 (CAS) and 48 CFR Part 31 (Cost Principles)

### Format Requirements (Department of State)
- Budget font: Calibri 12pt
- Paper: 8.5×11 letter (NOT legal)
- All amounts in whole U.S. dollars (no cents)
- Use DOS-provided Excel template with 5 tabs: Budget Guidelines, Summary Budget, Detailed Budget, SubRecipient Budget, MTDC Calculation
- Narrative font: Calibri 12pt (separate from proposal narrative's 15pt Open Sans)

### DOS Template: Personnel Structure (Tab 3 — Detailed Budget)
The DOS Detailed Budget Template expects personnel split into two subcategories:

| Subcategory | What Goes Here |
|---|---|
| **A.1 HQ-Based Personnel** | Program Director, Technical Lead, Compliance/Contracts Manager, Operations Manager, MEL Specialist, IT/Cloud Engineer — positions primarily based at the organization's headquarters |
| **A.2 Field Personnel** | Data Analytics Lead, Senior Data Analyst, Industry Engagement Lead, Industry Engagement Advisor, Training & Curriculum Specialist — positions deployed to partner countries for in-country work |

Each field position should list deployment regions (EAP, WHA, NEA, EUR). Travel costs for field personnel are budgeted separately under Category C.

### DOS Template: Travel Structure (Tab 3 — Detailed Budget)
The DOS template expects travel organized into three subcategories:

| Subcategory | Content | Example Detail Level |
|---|---|---|
| **C.1 International Travel** | Round-trip airfare between US and partner countries. Each line: traveler role, from/to, purpose, trips/year, cost per airfare, 24-month cost. | "Program Director (Henderson), Columbia SC → EAP/WHA/NEA/EUR capitals, EXBS coordination, 4 trips/year, $4,200/RT, $33,600" |
| **C.2 Country Travel** | In-country lodging, per diem (M&IE), and ground transportation. Each line: traveler role, country/region, purpose, trips, nights, lodging/night, M&IE/day, ground transport, cost/trip, 24-month cost. | "Data Analytics Lead, EAP (Singapore, Malaysia), trade data assessment, 8 trips, 8 nights, $165/nt lodging, $95/day M&IE, $400 ground, $2,480/trip, $19,840" |
| **C.3 Domestic/Monitoring Travel** | Domestic trips to Washington DC for coordination meetings, conferences, program reviews. Each line: traveler role, from/to, purpose, trips/year, cost/trip, 24-month cost. | "Program Director, Columbia SC → Washington DC, ACN/EXBS coordination, 6 trips/year, $1,200/trip, $14,400" |

Verify: C.1 + C.2 + C.3 must equal total Travel (Category C). C.1 + C.2 should equal international travel budget. All airfare must comply with Fly America Act.

### Required De Minimis Election Statement (Attachment H)
Organizations without a NICRA must submit a signed statement in Attachment H:
1. Certifying the organization has never had a federally negotiated indirect cost rate
2. Electing the 15% de minimis rate per 2 CFR 200.414(f)
3. Committing to apply this rate consistently across all federal awards

This is NOT optional — a blank Attachment H may be rejected. Create a one-page signed PDF.

### Year-by-Year MTDC Documentation
The DOS MTDC Calculation tab (Tab 5) expects a year-by-year breakdown showing exactly which cost elements drive the indirect cost split across Year 1 and Year 2. Document assumptions about when contractual MTDC-eligible portions and services costs are incurred. The year split must be defensible — a simple 50/50 split with no justification will be questioned.

## Pitfalls

- **Using one subaward's $50K instead of per-subaward:** Each subaward contributes its own first $50K to MTDC. With 3 subawards, that's $150K toward MTDC, not $50K. Getting this wrong shifts the entire budget.
- **Forgetting participant support exclusion:** Mark it clearly in Other Direct but run a separate subtotal for MTDC purposes.
- **Rounding the indirect after rounding direct:** Always compute indirect as `round(0.15 × MTDC)` AFTER all direct costs are finalized. Re-verify total.
- **Too-high fringe rate:** 28% is typical for small businesses. Rates above 35% raise eyebrows. Itemize the components.
- **Subrecipient vs. contractor classification:** DOS won't advise. Both are subject to no-profit rule regardless of classification. Classify per 2 CFR 200.331 criteria.
- **Missing the tiebreaker:** Per EO 14332, lower indirect rate wins ties. The 15% de minimis is likely the floor — mention this in the narrative.
- **Fringe rate can't be "actual costs" for a new entity:** A 74-day-old LLC with no employees, no payroll history, no insurance contracts, and no retirement plan cannot claim a 28% fringe rate "based on actual benefit costs." Use BLS-benchmarked rates for the entity's geographic area, or use statutory minimums (FICA 7.65%, FUTA 0.6%, SUTA new employer rate) producing ~9-10%. A fabricated rate is a cost proposal irregularity the evaluator will flag.
- **Personnel in budget must match narrative:** Every named key person in the narrative (e.g., Porbanderwala, Payne, Frawley) MUST appear in the budget with matching FTE and salary. The #1 adversarial review finding is "Key personnel in narrative DO NOT match budget." Fix the budget file first, then propagate changes to narrative and supporting docs.

## Verification

Before delivering, run `scripts/solve-budget.py` with the final fixed values and verify:
- Total = target ceiling with zero delta
- Each category subtotal matches its line items
- MTDC excludes equipment, participant support, and subaward excess
- Year split sums to total
- No cents appear anywhere

## Supporting Files

- `scripts/solve-budget.py` — Exact solver for personnel from fixed categories and MTDC equation
- `references/mtdc-rules.md` — Condensed regulatory reference for MTDC calculation under 2 CFR 200