---

name: sw-contract-archaeology
description: Contract Archaeology IP discovery from Book 1 Chapter 4. 4-step process (proposal sweep, delivery-lead interviews, repeat mapping, documentation assessment) producing scored IP inventory and 1-3 quick-win candidates. Dispatches into harvest-agent's existing 7-phase pipeline for deep work. Use when starting Harvest phase, when scoring a firm's hidden IP, or as part of /shrink-wrap.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - portfolio-or-self
arguments: subject
model: sonnet
when_to_use: contract archaeology, IP inventory, harvest IP, Ch 4 IP discovery
---

# /sw-contract-archaeology - Your Best Product Already Exists

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-4 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-4.md`

## Execution

### Step 1: Resolve subject input
Order: orchestrated run -> portfolio member directory -> AskUserQuestion.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/01-harvest/ch4-ip-inventory.html`
- Direct: `experiments/single-instrument/sw-contract-archaeology/$(date +%Y-%m-%d)-<subject>.html`

### Step 3: Dispatch into harvest-agent for deep work
This skill is the SURFACE; harvest-agent's existing 7-phase pipeline is the ENGINE.

```
Agent({subagent_type: "harvest-agent",
       description: "Contract archaeology deep sweep for <subject>",
       prompt: "Run your Phase 1 (proposal sweep) + Phase 2 (delivery-lead interview synthesis) for <subject>. Return scored IP inventory."})
```

### Step 4: Apply 3-type taxonomy classification
For each IP item from harvest output, classify as Process / Tool / Data IP per signs in abstract instrument.

### Step 5: Map reuse counts
1 / 2 / 3+ / 5+ priority bands per abstract instrument.

### Step 6: Documentation state assessment
None / Partial / Proposal-only / Full per candidate. Compute extraction effort.

### Step 7: Data-rights hard gate per candidate
Mark each candidate: data-rights-clear / restricted / unknown. Lens-keyed clause citations.

### Step 8: Quick-win filter (all 4 criteria)
Output 1-3 candidates passing High/Med priority + Full/Partial docs + 3+ identifiable buyers + no compliance gating.

### Step 9: Compliance Asset fallback
If Quick-Start filter rejects all inventory, recommend Compliance Asset productization (CMMC Readiness / FedRAMP Evidence Collector / ATO Doc Accelerator for federal; SOC 2 Readiness / ISO Gap / HIPAA Risk for commercial-US; GDPR DPIA / ISO 27701 for commercial-EU; etc).

### Step 10: Dispatch persona-strategic-advisor + persona-translation-lead (if lens != federal)

### Step 11: Write HTML + return structured summary
```json
{"subject": "...", "total_ip_items": 47, "quick_win_candidates": [...],
 "compliance_asset_fallback_recommended": false, "output_path": "...",
 "next_skill": "sw-s2p-scorecard"}
```

## Constraints
- Cross-portfolio leak grep BEFORE writing output if subject is portfolio member
- Data-rights clear required before listing in quick-win set
- Quick-Start targets 1-3 candidates, not exhaustive inventory
- harvest-agent is the engine - do not duplicate its 7-phase logic
