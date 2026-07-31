---
name: infrastructure
description: "Amyn's server infrastructure — Hostinger VPS, WalaGPT, picoclaw, Lenovo, and their production services, Hermes deployments, Docker fleets, and KB pipelines."
version: 1.0.0
tags: [infrastructure, servers, production, deployment, docker, systemd, caddy, tailscale]
tier: D
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Infrastructure

Amyn's server infrastructure — production VPS, local machines, and their services. Load this skill when working with Amyn's servers, investigating production deployments, setting up new services, or troubleshooting infrastructure issues.

## When to load this skill

- SSHing into any of Amyn's servers (Hostinger, WalaGPT, picoclaw, AP-Desktop)
- Investigating what's running where
- Checking tailscale status or running tailscale commands
- Troubleshooting production issues
- Troubleshooting production issues
- Planning infrastructure changes
- Understanding the Docker/Caddy/systemd landscape

## Servers

| Server | Hostname | IP | User | Access |
|--------|----------|----|------|--------|
| Hostinger VPS | srv1147959 | 72.61.15.208 (public, :22 filtered) / 100.90.143.51 (tailnet) | amynporb | `ssh hostinger` — tailnet-only via `wala-srv` MagicDNS |
| WalaGPT | — | 208.113.133.38 | ubuntu | `ssh WalaGPT` — `~/.ssh/walagpt.pem` |
| picoclaw | — | 192.168.1.236 | amynporb | `ssh_picoclaw` alias — ed25519 key |
| Lenovo (SOCKS) | — | 100.100.221.52 (Tailscale) | amynporb | `socks-tunnel-lenovo.service` on Hostinger |
| AP-Desktop | ap-desktop | 100.68.66.103 (tailnet) | amyn (likely) | Tailscale SSH — web-approval required before first access. DNS: `ap-desktop.tail003f9d.ts.net.` OS: Linux. Online as of Jun 2026. |

### SSH config (local `~/.ssh/config`)

```
# Hostinger VPS — SSH is tailnet-only (public :22 filtered as of 2026-05-07).
# Reach via Tailscale MagicDNS (wala-srv) or raw tailnet IP 100.90.143.51.
Host hostinger
    HostName wala-srv
    User amynporb
    IdentityFile ~/.ssh/id_hostinger_amynporb_ed25519
    IdentitiesOnly yes

Host hostinger-root
    HostName wala-srv
    User root
    IdentityFile ~/.ssh/id_hostinger_amynporb_ed25519
    IdentitiesOnly yes
```

Local aliases in `~/.zshrc`:
- `ssh_hostinger` → `ssh hostinger` (amynporb user, tailnet-only)
- `ssh_hostinger!` → `ssh root@hostinger` (root via tailnet)

### Hostinger VPS State (as of May 2026 — updated May 7)

The server migrated from `/opt/ai/v3/` to `/opt/stacks/`. **`/opt/ai/v3/` no longer exists.** Caddy now runs as a systemd service (not Docker). 26 Docker containers across 2 networks (`proxy` + `supabase_default`). Swap is nearly exhausted at 2G/2G — memory pressure flag.

**Key paths (current)**:

| What | Path |
|------|------|
| Docker Compose files | `/opt/stacks/*/source/docker-compose.yml` or `/opt/stacks/*/compose.yml` |
| Caddy main config | `/etc/caddy/Caddyfile` (imports `/etc/caddy/sites/*.caddy`) |
| Caddy site configs | `/etc/caddy/sites/<app>.caddy` (one per subdomain) |
| Landing page | `/var/www/porbanderwala.cloud/index.html` (static HTML/CSS) |
| Shared env | `/opt/stacks/.env.shared` |
| Secrets | Per-app: `/opt/stacks/<app>/.env` (gitignored) |
| Supabase self-host | `/opt/stacks/supabase/compose.yml` (full stack: Kong, GoTrue, PostgREST, etc.) |

## Server Architecture (current)

