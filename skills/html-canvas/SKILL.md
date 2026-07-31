---
name: html-canvas
description: "Build Thariq-style self-contained interactive HTML canvases for Hermes-human collaboration — single-file, all CSS/JS inline, HARBOR branded."
tags: [html, canvas, thariq, harbor, interactive, collaboration]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# HTML Canvas — Interactive Hermes Collaboration Surfaces

Build single-file, self-contained HTML documents that serve as interactive workspaces where Hermes and Amyn think through problems, build plans, triage work, and code together. Inspired by Thariq Shihipar's "Unreasonable Effectiveness of HTML" thesis (Anthropic/Claude Code team).

## When to use

- Amyn asks for an "interactive canvas" or "interactive HTML" to work together on
- Amyn asks for "plans" or "planning" output. Unless the user explicitly asks for markdown, planning deliverables are HTML — multi-page doc set in a repo's docs/ when the plan spans multiple concerns, single-file canvas when it's one coherent topic. This is a standing preference: "html plans not md files." Do NOT default to README.md or inline markdown for planning output.
- Amyn asks for a "microsite" or "client-facing" deliverable. Any external-facing HTML for a prospect, client, partner, or public audience MUST use the Thariq pattern (light theme, ivory bg, sticky nav, stat strips, card grids). Do NOT build dark-theme hero-section microsites — those are claude-design territory and the user will push back. The "microsite" keyword is a first-class trigger for this skill. If the microsite is part of the portfolio (under portfolio/{company}/), use multi-file with shared styles.css. Reference: references/acd-microsite-example.md for a corrected real-world build.
- Building a planning/triage/editor tool that Hermes generates and Amyn manipulates
- Creating throwaway editors, tuners, boards, or diagrams as single HTML files
- Any prompt mentioning Thariq-style HTML or the `html-comms` project
- **Writing HTML planning/spec docs into a project repo's `docs/` folder.** Even when the artifact is a multi-file doc set rather than a single canvas, the visual language MUST be Thariq: ivory `#FAF9F5` bg, navy `#080c14` headings, gold `#d4a853` accent, Georgia serif headings, sticky toolbar, Copy Outline button, checklist persistence on open-question sections. Use the multi-file pattern below — do not invent an ad-hoc HARBOR-styled CSS.
- **Building a scientific / experimental research report** with detailed methodology, results tables, and findings blocks. When the user asks for a "scientific briefing", "research findings", or to "take the persona of a data scientist / AIML scientist", use `references/scientific-reporting.md` for the data-scientist tone, stat cards, finding blocks, and performance budget tables. This pattern is the opposite of terse — it demands thoroughness, methodology sections, and open-problems closure.
- **Building a playbook / operating system guide** for a solo business, coaching practice, or founder. When the user asks for a "business operating system", "solo business guide", "coaching playbook", "how to run a [type] business", or mentions showing someone their business functions, roles, calendars, and tools in one visual canvas. Use `references/playbook-canvas-pattern.md` for the radial SVG function diagram, color-coded calendar grid, role cards with colored borders, business size toggle, and coaching flow patterns. Reference: `solo-business-canvas.html` (70KB, 5 tabs).

## Project home

`~/Documents/_Projects/html-comms/`

Contains:
- `thariq-repo/` — cloned from `ThariqS/html-effectiveness` (20 example files + index)
- `thariq-examples/` — separately pulled copies of the 20 HTML files
- Generated canvas files go here

## Thariq design patterns (from gallery study)

All 20 examples share these conventions:

