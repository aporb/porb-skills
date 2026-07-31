---
name: sources-sought-response
description: Draft, edit, and review federal Sources Sought and capability statement responses. Covers structure, domain-knowledge injection, overstatement detection, and honest sub-only posture for new/small businesses.
---

# Sources Sought Response — Drafting &amp; Editing

## Trigger

User asks to draft, fix, edit, review, or tighten a Sources Sought notice response, capability statement, or RFI response for a federal procurement — especially for a new or small business with limited past performance. Also triggered when the response strategy involves building on the agency's existing M365/cloud infrastructure rather than reselling a SaaS product. See `references/m365-productization-response-pattern.md` for the full M365-native response pattern including GCC High technical notes, data source strategy, and cost comparison.

## Required References

Before editing any capability statement, load these authoritative sources:

1. **Verified background** — `~/sources-sought-responses/raw/amyn-background-verified.md` (or equivalent). This is the single source of truth for what claims can be substantiated. Every capability claim in the response must trace back to this file.
2. **Domain research** — Agency/requirement-specific research document (e.g., `~/sources-sought-responses/raw/va-siem-domain-research.md`). Contains agency org structure, incumbent landscape, regulatory framework, pain points, and source citations.
3. **Current draft** — The file to edit.
4. **Earlier drafts** — Check for claims that were already removed from earlier versions but may have regressed.

## Workflow

### Phase 0: Web Presence Research (Raw Material Compilation)

**When to run:** Before any drafting begins. When the entity responding has a personal/company web presence (multiple domains, products, published IP) and the verified background file either doesn't exist or is stale. This phase produces `~/sources-sought-responses/raw/<entity>-web-presence-inventory.md` — the exhaustive, quantified source document that every capability claim traces back to.

**The pattern:** Research ALL web properties in parallel, cross-reference with local filesystem (resumes, portfolio docs, CLAUDE.md, persona docs), and compile a comprehensive inventory with quantified metrics, capability-to-requirement mapping, and PWS differentiation matrix.

**Tool selection heuristics:**
| Page type | Tool | Reason |
|---|---|---|
| Static HTML (porbanderwala.com, harborgovcon.com) | `web_extract` | Fast, cheap, returns clean markdown |
| JS-rendered SPAs (Next.js pages returning thin/empty content) | `browser_navigate` then `browser_vision` or `browser_snapshot(full=true)` | web_extract gets only footer; browser executes JS |
| Cloud/self-hosted domains blocked as "private/internal network address" | `browser_navigate` | web_extract blocks `*.cloud` domains; browser bypasses |
| Amazon product pages | `browser_navigate` then `browser_console(expression=...)` or `browser_vision` | Amazon blocks automated extraction; browser extracts ratings, rankings, reviews via JS |
| Local PDF/HTML resumes, portfolio docs, CLAUDE.md | `read_file` (HTML) or `firecrawl_parse` (PDF) | Local filesystem is richer than web sources for personal data |
| Firecrawl tools (scrape/parse) in general | Fall back to browser tools if firecrawl returns credit-exhaustion errors | Browser tools are slower but work when API credits depleted |

**Parallel extraction rule:** All web properties are independent. Batch up to 5 in `web_extract`. JS-rendered pages flagged from batch results should be re-queued via browser tools in the next turn. Never serialize independent extractions.

**Cross-reference rule:** Every capability claim must trace to a specific web property, a resume line, or a published artifact. If a claim doesn't appear in the inventory, it doesn't go in the response. This inventory is the single source of truth for the drafting phase.

**Inventory output structure:**
1. Executive Summary — top N differentiators for the target PWS
2. Per-property sections — URL, purpose, key facts, quantified metrics, federal/GovCon relevance
3. Cross-referenced resume/profile data (if available locally)
4. Quantified Metrics Summary — a table of every number with its source property
5. PWS Differentiation Matrix — every PWS capability area mapped to specific evidence from the inventory

For a full worked example covering 14 web properties, see `~/sources-sought-responses/raw/amyn-web-presence-inventory.md` (July 2026, ~29KB) and the detailed methodology in `references/web-presence-research-phase.md`.

### 1. Load All References (parallel reads)
Read the verified background, domain research, current draft, and any earlier drafts simultaneously. If a web presence inventory exists at `~/sources-sought-responses/raw/<entity>-web-presence-inventory.md`, load it FIRST — it is the most current and comprehensive source.

