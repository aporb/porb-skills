---

name: sw-s2p-scorecard
description: Score a productization candidate on the 6 Service-to-Product Fit dimensions from Book 1 Chapter 5. Returns weighted score with threshold tier (Proceed / Investigate / Deprioritize), enforces fatal-flaw vetoes on Vehicle Access and Economic Viability, applies 5-binary threshold check, and runs cannibalization sub-section. Use when evaluating whether a service should become a product, when scoring multiple candidates, or as part of /shrink-wrap full-methodology run.
parent: shrink-wrap
allowed-tools: "Read, Grep, Glob, Write, Bash(python3 *), AskUserQuestion, Agent, Skill"
argument-hint:
  - candidate-slug
arguments: candidate
model: sonnet
when_to_use: score this on S2P, S2P fit, service-to-product fit, S2P scorecard
---

# /sw-s2p-scorecard - Service-to-Product Fit Scorecard

## Book section (loaded at runtime)

!`python3 ${CLAUDE_SKILL_DIR}/../shrink-wrap/scripts/extract.py chapter-5 --lens ${HARBOR_LENS:-federal}`

## Abstract instrument (loaded at runtime)

!`cat ${CLAUDE_SKILL_DIR}/../shrink-wrap/references/abstract-instruments/chapter-5.md`

## Execution

You are running /sw-s2p-scorecard for the candidate specified in the argument.
The book chapter above gives you the narrative context; the abstract
instrument above gives you the executable rules.

### Step 1: Resolve candidate input

The candidate argument is a slug. Look for the candidate in this order:
1. `${CLAUDE_SKILL_DIR}/../shrink-wrap/references/fixtures/canned-candidate-<slug>.json`
   (P0 test fixtures live here)
2. `${RUN_FOLDER}/00-intake/candidate-<slug>.json` (orchestrated runs)
3. Otherwise, AskUserQuestion to capture the candidate's: title, one-paragraph
   description, target customer profile, current stage.

### Step 2: Determine output target

If invoked from architect-agent during orchestrated run: use
`${RUN_FOLDER}/02-architect/ch5-<slug>-s2p.html`.

If invoked directly: use `experiments/single-instrument/sw-s2p-scorecard/$(date +%Y-%m-%d)-<slug>.html`.

### Step 3: Dispatch the 4 personas in parallel

Single message, 4 Agent calls:

```
Agent({subagent_type: "persona-strategic-advisor",
       description: "S2P score contribution + founder bias check on <candidate>",
       prompt: "...candidate context + abstract instrument..."})
Agent({subagent_type: "persona-market-analyst-federal",
       description: "S2P Dim 2 + Dim 4 score on <candidate>",
       prompt: "..."})
Agent({subagent_type: "persona-customer-voice-federal-co",
       description: "S2P Dims 2, 4, 6 buyer-side reality check on <candidate>",
       prompt: "..."})
Agent({subagent_type: "persona-cfo",
       description: "S2P Dim 6 economic viability + cannibalization on <candidate>",
       prompt: "..."})
```

Each persona returns the structured JSON per its persona file's output shape.

### Step 4: Aggregate score contributions

For each dimension, collect all score contributions from the personas that
own it per the abstract instrument's persona dispatch table. Take the median
score across owning personas. Record the contributing personas' evidence
inline.

### Step 5: Apply fatal-flaw vetoes (BEFORE computing tier)

Check: did any persona score Vehicle Access at 1, or Economic Viability at 1?
If yes, set the result to ELIMINATED and flag the dimension. Skip Step 6.

### Step 6: Compute weighted total

`total = (rep * 0.20) + (cad * 0.15) + (cl * 0.15) + (va * 0.20) + (atf * 0.15) + (ev * 0.15)`

### Step 7: Apply 5-binary threshold check

All five must pass for PROCEED tier:
1. total >= 3.0
2. No dimension scored 1
3. At most one dimension scored 2
4. Vehicle Access >= 2
5. Economic Viability >= 2

If total >= 4.0 AND all 5 pass: tier = PROCEED.
If total >= 3.0 AND any of 2-5 fail: tier = INVESTIGATE.
If total < 3.0: tier = DEPRIORITIZE.

### Step 8: Run cannibalization sub-section

If the CFO persona's output flagged the candidate as cannibalistic, emit the
four management tactics from the abstract instrument. Otherwise omit.

### Step 9: Write the output HTML

Use the structure:

```html
<!DOCTYPE html>
<html>...</html>
```

Sections:
1. Cover: candidate name, run lens, date, score summary (tier + total)
2. 6-dimension table: per-dimension score, contributing personas with
   evidence, weight, weighted contribution
3. Fatal-flaw veto status
4. 5-binary threshold check results
5. Cannibalization sub-section (if triggered)
6. Persona memos cited with slug
7. References: book Ch 5 anchor, abstract instrument doc path

### Step 10: Return structured summary

Return to the invoker:

```json
{
  "candidate_slug": "...",
  "tier": "PROCEED | INVESTIGATE | DEPRIORITIZE | ELIMINATED",
  "weighted_total": 3.4,
  "fatal_flaw": null,
  "output_path": "..."
}
```

## Constraints

- You MUST dispatch all 4 personas, not a subset.
- You MUST apply fatal-flaw vetoes BEFORE computing the tier.
- You MUST NOT score any dimension yourself; defer to persona contributions.
- You MUST write the output HTML to the configured target path; do not write
  to alternate locations.
- You MUST cite the book Ch 5 anchor and the abstract instrument doc in the
  References section.
