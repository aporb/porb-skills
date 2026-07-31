---
name: federal-pitch-deck
description: Build CEO-facing HTML pitch decks for federal contractors.
---

# Federal CEO Pitch Deck

Use when building a live HTML pitch deck for a federal contractor CEO audience. Covers the full delivery workflow from research through deployment.

## Workflow

### Step 1: CEO Gap Analysis (before writing a line)
Think like the CEO, not the seller. Sit with:
- Their market position and recent wins
- What keeps them up at night (compliance, talent, acquisition, competition)
- What would make them say "this is exactly what I needed"

Output: gap analysis document listing what's there, what's missing, and what needs rethinking. Score it honestly (e.g., 42/100).

### Step 2: Implementation Plan
Write a plan with per-item acceptance criteria and definition of done. Organize into PASSES:

| Pass | Focus | Example Items |
|------|-------|---------------|
| P0 | Identity & Team | "Why Amyn" slide, Britta Jones team slide, capability statement |
| P1 | Math & Pricing | Correct subtotals, base total, immediate auth amount, honest pricing |
| P2 | Competitive | 4-row punch list (cost-of-inaction header, incumbent bordered red), competitive comparison, differentiation |
| P3 | Voice | Rewrite subtitle, remove consulting jargon, add first-person stories |
| P4 | Context & Content | Recent wins, acquisition context, success metrics, risk acknowledgment |
| P5 | CTA & Details | Unified CTA, payment terms, product demos, appendix slides |
| P6 | Verification | Full 18-item gate, no-stub scan, deploy |

### Step 3: Execution (parallel passes)
Use `execute_code` for multi-patch batches. Use terminal `sed -i` for slide insertion. Each pass is a standalone commit.

### Step 4: Verification Gate
Run ALL of these before declaring done:

**Math:**
- Phase subtotals correct (Phase 1, Phase 2, Phase 3)
- Base total ($425K-$530K or per engagement)
- Immediate authorization amount correct

**Forbidden terms:** Zero Aecon, Navaide, LFC, Leatherneck, OORAH, Wyoming(LLC), exact agent counts, non-public acquisition claims, internal entity structures (1099, LLC names)

**Ownership/OPSEC:** No non-public acquisition stated as fact. No Centrus/Worthington/Westerman-style ownership assumptions stated as fact. No concurrent role mentions. No "FSO-credentialed" — use "Export Control Practitioners."

**Voice:** No consulting jargon. No sponsor first-person voice. No "small team" framing. No names in CTA. No conditional language in CTA.

**No stubs:** Zero TBD / TODO / FIXME / TK / "coming soon" / "lorem ipsum"

**Slide count:** Known and reported

### Step 5: Self-Review
Dispatch an adversarial judge subagent before presenting to client. It should:
- Score each slide
- Flag consistency issues
- Check forbidden terms
- Validate math
- **Verify claims against public data** — if the sponsor makes claims about their own market (award values, nuclear contracts, DOE participation), the agent should verify via ddgr/Firecrawl before including in the deck
- **Cross-document alignment** — verify deck, brief, and SOW agree on all numbers, scope phasing, and scope priorities

## Deck Architecture

### Section Structure (typical 18-22 slides)

```
Section A: Why Now (3 slides)
  - Title + subtitle
  - Market stats (client's own wins preferred)
  - Compliance urgency + acquisition context

Section B: What We Do (4-5 slides)
  - Before/After state comparison
  - Agent Army overview
  - CLIN structure

Section C: Why Us (4-5 slides)
  - Competitive comparison table
  - Team (Amyn + key team members)
  - Published works / live products
  - Why Amyn (BALTOPS, Marine, CISA, 2 books)
  - Capability statement

Section D: The Ask (3 slides)
  - Risk acknowledgment ("What Could Go Wrong")
  - Pricing summary
  - CTA: unified, specific dollar amount

Appendix (2-4 slides)
  - Product demos (live, not slideware)
  - SOW pricing detail
  - Regulatory references
```