### 2. Search for Known Bad Patterns
Run targeted searches across all drafts for these red-flag patterns:

| Pattern | Example | Fix |
|---|---|---|
| Person-equivalent ratios | "15-20 person equivalent", "throughput of N people" | Remove — unverifiable |
| Fabricated statistics | "80% of VMO work is data gathering" with no source | Remove or cite a real source (Gartner, McKinsey) |
| Unverifiable repo counts | "103 GitHub repositories of operational code" when public count differs | Remove count entirely; name 2-3 specific deployed applications instead |
| Fake phone/email | Made-up contact info | Replace with `[INSERT ... BEFORE SUBMISSION]` placeholder |
| Overstated platform depth | "Hands-on with Databricks, Palantir, Qlik" when only reference knowledge | Downgrade to verified platforms only (e.g., Advana, M365 GCC High) |
| Unverifiable classification claims | "IL4-IL6 experience" with no system name, dates, or purpose | Remove unless specific project/date/system can be cited |
| Attribution errors | "Built Hermes Agent" when user is operator, not creator | Correct attribution |
| Revenue overstatements | "$140K deals closed" when $0 actual revenue | State accurately or remove |
| Portfolio inflation | "16+ companies" when active count is ~7-8 | Use verified count |
| Full-time dedication claims | "Full-time on HARBOR" when employed elsewhere | State capacity accurately |
| Title inflation | "Fractional CAIO" when title never used in verified sources | Use verified titles only (e.g., "Founder, HARBOR Initiative LLC") |
| Aspirational capabilities | "Zero Trust Architecture deployment" with no deployment history | Remove or reframe as awareness/knowledge |
| Internal jargon in public docs | "MCP agent fleet", "Agentic OS" | Use plain language or remove |
| Product count inflation | "14 shipped production applications" when 5-7 are true production apps | Use verified count. Name 3-4 with URLs — specificity beats aggregation. |
| Ambiguous employment / teaming | "No subcontracting" when personnel list includes individuals with separate SAM-registered LLCs | State W-2 employment explicitly or disclose teaming arrangement per SS notice. |

### 3. Map Capabilities to PWS Roles and Deliverables
**Before writing a single word of the response**, extract from the PWS:
- Every specialist role by name (e.g., "Program Manager," "Acquisition Specialist," "License Specialist")
- Every deliverable by name, description, and frequency (e.g., "BPA/ELA Tracking Report — Monthly")
- Every task area and its sub-requirements

For each role and deliverable, classify:
- **Covered** — a named person or demonstrated capability addresses it
- **Gap** — no one on the current team fills it (must be acknowledged with mitigation plan)
- **Subcontract** — will be filled via strategic hire or teaming partner

This mapping becomes the backbone of the response's Capabilities section. A response that maps to 100% of PWS elements (even with honest gaps) scores far higher than one that only maps to 30% and pushes AI on everything.

**The response's content proportions must match the PWS's requirement proportions.** If the PWS defines 8 specialist roles and 13 deliverables, and AI automation is mentioned once in Additional Requirements, then AI should be ~10% of the response — not 80%. Lead with the management consulting functions the PWS actually prioritizes.

### 4. Inject Domain Knowledge
Using the domain research, enrich thin sections with agency-specific details:

- **Understanding of Requirement**: Add agency org structure, system scale (e.g., "985K veteran genomes, 6.2M computing hours"), regulatory overlay (e.g., "VA Handbook 6500"), incumbent info
- **PD Sufficiency**: Reference relevant OIG/GAO findings that demonstrate domain awareness (e.g., July 2025 OIG Section 508 finding)
- **ROM justification**: Cite prior comparable procurements from domain research

### 4. Tighten Capability Matrix
Every row must satisfy three tests:
1. **Traceable**: Can the claim be mapped to a specific line in the verified background?
2. **Relevant**: Does it connect to the requirement (not just "we're good at X")?
3. **Honest**: Is the depth accurately described (hands-on vs. reference knowledge vs. awareness)?

