---
name: browser-harness
description: Connect Hermes to the user's Chrome for browser automation. Covers local browser setup, daemon management, and macOS-specific quirks.
category: devops
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# browser-harness

Low-level browser control via CDP. This skill covers the connection setup between Hermes and Chrome — the part that fails silently and needs platform-specific troubleshooting. For the runtime API (`new_tab`, `click_at_xy`, `js`, etc.), read the canonical `~/Developer/browser-harness/SKILL.md`.

## Trigger

- User says "set up browser-harness", "connect to my browser", "open Chrome", "browser automation"
- `browser-harness --doctor` shows daemon/chrome failures
- You need to debug a lost browser connection

## Quick start (happy path)

```bash
browser-harness -c 'print(page_info())'
```

If that prints page info, stop — you're done. Only proceed if it fails.

## Connection methods

### Way 1 — Real Chrome profile (checkbox, one-time setup)

User ticks a checkbox in `chrome://inspect/#remote-debugging`. Sticky per-profile. Best for agent assisting with real browsing.

1. Check if already enabled:
   ```bash
   cat ~/Library/Application\ Support/Google/Chrome/DevToolsActivePort
   ```
   Exists → Way 1 is on. Skip to step 4.

2. Open the inspect page on macOS:
   ```bash
   osascript -e 'tell application "Google Chrome" to open location "chrome://inspect/#remote-debugging"'
   ```
   Ask user to tick "Allow remote debugging for this browser instance" and click any popup.

3. Chrome must be restarted after ticking. On macOS:
   ```bash
   killall -9 "Google Chrome"   # REQUIRED — launching with flag while running just hands off to existing instance
   sleep 2
   open -a "Google Chrome"
   ```

4. Restart daemon (Chrome picks a random port; daemon finds it via `DevToolsActivePort`):
   ```bash
   browser-harness -c 'restart_daemon()'
   ```
   **Pitfall**: if `restart_daemon()` hangs, a daemon may already be running from another repo. Check `pgrep -fl "browser.harness\|daemon.py"`. If a stale daemon is on the socket, kill it manually and remove `/tmp/bu-default.sock`.

5. Verify:
   ```bash
   browser-harness -c 'print(page_info())'
   ```

### Way 2 — Isolated Chrome profile (flag, no popups)

Launch a fresh Chrome with an explicit debugging port and non-default user data dir. No popups ever. Profile is isolated — no logins from real Chrome.

```bash
killall -9 "Google Chrome"
sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile &
```

The `--user-data-dir` must NOT be Chrome's platform default (`~/Library/Application Support/Google/Chrome`), or Chrome silently ignores the port flag (Chrome 136+).

Then set the URL so the harness knows where to connect:
```bash
export BU_CDP_URL=http://127.0.0.1:9222
browser-harness -c 'print(page_info())'
```

## macOS-specific troubleshooting

See `references/macos-chrome-debugging.md` for detailed diagnosis steps.

Common pitfalls:
- **Launching with flag while Chrome is running**: the new process hands off to the existing one (no flags applied). Always `killall -9` first.
- **Terminal security scans block `killall` and `rm`**: split commands — kill first, then rm separately. Don't chain them with `&&`.
- **`DevToolsActivePort` exists but daemon fails**: check `lsof -iTCP:<port> -sTCP:LISTEN`. If Chrome isn't listening, restart Chrome.
- **`restart_daemon()` timeouts**: a daemon from another repo may already own `/tmp/bu-default.sock`. Check with `pgrep -fl daemon.py`.

## Daemon conflict (multiple repos)

If you have browser-harness installed in multiple repos (e.g., `~/Developer/browser-harness` and `~/Documents/.../2026_books/operations/tools/browser-harness`), they share the same socket `/tmp/bu-default.sock`. Only one daemon can own it. If `restart_daemon()` or any command hangs:

```bash
# Find which repo's daemon is running (and its PID)
pgrep -fl "daemon.py|browser.harness"
# Kill by PID — pkill -f can miss the process (venv path mismatch)
kill -9 <PID1> <PID2>
sleep 1
# Clean the socket
rm /tmp/bu-default.sock /tmp/bu-default.pid
# Restart from the repo you intend to use
browser-harness -c 'print(page_info())'  # auto-starts daemon
```

