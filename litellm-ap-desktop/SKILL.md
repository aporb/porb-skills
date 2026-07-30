---
name: litellm-ap-desktop
description: Manage LiteLLM proxy on ap-desktop — Docker container, config paths,
  model entry patterns, restart procedure
---

# LiteLLM Proxy on ap-desktop

## Architecture
The LiteLLM proxy runs as a Docker container on ap-desktop and is exposed at `https://litellm.h.porb.dev`.

## Container
- Image: `ghcr.io/berriai/litellm:main-stable`
- Config mount: `/home/amyn/repos/porb-server-2026/compose/litellm/config.yaml` → `/app/config.yaml`
- Data mount: `/data/litellm` → `/app/data`
- `store_model_in_db: true` — models persist in PostgreSQL
- Restart: `docker restart <container_id>` (find with `docker ps | grep litellm`)

## Config Location
The authoritative config is at `/home/amyn/repos/porb-server-2026/compose/litellm/config.yaml`.
The poolside_ai repo at `/home/amyn/repos/poolside_ai/litellm-config.yaml` is a LOCAL COPY — changing it does NOT affect the running proxy.

## Env Vars
`.env.local` is at `/home/amyn/.env.local` (NOT in the project directory).
Key vars: `LITELLM_MASTER_KEY`, `VLLM_API_KEY`, `DEEPSEEK_API_KEY`.

## Editing Models
1. Edit `/home/amyn/repos/porb-server-2026/compose/litellm/config.yaml`
2. `docker restart <container_id>`
3. Models appear immediately (DB-backed)

## Model Entry Template (Self-Hosted Backend)
```yaml
  - model_name: <name>
    litellm_params:
      model: openai/<name>
      drop_params: false
      api_base: http://<tailscale-ip>:<port>/v1
      api_key: os.environ/VLLM_API_KEY
    model_info:
      mode: chat
      max_input_tokens: <ctx>
      max_tokens: <output>
      supports_function_calling: true|false
      supports_vision: true|false
      supports_reasoning: true|false
```

## Model Entry Template (External API e.g. DeepSeek)
```yaml
  - model_name: <name>
    litellm_params:
      model: <provider>/<model>
      api_key: os.environ/<API_KEY_ENV>
    model_info:
      mode: chat
      max_input_tokens: <ctx>
      max_tokens: <output>
      input_cost_per_token: <cost>
      output_cost_per_token: <cost>
      supports_function_calling: true|false
      supports_reasoning: true|false
      supports_vision: true|false
```

## Fast Variant (Thinking Disabled)
Add `extra_body` with model-specific thinking disable: `enable_thinking: false` (NInfer/Qwen) or `thinking: {type: "disabled"}` (DeepSeek).
