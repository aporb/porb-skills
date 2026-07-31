# HTML-to-PDF Generation (Headless Chrome)

## When to Use
When an Aecon deliverable (or any html-effectiveness briefing) needs PDF output alongside the HTML version.

## CRITICAL: This is a print-first design task, not a web page that prints

**Pitfall:** The #1 failure mode is building an HTML page designed for screen viewing (large fonts, wide max-width, scroll-based layout) and then running it through headless Chrome `--print-to-pdf` as an afterthought. The result has oversized text, broken pagination, orphaned pages, missing background colors, and content clipped at margins. The user explicitly rejected this approach and called it out as a process failure.

**Rule:** When the deliverable is a PDF cheat sheet, briefing, or report:
1. Design for print FROM THE START — `@page` rules, print font sizes, `page-break-inside: avoid`, color-adjust exact.
2. The HTML is a print document that happens to be viewable in a browser, not the reverse.
3. Every page must be visually inspected as a rendered image AFTER PDF generation — never ship blind.
4. The full quality loop is: plan → build → deploy → generate PDF → **render pages to images → visually inspect** → gap analysis vs plan → fix → re-inspect → report.

## Prerequisites
- `google-chrome` (or `chromium`) installed with headless support
- `pdftoppm` (poppler-utils) for rendering PDF pages to PNG for visual inspection
- `pdfinfo` / `pdftotext` (poppler-utils) for metadata and text extraction verification
- HTML file deployed to a URL (e.g., `https://brief.h.porb.dev/filename.html`) or accessible via `file://`

## Print-First CSS (REQUIRED in the HTML source)

### Page setup
```css
@page {
  size: letter portrait;      /* or landscape */
  margin: 0.5in;              /* 0.5" margins for print/readability */
}
```

### Body and layout
```css
@media print {
  body {
    padding: 0;
    font-size: 9.5px;          /* print density — screen 14-15px is too large */
    background: #fff;
  }
  .page, .wrap {
    max-width: 100%;           /* remove screen max-width constraint */
  }
}
```

### Page break control (the most important section)
```css
@media print {
  /* Prevent sections from splitting across pages */
  section { page-break-inside: avoid; break-inside: avoid; }

  /* Prevent individual components from splitting */
  .box, .card, .ref-card, .stat-card,
  .decision-step, .callout, table {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Don't break right after a heading */
  h2, h3 { page-break-after: avoid; break-after: avoid; }

  /* Explicit page break markers */
  .section-break {
    page-break-before: always;
    break-before: page;
  }

  /* Keep grids together (e.g., 3x2 quick-ref card grid) */
  .ref-grid, .quick-ref {
    page-break-inside: avoid;
    break-inside: avoid;
  }
}
```

### Color preservation (backgrounds disappear without this)
```css
@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  /* Dark backgrounds need explicit !important */
  .bluf, .verdict, thead th, .dark-section {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
```

### Screen preview (optional, for browser viewing)
```css
@media screen {
  body {
    max-width: 8in;            /* simulate letter page width */
    margin: 0 auto;
    padding: 0.5in;
    background: #e0e0e0;       /* grey desktop background */
  }
  .page-surface {
    background: #fff;
    box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    padding: 0.5in;
  }
}
```

## Common Print CSS Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Background colors disappear | Chrome strips bg by default in print | `-webkit-print-color-adjust: exact` on every colored element |
| Content clipped at page edges | Screen padding/max-width too large | Reset to `padding: 0; max-width: 100%` in `@media print` |
| Tables/cards split across pages | No break control | `page-break-inside: avoid` on every discrete component |
| Font sizes too large | Screen 14-15px is unreadable dense in print | Shrink to 9-10px body, 7-8px for cards/badges |
| Orphan page with just footer | Content slightly overflows to next page | Tighten margins/padding on preceding sections; reduce font 0.5px; compress list items |
| Last page 90% empty | Forced page break before final section | Remove `section-break` div; let content flow naturally |
| Grid splits across pages (3+3 instead of 6 on one page) | Grid container not marked no-break | Add `page-break-inside: avoid` to the grid container itself |

## PDF Generation Command

```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/data/nextcloud/data/amyn/files/briefings/OutputFile.pdf" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  "https://brief.h.porb.dev/filename.html"
```

### Key flags
- `--headless` — no GUI needed
- `--no-sandbox` — required on Linux without SUID setup
- `--disable-gpu` — avoids GPU process crashes in headless
- `--print-to-pdf="path"` — output file path
- `--print-to-pdf-no-header` — suppresses default Chrome print header (URL, date)
- `--no-pdf-header-footer` — removes both header and footer chrome

