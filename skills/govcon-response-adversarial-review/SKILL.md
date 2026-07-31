---
name: govcon-response-adversarial-review
description: "Adversarial review of Sources Sought responses, proposals, and capability statements against their governing PWS/PD/SOW. Brutal line-by-line comparison with fact-checking of external claims, PWS coverage audit, and prioritized fix list (P0/P1/P2). Scores across accuracy, alignment, specificity, credibility, and structure. Used after a response draft exists and the actual PWS document has been extracted."
version: 1.0.0
author: Hermes Agent
trigger:
  - "adversarial review"
  - "red team"
  - "color team review"
  - "compare response to PWS"
  - "gap analysis against PWS"
  - "brutal review"
  - "team credential review"
  - "bio cross-reference"
  - "gap-to-strength"
  - "compare draft to bios"
  - "cross-reference team bios"
  - "analyze draft against team"
  - "technical evaluator review"
  - "product viability"
  - "architecture review"
  - "build vs buy"
  - "can this team build"
  - "pipeline action deck"
  - "pre-sales deck review"
  - "outreach strategy review"
  - "email draft audit"
  - "LinkedIn targeting review"
  - "action deck"
inputs:
  - name: response_path
    type: string
    description: "Path to the response/proposal draft"
    required: true
  - name: pws_path
    type: string
    description: "Path to the extracted PWS/PD/SOW text file"
    required: true
  - name: domain
    type: string
    description: "govcon, compliance, or general"
    default: "govcon"
---

# GovCon Response Adversarial Review

Brutal line-by-line comparison of a Sources Sought response, proposal, or capability statement against its governing PWS/PD/SOW document. The reviewer's persona is a federal Contracting Officer or technical evaluator with 500+ proposals reviewed — skeptical, detail-oriented, and unforgiving of unsupported claims.

**The goal is not to be nice. The goal is to find everything wrong before the KO does.**

## Prerequisites

### Extract Source Documents
Most government documents arrive as binary formats. Always convert first:
- **PDFs:** `pdftotext input.pdf /tmp/output.txt` (poppler-utils)
- **.docx:** Auto-extracted by `read_file`
- **.xlsx:** Auto-extracted by `read_file`
- **SAM.gov files:** May require login.gov authentication for download

### Read Response and Prior Art
- Read the latest draft AND any prior versions
- Read existing gap analyses or color team reviews (to flag unfixed prior findings)
- Read research/competitor analysis files for contextual knowledge
- Read entity factsheet for corporate details to cross-check

## Review Types

This skill covers three review personas. Load the appropriate reference for the one requested:

| Review Type | Reference | Use When |
|---|---|---|
| **General Adversarial Review** | This SKILL.md | Default — PWS line-item compliance, accuracy, credibility, structure |
| **Technical Evaluator Review** | `references/technical-evaluator-review.md` | Product architecture, build-vs-buy, team feasibility, AI claims |
| **Team Credential Cross-Reference** | `references/team-credential-cross-reference.md` | Cross-referencing team bios against draft to find unfilled gaps |
| **Pipeline Action Deck / Pre-Sales Strategy Deck** | `references/pipeline-action-deck-review.md` | Pre-sales outreach plans, email drafts, LinkedIn targeting, capability statements for prime contractor engagement. NOT a PWS-conforming proposal — different scoring dimensions (strategic coherence, tone, hidden assumptions). |
| **Project Opportunity List Verification** | `references/project-opportunity-list-verification.md` | Single-source batch verification of entity/project claims against a prime contractor's official supplier-facing project list (Bechtel, AECOM, Jacobs, etc.) |

### Technical Evaluator Review

When the user asks for a "technical evaluator review," "product viability assessment," "architecture review," or "can this team build this," load `references/technical-evaluator-review.md` and follow its methodology instead of the default scoring dimensions below. This persona evaluates six weighted dimensions: product viability, architecture soundness, build-vs-buy rationale, team feasibility math, AI claims credibility, and PWS technical coverage gaps specific to the product approach.

### General Adversarial Review (Default)

The methodology below applies to the default general adversarial review persona. When reviewing a full proposal (cooperative agreement, grant, or BAA) where the NOFO publishes explicit evaluation criteria with weights, use the NOFO-weighted scoring in `references/nofo-weighted-proposal-scoring.md` instead of the generic 5-dimension scoring below. The generic dimensions are best for Sources Sought responses and capability statements; NOFO-weighted scoring produces a more accurate competitive-range prediction for full proposals.

