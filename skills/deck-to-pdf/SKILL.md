---
name: deck-to-pdf
description: Convert a HARBOR HTML slide deck to a pixel-perfect PDF with clickable links. Auto-detects HTML deck files or accepts a path argument.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

# /deck-to-pdf -- HTML Deck to PDF with Clickable Links

Converts a HARBOR-branded HTML slide deck into a pixel-perfect PDF where all hyperlinks remain clickable. Uses Puppeteer to screenshot each slide at 2x retina resolution, extracts link positions from the DOM, then assembles the PDF with pdf-lib using invisible URI link annotations overlaid at the correct coordinates.

## How It Works

1. Puppeteer renders each `.slide` element in screen mode (dark theme preserved)
2. Screenshots captured at `deviceScaleFactor: 2` (retina quality)
3. `getBoundingClientRect()` extracts every `<a href>` position relative to its slide
4. pdf-lib creates a PDF: screenshot as full-page background + link annotations mapped from CSS pixels to PDF points
5. Coordinate math: CSS pixels (top-left origin) converted to PDF points (bottom-left origin, 72pts/inch)


## Execution (pure tool)

This skill is a **mechanical wrapper**. No agent dispatch. See `.claude/skills/SKILL-PATTERN.md` Tier D.

**Rationale:** Shell-out to a Chromium-based HTML-to-PDF renderer. Deterministic output, no judgment required, no voice or compliance considerations. Adding agent dispatch would inject latency + bureaucracy without quality improvement.

The invocation contract below is the complete tool interface. If cognitive work (triage, composition, voice-check) ever gets added to this skill, that work must be delegated to the appropriate specialist agent rather than inlined here.

---

The procedural playbook below is the tool contract.

## Workflow

### Step 1: Find the HTML Deck

If the user passed an argument (e.g., `/deck-to-pdf path/to/deck.html`), use that file.

If no argument was passed, auto-detect:
1. Use Glob to find `**/*_Deck_CLIENT.html` or `**/*_Strategy_Deck*.html` files in the current working directory and subdirectories
2. If multiple matches, use AskUserQuestion to let the user pick
3. If one match, confirm it with the user
4. If no matches, ask the user for the path

### Step 2: Verify Prerequisites

Check that the HTML file exists and contains `.slide` elements. Then check for dependencies:

```bash
# Check if puppeteer and pdf-lib are available
node -e "require('puppeteer'); require('pdf-lib')" 2>/dev/null
```

If dependencies are missing, check if there's a `package.json` with them in the deck's directory. If not, check the skill's references directory for the generation script and install dependencies:

```bash
cd <deck-directory>
npm install puppeteer pdf-lib
```

### Step 3: Ask User Options

Use AskUserQuestion to ask:

1. **Output filename** -- Default: same name as HTML but with `.pdf` extension. Let user override.
2. **Screenshots** -- "Do you also want individual slide screenshots saved?" Options: Yes (saves PNGs to a `slide-screenshots/` directory alongside the PDF) / No (PDF only)

### Step 4: Generate the PDF

Copy `generate-pdf.mjs` from `${CLAUDE_SKILL_DIR}/references/generate-pdf.mjs` to the deck's directory (if not already present), then run it:

```bash
node generate-pdf.mjs <input.html> <output.pdf>
```

If the user also wants screenshots, run the screenshot capture after:

```bash
node generate-pdf.mjs <input.html> <output.pdf> --screenshots
```

The `--screenshots` flag tells the script to also save individual PNGs.

### Step 5: Verify and Report

After generation:
1. Check that the PDF file exists and report its size
2. Report the number of pages and total link count
3. Remind the user to open the PDF and test a few links
4. If screenshots were generated, report the screenshot directory path

## Output

The skill produces:
- `<DeckName>.pdf` -- Pixel-perfect PDF with clickable links (11in x 8.5in landscape)
- (Optional) `slide-screenshots/slide-01.png` through `slide-NN.png` -- Individual slide PNGs at 2x resolution

## Technical Details

- **Slide detection:** `.slide` CSS class (standard HARBOR deck structure)
- **Page size:** 11in x 8.5in (792 x 612 PDF points) -- matches both dark and light HARBOR themes
- **Resolution:** 2x deviceScaleFactor for retina-quality screenshots
- **Link filtering:** Only `http://` and `https://` links are included. Internal anchors and javascript: links are skipped.
- **Coordinate mapping:** CSS pixels at 96dpi mapped to PDF points at 72dpi. Y-axis flipped (CSS top-left origin to PDF bottom-left origin).
- **Compatibility:** Links work in Adobe Acrobat, Chrome PDF viewer, Firefox PDF viewer, macOS Preview.

## Dependencies

- `puppeteer` (screenshots + DOM extraction)
- `pdf-lib` (PDF assembly + link annotations)

Both are installed in the deck's directory via `package.json`. The skill will install them if missing.
