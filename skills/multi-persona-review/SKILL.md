---
name: multi-persona-review
description: Dispatches 5-8 selected personas (from ~/.hermes/profiles/personas/) in parallel against a deliverable. Synthesizes via tied-weakest heuristic. Higher-fidelity than single-pass adversarial-reviewer for high-stakes drafts.
version: 1.0.0
tags: [quality, review, personas, harbor, multi-agent]
tier: B
owning_profile: orchestrator
dispatches_to: ["personas/*"]
moat_test: "Uses HARBOR's 27-persona reviewer library + draft-type-specific persona selection (federal CO + privacy counsel for SOW; CFO + product owner for SaaS roadmap). Generic LLM review cannot match this."
---

# Multi-Persona Review

The Tier B reviewer. Dispatches 5-8 persona profiles in parallel as adversarial lenses. Synthesizes with the tied-weakest dimension as the headline finding.

**One-line:** Many critics in parallel beat one critic.

## When to load this skill

- High-stakes deliverables: SOWs, Pre-Assessments, $50K+ proposals, public blog posts, book chapters
- Quarterly when used for the published HARBOR Index report
- Manual invocation when `adversarial-reviewer` is ambiguous

For day-to-day briefings, use `adversarial-reviewer` (Tier A, single-pass, faster, cheaper).

## Inputs

```json
{
  "draft_path": "...",
  "draft_type": "...",   // same enum as adversarial-reviewer
  "persona_selection": "auto" | ["cfo", "fedramp-auditor", "..."],
  "rubric_dimensions": "constitution-derived" | ["specificity","cite-density",...],
  "synthesis_model": "deepseek-v4-pro"  // synthesis uses pro; per-persona uses flash
}
```

## Persona selection (`auto`)

By draft_type, the auto-selector picks 5-8 personas with appropriate lenses:

| Draft type | Default personas (selectable count 5-8) |
|---|---|
| sow | customer-voice-federal-co, cfo, compliance-owner, fedramp-auditor (if cloud), pricing-strategist, gap-analyst |
| pre-assessment | strategic-advisor, founder-investor, cfo, market-analyst-federal, gap-analyst, sector-specific (energy/finance/healthcare per client industry) |
| competitive-canvas | strategic-advisor, gap-analyst, sales-lead, market-analyst-federal, customer-voice-federal-co |
| intel-canvas | gap-analyst, strategic-advisor, market-analyst-federal, founder-investor |
| meeting-prep | sales-lead, strategic-advisor, customer-voice-federal-co (if federal target), persona matched to target's industry |
| linkedin-long-form / blog | strategic-advisor, sales-lead, gap-analyst, voice-specific (Amyn-as-author calibration) |
| daily-briefing | (skip — use adversarial-reviewer; daily volume doesn't justify multi-persona cost) |
| sbir-proposal | customer-voice-federal-co, compliance-owner, pricing-strategist, engineering-lead, product-owner, sector-specific |

The auto-selector reads draft frontmatter (or asks the caller) for client industry and uses that to pick sector personas.

## Workflow

### Phase 1: Persona selection

If `persona_selection: "auto"`, run the selector. Otherwise honor the explicit list.

### Phase 2: Parallel persona reviews

Dispatch each persona as a separate Hermes subagent call. Each persona profile's SOUL.md (in `~/.hermes/profiles/personas/<slug>/SOUL.md`) defines its review dimensions and output format.

Each persona returns:
```json
{
  "persona": "cfo",
  "dimensions": [
    {"name": "unit economics", "score": 1-5, "finding": "...", "evidence_required": "..."},
    {"name": "payback period", "score": 1-5, "finding": "...", "evidence_required": "..."}
  ],
  "overall_score": 1-5,
  "tied_weakest_dimension": "payback period",
  "recommendation": "ship | revise | reject"
}
```

Use deepseek-v4-flash for each persona call (cost discipline).

### Phase 3: Synthesis

Aggregate all persona outputs. Identify the dimension(s) tied for lowest score across personas — that's the systemic weakness. Use pro for synthesis (it's a small but high-leverage call).

Synthesis prompt:
```
You have N persona reviews of the same draft. Synthesize:
1. The dimension(s) tied for weakest across personas — this is the systemic gap.
2. Cross-persona consensus (any finding flagged by ≥3 personas)
3. Cross-persona disagreement (personas that scored very different)
4. Overall recommendation: ship | revise | reject

Return JSON with verdict, tied-weakest, consensus, disagreements, top 3 fix recommendations.
```

### Phase 4: Persist + return

Write to `~/.hermes/cron/output/${HERMES_CRON_ID:-manual}/multi-persona-review-${draft_id}-${ts}.json`.

Append summary to `~/.hermes/state/review-log.jsonl`.

Return the synthesis JSON.

## Cost economics

5-8 persona calls (flash) + 1 synthesis (pro). ~$0.05-0.15 per high-stakes review. Reserve for $50K+ proposals where the cost is 0.0003% of deal value.

## Related

- v2.0 §2.3 (persona port)
- v2.0 §3.2 (single-pass reviewer companion)
- `~/.hermes/profiles/personas/` — 27 persona profiles
- HARBOR Constitution (always inherited)
