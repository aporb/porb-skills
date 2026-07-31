# Pipeline Action Deck / Pre-Sales Strategy Deck Review

**Use when:** The deliverable under review is an internal or external pre-sales strategy deck — outreach mapping, email drafts, project prioritization, LinkedIn targeting, or capability statements aimed at generating new business rather than responding to a solicitation.

This is distinct from a PWS-conformance proposal review. The dimensions are different because the KO is not evaluating compliance — a hiring manager, business development lead, or prime contractor procurement contact is evaluating whether the sender is worth engaging.

## When to Use This Reference

This methodology replaces the standard 5-dimension scoring (Accuracy, PWS Alignment, Generic v Specific, Credibility, Structure) when the artifact is:
- A Pipeline Action Deck (targeting specific prime contractors or government programs)
- A pre-sales outreach plan (email sequences, LinkedIn strategies, event plans)
- A business development capability statement (not for a specific solicitation)
- A partnership deck (small business → prime contractor engagement strategy)
- A "go packet" (research + outreach templates for specific opportunities)

## Scoring Dimensions (1-10 each, average = overall)

| Dimension | Score Driver |
|---|---|
| **ACCURACY** | Same as standard review. False entity data (emails, phone numbers, UEI, CAGE, NAICS) destroys credibility on contact. One placeholder phone number in an email signature is a P0. |
| **STRATEGIC COHERENCE** | Are the outreach targets correctly prioritized? Does each pitch reflect the specific project's phase, scope, and procurement stage? Or are all emails copy-paste? Are project-specific entry points correctly identified (e.g., SBA contacts vs technical PMs vs program directors)? |
| **TONE** | Are email drafts appropriately formal without stiffness? Do they avoid both the overly casual ("Hey!") and the overly bureaucratic ("Pursuant to...")? Is the pitch framed as learning-oriented rather than presumptuous? Does the signature block look complete and professional? |
| **COMPLETENESS** | Are all planned outreach channels covered (email, LinkedIn, supplier portal registration)? Are all targets prepped with specific contact names and contact data? Are there gaps in the targeting pipeline (projects identified but not drafted)? Are placeholders resolved? |
| **HIDDEN ASSUMPTIONS** | What does the deck assume about the recipient's behavior, role accessibility, business need, or procurement process? Are these assumptions testable or speculative? |

## Methodology

### Step 1: Platform-Independent Fact-Check

Strategy decks make claims about external entities — their project involvement, personnel, timelines, and procurement processes. Verify these independently before evaluating the strategic quality.

**Batch verification via official supplier portals (RECOMMENDED):**
Large EPC/construction prime contractors (Bechtel, AECOM, Jacobs, KBR, Fluor) publish **Project Opportunity Lists** on their supplier-facing websites. These list every current and pending project with:
- Job number, scope description, location
- Date opened / closing date
- Procurement and subcontract contacts (name, email, phone)
- Registration portal URLs

