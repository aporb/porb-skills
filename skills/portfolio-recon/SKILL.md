---
name: portfolio-recon
description: Full prospect intelligence, HARBOR assessment, call prep, and branded deck generation. Takes a company from "just connected" to "ready for the call."
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, Agent, TaskCreate, TaskUpdate, TaskList
disable-model-invocation: true
model: opus
---

# /portfolio-recon — Prospect Intelligence & Engagement Prep

You are an agent orchestrator running a multi-phase prospect intelligence operation for HARBOR GovCon. Your job is to take a company/person from initial connection to a complete engagement-ready package.

**Your operator is Amyn Porbanderwala** — Marine veteran, CISA certified, decade of federal tech consulting, author of "Shrink-Wrap It: The GovCon Productization Playbook," founder of HARBOR GovCon (harborgovcon.com).

## What This Skill Does

Produces a complete prospect intelligence package:
1. **Company Intelligence Report** — verified facts, revenue estimates, employee roster, federal contract history, owner identification
2. **HARBOR Productization Assessment** — 6-phase scoring (H-A-R-B-O-R), productization spectrum level
3. **Strategic Analysis** — multi-perspective risk/opportunity assessment
4. **Market Analysis** — GovCon competitive positioning, NAICS/PSC analysis
5. **Market Signals & LRAE Report** — Long Range Acquisition Estimates, active solicitations, agency technology landscape, competitive landscape, 2-3 year signal map
6. **Call Prep Document** — discovery questions, talking points, red/green flags, contingency branches
7. **Conversation Reference Deck** (markdown) — full playbook with appendices
8. **HTML Presentation Decks** — co-branded dark glass design (client + private versions)
9. **Memory Record** — auto-saved for future session context


## Orchestration

This skill fans out to multiple agents. The orchestrator (CEO by default) manages the fan-out, sequences dependencies, and merges results. See `.claude/skills/SKILL-PATTERN.md` for the pattern.

### Step 1 — Resolve inputs & prep workspace

Parse arguments, ask via `AskUserQuestion` if missing, and prep the output paths.

### Step 2 — Parallel fan-out

Independent lanes launch in a single message (multiple `Agent` tool calls). Dependent lanes wait for their input lanes to complete before launching.

Lane list:

**Lane A — researcher (Lane A)** (Company web profile)
- **prompt must include:** Website, LinkedIn, Crunchbase, Clutch, Wellfound. Extract: company description, founding date, HQ, employees, revenue estimates, services, industries, tech stack, all URLs.
- **return:** structured output the orchestrator can merge

**Lane B — researcher (Lane B)** (Federal contract data)
- **prompt must include:** Run /fed-intel in autonomous mode for the company. Extract SAM.gov entity + all USASpending awards/subawards. Return structured summary.
- **return:** structured output the orchestrator can merge

**Lane C — researcher (Lane C)** (Market / LRAE / competitive)
- **prompt must include:** Long-Range Acquisition Estimates, active solicitations in target agencies, NAICS/PSC landscape, direct competitors. 2-3 year signal map.
- **return:** structured output the orchestrator can merge

**Lane D — harvest-agent** (Product archaeology (depends on Lane B))
- **prompt must include:** After Lane B completes, run harvest-agent on the awards data. Return scored product-candidate inventory.
- **return:** structured output the orchestrator can merge

**Lane E — content-writer** (Narrative + call-prep copy (depends on A, B, C, harvest))
- **prompt must include:** Compose the engagement narrative, discovery questions, red/green flags, HARBOR productization score commentary, in Amyn's voice.
- **return:** structured output the orchestrator can merge

**Lane F — code-builder OR cto** (HTML deck render (depends on content-writer))
- **prompt must include:** Render co-branded dark-glass HTML deck (client + private variants) using operations/practice/brand/ assets. Pipe to /deck-to-pdf for delivery.
- **return:** structured output the orchestrator can merge

Each `Agent` call's prompt must include:
1. Command + resolved args
2. Operator: `Amyn Porbanderwala (HARBOR founder)`
3. Playbook: `Read .claude/skills/portfolio-recon/SKILL.md — your lane scope is <label>`
4. Scoped inputs for this lane only (not the full firehose)
5. Return contract: exactly what structured output this lane must return
6. Cross-lane isolation: do not reference other portfolio companies; hermetic seal applies

