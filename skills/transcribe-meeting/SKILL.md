---
name: transcribe-meeting
description: Transcribe a meeting recording (mp4/m4a/mp3/wav) with diarized speaker labels using OpenAI gpt-4o-transcribe-diarize. Handles audio longer than the 1400s model limit via chunking with per-chunk speaker reconciliation. Outputs a human-readable markdown transcript grouped into speaker turns plus a machine-readable JSON with absolute timestamps.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
model: sonnet
user-invocable: true
---

# /transcribe-meeting — Diarized Meeting Transcription

Takes a meeting recording of any length, transcribes it with OpenAI's `gpt-4o-transcribe-diarize` model, and produces a clean speaker-labeled markdown transcript.

**Born from LRN-20260410-006** — replaces the ad-hoc pipeline run by hand for the AXOLTL / Chandler Provence call on Apr 10, 2026. All the sharp edges (1400s limit, speaker-ID drift across chunks, audio compression floor) are encoded here so we don't step on them again.

## Prerequisites

- `ffmpeg` installed (`brew install ffmpeg`)
- Python 3
- `OPENAI_API_KEY` set in `~/.zshrc` (extracted via grep when running)
- Input file: `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, or `webm`

## When to Use

- You have a call recording longer than a couple of minutes
- You need speaker labels (not just a text dump)
- You want timestamps per speaker turn
- You're writing a call debrief, assessment report, or status update that references specific quotes

## When NOT to Use

- The recording already has a Zoom auto-generated transcript that's good enough for your purpose (check first — it's free)
- You only need a text dump and don't care who said what → use `whisper-1` or `gpt-4o-mini-transcribe` instead (cheaper, longer single-shot limit)

## Pipeline

```
input.mp4 (any size, any length)
    │
    ├─ ffmpeg: extract mono 44.1kHz MP3
    │    target bitrate depends on duration (see table below)
    │    output: <basename>_audio.mp3
    │
    ├─ ffprobe: get duration
    │
    ├─ if duration ≤ 1400s AND file ≤ 25MB:
    │    single API call with chunking_strategy=auto
    │
    ├─ else:
    │    split into N chunks ≤ 940s each
    │    (safety margin below the 1400s hard limit)
    │    upload each chunk sequentially to the API
    │
    ├─ per-chunk speaker remap
    │    each API call assigns A/B/C independently
    │    reconcile by reading first few segments per chunk
    │    (or prompt the user with the first segment text of each chunk)
    │
    ├─ merge with absolute timestamps
    │    offset = (chunk_index - 1) * chunk_duration
    │
    └─ outputs:
       - <basename>_audio.mp3 (extracted audio)
       - <basename>_chunk_{N}.mp3 (if chunked)
       - <basename>_chunk_{N}_diarized.json (raw per-chunk)
       - <basename>_merged_diarized.json (absolute-time merged)
       - <basename>_merged_diarized.md (speaker-turn markdown — THIS IS THE HUMAN-READABLE ONE)
       - README.md explaining what's in the folder
```

## Hard Limits to Work Around

| Limit | Value | Source |
|---|---|---|
| Max file size per request | 25 MB | OpenAI audio API |
| Max duration per `gpt-4o-transcribe-diarize` request | **1400 seconds (23.3 min)** | Undocumented, discovered via HTTP 400 on 2026-04-10 |
| Max file formats | mp3, mp4, mpeg, mpga, m4a, wav, webm | OpenAI audio API |

**Never submit a diarize request > 1400s — it will fail with `audio duration X seconds is longer than 1400 seconds which is the maximum for this model`.** Chunk first, always.

## Audio Compression Floor

Per ERR-20260403-001, compress cautiously. Too aggressive and Whisper hallucinates.

| Duration | Bitrate | Sample Rate | Channels | Expected Size |
|---|---|---|---|---|
| ≤ 30 min | 96 kbps | 44.1 kHz | mono | ~22 MB |
| 30-60 min | 64 kbps | 44.1 kHz | mono | ~22 MB at 47 min |
| 60-90 min | 48 kbps | 44.1 kHz | mono | ~24 MB at 66 min |

**Floor: never go below 44.1 kHz / 48 kbps.** Below that, hallucinations start.

For chunked workflows, total size is not the binding constraint (each chunk fits individually), so you can run higher bitrates if quality matters.

## Speaker Identity Across Chunks (The Hard Part)

`gpt-4o-transcribe-diarize` does NOT persist speaker identity across separate API calls. Each call re-assigns labels (A, B, C, …) based on the order speakers first appear in that chunk.

**Example failure from AXOLTL call:**
- Chunk 1: A=Amyn (greets first), B=Chandler ✓
- Chunk 2: A=**Chandler** (continues his answer from the end of chunk 1), B=Amyn (single "mm-hmm" backchannel), C=Amyn
- Chunk 3: A=**Chandler** (continues monologue), B=Amyn (drops a link), C=Chandler (single stray)

If you blindly map A→Amyn across all chunks, Amyn ends up with 71% of the talk time (wrong — he actually had 35%). Chunk 2 entirely inverts the mapping.

### Two Reconciliation Strategies

**Strategy 1 — Content-cue reconciliation (CURRENT, manual):**
1. After transcription, read the first 3-5 segments of each chunk
2. Identify who is speaking based on content (continuity from prior chunk, topic, tone)
3. Build a per-chunk `speaker_map` dict
4. Apply the map in the merge script

Works reliably for 2-speaker calls. Breaks down at 3+ speakers or rapid-fire turn-taking.

**Strategy 2 — `known_speaker_references[]` (BETTER, not yet implemented):**
1. Extract a 5-10 second reference clip for each known speaker from an early part of the audio (e.g., from the greeting exchange)
2. Base64-encode each clip as a data URL
3. Pass on EVERY chunk request via `--form 'known_speaker_references[]=data:audio/wav;base64,...'` and `--form 'known_speaker_names[]=Amyn'`
4. Every chunk then uses the same speaker IDs (e.g., "Amyn", "Chandler") directly — no remap needed

This is the right long-term approach. Up to 4 named speakers supported. Not implemented yet because the initial extraction of reference clips is a second ffmpeg pass that needs speaker timing. (Could be bootstrapped: transcribe chunk 1 first without references, identify 2 samples from segments where each speaker has a clean utterance, then use those references on chunks 2+N.)

## Cost

Per-chunk cost at 940s:
- Input: ~11K audio tokens + a few hundred text tokens
- Output: ~20K tokens (depends on speech density)
- Total: ~32K tokens per chunk

At current `gpt-4o-transcribe-diarize` pricing, that's **~$0.10-0.20 per chunk**. A 47-minute call (3 chunks) runs ~$0.30-0.60.


## Execution

This skill dispatches to **delivery-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `Audio file path (mp4/m4a/mp3/wav)`
  - `HARBOR_portfolio/<slug>/ (if portfolio-specific; delivery-agent enforces hermetic seal)`

### Step 3 — Dispatch to delivery-agent

Call the **Agent** tool with:

- `subagent_type`: `delivery-agent`
- `description`: `"Transcribe a meeting recording with diarized speaker labels"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/transcribe-meeting <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/transcribe-meeting/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `Diarized Markdown transcript saved to HARBOR_portfolio/<slug>/04-transcripts/<date>-<topic>.md OR admin/logs/formatted_transcripts/ for internal meetings`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

