---
name: deepswe-benchmark
description: Run the DeepSWE coding agent benchmark with a custom model via Pier +
  mini-swe-agent. Use when running DeepSWE evaluations against self-hosted or proxy-served
  models.
---

# DeepSWE Benchmark Runner

Run the [DeepSWE](https://deepswe.datacurve.ai) benchmark with a custom model through Pier + mini-swe-agent.

## Prerequisites

- Python ≥3.10 + uv
- Docker (or Modal account for cloud sandboxes)
- LiteLLM proxy or OpenAI-compatible endpoint serving the model
- Virtual API key (NOT master key for LiteLLM)

## Install

```bash
uv tool install datacurve-pier
git clone https://github.com/datacurve-ai/deep-swe.git
```

## Configure

Three critical flags:
1. **`--ae` (agent-env)** — pass auth vars into the Docker sandbox. `--env-file` does NOT propagate.
2. **`--ak model_class=litellm`** — force standard chat completions. Without this, `openai/` prefix triggers Responses API (`/v1/responses`).
3. **`provider/name` model format** — Pier validates `"/" in model_name`. Bare names fail.

## Run

```bash
# Single task smoke test
pier run -p deep-swe/tasks/<TASK_ID> \
  --agent mini-swe-agent \
  --model openai/<model-name> \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=<proxy-url>/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name smoke-test

# Full benchmark
pier run -p deep-swe/tasks \
  --agent mini-swe-agent \
  --model openai/<model-name> \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=<proxy-url>/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name full-run
```

## View Results

```bash
pier job list
pier view
pier analyze jobs/<job-name>
```

## Cost Estimation

Typical per-task: ~5.9M input + ~26K output tokens. At LiteLLM proxy pricing (~$0.306/M input, ~$2.65/M output), expect ~$1.88/task. 113 tasks ≈ $212. Runtime ~7 min/task, ~3.3 hours total with 4 concurrent Docker sandboxes.

## Troubleshooting

- **401 auth error**: `--env-file` doesn't reach the sandbox. Use `--ae OPENAI_API_KEY=...`.
- **"Model name must be in provider/name format"**: Pier requires `/` in model name. Always use `openai/<model>`.
- **Responses API errors**: Without `--ak model_class=litellm`, the `openai/` prefix triggers `litellm.responses()` which calls `/v1/responses`. Most proxies only serve `/v1/chat/completions`.
- **Virtual key lost**: LiteLLM Docker container recreation clears the VerificationTokenTable. Re-generate keys at `/ui`.
