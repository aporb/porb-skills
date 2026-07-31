# HTML Slide Deck Methodology Research

## Date: 2026-07-01
## Context: Researched reveal.js, Slidev, Spectacle, CSS-only approaches, and consulting-firm design patterns to improve Aecon SharePoint deck.

---

## 1. Framework Landscape

| Approach | What it is | Best for | Single-file? |
|---|---|---|---|
| **reveal.js** | JS framework, `<section>` slides, full nav engine, themes, plugins | Polished decks you'll maintain & re-skin; de-facto standard | Yes (CDN or vendored JS/CSS) |
| **Slidev** | Markdown + Vue + Vite; dev-oriented, HMR, code-first | Tech talks, code-heavy decks, devs who live in Markdown | No — needs build step |
| **Spectacle** (Formidable) | React-component deck library | React shops wanting programmatic slides | No — build step |
| **CSS-only / scroll-snap** | Pure HTML+CSS, JS only for counter/keyboard | Portable single-file deliverables, email-able, zero deps, PDF-via-print | Yes, natively |

**Conclusion:** CSS-only/scroll-snap is the correct choice for consulting deliverables that must open anywhere (SharePoint, email, locked-down GCC High AVD) with no build step and no external scripts.

---

## 2. Feature Checklist (table stakes from reveal.js + Slidev)

1. **Keyboard navigation** — ←/→/↑/↓, Space, Home/End
2. **Slide counter** — `current / total`
3. **Progress indicator** — bar or dots
4. **Overview mode** — `o`/`Esc` to see all slides at a glance, click to jump
5. **Fragments / staged reveals** — bullet-by-bullet build-up
6. **Speaker notes** — `s` opens presenter view; notes per slide
7. **Fullscreen** — `f` → `requestFullscreen()`
8. **Touch/swipe nav** for mobile/tablet
9. **PDF export** — `?print-pdf` query + Chrome print; or `@media print` with `page-break-after:always`
10. **Scroll-snap** — `scroll-snap-type: y mandatory` + `scroll-snap-align:start` + `scroll-snap-stop:always`
11. **Deep links / `#slide-id`** for sharing a specific slide; survives refresh
12. **Reduced-motion respect** — `@media (prefers-reduced-motion: reduce)`

---

## 3. The Single Highest-Leverage CSS Pattern: Scroll-Snap

```css
html {
  scroll-snap-type: y mandatory;
  overflow-x: hidden;
}
.slide {
  height: 100vh;       /* or 100dvh for mobile */
  height: 100dvh;      /* dynamic viewport — fixes iOS URL bar clipping */
  scroll-snap-align: start;
  scroll-snap-stop: always;  /* prevents skipping slides on fast scroll */
}
```

This is *the* technique that makes a pure-CSS deck feel like a real presentation: every wheel notch settles exactly on one slide.

---

## 4. Performance: IntersectionObserver over Scroll Listeners

Manual scroll handlers that call `getBoundingClientRect()` on every slide per scroll event are O(n) and jank on large decks. Replace with:

```javascript
const observer = new IntersectionObserver(function(entries){
  entries.forEach(function(entry){
    if(entry.isIntersecting){
      const idx = Array.from(slides).indexOf(entry.target);
      if(idx !== -1 && idx !== currentIndex){
        currentIndex = idx;
        updateProgress();
      }
    }
  });
}, { threshold: 0.6 });

slides.forEach(function(slide){ observer.observe(slide); });
```

O(1) per slide change, browser-native, no polling.

---

## 5. Accessibility Requirements for Compliance Audiences

1. `role="region"` + `aria-label="Slide N of M: <title>"` on each `<section class="slide">`
2. `aria-live="polite"` on the slide counter
3. `@media (prefers-reduced-motion: reduce)` to disable smooth-scroll and transitions
4. `<table>` accessibility: `<caption>` and `<th scope="col">`
5. Color contrast: verify ALL text/background pairs meet WCAG AA (4.5:1 for normal text)
6. Decorative glyphs (✓/✗) need `aria-label` or visually-hidden text

---

## 6. Consulting-Firm Design Patterns → HTML Translation

| Consulting pattern | HTML implementation |
|---|---|
| **Action-title** — full-sentence takeaway as title, not topic label | `h2` is a complete sentence; topic moves to eyebrow above |
| **"So what" synthesis box** | `.takeaway` class with accent left-border |
| **Data with source line** | `.footnote` with mono font, gray color |
| **One key message per slide** (pyramid principle) | Single bolded takeaway per dense slide |
| **Tight, gridded density** | CSS grid layouts — consulting decks pack info |
| **Inverted/dark "decision" slide** | Reserve dark background for the call-to-action slide |

---

## 7. Mobile Viewport Fix

iOS browser-chrome `100vh` bug causes bottom content to hide behind URL bar. Use:
```css
height: 100vh;      /* fallback */
height: 100dvh;     /* dynamic viewport — preferred */
```

---

## 8. Print Hardening

```css
@media print {
  @page { size: landscape; margin: 0; }
  html { scroll-snap-type: none; }
  .slide {
    height: 100vh;
    page-break-after: always;
    page-break-inside: avoid;
    overflow: visible;
  }
  .progress-bar-container, .slide-counter, .nav-hint { display: none; }
}
```

---

## 9. Eval Gate Pattern (for quality verification before delivery)

Run a Python script that checks:
- HTML tag balance (open/close `<section>`)
- Correct slide count
- No emojis (regex scan for Unicode emoji codepoints)
- Brand colors present, old colors absent
- Correct person titles
- Org chart relationships (e.g., "Eric reports to Brian")
- Key features present (scroll-snap, IntersectionObserver, ARIA, etc.)
- Self-contained (no `<link>` or external `src="http"`)

Output: PASS/FAIL per check, then ALL CHECKS PASSED / SOME FAILED.