If portfolio meeting: delivery-agent also extracts commitments and updates HARBOR_portfolio/<slug>/commitments.md.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what delivery-agent reads as its authoritative reference when executing this skill.

## Invocation

```
/transcribe-meeting <path-to-audio-or-video> [--speakers "Name1,Name2"]
```

If `--speakers` omitted, the skill will ask via AskUserQuestion for the participant names before uploading.

### What the skill does step-by-step

1. **Validate input** — check file exists, is a supported format, ffmpeg/ffprobe available, `OPENAI_API_KEY` loadable
2. **Extract audio** — run ffmpeg to produce mono 44.1kHz MP3 at the right bitrate for the duration (see table above)
3. **Probe duration** — via ffprobe
4. **Decide chunking** — if duration > 1400s, compute N = `ceil(duration / 940)` chunks of equal length
5. **Split** — if chunking needed, run ffmpeg with `-ss` and `-t` flags for each chunk (use `-acodec copy` for speed)
6. **Upload** — sequentially curl each chunk to `https://api.openai.com/v1/audio/transcriptions` with `model=gpt-4o-transcribe-diarize`, `response_format=diarized_json`, `chunking_strategy=auto`
7. **Verify chunks** — check each chunk's response is valid JSON with a `segments` array
8. **Reconcile speakers** — for chunked runs, read first 5 segments of each chunk, prompt the user via AskUserQuestion to confirm the per-chunk speaker map (or infer from continuity if only 2 speakers and clean turn boundaries)
9. **Merge** — run `scripts/merge_diarized.py` with the reconciled speaker map
10. **Write outputs** — merged JSON, merged MD, README in a `calls/` subfolder next to the input file
11. **Summarize** — report to the user: total duration, speaker turn counts, talk-time ratio, output file paths

## Output Format (the .md file)

```markdown
# <Meeting Title> — Diarized Transcript

**Date:** 2026-04-10
**Duration:** 47 minutes
**Participants:** Amyn Porbanderwala, Chandler Provence
**Source:** gpt-4o-transcribe-diarize, 3x 940s chunks merged

---

**[00:03:12] Amyn:**

Hey brother, how's it going?

**[00:03:14] Chandler:**

Oh, it's going pretty good. How are you doing?

**[00:03:16] Amyn:**

Good, good. How's life?

...
```

Turn grouping rule: consecutive segments from the same speaker merge into a single turn. Timestamps use absolute `HH:MM:SS` from the start of the audio file (not from when speech first occurs — so a 3-minute silent preamble shows the first turn at `00:03:XX`).

## Known Transcription Errors to Watch For

`gpt-4o-transcribe-diarize` is strong but not perfect. Common errors observed in the AXOLTL call:
- Proper nouns get mangled: "Jamil Jaffer" → "Jamal Jaffer", "Anduril" → "Andrel"
- Acronyms pronounced letter-by-letter or as words: "SBIR" → "Sibber"
- Casual profanity is preserved (useful for capturing natural speech)

Always do a pass over the merged MD for proper-noun corrections before using it in a client deliverable.

## See Also

- `ERR-20260403-001` — Whisper hallucinates on over-compressed audio (the 44.1kHz/64kbps floor comes from here)
- `LRN-20260410-006` — the chunking + speaker-identity-across-chunks discovery from the AXOLTL call
- `FEAT-20260403-001` — the original proposal for this skill
- `HARBOR_portfolio/axoltl_chandler/00-sources/calls/merge_diarized.py` — the prototype merge script this skill was built from

## Scripts

The helper scripts live in `scripts/`:

- `extract_audio.sh` — ffmpeg wrapper that picks bitrate based on duration
- `chunk_audio.sh` — splits an mp3 into N chunks of specified length using ffmpeg stream copy
- `upload_chunk.sh` — curl wrapper that posts one chunk to OpenAI and writes the response
- `merge_diarized.py` — merges per-chunk JSONs with per-chunk speaker mapping into the final MD + JSON outputs
