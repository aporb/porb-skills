---
name: daily-briefing
description: Generate HARBOR's daily briefing for Amyn Porbanderwala — comprehensive morning executive briefings (markets, defense, SBIR, synthesis) and focused engagement briefs (X/LinkedIn content calendars, draft posts). HTML output with dark theme, two-voice MP3 narration for daily variant.
version: 1.0.0
tags: [briefing, daily, cron, harbor, news, markets, federal-contracting]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Daily Briefing

Generates a comprehensive morning briefing HTML for Amyn Porbanderwala, delivered via cron. Covers four domains, uses browser-based news gathering (NOT web_search), and produces a dark-themed, mobile-readable HTML file.

## When to load this skill

- Running the daily briefing cron job
- Any "morning briefing" or "daily report" request for HARBOR
- User asks for a structured executive summary covering markets + federal contracting + personal knowledge

## Workflow

### Phase 0: Dedupe + Live Infra Snapshot (run BEFORE drafting)

**Two deterministic steps. Both run before Phase 1 research.**

**0a. Refresh infra snapshot.** Run the snapshot script so the Personal Knowledge card has live numbers (not hardcoded):
```bash
bash /Users/amynporb/.hermes/scripts/infra-snapshot.sh
```
This writes `~/.hermes/cache/infra-snapshot.json`. The Personal Knowledge card later in Phase 2 reads from this file. **Never hardcode profile/chunk/cron counts** — read from the JSON. If the JSON is stale (>24h) or missing fields, render "⚠️ infra snapshot stale" instead of guessing.

**0b. Dedupe story candidates against last 3 dailies.** Once Phase 1 has produced candidate stories, batch them through the dedupe script:

**When to dedupe:** Only when Phase 1 produces a STRUCTURED candidate list with consistent titles (e.g., from `session_search` of prior briefings, or from a pre-scraped URL list). For ad-hoc browser scraping where stories are gathered from multiple pages with inconsistent titles (e.g. "CNBC Daily Open..." vs "Oil prices fall..."), dedupe is impractical — the candidate list would need manual normalization first. In those cases, rely on the agent's own judgment: check `session_search` for recently-run stories and avoid verbatim repeats.

**Dedupe command:**
```bash
# Write candidates to /tmp before Phase 2 composition
python3 -c '
import json
candidates = [
    {"id":"story-1","title":"...","excerpt":"..."},
    # ... one entry per story Phase 1 found
]
json.dump(candidates, open("/tmp/daily-candidates.json","w"))
'

# Run dedupe (uses Hermes venv Python for sentence_transformers)
/Users/amynporb/.hermes/hermes-agent/venv/bin/python3 \
  /Users/amynporb/.hermes/skills/productivity/daily-briefing/scripts/dedupe.py \
  --candidates /tmp/daily-candidates.json \
  --out /tmp/daily-decisions.json \
  --threshold 0.85
```

Apply the decisions in Phase 2 composition:
- `verdict: "suppress"` → omit entirely from today's brief (it ran yesterday or 2 days ago with no material update)
- `verdict: "update"` → render under a small "Updates on prior stories" callout with explicit "what changed in last 24h"
- `verdict: "fresh"` → render as a new top-level story

Save the decisions JSON to the cron output dir for retrospective tuning:
```bash
cp /tmp/daily-decisions.json ~/.hermes/cron/output/${HERMES_CRON_ID:-manual}/dedup-decisions-$(date +%Y-%m-%d).json
```

**Why this matters:** v2.0 Section 1 Initiative 1.2. Output quality / reader trust. Briefings 5/22-5/25 repeated stories verbatim. Dedupe ends that.

### Phase 0.5: Eval-Gate Score (side-by-side, do not block)

**Run the harbor-eval-gate on the briefing text BEFORE writing the HTML.** This is the side-by-side gate from the eval-loop action plan. The score is logged but does NOT block the briefing from shipping. After 7 days of data, recalibrate the threshold.

**Step 1.** After Phase 2 composition, before `write_file`, extract the briefing body text to a temp file:

```bash
# Save the briefing body to a temp file
# (extracted from the in-progress HTML — strip the HTML tags)
python3 -c '
import re
html = """..."""   # the assembled HTML
text = re.sub(r"<[^>]+>", " ", html)
text = re.sub(r"\s+", " ", text).strip()
open("/tmp/daily-briefing-body.txt", "w").write(text)
print(f"Wrote {len(text)} chars")
'
```

**Step 2.** Score it:

```bash
python3 ~/.hermes/skills/harbor-eval-gate/scripts/eval_gate.py \
  --candidate-file /tmp/daily-briefing-body.txt \
  --benchmark ~/.hermes/skills/harbor-eval-gate/benchmark/benchmark-v0.yaml \
  --graders "google/gemini-2.5-flash" \
  --quiet
```

The script prints `PASS 0.945 (threshold 0.7)` to stderr. The exit code is 0 (PASS) or 1 (FAIL).

**Step 3.** Add a small badge to the briefing HTML header so the score is visible:

```html
<div class="eval-badge" style="display:inline-block;padding:0.2rem 0.6rem;
  border-radius:6px;font-size:0.7rem;background:rgba(212,168,83,0.15);
  color:#d4a853;border:1px solid rgba(212,168,83,0.3);">
  Eval: PASS · 0.945 / 0.7
</div>
```

**Step 4.** Append a one-liner to the briefing footer with the score, lowest metric, and the gate's rationale:

```
Eval: PASS · composite 0.945 · threshold 0.7 · weakest: positioning_fit (0.85)
```

**What this does NOT do:** The gate does NOT block the briefing. It scores, badges, and logs. The action plan is explicit: "run side-by-side for 7 days, no publishing changes." The data accumulates; the threshold recalibrates; only then does blocking become a decision.

**What this DOES do:** Every daily briefing is now scored. Every score is in the JSONL log. The weekly meta-loop (cron: `harbor-eval-meta`, Mondays 9 AM) harvests the fails and appends them to the benchmark. The benchmark compounds. The system gets sharper.

**The honest failure mode:** If the gate grades something the user would have published as PASS, the gate is calibrated. If the gate grades something the user would have killed as FAIL, the gate is calibrated. If neither, the benchmark needs more reference cases. Review the JSONL weekly.

### Phase 1: Research (parallel where possible)

**Markets** — navigate to CNBC individual quote pages for live indices and key rates (MarketWatch is DataDome-blocked — see pitfall below). Navigate ALL SIX in parallel at the start of Phase 1:
```
browser_navigate → https://www.cnbc.com/quotes/.SPX   (S&P 500)
browser_navigate → https://www.cnbc.com/quotes/.IXIC  (NASDAQ)
browser_navigate → https://www.cnbc.com/quotes/.DJI   (Dow)
browser_navigate → https://www.cnbc.com/quotes/.VIX   (Volatility)
browser_navigate → https://www.cnbc.com/quotes/US10Y   (10-Year Treasury yield)
browser_navigate → https://www.cnbc.com/quotes/@CL.1   (WTI Crude front-month)
```
Each quote page reliably returns the current price, change, and 52-week range in the snapshot.

**Tech/Business News** — navigate to CNBC (Reuters is DataDome-blocked — see pitfall):
```
browser_navigate → https://www.cnbc.com/technology/
```
Scroll down for "MORE IN TECH" and "TRENDING NOW" sections. Capture 8-10 top stories. Look for: AI, semiconductors, Big Tech, policy, earnings, M&A.

**Politics / EO Coverage** — navigate to CNBC Politics (Federal Register is fully blocked — see pitfall):
```
browser_navigate → https://www.cnbc.com/politics/
```
Capture: White House, Congress, policy stories. Look for executive order news, appropriations, federal workforce, regulatory changes. CNBC Politics carries EO coverage and DHS/funding stories that substitute for Federal Register access.

**Defense/Geopolitical** — navigate to:
```
browser_navigate → https://www.defensenews.com/
```
Capture: Pentagon, Congress, industry, international. Scroll for most-popular and special features.

**⚠️ Defense News may time out** — `defensenews.com` can return "Operation timed out" under load. If it fails, use:
```
web_search("defense news today PENTAGON latest")
```
Or try `web_search("site:insidedefense.com Pentagon latest")` for detail. InsideDefense.com is published daily (e.g. "Inside the Pentagon - May 28, 2026") and carries procurement/R&D/budget stories that substitute well.

**Federal Register** — FULLY BLOCKED as of May 2026 (see pitfall below). Skip entirely.
Use prior briefing knowledge and session_search for EO continuity. CNBC Politics section for policy news.

**SBIR/STTR** — navigate to:
```
browser_navigate → https://www.sbir.gov/
```
Capture open topics, deadlines, reauthorization status.

**Personal Knowledge** — use session_search to find yesterday's briefing and recent activity:
```
session_search(query="daily briefing OR harbor OR recent activity", limit=3)
```

**Weather** — if easily available, include in header. Otherwise skip.

### HTML Generation — Use `write_file`, not `execute_code` with f-strings

CSS uses `{}` curly braces extensively, which conflicts with Python f-string `{}` interpolation. **Writing HTML inside `execute_code` with an f-string will crash:**

```python
# ❌ CRASHES — CSS {} conflicts with f-string {pad:ding}
execute_code("html = f'''... .header{padding:32px}...'''")

# ✅ WORKS — use write_file directly
write_file("~/Documents/Briefings/daily-YYYY-MM-DD.html", "<!DOCTYPE html>...")
```

