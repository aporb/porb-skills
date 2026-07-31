---
name: knowledge-capture
description: "Personal knowledge capture system — ingests notes, transcripts, links, and brain dumps, structures them with tags and connections, and produces daily digests."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge, notes, transcripts, research, digestion, obsidian]
prerequisites:
  commands: []
  files:
    - path: ~/Documents/Knowledge-Base/
      why: Knowledge base root directory
related_skills:
  - personal-task-orchestrator
  - research-orchestration
  - youtube-content
  - obsidian
tier: B
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---

# Knowledge Capture System

Builds a personal knowledge capture system that takes voice notes, brain dumps, article links, and random ideas — structures them, connects them, and produces a daily digest of what you've captured and what needs attention.

## Triggers

- User shares raw notes, voice transcripts, article links, or random ideas
- "Build a knowledge base" or "knowledge capture system" request
- User wants to organize fragmented information
- Request for daily/weekly digests of captured content

## System Architecture

```
~/Documents/Knowledge-Base/
├── inbox/              — raw, unprocessed notes (the capture zone)
├── processed/           — structured, tagged, connected notes
│   ├── learning/
│   ├── ideas/
│   ├── research/
│   └── uncategorized/
├── connections/         — auto-generated link maps between notes
├── digests/             — daily and weekly summaries
├── archive/             — completed, obsolete, or dormant items
└── index.md             — master index with stats and quick links
```

## Workflow

### Phase 1 — Discovery

Ask these 5 questions before proceeding:

1. Where are your raw notes? (folder path, single file, "I'll start fresh", or "process everything in ~/Documents/Notes/")
2. What format are they in? (markdown files, plain text, voice memo transcripts, mixed)
3. What categories matter to you? (work projects, personal, learning, ideas, people, health, finances — pick any that apply)
4. How do you want the daily digest delivered? (markdown file, HTML briefing, both)
5. Where should the organized knowledge base live? (default: `~/Documents/Knowledge-Base/`)

If the user says "I don't know" or "figure it out," make reasonable defaults and proceed. If the user gets frustrated with questions, stop asking and execute with sensible defaults.

### Phase 2 — System Spec

After answers, produce or confirm the Knowledge System Spec:
- Directory structure (inbox/processed/connections/digests/archive)
- Processing pipeline steps
- Daily digest format
- Quality rules (no notes in inbox > 24h, every note gets ≥1 tag, etc.)

### Phase 3 — Delegation

Dispatch up to 4 sub-agents in parallel:

**Sub-agent 1 — Inbox Scanner**
- Read all files in inbox or specified raw notes location
- Extract: title, full text, file creation date, file type
- Return structured manifest of all notes with metadata
- Flag unreadable or corrupted files

**Sub-agent 2 — Knowledge Processor**
- Process each note through pipeline: extract → tag → connect → classify → surface
- Generate tags from controlled vocabulary (create vocabulary from first pass)
- Detect connections: same project name, same person, same URL, similar topic
- Extract action items using pattern matching (TODO, "action:", "follow up", deadline indicators)
- Write processed notes to appropriate category folders
- Move originals from inbox to processed (or copy if source is external)