## MANDATORY: Visual QA Loop (do NOT skip)

After generating the PDF, you MUST visually inspect every page before reporting completion. This is not optional. The user explicitly corrected this process failure.

### Step 1: Check metadata
```bash
pdfinfo /path/to/output.pdf | grep -E "Pages|Page size|Tagged|File size"
```
Verify: page count is reasonable (4-12), page size is US Letter (612 x 792 pts), tagged=yes.

### Step 2: Render every page to PNG
```bash
mkdir -p /tmp/pdf-inspect && rm -f /tmp/pdf-inspect/*.png
pdftoppm -png -r 200 /path/to/output.pdf /tmp/pdf-inspect/page
```
Use 200+ DPI for inspection — lower resolutions can cause vision models to hallucinate rendering glitches that don't exist in the actual PDF.

### Step 3: Measure page fill ratios
```python
from PIL import Image
for i in range(1, num_pages + 1):
    img = Image.open(f'/tmp/pdf-inspect/page-{i}.png')
    gray = img.convert('L')
    w, h = gray.size
    pixels = gray.load()
    last_y = 0
    for y in range(h):
        for x in range(0, w, 10):
            if pixels[x, y] < 240:
                last_y = y
                break
    pct = (last_y / h) * 100
    print(f'Page {i}: {pct:.1f}% filled')
```

**Fill ratio rules:**
- **70-95%** = healthy. Page is well-utilized without overflow.
- **< 50%** = orphan page problem. Content from the previous page needs to be tightened or redistributed.
- **> 95%** = overflow risk. Content is likely spilling to the next page.

### Step 4: Visually inspect each page
Use `vision_analyze` with `/tmp/pdf-inspect/page-N.png` for each page. Check:
1. Are all design elements rendering? (logos, colored boxes, badges, tables)
2. Is text legible at print font sizes?
3. Are there orphan pages or excessive whitespace?
4. Are page breaks clean (no split cards/tables)?
5. Does the footer/attribution appear on the last page?
6. Is the overall quality at a professional standard?

### Step 5: Verify text extraction and attribution
```bash
# Check text is extractable
pdftotext /path/to/output.pdf - | head -20

# Check no agent/tool references leaked
pdftotext /path/to/output.pdf - | grep -i -c "hermes\|agent\|auto-generated\|AI-generated"
# Should return 0

# Verify author attribution is present
pdftotext /path/to/output.pdf - | grep -i "amyn\|porbanderwala"
```

### Step 6: Fix issues and regenerate
If any page fails inspection:
1. Identify the specific issue (orphan, split table, overflow, missing color)
2. Patch the HTML CSS
3. Redeploy: `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
4. Regenerate PDF
5. Re-render and re-inspect — repeat until all pages pass

**Do NOT report completion until every page has been visually verified.**

## Page Break Distribution Strategy (preventing cross-page bleed)

CSS `page-break-inside: avoid` prevents a single component from splitting, but it does NOT prevent content from overflowing the page boundary and creating a near-empty orphan page. When a multi-section page (e.g., regulatory table + people/access + quick-ref cards) is too tall, you must decide which sections belong on which page.

### Diagnosing the problem
After rendering, check the **last 5 non-empty lines** of each page and the **first 3 of the next**:
```bash
for i in $(seq 1 $pages); do
  echo "=== PAGE $i ==="
  pdftotext -f $i -l $i /path/to/file.pdf - | grep -v "^$" | tail -3
  echo "--- PAGE $((i+1)) ---"
  pdftotext -f $((i+1)) -l $((i+1)) /path/to/file.pdf - | grep -v "^$" | head -3