## Scoring Dimensions (1-10 each, average = overall)

| Dimension | Score Driver |
|---|---|
| **ACCURACY** | Provably false claims destroy this score. Verify GitHub repos, published books, phone numbers (555 = fake), revenue figures, clearance levels. One verified falsehood drags the whole response down — a KO who catches one lie distrusts everything else. |
| **PWS ALIGNMENT** | Count PWS line items. Count how many the response addresses. The ratio is the score. List the most operationally significant missed requirements by name. |
| **GENERIC vs SPECIFIC** | Does the response name specific PWS elements (systems, protocols, regulations, deliverables, role titles)? Or offer vague claims any competitor could copy-paste? |
| **CREDIBILITY** | Would the agency's evaluator believe this team can perform? Assess: certifications held, domain experience demonstrated, institutional knowledge, gap honesty. |
| **STRUCTURE** | SSN items all addressed? Contact info complete? Page limits respected? Draft markers (TODO, INSERT, PLACEHOLDER) removed? |

### Verdicts
- **Score ≥ 70:** PASS — minor fixes only
- **Score 50-69:** CONDITIONAL — significant fixes required, may need rewrite
- **Score < 50:** FAIL — major rewrite or withdrawal recommended

## Methodology

### Step 0: Load and Analyze Prior Reviews (MANDATORY when prior reviews exist)

**Before reading the current response draft,** load every prior review, gap analysis, and color team review for this opportunity. This is not optional — it prevents you from flagging already-resolved issues as findings, identifies persistent problems that survived multiple review cycles, and enables evolution tracking.

1. Search for all prior reviews for this notice ID (e.g., `*7571*`, `*hhs*review*`, `*gap-analysis*`)
2. Load each prior review and extract:
   - The overall score and date of that review
   - Every P0 and P1 finding flagged
   - Any finding explicitly marked as "FIXED" or "NOT FIXED" in an intermediate review
3. Build a tracking matrix: Prior Finding → Prior Review Source → Status in Current Draft
4. When a P0 from a prior review persists in the current draft, flag it with **increased severity** and note the review cycle count: "This was flagged in [prior review] on [date] and remains unfixed. Nth review cycle. Process failure."

This step also loads the team credential gap analysis (if one exists) to cross-reference against bios and the verified background file.

### Step 1: Fact-Check External Claims

Before adjudicating any qualitative claim, verify quantitative/specific claims against public sources:

| Claim Type | Verification Method |
|---|---|
| GitHub repo count | `curl -s "https://api.github.com/users/<user>"` → check `public_repos` |
| Published book | `web_search` "title" author → verify Amazon/ISBN listing |
| Contract numbers | USAspending.gov API, SAM.gov, fpds.gov |
| Phone numbers | Any "555" exchange in a real area code = FAKE |
| Professional titles | Check the verified background file — does this title appear in ANY source? "Fractional CAIO" with zero verified-source matches is P1. |
| Platform depth | Cross-reference against platform depth tiers in the verified background. "Hands-on" ≠ "wrote a handbook chapter about it." Separate deployment experience from reference knowledge. |
| Federal contract vehicles | Check USAspending.gov for the entity's UEI. New entities (formed < 6 months ago) = $0 federal contracts. Any revenue claim for a new entity is suspect. |
| Company revenue | State registries, SAM.gov entity report |
| Security clearances | IL6 = classified Secret. Requires specific system/date/purpose. |
| Government report quotes | Search the actual report for the quoted text verbatim. If the quoted phrase doesn't appear or the response attributes findings the report never made, it's fabricated — P0. |
| DAWIA certifications | Verify the functional area series (1102 Contracting ≠ Program Management). A "DAWIA III PM" claim when the person holds 1102 is a factual error. |
| M365 "no ATO" claims | Custom apps on GCC High change the security boundary. Every agency has an SDLC/EPLC process. Platform-level FedRAMP ≠ application-level ATO. Flag "inherits ATO" claims as P0. |
| SBIR award amounts | Cross-reference against SBIR.gov or USAspending.gov. Without a contract number, dollar figures are unverifiable. Phase I is typically ≤$150K (DoD) — amounts above this need evidence. |
| Credential suppression | Verified background files may contain explicit "Do NOT use" instructions for certain certifications. Security+ listed when CISA is held violates user directive AND undersells the team. |

**Threshold:** Any claim off by >2x is a P0 factual error. A single P0 accuracy finding makes the entire response non-credible.

