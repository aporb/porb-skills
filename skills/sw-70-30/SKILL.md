---

name: sw-70-30
description: Standardization heuristic from Book 1 Chapter 11. Classifies features as must-standardize (Security / Compliance / Core / Infra+Ops / Data Models) or should-be-configurable (Workflows / Reporting / Integrations / UI / Business Rules). NOT a computed 70/30 split - presented as heuristic. Includes core-vs-surface decision rule, custom CLIN structure for unavoidable customization, integration compliance hard gate. Use after /sw-codify-expertise or as part of /shrink-wrap Build phase.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: 70-30 split, standardization heuristic, core vs surface, Ch 11 standardize
---

# /sw-70-30 - What Gets Standardized

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-11 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-11.md`

## Execution

### Step 1: Resolve candidate input + feature list
Expect: candidate slug + list of features (from product roadmap, RFP responses, customer asks).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/04-build/ch11-70-30.html`
- Direct: `experiments/single-instrument/sw-70-30/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel
- persona-engineering-lead (owns classification)
- persona-operations-lead (feasibility of operating the configurable surface)
- persona-pricing-strategist (custom CLIN pricing implications)

### Step 4: Classify each feature
Must-standardize: Security Controls / Compliance Artifacts / Core Functionality / Infrastructure+Ops / Data Models (5 effective categories).
Should-be-configurable: Workflows / Reporting / Integrations / UI / Business Rules.

### Step 5: Apply core-vs-surface test for ambiguous features
"If changing this for one customer would break it for others, it's core."

### Step 6: Custom CLIN structure (if any custom features will exist)
Subscription / Implementation / Custom Dev T&M / Custom Dev Maintenance T&M (customer-funded indefinitely).

### Step 7: Integration boundary hard gate
For each cross-boundary integration: boundary-assessment decision BEFORE feature build. Lens-keyed (federal: ATO boundary; commercial: third-party risk review).

### Step 8: Write HTML + return structured summary
```json
{"candidate_slug": "...", "feature_classifications": {...},
 "ambiguous_resolved_by_test": [...], "custom_clin_structure": [...],
 "boundary_gate_flags": [...], "output_path": "...",
 "next_skill": "sw-boundaries"}
```

## Constraints
- NOT a 70/30 percentage computation - heuristic only
- Security-critical components MUST be must-standardize - configurable security = audit findings
- Customer-facing preferences (UI/workflow/terminology) MUST be configurable - standardizing them = churn
- Integration boundary gate is mandatory, not advisory
