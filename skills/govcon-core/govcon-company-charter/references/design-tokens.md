# Design Tokens — HARBOR Company Charter / Capability Statement

## Web HTML (ivory/clay/slate aesthetic)

```css
:root {
  --ivory:  #FAF9F5;
  --paper:  #FFFFFF;
  --slate:  #141413;
  --clay:   #D97757;
  --clay-d: #B85C3E;
  --oat:    #E3DACC;
  --olive:  #788C5D;
  --g100:   #F0EEE6;
  --g200:   #E6E3DA;
  --g300:   #D1CFC5;
  --g500:   #87867F;
  --g700:   #3D3D3A;
  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
}
body {
  background: var(--ivory);
  color: var(--slate);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.6;
}
```

## Print HTML (for PDF generation)

```css
@page {
  size: letter;
  margin: 0.75in 0.85in 0.9in 0.85in;
  @bottom-center {
    content: "ENTITY NAME · Company Charter vX.X · Month YYYY · Page " counter(page);
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 8pt;
    color: #87867F;
  }
}
body {
  background: white;  /* pure white for print, not ivory */
  font-size: 10pt;
  line-height: 1.55;
}
```

## Key Layout Patterns

### Summary strip (web only)
```css
.summary-strip {
  display: grid;
  grid-template-columns: repeat(5,1fr);
  border: 1.5px solid var(--g300);
  border-radius: 12px;
  background: var(--paper);
}
```

### Persona grid (two-column)
```css
.persona-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
.persona-card.technical { border-top: 4px solid var(--clay); }
.persona-card.strategic { border-top: 4px solid var(--olive); }
```

### Past performance table (tight year column)
```css
table.pp-table td:first-child { width: 80px; }
```

### Tight sections (for final pages)
```css
section.tight { margin-bottom: 12pt; }
section.tight td { padding: 5pt 10pt; }
section.tight .callout { margin: 6pt 0; padding: 6pt 12pt; }
```

## PDF Generation Command

```bash
chromium --headless --disable-gpu --no-sandbox \
  --print-to-pdf="OUTPUT.pdf" \
  --no-pdf-header-footer \
  "https://brief.h.porb.dev/FILE.html"
```

Verify with: `pdfinfo OUTPUT.pdf` (pages, page size) and `pdftotext -f 13 -l 14 OUTPUT.pdf -` (spot-check last pages).
