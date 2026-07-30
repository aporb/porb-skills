---
name: sw-codify-expertise
description: Codification process from Book 1 Chapter 10. 4-criteria qualification gate (Repeatedly Applied / High Value / Differentiating / Transferable - 3 of 4 required) + 5-step process + SOP-to-Product bridge + MVP team (Compliance Owner non-negotiable). Outputs codification plan with 40-80 hour investment estimate. Use after /sw-survivability-arch or as part of /shrink-wrap Build phase.
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: codify expertise, codification process, MVP team, Ch 10 codify
---

# /sw-codify-expertise - Turning Expertise into Repeatability

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-10 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-10.md`

## Execution

### Step 1: Resolve candidate + named expertise to codify
Expect: candidate slug + which specific expertise (methodology, tool, data pattern) is being codified.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/04-build/ch10-codify-expertise.html`
- Direct: `experiments/single-instrument/sw-codify-expertise/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: 4-criteria qualification gate (run FIRST)
Score Repeatedly Applied (3+/yr) / High Value ($100K+ or 20%+ efficiency) / Differentiating / Transferable. 3 of 4 = codify. 4 of 4 = high priority. <3 = defer.

### Step 4: Dispatch personas in parallel

All three personas dispatch regardless of lens; compliance-owner's scope-of-work adapts to the run lens. No lens-conditional resolution needed at this step.

Dispatch:
- persona-operations-lead (SOP-to-Product bridge sub-steps)
- persona-engineering-lead (transferability)
- persona-compliance-owner (confirms in-firm role staffability + cadence; scope-of-work adapts to lens - FedRAMP/CMMC maintenance for federal, SOC 2 surveillance + ISO + vendor questionnaire portfolio for commercial, sector overlays for sector lenses)

### Step 5: 5-step codification plan
Identify Expertise / SME Interviews / Decision Trees / Process Flows / Checklists+Templates. Estimate hours per step (40-80 total upfront).

### Step 6: SOP-to-Product bridge (4 sub-steps)
Service Scope / Delivery Playbooks / Training Materials / Quality Checkpoints.

### Step 7: MVP team check
Name Product Owner, Delivery Lead, Compliance Owner. FLAG if Compliance Owner not named - non-negotiable.

### Step 8: Surface target economics
40-60% margin on productized vs 15-25% on custom work. The "why" for codification investment.

### Step 9: Write HTML + return structured summary
```json
{"candidate_slug": "...", "qualification": "3-of-4", "codify_recommended": true,
 "estimated_hours": 65, "compliance_owner_named": true,
 "output_path": "...", "next_skill": "sw-70-30"}
```

## Constraints
- Hard-flag missing Compliance Owner role
- Below 3-of-4 qualification = defer recommendation, not "try harder"
- Hour estimates from book (40-80 upfront, 70-100 if significant expertise)
