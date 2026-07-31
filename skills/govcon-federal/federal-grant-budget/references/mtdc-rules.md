# MTDC Rules — Condensed Regulatory Reference

## Definition (2 CFR 200.1)

Modified Total Direct Cost (MTDC) means all direct salaries and wages, applicable fringe benefits, materials and supplies, services, travel, and up to the first $50,000 of each subaward (regardless of the period of performance of the subawards under the award). MTDC **excludes** equipment, capital expenditures, charges for patient care, rental costs, tuition remission, scholarships and fellowships, participant support costs, and the portion of each subaward in excess of $50,000.

## What's Included in MTDC

| Category | Included? | Rule |
|---|---|---|
| Personnel (A) | ✅ FULL | All direct salaries and wages |
| Fringe Benefits (B) | ✅ FULL | All applicable fringe benefits |
| Travel (C) | ✅ FULL | All travel costs |
| Supplies (E) | ✅ FULL | All materials and supplies |
| Other Direct — Services | ✅ FULL | Professional services, cloud, software, translation, venues |
| Subawards — First $50K each | ✅ $50K per sub | Per subaward, not per prime |
| Subawards — Over $50K each | ❌ EXCLUDED | $50K cap per subaward |

## What's Excluded from MTDC

| Category | Excluded? | Rule |
|---|---|---|
| Equipment (D) | ❌ ALL | Items ≥$10K/unit, useful life >1 year |
| Participant Support Costs | ❌ ALL | Per 2 CFR 200.456 |
| Capital Expenditures | ❌ ALL | Buildings, facilities, major renovations |
| Rental Costs | ❌ ALL | Office/equipment lease |
| Tuition Remission | ❌ ALL | Not applicable to for-profits |
| Scholarships/Fellowships | ❌ ALL | Not applicable to for-profits |

## Key Regulatory Citations

| Rule | Citation | Notes |
|---|---|---|
| MTDC definition | 2 CFR 200.1 | The authoritative definition |
| De minimis indirect rate | 2 CFR 200.414(f) | 15% on MTDC, available to orgs without NICRA |
| Personnel compensation | 2 CFR 200.430 | Reasonable, allocable compensation |
| Fringe benefits | 2 CFR 200.431 | Actual costs or approved rate |
| Travel costs | 2 CFR 200.474 | Fly America Act for international |
| Equipment threshold | 2 CFR 200.1 | $10,000/unit, useful life >1 year |
| Participant support | 2 CFR 200.456 | Defined separately from Other Direct |
| Subrecipient monitoring | 2 CFR 200.331–333 | Classification, risk assessment, monitoring |
| Single Audit | 2 CFR 200 Subpart F | Required when federal awards >$1M |
| Cost Accounting Standards | 48 CFR Part 30 | Applies to for-profits |
| Contract Cost Principles | 48 CFR Part 31 | Allowability criteria |
| Buy America | 2 CFR 200.322 | Preference for domestic products |
| Trafficking in Persons | 2 CFR Part 175 | Certification when >$500K foreign |
| Tiebreaker preference | EO 14332, §4(b)(iii) | Lower indirect rate wins ties |

## Common Budget Build Errors

1. **Counting only one subaward's $50K cap.** MTDC includes the first $50K of EACH subaward.
2. **Including participant support costs in MTDC base.** They're explicitly excluded.
3. **Including equipment in MTDC base.** All equipment is excluded per 2 CFR 200.1.
4. **Using wrong fringe rate.** 28% is common for small businesses; 35%+ is unusual.
5. **Forgetting to exclude subaward portions over $50K.** For a $1.5M subaward, only $50K goes into MTDC.
6. **Applying indirect to total direct instead of MTDC.** This inflates indirect costs and may exceed ceiling.
7. **Rounding inconsistently.** All amounts must be whole dollars in federal budgets. Round each category after final calculation.

## Formula Reminder

```
MTDC = Personnel + Fringe + Travel + Supplies + (num_subs × $50,000) + OD_Services

Direct = Personnel + Fringe + Travel + Supplies + Equipment + Contractual + OD_Total

Indirect = 0.15 × MTDC  (or negotiated rate)

Total = Direct + Indirect
```

The closed-form solution for Personnel when fringe = 28% and indirect = 15%:
```
P = (Total - fixed - 0.15 × mtdc_fixed) / 1.472

where:
  fixed = Travel + Supplies + Equipment + Contractual + OD_Total
  mtdc_fixed = Travel + Supplies + (num_subs × 50,000) + OD_Services
```