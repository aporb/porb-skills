---

name: ceo-briefing
description: One-off HTML snapshots still work for archival purposes.
user-invocable: true
---

# /ceo-briefing (deprecated 2026-04-30)

Routine briefing reads happen via the **life-os** dashboard:
**http://localhost:9876/**

For one-off snapshot HTML (sharing, archiving), the renderer still works:

```bash
node .claude/skills/ceo-briefing/render.mjs <data.json> <template.html> <out.html>
```

After 2026-05-14, this skill is deleted and the snapshot path moves to
life-os. See `docs/superpowers/specs/2026-04-30-life-os-phase1-design.md`.

---

(legacy playbook below preserved for archival snapshot generation)


# CEO Briefing

Generate a business briefing for HARBOR. One HTML file written to `admin/briefings/`. Short, scannable, signal-dense. Built to be read in 2 to 5 minutes, not 20.

## Architecture

Claude's job is to **gather data into a JSON payload**, then call `render.mjs` to stamp `template.html`. HTML assembly is deterministic and mechanical. Editorial rules and cross-portfolio leak checks are enforced at build time by the renderer, not vibes.

```
state.md + portfolio.md + growth.md         /check-mail primitives       git log
commitments.md + sam-watch.md + certs.md         ->       briefing-data.json       ->       render.mjs       ->       briefing-YYYY-MM-DD-variant.html
ledger.md + ndas-ledger.md                Zoho .ics files
```

## When to Run

| Invocation | Result |
|------------|--------|
| `/ceo-briefing` (no arg) | Auto-detect variant from local hour: before 11:00 = morning, 11:00 to 17:00 = midday, 17:00 onward = evening |
| `/ceo-briefing morning` | Force morning variant |
| `/ceo-briefing evening` | Force evening variant |
| `/ceo-briefing weekly` | Force weekly variant (Investor Lens included) |
| `/ceo-briefing midday` | Force midday variant (same template as evening, different header) |


## Execution (CEO-direct)

This skill is **CEO-owned** and does NOT dispatch to a specialist agent. See `.claude/skills/SKILL-PATTERN.md` Tier C.

**Rationale:** The briefing IS the CEO speaking to Amyn. Delegating composition would mean an agent writing in the CEO's voice — the whole point is CEO synthesis of state/memory/mail/calendar/git into the daily frame. CEO may invoke researcher for a narrow fresh-signal check on a specific prospect inside the briefing, but composition stays CEO.

The CEO executes the playbook below directly. The CEO may spawn narrow sub-agents (typically `researcher` via the `Agent` tool) for specific sub-tasks — e.g., a fresh-signal check on a named prospect — but composition, framing, and final output stay CEO-authored.

---

The detailed playbook below is what the CEO reads to execute this skill.

## Variants at a Glance

Sizes below are **total file size**. The CSS shell from `template.html` is ~14 KB fixed overhead. Subtract that for the actual content budget.

| Variant | Target Total | Content Budget | Purpose | Signature Section |
|---------|--------------|----------------|---------|-------------------|
| **Morning** | 25-32 KB | 11-18 KB | Pre-load the day: calendar, overnight mail, pipeline heat, alerts | Today's Calendar |
| **Midday** | 25-32 KB | 11-18 KB | Re-center mid-day: what moved this morning, afternoon plan | Since Morning |
| **Evening** | 32-42 KB | 18-28 KB | Wrap the day: wins, decisions, tomorrow | Today's Wins |
| **Weekly** | 42-55 KB | 28-41 KB | Strategic review: traction, capital allocation | Investor Lens (Atif Kanji framework) |

**Hard cap:** if any variant generates more than 1.4x its target size, the skill prints a warning and suggests trimming.

Line count is a better proxy than raw byte size. Target line counts:

- Morning / midday: 600-900 lines
- Evening: 900-1200 lines
- Weekly: 1200-1500 lines

Anything over 1600 lines on a daily briefing is a trim signal.

See `REFERENCE.md` for the full section specs, data source mappings, editorial rules, and the worked example.

## Step-by-Step Workflow

### Step 0 | Orient

```bash
date
```

Trust `date` output over anything in state.md. If state says "Monday" and `date` says Tuesday, `date` wins.

Detect the variant from hour (or accept user arg). Set `VARIANT`, `DATE` (YYYY-MM-DD), `FILENAME` (`briefing-${DATE}-${VARIANT}.html`).

### Step 1 | Snapshot state and pull memory (parallel)

Take a snapshot first so in-flight memory edits do not race the briefing build:

```bash
cp admin/memory/state.md /tmp/state-$(date +%s).md
```

Then read these in parallel:

```
Read admin/memory/state.md           (priorities, decisions, calendar, session summary)
Read admin/memory/portfolio.md         (priority matrix + client details for each active engagement)
Read admin/memory/growth.md          (funnel stages, campaign cadence)
Read admin/memory/sam-watch.md       (UEI watch list)
Read admin/memory/certs.md           (cert/compliance watch list)
Read admin/memory/portfolio-aliases.md  (cross-portfolio leak grep source)
```

For weekly variant also read:

```
Read admin/memory/books.md
Read admin/memory/website.md
Read .learnings/LEARNINGS.md         (last 20 entries for themes)
```

### Step 2 | Sync mail (parallel with Step 1)

```bash
mbsync zoho
```

Window the mail scan by variant. On first run, the anchor file `admin/briefings/.last-briefing-timestamp` does not exist; fall back to "today 00:00" in the local timezone:

```bash
ANCHOR="admin/briefings/.last-briefing-timestamp"
if [ ! -f "$ANCHOR" ]; then
  TODAY_START=$(date -v0H -v0M -v0S +%s 2>/dev/null || date -d "today 00:00:00" +%s)
  touch -t "$(date -v0H -v0M -v0S +%Y%m%d%H%M 2>/dev/null || date -d '@'$TODAY_START +%Y%m%d%H%M)" "$ANCHOR"
fi
```

Then:

- **Morning:** parse `operations/mail/zoho/INBOX/new/` for unread + scan `INBOX/cur/` for items since `$ANCHOR`. Summarize by sender, flag any pipeline contacts.
- **Evening:** scan `Sent/cur/` for today's outbound (grep Date header). List recipients and subjects.
- **Weekly:** scan both INBOX and Sent for the last 7 days and bucket by client.

Use the `/check-mail` skill primitives documented in `.claude/skills/check-mail/SKILL.md`. Search all folders, not just INBOX. Auto-scheduler mail lives in `Notification/`.

### Step 3 | Read calendar

Parse `.ics` files in `operations/calendar/zoho/events/` with DTSTART in the window:

- Morning: today + next 3 days
- Midday: rest of today + next 2 days
- Evening: tomorrow + next 3 days
- Weekly: next 14 days

If calendar is sparse (fewer than 3 events), also pull from state.md Upcoming Calendar table.

**Never use Google Calendar MCP for operations.** Zoho is the source of truth. (LRN-20260406-001)

### Step 4 | Check watch lists

Read `admin/memory/sam-watch.md` and `admin/memory/certs.md`. Both files are bootstrapped (see REFERENCE.md). For each row, compute `days_until_expiry = expiry - today` and bucket into RED (within 14d), YELLOW (15-60d), BLUE (61-90d). Drop anything past 90d from daily briefings.

**Hardcoded tax cadence ripple:** regardless of the state of any file, the DEAD section for every daily briefing must also check whether any quarterly 1040-ES deadline is within 14 days of `$DATE`. Q1 Apr 15, Q2 Jun 15, Q3 Sep 15, Q4 Jan 15. Today (Apr 11) Q1 Apr 15 is 4 days out, so a RED row must appear: "Q1 2026 federal 1040-ES".

**Tax-payment suppression:** before emitting a tax row, read `admin/memory/tax-payments.md`. If the quarter is marked `Status = ✅ PAID`, suppress the row. Only `⏳ Upcoming` quarters within 14 days fire as RED.

### Step 5 | Read commitments ledgers

For each active portfolio listed in the PIPE section, read `HARBOR_portfolio/<slug>/commitments.md`. If the file does not exist, bootstrap an empty one with the two tables (Open, Fulfilled) and a "No commitments logged" placeholder so the file exists for next run. Then pull all rows where `Status = OPEN` and the `Owed By` / `Due` / `Days in state` are populated.

Feed these rows into the COM section data payload.

### Step 6 | Git activity (evening + weekly only)

```bash
# Evening: today's commits
git log --since="${DATE} 00:00" --until="${DATE} 23:59" --oneline --no-merges

# Weekly: last 7 days
git log --since="7 days ago" --oneline --no-merges | head -50
```

Filter noise: strip commits that are pure chore/docs if the list exceeds 15 items. Keep feat/fix/data.

### Step 7 | Compute staleness (header-only regex)

For each active client in the Priority Matrix, compute "days since last contact". Use a header-only regex; raw text like `<email>` inside a quoted paragraph should not match:

```bash
EMAIL="ak@braventsystems.com"
grep -l -E "^(To|From|Cc|Bcc):.*<${EMAIL}>" \
  operations/mail/zoho/Sent/cur/ \
  operations/mail/zoho/INBOX/cur/ 2>/dev/null
```

For each hit, parse `^Date:` and take the max. Compare to today to get days delta.

Flag any HIGH priority client greater than 5 days stale on an active deal. Check state.md decision log before flagging to avoid re-surfacing already-handled "silence" that was intentional.

