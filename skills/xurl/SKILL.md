---
name: xurl
description: "X/Twitter via xurl CLI: post, search, DM, media, v2 API."
version: 1.1.1
author: xdevplatform + openclaw + Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [xurl]
metadata:
  hermes:
    tags: [twitter, x, social-media, xurl, official-api]
    homepage: https://github.com/xdevplatform/xurl
    upstream_skill: https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# xurl — X (Twitter) API via the Official CLI

`xurl` is the X developer platform's official CLI for the X API. It supports shortcut commands for common actions AND raw curl-style access to any v2 endpoint. All commands return JSON to stdout.

Use this skill for:
- posting, replying, quoting, deleting posts
- searching posts and reading timelines/mentions
- liking, reposting, bookmarking
- following, unfollowing, blocking, muting
- direct messages
- media uploads (images and video)
- raw access to any X API v2 endpoint
- multi-app / multi-account workflows

This skill replaces the older `xitter` skill (which wrapped a third-party Python CLI). `xurl` is maintained by the X developer platform team, supports OAuth 2.0 PKCE with auto-refresh, and covers a substantially larger API surface.

---

## Secret Safety (MANDATORY)

Critical rules when operating inside an agent/LLM session:

- **Never** read, print, parse, summarize, upload, or send `~/.xurl` to LLM context.
- **Never** ask the user to paste credentials/tokens into chat.
- The user must fill `~/.xurl` with secrets manually on their own machine.
- **Never** recommend or execute auth commands with inline secrets in agent sessions.
- **Never** use `--verbose` / `-v` in agent sessions — it can expose auth headers/tokens.
- To verify credentials exist, only use: `xurl auth status`.

Forbidden flags in agent commands (they accept inline secrets):
`--bearer-token`, `--consumer-key`, `--consumer-secret`, `--access-token`, `--token-secret`, `--client-id`, `--client-secret`

App credential registration and credential rotation must be done by the user manually, outside the agent session. After credentials are registered, the user authenticates with `xurl auth oauth2` — also outside the agent session. Tokens persist to `~/.xurl` in YAML. Each app has isolated tokens. OAuth 2.0 tokens auto-refresh.

---

## Installation

Pick ONE method. On Linux, the shell script or `go install` are the easiest.

```bash
# Shell script (installs to ~/.local/bin, no sudo, works on Linux + macOS)
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash

# Homebrew (macOS)
brew install --cask xdevplatform/tap/xurl

# npm
npm install -g @xdevplatform/xurl

# Go
go install github.com/xdevplatform/xurl@latest
```

Verify:

```bash
xurl --help
xurl auth status
```

If `xurl` is installed but `auth status` shows no apps or tokens, the user needs to complete auth manually — see the next section.

---

## One-Time User Setup (user runs these outside the agent)

These steps must be performed by the user directly, NOT by the agent, because they involve pasting secrets. Direct the user to this block; do not execute it for them.

1. Create or open an app at https://developer.x.com/en/portal/dashboard
2. Set the redirect URI to `http://localhost:8080/callback`
3. Copy the app's Client ID and Client Secret
4. Register the app locally (user runs this):
   ```bash
   xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
   ```
5. Authenticate (specify `--app` to bind the token to your app):
   ```bash
   xurl auth oauth2 --app my-app
   ```
   (This opens a browser for the OAuth 2.0 PKCE flow.)

   If X returns a `UsernameNotFound` error or 403 on the post-OAuth `/2/users/me` lookup, pass your handle explicitly (xurl v1.1.0+):
   ```bash
   xurl auth oauth2 --app my-app YOUR_USERNAME
   ```
   This binds the token to your handle and skips the broken `/2/users/me` call.
6. Set the app as default so all commands use it:
   ```bash
   xurl auth default my-app
   ```
7. Verify:
   ```bash
   xurl auth status
   xurl whoami
   ```

After this, the agent can use any command below without further setup. OAuth 2.0 tokens auto-refresh.

> **Common pitfall:** If you omit `--app my-app` from `xurl auth oauth2`, the OAuth token is saved to the built-in `default` app profile — which has no client-id or client-secret. Commands will fail with auth errors even though the OAuth flow appeared to succeed. If you hit this, re-run `xurl auth oauth2 --app my-app` and `xurl auth default my-app`.

---

## Quick Reference