Use `write_file` with a raw string (no f-string subtitution needed since the date is the only dynamic value and it's in the filename). If you must parameterize, use `str.replace()` on the template after loading it as a raw string.

### HTML Generation Pattern

**HTML Design System** (dark theme, HARBOR blue accent):
- Background: `#08090a` (deepest), `#0f1011` (panel), `#1a1b1e` (elevated)
- Text: `#f0f1f3` (primary), `#c4c7cc` (secondary), `#71767d` (tertiary)
- Accent: `#2563eb` (HARBOR blue), `#3b82f6` (bright)
- Fonts: Inter (primary), JetBrains Mono (data/code)
- Status colors: `#10b981` (green/up), `#ef4444` (red/down), `#f59e0b` (amber)
- Cards: `1px solid rgba(255,255,255,0.06)`, `border-radius: 8px`
- Section dots: blue (news), cyan (contracting), violet (personal), amber (synthesis)
- Pulse animation on header for "live" feel
- Market bar: 6 cards in a row with monospace values
- Story grid: responsive `auto-fit, minmax(300px, 1fr)`
- Breaking stories: red left-border + subtle red background
- EO cards: left-border accent, monospace EO number
- Opportunity table: clean bordered table with status badges
- Synthesis cards: color-coded borders (green=opportunity, red=risk, blue=action)
- Action list: bullet items with blue dot markers

Full design reference loaded during generation via: `skill_view(name="popular-web-designs", file_path="templates/linear.app.md")`

**Structure** — six sections in order:
1. **News & Markets** (top) — 10 story cards + market bar + 6-index market bar
2. **Tech & AI** — 8-10 tech/AI/semiconductor story cards (AI capex, chip stocks, platforms, earnings)
3. **Defense & Geopolitics** — 8-10 defense/geopolitical story cards (Epic Fury aftermath, NATO, counter-drone, Iran, Russia, Taiwan)
4. **HARBOR Federal Contracting** (middle) — 6-8 contract stories + EO Digest cards + SBIR Opportunity Tracker table
5. **Personal Knowledge** (lower middle) — 4 cards: Hermes activity, vault, infra, calendar

   **CRITICAL: All numeric values for the Hermes Activity + Infrastructure cards come from the live snapshot at `~/.hermes/cache/infra-snapshot.json` (refreshed in Phase 0a). DO NOT HARDCODE.**

   Schema you can rely on:
   - `profiles.count` — total Hermes profiles
   - `skills.count` — total SKILL.md files under `~/.hermes/skills/`
   - `rag.chunks` + `rag.source` — pgvector chunk count and where it was read from
   - `gateway.status` + `gateway.uptime_seconds` — daemon state
   - `cron.total_enabled` + `cron.ok_24h` + `cron.failed_24h` + `cron.stale_24h` — cron health summary
   - `cron.jobs` — per-job last_run_at + last_status
   - `briefings.last_daily_date` + `briefings.last_engagement_date` — last produced briefings (sanity check vs today)
   - `errors[]` — any non-fatal snapshot warnings to surface as a small footnote

   If the snapshot is missing (`errors` contains "chunk_count: unable to read"), render the affected field as "⚠️ unavailable" rather than guessing or pulling from memory.

6. **Strategic Synthesis** (bottom) — 2 opportunities, 2 risks, 2 cross-domain signals + 6 action items

### Phase 3: Audio Narration (Two-Voice MP3)

**Generate AFTER the HTML is complete.** Produces a podcast-style spoken MP3 with two alternating voices.

**Voice Pairing** — xAI TTS provider with two voices, roughly 50-50 split. Full voice catalog: `references/xai-tts-voices.md`.

| Role | Voice | Tone | Covers |
|------|-------|------|--------|
| Anchor (male) | `leo` | Authoritative, commanding | Opening, markets, top headlines |
| Analyst (female) | `ara` | Warm, balanced, conversational | Federal contracting, strategic synthesis, close |

Narration structure (90-120 seconds at 1x, then speed to 1.15x, target ~80s at 1.15x):
1. **Leo** (~50%): "HARBOR Daily Briefing. [Date]." → Market snapshot → 3-4 top headlines → action items + sign-off
2. **Ara** (~50%): Federal contracting highlights → SBIR deadlines → Strategic takeaways

Allocate ~700-800 chars per voice segment (roughly 140-160 words) for the total 80s target. The confirmed rate is ~17.6 chars/sec at 1.15x speed. At that rate:

| Target length | Total chars (both voices) | Per voice segment |
|---------------|---------------------------|-------------------|
| ~80s at 1.15x | ~1,400-1,600 chars | ~700-800 chars each |
| ~100s at 1.15x | ~1,700-1,900 chars | ~850-950 chars each |
| ~2:00 at 1.15x | ~2,100-2,400 chars | ~1,050-1,200 chars each |

Real-world calibration from daily-2026-05-27 run: 2,360 chars total (Leo: ~1,120, Ara: ~1,240) = 134s at 1.15x = ~17.6 chars/sec. Aim for roughly equal length between voices for balanced pacing.

**Generation steps (xAI TTS with Python urllib — confirmed working May 2026):**

1. Write two separate narration scripts (~140-160 words or ~700-800 chars each, conversational, no markdown, save to `/tmp/script-leo.txt` and `/tmp/script-ara.txt`)
2. Generate both segments with a Python script (avoids shell escaping issues entirely):

```python
import json, urllib.request, subprocess, os

API_KEY = subprocess.run("grep XAI_API_KEY ~/.hermes/.env | cut -d= -f2",
    shell=True, capture_output=True, text=True).stdout.strip()

def generate_tts(text, voice, model, output_path):
    # CONFIRMED WORKING as of May 2026: use "model"+"voice" NOT "voice_id"
    # Voices: leo (male), ara (female), eve
    payload = json.dumps({
        "model": model,       # "grok-2-audio-preview"
        "voice": voice,       # "leo", "ara", or "eve"
        "text": text.strip(),
        "language": "en",
        "response_format": "mp3"
    }).encode()
    req = urllib.request.Request("https://api.x.ai/v1/tts", data=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(output_path, "wb") as f: f.write(resp.read())
    print(f"  {voice}: {os.path.getsize(output_path)//1024}KB")

leo_text = open("/tmp/script-leo.txt").read().strip()
ara_text = open("/tmp/script-ara.txt").read().strip()
generate_tts(leo_text, "leo", "grok-2-audio-preview", "/tmp/part1.mp3")
generate_tts(ara_text, "ara", "grok-2-audio-preview", "/tmp/part2.mp3")
```

3. Concat + 1.15x speed:
```bash
echo "file '/tmp/part1.mp3'" > /tmp/concat.txt
echo "file '/tmp/part2.mp3'" >> /tmp/concat.txt
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt \
  -filter:a "atempo=1.15" -ar 24000 -b:a 128k \
  ~/Documents/Briefings/daily-YYYY-MM-DD.mp3
rm /tmp/part1.mp3 /tmp/part2.mp3 /tmp/concat.txt /tmp/script-leo.txt /tmp/script-ara.txt
```

**Verified voice catalog (May 2026):** `leo` (male), `ara` (female), `eve` — all return HTTP 200 on `grok-2-audio-preview`. OpenAI-style voices (`alloy`, `ash`, `ballad`, `onyx`, `verse`) return `Voice 'X' not found` even with the correct payload. Stick to `leo`/`ara`/`eve`.

API key location: `grep XAI_API_KEY ~/.hermes/.env | cut -d= -f2`. Use curl directly — the `text_to_speech` tool may use a pre-xAI-TTS-launch endpoint that returns OGG only. Direct curl gives MP3 output and better error visibility.

**Output**: `~/Documents/Briefings/daily-YYYY-MM-DD.mp3`

### Phase 4: Save & Deliver

**File path**: `~/Documents/Briefings/daily-YYYY-MM-DD.html`

**Directory**: Create if missing:
```bash
mkdir -p ~/Documents/Briefings
```

**Verification**:
```bash
ls -la ~/Documents/Briefings/daily-$(date +%Y-%m-%d).html
```

**Delivery**: The final response is the text summary (5-8 bullets) with MEDIA: paths for BOTH the HTML and MP3 files. The cron system auto-delivers to Telegram. Do NOT use send_message.

## Support Files

- `references/xai-multi-segment-podcast.md` — Multi-segment xAI TTS podcast (v2, May 2026): concat-first-then-speed pattern, speech tags, Discord delivery. **Use this for all multi-segment podcasts.**
- `references/discord-media-delivery.md` — Discord 8MB file limit, compression recipes, `media.allow_dirs` config, delivery checklist
- `references/multi-segment-podcast.md` — Legacy edge-tts multi-segment pattern (superseded by xai-multi-segment-podcast for xAI voice quality)

## ⚠️ PITFALL: web_search / web_extract Behavior

`web_search` and `web_extract` now auto-fall-over at the tool layer (firecrawl
→ serper → brave-free → tavily → perplexity for search; firecrawl → tavily for
extract). Most "Payment Required" failures are absorbed transparently. Check
`_meta.attempts` in the response — if `_meta.provider == "serper"` or any
non-firecrawl name, the chain handled it and results are good.

**Only when** `success: false` AND `_meta.attempts` shows every chain provider
failed, escalate to browser-based gathering. For daily briefing news, `browser_navigate` directly to:
- `https://www.cnbc.com/quotes/.SPX` — S&P 500 (also .IXIC, .DJI, .VIX) — live market data
- `https://www.cnbc.com/markets/` — bonds, commodities, currencies headlines
- `https://www.cnbc.com/technology/` — tech/business news
- `https://www.defensenews.com/` — defense
- `https://www.sbir.gov/` — SBIR opportunities (landing page only; topic search is JS-dependent)
- Federal Register and MarketWatch are DataDome-blocked — skip entirely (see pitfalls below)

Use `browser_scroll` to get more headlines from each page. Extract content from the accessibility snapshots.

## ⚠️ PITFALL: Reuters Blocks Browser Automation (DataDome)

`https://www.reuters.com/technology/` now returns a DataDome "Verifying the device..." challenge page when accessed via `browser_navigate`. The page is effectively unreadable — only a "Verifying the device..." heading renders. **Do not waste time retrying Reuters.**

Workaround: CNBC (`https://www.cnbc.com/technology/`) fills the same niche with equally rich tech/business coverage and works reliably via browser_navigate. Scroll down for "MORE IN TECH" and "TRENDING NOW" sections for additional stories.

## ⚠️ PITFALL: MarketWatch Blocks Browser Automation (DataDome)

`https://www.marketwatch.com/` now returns a DataDome "Device Check" iframe, same as Reuters. The page is unreadable — only a DataDome ID string renders. **Do not waste time retrying MarketWatch.**

Workaround: CNBC individual quote pages return live market data reliably:
- `https://www.cnbc.com/quotes/.SPX` — S&P 500 price, change, 52W range, key stats
- `https://www.cnbc.com/quotes/.IXIC` — NASDAQ Composite
- `https://www.cnbc.com/quotes/.DJI` — Dow Jones Industrial Average
- `https://www.cnbc.com/quotes/.VIX` — CBOE Volatility Index

Each quote page snapshot includes the current price, directional arrow, percentage change, 52-week range, and key stats table. Navigate to all four in parallel at the start of Phase 1. CNBC's Markets page (`https://www.cnbc.com/markets/`) also carries bond yield headlines, commodity news, and currency stories.

## ⚠️ PITFALL: CNBC Quote Pages May Time Out Unpredictably

VIX (`/quotes/.VIX`), 10-Year Treasury (`/quotes/US10Y`), and WTI Crude (`/quotes/@CL.1`) quote pages sometimes time out under `browser_navigate` — returning "Operation timed out" even with a generous timeout. The index pages (S&P, NASDAQ, Dow) are more reliable.

**Workaround**: Navigate to the 3 index pages first. If any of VIX/10Y/WTI time out, fall back to `web_search` for those values:

```python
# Example: VIX fallback
web_search("CNBC VIX CBOE volatility index today")
# Results include CNBC quote page data in the snippet (open, prev close, 52W range)
```

Confirmed reliable sources for each fallback:
- **VIX**: `web_search("VIX CBOE Volatility Index - CNBC quote")` — Google SERP snippet usually shows Open, Prev Close, Day High/Low
- **10Y**: `web_search("Market Yield on U.S. Treasury Securities at 10-Year Constant")` — FRED.gov DGS10 snippet shows latest close and recent values
- **WTI Crude**: `web_search("Crude Oil WTI Futures")` — Investing.com or Barchart data available in snippets

Do not retry the timed-out URL more than once. If web_search fails too, leave the market card value as "unavailable" with the `.flat` CSS class.

## ⚠️ PITFALL: CNBC Markets Page — Bond/Commodity Data Invisible in Snapshots

The CNBC Markets page (`https://www.cnbc.com/markets/`) loads bond yields, commodities, and currency data dynamically via JavaScript. These values are NOT visible in browser snapshots — the snapshot will show the major index table (S&P, Nasdaq, Dow, VIX, FTSE, Nikkei, etc.) but the bonds/commodities sections below will be empty or missing.

**Workaround**: Navigate to individual CNBC quote pages for bonds and commodities:
- `https://www.cnbc.com/quotes/US10Y` — 10-Year Treasury yield, change in basis points
- `https://www.cnbc.com/quotes/@CL.1` — WTI Crude front-month futures, price + volume

These quote pages return the full price, change, and stats table in the snapshot — same reliability as the index quote pages. Navigate to them in parallel with the index pages during Phase 1.

## ⚠️ PITFALL: Federal Register Fully Blocked (Access Gate)

As of May 2026, ALL Federal Register URLs (including the main page, `/presidential-documents`, and individual document pages) return a "Request Access" gate with a disabled button. The browser automation IP is blocked. **Do not attempt Federal Register navigation — it will always fail.**

Workaround: rely on prior briefing knowledge for EO continuity, CNBC/Defense News for policy coverage, and session_search for recent EO summaries. If a specific EO's full text is needed, try alternate sources like whitehouse.gov or congress.gov rather than federalregister.gov.

## ⚠️ PITFALL: xAI TTS 429 May Be Credits Exhaustion, Not Rate Limit

The Hermes TTS tool reports `429 Client Error: Too Many Requests` for xAI, but the **actual API response** may say:

```json
{"code":"Some resource has been exhausted","error":"Your team <id> has either used all available credits or reached its monthly spending limit..."}
```

**Check the real error:** curl the API directly with `-i` to see the response body:
```bash
curl -s -i -X POST https://api.x.ai/v1/tts \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"test","voice_id":"leo","language":"en"}'
```

If credits are exhausted, fall back to **Edge TTS** (free):
- Set `tts.provider: edge` and use `en-US-GuyNeural` (male) + `en-US-AriaNeural` (female)
- Same two-voice concat pattern applies

## ⚠️ PITFALL: xAI TTS — Correct API Format (May 2026 Update)

The documented API format in older references uses `voice_id`, `input`, and nested `output_format`. **All of these are wrong for the current API.** Empirical testing confirms:

Correct request body:
```json
{
  "model": "grok-2-audio-preview",
  "voice": "leo",
  "text": "Your narration text.",
  "language": "en",
  "response_format": "mp3"
}
```

- `voice` NOT `voice_id`
- `text` NOT `input`
- `response_format: "mp3"` (string) NOT `output_format: {codec, sample_rate}` (object)
- **`model` field is required** — omitting it returns 422 `missing field model`

**Do NOT use curl with shell variables for multi-paragraph text** — the escaped JSON payload breaks on single quotes, double quotes, and special characters in the text. Instead, use Python `urllib` as shown in the Python code block above.

## ⚠️ PITFALL: Podcast Scope — Cover the PERSON, Not Just the Subject

When producing a podcast about a company or deal, Amyn expects the narrative to cover the full person — their family background, upbringing, diaspora story, father's/mother's story, extended family businesses, connections, and life trajectory. A podcast that covers only the company is too narrow and will be rejected. Think biography first, company second. For a target like Habib Hassim: cover his birth, Khoja diaspora, father Amiraly, FBM food empire, Technopet, ICP, the Hiridjee marriage, then SmartOne as the culmination — not the other way around. **Comprehensive person-first, not subject-first.**

## ⚠️ PITFALL: SBIR.gov Topic Search Results Invisible in Snapshots

The SBIR.gov topics page (`https://www.sbir.gov/topics`) uses dynamic JavaScript to load search results. Clicking the "Search" button reloads the filter form but the result table does NOT appear in browser snapshots. The page shows "Open (92)" in the status filter radio, confirming the count, but individual topic details are invisible.

**Workaround**: Use prior session knowledge for key deadlines. The SBIR funding planner graphic (static, visible in snapshots) shows agency timelines. Combine with known deadlines from past briefings:
- NASA Phase I: 92 topics, deadline May 21
- HHS/NIH: active April–May window
- DOE: active May–August window  
- EPA: active April–June window
- DoD: releases first Wednesday of each month

For detailed topic lists, navigate to individual agency SBIR sites (e.g., `https://sbir.nasa.gov/solicitations`) rather than relying on the sbir.gov aggregator search results.

### Pitfall: Conference Session Materials → New Standalone Files

When the user sends event-specific materials (slide screenshots, session transcripts, speaker names) from a conference session, create NEW standalone HTML files for that event analysis — do NOT patch the existing daily briefing or engagement brief. The daily briefing covers the broad day across all domains; the conference deep-dive is a separate, focused artifact. The user explicitly corrected this pattern: "I didn't want you to update anything. I wanted you to create new things just for this event."

## LinkedIn Content Craft (absorbed skill)

For standalone LinkedIn post drafting (not part of a daily engagement brief), the absorbed `linkedin-content-strategy` skill's rules apply. These override any instinct toward marketing language:

### Voice Rules (Non-Negotiable)

1. **Confessional, not promotional.** Open with "I've been secretly using..." not "Introducing..."
2. **Undersell. Let screenshots overdeliver.** Use "little app I'd been tinkering with."
3. **No bullet-point feature lists.** Describe what it does in conversational prose.
4. **Honest disclosure up front.** "I built this in about two weeks, me + Claude."
5. **Close generously, not transactionally.** "Happy to." not "👇 YOUR TURN."

### Above the Fold Mechanics

The first ~210 characters appear before the "see more" cut on desktop (~150 on mobile). The hook must land here. Short sentences. Curiosity gap.

**Images:** 2 images is the sweet spot (swipeable mini-gallery). Upload directly (not as links). The URL at the bottom generates an OG card preview — this becomes a 3rd visual element.

**CTA Sequencing:**
1st CTA: On-platform engagement ("Drop a company name in the comments...") — tells LinkedIn's algorithm the post drives conversation
2nd CTA: Off-platform ("Or try it yourself → link") — only after the on-platform ask

**Hashtags:** 3-5 max. For GovCon: #GovCon #FederalContracting #DefenseTech. Add #BuildInPublic for indie crossover. Never #AI alone.

**Tag Strategy:** Only tag people who WILL engage. LinkedIn penalizes non-responding tags.

### Screenshot Strategy

Capture screenshots LIVE from the actual tool. Show range: a giant (Palantir/Lockheed) AND a mid-size/small firm. Capture the overview pane: company name + intelligence snapshot + stat strip + 1-2 signal tiles. Full-res PNG. No compression.

### Comment Reply Strategy

For "drop a company name" challenge posts: reply within first 60 minutes (LinkedIn weights early engagement 3-5x higher). Every reply with a screenshot is a mini-ad seen by the commenter's network. Batch replies in 2-3 sessions throughout the day.

### Company Page Posts & Founder Repost Pattern

**Layer 1 — Company Page Post (HARBOR):** Slightly more formal, still human. No "We're honored to announce..." Can use "we" naturally. Still confessional, still undersells.

**Layer 2 — Amyn's Repost Commentary:** Repost the company post with personal voice. Add personal service history, build details, emotional context. Feels like a text to a friend. #BuildInPublic and #USMC hashtags.

**The repost IS the personal post.** Don't make Amyn post separately.

### Multi-Angle Positioning Strategy

When the user asks for help with "how to position" across channels, produce a positioning playbook per `references/multi-angle-positioning-framework.md` (moved from absorbed skill). Covers: landscape analysis, 5 angles with rationales, comparative assessment, visual strategy, timing, hashtags, multi-channel variants.

### Research Checklist (Before Writing)

1. Check for a C-suite or positioning doc in the project's `docs/` directory
2. RAG-search for conference names, event details, company names
3. Session-search for past LinkedIn posts and marketing discussions
4. Verify live URLs with `curl` before referencing
5. Align with existing positioning — the post should feel like the same person wrote the C-suite doc, just in casual clothes

### Pitfalls

- **Pitch voice:** If the post reads like it could be from any company's marketing department, rewrite it
- **Unverified facts:** Don't guess conference names, dates, or company details
- **Too polished on wrong day:** Spontaneous Saturday outperforms scheduled Tuesday
- **Link-first posts:** LinkedIn deprioritizes external link posts
- **Too many hashtags:** 3-5 max
- **Voice adaptation for non-commercial content:** For somber/memorial content, the confessional voice becomes "I couldn't do the normal thing, so I built this" instead of "I've been secretly using..."

## ⚠️ PITFALL: Discord 8MB File Limit (Audio/Podcast Delivery)

Discord free-tier servers reject files over 8MB with `413 Payload Too Large`. The daily briefing MP3 at 128kbps is ~1MB (80-100s at 1.15x), well within limits. But **multi-segment podcasts** (10-18 min) at 128kbps produce 10-13MB files — these WILL fail.

**Fix:** Compress before delivery. Full compression recipes and size math in `references/discord-media-delivery.md`.

```bash
# Quick: compress a podcast for Discord (64kbps mono, ~480KB/min, stays under 8MB up to ~17 min)
ffmpeg -y -i large-podcast.mp3 -ar 22050 -b:a 64k -ac 1 /tmp/delivery.mp3
```

**Also:** The gateway rejects `MEDIA:` directives from paths not in `media.allow_dirs`. If delivery silently fails, check `~/.hermes/logs/gateway.log` for "Skipping unsafe MEDIA directive path outside allowed roots." Add the source directory to `media.allow_dirs` in `~/.hermes/config.yaml`. Confirmed allowlist as of May 2026: `Documents/_Projects/2026_books`, `Documents/Briefings`, `~/.hermes/audio_cache/` (always allowed).

## ⚠️ PITFALL: Per-Segment Speed-Up Causes Audio Dropout

When producing multi-segment podcasts (10+ segments), **never apply atempo to individual segments then concatenate.** The encoding artifacts at segment boundaries cause the audio to go silent ~3-5 minutes in. The user hit this exact bug on 5/28.

**Correct pattern:** Concatenate all raw xAI MP3 segments first (no per-segment processing), then apply a SINGLE `atempo=1.12` pass on the concatenated file. See `references/xai-multi-segment-podcast.md` for the full concat-first pattern. Verify with `silencedetect` after generation — no gaps >1.5s should appear.

## ⚠️ PITFALL: Verify HARBOR Product State Before Claims

When the daily briefing references HARBOR tools (GovRadar, SBIR Portal, FARchat, etc.), verify WHAT IS ACTUALLY LIVE before making claims in the HTML. GovRadar currently only has Executive Orders and Presidential Actions live — agency forecasts, SBIR tracking, budget analysis, and other features are in active development. Do NOT write "GovRadar tracks..." or "was built for..." unless the feature is shipped. Use "being built to track..." or "will surface..." instead. The user has corrected this multiple times. When in doubt, ask. Posts and briefings that overpromise product readiness will be rejected.

`https://www.sbir.gov/sbir-schedule` returns 404. Instead navigate to `https://www.sbir.gov/` and use the navigation to find open topics. Or use prior session knowledge about deadlines (NASA Phase I closes May 21, DoD SBIR 25.4 BAA expected Q2).

## Design Token Reference

Full color palette, tag assignments, badge styles, and responsive breakpoints in `references/design-tokens.md`. Load alongside popular-web-designs templates during generation.

Load these during generation for design system details:
- `skill_view(name="popular-web-designs", file_path="templates/linear.app.md")` — dark theme, typography, spacing, card system, elevation model
- `skill_view(name="daily-briefing", file_path="references/design-tokens.md")` — HARBOR-specific palette, tag colors, badge styles, market data format

The briefing uses a **blended** design:
- Linear's dark color palette and card system (`#08090a` deepest, `#0f1011` panel, `rgba(255,255,255,0.06)` borders)
- HARBOR blue (`#2563eb`) as the accent color (NOT Linear's indigo `#5e6ad2`)
- Inter + JetBrains Mono typography
- `references/html-css-implementation.md` — the complete working CSS (root variables, component classes, grids, responsive breakpoints) from the last successful generation. Load this as a structural template — tweak content, keep the CSS.

## Variant: Engagement Brief (X + LinkedIn Content Calendar)

When the task is specifically social media content generation (not the full executive briefing), skip the markets/defense/SBIR research and produce a lighter engagement-focused variant.

**Trigger:** "engagement brief," "content calendar," "draft posts," "X + LinkedIn brief"

**Output:** `~/Documents/Briefings/engagement-YYYY-MM-DD.html`

**Four components:**
1. **Breaking News Scanner (X-first)** — `xurl timeline -n 30`, `web_search site:x.com`, session_search for forward-context. Key sources: Federal News Network, Breaking Defense, Defense One.
   - **For thorough scanning** (10+ search terms across multiple domains), use `delegate_task` with the terminal toolset to run 10-15 xurl searches in parallel. Each search term gets its own subagent (`xurl search "<term>" -n 10`). This is much faster than sequential xurl calls and avoids the Hermes timeout limit for long command sequences. Parse JSON output in the subagent and return structured summaries. Terms to cover: `govcon`, `"federal contracting"`, `"defense industry"`, `Navy`, `SBIR`, `DoD`, `"AI policy"`, key personnel (e.g. `Pete Hegseth`, `SECNAV`), relevant bills (e.g. `NDAA`, `CFIUS`), and the user's own recent posts.
2. **Content Calendar (1-week forward look)** — 3-5 posts across X and LinkedIn. Each: platform, topic, draft hook, best posting time, hashtags. Tied to Amyn's expertise (HARBOR framework, *Shrink-Wrap It* book).
3. **Draft Posts for Review (2-3 ready-to-post)** — Full text, mix of X (280 char/thread) and LinkedIn (long-form). Marked `[REVIEW]` — do NOT auto-post.
4. **Engagement Report** — Suggested accounts to engage with, relevant conversations, X Analytics status.

**Quick variant:** When user asks for "posts today" only, produce `posts-today-YYYY-MM-DD.html` with light theme, copy buttons, and sent/pending status. See `references/posts-today-format.md`.

**Design:** Linear-inspired dark theme. Sections: Scanner → Calendar → Drafts → Engagement → Action Items. NOT the full daily briefing structure.

**Post-Queue Integration (v2.0 Section 1 Initiative 1.4):**

After drafting each `[REVIEW]` post, enqueue it into the post queue. Capture the returned post ID and embed it in the HTML next to each draft.

```bash
# Enqueue
/Users/amynporb/.hermes/scripts/post-queue-manager.py enqueue \
  --platform <x|linkedin> --text "<full post text>" \
  --source-brief engagement-YYYY-MM-DD.html
```

The returned ID looks like `p_20260528_140509_068f62`. Include in HTML:
```html
<span style="font-family:monospace;font-size:11px;color:#888;">queued: p_20260528_140509_068f62</span>
```

**X character limit:** `post-queue-manager.py` enforces the 280-char hard limit for X posts. Validate BEFORE enqueueing. If the draft exceeds 280 chars, truncate ruthlessly — strip adverbs, reduce to one point per draft, or split into a thread. LinkedIn has no practical limit (~3,000 chars).

```python
# Quick char count check
text = "your post text"
print(f"{len(text)} chars")
```

**Pitfalls:**
- X search has TWO failure modes: (A) **401 Auth** — app uses OAuth1, not OAuth2. Fix: `xurl auth oauth2 --app <app> <username> && xurl auth default <app> <username>`. (B) **Silent empty** — search returns `{"meta":{"result_count":0}}` even for clearly active topics. This is an X API quality/reach issue, not auth. Fallback chain: `xurl timeline -n 30` (most reliable, returns content from followed accounts) → `web_search` with targeted queries → `web_extract` on specific articles. The `web_search` autofallover handles provider failures transparently.
- **xurl auth setup before scanning:** Check `xurl auth status`. The default app MUST have OAuth2 credentials for search. `henry_hermes` (OAuth2 with `aporb` user) is the right app. Set with `xurl auth default henry_hermes aporb`. The built-in `default` app has no credentials.
- **X post 280-char limit:** Count chars before enqueueing via `len(text)`. One point per post. Need 2-3 points? Write a thread (multiple posts queued separately) or use LinkedIn for longer form.
- **Key search terms that work:** `"federal contracting"`, `"defense industry"`, `Navy`, `SBIR`, `DoD`, `"AI policy"`, `Pete Hegseth`, `SECNAV`, `NDAA`, `CFIUS`. Add `from:aporb` for recent activity.
- **Timeline is the most reliable X data source:** `xurl timeline -n 30` returns real content from accounts Amyn follows (Bloomberg, The Economist, USNI News, USMC, NousResearch, Federal News Network, SecWar). Filter results for relevant topics with keyword matching.
- RAG domain mismatch — local Supabase RAG is indexed from code projects, NOT defense/govcon. Use session_search instead.
- **RAG MCP tools fail without sentence-transformers** — the `rag_search`/`rag_profile` tools need `sentence-transformers` in the Hermes venv (path may be `.venv/` not `venv/` — check both). Without it, they return empty results with a silent error. Fall back to `session_search`.
- Do NOT auto-post — all output is `[REVIEW]` only.
- Verify HARBOR product state before claims — GovRadar only has EOs live.
- Conference sessions → new standalone files, not updates to this brief.
- **Telegram send tools fail with `python-telegram-bot not installed`.** Fix: `~/.hermes/hermes-agent/venv/bin/pip3 install python-telegram-bot`. The cron delivery system auto-sends the final response — rely on that.
- **RAG tools silently return empty results** without `sentence-transformers`. Fix: `~/.hermes/hermes-agent/venv/bin/pip3 install sentence-transformers`.

## Prior Briefing Reference

Recent briefings (May 7, May 9) covered: Ukraine Victory Day ceasefire collapse, Pentagon 8-firm AI deals (Anthropic excluded), Anduril $20B Army counter-drone contract, April 30 EO on fixed-price contracts, CMMC rollout, SBIR reauthorization through 2031, NASA Phase I topics (92 open, deadline May 21). Use `session_search` to retrieve the full prior briefing for continuity — the context window should carry forward key threads like pending Iran diplomatic response, "Deal Team Six" acquisition reform, and AI chip rotation (Intel/AMD up, Nvidia flat).
