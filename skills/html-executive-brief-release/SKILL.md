---
name: html-executive-brief-release
description: Produce and verify a fixed two-page Letter executive brief from HTML
  through tagged PDF and PNG release artifacts
---

# HTML Executive Brief Release

Use this workflow when an HTML document must become an authoritative, fixed two-page US Letter PDF with page previews.

## 1. Lock the release contract

- Keep HTML as the editable source and PDF as authoritative.
- Define the exact basename and expected four files: HTML, PDF, page-1 PNG, page-2 PNG.
- Lock copy, source URLs, typography floors, and prohibited language before fit tuning.
- Remove only stale generated outputs matching the release basename; never delete the source HTML.

## 2. Preflight in the mounted browser

1. Open the local HTML once in the mounted browser at `816×1056` CSS pixels.
2. Emulate print media.
3. Wait for `document.fonts.ready` and every image load/error event.
4. Require exactly two page containers, each `816×1056`.
5. Check both page-level overflow and every constrained module:
   - page children;
   - exhibits;
   - sidebars;
   - proof rails;
   - notes;
   - fixed grid/flex cells.

A page can report no overflow while a fixed-height child clips text. Compare `scrollWidth/scrollHeight` against `clientWidth/clientHeight` for modules too.

## 3. Tune fit without weakening content

- Preserve locked copy, hierarchy, and type floors.
- Prefer measured spacing, padding, and row/column allocation changes.
- Recheck every affected module after each change.
- Do not blindly restore initial design geometry if runtime measurements prove it clips locked content.
- For review feedback proposing geometry changes, apply the values temporarily in the browser and report the resulting client/scroll dimensions before editing source.

## 4. Render the PDF

Use browser `page.pdf()` with:

- `printBackground: true`;
- `preferCSSPageSize: true`;
- `format: "Letter"`;
- zero margins when page CSS owns margins.

Render only after font/image and overflow checks pass.

## 5. Verify the PDF contract

Run `pdfinfo` and require:

- `Pages: 2`;
- `Page size: 612 x 792 pts (letter)`;
- `Tagged: yes`;
- `Encrypted: no`.

Extract text with `pdftotext` and inspect page order, required copy, exact statistics, and caveats. Use semantic DOM order as the tagged-PDF source of truth when visual multi-column extraction interleaves nearby blocks.

### Critical literal wrapping

If an exact qualifier fails only because PDF extraction inserts whitespace at a line break—especially after a hyphen—wrap the exact phrase in a small `white-space: nowrap` span. Rerender and re-extract. Do not loosen the literal check or alter approved wording.

## 6. Raster and inspect

Raster at 144 DPI with `pdftoppm`.

Require exactly:

- page 1 PNG: `1224×1584`;
- page 2 PNG: `1224×1584`;
- no third page image.

Inspect each page at full size for clipping, overlaps, weak contrast, awkward wraps, and footer/source fit. Also inspect reduced thumbnails for 30-second hierarchy.

## 7. Verify links and accessibility

- Compare literal HTML `href` targets to the approved source ledger.
- Exercise every unique public URL; use browser fallback when static reads are blocked by site mechanics.
- Run `pdfinfo -url` and require all expected external targets; duplicate annotations from wrapped links are acceptable.
- Confirm semantic headings, figure descriptions/captions, decorative-image treatment, named links, document language/title, and contrast.
- Exercise keyboard Tab order under screen media and require visible focus on every link; ensure the skip link becomes visible and reaches a real target.

## 8. Release only the exact artifact set

Confirm the basename matches exactly four release files and rerun metadata, raster dimensions, copy/statistics, confidentiality, and link checks after the final source edit.
