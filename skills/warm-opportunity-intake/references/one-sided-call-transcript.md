# One-Sided Call Transcript Annotation

When only your side of a call is recorded (e.g., speakerphone voice memo, Teams recording with local audio only), the STT output has one speaker and the other person's words are absent.

## Method

### 1. Transcribe via xAI STT
```bash
XAI_KEY=$(grep xai_api_key ~/.env.local | cut -d= -f2)
curl -s -X POST "https://api.x.ai/v1/stt" \
  -H "Authorization: Bearer $XAI_KEY" \
  -F "diarize=true" -F "language=en" -F "format=true" \
  -F "filler_words=false" -F "file=@audio.m4a;type=audio/mp4" \
  -o /tmp/stt.json
```

### 2. Build turns
```bash
python ~/.hermes/skills/productivity/audio-transcription/scripts/build_turns.py \
  /tmp/stt.json --output /tmp/turns.json
```

### 3. Infer what the other person said
Between each of your spoken turns, the other person spoke. Base inference on:
- Your own words ("So you need GIS help?" means they asked about GIS capability)
- The email they sent (has all attachment context)
- Their LinkedIn bio, company website, and the proposal they authored
- Your responses to their unheard questions

### 4. Annotation style in HTML
Use `<div class="context-gap">` blocks with italic gray text:

```html
<div class="context-gap">
  [Name] explains the opportunity: SEARF grant, $655K, due July 31.
  He needs a GIS subcontractor.
</div>
```

### 5. Post-call notes
Add a separate section after the transcript for your personal observations.
Format it differently (colored background, italic prefix) so it's clear these are
not part of the recorded call:

```html
<h2>Post-Call Notes</h2>
<div style="background: var(--g100); border: 1.5px solid var(--oat); border-radius: 14px; padding: 20px 24px; font: 14px/1.6 var(--sans); color: var(--slate);">
  <p><em>[Your personal observations — not part of the call.]</em></p>
</div>
```

## Worked Example

See `~/repos/art-gis-proposal/call-transcript-2026-07-28.html` — Art Trevethan call
where only Amyn's side was recorded. The transcript has 9 turns from Amyn (all
Speaker 0) with context gaps between them showing inferred Art responses.

## Limitations

- Inferred content is NOT verbatim. Do NOT present it as "they said X."
- If your recording missed a critical detail, you won't know. Flag open questions.
- Don't infer specifics that you can't verify — stick to structural gaps (scope,
  timeline, team, budget) that are confirmed by written materials.
