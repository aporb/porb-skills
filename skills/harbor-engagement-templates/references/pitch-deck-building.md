# HARBOR Pitch Deck Building — HTML/CSS/JS Pattern

Self-contained HTML slide deck pattern for HARBOR pitch decks. Uses one file — no build step, no dependencies, deploys to brief.h.porb.dev.

## Architecture

```
deck structure:
  <html scroll-snap container>
    <section class="slide">   ← full-viewport content slide
    <section class="slide">   ← section divider (centered, minimal)
    ...
  JS: keyboard nav + overview mode + slide counter
  CSS: 100dvh, scroll-snap, dark theme, print landscape
```

## CSS Variables (dark HARBOR theme)

```css
:root {
  --h:      #1A3A5C;    /* navy — sections A, D */
  --r1:     #8B3A3A;    /* deep red — section B (The Solution) */
  --b:      #2E5077;    /* steel blue — section C (The Why) */
  --bg:     #1A1A1A;    /* slide background */
  --bg2:    #252525;    /* card background */
  --text1:  #F5F0E8;    /* primary text (warm white) */
  --text2:  #B8B0A0;    /* secondary text */
  --text3:  #707070;    /* tertiary / muted */
  --accent: #C9A84C;    /* amber/gold accent */
  --border: #333333;    /* card border */
}
```

Use section colors for the left accent bar on each content slide (`.eyebrow` background or slide header border). Section dividers use that section's color as background.

## Slide Wrapper

```html
<section class="slide" id="s1">
  <div class="slide-inner">
    <div class="eyebrow">Section Label</div>
    <h2>Slide Title (action headline)</h2>
    ...content...
  </div>
  <div class="footer-meta">Footer attribution or source line</div>
</section>
```

## Section Divider

```html
<section class="slide" style="justify-content:center;">
  <div class="section-divider">
    <div class="eyebrow" style="justify-content:center;">Section B</div>
    <h2>The Solution</h2>
    <p>Transition statement — the presenter reads this aloud to bridge sections.</p>
  </div>
</section>
```

```css
.section-divider { text-align: center; max-width: 600px; margin: 0 auto; }
.section-divider h2 { font-size: 36px; margin-bottom: 16px; }
```

## Content Card Patterns

### Cards (generic content)

```html
<div class="card">
  <h3>Card title</h3>
  <p>Content...</p>
</div>
```

```css
.card { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 20px 24px; margin-bottom: 12px; }
.card.accent-r { border-left: 3px solid var(--r1); }
.card.accent-b { border-left: 3px solid var(--b); }
.card.accent-h { border-left: 3px solid var(--h); }
.card.accent-a { border-left: 3px solid var(--accent); }
```

### Stat/Number display

```html
<div class="stat">
  <div class="stat-num">$1.27M</div>
  <div class="stat-label">ITAR penalty, 2024 (22 CFR §127.10)</div>
</div>
```

```css
.stat { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 20px; text-align: center; }
.stat-num { font-size: 28px; font-weight: 700; color: var(--r1); }
.stat-label { font-size: 11px; color: var(--text2); margin-top: 4px; }
```

### Phase card (for phase detail slides)

```html
<div class="phase">
  <div class="phase-header">
    <span class="phase-num">Phase 1</span>
    <span class="phase-price">$125K</span>
  </div>
  <ul>
    <li>Deliverable one</li>
    <li>Deliverable two</li>
  </ul>
  <div class="phase-time">Weeks 1-8</div>
</div>
```

### Grid layouts

```css
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.card-grid.two { grid-template-columns: repeat(2, 1fr); }
.card-grid.four { grid-template-columns: repeat(4, 1fr); }
@media (max-width: 768px) { .card-grid { grid-template-columns: 1fr; } }
```

### Tables (for competitive positioning, CLIN lists)

```css
table { width: 100%; border-collapse: collapse; font-size: 12px; }
thead th { background: var(--bg2); padding: 8px 12px; text-align: left; font-weight: 600; color: var(--text2); font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
tbody td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
tbody tr:last-child td { border-bottom: none; }
.highlight-cell { background: rgba(201, 168, 76, 0.1); font-weight: 600; }
```

## JavaScript — Keyboard Navigation & Overview Mode

