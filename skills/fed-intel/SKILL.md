---
name: fed-intel
description: Extract federal spending and registration data from USASpending.gov and SAM.gov for any company. Produces structured JSON/CSV data plus an interactive HTML intelligence dashboard. Used standalone or as a /portfolio-recon dependency.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, Agent, TaskCreate, TaskUpdate, TaskList
disable-model-invocation: true
model: opus
---

# /fed-intel -- Federal Intelligence Extraction

You are running a federal data extraction pipeline for HARBOR GovCon. Your job is to pull all available federal spending and registration data for a target company, then produce a structured data package and interactive HTML dashboard.

**Your operator is Amyn Porbanderwala** -- Marine veteran, CISA certified, decade of federal tech consulting, founder of HARBOR GovCon.

## What This Skill Does

Takes any company identifier (name, URL, UEI, CAGE, folder path) and produces:
1. **USASpending data** (PRIMARY) -- all federal awards, transactions, subawards, award details, co-subcontractor network, subaward-share scoring, bulk downloads
2. **SAM.gov entity data** (VALIDATION) -- registration status, NAICS/PSC codes, business types, SBA certifications, exclusions, POCs
3. **Structured analytics** -- KPIs, agency breakdown, NAICS gap analysis, business line classification, seasonal patterns, HHI concentration, subaward-share classification
4. **Interactive HTML dashboard** -- self-contained intelligence dashboard with charts, tables, drill-down, intelligence tab

## Tool Locations

```
operations/tools/usaspending-sam/
  extractor.py           # USASpending extractor (no auth required)
  sam_extractor.py       # SAM.gov extractor (requires API key)
  build_generic_dashboard.py  # Dashboard builder (any company)
```

## Output Location

All output goes to:
```
HARBOR_portfolio/{company_slug}/00-sources/fed-intel/
  recipients.json/csv       # USASpending recipient matches
  recipient_profiles.json   # Full profiles with totals, business types, location
  recipient_children.json   # Subsidiaries
  awards.json/csv           # All federal awards
  transactions.json/csv     # All spending actions
  subawards.json/csv        # Subcontract appearances
  subaward_scoring.json     # Subaward-share scoring and classification
  co_subcontractors.json/csv # Co-subs on shared prime awards (teaming intel)
  award_details/            # Per-award detail JSON
  downloads/                # Bulk CSV ZIPs
  summary.json              # USASpending summary (includes scoring + UEI)
  sam_entities_raw.json     # Full SAM registration data
  sam_entities.csv          # Flattened entity data
  sam_entity_details.json   # Structured SAM details
  sam_exclusions.json       # Exclusion/debarment records
  sam_contract_awards.json  # FPDS contract awards
  sam_summary.json          # SAM summary (with fallback URLs)
  dashboard_data.json       # Computed analytics
  dashboard.html            # Interactive intelligence dashboard
```

---


## Orchestration

This skill fans out to multiple agents. The orchestrator (CEO by default) manages the fan-out, sequences dependencies, and merges results. See `.claude/skills/SKILL-PATTERN.md` for the pattern.

### Step 1 — Resolve inputs & prep workspace

Parse arguments, ask via `AskUserQuestion` if missing, and prep the output paths.

### Step 2 — Parallel fan-out

Independent lanes launch in a single message (multiple `Agent` tool calls). Dependent lanes wait for their input lanes to complete before launching.

Lane list:

**Lane A — (direct)** (API extraction + data writes)
- **prompt must include:** The skill itself runs the SAM and USASpending API calls, writes structured JSON, and renders the HTML dashboard. This is mechanical.
- **return:** structured output the orchestrator can merge

**Lane B — researcher** (Synthesis pass at the end)
- **prompt must include:** After extraction, delegate a researcher pass to interpret the award history, identify concentration risks, flag agency relationships, summarize top vehicles, and produce a human-readable summary.
- **return:** structured output the orchestrator can merge

Each `Agent` call's prompt must include:
1. Command + resolved args
2. Operator: `Amyn Porbanderwala (HARBOR founder)`
3. Playbook: `Read .claude/skills/fed-intel/SKILL.md — your lane scope is <label>`
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

### PHASE 0: SMART DISCOVERY

The skill accepts **any** starting input and auto-discovers the best identifiers for API calls.

#### When Called Standalone (/fed-intel)

**Step 1: Accept Input**

Use `AskUserQuestion` to gather what the user has:

