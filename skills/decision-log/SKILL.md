---
name: decision-log
description: Record a significant decision with options, confidence intervals, rationale, and review date. Stored in pipeline.db + RAG-indexed for future similar-decision retrieval.
version: 1.0.0
tags: [strategy, decisions, harbor, data-moat, constitution-p9]
tier: C
owning_profile: orchestrator
invoked_by: user-only
moat_test: "Builds HARBOR's decision-history data moat — compounds across engagements per Thiel framework. Generic decision-log doesn't capture confidence intervals or review_date."
---

# Decision Log

Per HARBOR Constitution P9: every significant decision is logged with date, context, options, confidence interval per option, decision, rationale, and review date.

**One-line:** Decisions compound. Capture them.

## When to load this skill

Triggered when Amyn faces or just made one of:
- **bid_no_bid** — proposal go/no-go on a federal opp
- **pricing** — Sprint customization, pilot scope adjustment, retainer extension
- **partnership** — referral split, co-delivery agreement, NDA decision
- **product** — feature priority for harbor.build SaaS
- **hiring** — fractional/contractor engagement
- **ops** — agent infrastructure, tool selection, policy change

## Workflow

### Phase 1: Gather

Prompt Amyn (or extract from context) for:
- **slug** — short kebab-case: `YYYY-MM-DD-<topic-kebab>`
- **type** — one of the enum above
- **context** — 1-3 sentences situating the decision
- **options** — 2-5 named alternatives, each with:
  - name (kebab-case label)
  - expected_outcome (1 sentence)
  - confidence_interval (e.g., "30-50% likelihood we hit this")
  - downside (1 sentence — what's the worst case)
- **decision** — which option you picked
- **rationale** — why this over the others
- **review_date** — when to revisit (default: +30/60/90 days based on type — bid/no-bid = 30d, pricing = 60d, product/partnership/hiring = 90d, ops = 30d)
- **related_prospect_slug** — if applicable

### Phase 2: Persist

Two writes:
1. `pipeline-manager.py decision add` — relational store in pipeline.db
2. `~/HARBOR/decisions/YYYY-MM-DD-<slug>.md` — markdown copy for human/RAG indexing

Markdown shape:
```markdown
---
slug: 2026-05-25-soal-darpa-bid
type: bid_no_bid
decided_at: 2026-05-25T22:30:00Z
review_date: 2026-06-25
related_prospect: soal-tech
---

# Soal — bid DARPA HR0011SB20254-03?

## Context
Soal has a unique CMMC L1 + cyber posture. DARPA topic SB20254-03 closes in 18 days.
Hussein already pushed Ahmed to evaluate.

## Options

### A. Bid solo
- Expected: win probability 20-30%, $250K Phase I if won
- Confidence: 30-50% Soal can produce a competitive proposal in 18 days
- Downside: Sinks 40-60 founder hours on a low-win-probability bid

### B. Bid with HARBOR as proposal partner ($15K Sprint scope)
- Expected: win probability 35-50%, HARBOR earns $15K + $50K Pilot path
- Confidence: 50-70% HARBOR can shape proposal in time
- Downside: Burns relationship if proposal is rejected — but win-share is real

### C. Skip; revisit next DARPA cycle (Q3 2026)
- Expected: 0% on this; preserves bandwidth for X, Y
- Confidence: 90% Q3 cycle has equal/better fit
- Downside: 90-day wait risks losing momentum with Soal

## Decision
**B** — bid with HARBOR as proposal partner. Frame as $15K Sprint with proposal as primary deliverable.

## Rationale
Win-share aligns incentives. Soal can't bid solo in 18d. HARBOR earns either way (closed-won = $15K + Pilot path; closed-lost = compliance-pattern data + Hussein referral strengthened by attempt). Sung's confidence-interval frame: option B has highest expected value across most plausible scenarios.

## Review
2026-06-25 — by then either Phase I awarded or not. Update outcome field; capture learnings for future GovCon SBIR Sprint-as-proposal-partner offering.
```

### Phase 3: RAG index

Embed the markdown via the supabase-rag pipeline (mark with `decision: true` in metadata).

### Phase 4: Cron reminder

The weekly ops review surfaces decisions where `review_date <= today + 7d` so Amyn can do the retrospective.

## Retrospective workflow (separate invocation)

When `review_date <= today` triggers:
- Re-open the decision
- Prompt: what actually happened? Score: did confidence_interval contain the actual outcome?
- Update `outcome` field; mark `reviewed_at`
- Track confidence-interval calibration over time — published in quarterly ops review

## Cost

Negligible — one prompt-and-record cycle. ~$0.01 per decision.

## Related

- v2.0 §5.5 (this skill)
- HARBOR Constitution P9 (decisions require intervals + review_date)
- pipeline.db `decisions` table
- Dr. Sung "Think Clearly" framework (P5 + P10) — confidence intervals + three traps