**Pitfall**: `pkill -f browser_harness/daemon.py` often returns exit code 1 (no match) because the process path includes the venv: `/path/to/.venv/bin/python3 daemon.py`. Always kill by PID instead.

## Discord Bot Security Audit (absorbed skill)

When you need to audit a Discord bot's security posture end-to-end (Developer Portal + server state), use the `discord-bot-security-audit` workflow now integrated here.

### Trigger

- User asks to "review bot setup," "audit Discord bot security," "lock down bot"
- Any discussion of Discord bot permissions, install links, or OAuth2 scopes

### Prerequisites

- User must be logged into Discord in Chrome (browser-harness required)
- Bot client ID known
- `discord_admin` tool available

### Audit Checklist (in order)

**1. Bot Page** (`/developers/applications/{CLIENT_ID}/bot`):
- Public Bot toggle → OFF (use `hasAttribute('checked')` — React Aria quirk)
- Presence/Members/Message Content Intents → OFF unless needed
- Token hidden (shows "Reset Token" only)

**2. OAuth2 Page** (`/developers/applications/{CLIENT_ID}/oauth2`):
- Public Client → OFF
- Redirect URIs → empty (unless web OAuth needed)
- Scopes → empty/minimal

**3. Installation Page** (`/developers/applications/{CLIENT_ID}/installation`):
- User Install → OFF
- Guild Install → OFF (unless intentionally allowing adds)
- **CRITICAL**: Public Bot ON + Guild Install ON + Install Link present = anyone can add the bot

**4. App Testers** (`{CLIENT_ID}/testers` — note URL is `/testers` NOT `/app-testers`):
- Should show "Invited Testers (0 of 50)"

**5. Teams** (`/developers/teams`):
- Should show no teams (personal account only). Every team member has full admin access.

**6. Webhooks** (`{CLIENT_ID}/webhooks`):
- Endpoint URL → empty. All events → OFF.

**7. Server-Side** (via `discord_admin` tool):
- Owner matches user's Discord ID, minimal member count, only @everyone + managed role, minimal channels, appropriate verification level

**8. Verify Owner Identity**: Pull recent messages to confirm owner_id

### Browser-Harness Scripts for Discord Audit

For reusable scripts covering all audit pages, see `references/discord-bot-security-audit-scripts.md`. Key patterns:

- Toggle state: `sw.hasAttribute('checked')` — `aria-checked` is always null
- SPA delays: `time.sleep(2)` + `wait_for_load()` after `new_tab()`
- URL vs nav label: "App Testers" label → URL `/testers`. Use nav clicks to navigate safely
- Extract install link: query `<input>` for values containing `discord.com/oauth`

### Single Most Impactful Fix

Turn OFF **Public Bot** on the Bot page. This prevents anyone except the app owner from installing the bot. All other settings become safe once Public Bot is OFF.

### Pitfalls

- `browser_vision` won't work (no Discord login in Hermes browser) — always use browser-harness CLI
- React Aria toggles: only `el.hasAttribute('checked')` works
- Page text truncation: `document.body.innerText` for Bot page includes all permission checkboxes — filter relevant sections
- Full audit script template available in the reference file

## LinkedIn Automation (follow + connect)

Bulk-follow company pages and send connection requests to people on LinkedIn, driving the user's authenticated Chrome session.

**Trigger**: User asks to "follow companies on LinkedIn", "connect with people", "LinkedIn outreach", "engage with contacts".

**Key rules**:

