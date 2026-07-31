# Font-to-Page-Count Estimation for Federal Submissions

## Why This Matters
Federal NOFOs often specify non-standard fonts and sizes (e.g., 15pt Open Sans for DOS). Standard word-count intuition breaks down at large font sizes — a page holds far fewer words than you expect. This reference provides estimation tables for common federal submission specs.

## Estimation Table

| Font | Size | Spacing | Paper | Margins | Words/Page (Prose) | Words/Page (Mixed) | Notes |
|------|------|---------|-------|---------|---------------------|---------------------|-------|
| Open Sans | 15pt | Single | Letter 8.5×11" | 1" | ~300–340 | ~240–280 | DOS NOFO standard. Mixed = with headers, tables, bullets |
| Calibri | 12pt | Single | Letter 8.5×11" | 1" | ~450–500 | ~380–420 | DOS budget narrative standard |
| Times New Roman | 12pt | Double | Letter 8.5×11" | 1" | ~250 | ~220 | NIH/NSF grant standard |
| Times New Roman | 11pt | Single | Letter 8.5×11" | 1" | ~500–550 | ~430–480 | Common DoD proposal format |
| Arial | 11pt | Single | Letter 8.5×11" | 1" | ~480–520 | ~400–450 | Common civilian agency format |

## Methodology
- **Prose (dense text):** Pure paragraphs, no section breaks, no bullet points, no tables.
- **Mixed (typical proposal):** Section headers at font size, bulleted lists (indented, less efficient horizontal space), occasional tables, short paragraphs with spacing.

For "Mixed" estimates, assume ~75-80% packing efficiency vs. dense prose due to formatting overhead.

## 15pt Open Sans — Detailed Breakdown
At 15pt Open Sans, single-spaced, 1" margins on US Letter:
- Average characters per line: ~55–62 (Open Sans is slightly condensed)
- Average words per line: ~8–10
- Lines per page: ~32–36 (assuming ~18–20pt effective line height with single spacing)
- Pure prose: ~290–340 words/page

With section headers, bullet lists, spacing, and tables (typical proposal density):
- ~240–280 words per effective page

**Target word count for a 20-page proposal at 15pt Open Sans: ~5,200–5,800 words.**

## The Trim Workflow
1. Write first draft without worrying about length (will typically be 2x target)
2. Count words → estimate pages → calculate overshoot
3. Trim in passes: cut redundant language → tighten activity descriptions → shorten bios → compress schedule → final compliance check
4. Target the LOW end of the range. It's easier to add back substance than to cut from an already-tight document.
5. After trimming, always verify no mandatory sections lost content.

## When Converting to Word (.docx)
- Word's "Single" line spacing at 15pt produces ~33 lines/page
- Word defaults to 8pt spacing after paragraphs — adds ~0.5 lines per paragraph break
- Tables at 15pt are very space-inefficient (fewer columns fit, cells wrap frequently)
- Headers at 15pt bold consume ~2.5 lines of vertical space each
- Final page count in Word may differ ±10% from estimation; always do a test render for submissions where page count is a hard gate