done
```
If page N ends mid-section and page N+1 starts with the continuation, that's a bleed.

### Fix: redistribute sections, don't just tighten spacing
The instinct is to shrink fonts and padding to squeeze content. This works for small overflows but fails when a page simply has too much content. The real fix is to **move a section to the next page deliberately**:

1. Identify which section is causing the overflow (usually the last major block on the page).
2. Place a `<div style="page-break-before: always; break-before: page;"></div>` BEFORE that section's heading.
3. Remove any existing `section-break` divs that were forcing the wrong content onto the wrong page.
4. Regenerate and re-measure fill ratios — both pages should now be 70-95% filled.

### Common distribution pattern for a 4-page cheat sheet
- **Page 1:** Header, BLUF, decision tree, context/stakes boxes
- **Page 2:** IN vs OUT comparison, systems/services matrix
- **Page 3:** Data classification tables, marking guides, callouts
- **Page 4:** People/access rules, incident response, quick-ref cards, regulatory table, footer

The regulatory table (10 rows) is the most common orphan culprit — it's too tall to share a page with other major sections. Put it last (as a reference appendix on the final page) rather than trying to fit it alongside other content.

### Iterative page tuning loop
1. Generate PDF → measure fill ratios
2. If page N < 50% filled (orphan): content from page N-1 overflowed. Move a section from N-1 to N, or tighten N-1 to pull the orphan back.
3. If page N > 95% filled (overflow): content will spill to N+1. Move the last section on N to N+1.
4. Regenerate → re-measure → repeat until all pages are 70-95%.
5. **Visually confirm** via vision_analyze that page breaks land at logical section boundaries.

## Page Count Optimization

If the PDF has an orphan last page (content spills by a small amount):

### Techniques to collapse N+1 pages to N pages (in order of preference):
1. **Remove forced page breaks** — Replace `<div class="section-break">` with natural flow where possible
2. **Tighten padding** — Reduce card/box padding from 8px to 6px, section margins from 16px to 12px
3. **Compress list items** — Combine related bullets into single lines ("Email CUI to non-enclave addresses or screenshot it")
4. **Shrink card grids** — Reduce card padding, gap, and font size by 0.5px
5. **Inline incident response** — Convert numbered list steps into inline paragraph text
6. **Reduce footer margin** — From 20px to 12px

**Last resort:** Reduce body font from 9.5px to 9px globally. This is visible to the user and should only be done if the content truly doesn't fit.

## Full Pipeline (deploy-to-PDF-to-verified-delivery)

```bash
# 1. Write HTML to Nextcloud briefings folder
# (via write_file to /data/nextcloud/data/amyn/files/briefings/)

# 2. Scan into Nextcloud
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"

# 3. Verify HTML loads
curl -sI https://brief.h.porb.dev/filename.html | head -3

# 4. Generate PDF
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/data/nextcloud/data/amyn/files/briefings/filename.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "https://brief.h.porb.dev/filename.html"

# 5. Scan PDF into Nextcloud
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"

# 6. VISUAL QA (mandatory — do not skip)
pdfinfo /data/nextcloud/data/amyn/files/briefings/filename.pdf | grep -E "Pages|File size"
mkdir -p /tmp/pdf-inspect && rm -f /tmp/pdf-inspect/*.png
pdftoppm -png -r 200 /data/nextcloud/data/amyn/files/briefings/filename.pdf /tmp/pdf-inspect/page
# Then: vision_analyze each page, measure fill ratios, fix issues, regenerate

# 7. Attribution leak check
pdftotext /data/nextcloud/data/amyn/files/briefings/filename.pdf - | grep -i -c "hermes\|agent\|auto-generated"
# Must return 0

# 8. Copy both to repo for version control
cp /data/nextcloud/data/amyn/files/briefings/filename.html ~/repos/aecon-fcs/deliverables/
cp /data/nextcloud/data/amyn/files/briefings/filename.pdf ~/repos/aecon-fcs/deliverables/

# 9. Commit and push
cd ~/repos/aecon-fcs && git add deliverables/filename.* && git commit -m "feat: deliverable name (HTML+PDF)" && git push
```

## Why Not Other Tools

- **wkhtmltopdf** — poor CSS Grid/Flexbox support, renders many modern layouts incorrectly
- **weasyprint** — better CSS support but missing some features (scroll-snap irrelevant for print, but some pseudo-element patterns fail)
- **puppeteer/playwright** — overkill for simple URL-to-PDF; adds Node.js dependency
- **LibreOffice** — rasterizes or mangles HTML CSS entirely

Headless Chrome uses the same Blink rendering engine that displays the HTML in the browser, so what you see is what you get in the PDF.

## Vision Model Inspection Notes

- **Always use 200+ DPI** for vision inspection. At 150 DPI, vision models frequently hallucinate "rendering glitches" or "corrupted graphics" that do not exist in the actual PDF — these are PNG compression artifacts misread as content errors.
- **Cross-check with text extraction.** If a vision model claims content is missing or tables are empty, run `pdftotext -f N -l N` on the specific page to verify the text IS present. Text extraction is ground truth; vision at low DPI is unreliable for detail verification.
- **Vision is good for:** layout assessment, color rendering confirmation, whitespace/orphan detection, overall professional quality rating.
- **Vision is bad at:** reading specific text content at small font sizes, distinguishing table rows at low DPI, accurate rendering glitch detection below 200 DPI.
