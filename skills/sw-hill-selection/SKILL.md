---

name: sw-hill-selection
description: Hill selection from Book 1 Chapter 6. Score Proceed candidates from S2P (Ch 5) on 4 filters (Market Access, Competitive Position, Authorization Alignment, Economics). 20-point max with viability floor 12. Outputs sequenced hill roadmap with 18-month commitment + 3-customer gate to second hill. Enforces concentration over diversification. Use after /sw-s2p-scorecard, as part of /shrink-wrap Architect phase, or to validate a Product
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate-list
arguments: candidates
model: sonnet
when_to_use: hill selection, choose the right hill, Ch 6 hill, sequenced roadmap
---

# /sw-hill-selection - Choosing the Right Hill

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-6 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-6.md`

## Execution

### Step 1: Resolve candidate list input
Expect input list of Proceed candidates from prior Ch 5 run. AskUserQuestion if missing.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/02-architect/ch6-hill-selection.html`
- Direct: `experiments/single-instrument/sw-hill-selection/$(date +%Y-%m-%d)-batch.html`

### Step 3: Dispatch personas in parallel
- persona-founder-investor (independent moat / defensibility)
- persona-market-analyst-<lens> (TAM math for Filter 4)
- persona-pricing-strategist (ACV achievability for Filter 4)
- persona-strategic-advisor (concentration vs diversification call)

### Step 4: Score each candidate on 4 filters (1-5 each)
Market Access / Competitive Position / Authorization Alignment / Economics.

### Step 5: Apply viability floor (12)
If all candidates score <12, return "no viable hill" rather than forcing. Orchestrator halts.

### Step 6: Pick selected hill (top scorer above floor)
Apply 18-month concentration commitment. Output 3-customer validation gate to Product #2.

### Step 7: For Product #2 candidates, enforce 3-customer threshold
Three UNRELATED customers paying FULL price under SIGNED contracts. Pilots, LOIs, "interested" don't count.

### Step 8: Write HTML + return structured summary
```json
{"selected_hill": "...", "score": 16, "viable_set": [...],
 "no_viable_hill": false, "output_path": "...",
 "next_skill": "sw-compliance-discipline"}
```

## Constraints
- Viability floor 12 is hard (must surface "no viable hill" not force a pick)
- 3-customer threshold applies only for Product #2 decisions; informational for Product #1
- Concentration default - one hill, sequenced; do not output multiple parallel hills
