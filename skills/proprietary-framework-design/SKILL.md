---
name: proprietary-framework-design
description: "Design a named, proprietary consulting methodology framework — research industry canonical sources, synthesize a branded acrostic or mnemonic framework, define phases with objectives/activities/deliverables/outcomes, ground in authoritative references, and build it into the site as both a long-form methodology page and a landing-page teaser section. Use for consulting firms, GovCon companies, or any professional-services business that needs a named productized methodology."
tags:
  - govcon
  - consulting
  - methodology
  - framework
  - productization
  - brand
related_skills:
  - nextjs-site-builder
  - consulting-assessment-report
triggers:
  - "create a named framework"
  - "productize our methodology"
  - "build a proprietary methodology"
  - "design a gap-to-audit framework"
  - "name our consulting process"
  - "we need a signature methodology"
  - "turn our process into a named product"
---

# Proprietary Framework Design

Design a **named consulting methodology** — the firm's signature product that turns a generic process ("we do gap assessments") into an ownable, branded framework ("The LFC OORAH Framework"). This is the productization play for services firms.

## When to Use

- The user asks to "productize," "name," or "brand" their consulting methodology
- "Turn our process into a named/ownable framework"
- "Build a methodology page for the site"
- "We need something like [Big4 firm]'s [Named Framework]"
- The firm has domain expertise and methodology but no named product wrapping it

## When NOT to Use

- Writing a one-off project plan → `plan`
- Designing visual brand identity → `brand-kit-extraction`
- Building the actual site → `nextjs-site-builder` (this skill designs the FRAMEWORK; `nextjs-site-builder` builds the pages it lives on)

## Workflow

### Phase 1: Domain Research

Before naming anything, understand the canonical methodology in the domain. Mine the authoritative sources AND the commercial consulting competitors.

**Authoritative sources (vary by domain):**
- CMMC / NIST 800-171 compliance: NIST SP 800-171 Rev 2/3, NIST SP 800-171A (assessment objectives), 32 CFR Part 170 (CMMC final rule), DFARS 252.204-7019/7020/7021, CMMC Assessment Process (CAP) & Scoping Guide v2.13, SPRS scoring (−203 → +110)
- FedRAMP / RMF: NIST SP 800-53, NIST RMF 6-step lifecycle (Categorize → Select → Implement → Assess → Authorize → Monitor), FedRAMP authorization paths (Agency ATO / JAB), Readiness Assessment Report (RAR)
- General: ISO 27001 PDCA (Plan-Do-Check-Act), NIST CSF 2.0 six functions (Govern, Identify, Protect, Detect, Respond, Recover)

**Commercial scanning:**
- How CMMC consultants/RPOs name and structure their phased offerings (Assess → Remediate → Implement → Certify → Maintain is the common pattern)
- Big-4 / major advisory framework names (Deloitte, KPMG, Accenture, Coalfire, Schellman)
- Recurring phase-name vocabulary: Assess/Scan/Gap, Design/Architect/Plan, Build/Implement/Remediate, Validate/Test/Rehearse, Certify/Authorize/Operate, Monitor/Sustain/Hold/Maintain

**Local knowledge mining:** Check the user's existing repos for compliance toolkits, SOPs, and methodology documents — they tell you what phases and artifacts the firm actually uses, which makes the framework credible rather than invented.

### Phase 2: Name the Framework

**Constraints:**
- Should be organizational-identity-aligned (Marine firm → "OORAH"; fire-service → "IGNITE"; naval → "ANCHOR"; precision/engineering → "CALIBER")
- Acrostics work best — each letter maps to a phase word naturally, not forced
- Must be a real, pronounceable word or well-known phrase (not a tortured acronym)
- Check: does any major competitor already use this name? A quick web search avoids collisions.

**Acrostic design rule:** Every letter must map to a natural, domain-relevant phase word. If a letter forces an awkward word, start over. The acrostic is the product — it has to read cleanly on a slide.

**Naming patterns that work (examples):**
- OORAH: **O**rient · **O**rganize · **R**emediate · **A**ssess · **H**old — Marine battle cry, all CMMC-appropriate phase words
- For comparison, what doesn't work: forced words ("Quantify" for Q, "X-ray" for X), or phases that don't match what the firm actually does.

### Phase 3: Define the Phases

For each phase, define:

