---
name: sw-pricing-model
description: Pricing model picker from Book 1 Chapter 13. Selects Per-User / Per-Unit / Subscription / Outcome-Based. Outcome-Based requires 5 qualifying conditions ALL pass. Mandatory ConMon cost allocation (FedRAMP Mod $200K-500K/yr; High $500K-1M+/yr) factored into floor. Mandatory 3-scenario stress test (Slow / Expected / High - profitable at all 3 required). Cites Acquisition Letter MV-24-03 for GSA upfront SaaS. Use after /sw-boundaries or as part of /shrink-wrap Replicate phase.
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: pricing model, per user, per unit, subscription, outcome-based, Ch 13 pricing
---

# /sw-pricing-model - Pricing Without Selling Hours

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-13 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-13.md`

## Execution

### Step 1: Resolve candidate input + pricing intent
Expect: candidate + product type + target customer profile + agency/buyer budget posture.

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/05-replicate/ch13-pricing-model.html`
- Direct: `experiments/single-instrument/sw-pricing-model/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel
- persona-pricing-strategist (primary)
- persona-cfo (3-scenario stress test)
- persona-sales-lead (buyer-acceptance reality check)
- persona-customer-voice-<lens> (willingness-to-pay validation)

### Step 4: Pick primary pricing model
Per-User / Per-Unit / Subscription / Outcome-Based.

### Step 5: Outcome-Based 5-condition check (if Outcome chosen)
Measurable outcomes / Agreed baseline / Causal correlation / Sophisticated buyer / Aligned timeframe. ALL 5 must pass.

### Step 6: Per-Unit unit definition (if Per-Unit)
Output suggested unit definition in SOW. Examples per abstract instrument.

### Step 7: Subscription O&M vs DME (federal Subscription only)
AskUserQuestion for budget classification. Capture answer.

### Step 8: ConMon allocation (MANDATORY input)
FedRAMP Mod $200K-500K/yr or High $500K-1M+/yr. At 10 customers Mod = ~$20-50K/customer/yr. Factor into floor pricing.

### Step 9: 3-scenario stress test (MANDATORY)
Slow / Expected / High. Profitable at ALL three required. If High-scenario-required to break even, recommend restructuring.

### Step 10: GSA MAS upfront SaaS note
Cite Acquisition Letter MV-24-03 (May 2024) for Per-User or Subscription on GSA vehicles - upfront annual SaaS payment is now allowed.

### Step 11: Write HTML + return structured summary
```json
{"candidate_slug": "...", "model": "Subscription",
 "outcome_5_conditions_passed": null, "om_vs_dme": "O&M",
 "conmon_allocation_per_customer_yr": 35000,
 "stress_test_passing": {"slow": true, "expected": true, "high": true},
 "output_path": "...", "next_skill": "sw-clin-vehicle"}
```

## Constraints
- ConMon allocation is MANDATORY input, not optional
- 3-scenario stress test is MANDATORY - must be profitable at all three
- All 5 outcome conditions required if Outcome-Based selected
- next_skill depends on lens: federal -> sw-clin-vehicle, commercial -> sw-channel-vehicle
