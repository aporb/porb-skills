---
name: aecon-pptx-spec-tables
description: "Use python-pptx native tables for spec-table-heavy PPTX slides (5+ rows). pptxgenjs shape-per-row tables corrupt positioning beyond 5 rows. Switch tooling mid-deck to keep layout slides in pptxgenjs and table slides in python-pptx."
category: govcon
---

# Aecon PPTX: Spec Tables with python-pptx

## Problem

Building a specification table (label/value rows) in pptxgenjs using individual shapes per row — a background rectangle, a label text box, and a value text box — creates 3 shapes per row. For a 2-column, 11-row table, that is ~70+ shapes on one slide. This overloads both LibreOffice and PowerPoint: all shapes snap to x=0 and text collapses into an illegible stack.

This was observed with a real Aecon deck (2026-07-22) on slide 7 (Standard Tier spec table) and slide 8 (Field & Engineering specs). Both had to be rebuilt using python-pptx native tables.

## Solution

Use python-pptx `add_table()` for any slide that is primarily a spec table with 5+ rows. The native PowerPoint table element renders reliably at any row count.

## Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def set_cell(table, row, col, text, bold=False, size=Pt(8), color=RGBColor(0x46,0x46,0x46), bg=None):
    cell = table.cell(row, col)
    cell.text = ""
    run = cell.text_frame.paragraphs[0].add_run()
    run.text = text; run.font.size = size; run.font.bold = bold; run.font.color.rgb = color
    cell.margin_left = Emu(45720); cell.margin_right = Emu(45720)
    cell.margin_top = Emu(22860); cell.margin_bottom = Emu(22860)
    if bg: cell.fill.solid(); cell.fill.fore_color.rgb = bg
    cell.vertical_anchor = 1

def build_spec_table(slide, specs, x, y, label_w=Inches(1.35), val_w=Inches(2.85)):
    """specs = [(label, value), ...]"""
    tbl = slide.shapes.add_table(len(specs), 2, x, y, label_w + val_w, Inches(0.34 * len(specs))).table
    tbl.columns[0].width = label_w
    tbl.columns[1].width = val_w
    ivory = RGBColor(0xFA, 0xF9, 0xF5)
    white = RGBColor(0xFF, 0xFF, 0xFF)
    charcoal = RGBColor(0x25, 0x25, 0x25)
    for i, (label, val) in enumerate(specs):
        bg = ivory if i % 2 == 0 else white
        set_cell(tbl, i, 0, label, bold=True, size=Pt(8), color=charcoal, bg=bg)
        set_cell(tbl, i, 1, val, bold=False, size=Pt(8), bg=bg)
```

## Usage Pattern

- Keep pptxgenjs for layout slides: title, summary cards, stat callouts, timelines, banners
- Switch to python-pptx for any slide that is primarily a spec table with 5+ rows
- Use the python-pptx add_textbox() for column headers and notes on table slides
- Call python-pptx on the saved pptxgenjs output file to rebuild corrupted tables in-place

## Verification

```bash
soffice --headless --convert-to pdf --outdir /tmp deck.pptx
pdftoppm -jpeg -r 150 /tmp/deck.pdf /tmp/slide
ls /tmp/slide-*.jpg | head -10  # visually inspect
python3 -c "from pptx import Presentation; p=Presentation('deck.pptx'); print(len(p.slides), 'slides')"
```

## Known Risks

- python-pptx `add_picture()` raises `UnidentifiedImageError` for SVG/EMF — don't use it for vector art
- python-pptx cannot duplicate a slide (its only entry point is `add_slide(layout)`) — delete-and-rebuild is the pattern
- Removing all shapes from a slide and repopulating it works but the slide retains its original layout reference (harmless for content slides)
