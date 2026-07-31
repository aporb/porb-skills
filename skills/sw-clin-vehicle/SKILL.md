---

name: sw-clin-vehicle
description: Federal vehicle stack picker from Book 1 Chapter 14. Composes multi-vehicle stack (GSA MAS / OASIS+ / SEWP VI / OTA / Agency IDIQ / SBIR Phase III), picks CLIN pattern (SaaS Subscription vs Managed Service + Platform), applies 4-rule design checklist. Federal lens. Use after /sw-pricing-model or as part of /shrink-wrap Replicate phase for federal candidates. Commercial / international use /sw-channel-vehicle instead.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: CLIN vehicle, federal vehicle stack, GSA MAS, OASIS, SEWP, Ch 14 federal
---

# /sw-clin-vehicle - CLINs, Schedules, and Reality (Federal)

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-14 --lens federal`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-14.md`

## Execution

### Step 1: Resolve candidate input + target federal buyer profile
Expect: candidate + target agency mix + SBIR heritage flag + DoD innovation flag + single-agency vs multi-agency target.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/05-replicate/ch14-vehicle-stack.html`
- Direct: `experiments/single-instrument/sw-clin-vehicle/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel
- persona-sales-lead (primary - vehicle selection)
- persona-pricing-strategist (vehicle compatibility with Ch 13 pricing)
- persona-sector-<sector> (if sector lens - sector-specific channels)

### Step 4: Apply 5-rule selection framework (compose a stack, NOT pick one)
1. Broad federal -> GSA MAS (primary)
2. Large task orders -> GWAC/IDIQ (OASIS+, SEWP VI)
3. DoD innovation -> OTA
4. SBIR heritage -> SBIR Phase III
5. Single-agency -> Agency IDIQ

### Step 5: Pick CLIN pattern
Pattern 1 (SaaS Subscription) - CLIN 0001 Subscription / 0002 Implementation / 0003 Custom Dev T&M (always T&M).
Pattern 2 (Managed Service + Platform) - 0001 Platform / 0002 Managed Services / 0003 Custom Dev T&M (always T&M).

### Step 6: Apply CLIN design checklist (4 rules)
1. Total evaluated price calculable in <60 seconds
2. Each CLIN distinct value
3. CLIN structure matches RFP
4. Option year structure obvious

### Step 7: Surface acquisition timelines + costs per vehicle in stack
Per abstract instrument table. Include $350K SAT effective Oct 1, 2025.

### Step 8: Write HTML + return structured summary
```json
{"candidate_slug": "...", "vehicle_stack": ["GSA MAS", "OTA"],
 "clin_pattern": "Pattern 1", "checklist_passed": 4,
 "total_acquisition_cost_estimate": 45000,
 "total_acquisition_timeline_months_max": 18,
 "output_path": "..."}
```

## Constraints
- Compose a stack (multiple vehicles), do not single-pick
- Custom Development is ALWAYS T&M (never FFP regardless of customer preference)
- $350K Simplified Acquisition Threshold (effective Oct 1, 2025) - cite explicitly
