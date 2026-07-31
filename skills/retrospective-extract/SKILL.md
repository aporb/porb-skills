---
name: retrospective-extract
description: End-of-engagement retrospective extractor. 10-question protocol that captures compliance patterns, procurement timelines, decision-maker preferences, and gotchas into pipeline.db.engagement_patterns. The data-moat compounder.
version: 1.0.0
tags: [strategy, retrospective, data-moat, harbor, constitution-p9]
tier: A
owning_profile: orchestrator
moat_test: "Builds HARBOR's accumulating engagement-pattern data moat per Thiel framework. Each retrospective compounds knowledge that future prospect work auto-retrieves."
---

# Retrospective Extract

When an engagement closes (won OR lost), capture what we learned in structured form
so the next engagement starts smarter.

**One-line:** Ten questions, ten patterns, one data-moat increment.

## When to load this skill

- An engagement transitions to `Closed-Won` or `Closed-Lost` in pipeline.db
- Manual invocation after a major milestone (Sprint complete, Pilot complete)
- Quarterly when reviewing all closed engagements for cross-engagement themes

## Inputs

```yaml
prospect_slug: "ace-of-cloud"
outcome: "Closed-Won" | "Closed-Lost" | "Paused" | "Sprint-Complete" | "Pilot-Complete"
amyn_notes: ""    # optional, freeform context Amyn wants to seed
```

## The 10 questions (forced — must all be answered)

Each question maps to one or more `engagement_patterns.pattern_type` rows in pipeline.db.

1. **What compliance framework surfaced as the binding constraint?** (CMMC tier, FedRAMP level, ATO, NIST 800-171, SOC 2, ITAR, EAR…)
2. **What procurement vehicle was used or required?** (8(a), GSA MAS, IDIQ, BPA, OTA, Phase III sole-source, commercial item, BAA, SBIR sequels…)
3. **How long did the timeline actually take vs what we predicted at scoping?** (Capture: predicted-X-weeks, actual-Y-weeks, primary slip driver)
4. **What decision-maker preferences did we learn?** (Communication style, meeting cadence, deck format, slide count, what they push back on)
5. **What were the gotchas we didn't see coming?** (Hidden dependencies, blocking stakeholders, technical traps, contractual surprises)
6. **What pattern is now repeatable for HARBOR's playbook?** (One sentence — generalizable, not engagement-specific)
7. **What sector-quirk surfaced that adjacent prospects share?** (Energy/finance/healthcare-specific norms, federal-vs-commercial-vs-state quirks)
8. **What HARBOR methodology stage scored highest/lowest?** (H/A/R/B/O/R — score each 0-100, identify highest + lowest)
9. **What referral-network signal emerged?** (Who introduced whom, who blocked, who endorsed)
10. **If we ran a Sprint identical to this one in 90 days, what's the ONE thing we'd change?** (The biggest learning)

## Workflow

### Phase 1: Pull engagement artifacts

- Read all artifacts from `pipeline.db artifacts WHERE prospect_slug = {slug}`
- Read all touches from `pipeline.db touches WHERE prospect_slug = {slug}`
- Read the original Pre-Assessment from `~/HARBOR/clients/{slug}/`
- Read the SOW + any deliverables

### Phase 2: Run the 10-question protocol

For each question:
1. Surface relevant artifact excerpts (cite source for evidence)
2. Pose the question to Amyn (via Telegram if interactive, or as an "Amyn-input-required" slot if batch)
3. Capture the answer
4. Map to `pattern_type` (Phase 3)

If Amyn isn't available, generate best-effort answers from artifacts + flag each as
`(needs Amyn confirmation)` in the database.

### Phase 3: Persist to engagement_patterns

For each pattern surfaced, INSERT into pipeline.db:

```sql
INSERT INTO engagement_patterns (prospect_slug, pattern_type, description, captured_at, indexed_to_rag)
VALUES (
  '{slug}',
  '{compliance-framework | procurement-vehicle | decision-maker-preference | timeline-actual |
    gotcha | repeatable-insight | sector-quirk | vehicle-gap}',
  '<full description>',
  datetime('now'),
  0  -- not yet RAG-indexed; vault-embedding-sync cron picks this up
);
```

### Phase 4: RAG-index the patterns

Write each pattern as a markdown note to `~/repos/henry-hermes-vault/harbor/patterns/{prospect_slug}/{pattern_type}-{timestamp}.md`:

```markdown
---
prospect: {slug}
type: {pattern_type}
captured: {iso}
outcome: {Closed-Won|Closed-Lost|...}
---

# {pattern_type} — {prospect_name}

{description}

## Evidence
- {source artifact or touch reference}

## Why this is repeatable
{generalization across engagements}
```

The vault-embedding-sync cron (hourly) embeds these into pgvector with `metadata.harbor_pattern=true`.

Future prospect work auto-retrieves: `rag_search("compliance pattern federal cyber")` surfaces
all CMMC patterns we've seen, weighted by recency.

### Phase 5: Update prospect closure

```bash
pipeline-manager.py prospect set-stage {slug} --stage {outcome} --next-action "(closed)"
pipeline-manager.py decision add --slug "{date}-{slug}-retrospective" \
  --type ops --context "Engagement closed with outcome {outcome}" \
  --decision "Captured {N} engagement_patterns" \
  --rationale "Quarterly retrospective review will surface cross-engagement themes" \
  --review-date "<next quarterly>"
```

### Phase 6: Generate the retrospective HTML

`~/HARBOR/clients/{slug}/retrospective-{date}.html`:

- The 10 Q&As
- The captured patterns table
- The HARBOR methodology stage scoring chart
- The "one thing we'd change" callout

Deliver to Telegram.

## Quarterly cross-engagement synthesis

Quarterly, query all engagement_patterns rows added in the last 90 days:

```sql
SELECT pattern_type, COUNT(*), GROUP_CONCAT(prospect_slug)
FROM engagement_patterns
WHERE captured_at > datetime('now', '-90 days')
GROUP BY pattern_type
ORDER BY COUNT(*) DESC;
```

If any pattern_type appears in ≥3 engagements, surface it as a HARBOR Index entry —
the public-facing anonymized aggregate per v2.0 §5.6 ("After fifty engagements, you're the authority").

## Cost

~$0.10-0.20 per engagement retrospective (10 questions × flash-tier per answer + persistence).

## Related

- v2.0 §5.6 (this skill)
- pipeline.db engagement_patterns table (schema defined in pipeline-init.sql)
- vault-embedding-sync cron (indexes the patterns into pgvector)
- decision-log skill (closure decision logged)
- HARBOR Constitution P9 (decisions logged + reviewed)
- Thiel framework: "The moat is context, not model" — this skill IS the context-build mechanism
