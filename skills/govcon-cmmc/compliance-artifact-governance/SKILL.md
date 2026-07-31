---
name: compliance-artifact-governance
description: "Sustainable governance model for AI-generated compliance artifacts — standards change detection (NIST, CMMC, FedRAMP, DFARS, EOs), agentic validation pipeline with adversarial review gates, artifact storage and lifecycle, confidence thresholds, cron-based monitoring, and Hermes infrastructure integration."
version: 1.0.0
category: govcon
tags: [compliance, governance, cmmc, fedramp, nist, dfars, validation, adversarial-review, cron, ai-artifacts]
---

# Compliance Artifact Governance Model

Design and operate a sustainable governance model for AI-generated compliance artifacts in a GovCon context. This skill encodes the full architecture: standards change detection, agentic validation pipeline with adversarial review gates, artifact storage and lifecycle, confidence thresholds, cron-based monitoring, and integration with existing Hermes infrastructure.

## When to Use

- Designing or setting up a compliance artifact governance system
- Configuring standards change monitoring for NIST, CMMC, FedRAMP, DFARS, or Executive Orders
- Building or tuning a multi-gate validation pipeline for AI-generated compliance content
- Defining confidence thresholds for automated vs. human-reviewed compliance artifacts
- Setting up Hermes cron jobs for compliance monitoring and artifact auditing
- Troubleshooting when a validation gate is failing too often or too rarely
- Responding to a detected standards change (NIST revision, CMMC rule update, etc.)

## Core Architecture

### Standards Change Detection (3 Tiers)

**Tier 1:** Firecrawl URL monitors + Hermes cron for page-level change detection on NIST CSRC, FedRAMP.gov, DoD CIO CMMC page, Federal Register, Cornell LII, White House.

**Tier 2:** Agent pipeline (Classify → Impact Analysis → Recommendation Engine → Judge Validation) triggered when Tier 1 detects a substantive change.

**Tier 3:** Artifact update queuing via Kanban board for validated recommendations.

### Agentic Validation Pipeline (5 Gates)

**Gate 1:** Technical Accuracy (Senior C3PAO assessor persona)
**Gate 2:** Cross-Artifact Consistency (Compliance program manager persona)
**Gate 3:** Completeness (CMMC documentation auditor persona)
**Gate 4:** Adversarial Review (Hostile DIBCAC auditor / contracting officer persona)
**Gate 5:** Human Review (Mandatory final gate)

Gates 1–3 run in parallel. Gate 4 runs sequentially after they pass. Gate 5 is always human.

### Confidence Scoring

Composite score = (accuracy × 0.35) + (consistency × 0.20) + (completeness × 0.15) + (adversarial × 0.30)

Tiers: HIGH (≥0.85), MEDIUM (0.70–0.84), LOW (0.50–0.69), REJECT (<0.50)

Special thresholds: fabricated citations auto-REJECT; outdated standard revision drops to LOW; cross-artifact contradiction drops both artifacts one tier.

### Artifact Lifecycle

States: DRAFT → REVIEW → AUTHORITATIVE → SUPERSEDED → ARCHIVED
(REJECTED is a terminal state from any point)

### Cron Schedule

- **Daily:** EO/OMB monitor (Mon–Fri), artifact health check, confidence trending
- **Weekly:** NIST 800-53/171 (Mon), FedRAMP (Tue), CMMC (Wed), DFARS (Thu), pipeline health (Fri), staleness sweep (Sat)
- **Monthly:** Cross-standard audit (1st), corpus consistency (15th), registry cleanup (28th)
- **Quarterly:** Full corpus re-validation (1st), pipeline tuning (2nd), adversarial persona rotation (3rd)

## Reference Files

- `references/monitoring-urls.yaml` — Complete URL inventory with schedules, goals, and cadences
- `references/gate-criteria.yaml` — Full gate criteria schemas, scoring methodologies, and output formats
- `references/cron-schedule.yaml` — Machine-readable cron job definitions with prompts and configurations

## Metadata Files (in ~/.hermes/compliance-artifacts/metadata/)

- `artifact-registry.json` — Index of all artifacts with state, scores, and dates
- `change-log.jsonl` — Append-only log of all state transitions

## Key Rules

1. **Every AI-generated compliance artifact MUST pass all 4 agent gates before human review.** No exceptions.
2. **Fabricated citations = auto-REJECT.** This is the cardinal sin.
3. **Maximum 3 iteration cycles** per artifact before mandatory human intervention.
4. **Adversarial reviewer persona MUST rotate quarterly** to prevent rubber-stamping.
5. **Artifacts referencing outdated standards drop to LOW tier** regardless of other scores.
6. **Human review is mandatory at Gate 5.** AI agents cannot authorize artifacts.
7. **Never represent internal mock assessments as external C3PAO findings.**
8. **When DFARS 7012 is cited, use the exact regulatory text:** "security requirements equivalent to those established by the Government for the FedRAMP Moderate baseline" — NOT "FedRAMP authorization at the Moderate or High baseline."

## Integration with Other Skills

- `cmmc-l2-compliance-toolkit` — CMMC L2 assessment lifecycle, control extraction, SOP templates, regulatory citations
- `fedramp-vendor-research` — FedRAMP Marketplace navigation, authorization paths, terminology, DFARS 7012 compliance
- `multi-agent-judge-loop` — Judge agent patterns, adversarial review criteria, fix-gate workflow
- `hermes-cron-patterns` — Cron job scheduling, time-windowing, script-only watchdogs, health checks
- `orchestrator-agent-workflows` — Subagent dispatch, reasoning effort levels, cost optimization

## Pitfalls

- **Judge reads wrong source file and produces false positives.** Always specify exact file paths in judge dispatch. Name files distinctively (RAW-SOURCE vs summary).
- **Fabricated quote survives one round of corrections.** Search the file for remnants of fabricated text after fixing; verify removal at source text level, not just by existence of a correction callout.
- **Grep alternation escaping.** `grep -qiE "Purpose\\|Scope"` is WRONG in ERE mode (literal backslash-pipe). Use `grep -qiE "Purpose|Scope"` or separate per-term checks.
- **Endless judge loop.** After 2 revision cycles, take over final evaluation yourself. Max 3 cycles total.
- **Judge only catches factual errors, misses framing errors.** Add framing criteria to adversarial review: "Is the causal direction of claims correct? Does the artifact imply retroactive rule application?"
- **CMMC 1.0 vs 2.0 scoring confusion.** 2.0 uses 110-point scale (MET/NOT MET/N/A), NOT 1.0's 1000-point weighted scale. Always load `cmmc-l2-compliance-toolkit` references before writing scoring details.
- **Internal assessment ≠ external audit.** Frame mock assessment output as internal analysis, never as C3PAO findings.
