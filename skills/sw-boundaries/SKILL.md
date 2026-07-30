---
name: sw-boundaries
description: "4-zone product boundary from Book 1 Chapter 12. Classifies features into Zone 1 (Core, >50% demand) / Zone 2 (Configurable, >50% demand + safe) / Zone 3 (Optional Modules, 20-40% demand) / Zone 4 (Excluded, <20%). Outputs 5-CLIN structure, ATO boundary change cost ($75K-150K + 2-4 mo) for Zone 4 promotion, exception criteria (first-in-segment / reference-quality / 3x deal value), ISSO consultation gate for new data flows. Use after /sw-70-30 or as part of /shrink-wrap Build phase."
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: product boundaries, 4 zones, ATO boundary change, Ch 12 boundaries
---

# /sw-boundaries - Product Boundaries That Hold

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-12 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-12.md`

## Execution

### Step 1: Resolve candidate input + feature roster with demand evidence
Expect: feature list with customer-demand evidence (customer counts, win/loss data, named customer requests).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/04-build/ch12-boundaries.html`
- Direct: `experiments/single-instrument/sw-boundaries/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel

Lens-conditional auditor resolution for boundary-expansion flags:

| HARBOR_LENS | Auditor persona |
|---|---|
| federal | persona-fedramp-auditor (ATO boundary impact) |
| commercial-us / -eu / -uk | persona-iso-soc2-auditor (SOC 2 audit re-scoping impact) |
| sector-healthcare | persona-iso-soc2-auditor + persona-sector-healthcare (BAA chain impact) |
| sector-finance | persona-iso-soc2-auditor + persona-sector-finance |
| sector-energy | persona-sector-energy |
| international | persona-fedramp-auditor (FedRAMP-equivalent baseline) |

Then dispatch:
- persona-product-owner (primary - owns zone classification with demand evidence)
- persona-engineering-lead (feasibility of each zone classification)
- persona-sales-lead (validate Zone 1-3 against actual customer asks; flag Zone 4 promotion requests)
- {resolved auditor persona from table}

### Step 4: 4-zone classification with explicit demand percentages
- Zone 1 (Core): >50%
- Zone 2 (Configurable): >50% + safely configurable
- Zone 3 (Optional Modules): 20-40%
- Zone 4 (Excluded Scope): <20%
Demand evidence must be cited per feature (not judgment-only).

### Step 5: 5-CLIN structure
0001 Subscription / 0002 Implementation / 0003 Optional Modules / 0004 Custom Dev T&M / 0005 Custom Dev Maintenance T&M (customer-funded indefinitely).

### Step 6: ATO boundary change cost for Zone 4 promotion
Surface $75K-$150K + 2-4 months whenever Zone 4 promotion involves new integration, new data flow, or new control implementation.

### Step 7: Exception criteria check (3 valid criteria for Zone 4 -> Zone 1/2/3 promotion)
First-in-segment / Reference-quality / 3x typical deal value. ONLY these three. "Strategic exception" without one of these is invalid.

### Step 8: ISSO consultation hard gate
Any feature involving new data flows -> mandatory ISSO consultation BEFORE zone assignment. Not advisory.

### Step 9: Write HTML + return structured summary
```json
{"candidate_slug": "...", "zone_classifications": {...},
 "zone_4_promotion_requests": [...], "exception_validity": [...],
 "isso_consultation_flagged": [...], "5_clin_structure": [...],
 "output_path": "...", "next_skill": "sw-pricing-model"}
```

## Constraints
- Demand percentages must be evidenced per feature, not judgment
- 5 CLINs (not 4) - CLIN 0005 (Custom Dev Maintenance T&M) is a distinct line
- Exception criteria are exclusive - no "strategic" overrides
- ISSO consultation is hard gate, not advisory
