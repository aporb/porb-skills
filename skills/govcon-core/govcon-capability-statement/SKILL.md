---
name: govcon-capability-statement
description: Build a formal company charter or capability statement for a federal contractor — dual-use (federal + private), self-contained HTML, with mandatory past-performance table, scope areas, and limitations. Use after researching the founder's full professional footprint.
trigger:
  - "company charter"
  - "capability statement"
  - "corporate overview"
  - "federal subcontractor profile"
  - "past performance document"
  - "PDF company charter"
---

# GovCon Capability Statement / Company Charter Builder

Build formal, externally-shareable company charters or capability statements for federal contractors. Output is self-contained HTML in the ivory/clay/slate aesthetic, served via Nextcloud briefings at `brief.h.porb.dev`.

## When to use

- A GovCon prime contractor asks for a "company charter" or "capability statement" for a subcontractor
- A solo practitioner / small LLC needs a formal capability document for proposal packages
- A founder needs a dual-use document (federal primes + commercial prospects)
- The document will be shared as a PDF with federal contracting officers under NDA

## Workflow (6 Phases)

### Phase 1: Interview the Founder

Before any research, use `clarify` to ask:
1. **Positioning**: dual-persona (technical execution + strategic/productization), full-spectrum, or targeted to a specific workstream?
2. **Federal/private balance**: 90/10, 60/40, or 50/50?
3. **Counterparty pairing**: explicit prime pairing section, implied, or entity-only?
4. **Pricing visibility**: include engagement pricing or keep it off-document?

Defaults if the founder says "just build it": dual-persona, entity-only, 60/40 federal/private, pricing visible.

### Phase 2: Research the Full Footprint

Research in parallel across all sources:
- **Resume/CV** — latest HTML in `~/repos/2026_books/_personal/job-applications/`
- **Personal website** — about page, blog, ecosystem
- **Company website** — framework, about, pricing pages
- **GitHub** — verify public repo count via API: `curl -s https://api.github.com/users/<user> | python3 -c "import sys,json; print(json.load(sys.stdin)['public_repos'])"`
- **Published books** — verify Amazon links and GitHub handbook repos
- **Product catalog** — porbanderwala.cloud or equivalent (use browser for terminal-style SPAs)
- **Canonical facts** — `00-canonical-facts.html` for UEI/EIN/NAICS/SOS/etc.
- **Pipeline context** — any existing proposals, budget docs, or team bios showing how the entity is positioned
- **LinkedIn** — web_extract or web_search

### Phase 3: Build the HTML Charter

**13 mandatory sections** in order:

1. **Summary strip** — entity name, UEI/EIN, founder, clearance, veteran status. 4-5 cells in a bordered grid at the top.
2. **What [entity] is** — opening section: entity type, methodology, operating model, target markets. Operating model stated honestly (solo practitioner, small team, etc.).
3. **Scope areas** — dual-persona grid for solo practitioners: Technical Execution (builder) + Strategic & Productization (strategist). Side-by-side cards, 6 bullets each. For multi-person firms, organize by capability area.
4. **Products & free resources** — named products with one-line problem statements and direct links. NOT a repository count. Each product: name, stage tag, what it solves, link.
5. **Credentials & proof points** — 6-10 numbered cards in a 2-column grid. Verifiable achievements only.
6. **Past performance table** — structured: year, contract/award (with contract number as subtext), agency, role, dollar value, key contribution. If entity is new and past performance is individual (founder as employee), add a callout.
7. **Federal domain depth** — platforms (chip grid), compliance frameworks (2-col grid), agencies served (prose).
8. **Certifications & socio-economic** — credentials table + socio-economic designation. If a designation requires pending application, state explicitly.
9. **Engagement models** — table: engagement type, description, structure/pricing. Include federal subcontracting note.
10. **Limitations & scope boundaries** — two-column grid: Current Operating Model + What [entity] Does Not Do. Include bus-factor acknowledgment for solo practitioners.
11. **Commercial relevance** — the non-federal translation. Required for dual-use documents.
12. **Federal identity & legal** — canonical values table + brand vs. legal display rule callout.
13. **Contact** — table: name, emails, phone, portfolio, websites, LinkedIn, GitHub, location.

