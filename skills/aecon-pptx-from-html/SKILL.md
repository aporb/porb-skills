---
name: aecon-pptx-from-html
description: "Convert an Aecon-branded HTML slide deck to a white-labeled PPTX using pptxgenjs. Used when the user asks for a shareable .pptx version of an existing HTML briefing or deck."
category: govcon
---

# Aecon PPTX from HTML

Convert an Aecon-branded, white-labeled HTML slide deck to a .pptx file using pptxgenjs. This skill documents patterns discovered through iterative build-and-fix cycles.

## Prerequisites

```bash
npm install pptxgenjs
```

## Process

1. **Extract slide structure** from the HTML — count slides, identify content per slide (title, subtitle, tables, cards, stats)
2. **Build pptxgenjs script** targeting `LAYOUT_16x9` (10" × 5.625"). Each slide is a separate IIFE.
3. **Use safe fonts** — Calibri for body/headers, not Univers (not installed in PowerPoint everywhere). Never use Aptos.
4. **Colors**: Aecon web red `C8102E`, charcoal `252525`, body `464646`, silver `747679`, border `EAEAEA`, ivory `FAF9F5`.
5. **White-label**: Set `pres.author = "IS Vendors & Contracts"` or role title. Never Amyn/hermes/harbor. Verify with markitdown.
6. **Dark slides** (title/closing): charcoal background, white/c0 text, thin red bar at top.
7. **Content slides**: white/ivory background. No accent stripes, no color bars.

## Known Issues & Fixes

- **Hex colors: never `#` prefix** — pptxgenjs silently accepts but PowerPoint may reject. Pass bare hex: `"C8102E"` not `"#C8102E"`.
- **Shadows**: `offset` must be ≥ 0. Use `angle` for direction.
- **Text overflow**: pptxgenjs does not auto-shrink text. For dense content, use font sizes 7–10pt and explicitly set `lineSpacingMultiple`.
- **LibreOffice rendering is NOT authoritative** — the QA step (soffice → PDF → pdftoppm → vision_analyze) will show rendering glitches that are absent in PowerPoint. Trust pptxgenjs output, not LibreOffice preview.
- **Lists**: `bullet: true` on each item, never literal `•`. Set `breakLine: true` on all items except last. Space with `paraSpaceAfter`.
- **Slide number placement**: `y: 5.2` works for LAYOUT_16x9 (total height 5.625"). Footer text at `y: 5.2, h: 0.3`.
- **Table alternation**: use `fill: { color: i % 2 === 0 ? ivory : white }` for readability.
- **One `new pptxgen()` per output** — never reuse instances.
- **After writing, verify**: `markitdown out.pptx | grep -ci "amyn\|hermes\|harbor"` = 0.

## QA Commands

```bash
# White-label check
markitdown out.pptx 2>/dev/null | grep -ci "amyn\|aporbanderwala\|hermes\|harbor\|auto-generated\|kerem" && echo "FAIL" || echo "CLEAN"

# PDF conversion for visual check
soffice --headless --convert-to pdf --outdir /tmp out.pptx
pdftoppm -jpeg -r 150 /tmp/out.pdf /tmp/slide
ls -1 /tmp/slide-*.jpg | head -5  # check slide images

# File validation
python -c "from pptx import Presentation; p=Presentation('out.pptx'); print(f'Slides: {len(p.slides)}'); print(p.core_properties.author)"
```