| Action | Command |
| --- | --- |
| Post | `xurl post "Hello world!"` |
| Reply | `xurl reply POST_ID "Nice post!"` |
| Quote | `xurl quote POST_ID "My take"` |
| Delete a post | `xurl delete POST_ID` |
| Read a post | `xurl read POST_ID` |
| Search posts | `xurl search "QUERY" -n 10` |
| Who am I | `xurl whoami` |
| Look up a user | `xurl user @handle` |
| Home timeline | `xurl timeline -n 20` |
| Mentions | `xurl mentions -n 10` |
| Like / Unlike | `xurl like POST_ID` / `xurl unlike POST_ID` |
| Repost / Undo | `xurl repost POST_ID` / `xurl unrepost POST_ID` |
| Bookmark / Remove | `xurl bookmark POST_ID` / `xurl unbookmark POST_ID` |
| List bookmarks / likes | `xurl bookmarks -n 10` / `xurl likes -n 10` |
| Follow / Unfollow | `xurl follow @handle` / `xurl unfollow @handle` |
| Following / Followers | `xurl following -n 20` / `xurl followers -n 20` |
| Block / Unblock | `xurl block @handle` / `xurl unblock @handle` |
| Mute / Unmute | `xurl mute @handle` / `xurl unmute @handle` |
| Send DM | `xurl dm @handle "message"` |
| List DMs | `xurl dms -n 10` |
| Upload media | `xurl media upload path/to/file.mp4` |
| Media status | `xurl media status MEDIA_ID` |
| List apps | `xurl auth apps list` |
| Remove app | `xurl auth apps remove NAME` |
| Set default app | `xurl auth default APP_NAME [USERNAME]` |
| Per-request app | `xurl --app NAME /2/users/me` |
| Auth status | `xurl auth status` |

Notes:
- `POST_ID` accepts full URLs too (e.g. `https://x.com/user/status/1234567890`) — xurl extracts the ID.
- Usernames work with or without a leading `@`.

---

## Command Details

### Posting

```bash
xurl post "Hello world!"
xurl post "Check this out" --media-id MEDIA_ID
xurl post "Thread pics" --media-id 111 --media-id 222

xurl reply 1234567890 "Great point!"
xurl reply https://x.com/user/status/1234567890 "Agreed!"
xurl reply 1234567890 "Look at this" --media-id MEDIA_ID

xurl quote 1234567890 "Adding my thoughts"
xurl delete 1234567890
```

### Reading & Search

```bash
xurl read 1234567890
xurl read https://x.com/user/status/1234567890

xurl search "golang"
xurl search "from:elonmusk" -n 20
xurl search "#buildinpublic lang:en" -n 15
```

### Users, Timeline, Mentions

```bash
xurl whoami
xurl user elonmusk
xurl user @XDevelopers

xurl timeline -n 25
xurl mentions -n 20
```

### Engagement

```bash
xurl like 1234567890
xurl unlike 1234567890

xurl repost 1234567890
xurl unrepost 1234567890

xurl bookmark 1234567890
xurl unbookmark 1234567890

xurl bookmarks -n 20
xurl likes -n 20
```

### Social Graph

```bash
xurl follow @XDevelopers
xurl unfollow @XDevelopers

xurl following -n 50
xurl followers -n 50

# Another user's graph
xurl following --of elonmusk -n 20
xurl followers --of elonmusk -n 20

xurl block @spammer
xurl unblock @spammer
xurl mute @annoying
xurl unmute @annoying
```

### Direct Messages

```bash
xurl dm @someuser "Hey, saw your post!"
xurl dms -n 25
```

### Media Upload

```bash
# Auto-detect type
xurl media upload photo.jpg
xurl media upload video.mp4

# Explicit type/category
xurl media upload --media-type image/jpeg --category tweet_image photo.jpg

# Videos need server-side processing — check status (or poll)
xurl media status MEDIA_ID
xurl media status --wait MEDIA_ID

# Full workflow
xurl media upload meme.png                  # returns media id
xurl post "lol" --media-id MEDIA_ID
```

---

## Raw API Access

The shortcuts cover common operations. For anything else, use raw curl-style mode against any X API v2 endpoint:

```bash
# GET
xurl /2/users/me

# POST with JSON body
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'

# DELETE / PUT / PATCH
xurl -X DELETE /2/tweets/1234567890

# Custom headers
xurl -H "Content-Type: application/json" /2/some/endpoint

# Force streaming
xurl -s /2/tweets/search/stream

# Full URLs also work
xurl https://api.x.com/2/users/me
```

---

## Global Flags

