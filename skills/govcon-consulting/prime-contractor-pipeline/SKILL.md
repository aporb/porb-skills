---
name: prime-contractor-pipeline
description: "Prime project pipeline → go/no-go deck with outreach tabs."
tags: [prime, pipeline, bechtel, action-deck, go-no-go, outreach, html-briefing, lfc]
related_skills: [contractor-portfolio-analysis, fedcon-opportunity-research, html-briefing, orchestrator-agent-workflows, contact-intelligence, quality-gate-pipeline]
---

# Prime Contractor Pipeline Action Deck

## Overview

Build a comprehensive, actionable pipeline evaluation when the user provides a prime contractor's project/opportunity list. Unlike `contractor-portfolio-analysis` (which analyzes a prime's existing federal contract portfolio) or `fedcon-opportunity-research` (which finds open solicitations), this skill handles the forward-looking case: a list of projects a prime is bidding, building, or planning, and you need to assess how to get in.

## When to Use

- User shares a prime contractor's project opportunity list (PDF, URL, document)
- User asks "how do we get into [prime]" or "what can we do with [prime]"
- You need to assess multiple opportunities across different service lines
- Pipeline analysis that spans federal compliance, technology advisory, AI infrastructure, and commercial work
- Building outreach materials for a specific prime contractor

## Critical Scope Rule

**Do NOT filter through a single-service-line lens.** The user's directive: "it's not just federal work... look at what [the entity] does and what I bring to the table." Evaluate every project across ALL capabilities:

- Federal compliance (NIST 800-53, CMMC L2, cybersecurity assessment)
- Technology advisory (fractional CAIO, AI strategy, digital transformation)
- AI infrastructure (RAG systems, MCP fleet, Agentic OS, document intelligence)
- Commercial consulting (program management, risk, innovation advisory)
- Training & workforce (AI-powered, SCORM-compliant)
- Any capability the combined team brings

## Branding Rule: LFC is the External Face

**Everything goes through LFC.** The user's directive: "everything goes through lfc. they get [deliverer] via [internal entity] behind the scenes but we present a united [external] front."

- LFC (Leatherneck Federal Consulting) is the single external entity
- HARBOR is the internal delivery engine for AI/productization work
- Amyn Porbanderwala is an internal delivery resource
- Never disclose the internal entity to external recipients
- All emails, capability statements, and portal registrations use the LFC name, UEI, CAGE, and contact info
- **Domain:** `leatherneckconsulting.com` — this is the single LFC domain. Do not use `harborgovcon.com` or any other domain in external-facing materials.

## Workflow

### Phase 1: Pipeline Classification

Classify every project in the pipeline using a structured go/no-go matrix. Use multiple lenses:

| Lens | What to Assess | Output |
|------|---------------|--------|
| **Federal Compliance** | NIST/CMMC requirements, cybersecurity, set-aside eligibility | Can LFC sub on compliance? |
| **Technology Advisory** | Digital transformation, AI/ML, data analytics, innovation | Fractional CAIO play? |
| **Commercial** | Non-federal EPC, construction, project management | Direct consulting engagement? |
| **Team Fit** | Does the team have relevant experience (DAWIA III, CISA, Secret clearance, $20B portfolio)? | Confidence score |
| **Entry Path** | Procurement portal, SBA outreach, LinkedIn connection, executive sell | Route recommendation |

**Decision categories:**
- **GO** — Direct path exists. Build outreach within 1 week.
- **WATCH** — No immediate path, but opportunity exists. Monitor and enter when ready.
- **NO-GO** — No plausible entry angle. Revisit only if conditions change.

### Phase 1.5: Decision Analysis (Tab 1 of the Unified Deck)

Produce the decision analysis as **Tab 1** of the single HTML action deck — never as a separate file. The user's hard rule: "add the additional tabs in the best way possible, not create two separate files." The analysis and the action materials live in one deliverable.

**Structure of Tab 1:**

