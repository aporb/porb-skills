---
name: deploy-qwen36-2x3090
description: Deploy Qwen3.6-35B-A3B-AWQ on 2× RTX 3090 via Vast.ai + vLLM + Tailscale
  with MTP speculative decoding
---

# Deploy Qwen3.6-35B-A3B-AWQ on 2× RTX 3090

## Hardware Requirements
- 2× RTX 3090 (24 GB each, 48 GB total), Ampere SM 8.6
- 50+ GB disk (AWQ model is ~24 GB; torch compile cache adds ~4 GB)
- Vast.ai image: `vastai/vllm:v0.25.1-cuda-13.0` (or newer)

## Model
- **AWQ INT4**: `QuantTrio/Qwen3.6-35B-A3B-AWQ` (~24 GB download)
  - Pipeline: image-text-to-text (vision encoder included)
  - vLLM compatible, no extra flags beyond standard
- **NVFP4** (alternative): `nvidia/Qwen3.6-35B-A3B-NVFP4` (~23.5 GB)
  - Requires `--quantization modelopt` flag
  - Pipeline tag is `text-generation` (may lack vision encoder)
  
## vLLM Launch Command

```bash
# Disable supervisor auto-start FIRST
mv /opt/supervisor-scripts/vllm.sh /opt/supervisor-scripts/vllm.sh.bak

vllm serve /models/qwen3.6-35b-a3b-awq \
    --served-model-name qwen3.6-35b-a3b \
    --tensor-parallel-size 2 \
    --max-model-len 262144 \
    --max-num-seqs 2 \
    --gpu-memory-utilization 0.80 \
    --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":1}' \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser qwen3 \
    --host 0.0.0.0 \
    --port 8001
```

**Critical**: Write this as a script on the instance (`/opt/vllm-launch.sh`) and execute it. NEVER inline via SSH nohup with multi-line backslash continuations — shell escaping drops flags silently.

## VRAM Budget (per GPU, 24 GB)
- AWQ weights: ~12 GB
- KV cache (256K × 2 seqs, TP-2): ~5 GB
- MTP overhead: ~1 GB
- Runtime + vision: ~2 GB
- **Total: ~18-19 GB** — fits with ~5 GB headroom

## Tailscale in Container
```bash
/usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state \
    --socket=/var/run/tailscale/tailscaled.sock \
    --tun=userspace-networking &
sleep 3
tailscale up --auth-key=tskey-auth-...
```
- `--tun=userspace-networking` required (no TUN device in container)
- Cannot bind vLLM to Tailscale IP — use `--host 0.0.0.0` (Vast.ai blocks public)

## Speculative Decoding
- **MTP** (Multi-Token Prediction): native to Qwen3.6, trained with multi-steps
- Method name: `qwen3_next_mtp` (deprecated but works in v0.25.1) or `mtp` (new)
- k=1: proven +27.5% throughput on 2×3090
- k=2: may work but untested at 256K
- Shares target embeddings and lm_head — no extra VRAM for draft model

## Gotchas
1. Vast.ai image auto-starts vLLM via supervisor → disable before custom launch
2. Caddy on port 8000 reverse-proxies to vLLM on 28265 — use different port
3. `--max-num-seqs` flag easily dropped by shell escaping → use script
4. Qwen3.6 thinks by default; disable with `chat_template_kwargs: {enable_thinking: false}`
5. torch.compile cache at `/workspace/.vllm_cache` can grow to ~4 GB — clean periodically
6. Use `fuser -k PORT/tcp` to kill processes on a port safely (avoid pkill pattern match on SSH)}
