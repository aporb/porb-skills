---
name: govcon-capabilities-brief
description: Use for a branded 1-2 page GovCon capabilities brief — deliver as browser-viewable HTML flyer or PDF.
tags:
  - govcon
  - capability
  - pdf
  - branding
  - marketing
  - weasyprint
triggers:
  - "capabilities brief"
  - "capabilities brief PDF"
  - "marketing PDF"
  - "2-page brief"
  - "govcon marketing one-pager"
  - "html flyer"
  - "browser-viewable brief"
  - "capabilities brief html"
related_skills:
  - govcon-capability-statement
  - govcon-company-charter
  - govcon-website-build
  - html-briefing
---

# GovCon Capabilities Brief — Short-Form Visual PDF

Build a branded 1-2 page visual capabilities brief PDF for a GovCon firm. This is the **marketing/sales document** — what a prospect receives when they click "Request Capabilities Brief" on the website or when you attach it to a cold email.

## When to Use

- A GovCon firm needs a **single-page or two-page visual PDF** for prospects
- User says "build a capabilities brief PDF" or "create a one-page brief"
- A capabilities brief PDF will accompany a LinkedIn headline banner or be attached to outreach emails
- The output is a **branded, visually-dense** marketing document — not a formal compliance/legal boilerplate

## When NOT to Use

- Formal SAM-registration capability statement with past-performance table and legal register → `govcon-capability-statement`
- Partner-facing NDA corporate document with partner-analysis framework → `govcon-company-charter`
- Full public website build → `govcon-website-build`
- Research briefing or intelligence report → `html-briefing`

## Distinction from Related Documents

| Dimension | Capabilities Brief | Capability Statement | Company Charter |
|-----------|-------------------|---------------------|-----------------|
| Purpose | Sales/marketing | SAM/SourceSought compliance | Partner/teaming evaluation |
| Length | 1-2 pages | 4-6+ pages | 6-10+ pages |
| Past Performance | Stats only (aggregate) | Full table with contract numbers | Full table with verification |
| Branding | Heavy (hero, color blocks) | Professional but restrained | Professional, NDA-partner voice |
| Legal | Minimal (entity status, NAICS) | Full (EIN, UEI, reps/certs) | Full + NDA markings |
| Audience | Prospects, cold outreach | COs, proposal evaluators | Teaming partners under NDA |
| Delivery | PDF attached to email | SAM.gov upload, proposal binder | Direct to partner |

## Pipeline

```
research (live site brand + founder facts) → cross-reference charter/foundational docs → persona review & adversarial check → design layout → build HTML → verify (browser screenshot + vision_analyze) → convert to PDF → deliver
```

### Phase 1: Research Brand from Live Site

Before writing a single line of HTML, extract the actual brand tokens from the firm's **live public website**. Do NOT guess or infer from industry conventions.

```bash
# Scrape branding tokens
curl -sL https://firmwebsite.com | grep -oE 'href="([^"]+\.css[^"]*)"' | head -5
# Then curl each CSS file to find :root / --color-* tokens
```

Alternatively use `firecrawl_scrape(url, formats=["branding"])` for automated extraction.

**Extract these from the live site:**
- Primary color hex values (navy, accent, gold/bronze)
- Font stack (body + display/serif)
- Logo treatment (SVG path, wordmark style)
- Dark vs light mode default
- Section styling patterns (cards, borders, CTAs)

**Common GovCon palettes:**
- **Marine Corps / expeditionary:** scarlet `#CC3333` as accent/action, gold `#C9A227` as data highlight, deep navy `#0D1B2A` for typography
- **Generic federal / defense:** navy `#0A1628` primary, brass/gold accent, ivory ground
- **HARBOR (navy/amber):** blue `#2563EB`, dark bg `#0F172A`, light bg `#F8FAFC`, purple accent `#7C3AED`

### Phase 2: Gather Firm Facts

Research in parallel across:
- Company website (about, capabilities, leadership pages)
- SAM.gov registration (UEI, CAGE, NAICS, entity status)
- LinkedIn (leadership profiles, current employers)
- Internal knowledge base (resumes, prior briefings, pipeline docs)
- GitHub (verify public repo counts if claiming AI/tech capability)

**Yes/no questions to answer:**
- Is the firm SDVOSB or VOSB? (Never claim SDVOSB without a VA disability rating)
- Is it a solo practitioner or multi-person?
- What's the proprietary methodology name and acronym?
- What clearance level does leadership hold (Active Secret, TS/SCI, etc.)?
- What's the total combined years of acquisition experience?

