---
name: pier-custom-model
description: Configure Pier to run DeepSWE/Harbor benchmarks with a custom model via
  LiteLLM proxy or any OpenAI-compatible endpoint. Use when setting up a new model
  for Pier-based benchmarks.
---

# Pier Custom Model Configuration

How to run Pier (DeepSWE / Harbor benchmarks) with a model served through a custom endpoint (LiteLLM proxy, vLLM, OpenRouter, etc.).

## Prerequisites

- Pier installed: `uv tool install datacurve-pier`
- DeepSWE tasks: `git clone https://github.com/datacurve-ai/deep-swe`
- Docker (or Modal for cloud runs)
- API key for the model endpoint

## The Three Constraints

Pier's mini-swe-agent integration has three interacting constraints:

1. **Model name MUST contain `/`** — `mini_swe_agent.py:832` raises ValueError otherwise
2. **`openai/` prefix auto-detects `litellm_response`** — which calls `litellm.responses()` → `/v1/responses`, NOT `/v1/chat/completions`
3. **Custom endpoints (LiteLLM proxy, vLLM) typically only serve `/v1/chat/completions`**

## The Fix: `model_class` Kwarg Override

Use `openai/` prefix to satisfy the `/` validation, but override the auto-detected model class:

```bash
pier run -p deep-swe/tasks \
  --agent mini-swe-agent \
  --model openai/your-model-name \
  --env-file .env \
  --agent-config '{"kwargs":{"model_class":"litellm"}}'
```

This forces `LitellmModel` (standard `litellm.completion()` → `/v1/chat/completions`) instead of `LitellmResponseModel`.

## Environment Variables (.env)

```
OPENAI_API_KEY=sk-your-key
MSWEA_API_KEY=sk-your-key        # fallback for unknown model names
OPENAI_BASE_URL=https://your-proxy/v1
MSWEA_COST_TRACKING=ignore_errors  # if model not in LiteLLM's pricing DB
```

Both `OPENAI_API_KEY` and `MSWEA_API_KEY` are needed: `MSWEA_API_KEY` is the fallback when Pier's `get_api_key_var_names_from_model_name()` can't resolve a custom model name.

## agents.yaml (Alternative)

```yaml
agents:
  - name: mini-swe-agent
    model_name: openai/your-model-name
    env:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      OPENAI_BASE_URL: ${OPENAI_BASE_URL}
    kwargs:
      model_class: litellm
      cost_limit: 0
```

## Auth Gotchas

- **LiteLLM master keys do NOT work** as Bearer tokens for `/v1/chat/completions`. Generate a virtual key at `/ui` → API Keys.
- **Container recreation clears the token DB.** After `docker restart` on the LiteLLM container, re-generate virtual keys.
- OpenRouter: use `openrouter/` prefix (no override needed, `openrouter` model class is correct).
- Anthropic: use `anthropic/` prefix with `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`.

## References

- Pier mini_swe_agent.py: `https://github.com/datacurve-ai/pier/blob/main/src/pier/agents/installed/mini_swe_agent.py`
- mini-swe-agent litellm_response_model.py: `https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_response_model.py` (L38: `litellm.responses()`)
- mini-swe-agent litellm_model.py: `https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py` (uses `litellm.completion()`)
