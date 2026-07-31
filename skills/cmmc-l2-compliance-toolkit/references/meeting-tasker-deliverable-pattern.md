# Meeting Tasker Deliverable Pattern

## Context

The user walks out of a meeting, dumps 10-15 screenshots (Teams invite, Copilot/M365 summary,
task list, presentation slides) into Discord, and says "Taskers [client]." They expect every
image visually inspected, action items extracted, deliverables built for each action item,
judge-gated, and published as HTML.

This file documents the workflow using the July 2026 Aecon example.

## The July 2026 Example

**Trigger:** 15 images dumped into Discord with "Taskers Aecon" as the only instruction.
Images included:
1. Teams meeting invite (USG BU Operational Priorities Meeting Prep, July 7 2026, Enzo Zoratto organizer)
2. M365 Copilot summary (meeting was not transcribed; Copilot inferred topics from action items)
3. Follow-up task list screenshot (your action items + other meeting actions)
4. Extended follow-up screenshot ("My Read of Why You Were Invited" — Copilot's analysis)
5-8. USG BU Operational Priorities document pages (Topic/Description/Expected Outcome table)
   - Operations (USG Opportunity Pipeline)
   - Compliance (Section 847 FCI rule)
   - Governance (FOCI-Mitigated BU structure, AFSI board)
   - Federal Compliance Function Reporting Line
   - CMMC Implementation
   - USG BU Structure
9-10. FOCI Mitigated BU Addendum slides
11. Compliance Gate slide (FOCI × CMMC × CAS Go/No-Go)
12. Aecon Federal Business Unit Governance deck title slide
13. "One source of truth, three audiences" (ExCo/SteerCo/Working Level tier model)
14. Forums & decision rights slide (ExCo → SteerCo → Working Level cascade)
15. The document set slide (6 documents mapped to 3 tiers)
16. Build phases & timeline (Phase 0 Stand-up through Phase 3 Enterprise Rollout)
17. Planner task list (7 follow-up tasks with assignees)

**Two action items assigned to the user:**
1. "Line out challenges and DOR for CMMC setup, implementation, and daily execution for Aecon and third parties"
2. "Develop timeline to CMMC audit from JV formation"

## Workflow

### Step 1: Batch Vision Analysis

Dispatch `vision_analyze` on ALL images simultaneously in one assistant turn. Some may fail
with 429 rate limits on the vision model — retry those individually after the batch completes.

Extraction targets per image:
- **Meeting invites:** title, date, organizer, attendees, response status, room
- **Copilot summaries:** key topics discussed, follow-up items with assignments
- **Task lists:** exact task wording, assignee names, due dates, status
- **Presentation slides:** topic / description / expected outcome tables (capture every cell)
- **Strategic frameworks:** visual models like "Compliance Gate" (FOCI × CMMC × CAS)
- **Org charts:** entity hierarchy, board composition, reporting lines
- **Timelines:** phase names, date ranges, milestones
- **Process maps:** decision gates, flow arrows, swim lanes

### Step 2: Session Context Retrieval

Search past sessions for context on the client, meeting participants, and prior deliverables:
```
session_search(query="Aecon CMMC task")
session_search(query="Aecon toolkit SSP templates evidence")
```

This surfaces prior work (enclave deployment plans, compliance toolkits, FOCI pathway docs,
process maps) that informs the deliverable.

### Step 3: Local Repo Cross-Reference

Search the client repo for existing materials:
```
search_files(path="/home/amyn/repos/aecon-fcs", pattern="*", target="files")
```

Key files to pull from (for Aecon):
- `08-onboarding/source-docs/AFSI_CMMC_L2_Enclave_Deployment_Plan.txt` — 210-day phased build
- `compliance-toolkit/templates/Shared-Responsibility-Matrix.csv` — 58 controls mapped
- `compliance-toolkit/templates/Subcontractor-CMMC-Flow-Down-Tracker.csv` — sub compliance
- `04-planning/foci-mitigation-pathway.html` — DCSA/SSA timeline
- `00-calls/20260701/PROCESS-MAP-2026-07-01.md` — procurement process map
- `compliance-toolkit/REMEDIATION-PLAN.md` — toolkit gap status

### Step 4: Build Deliverable

Synthesize images + repo context into HTML using the Thariq aesthetic (ivory/clay/slate).

**Deliverable structure for DOR + Timeline taskers:**

1. **Executive Summary** — stat cards (110 controls, 7-10mo timeline, 3 compliance gates, $5M threshold) + compliance gate visual (Go/No-Go cards)
2. **Goal 1: Challenges & DOR**
   - Challenge categories (FOCI×CMMC intersection, multi-CAGE scope, ESP chain, subcontractor flow-down, GCC High/commercial split, daily execution burden)
   - DOR matrix: Setup Phase (entity-level activities × parties)
   - DOR matrix: Implementation Phase (enclave build activities × parties)
   - DOR matrix: Daily Execution (cadence + activities × parties)
   - Use R/A/C/I tag styling (colored badges)
3. **Goal 2: Timeline**
   - Greenfield Gantt (7 phases, 7-10 months)
   - Phase detail tables with steps, owners, durations
   - Client-specific acceleration track (Aecon: Jan 2027 target)
   - BD lead-time reference card (scenario → minimum lead time table)
   - BD bid eligibility check (decision tree at opportunity intake)
4. **Regulatory Framework** — collapsible `<details>` for each citation
5. **Appendices** — source documents, immediate action items, cross-references

**Key insight:** The user's exact wording of the action item IS the deliverable requirement.
Don't paraphrase "line out challenges and DOR for CMMC setup, implementation, and daily execution
for Aecon and third parties" into something softer. Build exactly what was asked.

### Step 5: Judge Gate

Dispatch a judge agent that:
- Reads the HTML file via `read_file`
- Evaluates against: completeness, accuracy, gaps, presentation
- Uses the original action item wording as the evaluation criteria
- Returns PASS/FAIL/NEEDS_WORK per criterion with specific gap items

### Step 6: Publish and Report

1. Write HTML to `/data/nextcloud/data/amyn/files/briefings/`
2. `sg www-data -c "chown www-data:www-data ..."` and `chmod 644`
3. `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
4. Send link: `https://brief.h.porb.dev/[filename].html`
5. Discord: brief summary (1-2 sentences) with the link

## Deliverable Type Catalog

### DOR Matrix
- Three lifecycle phases: Setup / Implementation / Daily Execution
- Parties: contractor entity, compliance team (FCS), C3PAO, platform provider (Microsoft),
  ESPs (InEight, Box, Coupa, AvePoint, Abnormal), subcontractors, JV partners, DCSA, BD
- R/A/C/I tags as colored badges in table cells
- Cadence column for daily execution (Continuous / Monthly / Quarterly / Annually)
- Callout for staffing bottleneck insights (e.g., "FCS team holds R on 100% of daily execution")

### CMMC Timeline (JV Formation → Audit)
- Seven-phase Gantt with HTML/CSS bars (no JS, no external dependencies)
- Greenfield: 7-10 months from entity formation to certification
- Client-specific acceleration: shorter timeline leveraging existing certified CAGE codes
- BD lead-time reference card: scenario → minimum lead time → notes
- BD bid eligibility check: decision tree with Go/Stop gates at opportunity intake
- Phase detail tables: step number, activity, owner, duration

### Compliance Gate Briefing
- FOCI × CMMC × CAS three-gate model
- Visual: three cards (Gate 1 FOCI, Gate 2 CMMC, Gate 3 CAS) → Go/No-Go
- Each gate: trigger condition, requirement, failure state
- Bottom line: "any single gate failure blocks the pursuit"
- Status quo assessment: "effectively NO-GO for the strategic pipeline"

### FOCI Transition DOR (Pre-Mitigation vs. Post-Mitigation)

The standard DOR matrix assumes the entity is fully FOCI-mitigated. For foreign-owned
contractors, there is a **transition window** where ownership of several CMMC-adjacent
obligations shifts as the SSA, GSC, TCP, and ECP come online. A transition DOR table
should show:

- CMMC scope decisions: DFCS ad-hoc → GSC concurrence
- 72-hr DIBNet reporting: de facto DFCS → formally designated C-level Affirming Official
- CUI access decisions: ad-hoc DFCS + Legal → ECP framework + GSC exceptions
- Annual CMMC Affirmation: cannot execute → C-level submits in SPRS
- TCP enforcement: ATCP physical controls → full ATCP + TCP + ECP + DCSA annual review

**Key insight to include:** CMMC assessment and FOCI mitigation are **parallel tracks**, not
sequential. The C3PAO can assess regardless of FOCI status. But contract award may require
both (CMMC cert AND FOCI mitigation for Section 847 FCI awards >$5M). BD must track both
gates independently.

### Decisions Required from Leadership

Include a consolidated "Decisions Required" table with:
- Decision description
- Named owner (e.g., "Enzo Zoratto" or role title per sanitization rules)
- Deadline (specific date or quarter)
- Status (PENDING / IN PROGRESS / CRITICAL / DEFERRED)

This is what makes the deliverable actionable beyond being informational. The judge flagged
its absence as a P2 gap — without it, a SteerCo audience reads the briefing but doesn't know
what they need to decide.

### Timeline Realism — Acknowledge Current Readiness

**Problem:** The Aecon-specific timeline initially showed a clean Jan 2027 target without
acknowledging the documented toolkit readiness gap (SSP blanks, unfilled SOPs, zero evidence
artifacts). The judge flagged this as "materially misleading for a SteerCo audience making
resource allocation decisions."

**Resolution:** When building client-specific timelines, ALWAYS include a "reality check"
callout that:
- States the current readiness level (from internal mock assessment or prior QA)
- Identifies the gap between the planned timeline and actual state
- Provides a best-case / likely / worst-case range (not a single optimistic date)
- Recommends a working assumption for BD planning (e.g., "plan for Q2 2027")

Do not present an aspirational target date as a committed plan without that context.

### BD Integration — Non-Negotiable

The timeline is useless to BD without:
1. A **lead-time reference card** by scenario (existing CAGE / new CAGE same tenant / greenfield / FOCI-required)
2. A **bid eligibility check** embedded in the opportunity intake process (a table with Go/Stop gates)
3. A **Phase 2 deadline callout** — when CMMC becomes a hard award condition (~Nov 2026)

## Anti-Patterns to Avoid

- **Skipping images** — even blurry or partially-obscured screenshots contain critical context
- **Paraphrasing action items** — the user's exact wording is the deliverable spec
- **Building from images alone** — always cross-reference the local repo for control-level detail
- **Wall-of-text DOR matrices** — use colored R/A/C/I badges, not plain text letters
- **Generic timelines** — always include the client-specific acceleration track
- **Missing BD integration** — the timeline is useless to BD without a lead-time reference card
  and bid eligibility check embedded at opportunity intake
- **Citing wrong CMMC scoring model** — the CMMC 1.0 model (1000-point, 17×10 weighted) is NOT
  current. CMMC 2.0 uses 110-point max, per-requirement 1/3/5 values, MET/NOT MET/N/A. Always
  load `references/cmmc-l2-assessment-lifecycle.md` before writing scoring details.
- **Representing internal analysis as external findings** — internal mock assessment output must
  be framed as "internal mock assessment identified..." not "the C3PAO found..."
- **Optimistic timelines without readiness context** — always include a reality check showing
  current state vs. planned dates, with a best/likely/worst-case range
- **Missing FOCI transition DOR** — for foreign-owned contractors, show pre-mitigation vs.
  post-mitigation ownership shifts
- **Missing Decisions Required table** — without it the briefing is informational, not actionable
