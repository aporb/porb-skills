---
name: consulting-assessment-report
description: "Produce structured, self-contained HTML assessment documents for federal contracting consulting engagements — multi-phase analytical reports (e.g. HARBOR 6-phase, productization architecture, portfolio deep-dive, strategic pathway). Dark-theme, data-driven, with color-coded phase sections, risk registers, product portfolio cards, metric grids, timeline bars, and economic projection tables. Delivered as standalone HTML to Nextcloud briefings directory."
tags:
  - govcon
  - consulting
  - assessment
  - html-document
  - briefing
  - deliverable
  - dark-theme
  - harbormethod
related_skills:
  - contractor-portfolio-analysis
  - project-briefing
  - tailnet-agent-access-briefings
triggers:
  - "produce a comprehensive assessment for [company]"
  - "multi-phase analysis deliverable"
  - "consulting-grade HTML briefing"
  - "productization architecture assessment"
  - "strategic pathway document"
  - "6-phase assessment"
  - "dark-theme consulting deliverable"
---

# Consulting Assessment Report (HTML Deliverable)

## When to Use

- User asks for a **structured, multi-phase analytical assessment** of a federal contractor — productization readiness, strategic pathway, growth architecture
- The deliverable is a **self-contained HTML document** with color-coded phase sections, data tables, risk registers, product cards, metric grids, economic projections, and a call to action
- The consulting framework uses named phases (e.g. HARVEST → ARCHITECT → RISK-PROOF → BUILD → OPERATE → REPLICATE or any other structured methodology)
- The deliverable must be **standalone** (no CSS/JS dependencies), **responsive**, **printable**, and **projectable** (reads well on screen)
- Output path: Nextcloud briefings directory (`/data/nextcloud/data/amyn/files/briefings/`)
- User asks for a **partnership opportunity assessment** (two entities side-by-side, combined capabilities, tiered opportunities) — use the two-entity pattern below

## Interview-Then-Plan Workflow (for Open-Ended Research Requests)

When the user asks for open-ended research (e.g., "research opportunities closing in the next 30 days"), **always interview first** before executing. Use the `clarify` tool with up to 4 questions covering:

1. **Entity scope** — which entities are in play (e.g., Leatherneck only, HARBOR only, both, split by type)
2. **Capability lanes** — which service areas matter (e.g., CMMC compliance, cybersecurity, training, program management)
3. **Geographic scope** — national, state-specific, or unrestricted
4. **Deliverable format** — HTML briefing, CSV, JSON, all formats, plus whether to set up ongoing monitoring

Present the plan as a structured table (phases, data sources, timeline) and ask for confirmation before executing. This prevents wasted research on the wrong scope.

## Workflow: Interview → Research → Plan → Build (MANDATORY for Process/Org Design)

For any deliverable touching organizational design, process engineering, procurement workflows, or multi-stakeholder architecture, **do not jump directly to building the full HTML deliverable.** The user expects a phased approach:

1. **Interview** — Use `clarify` to get scope: who's the process owner, what's the current state (spreadsheets? email?), what's the org structure and reporting lines, what are budget/authority constraints, who are the stakeholders by role. The user will often provide a LinkedIn profile or org doc — read it and ask targeted questions about gaps. Key questions: financial approval thresholds, existing tech stack, volume of requests, reporting lines.
2. **Research** — Spin up parallel research agents (via `delegate_task`) to investigate: (a) enterprise best practices for this class of problem at similar-scale orgs, (b) technical feasibility in the target environment (e.g., M365 commercial tenant capabilities), (c) domain-specific governance/compliance requirements (e.g., federal procurement rules for GCC High software). Agents run in parallel — you keep working while they research.
3. **Plan** — Present a structured outline with research findings synthesized. Include the 70/30 boundary (standardized core vs. configurable surface — see `references/harbor-70-30-process-design.md`). Get user confirmation on the approach before building.
4. **Build** — Only then produce the final HTML deliverable. By this point, you have: confirmed scope, researched best practices, technical feasibility validated, governance requirements documented, and user sign-off on the outline.

The user will explicitly call out when you skip the research phase: "we should outline it first and research it all…spin it through multiple research agents figure out what works what's technically possible." This means you jumped to build without the research foundation. This workflow applies to: process design documents, org design proposals, procurement workflows, compliance architectures, and any deliverable where the user says "figure out what's technically possible."

