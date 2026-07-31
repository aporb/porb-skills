# DOE SBIR/STTR Research Patterns

DOE SBIR/STTR is structurally different from DoD SBIR. The program is administered by the DOE Office of Science (OSTI) rather than the service components. This file covers where to find DOE SBIR opportunities, how they're structured, and key research patterns.

## Where DOE SBIR Lives

| Source | URL | Notes |
|--------|-----|-------|
| DOE SBIR/STTR homepage | `science.osti.gov/sbir` | Program rules, solicitations, awards data |
| Current solicitations | `science.osti.gov/sbir/Funding-Opportunities` | Links to open FOAs (Funding Opportunity Announcements) |
| SBIR.gov (DOE filter) | `sbir.gov/topics?agency=DOE` | DOE topics mixed with DoD — filter by agency param |
| PAMS submission system | `pamspublic.science.osti.gov` | DOE's submission portal — pitch and full proposal go here |
| Solicitations archive | `science.osti.gov/sbir/Solicitations` | Past FOAs with award data |

## Key Differences from DoD SBIR

| Dimension | DoD SBIR | DOE SBIR |
|-----------|----------|----------|
| Solicitation system | Topic numbers (AF241-D001, etc.) with DoW batches | FOA numbers (DE-FOA-0003548) with release/close dates |
| Agency structure | Component-specific (Army, Navy, USAF, DARPA, MDA, SOCOM) | Office of Science (SC) + applied offices (EERE, FE, NE, EM) |
| Phase I format | Direct proposal (10-15 pages topic-specific) | **Pitch first** (700 words, 4 criteria) → invited full proposal |
| Topics on SBIR.gov | Current + prior batch (4-5 months overlap) | Current batch only — older FOAs drop off quickly |
| Phase II timing | Sequential: Phase I award → Phase II solicitation | Overlapping: Phase II FOA runs concurrently with Phase I |
| Program office | dodsbirsttr.mil | science.osti.gov/sbir |
| Registration | DSIP + SAM.gov | PAMS + SAM.gov + Grants.gov |

## DOE SBIR Structure

### Phase I (Concept Stage)

DOE Phase I uses a **two-stage submission**:

1. **Pitch** (Concept Paper) — ~700 words covering four equally weighted areas:
   - Technical merit and feasibility
   - Understanding of topic scope
   - Commercialization potential (from Stage 1 — not after award)
   - Qualifications of key personnel
   - *Pitch is the primary gate — DOE evaluates on content only, not format*

2. **Full Proposal** (by invitation only) — detailed technical proposal with budget
   - Only pitch submitters rated "encouraged" or "highly encouraged" advance
   - Typical award: ~$200K over 12 months
   - ~40 awards per topic cluster across 4-5 topics (roughly 8-10 per topic)

### Phase II (Development Stage) 

- Opens separately — typically 12-18 months after Phase I round
- **Gated to prior Phase I awardees** (unlike DoD Phase II which has open topics)
- FY25 Phase II had a **$147M pool** for selected awardees
- Funding up to $1M over 24 months
- Evaluation criteria: Phase I commercialization track record, technical results, Phase II plan

### Phase III

- Non-SBIR funds only (private, government procurement, follow-on)
- DOE encourages Phase III through its technology transfer programs

## FOA Numbering Pattern

DOE SBIR FOAs follow: `DE-FOA-000XXXX`

The same FOA number typically covers both Phase I and Phase II under a single umbrella, with separate submission tracks. Example breakdown:

```
DE-FOA-0003548
├── Phase I (Concept Stage) — pitch due Sept 10, 2026
│   ├── Topic 1: Radioisotope Power Systems (Topic 1a/b/c)
│   ├── Topic 2: Fission Surface Power (Topic 2a/b)
│   ├── Topic 3: Advanced Electric Propulsion (Topic 3a/b)
│   └── Topic 4: Enabling Technologies (Topic 4a/b/c/d)
└── Phase II (Development Stage) — due Sept 25, 2026 (FY25 release)
    └── Specific topic numbers (match prior Phase I topics under FY24 rounds)
```

## Research Workflow for DOE SBIR

### Step 1: Agency-Filtered SBIR.gov Search

Start broad — find all open DOE SBIR/STTR topics:

```
curl -sL -A "Mozilla/5.0 ..." "https://www.sbir.gov/topics?page=0&agency=DOE"
```

