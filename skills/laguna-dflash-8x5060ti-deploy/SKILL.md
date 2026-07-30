---
name: laguna-dflash-8x5060ti-deploy
description: Deploy Laguna S 2.1 with DFlash speculative decoding on 8× RTX 5060 Ti
  (16 GB each) via vLLM 0.26.0. Covers working config, OOM boundaries, quoting patterns,
  and verification.
---

# Laguna S 2.1 + DFlash on 8× RTX 5060 Ti

## Verified Working Config (2026-07-29)

```bash
vllm serve poolside/Laguna-S-2.1-NVFP4 \
    --host 0.0.0.0 --port 8000 \
    --api-key '$API_KEY' \
    --tensor-parallel-size 8 \
    --max-model-len 131072 \
    --max-num-seqs 4 \
    --gpu-memory-utilization 0.70 \
    --enforce-eager \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --served-model-name laguna-s-2.1 \
    --speculative-config '{"model":"/models/Laguna-S-2.1-DFlash-NVFP4","num_speculative_tokens":15,"method":"dflash"}'
```

## Hardware Requirements
- 8× RTX 5060 Ti (16 GB each) with CUDA 13.0+
- vLLM 0.26.0+ (bootstrap installs `vllm>=0.25.0`)
- PyPI + HF network ≥100 KB/s (verify before deploying)

## OOM Boundaries
- **128K context**: Works at 0.70 GPU mem util (~13.9 GiB/GPU post-inference)
- **256K context**: OOM — attention workspace warmup exceeds 16 GB. NVFP4 model fits but prefill workspace is the bottleneck.
- **DFlash draft model**: ~280 MB/GPU at TP-8 (2.1 GB total)
- **Boot time**: ~140s cold start with DFlash, ~5 min if AutoTuner runs

## Flags NOT to use
- `--moe-backend triton`: Not supported in vLLM 0.26.0. Auto-selects FLASHINFER_CUTLASS.
- `--trust-remote-code`: Unnecessary — architecture auto-detected.
- `--override-generation-config`: JSON double-quotes inside tmux double-quoted string break bash quoting.
- `--quantization nvfp4`: Not needed — NVFP4 auto-detected from model config.

## DFLASH_FLAG Quoting (for tmux scripts)

The only pattern that works for passing `--speculative-config` inside a tmux double-quoted string:

```bash
# Build OUTSIDE the tmux string:
DFLASH_FLAG=""
if [ -f /models/Laguna-S-2.1-DFlash-NVFP4/model.safetensors ]; then
    DFLASH_FLAG="--speculative-config '{\"model\":\"/models/Laguna-S-2.1-DFlash-NVFP4\",\"num_speculative_tokens\":15,\"method\":\"dflash\"}'"
fi

# Use INSIDE the tmux double-quoted string:
tmux new -d -s vllm "
...
    $DFLASH_FLAG \\
...
"
```

This works via double-evaluation: outer bash expands `$DFLASH_FLAG` to literal text with single quotes; inner tmux shell re-parses single quotes as active syntax.

Alternative (simpler): write the vLLM command to a disk script with a heredoc, then have tmux run that script. Avoids all quoting issues.

## Verification

```bash
# Health check
curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health

# DFlash active?
grep -c 'DFlashLaguna\\|auxiliary layers' /tmp/vllm.log
# 8+ workers with auxiliary layers = DFlash active

# Inference test
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer $API_KEY' \
  -d '{"model":"laguna-s-2.1","messages":[{"role":"user","content":"Hi"}],"max_tokens":5}'

# GPU memory
nvidia-smi --query-gpu=index,memory.used --format=csv,noheader
# Expected: ~15.6 GiB at load, ~13.9 GiB post-inference
```
