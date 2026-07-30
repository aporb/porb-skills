---
name: sam-monitor
description: Weekly check of HARBOR + flagged client UEIs against SAM.gov entity registration. Alerts when expiration is within 60 days. Cross-checks HigherGov when SAM API returns suspicious negatives. Reads watch list from admin/memory/sam-watch.md.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch
model: haiku
user-invocable: true
---

# /sam-monitor — SAM.gov Entity Registration Monitor

**Born from ERR-20260328-001** — A SAM.gov API search returned empty for an active entity, and the initial conclusion was "registration lapsed." It hadn't lapsed; the search query was wrong. This skill encodes the cross-check pattern so the same false negative cannot become a client-facing claim again.

## What This Skill Does

For every UEI on the watch list, this skill:

1. Queries the SAM.gov entity API for current registration status
2. Parses expiration date, NAICS codes, registration status
3. If status is "lapsed" or expiration is within 60 days, cross-checks HigherGov as a sanity check
4. Writes a status report to `admin/memory/sam-status-YYYY-MM-DD.md`
5. Alerts the CEO agent if any entity is lapsed, expiring soon, or showing data anomalies


## Execution

This skill dispatches to **ledger-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `admin/memory/sam-watch.md (watch list of UEIs)`
  - `admin/memory/state.md (for prior-run context)`

### Step 3 — Dispatch to ledger-agent

Call the **Agent** tool with:

- `subagent_type`: `ledger-agent`
- `description`: `"Weekly SAM.gov entity-registration check with HigherGov cross-verification"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/sam-monitor <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/sam-monitor/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `admin/memory/sam-status-<YYYY-MM-DD>.md report + alerts for any lapses/expirations within 60 days`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

If anomalies found, flag in admin/memory/state.md for the next CEO briefing.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what ledger-agent reads as its authoritative reference when executing this skill.

## What This Skill Does NOT Do

- Does NOT renew SAM registrations (manual process — Amyn must complete the renewal in SAM.gov UI)
- Does NOT track NAICS code changes (use `/fed-intel` for that)
- Does NOT track contract awards (use `/fed-intel`)
- Does NOT monitor SBA cert status (use `/cert-tracker` for 8(a), SDVOSB, WOSB, HUBZone)
- Does NOT email anyone — alerts only flow to CEO agent for review

## When to Use

| Trigger | Action |
|---------|--------|
| Weekly cron | Default schedule. Run every Monday morning. |
| Adding a new prospect to the pipeline | Add their UEI to the watch list, then run once |
| Pre-engagement audit | Run before signing any new SOW with a SAM-registered counterparty |
| Federal Activation Audit deliverable | Run as part of the audit, include findings in the report |
| CEO boot proactive scan | If any flagged entity is within 60 days, surface it in the morning briefing |

## Watch List Format

Read `admin/memory/sam-watch.md`. Format:

```markdown
# SAM Watch List

## HARBOR (always monitored)
| UEI | Entity | Notes |
|-----|--------|-------|
| <HARBOR-UEI> | HARBOR Initiative | Primary registration |

## Active Portfolio (monitored while engagement is active)
| UEI | Entity | Engagement | Added | Notes |
|-----|--------|-----------|-------|-------|
| E4GJKKGMYPY5 | Big Data Rhino | Patrick Parks advisory | 2026-03-24 | Expires 2026-06-02 |
| VUFEAB4T1LD9 | Rock Elm Inc. | Pre-engagement | 2026-03-25 | Expires 2026-08-29 |
| <UEI> | Focus Consulting | Federal Activation Audit | 2026-04-10 | Status TBD |