1. "What company are you researching? Provide whatever you have: company name, website URL, UEI, CAGE code, or a path to an existing research folder."
2. "Do you know any additional identifiers?" -- Options: I have their UEI / I have their CAGE code / I have both / Just the name -- find everything

**Step 2: Auto-Discovery**

Based on what the user provided, auto-discover identifiers:

- **If company name only:**
  1. Web search: `"{company name}" site:sam.gov UEI` and `"{company name}" federal contracts`
  2. Try to extract UEI, CAGE, legal business name from search results
  3. Also search for DBA names, parent company names, alternate spellings

- **If URL provided:**
  1. WebFetch the URL to identify the company name
  2. Look for "About" page, footer, or legal name
  3. Then proceed with name-based discovery above

- **If UEI or CAGE provided:**
  1. Use directly for SAM.gov lookup
  2. Extract the legal business name from SAM results
  3. Use that name for USASpending

- **If folder path provided:**
  1. Read any existing JSON files for identifiers (summary.json, sam_summary.json, etc.)
  2. Extract company name, UEI, CAGE from existing data
  3. Only re-extract what's missing or stale

**Step 3: Confirm identifiers**

Present what was discovered and confirm with the user before making API calls:
```
Found: "ACME CORP LLC"
  UEI: ABC123XYZ
  CAGE: 5A1B2
  Source: SAM.gov search result
Proceed with extraction?
```

#### When Called by /portfolio-recon (Autonomous Mode)

Skip the interview entirely. The calling agent provides:
- `company_name` (required)
- `company_slug` (required -- directory name)
- `uei` (optional -- from other research agents)
- `cage` (optional)

Run all phases automatically using provided identifiers.

---

### PHASE 1: CACHE CHECK

Before making any API calls, check for existing data.

**Check for existing output:**
```bash
ls HARBOR_portfolio/{company_slug}/00-sources/fed-intel/
```

**SAM.gov cache policy (30-day TTL):**
- If `sam_summary.json` exists AND is less than 30 days old: **skip SAM extraction**
- If stale or missing: proceed with SAM extraction
- USASpending has no rate limits, so always re-extract for freshness

**Cache age check:**
```bash
# Check file age in days
python3 -c "
import json, os
from datetime import datetime, timedelta
f = 'HARBOR_portfolio/{slug}/00-sources/fed-intel/sam_summary.json'
if os.path.exists(f):
    d = json.load(open(f))
    ext = datetime.fromisoformat(d.get('extraction_date','2000-01-01'))
    age = (datetime.now() - ext).days
    print(f'SAM data is {age} days old')
    print('FRESH' if age < 30 else 'STALE')
else:
    print('NO_DATA')
"
```

If SAM data is FRESH, log "Using cached SAM data (X days old)" and skip to Phase 3.

---

### PHASE 2: SAM.GOV EXTRACTION

**API Key Resolution:**
The SAM.gov API requires an API key. Resolve it in this order:
1. Environment variable: `SAM_API_KEY`
2. Fallback file: `operations/tools/usaspending-sam/.env.localsamgov` (read the `apikey=` value)

If no key is found, warn the user and proceed with USASpending only.

**Rate limit awareness:** Personal keys have 10 requests/day. The extractor makes ~4 calls per company. If the rate limit is hit (HTTP 429), log the error and continue with USASpending data only.

**Run SAM extractor (UEI-first when available):**
```bash
cd /Users/amynporb/Documents/_Projects/2026_books && \
python3 operations/tools/usaspending-sam/sam_extractor.py \
  "{company_name}" \
  --uei "{uei_if_known}" \
  --api-key "$SAM_API_KEY" \
  --company-dir "HARBOR_portfolio/{company_slug}/00-sources/fed-intel"
```

If no UEI is known, omit the `--uei` flag. The extractor will search by name (less reliable, uses more API calls).

The `--uei` flag does a direct UEI lookup instead of fuzzy name search. This is more reliable and uses fewer of the rate-limited API calls.

**If no SAM registration found:**
Try alternate search terms automatically:
1. Try without "LLC", "Inc", "Corp" suffixes
2. Try DBA name if known
3. Try parent company name if known
4. Try with common abbreviations expanded
5. If all fail, log "No SAM.gov registration found" and proceed

**After SAM extraction:**
Read `sam_entity_details.json` to extract:
- UEI (use for USASpending dedup in Phase 3)
- Legal business name (use as search term for USASpending)
- NAICS codes, SBA certifications, business types (for dashboard)

