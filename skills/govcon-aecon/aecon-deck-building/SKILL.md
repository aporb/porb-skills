---
name: aecon-deck-building
description: Build Aecon-branded HTML slide decks in McKinsey/BCG consulting style with scroll-snap, action titles, and Aecon brand compliance. Covers deck structure, stakeholder handling, FCS/Compliance split, print-to-PDF for scroll-snap decks, and white-label delivery.
category: govcon
triggers:
  - Building an Aecon-branded slide deck
  - Converting an Aecon briefing into a presentation
  - McKinsey or BCG style deck request
  - Print-to-PDF for a scroll-snap Aecon deck
  - Making a deck for an Aecon stakeholder
  - Building a PPTX version of an Aecon deck
  - User asks for a .pptx file
---

# Aecon Slide Deck Building

Build Aecon-branded HTML slide decks for internal stakeholders. McKinsey/BCG consulting style: action titles, frameworks over bullet points, clean layouts with Aecon brand colors. Required companion skill: load aecon-brand-system first for brand colors, typography, logo embedding, and the eval gate.

## Deck Structure

Standard deck: 14-16 slides, scroll-snap mandatory, keyboard navigation.

| Slide | Type | Content Pattern |
|-------|------|----------------|
| 1 | Title (dark) | Aecon logo, deck title, subtitle, attribution |
| 2 | Executive Summary | 3 impact cards showing current state gaps |
| 3 | Problem Assessment | 4 impact boxes showing cost per team |
| 4 | Process Overview | 7-stage horizontal process flow with owner badges |
| 5-6 | Deep Dives | Split layout with two or three parallel tracks |
| 7 | Compliance Detail | Table with FAR/DFARS citations |
| 8 | Lifecycle | 3 cards showing operational stages |
| 9 | Design Philosophy | 70/30 split visual |
| 10 | Technical Architecture | Lists plus flows, no-new-tools emphasis |
| 11 | RACI Matrix | Full accountability table with all stakeholders |
| 12 | Implementation Timeline | 4-week milestone timeline with dot and line |
| 13 | Success Metrics | 6 metric tiles with 90-day targets |
| 14 | Decisions Required | 4 leadership questions in cards |
| 15 | Risk Assessment | Risk table with severity and mitigations |
| 16 | Closing (dark) | Next steps and supporting detail reference |

## Stakeholder Handling

### Sinem Matay (Director, IS Vendors and Contracts)
- Zero Amyn attribution. Footer says Prepared for IS Vendors and Contracts, never Amyn's name or email.
- She reports to Jason, VP Technology / de facto CIO. He is the executive sponsor.
- She is corporate Canada IS, NOT in FBU. Do not confuse with FBU personnel.

### FCS and Compliance Are Two Distinct Roles

When building process flows or RACI matrices involving federal governance:

| Role | Entity | What They Own |
|------|--------|---------------|
| Federal Compliance | FBU | SAM.gov, Section 889, FedRAMP, CUI, Cloud SRG, CMMC |
| FCS (Federal Contract Solutions) | US Nuclear | FAR 12/13 path, small business, prime/sub flow-downs, terms review |

- FCS gets its own column in RACI tables and its own card in review-gate slides
- Never merge both under Federal Governance. The split is explicit.
- FCS is under US Nuclear, NOT FBU
- Compliance checklists: separate with a divider row. Six regulatory checks by Compliance above, three contractual checks by FCS below.

### Use Titles, Not Names
- Director of IS Vendors and Contracts (not Sinem)
- VP Technology (not Jason)
- Enclave Technical Team (not Isaiah)
- Federal Compliance (not Brian)
- No specific person names in any deck. The deck is a corporate artifact.

## McKinsey/BCG Style Rules

- Action titles: every slide has a full-sentence heading stating the key takeaway. Not "Process Overview" but "Seven stages. One owner per stage. Defined SLAs. Complete audit trail."
- Red emphasis: use var(--web-red) on the most important 3-5 words per slide
- Frameworks over bullet points: process flows, RACI tables, split layouts, timeline visualizations, metric tiles
- Dark slides only for title (slide 1) and closing (last slide). Charcoal background, white text, red accent.
- Takeaway boxes: red left-border callout at bottom of content slides. Answers "so what?"