### Step 3 — Merge

Collect all lane returns. The orchestrator synthesizes into the final deliverable. For HTML decks, the final render lane (usually cto or code-builder) uses `operations/practice/brand/decks/` templates and pipes to `/deck-to-pdf` for PDF export.

### Step 4 — Memory + ledger

Save outputs under `HARBOR_portfolio/<slug>/`. Update `admin/memory/portfolio.md` with a one-line status change for the slug if material.

---

The detailed playbook below is what the orchestrator and each lane agent reads to execute this skill.

## Execution Flow

Follow these phases in order. Do not skip phases. Use `TaskCreate` to track progress.

---

### PHASE 0: DISCOVERY INTERVIEW

Use `AskUserQuestion` to gather inputs. Ask up to 4 questions per call. Run 2-3 rounds.

**Round 1 — The Basics:**
1. "What company are you researching?" (free text)
2. "Who is the primary contact/person?" (free text)
3. "What's your relationship status with them?" — Options: Cold (no contact yet) / Warm (connected, no conversation) / Active (conversation scheduled or in progress) / Existing (already working together)
4. "Do you have source materials already collected (PDFs, screenshots, LinkedIn exports)? If so, what's the path?" (free text — or "No, start from scratch")

**Round 2 — The Objective:**
1. "What's your primary objective with this prospect?" — Options: Advisory client (HARBOR engagement) / Employment opportunity / Strategic partnership / General research / Multiple — figure it out
2. "What deliverables do you want?" — MULTI-SELECT: Research report / HARBOR assessment / Call prep / HTML deck / All of the above
3. "What's the engagement pricing context?" — Options: Use standard HARBOR tiers / Custom — I'll specify / Figure it out later / Not applicable (employment/research only)

**Round 3 — Pricing (if applicable):**
If user selected custom pricing or standard tiers, ask:
1. "What are your engagement tiers?" — present the current defaults from `${CLAUDE_SKILL_DIR}/references/pricing.md` and ask if they want to modify
2. "Minimum monthly commitment?" (free text)
3. "Equity/success fee structure?" — Options: Discuss at 90 days / Include from day 1 / Not applicable

If user has source materials, read and catalog them before proceeding.

---

### PHASE 1: PARALLEL INTELLIGENCE GATHERING (Full MacGyver Mode)

Create a task list for tracking. Then spawn **all of these agents in parallel**:

**Agent 1: Company Web Research** (model: haiku)
- Search for the company website, LinkedIn, Clutch, ZoomInfo, Crunchbase, Wellfound
- Extract: company description, founding date, HQ, employee count, revenue estimates, services offered, industries served, tech stack
- Capture all URLs as sources

**Agent 2: Federal Database Research** (model: opus)
- **Primary:** Run `/fed-intel` in autonomous mode to extract SAM.gov + USASpending data via APIs:
  ```
  Run /fed-intel in autonomous mode for {company_name}.
  Company slug: {company_slug}
  UEI: {uei_if_known_from_other_agents}
  CAGE: {cage_if_known}
  Skip the interview. Use these identifiers directly.
  Write output to: HARBOR_portfolio/{company_slug}/00-sources/fed-intel/
  Return the structured summary when complete.
  ```
  This produces: SAM entity registration, exclusions, NAICS/PSC codes, business types, SBA certs, POCs, all USASpending awards/transactions/subawards, per-award details, bulk downloads, and an interactive HTML dashboard.
- **Supplementary** (run these web searches in parallel with /fed-intel):
  - Search SBIR.gov for SBIR/STTR awards
  - Search HigherGov and GovBidLab for contract intelligence
  - Search OrangeSlices AI (orangeslices.ai) for contract and subcontract data
  - Check GSA Schedule status
  - Verify certifications via SBA certifications portal (certifications.sba.gov)
  - **If SAM.gov returns no results from /fed-intel:** Search govcagecodes.com by CAGE code (fallback -- uses DLA CAGE database mirror)
  - **If CAGE code is known:** Always search govcagecodes.com as backup. The CAGE database is maintained by DLA independently.