---

### PHASE 3: USASPENDING EXTRACTION

**Run USASpending extractor:**
```bash
cd /Users/amynporb/Documents/_Projects/2026_books && \
python3 operations/tools/usaspending-sam/extractor.py \
  "{company_name}" \
  --uei "{uei_if_known}" \
  --company-dir "HARBOR_portfolio/{company_slug}/00-sources/fed-intel"
```

If no UEI is known, omit the `--uei` flag. The extractor will search by name.

This runs the full 10-step pipeline:
1. Recipient search (UEI-first if provided, then name fallback)
2. Recipient profiles (full profiles with totals, business types, location)
3. Subsidiaries/children
4. Awards (all contracts, grants, IDVs -- paginated)
5. Transactions (all spending actions -- paginated)
6. Subawards (company as subcontractor)
7. Award details (per-award JSON)
8. Co-subcontractor discovery (other subs on same primes)
9. Subaward-share scoring (sub-dependency classification)
10. Bulk CSV downloads (comprehensive, async)

**This takes 3-8 minutes** depending on the company's federal footprint. Co-sub discovery (step 8) adds time proportional to number of prime awards. Bulk downloads (step 10) are async.

**Important:** The USASpending API has no authentication and no rate limits. Always run the full extraction. Use `--skip-co-subs` for faster runs when teaming intel isn't needed.

---

### PHASE 4: DASHBOARD GENERATION

After both extractors complete, generate the analytics dashboard.

**Run the generic dashboard builder:**
```bash
cd /Users/amynporb/Documents/_Projects/2026_books && \
python3 operations/tools/usaspending-sam/build_generic_dashboard.py \
  "HARBOR_portfolio/{company_slug}/00-sources/fed-intel" \
  --company-name "{company_name}" \
  --uei "{uei_if_known}"
```

The dashboard builder:
1. Loads all available JSON files (handles missing SAM data gracefully)
2. Auto-deduplicates recipients by UEI match
3. Auto-classifies business lines by awarding agency
4. Computes analytics: KPIs, HHI, NAICS gap, seasonal patterns, award sizing, YoY growth
5. Generates `dashboard_data.json` (structured analytics)
6. Generates `dashboard.html` (self-contained interactive dashboard)

---

### PHASE 4.5: EDITORIAL LINT + CROSS-CLIENT LEAK GATE (BLOCKING if delivered standalone)

The dashboard is primarily a machine-generated table/chart artifact, but when delivered as a standalone deliverable (not just feeding /portfolio-recon) it crosses the client-facing artifact threshold and inherits the same editorial rules as briefings, decks, and emails. See LRN-20260411-014.

When called by /portfolio-recon in autonomous mode, skip this gate. /portfolio-recon Phase 6.5 runs the combined gate against all downstream deliverables. When called standalone (`/fed-intel` user-invoked), run the gate before handing the file to the user:

```bash
DASH="HARBOR_portfolio/{company_slug}/00-sources/fed-intel/dashboard.html"

# Editorial lint (narrative fields only; table numbers are machine-generated and exempt)
grep -n -P '[\x{2013}\x{2014}]' "$DASH" && echo "BLOCK: em/en dash in dashboard narrative" && exit 1
grep -n -i -E 'rebuild|rebuilt|single sharpest|existential anchor|mind.blow|unprecedented|groundbreaking' "$DASH" && echo "BLOCK: banned phrase in dashboard narrative" && exit 1

# Cross-client leak grep against portfolio-aliases.md
python3 <<PY
import re
aliases = {}
current = None
with open("admin/memory/portfolio-aliases.md") as fh:
    for line in fh:
        m = re.match(r"^###\s+(.+)$", line)
        if m: current = m.group(1).strip(); aliases[current] = []; continue
        m = re.match(r"^-\s+(.+?)(?:\s*\(|$)", line)
        if m and current: aliases[current].append(m.group(1).strip())

this_slug = "{company_slug}"
with open("$DASH") as fh: content = fh.read().lower()
leaks = []
for slug, alist in aliases.items():
    if slug == this_slug: continue
    for alias in alist:
        if alias.lower() in content: leaks.append(f"{slug}: {alias}")
if leaks:
    print("CROSS-CLIENT LEAK in dashboard:")
    for l in leaks: print(f"  {l}")
    exit(1)
PY
```

If the gate fires, the dashboard is NOT delivery-ready. Fix the underlying build_generic_dashboard.py template (not the rendered HTML) and re-run.

