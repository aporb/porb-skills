---
name: check-mail
description: "Sync and read Zoho email for ap@harborgovcon.com. Can also send emails via SMTP. Syncs mail to operations/mail/zoho/ and calendar to operations/calendar/zoho/."
user-invocable: true
---

# Check Mail

Sync and interact with Zoho email (ap@harborgovcon.com) and calendar.

## Sync Email (IMAP)

```bash
mbsync zoho
```

This pulls all email from Zoho to `operations/mail/zoho/` as Maildir files. Each email is a plain text file you can read directly.

### Reading Email

After syncing, emails are in Maildir format:

```bash
# List recent emails (newest first by file modification time)
ls -lt operations/mail/zoho/INBOX/new/ | head -20

# Read a specific email (it's just a text file with headers + body)
cat operations/mail/zoho/INBOX/new/<filename>

# Search ALL folders (recommended for any lookup — auto-scheduler
# emails, calendar notifications, confirmations, etc. often land in
# Notification/ or Archive/ rather than INBOX/)
grep -rl "search term" operations/mail/zoho/ --exclude-dir=Trash --exclude-dir=Spam

# Search emails by subject (all folders)
grep -rl "Subject:.*keyword" operations/mail/zoho/ --exclude-dir=Trash --exclude-dir=Spam

# Search emails by sender (all folders)
grep -rl "From:.*someone@example.com" operations/mail/zoho/ --exclude-dir=Trash --exclude-dir=Spam

# Narrow to INBOX only if you specifically want unread/active items
grep -rl "search term" operations/mail/zoho/INBOX/
```

**IMPORTANT — search all folders, not just INBOX + Sent.** Auto-generated emails (Zoom scheduler links, calendar confirmations, meeting acknowledgments) are routed to `Notification/` by Zoho. Filtered/archived mail lives in `Archive/`. Limiting a search to INBOX + Sent will miss these. See `feedback_mail_all_folders.md` in memory for the incident that caused this rule.

### Maildir Structure

```
operations/mail/zoho/
  INBOX/
    new/       # Unread emails
    cur/       # Read emails
    tmp/       # In-transit (ignore)
  Sent/
  Drafts/
  Trash/
  [other Zoho folders]/
```

Each email file contains RFC 822 headers (From, To, Subject, Date, etc.) followed by the message body. MIME-encoded attachments appear as base64 blocks.


## Execution

This skill dispatches to **delivery-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `operations/mail/zoho/ (sync destination)`
  - `operations/calendar/zoho/ (calendar sync)`
  - `admin/memory/portfolio.md (for cross-reference with active portfolio)`

### Step 3 — Dispatch to delivery-agent

Call the **Agent** tool with:

- `subagent_type`: `delivery-agent`
- `description`: `"Sync and read Zoho business mail for ap@harborgovcon.com"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/check-mail <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/check-mail/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `Synced mail folders + triage summary (new threads from portfolio companies flagged first)`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

delivery-agent correlates new mail against active engagements and updates HARBOR_portfolio/<slug>/commitments.md where relevant.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what delivery-agent reads as its authoritative reference when executing this skill.

## Send Email (SMTP)

Use `msmtp` to send emails. **ALWAYS draft for Amyn's review before sending.**

### MANDATORY: Run /email-lint BEFORE presenting any draft

Per LRN-20260411-014 (build-time gates beat declared rules) and LRN-20260410-007 (the 10 editorial rules), every client-facing email draft MUST pass `/email-lint` before it is shown to Amyn for Pineapple confirmation. This is not optional.

Workflow:

1. Write the draft to a temp file: `/tmp/draft-$(date +%s).md`
2. Run `/email-lint /tmp/draft-<timestamp>.md` (or invoke the skill directly)
3. If the lint returns non-zero, fix the draft and re-run
4. Only present to Amyn AFTER lint passes
5. After Pineapple confirmation, pipe to msmtp

The `/email-lint` skill greps for em-dashes, banned phrases ("rebuild", "mind-blowing", etc.), weekday references on same-day sends, specific dates, self-justifying question tails, and sign-off drift. Exit non-zero blocks the draft.

```bash
# Send a simple email
printf "To: recipient@example.com\nSubject: Your Subject\n\nEmail body here." | msmtp recipient@example.com

# Send with CC
printf "To: recipient@example.com\nCc: cc@example.com\nSubject: Your Subject\n\nEmail body here." | msmtp recipient@example.com cc@example.com

