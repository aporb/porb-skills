---
name: secrets-before-first-push
description: Move secrets to .env.local and redact from committed files before initial
  git push
---

## When to use
Before the first `git push` on any project containing API keys, tokens, or credentials in config files, shell scripts, or documentation.

## Steps

1. **Identify all secrets**: grep for key patterns (`sk-`, `hf_`, long hex strings) across `*.sh`, `*.yaml`, `*.yml`, `*.html`, `*.md`.
2. **Create `.env.local`**: List every secret with its env var name as the key.
3. **Create `.env.example`**: Same structure but with empty values — serves as the template for collaborators.
4. **Update `.gitignore`**: Add `.env.local` plus runtime files (`*.log`, `*.pid`, `__pycache__/`, `.DS_Store`).
5. **Update config files**: Use language-appropriate env var syntax:
   - **LiteLLM config**: `api_key: os.environ/VAR_NAME` (NOT `${VAR}`)
   - **Shell scripts**: `source .env.local` with `set -a` for auto-export
6. **Update shell scripts**: Remove hardcoded defaults; source `.env.local` at the top.
7. **Redact docs/HTML**: Replace all secret values with `${VAR_NAME}` placeholders using `sed -i`.
8. **Verify**: Restart the service, confirm health check and end-to-end call still work.
9. **Pre-commit check**: `git status` to confirm `.env.local` is excluded; `grep` to confirm no secrets remain.

## Key gotcha
LiteLLM's YAML config does NOT support shell-style `${VAR}` — it requires `os.environ/VAR_NAME`. Using `${VAR}` will send the literal string as the key and fail auth silently.
