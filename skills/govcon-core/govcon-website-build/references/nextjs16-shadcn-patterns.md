# Next.js 16 + shadcn/ui (Base UI) — Migration Patterns

Next.js 16 bundles newer shadcn/ui that uses **Base UI** primitives instead of Radix UI.
The API changes are breaking and will cause build failures if you use the old patterns.

## Button: `asChild` → `render` prop

```tsx
// OLD (Radix, Next <16)
<Button asChild>
  <a href="/contact">CONTACT</a>
</Button>

// NEW (Base UI, Next 16)
<Button render={<a href="/contact" />}>
  CONTACT
</Button>
```

The `render` prop takes a React element. The child content becomes the button label.
Do NOT nest an `<a>` inside — pass the `<a>` as the `render` prop and put text between
the Button tags.

## Accordion: `type` and `collapsible` props removed

```tsx
// OLD (Radix)
<Accordion type="single" collapsible>

// NEW (Base UI)
<Accordion>
```

The accordion is now a simpler component. No `type` or `collapsible` props.
Items still need `value` props.

## `ssr: false` with `next/dynamic` in server components

Next.js 16 blocks `ssr: false` when using `next/dynamic` directly in a server
component. The error:

```
`ssr: false` is not allowed with `next/dynamic` in Server Components.
Please move it into a Client Component.
```

**Fix:** Move the dynamic import into a separate `'use client'` component. Then import
that client component in the server page normally (no dynamic needed).

```tsx
// ❌ FAILS in server component
const MyComponent = dynamic(() => import('./Component'), { ssr: false });

// ✅ WORKS: Create a wrapper client component
// components/HeroWrapper.tsx:
'use client';
import MyComponent from './MyComponent';
export default function HeroWrapper() { return <section><MyComponent /></section>; }

// app/page.tsx (server component):
import HeroWrapper from '@/components/HeroWrapper';
```

## `metadataBase` for OG images

If you have `opengraph-image.png` in `src/app/`, Next auto-detects it but needs
`metadataBase` to resolve the full URL:

```tsx
export const metadata: Metadata = {
  metadataBase: new URL("https://example.vercel.app"),
  // ...
};
```

Without this, `⚠ metadataBase property in metadata export is not set` appears in build log.

## Google Fonts

No change from prior Next.js — use `<link>` in the `<head>` of `layout.tsx`:

```tsx
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet" />
</head>
```

## Favicon & Icons (App Router conventions)

Files placed in `src/app/` are auto-detected — no `<link>` tags needed:

| File | Auto-detected as |
|------|-----------------|
| `favicon.ico` | classic browser tab icon |
| `icon.png` (any size) | `<link rel="icon">` |
| `apple-icon.png` (180×180) | `<link rel="apple-touch-icon">` |
| `opengraph-image.png` (1200×630) | `<meta property="og:image">` |

Generate with Python/Pillow. The ICO format supports multiple sizes via
`append_images` parameter.
