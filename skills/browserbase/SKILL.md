---
name: browserbase
version: 1.0.0
description: Browser automation with Browserbase CLI — local/remote Chrome, Fetch/Search APIs, cloud session management, and templates.
tags: [browser, automation, cli, browserbase, scrape, web]
trigger: browser automation, web scraping, browse pages, click elements, fill forms, screenshot
---

# Browserbase AI Agent Automation

**CLI tool:** `browse` — unified interface to browser automation, Fetch/Search APIs, cloud management  
**Modes:** Local (no API key) vs Remote (Browserbase-hosted, handles CAPTCHAs/Cloudflare)

---

## Setup

### Required: Install CLI
```bash
npm install -g browse
```

### Remote/Cloud Features (Browserbase-hosted sessions)
1. Get API key from https://browserbase.com/settings
2. Export it: `export BROWSERBASE_API_KEY="your_key"`
3. Install agent skills: `browse skills install`
4. Verify: `browse cloud projects list`

### Local Mode (default, no API key required)
- Uses local Chrome/Chromium
- Faster, isolated sessions
- Reuse cookies/logins with `--auto-connect`

---

## Tool Selection

| Need | Use | Why |
|------|-----|-----|
| Click, type, scrape JS pages | `browse` CLI | Full browser with interaction |
| Get HTML/JSON from static page | **Fetch API** | Fast, no browser needed |
| Find URLs for a topic | **Search API** | Structured results, no browsing |
| Manage projects, sessions, contexts | `browse cloud` | Cloud admin |
| Run automation on schedule | `browse functions` | Functions dev/deploy |
| Scaffold starter project | `browse templates` | Examples |
| Diagnose setup issues | `browse doctor` | Environment checks |

---

## Browser Automation Commands

### Environment Flags
- `--local` — Clean isolated local Chrome session
- `--auto-connect` — Reuse running local Chrome (keeps cookies/logins)
- `--cdp <port/url>` — Attach to specific Chrome DevTools Protocol
- `--remote` — Browserbase-hosted (CAPTCHAs, Cloudflare, proxies)
- `--session <name>` — Name the session (for state persistence)

### Core Workflow

**1. Open page**
```bash
browse open <url> [--local|--remote]
```

**2. Understand page state** (read refs, accessibility tree)
```bash
browse snapshot [--compact]
```
Returns refs like `@0-5`, `@1-3`, etc. that you use for interactions.

**3. Interact with elements**
```bash
# Click a button/link
browse click @0-5

# Fill a text field and submit
browse fill @0-8 "search query" --press-enter

# Type characters directly
browse type "Hello"
browse press Enter

# Select dropdown option
browse select "select[name=country]" "United States"

# Upload a file
browse upload @0-12 ./file.pdf
```

**4. Confirm action with another snapshot**
```bash
browse snapshot
```

**5. Stop browser when done**
```bash
browse stop
```

### Navigation & State
```bash
browse open <url>          # Open page
browse reload              # Refresh current page
browse back                # Go back in history
browse forward             # Go forward
browse wait load           # Wait for page to fully load
browse wait selector "#id" --state visible  # Wait for element
browse refs                # List interactive elements (quick)
browse get url             # Get current URL
browse get title           # Get page title
browse get markdown body   # Get page as markdown
```

### Mouse Actions
```bash
browse mouse click <x> <y>
browse mouse hover <x> <y>
browse mouse drag <x1> <y1> <x2> <y2>
browse mouse scroll <x> <y> <dx> <dy>
browse viewport 1280 720   # Set viewport size
```

### Screenshot
```bash
# Only take screenshot when you need visual context, not every step
browse screenshot --path page.png
```

### Tabs, Network & Sessions
```bash
browse tab list                    # List open tabs
browse tab new <url>               # Open new tab
browse tab switch <id>             # Switch to tab
browse tab close <id>              # Close tab

browse network on                  # Start intercepting network
browse network path                # Filter network requests
browse network clear               # Clear network events

browse doctor [--json]             # Environment diagnostics
browse status [--session <name>]   # Active session info
browse stop [--force]              # Stop browser
```

---

## Fetch API (no browser needed)

When you just need the page content without a full browser session.

**CLI:**
```bash
browse cloud fetch <url> [--allow-redirects] [--proxies] [--output page.html]
```

**What it returns:** HTML, status code, redirects, headers

**Use when:**
- Getting structured data (JSON)
- Simple HTTP GET/POST
- No JavaScript execution needed
- Static pages only

---

## Search API (find URLs for a topic)

Structured web search that returns ranked results.

**With CLI:**
```bash
browse cloud search "<query>" --limit 10 --language en --region us
```

**Direct API:**
```bash
curl https://api.browserbase.com/v1/search \
  -H "X-BB-API-Key: $BROWSERBASE_API_KEY" \
  -d '{"query":"modern web design","limit":10}'
```

**Returns:** List of results with `title`, `url`, `rank`, `description`

---

## Cloud Management

Manage Browserbase-hosted resources. All `browse cloud` commands use Remote by default.

### Projects
```bash
browse cloud projects list
browse cloud projects create "My Project" --description "My description"
browse cloud projects set <project-id>
```

### Sessions (persistent workspaces)
```bash
browse cloud sessions list
browse cloud sessions create --project <id> --name "my-session" --timeout 3600
browse cloud sessions get <session-id>
browse cloud sessions url <session-id>  # Get connectable URL
browse cloud sessions delete <session-id>
```

### Contexts (saved browser state)
```bash
browse cloud contexts list
browse cloud contexts create --project <id> --name "logged-in-state"
browse cloud contexts get <context-id>
browse cloud contexts set <context-id>  # Apply to new sessions
browse cloud contexts delete <context-id>
```