**Design**: Self-contained HTML. Ivory/clay/slate design tokens. Light mode only. System serif + sans + mono fonts. All links hyperlinked as `<a>` tags. Year column in past performance table: use `.pp-table` CSS class to shrink to 80px.

### Phase 4: Adversarial Review Gate

Dispatch via `delegate_task`. Load `govcon-response-adversarial-review` skill. Attack:
1. Factual errors (cross-reference every claim)
2. Omissions (what would a GovCon prime expect that's missing?)
3. Tone (too modest? too boastful? wrong register?)
4. Weak language (hedging, passive voice, qualifiers)
5. Structure (dual-persona split working? market balance right?)

After the subagent completes, do a FULL re-read of the document — never trust subagent self-reports. Apply all P0 fixes before user review. Apply P1 alongside user feedback.

### Phase 5: Past Performance Verification (Optional)

Spin up a research agent to cross-reference past performance claims against:
- USASpending.gov, FPDS, SAM.gov, GDICWins.com
- OrangeSlices AI, GAO protest docket
- Company press releases, GovTribe vendor profiles
- HigherGov contract pages

Add contract numbers, verify dollar values. If the document is an NDA partner document (not public filing), strip verification notes from the body — keep them in a separate research file.

### Phase 6: PDF Delivery

When the counterparty asks for a "PDF company charter," produce:
1. **Print-optimized HTML preview** — letter-size, `@page` rules, cover page with identity strip + NDA notice, page numbers, pure white background, page breaks before major sections
2. **Editable DOCX** — `pandoc charter-print-v2.html -o charter-v2.docx --from html --to docx`
3. **Final PDF** — only after user sign-off on preview

## Common Factual Pitfalls

### SBIR Claims
- "Active" vs "Prior": if the SBIR ended, say "Prior (completed [date])." Verify completion date.
- Designation: use exact agency/sponsor chain the founder specifies (e.g., "DoD/DoW CDAO SBIR PI").
- Dollar value: verify against published solicitation ceiling. Don't guess.

### SDVOSB Claims
- **Do NOT claim SDVOSB unless the founder has a VA disability rating.** VOSB self-certification needs only veteran status + honorable discharge.
- Default to "VOSB-eligible" unless the founder confirms disability rating.

### Protest Language
- "Under protest" = active and unresolved. "GAO protest denied" = resolved in awardee's favor.
- Verify protest status before writing. GAO docket is public.

### Solo Practitioner Language
- Do NOT say "cannot staff" or "cannot serve as prime." Say "currently operates as [solo], scaling through [AI/tech] rather than headcount."
- Always include bus-factor acknowledgment.

### GitHub Repo Counts
- Verify via API. Public count ≠ CLAUDE.md count. Round: "30+ public repositories."

### Products vs. Repos
- List named products, not repos. Each: name, tag, what it solves, link.

### Voice for NDA Partner Documents
- When shared under NDA: confident, declarative capability statement. NOT an audit report.
- Strip verification notes ("Source: founder's accounting; not independently verified") from the body.
- Partners under NDA get the inside truth — not a FOIA-proof filing.

### "Nearly Two Decades"
- Count from first professional work, not degree date. If 2006 → 2026 = two decades.

## HTML Output

- Self-contained HTML. No external CSS/JS.
- Write to `/data/nextcloud/data/amyn/files/briefings/`
- Scan: `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
- URL: `https://brief.h.porb.dev/<filename>.html`
- Version filenames: `-v1.html`, `-v1-1.html`, `-v2.html`
- All links hyperlinked. Every reference to a website, GitHub repo, Amazon listing, or email = clickable `<a>`.
- Print-friendly: `@media print { body { background: white; padding: 0; } }`
