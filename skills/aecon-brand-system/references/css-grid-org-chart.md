# CSS Grid Org Chart for HTML Slide Decks

Pattern for rendering organizational charts in single-file HTML decks.
Verified working in headless Chrome, handles nested hierarchies (CEO → VPs → reports with different children counts per VP).

## The Problem with Flexbox Org Charts

Flexbox-based org charts (using thin `<div>` elements as connector lines) fail because:
- Columns have different heights when one VP has 3 reports and another has 1
- Percentage-based horizontal bus lines (`left:25%; right:25%`) assume equal column widths
- Auto-placement causes boxes at different vertical levels
- Thin `<div>` connectors at 2px wide are fragile and misalign

## The Solution: CSS Grid with Explicit Rows + Pseudo-Element Connectors

### Grid Template
Use `grid-template-columns: repeat(6, 1fr)` with `grid-template-rows: auto 28px auto 28px auto`.

The 5 rows are: Level 1 box → bus gap → Level 2 boxes → bus gap → Level 3 boxes.

Each element gets explicit `grid-row` and `grid-column` assignments so nothing relies on auto-placement.

### Connector Lines via ::before / ::after

```
Vertical drop from parent:  bottom:-28px; left:50%; width:2px; height:28px;
Horizontal bus:             top:0; left:calc(100%/6); right:calc(100%/6); height:2px;
Vertical rise to child:     top:-28px; left:50%; width:2px; height:28px;
```

Use `background:#B0B0B0` for connector lines — NOT `var(--border)` (#EAEAEA) which is invisible on white backgrounds.

### Layout Pattern (6-column grid)

```
Col:    1     2     3     4     5     6
Row 1:              [ Enzo (3-4) ]
Row 2:  [======== bus line (1-7) =========]
Row 3:  [ Brian (1-2) ] [ Ryan (3-4) ] [ IT (5-6) ]
Row 4:  [bus(1-3)]         [drop(3-4)]
Row 5:  [Amyn(1)] [Eric(2)] [Kelly(3)]
```

- CEO spans cols 3-4 (centered)
- Level 2 nodes each span 2 columns
- Level 3 reports span 1 column each
- Bus lines span the columns they connect

### Verified Working Example

The Aecon FBU SharePoint deck (`aecon-sharepoint-deck-2026-07-01.html` slide 4) uses this exact pattern with:
- 7 boxes across 3 hierarchy levels
- One VP (Brian) has 2 reports, another (Ryan) has 1 report, IT has 0 (dotted-line)
- All boxes horizontally aligned at their respective levels
- Connector lines clearly visible at #B0B0B0

### Visual Verification

Headless Chrome screenshot for verification:
```bash
google-chrome --headless --no-sandbox --disable-gpu \
  --screenshot=/tmp/org_chart.png --window-size=1280,900 \
  'file:///path/to/test.html'
```

Then use `vision_analyze` to confirm: boxes aligned, lines visible, hierarchy correct.

### Why NOT to Use

- SVG paths — CSS variables don't work in SVG context, making theming harder
- JavaScript libraries — violates the "self-contained, no external deps" constraint
- Flexbox with absolute positioning — fragile, breaks on different viewport sizes
