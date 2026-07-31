---
name: aecon-brand-system
description: "When creating any branded deliverable for Aecon — documents, presentations, briefings, UI mockups, email templates, or any visual asset that needs to match Aecon's corporate identity."
version: 1.6.0
---

# Aecon Brand System

## When to Use

When creating any branded deliverable for Aecon — documents, presentations, briefings, UI mockups, email templates, or any visual asset that needs to match Aecon's corporate identity AND will be shared with Aecon stakeholders (FBU team, leadership, clients, partners).

**When NOT to use this brand system:** Internal intelligence documents, personal working briefings, repository sync reports, and agent-to-agent artifacts use the **html-effectiveness aesthetic** instead (ivory `#FAF9F5`, clay `#D97757`, slate `#141413`, oat/olive accents, system serif+sans+mono). These are internal working documents — NOT Aecon-branded deliverables. The distinction: if it carries the Aecon logo and is intended for Aecon stakeholders, use this brand system. If it's an internal intelligence report, repo index, or working briefing for Amyn's personal use, use html-effectiveness. When in doubt, default to html-effectiveness — it's safer to be unbranded internally than to brand something incorrectly.

## Logo
- **Official file:** `logo-aecon-red.png` — 460×69px PNG RGBA, stored at Nextcloud Downloads (`/data/nextcloud/data/amyn/files/Downloads/logo-aecon-red.png`)
- **Copy at:** `/data/nextcloud/data/amyn/files/briefings/aecon-assets/logo-aecon-red.png`
- **URL:** `https://brief.h.porb.dev/aecon-assets/logo-aecon-red.png`
- **Style:** Bold sans-serif wordmark "AECON", horizontal, slightly rounded letterforms
- **Color:** #E51937 (logo file red — authoritative)

## Two Reds (Important)
| Context | Hex | Usage |
|---------|-----|-------|
| Logo / Print / Branding | `#E51937` | Logo file, print materials, any deliverable placing the brand mark |
| Web UI / Digital | `#C8102E` | Website CSS (headings, links, CTAs, buttons) |

Never mix both reds in the same design. Pick based on context.

## Color Palette
- **Aecon Red (logo):** #E51937
- **Aecon Red (web):** #C8102E
- **Charcoal:** #252525 (dark text, grey headings)
- **Body Gray:** #464646 (default body text)
- **Silver:** #747679 (secondary CTA links)
- **Mid Gray:** #707070 (footer, metadata)
- **Border Gray:** #EAEAEA (subtle borders)
- **Teal:** #7DC4CC (decorative dividers ONLY — 1 use on entire site)
- **White:** #FFFFFF (base background)

## Typography
- **Font:** Univers LT Pro 45 Light (via MyFonts, ID: 39d17b)
- **Weights:** Regular 400, Italic 400i, Bold 700, Bold Italic 700i
- **Font files:** Downloaded at `/tmp/aecon-brandkit/fonts/` (woff2/woff/ttf/eot for all 4 weights)
- **Heading system:** Custom classes (.hs-largest, .hs-standard) — Univers Bold, negative letter-spacing (-1px to -6px), responsive scale (1.625rem → 4.5rem)
- **Body text:** 0.875rem (14px), line-height 1.429, color #252525
- **CSS fallback:** `font-family: "Univers", "Univers LT Pro", "Helvetica Neue", Arial, sans-serif`

