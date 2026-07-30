---
name: sw-authorization-route
description: "Authorization path picker from Book 1 Chapter 8. Selects FedRAMP (LI-SaaS / Low / Moderate / High) or CMMC (L1/L2/L3) or Agency ATO for federal, SOC 2 / ISO / HITRUST / StateRAMP for commercial. Enforces Product-vs-Organization distinction, sponsor-first hard gate, AI/ML 20-30% timeline modifier, inheritance leverage check. Use after /sw-compliance-discipline or as part of /shrink-wrap Risk-Proof phase."
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: authorization path, FedRAMP path, CMMC level, SOC 2 vs ISO, Ch 8 authorization
---

# /sw-authorization-route - Security, Authority, and Trust

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-8 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-8.md`

## Execution

### Step 1: Resolve candidate input + data sensitivity
Includes: data sensitivity, sponsor status, AI/ML inclusion, architecture cloud (commercial AWS vs GovCloud).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/03-risk-proof/ch8-authorization-route.html`
- Direct: `experiments/single-instrument/sw-authorization-route/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel
- persona-fedramp-auditor (federal primary)
- persona-iso-soc2-auditor (commercial primary)
- persona-privacy-counsel-<region> (EU/UK/sector overlays)
- persona-engineering-lead (inheritance + AI/ML modifier)

### Step 4: Sponsor-first hard gate
No sponsor (federal) or no enterprise deal in pipeline (commercial) = recommend "delay authorization, pursue traction first". Skip Step 5.

### Step 5: Path picker
Match data sensitivity + ARR + customer profile to path table. May select MULTIPLE (e.g., FedRAMP Moderate + CMMC L2 if both apply).

### Step 6: Product vs Organization distinction
Ask both questions separately. Output both recommendations if both apply.

### Step 7: Apply AI/ML modifier
If product has AI/ML: +20-30% timeline + model governance docs per OMB M-24-10.

### Step 8: Inheritance leverage check
Architecture supports GovCloud / Azure Government inheritance? If not, surface as redesign opportunity with cost-savings math (40-60% control burden, $50-150K/yr ConMon for Moderate).

### Step 9: Write HTML + return structured summary
```json
{"candidate_slug": "...", "product_path": "FedRAMP Moderate",
 "org_path": "CMMC L2", "sponsor_confirmed": true,
 "ai_ml_modifier_applied": false, "inheritance_recommended": true,
 "output_path": "...", "next_skill": "sw-survivability-arch"}
```

## Constraints
- Sponsor-first hard gate fires before path selection - do not "find sponsor harder"
- IL5 requires FedRAMP High base (Moderate-to-High uplift not viable)
- Cite specific control counts from abstract instrument for transparency