## Two-Entity Partnership Assessment Pattern

When assessing two entities for partnership (e.g., Leatherneck + HARBOR), use this structure:

1. **Executive summary callout** — the bottom-line thesis (who brings what, what's the play)
2. **Side-by-side entity rundown** — two cards: UEI/CAGE, formed date, entity type, SAM status, SBA certs, contracts, leadership, POC structure, flags (credit cards, disaster registry, etc.)
3. **"What X Actually Does" section** — B2B/B2G breakdown, productized models, portfolio, SaaS platform, published authority, AI infrastructure
4. **Combined capabilities table** — 8 rows: SAM infrastructure, GovCon admin, CMMC/NIST, cybersecurity, training, program management, capture/proposals, past performance. Columns: capability area, Entity A brings, Entity B brings.
5. **Core Gap callout** — what each entity lacks and why they need each other
6. **Tiered opportunity cards** — 🟢 pursue now, 🟡 with partner/next cycle, ⚪ watch/not fit. Each card: title, tags (SBIR/OTA/C-UAS/AI), meta (agency, phase, deadline, value), why it fits, action, entity recommendation.
7. **Near-term action plan** — prioritized table with priority pill, action, who, timing
8. **Open questions** — callout-amber boxes for unresolved issues (entity structure, clearance dependency, conflict of interest, member buy-in)
9. **Reference briefings** — cross-links to related briefings

**Dual-track B2B/B2G framing rule:** Never say "B2B not B2G." HARBOR is B2B today (portfolio members, productized engagements) but built for B2G (UEI assigned, engagement packet ready). The correct framing is "B2B today, B2G tomorrow" with the partnership as the bridge.

## When NOT to Use

- Construction/renovation planning → `project-briefing`
- UI/UX design artifact → `claude-design` or `sketch`
- Tailnet agent access briefing → `tailnet-agent-access-briefings`
- Contract portfolio analysis (USAspending API deep-dive) → `contractor-portfolio-analysis`
- Simple markdown document → `plan`
- One-off analysis without the consulting-deliverable quality bar → plain response is fine

## Aesthetic Standards

### Theme Selection: Audience Determines the Theme

**For external consulting deliverables (clients, prospects):** Use the HARBOR Dark Theme (`#0f172a` bg). This signals consulting-grade quality for client-facing documents.

**For internal compliance/regulatory briefings (same company, federal team):** Use the Thariq ivory/clay aesthetic (`#FAF9F5` / `#D97757`). This is the correct choice when the document supports internal decision-making (compliance, IT, legal, estimating) rather than external presentation. See the html-effectiveness reference gallery at `~/repos/html-effectiveness/`.

**Rule of thumb:** Client-facing → dark theme. Internal team → Thariq. The InEight briefing (July 2026) was an internal Aecon compliance briefing — Thariq ivory/clay was the correct choice. If the deliverable had been for a DoD contracting officer, it would have been dark theme.

Use this CSS variable system — it signals consulting-grade quality. **Do not substitute the Thariq ivory/clay aesthetic** (that's for internal briefings). The HARBOR dark theme is for consulting deliverable artifacts.

```css
:root {
  --harbor-harvest: #3B82F6;
  --harbor-architect: #8B5CF6;
  --harbor-riskproof: #EC4899;
  --harbor-build: #F97316;
  --harbor-operate: #10B981;
  --harbor-replicate: #06B6D4;
  --bg: #0f172a;
  --card: #1e293b;
  --card-elevated: #293548;
  --border: #334155;
  --text: #ffffff;
  --text-secondary: #cbd5e1;
  --text-dim: #94a3b8;
  --text-dimmer: #64748b;
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  --critical: #DC2626;
}
```

### Phase-Color Badge Rule

Each section gets a phase-letter badge (a colored circle with the phase letter, e.g. H, A, R, B, O, R) and colored border-left for highlight boxes matching the phase color:

| Phase | Color | Hex | Badge + Highlight |
|-------|-------|-----|-------------------|
| Harvest | Blue | `#3B82F6` | `var(--harbor-harvest)` |
| Architect | Purple | `#8B5CF6` | `var(--harbor-architect)` |
| Risk-Proof | Pink | `#EC4899` | `var(--harbor-riskproof)` |
| Build | Orange | `#F97316` | `var(--harbor-build)` |
| Operate | Green | `#10B981` | `var(--harbor-operate)` |
| Replicate | Cyan | `#06B6D4` | `var(--harbor-replicate)` |

### Known Issue: CSS Variable Names

The six-phase CSS variables use `--harbor-*` as a naming convention in the delivered HTML artifact. This is the naming convention for the design tokens — it is NOT a reference to the methodology in the body text. The methodology name ("HARBOR" or "HARBOR Initiative") appears **only in the attribution footer**, never in the body of the assessment. The analysis demonstrates capability through quality; it does not pitch the framework.

## Core Workflow

### Phase 1: Requirements & Source Intake

1. Read the brief carefully — identify: company facts, assessment structure, number of phases, any specific data to include or exclude
2. Collect all source files: existing OSINT dossiers, FRI scorecards, harvest reports, SBIR analyses, internal notes
3. Note the **indirect positioning constraint**: the framework is demonstrated through the work, never described as a methodology in the body. Attribution goes in the footer only.

### Phase 2: Data Organization

Organize all data before writing HTML. Key data categories:

- **Company profile:** legal name, UEI, CAGE, founded date, revenue (T12M, lifetime), FTE count, certifications (EDWOSB/WOSB/SB/8(a)), leadership, location
- **Contract archaeology:** vehicles (GSA MAS, SeaPort-NxG, OASIS+, agency IDIQs), lifetime obligations (prime vs sub), agency concentration (Navy/DoD %, other agencies)
- **Revenue composition:** T&M vs FFP vs product split, GP margins, revenue-per-employee
- **Hidden assets:** methodology, tech stack (AI/ML tools listed), partnerships (Celonis, Deloitte, KPMG), product-adjacent contracts (custom tools, training POs)
- **Acquisition targets (if applicable):** SBIR/STTR awards being acquired, cost, seller, customer of record, Phase III sole-source pathway
- **Risks:** concentration risk, legal/novation risk, T&M margin pressure, IP maturity, regulatory surface (CMMC, FedRAMP), competitive landscape
- **Economics:** build costs, margin targets, revenue-per-employee comparisons, build sequence, timeline to revenue

### Phase 3: HTML Composition

Build the document as a single self-contained HTML file. Standard structure:

1. **Cover** — HARBOR letter badges, h1 title, subtitle, metadata grid (UEI, CAGE, leadership, SAM exp)
2. **Hero Summary** — 3×2 grid of key metrics (revenue, FRI score, FTEs, acquisition cost, etc.)
3. **Timeline Bar** — horizontal milestone track showing current → Q3 2026 → Q1 2027 → Q4 2027 progression
4. **Phase Sections** — one per phase, each with:
   - Phase header (letter badge + h2 + subtitle)
   - Data tables with color-coded values
   - Highlights (warning/success/critical/architect/build/operate)
   - Callout boxes for key insights
   - Risk rows (when applicable) with severity badges
   - Product cards (when applicable) in 2-column grids
   - Metric grids (4-column stat blocks)
   - Trajectory boxes for sequential pathways
5. **Call to Action** — centering block with the engagement thesis
6. **Footer** — attribution (framework name once), disclosure (prior employment if applicable), status line

### Phase 4: Visual Components

Build these reusable components from CSS (defined in the `<style>` block):

- **`harbor-letters`** — flex row of 6 colored circles (36px, 800-weight) with phase letters
- **`hero-card`** — dark card with label/value/sub stack, phase-colored `.value`
- **`hero-summary`** — 3-column grid of hero cards
- **`phase-section`** — bottom-bordered section wrapper
- **`phase-badge`** — 48px colored circle with phase letter
- **`highlight`** — left-border-accented box (success/warning/critical/architect/build/operate variants)
- **`callout`** — bordered box with `.callout-label` header
- **`risk-row`** — flex row with severity badge + title + detail
- **`product-card`** — 2-column grid card with name/source/desc/meta
- **`comparison-matrix`** — two-product side-by-side table with color-coded cells (clay for risk, olive for strength, slate for neutral). Used for equivalency CSP vs. certified alternative comparisons. 8 rows typical: FedRAMP status, Marketplace listing, CR26 risk, POA&M risk, AO backstop, licensing, functional fit, CO/C3PAO scrutiny.
- **`question-tracker`** — persistent table at the bottom of a regulatory/compliance briefing tracking open questions. Columns: #, Question, Status (color-coded: olive=Answered, clay=Risk Identified, slate=Open, g500=Partial), Owner/Next Step. Rows can be 8-12 items spanning multiple rounds of inquiry. Critical for multi-stakeholder engagements where questions are being resolved incrementally across email threads and vendor responses.
- **`trajectory-box`** — numbered-step pathway with colored dots
- **`timeline-bar`** — horizontal milestone track with dots and connecting lines
- **`timeline-track`** — flex row of `.tl-marker` nodes with `.tl-line` connectors
- **`tag`** — inline badge (strong/mod/weak/critical variants)
- **`cta-block`** — centered gradient background with `.cta-text` + `.cta-sub`

### Phase 5: Data Presentation Standards

- **Tables:** full-width, collapsed borders, 13px font, 11px uppercase headers, first column bold, `.num` class for monospace numbers, `.delta-up`/`.delta-flat` for deltas
- **Currency:** always prefixed with `$`, use K/M suffixes after first occurrence (e.g. `$247M` not `$247,000,000`)
- **Percentages:** one decimal place for precision where available (`91%`, not `~91%`)
- **Em dashes** (`&mdash;`) in HTML for sentence breaks in body text
- **Bullet lists** for unordered items; numbered lists for ordered sequences
- **Tables for comparison** — avoid prose walls when tabular data is clearer
- **Question tracker tables** — status column uses color-coded badges: olive (`#788C5D`) for "✅ Answered", clay (`#D97757`) for "⚠️ Risk Identified", g500 (`#87867F`) for "◐ Partial", slate (`#141413`) for "Open". Every row has an Owner/Next Step column with a named person and specific action.
- **Comparison matrix** — header row labels the two options; cells use clay for risk factors and olive for strengths. Typically 8 rows. Makes the case visually without requiring paragraph reading.
- **Email drafts at the bottom** — for multi-stakeholder engagement briefings, include a send-ready reply-all email as the final phase (`.card` container with conversational prose). This is the operational deliverable — the briefing is the supporting document. Write it like a human, not a compliance analyst: short sentences, soft tone, acknowledge corrections transparently, ask specific people specific questions.

### Phase 6: Delivery

```bash
# Copy to Nextcloud briefings
cp /path/to/deliverable.html /data/nextcloud/data/amyn/files/briefings/<filename>.html

# Fix permissions
chown www-data:www-data /data/nextcloud/data/amyn/files/briefings/<filename>.html
chmod 644 /data/nextcloud/data/amyn/files/briefings/<filename>.html

# Scan into Nextcloud
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"
```

## Briefing Update Workflow (Plan-Driven)

When the user provides a structured update plan file (e.g., `briefing-v3-update-plan-2026-07-20.md`) with explicit changes for an existing HTML briefing, use this targeted-patch workflow rather than rebuilding from scratch:

### Pre-Flight
1. **Read the plan file first** — it lists every change with section references, exact content to add, and constraints (CSS preservation, section numbering, etc.)
2. **Read the entire current briefing file** with `read_file` (no offset/limit — read the full file). You need to understand the full structure before patching.
3. **Map the plan to insertion points.** For each new section, identify the exact context string that marks where it should be inserted (e.g., the closing `</div>` + opening comment of the NEXT section).

### Execution Order
Always update in this sequence:
1. **Meta/date line** — update "Updated [date]" in the meta paragraph
2. **Opening callouts** — any factual corrections (e.g., "contract" → "cooperative agreement")
3. **TOC** — add all new section entries BEFORE adding the sections themselves
4. **New sections** — insert each new section using `patch` with a unique surrounding context string. The `old_string` should include enough context (the section BEFORE and AFTER the insertion point) to ensure the match is unique
5. **Existing content updates** — modify tables, add dates, update bios
6. **Risk matrix / appendices** — add new rows at the end
7. **Footer attribution** — update sources and date

**For internal briefings (Thariq ivory/clay aesthetic):** Load `references/html-effectiveness-tokens.md` for the complete CSS token block, component classes, and color semantics. All internal briefings (Leatherneck+HARBOR, personal working docs, agent-to-agent artifacts) use this aesthetic — never Aecon branding or HARBOR dark theme.

### Patch Technique for HTML Sections
Use `patch(mode='replace')` with a context string that bridges the section BEFORE and AFTER:
```
old_string: the last unique snippet of the PREVIOUS section + the opening of the NEXT section
new_string: same previous snippet + YOUR NEW HTML + opening of next section
```
This ensures you never accidentally match a similar string elsewhere in the file.

### Verification After Updates
1. **Check all section anchors:** `search_files(pattern='<h2 id=')` — confirm every TOC entry has a matching `id`
2. **Count risks/items:** `search_files(pattern='<td>R\\d+</td>')` — verify expected count
3. **Check line count:** `wc -l` — sanity check the file grew, not shrunk
4. **Verify HTML structure:** Read the first 5 and last 10 lines — confirm `<doctype>`, closing `</body>`, `</html>` are intact
5. **Spot-fix introduced bugs:** If a patch produced a double `</td>` or similar artifact, fix it immediately with another targeted patch

### Common Pitfalls
| Pitfall | Prevention |
|---------|------------|
| `old_string` matches multiple locations | Include surrounding HTML context — the section before AND after the insertion point |
| Double-closing tags from malformed new_string | Count tags before patching; verify with search after |
| TOC doesn't match sections | Always update TOC first, verify with search_files after all sections are added |
| Forgetting to update footer/sources | Add the new sources (calls, people, dates) in the final patch |
| Using `read_file` with offset/limit, then patching | The tool warns about partial reads — re-read the full file before patching to avoid stale context |

- [ ] Single self-contained HTML file (no external CSS/JS/fonts)
- [ ] Dark theme (#0f172a background) for consulting deliverables
- [ ] No framework/methodology name in body text (footer attribution only)
- [ ] Every number traceable to source material (no invented data)
- [ ] Color-coded sections matching phase badges
- [ ] All tables rendered correctly (no broken cells, proper alignment)
- [ ] Timeline bar shows realistic milestone dates
- [ ] Risk register covers all identified risks with severity ratings
- [ ] Call to action presents the engagement thesis
- [ ] Footer includes: framework attribution once, disclosure note (prior employment if applicable), status line
- [ ] File saved to Nextcloud briefings directory
- [ ] Permissions: www-data:www-data 644
- [ ] Nextcloud scan: `docker exec --user www-data nextcloud php occ files:scan`
- [ ] Delivered with file path and Nextcloud URL

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Pitching the methodology in the body | Framework name appears **only** in the attribution footer. The analysis demonstrates capability — never describe it as a methodology in running text. |
| Thariq ivory/clay aesthetic on a consulting deliverable | Use HARBOR dark theme (#0f172a bg) for external/consulting deliverables. Reserve Thariq (#FAF9F5, #D97757) for internal briefings. |
| Inventing data or numbers | Every figure must come from the source materials. If a number is uncertain, flag it explicitly ("estimated," "approximately"). |
| Not correcting earlier errors when new data emerges | When a later document (email thread, new SAR section, deeper research) reveals the earlier analysis was wrong, insert a NEW discovery section with a .5 suffix (e.g., "03b") between existing phases — do not erase the old analysis. Acknowledge the correction transparently: name what the old analysis said, what the new data shows, and what changes. This builds credibility, not undermines it. Example: "The earlier briefing said: X. This was wrong in two ways: Y, Z." |
| Verbose CTA that sells, not summarizes | The CTA summarizes the analytical thesis and recommends action. It does not sell a service or pitch a product. |
| Missing prior-employment disclosure | If the analyst has a prior relationship to the subject company, disclose it prominently in the footer (not hidden). |
| Framework phase letters in body | The H-A-R-B-O-R letter badges appear in the cover and as section badges. Do NOT spell out the methodology name (e.g. "The HARBOR framework") in body text. |
| CSS variable names leaking into SVG | The HARBOR dark theme uses CSS variables that work in HTML/CSS. Do not use CSS variables in SVG `fill` or `stroke` attributes — SVG rendering silently drops them. For any SVG elements, hard-code the hex values. |
| `docker exec` without `--user www-data` | The `occ files:scan` command MUST run as the www-data user. Missing `--user www-data` causes permission errors. |
| **Referencing attachments you haven't extracted** | When working from user-provided screenshots or email threads, NEVER describe the content of files you can only see as attachment names or icons — architecture diagrams, CR26 response documents, POA&M registers. If OCR or vision_analyze didn't extract the content, don't talk about it. Say "I can't see this file" or ask the user to share it, rather than inventing or guessing. The user will correct you — and it damages credibility. |
| **Writing compliance-speak in email drafts** | Email drafts embedded in briefings should sound human, not like a compliance memo. Short sentences. Soft tone. Acknowledge corrections ("I flagged this earlier but it turned out to be a non-issue"). Ask specific people specific questions. No bullet points longer than two lines. The conversational version goes in the email — the analysis stays in the briefing. |
| **Editorial parentheticals and version history in deliverables** | Stakeholder-facing documents must read as a single voice — not a development changelog. Remove: "(reduced: Amyn no longer in-line)", "(updated after Justin's review)", "(per C3PAO assessor feedback)", "not the X originally proposed", version badges in titles, any before/after comparison language. The reader should never see the edit history. If you need to explain a decision, fold it into the prose naturally — don't parenthesize it. |
| **Splitting one person into multiple entries** | Call transcripts can reference the same person by first name in one turn and last name in another (e.g., "David" and "Gable" = David Gable). Always cross-reference people dossiers in the relevant project repo before treating references as separate individuals. For Aecon deliverables, check `~/repos/aecon-fcs/03-research/people-dossiers/` and the pre-start briefing roster. |
| **Using people's names instead of roles/titles in org process documents** | When building internal process or org design documents for a client, use role titles (e.g., "Director, IS Vendors & Contracts") not specific names in process flows, RACI tables, and approval chains. The only exception: the process owner who will own and socialize the deliverable. Remove names of people not directly relevant — the user will flag these explicitly ("no Kerem"). The user will correct this: "try not to mention random people and actually use their titles or roles." |
| **Including consultant branding in client-internal deliverables** | When building a document for a client stakeholder to socialize internally (e.g., a process design for a Director to present to their VP), the document must be white-label. No consultant name, no framework branding in body text. The user will say "let's leave our name off of this." The stakeholder presents it as their own work. Footer attribution only if the user explicitly approves it. |
| **Skipping the research phase for complex process design** | Do not jump from a brief interview directly to building a full HTML plan with process flows, SharePoint architecture, and action plans. The user expects: interview → parallel research agents → synthesized findings → outline for approval → then build. When the user says "we should outline it first and research it all…spin it through multiple research agents figure out what works what's technically possible," you skipped the research phase. Applies to process design, org design, procurement workflows, and compliance architectures. |
| **Writing for director-level audiences — tone calibration** | Director-level and above readers care about: options analysis, cost-benefit framing, risk identification, and a clear recommendation. They do NOT want: 'brutal' language about internal deficiencies (even if accurate), complaints about their organization's gaps, or framing that sounds like the author is telling them they are failing. Use a professional, options-forward tone: acknowledge what has been accomplished, identify the natural scaling constraints that any growing organization faces, and present the partnership as one viable option among several — not the only answer. The document should be something they would feel comfortable forwarding to their peers. Test before delivering: 'Would a director at this company feel respected reading this?' If the answer is no, rewrite. |

## Example: Known-Good Section Template

```html
<div class="phase-section">
  <div class="phase-header">
    <div class="phase-badge" style="background: var(--harbor-harvest)">H</div>
    <div class="phase-title-group">
      <h2>Harvest &mdash; What [Company] Already Has</h2>
      <div class="phase-subtitle">Inventory assets: vehicles, contracts, IP, distribution channels</div>
    </div>
  </div>
  <!-- Body content: tables, highlights, metric grids, risk rows -->
</div>
```

## Reference Files

- `references/significance-harbor-assessment-2026-07-10.html` — Working example of a full 6-phase consulting assessment report in HARBOR dark theme. 62KB self-contained HTML covering 8 contract vehicles, 2 SBIR acquisitions ($170K), 6 Signify products, 8 risks, build economics, organizational transition, and valuation impact. Demonstrates all visual components (hero-summary, timeline-bar, product-grid, risk-rows, trajectory-box, metric-grids) and the indirect positioning discipline (framework name appears once in footer only).
- `references/html-effectiveness-tokens.md` — Complete CSS design tokens for the Thariq ivory/clay aesthetic used in internal briefings (Leatherneck+HARBOR, personal working documents, agent-to-agent artifacts). Includes full token block, copy-ready CSS reset, reusable component classes (stat band, tables, cards, callouts, tags, verdict box, TOC, timeline), and color semantics table. Use this when building or updating any internal briefing that uses the html-effectiveness aesthetic rather than Aecon branding or HARBOR dark theme.