## CSS Architecture

```css
html { scroll-snap-type: y mandatory; }
.slide { min-height: 100dvh; scroll-snap-align: start; scroll-snap-stop: always; }
.slide.dark { background: var(--charcoal); }
```

Key components: cards (two, three, four column grids), process-flow with process-step, split layout, raci table, timeline with tl-item, metric-row with metric-tile, takeaway box, impact-box, check-list with red checkmark bullets.

## Print-to-PDF for Scroll-Snap Decks

Scroll-snap decks do NOT paginate cleanly by default. Without print CSS, the browser renders all slides as one continuous page and splits unpredictably. You MUST add @media print CSS.

### The working print pattern (landscape):

```css
@media print {
  @page { size: landscape; margin: 0; }
  body { scroll-snap-type: none; }
  .slide {
    break-after: page; break-inside: avoid;
    height: 100vh; min-height: 100vh;
    overflow: hidden;
    scroll-snap-align: none;
    display: flex; flex-direction: column; justify-content: center;
    padding: 28px 52px;
    font-size: 13px;
  }
  .slide:last-child { break-after: avoid; }
  .nav-hint { display: none; }
  .slide-footer {
    position: relative; bottom: auto; left: auto; right: auto;
    margin-top: auto; padding-top: 16px;
  }
  .slide .action-title { font-size: 26px; }
  .slide .card { padding: 18px 22px; }
  .slide .card h3 { font-size: 15px; }
  .slide .card p, .slide .card li { font-size: 12px; }
  .slide table { font-size: 11px; }
  .slide table thead th { font-size: 9px; }
  .slide table tbody td { padding: 8px 12px; }
  .slide .takeaway { padding: 12px 16px; font-size: 12px; margin-top: 16px; }
  .slide .process-step { padding: 16px 12px; }
  .slide .process-step .step-name { font-size: 11px; }
  .slide .process-step .step-owner { font-size: 9px; }
  .slide .metric-tile { padding: 18px; }
  .slide .metric-tile .metric-num { font-size: 30px; }
  .slide .metric-tile .metric-label { font-size: 11px; }
  .slide .impact-box .num { font-size: 28px; }
  .slide .impact-box .label { font-size: 11px; }
}
```

### Print iteration pitfalls observed in production:
- height:auto with overflow:visible causes slides to spill across pages (27 pages from 16 slides)
- page-break-after:always without overflow:hidden causes internal breaks within slides (24 pages)
- break-after:page with fixed height:100vh plus overflow:hidden is correct (16 pages)
- Content-heavy slides (tables, RACI) need font compression. Without it, the bottom takeaway box gets clipped.
- Always render to PNG and visually inspect after PDF generation. Use pdftoppm -png -r 150.

### PDF generation command:
```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/path/to/output.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "https://brief.h.porb.dev/filename.html"
```

### Post-generation QA:
```bash
pdftoppm -png -r 150 output.pdf /tmp/qa/slide
# Verify: page count matches slide count. Spot-check: title, content-heavy, closing slides.
```

## Converting Technical Briefings to Management Decks

When the source material is a comprehensive technical design (e.g., the FCS Access & Clearance Automation HTML briefing), the deck is a **presentation-layer distillation** — not a reimagining. Key rules:

