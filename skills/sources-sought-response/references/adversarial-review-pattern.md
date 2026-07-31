# Multi-Persona Adversarial Review for Sources Sought Responses

## When to Run

After a Sources Sought or capability statement draft exists and the actual PWS document has been extracted. The goal is to identify weaknesses, misalignments, and credibility gaps before submission from three distinct evaluator perspectives.

## The Three-Persona Panel

Dispatch THREE review agents in parallel, each with a specific evaluator persona and the current draft + PWS + domain research:

### 1. KO Compliance Review

Role: The Contracting Officer who issued the notice. Evaluates format compliance, content completeness, and whether they would put the respondent on the interested vendors list.

Evaluation criteria: Format compliance (page limits, margins, fonts, cover page elements), content completeness (all PWS roles/deliverables addressed), credibility (claims vs evidence), competitive differentiation, submission readiness.

Key question: "Would I put them on the interested vendors list?"

### 2. Technical Evaluator Review

Role: Federal IT technical evaluator. Evaluates whether proposed technical solutions are viable, architecture makes sense, and the team can actually deliver.

Evaluation criteria: Product viability, architecture soundness, build vs buy analysis, team feasibility, AI claims credibility, PWS technical coverage gaps.

Key question: "Can they actually build and deliver this?"

### 3. Program Lead Review

Role: The government program person who needs the work done. Evaluates whether the respondent understands the agency's actual problem and whether the proposed solution would help.

Evaluation criteria: Problem understanding, solution fit, team credibility, practical concerns, overall advocacy.

Key question: "Would I advocate for this respondent to my leadership?"

## Dispatch Pattern

```
delegate_task with tasks array of 3, all role=leaf
Each task gets: the file path, the PWS text, domain research, and the specific persona + evaluation criteria
Output: ~/sources-sought-responses/reviews/<notice-id>-ko-review.md etc.
```

## Common Findings to Expect

- KO review: Contact placeholders, DUNS missing, page limit violations, FAR Part citation errors
- Technical review: Architecture under-specified, missing platform components (Power BI, data model), build vs buy gaps
- Program Lead review: Team size vs scope mismatch, product/consulting ratio wrong, no direct VMO experience

## Session-Validated Pitfalls (July 2026 HHS ASPR Sources Sought)

These pitfalls were confirmed when three reviewers independently flagged the same issues. They are high-confidence.

### P0: Category Error — Answering the Wrong Question

The response proposes a fundamentally different solution than the SSN requested (e.g., asking for SaaS, proposing custom build). All three personas independently call this a P0. **How to catch it:** Read only the opening sentence of each section. Would the CO know which SSN this responds to? If the value proposition doesn't match the SSN's question (SaaS vs. build, product vs. services), it's a category error. Fix: either reframe to match the SSN, or add an explicit "What We Cannot Provide" section at the top.

### P0: Technical Data Source Claims Must Be Verified

A technical evaluator who verifies claims against actual documentation can destroy credibility. Common errors:
- Claiming FDA enforcement databases (Warning Letters, Form 483s) are REST APIs when they are individual PDF/HTML documents
- Claiming OFAC SDN, HHS OIG LEIE, BIS Entity Lists are APIs when they are downloadable flat files (CSV, .txt)
- Claiming DEA registrant data is integrable via API when only a manual web form exists
- **How to prevent:** Before submission, have the technical reviewer verify every "API" or "database" claim against the source's actual documentation.

### P1: "Honest Disclosure" Strategy for Non-Responsive Submissions

When the entity cannot provide what the SSN requests, leading with honesty scores better with reviewers than stretching to pretend. The validated pattern:
1. Open section: "We cannot provide X. If this results in a solicitation for X, we will not submit."
2. Middle: "We are responding to share research and propose an alternative approach."
3. Close: "If you are open to the alternative, we're available. If not, we understand."

This was specifically noted by the Program Lead reviewer as "operationally useful" — it saves the evaluation team the work of disqualifying you and demonstrates integrity.

### P2: Sources Sought Format Constraints

Sources Sought notices rarely specify page limits, font sizes, or formatting requirements. Always check the Attachments/Links section on SAM.gov for any formatting guidance PDFs. If none exist, standard 10.5-12pt TNR with 0.8-1in margins in 3-5 pages is the norm. Document the absence of format specs in the review notes.

## After the Reviews

Apply fixes in priority order: P0 (fatal) first, then P1 (major), then P2 (minor). Re-render PDF and verify page count after each batch of fixes.
