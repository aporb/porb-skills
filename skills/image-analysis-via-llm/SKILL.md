---
name: image-analysis-via-llm
description: "Analyze local images using a vision-capable LLM (e.g. Gemini 2.5 Flash via OpenRouter). Use when the user shares an image and needs description, transcription, layout extraction, or visual Q&A. Covers the full pattern: base64-encode, POST to a vision API, handle rate limits and tool-output redaction."
tier: B
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---

# Image Analysis via LLM

Analyze a local image (or any image URL) using a vision-capable LLM via API. The Hermes tool surface does NOT include a direct `vision_analyze` tool. This skill is the workaround.

## When to Use

Trigger this skill whenever the user says:
- "Review this image in detail"
- "Build a briefing on this screenshot / diagram / chart"
- "What does this show?" / "Read the text in this"
- "Transcribe this image" / "Describe the layout"
- Composer-images are dropped into the chat with failed analysis — recover by routing through here
- Any image attached or referenced in a chat that the model can't see directly

Do NOT use this for:
- Generating images (use `image_generate` instead)
- Reading PDFs (use `ocr-and-documents` skill)
- Reading web-page screenshots (use `browser_navigate` + snapshot, or `web_extract`)

## How Hermes Sees Images

`vision_analyze(image_url=...)` IS available on this install. Use it as the PRIMARY method for analyzing images. Accepts raw absolute file paths (e.g. `/Users/amynporb/screenshot.png`).

**CRITICAL path syntax:** Pass the RAW file path, NOT a `file://` URL. `file:///Users/...` will fail with "Invalid image source." The correct form is `/Users/amynporb/screenshot.png` (no scheme prefix).

If `vision_analyze` returns success, use its output directly. It is cheaper and faster than the OpenRouter base64 workaround.

**Fallback to this skill when:**
- `vision_analyze` returns an error (tool not found, rate limited, invalid source)
- You need to analyze 10+ images in batch (this script handles rate-limit fallback chains better)
- The image needs pre-processing (resize, format conversion) before analysis
- You need a specific model that `vision_analyze` doesn't use

If the image is in `~/Library/Application Support/Hermes/composer-images/`, the absolute path is what you pass into the script below.

### Batch Deck Analysis Pattern

When analyzing a product deck from screenshots (10+ images), use `vision_analyze` with a consistent question/prompt per slide. Process them in parallel batches of 3 (the tool accepts parallel calls). After extraction, compile into a structured analysis:

1. **Identify deck structure** — group screenshots into sections (carousel groups, sub-decks)
2. **Extract claims vs specs** — separate verifiable specifications from marketing claims
3. **Flag verification gaps** — note claims that lack sources, customer names, or specific data
4. **Cross-reference** — check website, company materials for consistency
5. **Save output** — write to `01-research/deck-analysis.md` under the prospect's portfolio folder

## The Pattern (5 steps)

1. **Locate** the image. Composer-images go in `~/Library/Application Support/Hermes/composer-images/`. User-attached files land there with timestamped filenames like `composer_2026-06-08_17-12-59-414_ac1ccf.jpg`. If the user references a file by URL, download to `/tmp/` first.

2. **Read the API key at runtime, never inline.** Tool outputs redact anything that looks like an API key (`***` substitution). If you put the key in a script via `write_file` or a heredoc, the redaction propagates into the file and the key is broken. Two safe patterns:
   - **Build the env var name from parts at runtime**: `prefix = "OPENROUTER"; suffix = "API_KEY"; key = os.environ.get(prefix + "_" + suffix)`.
   - **Read from the .env file line-by-line and never print the value** to tool output. The key may also be stored as `***` placeholder in `.env` if it was already redacted — fall back to env var, then prompt the user.

3. **Encode the image to a base64 data URI.** Detect mime from extension (`.jpg`/`.jpeg` → `image/jpeg`, everything else → `image/png`):
   ```python
   with open(path, 'rb') as f:
       b64 = base64.b64encode(f.read()).decode('utf-8')
   url = f"data:{mime};base64,{b64}"
   ```

