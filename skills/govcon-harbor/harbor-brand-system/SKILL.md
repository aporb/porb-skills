---
name: harbor-brand-system
description: "HARBOR brand system for subdomains, decks, briefings, cards."
version: 1.0.0
---

# HARBOR Brand System

## When to Use

When creating ANY branded deliverable for **HARBOR Initiative LLC** — website subdomains (`eo.h.porb.dev`, subsequent HARBOR properties), HTML briefings intended as HARBOR publications, landing pages, slide decks, social media cards (LinkedIn, X), proposal cover pages, email templates, or any visual asset that needs to match HARBOR's corporate identity.

**When NOT to use:** Internal working documents, personal research briefings, repository sync reports, and agent-to-agent artifacts. Those use the **html-effectiveness aesthetic** (ivory `#FAF9F5`, clay `#D97757`, slate `#141413`, oat/olive accents) — or simply plain markdown. The distinction: if it carries the HARBOR logo or is intended for HARBOR's external or partner-facing presence, use this brand system. If it's an internal working document, default to html-effectiveness.

## Source of Truth

**ALWAYS verify brand tokens against the live canonical source before starting any HARBOR-branded work.**

The authoritative source of truth is the `harbor-website` repo at `~/repos/harbor-website/`, specifically `src/app/globals.css`. If the repo is not available, scrape the live site at **https://harborgovcon.com**.

**Pitfall — do not assume or guess HARBOR brand tokens.** This session's error: I used clay/orange (Hallmark design system) instead of HARBOR's navy/amber. The user corrected this. HARBOR is NOT Hallmark-colored. Both are used by the same person for different contexts. Load the source-of-truth every time.

## Full Design Token Reference

The complete token set (CSS custom properties for light/dark mode, `@theme inline` block, Geist font setup, logo SVG, metadata format, footer structure, ThemeToggle pattern) is documented in the **`brand-kit-extraction`** skill's reference file:

**`brand-kit-extraction/references/harbor-design-tokens.md`**

Load `brand-kit-extraction` first, then access that reference. The key values at a glance:

### Color Story
- **Light mode:** Navy primary (`oklch(0.205 0.042 265)`) + amber accent (`oklch(0.625 0.14 55)`) on warm ivory background (`oklch(0.995 0.002 90)`)
- **Dark mode:** Amber primary (`oklch(0.65 0.12 55)`) on near-black background (`oklch(0.13 0.005 285)`)
- **NOT orange/clay.** The accent is a golden amber, not a rust/terracotta. This is the single most common mistake.
- **Tone:** Professional, conservative, GovCon-appropriate. No gradients, no neon, no saturated colors.

### Typography
- **Geist Sans** (from `next/font/google`) — body + headings
- **Geist Mono** — code
- No serif typefaces in the HARBOR brand
- Font variable names: `--font-geist-sans`, `--font-geist-mono`

### Logo
- 6 colored circles (blue → purple → pink → orange → green → teal) + "HARBOR" wordmark
- Inline SVG, not an image file
- Extracted from `harbor-website/src/components/nav.tsx` — do NOT reconstruct from memory
- Circles are `cx={5, 15, 25, 35, 45, 55}`, each `r=4`, colors: `#3B82F6`, `#8B5CF6`, `#EC4899`, `#F97316`, `#22C55E`, `#14B8A6`

### Layout
- Tailwind v4 + shadcn/ui with `@theme inline` mapping
- `next-themes` with `ThemeProvider(attribute="class", defaultTheme="system", enableSystem)`
- Dark mode via `.dark` CSS class overrides
- Container: `mx-auto px-4` on standard max-width container

## Workflow: Rebranding a Subdomain to HARBOR

This exact workflow was executed for **EO Explorer** (`eo.h.porb.dev`). Full detail in `brand-kit-extraction` → "Rebranding an Existing App" section and its `references/harbor-design-tokens.md`.

