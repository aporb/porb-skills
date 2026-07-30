---
name: google
description: "Google Workspace for amyn@porbanderwala.com (personal). Gmail, Calendar, Drive, Sheets, Docs via gws CLI. Separate from /check-mail (Zoho/business)."
user-invocable: true
---

# Google Workspace

Personal Google account access for **amyn@porbanderwala.com** via the `gws` CLI.

This is the **personal** channel. Business email (ap@harborgovcon.com) uses `/check-mail` (Zoho).

## Account & Auth

- **Account:** amyn@porbanderwala.com
- **CLI:** `gws` v0.22.5+ (Homebrew)
- **Config:** `~/.config/gws/` (credentials encrypted AES-256-GCM in macOS Keychain)
- **GCP Project:** `fluent-plate-438301-t0`
- **Scopes:** gmail, drive, calendar, sheets, docs, cloud-platform

If auth expires, re-run: `gws auth login -s gmail,drive,calendar,sheets,docs`

## Default Flow (no arguments)

When `/google` is invoked without arguments, run the **full morning triage**:

### Step 1: Gmail Triage

```bash
gws gmail +triage --max 20
```

Summarize unread personal email: sender, subject, date. Highlight anything from known contacts (family, community, professional network).

### Step 2: Calendar Agenda (3 days)

```bash
gws calendar +agenda --days 3 --timezone America/Chicago
```

Show upcoming events. Then cross-reference against Zoho calendar:

```bash
# Parse Zoho .ics files for the same 3-day window
today=$(date +%Y%m%d)
day2=$(date -v+1d +%Y%m%d)
day3=$(date -v+2d +%Y%m%d)

for f in operations/calendar/zoho/events/*.ics; do
  if grep -q "DTSTART.*\($today\|$day2\|$day3\)" "$f" 2>/dev/null; then
    summary=$(grep "SUMMARY:" "$f" | head -1 | sed 's/SUMMARY://')
    dtstart=$(grep "DTSTART" "$f" | head -1 | sed 's/DTSTART[^:]*://')
    echo "$dtstart | $summary"
  fi
done | sort
```

Build a combined calendar view:
- Events on **both** Zoho and Google: show normally
- Events **only on Google**: flag with **[GOOGLE ONLY]**
- Events **only on Zoho**: flag with **[ZOHO ONLY]**

**Zoho remains the source of truth for business scheduling.** Google Calendar is the personal/secondary calendar.

If any events appear to conflict (overlapping times across both calendars), flag them prominently.

### Step 3: Recent Drive Activity

```bash
gws drive files list --params '{"pageSize": 10, "orderBy": "modifiedTime desc", "fields": "files(id,name,mimeType,modifiedTime,owners)"}'
```

Show recently modified files (name, type, last modified).

---

## Gmail Operations

### Triage (read unread)

```bash
gws gmail +triage --max 20
gws gmail +triage --query "from:someone@example.com"
gws gmail +triage --query "is:unread newer_than:2d"
```

### Read a specific message

```bash
gws gmail +read --id <MESSAGE_ID> --headers
```

### Search

```bash
gws gmail users messages list --params '{"userId": "me", "q": "from:boss subject:urgent", "maxResults": 10}'
```

Use standard Gmail search syntax for the `q` parameter.

### Send (PINEAPPLE PROTOCOL REQUIRED)

**CRITICAL: All outbound email from this personal account requires full Pineapple Protocol.**

The process:
1. Draft the email and present to Amyn with full details (recipient, subject, body)
2. Wait for confirmation that includes BOTH:
   - The codeword **"pineapple"**
   - A **multi-word verbal affirmation** (not just "yes" or "ok")
3. Only then execute the send

```bash
# Send
gws gmail +send --to recipient@example.com --subject "Subject" --body "Body text"

# Send HTML
gws gmail +send --to recipient@example.com --subject "Subject" --body "<p>HTML body</p>" --html

# With CC/BCC
gws gmail +send --to main@example.com --cc copy@example.com --subject "Subject" --body "Body"

# With attachment
gws gmail +send --to recipient@example.com --subject "Subject" --body "See attached" --attach ./file.pdf

# Save as draft (no Pineapple needed for drafts)
gws gmail +send --draft --to recipient@example.com --subject "Subject" --body "Body"
```

### Reply (PINEAPPLE PROTOCOL REQUIRED)

```bash
gws gmail +reply --message-id <ID> --body "Reply text"
gws gmail +reply-all --message-id <ID> --body "Reply text"
```

### Forward (PINEAPPLE PROTOCOL REQUIRED)

```bash
gws gmail +forward --message-id <ID> --to newrecipient@example.com --body "FYI"
```

---

## Calendar Operations

### View agenda

```bash
# Today
gws calendar +agenda --today --timezone America/Chicago

# This week
gws calendar +agenda --week --timezone America/Chicago

# Next N days
gws calendar +agenda --days 7 --timezone America/Chicago
```

