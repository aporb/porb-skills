---
name: cert-tracker
description: Track expiration dates for certifications, registrations, and credentials (8(a), SDVOSB, WOSB, HUBZone, GSA MAS, CMMC, FedRAMP, CISA, Marine Reserve status, contract end-dates). Reads admin/memory/certs.md, alerts on anything within 60 days. Distinct from /sam-monitor which is SAM.gov entity registration only.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: haiku
user-invocable: true
---

# /cert-tracker — Certification & Credential Expiration Monitor

**Why this exists:** A solo operator can lose more revenue from a lapsed cert than from a missed deal. The 8(a) suspension that hit Focus Consulting in January (and was discovered Apr 10 during contract archaeology) is the cautionary tale. SBA 8(a), SDVOSB, GSA MAS, CMMC, and FedRAMP all have hard expiration dates and slow renewal cycles. Miss the window and the practice loses access to a vehicle.

This skill is the calendar for that risk. It does NOT renew anything (manual process). It does flag upcoming expirations early enough to act.

## What This Skill Tracks

| Category | Examples |
|----------|----------|
| **SBA certifications** | 8(a) (9-year clock), SDVOSB (annual SBA VetCert recertification), WOSB, HUBZone |
| **GSA / federal vehicles** | GSA MAS contract end-date, BPA expirations, IDIQ task order PoPs |
| **Compliance** | CMMC level 2 cert, FedRAMP authorization, ISO 27001, SOC 2 |
| **Personal credentials** | CISA, CISSP, Security+, PMP, Shipley Business Winning |
| **Military** | USMC Reserve obligation status, drill/AT requirements |
| **Insurance** | E&O, general liability, cyber liability |
| **Domain / hosting** | harborgovcon.com renewal, Vercel team plan, Supabase Pro |
| **Subscriptions critical to ops** | Resend, Stripe live mode, Zoho mail, OpenAI API quota |


## Execution

This skill dispatches to **ledger-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `admin/memory/certs.md (source of truth)`
  - `admin/memory/state.md (prior context)`

### Step 3 — Dispatch to ledger-agent

Call the **Agent** tool with:

- `subagent_type`: `ledger-agent`
- `description`: `"Track expiration of certifications, registrations, and credentials"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/cert-tracker <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/cert-tracker/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `Updated admin/memory/certs.md with current days-to-expiry + any alerts for the CEO briefing`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

Surface 60-day warnings in the next CEO briefing.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what ledger-agent reads as its authoritative reference when executing this skill.

## What This Skill Does NOT Track

- SAM.gov entity registration (use `/sam-monitor`)
- NDA countersignature deadlines (lives in `<client>/commitments.md`, owned by delivery-agent)
- Tax filing deadlines (separate quarterly skill, future work)
- Client engagement end-dates (lives in `<client>/engagement.md`)

## When to Run

| Trigger | Action |
|---------|--------|
| Weekly cron | Default. Run every Monday morning. |
| New cert obtained | Add entry to certs.md, then run once to confirm |
| Federal Activation Audit (client engagement) | Run for the client's certs as part of the audit |
| CEO morning briefing | If anything is within 60 days, surface it |
| Pre-engagement | Before signing any SOW that depends on a cert (e.g., "GSA MAS" engagement requires GSA active) |

## Watch List Format

Read `admin/memory/certs.md`. Format:

```markdown
# Certifications & Credentials Watch List

## HARBOR Initiative

| Category | Cert | Issued | Expires | Renewal Lead Time | Notes |
|----------|------|--------|---------|-------------------|-------|
| Domain | harborgovcon.com | 2025-12-15 | 2026-12-15 | 2 weeks | Auto-renew on |
| Hosting | Vercel Pro | rolling | rolling | n/a | Monthly billing |
| Email | Resend Pro | rolling | rolling | n/a | Monthly billing |

## Amyn Personal

| Category | Cert | Issued | Expires | Renewal Lead Time | Notes |
|----------|------|--------|---------|-------------------|-------|
| Professional | CISA | 2024-XX-XX | 2027-XX-XX | 3 months | CPE hours required |
| Military | USMC Reserve IRR | 2023-08-XX | 2031-08-XX | n/a | Contracted obligation |

## Active Portfolio (monitored while engagement is active)

| Client | Cert | Issued | Expires | Status | Engagement |
|--------|------|--------|---------|--------|-----------|
| Focus Consulting | 8(a) | 2018-XX-XX | 2027-XX-XX | SUSPENDED Jan 2026 batch | Federal Activation Audit |
| Focus Consulting | GSA MAS | XXXX-XX-XX | 2026-04-19 | LAPSING | Federal Activation Audit |
| Big Data Rhino | SDVOSB | XXXX-XX-XX | XXXX-XX-XX | Active | Patrick advisory |
| Rock Elm | HUBZone | XXXX-XX-XX | XXXX-XX-XX | Active | Pre-engagement |
| Rock Elm | TS FCL | XXXX-XX-XX | XXXX-XX-XX | Active | Pre-engagement |
```

The skill reads HARBOR + Amyn Personal + Active Portfolio sections. Each row needs: category, cert name, expiration date, renewal lead time, notes.

## Invocation

```
/cert-tracker                       # Default: scan all active certs
/cert-tracker --client <slug>       # Scan only one client's certs
/cert-tracker --add                 # Add a new cert entry (interactive)
/cert-tracker --export              # Export as JSON for dashboard ingestion
```

## Workflow

### Step 1: Read certs.md

```
Read admin/memory/certs.md
```

If file doesn't exist, create it from the template above and prompt Amyn to populate HARBOR + personal sections via AskUserQuestion. Skip client section until clients are explicitly added.

### Step 2: Compute Status Per Cert

For each row in the watch list, compute days-until-expiration:

```python
# Pseudocode
today = date.today()
for cert in certs:
    if cert.expires == "rolling":
        continue  # Skip subscription-style entries
    days = (cert.expires - today).days
    lead_time_days = parse_lead_time(cert.renewal_lead_time)

    if days < 0:
        cert.status = "❌ LAPSED"
    elif days < 30:
        cert.status = "🔴 CRITICAL"
    elif days < 60:
        cert.status = "🟡 APPROACHING"
    elif days < lead_time_days:
        cert.status = "🟢 RENEWAL WINDOW"
    else:
        cert.status = "✅ HEALTHY"