### Step 8 | Assemble briefing-data.json and render

Build `briefing-data.json` in memory with the shape documented in `render.mjs` (see the JSDoc at the top). Pass it to the renderer:

```bash
TMP=$(mktemp -t briefing-data-XXXXXX.json)
# ... write JSON to $TMP via a Write tool call ...
node .claude/skills/ceo-briefing/render.mjs \
  "$TMP" \
  .claude/skills/ceo-briefing/template.html \
  "admin/briefings/briefing-${DATE}-${VARIANT}.html"
```

The renderer will:

1. Load the template and inject theme-FOUC pre-paint script (idempotent)
2. Stamp all sections in canonical order (ALERT, CAL, TOMR, MAIL, PIPE, COM, CONT, WIN, DEC, BLOCK, PLAN, DEAD, INV, REV, LEARN, CAD, PERS)
3. Strip unused placeholders
4. Run editorial lint against the final HTML (banned phrases, em-dashes, en-dashes, double-hyphens, &mdash;, &ndash;)
5. Run cross-portfolio leak check against each PIPE client card using `admin/memory/portfolio-aliases.md`
6. Run dedupe warning: any client alias appearing 3+ times inside a non-PIPE section is a warning
7. Exit non-zero if editorial lint fails OR if `editorial.leak_strict` is true and a leak was found

If the renderer exits non-zero, Claude **must not** write the file. Fix the data payload (usually by compressing or renaming), re-render, verify pass.

### Step 8.5 | Write anchor timestamp

```bash
touch admin/briefings/.last-briefing-timestamp
```

Do this only AFTER the file was successfully written and linted. The next briefing uses this as the mail scan anchor.

### Step 9 | Size guard

```bash
F=$(ls -t admin/briefings/briefing-*.html | head -1)
L=$(wc -l < "$F")
[ $L -gt 1600 ] && echo "OVERSIZE: $F ($L lines)"
```

No shell variables persist across Claude tool calls. The one-liner above looks up the most recent briefing dynamically. If it prints OVERSIZE, trim the data payload per the Trimming Playbook in REFERENCE.md and re-render.

### Step 10 | Terminal summary

Print 8 lines to stdout:

```
CEO Briefing | {VARIANT} | {DATE}
File: admin/briefings/briefing-{DATE}-{VARIANT}.html

{1 line: top-priority alert if any}
{1 line: today's calendar count + next event}
{1 line: pipeline headline (number warm, number stalled)}
{1 line: deadline within 7 days if any}
{1 line: what moved (evening) or what's queued (morning)}
{1 line: open the file command}
```

Do NOT auto-open the file. Amyn opens it himself.

## Editorial Rules (hard gate, enforced by render.mjs)

The renderer scans the final HTML. These rules BLOCK the build, not warn.

1. **No em dashes, en dashes, or double hyphens.** Includes literal `\u2014`, `\u2013`, ` -- `, `&mdash;`, `&ndash;`. Use ` | `, ` to `, ` through `, or line breaks.
2. **Banned phrases:** `rebuild`, `rebuilt`, `single sharpest`, `existential anchor`, `mind-blowing`, `mind blowing`, `unprecedented`, `groundbreaking`. These are AI-padding language and superlative cliches. Rule aligned with email-lint (feedback_email_editorial_patterns.md).
3. **Light mode default.** The pre-paint script in `<head>` keeps theme sync before first pixel. No FOUC.
4. **Amyn, not Amy.** Hard gate (editorial phrase list).
5. **HARBOR Initiative** for internal briefings, consistent within one file.
6. **No self-referential "Session Stats" or "Learnings Captured This Session" sections.** Business signal only.
7. **Dedupe.** Each client has ONE home (their PIPE card). References elsewhere (Calendar, Deadlines, Decisions, Alerts) are name-only, not full restatements. The renderer warns if an alias appears 3+ times outside PIPE.
8. **Cross-client leak check.** If a section is scoped to a specific client (has a `client_slug` in the data payload), aliases of OTHER clients must not appear inside it. Enforced by render.mjs against `portfolio-aliases.md`.
9. **Lead with alerts, not KPIs.**
10. **Evening briefings look backward, morning briefings look forward.** No cross-contamination.
11. **Collapse everything below the fold.** First 3 sections open, rest closed.
12. **Empty sections collapse to a single chip row or omit entirely.** MAIL saying "nothing happened" across 23 lines is anti-signal.

## Error Handling

