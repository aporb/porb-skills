---
name: tone-strip
description: Final-stage LLM-tell remover and voice-aligner. Strips banned words, em-dash overuse, hedge stacking, corporate jargon. Aligns to Amyn's voice per HARBOR Constitution P7.
version: 1.0.0
tags: [quality, voice, tone, harbor, constitution]
tier: A
owning_profile: writer
moat_test: "Encodes Amyn's specific voice anchors (LinkedIn launch post, recent briefings) + HARBOR banned-word list. Not generic style guidance."
---

# Tone-Strip — DAI Advisor Layer

Inspired by Skyvern's Pangram pattern. Final pass before any deliverable ships externally. Catches the LLM-tells that survive the adversarial reviewer.

## When to load this skill

- AFTER `adversarial-reviewer` returns `verdict: ship` and BEFORE delivery
- On any new LinkedIn / X / blog draft before queueing
- Manual invocation on a one-shot draft

## Banned word/phrase list

Hard banned (replace or remove):
- `delve` / `delving`
- `tapestry`
- `leverage` (as verb) — replace with "use" / "apply" / "draw on"
- `robust` — replace with specifics
- `comprehensive` — replace with "covers X, Y, Z"
- `best-in-class`
- `next-generation`
- `synergy` / `synergistic`
- `ecosystem` (when meaning "set of services") — replace with specifics
- `let's` (as transition)
- `at the end of the day`
- `moving forward` (as transition)
- `in conclusion`
- `it is important to note`
- `it is worth mentioning`
- `furthermore` (often unnecessary)
- `moreover` (often unnecessary)

Soft banned (flag, only replace if context allows):
- `unleash`, `unlock`, `empower`, `streamline`, `optimize`, `revolutionize`

Style flags (warn):
- Em-dash density > 1 per ~500 words → flag
- Hedge stacking ("might possibly perhaps") → flag
- Bare weekday names without dates ("on Thursday" with no date context) → flag (HARBOR §16 gate)

## Workflow

### Phase 1: Scan

Read the draft. Run regex pass for banned terms. Count em-dash density. Detect hedge stacking. List flagged passages with line/section references.

### Phase 2: Replacement

For each hard-banned hit, propose a context-aware replacement. Use cheap-subagent (haiku/flash) — this is mechanical work.

Pass the model the surrounding 2-3 sentences and the banned phrase. Prompt:

```
Replace the banned phrase with a more specific, concrete alternative.
Preserve meaning. Match Amyn's voice (data-driven, federal-domain-expert, no jargon).
Voice anchors below.

[Surrounding text]

Banned phrase: "{phrase}"

Return JSON: {"replacement": "...", "rationale": "...", "confidence": "high|medium|low"}
```

If confidence is "low" on a replacement, flag for human review instead of auto-replacing.

### Phase 3: Voice alignment scan

Compare the draft to voice anchors. Anchors are samples from approved Amyn LinkedIn posts (e.g., the launch post at `linkedin-launch-post-2026-05-12.html`). Cheap subagent prompt:

```
Score the draft for voice alignment (1-5) on:
- specific numbers over adjectives
- concrete examples over abstractions
- federal-domain framing
- short-sentence average

Return JSON: {scores, top_3_passages_off_voice}
```

If overall voice score < 3.5, recommend a heavier rewrite pass (not just word-swap).

### Phase 4: Output

```json
{
  "original_path": "...",
  "edited_path": "...",  // new file with replacements applied
  "changes": [
    {"original": "...", "replacement": "...", "rationale": "..."}
  ],
  "flags": [...],
  "voice_score": 0-5,
  "recommendation": "ship | review-edits | rewrite-pass"
}
```

Write the edited file to `${original_dir}/tone-stripped/${basename}` (preserve original for diff).

### Phase 5: Audit log

Append per-piece tone-edit count to `~/.hermes/state/tone-strip-log.jsonl`. Weekly ops review surfaces trends — "we banned 'leverage' 14 times this week, suggesting voice drift in source drafts".

## Voice anchors (loaded at runtime)

Read these files into context for the voice-alignment scan:
- `/Users/amynporb/Documents/Briefings/linkedin-launch-post-2026-05-12.html` — voice baseline
- `/Users/amynporb/Documents/Briefings/harbor-elevator-pitches-2026-05-14.html` — pitch voice
- Recent daily briefings (last 3) — Hermes' current voice

## Cost economics

Per piece: scan + ~5-15 replacements + voice scan ≈ ~$0.01-0.03.

## Related

- v2.0 §3.5
- HARBOR Constitution P7 (one Amyn voice across platforms)
- MECHANICAL-GATES rows #12 (LLM-tell rejection) and #16 (email-lint editorial rules)