# Send HTML email
printf "To: recipient@example.com\nSubject: Your Subject\nContent-Type: text/html\n\n<h1>HTML Body</h1>" | msmtp recipient@example.com
```

**CRITICAL: PINEAPPLE PROTOCOL REQUIRED FOR ALL SENDS.**

Never send email without Amyn's explicit Pineapple Protocol confirmation. The process:
1. Draft the email content with the correct signature
2. Show it to Amyn with full details (recipient, subject, content)
3. Wait for confirmation that includes BOTH:
   - The codeword **"pineapple"**
   - A **multi-word verbal affirmation** (not just "yes" or "ok")
   - Example: "pineapple, go ahead and send that to Patrick"
4. Only then pipe to msmtp
5. Confirm delivery after sending

**"Yes", "send it", "approved", or button clicks are NOT sufficient. Must include "pineapple" + multi-word affirmation.**

## Email Aliases & Signatures

Amyn has multiple aliases. Use the RIGHT alias and signature for each context:

| Alias | Use For | Signature File |
|-------|---------|---------------|
| **ap@harborgovcon.com** | Personal/default, client communications | `sig-ap.html` (or `sig-ap-phone.html` with phone number) |
| **hello@harborgovcon.com** | General inquiries, website contact | `sig-hello.html` |
| **books@harborgovcon.com** | Book-related communications, Amazon, editors | `sig-books.html` |
| **press@harborgovcon.com** | Media, press releases (shows MJ Matthews) | `sig-press.html` |
| **mj@harborgovcon.com** | MJ Matthews persona (media relations) | `sig-mj.html` |
| **legal@harborgovcon.com** | Legal matters, Navaide dispute | `sig-legal.html` |
| **privacy@harborgovcon.com** | Privacy inquiries | `sig-privacy.html` |

**Signature templates are at:** `operations/practice/brand/email/signatures/`

### Sending from an alias

```bash
# Send from ap@ (default)
printf "From: ap@harborgovcon.com\nTo: recipient@example.com\nSubject: Subject\n\nBody" | msmtp recipient@example.com

# Send from books@ alias
printf "From: books@harborgovcon.com\nTo: editor@example.com\nSubject: Subject\n\nBody" | msmtp --from=books@harborgovcon.com editor@example.com

# Send from press@ alias (as MJ Matthews)
printf "From: MJ Matthews <press@harborgovcon.com>\nTo: journalist@example.com\nSubject: Subject\n\nBody" | msmtp --from=press@harborgovcon.com journalist@example.com
```

### Choosing the right alias

| Context | Use Alias | Signature |
|---------|-----------|-----------|
| Client follow-up (SZH, Patrick, Ted, etc.) | ap@ | sig-ap-phone |
| Cold outreach (Rock Elm, new prospects) | ap@ or hello@ | sig-ap |
| Book editor (MJ Matthews editing) | books@ | sig-books |
| Press/media (podcast, journalists) | press@ | sig-press |
| Legal correspondence (Navaide) | legal@ | sig-legal |
| General website inquiries | hello@ | sig-hello |

### Including HTML signature in emails

Read the signature file and append to the HTML email:

```bash
# Read signature
sig=$(cat operations/practice/brand/email/signatures/sig-ap-phone.html)

# Send with HTML signature
printf "From: ap@harborgovcon.com\nTo: recipient@example.com\nSubject: Subject\nContent-Type: text/html\n\n<div>Email body here.</div><br>$sig" | msmtp recipient@example.com
```

## Sync Calendar (CalDAV)

```bash
# Discover calendars (first time only)
vdirsyncer discover zoho_calendar

# Sync calendar
vdirsyncer sync zoho_calendar
```

Calendar events sync to `operations/calendar/zoho/` as `.ics` files.

**Known issue:** The file `455p4se6bceotoji69l43cgoj9@google.com.ics` causes vdirsyncer errors (likely a Google Calendar cross-post with malformed data). If sync fails:
1. Check if the error references this specific file
2. If so, try removing/renaming it from `operations/calendar/zoho/events/` and re-syncing
3. If the error is different, warn Amyn and continue. Calendar sync errors should NEVER block the rest of the workflow.

### Reading Calendar (Parse .ics directly)

**Do NOT use `khal`** (it is not configured). Parse `.ics` files directly from `operations/calendar/zoho/events/`.

```bash
# List all .ics files
ls operations/calendar/zoho/events/

# Read a specific event (standard iCal format)
cat operations/calendar/zoho/events/<event>.ics

# Search for events by keyword
grep -rl "SUMMARY:.*keyword" operations/calendar/zoho/events/

