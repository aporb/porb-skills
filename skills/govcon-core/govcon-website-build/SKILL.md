---
name: govcon-website-build
description: Build or improve a federal contractor's public website — crawl existing site, audit against SAM evaluator checklist, design premium consulting-brand identity, build with Next.js 16 + Tailwind + shadcn/ui, deploy to Vercel. Covers color palette for defense/GovCon, anonymous vs named personnel decisions, proprietary framework pages, favicon/OG generation, and evaluator compliance.
tags:
  - govcon
  - website
  - nextjs
  - branding
  - consulting
  - sdvosb
related_skills:
  - brand-kit-extraction
  - consulting-assessment-report
  - nextjs-site-builder
triggers:
  - "build a website for [govcon firm]"
  - "improve the [contractor] website"
  - "redesign the GovCon site"
  - "crawl and rebuild [federal consulting] site"
  - "govcon website evaluator checklist"
  - "audit a federal contractor website"
---

# GovCon Website Build

Use this skill when the user asks you to **build, rebuild, redesign, or improve a federal contractor's public website** — whether starting from scratch, migrating off a proprietary builder (GoDaddy Airo, Wix, Squarespace), or upgrading an existing site.

## When to Use

- User says "build a website for [GovCon firm]"
- User says "improve/redesign the [contractor] site"
- User asks to "review a site as a CPO" / provide CTO-level direction
- User wants a subdomain or child site rebranded under a parent organization
- User asks to crawl an existing GovCon site and create an improvement plan
- User needs to ensure SAM.gov evaluator checklist compliance with a public website rebrand
- User wants a proprietary methodology framework page for a federal consulting firm

## When NOT to Use

- General brand kit extraction without GovCon context → `brand-kit-extraction`
- Multi-phase consulting assessment reports → `consulting-assessment-report`
- Non-GovCon Next.js site builds → `nextjs-site-builder`
- HTML briefings about contractor research → `project-briefing`

## Core Workflow

```
crawl existing site → audit against evaluator checklist → research design trends
→ design color palette + typography → build Next.js + Tailwind + shadcn/ui
→ add checklist content → generate favicon/icons → add proprietary framework (if applicable)
→ deploy to Vercel → verify live
```

### 1. Crawl & Audit

```bash
# Mirror the existing site
wget --mirror --convert-links --adjust-extension --page-requisites \
  --no-parent -e robots=off -U "Mozilla/5.0 ..." "https://example.com/" \
  -P ~/sitename-mirror/

# Tech recon
curl -sI https://example.com/ | grep -iE "server|x-powered|cf-ray|ss-product"
dig +short A example.com; dig +short NS example.com

# Brand extraction — scrape the actual parent site for tokens
# DO NOT guess colors/fonts from brand-name alone
# Use firecrawl_scrape with formats: ["branding"] or formats: ["markdown"]
# to extract the actual color hexes, fonts, and logo treatment
```

**⚠️ CRITICAL: Scrape the parent/umbrella brand first.** Before designing a palette, typography, or logo treatment for a subdomain or child site that needs to match a parent brand (e.g., rebranding eo-explorer under HARBOR):

1. Scrape `https://<parentsite>.com` with `firecrawl_scrape(url, formats=["branding"])` to extract actual colors, fonts, brand tokens.
2. Extract CSS directly: `curl -sL https://parentsite.com | grep -oE 'href=\"([^\"]+\\.css[^\"]*)\"' | head -5`, then curl each CSS file to find `:root` / `--color-*` tokens.
3. Screenshot with `browser_vision` to confirm visual treatment (gradients, nav style, logo placement, light vs dark mode).
4. If no logo SVG is available via the page, try `https://parentsite.com/logo.svg` or inspect the nav for `<img src=.../>` and follow the link.

Do NOT infer the brand from Hallmark or any other system — always extract from the actual live site.

Check for: proprietary builder lock-in (`ss-product-id: aab-v1` = GoDaddy Airo), CDN/proxy, CMS platform, TLS cert details.

**Key audit questions:**
- Is it a single-page SPA or multi-page?
- Are there named personnel with current-employer references? (conflict risk)
- What GovCon trust assets are present (NAICS, CAGE/UEI, past performance, capabilities statement)?
- What's the tech stack and is the owner locked in?

### 2. Evaluator Checklist Compliance

SAM.gov evaluators will cross-reference the public website against the SAM registration. See `references/sam-evaluator-checklist.md` for the canonical 14-item list.

The critical constraint: **the public website and the SAM registration must be consistent.** If the SAM registration lists named principals, evaluators expect to find them on the site. However, **named personnel create day-job conflict risk.** The standard resolution: named bios live in a private capabilities-statement PDF shared directly with evaluators, not on the public crawled website. The public site sells aggregate credentials.

### 3. Color Palette for GovCon / Defense

Professional consulting sites default to **light mode** (ivory/paper ground, dark text, accent color for energy). Dark-mode sites are the exception, not the rule, for professional services.