**Sub-agent 3 — Index & Digest Builder**
- Build or update `index.md` with master list, stats, cross-references
- Build connections map showing linked notes and why
- Generate daily digest in HTML format (HARBOR briefing style: ivory #FAF9F5, serif headings, mono metadata, 1.5px borders)
- Include: new today, action items, connections found, random rediscovery from 30+ days ago, stats
- Save digest to `digests/[YYYY-MM-DD]-daily-digest.html`
- If Sunday (7th day), also generate weekly digest with trends

**Sub-agent 4 — Action Item Tracker**
- Extract all action items from processed notes
- Build or update `action-items.md` with status tracking
- Sort: overdue → due this week → due later → no deadline
- Mark items appearing in multiple notes (likely important)
- Flag items open > 14 days for review

### Phase 4 — Synthesis

After sub-agents complete, deliver:

```
## Knowledge Capture System — Initialized

### System Location
~/Documents/Knowledge-Base/

### Processing Summary
- Notes scanned: N
- Notes processed: N
- Categories populated: [list]
- Action items extracted: N
- Connections found: N

### Daily Digest
- File: ~/Documents/Knowledge-Base/digests/[date]-daily-digest.html
- Highlights: [top 3 items]

### Next Steps
- Drop new notes into ~/Documents/Knowledge-Base/inbox/
- Run this workflow anytime to process inbox and get fresh digest
```

## Processing Pipeline (for Sub-agent 2)

For every note in the inbox:

1. **Extract** — identify: key entities (people, projects, dates, URLs), action items (tasks with implied owners/deadlines), and sentiment/tone
2. **Tag** — apply 1–3 tags from controlled vocabulary (generate vocabulary from first pass)
3. **Connect** — if note references a project, person, or previous note, create bidirectional link
4. **Classify** — assign to one category folder based on content
5. **Surface** — if note contains action item, extract to task list
6. **Move** — relocate from inbox/ to processed/[category]/

## Daily Digest Format

```markdown
# Daily Knowledge Digest — [Date]

## New Today (N items)
- [note title] → [category] — [one-line summary with key entities]

## Action Items Extracted (N items)
- [ ] [action] — from "[note title]" — [owner] — [deadline if present]

## Connections Found (N links)
- "[Note A]" ↔ "[Note B]" — [why they're connected]

## Overdue Review (N items)
- [note title] — last reviewed [date] — [category]

## Stats
- Total notes: N | New this week: N | Orphaned (no connections): N
- Action items open: N | Completed this week: N

## Random Rediscovery
- [one random note from 30+ days ago worth revisiting]
```

## Quality Rules

- No note stays in inbox > 24 hours without being processed
- Every note gets at least 1 tag
- Action items must have an owner (default to "me" if not specified)
- Connections are bidirectional (if A links to B, B's index shows link to A)
- The index.md regenerates on every processing run

## Operational Constraints

- NEVER delete original notes — only move or copy them
- NEVER modify content of a note — only add metadata (tags, connections)
- If note is unreadable, flag it and skip — do not guess content
- Daily digest must be readable in under 2 minutes
- Maximum 4 sub-agents active at once
- If source folder has 50+ notes, process in batches of 20 to avoid timeout
- For batch processing existing YouTube transcripts: use `process_youtube_transcripts.py` script (see `references/youtube-transcript-pipeline.md`)

## YouTube Transcript Integration

Two paths: URL fetching (incoming) OR existing transcript files (batch processing).

### Path A — Incoming URL
When user provides a YouTube URL:
1. Use `youtube-content` skill to fetch transcript
2. Format as markdown with: title, URL, channel, duration, published date, tags, full transcript with timestamps
3. Add sections: Key Points, Analysis, Connections, Tags
4. Write to inbox for processing

**Pitfall:** If `youtube-transcript-api` not installed:
```bash
uv venv ~/.hermes/venv
uv pip install youtube-transcript-api --python ~/.hermes/venv/bin/python
~/.hermes/venv/bin/python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps
```

### Path B — Batch Processing Existing Transcripts
When user has existing transcript files (e.g., `*transcript-*.txt` in Briefings folder):

**Use the YouTube Transcript Processing Script** (`knowledge-capture/references/youtube-transcript-pipeline.md`):

```bash
cd ~/Documents/Knowledge-Base
python3 process_youtube_transcripts.py
```

**5-Stage Pipeline:**
1. **Extract** — Title, URL, date, duration, speaker, channel, key entities, themes, quotes
2. **Tag** — Generate 1-3 tags per note (AI/ML, Hardware/IoT, Mobile Dev, etc.)
3. **Connect** — Cross-reference by shared topics, entities, channels
4. **Classify** — Auto-assign to learning/ideas/research/uncategorized
5. **Surface** — Extract actionable insights and notable quotes

**Enhanced Note Structure:**
```yaml
---
title: [Extracted title]
url: [YouTube URL]
published: [Date]
duration: [Duration]
speaker: [Speaker/Creator]
channel: [Channel name]
processed: [Processing timestamp]

entities: [Comma-separated entities]
themes: [Comma-separated themes]
tags: [Comma-separated tags]
category: [learning/ideas/research/uncategorized]

connections:
  same_channel: [Related notes by channel]
  related_topics: [Related notes by theme]
  shared_entities: [Related notes by entity]

notable_quotes:
  - [Quote 1]
  - [Quote 2]

actionable_insights:
  - [Insight 1]
  - [Insight 2]
---

[Original transcript content preserved below]
```

**Classification Heuristics:**
- **Learning**: "how to", "explained", "guide", "tutorial", "concept", "introduction"
- **Ideas**: "ideas", "tools", "minimalist", "free", "open source", "built"
- **Research**: "targeting", "maven", "palantir", "iran", "war", "analysis"

**Connection Types:**
- Same channel (YouTube)
- Related topics (shared themes like AI Agents, Design)
- Shared entities (companies like Google, Meta)

**Pitfall:** Transcripts missing metadata headers (no title, URL, date):
- Skip with warning rather than crash
- Note in summary report which files were excluded
- Manual fix: fetch metadata via YouTube API or add headers manually

## HTML Digest Format

When delivering HTML digests to Discord:
- Self-contained HTML (no external dependencies)
- Ivory background: #FAF9F5
- Serif headings
- Monospace metadata
- 1.5px borders
- Clay accents
- No gradients/shadows/emoji

Format matches HARBOR briefing style (see `prompt-authoring` skill for templates).

## Pitfalls

- **Don't stop to ask obvious questions.** The user wants execution, not a Q&A. Make reasonable defaults. If the user says "figure it out" or "I'm tired of these questions," stop the discovery phase immediately and execute with sensible defaults. This is a hard preference — not a soft suggestion.
- **Don't wait for all sub-agents if user is impatient.** Provide partial results as they complete.
- **Don't overwhelm with metadata.** Keep tags to 1-3 per note.
- **Don't lose the source.** Always preserve original notes in inbox or archive.
- **Don't over-automate.** Categories and tags improve with human guidance.
- **Don't forget the digest.** The deliverable is the digest, not just the processed notes.
- **CRITICAL — Sub-agent race condition.** If you dispatch Sub-agent 3 (Index/Digest) in parallel with Sub-agent 2 (Processor), the digest will be built BEFORE processed notes exist, producing a stale 0-note output. Two fixes: (a) serialize — wait for Sub-agent 2 to complete before dispatching Sub-agent 3, or (b) rebuild — after all sub-agents complete, re-read the processed/ directory and regenerate the digest yourself with real content. Option (b) is preferred because it doesn't block the pipeline.
- **Sub-agents scan wider than you expect.** If you tell a sub-agent to scan a specific folder, it may find related files in adjacent directories (e.g., transcripts in `~/Documents/Briefings/` when you pointed at `~/Documents/ObsidianVaults/`). This is usually good — more content captured. But verify the processed output matches what was actually found, not what you expected to find.
- **Write race on shared files.** If you and a sub-agent both write the same file (e.g., the HTML digest), the last writer wins. Always verify the final file has real content after all sub-agents complete. If the sub-agent overwrote your good content with stale content, re-write yours.

## User Preference Signals (from session)

- "I'm tired of these questions. I think you know what to do. Just execute." — When user expresses frustration with discovery questions, stop asking and use reasonable defaults.
- User prefers HTML briefings to Discord over markdown files
- User expects proactive COO posture — figure it out and deliver
- Knowledge base location: default to `~/Documents/Knowledge-Base/`
- Categories: learning, ideas, research, uncategorized (auto-determined from content)

## Related Skills

- `personal-task-orchestrator` — for task extraction from brain dumps (distinct from knowledge capture)
- `research-orchestration` — for multi-source deep research (can feed into knowledge base)
- `youtube-content` — for fetching and formatting YouTube transcripts
- `obsidian` — for reading/writing notes in Obsidian vaults

## References

- `references/youtube-transcript-pipeline.md` — Batch processing script and documentation for existing transcript files
- `references/distinction-from-task-orchestrator.md` — How knowledge capture differs from task orchestration