**Workflow:**
1. Navigate to `<contractor>.com/supplier` or `<contractor>.com/supplier/project-opportunities`
2. Scrape the full page (it's typically one long HTML table, 10-20K chars)
3. Search the page for each project name claimed in the deck
4. Cross-reference: is the project listed? Does the contact email match? Is the scope description consistent with the deck's pitch angle?
5. For unlisted projects, flag the claim — it may be speculative, expired, or incorrect

**This single-source approach verified 15+ claims in one pass** for the Bechtel Pipeline Action Deck review (July 2026), covering all outreach targets across 6 projects.

**Single-claim verification (when no portal exists):**
Fall back to standard verification methods for each claim type (see SKILL.md Step 1 table):
- Email addresses: can't verify without access, but check format plausibility
- Phone numbers: any "xxx-xxxx" or "555" pattern = placeholder/fake
- NAICS size standards: check against current SBA table
- Personnel roles: search news + LinkedIn (can verify titles and team transitions)
- Project values and contract status: search news sources with the specific program name

### Step 2: Strategic Coherence Assessment

**Project-specific tailoring check:**
For each outreach target, evaluate:
1. Does the pitch reflect the project's **current phase** (pre-construction, under construction, commissioning, operations)?
2. Does the pitch address the project's **specific scope** (greenfield city, waste vitrification, LNG export terminal)?
3. Does the pitch identify a **plausible entry point** based on the project's procurement structure (SBA outreach contacts for federal primes, procurement managers for commercial, SVP transformation for org-level)?
4. Does the pitch **differentiate** from a generic "we do AI for EPC" by naming project-specific challenges?

**Targeting hierarchy check:**
Evaluate whether the targets are correctly prioritized:
- Newly created roles (e.g., "SVP EPC Transformation — Feb 2026") are higher value because the executive is building their function from scratch and likely open to new vendor relationships
- Generic procurement inboxes are lower value — they triage at admin level
- SBA/Outreach inboxes are medium value — they exist specifically to find new suppliers

**Pricing anchoring check:**
Strategy decks often include engagement pricing ranges. Verify:
- Are ranges anchored to a benchmark (e.g., "40-60% of Big 4 equivalent") or freestanding?
- Do ranges match the complexity of the named projects ($50K for a quick assessment of a $100B program is a red flag)

### Step 3: Tone Assessment (Cold Email Drafts)

Pre-sales email drafts require a different tone calibration than proposal cover letters.

**Green flags:**
- Formal but not stiff: "Dear Elizabeth" not "Dear Ms. Lovko" or "Hey!"
- Frames outreach as learning-oriented: "We'd like to understand your SBA goals" instead of "We can help you with your SBA goals"
- States boundaries explicitly: "We are not bidding for fabrication or equipment"
- Lists specific personnel credentials relevant to the target project: DOE experience → DOE prime projects
- Closes with low-friction ask: "Would a brief conversation be worth your time?"

**Red flags:**
- Placeholder contact information: `(803) xxx-xxxx`, `contact@company.com`, `Company Name`
- Aggressive follow-up commitment: "I'll follow up with a call to your office at 555-123-4567 early next week" — reads as presumptuous, implies the recipient has no choice
- Buzzword density: more than 2 of "synergy", "AI-powered", "revolutionary", "game-changing", "disrupt" in a single email
- Overpromising efficiency ratios: "Our 4-person team delivers what normally requires 15-20 people" — unsubstantiated and indistinguishable from vaporware

### Step 4: Completeness Audit

For each outreach target in the deck, check whether each element of the outreach is drafted:
- Email draft (with complete signature block)
- LinkedIn connection request message (not just a note to "connect")
- Alternative subject lines (A/B testing option)
- Follow-up sequence (what happens if no response in 1-2 weeks)
- Supplier portal registration steps (if applicable)

**Gap patterns:**
- Phone placeholder → P0 (most common, most damaging)
- LinkedIn profile not researched → P2 ("Search: John Platt Bechtel" without direct URL)
- Project identified but no draft prepared → P2 (acceptable if conditionally deferred, e.g., "wait until EPC signed")

### Step 5: Hidden Assumptions Audit

Every pre-sales deck makes implicit assumptions about the recipient. Document them explicitly with risk levels:

| # | Assumption | Risk | Fix |
|---|---|---|---|
| 1 | Recipient reads cold emails from unknown small businesses | HIGH | Assume inbox triaged by admin; plan secondary channel |
| 2 | Named contact is still in role (portal info may be stale) | MEDIUM | Verify role before sending; have fallback contact |
| 3 | Executive is reachable on LinkedIn and accepts cold connections | MEDIUM-HIGH | Plan alternative warm introduction path |
| 4 | Generic procurement inbox routes English-language outreach to a decision-maker | MEDIUM | Research whether inbox has local team vs central processing |
| 5 | Contractor's scope includes the service being pitched | MEDIUM-HIGH | Add discovery question, not assertion |

## Deliverable Structure

```markdown
# ADVERSARIAL REVIEW — [Company] [Deck Name]

## OVERALL SCORE: XX/100 — [CONDITIONAL PASS / FAIL]

| Criterion | Score | Notes |
|[... scoring table ...]|

## 1. ACCURACY: FACTUAL ERRORS AND OVERSTATEMENTS
[Verified against Project Opportunity List / press releases / news. Every finding with location reference.]

## 2. STRATEGIC COHERENCE
[What works: project-specific tailoring, targeting hierarchy, differentiation. What's weak: generic pitch angles, wrong entry points, missing differentiation.]

## 3. TONE ASSESSMENT
[Email draft analysis: green flags, red flags, signature completeness. Specific line references for each finding.]

## 4. COMPLETENESS AUDIT
[Table of all targets with: Draft Status, Contact Complete, LinkedIn Prepped, Placeholders.]

## 5. HIDDEN ASSUMPTIONS
[Table: Assumption → Risk Level → Location → Fix]

## 6. PRIORITIZED FIXES
### P0 — Must Fix Before Use
### P1 — Strongly Recommend Fix
### P2 — Should Fix to Improve

## 7. WHAT ACTUALLY WORKS
[Genuine strengths — preserve these]

## 8. BOTTOM LINE
[One-paragraph verdict with concrete recommendation]
```

## Pitfalls

- **Don't assume a project isn't a Bechtel project just because you didn't see it in press coverage.** The Project Opportunity List may list projects that haven't been announced publicly. Always check the official portal before making negative claims.
- **"Bid protests filed" on a 3-year-old contract is not "Recent."** Always check the date on any legal or regulatory action. A contract dispute from 2022 is not relevant to 2026 outreach strategy unless there's evidence of ongoing impact.
- **Efficiency ratios in sales decks are never backed by evidence.** They are marketing claims. The evaluator's job is to flag them, not to verify them. Mark them P1 and move on.
- **A placeholder phone number in an email signature is a P0.** Not because it's hard to fix, but because it signals the deck wasn't reviewed before distribution. The first impression is "incomplete, sloppy."
- **Generic procurement inboxes (like cm2023@bechtel.com) are black holes.** The deck should have a secondary outreach plan for projects where the only contact is a functional mailbox.
- **Don't flag lack of PWS alignment for a non-proposal deck.** A pipeline action deck does not need to conform to a solicitation. The relevant dimension is strategic coherence, not solicitation compliance.