| Element | Description |
|---|---|
| **Name** | Single verb or noun — active, domain-appropriate |
| **Headline** | 2-4 word subtitle (e.g., "Scope & Baseline", "Plan & Architect") |
| **Objective** | 1-2 paragraphs explaining WHAT this phase accomplishes and WHY it matters in the domain context. Should reference the real failure mode it prevents (e.g., "Most assessments fail here — over-scoped enclaves and undocumented CUI flows"). |
| **Key Activities** | 3-5 concrete, verifiable actions. Use domain-specific language and reference real artifacts (SSP, POA&M, SPRS, CAP) — this is what signals credibility to practitioners. |
| **Deliverables** | 3-5 named outputs per phase. These should be the canonical industry artifacts (SSP, POA&M, evidence matrix, mock-assessment report, ConMon plan). Name them as a peer in the field would. |
| **Outcome** | A 1-sentence result statement — what's true when this phase is done. |

**Credibility test:** Would a C3PAO assessor or CO read the phase definitions and recognize the methodology as grounded in the real assessment process? If the phases feel generic or invented, go back to the authoritative sources and tighten.

### Phase 4: Ground in Authoritative Sources

A named framework without citations is marketing fluff. Build a grounding strip — a concise table or grid that maps the framework to the canonical documents and scoring methodologies it derives from. This is what separates a consulting product from a brochure.

Structure: `{ ref: "NIST SP 800-171 Rev 2/3", note: "110 controls, 14 families — the substance of Level 2" }`

This grounding should appear on the methodology page itself — it's how the firm demonstrates domain authority.

### Phase 5: Build — Shared Data Module + Site Integration

**Single source of truth:** Define the framework in a TypeScript module (e.g., `src/lib/oorah.ts`) that exports typed arrays. Both the landing-page teaser and the dedicated methodology page import from this module — one edit propagates everywhere.

**Dedicated methodology page (e.g., `/oorah`):**
- Hero with the framework name + full letter-strip (linked to anchors)
- "Why [NAME]" positioning counterpoint (what it prevents)
- Authoritative-source grounding strip
- Per-phase detail cards: letter badge, objective paragraph, key activities + deliverables columns, outcome callout
- Final CTA ("Request a [NAME] Assessment")
- Footer with trademark status (be precise: "(pending)" if not yet filed, "™" if filed, "®" if registered; never claim a status the firm doesn't hold)

**Landing-page teaser section:**
- 2-column intro: "OUR PROPRIETARY METHODOLOGY" / framework name headline / 1-sentence tagline
- Phase letter-tile strip (compact — letter badge + name + headline only, 5 across)
- Info bar with phase run-on ("Orient · Organize · Remediate · Assess · Hold.") + source grounding sentence
- CTA button → dedicated page ("EXPLORE THE FRAMEWORK →")

**Trademark precision rule:** Only use ™ or ® if the firm has actually filed or registered. The default phrasing for a planned/pending mark is: `[NAME] is a trademark of [Company] (pending).` This is precise and defensible. Never claim ™ status speculatively — it's a legal claim with consequences.

### Phase 6: Commit & Document

- Commit the shared data module, methodology page, and landing page update separately for clean history
- Update the repo README with the framework name, phase table, and source-grounding references
- The framework name IS the product — treat it as such in git messages

## Pitfalls

| Pitfall | Prevention |
|---|---|
| **Forced acrostic letters** | If a letter needs an awkward word, scrap the name. The acrostic IS the product — every letter must be natural. |
| **Generic phase language** | Use domain-specific artifacts (SSP, POA&M, SPRS, CAP) in activities/deliverables. A practitioner should nod, not squint. |
| **No grounding sources** | Include the authoritative-source strip. A framework without citations is marketing fluff. |
| **Claiming ™ prematurely** | Only assert ™/® with legal standing. Default: "trademark of [Company] (pending)." |
| **Inventing deliverables** | Every deliverable should be a real, canonical industry artifact the firm actually produces. |
| **Separate copies of framework data** | One shared TypeScript module. Duplicated constants in two pages will drift. |
| **Framework name collision** | Run a quick web search for the proposed name in the domain before committing to it. |
| **Forgetting the silent-partner constraint** | When the firm has contributors who cannot be publicly named, fold their capability into the firm's aggregate methodology rather than attributing to named individuals. The framework belongs to the firm, not the people. |

## Reference Files

- `references/oorah-framework-full-example.md` — The complete LFC OORAH framework as a worked example: all five phases with objectives, activities, deliverables, and outcomes; the authoritative-source grounding strip; and how it was mapped onto a Next.js site.
