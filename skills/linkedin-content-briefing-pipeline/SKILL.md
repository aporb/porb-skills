---
name: linkedin-content-briefing-pipeline
description: "Full pipeline for LinkedIn/X content briefings: Research Scout, source screenshots, scored topic brief, draft posts. Outputs self-contained dark-theme HTML briefing with embedded source screenshots."
version: 1.0.0
author: Amyn Porbanderwala / HARBOR Initiative
---

# LinkedIn Content Briefing Pipeline

Two-agent architecture: **Research Scout** produces briefs, **LinkedIn Brand Manager** produces posts.

## Phase 1: Orchestrate Research
1. Get current date: `date`
2. Define 72-hour research window (last 3 days from current time)
3. Dispatch subagents in parallel for:
   - News Researcher (federal tech, AI, defense innovation)
   - GovCon Researcher (contract awards, SBIR/STTR, productization)
   - AI Researcher (LLM industry, enterprise AI, AI regulation)
   - LinkedIn Trend Researcher (executive discussions, debates)
4. Use web_extract on G2X Daily, PilieroMazza Weekly, Breaking Defense
5. Use x_search for real-time X discussions
6. Use web_search for source URLs (with rate-limit retries)

## Phase 2: Score and Select Topics
Score each topic 1-5 on: timeliness, credibility, HARBOR relevance, Amyn relevance, LinkedIn discussion potential, BD potential. Only topics with average >= 4.0.

## Phase 3: Capture Primary Source Screenshots
For each top topic, use `browser_navigate` + `browser_vision`:
1. Navigate to article URL, accept cookies
2. Capture tightly framed screenshot showing: title, author, date, first 1-2 paragraphs
3. Save to `~/Documents/Briefings/screenshots/` as `NN-topic-description.png`
4. Fix permissions: `chown amynporb:staff && chmod 644`

## Phase 4: Draft Posts
**LinkedIn HARBOR:** professional, practical, credible. Position as firm that helps contractors productize.
**LinkedIn Amyn:** builder voice, specific numbers, AI leader + GovCon innovator + Marine veteran.
**X @aporb:** standalone, lowercase, specific numbers, builder voice.

## Phase 5: Build HTML Briefing
Self-contained dark-theme HTML at `~/Documents/Briefings/content-strategy-YYYY-MM-DD.html` with:
- Executive summary, scoring table, topic cards with source screenshots
- Platform-specific draft posts
- Primary sources directory table
- Handoff box

## Phase 6: Quality Gate
```bash
python3 ~/.hermes/skills/harbor-eval-gate/scripts/eval_gate.py \
  --candidate-file "~/Documents/Briefings/content-strategy-YYYY-MM-DD.html" \
  --benchmark ~/.hermes/skills/harbor-eval-gate/benchmark/benchmark-v0.yaml \
  --dry-run
```

**Dash policy — user preference (overrides eval gate defaults):**
- User has explicitly banned double hyphens (`--`) for content output.
- Use en dashes (–) for number ranges ("$2M–$10M") and em dashes (—) for grammatical breaks.
- The eval gate will flag "em-dash over budget" as a violation, but for content posts this is acceptable if composite meets 0.7. The em-dash count is a stylistic default, not a hard rule for this user's content.
- For HTML structure (comments, CSS, code), still avoid em dashes — those count toward the eval gate budget.
- For visible post content and prose, em/en dashes are preferred punctuation and should be used as grammatically appropriate.

Minimum composite 0.7 to pass.

## Phase 7: Deliver
Open in Safari. Deliver path to user via Discord with MEDIA tag.

## Known Blockers
- Lawfare, G2X Change: connection refused by browser
- Business Insider: paywalled
- Brave Search: rate-limited after ~5 calls. Fall back to x_search or web_extract.
- Python inline file replace can corrupt files. Use write_file or terminal sed instead.
- Kanban MCP (`mcp_hermes_self_*`) intermittently unreachable — fall back to `delegate_task` directly
- `execute_code` blocked in cron-like contexts — use `terminal` or write Python files

## Reference Files

- `references/x-native-writing.md` — X.com voice, hook patterns, common LinkedIn-to-X mistakes
- `references/file-permissions.md` — macOS permission pitfalls when subagents write files
- `references/anti-ai-image-prompting.md` — header image prompting techniques and post-processing

## Scripts

- `scripts/multi-perspective-review.py` — dispatches parallel CMO/domain/platform reviews
- `scripts/post-process-headers.py` — anti-AI image post-processing pipeline (blur, grain, vignette)

## User Preferences (Critical)

**Dash policy:**
- User has banned `--` (double hyphens) in all content output.
- Use em dash (—) and en dash (–) for grammatical effect, sparingly.
- The eval gate will flag em-dash count but this is acceptable if composite ≥ 0.7.

**Content platform distinction:**
- LinkedIn = professional, structured, subheads, pullquotes, ~1,000 words
- X = lowercase, hooks, no subheads, debate invitation close, ~1,800 chars
- Never copy-paste LinkedIn content to X — see `references/x-native-writing.md`

**Orchestration preference:**
- User wants orchestrator role with parallel subagent dispatch.
- "Don't be lazy, use all tools, act like an orchestrator, don't do the work yourself."
- Dispatch specialized workers: Research Scout, CMO reviewer, Platform specialist, Source validator.
- Always review subagent output before delivering.

**Permissions:**
- Always `chown amynporb:staff` and `chmod 644` files created by subagents.
- Directories need `chmod 755` (execute bit for traversal).
- See `references/file-permissions.md` for full pattern.
