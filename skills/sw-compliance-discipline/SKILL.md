---

name: sw-compliance-discipline
description: Should-you-pursue-federal decision framework from Book 1 Chapter 7. Two-column logic - Pursue (AND-gate all 5) vs Reconsider (OR-gate any triggers delay) - plus $1.5M federal ARR floor and ConMon staffing model (A FT / B Fractional / C CaaS). Outputs gate result + 12-month cadence calendar. Use to validate compliance commitment before authorization prep or as part of /shrink-wrap Risk-Proof phase.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: compliance discipline, should pursue federal, ConMon staffing, Ch 7 gate
---

# /sw-compliance-discipline - Compliance Is Not a Phase

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-7 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-7.md`

## Execution

### Step 1: Resolve candidate input
Order: orchestrated run output of Ch 6 -> direct slug -> AskUserQuestion.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/03-risk-proof/ch7-compliance-discipline.html`
- Direct: `experiments/single-instrument/sw-compliance-discipline/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Lens-conditional persona resolution

Before dispatching, resolve the lens-specific persona using this exact table (based on `${HARBOR_LENS}`):

| HARBOR_LENS | Primary auditor persona |
|---|---|
| federal | persona-fedramp-auditor |
| commercial-us | persona-iso-soc2-auditor |
| commercial-eu | persona-iso-soc2-auditor + persona-privacy-counsel-eu-gdpr |
| commercial-uk | persona-iso-soc2-auditor + persona-privacy-counsel-uk |
| sector-healthcare | persona-sector-healthcare + persona-iso-soc2-auditor |
| sector-finance | persona-sector-finance + persona-iso-soc2-auditor |
| sector-energy | persona-sector-energy |
| international | persona-international-procurement-officer + persona-fedramp-auditor |

If HARBOR_LENS is unset or unknown, default to federal lens. Surface a warning in skill output noting the lens was defaulted.

### Step 4: Dispatch personas in parallel
- {resolved auditor persona from table above}
- persona-cfo (staffing vs gross margin)
- persona-operations-lead (cadence feasibility)

### Step 5: Apply ARR floor check
Federal: $1.5M within 24 mo. Lens-keyed alternatives in abstract instrument. Below floor = recommend delay.

### Step 6: Run Pursue column (AND-gate, ALL 5)
If any fail, gate result = HALT.

### Step 7: Run Reconsider column (OR-gate, ANY)
If any single condition triggers, gate result = DELAY.

### Step 8: ConMon staffing recommendation
Pick A / B / C based on projected ARR and current team. Cite lens-keyed cost ranges.

### Step 9: Emit 12-month cadence calendar
Monthly (scans+POA&M) / Quarterly (sampling+incident) / Annually (3PAO+pentest+AO renewal).

### Step 10: Write HTML + return structured summary
```json
{"candidate_slug": "...", "gate_result": "PURSUE|DELAY|RECONSIDER",
 "arr_floor_met": true, "conmon_staffing": "B",
 "cadence_calendar_path": "...", "output_path": "...",
 "next_skill": "sw-authorization-route"}
```

## Constraints
- Pursue is conjunctive (5/5 required); Reconsider is disjunctive (1 triggers)
- ARR floor is lens-keyed; do not apply federal $1.5M to commercial runs
- Output 12-month calendar artifact embedded in HTML, not as separate file