DOE topics are mixed with DoD on SBIR.gov but fewer in number (~4-5 topics per round vs 70+ for DoD). Extract by matching "Department of Energy" in the agency field.

### Step 2: Direct DOE SBIR Site Search

Check `science.osti.gov/sbir/Funding-Opportunities` for featured open solicitations. This site often publishes:
- FOA amendment notices
- Informational webinars (recorded, helpful for evaluation criteria)
- Topic-specific PDFs with full scope descriptions
- Phase II release announcements

### Step 3: FOA Number Cross-Reference

Search SBIR.gov by the FOA number directly — DOE FOAs have a dedicated page per solicitation. Pattern: `sbir.gov/node/<numeric-id>` (find via sbir.gov search).

### Step 4: Phase II Tracking

Phase II FOAs are released 12-18 months after the corresponding Phase I. They are **NOT** discoverable through Phase I keywords alone — search explicitly for "Phase II" + "DOE" + the FOA-release year. Phase II release cycles are separate from Phase I cycles and may already be open while Phase I is still accepting pitches.

### Step 5: Program Redesign Awareness

Under the SBIR Reauthorization Act, DOE has adopted the new naming:
- Phase I → **Concept Stage**
- Phase II → **Development Stage**
- Some DOE documents use the new names, some use the old — search both

## Sample DOE SBIR Topics (Genesis Mission, FY26)

From the Fall 2026 Phase I round (DE-FOA-0003548, topics 1-4):

| Topic | Subtopic | Focus |
|-------|----------|-------|
| 1. Radioisotope Power Systems | 1a | High-specific-power skutterudite-based RPS |
| | 1b | High-efficiency thermophotovoltaic converters |
| | 1c | Additive manufacturing of RPS components |
| 2. Fission Surface Power | 2a | Advanced Stirling converters for fission |
| | 2b | Manufacturing of uranium nitride fuel pins |
| 3. Advanced Electric Propulsion | 3a | High-power Hall thrusters (100+ kW) |
| | 3b | Lifetime-extending thruster simulations |
| 4. Enabling Technologies | 4a | Low-mass radiation-hardened power electronics |
| | 4b | High-temperature superconducting cables |
| | 4c | High-data-rate optical communications (deep space) |
| | 4d | Autonomous health management for nuclear systems |

## SBIR Reauthorization Act — DOE Impact

The 2023 reauthorization (extended through 2026 continuing resolutions) introduced:

- **Commercialization focus from Phase I** — the Phase I pitch must show a Stage 1 commercialization plan, not just "will commercialize in Phase II"
- **$147M Phase II pool (FY25)** — DOE set aside this amount specifically for Phase II-to-Phase III transition
- **Three-stage commercialization framework** (Stage 1 = market discovery, Stage 2 = customer discovery/partners identified, Stage 3 = sales/revenue)
- **Pilot programs** for Phase IIA (interim funding) and Phase IIB (bridge to Phase III)
- **Expedited award timelines** — DOE targets 90 days from full proposal submission to award

## Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Searching SBIR.gov by keyword misses DOE topics | Always filter by `agency=DOE` — DOE topic titles use program-specific terminology not captured by generic space/nuclear keywords |
| Treating Phase I and Phase II as sequential | They're **concurrent releases** — the Phase II FOA for the PRIOR cycle may be closing while this Phase I opens. Check both. |
| Applying DoD SBIR rates ($150K) | DOE Phase I awards are typically **$200K** — budget accordingly |
| Ignoring the pitch stage | DoD allows direct full proposals; DOE Phase I requires pitching first. Missing the pitch deadline locks you out for the round. |
| Mistaking "open to all small businesses" for "no competition" | DOE SBIR is HIGHLY competitive (~8-10 awards per topic from ~50+ pitches). The pitch is the first cut. |
| Assuming topic close dates are firm | DOE sometimes extends FOAs. Check the DOE SBIR site for amendment notices. |
| Using SBIR.gov detail pages as primary source for scope | DOE SBIR.gov pages for DOE topics are often sparse. The full scope document is on the DOE SBIR site as a PDF attachment to the FOA. Always find and read the PDF. |

## See Also

- `fedcon-opportunity-research` → `references/sbir-topic-scraping.md` (DoD-focused, but SBIR.gov listing parser works for DOE too)
- `fedcon-opportunity-research` SKILL.md Phase 6 section for the `/topics` curl recipe
- DOE SBIR/STTR program page: `science.osti.gov/sbir/About`
- PAMS submission docs: `pamspublic.science.osti.gov`
