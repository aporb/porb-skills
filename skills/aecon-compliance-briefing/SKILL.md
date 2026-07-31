---
name: aecon-compliance-briefing
description: "Build researched, citation-backed compliance briefings for Aecon FBU. Use when asked to research a regulatory/compliance question and produce a standalone HTML deliverable with bottom-line answer, regulatory framework, decision logic, risk matrix, and recommendations. Distinct from aecon-deliverable-patterns (which covers slide decks, process flows, RACI matrices) and aecon-brand-system (visual branding)."
category: govcon
triggers:
  - User asks for a compliance briefing, regulatory research, or FIPS/CMMC/DFARS/NIST interpretation for Aecon FBU
  - User asks "do we need to" or "are we required to" about a compliance/regulatory question
  - User asks for "compliance perspective" or "regulatory analysis" on a specific control or requirement
  - User asks for a researched answer with citations on a federal compliance topic
  - User asks about federal IT hardware procurement compliance (TAA, Section 889, hardware for CUI/CMMC environments)
  - User asks what hardware standard or device to procure for federal contract performance
  - User asks about CUI destruction, shredding, media sanitization, document destruction methods, or disposal of CUI paper/media
  - User receives an email or asks for a decision about secure document destruction equipment or services
---

# Aecon Compliance Briefing

Build researched, citation-backed compliance briefings for Aecon FBU stakeholders. This skill governs the STRUCTURE and RESEARCH METHODOLOGY for compliance opinion briefings — the aecon-brand-system governs VISUAL BRANDING (always load both).

## When to Use

When the task is: research a compliance/regulatory question → interpret it for Aecon FBU's specific environment (GCC High enclave, CMMC L2, nuclear sector) → produce a self-contained HTML deliverable with a clear bottom-line answer, regulatory citations, decision framework, risk assessment, and actionable recommendations.

NOT for: slide decks (use aecon-deliverable-patterns), process flows, RACI matrices, or general research without a compliance question.

## Prerequisites

Always load `aecon-brand-system` alongside this skill — it defines Aecon visual identity (colors, fonts, logo embedding, attribution rules). This skill defines research methodology and briefing structure.

Load relevant domain references from aecon-brand-system:
- `references/aecon-m365-environment.md` — tenant architecture, GCC High, IT contacts, CMMC deadline
- `references/fbu-org-structure.md` — verified reporting lines
- `references/cui-incident-reporting.md` — incident reporting and IRP gaps
- `references/fips-enclave-guidance.md` (in THIS skill) — FIPS protected-environment exception
- `references/ssp-fips-enclave-entry-template.md` (in THIS skill) — ready-to-paste SSP entry for FIPS exemption
- `references/cui-media-destruction-framework.md` (in THIS skill) — CUI paper/media destruction controls, NIST SP 800-88 Rev 2 specs, Section 889 analysis for non-IoT hardware, TAA for shredders, supply chain risk assessment for enclave hardware, DOE site considerations, outsourced destruction verification, media destruction log template

## Research Methodology

### Step 1: Identify the Controlling Authority
- What regulation/control is the question about? (NIST SP 800-171, DFARS 252.204-7012, CMMC, FIPS 140, NRC 10 CFR, TAA/FAR 52.225-5, Section 889/FAR 52.204-24/25/26, EO 14057, FAR 23.1)
- What is the exact control text?
- Who issues authoritative guidance on it? (DoD CIO, DIB SCC, NIST CSRC, NDISAC, C3PAO assessment guides)

### Step 2: Map the Multi-Regime Landscape
- Federal IT questions often involve 3-5 overlapping regimes (e.g., TAA + Section 889 + CMMC L2 + NIST 800-171 + DISA STIG + sustainability). Map ALL regimes before answering any one.
- For hardware procurement: TAA (origin of manufacture), Section 889 (supply chain), CMMC/NIST (security config), DoD SRG/IL (authentication), EO 14057/FAR 23 (sustainability).
- Each regime has different scope: TAA applies to the product's origin, CMMC applies to the configuration and management, Section 889 applies to the supply chain entity relationships. They are complementary, not redundant.
- Use delegate_task to research multiple regimes in parallel — fan out 3-4 subagents, then synthesize results.

### Step 3: Find the Interpretation, Not Just the Text
- The raw control text is rarely the answer — the guidance/interpretation is where the operational answer lives
- Search for: assessment guides, "Further Discussion" sections, implementation guidance, C3PAO assessment expectations
- Key sources: NDISAC DIB SCC CyberAssist, DoD CMMC Assessment Guide, NIST CSRC Implementation Guidance, 32 CFR 170
- Cross-reference with industry analysis (Totem, 112Cyber, Theodosian, Summit 7, BEMO) for practical interpretation

