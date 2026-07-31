# Grants.gov Pipeline Batch Workflow

End-to-end pattern for multi-opportunity grants.gov / simpler.grants.gov batches — the user drops 3-8 links plus attached zip documents and wants them all evaluated, ranked, and turned into an actionable briefing.

## Trigger Conditions

- User provides 3+ simpler.grants.gov or grants.gov opportunity links in one message
- Attached .zip files containing NOFO/BAA/PWS/SOW documents
- Request includes: "review all of these", "create a briefing", "figure out what needs to get done", "be thorough", "use agents"

## Anti-Patterns (DO NOT)

- **Do not dismiss opportunities by title or category label.** "RESTORE Act" sounds environmental (it is — state-govt-only, dead) but "CSBG" sounds social services (it is, but small businesses ARE eligible and it has a performance-management/data angle). "DoD EIE" sounds natural resources (it is, but cross-cutting priorities include "emerging technologies" and "data/information management"). Read every listing and every attached document before classifying. Kill only on: (a) hard eligibility bar the entity cannot meet, or (b) domain mismatch confirmed from actual text.
- **Do not incrementally patch an existing HTML briefing for major content additions.** When adding 3+ new opportunities and sections to an existing Douglas-format briefing, `patch(mode=replace)` with `replace_all` once wiped table CSS and produced duplicate `tr:nth-child` rules. For significant restructure: rewrite the full file with `write_file`. For small text edits: patch is fine.
- **Do not spin up deep-dive agents before the user confirms priorities.** Present the full table first with provisional assessments. Let the user make go/no-go calls. THEN dispatch agents on the confirmed list.

## Orchestrator Pattern

### Phase 1: Parallel Extraction (5-10 min)

1. `web_extract` all simpler.grants.gov links in ONE call (max 5 URLs per call)
2. Unzip all attached documents recursively: `unzip -o <file> -d <dir>` — grants.gov zips often contain nested zips (e.g., `DFOP0018157_Supporting_Documents.zip` inside `opportunity-DFOP0018157-attachments.zip`)
3. `pdftotext -layout` key PDFs for quick assessment (first 10-15 pages per doc)

### Phase 2: Provisional Triage Table

Build a table with ALL opportunities. Columns: #, Title, Agency, Due Date, Value, Can Prime?, Fit (⭐1-5), Provisional Verdict, Reason. Present to user with hard-kill reasons clearly stated. Wait for user confirmation before proceeding.

### Phase 3: Parallel Deep-Dive Agents

For each opportunity confirmed for pursuit, dispatch one sub-agent with:
- ALL extracted document paths as context
- Instruction to use `pdftotext -layout` for PDFs, `python3` + docx/openpyxl for Office files
- Structured output requirements (requirements checklist, evaluation criteria, format specs, submission mechanics, blockers, teaming strategy)
- Output to `~/govcon_research/leatherneck-pipeline/<slug>/01-requirements-analysis.md`
- Entity factsheet context (Leatherneck SDVOSB, UEI, CAGE, NAICS, key personnel)

Dispatch ONE additional agent for competitive landscape across all opportunities:
- USAspending API for incumbent discovery (award history, values, NAICS, set-aside)
- Web research for program office intel, PM backgrounds, likely competitors
- Teaming opportunities (universities, research firms, SMEs)

Max 3 agents concurrent (delegation.max_concurrent_children=3). Dispatch in batches if >3 opportunities.

### Phase 4: Master Briefing Assembly

Single HTML file at `/data/nextcloud/data/amyn/files/briefings/`:
1. **BLUF card** — dark background, 3-4 sentence summary
2. **Executive pipeline table** — all opportunities, 12+ columns, 1200px wrap, no horizontal scroll
3. **Deep-dive sections** — one per actionable opportunity (vehicle & terms, scope, evaluation criteria with weights, competitive landscape, teaming, submission requirements, blockers)
4. **Regulatory updates** — CMMC changes, new EOs, relevant policy shifts
5. **Risk matrix** — severity badges, mitigation per risk
6. **Action items** — grouped by week, with owners

Run Nextcloud files:scan, send link only in Discord.

## Douglas-Format Spec (Business Stakeholder Audience)

