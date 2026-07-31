---
name: govcon-partnership-assessment
description: "Research two GovCon entities side-by-side, map combined capabilities against NAICS/PSC codes, identify and rank partnership opportunities, and produce a structured forward-looking assessment brief. Used when evaluating teaming, JV, subcontracting, or merger opportunities between two federal contractors."
category: govcon
triggers:
  - "what can we do together"
  - "partnership opportunity"
  - "leatherneck and harbor"
  - "two companies working together"
  - "joint venture assessment"
  - "teaming opportunity"
  - "combined capabilities"
  - "what sort of work can we do"
  - "starting point for discussion"
  - "map our capabilities together"
---

# GovCon Partnership Assessment

Evaluate what two federal contracting entities can do together — map combined capabilities, identify ranked opportunities, and produce a forward-looking action plan. Distinct from single-entity dossiers or C-suite product evaluations.

## When to Use

- User wants to explore partnership / teaming / JV / subcontracting between two GovCon entities
- User asks "what can [Entity A] and [Entity B] do together"
- User has a new partnership discussion and needs a structured starting point
- Both entities have registrations or capabilities to map
- **Large commercial prime pipeline assessment** — user provides a prime's project portfolio (Bechtel, KBR, Fluor, AECOM, etc.) and wants go/no-go decisions on which projects the combined team can pursue. This is NOT a partner-entity assessment; the "partnership" is between the user's delivery team and the prime's project pipeline. Output format shifts from entity-cards to a master pipeline table + per-project deep-dive cards + weekly action items organized by "service lines" (e.g., federal compliance sub + technology advisory).

**Confirm the deliverable BEFORE building.** A partnership assessment (forward-looking: what can they do together) is NOT a person dossier (backward-looking: who is this person). When the user says "do full research and update everything" about a person they have history with, ask: "Dossier on the person, or partnership/opportunity assessment for the two entities?" Building the wrong one costs a full rebuild. In July 2026 the user asked to "research Douglas and update everything" — the correct deliverable was a Leatherneck+HARBOR partnership assessment, but a Douglas dossier was built first and had to be scrapped. One clarifying question would have prevented it.

## When NOT to Use

- Researching a single entity → use `contractor-portfolio-analysis`
- Evaluating a product/feature idea → use `opportunity-assessment`
- Person-company employment fit → use `opportunity-assessment` (person-company variant)
- External consulting deliverable for a client → use `consulting-assessment-report`
- Full C-suite strategic evaluation → use `opportunity-assessment` (multi-phase variant)

## Core Workflow

### Phase 1: Parallel Research (Local + Authoritative)

Before building anything, research both entities simultaneously:

1. **Search session history** — what does the user already know about these entities?
2. **Search local repos** — any briefings, dossiers, or project files referencing them?
3. **Check canonical entity records** — if an entity has a documented presence on the local machine (e.g., HARBOR Initiative LLC at `2026_books/operations/harbor-initiative-llc/00-canonical-facts.html`, Aecon at `repos/aecon-fcs/`), read those FIRST. Canonical facts trump memory. The HARBOR column of the July 2026 partnership briefing was initially wrong (said "UEI: not registered") because the canonical facts file wasn't consulted before building the side-by-side. See `references/canonical-entity-records.md` for known record locations.
4. **Pull SAM.gov data** — UEI, CAGE, NAICS, PSC codes, socio-economic status, leadership
5. **Check SBA certifications** — are claimed set-asides actually certified or self-attested?
6. **Check USAspending.gov** — any contract history? Revenue? Agency concentration?
7. **Search Nextcloud briefings** — any prior intel or call transcripts?

**Critical:** Use SAM.gov PDF exports as authoritative. Do not rely on inferred or cached data. The Leatherneck briefing (July 2026) initially reported "no SAM registration" based on stale API data, then was corrected to "active registration" using the actual SAM.gov entity PDF.

