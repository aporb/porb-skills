---
name: aecon-deliverable-patterns
description: "Companion to aecon-brand-system. Reusable patterns for building Aecon decks, process flows, RACI matrices, and white-label deliverables discovered across sessions. Load AFTER aecon-brand-system for brand rules, then load this for practical assembly patterns."
category: govcon
triggers:
  - User asks to build an Aecon deck, slide deck, presentation, or process visualization
  - User references the McKinsey/BCG style for Aecon deliverables
  - User asks for "white label" or "for Sinem" / "for someone else to present" / "as if he was the author"
  - User mentions Compliance vs FCS split in procurement governance
  - User corrects naming (personal names → role titles) in an Aecon deliverable
  - User asks for an SOP, standard operating procedure, internal operating procedure, or process documentation for an FCS function
  - User asks to "document [name]'s workflow" or "create a plan and execute" for a procurement/contracts/subcontracts function
  - User asks for a "pptx that we can share with [name]" or to "make it as if he was the author"
---

# Aecon Deliverable Patterns

Companion to `aecon-brand-system`. That skill defines the visual brand (colors, fonts, logos). This skill defines the *assembly patterns* — how to structure slides, name roles, split compliance functions, and handle white-label attribution. Load both when building Aecon-facing deliverables.

**Note:** This skill covers slide decks, process flows, RACI matrices, and white-label presentations. For researched compliance briefings (regulatory questions, FIPS/CMMC/DFARS interpretation, decision frameworks with citations), use `aecon-compliance-briefing` instead — it governs a different deliverable structure (long-form HTML briefing with bottom-line answer, regulatory framework, decision logic, risk matrix).

## Role-Based Naming

**Rule:** Use role titles, not personal names, in all body content of Aecon deliverables.

| ✓ Use | ✗ Don't Use |
|-------|-------------|
| Director of IS Vendors & Contracts | Sinem |
| Enclave Technical Lead | Isaiah |
| Federal Compliance | Brian, Kerem |
| VP Technology | Jason |
| Federal Contract Solutions (FCS) | — |

**Specific exclusion:** Kerem should never appear by name. His function is covered by "Federal Compliance" or "Procurement Governance."

## Amyn Role Boundaries (Hard Rules)

**Rule 1 — Amyn does not build.** IT builds all SharePoint, Power Automate, and technical infrastructure. Documents must reflect this:
- Week 1 sign-off: "Isaiah + Amyn + Mark" ✓
- Weeks 2-4 implementation: "IT + Isaiah" / "IT" / "IT + Isaiah + AP team" ✓
- Never: "Amyn builds," "Amyn creates," "Owner: Amyn" on any build/implementation step ✗
- The only Amyn-owned week is Week 1 (process sign-off). Everything else is IT.

**Rule 2 — Zero Amyn quotes or call-attributed speech.** No deliverable may contain:
- "Per Amyn's direction in the [date] call..."
- Quoted speech: "Amyn said 'get your process down...'"
- "Amyn advised/coached/recommended..."
- Any sentence that sources its authority from something Amyn said on a call

The only Amyn references allowed: functional role (FCICS compliance persona, compliance routing, permission settings like "Amyn=Edit on compliance columns") and Week 1 sign-off participation ("Isaiah + Amyn + Mark"). If a sentence references Amyn's call advice, rewrite it as a neutral statement of fact or remove it entirely.

**Rule 3 — Short, human emails.** When drafting emails for Amyn to send (follow-ups, meeting replies, internal comms):
- Open warm and direct — "Really appreciated the call today" not "Thank you for the time this afternoon"
- One sentence of context, then the ask
- Questions flow naturally, not tiered/color-coded/compliance-formatted
- ~8 questions max, one section, plain language
- No DFARS citations, no regulatory jargon in email body
- Close with a clear next step, not an agenda

## White-Label Mode

When building a deck for another stakeholder (e.g., Sinem) to present as their own:

1. Footer: `Prepared for IS Vendors & Contracts` — NOT `Prepared by Amyn Porbanderwala`
2. No email, no personal contact info
3. Verify before delivery: `grep -i "amyn\|aporbanderwala"` returns zero results
4. Confirm with the user: "Who presents this — you or [name]?"

## Compliance vs. FCS Split

**Pitfall:** Lumping all federal checks into one "Federal Procurement Governance" box. At Aecon, Compliance and FCS are separate functions. The user corrected this directly.

