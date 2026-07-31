# Markdown to DOCX Conversion for Federal Proposals

Converts markdown artifacts to properly formatted Word documents for federal proposal submissions.

## Format Requirements (Department of State)

| Element | Specification |
|---------|---------------|
| Narrative font | 15pt Open Sans |
| Budget font | Calibri 12pt |
| Margins | 1 inch all sides |
| Paper | 8.5 × 11 inches (letter, NOT legal) |
| Spacing | Single-spaced |
| Page numbers | All pages numbered |

## Conversion Script

The script at `~/govcon_research/leatherneck-pipeline/dfop/convert_to_docx.py` handles:
- Markdown paragraphs → Word paragraphs with correct font/size
- Markdown headings (##, ###) → Word headings
- Markdown tables → Word tables with proper borders
- Bold (**text**) and italic (*text*) inline formatting
- Bullet lists (- item) → Word bullet lists

### Usage

```python
from convert_to_docx import create_docx

# For narrative docs (15pt Open Sans)
create_docx('input.md', 'output.docx', body_font='Open Sans', body_size=15, table_font='Calibri', table_size=10)

# For budget docs (Calibri 12pt throughout)
create_docx('input.md', 'output.docx', body_font='Calibri', body_size=12, table_font='Calibri', table_size=10)
```

### After Conversion
- Verify page counts: open in Word, check narrative is ≤20 pages, SOW is ≤2 pages
- Verify font rendering: Open Sans must be installed or Word will fall back to Calibri
- Verify table formatting: merged cells and column widths may need manual adjustment
- Verify margins are 1 inch on all sides

## Common Issues

- **"Size: None" in font:** The Normal style may not inherit font size correctly. Fix: set `style.font.size = Pt(body_size)` explicitly.
- **Tables too wide:** Reduce table_font size (8-10pt for large tables at 15pt body).
- **SOW exceeds 2 pages:** Strip Inputs/Outputs/Indicators sub-structure. Collapse to single-line bullets per activity.
- **Budget tables misaligned:** Calibri 10pt for detailed budget tables fits on letter paper with ~90 columns.