| Section | Content |
|---------|---------|
| **BLUF** | Decision summary: how many GO/WATCH/NO-GO, total pipeline value, first action. **Structure as scannable short paragraphs** — one line per key message (Decision, Pipeline, Structure, Service Lines, First Action, New Intel). NO dense narrative walls of text. Example: |
| <code>&nbsp;</code> | `<p><strong>Decision:</strong> GO on <strong>5</strong> projects, WATCH on <strong>5</strong>, NO-GO on <strong>8</strong>.</p>` |
| <code>&nbsp;</code> | `<p><strong>Pipeline:</strong> $1.0M–$3.0M in near-term services revenue, assuming 1–2 engagements close within 12 months.</p>` |
| <code>&nbsp;</code> | `<p><strong>Structure:</strong> All work flows through [External Entity] as the single external face.</p>` |
| <code>&nbsp;</code> | `<p><strong>Service Lines:</strong> (1) Line item one. (2) Line item two.</p>` |
| <code>&nbsp;</code> | `<p><strong>First Action:</strong> Clear actionable step this week.</p>` |
| <code>&nbsp;</code> | `<p><strong>New Intel:</strong> What changed since initial analysis.</p>` |
| **Decision Summary** | Visual stat counters (GO/WATCH/NO-GO counts + pipeline value) |
| **Decision Criteria** | The lenses used for classification |
| **Master Pipeline Table** | Every project with verdict, opportunity type, entry path, LFC service — all project names hyperlinked to external source pages |
| **GO Deep Dives** | Full rationale per GO project: why, entry path, outreach plan, personnel, value range |
| **WATCH Deep Dives** | What to monitor, trigger conditions for upgrade |
| **NO-GO Summary** | Brief rationale |
| **Pipeline Value Table** | Service line × best case × probability × expected value |
| **Post-Analysis Discoveries** (updated after research) | What changed after research agents returned — new GO additions, leadership intel, status corrections |

**Pipeline value estimation:**
For each GO project, estimate a realistic fee range (e.g., $100K–$500K) based on comparable service engagements. Apply a probability of win (15%–30% for cold SBA outreach, higher for referred contacts). Calculate expected value as (best case × probability).

| Service Line | Best Case | Probability | Expected Value |
|-------------|-----------|-------------|----------------|
| Sentinel compliance platform | $250K | 20% | $50K |
| WTP training platform | $150K | 25% | $37.5K |

**Write Tab 1 as the analysis tab in the unified HTML file. The action tabs (Phase 3) are tabs 2–8 in the same file.**

### Phase 2: Research (Parallel Sub-Agents + Orchestrator Build)

Dispatch research sub-agents while you build the action deck:

**Agent 1: Leadership & Innovation Intel**
- Scrape prime's leadership page for technology/innovation executives
- Search for CTO, CIO, CDO, Chief Innovation Officer, VP Digital Transformation, Head of AI/ML
- Find LinkedIn profiles, public statements, and innovation initiatives
- Identify the EXACT person whose mandate matches what you're selling

**Agent 2: News & Recent Developments**
- Search for latest project awards, leadership changes, technology announcements
- Identify innovation labs, digital delivery programs, AI/ML partnerships
- Find conference appearances and speaking engagements by technology leaders

**Agent 3: Specific Project Intel (optional)**
- Deep-dive one or two flagship projects from the pipeline
- Understand contract vehicle, phase, current prime/sub structure

**While agents run, build the HTML deck skeleton.** Do NOT wait idle. The skeleton provides 80%+ of the value; agent outputs add depth and citations.

**URL hunting for project links:** After building the master pipeline table, verify every project has a live URL. For each project, search (`web_search` + `web_extract`) for the project name + "project" + prime name + "page" or "overview". Validate the URL resolves before embedding. Grep for `brief.h.porb.dev` — should be zero hits in the final file. If a project has no public source page, add a note "no public source found" instead of linking internally.

### Phase 3: Build the Tabbed HTML Action Deck

Produce a single self-contained HTML file with tab navigation. Required tabs:

| Tab | Content |
|-----|---------|
| **1. GO Decisions** | Deep-dive on every GO project. Why it's a go, the specific entry path, who at LFC reaches out, email draft or script, timeline, personnel to staff. |
| **2. WATCH Decisions** | What to watch for, trigger conditions for upgrade to GO, contacts to track. |
| **3. NO-GO Decisions** | Brief rationale. Avoid spending time here unless conditions change. |
| **4. Supplier Portal** | Step-by-step registration instructions with exact NAICS codes, capability keywords, and entity data. Include pricing schedule if the portal requires it. |
| **5. Capability Statements** | Reusable one-pager tailored to the prime's industry. Include engagement models with price ranges (e.g., $50K-$500K). |
| **6. Outreach Emails** | Complete email drafts for each GO project. Each includes: to, subject, body, sender info, call to action, **and a specific send-by date recommendation** (calendar week or exact date). |
| **7. LinkedIn Targets** | Populated from research. Ranked table with names, titles, LinkedIn URLs, approach strategy, and timing. |
| **8. Monitoring Setup** | Cron job instructions, trigger conditions, and what to flag as an entry point. |