**Rule:** On process slides, RACI matrices, and checklist cards, split into two distinct sections:

| Compliance Review | Contractual Governance (FCS) |
|---|---|
| SAM.gov debarment (FAR 9.4) | FAR 12/13 procurement path |
| Section 889 prohibition | Prime/subcontract flow-downs |
| **FedRAMP authorization status** | Small business & set-aside |
| CUI determination & DFARS 7012 | Terms review & contractual compliance |
| DoD Cloud SRG impact level | |
| CMMC verification via SPRS | |

**FedRAMP MUST appear** in compliance checklists — it's the most common omission. Two sessions have had it missing on first pass.

**SLA differ:** Compliance is 2–5 business days (light vs. full review). FCS is 3 business days.

## McKinsey/BCG Slide Deck Assembly

When building Aecon-branded slide decks (NOT long-form briefings — those use html-effectiveness):

### Structure (14–16 slides)
1. **Title slide** (dark charcoal) — logo, process name, attribution
2. **Executive Summary** — 3 impact cards with numbers
3. **Problem Assessment** — impact boxes showing cost to each team
4. **Process Overview** — horizontal 7-step flow with owner badges
5. **Intake & Triage** — before/after split
6. **Review Gates** — Technical Assessment (left) + Compliance + FCS (right, stacked)
7. **Compliance Detail** — table with FAR/DFARS citations
8. **Vendor Lifecycle** — 3 cards: negotiate, deploy, renew
9. **70/30 Framework** — split-grid visual
10. **SharePoint Architecture** — 4 lists + 3 flows
11. **RACI Matrix** — full accountability table
12. **Implementation Timeline** — 4-week roadmap
13. **Success Metrics** — 6 metric tiles
14. **Decisions Required** — 4 leadership questions
15. **Risk Assessment** — severity table
16. **Closing** (dark charcoal) — next steps

### Technical Specs
- **Scroll-snap:** `html { scroll-snap-type: y mandatory; }` — each `.slide` is `min-height: 100dvh; scroll-snap-align: start;`
- **Keyboard nav:** ↑↓/scroll, F fullscreen, O overview grid. Use `IntersectionObserver`, NOT manual scroll listeners.
- **Dark slides:** Only charcoal `#252525` — title and closing. Use solid hex (`#303030` for cards) — never `rgba(255,255,255,*)` (Safari renders it invisible).
- **Action titles:** Full sentences at top of each slide. Not topic labels. McKinsey/BCG pattern.
- **Takeaway boxes:** Red left-border (`var(--web-red)`), ivory background. "So what?" synthesis at bottom of key slides.

### Design Rules
- **Red accent < 15%** of any layout — use for badges, borders, key stats, not backgrounds
- **Body text:** 14px Univers, line-height 1.429 (exact brand spec)
- **Process flow:** Flexbox with equal-width `.process-step` cards. Highlight owner's steps with subtle pink tint (`#FEF5F5`).
- **RACI table:** A=Accountable in charcoal bold, R=Recommends in red, C=Consulted in gray, I=Informed in silver.
- **Metric tiles:** Large red numbers (38px) with small gray labels. 3×2 or 3×1 grid.

## HARBOR 70/30 in Aecon Decks

When presenting process designs: call it a "design principle," never "HARBOR framework."

- **70% standardized core:** Charcoal-bordered card — "Works the same way regardless of organization"
- **30% configurable surface:** Red-bordered card — "Adapts to the organization's structure"
- **Out of scope:** Muted card with ✗ markers — "Priced and managed independently"

Use `.split-grid` with `7fr 3fr` for the visual ratio.

## FCS Function SOP Pattern (Internal Operating Procedures)

When Mark Payne or FCS leadership requests an internal operating procedure / SOP for a specific FCS function (Procurement Manager, Subcontracts Manager, Contracts Manager, etc.):

