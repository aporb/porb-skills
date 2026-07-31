---
name: ocr-and-documents
description: "Extract text from PDFs, scans, and images — pymupdf, marker-pdf, tesseract, vision API fallback chain."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs, scanned documents, and standalone images**.

## Step 0: Vision API (First Choice for Images)

If the source is a **standalone image** (JPEG/PNG screenshot, photo, social media post), always try `vision_analyze` first:

```
vision_analyze(image_url="/Users/amynporb/screenshot.png", prompt="Extract ALL text verbatim.")
```

If `vision_analyze` is unavailable or returns a rate-limit error (HTTP 429), fall back to Step 0.1.

The ZAI vision tools (`mcp_zai_vision_extract_text_from_screenshot`, `mcp_zai_vision_analyze_image`) have weekly/monthly rate caps — use them sparingly and have a fallback ready.

## Step 0.1: Local Tesseract OCR (Fallback for Images)

**Prerequisite**: `brew install tesseract` (pre-installed on this Mac).

For any image file (screenshot, photo, scanned page not in PDF form):

```bash
# Basic attempt (works on clean screenshots with large text)
tesseract /path/to/image.jpeg stdout --psm 6

# PSM modes: 6=uniform text block, 3=auto (default), 4=single column, 11=sparse text
```

**Image preprocessing** — tesseract performs poorly on raw screenshots with small text, stylized fonts, or low contrast. Preprocessing dramatically improves results:

```python
# Grayscale + contrast + sharpen
from PIL import Image, ImageFilter, ImageEnhance
img = Image.open(source_path)
gray = img.convert('L')
enhancer = ImageEnhance.Contrast(gray)
gray = enhancer.enhance(1.5)
gray = gray.filter(ImageFilter.SHARPEN)
gray.save(output_path)

# Or aggressive binarization for dark-on-light text
gray = img.convert('L')
gray = gray.point(lambda x: 0 if x < 128 else 255, '1')
gray.save(output_path)
```

```bash
# Run tesseract on the preprocessed image
tesseract /path/to/preprocessed.tiff stdout --psm 6
```

**The complete fallback chain for image text extraction:**

1. `vision_analyze(image_url=...)` → success? done
2. `mcp_zai_vision_extract_text_from_screenshot` → success? done
3. Tesseract with preprocessing → success? done
4. Manual extraction / user asks the source

**Pitfall — macOS `/tmp/inspect.py` pollution**: A stale `/private/tmp/inspect.py` (left by a prior script run in `/tmp/`) hijacks Python's `import inspect` and breaks PIL and other packages. If you see `FileNotFoundError` with trajectory.json paths, the fix is:

```bash
rm -f /private/tmp/inspect.py /private/tmp/inspect.pyc
```

Always work in a non-`/tmp` directory (e.g. `~/.hermes/`) or remove the offending file first. If the fix works, the PIL import problem resolves immediately — no pip reinstall needed.

## Step 0.2: Quick Probe for Image-Based PDFs (no install)

Before reaching for heavy tools, a fast `pdftotext` probe tells you whether a local PDF is text-based or a scan:

```bash
# Text-based → pdftotext returns content immediately
pdftotext document.pdf -

# Empty output → likely scanned/image-based (CamScanner, photo, fax)
```

If `pdftotext` returns nothing, the PDF is probably a scanned image. The lightweight fallback chain (no pip installs, works on macOS with poppler-utils):

```bash
# 1. Check page count and scanner provenance
pdfinfo document.pdf | grep -E 'Pages|Author|Producer'

# 2. Compare file sizes — scanned PDFs are larger (972KB for a 2-page scan vs 150KB for a blank text form)
ls -la document.pdf

# 3. Convert target pages to PNG images (page 1 = -f 1 -l 1, page 2 = -f 2 -l 2)
pdftoppm -png -f 1 -l 1 -r 150 document.pdf /tmp/page1

# 4. Read the image with vision
vision_analyze(image_url="/tmp/page1-1.png", question="Describe this page in detail...")
```

**When to use this:** quick document verification (notarization checks, form field inspection, signature presence). For full-text extraction of scanned PDFs, use marker-pdf (Step 2). For text-based PDFs, pdftotext or pymupdf are faster and give machine-readable output.

**Common signal:** CamScanner PDFs (Producer: "iOS Version ... Quartz PDFContext") are always image-based — skip pdftotext and go straight to pdftoppm → vision.

## Step 0.3: PDF Page-by-Page Vision Reading (Multi-Page with Stamps/Handwriting)

When a PDF contains **stamps, seals, handwritten annotations, mixed scripts (e.g. Hindi + English), or low-quality scans** where text extraction (pdftotext, pymupdf text mode) fails or produces garbage, convert each page to a PNG and read it with `vision_analyze` individually.

**This is the correct approach for: Indian legal documents (court filings, stamp papers, notary seals, Aadhaar cards), property records, probate documents, and any government-issued PDF with embossed seals or handwritten entries.**

### Pipeline

```python
import fitz  # pymupdf
doc = fitz.open('document.pdf')
print(f'Pages: {len(doc)}')
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(dpi=200)  # 200 DPI is the sweet spot — legible without huge files
    pix.save(f'/tmp/doc_p{i+1}.png')
    print(f'Saved page {i+1}: {pix.width}x{pix.height}')
doc.close()
```

Then call `vision_analyze` on each page **individually** (not batched):

```
vision_analyze(image_url="/tmp/doc_p1.png", question="Read and transcribe this entire page exactly. Capture all text, names, dates, court references, amounts, legal terms, signatures, stamps, and any handwritten notes.")
```

### Critical Pitfalls

- **Batching all pages in one vision_analyze call causes timeouts.** Each page is a separate call. For a 9-page document, that's 9 calls.
- **Individual pages may still time out** (420s limit on large/dense pages). Retry the failed page individually — it usually succeeds on the second attempt.
- **DPI matters:** 150 DPI produces smaller files but may miss small text in stamps/seals. 200 DPI is the sweet spot. 300 DPI creates very large PNGs that slow down vision processing.
- **pymupdf must be installed:** `pip3 install pymupdf`. The import name is `fitz` (not `pymupdf` or `PyMuPDF`).
- **Mixed-script documents** (Hindi/Devanagari + English): vision models handle these well but may transliterate inconsistently. Cross-reference key names and numbers across pages.
- **Stamps and seals:** Ask the vision model specifically to "describe all stamps, seals, and handwritten annotations" — without this prompt, it may skip them.
- **Aadhaar cards / ID documents embedded in legal PDFs:** These often appear as separate pages with photos, QR codes, and bilingual text. Ask vision to capture the Aadhaar number, name, DOB, and address fields specifically.

### When to Use This vs Other Methods

| Scenario | Best Method |
|----------|-------------|
| Clean text-based PDF | `pdftotext` or `pymupdf` text mode |
| Scanned PDF, English only, clean scan | `marker-pdf` (OCR) |
| PDF with stamps, seals, handwriting, mixed scripts | **This method (page-by-page vision)** |
| Single image (screenshot, photo) | `vision_analyze` directly |
| Remote URL PDF | `web_extract` first |

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
