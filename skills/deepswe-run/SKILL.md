---
name: deepswe-run
description: "Run DeepSWE benchmark with custom models via Pier + mini-swe-agent on a LiteLLM proxy. Use when asked to run or configure DeepSWE, or set up Pier for custom models."
---

# DeepSWE Run Skill

## Quick Command

```bash
pier run -p deep-swe/tasks \
  --agent mini-swe-agent \
  --model openai/qwen3.6-27b-nvfp4 \
  --ae OPENAI_API_KEY=<key> \
  --ae OPENAI_BASE_URL=https://litellm.h.porb.dev/v1 \
  --ae MSWEA_COST_TRACKING=ignore_errors \
  --ak model_class=litellm \
  --job-name <name>
```

## Critical Gotchas

1. **Model name must contain `/`** — Pier validates this at runtime. Bare model names fail.
2. **`--ak model_class=litellm` is REQUIRED** — without it, `openai/` prefix auto-detects `litellm_response` which calls `/v1/responses` not `/v1/chat/completions`.
3. **Use `--ae`, NOT `--env-file`** — `--env-file` loads into the Pier process but does NOT propagate into Docker sandboxes where mini-swe-agent runs.
4. **Master keys don't work** — LiteLLM master keys aren't in `VerificationTokenTable`. Generate virtual keys at `/ui`.

## Prerequisites

- `uv tool install datacurve-pier`
- `git clone https://github.com/datacurve-ai/deep-swe`
- Docker Desktop running
- Valid LiteLLM virtual key (not master key)

## CLI Flags

| Flag | Purpose |
|------|---------|
| `--agent mini-swe-agent` | Agent type |
| `--model openai/<name>` | Model (must have `/`) |
| `--ak model_class=litellm` | Force standard completions |
| `--ae KEY=VALUE` | Pass env vars into sandbox |
| `--job-name <name>` | Output directory name |
| `--n-tasks N --sample-seed S` | Deterministic subset |
| `--env modal` | Cloud parallel (not docker) |

## Verification

```bash
# Test endpoint
curl https://litellm.h.porb.dev/v1/models -H "Authorization: Bearer <key>"

# Test completion
curl https://litellm.h.porb.dev/v1/chat/completions \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-27b-nvfp4","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

## Cost Estimation

Realistic per-task: ~6M input tokens (~$1.81) + ~26K output tokens (~$0.07) = ~$1.88/task. For 113 tasks: ~$212. Tasks take 7-40 min each depending on complexity.

## Retry Pass

After first pass, identify failed tasks (no COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT marker) and retry with same command on individual failed task paths.
