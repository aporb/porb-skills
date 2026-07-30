---
name: audiobook
description: Produce a multi-voice dramatized audiobook from a KDP-exported HTML book using xAI Grok TTS. Outputs a professional .m4b (Apple Books / Audible-compatible) with embedded chapter + section markers, cover art, and full metadata, plus per-chapter MP3s and a CUE sheet. Validated end-to-end on Book 1 (Shrink-Wrap It) — 7h 33m, ~$3.20 in API spend.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Task, Monitor, TaskCreate, TaskUpdate, TaskList
model: sonnet
---

# /audiobook — KDP HTML → professional multi-voice audiobook

Produces a dramatized, chapter-marked, cover-arted .m4b audiobook from a KDP-exported HTML manuscript. The pipeline lives at `projects/<book>/audiobook-xai/` and was validated end-to-end on Shrink-Wrap It (Book 1) on 2026-05-09.

## How It Works

A 5-stage pipeline:

1. **Analyze** — bs4 walks the KDP HTML, builds chapter map, counts tables/lists, estimates spoken duration + cost.
2. **Preprocess** — emits `[NARRATOR]`-tagged markdown drafts per chapter with pre-normalized numbers (dollar amounts spelled out, route/time numbers spelled, GovCon acronyms forced letter-by-letter).
3. **Cast + script** — for each chapter's opening vignette, hand-edit the draft to assign character voices. All other turns stay `[NARRATOR]`.
4. **Synthesize** — per-turn xAI TTS calls (`POST https://api.x.ai/v1/tts`), one voice per turn, SHA-cached for cheap iteration. Inter-turn silences inserted by ffmpeg.
5. **Stitch + M4B** — concat per-turn → per-chapter mp3 → master.mp3, then transcode to AAC and assemble a .m4b with cover art, full metadata, H1 chapter markers, and H2 section markers.

## Execution (pure tool)

This skill is a **mechanical wrapper** with project-local cognitive content. See `.claude/skills/SKILL-PATTERN.md` Tier D.

**Rationale:** the synthesis, stitching, and M4B assembly are deterministic. The cognitive work (cast decisions, dialogue hand-editing, pronunciation overrides) lives as project artifacts (`cast.json`, `scripts/ch-NN-final.md`, `scripts/06_html_to_script.py` overrides). When invoked, this skill dispatches against those artifacts. For a NEW book without an existing cast, this skill must AskUserQuestion through the cast-decision step rather than guessing.

The procedural playbook below is the tool contract.

## Critical lessons from Book 1 production (read before invoking)

These are the bugs that cost real money or sounded wrong, all now fixed in the v1 scripts. Don't re-discover them.

### `text_normalization` MUST be `false`
xAI's text_normalization parameter, when `true`, **reads bracketed inline tags as literal text**. A test run with `text_normalization: true` and `[long-pause]` tags produced an audiobook that opened with the spoken words "long pause long pause." Verified by probing same input with both flag values: 129 KB (true) vs 92 KB (false), a 37 KB delta consistent with the model speaking the bracketed tag names.

**Compensate by pre-normalizing numbers in source text.** `06_html_to_script.py` does this via regex (dollar amounts, times, route numbers, percentages). New books should extend the regex map.

### `[pause]` tags work but spaces matter
`[pause]` is honored when surrounded by spaces (`text. [pause] text`), partially honored without (`text.[pause]text`), and **stacked at start of text fails** (`[long-pause][long-pause]Hello` produces shorter audio than baseline — parser collapses or fails). Don't stack pause tags. Trust punctuation for most prosody.

### Drop redundant dialogue tags
Multi-voice production renders `she said` / `he said` redundant — voice change IS the cue. The `[NARRATOR]` only owns dialogue tags that carry emotional or stage information (`Rachel's voice was careful now`, `he leaned back, chair springs creaking`). Bare attribution gets dropped. This is the lever that makes dramatized audiobooks feel like film instead of "AI-narrated text."

### Position-based caching breaks on edits
Filename-based cache (`turn-005-narrator.mp3`) breaks when scripts get re-edited because adding/removing turns shifts indices. **The fix in `05_multivoice.py` is SHA-sidecar caching**: each segment writes a `.sha256` file with `hash(voice + text)`. Re-runs reuse only segments whose hash matches. Backfill sidecars for existing segments BEFORE editing scripts; otherwise everything re-synths.

### Compound modifiers + section titles need a hand-fix
Auto-normalization of "$75 million IT services firm" produces "seventy-five million dollars IT services firm" (ungrammatical). And titles like "$102.3 Billion Reality" become "one hundred two point three billion dollars Reality" — section header H2 match fails. Both need hand-fixes during script review. v3 fix: fuzzy-match on un-normalized stem.

### Voice scarcity → smart reuse, not wasted dramatization
xAI provides 5 stock voices; a typical book has 25-40 named characters. **Reuse voices across non-overlapping scenes** (Rachel in Ch 1, Jennifer in Ch 14, Patricia in Ch 14 §2 — all on Ara, never share a scene). Document the casting decisions in `cast.json` per character with `first_seen` and reuse rationale. Listeners disambiguate via narrator-spoken character names.