### 5. Verify Sub-Only Posture
For responses where the entity is NOT the prime/platform provider:
- Transparency section must explicitly disclaim what the entity does NOT do
- Capabilities must be framed as subcomponents, not prime deliverables
- Participation paths must list subcontractor, teaming partner, and SDVOSB credit options
- SDVOSB certification gap (if self-attested, not SBA VetCert) must be flagged

### 6. Final Verification
- Read the complete edited file
- Confirm no bad patterns remain
- Confirm domain knowledge is specific and sourced
- Confirm phone/email fields use honest placeholders, not fake data
- Confirm page count is within limits
- **Cross-check ALL cover page dates against the actual SS notice:** Notice date, response date, and issuance date on the cover must match what the SS notice says. A 5-day date error on the cover page signals carelessness before the KO reads a single word.
- **Run HARBOR regex sweep:** `\\bHARBOR\\b` must be 0. `K4CVRY71WQZ8` must be 0.
- **Run Aecon regex sweep:** `\\bAecon\\b` must be 0. Any occurrence of "Aecon Group," "Aecon Energy," "Aecon U.S.," or "Aecon AFSI" must be stripped and replaced with generic descriptors like "a defense-sector compliance role" or "federal nuclear sector."
- **Run exposed-contact regex sweep:** `\b\d{3}[\)-\.\s]\d{3}[\)-\.\s]\d{4}\b` must be 0 in the deliverable. `@porbanderwala\.com`, `@leatherneckfederal\.com`, or any personal domain in a mailto or email field must be replaced with `[INSERT ... BEFORE SUBMISSION]`.
- **If a team credential gap analysis exists** at `~/sources-sought-responses/plans/<agency>-team-credential-gap-analysis.md`, load it and verify: (a) no declared gaps are already filled by team members, (b) no credentials are stated as aspirational when already held, (c) all team members who fill PWS roles appear in Key Personnel.

## Deliverable Format: HTML, Not Markdown

The final deliverable for a Sources Sought response is a **self-contained HTML file** that prints correctly as a PDF. The Markdown draft is an internal working file — never the deliverable.

- **Print CSS required:** `@page { size: letter; margin: 1in; }`. Body max-width 6.5in. Times New Roman 12pt. Page breaks before major sections. Cover page with `page-break-after: always`.
- **Table column widths:** For key-value tables (corporate info, POC details), use `td:first-child { width: 30-32%; }` in CSS. For multi-column data tables (deliverables), use `width: auto; max-width: 100%` so tables size to content rather than stretching full-page.
- **Tables vs. Sections:** Tables are for DATA — key-value pairs, deliverables lists with short entries, compliance checklists. Do NOT use tables for capability descriptions where one column would be a 5-word label and the other 200 words of prose. That pattern creates cramped, unscannable layouts that waste vertical space. Replace with structured h3 sections: heading → context paragraph → bulleted list of specific capabilities. See `references/print-layout-principles.md` for when and how to restructure.
- **Format requirements from the SS notice:** Always extract and apply specific formatting (margins, font, spacing, page limits, cover page elements) from the actual notice PDF. Never assume.
- **Style:** Clean, professional, government-submission aesthetic. White background for printing. Subtle table styling with dark headers. No flashy colors.
- **When printed (Ctrl+P → Save as PDF):** Must produce a document indistinguishable from a Word-generated PDF — proper page breaks, cover page, 1" margins, correct font.
- **Place in Nextcloud:** Save to `/data/nextcloud/data/amyn/files/briefings/sources-sought-drafts/<notice-id>-final.html`. Run `docker exec` scan after writing. Also render and save a PDF copy at `<notice-id>-final.pdf` for page-count verification.

### DOCX Conversion (Required Deliverable)

After verifying PDF page count, convert the HTML response to a .docx file for the user to review and share:

```bash
pandoc /data/nextcloud/data/amyn/files/briefings/sources-sought-drafts/<notice-id>-final.html \
  -f html -t docx \
  -o /data/nextcloud/data/amyn/files/briefings/sources-sought-drafts/<notice-id>-final.docx
```

Run `docker exec` scan after writing. Deliver both the HTML link and the DOCX link to the user. The DOCX is the preferred format for business stakeholder review (Douglas Henderson); the HTML is the print-to-PDF source.

If pandoc is not installed: `sudo apt install pandoc`. It converts HTML → DOCX in seconds with no external dependencies.

### PDF Page Count Verification