```javascript
const slides = document.querySelectorAll('.slide');
const total = slides.length;

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { closeOverview(); return; }
  if (e.key === 'o' || e.key === 'O' || e.key === 'Escape') { toggleOverview(); return; }
  if (e.key === 'f' || e.key === 'F') { toggleFullscreen(); return; }

  const current = getCurrentIndex();
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'n' || e.key === 'N') {
    if (current < total - 1) goTo(current + 1);
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'p' || e.key === 'P') {
    if (current > 0) goTo(current - 1);
  } else if (e.key >= '0' && e.key <= '9') {
    // Single digit jump — 0 = slide 10, 1 = slide 1, etc.
    const idx = e.key === '0' ? 9 : parseInt(e.key) - 1;
    if (idx < total) { closeOverview(); goTo(idx); }
  }
});

// Two-digit jump: listen for a 2-key sequence
let keyBuffer = '';
document.addEventListener('keydown', (e) => {
  if (e.key >= '0' && e.key <= '9') {
    keyBuffer += e.key;
    if (keyBuffer.length === 2) {
      const idx = parseInt(keyBuffer) - 1;
      if (idx >= 0 && idx < total) { closeOverview(); goTo(idx); }
      keyBuffer = '';
    }
  } else {
    keyBuffer = '';
  }
});

// Overview mode
function toggleOverview() {
  overlay.classList.toggle('active');
  if (overlay.classList.contains('active')) { buildOverview(); }
}

function buildOverview() {
  overlay.innerHTML = '<div class="overlay-grid">' + 
    Array.from(slides).map((s, i) => {
      const sec = getSection(i);
      const h2 = s.querySelector('h2');
      const title = h2 ? h2.textContent : s.querySelector('.section-divider h2')?.textContent || 'Slide ' + (i+1);
      return `<div class="overlay-card" onclick="closeOverview();goTo(${i})" data-idx="${i}">
        <div class="overlay-num">${i+1}</div>
        <div class="overlay-section">${sec}</div>
        <div class="overlay-title">${title}</div>
      </div>`;
    }).join('') + '</div>';
}

function getSection(idx) {
  for (const s of sections) {
    if (idx >= s.start && idx <= s.end) return s.name;
  }
  return '';
}

// Section nav dots
const sections = [
  { name: 'The Case', start: 0, end: 2, color: 'var(--h)' },
  { name: 'The Solution', start: 3, end: 9, color: 'var(--r1)' },
  { name: 'The Why', start: 10, end: 14, color: 'var(--b)' },
  { name: 'The Ask', start: 15, end: 16, color: 'var(--b)' },
  { name: 'Appendix', start: 17, end: 20, color: 'var(--text3)' }
];
```

## Print CSS (Ctrl+P → landscape PDF)

```css
@media print {
  @page { size: landscape; margin: 0; }
  body { scroll-snap-type: none; background: white !important; }
  .slide {
    break-after: page; break-inside: avoid;
    height: 100vh; min-height: 100vh;
    overflow: hidden;
    scroll-snap-align: none;
    display: flex; flex-direction: column; justify-content: center;
    padding: 28px 48px;
    background: white !important;
    color: #141413 !important;
  }
  .slide * { color: #141413 !important; }
  .slide .eyebrow { color: #555 !important; }
  .slide .card { background: #f5f4f0 !important; border-color: #ccc !important; }
  .slide table thead th { background: #eee !important; color: #333 !important; }
  .slide table tbody td { border-color: #ddd !important; }
  .stat-num { color: #8B3A3A !important; }
  .highlight-cell { background: #fff8e0 !important; }
  .nav-hint, .slide-counter, .footer-meta { display: none; }
  .section-divider { break-after: page; }
}
```

## Mobile

- Use `100dvh` not `100vh` — mobile browser chrome hides on scroll, and 100vh jumps on first scroll. `100dvh` accounts for dynamic toolbar.
- Responsive grid: all multi-column layouts collapse to single column at 768px.
- Font sizes: 13-14px body on mobile, 20-24px for h2.

## Section Nav Dots

Bottom-center section indicator showing which section the current slide belongs to. Each section has a dot; the active dot is filled, others are outline. Clickable to jump to section start.

```html
<div class="section-nav" id="sectionNav"></div>
```

```css
.section-nav { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; z-index: 100; }
.section-nav .dot { width: 8px; height: 8px; border-radius: 50%; border: 1px solid var(--text3); cursor: pointer; transition: all 0.2s; }
.section-nav .dot.active { background: var(--accent); border-color: var(--accent); }
```

## Slide Counter

```html
<div class="slide-counter" id="slideCounter">S1 of N</div>
```

```css
.slide-counter { position: fixed; bottom: 20px; right: 24px; font-size: 11px; color: var(--text3); z-index: 100; font-family: var(--mono); }
```

## Deployment

Save to `/data/nextcloud/data/amyn/files/briefings/<slug>-pitch-deck.html`, run Nextcloud scan, deliver link: `https://brief.h.porb.dev/<slug>-pitch-deck.html`
