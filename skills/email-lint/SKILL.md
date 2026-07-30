---
name: email-lint
description: Grep-scans a client email draft against the 10 editorial rules captured in feedback_email_editorial_patterns.md and LRN-20260410-007. Flags em-dashes, "rebuild" language, specific dates, weekday references, previewed effort, redundant shared context, self-justifying questions, connective tissue, sign-off drift, and hard time windows. Acts as a BLOCKING gate before a draft can be saved to Zoho Drafts or piped to msmtp.
allowed-tools: Read, Bash, Grep, Glob
model: haiku
user-invocable: true
---

# /email-lint — Editorial Lint for Client Emails

**Born from LRN-20260410-007** — I had `feedback_no_em_dashes.md` saved for 11 days and still used 9 em-dashes in the AXOLTL NDA draft. Amyn edited every single one out before sending. This skill turns the post-hoc diff into a pre-send grep gate so the same violations can't sneak through again.

## The Rule

**Every client email gets linted before it leaves the draft state.** Not sometimes. Not "if I remember." Every single one. If `lint_email.py` exits non-zero, the draft is not ready and nothing downstream (Zoho save, msmtp send, Pineapple Protocol) may happen.

## When to Run

| Context | Run the lint? |
|---|---|
| New client email draft | **Yes** — before saving anywhere |
| Edit to an existing draft | **Yes** — re-run after every meaningful change |
| Email to a current client (Salima, Patrick, AK, Chandler, Asad, Kelley, Ted) | **Yes** |
| Email to a cold prospect | **Yes** |
| Warm continuation / social note | **Yes** |
| Internal-only draft (nobody reads it) | Optional |

The linter is cheap (< 100ms). There is no reason to skip it.

## What It Checks

Ten rules mechanically enforced from `feedback_email_editorial_patterns.md`:

| # | Rule | Severity |
|---|------|---|
| 1 | Zero em-dashes in prose (greeting `Name — ` exempted) | error |
| 2 | No "rebuild" / "rebuilt" / "rebuilding" | error |
| 3 | No weekday references for same-day events | warning |
| 4 | No specific dates ("April 10", "on the 10th", "on 4/10", "2026-04-10") | error |
| 5 | Don't preview effort ("I started putting...") | error |
| 6 | No "you showed me" / "you mentioned" — error if inside a question, warning otherwise | error / warning |
| 7 | Questions don't self-justify ("? I want to make sure...") | error |
| 8 | No connective tissue between paragraphs ("While you're...", "On that note...") | error |
| 9 | Pre-signature close is "Thanks!" not "Amyn" | error |
| 10 | Time windows should be generous ("early next week" → "early-to-mid next week") | warning |

**Errors** block the draft. **Warnings** need human review but don't block. Rules 3 and 10 are warnings because they're judgment calls (a weekday reference may be legitimate if NOT same-day; a hard deadline may be legitimate if externally imposed).


## Execution

This skill dispatches to **delivery-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `The email draft file path`
  - `admin/memory/feedback_email_editorial_patterns.md (rules source)`
  - `.learnings/LEARNINGS.md (LRN-20260410-007 and related)`

### Step 3 — Dispatch to delivery-agent

Call the **Agent** tool with:

- `subagent_type`: `delivery-agent`
- `description`: `"Lint a portfolio-facing email draft against the 10 editorial rules"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/email-lint <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/email-lint/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `Lint report with pass/fail per rule + suggested rewrites`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

If Amyn approves rewrites, delivery-agent applies them (with Pineapple Protocol gate before any outbound send).

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what delivery-agent reads as its authoritative reference when executing this skill.

## Invocation

```bash
python3 .claude/skills/email-lint/scripts/lint_email.py <draft_file>
```

The script accepts:
- Plain text (`.txt`, `.md`)
- HTML (`.html`) — tags are stripped before analysis
- Raw MIME / Maildir files (e.g., `operations/mail/zoho/Drafts/cur/...`) — the plain-text part is extracted

Exit codes:

| Code | Meaning |
|---|---|
| `0` | Clean — no errors (warnings may exist). Draft is ready. |
| `1` | Errors found — draft is NOT ready. Fix and re-run. |
| `2` | File not found or usage error |

## Workflow

```
draft content
    │
    ├─ save to temp file (/tmp/my_draft.md)
    │
    ├─ run lint ────────► errors?  ─── yes ──► fix, re-run
    │                        │
    │                        no
    │                        │
    ├─ save to Drafts (Zoho web, Maildir, msmtp pipe)
    │
    └─ request Pineapple Protocol approval