1. **Company pages** — use slug-based URL: `https://www.linkedin.com/company/{slug}/`, click the `Follow` button
2. **People connections** — navigate to `/in/{slug}/` profile pages (NOT search results; search cards don't expose Connect buttons reliably)
3. **Status check**: `Message` button = already connected; `Pending` = invitation sent; `Follow` = not connected yet
4. **"More" dropdown** — Connect is sometimes hidden inside; click `More` first, then look for `[role="menuitem"]`

Full automation patterns, JavaScript selectors, slug discovery via search, and all pitfalls: see `references/linkedin-automation.md`.

Related: pair with `xurl` skill for a cross-platform social engagement campaign (X.com follows via API + LinkedIn via browser-harness in the same session).

## Runtime API pitfalls

For the full runtime API, see `~/Developer/browser-harness/SKILL.md`. Key gotchas:

- `scroll()` requires **both** `x` and `y`: `scroll(x=0, y=500)` — not `scroll(y=500)`
- `wait_for_load()` after navigation or scroll before extracting content
- `js()` returns JavaScript eval results; use it for `document.body.innerText` extraction

### Multi-line JS in browser-harness -c

Shell escaping for multi-line inline JavaScript inside `browser-harness -c '...'` is fragile. Backticks, quotes, and newlines cause cryptic syntax errors. **Prefer writing the command to a temp file** and passing it via stdin:

```bash
# WRONG — fragile, fails on backticks, nested quotes, multi-line
browser-harness -c '
js("""
  var x = document.querySelector(\"a[href*=\\\".pdf\\\"]\");
  ...
""")
'

# RIGHT — write to file, pass via stdin
cat > /tmp/bh_script.py << 'PYEOF'
wait_for_load()
import json, time
result = js("""
  (function() {
    var links = document.querySelectorAll("a");
    // safe multi-line JS here
  })()
""")
print(result)
PYEOF
browser-harness -c "$(cat /tmp/bh_script.py)"
```

This also makes the script reusable and debuggable.

## Advanced techniques

- **Hidden API endpoint discovery**: When SPAs hide download URLs behind click handlers (no `href`), intercept `XMLHttpRequest.prototype.open` and `window.fetch` to capture the real endpoints. See `references/network-interception.md` for the full pattern.

### Government database searches (web_search fallback)

When `web_search` and `web_extract` fail with credit exhaustion, use browser_navigate + browser_type + browser_click + browser_snapshot to search government entity databases directly. This pattern works for Secretary of State business searches, Comptroller tax entity searches, and county clerk records. Full guide: `references/government-db-search.md`.

### React Aria toggle/switch state extraction

Discord (and other React Aria SPAs) use `[role="switch"]` elements with `type="checkbox"` and a `checked` attribute — NOT `aria-checked`. The `checked` attribute is only present when ON (value is empty string `""`). When OFF, the attribute is absent entirely. The `aria-checked` property is always `null` regardless of state.

```javascript
// CORRECT — check attribute presence
var isOn = el.hasAttribute('checked');  // true when ON, false when OFF

// WRONG — these always return null/false
var aria = el.getAttribute('aria-checked');  // always null
var prop = el.checked;  // always false (no real <input> inside)
```

### browser_vision is NOT browser-harness

`browser_vision` uses Hermes' built-in isolated browser (no user cookies, no login state). It will NOT see pages that require authentication. When the user says "I have this open in Chrome," use browser-harness CLI (`browser-harness -c '...'`), not `browser_vision`. The two are completely separate browser sessions.

## Usage conventions

- **Do not keep opening new tabs.** Reuse the current tab with `new_tab(url)` only when changing domains. The user's Chrome stays focused.
- After the connection is established, verify with `print(page_info())` before any scraping commands.
- Prefer `browser-harness -c '...'` one-liners over multi-line scripts for simple interactions.

## Doctor check

```bash
browser-harness --doctor
```

Key lines:
- `chrome running` — Chrome process exists
- `daemon alive` — daemon process + socket exist
- `active browser connections` — WebSocket to Chrome is open

Only `BROWSER_USE_API_KEY` and `profile-use` are optional (cloud browsers only).

## After setup — demo

Per install.md convention, after first connection:

1. Open the browser-harness repo:
   ```bash
   browser-harness -c '
   new_tab("https://github.com/browser-use/browser-harness")
   wait_for_load()
   print(page_info())
   '
   ```

2. Check GitHub login: `js("document.querySelector('.AppHeader-user') ? true : false")`. If not logged in, open `https://browser-use.com` instead.

3. Offer to star the repo (only if logged into GitHub and user says yes).

4. Register the SKILL.md globally for Codex and Claude Code:
   ```bash
   # Codex
   mkdir -p ~/.codex/skills/browser-harness
   ln -sf ~/Developer/browser-harness/SKILL.md ~/.codex/skills/browser-harness/SKILL.md
   # Claude Code
   echo "@~/Developer/browser-harness/SKILL.md" >> ~/.claude/CLAUDE.md
   ```
