---
name: harbor-engagement-templates
description: Research, structure, pitch, and formalize HARBOR's subcontract and consulting engagements -- from OSINT reconnaissance and compliance gap analysis, through HTML pitch decks and priced FFP SOWs, to legal entity setup and template filling. Covers the full engagement lifecycle including counterparty research, compliance gap mapping, incumbent provider analysis, pitch deck creation, SOW drafting, contracting entity formation, and legal template filling. Templates live in 2026_books/operations/harbor-initiative-llc/01-current/engagement-ready/.
---

# HARBOR Engagement Template Filling and Engagement Pipeline

This skill covers the full HARBOR engagement lifecycle — from identifying a counterparty through executing the subcontract. The legal template filling workflow (Section 2 onward) is one phase of a broader pipeline.

## 1. Engagement Pipeline Overview

For each new HARBOR subcontract or direct engagement, run this pipeline from top to bottom. Not all phases apply to every engagement (e.g., a direct consulting engagement may skip entity formation), but the research and compliance phases are mandatory.

```
Phase 1: Research         OSINT recon → tech stack mapping → DNS recon → LinkedIn analysis
Phase 2: Compliance Gap   CMMC/NIST 800-171 → DOE orders → QA standards → export control
Phase 3: Competitive      Map incumbent MSP/provider capabilities → find HARBOR's complement gap
Phase 3.5: Multi-Wave     Fill research gaps with Wave 2-3 agents → save traces
Phase 4: Pitch            Build HTML pitch deck → price FFP → outline delivery timeline
Phase 5: SOW              Create formal SOW with CLINs, deliverables, acceptance criteria
Phase 5.5: Trace Review   Read ALL subagent build transcripts → check for pricing drift,
                          entity violations, scope creep, forbidden references → fix before gate
Phase 5.75: PM Plan       Build Internal PM Execution Plan (POA&M, resources, risks, budget,
                          tools, cadence) as 4th deliverable
Phase 6: Entity Setup     Form masked LLC → SAM.gov registration → bank accounts (if needed)
--- QUALITY GATE ---      Parallel adversarial judges → cross-document grep validation → fix all
Phase 7: Legal Templates  Fill NDA/MSA from existing templates → sign
```

### Phase 1: Counterparty Research

Run these research actions in parallel where possible. All agents must be traced (save logs to a `research/` directory).

**OSINT Recon:**
- Website crawl: map products, services, locations, leadership, news
- DNS recon: identify tech stack (M365, Salesforce, ERP, MSP, hosting providers)
- LinkedIn: find key personnel, their roles, career history
- SAM.gov: search for prime contracts, past performance, NAICS codes (use `api.sam.gov` for registrations; `usaspending.gov` for awards)
- SEC filings: for public or large private entities, use EDGAR for business structure insights

**Tech Stack Mapping:**
- DNS TXT records (SPF, DKIM, DMARC) — reveal email security vendor
- MX records — reveal email platform (M365, Google, on-prem)
- CNAME subdomain probing — reveal CRM (Salesforce, HubSpot), ERP, ticketing systems
- Website JS bundle analysis — reveal analytics, CDN, payment processors
- SMTP banner / HTTP headers — reveal web server, application framework
- See `references/subcontract-research-pipeline.md` for the full tool chain

**Resume Scan:**
- Extract individuals' career history (LinkedIn, company bios)
- Map past employers, clearance history, relevant domain expertise
- Identify personal connections to the counterparty's decision makers

**Deliverable:** Structured research directory with all findings saved as markdown under `research/` in the engagement repo.

### Phase 2: Compliance Gap Analysis

Research the counterparty's regulatory environment based on their industry and prime contracts:

- **CMMC/NIST 800-171**: If they handle DoD contract data (CDI/CUI), check their MSP or IT provider's capability. Use `cmmc-l2-compliance-toolkit` skill for deep toolkit builds.
- **DOE Orders**: For nuclear/energy vendors — DOE O 471.1B (IT), 414.1D (QA), LANL Exhibit G cybersecurity appendices, Pantex/Y-12 UCNI protection protocols, PX-6668 training, Technology Control Plans. See `references/doe-compliance-pattern.md`.

**Export Control orientation (critical for nuclear/DOE):** When building the compliance narrative for a nuclear/DOE firm, lead with export control, not CMMC. The immediate risk for UF₆ cylinder manufacturers, NRC-licensed facilities, and DOE prime subcontractors is uncontrolled export of technical data (ITAR 22 CFR 120–130, EAR 15 CFR 730–774, DOE O 471.1B). CMMC Phase 2 compliance is not a genuine urgency driver for most DOE firms — the DoD enforcement timeline is soft and most nuclear work is DOE- or NRC-governed, not DoD. The deck should say "The immediate risk is export control" and address CMMC in one line at the bottom of the gap assessment.
- **NRC**: 10 CFR Part 73 (physical security), 10 CFR Part 110 (export of nuclear equipment/UF6 cylinders).
- **QA Standards**: ASME NQA-1, ISO 9001, 10 CFR 50 Appendix B — depending on the product.
- **Export Control**: ITAR vs EAR determination for the specific products/services.

**Key insight:** Research the counterparty's *incumbent* IT/MSP provider. Their capabilities define where HARBOR fits — complement, not replace. See Phase 3.

**Deliverable:** Compliance gap register — what they need vs. what they have today.

### Phase 3: Incumbent Provider Competitive Analysis

Before pitching, research who the counterparty already pays for IT and compliance:

- Identify their MSP, MSSP, cloud provider, compliance consultants
- Map that provider's known capabilities (CMMC certification? GCC High? DOE experience?)
- Identify what the provider CANNOT do (nuclear-specific compliance, enclave architecture, RPO advisory)
- Position HARBOR as complement, not replacement — this is more credible and less threatening

**Example from practice:** Westerman Inc. uses NexusTek as their MSP. NexusTek is CMMC Level 2 certified (C3PAO-verified, April 2026) but lacks nuclear/DOE domain expertise, RPO authorization, SharePoint/export-control partitioning, and proprietary methodology. HARBOR positioned as strategic complement with NexusTek as implementation subcontractor.

