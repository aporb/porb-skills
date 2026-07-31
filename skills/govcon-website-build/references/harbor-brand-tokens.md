# HARBOR Initiative Brand Tokens

Extracted from live harborgovcon.com (July 2026).

## Color Palette

| Token | Hex | Purpose |
|-------|-----|---------|
| Primary Blue | `#2563EB` | Buttons, links, action accents |
| Dark Background | `#0F172A` (slate-900) | Navbar, footer, dark sections |
| Light Background | `#F8FAFC` (slate-50) | Main page body |
| Purple Accent | `#7C3AED` (purple-600) | Secondary highlights, hover states |
| Muted Text | `#64748B` (slate-500) | Secondary/caption text |
| Border Color | `#E2E8F0` (slate-200) | Card borders, dividers |
| Text Dark | `#0F172A` | Body text on light backgrounds |
| Text Light | `#F8FAFC` | Body text on dark backgrounds |

## Brand Gradients

```css
/* Primary brand gradient — blue to purple */
background: linear-gradient(135deg, #2563EB, #7C3AED);

/* Alternate — teal to blue */
background: linear-gradient(135deg, #0D9488, #2563EB);
```

## Data Visualization (Chart Palette)

| Document Type | Hex | Token Name |
|---------------|-----|------------|
| Executive Order | `#3B82F6` (blue) | `--harbor-chart-blue` |
| Proclamation | `#10B981` (green) | `--harbor-chart-green` |
| Memorandum | `#8B5CF6` (purple) | `--harbor-chart-purple` |

| Relationship | Hex | Token Name |
|--------------|-----|------------|
| Revokes | `#EF4444` (red) | `--harbor-chart-red` |
| Modifies | `#F97316` (orange) | `--harbor-chart-orange` |
| Supersedes | `#EC4899` (pink) | `--harbor-chart-pink` |
| Extends | `#10B981` (green) | `--harbor-chart-green` |
| Implements | `#3B82F6` (blue) | `--harbor-chart-blue` |
| Relates To | `#6B7280` (gray) | `--harbor-chart-gray` |

## Visual Patterns

- **Dot grid background:** Small dots at 20% opacity on dark nav/footer sections. Use Tailwind utility `bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))]` or a custom `bg-dotted` class.
- **Gradient mesh orbs:** Large blurred circles (300-500px) at 30-60% opacity behind hero sections. Blue (`#2563EB`), teal (`#0D9488`), purple (`#7C3AED`) variants.
- **Glass nav:** `backdrop-blur-sm` on the sticky nav, semi-transparent background matching the dark section (`bg-slate-900/80`).
- **Gradient text highlights:** Key numbers and emphasized phrases use `bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent`.
- **"For federal contractors" badge:** A small pill/badge at the top of the hero, `border-primary/20 bg-primary/10 text-primary`, reading "For federal contractors" — signals the GovCon audience.

## Typography

- **Primary body:** Inter (sans-serif) — loaded via `next/font`
- **Display/headings:** SARA (serif) — loaded from Google Fonts `<link>` in layout.tsx. Used only on the `/` home page hero heading.
- **Fallback for headings:** system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
- **Monospace:** ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace

## Structure (HARBOR Subdomain Pattern)

- **Dark nav + light body:** Navigation is slate-900 with white text; page body is light (slate-50). The hero section may be dark with the blue→purple gradient, transitioning to a light content area below.
- **Parent brand link in footer:** The subdomain footer should link back to `https://harborgovcon.com` with "A HARBOR Initiative resource" or similar language.
- **Subdomain header:** Uses the same nav structure but with the subdomain's specific logo/wordmark alongside or replacing the HARBOR wordmark.

## Logo

- HARBOR logo available at harborgovcon.com nav (typically an SVG or text wordmark).
- No known local SVG asset — extract from the live site when needed via the nav `<img>` or inspect element.
- For subdomain logos, replace the wordmark or add the subdomain name next to the HARBOR mark.