- **Language:** BD/contracts/compliance. "Winnability," "teaming strategy," "discriminator," "discriminator not a gate." NO "model architecture," "agent orchestration," "transformer," "fine-tuning."
- **Structure:** BLUF → exec table → deep-dives → regulatory → risk matrix → action items by week
- **Styling:** `.wrap { max-width: 1200px; }`, table font ~0.82rem, header font ~0.66rem mono uppercase, `white-space: nowrap` on headers, zebra striping via `tr:nth-child(even)`, severity badges (`.bg-green`, `.bg-amber`, `.bg-red`), tags (`.tag-pursue`, `.tag-team`, `.tag-monitor`, `.tag-dead`)
- **Content per opportunity:** Vehicle type + FAR/2CFR citations, ceiling + PoP, set-aside status, eligibility with for-profit restrictions, evaluation criteria with weights, 3 mandatory workstreams (if applicable), competitive landscape with named incumbents + award values, teaming strategy with named partners, submission requirements with format specs, blockers with P0/P1 priority

## Worked Example: July 2026 Batch

**Input:** 5 simpler.grants.gov links + 3 attached zip packages

**Opportunities:**
| # | Opportunity | Due | Verdict |
|---|-----------|-----|---------|
| 1 | DARPA DICE (HR001126S0010) | Aug 25 | TEAM — don't prime TA1+TA2 (SRI/MIT/STR field), pursue TA3 or subcontract |
| 2 | DFOP0018157 (State ACN/EXBS) | Aug 21 | PRIME — $5.9M, incumbents lack AI DNA, need export control SME partner |
| 3 | DoD EIE (HQ003423NFOEASD07) | Rolling to 2028 | DEFER — environmental domain, no deadline pressure |
| 4 | CSBG PM (HHS-2026-ACF-OCS-ET-0031) | ~Aug 3 (forecast) | MONITOR — still forecast, domain-blocked |
| 5 | RESTORE Act (GR-RCE-25-001) | Oct 31 | DEAD — state governments only |
| 6 | HHS VMO (7571TE26Q00092) | Jul 20 — 2 DAYS | RESPOND — 5-page capability statement, incumbent LARGE under new NAICS 541611 |
| 7 | Treasury FMBSS (2032H326N00011) | Jul 23 | OPTIONAL — generic financial consulting, low differentiation |
| 8 | VA GenISIS SIEM (36C10B26Q0650) | Jul 28 | TEAM — product resale, need SIEM vendor partner |

**Key findings from agent deep-dives:**
- DICE PM (Dr. Susmit Jha) came from SRI International — incumbent-adjacent
- DFOP competitive gap: EXBS incumbents (Culmen, CTP) are logistics/training firms, not AI companies
- HHS VMO incumbent (Summit/Allocore) is LARGE under new NAICS 541611 — excluded from SB set-aside
- CMMC Phase II suspended July 13 — self-assessments only, removes biggest DICE barrier
- DFOP zero-profit restriction for for-profits (cost recovery only)
- VA SIEM is product resale, not services — Leatherneck is consulting firm

**Deliverable:** `leatherneck-pipeline-douglas-2026-07-18.html` — 8-opportunity pipeline briefing with executive table, per-opportunity deep-dives, CMMC update, risk matrix, 26 action items across 3 weeks.

## Intelligence Notes from This Session

- **Grants.gov zips nest zips.** DFOP0018157 attachments contained `DFOP0018157_Supporting_Documents.zip` which itself contained the NOFO/QA/budget/SOW files. Always `find` after each unzip to check for further archives.
- **simpler.grants.gov web_extract works without auth** for listing pages (title, agency, description, eligibility, documents table, due date, award info). No login wall for public listings.
- **State Dept NOFO format quirk: 15pt Open Sans.** This is unusually large — 20 pages gives relatively little text space. Budget accordingly for DFOP-type proposals.
- **For-profit restriction on State Dept cooperative agreements:** No profit/fee allowed. Cost recovery only (direct + allocable indirect). Use 15% de minimis indirect rate if no NICRA.
- **DARPA BAA Step 1 gate:** Mandatory Technical Conformance — originality check. "Generic, boilerplate, or broadly aggregated content lacking mission-specific synthesis will be found nonconforming." No cut-and-paste proposals.