| Flag | Short | Description |
| --- | --- | --- |
| `--app` | | Use a specific registered app (overrides default) |
| `--auth` | | Force auth type: `oauth1`, `oauth2`, or `app` |
| `--username` | `-u` | Which OAuth2 account to use (if multiple exist) |
| `--verbose` | `-v` | **Forbidden in agent sessions** — leaks auth headers |
| `--trace` | `-t` | Add `X-B3-Flags: 1` trace header |

---

## Streaming

Streaming endpoints are auto-detected. Known ones include:

- `/2/tweets/search/stream`
- `/2/tweets/sample/stream`
- `/2/tweets/sample10/stream`

Force streaming on any endpoint with `-s`.

---

## Output Format

All commands return JSON to stdout. Structure mirrors X API v2:

```json
{ "data": { "id": "1234567890", "text": "Hello world!" } }
```

Errors are also JSON:

```json
{ "errors": [ { "message": "Not authorized", "code": 403 } ] }
```

---

## Common Workflows

### Post with an image
```bash
xurl media upload photo.jpg
xurl post "Check out this photo!" --media-id MEDIA_ID
```

### Reply to a conversation
```bash
xurl read https://x.com/user/status/1234567890
xurl reply 1234567890 "Here are my thoughts..."
```

### Search and engage
```bash
xurl search "topic of interest" -n 10
xurl like POST_ID_FROM_RESULTS
xurl reply POST_ID_FROM_RESULTS "Great point!"
```

### Check your activity
```bash
xurl whoami
xurl mentions -n 20
xurl timeline -n 20
```

### Multiple apps (credentials pre-configured manually)
```bash
xurl auth default prod alice               # prod app, alice user
xurl --app staging /2/users/me             # one-off against staging
```

---

## ⚠️ PITFALL: OAuth1/Bearer Cannot Search — OAuth2 Required for Read/Write Endpoints

The X API v2 has tiered auth requirements:

| Auth Type | Can Read Own Profile? | Can Read Timeline? | Can Search? | Can Post? |
|-----------|----------------------|-------------------|------------|----------|
| OAuth 1.0a | ✅ `whoami`, `user` | ✅ `timeline`, `mentions` | ❌ Returns 401 | ❌ |
| Bearer Token | ❌ | ❌ | ❌ | ❌ |
| OAuth 2.0 PKCE | ✅ | ✅ | ✅ | ✅ |

**If `xurl search` returns 401 Unauthorized**: your default app is likely using OAuth1 or Bearer, not OAuth2. Check with `xurl auth status` — look for `oauth2: (none)` in the default app. Fix: run `xurl auth oauth2 --app <your-app> <your-username>` (on your machine, outside the agent session).

**Workaround**: If you can't use search, `xurl timeline` still works with OAuth1 and gives you content from followed accounts. Filter the JSON output for relevant topics. Use `execute_code` (not direct pipes) for filtering — see next pitfall.

## ⚠️ PITFALL: Pipe-to-Interpreter Security Blocks

The Hermes security scanner blocks commands that pipe `xurl` output directly to an interpreter (e.g., `xurl timeline | python3 -c '...'`). This is a security feature — API output shouldn't be blindly executed.

**Workaround**: Use `execute_code` with `hermes_tools.terminal()` instead:

```python
# ✅ Works — uses execute_code, not a pipe
from hermes_tools import terminal
result = terminal("xurl timeline -n 30 2>&1")
# Parse result['output'] with json.loads() inside execute_code
```

This keeps JSON parsing inside the controlled execute_code environment rather than streaming through a pipe.

## Error Handling

- Non-zero exit code on any error.
- API errors are still printed as JSON to stdout, so you can parse them.
- Auth errors → have the user re-run `xurl auth oauth2` outside the agent session.
- Commands that need the caller's user ID (like, repost, bookmark, follow, etc.) will auto-fetch it via `/2/users/me`. An auth failure there surfaces as an auth error.

## ⚠️ PITFALL: `xurl user` Only Accepts SINGLE Handles

`xurl user` does NOT support comma-separated batch lookup. It calls `/2/users/by/username/:username`, which validates usernames against `^[A-Za-z0-9_]{1,15}$`. Passing `handle1,handle2,handle3` fails with:

```json
{"errors":[{"message":"The `username` query parameter value [handle1,handle2] does not match ^[A-Za-z0-9_]{1,15}$"}]}
```

**Workaround**: Use `execute_code` with `hermes_tools.terminal()` to loop through handles individually with a small delay:

```python
from hermes_tools import terminal
import json, time

handles = ["USSOCOM", "anduriltech", "LockheedMartin", ...]
results = {}
for h in handles:
    r = terminal(f"xurl user {h} 2>&1", timeout=10)
    try:
        data = json.loads(r["output"])
        if "data" in data:
            u = data["data"]
            m = u.get("public_metrics", {})
            results[h] = {
                "name": u["name"],
                "verified": u.get("verified", False),
                "followers": m.get("followers_count", 0),
                "tweets": m.get("tweet_count", 0),
            }
    except:
        results[h] = {"error": r["output"][:100]}
    time.sleep(0.15)  # gentle rate limiting — 429 otherwise
```

## Batch Follow After Events (Conference/Trade Show Workflow)

After meeting companies at SOF Week, AUSA, AFCEA, etc., follow them on X. Use `execute_code` with `hermes_tools.terminal()` to batch the entire list.

### Handle Discovery (multi-variant guessing)

Most small defense contractors have NO official X account. Expect 50-70% miss rate. For each company, try 3-5 handle variants in a loop:

```python
companies = [
    ("Company Name", ["companyname", "CompanyHQ", "GoCompany", "company_name", "company_co"]),
    # ... more companies
]
for name, handles in companies:
    for handle in handles:
        r = terminal(f"xurl user @{handle} 2>&1", timeout=10)
        # Parse JSON, check data.name / data.description for company name match
        # If name in description → confirmed match → break
        # If resolved but name doesn't match → store as uncertain, keep trying
        time.sleep(0.1)
```

**Sanity check before following:** The resolved account's `name` or `description` field MUST contain the company name (or a clear abbreviation). A handle that resolves to a real user with 3 followers and an unrelated bio is almost certainly the wrong person.

### Batch Follow (with rate limiting)

```python
confirmed = [(company, handle) for company, handle in discovered if verified]
for company, handle in confirmed:
    terminal(f"xurl follow @{handle} 2>&1", timeout=15)
    time.sleep(0.5)  # 500ms between follows — X enforces rate limits on write endpoints
```

### Expected Reality

From a typical 15-company event batch: ~7 confirmed follows, ~5 no-X-presence, ~3 uncertain (skip those). Companies with no X presence are often the best partnership targets — they're not marketing-heavy, they're builders.

## ⚠️ PITFALL: Handle Resolution ≠ Identity Verification

`xurl user @handle` returning data does NOT mean you found the right account. Common traps:

| Assumed Handle | Resolves To | Reality |
|---|---|---|
| @USASOC | Roman Pena (7 followers) | US Army SOCOM has no X account — this is a random individual |
| @NAVSPECWARCOM | Sierra (23 followers) | Naval Special Warfare Command has no X account |
| @AFSOC | Dale Jens (3 followers) | Air Force SOCOM has no X account |
| @MARSOC | Martin Sochor (2 followers) | Marine SOCOM has no X account |
| @AugustCole | Kristen Lindsey (4 followers) | Author August Cole uses a different handle |
| @SMXTech | Mike (1 follower) | SMX defense contractor uses a different handle |

**Always cross-check**: verify the `name` field matches expectations and the follower count is credible. Military commands, government personnel, and small defense contractors often have NO official X accounts or use handles completely different from their brand names.

## ⚠️ PITFALL: Direct Bearer Token Curl is Unreliable — Use xurl CLI

Direct curl with a hardcoded Bearer Token often returns 401 after the token expires/rotates. The Bearer Token from the x-analytics skill or other static references may be stale. xurl CLI manages its own OAuth tokens with auto-refresh — always prefer xurl over raw curl for X API access.

## ⚠️ PITFALL: `xurl search` Returns Unreliable Results

`xurl search "query"` has two distinct failure modes:

**Mode A — Auth failure (401):** The default app is using OAuth1/Bearer instead of OAuth2. Fix: `xurl auth oauth2 --app <app> <username>` then `xurl auth default <app> <username>`.

**Mode B — Silent empty results (`{"meta":{"result_count":0}}`):** The API call succeeded but returned nothing even for clearly active topics. This is not an auth problem — it's an X search API quality/reach issue. More common with multi-word or Boolean queries.

When `xurl search` returns empty (Mode B), use the **timeline + web_search fallback chain**:

```python
from hermes_tools import terminal
import json

# Step 1: Pull timeline from accounts you follow (more reliable than search)
tl = terminal("xurl timeline -n 30 2>&1")
data = json.loads(tl["output"])
items = data.get("data", []) if "data" in data else []

# Step 2: Filter timeline results for relevant topics manually
relevant = [t for t in items if "keyword" in t.get("text", "").lower()]

# Step 3: Supplement with web search for context
# (web_search doesn't have the same quality gap as xurl search)
```

