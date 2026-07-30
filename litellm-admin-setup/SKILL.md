---
name: litellm-admin-setup
description: Set up or fix LiteLLM proxy admin access — env var propagation, model
  registration, virtual key management, pi/omp config wiring
---

# LiteLLM Admin Setup

## Common Issues & Fixes

### 1. Master key resolves as internal_user (not proxy_admin)

**Root cause**: `LITELLM_MASTER_KEY` set in `.env.local` but not reaching the process.

The pattern `export $(grep ... | xargs); nohup .litellm-venv/bin/litellm ...` does NOT propagate env vars to the nohup'd process.

**Fix**: Write a launch wrapper that sources vars then execs:

```bash
#!/usr/bin/env bash
# LiteLLM proxy launcher — sources secrets before starting
set -euo pipefail
cd /path/to/project
export $(grep "^LITELLM_MASTER_KEY=" .env.local | xargs)
export STORE_MODEL_IN_DB=True
exec .litellm-venv/bin/litellm --config litellm-config.yaml --port 4000 --host 0.0.0.0
```

Do NOT use `source .env.local` — that file may contain SSH keys and non-assignment lines that break shell execution.

**Verification**: `curl http://localhost:4000/user/info -H "Authorization: Bearer <master-key>"` returns without 401.

### 2. Model not showing in UI

`/v1/models` shows models from config YAML immediately. But the admin UI requires DB registration:

```bash
# Check if registered
curl http://localhost:4000/model/list -H "Authorization: Bearer <master-key>"

# Register
curl -s -X POST http://localhost:4000/model/new \
  -H "Authorization: Bearer <master-key>" \
  -H "Content-Type: application/json" \
  -d '{"model_name": "name", "litellm_params": {...}, "model_info": {...}}'
```

Requires `STORE_MODEL_IN_DB=True` in the process environment. If registration returns `Set 'STORE_MODEL_IN_DB=True' in your env`, add it to the wrapper and restart.

### 3. Virtual key management

```bash
# Create
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer <master-key>" \
  -H "Content-Type: application/json" \
  -d '{"key_alias": "name", "max_budget": 10}'

# Update (e.g. remove budget)
curl -X POST http://localhost:4000/key/update \
  -H "Authorization: Bearer <master-key>" \
  -H "Content-Type: application/json" \
  -d '{"key": "sk-...", "max_budget": null}'

# Get info
curl -X POST http://localhost:4000/key/info \
  -H "Authorization: Bearer <master-key>" \
  -H "Content-Type: application/json" \
  -d '{"key": "sk-..."}'
```

**Gotcha**: `/key/update` may clear unmentioned fields (e.g. `key_alias`) when updating `max_budget`. Re-set alias after budget changes.

### 4. Wiring pi/omp configs

After creating a virtual key, update:
- `~/.pi/agent/models.json` — `apiKey` field under `providers.litellm`
- `~/.omp/agent/models.yml` — `apiKey` field under `providers.litellm`
- `.env.local` — add `LITELLM_CLIENT_KEY=<key>` for scripts that reference it

Both configs should point to `http://localhost:4000/v1` (the local LiteLLM proxy, not the remote Tailscale IP directly).
