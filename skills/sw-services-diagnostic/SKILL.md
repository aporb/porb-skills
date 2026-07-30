---
name: sw-services-diagnostic
description: Pre-HARBOR posture diagnostic from Book 1 Chapter 1. Diagnoses where a firm sits on the services-to-product spectrum across 4 categories (Revenue Mix, Labor Dependency, Recompete Concentration, Technology Leverage) and surfaces qualitative warning signs. Returns a 100-point band + posture diagnosis (Denial / Premature Exit / Overcorrection / Healthy). Use when starting a /shrink-wrap full-methodology run, when assessing a firm's productization readiness, or when triaging a portfolio member's structural posture.
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - firm-or-self
arguments: subject
model: sonnet
when_to_use: diagnose services posture, services-to-product diagnostic, Ch 1 diagnostic, pre-H gate
---

# /sw-services-diagnostic - The End of Pure Services

## Book section (loaded at runtime)

!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-1 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument (loaded at runtime)

!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-1.md`

## Execution

You are running /sw-services-diagnostic for the subject in the argument. The book chapter gives narrative; the abstract instrument is the executable rules.

### Step 1: Resolve subject input
The subject is a portfolio slug or "self." Order:
1. `${RUN_FOLDER}/00-intake/firm-<subject>.json` if orchestrated
2. `HARBOR_portfolio/<subject>/info.md` if portfolio member
3. AskUserQuestion: revenue mix %, top 5 contracts, team size, named tools

### Step 2: Determine output target
- Orchestrated: `${RUN_FOLDER}/00-precheck/ch1-services-diagnostic.html`
- Direct: `experiments/single-instrument/sw-services-diagnostic/$(date +%Y-%m-%d)-<subject>.html`

### Step 3: Compute the 4-category 100-point score
Per abstract instrument Sections A-D rubric. Section A = inverse T&M%, Section B = inverse labor ratio, Section C = 25 minus penalties, Section D = scaled 5-25 -> 0-25.

### Step 4: Run Section E qualitative warning check
Four-question check; tally warning signs.

### Step 5: Assign band + posture
- 80-100 healthy / 60-79 transition / 40-59 urgent / <40 critical
- Posture: Denial / Premature Exit / Overcorrection / Healthy

### Step 6: Optionally dispatch persona-strategic-advisor (observer mode)
For interactive runs only. Asks Strategic Advisor to flag posture inconsistencies in user's free-text answers.

### Step 7: Write HTML output + return structured summary
```json
{"subject": "...", "score": 64, "band": "transition", "posture": "Denial",
 "warning_signs": [...], "output_path": "...", "next_skill": "sw-no-delusion-gate"}
```

## Constraints
- Score must use the verbatim formulas from the abstract instrument
- Cite book Ch 1 anchor + abstract instrument doc in output References
- If subject is "self," do NOT name any portfolio member
