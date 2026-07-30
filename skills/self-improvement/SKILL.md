---

name: self-improvement
description: "Captures learnings, errors, and corrections for HARBOR. Use when: (1) A command or operation fails, (2) User corrects you ('No, that's wrong...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) You realize knowledge is outdated, (6) A better approach is discovered. Also review learnings before major tasks."
---

# HARBOR Self-Improvement Skill

Capture learnings, errors, and corrections to enable continuous improvement across all HARBOR domains: books, website, consulting, and growth.

---

## When to Use This Skill

Trigger this skill when ANY of the following occur:

| Trigger | Example |
|---------|---------|
| **Command/operation fails** | `yt-dlp` fails to fetch transcript, Supabase query errors |
| **User corrects you** | "No, Book 1 is already published", "That's the wrong ASIN" |
| **Missing capability requested** | "Can you check the website traffic?" (no GA4 setup) |
| **External API/tool fails** | WebFetch returns error, GitHub API rate limited |
| **Knowledge gap discovered** | "I thought Book 1 wasn't launched but it is" |
| **Better approach found** | "Actually, we should use `mode: all` instead of `mode: primary`" |

**Also review learnings BEFORE major tasks:**
- Starting work on a client deliverable
- Making changes to the website
- Creating new agent files
- Editing book content

---


## Execution (CEO-direct)

This skill is **CEO-owned** and does NOT dispatch to a specialist agent. See `.claude/skills/SKILL-PATTERN.md` Tier C.

**Rationale:** Captures learnings about Claude's own behavior (ERR/LRN/FEAT entries). Meta-skill about the operator itself. Delegating would create infinite regress (an agent writing learnings about the CEO who would then need to write learnings about that). CEO owns the reflection.

The CEO executes the playbook below directly. The CEO may spawn narrow sub-agents (typically `researcher` via the `Agent` tool) for specific sub-tasks — e.g., a fresh-signal check on a named prospect — but composition, framing, and final output stay CEO-authored.

---

The detailed playbook below is what the CEO reads to execute this skill.

## Directory Structure

```
.learnings/
├── LEARNINGS.md      # General learnings (LRN-YYYYMMDD-XXX)
├── ERRORS.md         # Errors and failures (ERR-YYYYMMDD-XXX)
├── FEATURE_REQUESTS.md # Missing capabilities (FEAT-YYYYMMDD-XXX)
└── templates/
    └── learning-template.md
```

---

## ID Format

| Type | Prefix | Example |
|------|--------|---------|
| Learning | `LRN-` | `LRN-20260326-001` |
| Error | `ERR-` | `ERR-20260326-001` |
| Feature Request | `FEAT-` | `FEAT-20260326-001` |

Format: `{TYPE}-{YYYYMMDD}-{XXX}` where XXX is a sequential number.

---

## Required Fields

Every entry must include:

| Field | Description | Example |
|-------|-------------|---------|
| **ID** | Unique identifier | `LRN-20260326-001` |
| **Timestamp** | ISO 8601 datetime | `2026-03-26T14:32:00Z` |
| **Priority** | `critical` / `high` / `medium` / `low` | `high` |
| **Status** | `open` / `in_progress` / `resolved` / `wont_fix` | `open` |
| **Area** | Domain affected | `books` / `website` / `consulting` / `agents` / `general` |
| **Summary** | One-line description | "Book 1 ASIN was incorrect in memory" |
| **Details** | Full explanation | What happened, why, impact |
| **Resolution** | How to fix / what was learned | Steps taken or recommended |

---

## Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Source** | Where this came from | `user_correction`, `api_failure`, `discovery` |
| **Related Files** | Files involved | `/admin/memory/books.md` |
| **Tags** | Searchable keywords | `#ceo-agent`, `#book1`, `#kdp` |
| **See Also** | Related entries | `LRN-20260325-003` |
| **Promoted To** | If promoted to memory | `/admin/memory/books.md` |

---

## HARBOR-Specific Areas

| Area | Description | Memory File |
|------|-------------|-------------|
| `books` | Book 1, Book 2 content/status | `/admin/memory/books.md` |
| `website` | harbor-website features/bugs | `/admin/memory/website.md` |
| `consulting` | Clients, workshops, advisory | `/admin/memory/portfolio.md` |
| `agents` | CEO agent, spawned agents | `/admin/memory/state.md` |
| `brand` | Colors, logos, pricing | `/admin/memory/brand.md` |
| `general` | Cross-cutting or other | `/admin/memory/state.md` |

---

## Logging Workflow

### 1. Create the Entry

```markdown
## LRN-20260326-001

| Field | Value |
|-------|-------|
| **ID** | LRN-20260326-001 |
| **Timestamp** | 2026-03-26T14:32:00Z |
| **Priority** | high |
| **Status** | resolved |
| **Area** | books |
| **Source** | user_correction |

**Summary:** Book 1 ASIN was marked as "not launched" but was already published

**Details:**
The CEO agent memory stated Book 1 was "ready for KDP launch" but the user corrected that it's already live on Amazon with ASIN B0GQT9T1NF. The website correctly links to it.

**Resolution:**
- Updated `/admin/memory/books.md` with correct ASIN and published status
- Updated `/admin/memory/state.md` priorities
- Corrected CEO agent prompt to reflect published status

**Related Files:** `/admin/memory/books.md`, `/admin/memory/state.md`
**Tags:** #book1 #kdp #asin #user_correction
**Promoted To:** `/admin/memory/books.md`
```

### 2. Append to Appropriate File