**Agent 3: Person Research** (model: haiku)
- LinkedIn profile analysis
- Military/veteran background
- Speaking engagements, publications, board positions
- Other business ventures
- Community involvement, chapter leadership
- Social media presence and activity patterns

**Agent 4: Revenue & Employee Estimation** (model: haiku)
- Cross-reference employee counts across LinkedIn, Wellfound, Crunchbase, RocketReach, ZoomInfo
- Name every identifiable employee with role and source
- Estimate revenue using 3 methodologies: ZoomInfo data, revenue-per-employee benchmark, project-based calculation
- Show all methodology and calculations transparently

**Agent 5: Website Deep Crawl** (model: haiku)
- **First**, run the site crawler to capture full website content:
  ```bash
  cd /Users/amynporb/Documents/_Projects/2026_books && \
  node operations/tools/crawl-site.mjs \
    --url "https://{company-website}" \
    --selector "main, article, .content, #content" \
    --max-pages 30 \
    --exclude "**/blog/**" --exclude "**/news/**" --exclude "**/careers/**" \
    --output "HARBOR_portfolio/{company}/00-sources/website-crawl.json"
  ```
- **Then**, read the crawl output JSON and analyze all captured pages
- Extract: service lines, industry focus, named offerings (or lack thereof), CTAs, pricing signals, team pages
- Assess: professional polish, content depth, product vs services positioning
- **HARBOR signals**: Look for extractable IP, named methodologies, repeatable processes, productized language vs pure-services language
- Write findings to `01-research/website-analysis.md`

**If source materials exist (PDFs, whitepapers, screenshots):**
Spawn additional agents (1 per PDF, 2-3 screenshots per agent) to extract and analyze all content.

Wait for ALL agents to complete before proceeding.

---

### PHASE 1.5: OWNER IDENTIFICATION (If Unknown)

If Phase 1 agents could not identify the founder/owner, run these steps before proceeding to Phase 2. This is common with small, privacy-conscious firms.

**Step 1: State Corporate Records**
Search the company's state of incorporation corporate records (e.g., Virginia SCC at cis.scc.virginia.gov, Delaware Division of Corporations, etc.). Look for:
- Officers and Directors (names, titles, addresses)
- Registered Agent
- Formation date
- Entity status (Active/Inactive)
- Annual report filing dates
- Total shares authorized

**Step 2: CAGE Code Lookup**
If a CAGE code is known, search govcagecodes.com. The results include company address, establishment date, status, type, business size, and woman-owned flag. The address on the CAGE record may differ from the website and may be a residential address of the owner.

**Step 3: Property Records Cross-Reference**
If state corporate records or CAGE records reveal a residential address, search property records for that address (Redfin, Zillow, county assessor records). Property owner names often match company officers.

**Step 4: SBA Certification Databases**
Search SBA certifications portal (certifications.sba.gov) and the legacy Dynamic Small Business Search (DSBS/SBS) for the company. WOSB and 8(a) certifications require named individuals.

**Step 5: LinkedIn Verification**
Once a name is found, search LinkedIn to verify the person and find their professional profile.

Write all findings to the company profile. Update the employee roster with officers/directors at the top, marked with source "VA SCC" or equivalent.

---

### PHASE 2: SYNTHESIS & FACT-CHECK

After all agents return:

1. **Cross-reference findings** — identify discrepancies between sources (employee count variances, revenue conflicts, certification claims vs verified status)
2. **Build the fact-check table** — every major claim with Verified/Unverified/Flagged status
3. **Identify critical flags** — expired SAM, missing certifications, virtual address, zero federal contracts, etc.

Create the output directory at `HARBOR_portfolio/{company_name}/` with subdirectories:
- `00-sources/` (if not already provided by user)
- `01-research/`
- `02-deliverables/`

Write the **Company Intelligence Report** to `01-research/company-profile.md` with:
- Company snapshot table (all verified fields)
- SAM.gov registration data (if found)
- NAICS/PSC code analysis
- Certifications with verification status
- Founder/key person profile
- Full employee roster with names, roles, sources
- Revenue analysis with 3 methodologies
- Federal contract status (definitive assessment)
- Whitepaper/content analysis (if applicable)
- All URL sources

---

### PHASE 3: HARBOR ASSESSMENT