---

### PHASE 5: SUMMARY & HANDOFF

**Present findings to the user (or calling agent):**

1. **Key stats:** Total awards, total dollar value, agencies, active awards, SAM status
2. **Critical flags:** Lapsed SAM, exclusions, missing certifications, single-agency concentration
3. **HARBOR signals:** Productization indicators from the federal data (named offerings in award descriptions, repeat patterns, NAICS breadth)
4. **Files created:** List every output file with path

**If called by /portfolio-recon:**
Return a structured summary that the calling agent can incorporate:
```
FED-INTEL COMPLETE
Company: {name}
UEI: {uei}
CAGE: {cage}
SAM Status: Active/Lapsed/Not Found/Rate Limited
Total Federal Awards: {n}
Prime Value: ${amount}
Sub Value: ${amount}
Total Federal Footprint: ${amount}
Subaward Share: {pct}% ({classification})
Agencies: {list}
Active Awards: {n}
Certifications: {list}
Exclusions: Clean/WARNING
Co-Subcontractors: {n} found
Dashboard: HARBOR_portfolio/{slug}/00-sources/fed-intel/dashboard.html
Data Dir: HARBOR_portfolio/{slug}/00-sources/fed-intel/
```

---

## /portfolio-recon Integration

When `/portfolio-recon` Phase 1 runs, it spawns `/fed-intel` as **Agent 2** with these parameters:

```
Run /fed-intel in autonomous mode for {company_name}.
Company slug: {company_slug}
UEI: {uei_if_known_from_other_agents}
CAGE: {cage_if_known}

Skip the interview. Use these identifiers directly.
Write output to: HARBOR_portfolio/{company_slug}/00-sources/fed-intel/

Return the structured summary when complete.
```

The /portfolio-recon skill's Phase 2 (Synthesis) then reads the fed-intel output files to incorporate federal data into the company profile, HARBOR assessment, and market analysis.

---

## Constraints

- **Never fabricate data.** All numbers come from API responses. If an API call fails, report it.
- **SAM API key is rate-limited.** Check cache before calling. If rate-limited, continue with USASpending only.
- **Bulk downloads are slow.** The async ZIP downloads can take 1-3 minutes. The agent should wait for them.
- **UEI-based dedup is critical.** Without it, USASpending may return false positives (same company name, different entity). Always pass `--uei` to the dashboard builder when available.
- **Do not skip subawards.** Subaward data reveals teaming relationships and hidden revenue. Always extract it.
- **SAM API keys expire every 90 days.** If the key fails with 403/401, inform the user to renew at sam.gov > Account Details > API Information.
- **The .env.localsamgov file contains a real API key.** Never log it, commit it, or expose it in output.

---

## /shrink-wrap v2 orchestration integration (added 2026-05-26)

The /fed-intel skill provides federal contracts + subawards + agency-budget data that feeds two /shrink-wrap surfaces:

### Persona-side consumption

When /shrink-wrap runs at federal lens, these personas may consume /fed-intel-produced data:
- **persona-market-analyst-federal** — uses awards.json + agency budgets for Ch 5 Dim 2 (Cross-Agency Demand) + Dim 4 (Vehicle Access) scoring
- **persona-customer-voice-federal-co** — uses subawards.json to identify teaming patterns + comparable contract awards for Ch 13 (pricing) reality checks
- **persona-fedramp-auditor** — uses awards data to identify which agencies' authorization workflow patterns apply

### Recommended pre-/shrink-wrap sequence for federal-lens runs

1. `/fed-intel <UEI>` — pulls awards + subawards + agency procurement forecasts
2. `/shrink-wrap` scope=full-methodology lens=federal — runs the full HARBOR methodology with the fed-intel data already present in the member's directory

If /fed-intel hasn't been run, harvest-agent's Phase 1 (Contract Mapping) will lack the foundation data, and Ch 5 Dim 2 scoring will be qualitative-only.

### Deep-research escalation

If a /shrink-wrap persona (typically persona-market-analyst-federal) hits an unfamiliar agency or PSC during a run, it may fire /deep-research. /deep-research is a separate skill that produces narrow-topic research artifacts; /fed-intel is the broader data-pulling skill that runs once per UEI as a foundation.

### Cross-references

- harvest-agent reads /fed-intel output as prerequisite
- /portfolio-recon dispatches /fed-intel as part of its 3-way parallel research fan-out
