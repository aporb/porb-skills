# Design Tokens — ivory/clay/slate aesthetic

Used for all HARBOR-facing HTML briefings, charters, and capability statements.

```css
:root {
  --ivory:  #FAF9F5;   /* page background */
  --paper:  #FFFFFF;   /* card backgrounds */
  --slate:  #141413;   /* body text */
  --clay:   #D97757;   /* primary accent — section borders, links, badges */
  --clay-d: #B85C3E;   /* darker clay — hover states, table labels */
  --oat:    #E3DACC;   /* warm neutral (rarely used) */
  --olive:  #788C5D;   /* secondary accent — strategic/product side, success badges */
  --g100:   #F0EEE6;   /* subtle card borders, light dividers */
  --g200:   #E6E3DA;   /* table row borders */
  --g300:   #D1CFC5;   /* card borders, hr rules */
  --g500:   #87867F;   /* muted text, section subtitles */
  --g700:   #3D3D3A;   /* card body text */

  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
}
```

## Typography hierarchy

- **Document title:** `--serif`, 42px, weight 500, letter-spacing -0.015em
- **Section titles:** `--serif`, 26px, weight 500, left border 4px solid `--clay`, padding-left 14px
- **Section subtitles:** `--sans`, 13px, `--g500`, margin-left 18px
- **Card body:** `--sans`, 14px, `--g700`, line-height 1.65
- **Table headers:** `--mono`, 11px, uppercase, letter-spacing 0.06em, white on `--slate`
- **Eyebrow:** `--mono`, 11px, uppercase, letter-spacing 0.12em, `--clay`
- **Badges:** `--mono`, 11px, padding 3px 10px, border-radius 999px, rgba(clay,0.12) bg
- **Callout titles:** `--mono`, 10px, uppercase, letter-spacing 0.10em, `--clay-d`

## Layout conventions

- `.wrap` container: max-width 960px, margin auto
- Section margin-bottom: 56px
- Card: background `--paper`, border 1.5px `--g300`, border-radius 10px, padding 22px 26px
- Card-accent: left border 4px `--clay`, bg rgba(217,119,87,0.04)
- Card-amber: left border 4px #C78E3F, bg rgba(199,142,63,0.05) — for warnings/bus-factor
- Summary strip: CSS grid, 4-5 equal columns, border 1.5px `--g300`, border-radius 12px
- Persona cards: 2-column grid, 18px gap, top border 4px (clay for technical, olive for strategic)
- Proof points: 2-column grid, 12px gap
- Products: 2-column grid, 12px gap, each card with product-name (mono, 12px, 600 weight) + tag badge + desc + link
- Table rows: `--g200` bottom border, last row no border. First column: weight 600, `--clay-d`, whitespace nowrap, width 200px.
- Section margins: 56px bottom
- hr.rule: border-top 1px solid `--g300`, margin 0 0 22px

## Print

```css
@media print {
  body { background: white; padding: 0; }
  .wrap { max-width: 100%; }
  section { page-break-inside: avoid; }
}
```

## No dark mode

Light mode only. No toggle. The ivory background is the brand.