### Steps
1. **Locate source of truth** — read `harbor-website/src/app/globals.css` directly (most precise) OR scrape harborgovcon.com
2. **Copy the full `:root` + `.dark` + `@theme inline` block** — replace the target app's `globals.css` entirely (do not merge)
3. **Add Geist Sans + Geist Mono font imports** in `layout.tsx`
4. **Add `<ThemeProvider>`** wrapper in layout
5. **Swap logo SVG** — extract from `harbor-website/src/components/nav.tsx` (inline SVG, 6 circles + "HARBOR" text)
6. **Update metadata** — title template `"App Name — HARBOR Initiative LLC"`, description with GovCon framing
7. **Update footer** — `"© {year} HARBOR Initiative LLC. All rights reserved."`
8. **Wire ThemeToggle** component into nav
9. **Delete dead code** — search for old brand hex values and orphaned components
10. **Build + verify** — `curl -s | grep` for brand markers (navy CSS, amber accent, HARBOR name in footer/title)

### Polish Rounds (Initial Rebrand is Never One Pass)

After step 10, plan for 4-7 additional polish rounds. Each round reveals gaps that only surface after deployment:

| Round | What to check | Why step 10 misses it |
|-------|---------------|-----------------------|
| Visual patterns | Home page needs dot grids, gradient meshes, visual rhythm | CSS swap doesn't add visual richness — those are new components |
| Graph/chart colors | D3 charts, SVGs, and legends have hardcoded stroke/fill colors | CSS swap doesn't touch inline SVG or canvas renderers |
| Dark mode audit | Every page under `.dark`: tooltips, SVGs, chart labels, borders, footer | Each component needs its own dark mode CSS — no blanket fix |
| Content/taxonomy | GovCon topics, badges, contextual CTAs | Needs content modeling and new components, not just CSS |
| Detail pages | Persona tabs, cross-ref tables, CTA boxes | New sections outside initial scope |
| Edge cases | 404 page, loading states, empty states, responsive breakpoints | Easy to forget in main content push |
| Docs | CLAUDE.md, README, repo documentation | Not visible in the running app |

Key insight: **a brand migration is a sequence of deployments, not a single deploy.**

### Pitfalls — Rebranding HARBOR
| Pitfall | Prevention |
|---------|-----------|
| Assuming Hallmark colors (clay/orange) are HARBOR colors | HARBOR is navy/amber. Hallmark is a separate design system for internal docs. Load the source of truth every time. |
| Reconstructing the logo from memory | Extract the SVG from the harbor-website repo. It's never just a text wordmark. |
| Merging old CSS into new | Replace `globals.css` entirely. Old tokens create conflicts. |
| Forgetting dark mode | The parent's `:root` AND `.dark` block must both be present. |
| Leaving old brand hex values in the codebase | Search for old hex values after the CSS swap. |
| Not verifying with curl | After deploy, grep for brand markers in the live HTML output. |
| Graph/visualization colors not migrated | D3 charts, SVGs, and legend UIs have hardcoded colors that the CSS swap doesn't touch. Grep graph components for remaining hex values and light-mode-only fallbacks as a separate sub-pass. |
| Stopping after one deploy | Plan for 4-7 polish rounds (see Polish Rounds table above). CSS swap is step 10 of ~17. |

## HTML Slide Deck Construction

When building a HARBOR-branded pitch deck (not a research briefing — those use `html-briefing`), the deliverable must be a proper slide deck with scroll-snap, not a stacked PDF-page layout.

### Slide Deck CSS Architecture

Each slide is a full-viewport section with scroll-snap:
```css
html { scroll-snap-type: y mandatory; }
.slide { min-height: 100dvh; scroll-snap-align: start; scroll-snap-stop: always; display: flex; flex-direction: column; justify-content: center; padding: 48px 56px; position: relative; }
```

**Do NOT stack slides vertically like PDF pages.** Each slide is exactly one viewport. The user corrected this: "this is not a slide deck. it looks like pdf pages."

