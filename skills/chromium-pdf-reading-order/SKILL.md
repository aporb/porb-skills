---
name: chromium-pdf-reading-order
description: Preserve approved multi-column HTML-to-PDF layouts while fixing Chromium/Poppler
  text extraction order and link annotations
---

# Chromium PDF Reading-Order Repair

Use this only when all of these are true:

- Chromium `page.pdf()` is the required renderer.
- The approved design contains columns or independently positioned modules.
- The rendered pixels are correct.
- Default `pdftotext` crosses module boundaries or extracts later modules too early.
- Replacing the columns with stacked content is not an acceptable design change.

This is a last-resort print-layer technique. First try semantic DOM order and ordinary CSS layout.

## 1. Prove the defect

Render the PDF with the approved visual layout. Extract with default Poppler behavior, not `-raw` or `-layout`:

```sh
pdftotext output.pdf /tmp/output.txt
```

Define ordered anchor strings for each page and assert that every anchor is present and its index is strictly increasing. Keep a rasterized visual baseline.

## 2. Isolate only the problematic visual modules

In `@media print`, apply a no-op filter to the modules whose glyph geometry confuses Poppler:

```css
@media print {
  .opening-columns,
  .proof-rail,
  .closing,
  .notes {
    filter: brightness(1);
  }
}
```

Chromium preserves the visual paint but no longer emits those module glyphs as ordinary extractable text. Do not filter unaffected modules.

## 3. Add canonical print-only text

Keep duplicate canonical copy out of DOM `textContent` by placing it in a data attribute:

```html
<div
  class="print-extraction extraction-opening"
  data-extraction="Exact canonical text in intended reading order."
></div>
```

```css
.print-extraction { display: none; }

@media print {
  .print-extraction {
    position: absolute;
    left: 0.52in;
    z-index: 30;
    display: block;
    width: 7.46in;
    color: rgba(255, 255, 255, 0.001);
    font: 400 1pt/1 Arial, sans-serif;
    letter-spacing: 0;
    white-space: normal;
    pointer-events: none;
  }

  .print-extraction::before {
    content: attr(data-extraction);
  }
}
```

Position one layer at the vertical start of each filtered module so default extraction encounters it between the preceding and following modules.

Important:

- Do not use `aria-hidden` on the canonical print layer; otherwise Chromium may omit it from the PDF tag tree.
- Keep it `display:none` in screen media, so browser accessibility and word counts do not duplicate content.
- `rgba(..., 0.001)` may serialize through computed style as alpha zero, yet Chromium can still emit extractable text. Always verify the actual PDF.
- If source-level invariant checks count exact literals, HTML-encode punctuation in the canonical attribute while leaving the visible copy literal. The browser decodes it in the PDF.

## 4. Restore filtered link annotations

A filtered ancestor can suppress its descendants' PDF link annotations. Add empty, print-only overlays matching the original link rectangles:

```html
<a
  class="print-link-overlay"
  href="https://example.com/source"
  aria-label="Source description"
  tabindex="-1"
  style="left:0.70in;top:9.34in;width:3.24in;height:0.25in"
></a>
```

```css
.print-link-overlay { display: none; }

@media print {
  .print-link-overlay {
    position: absolute;
    z-index: 40;
    display: block;
    color: transparent;
    text-decoration: none;
  }
}
```

Measure each original anchor with `getBoundingClientRect()` relative to its fixed-size page. Convert pixels to inches using the browser's 96 px/in CSS scale. Preserve source order between original anchors and overlays.

Do not add `aria-hidden` to overlays. Hidden screen media plus `tabindex=-1` keeps them out of normal browser navigation; leaving them exposed in print lets Chromium associate annotations with PDF Link tags.

## 5. Verify every contract

### Visual geometry

- Exact page dimensions and no overflow.
- Required column counts remain intact via computed `gridTemplateColumns`.
- Rasterize every page and inspect full-size images.
- Render a comparison PDF with `.print-extraction { display:none !important; }` and pixel-diff it against the release raster. Require zero changed pixels when feasible.

### Extraction

- Use default `pdftotext`.
- Assert all page anchors are present and strictly increasing.
- Assert complete required copy and exact statistic counts.
- Confirm the canonical layer matches each visual module's `innerText`; add explicit list numbering where `innerText` omits generated markers.

### Links

- Use `pdfinfo -url` to enumerate external annotations.
- Compare overlay hrefs and rectangles to original links in the browser.
- Require equal counts, exact href matches, and subpixel geometry tolerance.
- Exercise the unique public destinations separately.

### Accessibility

- In screen media, require canonical layers and overlays to be hidden.
- Tab through only the visible links; overlays must never receive focus.
- Require the PDF to be tagged and marked.
- If inspecting the low-level PDF, verify overlay annotation objects have `StructParent` entries and corresponding `/S /Link` structure elements.

### Release integrity

- Regenerate the authoritative PDF and page images after the final source change.
- Re-run metadata, extraction, links, copy, confidentiality, dimensions, and exact-artifact-set checks.

## Failure modes

- `opacity: .999` usually does not change Poppler grouping; `filter: brightness(1)` does.
- Solid white canonical text can erase a few raster pixels where it overlaps visible content. Use near-transparent text and prove pixel neutrality.
- Filtering an entire module without link overlays silently removes clickable PDF links.
- `aria-hidden` on print artifacts can produce a superficially tagged PDF whose corrected text or links are absent from the structure tree.
- Stacking approved columns merely to satisfy extraction is a design regression, not a reading-order fix.