After writing the HTML, render to PDF and verify the page count:

```bash
google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="/tmp/<notice-id>.pdf" \
  --no-pdf-header-footer \
  "file:///data/nextcloud/data/amyn/files/briefings/sources-sought-drafts/<notice-id>-final.html"
pdfinfo /tmp/<notice-id>.pdf | grep -i pages
```

Inspect what lands on each page:
```bash
for page in $(seq 1 $(pdfinfo /tmp/file.pdf | grep Pages | awk '{print $2}')); do
  echo "=== PAGE $page ===" && pdftotext -f $page -l $page /tmp/file.pdf - 2>/dev/null | head -5
done
```

If over the page limit, tighten iteratively (approx word counts at TNR 12pt single-spaced, 1in margins):
| Body Words | ~Pages | | Body Words | ~Pages |
|---|---|---|---|---|
| 1,500 | ~3 | | 2,300 | ~4.5 |
| 2,000 | ~4 | | 2,500 | ~5 |

Proven tightening sequence: (1) `line-height: 1.15` → `1.12`; (2) body `11pt` → `10.5pt`; (3) bio text `10.5pt` → `10pt`; (4) reduce h2/h3/p margins 20-30%; (5) shrink cover page; (6) condense closing from bulleted list to prose paragraph + single-line POC; (7) remove explicit `page-break-before` divs; (8) eliminate duplicate bios (Section 4 repeating Section 2). See `references/print-layout-principles.md` for full troubleshooting.

## HARBOR / Entity Name Stripping

When producing responses for external submission (going to a Contracting Officer, shared with Leatherneck, or submitted through another entity):

- **Strip ALL references to HARBOR Initiative LLC** — name, UEI (K4CVRY71WQZ8), SAM status, formation date, portfolio companies, revenue figures, product names.
- **Strip ALL references to Aecon** (Aecon Group Inc., Aecon U.S., Aecon Energy Group) — replace with generic descriptors like "federal nuclear sector" or "energy-sector infrastructure." Never mention Aecon by name.
- **Amyn Porbanderwala appears as an individual** — not as HARBOR's founder. Use "Technical Lead" or a Leatherneck role title. His background and capabilities are attributed to him personally.
- **No HARBOR entity in corporate/teaming tables.** Amyn's row shows his personal credentials, not his LLC.
- **No HARBOR product names in deployed AI lists.** Replace "HARBOR platform" with generic equivalents like "federal analytics platform."
- **Redact ALL personal contact info** — phone numbers, email addresses, personal domains. Use `[INSERT ... BEFORE SUBMISSION]` placeholders for Douglas AND Amyn. Never expose real contact info in the deliverable HTML.

## Pitfalls