## Prospects (one-shot lookups, not weekly)
| UEI | Entity | Added | Notes |
|-----|--------|-------|-------|
```

The skill reads the "HARBOR" and "Active Portfolio" sections automatically each run. Prospects are skipped — they're for one-shot lookups when explicitly requested.

## Invocation

```
/sam-monitor                    # Run against the full active watch list
/sam-monitor <UEI>              # One-shot lookup for a single UEI
/sam-monitor --add <UEI>        # Add a UEI to the active client watch list (prompts for entity name + engagement)
/sam-monitor --remove <UEI>     # Remove a UEI from the watch list (engagement closed)
```

## Workflow (Default Run)

### Step 1: Read Watch List

```
Read admin/memory/sam-watch.md
```

Extract all UEIs from "HARBOR" and "Active Portfolio" sections. If file doesn't exist, create it from the template above with HARBOR's UEI populated.

### Step 2: Query SAM.gov for Each UEI

For each UEI, use the SAM.gov Entity Management API:

```bash
curl -s "https://api.sam.gov/entity-information/v3/entities?api_key=$SAM_API_KEY&ueiSAM=<UEI>"
```

The API key is in `~/.zshrc` as `SAM_API_KEY`. Source it before running.

Extract:
- `legalBusinessName`
- `registrationStatus` (Active / Inactive / Submitted / etc.)
- `registrationExpirationDate`
- `purposeOfRegistration`
- `entityStartDate`
- NAICS codes from `naicsList`
- Address from `physicalAddress`

### Step 3: Compute Status Per Entity

For each entity, classify:

| Status | Criteria |
|--------|----------|
| ✅ **Healthy** | Active, expiration > 60 days |
| 🟡 **Approaching renewal** | Active, expiration within 60 days |
| 🔴 **Critical renewal** | Active, expiration within 30 days |
| ❌ **Lapsed** | Inactive OR past expiration date |
| ⚠️ **Anomaly** | API returned no records, or unexpected status |

### Step 4: Cross-Check Anomalies (CRITICAL)

Per ERR-20260328-001, **if status is "Lapsed" or "Anomaly" you MUST cross-check before reporting.**

Cross-check sources:
1. **HigherGov.com** — search for the UEI; if HigherGov shows the entity as active, the SAM API result is wrong
2. **USASpending.gov** — search recent awards; if there are FY2025 or FY2026 awards, the entity is almost certainly active in SAM
3. **The entity's website** — if listed in `HARBOR_portfolio/<client>/`, check for any recent press release or news that suggests active operation

If cross-check disagrees with SAM API, report the discrepancy as `⚠️ DISCREPANCY` and ask Amyn to verify manually. Never report "lapsed" as a fact when there's a discrepancy.

### Step 5: Write Status Report

Output to `admin/memory/sam-status-YYYY-MM-DD.md`:

```markdown
# SAM Watch Report — YYYY-MM-DD

## Summary
- ✅ Healthy: X
- 🟡 Approaching renewal: Y
- 🔴 Critical: Z
- ❌ Lapsed: 0
- ⚠️ Anomalies/discrepancies: 0

## Detail

### HARBOR Initiative (UEI: <UEI>)
- Status: Active
- Expires: 2026-08-29
- Days remaining: 140
- Action: None

### Big Data Rhino (UEI: E4GJKKGMYPY5)
- Status: 🔴 Critical (53 days remaining)
- Expires: 2026-06-02
- Action: Patrick should renew. Flag in next conversation.

### [...]

## Anomalies (if any)
[None / detail of each]
```

### Step 6: Update CEO Memory

If any entity is in 🔴 Critical or 🟡 Approaching renewal state, update `admin/memory/state.md` Deadline Alerts section with the entity name + expiration date. CEO will surface this in next morning briefing.

If any anomaly was found, log it via `/self-improvement` so the cross-check rule keeps being reinforced.

### Step 7: Report Back

Print a one-screen summary:
- Total entities checked
- Healthy / approaching / critical / lapsed counts
- Specific entities needing attention
- Path to full report

## Limitations

- **Requires `SAM_API_KEY` in ~/.zshrc.** Without it, the API call fails with HTTP 401.
- **API rate limits.** SAM.gov public API allows ~1000 calls/day. Not a constraint at current watch list size, but worth noting.
- **No historical tracking.** Each run produces a snapshot. To compare run-over-run, manually diff two `sam-status-*.md` files.
- **NAICS changes are not flagged.** A counterparty may add or remove NAICS codes without changing registration status. Use `/fed-intel` for NAICS-aware analysis.
- **Does not call cell phones.** This is a watchdog skill. It only writes files and alerts CEO. It does not push notifications.

## See Also

- `ERR-20260328-001` — The SAM API false negative incident that prompted this skill
- `/fed-intel` — Full federal intelligence extraction (SAM + USASpending + dashboard) for a specific company
- `/cert-tracker` — Sister skill for SBA certifications (not SAM registrations)
- `ledger-agent.md` — Owns the SAM watch list curation and renewal escalation
- `admin/memory/sam-watch.md` — Source of truth for which UEIs are monitored

## Implementation Notes (For Future Build)

This skill currently relies on:
- `curl` to query SAM.gov API (no SDK required)
- `jq` to parse JSON responses (`brew install jq` if missing)
- A Python script `scripts/check_sam.py` (to be written) that wraps the curl + jq + cross-check logic and outputs the Markdown report

The Python script does not yet exist. Bootstrap order:
1. Write the curl invocation manually for one UEI (HARBOR's own)
2. Verify the JSON response shape
3. Build the parser
4. Add the cross-check logic
5. Wrap in a Python script with `argparse` for CLI use

Expected total dev time: ~2 hours of focused work. Until then, this skill spec serves as the contract; manual runs are acceptable.