**Deliverable:** Provider gap analysis — what they cover vs. what HARBOR adds.

### Phase 3.5: Research Delivery (Multi-Wave Pattern)

Research agents are often incomplete on the first pass. Use this multi-wave pattern — but critical distinction below.

1. **Incorporate immediately:** As each research agent finishes, read its output. Don't wait for all agents.
2. **Identify gaps:** What's missing? Compliance timeline details? Incumbent MSP's specific CMMC cert status? Key personnel career history?
3. **Wave 2:** Dispatch 1-3 more targeted agents with narrower scope based on gaps. If an agent timed out, re-dispatch with fewer URLs or a smaller goal.
4. **Wave 3 (if needed):** One final agent per remaining gap before compiling deliverables.
5. **Save everything:** All agent outputs go into `research/` in the engagement repo with clear filenames.

**⚠️ Critical distinction — build-in-parallel vs. deliver-after-complete:**

You CAN build deliverables from local context while research agents are still running (this is parallel work, not premature delivery). You CANNOT ship deliverables to the user until ALL research waves are complete AND incorporated.

- **Allowed:** Start drafting the pitch deck HTML while Wave 1 research agents run, using your own analysis of the local site mirror and OSINT data. Fill in research-dependent sections (pricing benchmarks, competitor capabilities, compliance timeline) as placeholders or range estimates.
- **Not allowed:** Presenting the pitch deck as "complete" or "ready" when research agents haven't returned findings that could materially change pricing, compliance advice, or competitive positioning.

The pattern from the July 2026 Westerman engagement: 3 research agents dispatched (website scan, competitive landscape, repo catalog). While they ran, the orchestrator built the capability inventory from porbanderwala.com browser scans. When agents returned, their findings were incorporated into the pitch deck and SOW — one agent revealed NexusTek was CMMC L2 certified (not just "CMMC-registered"), which materially changed the competitive positioning section. If the deliverables had shipped before that finding arrived, the competitive analysis would have been wrong.

