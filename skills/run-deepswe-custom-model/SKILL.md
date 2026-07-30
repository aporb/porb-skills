---
name: run-deepswe-custom-model
description: Run the DeepSWE benchmark with a custom model behind a LiteLLM proxy using Pier + mini-swe-agent. Use when the user wants to benchmark a self-hosted model on DeepSWE.
---

# Run DeepSWE with a Custom LiteLLM Model

Run DeepSWE (113 coding tasks) with mini-swe-agent behind a custom LiteLLM proxy.

## Prerequisites
- Docker running
- DeepSWE tasks cloned: `git clone https://github.com/datacurve-ai/deep-swe`
- Pier installed: `uv tool install datacurve-pier`
- A LiteLLM virtual key (NOT master key — master keys return 401)

## The Working Command

```bash
pier run -p deep-swe/tasks \
  --agent mini-swe-agent \
  --model openai/YOUR-MODEL-NAME \
  --ae OPENAI_API_KEY=sk-your-virtual-key \
  --ae OPENAI_BASE_URL=https://your-proxy/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name deepswe-run
```

## Critical Flags

| Flag | Purpose | Required? |
|---|---|---|
| `--ae OPENAI_API_KEY=...` | Passes API key into Docker sandbox | **Required** — `--env-file` doesn't propagate to sandbox |
| `--ae OPENAI_BASE_URL=...` | Routes calls to custom proxy | **Required** |
| `--ae MSWEA_COST_TRACKING=ignore_errors` | Suppresses unknown model cost warnings | **Required** for custom models |
| `--ak model_class=litellm` | Forces standard chat completions (not Responses API) | **Required** — openai/ prefix auto-detects `litellm_response` |
| `--ak` / `--agent-kwarg` | Passes kwargs to Pier's agent constructor | Use for any agent-specific config |

## Why model_class=litellm Is Needed

1. Pier requires model name contain `/` (e.g. `openai/model-name`)
2. The `openai/` prefix triggers `litellm_response` adapter → `litellm.responses()` → `/v1/responses`
3. Standard LiteLLM proxies only serve `/v1/chat/completions`, not Responses
4. `--ak model_class=litellm` overrides the auto-detection → `litellm.completion()` → `/v1/chat/completions`

## Subset / Single Task

```bash
# Deterministic 10-task subset
pier run -p deep-swe/tasks --n-tasks 10 --sample-seed 0 ...

# Single task smoke test
pier run -p deep-swe/tasks/<task-id> ...
```

## Retry Failures

After first pass, check which tasks failed and retry:
```bash
# Identify failed tasks (those missing COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT)
for d in jobs/<job-name>/*/; do
  name=$(basename "$d")
  task="${name%%__*}"
  # Check for completion marker in trajectory
  ...
done

# Retry individually
pier run -p deep-swe/tasks/$task --job-name retry-pass ...
```

## Expected Costs

~$1.88 per task (5.9M input + 26K output tokens). 113 tasks ≈ $212. Each task takes ~7 minutes with thinking ON.

## Common Errors

- **401 token_not_found_in_db**: Using master key. Generate virtual key at proxy /ui.
- **InternalServerError: Missing credentials**: `--ae` flags not set or not propagating. `--env-file` is insufficient.
- **NonZeroAgentExitCodeError**: Agent failed to complete. Check trajectory for failure mode.
- **ValueError: Model name must be in format provider/model_name**: Bare model name used. Add `openai/` prefix.