### Slide Format
```html
<section class="slide" id="sN">
  <div class="slide-inner">
    <div class="eyebrow">Section Title</div>
    <h2>Slide Title</h2>
    <!-- content -->
  </div>
  <div class="footer-meta">Source or attribution line</div>
</section>
```

### Design System (Dark HARBOR Theme)
```css
:root {
  --slate: #0A0A0B;     /* page background */
  --card: #141517;      /* card backgrounds */
  --card-b: #1A1B1E;    /* card border */
  --text: #F1F0ED;      /* primary text */
  --text2: #B0ADAC;     /* secondary text */
  --text3: #6B6968;     /* tertiary text */
  --a: #D4A843;         /* HARBOR amber -- accent */
  --b: #1A3A5C;         /* navy */
  --r1: #EC4899;        /* pink accent */
  --r2: #8B5CF6;        /* purple accent */
}
```

### Four-Question Filter Slide (CEO Deep-Dive Decks)

Add a dedicated slide after the Team slide with four diagnostic questions that reframe the engagement from "what are you selling?" to "what's actually wrong here?":

- Frame: Four questions that determine readiness — each one surfaces a pain point the CEO already suspects but hasn't quantified.
- Each question has a pointed sub-question: "Do you know where your CUI lives? ...your data flows? ...your boundary?"
- Footer line: "If the answer to any is 'no,' you're paying for risk — not running lean."
- Effect: turns the sale into a risk-management conversation. The CTA feels like closing an exposure, not buying a service.

### Competitive Positioning — Architecture

The competitive positioning slide needs to go through iterations. Proven evolution from practice (Westerman, Jul 2026):

**Iteration 1 — Wide table (rejected):** 8+ columns of competitor comparison. Unreadable at presentation scale — headers break mid-word. Do not start here.

**Iteration 2 — Capability cards (rejected):** Stacked cards per competitor type. Cleaner but redundant — repeats Team and Pricing slide content.

**Iteration 3 — 4-row punch list (accepted):** One punch per competitor type. Headers: HARBOR | Fractional CAIO | Big 4 Federal | Other CMMC Shops. Body is one line of differentiation per row. No table markup, no extended capabilities list. Minimal and unique — CEO scans in 10 seconds.

**Design rules:**
- The incumbent MSP row (highest threat) gets a red left-border accent — CEO's eye catches the conflict-of-interest argument immediately
- No table HTML — use flexbox rows with label + body columns
- Start with the cost-of-inaction header not a feature comparison — "most expensive option: doing nothing"
- Max 4 rows (HARBOR + 3 competitors). 5+ rows is too many for a single slide

### Ownership/Acquisition Handling

NEVER state an acquisition as fact in a client-facing deck unless it is a matter of public record (SEC filing, press release on both sides).

| Scenario | In Deck | In Internal Brief |
|----------|---------|-------------------|
| Public acquisition (SEC filing, press) | Reference as context | Same |
| Internal knowledge only (sponsor shared) | Omit entirely | Include with source attribution |
| Industry speculation | Omit entirely | Omit entirely or flag as unverified |

If a sponsor shares non-public acquisition info, it stays in their internal brief. The CEO deck references only confirmed, public data points.

### Internal Entity Structure — Never Visible

Do not expose internal entity structures in client-facing slides:
- No "1099 under HARBOR" or similar employment-structure language
- No LLC references (entity name on SOW/contract only)
- No parent/subsidiary relationships
- No concurrent role mentions
- No "FSO-credentialed" on team slides — use "Export Control Practitioners" or "Nuclear Compliance Practitioners"

Test: if a competitor could infer your contracting structure from a slide, remove it.

### CTA Patterns

Refined from practice (Westerman, Jul 2026):
- No names in CTA — never "Doug will schedule a follow-up with Amyn." Say "Authorize Phase A today."
- No conditional language — "Sign the SOW" not "If you've reviewed the proposal, sign the SOW"
- No intermediary scheduling — the ask is the ask
- Unify CTA across all deliverables — same dollar amount, same authorization structure in deck, SOW, and brief

