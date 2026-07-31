# Emergency DOCX Text Extraction via ZIP

When standard tools (python-docx, mammoth, markitdown, pandoc) are unavailable
or slow, DOCX text can be extracted via its ZIP structure.

## Method

A DOCX file is a ZIP archive containing `word/document.xml`. Extract the XML
and strip tags for clean text:

```bash
unzip -p file.docx word/document.xml | python3 -c "
import sys, re
xml = sys.stdin.read()
text = re.sub(r'<[^>]+>', ' ', xml)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:50000])
"
```

## When to Use

- `uvx markitdown` is cold-starting slowly (>10s) and you need text now
- No pip/uv available (CI sandbox, minimal container)
- The DOCX is corrupted and standard tools fail
- Quick keyword scan before deciding which tool to invest in
- The files are in Nextcloud and you can't install packages there

## What You Lose

- **Tables:** cells are concatenated with spaces; no row/column structure
- **Lists:** numbering and bullets are stripped
- **Formatting:** bold, italic, fonts, colors — all stripped with XML tags
- **Headers/footers:** in separate XML files (`word/header1.xml`, etc.)
- **Images:** not extracted (binary data in `word/media/`)

## What You Keep

- ~100% of body paragraph text
- Reading order (paragraphs remain in sequence)
- Unicode and special characters (XML entities are decoded by the parser)

## Verification

Check the first 1000 chars for sensible sentence flow. XML encoding errors can
produce concatenated garbage. Typical output: a 50 KB DOCX yields 20-40 KB of
clean text.

## Cross-Check

If the output seems wrong or truncated, verify with the file size ratio:
```bash
echo "scale=2; $(wc -c < output.txt) * 100 / $(wc -c < file.docx)" | bc
# Should be 30-80% for a text-heavy DOCX; <10% means extraction failed
```