```

### Step 3: Cross-Check Suspensions

For 8(a), SDVOSB, WOSB, HUBZone — these can be SUSPENDED separately from expired. SBA enforces eligibility recertification annually. If `notes` contains "SUSPENDED" or "DECERTIFIED", treat as effectively lapsed regardless of expiration date.

For SDVOSB specifically, per LRN-20260406-008, verify against SBA VetCert (https://veterans.certify.sba.gov/) — website "SDVOC" badges may be self-designated, not SBA-verified.

### Step 4: Write Report

Output to `admin/memory/cert-status-YYYY-MM-DD.md`:

```markdown
# Certification Watch Report — YYYY-MM-DD

## Summary
- ✅ Healthy: X
- 🟢 Renewal window open: Y
- 🟡 Approaching (<60 days): Z
- 🔴 Critical (<30 days): W
- ❌ Lapsed: V
- ⚠️ Suspensions: U

## HARBOR Initiative
| Cert | Status | Expires | Days | Action |
|------|--------|---------|------|--------|

## Amyn Personal
| Cert | Status | Expires | Days | Action |
|------|--------|---------|------|--------|

## Active Client Certs
### Focus Consulting
| Cert | Status | Expires | Days | Action |
|------|--------|---------|------|--------|
| 8(a) | ⚠️ SUSPENDED | 2027-XX-XX | — | Recovery path TBD via Federal Activation Audit |
| GSA MAS | 🔴 CRITICAL | 2026-04-19 | 8 | Renew NOW or lose vehicle |

### [other clients]

## Recommended Actions (priority-ordered)
1. <Most urgent action>
2. <Next>
3. <Next>
```

### Step 5: Update CEO Memory

If anything is in 🔴 CRITICAL or ❌ LAPSED state, append to `admin/memory/state.md` Deadline Alerts section. Format:

```markdown
- 🔴 [Cert name] expires YYYY-MM-DD (X days) — [action required]
```

CEO surfaces these in next morning briefing.

### Step 6: Print Summary

Print one-screen output to user:
- Total certs tracked
- Status counts
- Top 3 actions needed
- Path to full report

## Edge Cases

### Rolling subscriptions
Entries with `expires: rolling` are skipped — they're monthly billing, not real expirations. They're listed in certs.md for visibility, not for alerting.

### SBA suspensions
A cert can be SUSPENDED without being expired. Read the `notes` column for `SUSPENDED`, `DECERTIFIED`, `LAPSED`, or `REVOKED` strings — these override the date-based status.

### Lead time vs. expiration
Some certs have a renewal window that opens before expiration (e.g., GSA MAS lets you start renewal 240 days before option exercise). The `Renewal Lead Time` column captures this. If the window is open and renewal hasn't started, status is 🟢 RENEWAL WINDOW (not yet urgent, but actionable).

### Self-attested vs. verified
For SDVOSB, only count it as active if it's verified in SBA VetCert. Website badges or SAM.gov self-designation are NOT sufficient. (LRN-20260406-008)

## Limitations

- **No external API integration.** This skill reads a manually-maintained Markdown file. It does NOT call SBA, GSA, or any cert authority. The watch list is only as accurate as the human who updates it.
- **Does not trigger renewals.** Renewal is a manual process (forms, fees, narratives). This skill only alerts.
- **Does not predict approval.** A renewal application's approval rate depends on the agency, the applicant's compliance history, and luck. This skill assumes "if you submit on time, you'll get it."
- **Does not handle CPE/CEU tracking.** Certifications like CISA require continuing-education hours. Tracking those is a separate, future skill.

## See Also

- `/sam-monitor` — Sister skill for SAM.gov entity registration (NOT certs)
- `LRN-20260406-008` — SDVOSB self-designation vs. SBA VetCert verification
- `admin/memory/certs.md` — Source of truth for the watch list
- `ledger-agent.md` — Owns this skill's invocation cadence and surfaces critical alerts to CEO
- `HARBOR_portfolio/focus_zambrano/` — Reference: the 8(a) suspension that prompted this skill

## Implementation Notes

This skill is currently a Markdown-only spec. The Python script to compute status from certs.md does not yet exist. Bootstrap order:

1. Populate `admin/memory/certs.md` with HARBOR + Amyn + active client certs (manual one-time)
2. Write `scripts/check_certs.py` that reads certs.md, parses dates, computes status, writes report
3. Add cron entry: `0 9 * * 1 cd <repo> && /cert-tracker` (Monday 9am weekly)
4. Wire ledger-agent to read the latest cert-status report on boot

Until the Python script exists, the skill spec serves as the contract; manual cert audits are acceptable.
