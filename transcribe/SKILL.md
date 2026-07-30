---
name: transcribe
description: Transcribe audio recordings using OpenAI API with speaker diarization,
  generate enhanced markdown transcripts with summaries, and update catalogues. Use
  when processing .m4a files or clearing transcript backlogs.
argument-hint:
- folder-path or file-path
disable-model-invocation: true
---

# Audio Transcription Pipeline

You are executing a full transcription pipeline. Process audio files through: scan -> transcribe -> format -> summarize -> catalogue.

## Environment

- OpenAI API key: `$OPENAI_API_KEY` (from shell environment)
- Transcription script: `${CLAUDE_SKILL_DIR}/scripts/transcribe_audio.py`
- Current project directory: the working directory

## Step 1: Identify Files to Process

If `$ARGUMENTS` is provided, use it as the target (file or folder path).

Otherwise, **auto-detect**: scan all `transcripts_*/` and `transcript_*/` folders in the working directory for `.m4a` files that lack a matching processed markdown file.

A file is **unprocessed** if no sibling file matches any of these patterns:
- `{basename}_combined.md`
- `{basename}_large-v3.md`

```bash
# Example detection logic — adapt as needed
for dir in transcripts_* transcript_*; do
  for m4a in "$dir"/*.m4a; do
    base="${m4a%.m4a}"
    if [ ! -f "${base}_combined.md" ] && [ ! -f "${base}_large-v3.md" ]; then
      echo "UNPROCESSED: $m4a"
    fi
  done
done
```

Report what you found: total .m4a files, how many unprocessed, which folders. Ask the user to confirm before proceeding if there are more than 5 files.

## Step 2: Transcribe via OpenAI API

For each unprocessed `.m4a` file, run the transcription script:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/transcribe_audio.py" "<audio_file>" -o "<output_json>"
```

- Default model: `gpt-4o-transcribe-diarize` (transcription + speaker identification)
- Output: JSON file saved alongside the audio as `{basename}.json`
- If a file exceeds 25MB, warn the user and suggest local MLX Whisper as an alternative
- Process files sequentially to avoid API rate limits

If `_original.txt` exists alongside the `.m4a`, note it — we'll use it in Step 3 to improve speaker names.

## Step 3: Generate Combined Markdown

For each transcribed file, create `{basename}_combined.md` with this structure:

```markdown
# {Recording Name}

**Source:** `{filename}.m4a`
**Model:** {model used}
**Language:** English
**Generated:** {YYYY-MM-DD HH:MM}

---

## Summary

**Participants:** {count} speakers identified ({Speaker 1 Name}, {Speaker 2 Name}, ...)
**Conversation Type:** {call|meeting|presentation|voice_memo|training|roundtable|interview}
**Key Topics:** {topic1}, {topic2}, {topic3}

### Key Discussion Points
- {point 1}
- {point 2}
- {point 3}

### Action Items
- {action item 1, if any}
- {action item 2, if any}

---

## Detailed Transcript

**[{Speaker Name}]** ({MM:SS})
{text content}

**[{Speaker Name}]** ({MM:SS})
{text content}

...

---

## Full Text

{complete unformatted transcript text}
```

### Speaker Name Resolution

1. If `gpt-4o-transcribe-diarize` returns speaker labels (e.g., "Speaker 1", "Speaker 2"), use them as-is initially
2. If an `_original.txt` file exists alongside the audio, read it and map speaker IDs to real names using context clues (names mentioned, self-references like "I'm [name]", etc.)
3. If no `_original.txt` exists, attempt to identify speakers from transcript context (introductions, name mentions)
4. When uncertain, keep generic labels ("Speaker 1", "Speaker 2")

### Summary Generation

Read the full transcript and generate:
- **Conversation type**: classify as call, meeting, presentation, voice_memo, training, roundtable, or interview
- **Key topics**: 3-6 main subjects discussed (use specific terms, not generic)
- **Key discussion points**: 3-5 bullet points capturing the substance
- **Action items**: any commitments, next steps, or follow-ups mentioned
- **Key people**: everyone mentioned by name, with their role/context if apparent

## Step 4: Update Catalogues and Index

### Update `index/index.csv`

Append a new pipe-delimited row for each processed transcript:

```
filename|folder|date|size_kb|summary|conversation_type|key_people|key_topics|mentions_ssp|mentions_anas|mentions_stephen|mentions_bonita|mentions_spn|mentions_vlad|mentions_tony
```

- `filename`: the `_combined.md` filename
- `folder`: which transcript folder it's in
- `date`: extracted from filename (YYMMDD format) or "unknown"
- `size_kb`: file size of the generated .md
- `summary`: 1-2 sentence summary (no pipes!)
- `conversation_type`: classified type
- `key_people`: semicolon-separated names
- `key_topics`: semicolon-separated topics
- Boolean flags: TRUE/FALSE based on whether the transcript mentions each person/term

### Update Folder CATALOGUE.md

If the folder already has a `CATALOGUE.md`, append the new transcript(s) to the table and add detailed summary entries. If no `CATALOGUE.md` exists, create one following this format:

```markdown
# {folder_name}/ Catalogue

**Total transcripts:** {count}
**Format:** Combined (OpenAI {model} + diarization) — `_combined.md`
**Date range:** {date range}

{brief description of folder contents}

---

## Transcripts

| # | Filename | Date | Size | Type | Summary |
|---|----------|------|------|------|---------|
| 1 | {filename} | {date} | {size} | {type} | {summary} |

---

## Detailed Summaries

### {filename}
{2-3 sentence detailed summary}
```

### Update Root CATALOGUE.md

Update the root `CATALOGUE.md` to reflect new transcript counts and folder descriptions. Update the Repository Structure table and total count.

## Step 5: Report Results

After processing, report:
- Number of files processed
- Any errors or skipped files
- Summary of what was transcribed (names, types, durations)
- Reminder of any files that were too large for the API

## Error Handling

- If OpenAI API returns an error, report it and continue with next file
- If a file is too large (>25MB), skip it and suggest using local MLX Whisper
- If `openai` package is not installed, run `pip install openai` first
- If `OPENAI_API_KEY` is not set, tell the user to check their shell environment