**Palette selection by identity:**
- **Marine Corps / expeditionary:** scarlet (#CC3333) as accent/action, gold (#C9A227) as secondary data highlight, deep navy (#0D1B2A) for typography only. Avoid green/OD for consulting.
- **Generic federal / defense:** navy (#0A1628 or #14213D) as primary, brass/gold accent, ivory ground. Reads "Naval Academy" — safe but not distinctive.
- **Tech-forward:** keep the light ground but use a cooler slate accent (#475569 or similar).

Scarlet works well for veteran-owned firms because it's unambiguously Marine and ownable. Use it for: section labels, CTAs, nav hover, hero accent, phase tiles. Reserve gold for numbers, trust-bar stats, and the logo mark. Navy stays for headings and the logo background.

**HARBOR brand tokens (extracted from harborgovcon.com):**
When a subdomain or child site needs to match HARBOR branding, use these exact tokens:

```css
/* HARBOR brand — extracted from live harborgovcon.com */
:root {
  --harbor-blue: #2563EB;           /* primary button, action accents */
  --harbor-dark-bg: #0F172A;        /* slate-900 — nav, footer, dark sections */
  --harbor-light-bg: #F8FAFC;       /* slate-50 — main page background */
  --harbor-grid: #1E293B at 20% opacity; /* dot grid overlay */
  --harbor-accent: #7C3AED;         /* purple-600 — secondary highlights */
  --harbor-muted: #64748B;          /* slate-500 — secondary text */
  --harbor-border: #E2E8F0;         /* slate-200 — borders */
  --harbor-text: #0F172A;           /* dark text on light */
  --harbor-text-light: #F8FAFC;     /* light text on dark */
  --harbor-gradient: linear-gradient(135deg, #2563EB, #7C3AED); /* blue→purple hero gradient */
  --harbor-gradient-teal: linear-gradient(135deg, #0D9488, #2563EB); /* teal→blue variant */
  --harbor-chart-blue: #3B82F6;     /* data viz — executive orders */
  --harbor-chart-green: #10B981;    /* data viz — proclamations */
  --harbor-chart-purple: #8B5CF6;   /* data viz — memoranda */
  --harbor-chart-red: #EF4444;      /* data viz — revokes */
  --harbor-chart-orange: #F97316;   /* data viz — modifies */
  --harbor-chart-pink: #EC4899;     /* data viz — supersedes */
}
```

**HARBOR visual patterns:**
- **Dot grid:** `bg-dotted` utility class — small dots at 20% opacity on dark backgrounds
- **Gradient mesh orbs:** Large blurred circles (`gradient-mesh` classes) — blue, teal, purple at 30-60% opacity, placed behind hero sections
- **Glass effect:** `backdrop-blur-sm` on sticky nav, semi-transparent background
- **Gradient text:** `bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent` for emphasized numbers/key phrases
- **Dark nav + light page:** Navber in slate-900 with white text, page body in light mode

**HARBOR fonts:** Inter (body/text) — loaded via next/font. SARA (display/headings) — loaded from Google Fonts via `<link>` in layout.tsx. Use Inter for UI, SARA for headings on `/` page only. Fall back to system sans-serif for SARA on subpages.

### 4. Build Stack

**Recommended stack (2026):**
- **Next.js 16** (App Router, Turbopack, static prerender) — best-in-class for SEO, perf, and free Vercel hosting
- **Tailwind CSS v4** with brand design tokens in `globals.css`
- **shadcn/ui** (Base UI primitives in 2026 — see `references/nextjs16-shadcn-patterns.md`)
- **framer-motion** for tasteful scroll reveals and hero entrance (not flashy animation)
- **Canvas particles** (vanilla JS, no library) for hero background — subtle dot network at very low opacity
- **Fonts:** Rajdhani (headings), Cormorant Garamond (display serif), Source Sans 3 (body)

**Avoid:** GoDaddy Airo, Wix, Squarespace, Webflow — proprietary lock-in prevents git ownership, incremental improvement, and free hosting.

### 5. Favicon & Icons

Generate per Next.js App Router conventions (files in `src/app/` auto-served, no `<link>` tags needed):

| File | Size | Purpose |
|------|------|---------|
| `favicon.ico` | 16/32/48 multi-size | classic browser tab |
| `icon.png` | 512×512 | modern browsers |
| `apple-icon.png` | 180×180 | iOS home screen |
| `opengraph-image.png` | 1200×630 | social/LinkedIn unfurl |

Use Python/Pillow for generation. The monogram should match the header logo mark. Avoid using the founder's headshot as `og:image` — it unfurls on every LinkedIn share.

### 6. Proprietary Framework Page

If the firm has (or wants) a named methodology, build it as a dedicated page (e.g., `/oorah`, `/framework`) with:
- **Acrostic letter tiles** in the hero (one tile per phase, clickable anchors)
- **Phase detail cards** — objective, key activities (bulleted), deliverables (badges), outcome (callout box)
- **Authoritative-source grounding strip** — the NIST/DFARS/CMMC references that make it credible
- **CTA** at the bottom ("Request an assessment")
- **Shared data module** — `src/lib/framework.ts` as single source of truth for both the landing-page teaser and the full page
- **Trim badge text** — deliverables rendered as badges must fit; use `whitespace-normal` and keep text under ~120 chars

### 7. Visual QA Before Deploy

Use `browser_vision` with `annotate=true` to capture screenshots of every key page state:

```text
1. Home page hero (desktop + mobile viewport)
2. Navigation (open mobile menu if applicable)
3. Explore/list page (verify pagination, filter controls)
4. Detail/document page
5. Graph/visualization page (verify legend colors match brand palette)
6. Search results (empty state, populated state)
7. Dark mode toggle (if implemented)
```

**Review checklist per screenshot:**
- Are the colors from the correct brand (parent/umbrella, not Hallmark or default Tailwind)?
- Does the logo/image load?
- Is there a hardcoded `data-theme` that should use ThemeProvider?
- Do font imports work (SARA, Inter, etc.)?
- Do the graph/visualization legend colors match the new palette?

Take 4-5 screenshots at once and compare against the parent brand site's look-and-feel. Flag each discrepancy as a separate issue.

### 8. Deployment

Deploy to Vercel (free tier, git-backed). The Vercel CLI needs a one-time login. DNS cutover from the old host (GoDaddy, etc.) requires changing only A and CNAME records — leave MX/SPF/M365 TXT untouched to preserve email.

```bash
npx next build          # verify static prerender
vercel deploy --prod    # deploy to production
```

## Content Architecture for GovCon Sites

A complete GovCon site should have:

| Page | Content | Priority |
|------|---------|----------|
| `/` (Home) | Hero + trust bar + who-we-are + federal experience + capabilities + NAICS + framework teaser + anonymous leadership + contact | P0 |
| `/oorah` (or framework name) | Full proprietary methodology detail | P1 |
| `/capabilities` | Deep-dive services + downloadable capabilities statement PDF | P1 |
| `/experience` | Anonymized representative program experience | P2 |
| `/teaming` | Subcontracting/partnership for primes | P2 |
| `/insights` | Blog/whitepapers for SEO + long-cycle nurture | P3 |
| `/contact` | Full form + CO-friendly direct contact | P1 |

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Named personnel with current-employer references | Strip all names from public site. Bios go in private capabilities statement. |
| Dark-mode default for professional site | Light mode (ivory/paper ground) is the professional default. Correct if user pushes back. |
| `asChild` prop on shadcn Button in Next 16 | shadcn uses Base UI now — use `render={<a href="..." />}` instead of `asChild`. |
| `ssr:false` with `next/dynamic` in server component | Next 16 blocks this. Move the dynamic import into a `'use client'` component instead. |
| Badge text overflow on deliverable pills | Keep deliverable text under ~120 chars; add `whitespace-normal` to Badge className. |
| Founder headshot as `og:image` | Social unfurls show the headshot. Generate a branded opengraph-image.png instead. |
| No evaluator-checklist items on site | UEI/CAGE/NAICS/entity status must be present. EIN should NOT be on the public site — it's sensitive. Use UEI + CAGE instead. See `references/govcon-contact-section-pattern.md`. |
| Exposing EIN or full street address | EIN is sensitive; remove it. Street address is unnecessary — city/state is sufficient; SAM.gov has the full address. |
| Proprietary builder lock-in | Migrate off GoDaddy Airo/Wix/Squarespace. Owner must own the source in git. |
| **Plan-only, no implementation** | When user says "fix it" or "take action", implement code changes — not a plan document. A plan without execution is not a deliverable. If they explicitly ask for a plan (CPO review, CTO directions), write the plan AND then implement it in the same session unless told otherwise. |
| **Guessing brand colors instead of scraping** | Before any palette work for a subdomain/child site, extract the actual parent brand tokens first. See §1 Crawl & Audit. Do NOT infer from Hallmark, industry conventions, or assumed associations — always scrape the live site. |
| **Hardcoded data-theme="dark" on a page** | If the parent site is dark-mode-dominant (like harborgovcon.com's dark hero), the child site should use the ThemeProvider pattern from shadcn/ui, not a hardcoded `data-theme` attribute. Hardcoding breaks the light/dark toggle and forces a single mode on all users. |
| **Using documents.length for count display** | When the page receives pre-filtered data, `docs.length` is the filtered-in-memory count, not the database total. Always pass a separate `totalCount` prop from the SSR page and display it correctly: "Showing {paginated.length} of {filtered.length} ({totalCount} total)". |

## References

- `references/sam-evaluator-checklist.md` — The 14 items SAM.gov evaluators verify against the public website
- `references/nextjs16-shadcn-patterns.md` — Next.js 16 + shadcn/ui (Base UI) migration notes and API changes