### Chapter-opening vignettes carry the dramatization
Each chapter's first ~15-25 paragraphs is a dramatic vignette; the rest is analytical prose. Multi-voice on the openings is high-leverage. Multi-voice on every quoted phrase mid-chapter is diminishing returns and exhausting to hand-edit. The Book 1 pattern (only openings dramatized) was the right scope.

## Prerequisites

- `uv` available on PATH (creates ephemeral envs for bs4 + requests + python-dotenv)
- `ffmpeg` 6+ on PATH (for concat + AAC transcode + M4B assembly)
- `XAI_API_KEY` (or `xAI_API` legacy var) in repo-root `.env`
- Cover image at known path (recommended: project's `apple-books/covers/apple-inbook-cover.jpg`)

## Project layout

The pipeline expects a self-contained sub-project at `projects/<book>/audiobook-xai/`:

```
projects/<book>/audiobook-xai/
├── PLAN.md                   ← production plan, voice rules
├── README.md                 ← run instructions
├── cast.json                 ← canonical character → voice map
├── reading-notes/            ← per-chapter scene/cast catalogs
│   └── master-cast.md
├── scripts/
│   ├── 01_analyze_html.py    ← HTML → analysis.json
│   ├── 02_preprocess.py      ← HTML → cache/ch-XX-NN.txt (legacy v1 chunker)
│   ├── 03_synthesize.py      ← legacy v1 unary synth
│   ├── 04_stitch.py          ← legacy v1 per-chapter stitch
│   ├── 05_multivoice.py      ← speaker-segment synth (active)
│   ├── 06_html_to_script.py  ← HTML → [NARRATOR]-tagged draft (active)
│   ├── 07_stitch_master.py   ← master.mp3 stitcher
│   ├── 08_build_m4b.py       ← .m4b with chapter + section markers
│   ├── ch-NN-final.md        ← actual hand-edited multi-voice scripts
│   └── section-NN-script.md  ← original test sample(s)
├── cache/                    ← preprocessed text + sha sidecars
├── output/
│   ├── shrink-wrap-it-audiobook.m4b   ← deliverable
│   ├── master.mp3                     ← MP3 fallback
│   ├── master.cue                     ← CUE sheet
│   ├── manifest.json                  ← nav structure
│   ├── analysis.json                  ← chapter map + cost estimate
│   ├── ch-NN-full.mp3                 ← per-chapter masters
│   ├── m4a/ch-NN.m4a                  ← AAC transcodes
│   └── segments/ch-NN-full/           ← per-turn caches + sidecars
└── logs/
    ├── usage.jsonl                    ← every API call
    └── ch-NN-run.log
```

## Casting strategy (the permanent rules)

xAI's 5 stock voices: `eve` (energetic F), `ara` (warm F), `rex` (confident M business), `sal` (smooth balanced), `leo` (authoritative M).

**Permanent rules:**
1. NARRATOR is ALWAYS rex. Switching narrators across chapters breaks listener trust.
2. Within any single scene, every character must use a different voice. No exceptions.
3. Across non-overlapping scenes, voices may repeat. Document the reuse in `cast.json`.
4. Archetype consistency: leo = "executive in the hot seat", ara = "competent woman", eve = "authority figure / Navy / federal CO", sal = "second-in-command / advisor / federal PM".
5. Walk-on characters with ≤2 lines may stay [NARRATOR] (Rex reads them). Don't blow voice slots on minor roles.

For a NEW book, build the master cast BEFORE any synthesis. Read every chapter opening, catalog speakers, save to `reading-notes/master-cast.md` and `cast.json`. This step can take 30-60 min of reading per book.

## Workflow — full book from scratch

### Step 1: Analyze
```bash
cd projects/<book>/audiobook-xai
uv run --quiet --with beautifulsoup4 --with lxml \
    scripts/01_analyze_html.py ../kdp/output/kdp-ebook.html
```
Outputs `output/analysis.json`. Reports chapter count, total chars, est. duration, est. cost.

### Step 2: Preprocess all chapters to draft scripts
```bash
for ch in $(seq 1 14); do
  uv run --quiet --with beautifulsoup4 --with lxml \
      scripts/06_html_to_script.py ../kdp/output/kdp-ebook.html \
      --chapter $ch --out scripts/ch-$(printf '%02d' $ch)-final.md
done
```
Produces all-`[NARRATOR]` drafts with normalized numbers + acronyms.

### Step 3: Read every chapter opening, build the cast
**This is the slow cognitive step.** AskUserQuestion if no `cast.json` exists. Read the HTML opening (h1 to first h2) for each chapter. For each named speaker, catalog:
- Name + role + chapter first appearance
- Voice assignment (Leo/Ara/Eve/Sal — never Rex)
- Within-scene differentiation: confirm no two simultaneous speakers share a voice

Save findings to `reading-notes/master-cast.md` and `cast.json`. The `cast.json` keys are the `[SPEAKER]` tags used in scripts; values are voice IDs.

### Step 4: Hand-edit each chapter's opening into multi-voice
For each chapter, replace the auto-generated `[NARRATOR]`-only opening (from chapter h1 down to first h2) with a hand-edited multi-voice version:

- Split paragraphs that mix narration + dialogue into separate turns
- Strip bare dialogue tags (`he said`, `she said`); keep emotional/stage tags
- Verify number normalizations look right
- Each character gets the correct `[SPEAKER]` tag from `cast.json`

This took ~10-15 min per chapter for Book 1.

### Step 5: Synthesize all chapters in parallel
```bash
for ch in $(seq -f '%02g' 1 14); do
  uv run --quiet --with requests --with python-dotenv \
      scripts/05_multivoice.py scripts/ch-${ch}-final.md \
      --out output/ch-${ch}-full.mp3 > logs/ch-${ch}-run.log 2>&1 &
done
```
Then **use the Monitor tool** to wait for all `pgrep -f 05_multivoice` to clear. Don't poll. Don't sleep. ~10-25 min total wall time depending on concurrency.

### Step 6: Build the M4B
```bash
uv run --quiet scripts/07_stitch_master.py    # rebuilds master.mp3
uv run --quiet --with beautifulsoup4 --with lxml scripts/08_build_m4b.py
```
Outputs `output/<slug>-audiobook.m4b` with H1 chapter markers + H2 section markers + cover art + full metadata.

## Workflow — iterating after listening

If Amyn listens and finds a problem, the SHA cache makes per-segment iteration cheap (~$0.001 per regenerated turn).

### Recasting one character (voice change)
1. Edit `cast.json` to change the character's voice.
2. Re-run `05_multivoice.py` for affected chapters. SHA cache invalidates only that character's turns.
3. Re-run `07_stitch_master.py` and `08_build_m4b.py`.

### Fixing one mispronounced phrase
1. Edit the relevant `scripts/ch-NN-final.md` line (e.g., force "C-LIN" → "C L I N").
2. Re-run `05_multivoice.py` for that chapter. SHA cache regenerates only the changed turn.
3. Re-run `07_stitch_master.py` and `08_build_m4b.py`.

### Adding a missing pronunciation override globally
1. Edit `scripts/06_html_to_script.py`'s `ACRONYM_OVERRIDES` map.
2. Re-run `06_html_to_script.py` for ALL chapters (overwrites the all-NARRATOR drafts).
3. Re-apply hand-edits to opening vignettes (this is destructive — keep `scripts/ch-NN-final.md` under git; revert overwritten openings via `git restore`).
4. Re-run `05_multivoice.py` per chapter.

## Cost & duration expectations

Validated on Book 1 (Shrink-Wrap It, 56k words, 14 chapters):

| Phase | Cost | Wall time |
|---|---|---|
| Initial all-NARRATOR synthesis | ~$1.71 | ~15 min (12 chapters parallel) |
| Re-synth with multi-voice openings | ~$1.47 | ~17 min (12 chapters parallel) |
| Stitch + M4B | $0 | ~2 min |
| **Total per full book** | **~$3.20** | **~35 min** |

Per-segment iteration is essentially free (~$0.001 per turn).

## Hard constraints

- **Never set `text_normalization: true`.** Pre-normalize in source instead.
- **Never push pause tags as `[long-pause][long-pause]`.** Single tag with spaces around it.
- **Never overwrite hand-edited `ch-NN-final.md` without backing it up first.** The opening vignettes are the most expensive cognitive artifact in the project.
- **Never invent a pronunciation override without testing.** The override map in `06_html_to_script.py` should grow only after empirical evidence the model gets a term wrong.
- **Never skip the cover-art embed for a final M4B delivery.** Apple Books renders without it but it looks unprofessional.
- **Never declare the book "done" without a master.mp3 stitch + M4B build + manifest.json regeneration.** All three must reflect the same content. The M4B builder owns the canonical manifest.

## Test sample for new pipelines

Before committing to a full book, do a smoke test on one chapter's opening:
1. Hand-edit just one chapter's opening into multi-voice (~5 min).
2. Run `05_multivoice.py` on that one chapter (~$0.05).
3. Stitch with `04_stitch.py --chapter N`.
4. Listen. Confirm voices, prosody, pronunciation.
5. Only then proceed to the full book.

This was the protocol that caught the `text_normalization=true` bug for Book 1.

## Reference: Book 1 final state

- M4B: `projects/book1-shrink-wrap-it/audiobook-xai/output/shrink-wrap-it-audiobook.m4b`
- Duration: 7h 33m
- Size: 427 MB
- Markers: 14 H1 + 92 H2 = 106 nav points
- Cast: 38 named characters across 5 voices
- Total xAI spend: $3.18
- Voice cast canonical doc: `~/.claude/projects/-Users-amynporb-Documents--Projects-2026-books/memory/audiobook_xai_cast.md`
- Pronunciation rules: `~/.claude/projects/-Users-amynporb-Documents--Projects-2026-books/memory/audiobook_xai_pronunciation.md`
