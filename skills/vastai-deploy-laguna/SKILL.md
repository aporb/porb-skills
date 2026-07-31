---
name: vastai-deploy-laguna
description: Deploy poolside/Laguna-S-2.1-NVFP4 on Vast.ai with vLLM, Tailscale, and
  LiteLLM routing. Covers both 4× RTX 5090 (TP-4) and 8× RTX 5060 Ti (TP-8) paths.
---

# Vast.ai Laguna S-2.1 Deployment

Deploy `poolside/Laguna-S-2.1-NVFP4` on Vast.ai with vLLM + Tailscale + LiteLLM routing through `ap-desktop`.

## Prerequisites

- Vast.ai API key in `~/.config/vastai/vast_api_key` or `~/.env.local`
- `HF_TOKEN` and `VLLM_API_KEY` in `.env.local`
- Tailscale auth key (7-day reusable, tagged)
- Working SSH key at `~/.ssh/id_vast_ai_ed25519`

## Image Selection

- **4× RTX 5090**: `vastai/base-image:cuda-12.8.1-cudnn-devel-ubuntu24.04` or `nvidia/cuda:13.0.1-devel-ubuntu24.04`
- **8× RTX 5060 Ti**: **MUST use CUDA 13.0+** — `vastai/base-image:cuda-13.0.3-auto`. CUDA 12.8 fails with "No supported CUDA architectures" on 5060 Ti despite SM 120.

## Bootstrap Adjustments by GPU

### 4× RTX 5090 (current active deployment)
- `--tensor-parallel-size 4` (in bootstrap-laguna.sh)
- `--max-model-len 262144`
- `--enforce-eager`
- `--max-num-seqs 8`
- `--gpu-memory-utilization 0.85`
- DFlash with 5 spec decode tokens (32 GB VRAM)
- Only confirmed working host: Vast.ai host 410852
### 8× RTX 5060 Ti
- `--tensor-parallel-size 8` (patch: `sed -i 's/--tensor-parallel-size 4/--tensor-parallel-size 8/'`)
- `--gpu-memory-utilization 0.70` (16 GB VRAM — DFlash causes OOM)
- **Remove DFlash** — don't pass `--speculative-config`
- Reduce `--max-model-len` to 131072
- Model fits: ~9 GB/GPU weights, ~7 GB/GPU KV cache at 0.70 util
- First-start AutoTuner warmup: 5-10 min

## Common Gotchas

### PyPI CDN Dead
Many Vast hosts have `files.pythonhosted.org` unreachable (0 B/s). Bootstrap-laguna.sh has a fatal check that exits. **Patch it**:
```bash
sed -i 's/if \[ "$PYPI_FILES" -eq 0 \]; then/if false; then/' bootstrap-laguna.sh
```
If `pypi.org/simple/` works (metadata resolution), pip can install — the CDN is for file downloads but pip uses mirrors. If it stalls, use Tsinghua mirror:
```bash
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Network Test First
Always test PyPI + HF speed BEFORE running bootstrap. Destroy immediately if:
- PyPI simple < 100 KB/s
- HF < 50 KB/s (71 GB model takes too long)

### Env Var Passing
Don't try nested quoting through SSH — use wrapper script:
```bash
# Write env file on instance
cat > /tmp/bootstrap-env << 'ENVEOF'
HF_TOKEN=<token>
VLLM_API_KEY=<key>
ENVEOF

# Write wrapper
cat > /tmp/run-bootstrap.sh << 'WRAPEOF'
source /tmp/bootstrap-env
export HF_TOKEN VLLM_API_KEY
bash /tmp/bootstrap-laguna.sh
WRAPEOF

# Launch detached
nohup /tmp/run-bootstrap.sh > /tmp/bootstrap-run.log 2>&1 &
```

### Tailscale
Install after bootstrap completes:
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --auth-key=<key> --hostname=laguna-s2
```
Use `--hostname=laguna-s2` consistently (also update `vastai-on-start.sh` line 28).

### On-Start Script Registration
Vast CLI requires `--image` with `--onstart`:
```bash
vastai update instance <ID> --image vastai/base-image:cuda-13.0.3-auto \
  --onstart "$(base64 -i vastai-on-start.sh)"
```

### LiteLLM Container Recreate
When `docker compose down/up` LiteLLM, the token DB is cleared. Re-register client key:
```bash
docker exec litellm curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer <MASTER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"key":"<CLIENT_KEY>","models":["laguna-s-2.1"],"max_budget":100}'
```
Master key is in container env as `LITELLM_MASTER_KEY`.

### Caddy HTTP→HTTPS Redirect
If `litellm.h.porb.dev` 308-redirects HTTP to a non-existent HTTPS, add `tls internal`:
```
litellm.h.porb.dev {
    tls internal
    reverse_proxy litellm:4000
}
```
Then `caddy reload`.

## Verification

```bash
# Direct vLLM health (from instance)
curl http://localhost:8000/health

# Full chain
curl -sk https://litellm.h.porb.dev/v1/chat/completions \
  -H "Authorization: Bearer <CLIENT_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"model":"laguna-s-2.1","messages":[{"role":"user","content":"Hi"}],"max_tokens":5}'
```