### Phase 2.5: Cross-Reference Charter / Foundational Docs

**Critical step — skip at your peril.** After gathering firm facts but before writing a line of HTML, cross-reference ALL brief claims against the firm's charter, partnership agreements, entity factsheets, and any foundational documents on disk.

**What to look for:**
- Does the brief's entity name, UEI, CAGE match what's in the charter? (OMP and LLMs hallucinate these — verify every identifier against source documents.)
- Are the founding members exactly as named in the charter? Titles correct?
- Does the brief's "proprietary methodology" match what's actually written in the charter?
- Are NAICS codes, entity status (SDVOSB vs VOSB vs small business), and formation date consistent?
- Does every person's past experience trail back to their named role in the charter?

**Workflow:**
1. Search filesystem for charter docs, entity factsheets, partnership agreements over the past 90 days
2. Read the charter analysis if one exists (often a structured HTML briefing)
3. Map each brief assertion to its charter source section; mark assertions with no source as "verify before publish"
4. Check the "Gaps & Risks" section of any charter analysis — those gaps often surface claims that look wrong to evaluators

**Signal that tells you to do this:** You're filling in names, UEI, CAGE, or stat numbers. If you're typing a person's name without checking the charter, you're going to get it wrong.

### Phase 3: Design the Layout

A 1-page brief fits: hero + stats + services + methodology + contact.
A 2-page brief fits: (p1) hero + services + methodology → (p2) leadership + differentiators + NAICS + contact.

**Page 1 structure (full-page color-blocking pattern — preferred):**
1. **Hero band (top 25-30%)** — dark navy `#0D1B2A` with subtle grid-line texture (repeating-linear-gradient). Contains: logo/shield left, UEI/CAGE/badges right, 4 large stat callouts (white numbers, gold labels), serif tagline with gold accent bar.
2. **NAICS pill bar** — thin dark band below hero, lists primary NAICS and entity type (e.g. "SC LLC · NAICS: 541611, 541519...")
3. **Core capabilities (next ~40%)** — ivory `#F7F5F0` background. 3-column card grid. Each card: white background, scarlet top border, gold dot-bulleted list. Section label and title above the grid.
4. **Experience table (next ~18%)** — dark-header table (navy header, gold uppercase mono column titles, alternating white/ivory rows, scarlet-highlighted names). Compact — 5 rows max.
5. **FAR 15.305 note** — italic left-bordered quote acknowledging new entity status ($0 federal prime contracts)
6. **Differentiators (next ~10%)** — 3-column icon cards (SVG inline icons — shield, star, crosshair — in colored circles). Each: short header, 1-line body.
7. **Methodology flow** — 5-step horizontal OORAH flow: letter in scarlet circle → gold connector → next letter. Compact, bottom of page.
8. **Footer (bottom ~5%)** — dark navy `#060F18` band with entity name, address left; phone/email/CTA button right.
9. **Copyright strip** — thin dark strip below footer.

**Page 2 structure (if 2 pages needed):**
1. **Leadership bios** — 2×2 grid. Each: role title, name, short bio (2-3 lines), clearance/cert badges
2. **Differentiators** — 3-column: (1) Operator DNA, (2) AI-Augmented Execution, (3) The OORAH Framework
3. **Capability strip** — horizontal row of badge-pills: platforms (Advana, Databricks, Palantir), compliance (FedRAMP, CMMC, NIST), vehicles (SBIR, GSA, OTAs)
4. **NAICS table** — code | description | status. Compact table
5. **Contact footer** — full entity name, UEI, CAGE, address, phone, email, CTA button (styled link)

### Phase 4: Build the HTML (Single File)

Write a self-contained HTML file. For a 2-pager the file size is small enough for a single `write_file` call — no skeleton+patch pattern needed unless otherwise constrained.

**CSS essentials:**
```css
@page {
  size: letter;
  margin: 0;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Source Sans 3', sans-serif; color: #1a1a1a; }
```