- **Do NOT expose real phone numbers or email addresses in deliverable HTML.** Use `[INSERT ... BEFORE SUBMISSION]` placeholders for ALL personal contact info — Douglas AND Amyn. The deliverable is shared as a file; the recipient fills in their own contact details before sending.
- **Do NOT deliver Markdown as the final product.** Markdown drafts are internal working files. The Contracting Officer receives a print-ready HTML that converts to PDF with proper formatting. Always produce the `-final.html` version.
- **Do NOT pad with marketing fluff.** Sources Sought responses are market research tools for the CO. Concise honesty beats verbose puffery.
- **Do NOT claim platform expertise you can't prove.** "Covered in my open-source handbook" is NOT the same as "deployed on this platform for a federal client."
- **Do NOT invent past performance.** "We supported X agency" when the work was through a previous employer — attribute correctly.
- **Do NOT bury the SDVOSB cert gap.** If SBA VetCert is pending, state it prominently. Hiding it in fine print is worse than not responding.
- **Do NOT claim team gaps that don't exist.** Cross-reference every team member's bio against the PWS before declaring a gap. In one response, we claimed "must subcontract for a FAC-C/DAWIA Acquisition Specialist" when a team member had DAWIA Level III Contracting and 15 years as USMC Director of Contracting. Another team member with 15+ years of commercial management was invisible in the draft. Always inventory EVERY team member's credentials before writing gap notes.
- **DAWIA certification series MUST be accurate.** DAWIA certifications are functional-area-specific. "DAWIA III PM" (Program Management) is NOT the same as "DAWIA Level III (1102 Contracting Officer)." If a team member's credential is 1102 Contracting, state it exactly. Mislabeling a DAWIA series makes the team look like they inflate credentials or don't understand the DAWIA system. Cross-reference every certification claim against the verified background file.
- **Never fabricate quotes from government reports.** If you cite GAO, NIST, or any government publication, the quoted text must appear verbatim in the source. A CO will check. One fabricated quote destroys the entire response's credibility. If you cannot verify exact wording, paraphrase without quotation marks or remove the reference entirely. NIST SP 1326 alone is sufficient regulatory driver — you don't need a GAO quote to make the case.
- **Don't claim data sources that aren't publicly accessible.** The DEA Registrant Database is a restricted system under 21 CFR Part 1301 — NOT a public API. Saying "DEA Registrant Database (free)" is false. Verify every listed data source. If you need to reference DEA validation, say "DEA registration validation (manual lookup or commercial provider)."
- **Be honest about ATO requirements.** Custom applications on FedRAMP-authorized platforms still require application-level EPLC/SDLC review. Never claim "no new ATO required." Say: "The platform authorization reduces the ATO burden; it does not eliminate it, and we would not claim otherwise." A CO who knows their agency's compliance process will catch the overstatement.
- **Amyn Porbanderwala's credential: use CISA, not Security+.** The verified background file explicitly states Security+ "undersells." CISA (Certified Information Systems Auditor, ISACA) is more rigorous and directly relevant to due diligence and compliance auditing. Use "Amyn Porbanderwala, CISA" — not "Security+."
- **Cover page design: no repeated titles.** The requirement name is the h1. "Sources Sought Response" is the subtitle. Notice ID goes in monospace below. Agency line follows. Corporate details in a compact table. Georgia serif for headings, TNR for body. The cover should look like a human-designed document, not a header repeated twice with slightly different wording.
- **Do NOT present already-held credentials as aspirational.** The single most common self-inflicted credibility wound in these responses: the PM already holds PMP + DAWIA III, but the draft says "commits to obtaining PMP by contract start date." The acquisition specialist already has DAWIA III Contracting, but the draft declares it a gap and proposes subcontracting. When a credential exists, state it as current — not as something the team will go get. "Will obtain" signals the credential doesn't exist. "Currently holds" signals readiness. Before writing any certification claim, check the verified background or team gap analysis to confirm whether the person already has it.
- **Placeholders are better than fakes.** `[INSERT PHONE BEFORE SUBMISSION]` is honest. `555-0199` is not.
- **Do NOT cite FAR 15.305 in a Sources Sought response.** FAR 15.305 is a proposal evaluation rule under FAR Part 15 (Contracting by Negotiation). A Sources Sought is market research under FAR Part 10. Citing proposal evaluation rules in a market research response signals procurement process misunderstanding. Frame capability evidence as information for the KO's market research consideration — not as past performance mitigation under a proposal evaluation rule.
- **Do NOT build your response around the one novel thing you can do.** Your AI agent infrastructure may be real and differentiated. But if the PWS has 8 specialist roles, 13 deliverables, and 5 task areas — and AI is one sentence in Additional Requirements — then AI should be ~10% of the response, not 80%. The KO evaluates how well you cover the PWS, not how impressive your AI stack is. Lead with management consulting capability. AI is your *how* — not your *what*.
- **Do NOT frame a management consulting PWS as a software product build.** If the PWS defines a management consulting engagement (NAICS 541611, PSC R408) with specific specialist roles, recurring deliverables, and operational governance — do not position the response around "we'll build you a product." This is a category error the KO will catch immediately. The PWS asks for a team to operate a VMO. Building a custom SAM platform on M365 is a software development project the PWS didn't solicit. Three specific failure modes: (a) the product approach ignores the existing VMO application the PWS requires you to maintain — parallel-operations risk; (b) custom-built tools create vendor lock-in for the government when the PWS requires a 30-day transition-out plan with successor training; (c) custom development triggers EPLC/SDLC compliance requirements the response never acknowledges. Frame the product as an analytics/reporting augmentation layer on top of existing tools, not as a ground-up platform replacement.
- **Do NOT inflate product/deployment counts.** "14 shipped production applications" when verified inventory shows 5-7 true production apps (with the rest being one-off websites, community portals, or internal tools) is inflated. An evaluator who asks "which 14?" will expose the gap. Use the verified count from the background file or web presence inventory. If the count is borderline, name 3-4 with URLs — specificity beats aggregation.
- **Do NOT default to SaaS resale when the Sources Sought asks for alternatives to a commercial SaaS subscription.** If the agency already licenses M365 (GCC/GCC High), Salesforce, or ServiceNow, evaluate whether building on their existing platform beats reselling a competing SaaS. The HARBOR approach: audit existing licenses → identify under-leveraged platform capabilities (Power Platform, custom apps, automation) → propose building a tailored solution on the platform they already own. This eliminates the SaaS subscription cost, inherits existing FedRAMP authorization, and integrates into existing workflows. The SS response should reframe the requirement from "which SaaS should we buy" to "how can we build this on what we already have." For the full pattern, technical notes (Azure OpenAI GCC High workaround, sanctions.io integration, AI Builder availability), and a worked example (HHS ASPR due diligence, July 2026), see `references/m365-productization-response-pattern.md`. This decision should be informed by incumbent product research — see `references/incumbent-product-research.md` for the competitive intelligence framework that surfaces the incumbent's data moats, pricing model, and weaknesses.

