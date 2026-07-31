# Web Presence Research for Federal Response Differentiation

## Purpose

This document covers the comprehensive web presence research phase — the step BEFORE drafting a Sources Sought response, capability statement, or proposal. It produces the raw evidence file that every capability claim traces back to.

## When To Run

- A federal response requires background on an individual or small business with multiple web properties
- The entity has scattered evidence across personal sites, product sites, published IP, GitHub, Amazon, and local files
- The existing "verified background" file is stale or doesn't exist
- You need to differentiate against competitors by surfacing quantified metrics from a sprawling digital footprint

## Output Deliverable

`~/sources-sought-responses/raw/<entity>-web-presence-inventory.md`

~25-35KB comprehensive markdown file with:
1. Executive Summary (top differentiators for target PWS)
2. Per-property sections (URL, purpose, facts, metrics, relevance)
3. Cross-referenced resume/profile data
4. Quantified Metrics Summary table
5. PWS Differentiation Matrix

## Extraction Methodology

### Phase 1: Gather All URLs

Find every domain and subdomain the entity controls. Sources:
- Personal website navigation menus and footer "Ecosystem" links
- Domain landing pages (e.g., `porbanderwala.cloud` terminal index listing all products)
- Resume/CLAUDE.md references to independent projects
- GitHub profile/organization pages
- Amazon author pages

### Phase 2: Parallel Batch Extraction

Group URLs by extraction method:

**Group A — static pages (web_extract, 5 at a time):**
- Personal website content pages (why-me, about, book descriptions)
- Self-contained product pages (harborgovcon.com, farchat.app)
- GitHub Pages sites (federal-ds-handbook)
- Any page that renders meaningful content without JavaScript

**Group B — JS-rendered SPAs (browser_navigate):**
- Next.js pages that return thin/empty content from web_extract (services, proof, subpages)
- Single-page applications
- Pages with dynamic content behind cookie consent banners

**Group C — blocked/private domains (browser_navigate):**
- `*.cloud` domains (web_extract returns "Blocked: URL targets a private or internal network address")
- Self-hosted VPS sites behind reverse proxies

**Group D — gated platforms (browser tools):**
- Amazon product pages (browser_console for JS data extraction, browser_vision for screenshots)
- LinkedIn profiles (if accessible)

**Group E — local filesystem (read_file):**
- Resume HTML/PDF
- CLAUDE.md, MEMORY.md, portfolio docs
- Existing persona research or background files

### Phase 3: Enrich with Detail Pages

After the initial batch, follow links to:
- `/about` pages on product sites for methodology, data sources, tech stack
- `/pricing` pages for SaaS tiers and revenue model evidence
- `/framework` pages for methodology documentation
- `/proof` or case study pages for quantified results
- `/book` pages for publication details

### Phase 4: Browser Extraction Techniques

For JS-rendered pages:
1. `browser_navigate(url)` — initial load
2. If content is behind a cookie banner: `browser_click(ref=accept_button_ref)` to dismiss
3. `browser_vision(question="Read all content...")` for visual inspection
4. `browser_snapshot(full=true)` for full accessibility tree

For Amazon product pages:
1. `browser_navigate(url)` 
2. `browser_vision(question="Read star rating, reviews, rankings...")` for overview
3. `browser_console(expression=JS_CODE)` for structured data extraction:
```js
(() => {
  return {
    title: document.querySelector('#productTitle')?.textContent.trim(),
    rating: document.querySelector('[data-hook="rating-out-of-text"]')?.textContent,
    numRatings: document.querySelector('#acrCustomerReviewText')?.textContent,
    // ... more fields
  };
})()
```

### Phase 5: Compile and Differentiate

- Cross-reference every claim against at least two sources
- Build quantified metrics table — every number must have a source URL
- Build PWS differentiation matrix — map PWS capability areas to specific evidence
- Flag gaps: what the PWS requires that has no evidence yet

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Firecrawl credit exhaustion (402 errors) | Stop ALL firecrawl calls immediately. Fall back to browser tools for scraping, parser for local PDFs, or web_search for discovery. Do not retry. |
| web_extract blocking `.cloud` domains as "private network" | These are self-hosted VPS sites, not actually private. Use browser_navigate. |
| JS-rendered pages returning only footer text via web_extract | Queue for browser rendering. Check if the page needs a cookie consent dismissal first. |
| Amazon pages returning 404 or empty via web_extract | Always use browser for Amazon. |
| Local resume PDF won't parse via firecrawl | Read the HTML version instead — resumes are often maintained in HTML for print. |
| Page content blocked by cookie consent overlay | Click "Necessary Only" or "Accept All" before extracting content. |
| Page has filter tabs (ALL PROJECTS / AI & DEV / etc.) | The "ALL" tab usually loads everything. If individual tabs have detail pages, follow those links. |

## Worked Example

See `~/sources-sought-responses/raw/amyn-web-presence-inventory.md` for a complete July 2026 example covering:
- 14 web properties across 5 domains (porbanderwala.com, .cloud, farchat.app, studybot.fun, harborgovcon.com)
- Amazon book page with ratings/rankings extraction
- Federal Data Science Handbook (96K words, 5 platform guides)
- Cross-referenced resume with local HTML file
- 30+ quantified metrics compiled into a differentiation matrix