**Extract the FULL SAM.gov entity PDF + SBA DSBS PDF, not just the headline fields.** The coreData PDF (sam.gov/entity/<UEI>/coreData) and the SBA certifications profile PDF (search.certifications.sba.gov/profile/<UEI>/<CAGE>) carry fields easy to miss that change the assessment:
- **Entity structure** — may contradict the legal name (Leatherneck's SAM record says "Partnership or Limited Liability Partnership" despite "...LLC" in the name — a registration error or genuine structure question that materially affects adding members; surface as an open question)
- **POC structure** — who holds Electronic Business vs Government Business POC roles, and who was the last SAM editor (reveals operational control)
- **Registration flags** — accepts credit card payments, debt subject to offset, EFT indicator, disaster response registry membership (relevant for FEMA/emergency work)
- **SBA small-business designation per NAICS** — all codes may qualify as "Small" with size-standard exceptions (e.g., 541519 IT Value Added Reseller exception) — affects set-aside eligibility per code

**PDF extraction when firecrawl is out of credits:** `pdftotext -layout <file> -` (poppler-utils) handles SAM.gov and SBA PDFs cleanly, preserving the two-column table layout. Do not read raw PDF bytes with read_file — it's binary garbage.

### Phase 2: Entity Rundown

Build side-by-side comparison covering:

| For Each Entity | Data Points |
|-----------------|-------------|
| Identity | Legal name, UEI, CAGE, formation date, state |
| Registration | SAM status, expiration, purpose |
| Socio-economic | SBA certifications (certified vs self-attested) |
| Contract history | Lifetime awards, active vehicles, agency concentration |
| Leadership | Named principals with roles |
| Capabilities | NAICS codes, PSC codes, claimed services |
| Gaps | What's missing — past performance, certifications, banking |

If one entity is pre-revenue (like both Leatherneck and HARBOR in July 2026), document the gaps honestly rather than pretending capability.

### Phase 2b: What Each Entity Actually Does

After the side-by-side rundown, add a section clarifying each entity's business model — especially needed when one entity has a complex, multi-faceted business that the comparison table alone can't convey. The user may specifically ask: "What type of work does [Entity] do so far and what can they go after? Are they B2B or B2G?"

For the less-familiar or more complex entity, research and present:

| Area | What to Surface |
|------|----------------|
| **Business model** | B2B (selling to contractors) vs B2G (selling to government) vs hybrid |
| **Productized offerings** | Fixed-price engagement models, SaaS tiers, published IP |
| **Active portfolio** | Named clients/members with engagement types and revenue evidence |
| **Technical infrastructure** | AI platforms, agent frameworks, repo count, deployed systems |
| **Published authority** | Books, frameworks, methodologies, speaking |

The July 2026 assessment added this after the user asked "what HARBOR actually does" — the side-by-side table showed entity facts but didn't convey that HARBOR is a B2B productization platform with 18 portfolio members, 5 productized engagement models ($12.5K-$50K), a published book on Amazon, a live SaaS website at harborgovcon.com, and 103 GitHub repos of AI infrastructure.

### Phase 3: Combined Capabilities Table

Map what each entity brings to each capability area:

| Capability Area | Entity A Brings | Entity B Brings |
|-----------------|-----------------|-----------------|
| SAM Infrastructure | UEI, CAGE, NAICS | — or "can register separately" |
| GovCon Admin | Named person + role | Named person + role |
| Technical Delivery | Specific skills | Specific skills |
| Past Performance | Documented contracts | Can build from Day 1 |
| etc. | | |

This table makes the complementarity visible and identifies gaps neither entity covers.

### Phase 4: Ranked Opportunities

Identify 4-6 concrete opportunity types, ranked by near-term viability:

- **🟢 Ready Now** — can pursue immediately (direct subcontracting, existing relationships)
- **🟡 Medium-Term** — needs setup (SBA certification, bank account, SAM registration)
- **🔴 Long-Term** — requires past performance or infrastructure neither entity has yet

Each opportunity card should include:
- Viability level + name
- Relevant NAICS/PSC codes
- Concrete description of the play
- What makes it viable (relationship, capability, timing)
- What's blocking it (if anything)

**Format each as a styled card** — short header, meta line with codes, 1-2 paragraph description. No generic categories — each must be specific to the two entities.

### Phase 5: Action Plan

Priority-ordered table with 5-8 near-term actions:

| Priority | Action | Owner | Timing |
|----------|--------|-------|--------|
| 1 (highest) | Specific next step | Name | Date window |

Lead with what can happen THIS WEEKEND. The July 2026 assessment had "Research opportunities closing in next 30 days" as Priority 1 because the user committed to doing it that weekend.

### Phase 6: Open Questions

Surfaced as 4-6 callout boxes covering:
- Entity structure decisions (member vs subcontractor)
- Clearance dependencies
- Employment conflict risks
- Member/partner buy-in
- Compensation model

These are the questions the two parties need to resolve before bidding. Don't propose answers — just frame the questions clearly.

### Phase 7: Reference Links

Include links to all source briefings at the bottom. The partnership assessment is a synthesis document — it should point to the detailed entity research, not duplicate it.

## HTML Aesthetic

Use **Thariq ivory/clay** (`#FAF9F5` / `#D97757` / `#141413`). This is an internal decision-making document, not an external consulting deliverable. The Thariq aesthetic signals "internal team briefing" vs the HARBOR dark theme which signals "client-facing consulting."

Key design elements:
- Side-by-side entity cards in a 2-column grid
- Callout boxes with color-coded left borders (green=ready, amber=medium-term, rust=blockers)
- Opportunity cards with left-border accent
- Compact tables for data
- Monospace meta-pills for dates/tags
- Reference links in monospace font at the bottom

## Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Building a dossier when the user wants a partnership assessment | The deliverable is forward-looking (what can they do together), not backward-looking (who is this person). If the user says "not a dossier, a starting point for discussion," delete the dossier and build the assessment. |
| Splitting one person into two | Cross-reference people dossiers in the relevant project repo (e.g., `~/repos/aecon-fcs/03-research/people-dossiers/`). Call transcripts can confuse first-name-only references. Verify against known rosters. |
| Using stale SAM.gov data | Pull fresh SAM.gov entity PDFs in the same session. Do not rely on cached or inferred registration status. The Leatherneck briefing was initially wrong about SAM status because it used stale search results. |
| Over-selling capability | Document gaps honestly. Both entities in the July 2026 assessment were pre-revenue with zero contract history. The briefing said so directly. |
| Generic opportunity categories | Every opportunity must be specific to THESE two entities — their NAICS codes, their relationships, their actual capabilities. "Subcontracting" is too vague. "CMMC/NIST compliance support through Westerman relationship" is specific. |
| Missing the "open questions" section | Partnership assessments need unresolved questions surfaced explicitly. Entity structure, member buy-in, clearance dependencies, comp model — frame them as callout boxes, not buried in prose. |
| Competing with entity research briefings | The partnership assessment is a synthesis. It links to the detailed Leatherneck intel briefing rather than duplicating its 500+ lines of research. |
| Not checking canonical entity records | If an entity has a documented presence on the local machine (canonical facts file, operations binder, portfolio directory), read those BEFORE building the side-by-side table. The July 2026 HARBOR column was initially wrong (said "no UEI, no SAM") because the HARBOR Initiative LLC canonical facts at `2026_books/operations/harbor-initiative-llc/00-canonical-facts.html` weren't consulted. SAM.gov data alone would have shown the UEI, but local canonical files have richer detail (EIN, formation docs, engagement-ready packet status, productized models). |
| Over-classifying business model as B2B-only when the entity is building toward B2G | Never write "B2B, not B2G" as a flat classification. If the user pushes back, they're usually right — check for B2G indicators: UEI assigned, SAM registration in progress, engagement-ready contracting packet (MSA/SOW/NDA/invoicing), federal activation in the roadmap. The correct framing when both are true: **"Dual-track: B2B today, B2G tomorrow"** — state current revenue source (B2B portfolio), then state the B2G trajectory with concrete blockers and timeline (e.g., "UEI assigned; full SAM completes ~2 weeks after bank account opens; then entity can bid as prime"). The July 2026 briefing used exactly this framing after user correction. |
| Missing the "what they actually do" section | When one entity has a complex business model (B2B vs B2G, SaaS platform, portfolio members, multiple revenue streams), the side-by-side table doesn't convey this. The user may explicitly ask: "what type of work do they do? B2B or B2G?" Add a dedicated section after the entity rundown with: business model classification, productized offerings with prices, active portfolio with named evidence, technical infrastructure, and published authority. |
| Skipping the NAICS overlap flag | If both entities share a primary NAICS code (e.g., both 541611), flag it. This is both an opportunity (they can bid the same codes through different vehicles) and a competitive risk (they're positioned identically). Don't let this go unremarked. |
