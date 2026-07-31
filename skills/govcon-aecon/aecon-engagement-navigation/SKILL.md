---
name: aecon-engagement-navigation
description: Navigate the Aecon FCS engagement repo — find call recordings, transcripts, working analyses, research, and deliverables. Use when the user references past Aecon events, people, calls, or asks "remember when X happened" in the Aecon context.
triggers:
  - User references past Aecon calls, meetings, or conversations ("remember the call with...", "what did X say about...")
  - User asks about Aecon personnel, processes, or events that predate the current session
  - User mentions "Issiah," "Isaiah," "Mark," "Lisa," "Justin," "Douglas," "Brian," "Eric," or other Aecon FCS team members
  - User says "check the call recordings" or "look at the briefing htmls"
---

## Engagement Repository Structure

The Aecon FCS engagement lives at `~/repos/aecon-fcs/`. All research, call recordings, working files, and deliverables live here. The briefings folder on Nextcloud (`/data/nextcloud/data/amyn/files/briefings/`) also contains Aecon-related HTML briefings.

```
~/repos/aecon-fcs/
├── 00-calls/           # Call recordings, transcripts, meeting minutes — organized by date
│   ├── 20260512/       # May 2026 calls
│   ├── 20260610/       # June 10 calls (Douglas, Isaiah transcripts)
│   ├── 20260630/       # June 30 standup, emails, analyses
│   ├── 20260701/       # July 1 process alignment call, meeting minutes, process map
│   ├── 20260713/       # July 7-13 transcripts (Recordings 89-91, Bentree Road, Enclave standup)
│   └── 20260714/       # July 14-15 recordings (bentree-road/, new-recordings/, 1-on-1 calls)
├── working/            # Analysis files, extracts, overlays, master analyses
│   ├── 09-isaiah-drive-master-analysis.html   # Isaiah's Google Drive deep analysis
│   ├── extracts/                               # Raw extracts from documents/spreadsheets
│   └── overlay-2026-06-13/                     # Org overlay analysis
├── 03-research/        # Research dossiers
│   ├── compliance/     # Compliance research (TA, federal facilities, etc.)
│   └── personnel/      # Personnel dossiers (sinem-matay.md, etc.)
├── deliverables/       # Final client-facing deliverables
│   └── aecon-federal-plan.html
└── CLAUDE.md           # Engagement-level guidance (if present)
```

## Critical Workflow: Finding Past Aecon Information

**When the user references a past Aecon event, person, or conversation:**

1. **Check the file system FIRST** — call recordings and briefings are the most detailed source. Search `~/repos/aecon-fcs/00-calls/` for relevant date folders and files. Use `search_files` with `target='content'` and `path='~/repos/aecon-fcs/00-calls/'` for person names or topics.

2. **Check Nextcloud briefings** — use `search_files` with `path='/data/nextcloud/data/amyn/files/briefings/'` for Aecon-related briefings.

3. **Check session history SECOND** — `session_search` for relevant queries. Session history may only contain summaries; the file system often has richer detail (full transcripts, meeting minutes, analyses).

4. **Cross-reference** — file-system findings against session history to fill gaps.

**Pitfall:** Session history alone often misses call details. The file system `00-calls/` directory contains full transcripts with speaker-labeled turns, meeting minutes, and analyses that session history only references in passing. If the user sends an OOB message redirecting you ("check the call recording briefing htmls"), immediately switch to file-system search — don't keep searching session history.

## Key Aecon FCS Personnel (for search targeting)

| Person | Role | CAGE/Unit | Notes |
|--------|------|-----------|-------|
| Issiah/Isaiah Castle | Federal Procurement Manager (FPM) | FCS / US Nuclear | USMC. Amyn's referral. Built SharePoint structure. Drives procurement vendor analysis. |
| Mark Payne | Federal Operations Manager (FOM) | FCS | Team lead, runs daily standups. USMC. |
| Lisa Gloster | Federal Contract Manager (FCM) | FCS | Contracts & compliance. |
| Justin Frawley | Federal Subcontract Manager (FSM) | FCS | Clearance grantor, manual access process. |
| Douglas Henderson | Federal Compliance Director (FCD) | AFSI/FCS | Amyn's direct supervisor. On leave (badge reprocessing). |
| Brian Gregorio | Sr. Director, Compliance | FBU | Amyn's interim reporting line. |
| Eric Atkinson | Federal CAS & Audit Manager (FCAM) | FBU | Budget, finance, timekeeping. |
| Amyn Porbanderwala | FCICS | AFSI/FBU | Controlled Information Compliance Specialist. |

## Call Recording Naming Conventions

Files in `00-calls/` follow several patterns:
- **Transcripts:** `transcript-<person>-<date>.txt` or `Call_Transcript_<description>.html`
- **Meeting minutes:** `meeting-minutes-<date>.html` or `meeting-minutes-<person>-<date>.html`
- **Pre-meeting briefs:** `<Description>_Brief_<date>.html`
- **Standup recordings:** `New_Recording_<NN>_<Description>_<date>.html`
- **Bentree Road project:** `Bentree_Rd_<NN>_<Description>_<date>.html`
- **Raw audio:** `Voice <YYMMDD>_<timestamp>.m4a`

Recordings with generic "Speaker N" labels need context from meeting minutes or pre-briefs to identify who's speaking.

## Isaiah/Issiah-Specific Notes

- Isaiah's Google Drive (shared June 10, 2026) contains 20 files — the full operating blueprint for Aecon's Federal Procurement Branch. The deep analysis is at `working/09-isaiah-drive-master-analysis.html`.
- Isaiah is building the procurement department from scratch — all 3 procurement specialist roles are unfilled.
- His key process documents include the AFSI Federal Playbook (689 lines), Nuclear Project Execution Overlay Framework, and the Federal vs. Commercial procurement presentations (R2/R3).
- In standups, Isaiah alternates between "Speaker 7" (New Recording 90), "Speaker 2" (Call Transcript Aecon), or is explicitly named depending on the recording's transcription method.
- His start date is blank in the org chart — formal HR status may be lagging behind operational reality.

## Reference Files

- `references/call-index.md` — Indexed listing of all call recordings, transcripts, meeting minutes, and working analyses by date, with speaker mappings and key topics.
