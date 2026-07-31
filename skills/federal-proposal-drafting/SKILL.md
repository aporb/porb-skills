---
name: federal-proposal-drafting
description: Draft full federal cooperative agreement and grant proposal narratives (SF-424, DOS NOFOs, assistance awards). Covers multi-source research synthesis, 13-section DOS proposal structure, 15pt Open Sans pagination estimation, for-profit/no-profit constraint handling, mandatory workstream coverage rules, and the trim-to-page-limit workflow. Complements sources-sought-response (shorter documents) and federal-grant-budget (financial side).
tags:
  - govcon
  - proposals
  - state-department
  - cooperative-agreement
  - grants
---

# Federal Proposal Drafting

## When to Use
When a user asks you to draft a full federal cooperative agreement or grant proposal narrative — NOT a Sources Sought response, capability statement, or budget narrative alone. This is the core 20-page (or similar) narrative document submitted to an agency like State/ACN, USAID, DoD, etc. For shorter documents, use `sources-sought-response`. For budgets, use `federal-grant-budget`. For adversarial review after drafting, use `govcon-response-adversarial-review`.

## Full Pursuit Pipeline (5 Phases)

This skill covers the full lifecycle from raw NOFO to submission-ready package with Word documents. The phases are sequential but sub-agents can run in parallel within each phase.

### Phase 1: Research (Parallel Agents)

Before ANY planning or drafting, build the complete intelligence picture. Dispatch parallel research agents:

1. **Requirements Analysis Agent:** Extract every requirement from the NOFO — structure, format, evaluation criteria, mandatory sections, compliance traps. Output a comprehensive checklist.
2. **Program/Domain Intelligence Agent:** Research the agency's prior awards via USASpending, identify incumbents, map the competitive landscape, find prior related programs.
3. **Domain Expertise Agent:** Build deep subject-matter knowledge the proposal must demonstrate (export controls, trade data, AI/ML, etc.).
4. **Mechanics Agent:** Research submission systems (MyGrants, Grants.gov, BAAT), forms required (SF-424 family), compliance certifications, budget template rules.

**Key rule:** Agents MUST write their findings to named output files. The orchestrator reads ALL outputs before beginning Phase 2.

### Phase 2: Plan (Pursuit Plan HTML)

