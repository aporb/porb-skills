---
name: deepswe-benchmark
description: Run the DeepSWE coding agent benchmark with a custom model via Pier + mini-swe-agent. Use when running DeepSWE evaluations against self-hosted or proxy-served models.
---

# DeepSWE Benchmark Runner

Run the [DeepSWE](https://deepswe.datacurve.ai) benchmark (113 coding tasks) with a custom model through Pier + mini-swe-agent.

## Prerequisites

- Python ≥3.10 + uv
- Docker (or Modal account for cloud sandboxes)
- LiteLLM proxy or OpenAI-compatible endpoint serving the model
- Virtual API key (NOT master key for LiteLLM — master keys return 401)

## Install

```bash
uv tool install datacurve-pier
git clone https://github.com/datacurve-ai/deep-swe.git
```

## Why `model_class=litellm` Is Required

Three constraints interact:

1. Pier requires model name contain `/` (e.g. `openai/model-name`)
2. The `openai/` prefix auto-detects `litellm_response` adapter → `litellm.responses()` → `/v1/responses`
3. Standard LiteLLM proxies only serve `/v1/chat/completions`, not Responses

`--ak model_class=litellm` overrides the auto-detection → `litellm.completion()` → `/v1/chat/completions`.

## CLI Flags

| Flag | Purpose | Required? |
|------|---------|-----------|
| `--agent mini-swe-agent` | Agent type | Yes |
| `--model openai/<name>` | Model (must contain `/`) | Yes |
| `--ae OPENAI_API_KEY=...` | API key into Docker sandbox | **Required** — `--env-file` doesn't propagate |
| `--ae OPENAI_BASE_URL=...` | Routes calls to custom proxy | **Required** |
| `--ae MSWEA_COST_TRACKING=ignore_errors` | Suppresses unknown model cost warnings | **Required** for custom models |
| `--ak model_class=litellm` | Force standard chat completions | **Required** |
| `--job-name <name>` | Output directory name | Yes |
| `--n-tasks N --sample-seed S` | Deterministic subset | Optional |
| `--agent-config '{"kwargs":{"model_class":"litellm"}}'` | Alternative to `--ak` for JSON config | Optional — use instead of `--ak` |

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

# Deterministic 10-task subset
pier run -p deep-swe/tasks --n-tasks 10 --sample-seed 0 \
  --agent mini-swe-agent \
  --model openai/<model-name> \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=<proxy-url>/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name subset-run

# Full benchmark (113 tasks)
pier run -p deep-swe/tasks \
  --agent mini-swe-agent \
  --model openai/<model-name> \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=<proxy-url>/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name full-run
```

## Verification

```bash
# Test proxy endpoint
curl https://litellm.h.porb.dev/v1/models -H "Authorization: Bearer <key>"

# Test a completion
curl https://litellm.h.porb.dev/v1/chat/completions \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-27b-nvfp4","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

## View Results

```bash
pier job list
pier view
pier analyze jobs/<job-name>
```

## Retry Failures

After first pass, identify failed tasks and retry individually:

```bash
# Find tasks missing completion marker
for d in jobs/<job-name>/*/; do
  name=$(basename "$d")
  task="${name%%__*}"
  # Check for COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT marker in trajectory
done

# Retry individually
pier run -p deep-swe/tasks/$task --job-name retry-pass \
  --agent mini-swe-agent \
  --model openai/<model-name> \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=<proxy-url>/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm
```

## Cost Estimation

Typical per-task: ~5.9M input + ~26K output tokens. At LiteLLM proxy pricing (~$0.306/M input, ~$2.65/M output), expect ~$1.88/task. 113 tasks ≈ $212. Runtime ~7 min/task, ~3.3 hours total with 4 concurrent Docker sandboxes.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| **401 token_not_found_in_db** | Using master key | Generate virtual key at proxy `/ui` |
| **InternalServerError: Missing credentials** | `--ae` flags not set or not propagating | Use `--ae`, not `--env-file` |
| **ValueError: Model name must be in format provider/model_name** | Bare model name | Add `openai/` prefix |
| **NonZeroAgentExitCodeError** | Agent failed to complete | Check trajectory for failure mode; retry |
| **Responses API errors** | `openai/` prefix triggers `/v1/responses` | Ensure `--ak model_class=litellm` is set |
| **Virtual key lost after restart** | LiteLLM container recreation clears token DB | Re-generate keys at `/ui` |

## agents.yaml (Alternative to CLI flags)

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

## Non-LiteLLM Providers

**OpenRouter:** Use `openrouter/` prefix — no `model_class` override needed. The `openrouter` model class is correct.

**Anthropic:** Use `anthropic/` prefix with `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`.

## Source References

- Pier mini_swe_agent.py: https://github.com/datacurve-ai/pier/blob/main/src/pier/agents/installed/mini_swe_agent.py
- mini-swe-agent litellm_response_model.py: https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_response_model.py
- mini-swe-agent litellm_model.py: https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py