### Step 4: Map to Aecon FBU Context
- Does the GCC High enclave boundary matter? (often yes — it's the "protected environment")
- Is this about data at rest, in transit, or in use?
- Does the nuclear sector add requirements above and beyond the standard control?
- What's the CMMC L2 certification timeline impact? (November 2026)

### Step 5: Build the Decision Framework
- The deliverable must give a clear YES/NO answer where possible
- For conditional answers, build a decision tree or framework (2-4 questions that lead to a clear determination)
- Each branch must cite the specific regulatory basis

### Step 6: Identify Operational Risks
- Deadlines (certificate expiry, assessment windows)
- Hidden egress paths (telemetry, logging, vendor APIs)
- Assessment-day failure modes
- Compatibility risks (FIPS mode breaking applications)

### Step 7: Synthesize Multi-Regime Findings
- For questions spanning 3+ regimes (e.g., hardware procurement), don't present separate analyses per regime — synthesize into a unified recommendation that satisfies ALL regimes simultaneously
- Map which requirements are additive (TAA + Section 889 both constrain vendor choice) vs. independent (CMMC config requirements don't interact with TAA origin rules)
- Build a combined compliance checklist: a single procurement action that verifies all regimes at once
- The deliverable structure in this skill supports this — the Controlling Requirement section can list all regimes, and the Decision Framework branches on combined compliance status

## Briefing Structure

Every compliance briefing follows this structure:

1. **Header** — Aecon logo, document type label, title, date, control reference
2. **Bottom Line** — the answer in 1-2 sentences, pulled up front (executives read this first)
3. **Controlling Requirement** — exact control text, regulatory hierarchy, related controls
4. **The Interpretation** — the guidance/assessment language that answers the question; quote directly from authoritative sources
5. **When [X] IS Required** — clear scenarios, each with regulatory basis
6. **When [X] Is NOT Required** — equally clear; this is often the surprising finding
7. **Deadlines / Transition Risks** — if applicable (FIPS 140-2 expiry, assessment windows)
8. **Decision Framework** — 2-4 sequential questions per application/system; each answer leads to a clear determination
9. **Practical Recommendations** — numbered, actionable, owner-identified
10. **Risk Assessment** — table: risk, severity (High/Medium/Low), mitigation
11. **Sources** — every regulatory citation and industry source used
12. **Footer** — Amyn Porbanderwala, CICS, aporbanderwala@aecon.com, date, "Internal Reference"

## Visual Rules (from aecon-brand-system)

- Aecon web red (#C8102E), charcoal (#252525), body gray (#464646)
- Univers font family, 14px body, 1.429 line-height
- Logo: base64-embedded from `/data/nextcloud/data/amyn/files/briefings/aecon-assets/logo-aecon-red.png`
- Red accent < 15% of layout
- Bottom-line box: ivory background, red left border
- Decision framework: left-border boxes (red for required, silver for not required)
- Risk table: charcoal header, ivory alternating rows
- NO Hermes/agent mentions, NO editorial parentheticals, NO personal names in body (use role titles)
- Attribution: "Prepared by Amyn Porbanderwala, CICS"

## Quality Gate

Before delivery, run these checks:
```
- No rgba(255,255,255,*) — Safari rendering bug
- No forbidden colors: #2A2A2A, #FDE8EB, #B0B0B0, #2D8659
- No Hermes/agent/auto-generated mentions
- No personal names (Kerem, Sinem, Brian as contact) in body
- Amyn contact email present (aporbanderwala@aecon.com)
- All regulatory quotes directly verifiable against source documents
- Every risk has a concrete mitigation
- Decision framework covers all branches with no gaps
- NIST SP 800-171 revision: if cited in CMMC context, verify Rev 2 (not Rev 3) with note about pending Rev 3 adoption
- FAR clause attribution: 52.204-30 NOT grouped under Section 889 (it's FASCSA)
- TCO: includes realistic support costs ($600-1,200/3yr for STIG-hardened devices, not $250), STIG maintenance, secure disposal
- Windows 10 EOL: if hardware standard recommendation, includes current-state assessment of any existing Windows 10 devices (EOL was Oct 14, 2025)
- FIPS mode: if prescribed, includes operational risk note (app compatibility testing required)
- WDAC: if prescribed, specifies audit-mode-first deployment (not enforcement mode without testing)
- TAA compliance: verified per SKU at procurement time (not assumed from standard creation)
- Current-state language: do not use "is being evaluated" or "pending" unless confirmed. Verify with user before defaulting to future-tense language about existing systems.
```

## Vendor FedRAMP Authorization Reviews

A specific subclass of compliance briefing: reviewing a named vendor's FedRAMP authorization for use in Aecon's CMMC L2 enclave. Examples: InEight Document (July 2026), Autodesk AFG (July 2026). This pattern differs from general compliance interpretation because the primary research source is the vendor's claims + third-party (3PAO) assessment documents, not regulatory text.

### When to Use

- Task: "Review [Vendor]'s FedRAMP products" or "analyze [Vendor]'s FedRAMP posture"
- An email thread or Asana task provides the initial context
- The deliverable goes to Sinem Matay (IS Vendors & Contracts) or the enclave team

### Research Methodology for Vendor FedRAMP Reviews

**Step 1 — Extract from primary sources first.**
The email thread is the primary source — not the Marketplace. Extract everything from the vendor's email responses before doing external research. Email content is the most reliable (the vendor said it directly). Use screenshots as evidence.

**Step 2 — Attempt external verification in order of reliability:**
1. FedRAMP Marketplace (marketplace.fedramp.gov) — search the vendor name. NOTE: this is a SvelteKit SPA that blocks automated access (JS-rendered, anti-bot detection). A human at Aecon should manually verify and screenshot.
2. Vendor's trust center — often bot-blocked. Document all access failures as caveats.
3. Vendor's investor relations / press releases — may contain FedRAMP milestone announcements.
4. GSA FedRAMP GitHub (github.com/GSA/fedramp-data) — may have structured data.
5. web_search / Firecrawl — unreliable for niche FedRAMP queries, frequent 402/432 errors. Use as last resort.

**Step 3 — When external research is systematically blocked (common), pivot to the primary source.**
Document every blocked attempt in the caveats section. Build the briefing entirely from what the vendor confirmed via email. Flag what couldn't be independently verified. Use a table of "Confirmed vs. Not Confirmed" attributes.

### Briefing Structure for Vendor Reviews

Every vendor FedRAMP briefing follows this 10-section pattern (exemplar: aecon-autodesk-fedramp-review-2026-07-28.html):

1. **Header** — Eyebrow (Aecon FCS · IS Vendors & Contracts · FedRAMP Product Review), title, author, date, tag strip (Past/Present/Next)
2. **BLUF** — Bottom Line Up Front box: authorization status, material gaps, assessment (not a blocker vs. is a blocker), what Aecon must do
3. **What Started This** — Asana task context, vendor email thread, relevant meeting minutes (cite sources)
4. **What the Vendor Confirmed** — Full email transcript (not just summary). Use card block with direct quotes. Color-code vendor answers (e.g., clay text prefix `[ARR]` for Autodesk).
5. **What Is the Product** — Overview table comparing the vendor's commercial offering vs. government offering (cloud environment, FedRAMP status, deployment model, data residency, CUI handling, GovCloud usage, ITAR support)
6. **FedRAMP Analysis** — Table: for each attribute (authorized?, authorization level, deployment model, infrastructure, ITAR, CMMC evidence, CRM/SSP/POA&M availability, DoD references, NDA status), show status (✅, ⚠️, ❌), source, and details. Follow with "What is NOT confirmed" as a numbered gap list.
7. **Risk Analysis** — Three-layer framework: (a) Layer 1 — DFARS text ("equivalent to FedRAMP Moderate"), (b) Layer 2 — DoD 2023 Equivalency Memo conditions, (c) Layer 3 — Infrastructure (GovCloud vs. commercial region). Then a Risk Register table: risk, severity (High/Medium/Low), likelihood, difference from baseline, mitigation. Follow with deep analysis of the single most significant risk (e.g., AWS commercial region vs. GovCloud).
8. **Comparison with InEight Document** — Table contrasting the new vendor with InEight. Key insight: the irony column — which vendor is stronger on paper vs. in practice for Aecon's specific CUI/GCC High environment.
9. **What's Approved / Not Approved** — Two numbered lists: ✅ Approved/acceptable attributes, ❌ Not approved/gap areas. Answer the direct question: based on everything known, where do we stand?
10. **Recommendations** — Timeline: immediate actions (this week), short-term (next 2 weeks), medium-term (before CMMC assessment). Include a draft email to the vendor with follow-up questions numbered 1-6.
11. **Caveats** — What couldn't be independently verified, access failures, inferred assumptions.
12. **Footer** — Prepared by Amyn Porbanderwala, role, sources, revision number, date, confidentiality

### Design Pattern (Visual)

- Branding: Ivory/clay/slate (briefing-specific, NOT Aecon web red — these go to internal Aecon stakeholders not external clients). aecon-brand-system applies to client-facing deliverables; this pattern is for internal compliance analysis.
- Background: var(--ivory) #FAF9F5
- Accent: var(--clay) #D97757 (section numbers, step indicators)  
- Text: var(--slate) #141413
- Callout types: warn (yellow), good (green), info (blue), tldr (white + clay left border), critical (red)
- BLUF box: dark background (var(--slate) #141413 with ivory text)
- Comparison grids: side-by-side with 2-column grid layout
- Step cards: flex with numbered circle (clay background, white number)
- Email cards: light gray background (var(--g100))
- Tables: rounded borders, striped headers
- Caveats section: warn-style callout

### Draft Email Pattern

End each briefing with a draft email to the vendor. Format:
- Thank them for their response
- Numbered follow-up questions (6-8 questions covering: documentation requests, product scope confirmation, continuous monitoring, CR47/CR26 transition, Letter of Attestation)
- Each question references a specific line from their prior email (shows you read it)
- Sign as Amyn Porbanderwala, Controlled Information Compliance Specialist

### Key Pitfalls for Vendor Reviews

- **DO NOT claim the Marketplace was independently verified without a human check.** The SPA blocks automation. Always note this as a caveat and recommend Aecon do a manual search + screenshot.
- **DO NOT assume all products under a vendor's name are covered by the same FedRAMP authorization.** The authorization has a specific product boundary. Verify each product Aecon plans to use.
- **DO NOT conflate "FedRAMP Ready" with "FedRAMP Authorized" or "Equivalency."** They are three different tiers. InEight had Ready (expired) + Equivalency. AFG has full Authorization. Write them as distinct statuses.
- **DO NOT assume GovCloud is the only acceptable infrastructure.** FedRAMP PMO accepted AFG's AWS commercial region + tenant isolation as meeting Moderate baseline. But DoD C3PAOs and contracting officers often expect GovCloud — proactively document the justification.
- **SSP/POA&M access is the highest-value gap to flag.** If the vendor restricts SSP to Gov ID holders, Aecon cannot independently verify controls. This is a material limitation for C3PAO review. Mitigation: CRM + continuous monitoring attestation + Letter of Attestation.
- **CMMC tracking is NOT a FedRAMP requirement.** A vendor may have full FedRAMP authorization but zero CMMC documentation. Aecon must map 800-53 → 800-171 independently. Flag this clearly — it's not a vendor gap, it's an Aecon assumption to correct.
- **The comparison with InEight is the most useful framing for Aecon stakeholders.** It grounds the new vendor in an analysis they already understand. Namedrop the irony when there is one (e.g., equivalency vendor runs on GovCloud, full-auth vendor runs on commercial regions).

## Pitfalls

- **Citing the control, not the interpretation.** The raw control text ("Employ FIPS-validated cryptography") is vague. The answer is in the assessment guidance, the "Further Discussion" sections, and the C3PAO assessment expectations. Go there first.
- **Missing the protected-environment exception.** Many controls have scope limitations based on physical safeguards or protected boundaries. The GCC High enclave IS that boundary for Aecon. Always check whether the control applies differently inside vs. outside.
- **Over-applying requirements.** "Must use FIPS" doesn't mean "must enable FIPS mode on every application." The scope may be limited to specific data paths, specific data classifications, or specific boundary crossings.
- **Ignoring hidden egress.** Applications that "don't send CUI outside the enclave" may still do so through logging, telemetry, error reporting, or vendor API calls. Audit actual network traffic, not documented architecture.
- **Forgetting transition deadlines.** FIPS 140-2 expires September 2026. CMMC L2 certification is November 2026. Any recommendation that assumes current certificates will still be valid needs a migration path.
- **Assuming search tools will surface federal procurement content.** web_search and Firecrawl often return empty or 402 for niche FAR/acquisition queries. Always try direct web_extract from known authoritative URLs first: acquisition.gov (FAR), csrc.nist.gov (NIST pubs), public.cyber.mil (STIGs), esd.whs.mil (DoD issuances), federalregister.gov. Maintain a list of these fallback URLs — search is unreliable for federal regulatory research.
- **Researching one regime at a time for multi-regime questions.** Federal IT hardware questions touch TAA + Section 889 + CMMC + NIST + STIGs + sustainability simultaneously. Research ALL regimes in parallel (use delegate_task) and synthesize at the end. A single-regime answer misses critical constraints and may be wrong in practice.
- **CMMC references SP 800-171 Rev 2, not Rev 3.** The CMMC 2.0 rule (32 CFR 170) explicitly references NIST SP 800-171 Rev 2. Rev 3 was published May 2024 but DOD has NOT incorporated it into CMMC — adoption requires a separate future rulemaking. A C3PAO assessor will flag Rev 3 citations as a knowledge gap. Always note "Rev 2 (Rev 3 adoption pending separate rulemaking)" in CMMC-context regulatory references.
- **FAR 52.204-30 is NOT a Section 889 clause.** It's the Federal Acquisition Supply Chain Security Act (FASCSA) clause — covers orders to exclude/remove covered articles under FASCSA, not NDAA Section 889. The correct Section 889 clauses are 52.204-24 (representation), 52.204-25 (prohibition), and 52.204-26 (initial representation). Grouping -30 under Section 889 is a factual error that anyone familiar with the clauses will catch immediately.
- **TCO for federal hardware must include realistic support and lifecycle costs.** STIG-hardened devices have support costs 3-5× higher than standard enterprise devices ($600-1,200/3yr vs $250). Missing costs: STIG maintenance after each quarterly release, NIST SP 800-88 secure disposal ($50-100/device), deployment/provisioning for STIG-hardened images ($150-300), and security incident response allocation. A TCO that omits these understates real costs by 30-50%.
- **FIPS mode breaks applications — flag operational risk, don't prescribe as default.** Enabling Windows FIPS AlgorithmPolicy breaks all .NET and SCHANNEL applications that don't use FIPS-validated crypto. This includes many construction/project management tools (Procore desktop, Bluebeam Revu, older .NET apps). Always recommend pilot compatibility testing before FIPS enforcement, and document apps requiring exceptions with risk acceptance.
- **WDAC enforcement mode is operationally disruptive.** Windows Defender Application Control in enforcement mode blocks any unsigned binary. This breaks most third-party construction tools without extensive policy tuning. Always recommend audit-mode-first deployment, transitioning to enforcement only after full application compatibility validation.
- **Windows 10 EOL is already past (October 14, 2025).** Any briefing about federal laptop standards must include a current-state assessment of Windows 10 devices. Existing Windows 10 laptops are already noncompliant for CUI processing and will be flagged by CMMC assessors and DOD contracting officers immediately.
- **Pluton vs TPM 2.0 — not interchangeable for federal procurement.** Microsoft Pluton (on-chip security processor) raises supply chain risk management concerns for some federal buyers due to Microsoft's closed firmware and vendor lock-in. TPM 2.0 from third-party vendors (Infineon, Nuvoton) with public FIPS certificates is preferred for federal procurement. If briefing mentions Pluton, add a note about the SCRM implications and recommend TPM 2.0 for the primary recommendation.
- **OEM supply chain mobility — TAA compliance per SKU can change without notice.** Manufacturers shift assembly locations between orders. A previously TAA-compliant SKU can lose compliance status if the factory moves to China. Verify manufacturing location at time of each procurement, not just when the standard is created. Include this as a recurring compliance verification gate.
- **CUI media destruction is a distinct domain from data-at-rest encryption.** A briefing about protecting CUI in the enclave does NOT cover what happens to printed CUI. The controls are different (MP.L2-3.8.6 vs SC.L2-3.13.11), the standards are different (NIST SP 800-88 vs FIPS 140/CMVP), and the evidence artifacts are different (destruction logs/certificates vs SSP configuration entries). Always scope each briefing explicitly — "data protection" and "media disposal" are separate assessment areas. A CMMC assessor checks both independently.
- **Outsourced destruction requires the same SSP documentation as in-house destruction.** Using a third-party vendor (locked bins, off-site shredding) does not reduce the documentation burden. The SSP must still describe the destruction process, chain of custody, verification method, and provide Certificates of Destruction. The only difference is who performs the physical act — the compliance obligation is identical.
- **Multi-step destruction is a permitted alternative, not a compliance shortcut.** CUI Notice 2019-03 permits shredding to below single-step standards followed by contractor recycling/destruction — but the organization must verify and document that the process renders CUI "unreadable, indecipherable, and irrecoverable." A "we outsource it" statement without this verification is a CMMC finding.
