---
name: high-stakes-briefing-workflow
description: Use for high-stakes internal briefings, meeting minutes, interview/call debriefs, strategic readouts, or any artifact where Amyn expects deep context from a project folder. Prevents shallow plausible synthesis by forcing source-tree discovery, evidence separation, screenshot review, and eval gates before delivery.
tags: [briefing, meeting-minutes, debrief, quality, evidence, html]
tier: A
---

# High-Stakes Briefing Workflow

Use this skill when the user asks for a detailed briefing, meeting minutes, call analysis, interview debrief, strategic readout, or HTML artifact tied to a folder/repo/project.

## Failure Mode This Prevents

Do **not** write a polished artifact after reading only the primary transcript or one obvious file. That produces plausible but shallow synthesis. The required deliverable is a source-grounded artifact that reflects the full project context and the user's background, not generic meeting minutes.

## Mandatory Workflow

### 1. Source-tree discovery first

Before drafting, inspect the project folder structure.

```bash
cd /path/to/project && tree -a -L 3
```

If `tree` is unavailable, use a Python directory walk. Identify:

- primary transcript or meeting recording text
- screenshots / shared materials
- prior briefings and prep documents
- status files, README, index, or project memory
- people dossiers
- planning artifacts
- deliverables already produced
- source docs and extracted text

Do not assume the user named every relevant file. If they point to a project folder, mine it.

### 2. Evidence-stack separation

Keep these categories separate in the artifact:

- **Transcript facts:** what someone said on the call
- **Screenshot/shared-material facts:** what was shown visually
- **Local project artifacts:** prior prep, status, planning, dossiers, deliverables
- **Public sources:** external URLs, official docs, press releases, regulatory pages
- **Interpretation/opinion:** Hermes analysis with confidence range

Never blend these into one undifferentiated narrative.

### 3. Speaker-label sanity check

If transcript speaker labels are ambiguous or noisy:

- use the user's mapping if provided
- state the mapping in the artifact
- identify echo/duplication artifacts
- quote only anchored, high-confidence passages

### 4. Screenshot discipline

Count screenshots/files first. Analyze every screenshot or explicitly state why one was skipped. Include:

- visible title/headings
- names and roles
- diagrams/org charts
- dates, values, deadlines, status labels
- strategic meaning
- alt text if embedded in HTML

### 5. User-background mapping

Before drafting insights, pull the user's relevant background from local artifacts or memory. For Amyn, this often includes:

- HARBOR founder / productization thesis
- federal compliance and GovCon experience
- CUI/GCC High/NIST/DFARS background
- Shipley/capture experience
- USMC cyber/network experience
- SBIR/AI systems work
- current strategic objective or director-slot angle

The artifact should explain why the user's background changes the read.

### 6. Write the artifact as a strategic brief, not a transcript summary

Minimum sections for high-stakes meeting minutes:

1. BLUF
2. Evidence stack and source caveats
3. Timeline / call flow
4. Critical revelations
5. Screenshot/shared-material analysis
6. Strategic interpretation
7. Stakeholder perspectives
8. Risks and constraints
9. Opportunity / positioning map
10. What can be shared with whom
11. Sources

For HTML: ensure readable, accessible layout and image alt text. Prefer warm HARBOR-style palette unless another style is requested.

### 7. Share-outs must match requested use

If the user asks for messages to specific people, distinguish:

- **Concise backfill message** — a few sentences or short bullets the user can copy-paste. "I told them I'd fill them in." This is NOT operational advice for the user — it is draft text to send. Keep it short, factual, and not oversharing.
- **Operational guidance for the user** — longer, internal-only context about how to handle a person or situation. Label it clearly as guidance, not a message to send.
- **Sensitive internal/private notes** — things the user should know but never share.

Do not confuse these categories. The user's phrasing ("what I can share," "help me respond," "backfill them") signals which they need. When in doubt, ask: "Do you want a short message to send, or operational guidance for yourself?"

### 8. Cross-reference update pattern

When multiple calls happen on the same day about the same subject:

- Create a standalone briefing for each call.
- Then update the primary strategic brief with a cross-reference section containing:
  - What the second source confirmed (two-source verification table)
  - What the second source contradicted or clarified
  - What new intelligence emerged
  - Whether the user's positioning changes
- Do NOT just create two standalone files and stop. "Update everything" means cross-reference the new intel into existing artifacts.
- Reference the new transcript and briefing file paths in the updated section.

### 9. Call transcription and speaker diarization

When the user asks for a call transcript with speaker attribution, follow the full workflow documented in `references/call-transcription-and-diarization.md`. Quick reference:

1. Retrieve audio via Nextcloud web download or SCP from AP-Desktop
2. Transcribe with `mlx_whisper --model mlx-community/whisper-large-v3-turbo`
3. Attribute speakers manually via content patterns for two-person calls
4. Save as timestamped `.md` transcript with attribution header

### 10. Eval and verification gates

Before final delivery:

```bash
python3 ~/.hermes/skills/harbor-eval-gate/scripts/eval_gate.py \
  --candidate-file /path/to/artifact.html \
  --benchmark ~/.hermes/skills/harbor-eval-gate/benchmark/benchmark-v0.yaml \
  --dry-run
```

For important artifacts, also run full eval gate if available.

Static checks:

```bash
python3 - <<'PY'
from pathlib import Path
p=Path('/path/to/artifact.html')
s=p.read_text()
print('chars', len(s))
print('em_dash_count', s.count('—'))
for b in ['delve','tapestry','leverage','robust','comprehensive','best-in-class','next-generation','synergy','in conclusion','at the end of the day','moving forward']:
    if b in s.lower(): print('banned', b)
PY
```

### 9. File permissions after write_file

Hermes `write_file` may create files as `root:staff` with restrictive permissions. Always run:

```bash
chown amynporb:staff /path/to/artifact.html
chmod 644 /path/to/artifact.html
```

Then verify with `ls -la`.

### 10. Open or deliver the final artifact

If the user needs to inspect locally:

```bash
open /path/to/artifact.html
```

Final response should include:

- exact file path
- what was improved
- eval result
- permission status
- concise requested outbound text, if any

## Audio Ambiguity Rule

Audio transcription is probabilistic, not ground truth. The same 2-second clip can be heard as "I terminated all three" or "I didn't hire all three" depending on acoustic context. Before you encode a personnel action as fact, read `references/call-transcription-and-diarization.md` — specifically the Critical Evidence Triangulation and Audio Ambiguity Pitfall sections — and verify against:
- organizational artifacts (Team Roles sheets, RACI matrices)
- other call transcripts
- whether the speaker's next sentence contradicts or qualifies the phrase
- whether independent HR or source documents exist

If unverifiable, label it **allegation; unverified** and explain what would resolve the uncertainty. In an HTML briefing, use a table row with an explicit "Unverified" status column. Never state ambiguous audio as certainty.

## Red Flags

Stop and gather more context if:

- the user says "do not be lazy," "research hat," or "everything is in this folder"
- the user says "update everything" — this means cross-reference new intel into all existing artifacts, not just create new standalone ones
- a meeting transcript references documents or screenshots not yet reviewed
- there are screenshots in a sibling folder
- local project contains prior prep or analysis files
- the task mentions "my background," "the role," "director slots," or strategic positioning

Those are explicit signals that shallow meeting minutes will fail.
