---

name: sw-channel-vehicle
description: Commercial / international channel stack picker from Book 1 Chapter 14. Composes hyperscaler marketplaces (AWS / Azure / GCP / Salesforce AppExchange / AppSource) + VAR/SI partnerships + pilot-to-enterprise sales motion + named-account MSAs + (intl) AUKUS / NATO / allied frameworks + (sector) GPO / EHR marketplace channels. Picks MSA/SOW structure. Use after /sw-pricing-model for commercial / international / sector candidates. Federal candidates use /sw-clin-vehicle instead.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent"
argument-hint:
  - candidate
arguments: candidate
model: sonnet
when_to_use: channel vehicle, marketplace strategy, AWS marketplace, SI partnership, Ch 14 commercial
---

# /sw-channel-vehicle - Channels, Marketplaces, and Reality (Commercial / International)

## Book section
!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-14 --lens ${HARBOR_LENS:-commercial-us}`

## Abstract instrument
!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-14.md`

## Execution

### Step 1: Resolve candidate input + target commercial/intl/sector buyer profile
Expect: candidate + lens + target market (geo + sector) + named accounts in pipeline + tier (SMB / mid-market / enterprise).

### Step 2: Output target
- Orchestrated: `${RUN_FOLDER}/05-replicate/ch14-channel-stack.html`
- Direct: `experiments/single-instrument/sw-channel-vehicle/$(date +%Y-%m-%d)-<slug>.html`

### Step 3: Dispatch personas in parallel
- persona-sales-lead (primary)
- persona-channel-partner-commercial (commercial lens - reseller / marketplace economics)
- persona-international-procurement-officer (international lens - allied / NATO frameworks)
- persona-pricing-strategist (vehicle compatibility with Ch 13 pricing)
- persona-sector-<sector> (sector lens - GPO / EHR marketplace / sector-specific)
- persona-pilot-to-production-counsel (commercial - pilot agreement structure for enterprise sales motion)

### Step 4: Apply commercial-equivalent selection logic
Per abstract instrument lens entries:
- Self-serve catalog -> hyperscaler marketplaces
- Project deals -> VAR / reseller / SI partnerships
- Enterprise sales motion -> pilot-to-enterprise with right-of-first-negotiation
- Named-account custom -> EFA / MSA

### Step 5: Apply lens-keyed channel additions
- commercial-EU: Crown Commercial G-Cloud (UK), Cabinet Office Frameworks (UK), France UGAP, Germany Bundeskanzleramt frameworks
- international-allied: AUKUS (TS clearance dependent), NATO commercial procurement, Five Eyes implications
- sector-healthcare: GPO relationships (Premier, HealthTrust, Vizient), EHR marketplaces (Epic App Orchard, Cerner CODE)
- sector-finance: bank-specific procurement frameworks + SI partnerships (Accenture, Deloitte, IBM)

### Step 6: Surface marketplace fees
AWS 3-5% / Azure 3-5% / GCP 3-5% / Salesforce AppExchange 15-25% / AppSource 3-5%.

### Step 7: Pick MSA/SOW structure
Equivalent to CLIN patterns - line items: Subscription / Implementation / Optional Add-ons / Custom Dev T&M / Custom Dev Maintenance T&M.

### Step 8: Write HTML + return structured summary
```json
{"candidate_slug": "...", "lens": "commercial-us",
 "channel_stack": ["AWS Marketplace", "Tier-1 SI partner"],
 "msa_structure": [...],
 "marketplace_fee_impact_pct": 4.0,
 "output_path": "..."}
```

## Constraints
- Compose a stack (multiple channels), do not single-pick
- Marketplace fees factor into margin calculation
- AUKUS Pillar 2 requires TS clearance dependency check
- Sector channels (GPO, EHR marketplace) are additive, not replacements