- **OS**: Ubuntu 24.04, kernel 7.0.0, 2 vCPU, 7.7 GiB RAM, 96 GB NVMe (27G used)
- **Docker**: Engine 29.4.3, Compose v5.1.3
- **Caddy**: systemd service, `/usr/bin/caddy run --config /etc/caddy/Caddyfile`
- **Tailscale**: hostname `wala-srv`, IP `100.90.143.51`
- **Container pattern**: All app containers bind to `127.0.0.1` — Caddy is the sole reverse proxy
- **Deployment pattern**: `/opt/stacks/<app>/source/` (repo clone) + `/opt/stacks/<app>/docker-compose.yml` (or `compose.yml`) + `/etc/caddy/sites/<app>.caddy`

## Docker Containers (26 total)

### Application Services (proxy network, 127.0.0.1 bound)

| Container | Image | Port | Subdomain |
|-----------|-------|------|-----------|
| econpulse | econpulse-app | 127.0.0.1:3001 | econpulse.porbanderwala.cloud |
| sbir | sbir-app | 127.0.0.1:3002 | sbir.porbanderwala.cloud |
| govradar | govradar-app | 127.0.0.1:3003 | govradar.porbanderwala.cloud |
| khidmat | khidmat-app | 127.0.0.1:3004 | khidmat.porbanderwala.cloud (tailnet-only) |
| farchat | farchat-app | 127.0.0.1:3005 | farchat.porbanderwala.cloud |
| umami | umami:postgresql-latest | 127.0.0.1:3010 | umami.porbanderwala.cloud |
| uptime-kuma | louislam/uptime-kuma:1 | 127.0.0.1:3011 | status.porbanderwala.cloud |
| vaultwarden | vaultwarden/server:latest | 127.0.0.1:8222 | vault.porbanderwala.cloud (tailnet-only) |
| ops-disk-pusher | alpine:3 | — | (disk heartbeat to Kuma) |

### Infrastructure (bridge network)

| Container | Image | Port |
|-----------|-------|------|
| redis | redis:7-alpine | 127.0.0.1:6379 |
| coredns | coredns/coredns:1.12.0 | 100.90.143.51:53 tcp/udp |
| docker-socket-proxy | tecnativa/docker-socket-proxy:latest | 2375/tcp |

### Supabase Self-Hosted Stack (supabase_default network)

| Container | Image | Port |
|-----------|-------|------|
| supabase-db | supabase/postgres:15.8.1.085 | 5432 (shared postgres via Supavisor) |
| supabase-pooler | supabase/supavisor:2.7.4 | 127.0.0.1:5432, 127.0.0.1:6543 |
| supabase-kong | kong/kong:3.9.1 | 127.0.0.1:8000 |
| supabase-studio | supabase/studio:2026.04.27 | 127.0.0.1:3000 |
| supabase-auth | supabase/gotrue:v2.186.0 | — |
| supabase-rest | postgrest/postgrest:v14.8 | — |
| supabase-realtime | supabase/realtime:v2.76.5 | — |
| supabase-storage | supabase/storage-api:v1.48.26 | — |
| supabase-edge-functions | supabase/edge-runtime:v1.71.2 | — |
| supabase-analytics | supabase/logflare:1.36.1 | — |
| supabase-meta | supabase/postgres-meta:v0.96.3 | — |
| supabase-vector | timberio/vector:0.53.0-alpine | — |
| supabase-imgproxy | darthsim/imgproxy:v3.30.1 | — |

**Landing page**: Static HTML/CSS at `/var/www/porbanderwala.cloud/index.html`. Title: "amyn porbanderwala — marine. builder. author." JetBrains Mono font, dark theme. Umami analytics on all subdomains.

