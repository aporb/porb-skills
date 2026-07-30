---
name: vllm-sequential-test
description: Sequential vLLM model testing on 4× RTX 5090 with primary server stopping/restart
---

## When to Use This Skill

Testing additional NVFP4 models on an existing 4× RTX 5090 vLLM instance where the primary model uses TP-4 at `--gpu-memory-utilization 0.85` (leaving only ~4.8 GB free per GPU — insufficient for 18-22 GB additional models).

## Key Constraint

**Never run additional vLLM servers simultaneously with the primary.** TP-4 primary uses all 4 GPUs. Co-location causes OOM.

## Sequential Testing Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# Stop primary
if tmux has-session -t vllm 2>/dev/null; then
    tmux kill-session -t vllm
fi
sleep 2

# Start additional model on dedicated GPU
# Primary is stopped, so 0.90 utilization is safe
CUDA_VISIBLE_DEVICES=0 CUTE_DSL_ARCH=sm_121a \
vllm serve <MODEL_ID> \
    --host 0.0.0.0 --port 8001 \
    --api-key "$API_KEY" \
    --tensor-parallel-size 1 \
    --max-model-len 262144 \
    --max-num-seqs 32 \
    --gpu-memory-utilization 0.90 \
    > /tmp/vllm-test.log 2>&1 &

# Test, then kill, then restart primary
```

## Model-Specific Flags

| Model | MoE? | moe-backend flag | CUTE_DSL_ARCH |
|-------|------|-----------------|---------------|
| Qwen3.6-35B-A3B | YES | `flashinfer_b12x` | `sm_121a` |
| Qwen3.6-27B | NO (dense) | omit | `sm_121a` |
| Laguna XS 2.1 | N/A | omit | omit |

## Common Pitfall: tmux Quoting

```bash
# BROKEN — inner " terminates the outer double-quoted string
tmux new -d -s vllm "
echo "inner quote breaks this"
"

# FIX — move inner code outside tmux string
echo "inner stuff"
tmux new -d -s vllm "
vllm serve ...
"
```

## DFlash Flag (briefing-tested)

```bash
--speculative-config '{"model":"poolside/Laguna-S-2.1-DFlash-NVFP4","num_speculative_tokens":5,"method":"dflash"}'
```

Keep `num_speculative_tokens=5` (briefing) — not 7 (model card — would require re-measuring JIT time).