### Section Dividers (for CEO deep-dive decks)

Between each major section, add a dedicated divider slide with:
- Section letter + name (large, accent color)
- One-line summary statement the presenter reads aloud
- Purpose: natural pause point, signals section transition

```html
<section class="slide section-divider" id="divB">
  <div class="slide-inner" style="display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;">
    <div class="section-letter" style="font-size:72px;color:var(--accent);font-weight:700;">B</div>
    <h2 style="margin-top:0;">The Solution</h2>
  </div>
</section>
```

### Critical Design Requirements
1. **Mobile 320px** -- everything readable without horizontal scroll.
2. **Print landscape 16:9** -- `@media print { @page { size: landscape; } }`
3. **Keyboard navigation** -- arrow keys, Escape to overview, N/P for next/prev.
4. **Scroll-snap** -- `scroll-snap-type: y mandatory`
5. **Slide counter** -- bottom-right, e.g., `2 / 22`.

### Voice Rules
- First-person for credentials ("I built," "I deployed," "I am a Marine")
- Concrete numbers and stories (BALTOPS 2017, $616M in contracts)
- No consulting jargon: no "AI-augmented execution," "disproportionate market share"
- Marine-direct: short sentences, active voice
- **No sponsor first-person voice** — do NOT write slides in the sponsor's voice ("As your VP X, I've seen..."). The deck is the principal's narrative. Sponsor endorsement lives in the CTA slide context line, not as a dedicated "How This Came Together" slide.
- **No framing objections as "too small"** — don't say "we're a small team of ~30 agents." Say "~30 agents." The "small team" framing invites the objection you're trying to preempt.
- **No "caveat emptor" tone** — the risk slide states honest risks then immediately follows with mitigation. Don't talk yourself out of the deal.
- **No internal entity structure** — never mention 1099, LLC names, parent/subsidiary, or concurrent roles.
- CTA uses "Authorize" not "Get Started" or "Learn More"
- No names in CTA — no "Doug will schedule a follow-up." Just the ask.

### Verification Gate — Multi-Document Alignment

After EVERY change batch, verify ALL documents in the proposal package as a group:

**Pricing cross-check:**
- Deck base total = Brief total = Sum of SOW CLIN totals
- Phase subtotals match across documents
- Immediate authorization amount identical everywhere

**Narrative cross-check:**
- Leading priority (e.g. export control first) appears in deck intro, deck slide body, AND SOW Background
- Scope items in SOW are all referenced in deck slides
- Acquisition/ownership claims identical (or absent) in ALL client-facing docs

**Forbidden terms scan (ALL files in one pass):**
- `grep -ci 'term' deck.html sow.html brief.html` per term
- Report any mismatch immediately — fix both documents before committing

### Pitfalls

- Don't use exact agent counts -- round to "~30"
- Don't forget the risk acknowledgment slide
- Don't start coding before the CEO gap analysis
- Commit after EVERY pass, not at the end
- Brief and SOW use ivory/clay theme, deck uses dark theme — two design systems. Don't mix them.
- Deliver PDF or DOCX when the user asks for printable/award formats — Chrome headless for PDF, Pandoc for DOCX
- The four-question filter slide is not optional for CEO deep-dives above 15 slides
- If the sponsor gives direction that contradicts the scope or another sponsor's direction, TRACE don't OBEY. Build a conversation timeline of their claims, verify claims against public data (ddgr with 1.5s spacing), identify what they can ACTUALLY sell to their audience, then realign docs around the sellable scope.
- After any pricing change, update ALL cross-referenced documents before declaring done. A $25K shift in Phase 1 pricing ripples through the Phase subtotal, base total, and immediate authorization number — and those numbers live in 3 separate files.
- Don't create redundant documents. One artifact = one audience. The CEO pitch deck IS for the CEO. The internal brief IS for the sponsor. If someone asks for a "separate version," the answer is usually "the deck already serves that purpose."