**Font import pattern (Google Fonts):**
```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Rajdhani:wght@400;500;600;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Page sizing — each page is exactly 8.5×11in:**
```css
.page {
  width: 8.5in; height: 11in;
  overflow: hidden;
  position: relative;
}
```

**Key visual patterns:**
- **Full-page color blocking** — the page is divided into 3-4 horizontal color bands that fill the entire 8.5×11 canvas. No floating sections on white space. Typical pattern: dark hero (25%) → ivory content (55%) → dark footer (5%) → thin copyright strip.
- **Grid-line texture on hero** — subtle repeating-linear-gradient pattern over the dark navy background: `background-image: linear-gradient(to right, rgba(gold,0.035) 1px, transparent 1px), linear-gradient(to bottom, rgba(gold,0.035) 1px, transparent 1px); background-size: 44px 44px;`
- **Stat blocks** — oversize white numbers (Rajdhani bold, 17pt) with tiny gold uppercase labels below. 4 across. Separated by thin gold dividers.
- **Capability cards** — white cards on ivory background, 2pt scarlet top border, 0.4pt `#DDD9CE` border, 1.5pt border-radius, subtle shadow (`0 1pt 3pt rgba(13,27,42,0.04)`). Gold dot bullets (2.5pt circle, `#C9A227`).
- **Experience table** — navy header row, gold mono column titles (Rajdhani, 4.2pt, uppercase). Alternating rows: white / `rgba(247,245,240,0.6)`. Person names in scarlet `#CC3333`. Thin `#DDD9CE` 0.4pt borders.
- **Methodology flow** — horizontal flex of 5 elements, each a scarlet stroke circle (1.2pt, `#CC3333`, 14pt diameter, subtle scarlet fill at 5%) with a letter in the center. Gold line `#C9A227` connectors (8pt wide, 0.8pt tall) between circles. Step name in small Rajdhani uppercase below.
- **Differentiator icon cards** — white cards on ivory, 0.4pt border, 14pt circle with icon (SVG inline, 9×9pt, stroke=scarlet or gold), background tinting matching icon color at 6-8% opacity. Short header, 1-line description.
- **Badges** — scarlet pill for SDVOSB (`display: inline-block; background: #CC3333; font-family: Rajdhani; font-size: 5.5pt; letter-spacing: 0.14em; padding: 1.5pt 7pt; border-radius: 1pt`). Small note below for "Self-attested · VetCert Pending" in low-opacity white.
- **FAR note** — 4.2pt italic serif text, left border: 1.5pt solid gold `#C9A227`, background `rgba(201,162,39,0.03)`. Sits between experience table and differentiators.
- **Footer** — dark navy `#0D1B2A` → `#060F18` gradient. Left: company name (Rajdhani bold, gold) + address (low opacity). Right: contact info + scarlet CTA pill ("REQUEST BRIEFING →").
- **Copyright strip** — `#060F18` background, 3.5pt Rajdhani, 0.12em letter-spacing, `rgba(255,255,255,0.25)` color.

**Iron triangle of visual quality (cannot sacrifice any one):**
1. **Full-page coverage** — the page must look cohesive, not like text on a white canvas. Color blocks, background tints, borders, and rules fill space.
2. **Typography hierarchy** — 3 font families: Rajdhani (display/headers/mono labels), Cormorant Garamond (section titles/tagline/serif italic notes), Source Sans 3 (body text). Each has a defined role. No mixing.
3. **Color discipline** — exactly 3 active colors (navy `#0D1B2A` = structure/background, gold `#C9A227` = accent/data highlights, scarlet `#CC3333` = action/exclamation). Never introduce a fourth independent color.

### Phase 4.5: HTML Flyer — Primary Deliverable Path

When the user asks for an **editable, browser-viewable format** (e.g. "give me an HTML flyer", "I want to see it in the browser like printed pages"), the HTML file IS the primary deliverable, not a stepping stone to PDF. Shift your workflow accordingly.

**Deliverable contract:** The HTML file must:
1. **Render like printed pages in a browser** — each page fills an 8.5×11in viewport with embedded CSS. No scrollable endless page. Use `.page` containers with explicit dimensions.
2. **Work when opened as `file://`** — no external dependencies: no CDN fonts, no external CSS, no network requests. Google Fonts `@import` will fail on `file://`. Either inline fonts as `@font-face` data URIs, use system font fallbacks, or use the `brief.h.porb.dev` served path for Google Fonts.
3. **Be fully self-contained** — all CSS inline in `<style>` blocks, all images as inline `<svg>` or data URIs, no `<script>` tags unless needed for print behavior.
4. **Print correctly from the browser** — Ctrl+P / Cmd+P should show each page as expected. Test `@media print` if needed.

**Workflow differences from PDF-first path:**