## UI Components
- **Buttons:** Outline style — white fill, 2px solid red border, Univers Bold. Hover: fills red, border becomes white, text becomes white. 0.25s transition.
- **CTA Links:** Red text with animated red underline bar (::after pseudo, 2px height)
- **Grey CTAs:** Silver (#747679) text/underline, transitions to red on hover
- **Chevron:** Solid red angled right-pointing arrow (icon-chevron-right-red.png) — flat, no gradients

## Iconography
- **Core Values:** 4 icons (Safety First, Accountability, Inclusion, Integrity) — 417×418px PNG, grayscale line-art in circular frames
- **Social Icons:** Grayscale (Twitter/X, LinkedIn, Instagram, Facebook, TikTok)
- **UI Icons:** Close, mail, email, play, pause, zoom in/out, chevron — all flat PNG with alpha

## Photography Style
- Large-scale infrastructure (bridges, dams, nuclear facilities, utility lines)
- Aerial/drone perspectives preferred
- Workers always in orange safety vests + white hard hats with AECON wordmark
- Signature treatment: B&W with selective orange (safety gear pops)
- Red corrugated metal as recurring portrait background
- NO stock photos, NO unbranded workers

## Full Brand Kit
- **HTML reference:** https://brief.h.porb.dev/aecon-brandkit.html
- **Source HTML/CSS:** `/tmp/aecon-brandkit/` (18MB — 32 images, 16 fonts, 5 CSS files, 4 HTML pages)

## Brand Rules
1. Always use the logo file (logo-aecon-red.png) — don't reconstruct from CSS text

### CRITICAL: AECOM ≠ Aecon — confirm the employer before any external research or deliverable
**Pitfall:** Amyn works for **Aecon** (Canadian, TSX: ARE, @aecon.com email — established by this skill and his M365 environment). A task that says "AECOM" almost always means **a different company**: AECOM (NYSE: ACM, American, HQ Dallas, $16B infrastructure consulting firm). The two are constantly confused — even Wikipedia carries an explicit hatnote disambiguating them. Researching or writing about the wrong one produces a deliverable that is useless or actively misleading, and the error is expensive because it's discovered late (after the full research/build cycle).

This session, a research task literally named "AECOM" was executed against the American firm (AECOM) and produced a 17-page findings doc — but the loaded skill context (Amyn's @aecon.com email, the FBU/M365 references) indicated Aecon was the intended subject. The ambiguity was flagged only in the final report rather than confirmed up front.

**Rule — stop and confirm before starting work:** When ANY task (research, briefing, deck, analysis, partner/competitor scan) names a company that sounds like "Aecon" / "AECOM" / "Aecom":
1. **Check the spelling AND the entity.** "AECOM" (all-caps, American, NYSE: ACM) ≠ "Aecon" (mixed-case, Canadian, TSX: ARE). They are unrelated companies.
2. **If the task involves Amyn's employer**, it is almost certainly **Aecon (Canadian)** — Amyn's email is @aecon.com, his FBU/CMMC work is Aecon. Default to Aecon unless the user explicitly says otherwise.
3. **If the task is a competitor/benchmark scan or names the ticker (ACM, NYSE)**, it may genuinely be the American AECOM — but still confirm.
4. **Ask before researching:** "Quick check — you mean Aecon (Canadian, your employer) or AECOM (American, NYSE: ACM)? They're different companies and often confused." One sentence, then proceed on the answer.
5. **Do not bury the ambiguity in the final report.** Surface it as the FIRST thing, before any tool calls, so the user can redirect cheaply.

Quick disambiguation table (full detail in `references/aecon-vs-aecom.md`):

| | **Aecon** (Amyn's employer) | **AECOM** (different company) |
|---|---|---|
| HQ | Toronto, Canada | Dallas, TX, USA |
| Ticker | TSX: ARE | NYSE: ACM |
| Domain | aecon.com | aecom.com |
| Identity | Canadian construction contractor | American infrastructure consulting (Fortune 500) |
| Notable | CMMC L2 work (Amyn's FBU), Canadian infra | Consigli AI acquisition ($390M, 2025), GSA OASIS+ |
2. Use #E51937 for print/branding, #C8102E for web UI
3. Univers only — no other typefaces
4. Red is an accent — never more than 15% of any layout
5. Teal is decorative only (thin dividers) — never use for text/buttons/backgrounds
6. Canadian English spelling (French for Québec materials)

## Building Self-Contained HTML Deliverables (decks, briefings, reports)

When creating single-file HTML artifacts (no external dependencies, must open in SharePoint/GCC High/email):

### Logo embedding
The logo PNG (9.7KB) can be base64-inlined for true portability:
```python
import base64
with open('/data/nextcloud/data/amyn/files/briefings/aecon-assets/logo-aecon-red.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()
# Use: <img src="data:image/png;base64,{logo_b64}" alt="Aecon">
```

### CSS token block
Copy-ready `:root` design tokens at `templates/aecon-css-tokens.css`. Key values:
- Charcoal `#252525` for headings, dark backgrounds
- Body gray `#464646` for body text
- Red `#E51937` for accent borders, eyebrow labels, key stats
- **WCAG AA contrast gotcha:** `--silver #747679` on light backgrounds is ~3.9:1 — FAILS 4.5:1. Darken to `#64666A` for accessible secondary text.

### Consulting-grade slide deck pattern (scroll-snap, not fixed canvas)
For web-deployable decks (vs projector-only fixed 1920×1080), use scroll-snap:
- `html { scroll-snap-type: y mandatory; }` — makes it feel like a real deck
- Each `.slide { height: 100dvh; scroll-snap-align: start; scroll-snap-stop: always; }`
- `IntersectionObserver` for progress tracking (NOT manual scroll listeners — they're O(n))
- `role="region"` + `aria-label="Slide N of M: Title"` on each slide section
- Fullscreen key (F), overview mode (O), hash routing (`location.hash`)
- Action-titles (full sentences) not topic labels — McKinsey/BCG pattern
- `.takeaway` box with red left-border for "so what" synthesis
- Dark/inverted background reserved for decision slides only

### Eval gate (quality verification before delivery)
Run `references/aecon-deck-eval-gate.py` or the equivalent inline Python checking: tag balance, slide count (14), no emojis, brand colors present (`--web-red`, `--charcoal`, `--body-gray`, `--silver`, `--border-gray`) + old/forbidden colors absent (no `#2A2A2A`, `#FDE8EB`, `#B0B0B0`, `#2D8659`, `rgba(255,255,255,*)`), correct person titles, org relationships (Eric→Brian, Kelly→Ryan, Brian/Ryan both→Enzo), key features (scroll-snap, IntersectionObserver, keyboard nav, fullscreen, overview mode, ARIA roles), self-contained (no external resources beyond data: URLs), body specs (14px, 1.429 line-height, Univers font-family). 31-point reference script at `references/aecon-deck-eval-gate.py`.

### CRITICAL: Read source documents before building
**Pitfall:** Building a deck/report from scratch without reading existing source artifacts (briefings, workbooks, prior versions). This session, an entire deck was built with the wrong narrative ("build an enclave from scratch") when the actual task was "configure FBU SharePoint in the commercial tenant." User had to correct framing THREE times before it was right.

**Rule:** Before building any deliverable that has existing source documents:
1. Read the source briefing/workbook/report FIRST — read the full file, not a skim
2. The deck is a **presentation-layer version** of those docs, not a reimagining
3. Match the content, framing, org relationships, and terminology exactly
4. When user says "it should match what the report says" — they mean it literally
5. Ask the user to confirm framing BEFORE writing any HTML: "This deck is about X, for audience Y, to achieve Z — correct?"
6. When user gives corrections (dates, reporting lines, scope), apply them to the CURRENT slide content, not just acknowledge them — stale content in unedited slides undermines the whole deck

### CRITICAL: Get org reporting lines right
**Pitfall:** Wrong reporting relationships are the #1 correction pattern on Aecon deliverables. Multiple sessions have produced org charts with incorrect lines that the user had to fix.

**Rule:** Before drawing any org chart or listing FBU personnel, load `references/fbu-org-structure.md` for the verified reporting lines. Key facts that have been wrong before:
- Amyn's title is **CICS** (not FCICS)
- **Eric reports to Brian** (not Enzo directly)
- **Kelly reports to Ryan** (not Brian)
- Brian and Ryan are **peers** (both report to Enzo)

### CRITICAL: Design quality bar — the user is a design critic
**Pitfall:** The user has high visual design standards and rejects decks that look like developer-built HTML. Phrases like "looks like shit", "act like a designer", "just follow the aecon brandkit" mean the output fails a BCG/McKinsey presentation bar. This happened across THREE+ slide redesigns — each iteration still missed the mark because I was making incremental CSS patches instead of doing a full brand audit and rebuild.

**Rule:** Before building or deploying any Aecon-branded deck:
1. **Re-read the brandkit HTML** every session — do NOT build from memory. Fetch `https://brief.h.porb.dev/aecon-brandkit.html` or load the skill fresh. Previous-session CSS values drift.
2. **Full rebuild, not patch.** When the user says "just follow the brandkit" after rejecting multiple iterations, the right move is a complete CSS+HTML rebuild from scratch using the brandkit as source of truth — not another round of `patch` calls.
3. **Use #C8102E for web-deployed decks** (web red), NOT #E51937 (logo/print red). The brandkit explicitly separates these.
4. **Body: 14px / line-height 1.429.** Sub-headings can be 15px. These are exact brandkit specs.
5. **No off-brand colors.** Audit for: `#2A2A2A`→`#252525`, `#FDE8EB`→`#FAF9F5`, `#B0B0B0`→`#C0C0C0`, `#2D8659`→remove entirely, any `rgba(255,255,255,*)`→solid hex.
6. **Visual hierarchy per slide.** Cards with numbered red badges, bold titles + lighter descriptions, generous gap/padding. Dense text walls get rejected. Each information unit gets its own card.
7. **Eval gate catches structure, not aesthetics.** After passing 31 checks, ask: "Would I present this at a client meeting?" If no, iterate on spacing, hierarchy, and visual polish before deploying.
8. **When user says "act like a designer"** — they mean: think about whitespace, visual flow, information hierarchy, and brand compliance as a holistic system. Not just "make it pass the eval gate."

### CRITICAL: Know the M365/IT environment before recommending tools
**Pitfall:** Recommending Microsoft 365 features (Copilot, Cowork, AI agents) without understanding Aecon's dual-tenant architecture (commercial + GCC High enclave) and licensing state leads to inaccurate availability assessments.

**Rule:** When any Aecon task involves M365 features, AI tools, Copilot, licensing, or IT procurement, load `references/aecon-m365-environment.md` for the current tenant architecture, Copilot licensing status, IT contacts (Olivia/Joe), CMMC L2 deadline (Nov 2026), and compliance boundary constraints. Key facts:
- FBU uses a **commercial M365 tenant** for day-to-day + a **GCC High enclave** for CUI
- CUI cannot be processed by AI tools outside the GCC High boundary
- Any Copilot feature requires IT license procurement through Olivia Baer / Joe Smith
- GCC High Copilot requires the separate "Copilot for US Government" SKU
- Brian Gregorio (Sr. Director, Federal Compliance) approves compliance tools

### CRITICAL: Incident reporting structure — employees report to Amyn (CICS), but escalation is undefined
**Pitfall:** Deliverables (cheat sheets, SOPs, quick-reference cards) may imply a complete incident response process exists when the FBU's IRP template is entirely unfilled and the readiness scorecard flags IR as "Not Started."

**Rule:** When any Aecon task involves incident response, CUI mishandling, or security reporting instructions, load `references/cui-incident-reporting.md` for the verified reporting structure and IRP gap analysis. Key facts:
- **Employees report to Amyn (CICS)** — this is the correct first point of contact (Amyn holds R/A on all security domains)
- **Amyn does NOT make the DIBNet filing** — DFARS 252.204-7012 requires a director-level officer (Douglas Henderson's role) to file via DIBNet within 72 hours
- **No documented escalation chain exists** — the IRP template is unfilled; all contacts are `[INSERT]`
- **IR is "Not Started" on readiness scorecard** — Amyn's job includes "Crisis management for breaches," confirming this is his to build
- **For deliverables** — instruction "Report to Amyn" is correct for the employee-facing step. Do not list Douglas, Brian, or other FBU staff as contacts (Amyn-only rule applies)

### Large HTML file construction (write_file truncation)
`write_file` and `patch` can truncate on files >35KB. For large self-contained HTML decks (200KB+ with base64 logos):
- Build CSS + slides in separate Python string variables via `execute_code`
- Use `__LOGO__` placeholder, replace with base64 at the end
- Assemble `head + slides + footer` in one final write
- Validate with eval gate script (tag balance, slide count, content checks)

### Org charts in HTML decks
For organizational charts inside slide decks, use CSS Grid with pseudo-element connectors — NOT flexbox with thin divs. The flexbox approach breaks when VPs have different numbers of reports. See `references/css-grid-org-chart.md` for the verified pattern (6-column grid, explicit rows, `::before`/`::after` connectors at `#B0B0B0`).

Before drawing any FBU org chart, load `references/fbu-org-structure.md` for verified reporting lines (Eric→Brian, Kelly→Ryan, Amyn=CICS not FCICS).

### Dark backgrounds: use charcoal (#252525), never arbitrary grays
**Pitfall:** Using `#2A2A2A` or any gray other than `#252525` for dark slide backgrounds is NOT brand-compliant. The brand's single dark color is charcoal `#252525`. All dark-background slides (title, closing, dark decision slides) must use `background: var(--charcoal)` — not `#2A2A2A`, `#333`, or any other custom value.

**Dark-background text conventions** (consistent, brand-aligned):
- Primary text (h1, strong): `var(--white)` `#FFFFFF`
- Secondary/subtitle text: `#C0C0C0` (brand `--c0-silver`)
- Metadata/labels: `var(--mid-gray)` `#707070`
- Code/footnotes: `var(--silver)` `#747679`
- Box borders on dark: `var(--mid-gray)` `#707070`

### Safari rgba rendering bug — use solid hex only
**Pitfall:** Safari renders `rgba(255,255,255,0.08)` or any low-opacity white overlay as completely invisible. The alpha channel blending works differently than Chrome/Firefox. On dark backgrounds, text using `color: rgba(255,255,255,0.85)` appears as unreadable gray-on-charcoal.

**Rule:** NEVER use `rgba(255,255,255,*)` for text on dark backgrounds. Always use solid hex values:
- Instead of `rgba(255,255,255,0.9)` → use `#E0E0E0` or `#C0C0C0`
- Instead of `rgba(255,255,255,0.6)` → use `#999` or `var(--silver)`
- Instead of `rgba(255,255,255,0.12)` for borders → use `var(--mid-gray)` `#707070`

This applies to ALL text, borders, and background overlays on charcoal slides, not just the title/closing slides.

### Brand colors: no arbitrary substitutes
**Pitfall:** The brand kit defines exactly 12 colors. Using anything outside that range (green `#2D8659`, arbitrary grays `#B0B0B0`, pink `#FDE8EB`, non-charcoal dark grays `#2A2A2A`) breaks brand consistency.

**Connector lines** (org charts, timelines) should use `var(--c0-silver)` `#C0C0C0` — the brand's UI gray for form fieldset borders — NOT `#B0B0B0` or similar arbitrary values.

**Non-brand colors to never use:**
- `#2D8659` (green) — not in brand palette
- `#B0B0B0` (connector gray) — use `#C0C0C0` instead
- `#FDE8EB` (pink tint) — not in brand palette
- `#2A2A2A` (near-charcoal) — use `#252525` instead
- `#2D8659` (checkmark green) — use charcoal text or web red instead

### Full design audit workflow
Before delivering any Aecon-branded HTML deliverable, run this systematic audit:

1. **Load the brandkit** — `skill_view(name='aecon-brand-system')` or fetch `https://brief.h.porb.dev/aecon-brandkit.html`
2. **Compare point by point:**
   - Color palette: verify every hex value in the deliverable matches a brand color (list: `--web-red #C8102E`, `--logo-red #E51937`, `--charcoal #252525`, `--body-gray #464646`, `--silver #747679`, `--mid-gray #707070`, `--border-gray #EAEAEA`, `--c0-silver #C0C0C0`, `--teal #7DC4CC`, `--white #FFFFFF`, `--black #000000`, `--ivory #FAF9F5`)
   - No non-brand colors present (check for `#2A2A2A`, `#333`, `#FDE8EB`, `#B0B0B0`, `#2D8659`, `#555`, `#888`, `#999`, `#CCC`, `#DDD`)
   - No `rgba(255,255,255,*)` values
   - Backgrounds: all white or ivory (#FAF9F5) for content, charcoal for bookend slides
   - Typography: Univers font-family, negative letter-spacing on headings, body 14px/1.429
   - Red usage: accent only (<15%), never body text or large background fills
3. **Flag every discrepancy** as a concrete issue, not a vague observation
4. **Fix each issue** in the deliverable
5. **Run eval gate** (`references/aecon-deck-eval-gate.py` pattern)
6. **For page consolidations** (N pages → fewer): run programmatic gap analysis — extract all text via `pdftotext`, check every content element from the original is present. See `references/pdf-production-workflow.md` → "Programmatic gap analysis after consolidation".
7. **Deploy and verify** (copy to Nextcloud briefings, scan files, verify URL loads)

### CRITICAL: Attribution — no Hermes/agent mentions, Amyn is the author
**Pitfall:** Aecon deliverables are handoff-ready artifacts for the FBU team. They carry Amyn's name as author. Any mention of Hermes, AI agents, "auto-generated," or tooling attribution undermines Amyn's credibility and positioning inside Aecon.

**Rule:** All Aecon-branded deliverables (briefings, cheat sheets, decks, reports, transcripts, compliance docs) must:
1. Be attributed to **Amyn Porbanderwala** with his current title (**CICS** — Controlled Information Compliance Specialist)
2. Contain **zero references** to Hermes, AI agents, "auto-generated by," tool names, or automated pipelines
3. Use neutral footer language like "Prepared by Amyn Porbanderwala, CICS" — never "Generated by..." or "AI-assisted"
4. The `auto-pill` badge in html-effectiveness templates should say something neutral (e.g., "Internal Reference") or be removed entirely for Aecon deliverables — NOT "AI-Generated"

### CRITICAL: Single-voice deliverable — no editorial parentheticals or development history

**Pitfall:** Including editorial parentheticals like "(reduced: Amyn no longer in-line, fewer flows to configure)," "(Updated after Justin's review)," "(per Mark Payne's recommendation)," version comparisons like "not the 4-person list originally proposed" or "Per C3PAO assessor feedback," and any other internal development commentary in a deliverable meant for stakeholder review.

**Rule:** All Aecon deliverables (technical designs, proposals, briefings, cheat sheets) must read as a clean, single-voice professional document — never as a changelog or development artifact. Specifically:

1. **No parenthetical asides** — remove ALL `(reduced: ...)`, `(per Mark)`, `(Updated: ...)`, `(now ... total with ...)` parentheticals
2. **No version comparisons** — never reference "originally proposed," "from the previous version," "v1.0 had...," "not the 4-person list" — the current version is the only version that exists
3. **No internal attribution** — never say "Per C3PAO assessor feedback," "Per Justin's review," "Per the user's correction" — the deliverable presents final facts, not how they were arrived at
4. **No self-evaluation** — never say "This is a genuine improvement," "better than the original," "improved from FAIL" — let the content speak for itself
5. **No development process artifacts** — remove `[INSERT]`, `[confirm]`, `[TBD]`, draft markers, version badges ("v2.0"), and inline TODO notes before delivery
6. **Strip before delivery** — after all adversarial reviews and fixes are applied, do a final pass to remove ALL editorial artifacts before publishing. The adversarial review process is for BUILDING the document; it should not be VISIBLE in the document

This applies regardless of whether the deliverable uses Aecon brand kit CSS or html-effectiveness styling. The rule is about voice and polish, not visual branding.

### CRITICAL: Contact routing — Amyn only, never Brian or other FBU staff
**Pitfall:** Listing Brian Gregorio or other FBU staff as contact points in deliverables. The user explicitly directed: "do not reach out to Brian — reach out to Amyn only."

**Rule:** All Aecon-branded deliverables (cheat sheets, briefings, compliance docs, quick-reference cards, incident response steps) must list **Amyn Porbanderwala (aporbanderwala@aecon.com)** as the sole contact. Never Brian Gregorio, never other FBU staff. This applies to:
- Decision tree "Unsure: Ask" branches
- Incident response reporting steps
- Quick-reference "Who to contact" cards
- Footer attribution
- Any "contact compliance" reference

### CRITICAL: CSS ::before bullet markers overlap text at small print sizes
**Pitfall:** When using CSS `::before` pseudo-elements for custom bullet markers (✓, ×, !, –) on `<li>` elements in print-first HTML, `padding-left: 11px` is INSUFFICIENT at 9px font size. The marker renders on top of the first letter of each line, creating the visual illusion that first letters are colored differently (an accidental acrostic like "SEPSDAD"). This happened THREE times in a single session across three fix iterations — the user had to send screenshots each time before it was properly fixed. The HTML source looked clean (no spans, no first-letter CSS), but the `::before` content was positioned at `left: 0` / `left: 2px` with only `padding-left: 11px`, and at 9px the glyph width + positioning consumed most of that padding.

**Rule:** For ANY `::before` bullet marker in print-first HTML:
1. Use `padding-left: 16px` minimum (not 11px) on the `<li>` element
2. Position the marker at `left: 2px` (not `left: 0`)
3. After generating the PDF, **render at 300 DPI and vision-inspect the bullet alignment specifically** — do not assume the HTML preview matches the print output
4. Verify by reading the first 3 list items verbatim in the vision check — if the vision model reads the marker letter as part of the word, the spacing is still wrong
5. This applies to ALL `::before` markers in print contexts: `.b-in li::before` (✓), `.b-wn li::before` (×), `.rc li::before` (–), `.io-col li::before`, etc.
6. **Do NOT use red `!` as a bullet marker** — at small print sizes it visually merges with adjacent text and looks like punctuation. Use charcoal `×` for prohibited items and charcoal `✓` for required items.

### CRITICAL: HTML-to-PDF — print-first design + mandatory visual QA loop
**Pitfall:** Building an HTML page designed for screen viewing (large fonts, wide max-width, scroll layout) and running it through `--print-to-pdf` as an afterthought. The result has oversized text, broken pagination, orphaned pages, missing colors, clipped content. The user explicitly rejected this as a process failure: "you built an HTML briefing and then you saved it to PDF and you did not visually inspect it afterwards."

**Rule:** When the deliverable is a PDF cheat sheet, briefing, or report:
1. **Design for print from the start** — `@page { margin: 0.5in }`, print font sizes (9-10px body, 7-8px cards), `page-break-inside: avoid` on all discrete components, `-webkit-print-color-adjust: exact` on every colored element.
2. **The full quality loop is mandatory:** plan → build → deploy → generate PDF → **render every page to PNG at 200+ DPI → visually inspect each page via vision_analyze → measure page fill ratios → gap analysis → fix → re-inspect → report.** Never ship a PDF without visually verifying every page.
3. **Page fill ratios** — every page should be 70-95% filled. Under 50% = orphan page (tighten preceding content). Over 95% = overflow risk. Use the PIL pixel-scan script in the reference to measure.
4. **Use 200+ DPI for vision inspection** — lower resolutions cause vision models to hallucinate rendering glitches. Cross-check vision claims with `pdftotext` extraction (ground truth).
5. **Page count optimization** — if N+1 pages with an orphan last page: remove forced page breaks, tighten padding (8px→6px), compress lists, shrink card grids, reduce footer margin. See reference for the ordered technique list.

Full technique (CSS patterns, visual QA pipeline, page optimization) in `references/pdf-production-workflow.md`.

Quick command:
```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/path/to/output.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "https://brief.h.porb.dev/filename.html"
```

### Word .docx Generation (editable deliverables)

When the user needs an editable format (vs a fixed PDF/HTML), generate a `.docx` with `python-docx`. This is what M365 shops expect — Word desktop/online compatible, exports to PDF natively.

**CRITICAL — no nested tables:** `cell.add_table()` (tables inside table cells for side-by-side layouts) causes Word to silently inflate a 2-page document to 4+ pages. The user caught this directly. Flatten ALL table structures: side-by-side sections use borderless 2-column layout tables, decision trees use a single multi-column table, quick-reference cards use a 2×3 grid.

**Template script:** `templates/build_aecon_docx.py` — copy and modify for any Aecon .docx deliverable. Includes all helper functions (shading, borders, cell margins, red badges, header blocks).

**Full patterns (cell margins, borderless layouts, selective borders, font sizes, pitfalls):** `references/docx-generation.md`.

**Quick specs for Word .docx:**
- Font: Arial (Univers not installed on most systems — user can switch locally)
- Body: 8.5-9pt, line-spacing 1.05, space_before/after = 0pt (override Word's 8pt default)
- Table headers: 7.5-8pt bold white on charcoal `#252525`
- Cell margins: 1-2pt top/bottom (20-40 twips, not Word's default 5pt)
- Margins: 0.4" top/bottom, 0.5" left/right
- Logo: embed from physical file path (not URL), width 1.1"

### Interactive BPMN workflow visualizations

When building interactive process diagrams (swimlanes, state diagrams, SLA escalation, clickable detail panels), load `references/interactive-bpmn-swimlane-pattern.md` for the complete CSS/JS architecture. Covers: 7-lane swimlane layout, BPMN decision diamonds, role-based color coding, view filter controls, clickable node detail panels, state transition diagrams, and SLA timeline visualization. Reference implementation: `fcs-process-flows-v3-interactive.html`.

### CRITICAL: Stale in-line approver references — full document sweep after role changes

**Pitfall:** When a role is removed from a workflow (e.g., Amyn removed from in-line access approval chain), stale references persist across the document. The primary diagram gets updated, but derivative artifacts don't. This session, Amyn's role was removed from the swimlane but references survived in: list schemas (Filled By: Amyn on CitizenshipStatus and NDAStatus columns), flow step descriptions, state diagram entries, decision tree labels, permission model entries, JavaScript nodeDetail data, quick-reference approval chains, build estimate notes, and SharePoint view filters (`[AmynVerification]=[Me]`). Each stale reference was discovered one at a time across 8+ fix rounds.

**Rule — full document sweep after any role change:**
1. After removing a role from a workflow diagram, do a full-text search for the role name across the entire document
2. Check EVERY section: list schemas (filled-by column), flow descriptions (step text), state diagrams (status names), decision trees (branch labels), detail panel JavaScript (owner/trigger/fields/rules), quick-reference tables, permission models, build estimates, view filters, indexed column lists
3. Not just the person's name — check title variants (FCICS, CICS), email variants, and column names (AmynVerification)
4. If the role moves from in-line approver to exception handler, update ALL instances — don't just change the diagram and assume the rest follows
5. Run a second full-text sweep AFTER all fixes are applied to confirm zero stale references remain
6. This applies to any deliverable with embedded data: HTML briefings, technical designs, proposals, cheat sheets, SOPs

### Multi-agent persona workflow (user-requested pattern)

When the user asks for "agents with different personas, then a judge agent, loop through":

1. **Fan out 3 leaf agents via `delegate_task`**: Research agent (investigate context), Drafting agent (produce the deliverable text), Judge agent (evaluate against criteria).
2. **Pass the draft IN the judge's context** — not as a file path. The judge agent needs the actual content inline.
3. **Pitfall:** The judge agent may search the filesystem for the draft instead of evaluating content provided in its context. When dispatching, explicitly include the draft text in the judge's `goal` or `context` field: "Evaluate this draft: [paste full text]". Do NOT tell it to "find the section in the workspace."
4. **For deliverable QA (user standard):** After building any deliverable, dispatch a judge agent to evaluate it against quality criteria using browser tools. The user explicitly wants this loop — it's not optional when they ask for "judge the final output."
5. **Judge agents catch what builders miss.** In practice, a judge agent caught green `#2D8659` on 10 elements — a documented brand violation the builder agent had introduced and not caught across multiple iterations. The judge approach works because it reads the brand rules fresh without the builder's assumptions.

### Full methodology reference
`references/html-slide-deck-methodology.md` — complete research findings on HTML slide deck frameworks, CSS patterns, accessibility, performance, and consulting-firm design patterns.

`references/html-to-pdf-generation.md` — headless Chrome PDF generation pattern with print-specific CSS, verification steps, and the deploy-to-PDF pipeline.