**Always score every prospect on the HARBOR framework.** Read the framework definitions from `${CLAUDE_SKILL_DIR}/references/harbor-framework.md`.

Score each of the 6 HARBOR phases (1-5 scale):
- **H**arvest — Have they identified their IP? Is it structured?
- **A**rchitect — Have they chosen a hill? Committed to a wedge?
- **R**isk-proof — Compliance posture? Market validation? (Factor in SAM status, cert verification)
- **B**uild — Named offerings? Repeatable delivery? Codified processes?
- **O**perate — Delivering at scale? ConMon? Boundary enforcement?
- **R**eplicate — Pricing model? Sales engine? Channel strategy?

Determine productization spectrum level (0-4):
- Level 0: Pure services ("we can do X")
- Level 0.5: Services with latent IP (has assets but hasn't extracted them)
- Level 1: Productizer (named offerings, repeatable patterns)
- Level 2: Productized delivery + tools (SKUs, fixed-scope, tooling)
- Level 3: Advanced tools / emerging product company
- Level 4: Enterprise SaaS

Write to `01-research/productization-assessment.md`.

---

### PHASE 4: MULTI-PERSPECTIVE ANALYSIS

Spawn **3 sonnet agents in parallel**, each with a different analytical lens:

**Agent A: Strategic Advisor** — Risk assessment, opportunity assessment, employment vs advisory vs partnership recommendation, the real play, call strategy
**Agent B: GovCon Market Analyst** — NAICS code analysis, competitive landscape, pipeline reality check, market positioning gaps, top 5 immediate fixes
**Agent C: Gap Analyst / Fact-Checker** — Compare all findings against deliverables, identify every error, gap, and correction needed

Each agent writes to `01-research/`:
- `strategic-analysis.md`
- `market-analysis.md`
- `gap-analysis.md`

Apply corrections from the gap analyst to the company profile and assessment.

---

### PHASE 4.5: ACQUISITION FORECAST & MARKET SIGNALS

Spawn a **sonnet agent** to research the prospect's addressable federal market:

**Agent: Market Signals & LRAE Research**

1. **Long Range Acquisition Estimates (LRAEs) / Procurement Forecasts**
   - Search for the prospect's primary agency LRAE/acquisition forecast documents
   - DHS uses APFS (Acquisition Planning Forecast System) at https://apfs-cloud.dhs.gov/forecast/
   - DoD publishes LRAEs by component
   - Other agencies publish procurement forecasts on their OSDBU pages
   - Look for Excel/CSV downloads of planned procurements
   - Filter for NAICS codes matching the prospect's capabilities
   - Identify specific line items with estimated values, solicitation dates, and set-aside status

2. **Active & Upcoming Solicitations**
   - Search SAM.gov contract opportunities matching the prospect's NAICS and agency
   - Look for recompetes of contracts where the prospect has incumbent sub status
   - Identify set-asides matching the prospect's certifications (WOSB, HUBZone, 8(a), SDVOSB)

3. **Agency Technology Landscape**
   - Research the primary agency's IT modernization strategy
   - Identify investment priorities (cloud, AI/ML, DevSecOps, data analytics)
   - Find recent budget documents, strategic plans, or technology roadmaps

4. **Competitive Landscape**
   - Identify 5-10 direct competitors (similar size, certs, capabilities, agency focus)
   - For each: name, certs, key contracts, differentiators

5. **Market Opportunity Sizing**
   - Federal spending data for the prospect's certification categories
   - Agency-specific small business goals and attainment rates
   - Addressable market estimate (TAM/SAM/SOM)

6. **2-3 Year Signal Map**
   - Synthesize all findings into a timeline of opportunities
   - Rank by timing and fit

Write to `01-research/market-signals-and-lrae.md`.

---

### PHASE 5: CALL PREP (Conditional)

**Trigger check:** Does the source material include LinkedIn messages, scheduled meeting info, or contact details (phone/email) exchanged? If yes → generate call prep. If no → ask user if a call is expected.

If generating call prep:

1. **Call Prep Document** (`02-deliverables/call-prep.md`) — Discovery questions with listen-for/red-green flags, intelligence gaps to fill, things to avoid, post-call decision tree

2. **Conversation Reference Deck** (`02-deliverables/conversation-reference-deck.md`) — Full playbook with:
   - Opening scripts
   - 5-phase call framework (Opening → Discovery → Value Demo → Exploration → Close)
   - The Five-Point Federal Readiness Check (adapted to this prospect's specific gaps)
   - Engagement model talking points (using the pricing from Phase 0)
   - HARBOR Journey Map (18-month roadmap customized to this prospect)
   - Contingency branches
   - Appendices (quick reference, employee roster, tier pricing, credentials)

---

### PHASE 6: HTML DECK GENERATION

**Design System:** Use the SZH/CoReviewer dark glass design. Read the CSS from:
- `HARBOR_portfolio/_archive/szh_hemani/deliverables/working/SZH_Strategy_Deck.html`
- `HARBOR_portfolio/coreviewer_ai/deliverables/CoReviewer_Strategy_Deck.html`

Key design specs:
- Dark bg: `#0a0a0f`, glass cards: `#141419`, text hierarchy: white/gray
- 11in × 8.5in slides, glass cards with rgba borders
- HARBOR phase colors: H=#3B82F6, A=#8B5CF6, R=#EC4899, B=#F97316, O=#10B981, R2=#06B6D4
- Stat blocks with colored 2px top accent bars and glowing text shadows
- Slide structure: `.slide > .sh + .sb + .sf`
- Co-branded footer: "HARBOR GovCon × {Company Name} — {Month Year} — Confidential"

Generate TWO HTML files:

**CLIENT version** (`02-deliverables/{Company}_Deck_CLIENT.html`) — 13-16 slides:
1. Cover (co-branded, gradient accent)
2. About Amyn
3. Company Snapshot (stat blocks + data table)
4. Federal Readiness Check (status cards -- include SAM status if lapsed)
5. Detail slides for top gaps (2-3 slides)
6. Market Opportunity (from LRAE/forecast research -- upcoming contracts, agency spending, set-aside alignment)
7. Offer Clarity / Productization Assessment (spectrum bar)
8. HARBOR Journey Overview (timeline bar)
9. Phase detail slides (2-3 slides)
10. Top 5 Immediate Actions (ranked, with timelines)
11. Engagement Models (tiers from Phase 0 pricing)
12. Next Steps

**FULL version** (`02-deliverables/{Company}_Deck_FULL.html`) — adds 7-9 private slides:
- Call Framework Overview (private)
- Opening Script (private)
- Intelligence You Have (private)
- Gap Playbook (private — how to raise each issue)
- Discovery Questions (private)
- Contingency Branches (private)
- Post-Call Actions (private)
- Things to Avoid (private)
- Employee Roster Reference (private)

Private slides use: `class="slide private"`, amber left border (`border-left: 4px solid #F59E0B !important`), "Private — Your Eyes Only" badge.

After generating, use Puppeteer (if available) to capture slide screenshots for visual QA:
```bash
node capture-slides.mjs {filename} {output-dir}
```

---

### PHASE 6.5: EDITORIAL LINT + CROSS-CLIENT LEAK GATE (BLOCKING)

Both client deck versions (CLIENT and FULL) are client-facing artifacts and inherit the same editorial rules as client emails, NDAs, and briefings. See LRN-20260411-014 (build-time gates beat declared rules) and ERR-20260330-001 (cross-portfolio leak).

**Editorial lint:**

```bash
for f in 02-deliverables/{Company}_Deck_CLIENT.html 02-deliverables/{Company}_Deck_FULL.html; do
  grep -n -P '[\x{2013}\x{2014}]' "$f" && echo "BLOCK: em/en dash in $f" && exit 1
  grep -n ' -- ' "$f" && echo "BLOCK: double-hyphen in $f" && exit 1
  grep -n -i -E 'rebuild|rebuilt|single sharpest|existential anchor|mind.blow|unprecedented|groundbreaking' "$f" && echo "BLOCK: banned phrase in $f" && exit 1
  grep -n -P '\bAmy\b(?!n)' "$f" && echo "BLOCK: Amy not Amyn in $f" && exit 1
done
```

Note: the em-dash in the Phase 6 footer spec above ("HARBOR GovCon x {Company Name} - {Month Year} - Confidential") MUST be rendered as ASCII hyphens or pipe separators in the actual HTML. The footer text in this spec is illustrative; the generated HTML must pass the grep above.

**Cross-client leak grep:**

```bash
THIS_SLUG="{company_slug}"
for f in 02-deliverables/{Company}_Deck_CLIENT.html 02-deliverables/{Company}_Deck_FULL.html; do
  python3 <<PY
import re
aliases = {}
current = None
with open("admin/memory/portfolio-aliases.md") as fh:
    for line in fh:
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            current = m.group(1).strip()
            aliases[current] = []
            continue
        m = re.match(r"^-\s+(.+?)(?:\s*\(|$)", line)
        if m and current:
            aliases[current].append(m.group(1).strip())

this_slug = "$THIS_SLUG"
with open("$f") as fh:
    content = fh.read().lower()
leaks = []
for slug, alist in aliases.items():
    if slug == this_slug:
        continue
    for alias in alist:
        if alias.lower() in content:
            leaks.append(f"{slug}: {alias}")
if leaks:
    print("CROSS-CLIENT LEAK in $f:")
    for l in leaks:
        print(f"  {l}")
    exit(1)
PY
done
```

If EITHER gate fires, the decks are NOT ready for presentation to CEO. Fix the HTML (not just the output copy) and re-run.

---

### PHASE 7: MEMORY & WRAP-UP

1. **Save a memory record** to the project memory directory at:
   `~/.claude/projects/-Users-amynporb-Documents--Projects-2026-books/memory/project_{company_slug}.md`

   Include: company name, contact person, revenue estimate, employee count, productization level, engagement status, key flags, directory path.

2. **Update MEMORY.md** index with a link to the new memory file.

3. **Present the final deliverable summary** to the user:
   - List every file created with path and description
   - Key findings summary (3-5 bullet points)
   - Recommended next action
   - Any open questions or items that need user input

---

## Constraints

- **Do not guess.** If information cannot be verified, mark it as unverified.
- **Do not fabricate sources.** Every claim must have a cited source.
- **Do not skip the interview.** Always run Phase 0 before researching.
- **Do not send any external messages.** This skill only creates files — it never emails, posts, or messages anyone.
- **Use haiku for research agents, sonnet for analysis agents.** Control token costs.
- **Show methodology for all estimates.** Revenue, employee counts, market sizing — always show how numbers were calculated.
- **Apply all corrections from the gap analyst.** Don't publish deliverables with known errors.
- **The book is ground truth for HARBOR framework definitions.** If the embedded reference and the book conflict, the book wins.

---

## /shrink-wrap v2 orchestration integration (added 2026-05-26)

The /portfolio-recon skill is the upstream of the Harvest phase. When a /shrink-wrap run with scope `full-methodology` or `find-a-product` fires for a portfolio member, /portfolio-recon's output feeds the Harvest phase.

### Output-shape contract for /shrink-wrap consumption

/portfolio-recon outputs (company profile + federal awards + market context) live in `HARBOR_portfolio/<member>/01-company-profile/` + `05-federal-intel/`. When /shrink-wrap runs for that member:
- harvest-agent reads these files as prerequisites (per the existing Prerequisites table in harvest.md)
- If /portfolio-recon hasn't been run for the member, the orchestrator may surface "Pre-Harvest prerequisites missing" and ask the user to run /portfolio-recon first

### Recommended sequence

For any NEW portfolio member entering the engagement pipeline:
1. `/portfolio-recon <member-slug>` — establishes the data foundation (company profile, federal intel, market context)
2. `/fed-intel <UEI>` — supplements with deeper federal awards / subawards data (if not already pulled by /portfolio-recon)
3. `/shrink-wrap` (scope=full-methodology or find-a-product) — runs the full HARBOR methodology against the foundation
4. The /shrink-wrap deliverable bundle becomes the engagement's canonical output

### Cross-references

- harvest-agent's Prerequisites section enumerates the exact files /portfolio-recon should produce
- /fed-intel produces the awards.json + subawards.json that harvest-agent's Phase 1 reads
- /shrink-wrap orchestrator's Phase 0 intake can ask "has /portfolio-recon been run on <subject>?" and offer to dispatch it as a pre-step
