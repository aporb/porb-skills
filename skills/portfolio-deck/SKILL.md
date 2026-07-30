---
name: portfolio-deck
description: Generate a HARBOR-branded client strategy deck. Use when creating a productization pitch or advisory engagement deck for a prospective client.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, Agent
disable-model-invocation: true
model: opus
---

# Client Strategy Deck Generator

You generate self-contained HTML slide decks for HARBOR consulting engagements. Each deck tells a narrative story using elite consulting frameworks (Challenger Sale, McKinsey Pyramid, MECE, Andy Raskin's Greatest Sales Deck) to help prospective clients discover why they need productization.

## Workflow

Follow these steps in order. Do not skip steps.

### Step 1: Choose Theme and Brand

Use AskUserQuestion to ask two questions:

1. **Theme** — Dark (defense-tech glass-morphism) or Light (clean corporate)?
2. **Brand** — HARBOR GovCon (federal) or HARBOR Initiative (commercial)?

### Step 2: Client Discovery Interview

Use AskUserQuestion to gather client intel. Ask 3-4 questions at a time (the tool supports up to 4 per call). Cover all of these areas across 2-3 rounds:

**Round 1 — The Basics:**
- Client name and company name
- What does the company do? (services, industry, vertical)
- How long have they been in business? Team size? Revenue range?
- What triggered their interest in productization?

**Round 2 — The Pain:**
- Have they lost a deal or felt competitive pressure from productized competitors? (Specific story preferred)
- What's their current revenue model? (100% services? Any recurring revenue?)
- What certifications, frameworks, or proprietary methodologies do they have?
- Who are their top 2-3 competitors, and are any of them productized?

**Round 3 — The Opportunity:**
- What repeatable deliverables or processes could become a product? (List candidates)
- What does success look like in 12-18 months?
- Any specific constraints? (Budget range, timeline, team limitations)
- What's the engagement entry point? (HARVEST only? Full HARBOR?)

Adapt your questions based on previous answers. Skip questions that have already been answered. If the user gives short answers, probe deeper on the most important gaps.

### Step 3: Read Reference Material

Read these files to inform your generation:

1. **Theme CSS source:**
   - Dark theme: Read the `<style>` block (first ~300 lines) from `HARBOR_portfolio/_archive/szh_hemani/deliverables/working/SZH_Strategy_Deck.html`
   - Light theme: Read `operations/practice/brand/decks/harbor-slides.css`

2. **Narrative framework:** Read `${CLAUDE_SKILL_DIR}/references/narrative-framework.md`

3. **Slide component patterns:** Read `${CLAUDE_SKILL_DIR}/references/slide-components.md`

4. **Brand constants:** Read `${CLAUDE_SKILL_DIR}/references/brand-constants.md`

### Step 4: Design the Narrative Arc

Before writing any HTML, plan the deck structure using the 5-act framework from the narrative reference. Write this plan out as a numbered slide list with:
- Slide number and title
- Slide type (title, stats, comparison, table, phase-cards, pricing, CTA)
- Emotional beat (tension, validation, reflection, urgency, hope, commercial, close)
- Key content points (2-3 bullets)

Share this plan with the user and ask for approval before generating.

### Step 5: Generate the HTML Deck

Generate a single self-contained HTML file with:

**Structure:**
- All CSS inline in a `<style>` block (copy the full theme CSS, then customize)
- HARBOR logo SVG defined once in a hidden `<svg>` block, reused via `<use href="#hlogo"/>`
- Each slide is a `<div class="slide">` with header (.sh), body (.sb), and footer (.sf)
- Print-ready: `@page` rules, `page-break-after: always`, color-adjust: exact

**Content rules:**
- Title slide: Client name, "From Services to Scale" subtitle, HARBOR brand, date, "Prepared for [name]", "Confidential" notice
- Every slide has a footer with the HARBOR logo and slide number
- Use the component patterns from the reference file (stat blocks, insight boxes, tables, phase cards, etc.)
- Links should be functional (book: https://a.co/d/04VKrMmr, tools: https://harborgovcon.com/tools/*, contact: questions@harborgovcon.com)
- Limit insight boxes to 3-4 across the entire deck (they lose power if overused)
- All competitor names should be clickable links to their websites when possible

**Dark theme specifics (if chosen):**
- Slide dimensions: 11in × 8.5in landscape
- Background: #0a0a0f, glass containers: #141419
- System fonts: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif
- Font base: 18px on html element

**Light theme specifics (if chosen):**
- Slide dimensions: 1200×675px (16:9)
- Background: #FFFFFF, cards: #F8FAFC
- Inter font (with system fallbacks)
- Uses slide-header/slide-inner/slide-footer structure

### Step 6: Save the Deck

1. Create the client directory: `HARBOR_portfolio/{client_slug}/deliverables/`
   - Use lowercase, underscores for the slug (e.g., `acme_solutions`)
2. Save the HTML file as `{Client_Name}_Strategy_Deck.html`
3. Tell the user the file path and how to convert to PDF:
   ```
   To convert to PDF: Copy html_to_pdf.mjs from the SZH project, update the input path, and run:
   node html_to_pdf.mjs
   ```

### Step 7: Editorial Lint (BLOCKING gate, LRN-20260411-014)

Before presenting the deck to CEO, run the editorial lint rules from `/email-lint` against the rendered HTML body. These rules apply to ANY client-facing artifact, not just emails. The same rules enforced by `ceo-briefing` render.mjs and `/nda-draft` Step 5:

```bash
FILE="HARBOR_portfolio/{client_slug}/deliverables/{Client_Name}_Strategy_Deck.html"

# Em-dash / en-dash / double-hyphen check
grep -n -P '[\x{2013}\x{2014}]' "$FILE" && echo "BLOCK: em/en dash found" && exit 1
grep -n ' -- ' "$FILE" && echo "BLOCK: double-hyphen found" && exit 1

# Banned phrases (aligned with ceo-briefing render.mjs)
grep -n -i -E 'rebuild|rebuilt|single sharpest|existential anchor|mind.blow|unprecedented|groundbreaking' "$FILE" && echo "BLOCK: banned phrase found" && exit 1

# Amyn not Amy
grep -n -P '\bAmy\b(?!n)' "$FILE" && echo "BLOCK: Amy not Amyn" && exit 1
```

If any of the checks fire, fix the HTML (not just the output copy). Client-facing artifacts inherit the same editorial rules as client emails because clients do not know the difference between an "email" and a "deck" when they are reading it.

### Step 8: Cross-Client Leak Grep (BLOCKING gate, ERR-20260330-001)

Grep the rendered HTML for every OTHER client's aliases. Source of truth: `admin/memory/portfolio-aliases.md`.

```bash
FILE="HARBOR_portfolio/{client_slug}/deliverables/{Client_Name}_Strategy_Deck.html"
THIS_CLIENT="{client_slug}"

# Read portfolio-aliases.md, extract every alias NOT belonging to THIS_CLIENT, grep for them
python3 <<EOF
import re
aliases = {}
current = None
with open("admin/memory/portfolio-aliases.md") as f:
    for line in f:
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            current = m.group(1).strip()
            aliases[current] = []
            continue
        m = re.match(r"^-\s+(.+?)(?:\s*\(|$)", line)
        if m and current:
            aliases[current].append(m.group(1).strip())

this_client = "$THIS_CLIENT"
leaks = []
with open("$FILE") as f:
    content = f.read().lower()
for slug, alist in aliases.items():
    if slug == this_client:
        continue
    for alias in alist:
        if alias.lower() in content:
            leaks.append(f"{slug}: {alias}")

if leaks:
    print("CROSS-CLIENT LEAK DETECTED:")
    for l in leaks:
        print(f"  {l}")
    exit(1)
EOF
```

If any leaks fire, the deck is NOT closeout-ready. Remove every reference to other clients before presenting.


## Orchestration

This skill fans out to multiple agents. The orchestrator (CEO by default) manages the fan-out, sequences dependencies, and merges results. See `.claude/skills/SKILL-PATTERN.md` for the pattern.

### Step 1 — Resolve inputs & prep workspace

Parse arguments, ask via `AskUserQuestion` if missing, and prep the output paths.

### Step 2 — Parallel fan-out

Independent lanes launch in a single message (multiple `Agent` tool calls). Dependent lanes wait for their input lanes to complete before launching.

Lane list:

**Lane A — content-writer** (Deck copy in Amyn's voice)
- **prompt must include:** Write the narrative slides (positioning, HARBOR assessment, roadmap, pricing, next steps). Uses brand + framework references.
- **return:** structured output the orchestrator can merge

**Lane B — code-builder OR cto** (HTML render + styling)
- **prompt must include:** Render the deck as HTML using operations/practice/brand/decks/ templates. Light-mode default. Pipe to /deck-to-pdf if PDF requested.
- **return:** structured output the orchestrator can merge

Each `Agent` call's prompt must include:
1. Command + resolved args
2. Operator: `Amyn Porbanderwala (HARBOR founder)`
3. Playbook: `Read .claude/skills/portfolio-deck/SKILL.md — your lane scope is <label>`
4. Scoped inputs for this lane only (not the full firehose)
5. Return contract: exactly what structured output this lane must return
6. Cross-lane isolation: do not reference other portfolio companies; hermetic seal applies

### Step 3 — Merge

Collect all lane returns. The orchestrator synthesizes into the final deliverable. For HTML decks, the final render lane (usually cto or code-builder) uses `operations/practice/brand/decks/` templates and pipes to `/deck-to-pdf` for PDF export.

### Step 4 — Memory + ledger

Save outputs under `HARBOR_portfolio/<slug>/`. Update `admin/memory/portfolio.md` with a one-line status change for the slug if material.

---

The detailed playbook below is what the orchestrator and each lane agent reads to execute this skill.

## Key Design Principles

- **Conversation, not presentation.** The deck should make the client want to correct, validate, and discuss — not passively receive.
- **Tension before resolution.** Always establish the problem before showing the solution.
- **Their framework, your lens.** If the client uses a known methodology (7S, balanced scorecard, etc.), apply it to their own business as a mirror.
- **Earned commercial moments.** Pricing comes after the client has already concluded they need help. Only 1 insight box near pricing.
- **Self-contained files.** No external dependencies. No CDN links. No JavaScript. Pure HTML + CSS.
- **Print-first.** Must look beautiful when printed to PDF. Test mentally at 72 DPI.

## HARBOR Phase Reference

| Letter | Phase | Color | What It Does |
|--------|-------|-------|-------------|
| H | Harvest | #3B82F6 | Mine existing delivery for productizable IP |
| A | Architect | #8B5CF6 | Design the product structure and business model |
| R | Risk-Proof | #EC4899 | Validate market fit, legal, compliance |
| B | Build | #F97316 | Develop MVP, create PRD, build the product |
| O | Operate | #10B981 | Launch beta, establish operations, onboard users |
| R | Replicate | #06B6D4 | Scale, systematize, create growth engine |