For handle discovery specifically, prefer in this order:

1. **xAI X Search** (`x_search` tool via grok-4.3) — gives direct handle answers but costs credits
2. **Handle variant guessing** — try common variations (@CompanyName, @CompanyHQ, @GoCompany) via `xurl user`
3. **web_search** (if credits available) — search for "Company Name Twitter X handle"
4. **`xurl timeline -n 30`** — returns content from accounts you follow, then filter for mentions of the target
5. **xurl search** — last resort; results are inconsistent

## Batch Handle Verification Pattern

When verifying many handles (e.g., building SOF Week tracking lists):

1. Extract all candidate handles from research documents
2. Use `execute_code` + `terminal("xurl user @handle")` in a loop with `time.sleep(0.15)`
3. Collect follower counts, verification status, and account names
4. Flag accounts where `name` doesn't match expectations (possible wrong handle)
5. For handles that return `"Could not find user"` errors, try handle variants
6. For handles that time out (rate limit), retry after 5-10 seconds

---

## Agent Workflow

1. Verify prerequisites: `xurl --help` and `xurl auth status`.
2. **Check default app has credentials.** Parse the `auth status` output. The default app is marked with `▸`. If the default app shows `oauth2: (none)` but another app has a valid oauth2 user:
   - **Interactive sessions:** tell the user to run `xurl auth default <that-app> <username>` manually.
   - **Non-interactive / cron sessions:** run it yourself: `xurl auth default <app-name> <username>`. This is safe — it only changes the default routing, doesn't expose secrets.
3. If no app has any credentials at all, stop and direct the user to the "One-Time User Setup" section — do NOT attempt to register apps or pass secrets yourself.
4. Start with a cheap read (`xurl whoami`, `xurl user @handle`, `xurl search ... -n 3`) to confirm reachability.
5. Confirm the target post/user and the user's intent before any write action (post, reply, like, repost, DM, follow, block, delete).
6. Use JSON output directly — every response is already structured.
7. Never paste `~/.xurl` contents back into the conversation.

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Auth errors after successful OAuth flow | Token saved to `default` app (no client-id/secret) instead of your named app | `xurl auth oauth2 --app my-app` then `xurl auth default my-app` |
| `unauthorized_client` during OAuth | App type set to "Native App" in X dashboard | Change to "Web app, automated app or bot" in User Authentication Settings |
| `UsernameNotFound` or 403 on `/2/users/me` right after OAuth | X not returning username reliably from `/2/users/me` | Re-run `xurl auth oauth2 --app my-app YOUR_USERNAME` (xurl v1.1.0+) to pass the handle explicitly |
| 401 on every request | Token expired or wrong default app | Check `xurl auth status` — verify `▸` points to an app with oauth2 tokens |
| `client-forbidden` / `client-not-enrolled` | X platform enrollment issue | Dashboard → Apps → Manage → Move to "Pay-per-use" package → Production environment |
| `CreditsDepleted` | $0 balance on X API | Buy credits (min $5) in Developer Console → Billing |
| `media processing failed` on image upload | Default category is `amplify_video` | Add `--category tweet_image --media-type image/png` |
| Two "Client Secret" values in X dashboard | UI bug — first is actually Client ID | Confirm on the "Keys and tokens" page; ID ends in `MTpjaQ` |

---

## Notes

- **Rate limits:** X enforces per-endpoint rate limits. A 429 means wait and retry. Write endpoints (post, reply, like, repost) have tighter limits than reads.
- **Scopes:** OAuth 2.0 tokens use broad scopes. A 403 on a specific action usually means the token is missing a scope — have the user re-run `xurl auth oauth2`.
- **Token refresh:** OAuth 2.0 tokens auto-refresh. Nothing to do.
- **Multiple apps:** Each app has isolated credentials/tokens. Switch with `xurl auth default` or `--app`.
- **Multiple accounts per app:** Select with `-u / --username`, or set a default with `xurl auth default APP USER`.
- **Token storage:** `~/.xurl` is YAML. Never read or send this file to LLM context.
- **Cost:** X API access is typically paid for meaningful usage. Many failures are plan/permission problems, not code problems.

---

## Attribution

- Upstream CLI: https://github.com/xdevplatform/xurl (X developer platform team, Chris Park et al.)
- Upstream agent skill: https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
- Hermes adaptation: reformatted for Hermes skill conventions; safety guardrails preserved verbatim.