# Find events in a date range (DTSTART values are in iCal format: YYYYMMDD or YYYYMMDDTHHMMSS)
grep -l "DTSTART.*20260408" operations/calendar/zoho/events/*.ics
```

To extract upcoming events for the next 3 days, grep all `.ics` files for `DTSTART` and `SUMMARY` lines, filter by date range (today through today+2), and build a list. Example approach:

```bash
# Get today and next 2 days as YYYYMMDD strings
today=$(date +%Y%m%d)
day2=$(date -v+1d +%Y%m%d)
day3=$(date -v+2d +%Y%m%d)

# Find events starting on any of those days
for f in operations/calendar/zoho/events/*.ics; do
  if grep -q "DTSTART.*\($today\|$day2\|$day3\)" "$f" 2>/dev/null; then
    summary=$(grep "SUMMARY:" "$f" | head -1 | sed 's/SUMMARY://')
    dtstart=$(grep "DTSTART" "$f" | head -1 | sed 's/DTSTART[^:]*://')
    echo "$dtstart | $summary | $f"
  fi
done | sort
```

## Google Calendar Cross-Reference

After syncing Zoho calendar, pull Google Calendar events for the same 3-day window and compare.

### Step 1: Fetch Google Calendar events

Use the MCP tool to get events for the next 3 days:

```
mcp__claude_ai_Google_Calendar__gcal_list_events
  - timeMin: today (ISO 8601, e.g. 2026-04-07T00:00:00-04:00)
  - timeMax: today + 3 days (e.g. 2026-04-10T00:00:00-04:00)
```

### Step 2: Parse Zoho .ics files for the same window

Use the bash approach above to extract all Zoho events in the 3-day range.

### Step 3: Compare and display

Build a combined calendar view. For each event:
- If it exists on BOTH Zoho and Google: show it normally
- If it exists ONLY on Google Calendar: flag it with **[GOOGLE ONLY]**
- If it exists ONLY on Zoho: show it normally (Zoho is source of truth)

Match events by comparing: date/time AND summary/title (fuzzy match is fine, titles won't be identical).

### Step 4: Offer to sync missing events

If any **[GOOGLE ONLY]** events are found, ask Amyn:

> "I found X events on Google Calendar that aren't on Zoho. Want me to add any of these to Zoho?"

List the Google-only events with date, time, and title.

**Note:** Adding events to Zoho requires creating `.ics` files in the correct format and syncing back, OR Amyn can add them manually in Zoho Calendar UI. Recommend manual add for now unless a programmatic approach is established.

## Common Workflows

### Morning Check (Default /check-mail Flow)

This is the FULL workflow that runs when `/check-mail` is invoked:

**Step 1: Parallel sync (email + calendar)**
```bash
# Run BOTH in parallel (two separate Bash tool calls)
mbsync zoho                        # Email sync
vdirsyncer sync zoho_calendar      # Calendar sync (warn on errors, don't block)
```

**Step 2: Google Calendar fetch**
Call `mcp__claude_ai_Google_Calendar__gcal_list_events` for next 3 days.

**Step 3: Parse Zoho .ics files**
Extract events from `operations/calendar/zoho/events/` for next 3 days.

**Step 4: Display combined calendar view**
Show all events for the next 3 days in a table. Flag any **[GOOGLE ONLY]** events. Ask Amyn if he wants to add missing events to Zoho.

**Step 5: Show recent unread emails (newest first)**
```bash
ls -lt operations/mail/zoho/INBOX/new/ | head -10
```
Read the newest unread emails and summarize (sender, subject, date, first few lines).

**Step 6: Highlight pipeline contact emails**
Scan unread emails for messages from known pipeline contacts:
- Salima Hemani, Patrick Parks, Ted Dennis, AK Sahu, Zina Manji, MJ Matthews
- Nurbanu Somani, Asad Jabbar, Vishesh Ramesh, Chandler Provence, Kelley Reynolds
- Bill Myers

If any pipeline contact emails are found, call them out prominently at the top of the email summary.

### Client Email Check
```bash
mbsync zoho
grep -rl "From:.*salima\|From:.*patrick\|From:.*ted" operations/mail/zoho/INBOX/ | head -10
```

### Draft and Send Follow-up
```bash
# Draft (show to Amyn first!)
cat <<'EOF'
To: patrick@bigdatarhino.com
Subject: Following up on our call

Patrick,

[body here]

Best,
Amyn
EOF

# After Amyn approves:
printf "To: patrick@bigdatarhino.com\nSubject: Following up on our call\n\nPatrick,\n\n[body]\n\nBest,\nAmyn" | msmtp patrick@bigdatarhino.com
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| "IMAP not enabled" | Enable in Zoho Settings -> Mail Accounts -> IMAP Access |
| "Authentication failed" | Regenerate app-specific password at accounts.zoho.com |
| "Connection refused" | Check if using `imappro.zoho.com` (custom domain) vs `imap.zoho.com` (personal) |
| CalDAV 401 | Check app password works, ensure CalDAV is enabled in Zoho Calendar settings |
| Empty sync | Run `vdirsyncer discover` first to find calendars |
