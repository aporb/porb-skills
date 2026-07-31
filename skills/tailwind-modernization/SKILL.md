---
name: tailwind-modernization
description: Modernize existing Tailwind projects with design tokens, dark mode, animations, and component redesign.
version: 1.0.0
author: Hermes Agent
tags: [tailwind, css, design-system, dark-mode, nextjs, react, dashboard, animation]
triggers:
  - modernize the dashboard
  - redesign this UI
  - update the design
  - make this look modern
  - design overhaul
  - tailwind upgrade
  - dark mode
  - design tokens
  - refresh the look
  - make it look better
  - modernize this page
  - redesign the components
tier: A
---

# Tailwind Design Modernization

Use when upgrading a functional-but-flat Tailwind project into a modern design system with tokens, dark mode, animations, and component polish. Covers both greenfield setup and in-place component redesign.

**Reference files:** `references/tailwind4-patterns.md` (advanced patterns), `references/globals-template.md` (complete globals.css template with animations, dark mode, and design tokens).

## Before Starting

Check whether the project is standalone HTML or an existing repo with a framework:

- **Standalone HTML** → use `claude-design` + `popular-web-designs` instead
- **Existing Next.js/React/Tailwind repo** → use this skill
- **Design token spec authoring** → use `design-md`

## Phases

### Phase 1: Foundation — Design Tokens + Dark Mode

**In `globals.css` (Tailwind 4):**

1. Define CSS custom properties for the full palette in `:root`, then mirror in `.dark`:

```css
@import "tailwindcss";

@variant dark (&:where(.dark, .dark *));

:root {
  --background: #f8f6f3;
  --foreground: #171717;
  --card: #ffffff;
  --card-border: #e5e2dd;
  --muted: #78716c;
  --muted-bg: #f0ede8;
  /* brand colors, section accent colors */
}

.dark {
  --background: #0f172a;
  --foreground: #e2e8f0;
  --card: #1e293b;
  --card-border: #334155;
  --muted: #94a3b8;
  --muted-bg: #1e293b;
}
```

2. Map custom properties into Tailwind 4's `@theme inline` to create utility classes:

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-border: var(--card-border);
  --color-muted: var(--muted);
  --color-muted-bg: var(--muted-bg);
  /* brand, accent, section colors */
}
```

3. Apply to `body`:

```css
body {
  background: var(--background);
  color: var(--foreground);
  transition: background-color 0.3s ease, color 0.3s ease;
}
```

**In `layout.tsx` (Next.js):**

Add dark mode prevention flash script in `<head>`:

```tsx
<html lang="en" suppressHydrationWarning>
  <head>
    {/* Safe: static inline script, no user input */}
    <script dangerouslySetInnerHTML={{ __html: `
      try {
        const t = localStorage.getItem('dark-mode-key');
        if (t === 'true' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
          document.documentElement.classList.add('dark');
        }
      } catch {}
    `}} />
  </head>
  <body className="min-h-screen antialiased">...</body>
