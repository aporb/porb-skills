---
name: crawl-site
description: Crawl a website and extract its content as structured JSON for analysis. Used by /portfolio-recon and the CEO agent for prospect research, competitive intelligence, and content ingestion.
---

# /crawl-site -- Website Content Crawler

Crawls a target website using gpt-crawler (Playwright/Crawlee) and outputs structured JSON with page titles, URLs, and extracted text content. The output is optimized for ingestion by Claude agents for analysis.

## When to Use

- **During /portfolio-recon** Phase 1 Agent 5 (Website Deep Crawl) to capture full site content
- **Prospect research** to understand a company's positioning, services, and messaging
- **Competitive intelligence** to analyze competitor websites
- **Content auditing** to catalog a site's pages and structure
- **Documentation ingestion** to pull in technical docs or knowledge bases

## Tool Location

```
operations/tools/crawl-site.mjs
```

## Usage

### Quick (auto-detect match pattern)

```bash
node operations/tools/crawl-site.mjs \
  --url "https://target-company.com" \
  --output "/path/to/output.json"
```

### Full Options

```bash
node operations/tools/crawl-site.mjs \
  --url "https://target-company.com" \
  --match "https://target-company.com/**" \
  --selector "main" \
  --max-pages 30 \
  --max-tokens 50000 \
  --exclude "https://target-company.com/blog/**" \
  --timeout 5000 \
  --output "/path/to/output.json"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--url` | Yes | -- | Starting URL or sitemap URL (ending in .xml) |
| `--match` | No | `{origin}/**` | URL glob pattern to follow links |
| `--selector` | No | `body` | CSS selector for content extraction |
| `--max-pages` | No | `50` | Maximum number of pages to crawl |
| `--output` | No | `./output.json` | Output file path (absolute or relative) |
| `--max-tokens` | No | unlimited | Cap output file size by token count |
| `--exclude` | No | none | URL patterns to skip (repeatable) |
| `--timeout` | No | `3000` | Selector wait timeout in ms |

### Output Format

The output is a JSON array of objects:

```json
[
  {
    "title": "Page Title",
    "url": "https://target-company.com/about",
    "html": "Extracted text content from the selector..."
  }
]
```

Despite the field name `html`, the content is **extracted innerText** (not raw HTML), making it directly readable by agents.


## Orchestration

This skill fans out to multiple agents. The orchestrator (CEO by default) manages the fan-out, sequences dependencies, and merges results. See `.claude/skills/SKILL-PATTERN.md` for the pattern.

### Step 1 — Resolve inputs & prep workspace

Parse arguments, ask via `AskUserQuestion` if missing, and prep the output paths.

### Step 2 — Parallel fan-out

Independent lanes launch in a single message (multiple `Agent` tool calls). Dependent lanes wait for their input lanes to complete before launching.

Lane list:

**Lane A — (direct)** (Crawl execution)
- **prompt must include:** The skill runs gpt-crawler directly. Output is raw JSON.
- **return:** structured output the orchestrator can merge

**Lane B — researcher** (Content analysis pass)
- **prompt must include:** After the crawl, delegate a researcher pass to synthesize the crawl JSON into a brief: stated offerings, claimed clients, technology stack, leadership, contracts mentioned, notable signals.
- **return:** structured output the orchestrator can merge

Each `Agent` call's prompt must include:
1. Command + resolved args
2. Operator: `Amyn Porbanderwala (HARBOR founder)`
3. Playbook: `Read .claude/skills/crawl-site/SKILL.md — your lane scope is <label>`
4. Scoped inputs for this lane only (not the full firehose)
5. Return contract: exactly what structured output this lane must return
6. Cross-lane isolation: do not reference other portfolio companies; hermetic seal applies

### Step 3 — Merge

Collect all lane returns. The orchestrator synthesizes into the final deliverable. For HTML decks, the final render lane (usually cto or code-builder) uses `operations/practice/brand/decks/` templates and pipes to `/deck-to-pdf` for PDF export.

### Step 4 — Memory + ledger

Save outputs under `HARBOR_portfolio/<slug>/`. Update `admin/memory/portfolio.md` with a one-line status change for the slug if material.

---

The detailed playbook below is what the orchestrator and each lane agent reads to execute this skill.

## Execution Flow

### Step 1: Interview (if called directly via /crawl-site)

Use `AskUserQuestion` to gather:

1. **"What URL do you want to crawl?"** (required)
2. **"What content are you trying to capture?"** Options:
   - Full site (services, about, case studies, blog)
   - Just the main pages (skip blog/news)
   - Documentation / knowledge base
   - Specific section (specify URL pattern)
