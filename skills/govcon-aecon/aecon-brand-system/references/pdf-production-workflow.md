# PDF Production Workflow (Aecon Brand)

## Print-First Design (Not Web-Export)

**Fonts:**
- Body: 9.5px (0.875rem) for readability at US Letter scale
- Tables/cards: 8-8.5px for dense data
- Monospace code: 8px for paths/technical references
- Univers LT Pro fallback (system-ui, Helvetica Neue, Arial, sans-serif)

**Colors:**
- Print uses solid hex values — NO `rgba()` opacity tricks (Safari renders transparent layers incorrectly)
- Dark backgrounds: `#252525` (charcoal) for headers, `#363636` for cards
- Text on dark: `#DDD` for body, `#CCC` for subtitles
- Accent red: `#E51937` (logo/branding), web red `#C8102E` (UI only)
- Ivory backgrounds: `#FAF9F5` for callout boxes with red left border

**Margins:**
- `@page { margin: 0.5in; }` — US Letter with 0.5" all around
- Content constrained to ~716px printable width

**CSS Print Properties:**
- `-webkit-print-color-adjust: exact` on ALL colored elements (headers, tables, callouts, badges)
- `page-break-inside: avoid` on cards, tables, boxes, ref-grids
- `page-break-before: always` to force clean section breaks between pages

## Headless Chrome PDF Generation

**Command:**
```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/path/to/output.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "https://brief.h.porb.dev/document.html"
```

**Key flags:**
- `--print-to-pdf-no-header` — suppresses Chrome's default header (URL, page numbers)
- `--no-pdf-header-footer` — suppresses Chrome's default footer
- HTML should include running headers in `.cover-header` div (mono font, uppercase, letter-spacing)

## Visual Inspection Pipeline

**Never skip visual inspection.** A pass without pdftoppm + vision_analyze is not a pass.

**Workflow:**
1. Generate PDF via headless Chrome
2. Check page count: `pdfinfo output.pdf | grep Pages`
3. Verify each page's content with `pdftotext -f N -l N output.pdf -`
4. Render each page at 200 DPI for inspection:
   ```bash
   pdftoppm -png -r 200 -f N -l N output.pdf page
   ```
5. Measure fill ratios to detect orphans/underfilled pages:
   ```python
   from PIL import Image
   img = Image.open(f'page-N.png')
   gray = img.convert('L')
   # Find last non-white pixel
   last_y = max(y for y in range(h) for x in range(0, w, 10) if gray.load()[x, y] < 240)
   pct = (last_y / h) * 100
   ```
6. Run `vision_analyze()` on each page PNG to verify rendering

**Fill ratio targets:** 70-90% per page. Below 70% = orphan or excessive whitespace. Above 95% = risk of bleed.

**Vision model reliability:** The vision model may hallucinate artifacts at low DPI (150px). Always cross-reference with `pdftotext` extraction before accepting visual claims.

## Page Break Management

**Forced breaks:** Use `<div style="page-break-before: always; break-before: page;"></div>` between logical sections when content doesn't flow naturally.

**No-break protection:**
- Tables: `<table class="no-break">`
- Callout boxes: `<div class="callout no-break">`
- Cards: `<div class="ref-card no-break">`
- Grids: `<div class="ref-grid no-break">`

**Compression tactics when hitting page limits:**
- Convert 2-column layouts to single column (saves 2-4 lines)
- Remove redundant items from lists
- Tighten spacing: `margin-bottom: 6px` → `4px`
- Compress multi-step lists into single paragraph: `1. X. 2. Y. 3. Z.`

### CRITICAL: `page-break-after: always` is silently ignored on overflowing content

**Pitfall:** If a `<div class="page-break">` (with `page-break-after: always`) contains MORE content than fits on one physical page, Chrome **silently ignores the page break** and lets all content flow continuously into subsequent pages. The CSS property only works when the div's content actually fits within one physical page boundary. This caused page 1 content to overflow into page 2's space, defeating the 2-page layout entirely.

**Rule:** Before relying on `page-break-after: always`:
1. Ensure the content BEFORE the break fits within one physical page. Measure fill ratio — if page 1 is >95% filled, the break will fail silently.
2. Use a **standalone breaker div** between two content blocks: `<div style="page-break-before: always; break-before: page;"></div>` placed as a separate element, NOT as a class on a content div. This is more reliable than `page-break-after` on a content div.
3. Test by checking page count AND per-page line counts: `pdftotext -f N -l N` — if page 1 has 200+ lines and page 2 has 15, the break failed.
4. If the break fails, reduce page 1 content (move sections to page 2) until the break fires.

## Multi-Page Consolidation (N pages → fewer pages)

