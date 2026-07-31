# Print-to-PDF for Scroll-Snap HTML Decks

The print CSS pattern that converts scroll-snap slide decks to clean landscape PDFs. Discovered through iteration: 16 slides became 18, then 24, then 27, then back to 16 pages.

## The Pattern (Copy-Paste Ready)

```css
@media print {
  @page { size: landscape; margin: 0; }
  body { scroll-snap-type: none; }
  .slide {
    break-after: page;
    break-inside: avoid;
    height: 100vh;
    min-height: 100vh;
    overflow: hidden;
    scroll-snap-align: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 28px 52px;
    font-size: 13px;
  }
  .slide:last-child { break-after: avoid; }
  .nav-hint { display: none; }

  /* Reposition sticky footer into flow */
  .slide-footer {
    position: relative;
    bottom: auto;
    left: auto;
    right: auto;
    margin-top: auto;
    padding-top: 16px;
  }

  /* Compress for landscape fit */
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

## Why Each Rule Matters

| Rule | Without It |
|------|-----------|
| `@page { size: landscape }` | Portrait PDF cuts off slide sides |
| `height: 100vh` + `overflow: hidden` | Content spills across multiple pages |
| `break-after: page` on `.slide` | Multiple slides render on one page |
| `break-inside: avoid` | Single slide splits mid-content |
| `scroll-snap-type: none` on body | Browser applies scroll snapping in print |
| Footer `position: relative` | Sticky footer overlaps bottom content |
| Font compression | Bottom content (takeaway boxes) gets clipped |

## Failed Approaches (Do Not Use)

- `height: auto` with `overflow: visible` → 27 pages from 16 slides
- `page-break-after: always` without `overflow: hidden` → 24 pages (internal breaks)
- No font compression → takeaway box clipped on content-heavy slides

## Generation Command

```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --print-to-pdf="/path/to/output.pdf" \
  --print-to-pdf-no-header --no-pdf-header-footer \
  "https://brief.h.porb.dev/filename.html"
```

## QA Steps

```bash
# Render to PNG
pdftoppm -png -r 150 output.pdf /tmp/qa/slide

# Verify: page count equals slide count
ls /tmp/qa/slide-*.png | wc -l

# Spot-check: title slide, content-heavy slide, closing slide
# Use vision_analyze on /tmp/qa/slide-01.png, slide-07.png, slide-16.png
```
