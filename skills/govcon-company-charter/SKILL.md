---
name: govcon-company-charter
description: Build a professional company charter or capability statement for a GovCon entity. Also covers partner charter analysis — adversarial comparison against your own charter, call transcript integration, strategic gaming questions, and cross-reference against prior proposals. NDA-partner voice with no hedging or audit-report qualifiers.
---

# GovCon Company Charter / Capability Statement

## When to Use

A federal prime contractor, teaming partner, or client asks for a "company charter," "corporate capability statement," or "corporate profile" PDF. This is a formal document that proves the entity is real with legitimate capabilities — used in proposal packages, teaming agreements, and partner evaluations.

## The Workflow

### Phase 1: Research the Founder's Footprint

Before writing a single word, exhaustively research the founder and entity across all sources:
- Resume / CV — most recent version in the repos/books
- LinkedIn — current title, past roles, posts, recommendations
- Personal website(s) — about page, portfolio, blog
- Company website — framework, about, pricing, products
- GitHub — public repo count (verify via API, don't trust memory), pinned repos, READMEs
- Published books — Amazon links, descriptions, chapter counts
- Internal knowledge base — 2026_books, Henry wiki, Obsidian vault
- Product catalog — any dev-box or portfolio page listing products/tools
- IPN/community posts — contract claims, past performance data points
- Federal databases — USASpending.gov, FPDS, SAM.gov, GAO protests, GDICWins, OrangeSlices

### Phase 2: Interview for Scope and Positioning

Use `clarify` to ask the founder these questions before building:

1. Scope positioning — full-spectrum, targeted to a specific award, productization-forward, or dual-persona?
2. LFC/partner pairing — explicit pairing section, implied, or HARBOR-only?
3. Federal vs. private balance — 60/40, 90/10, or 50/50?
4. Past performance — what contracts to feature? What's the total involvement figure?

### Phase 3: Build the HTML Charter

Use the ivory/clay/slate design system. Load `references/design-tokens.md` for CSS variables.

**Required sections for a complete charter:**
1. What [Entity] Is — entity type, methodology, operating model, markets served
2. Scope Areas — dual-persona grid (Technical Execution + Strategic/Productization) for solo practitioners
3. Products and Free Resources — named products with one-line problem statements, NOT repo counts
4. Credentials and Proof Points — 8-item grid with numbered proof points
5. Past Performance — structured table with Year, Contract/Award, Agency, Role, Value, Key Contribution
6. Federal Domain Depth — platforms grid, compliance frameworks, agencies served
7. Certifications and Socio-Economic Designation — active credentials table, entity classifications
8. Engagement Models — how the entity engages, with pricing
9. Limitations and Scope Boundaries — what the entity does NOT do, bus-factor acknowledgment for solos
10. Commercial Sector Relevance — if 60/40 or 50/50 split
11. Federal Identity and Legal — canonical values table (UEI, EIN, NAICS, etc.)
12. Contact — emails, phone, websites, LinkedIn, GitHub, location

### Phase 4: Adversarial Review

Before delivering, run an adversarial review sub-agent. Give it the full HTML file and a known-facts checklist. It should check:
- Every dollar amount, date, certification, and contract claim
- Publicly verifiable claims (repo counts, book availability, clearance status)
- Omissions (missing sections a prime would expect)
- Tone (too modest? too boastful? hedging language?)
- Weak language (passive voice, qualifiers, "architecture-level understanding")

### Phase 5: Incorporate Corrections

Process all P0/P1 findings from the review. Common fixes:
- SBIR designation precision (e.g., "DoD/DoW CDAO" not "DAF")
- SDVOSB — never claim without a VA disability rating. VOSB-eligible is the fallback.
- Repo counts — verify via GitHub API, don't trust memory numbers
- Past performance — add contract numbers where publicly verifiable
- Remove hedging language — "Source: Amyn's accounting" becomes a direct statement for NDA docs

### Phase 6: Generate Print PDF

Create a separate print-optimized HTML with:
- `@page { size: letter; }` CSS rules
- Cover page with identity strip and confidentiality notice
- Auto page numbers via `@bottom-center` with `counter(page)`
- Page breaks before major sections
- Tighter spacing for final sections (class="tight")
- Pure white background (no ivory for print)
- Generate PDF via `chromium --headless --print-to-pdf=OUTPUT.pdf --no-pdf-header-footer URL`

## Voice Rules for NDA Partner Documents

This is NOT an audit report. It's shared with partners under NDA. Voice must be:
- Declarative, not hedging — "Architected the winning technical solution" not "was involved in technical architecture"
- No verification notes — don't say "Source: Amyn's accounting; not independently verified in public databases"
- No "pending" or "under protest" for won awards — if an award was protested and survived, it's "won — protest survived/denied"
- Products, not repos — "FARchat — AI regulatory intelligence across 13 federal regulation libraries" not "30+ GitHub repositories"
- All claims hyperlinked — Amazon, GitHub, cloud URLs, LinkedIn
- No staff-aug language in limitations — solo practitioners: "currently operates as a solo practitioner, scaling through AI infrastructure rather than headcount"

## Common Pitfalls

- SBIR designations — get the exact agency/sponsor right. "DoD/DoW CDAO SBIR" is not "DAF SBIR." CDAO was the sponsor; Air Force DTO was the contracting vehicle.
- SDVOSB — never claim SDVOSB-eligible without a confirmed VA disability rating. VOSB self-certification requires only veteran status plus honorable discharge.
- "Two decades" claim — verify actual career start year. If first professional work was 2006, "two decades" is accurate in 2026.
- Repos vs. products — GitHub public repo counts are one-click verifiable. Never use a stale number. Better: list named products with problem statements.
- Past performance dates — cross-reference against USASpending.gov. A contract claimed as "2020" that was actually awarded "Dec 2024" will be caught.
- Residential address — for NDA partner docs, full street address is fine. For public-facing docs, consider redacting to city/state only.
- Year column width — past performance tables need only ~80px for the Year column. Don't waste space on it.

## Companion Workflow: Partner Charter Analysis

When a partner/teaming counterparty sends you THEIR company charter for review and feedback, do not just skim it. Run a full adversarial analysis. This workflow was developed analyzing Leatherneck Federal Consulting's Charter v2.0 against HARBOR's Charter v2.0.

### Step 1: Load All Source Documents

Pull every relevant document in parallel before starting analysis:
- **The partner's charter** — the document they sent you
- **Your own charter** — the one they used as a template (if applicable)
- **Call transcripts** — any recent calls where the charter was discussed, especially if feedback was given that may not be reflected yet
- **Prior partnership proposals/plans** — what you've already sent them (partnership proposals, strategic assessments, revenue models)
- **WhatsApp/chat transcripts** — informal comms often contain the real dynamics absent from formal docs

### Step 2: Map the Structure

Compare section-by-section against your own charter (if they used it as a template). Identify:
- Which sections are direct mirrors vs. remapped
- Which sections are custom additions (their "moat")
- Which sections from your charter are absent from theirs

### Step 3: Audit Positioning

Check how your entity is represented in THEIR document:
- Are your UEI/EIN/NAICS/founder name correct?
- Are your credentials represented (clearances, certs, key wins)?
- Are you positioned as equal partner, optional add-on, or subordinate?
- What's missing that a prime evaluating the joint team would want to know?

### Step 4: Cross-Reference Against the Plan You Sent

The partner's charter and your prior proposals/plans often tell DIFFERENT stories about the business. Surface the gap:
- Your plan says X; their charter says Y
- Identify the "fundamental tension" between the two narratives
- Note what their charter gets right that your plan misses (be honest)

### Step 5: Integrate Call Transcripts — Watch for Attribution &amp; STT Errors

Call transcripts often reveal feedback given that hasn't been incorporated yet. Specifically:
- Was the charter sent BEFORE or AFTER substantive feedback was given?
- What did you ask for on the call that's still missing?
- What did the partner say they'd "go back and revise"?

**CRITICAL — Speaker attribution verification.** Before quoting anyone from a transcript:
1. Read the transcript's metadata/stats section to identify which Speaker number maps to which person. The talk-time percentage is a strong signal (often the person who speaks most is your founder/principal).
2. Do NOT assume Speaker 0 is the partner and Speaker 1 is you based on who spoke first. Verify against known timing and content.
3. Cross-reference proper nouns in the transcript against known entity names. STT frequently mangles names: "Leatherneck" → "Levenick," "Leatherneck" → "Levenich," etc. When a STT-transcribed name doesn't match any known entity, check if it's a phonetic misspelling of something real before treating it as a separate entity.

**Pitfall — Employment assumptions.** Do NOT assume people are leaving their day jobs or that employment status at another company is a risk factor. Many GovCon partnerships are side ventures where everyone keeps their primary employer. This is the norm, not a risk factor. The charter should reflect partnership capabilities, not members' employers.

### Step 6: Surface Strategic Gaming Questions

Load `references/partnership-gaming-questions.md` and apply the framework. Produce 5-7 concrete strategic questions with gaming options (Option A vs. Option B) and recommendations. This is the most valuable part of the analysis — it's what the founder needs to game-theory before the next partner meeting.

### Step 7: Build the HTML Briefing

Produce a self-contained HTML briefing using the ivory/clay/slate design system with:
- Executive verdict with grade strip (A/B/C for multiple dimensions)
- Section-by-section assessment with color-coded cards (green=strong, amber=needs work, red=gap)
- Gaps & risks table (P0/P1/P2 priority tags)
- Strategic gaming questions with option pairs
- Cross-reference table comparing their charter vs. your plan
- Specific questions for the founder to answer before the next partner meeting
- A response framework (what to send back to the partner)

Deliver to `https://brief.h.porb.dev/<slug>.html`. For the TOC, use the left-sidebar sticky nav pattern with numbered sections.

### Step 8: Report in Discord

Send a concise summary with the link, the grade, the P0 problems, and 2-3 most important strategic insights. Do not dump the full analysis into Discord — the briefing IS the deliverable.

## Support Files

- `references/design-tokens.md` — ivory/clay/slate CSS variables and print CSS template
- `references/past-performance-verification.md` — how to verify contract claims against federal databases
- `references/partnership-gaming-questions.md` — reusable strategic question framework for evaluating any GovCon partnership
- `templates/charter-print.html` — starter print-optimized HTML with @page rules