| Failure | Fallback |
|---------|----------|
| `mbsync zoho` fails | Show "Mail sync failed, last sync {mtime of INBOX dir}" in the MAIL section. Do not abort. |
| Calendar dir empty | Show "Zoho calendar empty, pulling from state.md" and fall through. |
| state.md greater than 10k tokens | Use offset reading. Never skip state.md. |
| portfolio.md greater than 10k tokens | Read Priority Matrix first (offset 1, limit 30), then read client blocks on-demand only for clients flagged in the Priority Matrix. |
| Missing `commitments.md` for an active client | Bootstrap an empty one in place and continue. |
| Missing `sam-watch.md` or `certs.md` | Treat as critical. These are bootstrapped. If missing, log the failure to `.learnings/LEARNINGS.md` and fall through to portfolio.md scraping. |
| Renderer editorial lint fails | Do NOT write the file. Fix the data payload, re-render. |
| Cross-client leak detected | Block the build if `editorial.leak_strict = true`. Otherwise warn. |
| Supabase / Amazon rank fetch fails | Omit the metric. Do NOT show "offline" placeholders. |

## Output Contract

| Item | Location |
|------|----------|
| HTML briefing | `admin/briefings/briefing-${DATE}-${VARIANT}.html` |
| Terminal summary | stdout, 8 lines |
| Anchor timestamp | `admin/briefings/.last-briefing-timestamp` (touched after successful write) |
| Self-improvement log | Only if a data source failed, log the failure to `.learnings/LEARNINGS.md` |

## Companion Files

- `REFERENCE.md` | full section specs, data source mappings, editorial rules, worked example
- `template.html` | HTML shell with CSS, JS, and section placeholders
- `render.mjs` | Deterministic Node renderer (zero deps)
- `fixtures/briefing-data-example.json` | Reference data payload shape for tests
- `CHANGELOG.md` | Dated log of what changed in each iteration

## Smoke Test

```bash
node .claude/skills/ceo-briefing/render.mjs --smoke
```

Should print `SMOKE OK: rendered <N> bytes, <M> lines.` and exit 0.

## Known Follow-ups (P2, deferred from this iteration)

These are acknowledged gaps that will be addressed in the next revision. Not blockers for daily use.

1. **SIG (External Signals) section** with a hard "never invent news items" rule. Would subscribe to real RSS feeds.
2. **Procurement forecast cross-reference** from `operations/reference/procurement-forecasts/` for weekly briefings.
3. **TECH (Platform Health) section** for harbor-website uptime, deploy status, open issues.
4. **Pineapple queue section** listing outbound drafts awaiting Pineapple Protocol confirmation.
5. **RCP (Recompete Calendar) portfolio view** for weekly briefings.
6. **CAT (Catalog Velocity) sub-block** tracking productized engagement pipeline.
7. **Research delta surfacing** from new files in `HARBOR_portfolio/`.
8. **Competitive intel layer.**
9. **COMPLIANCE aging rule** (30d yellow, 60d red) for stuck entity/compliance blockers.
10. **CRD interim milestones** nested inside PERS.
11. **HTML validation gate** (tidy / html-validate).
12. **Fixture / golden test** for the builder script beyond the smoke test.
13. **Per-client meeting prep packet in CAL** pulling from `05-meetings/*.md`.
14. **NDA lifecycle fields on PIPE cards** (sent, days-in-state, yellow/red rules).
15. **Per-section "sourced from" footers** listing memory file + line anchor for every factual claim. (Partially implemented in P1; richer version pending.)

---

## /shrink-wrap v2 orchestration integration (added 2026-05-26)

The /ceo-briefing skill is the CEO agent's daily synthesis tool. With /shrink-wrap v2 live, the briefing now includes a portfolio-orchestration layer pulling state from past /shrink-wrap runs.

### New briefing section: /shrink-wrap activity

Within the CEO briefing's portfolio section, surface:
- Any /shrink-wrap runs completed in the past 7 days (read from `admin/memory/state.md` decisions log entries matching `| /shrink-wrap |`)
- Each run's verdict (proceed / proceed-with-conditions / drop / halt-no-candidates) + portfolio member + lens
- Open conditions or kill criteria that have aged > expected window
- Any halt conditions that need user attention (e.g., Pre-H gate failed; Ch 7 returned DELAY; Ch 13 stress test failed)

### Briefing-format addition

In the briefing HTML output, add a row to the priorities table for any portfolio member with an OPEN /shrink-wrap finding:

| Priority | Member | /shrink-wrap state | Next action |
|---|---|---|---|
| <int> | <slug> | <verdict>, run <date> | <30/60/90 day next step from decision memo> |

### Cross-references

- `admin/memory/book-orchestration-v2.md` — canonical pointer
- `admin/memory/state.md` decisions log — appended to by orchestrator after every run
- `HARBOR_portfolio/<member>/commitments.md` — orchestrator appends post-run commitment entry

### What ceo-briefing does NOT do

- Run /shrink-wrap itself (the CEO agent decides when to dispatch, not the briefing skill)
- Replicate the decision memo's content (briefing surfaces summary + next action only; full memo is the artifact path)