| Aspect | PDF-First | HTML-Flyer-First |
|--------|-----------|-------------------|
| Primary deliverable | `*.pdf` | `*.html` |
| Font loading | Google Fonts OK (weasyprint downloads) | Must work offline — system fallbacks or embedded data URIs |
| CSS scoping | weasyprint-specific `@page` rules | Browser CSS + `@media print` for print |
| Verification | pdftoppm + vision_analyze | browser_navigate + browser_vision + Ctrl+P print preview |
| Sharing | `brief.h.porb.dev` link to HTML (PDF attached if needed) | `brief.h.porb.dev` link to HTML (user can Ctrl+P → Save as PDF) |
| Editing | User can't edit PDF | User opens HTML in browser, saves, edits source |
| Deployment | Copy both `.html` + `.pdf` to Nextcloud | Copy `.html` to Nextcloud, offer PDF as secondary |

**CSS for `file://` compatibility (critical):**
```css
/* Google Fonts will fail on file:// — provide system fallbacks */
/* On file://, browser uses system fonts; on brief.h.porb.dev, Google Fonts load */
body { font-family: 'Source Sans 3', system-ui, -apple-system, sans-serif; }

/* Page containers for print-like rendering */
.page {
  width: 8.5in; height: 11in;
  overflow: hidden;
  position: relative;
  margin: 0 auto;         /* centering on screen */
  box-shadow: 0 2px 20px rgba(0,0,0,0.1); /* page shadow for screen view */
}

/* Print styles — hide shadows, remove margins */
@media print {
  .page {
    box-shadow: none;
    margin: 0;
    page-break-after: always;
  }
  @page {
    size: letter;
    margin: 0;
  }
  body { margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
```

**Typo-avoidance pattern:** After writing the HTML, grep for common typos before deploying:
```bash
grep -n -i "leathrneck\|leathernck\|leathernecck\|leathernack\|capabilites\|capablities\|principial\|princple\|methedology\|methedolgy\|OORAHH\|OORAAH\|OORRAH\|porbanderawala\|porbandewala\|porbanderwalaa\|ampy\|amyne" /path/to/brief.html
grep -n "Amyn\|Adam\|Douglas\|Henderson\|Probst\|Wurtsfeld" /path/to/brief.html  # check for hallucinated names
```

### Phase 5: Verify — Browser + Vision

**HTML flyer verification (when HTML is primary deliverable):**
1. `browser_navigate` to the HTML (served at `brief.h.porb.dev` or opened as `file:///path/to/file.html`)
2. **Test `file://` compatibility**: open the HTML with `file://` protocol. Fonts should fall back gracefully, no console errors for failed network requests
3. `browser_vision` with `annotate=true` — check each `.page` container renders at correct dimensions, no content overflow or cut-off
4. `browser_console` — should show zero errors. Google Fonts failing on `file://` is expected and OK (check for anything else)
5. Test print: `browser_click` on the page, then evaluate `window.matchMedia('print').matches` — or check that `@media print` rules would apply. If possible, use Ctrl+P preview to verify page breaks
6. **Gallery comparison (mandatory):** Open `~/repos/html-effectiveness/index.html` visually in a real browser. Compare your brief's design against the closest example. If your output has less visual depth, larger margins, or poorer typography, redesign before delivering.

**PDF vision verification (critical — skip only for internal drafts):**
After converting to PDF with weasyprint, render the first page as a PNG and run vision_analyze:

```bash
pdftoppm -png -r 200 -f 1 -l 2 /path/to/brief.pdf /tmp/brief-check
```

Then call `vision_analyze(image_url="/tmp/brief-check-1.png")` with this question:
*"Full design review. Check: (1) Does it fill the entire page with no wasted white space? (2) Is the dark hero section visually striking? (3) Is typography professional and readable? (4) Color palette used consistently? (5) Is layout clean with good visual hierarchy? (6) Any design issues that look cheap/amateur? (7) Does it look like a real GovCon capabilities brief?"*

**Do NOT skip this step.** The vision model catches layout gaps, overflow, font rendering failures, and color issues that browser inspection misses. If the model says the design is weak or amateur, redesign before delivering.

**Checklist — all must pass before delivery:**
- No overflow — each page ends cleanly at 11in
- Fonts load (Google Fonts may fail — test PDF output)
- Color contrast is readable
- No text is cut off
- @page size renders correctly for print
- Vision model says "professional" or "high quality" (not "text dump" or "white page with text")

### Phase 6: Convert to PDF

Use weasyprint, which is installed globally or in the active Python environment:

```python
from weasyprint import HTML
HTML('/path/to/brief.html').write_pdf('/path/to/brief.pdf')
```

If weasyprint fails, try Chromium headless:
```bash
chromium --headless --print-to-pdf=/path/to/brief.pdf --no-pdf-header-footer --disable-gpu file:///path/to/brief.html
```

### Phase 7: Deliver

