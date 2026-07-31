---

name: sw-builder-operator
description: Builder-Operator Mindset team assessment from Book 1 Chapter 3. 4-section assessment (Individual / Gap Analysis / Specialized Help / Go-No-Go) with strict AND-gate of 6 binary criteria and per-capability minimums. Use to validate team readiness for federal productization before investment, or as part of /shrink-wrap pre-H gate.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - team-roster
arguments: roster
model: sonnet
when_to_use: team assessment, builder-operator gate, Ch 3 go-no-go, team readiness check
---

# /sw-builder-operator - The Builder-Operator Mindset

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-3 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-3.md`

## Execution

### Step 1: Resolve roster input
Order: orchestrated run -> portfolio member info.md -> AskUserQuestion (named team members + roles).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/00-precheck/ch3-builder-operator.html`
- Direct: `experiments/single-instrument/sw-builder-operator/$(date +%Y-%m-%d)-<roster>.html`

### Step 3: Section A - Individual Assessment (5 capabilities, 1-5 each)
For each named team member, score the 5 capabilities. Store the highest rating per capability across the team.

### Step 4: Section B - Gap Analysis
Required level vs current team max per capability. Prioritize gaps (Critical 3+ / Significant 2 / Moderate 1 / None 0).

### Step 5: Section C - Specialized Help Needs
Resource planning: 3PAO, SSP author, legal/IP, vehicle strategy, CLIN structuring. Estimate budget.

### Step 6: Dispatch personas
- persona-strategic-advisor (outside-CEO read of team)
- persona-cfo (gap-closure cost vs Ch 2 Filter 2 budget)

### Step 7: Section D - 6-criterion AND-gate Go/No-Go
ALL 6 must Y. Per-capability minimums from Section A wired in. Any N halts.

### Step 8: Write HTML + return structured summary
```json
{"roster_id": "...", "section_a_max_per_capability": {...},
 "critical_gaps": [...], "go_no_go": "GO|NO-GO",
 "blocking_criteria": [], "output_path": "...", "next_skill": "sw-contract-archaeology"}
```

## Constraints
- Strict AND-gate: any single N halts, regardless of A/B/C totals
- Per-capability minimums (ATO Level 4+, Cross-functional Level 4+, others Level 3+)
- Hard-flag missing Compliance Owner role