### Create event

For personal-only events (no attendees), create directly:

```bash
gws calendar +insert \
  --summary "Event name" \
  --start "2026-04-15T10:00:00-05:00" \
  --end "2026-04-15T11:00:00-05:00" \
  --location "Place" \
  --description "Notes"
```

For events with attendees: **PINEAPPLE PROTOCOL REQUIRED** (sends invitations).

```bash
gws calendar +insert \
  --summary "Meeting" \
  --start "2026-04-15T10:00:00-05:00" \
  --end "2026-04-15T11:00:00-05:00" \
  --attendee person@example.com \
  --meet
```

### List all calendars

```bash
gws calendar calendarList list --params '{"fields": "items(id,summary,primary)"}'
```

---

## Drive Operations

### List recent files

```bash
gws drive files list --params '{"pageSize": 10, "orderBy": "modifiedTime desc", "fields": "files(id,name,mimeType,modifiedTime)"}'
```

### Search files

```bash
# By name
gws drive files list --params '{"q": "name contains '\''keyword'\''", "pageSize": 10, "fields": "files(id,name,mimeType)"}'

# By type
gws drive files list --params '{"q": "mimeType='\''application/vnd.google-apps.spreadsheet'\''", "pageSize": 10, "fields": "files(id,name)"}'

# In a specific folder
gws drive files list --params '{"q": "'\''FOLDER_ID'\'' in parents", "pageSize": 20, "fields": "files(id,name,mimeType)"}'
```

### Upload

```bash
gws drive +upload ./report.pdf --name "Q1 Report"
gws drive +upload ./data.csv --parent FOLDER_ID
```

### Download

```bash
# Binary files (PDF, images, etc.)
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' -o ./downloaded-file.pdf

# Export Google Docs/Sheets to other formats
gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "application/pdf"}' -o ./exported.pdf
```

---

## Sheets Operations

### Read a spreadsheet

```bash
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A1:Z100"
```

### Append a row

```bash
gws sheets +append --spreadsheet SPREADSHEET_ID --values "col1,col2,col3"

# Multiple rows via JSON
gws sheets +append --spreadsheet SPREADSHEET_ID --json-values '[["row1col1","row1col2"],["row2col1","row2col2"]]'
```

### Get spreadsheet metadata

```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "SPREADSHEET_ID", "fields": "properties.title,sheets.properties"}'
```

**Shell escaping note:** Sheets ranges use `!` which bash interprets as history expansion. Always wrap in single quotes: `'Sheet1!A1:C10'`

---

## Docs Operations

### Read a document

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

### Append text

```bash
gws docs +write --document DOC_ID --text "Text to append"
```

For rich formatting, use `batchUpdate`:

```bash
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{"requests": [{"insertText": {"location": {"index": 1}, "text": "Hello"}}]}'
```

---


## Execution (pure tool)

This skill is a **mechanical wrapper**. No agent dispatch. See `.claude/skills/SKILL-PATTERN.md` Tier D.

**Rationale:** Wrapper around the `gws` CLI for Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) on the personal account. Mechanical CLI calls. Any triage or composition would go to delivery-agent or content-writer through their own skills (/check-mail, etc.), not this wrapper.

The invocation contract below is the complete tool interface. If cognitive work (triage, composition, voice-check) ever gets added to this skill, that work must be delegated to the appropriate specialist agent rather than inlined here.

---

The procedural playbook below is the tool contract.

## Workflow Helpers

Built-in cross-service workflows:

```bash
# Morning standup: today's calendar + tasks
gws workflow +standup-report

# Prep for next meeting: attendees, description, linked docs
gws workflow +meeting-prep

# Convert email to task
gws workflow +email-to-task

# Weekly summary: meetings + unread count
gws workflow +weekly-digest
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| Auth error (401/402) | Re-run `gws auth login -s gmail,drive,calendar,sheets,docs` |
| API not enabled (403 accessNotConfigured) | Enable the API at the link in the error message |
| Drive permission error | Check IAM: `amyn@porbanderwala.com` needs `Service Usage Consumer` on project `fluent-plate-438301-t0` |
| "Google hasn't verified this app" | Expected in testing mode. Click Advanced > Go to gws-cli |
| Scope limit exceeded | Use `-s gmail,drive,calendar,sheets,docs` to stay under 25-scope cap |
| Token expired (7 days inactive) | Re-run `gws auth login` (unverified apps expire after 7 days) |

## Notes

- **This is a personal account.** No HARBOR branding, no business signatures. Keep personal and business email channels separate.
- **Zoho is the business calendar.** Google Calendar is secondary. When creating business events, use Zoho (via `/check-mail` or CalDAV).
- **All outbound requires Pineapple Protocol.** Drafts are exempt.
- **Use `--dry-run`** on any command you're unsure about before executing.
- **Use field masks** on list/get calls to keep output manageable: `--params '{"fields": "files(id,name)"}'`
