---
name: two-page-html-pdf-release
description: Build and verify a fixed two-page US Letter HTML brief with tagged PDF,
  PNG previews, live links, and deterministic fit checks
---

# Two-page HTML → PDF release workflow

Use this for polished proposal briefs or leave-behinds that must ship as editable HTML, an authoritative two-page PDF, and one PNG per page.

## 1. Define the print contract

- Use `@page { size: Letter; margin: 0; }`.
- Make each `.page` exactly `8.5in × 11in`, `box-sizing:border-box`, and `overflow:hidden`.
- At 96 CSS px/in, each page must measure `816×1056` CSS pixels.
- Use a page break after page 1 and none after page 2.
- Keep DOM order identical to intended PDF reading order.
- Treat the PDF as authoritative; external font/image dependencies may remain in editable HTML only if the generated PDF and PNGs are self-contained.

## 2. Preflight in `xd://browser`

Open the local HTML once with viewport `816×1056`, then run Puppeteer code that:

1. Calls `page.emulateMediaType("print")`.
2. Awaits `document.fonts.ready`.
3. Awaits every image's load/error state.
4. Requires exactly two `.page` elements.
5. Requires each page rectangle to be exactly `816×1056`.
6. Requires `scrollWidth <= clientWidth` and `scrollHeight <= clientHeight` for each page.
7. Requires every approved image to have `complete && naturalWidth > 0`.
8. Generates the PDF only after those assertions pass:

```js
await page.pdf({
  path: "/absolute/path/output.pdf",
  printBackground: true,
  preferCSSPageSize: true,
  format: "Letter",
  margin: { top: "0in", right: "0in", bottom: "0in", left: "0in" },
});
```

If a web font fails, switch to the specified system fallback and rerun dimensions without changing copy or type sizes. If an approved image fails, fetch that exact asset once and embed it as a data URI; do not substitute an unapproved image.

## 3. Verify the PDF contract

```bash
/opt/homebrew/bin/pdfinfo output.pdf
```

Require:

- `Pages: 2`
- `Page size: 612 x 792 pts (letter)`
- `Tagged: yes`
- `Encrypted: no`

## 4. Generate page previews

Delete only stale previews for this output, then rasterize:

```bash
/opt/homebrew/bin/pdftoppm -png -r 144 output.pdf output-page
```

Require exactly:

- `output-page-1.png`
- `output-page-2.png`

Each must be `1224×1584` pixels. A third image is a pagination failure.

Inspect both pages at full size for clipping, overlap, broken glyphs, awkward wraps, orphan headings, invisible rules, and text touching frames. Inspect both together at thumbnail scale to confirm the intended 30-second scan hierarchy.

## 5. Verify text and links

```bash
/opt/homebrew/bin/pdftotext output.pdf /tmp/output.txt
/opt/homebrew/bin/pdfinfo -url output.pdf
```

- Read extracted text top-to-bottom; require the intended page and module order.
- Assert each approved literal appears in both HTML and extracted PDF text after whitespace normalization.
- Assert exact public statistics have the intended occurrence counts in both outputs.
- Run an extended-regex confidentiality/unsupported-claim denylist against both outputs.
- Compare `pdfinfo -url` targets with the expected external URL set; duplicates are acceptable, missing targets are not.

## 6. Fix fit deterministically

If two-page fit fails, tighten only pre-approved vertical whitespace in a fixed order, for example:

1. Module row gaps.
2. Exhibit padding.
3. Page top/bottom padding.

Set explicit floors before implementation. Never cut approved copy, change hierarchy, create a third page, or shrink body/caption/note type below those floors merely to force fit.

## 7. Release gate

Release only when all four artifacts exist and every check passes:

1. Editable HTML
2. Authoritative two-page PDF
3. Page 1 PNG
4. Page 2 PNG