Write a self-contained HTML pursuit plan with Thariq/html-effectiveness tokens (ivory #FAF9F5, clay #D97757, slate #141413). Publish to Nextcloud briefings. The plan must contain:
- Go/no-go recommendation with honest winnability assessment
- Artifact inventory (every required document with owner, format, page limit, status)
- Day-by-day countdown with gates and owners (distribute across the full team — don't put everything on two people)
- Teaming gaps (who needs to be recruited, by when)
- Risk register with severity and mitigation owners
- Competitive field analysis
- Evaluation criteria with scoring strategy

### Phase 3: Implement (Parallel Drafting Agents)

Dispatch parallel agents for ALL artifacts simultaneously. Give each agent ALL Phase 1 research outputs as context (they have no memory of the conversation):
1. **Proposal Narrative Agent:** Draft the complete narrative — all mandatory sections, all workstreams, proper voice, domain depth.
2. **Budget Package Agent:** Build detailed line-item budget, budget narrative, and SF-424A mapping. Must solve for the exact total using the MTDC equation. Use `federal-grant-budget` for guidance.
3. **Supporting Documents Agent:** Draft SOW (outline form — 2 pages MAX), Risk Assessment, and M&E Plan with output AND outcome indicators.

### Phase 4: Review & Fix (Adversarial + Compliance)

Dispatch two review agents in parallel:
1. **Adversarial Review Agent:** Score the full package against the NOFO's ACTUAL evaluation criteria using their specific weights. Use `govcon-response-adversarial-review`. Produce CRITICAL/MAJOR/MINOR findings with line references and a 0-100 weighted score.
2. **Compliance Review Agent:** Check every mechanical requirement — font, margins, page limits, file naming, budget math, attachment order, prohibited references. Use `references/compliance-checklist.md`.

Then dispatch fix agents to resolve ALL CRITICAL and MAJOR findings. After fixes, verify changes propagated correctly before proceeding.

**Personnel/budget reconciliation is the #1 failure point.** After fixes, always check: do the named individuals in the narrative exist in the budget with matching FTEs and salaries? Budget line items MUST reference named key personnel by name, FTEs MUST match, and no person listed in the narrative should be missing from the budget.

### Phase 5: Summary & Package Assembly

1. **Convert markdown to Word:** Use `convert_to_docx.py` (see `references/markdown-to-docx-conversion.md`) to produce properly formatted .docx files with correct fonts (15pt Open Sans for narrative, Calibri 12pt for budget), 1-inch margins, and single-spacing.
2. **Create remaining attachments:** De minimis election statement, Single Audit statement, etc.
3. **Assemble final package:** README mapping attachments A-J to files, all Word docs in one folder.
4. **Copy to Nextcloud** for team access (`/data/nextcloud/data/amyn/files/Documents/`), run `docker exec --user www-data nextcloud php occ files:scan`.
5. **Write final briefing HTML** with before/after scorecard, artifact inventory, remaining steps, and open risks.
6. **Optionally create Zoho Mail draft** (`.eml` to `~/repos/2026_books/operations/mail/zoho/Drafts/cur/` or HTML paste-into-browser at `brief.h.porb.dev`).
7. **Commit to GitHub:** Initialize repo, push all research + artifacts + final package.

## Drafting Workflow (Phase 3 Detail)

### Step 1: Ingest All Phase 1 Research
Read ALL research outputs before starting any draft.

### Step 2: Map the Mandatory Structure
Extract every mandatory section from the NOFO. For DOS cooperative agreements, the standard is 11 items (see `references/dos-13-section-structure.md` for expanded 13-section version). If any workstream/line-of-effort is mandatory and missing = disqualification.

### Step 3: Draft at Full Fidelity
Write the complete first draft without worrying about page limits. This draft typically runs 2x the target word count.

### Step 4: Trim to Page Limit
Use font-specific pagination estimates in `references/font-pagination.md`. For 15pt Open Sans single-spaced with mixed formatting, use ~240–280 words per page.

### Step 5: Compliance Verification
Run final checks on mandatory sections, workstreams, budget ceiling, for-profit constraints, past performance claims, and prohibited entity references.

## Key Constraints to Enforce

### Hard Page Limits
DOS NOFOs enforce strict page limits. Non-compliant proposals may be rejected before evaluation. Always verify the font, margin, and spacing specs before estimating page count.

### SBA SCALE NOFO Structure (Non-DOS Grant Pattern)

The SBA SCALE program (SBA-OIIGA-26-001) uses a different structure from DOS cooperative agreements. Application components:

- **Cover Letter (1 page):** NOFO number, applicant name/address/UEI, POC, dollar amount requested.
- **Technical Approach (5 pages max, 12pt TNR single-spaced, 80 points):**
  - Supply Chain Challenge and Opportunity (20 pts, ~1 page)
  - Small Business Support Programming (45 pts, ~3 pages) — activities, partnerships, recruitment plan
  - Key Milestones and Outcomes (15 pts, ~1 page) — 2-year plan with quantified goals
- **Organizational Qualifications (5 pages max, 20 points):**
  - Organizational Mission and Viability (4 pts)
  - Project Team and Management Approach (4 pts)
  - Data Collection, Reporting, and Performance Management (4 pts)
  - Relevant Experience and Past Performance (8 pts)
- **Attachments:** Resumes (2 pages max each), SF-424/SF-424A, Budget Narrative, COI Policy per 2 CFR 2701.112, Org Chart, Financial Statements (in lieu of A-133 for new entities)
- **Eligibility:** For-profit, nonprofit, public/private entities all eligible. 15% de minimis on MTDC if no NICRA. No pass-through/fiscal agent arrangements. Max 49% of work subcontracted.
- **Supply Chain Priorities:** Defense Industrial Base, Advanced Manufacturing, Biotechnology, Energy/Critical Materials, Food/Agriculture, Transportation/Logistics.
- **New entity tip:** No A-133 audit? Submit "most recent financial statements." A bank statement with opening balance + signed explanation letter satisfies this for entities under 6 months old.

### Mandatory Workstream Coverage
Some NOFOs (e.g., DFOP0018157) require ALL lines of effort to be addressed. Missing any = "deemed non-responsive and disqualified." Always check for this language.

### For-Profit / No-Profit Rules
DOS assistance awards prohibit profit or fee to for-profit organizations. The proposal must explicitly acknowledge this and explain the cost-recovery structure. Never include margin, markup, or profit elements. Address the 15% de minimis indirect rate on MTDC (2 CFR 200.414(f)) as the cleanest path for entities without a NICRA.

### No Invented Past Performance
If the applying entity has no prior federal experience, frame around (a) individual key personnel qualifications, (b) sub-awardee organizational past performance (explicitly allowed by many NOFOs), and (c) purpose-built internal controls. Be transparent — evaluators prefer honest disclosure over detectable overstatement.

### IP Language
DOS NOFOs follow 2 CFR 200.315: background IP is protected, new IP developed under the award gets a government royalty-free nonexclusive license, and the recipient retains ownership and commercialization rights. Frame all IP discussion accordingly.

## Common Pitfalls
- **Writing to page limit from the start:** produces thin, uncompetitive proposals. Always over-write then trim.
- **Treating all sections as equal weight:** Problem Statement and Workstream descriptions get the most evaluator attention. MEL Plan and Future Funding get less. Allocate word budget accordingly.
- **Inventing past performance:** "We have extensive experience in..." when the entity is brand new. Frame individual qualifications honestly instead.
- **Missing the Workstream B technical credibility:** AI/ML proposals must name specific architectures, training data quantities, accuracy targets, and deployment constraints. Generic AI language loses to specific technical proposals.
- **Forgetting the cooperative agreement "substantial involvement" implications:** approval gates, review cycles, and shared responsibilities must be reflected in the schedule and methods sections.
- **Personnel/budget mismatch (THE #1 FAILURE):** The narrative names individuals (Henderson, Porbanderwala, Payne, Frawley) but the budget lists different positions with none of those names. This is an automatic scoring failure — the evaluator cannot score personnel who are not in the budget. Always cross-check after Phase 4 fixes: every named person in the narrative MUST appear in the budget with matching FTE and salary.
- **Conflicting numbers across documents:** MVP delivery dates (Month 6 vs Month 8 vs Month 9), training targets (120 vs 240 officials), accuracy metrics (top-1 vs top-3 vs top-5) must be IDENTICAL in narrative, SOW, budget, and M&E plan. Pick ONE authoritative value and propagate everywhere via global search-and-replace.
- **Drafting agents invent past performance:** When given entity facts (new LLC, $0 federal contracts), drafting agents may still write "We have extensive experience in..." GATE THIS. Give every drafting agent an explicit constraint: "NO invented past performance. Frame ALL experience as individual/key personnel qualifications."
- **Never reuse proposal-generated bios as authoritative for a new proposal.** A prior proposal's resume package (e.g., DFOP structural fixes) was written to win funding and may have systematically inflated every team member's credentials. The Company Charter v2 — the entity's own formal document — contradicted 12 claims across 3 people including a fabricated MBA and a fabricated COO title. Before any new proposal, verify every credential against the entity's own charter, internal dossiers compiled from actual interviews, and working files showing current job titles. Proposal-generated bios are the lowest-trust source for personnel facts. Build a source hierarchy: entity charter > internal dossiers > working files > call transcripts > marketing website > prior proposal artifacts.
- **Stacking all tasks on two people:** The artifact inventory and countdown must reflect the full team. Contracts/budget to the contracts lead (DAWIA III). Risk to compliance lead. Technical to technology lead. BD/capture to program director.
- **Verify SBIR/contract completion dates before framing as active obligations.** A completed SBIR (ended Feb 2026) was repeatedly described as "active" and used to artificially constrain FTE and add unnecessary disclosure requirements. A completed federal credential is stronger than an active one — no overlap, no disclosure, full FTE available. Cross-reference against the entity charter or personnel dossier for completion dates before writing any "active obligations" language. This applies to any former federal contract, grant, or SBIR — if it ended, frame it as a completed credential, not an active conflict.
- **Phone numbers must be verified per-person.** The user's phone number is 210-595-9401. Each key personnel has their own number (e.g., Douglas Henderson: 803-904-3500). Never use one person's phone for another. If an email or document includes "call me" contact text, verify it uses that person's number, not a team member's.
- **Cost share via uncompensated member effort is allowed and strengthens proposals.** For new LLCs where the members already have day-job compensation (e.g., at Aecon FCS), they can contribute uncompensated FTE as cost share. This reduces the grant-funded personnel line, demonstrates organizational commitment, and keeps the total under the award cap. Document clearly in the budget narrative.

## Reconciliation After Review
When an adversarial review or compliance review produces a prioritized fix list spanning multiple documents, use the reconciliation workflow in `references/reconciliation-from-review-findings.md`. Key rules:
- **Fix the budget file first** — all dollar figures cascade downstream through fringe, MTDC, indirect, and SF-424A.
- **Preserve the personnel total** when reconciling named individuals to budget positions. Change names, redistribute within the envelope, but keep the total constant to avoid recalculating everything.
- **Pick authoritative values for every conflicting number** (MVP date, training targets, accuracy metrics, language counts), document the choice, and propagate to all three documents.
- **SOW page limits are real**: remove Inputs/Outputs/Indicators substructure and collapse to single-line bullets per activity. Detailed indicator targets belong in the M&E Plan, not the SOW.

## References
- `references/font-pagination.md` — Font-to-page-count estimation table for common federal submission specs
- `references/dos-13-section-structure.md` — Expanded 13-section DOS cooperative agreement proposal structure with word budgets
- `references/reconciliation-from-review-findings.md` — How to fix multiple documents after adversarial review without breaking consistency
- `references/markdown-to-docx-conversion.md` — Converting markdown artifacts to properly formatted Word documents with NOFO-compliant fonts, margins, and spacing