</html>
```

**In `Header.tsx`:** Dark mode toggle reads/writes `document.documentElement.classList` and `localStorage`. Use `useRef` to batch initial mount state reads and avoid the `react-hooks/set-state-in-effect` lint rule:

```tsx
const mountedRef = useRef(false);
useEffect(() => {
  if (!mountedRef.current) {
    mountedRef.current = true;
    setDark(document.documentElement.classList.contains("dark"));
    setMounted(true);
  }
}, []);
```

### Phase 2: Component Redesign

**Header:** Use `backdrop-blur-lg` + semi-transparent background for glass effect. Use pill-shaped nav links with active state. Include dark mode toggle in the nav bar.

**SectionCard:** Replace uniform card styling with per-section accent. Use left-border accent bar (`absolute left-0 top-0 bottom-0 w-[3px]`), multi-layer shadow tokens, hover lift, color-coded by section name.

**Feedback components:** Add scale transitions on vote (scale-110 on selected), toast confirmation messages with `animate-fade-in`, and staggered star-fill animations for ratings.

**Loading/empty/error states:** Every component should handle all states with animation. Use gradient backgrounds for state banners, animated spinners, and empty-state illustrations (emoji + text).

**Brief/section views:** Apply staggered entrance animations using inline `animation-delay` (50-80ms increments per card). Group items with hover transitions on headlines. Use color-coded sentiment badges.

### Phase 3: Charts (Recharts)

When adding charts to an existing page:

1. Install: `npm install recharts`
2. Import only what's used: `{ BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell }`
3. Match the design system by setting Tooltip `contentStyle` to CSS custom properties:

```tsx
contentStyle={{
  background: "var(--card)",
  border: "1px solid var(--card-border)",
  borderRadius: "8px",
  fontSize: "12px",
}}
```

4. Use stacked bar charts for upvote/downvote or section breakdown; use donut pie charts for distribution; add inline legends below charts.

### Phase 4: Build + Lint

After all changes:
1. `npm run build` — verify zero compilation errors
2. `npm run lint` — fix any warnings, especially:
   - **Unused imports** — remove any chart components not actually used
   - **`set-state-in-effect`** — wrap in `queueMicrotask()` or batch with `useRef` guard

**Pitfall: `react-hooks/set-state-in-effect`**

Setting state synchronously inside `useEffect` triggers this lint error in React 19/Next.js 16. Fixes:

- **For initial mount state** (dark mode detection): Use `useRef` guard to batch the first-effect setState calls
- **For fetch-driven state** (loading/error): Wrap in `queueMicrotask(() => { setLoading(true); setError(null); })` before the fetch

### Phase 4.5: Framer Motion Animation Infrastructure

When the user wants "things moving everywhere" or "Apple product page" level polish, Framer Motion (now `motion`) is the standard. Install with `npm install framer-motion`.

**Reference:** `references/framer-motion-patterns.md` contains the full set of reusable animation infrastructure components (ScrollProgress, CursorGlow, GradientOrbs, MotionSection/MotionItem stagger system, SplitText, Parallax). Copy these as starter files — they are designed to be dropped into any Next.js + Tailwind project.

**Critical patterns to always include:**

1. **ScrollProgress bar** — thin gradient bar at top, `useScroll` + `useSpring` for smooth fill
2. **Hero parallax** — `useScroll` with `target: ref`, `useTransform` for y/opacity/scale on scroll
3. **Staggered reveals** — `whileInView` with `viewport={{ once: true }}` and staggered `delay` per item
4. **Glassmorphism navbar** — `backdrop-filter: blur(20px)` + semi-transparent bg, transitions on scroll
5. **Active section tracking** — IntersectionObserver with `rootMargin: "-40% 0px -40% 0px"` to highlight nav item for current section
6. **Cursor spotlight** — fixed radial gradient div that follows mouse, disabled on touch devices
7. **Gradient orbs** — absolutely positioned blurred circles with `animate` loop for slow drift

**Always respect `prefers-reduced-motion`:** Wrap every animated component with `useReducedMotion()` check that returns static JSX when true.

### Phase 5: Build + Lint + Verify

After all changes:
1. `npm run build` — verify zero compilation errors
2. `npm run lint` — fix any warnings
3. Check for placeholder text: `grep -ri "lorem\|placeholder\|sample content" --include="*.tsx" app/`
4. Deploy verification: `curl -o /dev/null -s -w '%{http_code}' <url>` should return 200
5. Browser console check: verify computed `opacity` of key elements is `"1"` (not stuck at 0)
6. Dark mode toggles without flash
7. All components render in both themes
8. Animations respect `prefers-reduced-motion`

## Critical Pitfalls

### ⚠️ The "Invisible Content" Bug — CSS Reveal Classes Without Triggers

**Symptom:** Content is in the DOM (visible in snapshot, console confirms text content) but appears as blank space to the user. The user sees the page structure but no text.

**Root cause:** A component uses a CSS class like `.reveal { opacity: 0; transform: translateY(24px); }` for scroll-triggered animation, but there is no IntersectionObserver (or equivalent) to add the `.visible` class that sets `opacity: 1`. The content starts invisible and stays invisible.

**How this happens:** You copy the reveal pattern from a `SectionWrapper` component that has an observer, but use it in a standalone component (like `Hero`) that does NOT have the observer. The class works in one context but not the other.

**Fix:** Every component using `.reveal` or `opacity: 0` initial states MUST have its own IntersectionObserver OR use Framer Motion's `whileInView` (which handles this internally). Add a safety fallback timer:

```tsx
useEffect(() => {
  const reveals = el.querySelectorAll('.reveal');
  reveals.forEach(c => observer.observe(c));
  // Safety: force visible after 300ms if observer hasn't fired
  const fallback = setTimeout(() => {
    reveals.forEach(c => c.classList.add('visible'));
  }, 300);
  return () => { observer.disconnect(); clearTimeout(fallback); };
}, []);
```

**Detection:** After deploying, run a browser console check:
```js
JSON.stringify({
  reveal_count: document.querySelectorAll('.reveal').length,
  visible_count: document.querySelectorAll('.reveal.visible').length,
  h1_opacity: getComputedStyle(document.querySelector('h1')).opacity
})
```
If `visible_count < reveal_count` or `opacity !== "1"`, you have this bug.

**Prevention:** Prefer Framer Motion `whileInView` over manual CSS reveal classes — it handles the observer internally and eliminates this entire class of bug.

### ⚠️ Framer Motion TypeScript: `Variants | null` vs `Variants | undefined`

**Symptom:** Build fails with `Type 'Variants | null' is not assignable to type 'Variants | undefined'`.

**Cause:** React Context returns `null` as default, but Framer Motion's `variants` prop expects `Variants | undefined`.

**Fix:** Coalesce with `?? undefined`: `<motion.div variants={variants ?? undefined}>`.

### ⚠️ Vercel Production Deploy: Alias May Not Auto-Update

**Symptom:** `vercel --yes --prod` deploys successfully, but the canonical alias URL (e.g., `personal-portfolio-wheat-eta.vercel.app`) still points to the old deployment.

**Fix:** Manually update the alias:
```bash
vercel alias set <new-deployment-url> <canonical-alias>
```

### ⚠️ `className` vs `class` Typo in TSX

**Symptom:** Build fails or component silently renders without styles. Common when hand-writing JSX quickly.

**Cause:** Writing `class=` instead of `className=` in React/TSX files. TypeScript may not catch this depending on config.

**Fix:** Always use `className` in TSX. After writing components, grep-check: `grep -rn 'class=' --include='*.tsx' app/ | grep -v className`