1. **Single file, zero dependencies** — all CSS in `<style>`, all JS in `<script>`, no external assets
2. **CSS custom properties** for theming — `--ivory`, `--slate`, `--clay`, `--oat`, `--olive`, grays, font stacks
3. **Three font families** — serif for headings, sans for body, mono for labels/code
4. **Sticky toolbar** with primary action button (copy/export) + ghost reset button
5. **`contenteditable`** for text editing (prompt tuner), native drag-and-drop for board interactions
6. **Max-width ~1180px**, generous padding (48–64px vertical, 32px horizontal)
7. **Border-radius 12px** on panels, `999px` on buttons/pills (pill shape)
8. **1.5px borders** everywhere — not 1px, not 2px
9. **Gray-200 (#D1CFC5)** for borders, **gray-50 (#F0EEE6)** for subtle fills
10. **Collapsible/expandable** sections for progressive disclosure

### Gallery categories (20 examples)

```
Exploration & Planning: 01-code-approaches, 02-visual-designs, 16-implementation-plan
Code Review:           03-code-review-pr, 04-code-understanding, 17-pr-writeup
Design:                05-design-system, 06-component-variants
Prototyping:           07-prototype-animation, 08-prototype-interaction
Diagrams:              10-svg-illustrations, 13-flowchart-diagram
Decks:                 09-slide-deck
Research:              14-feature-explainer, 15-concept-explainer
Reports:               11-status-report, 12-incident-report
Custom Editors:        18-triage-board, 19-feature-flags, 20-prompt-tuner
```

### Key interaction patterns

- **Triage board** (`18`): HTML5 drag-and-drop, column state in JS array, "Copy as markdown" export
- **Prompt tuner** (`20`): `contenteditable` with slot highlighting via `{{var}}` regex, live preview re-render, caret save/restore
- **Implementation plan** (`16`): Milestone timeline with dot/line SVG, data-flow diagram inline, collapsible sections

## HARBOR brand kit

HARBOR uses TWO theme variants. **Light is the default** (user preference: HTML/docs always light theme).

### Brand assets (see `references/harbor-brandkit.md`)

The complete HARBOR brandkit lives in the 2026_books repo:
- Brandkit CSS tokens: `admin/v2/assets/harbor.css`
- Primary logo SVG: `projects/harbor-website/public/images/harbor-govcon-logo.svg`
- Social/presentation logo variants: `operations/practice/brand/logos/social/`
- Full reference with logo embed code: `references/harbor-brandkit.md`

**When building a client-facing microsite:** use the HARBOR light theme tokens + the actual HARBOR GovCon logo SVG (embedded inline) — not the Thariq ivory/navy/gold palette. Blue (#3B82F6) is the HARBOR accent, not gold (#d4a853). The font stack is system-ui sans-serif for body, Georgia serif for headings.

### Light theme (default — planning docs, specs, briefings)

```css
:root {
  --ivory: #FAF9F5;
  --navy: #080c14;
  --gold: #d4a853;
  --gold-d: #b88a3e;
  --oat: #E8E4DC;
  --gray-50: #F5F3EF;
  --gray-200: #D9D7CF;
  --gray-400: #A39C94;
  --gray-700: #5A564F;
  --white: #ffffff;
  --r: 6px;
  --shadow: 0 1px 3px rgba(8,12,20,.06), 0 2px 12px rgba(8,12,20,.04);
  --serif: Georgia, 'Times New Roman', serif;
  --sans: system-ui, -apple-system, 'Segoe UI', sans-serif;
  --mono: 'SF Mono', Menlo, Consolas, monospace;
}
body { background: var(--ivory); color: var(--gray-700); }
```

### Dark theme (dashboards, operational views, mission control)

```css
:root {
  --harbor-bg:     #080c14;
  --harbor-gold:   #d4a853;
  --harbor-surface: #0f1520;
  --harbor-border: #1e2a3a;
  --harbor-text:   #e8e6e1;
  --harbor-muted:  #7a8a9e;
}
```

### Tabbed planning canvas pattern

**For ANY multi-section spec, planning doc, brainstorm, or build plan — even a multi-FILE doc set in a repo's `docs/` directory — the planning-canvas pattern is the DEFAULT, not an option.** Use `references/planning-canvas-pattern.md`:
- Sticky toolbar with tab buttons + export action (one toolbar per file when multi-file; single toolbar across tabs when single-file)
- `localStorage` tab persistence (single-file) OR filename-keyed active-tab highlighting (multi-file)
- Checklist persistence (`data-key` + JSON in localStorage) — non-negotiable for open-questions / acceptance-criteria / ratification sections
- "Copy Outline" export button — the defining feature that makes a doc a collaboration surface vs static page
- Kv grids, data tables, badges, flow columns, spec grids
- See `sbir-datascope-full-spec.html` and `sbir-connect-platform-canvas.html` for single-file reference implementations
- For multi-file repos: shared `_harbor.css` + `_canvas.js` linked from each doc is the right call; the single-file rule bends because git-diff friendliness wins. Each doc still gets the full toolbar + header + main pattern.

### PITFALL: Building planning docs without interviewing the user first

**Symptom:** User asks for a plan, you research and build a doc set, but the user pushes back because core decisions (build scope, funding path, timeline, team structure) were guessed rather than asked. The docs are well-structured but answer the wrong questions.

**Fix:** When the task is a STRATEGIC planning doc (not a spec doc for an already-decided build), interview the user FIRST with `clarify` before building. Ask the 5-10 strategic questions that shape everything downstream. Capture answers as persistent checklists in the hub page. Then build the doc set around actual decisions, not assumptions. The 10-question session in this conversation (Drone Dominance planning, June 2026) is the reference pattern: 10 clarify calls covering identity, build scope, TRL, funding path, timeline, team, environment, AI thesis, deliverables → 6-page HTML doc set built from actual answers.

**Pitfall:** defaulting to ad-hoc HARBOR-ivory styling instead of the canvas pattern. When a task involves building a planning-doc set (vision + spec + architecture + roadmap + brainstorm, etc.) it is *the* planning-canvas use case. Do NOT invent a new stylesheet from scratch with chunky navy heroes, 4px radii, 2px borders, and 920px max-width. Load `references/planning-canvas-pattern.md` first, copy the token block (ivory `#FAF9F5`, navy `#080c14`, gold `#d4a853`, oat `#E8E4DC`, `--r: 6px`, 1.5px borders, 1040-1180px max-width), wire the toolbar + Copy Outline + checklist JS, then write content. The aesthetic difference vs ad-hoc HARBOR styling is large and visible — vision_analyze will flag it as "not the Thariq design language" and the user will (correctly) push back.

**Pitfall: vision_analyze can misread an unstyled-looking screenshot of a correctly-styled page.** If a page just loaded but the browser snapshot was taken before the stylesheet finished applying (or a stale cache returned the prior render), vision will report "raw form inputs", "no oat highlight", "no gold accents" even when JS-console inspection (`Array.from(document.styleSheets).map(s=>s.href)`, `getComputedStyle(document.body).backgroundColor`) confirms everything is loaded and computed correctly. Trust JS console truth over vision for CSS verification. Cache-bust with `?v=N` query string and re-snap if vision flags style failures that the console disproves.

## Hermes integration (question 5 — evolving)

The canvas is a collaboration surface between Hermes and Amyn. Open questions being figured out:
- Hermes generates the initial HTML from a prompt/conversation
- Amyn interacts with it (drag, edit, configure) in browser
- Export back: "Copy as markdown" or "Copy as diff" or "Copy as prompt" buttons
- Could be served via `python3 -m http.server` bound to Tailscale IP
- Or opened directly as file:// in browser

The canvas should feel like a shared whiteboard that happens to be a single HTML file.

## Workflow

1. **Identify the canvas type** from the task: triage board, prompt tuner, implementation plan, exploration/comparison, report, etc.
2. **Study the matching Thariq example** in `thariq-repo/` for interaction patterns and layout
3. **Adapt** the pattern with HARBOR brand kit (dark theme, gold accents)
4. **Build** as single self-contained HTML file with all CSS/JS inline
5. **Include export buttons**: Copy as markdown, Copy as prompt, or whatever output format makes sense
6. **Deliver** to `~/Documents/_Projects/html-comms/`
7. **If Tailscale access needed**: serve with `python3 -m http.server PORT --bind 100.66.165.40`

## Slide Deck Pattern

For presentation decks (slides with keyboard navigation for meetings/conferences), see `references/slide-deck-pattern.md`. Covers full-bleed aesthetic rules (16:9, alternating backgrounds, dramatic typography), the critical DOCUMENT vs. DECK distinction, reusable components, navigation, and the rule: always show Amyn's full product portfolio (5 live products + HARBOR + THE DAILY) when building external-facing materials. **If a \"deck\" looks like a white card on a pale gray background, it's wrong — rebuild it as full-bleed slides.**

**The dead giveaway you did it wrong:** if any `<pre>` block in your HTML contains box-drawing characters (anything in U+2500–U+257F), you produced ASCII art instead of an SVG. Rebuild it as inline SVG.

### Pitfall: "Briefing" and "microsite" deliverables need multi-page structure, not single-canvas

A multi-topic deliverable (covering multiple distinct themes, phases, or audiences) warrants **multi-page navigation** (a nav bar with anchor links to per-page HTML files in a shared directory, e.g. `docs/index.html` + `docs/topic-1.html` + `docs/topic-2.html` + `docs/_harbor.css`), NOT a single file with 5+ tabs. Single-canvas-with-tabs is correct when the content is one coherent topic viewed from different angles. Multi-file is correct when content genuinely splits into separate concerns.

Shared CSS file convention: all pages link `href="_harbor.css"` in the same directory. All pages share the same nav bar at the top. Each page's nav link is highlighted via inline JS that matches `location.pathname.split('/').pop()` to the href.

### Pitfall: image-analysis fallback when vision_analyze tool isn't in the toolset

When `vision_analyze` isn't available in the current toolset, use OpenAI GPT-4o-mini vision via direct API call. See `references/image-analysis-fallback.md` for the exact pattern (read file → base64 encode → POST to api.openai.com with API key from `~/.hermes/.env` OPENAI_API_KEY entry).

## Related skills

- **claude-design** — general design-artifact skill (visual, aesthetic, from-scratch HTML artifacts). Use `html-canvas` when the artifact is an *interactive collaboration surface* (triage board, prompt tuner, planning canvas), not just a visual design. Use `claude-design` for landing pages, decks, visual explorations.
- **youtube-content** — source of the Thariq thesis video transcript

## Pitfalls

- Do NOT split into multiple files — the whole point is single-file portability (exception: multi-doc planning repos — see `references/multi-doc-planning-repo-pattern.md`)
- Do NOT use external CDNs or font links — must work offline
- Do NOT forget the export/copy button — the canvas must produce usable output
- macOS `pip` doesn't exist; use `pip3` for any Python dependency installs
- `yt-dlp --dump-json | python3` requires user approval (pipe-to-interpreter security scan) — pre-warn or use temp file approach

### Pitfall: building playbook/OS canvases without fresh research

When building or improving a solo business / coaching / operating-system canvas, do NOT write from the model's training data alone. The user expects RAG-enriched content: current stats, real tool pricing, research-backed scheduling advice, and industry data. Before touching the HTML, run 3-4 targeted web_search queries for domain stats, tool comparisons, and best practices. Extract the top articles. Inject findings through targeted patches (not full rewrites). The `solo-business-canvas.html` enrichment session (June 2026) demonstrated this: 8+ external sources → 31% content density increase across 5 patches. See `references/playbook-canvas-pattern.md` → RAG-Enrichment Workflow for the full 4-step pattern.

### Pitfall: shipping a "generic deliverable with a name dropped in" — personalization is a workflow, not a find-replace

**Symptom**: User asks for a deliverable "for X" or "for Y's practice" and you produce a generic template with the name pasted into the title. User pushes back with "is this customized for them?" / "do not be lazy" / "act like an agent orchestrator." The deliverable reads like a stock template with one swap — same generic functions, same generic pricing, same generic tooling. The user can tell.

**Fix — run the personalization workflow before writing HTML**:

1. **Profile lookup first.** Before writing any HTML, search the user's repos for an existing profile of the named person. Common locations: `~/Documents/coaching-wondrinn/profiles/<name>.md`, `~/repos/<repo>/clients/<name>.md`, `~/repos/<repo>/entities/<name>.md`. These are gold — 1000+ lines of structured profile data beats any model-knowledge guess. Read the full file with `read_file(offset=, limit=)` since they're often large.
2. **Gap analysis against the current deliverable.** If there's an existing version of the deliverable, run a 12-item gap audit: identity, diagram interactivity, offerings, methodology, session structure, roles, calendar, pricing, tools, voice/quote density, spiritual/cultural layer, em-dash discipline. For each item: current state, what's wrong, the specific fix.
3. **Customize vocabulary to the named person's terminology.** The biggest tell of a generic deliverable is generic vocabulary. If a coach's actual method is called "Present-Space Coaching" and his metaphor is "the compass" — those exact terms must appear. Use `grep -r "<term>"` on the profile to find the canonical vocabulary, then use those terms verbatim. This is the difference between a stock template and a deliverable that feels built FOR the person.
4. **Match pricing to the person's actual positioning, not industry averages.** Industry averages for "coaching" don't exist. The named person has specific pricing evolution (`$5K-3mo → $10K-6mo → $20K-12mo`), specific package types (3/6/12 month containers, not generic "monthly"). Pull these from the profile.
5. **Reference the actual quote library.** Every named person has signature quotes (Rumi, Ram Dass, their own). Pull 4-6 from the profile or session transcripts. Use them in pull-quote blocks with `<cite>` attribution. Zero quotes = generic.
6. **Reference the actual full project lookup before rebuilding.** Then verify the deliverable against `harbor-eval-gate` in dry-run mode. The composite_estimate should clear 0.8 — anything below means you left value on the table.

Real example: June 2026 WONDRINN coaching canvas rebuild took a generic "Solo Business Operating System" from 0.7 → 0.9 by closing 12 specific gaps, mostly by reading the existing `zamir_janmohamed.md` profile and using his actual vocabulary throughout.

### Pitfall: fake interactivity — toggles that look like they do something but don't

**Symptom**: You add a toggle, dropdown, or interactive element that visually responds (button highlights, panel changes) but the data it claims to change doesn't actually change. The user asks "does this actually work?" and the answer is no. Classic example: a "business size" toggle that only changes the bottom annotation text, not the function ownership labels in the diagram.

**Diagnostic — your toggle is fake if:**
- The data displayed is the same across all states (only chrome changes)
- State changes are limited to text/captions, not the actual data structure
- The `setX(state)` function only modifies one element, not the data the labels describe

**Fix**: When you build an interactive element, the JS handler must mutate the actual displayed data, not just adjacent captions. For a "business size" toggle: the handler should rewrite the owner labels per state (YOU → VA → Marketing VA → Bookkeeper), not just toggle a bottom annotation. For a date picker: the displayed values should reflect the picked date. For a filter: the filtered subset should appear, not the same list with a different header.

**Test before shipping**: Click through every state and verify the data, not just the chrome, changed. Run `browser_console` to inspect the DOM after each state change — confirm the relevant element IDs hold new text.

Reference: June 2026 WONDRINN canvas rebuild — the original "size toggle" only changed bottom annotation. After fix, clicking Solo/Retreat-Led/Practice actually rewrites each function's `id="own-{function}"` text and shrinks the center node. The diagram became a real operating model instead of a decoration.

See `references/personalization-workflow.md` for the full customization checklist (identity, methodology, pricing, terminology, interactivity, verification).

### ⚠️ PITFALL: "Briefing" trigger — building HTML for a non-user audience with ad-hoc styling

**Symptom**: User asks for an "HTML briefing" for a family member, colleague, client, or other person who isn't Amyn. You build a functional but visually plain HTML page with ad-hoc CSS (custom color names, emoji bullets, inline styles, no component library). User pushes back: "make sure to use the thariq-examples html-effectiveness styles and examples." You have to rebuild from scratch.

**Root cause**: The word "briefing" didn't trigger any of the existing design-language pathways. "Microsite", "planning canvas", "playbook", "scientific report" all have explicit triggers, but "briefing" was treated as generic HTML. The default for ANY HTML deliverable — briefing, report, summary, guide, one-pager — is the Thariq design language. There is no class of HTML deliverable where ad-hoc styling is correct.

**The rule**: If the output is HTML, it uses Thariq components. Period. The only question is which PATTERN within Thariq (single-file canvas with tabs, multi-file microsite, planning doc set, report with stat tiles). A "briefing" is a single-file tabbed canvas: sticky toolbar with Copy Outline + Print/PDF, stat grid at top, card grid with SVG icons, expandable detail sections, KV grids for structured data, badges for status, checklist with localStorage persistence, highlight/warn/info/good boxes.

**Fix**: When the user says "HTML briefing" or "build an HTML document for X", load this skill FIRST, identify it as a tabbed canvas pattern, copy the CSS token block from `references/planning-canvas-pattern.md`, and build with the full component library from the start. Do not invent ad-hoc CSS classes.

**Real example**: July 2026 estate briefing for Anil (Amyn's father). First version: 16KB with custom `.alert.red`, `.watch-card`, emoji-style numbered circles, no SVG icons, no tabs, no export button. Rejected. Second version: 50KB with full Thariq components (5 tabs, SVG card icons, stat grid, expandable property details, KV grids, badge system, checklist with localStorage, Copy Outline button). Accepted.

**Additional lesson from the same session**: When building a briefing about a legal/financial matter FROM the user TO a family member, the tone must be "from son to father" (or equivalent), not clinical analyst. The briefing gets revised iteratively as the user provides corrections from the family member (WhatsApp messages clarifying the strategy, correcting who lives where). Build the initial briefing with explicit "awaiting confirmation" markers for assumptions about people, addresses, and motivations — then patch aggressively as the principal party provides context. Do NOT lock in adversarial conclusions (e.g., "65-80% probability hostile filing") from document analysis alone without the principal party's explanation.

### ⚠️ PITFALL: Static-HTML-with-HARBOR-colors is NOT a Thariq canvas

**Symptom**: User asks for "Thariq-style HTML" or to "follow the planning-canvas pattern" and you produce static HTML documents with hero blocks, navy gradients, and ivory backgrounds. The output looks branded but lacks every defining property of a Thariq canvas.

**Diagnostic — your output is NOT a Thariq canvas if it lacks any of these:**
1. CSS custom-property token set matching the actual spec: `--ivory: #FAF9F5`, `--navy: #080c14`, `--gold: #d4a853`, `--oat: #E8E4DC`, `--r: 6px`
2. Sticky toolbar at the top with tab buttons + at least one export action button (Copy Outline / Copy as Markdown / Print PDF)
3. `localStorage` persistence for at least one piece of state (active tab, checklist progress, form values)
4. `.wrap` max-width container around `~1040-1180px`
5. 1.5px borders (not 1px, not 2px), 6px radius on panels, 999px or 6px on tab pills
6. Three-font-family discipline: serif headings, sans body, mono code
7. Generous whitespace — sections breathe, not packed
8. A `Copy <something>` action that actually produces useful output for the next tool the user will paste it into

**The dead giveaway**: if your design has a big `<div class="hero">` with a navy gradient background and bottom gold border, you are NOT in Thariq territory. That is `claude-design` territory. Thariq canvases START with the sticky toolbar, not a hero.

### ⚠️ PITFALL: Visual commitment — text-with-styling is NOT beautiful

**Symptom**: You built a Thariq document with correct CSS tokens (ivory bg, navy headings, gold accents) but it uses ASCII diagrams in `<pre>` blocks, flat tables, and no visual variety. The user says "it's not beautiful" or "it doesn't look visually appealing." You rebuild it with minor spacing tweaks and it's rejected again.

**The real problem**: A document that's 80% `<pre>` blocks and `<table>` elements — even with correct CSS — is NOT a Thariq canvas. The visual language REQUIRES SVG diagrams (inline, with fills/strokes/labels), card grids, flow columns, stat tiles, badges, KV grids, and highlight/warn boxes. The difference between "text with HARBOR styling" and "a designed visual briefing" is the FULL component set, not just the CSS tokens.

**Fix**: Before building, study `references/thariq-visual-commitment.md` (the 3-rebuild saga). Build the SVG diagram FIRST, then lay out the content around it. Every major section needs visual variety — cards, badges, icons, stat tiles, KV grids. One `<pre>` block or ASCII diagram in an otherwise rich visual layout is fine. Two is suspicious. Three means you're building the wrong thing. See the working reference at `~/Documents/Briefings/hermes-microsite/index.html` for a page that passed first-time review.

**Reference files:**
- `references/thariq-visual-commitment.md` — The "what beautiful actually means" guide with checklist and failure-signature breakdown
- `~/Documents/Briefings/hermes-microsite/kanban.html` — Reference for a full-page (29 KB) Thariq document with SVG swarm diagram, stat tiles, flow cards, KV grids, cmd-grids, timelines, badges, and highlight boxes

**Fix recipe when you realize partway through:**
1. Stop writing more docs
2. Create `_harbor.css` and `_canvas.js` shared assets (per multi-doc pattern below) OR migrate to single-file canvas
3. Bulk-patch existing docs via a Python script: strip old hero/nav, inject toolbar header, wrap in `.wrap`, add `<main>`
4. Verify in browser via `python3 -m http.server` bound to `127.0.0.1` — do NOT trust vision-tool screenshots alone, which can read stale renders. Use `mcp_browser_console` to JS-inspect `getComputedStyle(document.body).backgroundColor` and check it matches the spec.
5. Render at least one page in browser BEFORE writing more docs — catches missing stylesheet links, broken tab markup, etc.

**Verification one-liner** to run in `mcp_browser_console`:
```javascript
JSON.stringify({
  sheets: Array.from(document.styleSheets).map(s => s.href),
  bg: getComputedStyle(document.body).backgroundColor,
  h1font: getComputedStyle(document.querySelector('h1')).fontFamily,
  tabs: document.querySelectorAll('.toolbar .tab').length,
  active: Array.from(document.querySelectorAll('.toolbar .tab.active')).map(t=>t.textContent),
  checks: document.querySelectorAll('.chk-item input[data-key]').length
})
```
Expect: `bg: "rgb(250, 249, 245)"`, h1font starts with `"Georgia"`, tabs > 0, exactly one active tab matches the current page, checks > 0 if you wrapped any open-questions sections.

### PITFALL: Reversible-drafts pattern when user is absent during design

**Symptom**: User asks for a doc set / plan / spec but goes AFK. You wait for `clarify`, get no answer, decide to bulldoze ahead. You write 13 documents committed to one interpretation. User comes back and reframes the entire problem. Now half your work is wrong and you have to rewrite from scratch.

**Better pattern**:
1. State the decision you're making explicitly in plain text at the top of your reply: "User AFK. Best-judgment decisions: X, Y, Z. Reversible. Proceeding."
2. In the doc set itself, maintain a `brainstorm-session.html` (or equivalent) that captures the REFRAMES that happened, not just the final state. Each reframe gets its own subsection with: what was decided, what user input triggered the reframe, why the prior decision was scrapped.
3. This gives the next agent (and the user) the WHY across reframes, not just the WHAT.
4. Real example from a 2026-05 session: user reframed three times in one conversation ("fleet consolidation" → "one product, reuses fleet back-ends" → "fully standalone, own VPS"). The `brainstorm-session.html` doc tracked all three reframes with `Reframe 1` / `Reframe 2 (scrapped)` / `Reframe 3 (current)` markers. Made the fourth reframe (own VPS) cleanly insertable without confusion.

### PITFALL: Vision tool can read stale snapshots

When verifying a canvas in browser, `mcp_browser_vision` sometimes returns analysis from a previous viewport state — e.g., reports "no sticky toolbar visible" / "page looks unstyled" when the page is actually fine. **Always cross-check with `mcp_browser_console` running JS inspection** before believing a vision-tool failure report. JS inspection of `document.styleSheets`, `getComputedStyle`, and `querySelectorAll` is ground truth; vision is interpretation. Cache-bust the URL (`?v=2`) and re-snapshot if vision and console disagree.

### Pitfall: ad-hoc styling when writing planning docs into a repo

If the task is "write planning HTML docs into `repo/docs/`" (multi-file, not single canvas), the temptation is to invent a fresh stylesheet because "this isn't really a Thariq canvas." DON'T. The visual language is still Thariq. Use shared `_harbor.css` + `_canvas.js` files in the same `docs/` folder so every doc loads them. See `references/multi-file-docs-pattern.md` for the exact CSS/JS to drop in and the bulk-patch recipe. The user WILL notice if the docs use a different palette, a chunky navy hero block, or non-Thariq tab styling. Reference cases: HARBOR Intel planning repo at `~/repos/govcon-intelligence-platform/docs/`.

### PITFALL: Shareable HTML has a higher visual quality bar than internal docs

**Symptom**: User asks for "beautiful HTML", "HTML I can share with a friend", or "visual and appealing so users can digest it" — and you produce something that reads like plain documentation with box-drawing characters in `<pre>` tags and simple tables. User pushes back multiple times ("fix this because it does not look beautiful", "it needs to be beautiful it needs to be HTML that's the whole point").

**Diagnostic — your shareable HTML is NOT high-quality if you used any of these for visual content:**
1. ASCII box-drawing chars (`┌─┐│└─┘`) inside `<pre>` blocks as "diagrams"
2. Plain `<table>` tags without card wrappers, stat tiles, or flow columns
3. Inline `<svg>` not used for architecture diagrams, flow charts, or topology visualizations
4. No card grid, no KV grid, no stat grid, no timeline component anywhere on the page
5. Only one column of content (everything stacked vertically) with no flow-cols

**The distinction**: *Internal* HTML (Amyn reading it in his own browser across sessions) can be a tight planning canvas — toolbar, checklists, tabs, concise content. *Shareable* HTML (friend / client / colleague opening it cold) needs to be **visually self-explanatory** on first load:
- **Architecture diagrams = inline SVG** with boxes, labeled arrows, colored regions. NOT ASCII in `<pre>`. Reference `references/thariq-gallery-patterns.md` → pattern 10-svg-illustrations and 13-flowchart-diagram.
- **Stats at the top** = stat grid of 4 tiles with big numbers + labels + context. First impression.
- **Component cards** = use flow cards with icons (`.card-icon.v`, `.card-icon.g`, `.card-icon.r`, `.card-icon.n`, `.card-icon.b`) for the "what the layers do" sections.
- **Key-value grids** = for config tables, performance budgets, capability comparisons that read as data.
- **Timeline component** = for chronological sequences (release history, project phases, pipeline steps).
- **Tables get wrapped** in `.tbl-wrap` with `overflow-x: auto` so they scroll gracefully on mobile.
- **Badges** = inline `.badge.navy`, `.badge.gold`, `.badge.green`, `.badge.red`, `.badge.blue`, `.badge.purple` to label status / categories inline with text.

**Fix recipe when you realize partway through**: stop, rebuild with the full Thariq component library from `references/planning-canvas-pattern.md` (stat tiles, flow-cols, KV grids, card headers with icons). The SVG diagram is the most impactful single improvement — replace any ASCII architecture drawing with actual inline SVG boxes + labeled arrows.

**Real-world trigger phrases from past sessions**: "build me a beautiful MicroSite", "HTML so users can actually digest it", "save it for sharing with a friend", "it needs to be HTML that's the whole point", "I want it to be visual and appealing". When any of these appear in a request, reach for the FULL component library from the start — don't try a "good enough" version and iterate.

**Contrast with internal planning canvases**: an interactive triage board with contenteditable + a Copy-as-markdown button is a perfect *internal* canvas. The same page handed to a client would feel underproduced. Audience drives the design.

### Pitfall: visually weak HTML when source material is visually rich

**Symptom**: User says "it looks ugly" or "not visually appealing" after you deliver an HTML briefing decoded from an infographic, screenshot, or visually-rich source. The content is comprehensive but the visual design is flat — text-heavy cards, no color energy, ASCII-art boxes where SVG diagrams belong, muted palette when the source was vibrant.

**Root cause**: You built content-first HTML using the shared microsite CSS as a base template, treating the canvas as a document rather than a visual experience. When the source material was a dark-themed infographic with orange/cyan/green accents and strong visual hierarchy, your white-background template with navy text felt wrong even though the content was accurate.

**Fix recipe**:
1. Before writing any HTML, assess the SOURCE's visual energy. Is it dark mode? Vibrant colors? Infographic-style with icons and data visualizations?
2. If the source is visually rich, match its energy — don't force it into the ivory/navy/gold HARBOR theme. Build a self-contained dark-mode or vibrant HTML with inline CSS that echoes the source's palette.
3. Use **SVG diagrams** for any architectural topologies, flow diagrams, or structural relationships — never ASCII `<pre>` art blocks for diagrams in HTML. ASCII is fine for code snippets or command examples only.
4. Cards should have colored icon badges (the card-icon component with `.v`, `.g`, `.r`, `.n`, `.b` classes), not just numbered headers.
5. Stat tiles should use gradient accents matching the source palette, not just navy text.

**Verification**: Open the HTML in the browser. If it looks like a corporate whitepaper when the source was a vibrant infographic, rebuild it. The user should feel the same visual energy as the original.

### PITFALL: Using OpenAI vision API to decode infographics

**Technique**: When the `vision_analyze` tool isn't available or returns poor results (common on complex infographics with small text), use OpenAI's gpt-4o-mini directly via their API with base64-encoded images:

```python
import base64, os
from openai import OpenAI

# Read API key from ~/.hermes/.env
env_file = os.path.expanduser("~/.hermes/.env")
api_key = None
with open(env_file) as f:
    for line in f:
        if '=' in line and 'OPENAI' in line.split('=',1)[0]:
            api_key = line.split('=',1)[1].strip()
            break

# Encode image
with open(image_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":[
        {"type":"text","text":"Transcribe ALL visible text in extreme detail."},
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{image_data}"}}
    ]}],
    max_tokens=3000
)
```

This reliably extracts 90%+ of text from infographics including small labels, data values, and hierarchical structure. The `image_url` accepts `data:image/{png|jpeg};base64,...` URIs directly — no upload needed.

### Pitfall: trusting browser_vision over console reads for visual verification

When verifying that a stylesheet loaded and the page looks right, `browser_vision` can lie to you — it may screenshot before fonts/CSS finished loading, misjudge subtle palette differences (oat #E8E4DC vs ivory #FAF9F5 is only ~5 RGB units), or read a stale viewport. ALWAYS cross-check with `browser_console` and a JS expression that reads computed styles:

```js
JSON.stringify({
  sheets: Array.from(document.styleSheets).map(s => s.href),
  bodyBg: getComputedStyle(document.body).backgroundColor,
  h1Color: getComputedStyle(document.querySelector('h1')).color,
  h1Font: getComputedStyle(document.querySelector('h1')).fontFamily,
  tabs: document.querySelectorAll('.toolbar .tab').length,
  activeTab: document.querySelectorAll('.toolbar .tab.active').length
})
```

If `sheets: []` you have a stale page or wrong path — force a cache-bust reload with `?v=N`. Console truth wins over screenshot interpretation.

### PDF rendering pitfalls (critical)

When generating PDFs from HTML canvases:

- **CSS grid breaks in ALL PDF renderers.** Chrome headless produces garbled, scattered text with missing content. WeasyPrint silently drops grid items. Neither renders `display: grid` correctly. **Use pure HTML tables** for any layout that needs to become a PDF.
- **`ui-serif`, `ui-monospace`, `system-ui` font stacks do not resolve in headless Chrome PDF mode.** Use explicit web-safe fonts: `Georgia, "Times New Roman", serif` for headings, `"Courier New", Courier, monospace` for mono text.
- **`page-break-before: always`**: WeasyPrint respects it reliably. Chrome headless does not — content flows across pages unpredictably. For multi-page PDFs, use WeasyPrint.
- **WeasyPrint** is the preferred PDF renderer for CSS-styled documents. Chrome headless works for simple layouts but fails on complex CSS. The WeasyPrint binary lives at `/opt/homebrew/bin/weasyprint`.
- **Ghostscript PNG conversion** from PDFs can introduce visual artifacts (yellow smudges, noise) — these are conversion artifacts, not PDF defects. Trust the PDF, not the PNG.
- **Always visually inspect the generated PDF** by converting pages to PNGs (`gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r150 -dFirstPage=1 -dLastPage=N -sOutputFile=page_%d.png input.pdf`) and running vision_analyze on each page. Do not trust that it rendered correctly without inspection.
- **User's document verbosity rule**: Questions must be complete sentences that someone can read cold and understand. Not headlines ("SPRS score?") and not essays. Each question = one sentence with enough context to stand alone.

## References

- `references/thariq-thesis-analysis.md` — analysis of the "HTML > Markdown for AI agents" thesis
- `references/thariq-gallery-patterns.md` — detailed pattern notes from all 20 examples
- `references/planning-canvas-pattern.md` — single-file tabbed planning canvas pattern
- `references/multi-doc-planning-repo-pattern.md` — variant for repo-hosted multi-doc planning sets (shared _harbor.css + _canvas.js across N cross-linked HTMLs)
- `references/scientific-reporting.md` — scientific / experimental research report HTML style. Stat cards, finding blocks, performance budget tables, ASCII architecture diagrams, data-scientist persona guidelines. Use when building experimental results briefings, benchmark comparisons, or methodology docs. Antonym of the terse planning-canvas style.
- `references/playbook-canvas-pattern.md` — solo business / coaching playbook canvas pattern: radial SVG function diagrams with orbiting nodes, color-coded calendar grids, role cards with colored top borders, business size toggles, coaching client journey flows, session type cards. Use when building "how to run X business" or operating system guides.
- `references/personalization-workflow.md` — 6-step workflow for customizing a generic deliverable to a specific named person (coaching, consulting, client work). Profile lookup → gap analysis → verbatim vocabulary → actual pricing → quote library → verify. Triggered by "this is for X" / "customize for Y" / "do not be lazy" / pushback on stock templates. Real example: WONDRINN canvas rebuild from 0.7 → 0.9 eval score.
- `references/pdf-rendering.md` — PDF rendering pitfalls, font stacks, renderer selection, inspection workflow
- `references/legal-document-briefing-pattern.md` — Legal PDF → vision OCR → research agents → HTML briefing for a principal party. Includes pymupdf page-to-image technique, iterative fact-correction pattern, and the "don't lock in adversarial conclusions without principal-party input" lesson.