4. **POST to OpenRouter's `/api/v1/chat/completions` with the image in a multimodal message.** Use a vision-capable model. Recommended model order (cheapest reliable first):
   - `google/gemini-2.5-flash` — **primary**. Fast, accurate, free tier available. Handles handwriting, diagrams, screenshots.
   - `google/gemini-3-flash-preview` — newer, similar cost, sometimes better on dense text.
   - `google/gemma-4-26b-a4b-it` — fallback. Free but commonly **rate-limited (HTTP 429)** on the public free tier; have a fallback behind it.
   - Paid fallbacks if free fails: `anthropic/claude-sonnet-4`, `openai/gpt-5-mini`.

5. **Save the result to a file, not just stdout.** Tool output truncates around 50KB; long analysis gets cut. Write to `/tmp/image{N}_full.txt` and `cat` the relevant slices back. The user can also re-read the saved file from a future session.

## Template Script

See `scripts/analyze_image.py` for a self-contained, copy-paste-ready template. It:
- Builds env var name at runtime (no inline key)
- Encodes the image
- POSTs to OpenRouter with configurable model + prompt
- Writes result to `/tmp/image_full.txt`
- Returns clean status + content

## Prompt Design (for analysis tasks)

For a faithful "reconstruction-grade" description, use this skeleton:

```
Analyze this image in extreme detail. I need a complete reconstruction-grade description.

Please provide:
1. WHAT IS THIS: One-sentence purpose/identity
2. VISUAL LAYOUT: Position of each section (top/middle/bottom, left/right), structure, color scheme, dimensions
3. TEXT CONTENT: Transcribe ALL visible text verbatim. Use quotes. Include all labels, captions, arrows text, annotations.
4. ALL DATA/VALUES: Numbers, percentages, statistics
5. ARROWS/CONNECTIONS: Flow connections, which elements connect to which
6. BRANDING/STYLING: Colors, fonts, drawing style (hand-drawn / vector / sketch)
7. TECHNICAL ELEMENTS: Code, command lines, technical diagrams
8. CONTEXT: Domain, industry, use case

Do not summarize. Provide EVERY visible text element.
```

For a comparison prompt (e.g. "are these two images the same?"), use the same prompt on each image separately, then ask the second-pass question explicitly.

## Pitfalls

- **Tool-output redaction of API keys.** The most common failure mode. `cat ~/.hermes/.env` shows `OPENROUTER_API_KEY=***` to you, even when the real key is on disk. Don't write a script that has the key inline — build the env var name from string parts at runtime. Don't `print(api_key)` either; just use it.
- **Free-tier 429 rate limits.** `google/gemma-4-26b-a4b-it:free` and `google/gemma-4-31b-it:free` are commonly rate-limited. `google/gemini-2.5-flash` is the most reliable free tier. Have a fallback chain: try free first, on 429 switch to the next model.
- **Output truncation.** Long analyses get cut by the tool's output cap. Save to a file (`/tmp/image1_full.txt`) and read the file in slices, OR set `max_tokens: 8000` on the API call.
- **Image too large.** Most vision APIs accept up to ~20MB. If the image is bigger, downscale with `sips` (macOS): `sips -Z 2000 input.jpg --out /tmp/resized.jpg`. `-Z 2000` fits within 2000px on the long edge.
- **Timeouts.** Set urllib timeout to 120–180 seconds. Vision calls on big images are slow.
- **`vision_analyze` path syntax.** Pass raw paths like `/Users/amynporb/image.png`. NOT `file://` URLs — those return "Invalid image source."
- **Wrong mime type.** `.jpg` and `.jpeg` → `image/jpeg`. `.png` → `image/png`. `.webp` and `.heic` are NOT accepted by most vision APIs — convert first with `sips -s format jpeg input.heic --out /tmp/converted.jpg`.
- **Composer-image filenames are timestamped.** They're `composer_YYYY-MM-DD_HH-MM-SS-mmm_HASH.{jpg,png}`. Match by the timestamp, not the hash, when retrieving from a previous session.

## Setup Notes

Requires:
- `OPENROUTER_API_KEY` env var (or in `~/.hermes/.env`)
- Python 3 with stdlib only (no `pip install` needed — `urllib`, `base64`, `json`, `os` are all stdlib)
- Network egress to `openrouter.ai`

No LLM dependencies to install. The script is portable to any machine with Python 3 and internet.

## Related Skills

- `browse` — for browser-based image capture (different use case: capture from a live page, not analyze a local file)
- `ocr-and-documents` — for text extraction from PDFs and scans (different path: marker-pdf / pymupdf, not a vision LLM)
- `harbor-interactive-canvas` — for building the HTML briefing once you have the analysis
