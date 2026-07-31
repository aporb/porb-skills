# Print Layout Principles for Sources Sought Responses

## Cover Page Design (Human-Designed, Not AI-Generated)

The cover page is the first thing a CO sees. It should look designed, not templated.

**Typography hierarchy:**
- h1: Georgia 16pt, weight 400. The requirement name — e.g., "Financial Crime Search & Due Diligence Software"
- Subtitle: Georgia 10.5pt. "Sources Sought Response" — NOT a repeat of the h1
- Notice ID: Courier New 9.5pt, color #555. Monospace signals "this is the tracking number"
- Agency line: Georgia 10.5pt. "HHS · ASFR · OMAS Strategic Buying Center — Information Technology"
- Date: Georgia 9.5pt
- Corporate details table: 9pt, left-aligned, no borders. Labels (col 1): weight 700, color #555. Values (col 2): color #333.

**Layout:** padding-top: ~1.8in (adjust for vertical balance). Table: `width: auto; margin: 24pt auto 0;`.

**Anti-pattern:** The requirement name appearing twice — once as h1 and again as a subtitle with nearly the same wording. This is the most common AI-generated cover-page tell. The h1 is the requirement. The subtitle is the document type. They are different things.

**Proportional font scaling:** When shrinking body (e.g., 11pt → 10.5pt), scale h1/h2/h3/cover fonts/table fonts proportionally. Never change only body — it creates broken visual hierarchy. h2 should be ~0.5-1pt larger than body. h1 should be ~5-6pt larger than body.

## When Tables Fail

Tables are for data where each column has comparable content density. They fail when one column has 5-word labels and another has 200-word paragraphs.

### The Failure Pattern
Two-column capability table — left: short label, right: dense paragraph. No column width can fix the inherent asymmetry. Print rendering produces page-height rows with massive empty cells.

### The Replacement Pattern
Replace with structured sections: h3 heading → context paragraph (1-2 sentences showing domain knowledge) → bulleted list (3-4 specific, measurable capabilities). Each capability gets proportional vertical space. KO can scan headings. Prints correctly at any width.

### Decision Rule
- Key-value corporate info, deliverables lists, compliance checklists → Use tables (width: auto, max-width: 100%)
- Capability descriptions, technology differentiators, team bios, past performance → Use structured sections (h3 + p + ul)

### Real Examples
- **Treasury 2032H326N00011:** 2-column table (15-word left / 200-word right, 13:1 ratio) → 6 h3 sections. Same content, 40% less space, scannable.
- **VA SIEM 36C10B26Q0650:** 3-column table (29-char / 170-char / 170-char, 6:1 ratio) → 5 h3 sections. Same improvement.

## PDF Page Count Verification

```bash
google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="/tmp/out.pdf" \
  --no-pdf-header-footer "file:///path/to/final.html"
pdfinfo /tmp/out.pdf | grep -i pages
```

### Page Count Reference (TNR, single-spaced, letter)

Start with the target page count and work backward. For a **5-page Sources Sought (cover + 4 content pages):**

| Format | Font | Line-Height | Margins | ~Words Fit |
|--------|------|-------------|---------|-----------|
| Starting (5-page target) | 11pt | 1.35 | 0.85in | ~1,900 |
| Default (12pt, 1in) | 12pt | 1.55 | 1in | ~1,500 (3 pages) |

At 12pt/1in, word counts: 1,500 ≈ 3 pages | 2,000 ≈ 4 | 2,300 ≈ 4.5 | 2,500 ≈ 5 | 2,800 ≈ 5.5 | 3,200+ ≈ 6+. Tables add ~0.2-0.4 pages each. Cover page does NOT count.

**Prose instead of data tables:** Multi-column data tables (e.g., 3-column API source table with 12 rows) can consume an entire page alone. Replace with prose paragraphs when the data doesn't need side-by-side comparison. Reserve tables for key-value corporate info, pricing, and compliance checklists — things the CO scans for specific fields.

### Tightening Sequence (apply in order until within limit)
1. line-height: 1.15 → 1.12
2. body font: 11pt → 10.5pt
3. h3 font: 11pt → 10.5pt
4. bio text: 10.5pt → 10pt
5. Reduce h2/h3/p margins 20-30%
6. li font-size: 10.5pt → 10.25pt
7. Shrink cover page padding + font sizes
8. Condense closing: bullets → prose, multi-line POC → single line with · separators
9. Remove explicit page-break-before divs
10. Eliminate duplicate bios (Section 4 repeats Section 2)
11. Last resort: drop deliverables table, state as prose
