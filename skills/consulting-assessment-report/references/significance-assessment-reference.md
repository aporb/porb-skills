# Significance Inc. Comprehensive Assessment — Reference Example

## Source File

This reference is a symlink/documentation pointer. The actual deliverable lives at:

`/home/amyn/repos/2026_books/HARBOR_portfolio/significance/04-deliverables/significance-harbor-assessment-2026-07-10.html`

## Why It's a Good Reference

The Significance assessment is a complete 6-phase consulting deliverable that demonstrates:

### Structural Patterns
- **Cover block** with HARBOR letter badges, h1 title, subtitle, metadata grid (UEI, CAGE, leadership, SAM expiration)
- **Hero summary** — 2 rows of 3 metric cards each (revenue, lifetime obligations, FRI score, FTEs, acquisition cost, projected FRI)
- **Timeline bar** — 6 milestone markers (Jul 2026 → Q4 2027) with connecting lines
- **6 phase sections** — each with phase badge (colored circle + letter), h2, subtitle, data tables, highlights, component blocks
- **Call-to-action** block — one paragraph thesis + one paragraph elaboration
- **Attribution footer** — framework name once, prior-employment disclosure, status line

### Visual Components (all CSS-defined in `<style>`)
| Component | CSS Class | Purpose |
|-----------|-----------|---------|
| Phase-letter circles | `.harbor-letters span` | 6 colored circles in cover |
| Metric cards | `.hero-card` | Key stats in 3-column grid |
| Phase badge | `.phase-badge` | 48px colored circle |
| Highlight box | `.highlight` | Left-border-accented card (5 variants: default, critical, warning, success, architect, build, operate) |
| Callout | `.callout` | Bordered info box with label |
| Risk row | `.risk-row` | Severity badge + title + detail |
| Product card | `.product-card` | 2-column grid, `.lead` variant highlighted |
| Metric grid | `.metric-card` | 4-column stat blocks |
| Trajectory box | `.trajectory-box` | Numbered-step pathways |
| Timeline bar | `.timeline-bar` | Horizontal milestone track |
| Tags | `.tag` | Inline severity badges (strong/mod/weak/critical) |
| CTA | `.cta-block` | Gradient-background centered callout |

### Data Presentation
- Tables: full-width, collapsed borders, 13px font, uppercase 11px headers, `.num` class for monospace, `.delta-up`/`.delta-flat`
- Currency always with `$` and K/M suffixes
- Percentages at whole-number precision
- Every figure traceable to source dossier

### Indirect Positioning
- The six-phase framework is implied by the section badges (H, A, R, B, O, R) and the structured analysis
- "HARBOR" appears exactly once — in the footer attribution sentence
- The body never says "this analysis uses the [framework] methodology" — it just delivers the analysis

### Key Data Points Used
- Company: Significance Inc., Annapolis MD, EDWOSB
- Revenue: $32.8M T12M (91% Navy), $247M lifetime ($143.7M prime + $103.5M sub)
- FTEs: 75-100, rev/head: ~$260K-$280K
- Vehicles: 8 (GSA MAS, SeaPort-NxG, OASIS+ SB Pools 2/3, OASIS+ WOSB Pool 3, NAVFAC IDIQ, MCICOM, MDA SHIELD)
- FRI Score: 65/100 (B, Transitioning mid-band), projected 77/100 by Q1 2027
- SBIR acquisition: 2 USAF Phase I awards for $170K combined (Stottler Henke $55K + Bryant Alliance $115K)
- Products: 6 Signify-branded offerings across 2 acquisition threads
- Build cost range: $480K-$640K cumulative for all 6 products
- Projected product revenue: $4M-$6M annualized by Q4 2027
- Risks: 8 assessed (3 critical: Navy 91% concentration, novation FAR 42.12/B-418028, T&M margin pressure)

## Lessons for Future Deliverables

1. **Source-data discipline** — every figure must be traceable. If using backchannel intel (like the Ted Dennis report), cite it as structural influence on framing, not as a source for factual claims.
2. **Prior-employment disclosure** — if the analyst worked at the subject company, put this in the footer with a clear statement that factual claims are independently verifiable from public records.
3. **Timeline bar as narrative device** — the horizontal milestone track gives the reader an immediate sense of the journey. Place it right after the hero scores, before any phase content.
4. **Risk severity tiering** — use the `risk-row` component with severity badges (critical/high/medium). Each risk needs: what it is, why it matters, and a specific mitigation. Never leave a risk at "this is bad" — always provide the mitigation.
5. **Product cards with lead variant** — for multi-product lineups, use 2-column grids with a `.lead` (bordered/orange) variant for the recommended launcher. Include source badge (from which acquisition) and priority label.
6. **Margin math upfront** — the Build section should lead with the GP comparison (services 8-12% vs products 40-60%) and the revenue-per-employee delta. This is the economic argument that justifies the entire productization motion.
