---
name: adversarial-release-review
description: When preparing a deliverable for client submission and the user wants
  adversarial quality review — dispatches parallel agents with detailed personas (evaluator
  POV, source auditor, design steward, editorial QA, technical accuracy, artifact
  auditor, methodology reviewer, RFP compliance) to produce structured PASS/FLAG findings.
---

# Adversarial Release Review

Use when the user wants a thorough review of a client-facing deliverable before submission. Dispatches 6-8 independent parallel read-only review agents, each with a specific adversarial or technical persona.

## When to Use
- User says "review everything," "adversarial review," "multiple agents reviewing," or wants a second opinion on a deliverable.
- Client-facing documents (proposals, white papers, briefs, reports) before submission.

## Agent Slots (dispatch in one batch)

### Core (always include)
1. **AdversarialEvaluatorPOV** — skeptical target-audience evaluator. Reads the document as the actual recipient would. Persona: "You are a [target role] with [N] years of experience. You distrust jargon and inflated claims." Checks: factual accuracy, claims vs evidence, tone, whether it reads as standalone vs appendix, would you hand this to a [senior stakeholder] without embarrassment.

2. **SourceEvidenceAuditor** — forensic trace-every-claim auditor. Checks: all endnotes present and correctly numbered, every public URL resolves, statistics traced to primary sources, caveats present, no unsourced claims.

3. **DesignBrandIntegrity** — brand steward reviewing visual system, typography, color tokens, logo marks, layout geometry, and accessibility. Checks against approved brand guidelines.

4. **CopyEditorialReviewer** — managing editor checking exact approved copy, prohibited phrases, tone/register, word counts, dates, bylines, disclaimers. Cross-references against the canonical plan or spec.

5. **ArtifactDeliveryAuditor** — release manager checking file completeness, PDF contract (pages, dimensions, tagged, encrypted), PNG dimensions, link annotations, pdftotext extraction, stale files.

### Context-dependent
6. **RFPComplianceAdversarial** — if responding to an RFP: checks for disqualifying content (pricing in public docs, unauthorized personnel names, internal proposal mechanics, scope overreach, prohibited phrases). This is the highest-stakes review.

7. **TechnicalAccuracy** — if the document makes technical claims: checks tool names, version numbers, API/product claims, complementarity language, unsupported performance assertions.

8. **MethodologyReviewer** — if the document includes benchmarks, comparisons, or analytical frameworks: checks methodology description, ranking language, caveats, data categories.

## Contract
Every agent MUST return structured findings:
```json
{"verdict":"PASS"|"FLAG","findings":[{"severity":"critical"|"important"|"advisory","location":"<file:line or URL>","claim":"<what is asserted>","problem":"<what is wrong>","fix":"<minimum fix>"}]}
```
If PASS, findings array is empty.

## Rules
- READ ONLY — agents never edit files.
- Every claim MUST cite exact evidence (file:line, URL, tool output).
- Agents are `scout` type — they only read and report.
- Dispatch all agents in one `task` call for maximum parallelism.
- Present adversarial evaluator's honest reactions to the user without sanding them down — even if the flagged items were previously approved. Frame as "the evaluator will notice this — are you comfortable?"