**Technique:** When the user asks to reduce page count (e.g., "bring it down to two pages instead of four"):

1. **Inventory all content sections** across all pages — write a content map.
2. **Redesign from scratch** — don't patch the existing multi-page HTML. Build a fresh layout with 2-column grids throughout to pack more horizontally.
3. **Iterative font scaling loop:**
   - Start at 9.5px body / 8px tables (NOT smaller — 7.5px produces ~50% fill pages = way too sparse)
   - Generate PDF, measure fill ratio per page
   - If pages are <70% filled → scale UP (body +1px, tables +1px, increase padding/gaps)
   - If pages are >90% filled → scale DOWN or move section to other page
   - For 4→2 page consolidation with ~66 content elements: target 10.5px body, 9.5px tables, 0.35in margins
   - Repeat until target pages are 80-85% filled each (both pages should be balanced within 5%)
4. **Balance content between pages** — don't put all dense content on page 1 and leave page 2 sparse. Split by logical groupings (e.g., classification on page 1, rules/reference on page 2).
5. **Run programmatic gap analysis** — see below.

### Programmatic gap analysis after consolidation

After any page consolidation, verify ZERO information loss:

```python
from hermes_tools import terminal
result = terminal(f"pdftotext /path/to/output.pdf -")
text = result["output"].lower()

checks = [
    ("Section name", "expected text fragment"),
    # ... one entry per content element
]
for label, search in checks:
    if search not in text:
        print(f"  MISSING: {label}")
```

**Line-wrapping false negatives:** `pdftotext` inserts `\n` at line breaks, so multi-word phrases that wrap across lines will fail exact match. Before flagging as missing:
- Search for the first 2-3 words only
- Use `grep -i "keyword"` on the raw text to find context
- Check if the words appear on separate lines (normal wrapping, not actual omission)

## Nextcloud Deployment

**Path:** `/data/nextcloud/data/amyn/files/briefings/`

**After writing HTML:**
```bash
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"
```

**User permissions:** User is in `www-data` group; use `sg www-data -c "..."` for file ops in Nextcloud data dirs.

**URL pattern:** `https://brief.h.porb.dev/filename.html` or `.pdf`

## Quality Gate (What Shipped)

**Initial mistake:** Built as web page, exported to PDF without print-first design. User called this out directly.

**Correction cycle:**
1. Redesigned for print (font sizes, margins, color adjustment)
2. Added `-webkit-print-color-adjust: exact` everywhere
3. Implemented visual inspection pipeline (pdftoppm → vision_analyze)
4. Fixed page break issues (regulatory table orphan → moved to end)
5. Verified all 4 pages at 200 DPI before shipping

**HTML rebuild for page consolidation — build from scratch, don't patch:**
When consolidating N pages → fewer pages, don't try to patch the existing HTML. Build a fresh file:
1. Extract logo b64: `grep -o 'data:image/png;base64,[A-Za-z0-9+/=]*' old.html | head -1`
2. Write new HTML via `execute_code` using `LOGO` placeholder string
3. Replace: `html = html.replace("LOGO", logo_b64)`
4. This avoids `write_file` truncation on large HTML (>35KB with embedded base64) and gives full control over the new layout structure

## CSS ::before Bullet Spacing (Print-First)

**Problem:** At 9px print font size, `::before` pseudo-element markers (✓, ×, !, –) overlap the first letter of list item text when `padding-left: 11px` and `left: 0/2px`. This creates accidental acrostic effects (letters appearing colored differently) that the user will flag as bugs.

**Verified fix pattern:**
```css
/* WRONG — marker overlaps text at 9px */
.box li { padding-left: 11px; }
.box li::before { left: 0; }

/* CORRECT — clear separation at 9px */
.box li { padding-left: 16px; }
.box li::before { left: 2px; }
```

**Also:** Never use red `!` as a bullet marker in print — it visually merges with adjacent text. Use charcoal `×` for prohibited items, charcoal `✓` for required items.

## Lessons Learned

1. **Print ≠ web.** A web page printed to PDF is not a print-quality document. Design for the medium.
2. **Visual inspection is mandatory.** Text extraction alone misses rendering artifacts.
3. **Vision model hallucinates.** Cross-check with pdftotext before believing visual claims.
4. **Page breaks require active management.** CSS `page-break-inside: avoid` isn't enough — test with real content.
5. **Forced breaks push content.** When adding forced breaks, verify downstream content still fits on subsequent pages.
6. **`::before` spacing must be verified at print DPI.** The HTML source may look correct but the rendered PDF can show overlaps that only appear at 9px print scale. Always render at 300 DPI and check bullet-to-text separation visually.