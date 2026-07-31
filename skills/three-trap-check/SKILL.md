---
name: three-trap-check
description: Force Dr. Sung's three-trap cognitive classification (stuck / overwhelmed / uncertain) before producing any synthesis or recommendation. Implements HARBOR Constitution P10.
version: 1.0.0
tags: [quality, cognitive, constitution-p10, sung, harbor]
tier: A
owning_profile: orchestrator
moat_test: "Encodes Dr. Sung's framework adapted to HARBOR deliverables (proposals, briefings, decisions) — the meta-process gate that Constitution P10 declares."
---

# Three-Trap Check

Per Constitution P10. Before producing any synthesis, recommendation, or decision, classify
the situation into one of three cognitive traps and apply the matched fix.

**One-line:** Stuck → separate; overwhelmed → constrain; uncertain → widen.

## When to load this skill

- Auto-invoked as a pre-check by `adversarial-reviewer` and `multi-persona-review`
- Before drafting a Pre-Assessment recommendations section
- Before logging a `decision-log` entry
- When Amyn asks "what should I do about X?"
- When stuck on a brief, proposal, or strategic call (i.e., when you'd otherwise produce mush)

## The three traps + matched fixes

| # | Trap | Symptom | Fix | Required output |
|---|---|---|---|---|
| 1 | **Stuck** | Tangled problem; can't make progress; multiple variables in tension | Separation of Concerns: isolate independent variables, resolve each on its own, reassemble | `independent_variables: [name1, name2, ...]` |
| 2 | **Overwhelmed** | Too many things at once; feels like a capacity problem; want to "do everything" | Theory of Constraints: find the one biggest bottleneck. Fix it. Downstream simplifies. | `primary_constraint: "specific bottleneck"` |
| 3 | **Uncertain** | Don't know which option is right; tempted to invent precision | Confidence Intervals: widen scope until you can be honest about what you know. Aim for accuracy, adjust precision. | `confidence_interval: "X-Y% likelihood"` |

## Workflow

### Phase 1: Classify

Read the situation. Pick ONE primary trap. Don't try to be all three. Don't skip — if
the situation doesn't fit any trap, the work probably doesn't need this skill at all
(it's a clear execution task, not a synthesis call).

### Phase 2: Emit the classification

Required output shape (forced — must appear before any prose):

```yaml
trap: stuck | overwhelmed | uncertain
applied_fix: separation_of_concerns | theory_of_constraints | confidence_intervals
# REQUIRED based on trap value:
independent_variables: [...]    # only when trap=stuck
primary_constraint: "..."       # only when trap=overwhelmed
confidence_interval: "..."      # only when trap=uncertain
notes: "1-2 sentence rationale"
```

### Phase 3: Apply the fix in the actual response

Now produce the synthesis/recommendation, but explicitly following the fix:

- **Stuck → separation**: present each independent variable as its own sub-section.
  Don't conflate them. Reassemble at the end.
- **Overwhelmed → constraint**: lead with the constraint. Other items get one-line
  treatment until the constraint is resolved.
- **Uncertain → intervals**: every probabilistic claim has an explicit interval.
  No invented precision.

### Phase 4: Self-check

Before delivering, re-read the response. Did the fix actually shape the output?
If the trap classification appears but the response reads the same as if it had been
omitted, the skill failed — the trap was wrong, or the fix wasn't applied.

## Examples

### Example 1 — Pre-Assessment recommendations (Stuck)

Situation: "Should we recommend Soal pursue 8(a) cert OR GSA MAS schedule OR neither?"

```yaml
trap: stuck
applied_fix: separation_of_concerns
independent_variables: [revenue_impact, time_to_value, opportunity_cost, optionality_preserved]
notes: "These four variables pull in different directions. Resolving each separately surfaces a clear ranking."
```

Then the recommendations section addresses each variable separately, then synthesizes
("8(a) wins on revenue_impact + opportunity_cost; GSA MAS wins on time_to_value...").

### Example 2 — Q3 roadmap reprioritization (Overwhelmed)

Situation: "Q3 has 6 SaaS milestones. Compliance Autopilot needs 4 weeks; Opportunity
Radar needs 3; Health Score needs polish; book 2 needs an editor; Soal Sprint kickoff;
North AI partnership decision."

```yaml
trap: overwhelmed
applied_fix: theory_of_constraints
primary_constraint: "Opportunity Radar (3wk) blocks 3 of the other 5 — Health Score polish, book 2 chapter on Radar, and the Soal pilot. Fixing it first uncorks the rest."
notes: "Without solving Radar, the other items either depend on it directly or get less attention."
```

### Example 3 — Bid/no-bid call (Uncertain)

Situation: "DARPA HR0011 closes in 18 days. Win probability?"

```yaml
trap: uncertain
applied_fix: confidence_intervals
confidence_interval: "win probability 25-45% conditional on having a credible CMMC-tier-3 path; 5-15% otherwise. Source: 3 comparable past Phase I awards in adjacent NAICS, base rate 22%."
notes: "Two scenarios. Picking the higher interval requires confirming the compliance path before bidding."
```

## Anti-patterns

- ❌ Classifying every response as "uncertain" (lazy default)
- ❌ Picking "stuck" when the actual problem is "I don't have enough information" (that's a research task, not a trap)
- ❌ Skipping the classification because the response feels obvious — the skill is the meta-process discipline. Trust the loop.

## Cost

~$0.001-0.005 per classification (flash-tier).

## Related

- HARBOR Constitution P10 (this skill is the mechanical enforcement)
- `decision-log` skill (requires confidence_interval when trap=uncertain)
- `adversarial-reviewer` (invokes this skill as a pre-check)
- `multi-persona-review` (synthesis step references the trap classification)
- Source: Dr. Sung "Think Clearly" framework, per think-clearly-2026-briefing.html