- Learnings → `.learnings/LEARNINGS.md`
- Errors → `.learnings/ERRORS.md`
- Feature Requests → `.learnings/FEATURE_REQUESTS.md`

### 3. Promote to Memory (if applicable)

If the learning should persist in CEO agent memory:

1. Update the relevant `/admin/memory/*.md` file
2. Add `**Promoted To:**` field to the learning entry
3. Log the decision in `/admin/memory/state.md` decisions table

---

## Promotion Rules

Promote a learning to CEO memory when:

| Condition | Action |
|-----------|--------|
| Affects business priorities | Update `/admin/memory/state.md` |
| Affects client information | Update `/admin/memory/portfolio.md` |
| Affects book status | Update `/admin/memory/books.md` |
| Affects website architecture | Update `/admin/memory/website.md` |
| Affects brand/pricing | Update `/admin/memory/brand.md` |
| Recurring pattern (3+ times) | Add to CEO agent prompt |

---

## Example: Error Entry

```markdown
## ERR-20260326-001

| Field | Value |
|-------|-------|
| **ID** | ERR-20260326-001 |
| **Timestamp** | 2026-03-26T10:15:00Z |
| **Priority** | medium |
| **Status** | resolved |
| **Area** | agents |
| **Source** | config_error |

**Summary:** CEO agent `model: inherit` not valid in OpenCode

**Details:**
When Tab-cycling to CEO agent in OpenCode, got error: "Agent ceo's configured model inherit/ is not valid". The `model: inherit` field is not supported in OpenCode agent markdown files.

**Resolution:**
- Removed `model: inherit` from `.opencode/agents/ceo.md`
- Agent now uses default model
- Changed `mode: primary` to `mode: all` for @mention support

**Related Files:** `.opencode/agents/ceo.md`
**Tags:** #ceo-agent #opencode #config
```

---

## Example: Feature Request

```markdown
## FEAT-20260326-001

| Field | Value |
|-------|-------|
| **ID** | FEAT-20260326-001 |
| **Timestamp** | 2026-03-26T09:00:00Z |
| **Priority** | medium |
| **Status** | open |
| **Area** | website |
| **Source** | user_request |

**Summary:** Need GA4 analytics setup for website

**Details:**
User wants to track website traffic but GA4 is not configured. The `NEXT_PUBLIC_GA_MEASUREMENT_ID` environment variable is not set.

**Resolution:**
- Create GA4 property
- Add measurement ID to Vercel environment
- Configure conversion events

**Related Files:** `/projects/harbor-website/.env.example`
**Tags:** #website #analytics #ga4
```

---

## Review Before Major Tasks

Before starting significant work, read relevant learnings:

```bash
# Check for learnings in specific area
grep -A 20 "Area.*books" .learnings/LEARNINGS.md
grep -A 20 "Area.*website" .learnings/ERRORS.md

# Check open items
grep -B 5 -A 10 "Status.*open" .learnings/*.md
```

---

## Integration with CEO Agent & System

### CEO Agent Boot Sequence
The CEO agent reads `.learnings/LEARNINGS.md` during its boot sequence (Step 2: Context Check) before major work. Learnings directly influence decisions.

### Continuous Memory Protocol
When a learning is promoted to memory, the CEO agent's Continuous Memory Protocol triggers an immediate update to the relevant `/admin/memory/*.md` file. Do NOT batch these.

### Claude Code Auto-Memory
For learnings that should persist across ALL projects (not just HARBOR), also update:
- `~/.claude/projects/-Users-amynporb-Documents--Projects-2026-books/memory/` (project memory)

Only promote to Claude Code memory if the learning is:
- About Amyn's preferences or working style
- About tool/platform behavior (not HARBOR-specific)
- A feedback correction that applies broadly

### Agent-Specific Learnings
When a spawned agent (researcher, content-writer, code-builder) produces a learning:
1. The agent should flag it to the CEO
2. CEO logs it via this skill
3. If the learning affects the agent's behavior, update the agent file in `.claude/agents/`

### Available Skills Context
When logging a feature request, check if an existing skill could address it:
- `/ceo-briefing` - Business dashboard generation
- `/check-mail` - Zoho email sync, read, search, send
- `/portfolio-deck` - Client strategy decks
- `/portfolio-recon` - Prospect intelligence (spawns /fed-intel and /crawl-site)
- `/crawl-site` - Website content crawler for analysis
- `/deck-to-pdf` - HTML deck to PDF with clickable links
- `/excalidraw-diagram` - Visual diagrams
- `/fed-intel` - SAM.gov + USASpending federal data extraction and dashboard
- `/frontend-design` - Web UI building
- `/self-improvement` - This skill (learnings, errors, feature requests)
- `/smart-commit` - Intelligent git commits

---

## Quick Reference

| Action | Command |
|--------|---------|
| Log a learning | Add entry to `.learnings/LEARNINGS.md` |
| Log an error | Add entry to `.learnings/ERRORS.md` |
| Request a feature | Add entry to `.learnings/FEATURE_REQUESTS.md` |
| Promote to memory | Update `/admin/memory/*.md` + add `Promoted To` field |
| Review learnings | `grep "Area.*{domain}" .learnings/*.md` |

---

## Remember

1. **Log immediately** - Don't wait, capture while fresh
2. **Be specific** - Include files, commands, exact errors
3. **Promote wisely** - Only persistent knowledge goes to memory
4. **Review regularly** - Check open items before major work
5. **Link related** - Use `See Also` to connect entries
