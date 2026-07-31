---

name: sw-survivability-arch
description: Architecture for Survivability from Book 1 Chapter 9. Scores against 5 principles (Minimize Boundary / Layered + Segmented / Configuration over Customization / API-first / Environment Parity). Produces 3-bucket SSP structure (Inherited / Shared / Customer). Runs 4-rule POC readiness check. Hard gate - redesign required if 3+ principles fail. Use after /sw-authorization-route or as part of /shrink-wrap Risk-Proof phase.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: survivability architecture, 5 principles, SSP buckets, POC readiness, Ch 9 architecture
---

# /sw-survivability-arch - Architecture for Survivability

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-9 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-9.md`

## Execution

### Step 1: Resolve candidate input
Expect: architecture description (cloud platform, network topology, auth model, encryption posture, env management).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/03-risk-proof/ch9-survivability-arch.html`
- Direct: `experiments/single-instrument/sw-survivability-arch/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel

Lens-conditional resolution for the SSP / POC auditor:

| HARBOR_LENS | Auditor persona for SSP buckets + POC rules |
|---|---|
| federal | persona-fedramp-auditor |
| commercial-us / -eu / -uk | persona-iso-soc2-auditor |
| sector-healthcare | persona-iso-soc2-auditor + persona-sector-healthcare |
| sector-finance | persona-iso-soc2-auditor + persona-sector-finance |
| sector-energy | persona-sector-energy (IEC 62443) |
| international | persona-fedramp-auditor (FedRAMP-equivalent baseline) |

Then dispatch:
- persona-engineering-lead (primary - scores all 5 principles, always)
- {resolved auditor persona from table}
- persona-operations-lead (env parity feasibility, always)

### Step 4: Score 5 principles (pass/fail per principle)
1. Minimize the boundary
2. Layered and segmented
3. Configuration over customization
4. API-first
5. Environment Parity (NOT "Multi-Environment")

### Step 5: Build 3-bucket SSP structure
Per control: Inherited / Shared / Customer. All three buckets MUST appear in output. Vague claims like "we inherit AWS GovCloud" generate assessment findings.

### Step 6: POC readiness check (4 rules)
GovCloud day 1 / auth+logging+encryption at POC / SSP sections as you build / Terraform infra.

### Step 7: Redesign-or-proceed hard gate
3+ principles failing = redesign before authorizing (hard halt). 2 or fewer = remediate during auth prep.

### Step 8: IL5 flag check
If data sensitivity from Ch 8 = IL5 or higher, flag "build to FedRAMP High from day one" (Moderate-to-High uplift not viable).

### Step 9: Write HTML + return structured summary
```json
{"candidate_slug": "...", "principles_passed": 4,
 "principles_failed": ["env-parity"], "verdict": "PROCEED|REMEDIATE|REDESIGN",
 "ssp_bucket_summary": {...}, "poc_readiness_passed": 3,
 "il5_flag_active": false, "output_path": "...",
 "next_skill": "sw-codify-expertise"}
```

## Constraints
- Hard gate on 3+ principle failures - cannot soft-pass with remediation handwave
- All 3 SSP buckets must appear in output
- IL5 flag fires from Ch 8 hand-off, not re-derived here