### Profiles (persistent identity storage)
```bash
browse cloud profiles list
browse cloud profiles create --project <id> --name "my-chrome-profile"
browse cloud profiles get <profile-id>
browse cloud profiles url <profile-id>  # Interactive CDP connection details
browse cloud profiles delete <profile-id>
```

### Extensions (inject Chrome extensions)
```bash
browse cloud extensions list
browse cloud extensions create --project <id> --extension <id> --folder ./ext-dir
browse cloud extensions update <ext-id> --folder ./updated-ext
browse cloud extensions download <ext-id>
browse cloud extensions delete <ext-id>
browse cloud extensions get <ext-id>   # Get latest version
browse cloud extensions set <ext-id> <version>  # Set as active
```

### Functions (cron/webhook automation)
```bash
browse cloud functions list
browse cloud functions get <function-id>
browse cloud functions delete <function-id>
browse cloud functions invoke <name>    # Trigger function
browse cloud functions runs get <run-id>
browse cloud functions logs <run-id> --limit 100
```

---

## Functions Development

Build automation that runs on schedule/webhook with full browser access.

**Commands:**
```bash
browse functions init my-function --template typescript  # Create project
browse functions run                # Local dev (localhost:5001)
browse functions deploy             # Deploy to Browserbase Cloud
browse functions invoke <name>      # Test deployed function
```

**Triggers:** `cron` (schedule), `webhook` (URL), `manual`

**Available in function code:**
- Full browser (`open`, `snapshot`, `click`, `fill`, `screenshot`)
- Search API (`search("query", {limit:10})`)
- Secrets (`process.env.MY_API_KEY`)
- Contexts & Profiles (set in project settings)

---

## Templates (scaffold examples)

```bash
browse templates list
browse templates create browser-captcha-solving --out ./my-captcha
# Options: browser-captcha-solving, browser-form-submission-wait, 
#          browser-google-search, browser-scrape-tables, browser-verify-download
```

---

## Diagnostic Tool

When setup fails, run:
```bash
browse doctor [--json]
```

Checks:
- ✓ CLI version
- ✓ `BROWSERBASE_API_KEY` set
- ✓ API connectivity
- ✓ `BROWSER_PATH` or local Chrome found
- ✓ `~/.bb` directory exists

---

## Practical Examples

### Scrape a website
```bash
browse open "https://example.com"
browse wait load
browse snapshot
browse get markdown body
browse stop
```

### Fill a form
```bash
browse open "https://example.com/form"
browse snapshot  # Find the form field refs
browse fill @0-12 "John Doe"
browse fill @0-13 "john@email.com"
browse select @0-14 "California"
browse click @0-15  # Submit button
browse wait load
browse snapshot  # Confirm success
browse stop
```

### Automate a multi-step workflow
```bash
# Step 1: Login (reuse cookies with --auto-connect)
browse open "https://app.example.com" --auto-connect
browse snapshot
browse fill @0-3 "my@email.com"
browse fill @0-4 "password"
browse click @0-5  # Login button
browse wait load

# Step 2: Navigate to dashboard
browse open "https://app.example.com/dashboard"
browse snapshot
browse get markdown body > /tmp/data.md

# Step 3: Export data (if needed)
browse click @0-20  # Export button
browse wait load
browse get markdown body > /tmp/exported.md
browse stop
```

---

## Common Patterns

### Reusing a logged-in session
```bash
# First time: login + save context
browse open "https://app.com" --local --session my-login
# ... fill login form, click submit ...
browse cloud contexts create --project <id> --name "logged-in"
browse stop

# Later: reuse the saved state
browse open "https://app.com/dashboard" --local --auto-connect
# Already logged in!
```

### Handling protected sites
```bash
# Use --remote to handle Cloudflare, CAPTCHAs, etc.
browse open "https://protected-site.com" --remote
browse snapshot
# Browserbase handles the protection automatically
```

### Waiting for dynamic content
```bash
browse open "https://site.com"
browse wait selector "#dynamic-content" --state visible
browse snapshot
# Now #dynamic-content is in the accessibility tree
```

---

## Pitfalls & Solutions

### Problem: "No Chrome found"
**Solution:** Set the path explicitly:
```bash
export BROWSER_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Or on Linux:
export BROWSER_PATH="/usr/bin/chromium-browser"
```

### Problem: Page not loading
**Solution:** Always `browse wait load` before taking actions:
```bash
browse open <url>
browse wait load
browse snapshot
```

### Problem: "Element not interactive"
**Solution:** Wait for the specific element to be visible/clickable:
```bash
browse wait selector "#btn" --state visible
browse click @0-5
```

### Problem: Network requests aren't working
**Solution:** Enable network interception first:
```bash
browse network on
# ... do your actions ...
browse network path   # See what happened
```

### Problem: Login form won't persist
**Solution:** Use `--auto-connect` to reuse cookies:
```bash
browse open <url> --auto-connect --session my-session
```

---

## Command Reference Cheat Sheet

```bash
# Setup
npm install -g browse
browse skills install
export BROWSERBASE_API_KEY="<key>"

# Basic workflow
browse open <url> --local
browse snapshot
browse click @ref
browse fill @ref "text"
browse snapshot
browse stop

# Advanced
browse wait load
browse wait selector "#id" --state visible
browse tab new <url>
browse screenshot --path img.png
browse get markdown body

# Diagnostics
browse doctor
browse status --session my-session

# Cloud management
browse cloud projects list
browse cloud sessions create
browse cloud contexts list
browse cloud functions list

# Functions dev
browse functions init
browse functions run
browse functions deploy
browse functions invoke <name>
```