**Common fact-check targets reference:** `references/common-fact-check-targets.md` — catalog of recurring false/overstated GovCon claims with verification methods, severity, and domain-specific guidance. Load this when you encounter claims about DEA databases, government report quotations, ATO inheritance, DAWIA certifications, SBIR awards, credential suppression, free government API claims (OFAC/HHS OIG/BIS are downloadable files, not APIs), FDA enforcement database accessibility (openFDA has no Warning Letter or 483 endpoint), commercial integration guides cited as architecture validation, or Power Automate connector limits for multi-source screening.

### Step 2: PWS Line-Item Coverage Audit

1. Count every specific requirement in the PWS (table rows + "shall" statements)
2. For each: mark ADDRESSED, PARTIALLY, or NOT MENTIONED
3. Coverage % = ADDRESSED + (PARTIALLY × 0.5) / TOTAL
4. Multiply by 10 for the PWS Alignment score

### Step 3: Disproportionate Emphasis Check

**The single most common failure:** A response builds its entire value proposition (80% of content) around something the PWS mentions once in passing, while ignoring the PWS's actual structure. Always ask: does the response's content proportion match the PWS's emphasis?

**Red flag pattern:** Response has 6 pages about AI automation. PWS has 1 sentence about AI, buried in "Additional Requirements." The response's emphasis is inverted.

### Step 4: Credibility Assessment

Write from the evaluator's perspective:
- "What 3 things would the evaluator believe?"
- "What 3 things would make the evaluator dismiss this immediately?"
- "What is the single most incredible claim in this response?"

### Step 5a: Team Credential Cross-Reference (When Team Bios Exist)

When team member bios/resumes are available (from session context, PDFs, people dossiers, or prior research), run a systematic gap-to-strength cross-reference against the draft. This answers: "Are team credentials properly leveraged, or are we advertising gaps we already filled?"

**Procedure (detailed in `references/team-credential-cross-reference.md`):**

1. **Consolidate all team bios** — extract credentials from every source (PDFs, dossiers, session memory, call transcripts). Build a master credential table per person: education, certifications, service, key roles/scale, domain skills.

2. **Section-by-section mapping** — for each section of the draft, ask:
   - Does a team member's credential fill a gap the draft acknowledges?
   - Does a team member's credential replace a weak/vague claim?
   - Is any credential misattributed to the wrong person?
   - Is any team member entirely invisible in the draft?

3. **Flag critical errors** — common patterns:
   - **Aspirational credentials that are already held** (e.g., "will obtain PMP" when the person already has PMP + DAWIA III)
   - **Gap notes for gaps that are filled** (e.g., "no DAWIA-certified acquisition professional" when a team member holds DAWIA III Contracting)
   - **Wrong attribution** (e.g., FOCI mitigation credited to the technical lead when the compliance director is the actual SME)
   - **Missing team members** (e.g., 4-person team but only 2 appear in Key Personnel section)

4. **Produce a gap-to-strength matrix** — a section-by-section table showing: Current Draft → Gap/Weakness → Team Credential Replacement → Priority.

5. **Identify new sections** enabled by team credentials that the current draft doesn't include (e.g., a subcontract management section when the team has a federal subcontracts manager).

**Output:** The matrix becomes the edit plan. Every row is a concrete edit instruction — not an abstract suggestion.

### Step 5b: Gap Classification

| Tier | Definition | Action |
|---|---|---|
| **P0** | Fatal — cannot submit. False claims, missing contact info, missing mandatory sections, unfixed prior-review findings. | Fix before submission |
| **P1** | Severe — damages competitive position. Unsubstantiated ratios, missing PWS task areas, certification gaps, overstatements. | Strongly recommend fix |
| **P2** | Moderate — weakens but doesn't destroy. Vague language, repeated differentiators, missing secondary requirements. | Should fix to improve |

## Deliverable Structure

**Every finding MUST include a line reference.** Format: `Line(s) XX` for the response document, `PWS lines YY-ZZ` for PWS cross-references, or `§SectionName` for verified background/file references. A finding without a line reference is incomplete — the author cannot fix what they cannot locate.