**Pitfall — Monitor live transcripts:** Read `delegate_task` live transcripts while agents run. If an agent is researching the wrong thing (e.g., researching the MSP's entire service catalog instead of just their CMMC cert status), kill and re-dispatch with a tighter goal. Don't wait for it to finish.

**Pitfall — Don't accept gaps as final:** If DNS recon returned partial data, dispatch a second agent with just the missing domain. If the compliance landscape agent missed DOE orders, dispatch a DOE-specific agent. The first wave almost always has gaps — Wave 2 fills them.

### Phase 4: Pitch Deck

Build an HTML pitch deck (Thariq aesthetic, self-contained) targeting the counterparty's decision maker. Choose between two templates based on audience and context.

**TEMPLATE A — Quick 5-slide (first meeting, <15 minutes, cold audience):**

| Slide | Content |
|-------|---------|
| 1 | **The Opportunity** — Industry tailwinds + counterparty position + urgency/compliance imperative |
| 2 | **Current State** — OSINT-derived gaps with severity ratings; shows you did your homework |
| 3 | **Proposed Engagement** — 3-phase delivery with key deliverables per phase |
| 4 | **Investment & Returns** — FFP pricing with breakdown + value proposition |
| 5 | **Why HARBOR** — Credentials, agent army model, ~30 AI agents with full audit trails, Export Control Practitioners, relevant experience |

**TEMPLATE B — Evolved 21-slide (CEO deep-dive, 30-60 minutes, prepared audience):**

| Section | Slides | Content | 
|---------|--------|---------|
| **A: The Case** | 3 | Title, market stats/compliance imperative, competitive context |
| Section B Divider | 1 | Transition slide: "The Solution" with summary statement |
| **B: The Solution** | 6 | Discovery sprint detail, phase timeline (all CLINs at a glance), 3 phase detail slides with deliverables and acceptance criteria, before/after transformation |
| Section C Divider | 1 | Transition slide: "The Why" |
| **C: The Why** | 5 | Team (Amyn & ~30 AI agents, export control practitioner network), four-question filter, competitive positioning punch list (4 rows, cost-of-inaction header), pricing transparency |
| Section D Divider | 1 | Transition slide: "The Ask" |
| **D: The Ask** | 1 | CTA — authorize Phase A (CLINs 0000-0002) today, Phase B contingent on discovery findings |
| Appendix Divider | 1 | Transition slide: "Supporting Evidence" |
| **Appendix** | 4 | OSINT methodology, regulatory references, full SOW pricing table, risk register backup |

**Navigation features required for Template B:**
- Section dividers between A/B, B/C, C/D, and before Appendix — each is a dedicated slide with section name and a 1-line transition statement the presenter reads aloud
- Keyboard shortcuts: `N`/`Right Arrow` (next), `P`/`Left Arrow` (prev), `1-9`/`0` (jump to slide N), `O` (overview grid with thumbnails), `F` (fullscreen toggle)
- Mobile: `100dvh` slides (not 100vh — avoid mobile browser chrome collapsing), touch-swipe through overflow-y
- Print: `@page { size: landscape; }` with `break-after: page` and light/white background
**Slide 5 (Template A) / Team slide (Template B) — the agent army differentiation:**

HARBOR is not a consultancy selling hours. The "army of AI agents" model is the structural competitive advantage. Frame it as: "One principal with an agent army delivers what would take a 5-person consultancy." Back it with specific infrastructure evidence (37 Docker containers, 13 cron jobs, 6 live web applications, autonomous coding/research/compliance agents with full audit trails) drawn from Amyn's live production environment. Every slide that mentions delivery velocity should subtly reinforce this — it's the reason HARBOR can do websites + compliance + automation under one FFP contract when competitors specialize in one.

**Slide deck format — HTML scroll-snap, not PDF pages:** Use `scroll-snap-type: y mandatory` with 100dvh full-viewport sections for proper slides. Each slide is a `<section>` with `scroll-snap-align: start`. Include a slide counter in the bottom-right corner. Use HTML-first format so the deck renders in any browser without a PDF viewer. Dark theme for presentations (HARBOR brandkit with navy/amber); light theme (ivory/clay, html-effectiveness aesthetic) for reference documents. The slide deck is a presentation tool — it should feel like slides, not a vertically scrolling web page. See `references/pitch-deck-building.md` for the complete CSS/HTML/JS pattern.

**Practitioner positioning (team slide):

**The "proven equivalence" clause for new entities (FAR 15.305(a)(2)(iv)):** When the contracting entity is a newly formed LLC with no past performance of its own, include this note in the FAR disclaimers section of the pitch deck and SOW. The regulation allows evaluating individual past performance and technical capability when the entity itself has no track record. Use exact language: "Per FAR 15.305(a)(2)(iv), this proposal evaluates individual past performance and technical capability. Federal prime contract revenue is $0. Individual past performance and technical qualifications are as documented."

**Pricing pattern:** For a sub-k engagement (nuclear/DOE compliance), benchmark:
- Base FFP: $450K-$570K for 12 months
- CLIN structure: 10 CLINs across 3 phases
- Phase 1 (Foundation): ~$120-150K, Phase 2 (Build): ~$200-250K, Phase 3 (Operate): ~$130-170K
- Annual maintenance (Year 2+): ~$60-100K (compliance monitoring, advisory retainer)

**Deliverable:** Self-contained HTML at `brief.h.porb.dev/<slug>-pitch-deck.html`, saved in engagement repo under `research/`.

**Pitfall — fabricated and unverified statistics destroy credibility.** The adversarial review WILL catch wrong dollar figures, fake regulatory citations, and fabricated source attribution. In the Westerman engagement (Jul 2026), three claims failed fact-checking:

1. **"Centrus — your acquirer" was FALSE.** Worthington Industries acquired Westerman in 2012. Centrus is a supply chain customer. The deck incorrectly labeled a customer relationship as an acquirer — caught immediately.
2. **ITAR penalty $1,448,000 under 22 CFR 126.13 was WRONG.** Correct: $1,271,078 under 22 CFR §127.10(a)(1)(i). Wrong regulation citation AND wrong dollar amount on the same claim — fatal to a compliance-focused pitch.
3. **"88-95% AI pilots never reach production (MIT/McKinsey 2025-2026)" was UNVERIFIABLE.** No evidence found for this specific statistic from these sources. Related stats exist (Gartner at 70-87%) but the precise range + prestigious attribution adds false specificity.

**Rule:** If the counterparty can independently verify a claim in 30 seconds and it's wrong, the entire pitch is undermined. Fact-check every dollar figure (cross-reference against federal register inflation adjustments), every regulatory citation (verify the subpart actually exists), and every attributed statistic (search for the source verbatim). ONE claim with two errors (wrong amount + wrong citation) is fatal.

### Phase 5: SOW Creation

Build a formal Firm-Fixed-Price SOW when templates don't exist for the engagement type. Structure:

**SOW Sections:**
1. Parties and Effective Date
2. Background / Recitals (1-2 paragraphs establishing context)
3. Scope of Work — table of CLINs with description, deliverables, acceptance criteria, timeline
4. Period of Performance (specific dates or "upon execution + N months")
5. Payment Terms (FFP, milestone-triggered invoicing)
6. Assumptions (critical — what the price depends on)
7. Exclusions (what is NOT in scope)
8. General Provisions (governing law, IP ownership, data rights, export control compliance)
9. Signatures

**CLIN 0000 — The Discovery Sprint (low-risk entry point):** Before the main engagement, offer a paid 2-week discovery sprint at a fixed price ($25K for most engagements). This single CLIN produces the detailed implementation roadmap, validates OSINT findings with on-site inspection, refines pricing for remaining CLINs, and builds trust through immediate delivery. The sprint is FFP, billed at completion (Week 2). No long-term commitment until the roadmap is signed off. If the counterparty walks away, they have a comprehensive infrastructure assessment for minimal cost. This is the single most effective deal-closing mechanism — it turns "should we spend $450K?" into "should we spend $25K to find out?"

**Immediate Authorization structure (Phase A/B/C pricing tier):** Do NOT present the SOW as a single $450K+ commitment. Structure it as three authorization tiers so the CEO sees a small first step, not a large bet:

| Tier | Authorization | CLINs | Total | Decision |
|------|---------------|-------|-------|----------|
| **Phase A — Immediate** | Signed now | CLINs 0000, 0001, 0002 | ~$55K | CEO says yes to a discovery sprint + quick wins |
| **Phase B — Contingent** | Authorized after discovery findings | CLINs 0003-000N | ~$350K-$400K | Requires seeing the roadmap first |
| **Phase C — Options** | Exercised at client discretion | CLINs >1000 | ~$50K-$100K | Separate approval gate |

Add a "Immediate Authorization" box at the top of the SOW: "CLINs 0000, 0001, and 0002 are authorized immediately upon signature. Remaining CLINs are contingent on Discovery Sprint findings (CLIN 0000 completion) and mutual agreement. Signing this SOW authorizes Phase A only."

This structure: (1) lowers the perceived risk for the CEO — $55K feels like a pilot, not a bet-the-farm decision, (2) gives the internal sponsor something concrete they can sell, (3) creates a natural check-in point where the relationship either accelerates or stops — no awkward "how do we cancel?" conversation needed.

**CLIN structure pattern (10-CLIN FFP, always start at 0001):**

| CLIN | Phase | Description | Deliverables | Price |
|------|-------|-------------|--------------|-------|
| 0001 | 1 | Compliance Assessment | Gap report, Risk register | $XX |
| 0002 | 1 | Roadmap & Planning | Implementation roadmap, Kickoff deck | $XX |
| 0003 | 2 | CUI Enclave Architecture | Architecture diagram, Configuration baseline | $XX |
| 0004 | 2 | Enclave Build & Deploy | Deployed enclave, SSP, SOPs | $XX |
| 0005 | 2 | Policy & Procedure Development | Policy manual, SOP library | $XX |
| 0006 | 2 | Compliance Artifacts | POA&M, Evidence matrix | $XX |
| 0007 | 3 | Training & Awareness | Training materials, Workshop delivery | $XX |
| 0008 | 3 | Audit Support | C3PAO liaison, Remediation | $XX |
| 0009 | 3 | Continuous Monitoring | Monthly reports, Quarterly reviews | $XX |
| 0010 | All | Project Management | Status reports, PM calls | $XX |

**CLIN specialization for nuclear/DOE engagements:** Adapt the generic CLIN structure to the counterparty's specific gaps:
- **Dual-website CLINs** (0001, 0002): When the counterparty has a main corporate site AND a separate division/product site, split them. Each gets its own CLIN with its own budget. If one site is statically hosted and the other is WordPress, they require separate approaches.
- **Export control assessment** (typically CLIN 0003): Data flow mapping, Technology Control Plan (TCP), DMARC enforcement, DLP rule configuration. Requires on-site stakeholder interviews.
- **NIST 800-171 assessment + SPRS posting** (typically CLIN 0005): Full 110-control assessment, SSP + POA&M development. Note CMMC Phase 2 status in the compliance clause.
- **UCNI/DOE training CLIN** (typically CLIN 0007): DOE O 471.1B awareness training, site-specific acknowledgment forms (PX-6668 at Pantex, Y-12 UCNI Briefing, SRS Training, LANL Exhibit G), deemed export awareness, automated 2-year recertification tracking.

**CLIN renumbering propagation:** When the SOW CLIN structure changes (e.g., a new CLIN is added to Phase 2 shifting all subsequent numbers), you MUST update ALL other deliverables (pitch deck, research brief, pricing tables) that reference those CLIN numbers. Search every file in the engagement repo for the old CLIN range (e.g., "0004–0006") and replace with the new range. The adversarial review WILL catch stale CLIN references.

**Acceptance criteria:** For each CLIN, define what "done" means — document delivered, last review complete, training hours logged, certificate issued.

**SOW provisions checklist (commonly missed, caught by adversarial review):**
- **Export Control Clause:** Explicitly state whether HARBOR will access export-controlled data. If HARBOR accesses it, state protections (enclave, access controls, nationality verification). If HARBOR does NOT access it, state the exclusion clearly and how the SOW accommodates that gap.
- **Limitation of Liability:** Maximum liability (typically 1× SOW value or $50K, whichever is greater). Exclusions (IP breach, confidentiality breach, gross negligence — these should have no cap).
- **Force Majeure:** Standard clause covering acts of God, war, terrorism, government action, internet outages, etc. Mutual (both parties excused). Supplement with a "mutual cooperation" obligation to mitigate.
- **Intellectual Property:** Pre-existing IP (HARBOR methodology, OORAH model, Agentic OS, templates) stays with HARBOR. Custom deliverables (SOPs, policies, architecture diagrams for this engagement) are work-for-hire owned by client. All IP must be flow-down protected through the prime contract.
- **Data Rights:** Unlimited rights for government data produced under the contract. HARBOR gets limited rights to use anonymized/aggregated compliance data for methodology improvement.
- **Insurance Requirements:** Professional liability ($1M minimum), cyber liability ($2M minimum), general liability ($1M). Certificates required before invoice 0001.

**Delivery model clause (the agent army):** Include a background section and delivery model description early in the SOW (after "Background & Purpose") describing the AI agent-augmented delivery model. Template language: "[Contracting Entity] LLC operates an army of AI agents — autonomous AI research, coding, and compliance systems — enabling speed, scale, and precision that traditional consultancies cannot match. Every deliverable is augmented by this agent infrastructure, reducing human labor hours while increasing output quality and auditability. The Contractor deploys autonomous AI agents for research synthesis, code generation, compliance assessment, content creation, and process documentation. These agents produce fully-auditable deliverables with traceable reasoning chains. Human oversight validates outputs; agents handle the heavy lifting. This model enables the Contractor to deliver at 70–80% automation efficiency — one principal covering what would traditionally require 2–3 FTE equivalents." This clause preempts "how does one person do all of this?" objections.

**Deliverable:** Self-contained HTML SOW at `brief.h.porb.dev/<slug>-sow.html`, saved in engagement repo under `research/`.

### Phase 5.5: Subagent Build Trace Review Protocol

After you dispatch parallel subagents to BUILD deliverables (pitch deck, SOW, brief, PM plan), and BEFORE the adversarial review gate, you MUST systematically review every subagent's build transcript for drift from the plan.

**Why this is needed:** Subagents with write access and broad instructions will independently change pricing, add scope, rename entities, and restructure sections — all without asking. These changes silently propagate across deliverables and break cross-document consistency. In the Westerman engagement (Jul 2026), the SOW subagent changed CLIN 0001 from $15K to $40K-$50K and CLIN 0002 from $15K to $25K-$35K — causing the immediate authorization total to jump from $55K to $90K-$110K across the pitch deck, brief, and SOW before the orchestrator caught it.

**The protocol:**
1. **Read the full transcript.** Every subagent task has a live transcript under `~/.hermes/cache/delegation/live/<delegation_id>/task-<N>.log`. Read it completely — especially the write_file and patch calls.

2. **Check for drift on these dimensions:**

   - **Pricing changes** — Did the agent modify any CLIN prices from what the plan specifies? Even a single changed number ($15K → $40K) will cascade across all deliverables.
   - **AC/DoD violations** — Did the deliverable meet its Acceptance Criteria and Definition of Done from the plan? If the plan specified per-item DoD, verify the subagent actually met it.
   - **Entity name changes** — Did the agent add, remove, or rename the contracting entity?
   - **Scope additions** — Did the agent add CLINs, phases, or deliverables that were not in the plan?
   - **Forbidden references** — Did the agent mention LFC, Navaide, Aecon, or any other OPSEC-prohibited entity?
   - **Section restructuring** — Did the agent reorder sections or change the document's structure from what was planned?
   - **Agent count** — Did the agent use an exact number when the plan specifies "~30"?

3. **Build a gap plan.** Identify every discrepancy between the subagent's output and the plan. Present these to the user as findings with fix instructions.

4. **Do NOT accept subagent output on trust.** Subagents consistently over-scope (adding CLINs), modify prices independently, and insert forbidden references. Assume every subagent drifted until the trace proves otherwise.

**Pitfall — the pricing cascade:** The most expensive failure mode. When the SOW subagent changes CLIN 0001 from $15K to $40K (because they felt the website redesign was undervalued), the Phase A total jumps from $55K to $95K. Now the pitch deck, the brief, and the internal plan all reference different prices. Fixing this requires: reverting the SOW price, checking every other deliverable for the wrong price, verifying the new total in each document's pricing table, subtotals, and Phase A/Immediate Authorization box, AND checking that no other CLIN was changed as a side effect. This cleanup costs 5-10× the minutes the subagent "saved" by modifying prices on its own.

**Fix:** Before any subagent dispatch, write a single source-of-truth pricing table to disk as a reference file (e.g., `research/pricing-lookup.md`). Include in the subagent's context: "CLIN prices are locked in `/absolute/path/to/pricing-lookup.md`. Do not change any CLIN price. If you believe a price is wrong, stop and flag it — do not modify on your own."

**Pitfall — identical drift across subagents:** When three subagents independently add "Comprehensive assessment report" to different CLIN descriptions, the result is three nearly identical CLINs with different prices. This is a symptom of insufficiently specific CLIN descriptions in the plan. The fix is to write each CLIN's description and deliverables with enough specificity that a subagent cannot confuse it with another CLIN.

### Phase 5.75: Internal PM Execution Plan (4th Deliverable)

After the pitch deck, SOW, and internal brief are drafted, build a comprehensive Internal PM Execution Plan as a fourth sibling deliverable. This document is for the project manager and internal team — not for the client/CEO. It is the single source of execution truth after the deal closes.

**Target audience:** The project manager (Doug, in Westerman's case) who needs to understand what happens after the SOW is signed — not the CEO making the buy decision.

**Sections (from practice — Westerman engagement, Jul 2026, 883 lines, 150KB):**

| Section | Content | Detail Level |
|---------|---------|-------------|
| **Master POA&M** | All 12 CLINs (0000–0010 + 1001–1002) with numbered step-by-step work breakdown | Every CLIN has 5-9 concrete numbered sub-steps, not one-liners |
| **Resource Matrix** | Phase assignment table — which CLIN belongs to which Phase (A/B/C), dependencies between CLINs | One row per CLIN with phase, duration, predecessor CLINs, personnel need |
| **Dependency Map** | Directed graph of CLIN prerequisites — what must finish before what can start | DO NOT scope this smaller than the plan demands |
| **Staffing & 1099 Plan** | What work the principal does directly vs what gets subcontracted to 1099 practitioners | Practitioner skills mapped to CLINs, no names |
| **Tools & Infrastructure Registry** | Every tool needed per CLIN (SharePoint, DNS, WordPress, Nextcloud, AdGuard, social platforms) | Include setup time, account creation burden |
| **Risk Register** | 10-15 risks with likelihood, impact, mitigation, owner | Include ITAR/OPSEC/infrastructure risks |
| **Budget Model** | Per-CLIN pricing with subtotals, total range, and a multi-year view (base + 2 option years) | Same pricing as all other deliverables — cross-reference enforced |
| **Delivery Cadence** | Weekly sprint structure, monthly review cadence, quarterly business reviews | Standard project management templating |
| **Quality Gates** | Per-CLIN completion criteria, review process, sign-off requirements | Distilled from the SOW's acceptance criteria |

**Design pattern:** This is a REFERENCE document, not a pitch piece. Use the ivory/clay html-effectiveness aesthetic (not the dark HARBOR deck theme). Maximize information density — dense tables, compact typography. Add a table of contents at the top with anchor links. This document is printed and brought to the kickoff meeting.

**Pricing consistency enforcement:** The Internal PM Plan's pricing table MUST match the SOW's pricing table exactly. Before deploying, `grep '\$'` in both files and compare. If they differ, the PM plan's pricing is wrong — fix it to match the SOW.

**Deliverable:** Self-contained HTML at `brief.h.porb.dev/<slug>-internal-execution-plan.html`, saved in engagement repo under `research/`.

### Phase 6: Entity Setup (Masked LLC)

When the engagement requires a separate contracting entity (e.g., when Amyn has a concurrent role at another firm and needs name separation):

**Choice of state:** Two options have been used in practice — Wyoming (lower cost) and Delaware (higher credibility with traditional firms). Both provide the same anonymity at the state public record level — no personal names appear on formation documents.

**State comparison:**

| Consideration | Wyoming | Delaware |
|--------------|---------|----------|
| Anonymity | Members/managers NOT on public Articles | Members/managers NOT on public record |
| Formation cost | $104 one-time | ~$90 filing + $300 initial franchise tax |
| Annual/recurring | $62 annual report | $300 annual franchise tax |
| State income tax | 0% | 8.7% corp rate (disregarded entity passes through to HARBOR's TX return — DE tax generally not owed) |
| Registered agent | Northwest $125/yr | Northwest ~$125/yr |
| Processing time | ~8 hours | ~8 hours |
| Legal precedent | Strong veil protection | Strongest (most litigated corporate law) |
| Perceived credibility | Lower (some primes unfamiliar with WY) | Higher (standard corporate state) |

**Decision rule:** Use Delaware when the engagement goes to a contractor who expects standard corporate domicile and anonymity is the primary driver. Use Wyoming when minimizing total cost (formation + annual) matters more and the counterparty is comfortable with non-standard domicile.

**Example in practice (Westerman engagement, Jul 2026):** The user chose Delaware explicitly for the sub-k contracting entity. The SOW references "[Contracting Entity] LLC (Delaware)" — no parent company, no personal names. Previous engagements used Wyoming for cost minimization; this one used Delaware for credibility with a traditional manufacturing firm that expects standard corporate domicile.

**Registered agent:** Northwest Registered Agent ($125/yr) — uses their address as the LLC's principal office. Same agent works for both WY and DE.

**SAM.gov registration:** An anonymous LLC CAN register in SAM.gov. The anonymity is at the state public record level; beneficial ownership is not publicly displayed in SAM.

**Tax treatment:** Disregarded entity — income flows to HARBOR's return. No separate federal tax filing. Eligible for QBI deduction (20% pass-through). Texas franchise tax applies to combined margin.

**Timeline:** ~4 weeks to operational. Formation in 8 hours. SAM.gov validation is the bottleneck (10-15 business days).

**Cost:** ~$2,600-$4,600 over 3 years (formation + registered agent + attorney for operating agreement + CPA). Delaware is slightly more expensive due to annual franchise tax.

**Deliverable:** Formed LLC with EIN, SAM.gov registration, bank account, operating agreement. See `references/masked-llc-formation-pattern.md` for full Wyoming step-by-step (adapt for Delaware by substituting state forms and fees).

### Phase 7: Legal Template Filling

Proceed to Section 2 below (Mutual NDA Filling Workflow) for the standard template-filling workflow.

### Pipeline Quality Gate: Adversarial Review & Cross-Document Consistency

After Phases 4-6 (Pitch Deck + SOW + Entity Setup) are complete and BEFORE Phase 7 (Legal Templates), run this mandatory quality gate:

1. **Self-audit first:** Check all deliverables for surface-level issues — do cited URLs resolve? Are pricing ranges the same across all docs? Do CLIN numbers match? Is the entity name consistent? Fix these before the formal review.

2. **Dispatch parallel adversarial judges:** One judge per deliverable (pitch deck, SOW, research brief, LLC guide). Each gets full tool access, all files, and explicit criteria to verify facts, citations, and internal consistency. Judges run independently.

3. **Cross-document cohesion framework:** After all judge verdicts arrive, build a cohesion matrix — claims as rows, deliverables as columns. Check every dimension:

   **Evidence consistency (the baseline):** Same entity name everywhere? Same compliance stance on CMMC Phase 2? Same vendor descriptions? Same Phase 2 CLIN range? Same dollar figures? Same regulatory citations? Every inter-document contradiction is P0.

   **Vocabulary consistency (the upgrade):** Three terms should appear in the same form across ALL deliverables:
   - Signature narrative framing (e.g., "Nuclear Renaissance → Compliance Moat → AI Execution" appears in deck AND in brief's executive summary)
   - Named frameworks (e.g., "HARBOR Compliance Framework" defined in SOW, referenced in deck AND brief)
   - Delivery model (e.g., "37 AI agents" referenced in both deck and brief, even if only summarized in deck)
   - If the deck has a tagline that doesn't appear in the brief, add it. If the brief has a framing the deck doesn't use, consider adding it.

   **CTA consistency (the ask):** Every document must present the same call to action — "Authorize CLINs 0000, 0001, and 0002 today. Phase B is contingent on discovery findings." The pitch deck's CTA, the brief's recommendation, and the SOW's signature block must say the same thing at different levels of detail.

   **Narrative arc consistency (the story):** The pitch deck's slide order should be reflected in the brief's section order. If the deck leads with "Nuclear Renaissance → Current State → The Engagement → Why HARBOR," the brief should flow the same way. Don't tell one story in the deck and a different one in the brief.

   **Pricing tier consistency:** If the deck presents $55K entry + $450-$570K full, the SOW must have an immediate authorization section for the same $55K, and the brief must explain the same structure. All three must match.

   **Tool: Cohesion matrix.** Build this before fixing:
   | Claim/Option | Pitch Deck | Brief | SOW | Status |
   |--------------|-----------|-------|-----|--------|
   | Entity name | HARBOR Initiative LLC (TX) | HARBOR Initiative LLC (TX) | HARBOR Initiative LLC (TX) | ✅ |
   | CTA | "Authorize CLINs 0000-0002" | "Doug presents → Jacob approves → Amyn joins" | "Phase A authorized immediately" | ⚠️ Different framing |
   | ITAR penalty | $1,271,078 | $1,271,078 | not cited | ⚠️ Missing from SOW |

   Every ⚠️ or ❌ in the matrix is a P0 fix.

4. **Run the 8-item grep validation:** After applying all fixes, run this concrete checklist before declaring the set clean:

   ```bash
   # 1. Zero forbidden entities
   grep -in "LFC\|Navaide\|Aecon\|OORAH\|Leatherneck" *.html

   # 2. ITAR citation correct (both dollar amount and regulation)
   grep -c "127.10\|1,271,078" *.html

   # 3. Agent count rounded (not exact)
   grep -c "~30\|approximately 30" *.html

   # 4. CMMC language: third-party C3PAO certification
   grep -c "third-party C3PAO" *.html

   # 5. Entity name: HARBOR Initiative LLC (check state too)
   grep -c "HARBOR Initiative LLC" *.html

   # 6. CTA: Phase A authorization language
   grep "CLINs 0000\|CLIN 0000" *.html

   # 7. Competitive table: all expected competitors present
   grep -c "Competitor A\|Competitor B" *.html

   # 8. Pricing consistency: same dollar amounts across all docs
   grep "\$.*[0-9]\{3,\}" *.html | grep -v "http"
   ```

   Every doc should have ≥1 hit on each check (except #1 which should be 0). If a doc scores 0 on #2-#7, investigate — the doc may be missing a required section.

5. **Fix everything:** Apply ALL judge findings AND cross-document contradictions to all deliverables. The judges' output IS the fix worklist — do not re-evaluate.

5. **Re-deploy:** After all fixes are applied, verify the combined set is consistent (re-read the most-changed docs), then deploy all deliverables to Nextcloud together.

**Critical Pattern — Fix Propagation:** A single error often propagates across multiple deliverables from the same author (e.g., "NexusTek described as CMMC-registered RPO" appears in the pitch deck, SOW, brief, AND guide). After patching the primary doc, grep for the root of the error (`grep -rn "RPO\|CMMC-registered" research/`) across every file and patch each hit. Do not assume the error is localized — it's almost certainly not.

**This gate is NOT optional.** The Pineapple Protocol requires founder review on all outbound deliverables. The adversarial gate gives the founder a clean, verified set with an audit trail of what was caught and fixed.

### Operational Security (OPSEC) — Internal Relationships

**Critical rule: HARBOR deliverables MUST NOT reveal HARBOR's internal relationships, concurrent engagements, partnership pipelines, or principal's concurrent roles.**

When a HARBOR principal (Amyn or otherwise) has a concurrent role at another firm — consulting, employment, board membership, or other engagement — that relationship does not appear in HARBOR's deliverables to any client. The contracting entity and the HARBOR relationship are the only relationships that go on paper.

**Specific prohibitions (from practice):**
- **No concurrent role mentions.** If the principal is engaged on another contract (Aecon FCS, LFC partnership, Bechtel pipeline, etc.), do not mention that firm or engagement in deliverables to any client. Deliverables to Client A must appear as if Client A is the principal's sole commitment.
- **No partner/prime relationships.** Do not mention LFC, Aecon, Navaide, or any other HARBOR partner or prime in deliverables unless they are the counterparty. "Internal pipeline" or "other clients" references are forbidden. This includes internal email domains, prior employer names, and concurrent consulting roles.
- **No personal names on contracting entities.** The masked LLC is the signatory. The principal's personal name does not appear on the SOW, NDA, or any contractual document unless explicitly required by the counterparty.
- **No Aecon conflict reference in deliverables.** The risk register/mitigation table in the briefing covers this internally. Do not reference the Aecon engagement, LFC partnership, or any conflict-mitigation structure in outbound documents.
- **No pipeline or in-progress data.** Do not reference other active deals, proposals, or engagements in any deliverable. Every deliverable stands alone as if it is the firm's only current work.

**Enforcement:** The adversarial review gate (Section above) explicitly checks for these OPSEC violations. Add "OPSEC — internal relationship leaks" to the judge criteria for every deliverable. Grep for known prohibited names (LFC, Aecon, client names from other engagements) across all files before delivery.

### Networked Practitioner Integration (Team Positioning)

When HARBOR's principal has a network of independent credentialled practitioners who augment the delivery team, position their credentials as "HARBOR team capabilities" without naming individuals. This is especially valuable for compliance CLINs that benefit from practitioner-level security experience.

**The pattern:** One principal with relationships to 2-3 independent practitioners with deep domain credentials (FSO, CACI/SAIC alumni, cleared engineers). The client sees HARBOR as a capable team. The practitioners are 1099'd per-deliverable. Their names never appear in client-facing materials.

**Skill-to-CLIN mapping (from practice):**

| Practitioner Skill | CLIN Application | Deliverable |
|-------------------|-----------------|-------------|
| FSO credentials (FCL, PCL, DCSA, SF-86) | Export Control Assessment | TCP, visitor control protocols |
| CACI/SAIC defense prime experience | NIST 800-171 Assessment | SSP, POA&M, evidence matrix |
| Training program development | UCNI/DOE Training | Course materials, 2-yr recert tracking |

**Language template for internal brief:**
> "Beyond the AI agent army, HARBOR draws on practitioner-level federal security expertise. Our network includes Facility Security Officers who have managed facility clearances and DCSA compliance, senior systems analysts from CACI, and solutions architects who have presented AI/ML defense solutions at SNA 2026 and AFCEA NOVA. This means CLINs 0003, 0005, and 0007 are delivered by people who have actually done this work — not studied it from a textbook."

**Language template for pitch deck (Slide 5):**
> "HARBOR's execution model combines [N] AI agents with a network of cleared practitioners who have served as Facility Security Officers, delivered systems at CACI and SAIC, and presented AI solutions at Surface Navy Association and AFCEA NOVA."

**Language template for SOW (§1 Contractor Description or CLIN descriptions):**
> "The Contractor's delivery team includes FSO-credentialed security practitioners with experience at CACI and SAIC."

**Key rules:**
- No names. Ever. The practitioner's name does not appear in any client-facing document.
- Position skills as "HARBOR team experience" — not as a named individual's skill set.
- Map each practitioner skill to a specific CLIN so the compliance depth is concrete, not vague.
- The internal brief (for the sponsor) can be more explicit about team structure than the pitch deck or SOW. The sponsor needs to know the truth; the CEO needs to see capability.

## 2. Templates Available

| # | Template | File | Use Case |
|---|----------|------|----------|
| 1 | MSA | `msa-template.html` | Governs ongoing client relationship |
| 2 | SOW | `sow-template.html` | One engagement, attaches to MSA |
| 3 | Mutual NDA | `mutual-nda-template.html` | Both parties share confidential info |
| 4 | One-Way NDA | `oneway-nda-template-harbor-receives.html` | Prospect shares, HARBOR receives only |
| 5 | Invoice | `invoice-template.html` | Billing against signed SOW |

## Mutual NDA Filling Workflow

### Step 1: Gather Counterparty Fields

Eight bracketed fields must be filled. Source them from session history, the Henry wiki, SAM.gov data, or the counterparty's website — do NOT ask the user for information you already have on disk.

| # | Field | Source Priority |
|---|-------|----------------|
| 1 | Counterparty legal name | SAM.gov > website > user |
| 2 | Entity type + state | SAM.gov > website > user |
| 3 | Principal business address | SAM.gov > website > user |
| 4 | Short name (used throughout doc) | Convention: acronym or single word |
| 5 | Business description (Section 7.b) | See pitfall below |
| 6 | Notice email (Section 12.e) | Session history > website > user |
| 7 | Signatory name + title | SAM.gov (officer records) > user |
| 8 | Effective date | User provides |

### Step 2: Write Section 7.b — CRITICAL PITFALL

**Keep the counterparty's business description HIGH-LEVEL and GENERAL.** Do NOT copy-paste their detailed service catalog from their website. The purpose is to establish that both parties have ongoing businesses, not to enumerate capabilities.

**Right** (~1 line, broad):
> "For LFC: consulting and advisory services, partnership development, and the joint pursuit of commercial and federal business opportunities, including related services to government agencies and commercial enterprises."

**Wrong** (detailed service catalog — user will reject):
> "For LFC: federal compliance and government contracting consulting services, including CMMC and NIST 800-171 compliance, federal enclave development, acquisition lifecycle and vendor management office (VMO) support, M365 and GCC High secure automation, secure technology and AI integration, audit readiness and corrective action, federal business unit standup..."

The HARBOR side (Section 7.a) uses the standard language from the template — do not modify it.

### Step 3: Fill and Format

Copy the template HTML. Replace every `[BRACKETED FIELD]` with the actual value. Remove the brackets. The effective date replaces `[EFFECTIVE DATE]`. All counterparty placeholders use the short name consistently.

### Step 4: The 2-Page, 2-Column Constraint (HARD REQUIREMENT)

**The mutual NDA must fit on exactly 2 Letter-size pages with 2-column layout.** No exceptions. Both constraints are non-negotiable. The full working CSS at multiple sizes is in `references/2-page-nda-compression-css.md`.

**CRITICAL: Proportional font scaling.** When you adjust the body font size, you MUST scale ALL other font sizes proportionally. Changing only the body while leaving section headers, labels, signatures, and footer at their old sizes creates a broken visual hierarchy. The user will flag this immediately. See the proportional scaling table in the reference CSS file.

**Tested font range:** 7.5pt through 11pt body all fit on 2 pages with appropriate line-height tuning. The approved final version uses **11pt Georgia body, 1.06 line-height**. Do NOT go below 9pt — 7.5pt was rejected as "ugly."

Key parameters:
- **11pt body, 1.06 line-height** (tighten to 1.04 or 1.02 to reclaim space if needed)
- **2-column** with `column-span: all` on title, parties, signatures, and footer
- **0.45" margins**, 16pt column gap
- Compact section spacing (4pt between sections, 1.5pt paragraph margins)
- Title/signatures span full width; body flows in 2 columns
- **No HARBOR branding header** — the `.header`/`.brand`/`.brand-sub` block is omitted. Document starts with the title.
- **No DRAFT watermark**

**Compression priority** (when pushing to fit): reduce line-height → reduce margins → reduce title size → drop body font size (last resort).

**Never cut legal text to fit.** Compression is pure CSS — every word of every section stays.

### Step 5: Verify Page Count and Cache-Bust

After generating PDF with Chromium headless, verify with `pdfinfo`:

```bash
chromium --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/path/to/output.pdf /path/to/input.html
pdfinfo /path/to/output.pdf | grep Pages
```

Must return `Pages: 2`. If 3, tighten CSS. If 1, you overshot.

**Cache-busting: browsers cache PDFs aggressively.** When the user has loaded a previous version, they'll see the stale cached copy even after regeneration. Always save with a versioned filename and deliver the versioned link:

```bash
cp output.pdf /data/nextcloud/data/amyn/files/briefings/<base>-v<N>.pdf
# Deliver: https://brief.h.porb.dev/<base>-v7.pdf
```

Increment the version number on every regeneration during the same session. The base (unversioned) file is for the repo copy only.

### Step 6: Save and Publish

Two destinations:

1. **Briefings (for review):** `/data/nextcloud/data/amyn/files/briefings/` — accessible at `https://brief.h.porb.dev/<filename>`. Run `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"` after writing.

2. **2026_books repo (permanent):** `HARBOR_portfolio/<counterparty_slug>/01-legal/` — create the directory if it doesn't exist. Copy both HTML and PDF.

### Step 7: Flag for User

After publishing, flag:
- Governing law / venue (Section 11 — always Texas/Fort Bend County by default; counterparty may want their state)
- Any template customizations beyond bracket fills (rare — most NDAs are pure fill)
- Font size: default to 11pt body from the reference CSS. If the user asks to go "slightly bigger," try 11pt first — it's the tested ceiling for 2 pages. Scale all elements proportionally (see reference CSS table). To go smaller, drop line-height before touching font size.

## Cross-References

- Canonical HARBOR facts (legal name, address, UEI, EIN): `operations/harbor-initiative-llc/00-canonical-facts.html`
- Template index and usage notes: `operations/harbor-initiative-llc/01-current/engagement-ready/index.html`
- Pineapple Protocol: all outbound documents require founder review before sending — templates are internal drafts until approved
- Counterparty research: use `session_search` for prior conversations, the Henry wiki (`operations/henry-hermes/wiki/`) for entity profiles, and SAM.gov for verified registration data
- CMMC L2 compliance toolkit: `cmmc-l2-compliance-toolkit` skill for deep compliance builds (SOPs, SSPs, POA&Ms, mock assessments)
- GovCon partnership assessment: `govcon-partnership-assessment` skill for side-by-side entity research (complementary — use before Phase 1 if evaluating multiple target partners)

## Reference Files

- `references/2-page-nda-compression-css.md` — Full copy-paste CSS block for 2-page NDA compression.
- `references/subcontract-research-pipeline.md` — Full DNS recon, OSINT, and tech stack mapping toolchain for Phase 1.
- `references/sow-10-clin-structure.md` — Concrete 10-CLIN FFP SOW structure with price ranges and acceptance criteria.
- `references/masked-llc-formation-pattern.md` — Wyoming LLC formation for HARBOR subsidiary contracting entities.
- `references/doe-compliance-pattern.md` — DOE Order 471.1B vendor requirements, LANL Exhibit G, UCNI protection.
- `references/cross-document-cohesion-pattern.md` — Cross-document consistency framework: evidence, vocabulary, CTA, and narrative arc alignment across multiple deliverables for a single engagement. Use when building pitch deck + brief + SOW as a set.
- `references/westerman-engagement-2026-07.md` — Worked example from the first full HARBOR sub-k engagement. Prices ($15K-$80K per CLIN), entity decisions (Delaware LLC), competitive positioning (NexusTek complement), errors caught by adversarial review (3 fact failures), and the 4-document deliverable package structure. Use for pattern-matching on future nuclear/DOE engagements.
