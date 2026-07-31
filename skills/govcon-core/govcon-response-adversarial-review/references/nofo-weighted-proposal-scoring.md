# NOFO-Weighted Proposal Scoring

For full federal proposals (cooperative agreements, grants, BAAs) where the NOFO publishes explicit evaluation criteria with weights. Use this scoring methodology instead of the generic 5-dimension scoring when reviewing proposals for competitive range.

## Methodology

### Step 1: Extract NOFO Evaluation Criteria
Parse the NOFO's evaluation section to extract:
- Each criterion name (exact wording)
- Each criterion weight (as published — 30%, 20%, etc.)
- Any sub-criteria or tiebreaker provisions

### Step 2: Score Each Criterion 0-100
Score independently per criterion on the 0-100 scale used by federal evaluation panels:
- **80-100:** Outstanding — exceeds requirements
- **70-79:** Good — meets all requirements, some strengths
- **50-69:** Acceptable — meets minimum requirements
- **30-49:** Marginal — significant weaknesses
- **<30:** Unacceptable — fails to meet minimum

### Step 3: Compute Weighted Total
Multiply each criterion score by its weight, sum for overall. Report as weighted score/100.

### Step 4: Classify Findings
| Tier | Definition |
|---|---|
| **CRITICAL (P0)** | Disqualifying or would cause ≥20 point loss on any criterion |
| **MAJOR (P1)** | Would cause significant point loss (10-20 points on a criterion) |
| **MINOR (P2)** | Would cause minor point loss (<10 points) |

### Step 5: Before/After Scorecard
When fixes are applied, produce a before/after comparison table showing the score delta. This is the key deliverable for stakeholders — it proves the fix cycle was worth running.

## Example: DFOP0018157 (State Dept Cooperative Agreement)

| Criterion | Weight | Before | After (est.) | Delta |
|---|---|---|---|---|
| Quality & Achievability | 30% | 38 | 75+ | +37 |
| Experience & Qualifications | 30% | 25 | 65+ | +40 |
| Cost & Budget | 20% | 55 | 80+ | +25 |
| Long-Term Impact | 15% | 60 | 70+ | +10 |
| Monitoring & Evaluation | 5% | 52 | 75+ | +23 |
| **Weighted Total** | | **42** | **72+** | **+30** |

## Common Full-Proposal Findings

- **Personnel in narrative not in budget:** This is a CRITICAL finding. Named key personnel in the narrative MUST appear in the budget with matching FTE and salary. An evaluator cannot score personnel who are not budgeted.
- **Conflicting numbers across documents:** MVP dates, training targets, accuracy metrics that differ between narrative/SOW/budget/M&E plan. These must be identical — pick ONE authoritative value and propagate everywhere.
- **Fringe rate fabricated for new entity:** A 74-day-old LLC with no payroll cannot claim "actual benefit costs" as the basis for a 28% fringe rate. Use BLS-benchmarked rates or statutory minimums.
- **For-profit credibility:** For-profit entities in a nonprofit-dominated space (e.g., CFDA 19.317) must address the credibility gap head-on. Acknowledge it in the organization introduction. Don't pretend to be a nonprofit.
- **Missing sub-awardee:** A "$1.5M sub-awardee TBD" is unscorable — the evaluator has zero information about a quarter of the budget. Identify or restructure.