# 2-Page, 2-Column NDA Compression CSS

Tested range: **7.5pt → 11pt body all fit on 2 Letter pages** with appropriate CSS tuning. The final approved version uses **11pt Georgia body** with all elements scaled proportionally. Both constraints are hard — 2-column layout and 2 pages, no exceptions.

**CRITICAL: Proportional font scaling.** When you change the body font size, you MUST scale ALL other font sizes proportionally. Changing only body while leaving headers/labels/footer at their old sizes creates a broken hierarchy. The user will flag it immediately: "review ALL the different text sizes. the doc doesn't look right."

## Approved 11pt Proportional CSS (v7 — final)

No HARBOR branding header. No DRAFT watermark. Replace the entire `<style>` block:

```css
  @page { size: letter; margin: 0.45in 0.45in 0.4in 0.45in; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.06;
    color: #1e293b;
  }
  @media screen {
    html { background: #e5e5e5; }
    body { background:#fff; max-width: 7.5in; margin: 0.4in auto; padding: 0.45in; box-shadow:0 4px 20px rgba(0,0,0,0.1); }
  }

  .title {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 15pt;
    font-weight: 700;
    text-align: center;
    text-transform: uppercase;
    color: #0f172a;
    letter-spacing: 0.5px;
    margin-bottom: 5pt;
    column-span: all;
  }
  .date-line {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 11pt;
    margin-bottom: 4pt;
    column-span: all;
  }
  .parties {
    margin-bottom: 5pt;
    padding-bottom: 4pt;
    border-bottom: 0.75px solid #cbd5e1;
    column-span: all;
  }
  .parties p { margin-bottom: 1.5pt; font-size: 11pt; }
  .parties .label {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-weight: 700;
    font-size: 10pt;
    color: #0f172a;
  }
  .body-columns {
    column-count: 2;
    column-gap: 16pt;
    column-rule: 0.5px solid #e2e8f0;
  }
  .section { break-inside: avoid; margin-bottom: 4pt; }
  .section h2 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 10.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1.5pt;
    padding-bottom: 1pt;
    border-bottom: 0.5px solid #e2e8f0;
  }
  .section p { margin-bottom: 1.5pt; text-align: justify; }
  .section ol, .section ul { margin-left: 11pt; margin-bottom: 1.5pt; }
  .section li { margin-bottom: 0.5pt; text-align: justify; }
  .signatures {
    margin-top: 8pt;
    padding-top: 5pt;
    border-top: 1.5px solid #1e293b;
    display: flex;
    justify-content: space-between;
    gap: 22pt;
    page-break-inside: avoid;
    column-span: all;
  }
  .sig-block { flex: 1; }
  .sig-name {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-weight: 700;
    font-size: 10.5pt;
    margin-bottom: 12pt;
  }
  .sig-line { border-bottom: 0.75px solid #1e293b; height: 14pt; margin-bottom: 2pt; }
  .sig-label {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.6px;
  }
  .sig-detail {
    margin-top: 4pt;
    font-size: 9pt;
  }
  .footer-text {
    margin-top: 6pt;
    padding-top: 3pt;
    border-top: 0.75px solid #cbd5e1;
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 7.5pt;
    color: #94a3b8;
    text-align: center;
    letter-spacing: 0.3px;
    column-span: all;
  }
```

## Proportional Scaling Table

When adjusting font sizes, scale ALL elements together. The ratios relative to body are:

| Element | Size | Ratio to Body |
|---|---|---|
| Body | 11pt | 1.00× |
| Title | 15pt | 1.36× |
| Date / parties text | 11pt | 1.00× |
| Party labels | 10pt | 0.91× |
| Section h2 | 10.5pt | 0.95× |
| Sig names | 10.5pt | 0.95× |
| Sig details | 9pt | 0.82× |
| Sig labels / footer | 7.5pt | 0.68× |

**Compression levers** (in priority order, when pushing to fit 2 pages):
1. Reduce line-height (1.06 → 1.04 → 1.02)
2. Reduce margins (0.45" → 0.4")
3. Reduce title size (15pt → 14pt)
4. As last resort: drop body to 10.5pt or 10pt

**Never:** switch to single column, cut legal text, go below 9pt body, or scale fonts independently.

## Key Design Decisions

- **No HARBOR branding header** — the `.header` / `.brand` / `.brand-sub` block was removed per user preference. The document starts with the title.
- **No DRAFT watermark** — removed. The watermark CSS + div should be omitted entirely.
- **2-column layout is mandatory** — user explicitly rejected single-column. Body flows in 2 columns via `.body-columns`. Title, parties, signatures, and footer use `column-span: all`.
- **Section 7.b (counterparty business description)** must be general/high-level (~1 line), never a detailed service catalog.

## Cache-Busting PDF Delivery

Browsers cache PDFs aggressively. When you regenerate a PDF that the user already loaded, they'll see the old version. Solution: use versioned filenames.

```bash
# After each PDF regeneration:
cp output.pdf /data/nextcloud/data/amyn/files/briefings/<base>-v<N>.pdf
```

Deliver the versioned link: `https://brief.h.porb.dev/<base>-v7.pdf`

## Verification

```bash
chromium --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=output.pdf input.html
pdfinfo output.pdf | grep Pages
# Must return: Pages:           2
```
