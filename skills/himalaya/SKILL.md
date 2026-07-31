---
name: himalaya
description: "Gmail via Himalaya CLI — IMAP/SMTP with Google OAuth2. Preferred over gws for Gmail on this user's machine."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [Gmail, Email, OAuth2, IMAP, SMTP, Google]
    related_skills: [google-workspace]
tier: A
---

# Himalaya — CLI Email for Gmail

Himalaya is a Rust CLI email client. For this setup, it's configured with Google OAuth2 (PKCE, XOAUTH2) for `amyn@porbanderwala.com`. It is **preferred over gws for Gmail** because it avoids the keyring backend mismatches and `invalid_rapt` token errors that gws encounters in the Hermes desktop shell.

## Quick reference

| Command | What it does |
|---|---|
| `himalaya envelope list` | List inbox (recent) |
| `himalaya envelope list --folder "Sent Mail"` | List sent mail |
| `himalaya envelope list --page 2` | Next page |
| `himalaya envelope list --output json` | JSON output |
| `himalaya envelope search SUBJECT "keyword"` | Search by subject |
| `himalaya envelope search FROM "sender"` | Search by sender |
| `himalaya envelope search TEXT "body keyword"` | Search body text |
| `himalaya message read <ID>` | Read a message by ID |
| `himalaya folder list` | List all folders/labels |
| `himalaya account list` | Show configured accounts |
| `himalaya account doctor` | Diagnose account config |

Full path: `~/.cargo/bin/himalaya` (cargo-installed with features).

## Installation

```bash
# NOT the Homebrew bottle — it lacks oauth2/wizard features
brew uninstall himalaya 2>/dev/null

# Cargo install with required features
cargo install himalaya --locked --features oauth2,keyring,wizard
```

Verify:
```bash
~/.cargo/bin/himalaya --version
# Expected: himalaya v1.2.0 +wizard +oauth2 +keyring +imap +smtp
```

## Config file

Location: `~/.config/himalaya/config.toml`

```toml
[accounts.amyn]
default = true
email = "amyn@porbanderwala.com"
display-name = "Amyn Porbanderwala"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.login = "amyn@porbanderwala.com"
backend.auth.type = "oauth2"
backend.auth.method = "xoauth2"
backend.auth.client-id = "<client-id>"
# Client secret goes in keyring OR as backend.auth.client-secret.raw
backend.auth.auth-url = "https://accounts.google.com/o/oauth2/v2/auth"
backend.auth.token-url = "https://www.googleapis.com/oauth2/v3/token"
backend.auth.pkce = true
backend.auth.scope = "https://mail.google.com/"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.login = "amyn@porbanderwala.com"
message.send.backend.auth.type = "oauth2"
# ... same oauth2 fields as IMAP backend.auth above
```

**Key structural rules** (learned from parse errors):
- Accounts go under `[accounts.<name>]`, NOT `[<name>]` directly
- No `backend.encryption = "tls"` — this field doesn't exist in himalaya 1.2.0. Encryption is inferred from port (993 = implicit TLS, no config needed)
- OAuth2 auth is nested under `backend.auth.*` — `backend.oauth2.*` does NOT work
- Folder aliases for Gmail use `[Gmail]/` prefix: `[Gmail]/Sent Mail`, `[Gmail]/Drafts`, `[Gmail]/Trash`

## OAuth2 setup — wizard

The wizard is interactive and **requires PTY + background mode** in the Hermes terminal tool.

```bash
~/.cargo/bin/himalaya account configure amyn
```

The wizard walks through ~15 prompts. Defaults are almost always correct (press Enter). The only values you need to type:

1. **Enable OAuth 2.0?** → Enter (Y default)
2. **IMAP OAuth 2.0 client id:** → paste the full client ID
3. **IMAP OAuth 2.0 client secret:** → paste the client secret

After the last prompt (PKCE verification = Yes), the wizard prints a Google OAuth URL and starts an HTTP server. **Open that URL in Chrome.** The wizard receives the callback automatically, exchanges the code, and stores tokens in the system keyring.

From Hermes, driving the wizard through PTY:
```bash
# Start in background with PTY
terminal(background=true, pty=true, command="himalaya account configure amyn")

# For each prompt, send newline to accept default:
process(action="write", data="\n")

# For client ID / client secret, type the value followed by newline:
process(action="write", data="1075066238634-...\n")

# When the OAuth URL appears, extract it and open in Chrome:
terminal(command='open -a "Google Chrome" "<oauth-url>"')
```

## Token storage

Himalaya stores OAuth tokens via the **system keyring** (`keyring` feature). On macOS this is the Keychain. Tokens are auto-refreshed. No plain-text token files.

If tokens expire or are revoked:
```bash
himalaya account doctor    # diagnose issues
himalaya account configure amyn  # re-run wizard to re-auth
```

## Searching

```bash
# Full-text search (Gmail search syntax)
himalaya envelope search TEXT "HARBOR newer_than:14d"

# Subject search
himalaya envelope search SUBJECT "Aecon"

# From search
himalaya envelope search FROM "twashington@aecon.com"

# List with custom filter
himalaya envelope list --folder INBOX --page 1
```

## Reading messages

```bash
# Read by message ID (from envelope list output)
himalaya message read <ID>

# Read with JSON for parsing
himalaya message read <ID> --output json
```

## Pitfalls

### Homebrew bottle lacks oauth2/wizard — cargo install required

`brew install himalaya` gives v1.2.0 but WITHOUT `oauth2`, `keyring`, or `wizard` features. It will fail with `missing 'oauth2' cargo feature` when trying OAuth2 config. **Fix:** `brew uninstall himalaya && cargo install himalaya --locked --features oauth2,keyring,wizard`.

### Config format: accounts under [accounts.name], not [name]

Himalaya 1.2.0 expects `[accounts.amyn]`, not `[amyn]`. Wrong format produces: `unknown field 'amyn', expected one of 'display-name', 'name', 'accounts', 'account'`.

### No backend.encryption field — encryption is inferred from port

`backend.encryption = "tls"` or `backend.encryption.type = "tls"` both fail. Himalaya 1.2.0 infers encryption from port: 993 = implicit TLS, 143 = STARTTLS or none. Just omit the encryption field entirely.

### Auth nested under backend.auth, not backend.oauth2

`backend.oauth2.client-id = "..."` does NOT work. Use `backend.auth.type = "oauth2"` with `backend.auth.client-id = "..."`.

### Wizard requires PTY + background in Hermes terminal

The wizard is `inquire`-based (interactive TUI). Running it in foreground without PTY hangs. Use `terminal(pty=true, background=true)`.

### OAuth URL must be opened during wizard session

The wizard prints the URL and then waits for the local HTTP callback. The user must open the URL and approve the consent screen while the wizard is still running. If the wizard times out, re-run.

### Token storage depends on keyring feature

Without `keyring` feature, tokens can't be stored/retrieved. The error is: `cannot get oauth2 access token from global keyring`. Make sure `+keyring` appears in `himalaya --version`.