### Audience adaptation
- **Management approval decks need:** impact numbers up front (slide 2), simplified process flows (5 steps max, not 12), clear "decisions required" slide, honest limitations (what it does vs. doesn't do), and a closing slide that makes the ask explicit.
- **Strip technical detail.** The original briefing had 117 SharePoint columns, 8 flow specs, and interactive swimlanes. The deck shows: what it replaces, how the flow works at a glance, what leadership needs to approve. Save the deep detail for the reference document.
- **Use the briefing's own structure as the outline** — the deck mirrors the source's logical flow (Problem → Solution → How It Works → Compliance → RACI → Implementation → Decisions). Don't invent a new structure.

### Standard slide count
14 slides works for management approval. 16 for detailed stakeholder review. Compress adjacent topics if the audience doesn't need the granularity:
- "Deep Dives" (slides 5-6 in the template) → combine into one process overview
- "Design Philosophy" and "Lifecycle" → skip if the deck is about an operational system, not a methodology
- "Success Metrics" → fold into executive summary and closing

### What to preserve from the source
- Role names, org relationships, RACI assignments — match the source exactly
- The "honest answer" about compliance — management decks that over-promise on CMMC get rejected
- Amyn's role clarity — if the source says "Amyn is not an in-line approver," the deck must say the same thing

## PPTX Deck Building (python-pptx)

When the user asks for a PPTX version, use python-pptx with `python3.12` (installed for 3.12, not 3.11). Always check for a reference PPTX first — the user may have provided one as an example. Extract its slide structure before building.

### Check for existing PPTX first
Search the briefings folder for `.pptx` files. If the user drops "here's an example: filename.pptx," load it immediately: `python3.12 -c "from pptx import Presentation; prs=Presentation('file.pptx'); ..."` to extract slide count, sizes, and text patterns. Mimic the reference deck's spacing, card styles, and visual hierarchy.

### Build approach
Write the full build script to `/tmp/build_<name>.py` and run with `python3.12`. Do NOT try to build in execute_code — the sandbox lacks python-pptx. The terminal has it on python3.12 (`pip install --break-system-packages python-pptx` if missing).

### PPTX specs (matching reference deck pattern)
- **Slide size:** 13.333" x 7.5" (widescreen 16:9)
- **Font:** Arial (Univers not available on recipient machines)
- **Colors:** Print red `#E51937` for PPTX (presentation format, not web red #C8102E)
- **Layout:** `prs.slide_layouts[6]` (blank — no built-in placeholders)
- **Dark slides:** `slide.background.fill.fore_color.rgb = CHARCOAL`
- **Cards:** `MSO_SHAPE.ROUNDED_RECTANGLE` with white fill, 1pt border-gray stroke
- **Takeaway box:** Thin red rectangle (0.03" wide) + adjacent textbox
- **RACI cells:** Small rounded rectangles with colored fills (A=charcoal, R=red, C=I=light gray)
- **Process flow:** Rounded rect step cards with red step numbers, centered text, owner badges
- **Timeline:** Oval dots + adjacent text blocks for phases
- **Logo:** `slide.shapes.add_picture(LOGO_PATH, ...)` — embed from file path, not URL

### PPTX helper functions reference
See `templates/build_aecon_pptx.py` in aecon-brand-system for a complete build script with all helpers: `bg()`, `footer()`, `snum()`, `logo()`, `card()`, `takeaway()`, `impact()`, `action_title()`, `step_card()`, `tl_item()`, `raci_cell()`, `arun()`, `tb()`, `rich_tb()`.

### PPTX QA workflow
```bash
soffice --headless --convert-to pdf --outdir /tmp/qa-pptx deck.pptx
pdftoppm -jpeg -r 150 /tmp/qa-pptx/deck.pdf /tmp/qa-pptx/slide
# Visually inspect 4 slides minimum: title, exec summary, one complex (RACI), closing
```

## Pitfalls

- Safari rgba bug: never use rgba(255,255,255,*) on dark slides. Use solid hex: #303030 for dark card backgrounds, #C0C0C0 for secondary text.
- Name leakage: decks are corporate artifacts. Use titles, not names. Verify with grep before delivery.
- Missing FCS split: if a deck mentions federal governance, check whether FCS should be a separate column/card. The user has explicitly corrected this.
- Print without @media print: scroll-snap invisible to PDF engine. Must force break-after:page on each slide.
- Print overflow hidden clips content: if content is too tall, it gets clipped. Fix is font size compression in @media print, not removing overflow.
- AECOM vs Aecon confusion: before any research or brand work, confirm the entity.
- Stale source material: if the deck recycles an older briefing, verify the current briefing is the latest version before building. If the briefing is weeks old, confirm no updates before starting.
- PPTX: Use `python3.12` not `python3` — python-pptx is installed for 3.12 only. Run from terminal, not execute_code.
- PPTX: Check for reference PPTX files in briefings before building. The user may have dropped an example that defines expected structure.
- PPTX: Font is Arial not Univers — Univers is not installed on recipient machines. PPTX embeds font names, and missing fonts fall back poorly.
- PPTX: Print red `#E51937` for PPTX (presentation format), not web red `#C8102E`.
