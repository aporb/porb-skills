---
name: x-engagement
description: "Read X (Twitter) engagement for @aporb via the official X API v2. Use when asked to check our current X/Twitter engagement, reach, impressions, likes, or recent post performance. Read-only."
---

# X Engagement

Pull live X (Twitter) engagement for the HARBOR account (@aporb) through the official X API v2. Read-only: this skill never posts. Posting stays on the Pineapple Protocol through the CMO / content-writer path.

## Credentials

API credentials live in the gitignored `.env.xapi` at the repo root (X app "Henry_Hermes", created 2026-06-08). The helper script finds it automatically by walking up from the working directory, or reads `X_BEARER_TOKEN` / `X_API_ENV` from the environment.

App-only bearer auth covers profile stats and public + owner-visible tweet metrics (including impressions for our own posts). Never echo the secrets back in plaintext. If the token stops working, regenerate at the X developer portal and update `.env.xapi`.

## Usage

```bash
# Account snapshot (followers, following, tweet count)
python3 .claude/skills/x-engagement/scripts/x_api.py profile

# Last 20 ORIGINAL posts + per-post and aggregate engagement (default)
python3 .claude/skills/x-engagement/scripts/x_api.py engagement

# Last N original posts
python3 .claude/skills/x-engagement/scripts/x_api.py engagement aporb 30

# Recent posts INCLUDING replies
python3 .claude/skills/x-engagement/scripts/x_api.py recent aporb 20

# A single tweet's metrics
python3 .claude/skills/x-engagement/scripts/x_api.py tweet <tweet_id>

# Machine-readable: add --json to any command
python3 .claude/skills/x-engagement/scripts/x_api.py engagement --json
```

Default handle is `aporb`. Pass any public handle as the first argument to read a competitor or partner account (profile + public metrics only).

## Execution (pure tool)

This skill is a mechanical wrapper around the X API v2. No agent dispatch for the data pull. Rationale: fetching engagement metrics is deterministic; adding agent dispatch would inject bureaucracy without quality improvement. See `.claude/skills/SKILL-PATTERN.md` Tier D.

**Where cognition belongs:** raw numbers are mechanical, but *interpretation* (what the engagement means, what to change about cadence / hooks / topics, whether to amplify a post) is marketing strategy and belongs to the **cmo** agent. When the user asks for analysis or recommendations rather than just the numbers, hand the script's output to the cmo agent. Any drafting or posting goes to content-writer and is Pineapple-gated.

## API notes

- Base: `https://api.x.com/2/`. Auth header: `Authorization: Bearer <token>`.
- `GET /2/users/by/username/:handle?user.fields=public_metrics` resolves a handle to an id + follower/following/tweet counts.
- `GET /2/users/:id/tweets?max_results=N&exclude=retweets,replies&tweet.fields=public_metrics,created_at` returns recent posts. `public_metrics` carries like / retweet / reply / quote counts, plus `impression_count` for the authenticated account's own posts.
- Free-tier read limits are low. Keep `max_results` modest and avoid tight polling loops.
- `impression_count` for accounts you do not own is not returned under app-only auth; the table shows it as `-` in that case.

## Related

- `admin/setup/xactions-twitter-mcp-setup.md` — the older browser-cookie XActions MCP (posting/automation, 140+ tools). This skill is the lighter, official-API read path; prefer it for engagement reads.
- `operations/henry-hermes/vault/Operations/X Twitter Integration.md` + `X Pineapple Protocol.md` — posting cadence + the no-autonomous-send rule.
- `feedback_tweeting_style.md` (memory) — voice rules for any drafted post.