```

## Example Output

### Clean draft
```
Email editorial lint
  File: /tmp/draft_clean.md
  Body: 892 chars / 154 words
  Signature: detected

✓ Clean. No violations. Draft is ready.
```

### Dirty draft
```
Email editorial lint
  File: /tmp/draft_dirty.md
  Body: 1104 chars / 187 words
  Signature: detected

✗ Rule 1: Zero em-dashes in prose (3 hits)
    line 4: em-dash in prose — restructure with periods, semicolons, or commas
      match   : —
      context : Good call earlier. I'm putting the assessment together — a few questions would sharpen it.
    ...

✗ Rule 2: No 'rebuild' in client-facing language (1 hit)
    line 7: 'rebuild' signals failure — use 'assessment', 'analysis', 'report'
      match   : rebuild
      context : before the rebuild.

Summary: 4 errors, 0 warnings
✗ DRAFT NOT READY. Fix all errors above before saving to Drafts or piping to msmtp.
```

## Design Notes

### Signature detection
The linter detects the signature block and excludes it from most rules. Detection priority:
1. A line that is exactly `--` or `-- ` (RFC 3676 sig delimiter)
2. A line containing `Founder, HARBOR` / `HARBOR Initiative` / `harborgovcon.com` / etc., then walks back to the most recent blank line

If the signature isn't detected, the linter warns but continues — the HTML signature may still be appended downstream. This is acceptable because the signature itself never violates the rules (it's static).

### Greeting exemption
Rule 1 allows exactly ONE em-dash on the first non-empty line if it matches `Name — ` (the inline greeting pattern from `feedback_email_greeting_style.md`). Every other em-dash is a violation.

### HTML stripping
HTML tag stripping is crude but sufficient for lint purposes. Block-level closers become paragraph breaks; inline tags are dropped. HTML entities are decoded so `&mdash;` becomes `—` and gets caught by Rule 1.

### MIME extraction
If the file looks like a MIME message (starts with `Return-Path:`, `Received:`, `From:`, or has `Content-Type:` + `MIME-Version:` near the top), the linter extracts the `text/plain` part for analysis. This lets you lint a live Maildir file without any pre-processing.

### Line numbers
Line numbers are relative to the extracted body after HTML stripping and MIME extraction — they won't match the source file exactly if the source was HTML or MIME. The `context` field is always shown so violations can still be located by content.

## Limitations

- **No grammar / voice checking.** This is a grep-based mechanical lint. It catches rule violations but doesn't catch tone drift, weak verbs, passive voice, or off-brand phrasing. A human read is still required.
- **False positives on Rule 3 (weekday references).** If you're writing Tuesday about a Monday event, "on Monday" is correct and the linter will still flag it. That's why Rule 3 is a warning, not an error.
- **Rule 10 (time windows) is a suggestion.** Some deadlines are externally imposed and legitimate. Review each warning before dismissing.
- **Does not check subject lines.** Subject-line lint is a future improvement — the rules there are different (Rule 2 applies, but most others don't).
- **Does not check attachment alignment.** If you say "PDF attached" and there's no attachment, this won't catch it.

## See Also

- `feedback_email_editorial_patterns.md` (memory) — source of truth for the 10 rules, with worked examples from the NDA diff
- `feedback_no_em_dashes.md` (memory) — the standalone em-dash rule (pre-existed but was violated on 2026-04-10)
- `feedback_email_greeting_style.md` (memory) — inline `Name — ` greeting pattern (Rule 1 exemption)
- `feedback_email_formatting.md` (memory) — HTML signature requirement
- `LRN-20260410-007` — the post-mortem diff analysis that produced this skill
- `.claude/skills/check-mail/SKILL.md` — downstream consumer: the Pineapple Protocol send gate should call this linter before piping to msmtp

## Future Improvements

- Subject-line lint (Rule 2 + dedicated subject rules)
- Pre-commit integration: git hook that lints any `.eml` / `operations/mail/zoho/Drafts/**` file before commit
- Attachment sanity check: if the body says "attached" and there's no `Content-Disposition: attachment` in the MIME, flag it
- Hook into `/check-mail` skill so the Pineapple Protocol gate mechanically runs this before sending
- Learnable exemptions: a `.email-lint-ignore` file per-draft for one-off exceptions (use sparingly)

## Scripts

- `scripts/lint_email.py` — the linter (pure Python 3, no deps)