3. **"Where should the output go?"** Suggest: `HARBOR_portfolio/{company}/00-sources/website-crawl.json` for portfolio-recon, or `/tmp/` for ad-hoc research
4. **"How many pages max?"** Default: 30 for company sites, 100 for documentation

### Step 2: Configure and Run

Based on the interview, determine the right parameters:

**Company websites** (most common for /portfolio-recon):
```bash
--selector "main, article, .content, #content"
--max-pages 30
--exclude "**/blog/**" --exclude "**/news/**" --exclude "**/careers/**"
```

**Documentation sites**:
```bash
--selector ".docs-content, .documentation, main"
--max-pages 100
--max-tokens 100000
```

**Blog/content marketing analysis**:
```bash
--match "https://example.com/blog/**"
--selector "article"
--max-pages 50
```

Run the crawler:
```bash
cd /Users/amynporb/Documents/_Projects/2026_books && \
node operations/tools/crawl-site.mjs \
  --url "<url>" \
  --match "<pattern>" \
  --selector "<selector>" \
  --max-pages <n> \
  --output "<output-path>"
```

### Step 3: Verify and Summarize

After the crawl completes:

1. Read the output file
2. Report: number of pages captured, total size, list of page titles/URLs
3. Flag any issues (0 pages = selector mismatch or blocked by JS rendering)

### Step 4: Analysis (if part of /portfolio-recon)

If this crawl is feeding into a /portfolio-recon engagement, analyze the content for:

- **Service lines** and how they're described
- **Named products/offerings** (or lack thereof -- key productization signal)
- **Industry focus** and target customer language
- **Case studies** and proof points
- **Team page** presence and depth
- **Content maturity** (blog frequency, recency, depth)
- **CTAs and sales language** (booking calls vs. contact forms vs. pricing pages)
- **Technology mentions** (platforms, certifications, partnerships)
- **HARBOR signals**: Is there extractable IP? Named methodologies? Repeatable processes?

Write the analysis to `01-research/website-analysis.md` in the client directory.

## Integration with /portfolio-recon

The `/portfolio-recon` skill's Phase 1 Agent 5 (Website Deep Crawl) should use this tool:

```bash
# Inside the portfolio-recon Phase 1 Agent 5
node operations/tools/crawl-site.mjs \
  --url "https://prospect-company.com" \
  --selector "main, article, .content" \
  --max-pages 30 \
  --output "HARBOR_portfolio/{company}/00-sources/website-crawl.json"
```

Then read the output JSON and perform the website analysis.

## CRITICAL: Visual Verification Step (Layer 2)

**The crawl extracts raw HTML source code, which may include hidden template defaults, disabled widgets, and conditional content that is NOT visually rendered.** Before using crawl findings in client-facing deliverables, you MUST verify key pages with a headed browser.

### After crawl completes:

1. Use Claude-in-Chrome (or headed Playwright) to navigate to the 5-6 most important pages:
   - Homepage
   - About page
   - Products/Services page
   - Contact page
   - Footer (scroll to bottom of homepage)

2. Take screenshots and use `get_page_text` to capture what a human visitor actually sees.

3. Compare crawl findings (Layer 1) against visual findings (Layer 2). Flag discrepancies.

4. Common source-code artifacts that may NOT be rendered:
   - WordPress theme demo testimonials
   - Template phone numbers (e.g., +855 Cambodia default)
   - Placeholder employee counts or experience claims
   - Disabled Elementor widgets still in HTML
   - Hidden sections with `display:none` or zero opacity

5. **RULE: Only visually confirmed data goes into client-facing deliverables.** Source-code-only findings go into internal notes with the tag "in source code, not rendered."

### Why this matters:
During the Bravent engagement, crawl flagged "fake Facebook testimonials" and a "Cambodia phone number" as critical website issues. Chrome verification confirmed neither was visible. If presented to the client, it would have destroyed credibility.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 0 pages captured | JS-heavy SPA, selector mismatch | Try `--selector "body"`, increase `--timeout` |
| Crawl hangs | Rate limiting or infinite pagination | Reduce `--max-pages`, add `--exclude` patterns |
| Output too large | Blog/news pages inflating content | Add `--exclude` for blog/news, use `--max-tokens` |
| CAPTCHA/block | Bot detection | Try a different `--selector`, reduce crawl speed |
| "Cannot find module" | gpt-crawler not built | Run `cd operations/tools/gpt-crawler && npm install && npm run build` |

## Constraints

- **Do not crawl sites you don't have authorization to access** (login-gated, subscription content)
- **Respect robots.txt** -- Crawlee/Playwright respects it by default
- **Rate limiting** -- the crawler has built-in concurrency management via Crawlee
- **Output is text only** -- images, PDFs, and media are excluded by default
- **The `storage/` directory** in gpt-crawler accumulates data between runs. The crawler purges it on each start (`purgeOnStart: true`).