**Hyperlinking rule:** Every project name referenced in tables MUST be hyperlinked to its EXTERNAL source page (prime's project page, news article, press release). Never link to internal `brief.h.porb.dev` URLs. Verify each URL is live before deploying.

**Adversarial review gate:** Before delivery, review every email draft for:
- Does it lead with the right qualification (CISA over Security+, DAWIA III, Secret clearance)?
- Is the ask clear and specific?
- Is the tone appropriate for the recipient (procurement vs. executive)?
- Are all names, UEIs, CAGE codes, and contact info correct?
- Does every section use LFC branding, not internal entity branding?

### Phase 4: Research Integration

When research agents return, patch their findings into the HTML deck:
- Tab 7 (LinkedIn Targets) gets specific names, titles, LinkedIn URLs, approach strategy
- Tab 8 (Monitoring) gets their innovation programs and recent developments
- Tab 3 (WATCH) may get upgraded to GO if research reveals a connection path

**Curation rule:** Agent outputs are self-reports. Extract the strongest 80% and discard obvious/weak material. Reconcile contradictions against your own research.

### Phase 4.5: Decision Update

After integrating research outputs, **update the go/no-go decision briefing** (from Phase 1.5). New intel often changes the counts:

- A new GO project may be discovered (e.g., Australia HSR added as GO #5)
- A WATCH project may be confirmed or upgraded (e.g., Micron NY fab added to WATCH)
- A project timeline may shift (e.g., Poland AP1000: EPC not signed, stay WATCH)
- A leadership change may open a strategy window (e.g., new NS&E President = refresh opportunity for Sentinel/WTP/Natrium outreach)
- A specific LinkedIn target may be confirmed whose role directly matches your offering

**Add a "Post-Analysis Discoveries" section** to the decision briefing showing:
- What changed
- What was added or upgraded
- Updated pipeline count and value

### Phase 5: Verify & Deploy

Before deploying, run the html-effectiveness gallery comparison:
1. Open `~/repos/html-effectiveness/index.html` in a browser
2. Find the example closest to your deliverable (status report #11, pull deck #09, or concept explainer #14-15)
3. Visually compare: padding inside cards, border radius consistency, typography hierarchy (serif 500), table header styling, section spacing
4. If your output looks materially worse than the gallery equivalent, rewrite before deploying

Then deploy:
```bash
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"
```

Deliver as `https://brief.h.porb.dev/<slug>.html`

## LinkedIn C-Suite Bypass Pattern

For technology advisory opportunities, procurement portals and SBA outreach programs are the WRONG entry channel. The user's capabilities (fractional CAIO, AI infrastructure, digital transformation strategy) map directly to executive roles that do NOT sit in procurement — they sit in innovation, transformation, or engineering leadership.

**Target identification:**
- SVP/Director of Digital Transformation, EPC Transformation, Innovation
- Chief Innovation Officer, VP Engineering Technology, Head of AI/ML
- Any role whose title contains "digital", "innovation", "transformation", "AI", or "technology"
- Look for BRAND-NEW roles — the user created them for a specific mandate, which makes them open to outside help

**Approach pattern:**
1. **Connect on LinkedIn** — no pitch in the connection request. Just an observation from a shared interest.
2. **Wait for acceptance** — do NOT follow up on any other channel during this window.
3. **Post-connection message** — lead with a specific observation about THEIR mandate (e.g., "Your AI/robotics integration mandate for EPC delivery is exactly the framework I've been building"). Reference your own work (book, methodology, published framework).
4. **Offer value** — "I'd be happy to share what I've learned from the [domain] side." Not "let me pitch you."
5. **If no response in 2 weeks** — engage with their LinkedIn content (comment meaningfully on posts). Do NOT double-message.

**Key principle:** The C-suite LinkedIn approach BYPASSES procurement entirely. Once an executive wants you, procurement becomes a formality. Never pitch in the first message — build context first.

## HTML Design Standards

Use the Thariq/html-effectiveness aesthetic (see `html-briefing` skill). Tab navigation uses JavaScript with `data-tab` attributes:

```html
<div class="tab-nav">
  <button data-tab="tab-sentinel" class="active">1. Sentinel</button>
  <button data-tab="tab-welcome">2. WTP</button>
  ...
</div>
<div class="tab-panel active" id="tab-sentinel">...</div>
```

**CRITICAL: Tab CSS is REQUIRED, not optional.** Without `.tab-nav` / `.tab-panel` CSS rules, all tab panels render simultaneously and buttons have no visual state. The JS toggle cannot fix what CSS doesn't define. Build the tab CSS into every action deck.

Required styles (inline in `<style>`):
```css
.tab-nav {
  display: flex; flex-wrap: wrap; gap: 0;
  border-bottom: 1.5px solid var(--g300);
  margin: 20px 0 0; overflow-x: auto;
}
.tab-nav button {
  font-family: var(--mono); font-size: 10.5px; letter-spacing: 0.06em;
  text-transform: uppercase; font-weight: 500;
  padding: 9px 14px; border: none; background: none;
  color: var(--g500); cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1.5px; white-space: nowrap;
  transition: color 0.15s, border-color 0.15s;
}
.tab-nav button:hover { color: var(--slate); }
.tab-nav button.active { color: var(--clay-d); border-bottom-color: var(--clay); }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.tab-panel.active section:first-of-type { margin-top: 28px; }
```

The mono 10.5px uppercase style is denser than a full-fill button — critical when you have 7-8 tabs in a row. If there are fewer tabs (3-4), the simpler clay-fill style works:
```css
.tab-nav { display: flex; gap: 4px; border-bottom: 2px solid var(--g300); margin-bottom: 24px; }
.tab-nav button { padding: 8px 16px; border: none; background: transparent; cursor: pointer; font: 500 13px/1 var(--sans); color: var(--g500); border-radius: 8px 8px 0 0; }
.tab-nav button:hover { background: var(--g100); }
.tab-nav button.active { background: var(--clay); color: white; }
```

JS at bottom of body:
```javascript
document.querySelectorAll('.tab-nav button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-nav button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});
```

## Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Filtering too narrowly (federal-only when commercial applies) | Use the multi-lens classification matrix. Force at least three lenses per project. |
| Internal entity branding in external-facing docs | After writing, grep for mentions of the internal entity. Every external reference must be LFC. |
| Internal URLs (brief.h.porb.dev) in external-facing tables | After writing, grep for `brief.h.porb.dev` — should be zero hits. |
| Vague outreach emails | Every email must have: specific person, specific project name, specific ask, sender's qualification that differentiates, send-by date. |
| **No send-by dates on email drafts** | Every email draft in the action tabs must include a `Send by:` recommendation in the email-meta block (e.g., `Send by: July 28–30, 2026`). This drives accountability. |
| **Wrong domain in external materials** | The canonical domain for LFC is `leatherneckconsulting.com`. Never use `harborgovcon.com`, `porbanderwala.com`, or any other domain in external-facing emails, capability statements, or portal registrations. |
| Research tab with placeholder text | The LinkedIn tab must name names. "Send connection request" is insufficient — specify the person. |
| Waiting idle while research agents run | Build the HTML skeleton immediately. 80% of content comes from the user's own documents and your domain knowledge. |
| One-size-fits-all capability statement | Each capability statement must reference at least one specific project from the pipeline. |
| No follow-up logic | Every email draft must include: expected response timing, follow-up cadence (5 business days), pivot strategy if no response (LinkedIn, alternative contact). |
| Decision briefing not updated after research | After research returns, GO/WATCH counts may change. Update the decision briefing's count, value, and add a Post-Analysis Discoveries section before delivering. |
| **Two separate files instead of one unified tabbed deck** | The decision analysis and action tabs MUST live in one HTML file with tab navigation. Tab 1 = analysis & decisions. Tabs 2-8 = action materials. Never create two separate HTML files. |

## Reference Files

- `references/prime-pipeline-bechtel-2026-07-25.md` — Full worked example from the Bechtel pipeline session. Includes: go/no-go classification, email drafts, supplier portal steps, capability statements, LinkedIn target tables, monitoring setup.