**HTML-flyer-first path (user wants editable/visible format):**
1. Copy the HTML file(s) to: /data/nextcloud/data/amyn/files/briefings/
2. Sync: `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
3. Share the link: `https://brief.h.porb.dev/<filename>.html`
4. **Send only the link in Discord**, never the file itself
5. If user also wants PDF: produce it separately via weasyprint, copy both to Nextcloud, but refer to the HTML as the editable version
6. **Grep for hallucinated names before sharing:** run `grep -n -i "adam\|probst\|wurtsfeld\|douglas\|henderson\|hallucinated" /path/to/brief.html` before delivery. OMP frequently poisons names.

**PDF-only path (user explicitly asks for PDF):**
1. Copy HTML and PDF to: /data/nextcloud/data/amyn/files/briefings/
2. Sync: `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
3. Also copy to the firm's website `public/` directory if one exists: `cp brief.html ~/repos/<firm-site>/public/`
4. Share the link: `https://brief.h.porb.dev/<filename>.html`
5. **Send only the link in Discord**, never the file itself

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| PDF font rendering fails (weasyprint can't load Google Fonts) | Include `@font-face` fallbacks using system fonts. Test PDF output before declaring done. |
| Page 2 content overflows past 11in | Tighten spacing, reduce font sizes, or trim bio text. Use `height: 11in; overflow: hidden;` and check. |
| Colors don't match live site brand | Extract from the actual site CSS, don't guess from Hallmark or memory. |
| Using googled/imagined stats instead of researched | Every number (years experience, contract value, scope) must come from research. If unverifiable, omit. |
| Leadership doesn't match SAM registration | SAM-registered principals must appear in the brief. If personnel are contractors at another firm, blur the current-employer reference. |
| NAICS category count mismatch | Verify against SAM.gov, don't round up. |
| "SDVOSB" claimed without VA rating | Default to VOSB unless user confirms disability rating. |
| Missing occ files:scan | File won't appear at brief.h.porb.dev without the Nextcloud scan command. |
| No public/ copy for website | If the brief accompanies a "Request Capabilities Brief" button, put a copy in the site's public/ directory. |
| External-facing brief mentions HARBOR or internal entity | LFC is the external face. HARBOR and Amyn are internal delivery. Grep for internal names before delivering. |
| **OMP hallucinates names/identifiers when generating HTML** | omp-generated HTML frequently contains fabricated names, wrong UEI/CAGE, wrong citations (e.g. "Douglas Henderson" became "Adam Probst-Wurtsfeld"). Verify EVERY identifier, person name, and citation against source documents before delivering. Do NOT trust omp's prose even when the structure looks right. |
| **No charter cross-reference before designing** | A brief that hasn't been checked against the firm's charter WILL contain factual errors (wrong titles, wrong past performance, wrong NAICS). Add Phase 2.5 to every brief. |
| **User says "it looks like a text dump on a white background"** | This means the brief lacks color blocking, background textures, typography hierarchy, and full-page coverage. Redesign using the full-page color-blocking pattern in Phase 3. Add a dark hero, colored content sections, and a dark footer. |
| **Missing FAR 15.305 note for new entities** | For firms with $0 federal prime revenue, include a FAR 15.305(a)(2)(iv) citation acknowledging the brief evaluates individual past performance, not entity past performance. Omission looks like you're hiding something. |
| **Skills: no vision_analyze verification after pdf conversion** | The vision model catches visual gaps that browser inspection misses. Always run pdftoppm + vision_analyze on the PDF before declaring done. |
| **HTML flyer viewed as file:// has broken fonts** | Google Fonts @import/link fails on file:// protocol. Either serve via brief.h.porb.dev or provide system font fallbacks in the font-family stack. Test both paths before delivery. |
| **HTML flyer has external CSS/JS dependencies** | User saves HTML and opens on another machine — all external resources break. Everything must be self-contained: inline style, inline svg, data URIs. |
| **HTML flyer renders as endless scroll, not printed pages** | Without .page containers at 8.5x11in, the brief looks like a web page, not a document. Always use explicit .page dimensions with overflow: hidden. |
| **User wanted editable format, delivered PDF** | If user says give me an editable format or HTML flyer, HTML is PRIMARY. PDF is secondary/optional. Ask before producing a PDF if they didnt request it. |
| **OMP hallucinates company names, UEI, CAGE in HTML content** | Grep the output for hallucinated names (grep -n Adam Probst Wurtsfeld Douglas Henderson /path/to/brief.html) before deploying. OMP introduces fabricated data even when the structure is correct. |
