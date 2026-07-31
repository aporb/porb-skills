# Word .docx Generation (python-docx)

When the user needs an editable deliverable (not a fixed PDF/HTML), generate a `.docx` with `python-docx`. This is the format for M365 shops — Word desktop and Word Online compatible, exports to PDF natively.

## CRITICAL: Never Nest Tables Inside Table Cells

**Pitfall:** python-docx allows `cell.add_table()` (tables inside table cells) for side-by-side layouts. Word's renderer adds ~5pt padding per nesting level AND treats each nested table as an independent layout context. A 2-page document silently becomes 4 pages. The user saw this directly and flagged it.

**Rule:** Flatten ALL table structures:
- Side-by-side sections → single 2-column borderless layout table, content goes directly in cells
- Decision trees → single multi-row × multi-column table (Question | No | Yes columns)
- Quick-reference cards → single 2×3 grid table (not 6 separate boxes)
- NO tables inside table cells, ever

## Cell Margin Control (Critical for Dense Layouts)

Word's default cell margins are ~5pt (100 twips) top/bottom. For dense cheat-sheet-style layouts, override to 1-2pt:

```python
def set_margins(cell, top=20, bottom=20, left=40, right=40):
    """Set cell margins in twips (1 twip = 1/20 pt). 20 twips = 1pt."""
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:tcMar {nsdecls("w")}>'
                  f'<w:top w:w="{top}" w:type="dxa"/>'
                  f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                  f'<w:left w:w="{left}" w:type="dxa"/>'
                  f'<w:right w:w="{right}" w:type="dxa"/>'
                  '</w:tcMar>')
    )
```

## Borderless Layout Tables

For side-by-side sections, use a 2-column table with borders explicitly disabled:

```python
def no_borders(cell):
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                  '<w:top w:val="none" w:sz="0"/>'
                  '<w:bottom w:val="none" w:sz="0"/>'
                  '<w:left w:val="none" w:sz="0"/>'
                  '<w:right w:val="none" w:sz="0"/>'
                  '</w:tcBorders>')
    )
```

## Cell Background Shading

```python
def shade(cell, hex_color):
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    )
```

## Selective Cell Borders (for callout boxes with red left border)

```python
def borders(cell, color="E0E0E0", sz="4", sides="all"):
    opts = {'top': f'<w:top w:val="single" w:sz="{sz}" w:color="{color}"/>',
            'bottom': f'<w:bottom w:val="single" w:sz="{sz}" w:color="{color}"/>',
            'left': f'<w:left w:val="single" w:sz="{sz}" w:color="{color}"/>',
            'right': f'<w:right w:val="single" w:sz="{sz}" w:color="{color}"/>'}
    if sides == 'all':
        parts = list(opts.values())
    else:
        parts = [opts[x] for x in sides.split(',')]
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:tcBorders {nsdecls("w")}>{"".join(parts)}</w:tcBorders>'))
```

## Red Section Badge (Number in Red Square)

```python
def badge(p, num):
    r = p.add_run(f' {num} ')
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    r.font.name = 'Arial'
    r._element.get_or_add_rPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:fill="E51937"/>'))
```

## Logo Embedding

```python
# Physical file path required (not URL)
run = paragraph.add_run()
run.add_picture('/data/nextcloud/data/amyn/files/briefings/aecon-assets/logo-aecon-red.png',
                width=Inches(1.1))
```

## Page Setup for 2-Page Target

```python
for s in doc.sections:
    s.top_margin = Inches(0.4)
    s.bottom_margin = Inches(0.4)
    s.left_margin = Inches(0.5)
    s.right_margin = Inches(0.5)

# Default style
ns = doc.styles['Normal']
ns.font.name = 'Arial'  # Univers not installed on most systems
ns.font.size = Pt(9)
ns.paragraph_format.space_before = Pt(0)
ns.paragraph_format.space_after = Pt(0)
ns.paragraph_format.line_spacing = 1.05
```

## Font Sizes for Word (Tighter Than Web)

| Element | Size |
|---------|------|
| Section heading | 11-13pt bold |
| Body text | 8.5-9pt |
| Table headers | 7.5-8pt bold white on charcoal |
| Table data | 8-8.5pt |
| Quick-ref cards | 8-8.5pt |
| Footer/metadata | 8pt |

## Paragraph Spacing Helper

```python
def para(container, space_before=0, space_after=0):
    """Add paragraph with tight spacing — Word defaults to 8pt after."""
    p = container.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    return p
```

## Deployment

Same as HTML briefings — copy to Nextcloud briefings folder, scan, deploy:

```bash
sg www-data -c "chmod 644 /data/nextcloud/data/amyn/files/briefings/Filename.docx"
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"
# URL: https://brief.h.porb.dev/Filename.docx
```

## Common Pitfalls

1. **Nested tables bloat page count** — never put a table inside a table cell
2. **Word adds 8pt space_after by default** — always override to 0-2pt
3. **Borders need explicit XML per cell** — Word doesn't inherit table-level borders reliably
4. **Arial not Univers** — Word on most systems doesn't have Univers LT Pro installed; use Arial as fallback. The user can switch to Univers on their machine if licensed.
5. **python-docx functions don't persist across execute_code calls** — write the full build script to a file and run it, don't try to define helpers in one execute_code call and use them in another
6. **Page break**: `doc.add_page_break()` works reliably in Word (unlike CSS page-break-after)