### HARBOR Presentation Theme (Dark)

HARBOR pitch decks use a dark navy/amber theme — distinct from the ivory/clay briefing aesthetic:
```css
:root {
  --bg: #0F1115;  --surface: #1A1D24;  --amber: #C8962E;  --amber-bright: #DFB85A;
  --text: #E8E6E0;  --text2: #9A978E;  --text3: #6B695F;
  --r1: #C44A4A;  --g1: #4A7C5C;  --border: #2A2D35;
  --mono: ui-monospace, ...;  --sans: system-ui, ...;
}
```
Cards: `background: var(--surface); border: 1px solid var(--border);`. Stat numbers: `font-weight: 700; font-size: 28px` with amber color.

### The 5-Slide Pitch Structure

| Slide | Type | Content |
|-------|------|---------|
| 1 | Title (dark) | Keynote impact statement, counterparty name, HARBOR footer |
| 2 | Market Context | Verifiable industry stats as stat cards |
| 3 | Compliance Imperative | OSINT gap cards — regulatory/financial/competitive risk |
| 4 | Engagement (dark) | Discovery sprint + phased FFP, CLIN table |
| 5 | Why HARBOR + CTA | Comparison table, credentials, clear ask |

Slide counter: `position: absolute; bottom: 20px; right: 32px; font: 11px var(--mono); color: var(--text3);`
Footer: `position: absolute; bottom: 20px; left: 32px; font-size: 10px; color: var(--text3);`

### Comparison Table (Slide 5)

`.check` = amber checkmark for HARBOR. `.cross` = red ✗ for genuine competitor gaps. `.partial` = muted text for partial capabilities. **Do NOT give blanket ✗ to competitors with real capability** (Big 4 have nuclear/DOE practices — use ".partial Minimal" not "✗").

### Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Stacking slides like PDF pages | scroll-snap-type: y mandatory + min-height: 100dvh |
| Using ivory/clay for presentation decks | HARBOR decks = dark navy/amber. Briefings stay light |
| 14-slide Aecon format for a 5-slide pitch | Precisely 5 slides |
| Unverified stats — wrong amounts, fake citations | Fact-check EVERY stat. One wrong claim destroys credibility |
| Blanket ✗ on competitors with real capabilities | Use .partial with qualifiers |
| Production metrics as verifiable facts | Frame as "operating environment" with live demo offer |

## Brand Voice & Tone

HARBOR's external voice is **authoritative, evidence-based, direct** — the brand of a consulting firm that delivers hard-won federal expertise, not a software startup or thought-leadership blog.

- **No hype.** No "AMAZING", "CRUSH IT", "game-changer", "incredible". No startup superlatives.
- **No startup tropes.** No "about us" → "our mission" → "our values" boilerplate. No "disrupt", "democratize", "transformational".
- **Professional gravitas.** Short sentences. Active voice. Claims backed by evidence, not assertion.
- **GovCon-appropriate.** The audience is contracting officers, prime BD teams, compliance officers, and agency program managers. Write for them — not a tech conference crowd.
- **Productization language.** References to the HARBOR framework (6 phases), products (EconPulse, SBIR Portal, GovRadar), and services (Fractional CAIO).
- **No AI/agent mentions in external-facing copy.** "AI-powered" is fine as a product attribute; Hermes, agent names, and tooling references are not.

## Related Skills

- **`brand-kit-extraction`** — Load this first for the full `references/harbor-design-tokens.md` including exact CSS values, logo SVG, font setup, and the complete rebranding workflow documentation.
- **`nextjs-site-builder`** — For building/deploying HARBOR subdomain sites (Next.js App Router + Tailwind + shadcn/ui + Docker deploy to porb-server).
- **`html-briefing`** — For creating self-contained HTML research briefings that use HARBOR styling when marked as HARBOR publications.
- **`aecon-brand-system`** — Separate brand system for Aecon deliverables (charcoal/red, Univers, construction infra). Do not confuse with HARBOR brand.