### Research Phase
1. **Read all local source files** — the user's `~/repos/aecon-fcs/` repo is the primary source:
   - `00-calls/` — call transcripts and meeting minutes (search for the function owner's name)
   - `working/` — extracted documents from Google Drive, analysis files
   - `working/extracts/` — raw extracted text from PPTX, DOCX, XLSX files
   - `03-research/` — personnel dossiers, compliance research
2. **Cross-reference standup recordings** — daily standup minutes often contain the function owner describing their process in their own words.
3. **Map the workflow** — identify 8-12 stages. The 10-stage template used for FPM SOP: Requirement Intake → Vendor Sourcing → Compliance Verification → Decision Gate → PO Execution → Invoice & Payment → Root Cause Analysis → Team Building → Process Documentation → Small Business Program.

### Build Phase
4. **Produce two deliverables:**
   - **HTML reference document** — html-effectiveness aesthetic (ivory/clay/slate), self-contained. Detailed walkthrough of each stage with owner, trigger, inputs, outputs, decision gates, and compliance checkpoints. RACI matrix. Appendices for frameworks and SharePoint references. 30-40KB.
   - **PPTX deck (white-labeled)** — 10-12 slides using pptxgenjs. Aecon brand (charcoal `#252525` dark slides, web-red `#C8102E` accent, ivory `#FAF9F5` backgrounds). Set `pres.author` to the function owner. No Amyn references anywhere.
5. **For the HTML:** Use the same structure as `fcs-procurement-sop-fpm-2026-07-22.html` — BLUF card, role overview, process flow grid, stage cards with numbered steps, RACI table, compliance checkpoint grid, appendices.
6. **For the PPTX:** 12-slide template: Title → BLUF → Role → Lifecycle Overview → Stages 1-2 → Compliance → Decision Gate & PO → Invoice & Root Cause → Team Building & Docs → Small Business → RACI → Next Steps. Use Calibri (safe font for cross-platform rendering). Layout structure: `LAYOUT_16x9`, 0.5" minimum margins.

### PPTX White-Label Verification
7. **After building the PPTX**, verify white-labeling with these commands:
```bash
# Check pptxgenjs author metadata
python3 -c "from pptx import Presentation; p=Presentation('output.pptx'); print(p.core_properties.author)" 
# Must show the function owner's name, NOT Amyn

# Check slide content for Amyn references
markitdown output.pptx 2>/dev/null | grep -i "amyn\|aporbanderwala" && echo "FAIL" || echo "CLEAN"

# Check for agent attribution
markitdown output.pptx 2>/dev/null | grep -i "hermes\|ai agent\|auto-generated" && echo "FAIL" || echo "CLEAN"
```

### Dual-Format Delivery
8. Deploy both files to Nextcloud briefings with consistent naming:
   - `fcs-sop-<function>-YYYY-MM-DD.html` — full reference
   - `fcs-sop-<function>-YYYY-MM-DD.pptx` — shareable deck
9. Report both links to the user. The HTML is the authoritative reference; the PPTX is for sharing with the function owner and team.

### Adversarial Review Gate (Required Before Delivery)
10. **After building the SOP**, dispatch an adversarial review agent to check for regulatory and process errors:
    - Use a leaf agent with federal procurement expertise context
    - The agent reads both the HTML and PPTX via their URLs
    - Key questions: factual regulatory errors, missing process stages, RACI sense, missing compliance gates, PPTX usability
    - The review agent MUST have a working provider — check delegation config first (see pitfall below)

### Pitfalls
- **Don't guess the workflow** — every stage must be traceable to a source file (call transcript, standup minutes, or extracted document). If you can't trace a stage, don't include it.
- **Don't skip the function owner's own words** — call transcripts where they describe their process are the most authoritative source.
- **The PPTX must be genuinely white-labeled** — if the user says "make it as if he was the author," the PPTX metadata author field must be set to that person, and markitdown extraction must return zero Amyn/agent references.
- **The HTML SOP is NOT a branding vehicle** — use html-effectiveness (unbranded internal reference), not Aecon brand kit. Only the PPTX carries Aecon branding.
- **Delegation provider must be direct, not OpenRouter** — OpenRouter frequently hits credit limits on subagent dispatches. Before running the adversarial review, ensure `hermes config get delegation` shows `provider: deepseek` (or the user's primary provider), NOT `provider: openrouter`. Configure with: `hermes config set delegation.provider deepseek` and `hermes config set delegation.model deepseek-v4-pro`.
- **3 common regulatory errors in procurement SOPs** — the adversarial review found these in the FPM SOP v1.0 and they will recur in future SOPs unless checked: (1) Small business set-aside triggers at the simplified acquisition threshold ($250K) when FAR 19.502-2(a) triggers at the micro-purchase threshold ($15K). Always cite the correct threshold. (2) "Three bids in a buy" presented as a FAR requirement — it's not. FAR Part 6 requires full and open competition; the three-bid rule is guidance under FAR 13.106-3(b) for simplified acquisitions only. Use tiered standards: ≤$15K no competition, $15K-$250K 3+ sources, >$250K full FAOC. (3) Section 889 Part B (FAR 52.204-26, use ban) is separate from Part A (FAR 52.204-25, procurement ban) and must be a distinct compliance gate. Both must be flowed down.

## Competitive Landscape / Vendor Assessment Briefings

A new class of Aecon deliverable emerged in July 2026: evaluating **how a third-party service provider or vendor could address Aecon's specific federal compliance needs** — and comparing multiple options side-by-side against Aecon's unique situation (FOCI-exposed Canadian parent, 2-person IT team, existing GCC High enclave, CMMC L2 cert under Jackson, sub CUI leasing model).

### When to Use This Pattern

- User asks to research a company "and what they could do for Aecon"
- User mentions a specific service provider and asks for a briefing with recommendations
- User needs to evaluate multiple vendors/partners against Aecon's specific compliance gaps
- User asks for a buy/build/partner recommendation for a federal compliance capability

### Research Cascade (Multi-Source, Parallel)

When researching a provider from scratch for Aecon:

1. **Primary source:** Browser-navigate the company's website (fastest, captures dynamic content and navigation structure). Extract their product pages, about page, leadership, and case studies via `browser_navigate` + `browser_snapshot` or `web_extract`.
2. **Competitor discovery:** Search for comparables. Use `web_extract` with known competitor URLs when search engines are rate-limited. Focus on: (a) full-service MSPs, (b) platform-only GRC tools, (c) boutique consultancies. Categorize each.
3. **Aecon context:** Session-search for existing Aecon project analysis, strategic assessments, needs matrices, and compliance gap analyses. Cross-reference every provider capability against Aecon's documented needs — NOT against generic DIB needs.
4. **Direct competitor pages:** `web_extract` each competitor's landing page and core product pages for positioning, metrics, team size, and target customer profile.

**Fallback chain when search backends fail** (web_search empty, firecrawl 402, ddgr rate-limited): `web_extract` known URLs → `browser_navigate` for dynamic pages → `read_file` for cached dot-mil/dot-gov pages → session_search for existing project context on the client. Do NOT burn time retrying broken search APIs.

### Deliverable Structure

Use the following eight-section structure for Aecon vendor assessment briefings:

| Section | Content |
|---------|---------|
| **01 — Provider Profile** | What they do, founding story, key stats (customers, team, certifications), business model, differentiator |
| **02 — Service Portfolio** | Specific services mapped against Aecon needs, with a fit column (HIGH/MEDIUM/LOW) |
| **03 — Competitor Landscape** | 2-4 comparable firms with profile cards — each card: name, URL, scale, model summary, key strength, key limitation |
| **04 — Comparative Analysis Matrix** | Capability × competitor table with rows for every Aecon-relevant dimension. Score each: green (core strength), amber (partial), red (not available). Columns: capability name + one per competitor. |
| **05 — Aecon Situation & Needs** | Current state, known gaps, regulatory urgency. List needs as a table with priority (P0–P2) and explanation. |
| **06 — Multi-Lens Assessment** | Evaluate the primary provider through **three distinct lenses**, each with its own section header and banner signal: |
| | **Lens 1 — As a Managed Service Provider:** Can they offload operational work for Aecon's team? What specific gaps do they fill? |
| | **Lens 2 — As a Technology Provider:** Is their platform/tool right for Aecon's scale? Will Aecon outgrow it? |
| | **Lens 3 — As a Strategic Benchmark:** What can Aecon learn from their business model even without partnering? (Validates market assumptions, pricing models, competitive positioning) |
| **07 — Alternative Partner Paths** | 2-3 named alternatives (Option A/B/C), each with: advantage over primary, disadvantage, verdict sentence. Include a recommended hybrid approach as a highlighted callout. |
| **08 — Recommendations & Action Items** | Numbered recommendation cards (border-left colored), each with: why, action, cost, timeline. End with a **Summary Decision Framework** table: if priority X → lead partner → Amyn role → timeline. |

### The Three Lenses

This framework is the key analytical move that differentiates Aecon vendor assessments from generic company research. Every vendor evaluation should pass through all three:

**Lens 1: As a Managed Service Provider (operational fit)**
- Can they offload work Aecon's team can't or shouldn't do?
- Do their service lines match Aecon's documented gaps (P0/P1 needs)?
- What's their pricing model — does it scale the way Aecon needs?
- *Output: fit ratings per Aecon need (Strong/Moderate/Weak)*

**Lens 2: As a Technology Provider (platform fit)**
- Is their tool/platform appropriate for Aecon's scale and complexity?
- Will Aecon outgrow it? If so, when?
- Does it compete with or complement what Amyn is building in-house (AI automation, FARchat, compliance agents)?
- *Output: adoption recommendation (use now / pilot / skip / integrate)*

**Lens 3: As a Strategic Benchmark (market intelligence)**
- What does their business model tell Aecon about the market?
- Their customer count validates the market opportunity — what does it prove about Aecon's own plans?
- Their pricing model is a reference point for Aecon's enclave-as-a-service pricing
- What gaps exist in the market that NEITHER this provider NOR Aecon currently fills? (These are product opportunities)
- *Output: validated market assumptions, pricing reference, identified product gaps*

### Decision Framework Table

End every vendor assessment with a single decision table:

```
| If Aecon's Priority Is… | Then Lead Partner Is… | And Amyn's Role Is… | Timeline |
|---|---|---|---|
| Immediate [gap] relief | [Provider] ([specific service]) | Define scope, manage transition | Weeks 1-2 |
| [Specific objective] | [Provider] ([area of expertise]) | Adapt their methodology; build X in-house | Weeks 2-6 |
| [Tactical need] | [Provider] (free/bridge tier) | Pilot deploy, validate, present results | Week 1 |
| [Strategic need] | External counsel + HARBOR research | Lead research, engage counsel, draft pathway | Months 1-3 |
| [Differentiator need] | HARBOR (Amyn's IP) | Build agents, automate, measure savings | Ongoing |
```

### Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Evaluating provider against generic DIB needs instead of Aecon's specific FOCI situation | Every section must cross-reference Aecon's documented gaps (from Aecon project analysis). If it doesn't answer "how does this help Aecon with its Canadian parent / 2-person IT team / sub leasing model?", it's off-target. |
| One-dimensional assessment (only as MSP, not as tech provider or benchmark) | All three lenses required. Each lens produces different insights. Lens 3 (benchmark) is often the most actionable even when the provider isn't a fit. |
| Search engine dependency blocking research | Build the fallback chain proactively. When search tools fail in the first call, switch to web_extract + browser_navigate immediately. Don't retry the same failing tool. |
| Recommendations without costs | Every recommendation must include a cost indicator (free to start, $450/mo, retainer-based) — Aecon needs budget data for decision-making. |
| Missing the "Amyn's role" column in the decision framework | The table isn't just about which partner — it defines what Amyn personally does in each scenario. This clarifies scope and prevents expectation mismatch. |

## Eval Gate (Pre-Delivery)

Before any Aecon deck goes live, run these checks:

```
# White-label (for Sinem's decks)
grep -ci "amyn\\|aporbanderwala" deck.html  # must be 0

# Brand compliance
grep -c "rgba(255,255,255" deck.html        # must be 0
grep -c "#2A2A2A\\|#FDE8EB\\|#B0B0B0\\|#2D8659" deck.html  # must be 0

# Content completeness
grep -c "FedRAMP" deck.html                 # must be >0 on compliance slides
grep -ci "kerem" deck.html                  # must be 0

# Attribution
grep -ci "hermes\\|ai agent\\|auto-generated" deck.html  # must be 0

# Current-state language — flag "is being evaluated" / "pending" for manual review
grep -ci "is being evaluated\\|is being assessed\\|is being considered\\|pending review\\|under evaluation" deck.html
```

## Current-State Language Rule

**Pitfall:** Defaulting to "is being evaluated" or "pending" for systems whose deployment status you haven't verified. This was caught when AVD was described as "being evaluated" when it was already deployed for CUI workloads.

**Rule:** Before writing any future-tense or conditional language about an operational system:
1. Ask the user or check source documents whether the system is actually deployed
2. If confirmed deployed, use present tense: "is already deployed," "is in use," "the current operational posture"
3. If truly unknown, state it explicitly as an assumption — not as a fact about the system
4. Never use "being evaluated" as a default — it erodes trust when the system turns out to be live