```markdown
# ADVERSARIAL REVIEW — [Agency] [Program] Response ([Notice ID])

## OVERALL SCORE: XX/100 — [VERDICT]

| Criterion | Score | Notes |
| [...] scoring table ...]

## 1. ACCURACY: FACTUAL ERRORS AND OVERSTATEMENTS
[Every false claim with source evidence. Each finding: ❌/⚠️ → Location (line refs) → Reality → Severity → Fix.]

## 2. PWS ALIGNMENT
[Coverage audit table. Count of requirements addressed vs total. For roles: per-role depth assessment (STRONG/ADEQUATE/THIN/TOKEN). For deliverables: per-item match. Proportionate emphasis check — does response content % match PWS requirement %?]

## 3. GENERIC vs SPECIFIC
[What's tailored. What's boilerplate. Agency-specific knowledge shown vs missed. Separate into two sub-sections: "What Is Specific" and "What Is Generic" with line references.]

## 4. CREDIBILITY
[What evaluator would believe vs dismiss. Single most incredible claim. For new entities: explicit FAR 9.104-1 responsibility assessment.]

## 5. STRUCTURE AND FORMAT
[SSN items compliance, contact completeness, page limits, draft markers. Font size/format compliance. Cover page checklist against notice requirements.]

## 6. COMPARISON TO PRIOR REVIEWS — EVOLUTION TRACKING (include when prior reviews exist)
[Table: Prior Finding | Source Review | Status in Current Draft | Delta. Shows what was fixed, what persists, and what regressed. This section proves the review was informed by prior work and prevents re-flagging resolved issues.]

## 7. PRIORITIZED FIXES
[P0, P1, P2 tables with explicit fix instructions including line references and proposed replacement text.]

## 8. WHAT ACTUALLY WORKS
[Genuine strengths — preserve these during rewrite]

## 9. BOTTOM LINE
[One-paragraph verdict with concrete recommendation. Include the KO's likely market research determination if this is a Sources Sought.]
```

## Pitfalls