**Live subdomains** (all TLS via Caddy/Let's Encrypt):

| Subdomain | App | Stack | Access |
|-----------|-----|-------|--------|
| porbanderwala.cloud | Static landing | HTML/CSS | Public |
| econpulse.porbanderwala.cloud | EconPulse dashboard | Next.js 15 + Turbopack | Public |
| sbir.porbanderwala.cloud | SBIR Portal | Next.js 15 + Turbopack | Public |
| govradar.porbanderwala.cloud | GovRadar (EO monitor) | Next.js 15 + Turbopack | Public |
| farchat.porbanderwala.cloud | FARchat (AI for FAR) | Next.js 15 + Turbopack | Public |
| khidmat.porbanderwala.cloud | Khidmat | Next.js 15 | Tailnet-only |
| status.porbanderwala.cloud | Uptime Kuma status | Kuma standalone | Public (admin: tailnet) |
| umami.porbanderwala.cloud | Umami analytics | Next.js 15 | Mixed (tracker public, admin tailnet) |
| supabase.porbanderwala.cloud | Supabase Studio | Kong+Studio | Mixed (API public, studio tailnet) |
| vault.porbanderwala.cloud | Vaultwarden | Standalone | Tailnet-only |

**Dead subdomains** (DNS resolves but TLS fails — no Caddy config):
`auth.`, `ai.`, `dashboard.`, `notes.`, `api.`, `admin.`, `coredns.`, `traefik.` — these are remnants from the v3 architecture that was superseded.

## Current Deployment Pattern

New services follow this convention (discovered May 2026):

1. **Repo clone**: `/opt/stacks/<app>/source/` (git clone of the project)
2. **Docker Compose**: `/opt/stacks/<app>/compose.yml` or `docker-compose.yml` — builds or pulls images, binds to `127.0.0.1:<port>`
3. **Caddy config**: `/etc/caddy/sites/<app>.caddy` — reverse proxy from `<app>.porbanderwala.cloud` to `127.0.0.1:<port>`
4. **Env/Secrets**: `/opt/stacks/<app>/.env` (gitignored, never in repo)
5. **Shared env**: `/opt/stacks/.env.shared` for cross-app vars (API keys, DB URLs)
6. **Caddy reload**: `caddy validate --config /etc/caddy/Caddyfile && systemctl reload caddy`

**Tailnet perimeter**: Admin UIs (Kuma admin, Vaultwarden, Supabase Studio, Umami admin, Khidmat) are restricted to Tailscale IPs (`100.64.0.0/10`) via Caddy `remote_ip` matchers.

**Shared Postgres**: `supabase-db` serves all apps via Supavisor pooler at `127.0.0.1:5432`. Apps connect to their own databases within the same Postgres instance.

## Reference files

- `references/caddy-hermes-dashboard.md` — Caddy reverse proxy setup for Hermes dashboard: eliminate port 9119 from URLs, Host header passthrough fix for uvicorn, system LaunchDaemon for port 80 binding.
- `references/hermes-dashboard-config.md` — Dashboard config keys, launch flags, `--tui` backcompat note, gateway auto-spawn race, restart pattern, verification commands.
- `references/static-site-deployment.md` — Static HTML/MP3 site deployment on Hostinger VPS with Caddy. Steps, Caddy config pattern, verification, and pitfalls (used for client-facing assessment reports with podcast integration).
- `references/docker-build-dns-hostinger.md` — Docker build DNS failures on Hostinger VPS: apt-get can't reach deb.debian.org despite daemon DNS config. Fix with `--network=host` on `docker build`. Also covers Alpine→Debian migration for native binary compatibility (e.g. @vercel/og).
- `references/hostinger-server.md` — Full Hostinger VPS architecture: Docker fleet, systemd services, Hermes Agent deployment, KB pipeline, Caddy routes, cron jobs, security posture. *Note: some sections reference pre-May-2026 v3 architecture that used `/opt/ai/v3/` — current state is `/opt/stacks/` with 26 containers, Caddy as systemd.*
- `references/hermes-remote-survey.md` — Reusable SSH heredoc technique for comprehensively surveying any remote Hermes deployment (skills, cron, profiles, services, config) in one round-trip. Includes macOS launchd equivalents and pitfall documentation.
- `references/hostinger-to-local-recreation.md` — Active migration plan: Hostinger → local dev Mac. Selective skill transfer, interview-first cron migration, commented-out .env key pitfall, Tailscale HTTPS setup, profile fixing.
- `references/hostinger-v3-deploy-lessons.md` — Deployment pitfalls from the May 2026 rebuild: heredoc quoting nightmares, Caddy syntax, Authelia fixes, Postgres init SQL, Docker Compose dependency healing. *Note: many paths reference `/opt/ai/v3/` which no longer exists — apply the lessons, not the literal paths.*
- `references/vercel-static-deployment.md` — Vercel static site deployment: fast, no-server alternative to Hostinger for dashboards and single-page apps. Pattern, comparison table, pitfalls.
- `references/discord-thread-management.md` — Discord thread cleanup and bulk message deletion for the Hermes-MBP bot. Bot token location, curl API patterns, rate limiting, and the decision tree: when to nuke messages vs. create a fresh thread.
- `references/macos-disk-cleanup.md` — Local macOS disk cleanup: finding/clearing caches, node_modules, virtual envs, npx artifacts. Commands for discovery, size ranking, and deletion. Pitfalls: SIP-protected dirs, VSCode locks, npm timeout on large dirs.
- `templates/docker-rebuild.sh` — Starter template for Docker service rebuilds on Hostinger. Customize SERVICE_NAME, REPO_DIR, COMPOSE_DIR.
- `templates/static-site-deploy.sh` — Deploy a static HTML site to Hostinger via scp + Caddy. Tailscale required.

## Deployment Pitfalls (v3 Rebuild)

### Static Site Deployment (No Docker)
For simple HTML/MP3 deliverables, use pure static hosting — no Docker, no app needed:

```bash
# On server
mkdir -p /opt/stacks/<app>
# scp files from local → hostinger:/tmp/
# ssh hostinger 'mv /tmp/file /opt/stacks/<app>/'
chmod 644 /opt/stacks/<app>/*
```

Caddy config (`/etc/caddy/sites/<app>.caddy`):
```
<app>.porbanderwala.cloud {
    tls info@porbanderwala.cloud
    encode gzip
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
    root * /opt/stacks/<app>
    file_server {
        index index.html
    }
}
```

Validate and reload: `caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy`

Pitfall: `amynporb` user cannot write to `/etc/caddy/sites/`. Use `sudo tee` through a pipe after ssh: `cat file.caddy | ssh hostinger "sudo tee /etc/caddy/sites/file.caddy"`. Verify with `curl -k -s https://subdomain.porbanderwala.cloud/`.

### `docker compose up -d` triggers Hermes terminal watchdog

Hermes' terminal tool detects `docker compose up -d` as a long-lived server process and refuses to run it in foreground mode. **Workaround**: use `background=true` with `notify_on_complete=true` and poll with `process(action='wait')`. Check progress directly with `docker ps` in a separate terminal call if the background process is slow.

### SSH + bash -c + heredoc quoting: triple-escape nightmare

When running multi-line scripts through `ssh hostinger 'bash -c "..."'`, heredoc variable interpolation breaks in unpredictable ways:
- Variables set with `\$VAR` inside `bash -c` may or may not be available in inner unquoted heredocs
- Postgres init SQL had empty password because `\${OPENWEBUI_DB_PASSWORD}` wasn't expanded in the heredoc chain
- **Better approach**: scp the script file to the server, then execute it there. Avoid nested heredocs through SSH altogether.
- When you MUST use inline heredocs, use Python on the server instead of bash for complex config generation.

### Caddy: `protocol { experimental_http3 }` is dead

Newer Caddy versions reject the old syntax. Use:
```
servers {
    protocols h1 h2 h3
}
```

### Authelia startup: SMTP check kills boot if Resend key is invalid

Authelia v4.39+ performs SMTP startup check. If the Resend API key is bad, Authelia crashes with `535 Authentication credentials invalid`. **Quick fix**: switch to filesystem notifier:
```bash
sed -i '/^notifier:/,/^[a-z]/{ /^notifier:/!{ /^[a-z]/!d }; /^notifier:/c\
notifier:\
  filesystem:\
    filename: /config/notification.txt
}' /opt/ai/v3/authelia/config/configuration.yml
```
TOTP setup codes are then available via `docker exec authelia cat /config/notification.txt`.

### Authelia storage: must pre-create schema in Postgres

Authelia connects to `postgres` database with `schema: authelia` but may fail if the schema doesn't exist. Fix:
```bash
docker exec postgres psql -U postgres -c "CREATE SCHEMA IF NOT EXISTS authelia;"
```

### Caddy doesn't heal when dependency recovers

If `authelia` goes unhealthy (causing Caddy to fail its `depends_on`), and authelia is later fixed, Caddy does NOT auto-start. Docker Compose only evaluates dependencies on initial `up`. Fix: `docker start caddy` after the dependency is healthy.

### Postgres init SQL only runs on first start

Any password/DB changes require wiping the data directory:
```bash
docker compose down && rm -rf postgres/data/* && docker compose up -d
```
Or fix manually with `docker exec postgres psql`.

### OpenWebUI health check takes 60s

The `start_period: 60s` in docker-compose means OpenWebUI shows `(health: starting)` for a full minute. Don't panic — it's normal. Check logs if it exceeds 90s.

## Prospect Infrastructure Reconnaissance

For competitive intelligence or sales prep, run this DNS/web stack recon pipeline against any domain. Produces: hosting provider, email setup, CMS/framework fingerprinting, tech stack detection.

### 1. DNS Enumeration
```bash
nslookup -type=A {domain} && nslookup -type=MX {domain} && nslookup -type=NS {domain} && nslookup -type=TXT {domain} && nslookup -type=CNAME www.{domain}
```
Extract: MX → email provider (Outlook=Microsoft 365, Google=Workspace), NS → DNS host, CNAME → hosting platform (azurestaticapps.net, vercel.app, etc.), TXT → SPF/DKIM/DMARC.

### 2. HTTP Headers
```bash
curl -sI https://www.{domain}/ | grep -i "server\|x-\|powered\|via\|cf-"
```
Extract: hosting platform signatures, security headers (HSTS, CSP), Cloudflare proxy detection.

### 3. Page Source Fingerprinting
```bash
curl -sL https://www.{domain}/ | grep -Ei "(next\.js|react|vercel|netlify|supabase|wordpress|shopify|wix|webflow|tailwind)"
```

### 4. Certificate Transparency
```bash
curl -s "https://crt.sh/?q=%.{domain}&output=json" | head -20
```
Discovers subdomains via SSL certificates.

**Pitfalls:** Cloudflare masks real IP — CNAME chain reveals origin. Privacy-protected WHOIS is normal. Lovable.dev detection: look for `lovable` in page source + rapid iteration markers.

## References

- `references/dns-record-types.md` — DNS record interpretation guide
- `references/hosting-signatures.md` — Known hosting provider CNAME patterns
- `references/self-hosted-tool-evaluation.md` — Methodology for evaluating open-source self-hosted tools before deployment (GitHub health, Docker reqs, feature fit, Hostinger capacity check, agent research pattern)

## Tailscale CLI on macOS (App Store limitation)

Tailscale is installed at `/Applications/Tailscale.app/` (App Store variant). Key differences from the Standalone variant:

- **CLI binary**: `/Applications/Tailscale.app/Contents/MacOS/Tailscale` — NOT on PATH. Use the full path or alias it.
- **No `tailscale ssh` subcommand**: The App Store build does not include `tailscale ssh`. Use regular `ssh` client instead: `ssh user@<tailnet-ip-or-dns>`.
- **Status**: `/Applications/Tailscale.app/Contents/MacOS/Tailscale status` — works.
- **Ping**: `/Applications/Tailscale.app/Contents/MacOS/Tailscale ping 100.x.y.z` — works.
- **Whois**: `/Applications/Tailscale.app/Contents/MacOS/Tailscale whois 100.x.y.z` — works.
- **`--json` flag**: output pipeable to `python3 -c` for machine parsing.
- **Fix**: Download the Standalone variant from `https://pkgs.tailscale.com` to get the full CLI including `tailscale ssh`.

## Tailscale SSH web-approval flow

When a remote machine runs Tailscale SSH, connections are intercepted. SSH keys are NOT used for authentication — Tailscale verifies the connection against its ACL. In the default ACL (no custom rules), the node owner can SSH in but must complete a **one-time web approval**:

1. Attempt SSH with the correct local username (e.g. `ssh amyn@ap-desktop.tail003f9d.ts.net`)
2. Server responds: `Tailscale SSH requires an additional check. To authenticate, visit: https://login.tailscale.com/a/<token>`
3. Open that URL in a browser logged into the Tailscale account
4. Approve the session
5. Subsequent SSH connections work without re-approval

**Username discovery**: Try common usernames. A timeout (30s+) means the user exists but key auth is being tried (or Tailscale SSH is negotiating). An immediate "failed to look up local user" rejection means no local account by that name. For Amyn's AP-Desktop, the local user appears to be **amyn**.

## Pitfalls

### Hermes sandbox cannot reach Hostinger via SSH (Tailscale-only)

Hostinger SSH (port 22) is filtered on the public IP — accessible ONLY via Tailscale. The Hermes agent's sandboxed terminal does NOT have Tailscale networking, so `ssh hostinger` will always fail with "No route to host" or "Could not resolve hostname wala-srv." The web server (port 80/443) IS reachable from the sandbox — Caddy serves public traffic fine.

- **Symptom:** `ssh hostinger` → `Could not resolve hostname wala-srv` or `Operation timed out` on `100.90.143.51`
- **Workaround:** Write a deployment script (`deploy.sh`), commit it to the repo, and tell the user to run it from their local terminal where Tailscale is active.
- **Verify web reachability:** `curl -k -sI https://porbanderwala.cloud/` should return HTTP/2 200 — confirms Caddy is running even when SSH is unreachable.
- **Never spend >2 attempts trying SSH** — if the first try fails and Tailscale DNS doesn't resolve, fall back to the script approach immediately.

### Local Mac CAN reach tailnet machines (Tailscale installed)

Unlike the Hermes sandbox, this Mac has Tailscale (App Store variant) and can SSH into any online tailnet machine. No special config needed — Tailscale networking is active on the system.

- **Ping:** `/Applications/Tailscale.app/Contents/MacOS/Tailscale ping 100.x.y.z` confirms DERP/direct connectivity
- **SSH:** `ssh user@100.x.y.z` — Tailscale SSH may intercept and require web approval on first connection
- **Tailscale API:** `--json` flag on status/whois pipes to `python3 -c` for machine parsing

### AP-Desktop SSH: first connection requires Tailscale web-approval

AP-Desktop (100.68.66.103, `ap-desktop.tail003f9d.ts.net`) runs Tailscale SSH. Initial connection requires the user to approve via a browser URL. After approval, connections work normally.

- **Discovered user:** `amyn` (triggers the approval prompt; other usernames get immediate rejection)
- **Approval URL pattern:** `https://login.tailscale.com/a/<token>` (displayed on first SSH attempt)
- **Post-approval:** works like regular SSH — no further web checks

### Schema drift: repo has migrations the server never got

Drizzle migrations in the repo may not have been run against the production database. Compare `src/lib/db/schema.ts` column count against `SELECT column_name FROM information_schema.columns WHERE table_name='opportunities'` on the server. Missing columns = un-run migrations. Symptom: queries fail with "column does not exist" on columns that clearly exist in the codebase. Fix: run `drizzle-kit push` or the migration command on the server.

### Nextcloud: SCP'd files need ownership fix + occ files:scan

AP-Desktop runs a Docker Nextcloud (v34.0.0) at cloud.h.porb.dev. Simply SCPing a file into `/data/nextcloud/data/amyn/files/<folder>/` puts it on disk but Nextcloud won't see it:

1. **Ownership**: SCP lands as `root:root` — Nextcloud's web server runs as `www-data:www-data`. Fix with `chown www-data:www-data`.
2. **Registration**: Run `docker exec -u www-data nextcloud php occ files:scan --path=amyn/files/<folder>/<file>` to register in the DB.
3. **Verify**: Query `docker exec nextcloud-db psql -U nextcloud -c "SELECT path, size, mimetype FROM oc_filecache WHERE path LIKE '%filename%';"` — check that mimetype resolves correctly (e.g. `12` = `video/mp4` via `oc_mimetypes`).

Full reference: `references/nextcloud-file-upload.md`.

### LinkedIn video downloads

Auth-gated LinkedIn videos can be downloaded with yt-dlp using Chrome's session cookies:
```bash
yt-dlp --cookies-from-browser chrome "https://www.linkedin.com/posts/..."
```
Works because Chrome has an active LinkedIn session. Safari binary cookie format is not compatible with yt-dlp. Combine with Nextcloud upload above to archive LinkedIn content to cloud.h.porb.dev.

### `data/` directory is gitignored — create it before running pipelines

Many sbir-portal pipeline scripts write to `data/` (e.g., `data/dsip_topics.json`). This directory is in `.gitignore` and does NOT exist on a fresh clone. Create it manually: `mkdir -p /opt/stacks/sbir/source/data/`. Scripts will silently fail or write nowhere if it's missing.

### Container name mismatch in pipeline scripts

`load_dsip_data.py` uses `docker exec -i postgres psql` but the Hostinger supabase stack uses `supabase-db` as the container name. Always verify container names with `docker ps | grep postgres` before running any script that does `docker exec` into the database.

The Hostinger VPS Docker daemon has DNS configured (`8.8.8.8`, `1.1.1.1`) but during `docker build`, apt-get inside the container may fail to resolve `deb.debian.org`. Workaround: use `docker build --network=host` (or `DOCKER_BUILDKIT=1 docker build --network=host`). This gives the build container access to the host's network stack, where DNS works correctly. The `docker compose build` command does NOT support `--network=host` — use raw `docker build` instead, then `docker compose up -d`.

### Git push hangs when osxkeychain has no GitHub credentials

`git push origin main` silently hangs (never returns) when the credential helper is `osxkeychain` but no GitHub credentials are stored in the keychain. The push gets a `401 Unauthorized`, then the helper tries to prompt interactively — which blocks forever in a non-interactive terminal. `security find-internet-password -s github.com` returns "item could not be found." SSH key auth may also fail if not configured.

**Fix (one-liner):** Use the `gh` CLI token inline, then restore the clean URL:
```bash
git remote set-url origin "https://aporb:$(gh auth token)@github.com/aporb/usaspending-app.git"
git push origin main
git remote set-url origin https://github.com/aporb/usaspending-app.git
```

**Diagnostic:** `GIT_CURL_VERBOSE=1 git push origin main 2>&1 | head -40` — look for `HTTP/1.1 401 Unauthorized` followed by silence.

### Backend container health check: use docker exec, not host curl

When a backend container is on the Docker `proxy` network but does NOT publish a host port (e.g., `usaspending-backend` exposes `8787/tcp` internally only), `curl http://127.0.0.1:8787/api/health` from the host fails with exit code 7. The container is healthy — `docker ps` shows `(healthy)` — but the port is unreachable from the host.

**Fix:** Health-check via `docker exec`:
```bash
docker exec usaspending-backend wget -qO- http://127.0.0.1:8787/api/health
```
Or use the public URL through Caddy: `curl -sf https://govintel.porbanderwala.cloud/api/health`

### .env keys that look "not set" may just be commented out

`grep` and `hermes status` both detect commented-out lines in `.env` (e.g. `# OPENROUTER_API_KEY=sk-...`). Treat a `✗ (not set)` as "check if commented out" before assuming the key is absent. Fix with `sed -i '' 's/^# KEY_NAME=/KEY_NAME=/'` (macOS) or `sed -i 's/^# KEY_NAME=/KEY_NAME=/'` (Linux) — do NOT echo a duplicate. If the user says "you should have it" and it shows as `✗ (not set)`, check for the commented form first.


