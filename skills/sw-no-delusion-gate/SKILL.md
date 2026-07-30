---
name: sw-no-delusion-gate
description: Productization Without Delusion 5-filter gate from Book 1 Chapter 2. Conjunctive AND-gate (any failure halts) across TAM, Compliance Cost Reality, ATO Path Viability, Vehicle Access, Internal Capability. Also runs the productization spectrum picker (Level 1-4). Use when validating that a productization candidate is worth investment, before any meaningful capital commitment, or as part of /shrink-wrap.
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - idea-or-candidate
arguments: candidate
model: sonnet
when_to_use: 5-filter gate, no-delusion gate, productization spectrum level, Ch 2 gate
---

# /sw-no-delusion-gate - Productization Without Delusion

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-2 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-2.md`

## Execution

### Step 1: Resolve candidate input
Slug lookup: fixtures -> run folder -> AskUserQuestion (title, description, target customer, stage).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/00-precheck/ch2-no-delusion-gate.html`
- Direct: `experiments/single-instrument/sw-no-delusion-gate/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Run the productization spectrum level picker FIRST
5-question worksheet (data sensitivity, product maturity, capital depth, TAM size, revenue urgency). Pick the level satisfying all 5.

### Step 4: Dispatch personas in parallel

Lens-conditional resolution (apply BEFORE dispatch):

| HARBOR_LENS | Market analyst | Filter-2 auditor |
|---|---|---|
| federal | persona-market-analyst-federal | persona-fedramp-auditor |
| commercial-us | persona-market-analyst-commercial-us | persona-iso-soc2-auditor |
| commercial-eu | persona-market-analyst-commercial-eu | persona-iso-soc2-auditor + persona-privacy-counsel-eu-gdpr |
| commercial-uk | persona-market-analyst-commercial-eu (UK overlap) | persona-iso-soc2-auditor + persona-privacy-counsel-uk |
| sector-* | persona-market-analyst-federal OR -commercial-us (closest lens) | persona-sector-<sector> + persona-iso-soc2-auditor |
| international | persona-market-analyst-commercial-eu (closest geo) | persona-international-procurement-officer |

Default to federal lens if HARBOR_LENS unset; surface defaulted-lens warning.

Then dispatch:
- persona-strategic-advisor (TAM + capability reality check, always)
- {resolved market analyst from table}
- persona-cfo (Filter 2 math, always)
- {resolved Filter-2 auditor from table}

### Step 5: Apply the 5-filter conjunctive gate
ALL must pass. Any failure = halt with explicit "fails Filter N because..." Output.

### Step 6: Cross-check level-vs-gate consistency
Spectrum level must be consistent with gate outputs. Warn on inconsistency.

### Step 7: Write HTML + return structured summary
```json
{"candidate_slug": "...", "spectrum_level": 3, "gate_result": "PASS|HALT",
 "failed_filters": [], "filter_5_hiring_gaps": [...], "output_path": "...",
 "next_skill": "sw-builder-operator"}
```

## Constraints
- Conjunctive gate: any single filter failing IS a fatal flaw, no averaging
- Spec lens-keyed entries override federal defaults when HARBOR_LENS != federal
- Cite book Ch 2 + abstract instrument in References
