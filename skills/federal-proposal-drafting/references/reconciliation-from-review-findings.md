# Reconciling Multi-Document Proposals After Adversarial Review

When an adversarial review produces a prioritized fix list (P0/P1/P2) spanning three or more proposal documents (narrative, budget, supporting docs), follow this systematic reconciliation workflow. The goal is to fix every inconsistency while maintaining budget arithmetic integrity.

## Core Principle: Budget Integrity First

**The budget file is the master arithmetic source.** Changes to any dollar figure cascade through fringe benefits, MTDC, indirect costs, year splits, SF-424A mappings, and all summary tables. Always start fixes in the budget file, then propagate narrative and supporting doc changes.

### Personnel/Budget Reconciliation (Most Common P0)

When the narrative names key personnel that don't appear in the budget:

1. **Map narrative names to budget positions.** Identify exact matches, partial matches, and gaps.
2. **Keep the personnel TOTAL unchanged when possible.** Changing the total from (say) $1,743,546 to $2,040,000 forces recalculation of fringe, MTDC, indirect, year splits, SF-424A, and every summary table. It's far cleaner to redistribute within the existing envelope.
3. **If keeping the total, adjust individual rates** to sum to the original total. Use SC/regional BLS rates with a domain-expertise escalation factor (6-8%) to justify cost reasonableness.
4. **Add missing positions and remove/reduce others** to hold the line.
5. **Update the budget narrative** (Part 2 of the budget package) with full position descriptions for every renamed/added position.
6. **Update the narrative's governance section** to match.

### Equipment-to-Cloud Conversion

When the adversarial review flags on-premises equipment contradictory to a cloud architecture:

1. Zero out Equipment (Category D).
2. Add the equipment amount to cloud hosting in Other Direct Costs (Category H), increasing the monthly rate.
3. The math constraint: net direct cost change = (cloud increase) - (equipment removed). But equipment was excluded from MTDC while cloud services ARE in MTDC. So MTDC increases by the full cloud increase, and indirect costs increase by 15% of that.
4. Solve: D + 0.15M = $5,901,000 (the ceiling). Keep additional ODC services modest enough to stay under the ceiling.
5. Add data labeling and independent evaluation as new ODC line items to address review findings.

### Fringe Benefits Math Fix

Common failure: components don't sum to stated total. The original says "28% effective rate" but components sum to 27.1% or 28.04%.

1. Set the health insurance line item as the balancing figure.
2. Compute: health = (total fringe) - (FICA + WC + UI + retirement + other).
3. Divide by (FTE count × 24 months) to get the monthly rate.
4. Verify the per-FTE monthly rate is market-competitive for the entity's actual location.

## Edit Order: File-by-File

### 1. Budget-Package.md (Numbers first)
- Personnel table (rename positions, adjust rates to hold total)
- Fringe benefits (recompute components to sum)
- Equipment ($0 if cloud-only)
- Other Direct Costs (added: cloud increase, data labeling, independent evaluation)
- MTDC base recalculation
- Indirect cost (15% de minimis on new MTDC)
- Year-by-year split with documented basis
- Annual budget split table
- Budget narrative Part 2 (position descriptions, fringe justification, equipment removal, cloud narrative)
- SF-424A mapping tables
- Budget narrative summary table
- Workstream crosswalk
- Attachment references (A-133 → Single Audit; NICRA → de minimis election statement)
- File naming conventions

### 2. Proposal-Narrative.md (Dates, targets, metrics, structure)
- Training targets (120→240 / 8→12)
- MVP delivery date (pick one: Month 9 is most realistic for complex AI dev)
- Accuracy metrics (single spec: top-1 only, specific threshold, specific category counts)
- Geographic classification (verify against State Dept regional bureau taxonomy)
- Henderson FTE (reconcile narrative 75% ↔ budget 1.0)
- Organizational structure (add MEL Specialist, match budget positions)
- Indicator table (update targets to match reconciled values)
- Governance section (match budget's named positions)
- Additional hires paragraph
- Schedule/milestone tables (update MVP date references)

### 3. Supporting-Documents.md (SOW compression + indicator alignment)
- **SOW compression:** Collapse Inputs/Outputs/Indicators into single-line bullets. Move detailed indicator targets to M&E Plan section. Target: ~2 pages formatted. Each activity becomes a single bold paragraph with targets in parentheses.
- Update MVP dates throughout (B-OUT-01, M4 milestone, Activity 2.1 outputs)
- Update accuracy specs (B-OUT-04, Activity 2.1 indicators)
- Update training targets (A-OUT-06, Activity 1.3 outputs)
- M&E Plan indicator tables: align with reconciled targets
- Milestone table: align dates

## Common Cross-Document Inconsistencies to Hunt

| Type | Budget | Narrative | SOW | Fix |
|---|---|---|---|---|
| MVP delivery date | Month 9 | Month 6 | Month 8 | Pick Month 9 |
| Training officials | — | 120/8 | 240/12 | Use 240/12 |
| Accuracy: metric | — | top-3 | top-5 | Use top-1 only |
| Accuracy: threshold | — | 80% | 85% | Use 80% top-1 |
| Accuracy: categories | — | 15 | 30 | 15 at MVP, 30 at v2.0 |
| Translation languages | 15 | 4 | 4 | Use 4 |
| Equipment | $150K | cloud-only | — | $0 equipment, cloud GPU |
| Geographic: Georgia | — | NEA | — | EUR (State Dept taxonomy) |
| Geographic: Ukraine | — | NEA | — | EUR |
| Personnel: Henderson FTE | 1.0 | 75% | — | 1.0 (both) |
| MEL Specialist | missing | not listed | 0.5 FTE | Add to budget + narrative |
| Attachment names | A-133 | — | — | Single Audit / 2 CFR 200 Subpart F |
| NICRA attachment | "Not applicable" | — | — | De minimis election statement |

## Post-Reconciliation Verification

After all edits, verify:
1. Budget grand total = exactly $5,901,000
2. Personnel total unchanged from original
3. Fringe components sum to stated total (verify each component calculation)
4. MTDC = correct sum of eligible categories
5. Indirect = 15% × MTDC (verify rounding)
6. Y1 + Y2 direct = total direct
7. Y1 + Y2 indirect = total indirect (splits must be documented)
8. SF-424A Section B totals match
9. All three docs use same MVP date, same training targets, same accuracy metrics
10. No "A-133" references remain