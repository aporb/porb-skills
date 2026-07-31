# html-effectiveness (Thariq) CSS Design Tokens

The internal briefing aesthetic used for Leatherneck+HARBOR, personal working briefings, and internal intelligence documents. This is the "Thariq" aesthetic referenced in `aecon-brand-system`'s "When NOT to use" section and `consulting-assessment-report`'s "Theme Selection" guidance.

## Complete CSS Token Block

```css
:root {
  --ivory: #FAF9F5;
  --paper: #FFFFFF;
  --slate: #141413;
  --clay: #D97757;
  --clay-d: #B85C3E;
  --oat: #E3DACC;
  --olive: #788C5D;
  --g100: #F0EEE6;
  --g200: #E6E3DA;
  --g300: #D1CFC5;
  --g500: #87867F;
  --g700: #3D3D3A;
  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
}
```

## When to Use
- Internal intelligence briefings (Leatherneck+HARBOR, personal working docs)
- Repo sync reports
- Agent-to-agent artifacts
- Any document NOT intended for external stakeholder presentation
- When the audience is Amyn (not a client, not Aecon stakeholders)

## When NOT to Use
- Aecon-branded deliverables for FBU team → `aecon-brand-system` (Univers, #E51937/#C8102E, Aecon logo)
- External consulting deliverables for clients → HARBOR Dark Theme (#0f172a, phase colors)
- Public-facing GovCon website → dark govcon aesthetic (different token set)

## CSS Reset + Base (copy-ready)
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--ivory);
  color: var(--slate);
  font-family: var(--sans);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
.wrap { max-width: 880px; margin: 0 auto; padding: 3rem 1.5rem 5rem; }
h1 { font-family: var(--serif); font-size: 2.2rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.25rem; }
h2 { font-family: var(--serif); font-size: 1.5rem; font-weight: 600; margin: 3rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--oat); }
h3 { font-size: 1.05rem; font-weight: 600; margin: 1.5rem 0 0.5rem; color: var(--g700); }
p { margin: 0.75rem 0; }
.meta { color: var(--g500); font-size: 0.85rem; margin-bottom: 1.5rem; }
```

## Reusable Component Classes

### Stat Band
```css
.stat-band { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin: 2rem 0; }
.stat-card { background: var(--paper); border: 1px solid var(--g200); border-radius: 8px; padding: 1.25rem; text-align: center; }
.stat-card .number { font-family: var(--serif); font-size: 2rem; font-weight: 700; color: var(--clay); }
.stat-card .label { font-size: 0.8rem; color: var(--g500); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.25rem; }
```

### Tables
```css
table { width: 100%; border-collapse: collapse; margin: 1rem 0 1.5rem; font-size: 0.9rem; }
thead { background: var(--g100); }
th { text-align: left; padding: 0.6rem 0.75rem; font-weight: 600; color: var(--g700); border-bottom: 2px solid var(--oat); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
td { padding: 0.6rem 0.75rem; border-bottom: 1px solid var(--g200); vertical-align: top; }
tr:last-child td { border-bottom: none; }
```

### Cards
```css
.card { background: var(--paper); border: 1px solid var(--g200); border-radius: 8px; padding: 1.5rem; margin: 1.25rem 0; }
.card h3 { margin-top: 0; }
```

### Callouts
```css
.callout { border-left: 4px solid var(--clay); background: var(--g100); padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0 6px 6px 0; font-size: 0.92rem; }
.callout.warn { border-left-color: #C94A4A; }
.callout.good { border-left-color: var(--olive); }
.callout strong { color: var(--slate); }
```

### Tags/Badges
```css
.tag { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.03em; }
.tag-red { background: #FDE8E8; color: #C94A4A; }
.tag-green { background: #E6F0DC; color: var(--olive); }
.tag-amber { background: #FEF3C7; color: #B45309; }
.tag-clay { background: #FDE8E0; color: var(--clay-d); }
```

### Verdict Box
```css
.verdict { background: var(--slate); color: var(--ivory); padding: 2rem; border-radius: 10px; margin: 2rem 0; }
.verdict h2 { color: var(--ivory); border-color: var(--g700); margin-top: 0; }
.verdict .big { font-family: var(--serif); font-size: 1.4rem; line-height: 1.5; }
.verdict .sub { color: var(--g300); font-size: 0.9rem; margin-top: 0.75rem; }
```

### TOC
```css
.toc { background: var(--paper); border: 1px solid var(--g200); border-radius: 8px; padding: 1.25rem 1.5rem; margin: 1.5rem 0; }
.toc ol { margin: 0.5rem 0 0 1.25rem; }
.toc li { margin: 0.4rem 0; }
.toc a { color: var(--clay-d); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
```

### Timeline
```css
.timeline { position: relative; padding-left: 2rem; margin: 1.5rem 0; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: var(--g200); }
.timeline-item { position: relative; margin-bottom: 1.5rem; }
.timeline-item::before { content: ''; position: absolute; left: -2rem; top: 4px; width: 14px; height: 14px; border-radius: 50%; background: var(--clay); border: 2px solid var(--ivory); }
.timeline-date { font-size: 0.8rem; color: var(--g500); font-weight: 600; }
.timeline-body { font-size: 0.92rem; }
```

## Color Semantics
| Token | Hex | Used For |
|-------|-----|----------|
| `--ivory` | `#FAF9F5` | Page background |
| `--paper` | `#FFFFFF` | Cards, TOC, stat cards |
| `--slate` | `#141413` | Body text, primary headings, verdict bg |
| `--clay` | `#D97757` | Accent (stat numbers, callout borders, timeline dots) |
| `--clay-d` | `#B85C3E` | Clay tag text, TOC links |
| `--oat` | `#E3DACC` | h2 bottom border, table header border |
| `--olive` | `#788C5D` | Good callout border, green tags |
| `--g100` | `#F0EEE6` | Table header bg, callout bg, code bg |
| `--g200` | `#E6E3DA` | Card/stat borders, table cell borders |
| `--g300` | `#D1CFC5` | Verdict subtitle text |
| `--g500` | `#87867F` | Meta text, stat labels, timeline dates |
| `--g700` | `#3D3D3A` | h3 headings, th text |