- **Do NOT leave employment relationships ambiguous.** If the response claims \"no subcontracting\" or \"all work by prime personnel\" but lists individuals who publicly operate separate LLCs registered in SAM.gov, flag it in review as P0. A competitor can check SAM.gov and file a size protest. If the individual is truly a W-2 employee, state it explicitly. If a 1099 contractor or separate-entity subcontractor, disclose the teaming arrangement properly per the SS notice.
- **Category error: answering the wrong question is a P0 fix.** If the SSN asks about SaaS platforms and you propose custom development, you are answering a question nobody asked. The CO cannot compare your response to other respondents offering actual SaaS products. If you must submit anyway (Option A+C strategy): open Section 1 with \"What We Cannot Provide,\" state clearly what you don't sell, share relevant domain research, propose your alternative, and close with honest boundaries. The Program Lead in the July 2026 HHS ASPR session specifically noted this honesty as \"operationally useful.\"
- **Technical data source verification is mandatory before submission.** The technical evaluator in the July 2026 HHS ASPR session verified claims against actual API docs and found multiple false assertions: FDA enforcement data (Warning Letters, Form 483s) are not REST APIs; OFAC SDN, HHS OIG LEIE, and BIS Entity List are downloadable flat files, not APIs; DEA registrant data has no public API. Every data source claim must be verified against the source's documentation before submission. An unverified claim about data availability is a P0 accuracy finding.

## Reference Files

- `references/incumbent-product-research.md` — **Pre-draft competitive intelligence on the incumbent commercial product.** 7-dimension research framework for understanding the product the agency currently uses before drafting the response. Use when the Sources Sought names a specific incumbent product (not just a contractor). Covers product capabilities, integration ecosystem, data sources, pricing model, competitor landscape, federal agency usage, weaknesses/API flexibility, and the build-vs-buy strategic positioning framework. Worked example: HHS ASPR Dow Jones (July 2026).
- `references/overstatement-checklist.md` — Detailed checklist of claims to verify before submission
- `references/pws-mapping-template.md` — Template for mapping response capabilities to every PWS specialist role, deliverable, and task area
- `references/web-presence-research-phase.md` — Pre-draft research methodology: extracting evidence from web properties before drafting
- `references/print-layout-principles.md` — When tables fail, when to use structured sections, PDF page count verification, and tightening sequence for over-limit responses
- `references/product-augmentation-pattern.md` — Valid M365-native augmentation product approach for management consulting PWS (when and how to pitch a product without committing the ground-up replacement category error)
- `references/m365-productization-response-pattern.md` — Full M365-native productization response pattern: core argument structure, GCC High technical notes (Azure OpenAI workaround, AI Builder availability table, Power Automate HTTP connector), data source strategy (free government + paid API layers), cost comparison, competitor weakness mapping, and regulatory timing advantage pattern. For Sources Sought notices where the agency asks for SaaS alternatives but already licenses M365.
- `references/adversarial-review-pattern.md` — Three-persona parallel review panel (KO compliance + technical evaluator + program lead) for pre-submission quality gate