- **Don't be diplomatic.** This is an adversarial review. The reviewer's job is to find everything that's wrong before the KO does. Sugar-coating defeats the purpose.
- **Don't skip fact-checking.** "103 GitHub repos" took 10 seconds to verify as 30. That single check earned the review.
- **Read the PWS first, then the response.** If you read the response first, you absorb its framing. Read the PWS cold, understand what it asks for, then see if the response maps to it.
- **Watch for the inverted emphasis pattern.** Response spends 80% of ink on what the PWS treats as a footnote. This is the #1 structural failure in GovCon responses.
- **Prior reviews are your friend.** Always check if prior gap analyses flagged things that weren't fixed. Nothing damages credibility more than a P0 that survived multiple review cycles.
- **"555" phone numbers are ALWAYS fake.** This is settled telephony convention — 555 exchanges are reserved for fictional use. Any "555" in a real area code is a fabricated number that a federal CO will catch immediately.
- **Efficiency ratios without methodology are fabricated.** "4-person = 15-20 person output" with no benchmark, no methodology, no comparative data is marketing puffery. Flag it as P1 every time.
- **PWS coverage % is objective.** Don't guess. Count the line items. Do the math. A 6% coverage rate is a 6% coverage rate — report it honestly.
- **Flag P0 findings that survived prior review cycles with increased severity.** If a gap analysis flagged "fake phone number" 2 days ago and the draft still has it, that's not just a P0 — it's a process failure. Note in the review: "This was flagged in [prior review] on [date] and remains unfixed. Third review cycle." This signals that something is wrong with the fix-it workflow, not just the draft.
- **The "no one read the PWS" failure.** If the PWS PDF was never downloaded (confirmed by research file stating "attachments could not be downloaded"), and the response was built against an estimated PWS scope, flag this as a P0 compliance failure. The response may have zero format compliance with the KO's requirements. You cannot review alignment against a document that was never read.
- **Entity-name contamination in external responses.** If the response is being submitted through one entity (e.g., Leatherneck) but the draft contains references to another entity (e.g., HARBOR Initiative LLC, UEI K4CVRY71WQZ8) that should not appear in external-facing documents, flag every occurrence as a P0. Run regex sweeps for the entity name, UEI, and any product names associated with the restricted entity.
- **Aspirational credentials that are already held.** If the draft says "commits to obtaining PMP by start date" but the proposed PM already holds PMP + DAWIA III, flag it as P0. The team looks unqualified when they're overqualified.
- **Gap notes for gaps the team fills.** If the draft acknowledges "no DAWIA-certified acquisition professional" but a team member holds DAWIA III Contracting, the gap note must be deleted and the team member added. Advertising a weakness that doesn't exist is self-inflicted damage.
- **Wrong person credited for core capability.** If the draft credits the technical lead with FOCI mitigation but the compliance director is the actual FOCI SME, fix the attribution. The evaluator can't verify who holds which credential, but they can tell when the claim is in the wrong section.
- **Team members invisible in the draft.** If 4 people are on the team but only 2 appear in Key Personnel, the evaluator can only score the 2 they can see. Missing team members are lost scoring opportunities.
- **Every finding must carry a line reference.** A finding without a line reference (e.g., `Line XX`, `PWS lines YY-ZZ`, `§Section`) is incomplete. The response author cannot fix what they cannot locate. This applies to every claim in Sections 1-5 of the deliverable.
- **Ambiguous employment relationships are protest bait.** If the response claims "no subcontracting" or "all work by prime personnel" but lists individuals who publicly operate separate LLCs (e.g., a "Product Lead" who is the founder of a separate SAM-registered entity), flag it as P0. The KO cannot determine the truth, and a competitor who checks SAM.gov can file a size protest. Demand an explicit W-2 employment statement or proper teaming disclosure.
- **Fabricated government quotations are the fastest credibility killer.** When a response puts quotation marks around text attributed to GAO, CBO, NIST, or an IG report, search the actual document for that exact string. If it doesn't appear, it's fabricated — P0. Even a real report number with a fake quote is toxic. A CO can verify this in 30 seconds. See `references/common-fact-check-targets.md` for recurring patterns.
- **DAWIA certifications are functional-area-specific.** "DAWIA III" without the functional area is meaningless. DAWIA III (1102 Contracting) ≠ DAWIA III (Program Management). Cross-reference the claimed functional area against team bios. A mismatch is P1 — it makes the team look like they're inflating credentials or don't understand the DAWIA system.
- **"No new ATO required" is never true for custom applications.** Platform-level FedRAMP authorization does not eliminate application-level ATO requirements under agency SDLC/EPLC processes. Flag this claim as P0 every time. The fix: acknowledge the EPLC process and describe how you'll support it.
- **Sources Sought ≠ proposal.** If a Sources Sought response spends >50% of content on technical solution/architecture/implementation (unsolicited mini-proposal) and <50% on the SSN-requested items (company profile, capability, contract vehicles, pricing, NAICS), flag the disproportionate emphasis as P1. The CO is doing market research, not evaluating proposals. Over-investing in a technical proposal for a requirement that hasn't been solicited signals you don't understand the acquisition vehicle.
- **Gap analyses are tied to specific notice IDs.** A team credential gap analysis built for notice 7571TE26Q00092 (HHS OCIO VMO) contains PWS-specific findings that do NOT transfer to notice ACQ-OMAS-2026-SAT-0015 (HHS ASPR). When loading a prior gap analysis, check its notice ID first. Credential facts (certifications, employment) are transferable; PWS line-item gaps and deliverable assignments are not. Applying wrong-notice PWS findings produces phantom gaps and misses real ones.
- **Proposal-generated bios are the lowest-trust source for personnel credentials.** A prior proposal's resume package (like the DFOP structural fixes) may have systematically inflated every team member's credentials to win funding. A Company Charter v2 — the entity's own formal document — contradicted 12 claims across 3 people including a fabricated MBA and a fabricated COO title. Treat entity charters, internal dossiers compiled from actual interviews, and working files showing current job titles as HIGHER authority than any proposal artifact. When cross-referencing personnel claims, build a source hierarchy: entity charter > internal dossier > working files > call transcripts > marketing website > proposal artifacts. Proposal-generated bios sit at the bottom. Do NOT use a prior proposal's resumes as the basis for a new proposal without re-verifying every claim against the entity charter.
- **An adversarial review is only as good as its source set.** A review that checked 11 files missed 11 personnel inflation errors because the entity's own formal Company Charter v2 was not in the source set. Always do a complete file inventory across all relevant directories before beginning any adversarial review; always include entity charters, founding documents, and internal dossiers. When the entity is new (< 6 months old), go out of your way to locate every internal document that describes team members. A two-pass review (first with surface files, second after discovering the charter) found 36 total findings — 11 of which only surfaced in the second pass. The methodology is: (1) inventory all available files, (2) identify what's missing, (3) if key entity documents are absent, defer final scoring until they're located. See `references/personnel-inflation-lessons.md` for the worked SCALE/DFOP example. A verified background file (e.g., `amyn-background-verified.md`) may include explicit instructions like "Do NOT use Security+ in capability statements — it undersells." Before listing any credential from the verified background, scan for "Do NOT" directives. Violating these is a P1 — the user explicitly told you not to, and you did it anyway.