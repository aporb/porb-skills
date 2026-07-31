---
name: adversarial-reviewer
description: Counterfactual-debating reviewer for HARBOR deliverables. Argues AGAINST a draft from 3 preset stances, surfaces unsupported claims, returns structured JSON with confidence_score. Gating step before any deliverable ships.
version: 1.0.0
tags: [quality, review, adversarial, harbor, constitution]
tier: A
owning_profile: reviewer
moat_test: "Embeds the 10-principle HARBOR Constitution as its rubric + GovCon-specific factual-risk patterns (FAR/DFARS, agency claims, dollar figures). Not a generic LLM reviewer."
---

# Adversarial Reviewer

The headline output-quality intervention from v2.0 Section 3. Implements counterfactual debating (arXiv 2406.11514) with preset stances, gated by the HARBOR Constitution at `~/.hermes/HARBOR-CONSTITUTION.md`.

**One-line:** Argue against the draft. Find what's wrong before it ships.

## When to load this skill

- After drafting ANY of: briefing (daily, engagement), Pre-Assessment, Intel Canvas, Meeting Prep, Competitive Canvas, SOW, LinkedIn long-form post, X thread, blog post
- Before delivery to Telegram, before posting externally, before sending to a client
- Mandatory gating step in the `harbor-assess` skill's deliverable pipeline (Tier B)

## Inputs

```json
{
  "draft_path": "/path/to/draft.html or .md or .txt",
  "draft_type": "daily-briefing | engagement-brief | pre-assessment | intel-canvas | meeting-prep | competitive-canvas | sow | linkedin-post | x-thread | blog-post",
  "audience": "amyn-only | telegram | external-client | public",
  "constitution_path": "~/.hermes/HARBOR-CONSTITUTION.md"
}
```

## Workflow

### Phase 1: Read the draft + Constitution

Load the full draft. Load `HARBOR-CONSTITUTION.md`. Skim any associated source documents (briefings the draft cites, prior conversations referenced).

### Phase 2: Three preset-stance critiques (parallel)

Run THREE independent reviews. Each is a separate LLM call. Use deepseek-v4-flash for cost discipline; the synthesis step (Phase 4) can use pro if findings disagree materially.

**Stance 1 — Counterfactual: "This draft is wrong about X. Find the strongest evidence against the main claim."**

Prompt the model with the draft + this instruction:
```
You are arguing this draft is WRONG. Identify the central claim. List 3-5 reasons the claim might be incorrect, citing what evidence would be needed to validate. Be specific. No softening.

Return JSON:
{
  "central_claim": "...",
  "counter_arguments": [
    {"argument": "...", "evidence_needed": "...", "strength": 1-5}
  ]
}
```

**Stance 2 — Skeptical GovCon CO: "A federal contracting officer reads this. What's the first thing they reject?"**

```
You are a skeptical federal Contracting Officer (CO) reading this draft. You have seen
thousands of consulting decks. You spot puffery. You catch invented clauses.
What rejection would you write? List the top 3 things you'd push back on, with the
specific line/passage that triggered each.

Return JSON:
{
  "rejection_summary": "...",
  "objections": [
    {"objection": "...", "passage": "exact quote", "severity": "blocker|concern|nitpick"}
  ]
}
```

**Stance 3 — Citation auditor: "Three claims have no citation. List them with line/section references."**

```
You are a citation auditor. Find every factual claim about an agency, contract, regulation,
dollar figure, person, or organization that lacks a citation OR is not marked
"(unverified)". HARBOR Constitution P1 requires cite-or-hedge.

For each, provide: claim text, location in draft, severity, and what kind of citation
would resolve it.

Return JSON:
{
  "unsupported_claims": [
    {"claim": "...", "location": "section X / paragraph N", "severity": "blocker|concern|nitpick", "needed": "..."}
  ],
  "P2_violations": [...],  // invented FAR/DFARS clauses
  "P3_violations": [...]   // opinion presented as fact
}
```

### Phase 3: Constitutional sweep

Score the draft against each of the 10 principles (1-5 each):
- P1 cite-or-hedge
- P2 no invented clauses
- P3 opinion vs fact
- P4 no disparagement
- P5 confidence intervals over false precision
- P6 Section 508 / accessibility
- P7 Amyn voice (specific over abstract, banned words)
- P8 compliance posture
- P9 decisions have intervals + review date (if draft includes decisions)
- P10 three-trap classification (if draft is a synthesis/recommendation)

For each violation, capture: principle id, severity (blocker/concern/nitpick), passage, fix-suggestion.

### Phase 4: Synthesize

Combine the three stance outputs + the constitutional sweep into a final report:

```json
{
  "verdict": "ship" | "revise" | "reject",
  "confidence_score": 0-100,
  "tied_weakest_principle": "P1" | ... | "P10",
  "blockers": [
    {"principle": "P1", "passage": "...", "fix": "..."}
  ],
  "concerns": [...],
  "nitpicks": [...],
  "stance_summaries": {
    "counterfactual": "...",
    "co": "...",
    "citation_audit": "..."
  }
}
```

**Verdict routing:**
- `ship` — confidence_score ≥ 95, 0 blockers, ≤2 concerns total. Draft proceeds.
- `revise` — confidence_score 70-94, OR any blocker. Return findings; require rewrite + re-review.
- `reject` — confidence_score < 70, OR ≥3 blockers. Caller should reconsider scope, not iterate on the draft.

### Phase 5: Persist + return

- Write the full report to `~/.hermes/cron/output/${HERMES_CRON_ID:-manual}/review-${draft_id}-${timestamp}.json`.
- Append a one-line summary to `~/.hermes/state/review-log.jsonl` for the weekly ops review to aggregate.
- Return the JSON to the caller.

## Threshold tuning notes

Per v2.0 §3.2 risk note: self-consistency reduces hallucinations PRIMARILY by abstaining. Briefings will get shorter and more hedged. Tune the threshold or you trade hallucinations for uselessness.

**Starting thresholds (revise these in weekly ops review):**
- `ship` confidence floor: 95 (conservative — drafts will revise often)
- `reject` confidence ceiling: 70 (only for truly broken drafts)
- Blocker count threshold: 0 (one blocker = revise)

If after 2 weeks the ship-rate is < 30%, lower the ship floor to 90 and re-evaluate.

## Cost economics

Three stance LLM calls (flash) + 1 constitutional sweep (flash) + 1 synthesis (flash or pro depending on disagreement) per draft.

Rough estimate at flash pricing: ~$0.005-0.015 per review for a 2K-token draft. Daily briefing + engagement = ~$0.03/day.

## Related

- v2.0 Section 3.1 (Constitution) → `~/.hermes/HARBOR-CONSTITUTION.md`
- v2.0 Section 3.2 (this skill)
- v2.0 Section 3.5 (tone-strip — runs AFTER reviewer, before delivery)
- v2.0 Section 3.4 (Inspect AI gold set — separate eval-time skill, not invoked per-draft)
- Companion: `multi-persona-review` skill (alternative for higher-stakes deliverables)
