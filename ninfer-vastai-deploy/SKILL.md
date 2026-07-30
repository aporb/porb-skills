---
name: ninfer-vastai-deploy
description: Deploy NInfer Qwen3.6-27B-NVFP4 on Vast.ai 1x RTX 5090 with Tailscale
  + LiteLLM proxy
---

# NInfer Deployment on Vast.ai

## Quick Reference

NInfer is a from-scratch C++/CUDA inference engine — NOT vLLM. It uses `.ninfer` artifact files, requires source build, and runs on a single RTX 5090.

### Prerequisites
- Ubuntu 24.04 (NOT 22.04 — FFmpeg versions too old)
- CUDA toolkit matching host driver version (check `nvidia-smi` first)
- cmake ≥ 3.28, Ninja, FFmpeg ≥ 7.x (libavformat ≥ 60)
- Tailscale userspace networking for Vast.ai

### CUDA Version Matching (Critical)
The Docker image CUDA version MUST match the host driver:
- Host driver 580.119.02 → use `nvidia/cuda:13.0.1-devel-ubuntu24.04`
- Host driver 580.95.05 → may support CUDA 13.1 forward compat
- Always check: `nvidia-smi --query-gpu=driver_version --format=csv,noheader`
- CMakeLists.txt line 37-41 enforces `VERSION_LESS 13.1` — patch to match installed toolkit

### Vast.ai Host Selection
- Test network BEFORE provisioning: HF ≥ 100 KB/s minimum, prefer ≥ 1 MB/s
- Host 366851 (California) had 15-19 Gbps — excellent
- Host 155385 had 72 KB/s — non-viable
- Check: `curl -s -o /dev/null -w '%{speed_download}' --max-time 15 https://huggingface.co`

### Bootstrap Pattern
Write a single comprehensive bootstrap script, SCP it to the instance, run with `nohup`. The script should: clone NInfer → cmake → build → download model → install Tailscale → launch server → health check. Avoid SSH heredocs — they break with special characters in API keys.

### Model Artifacts
- NVFP4: `neroued/Qwen3.6-27B-nvfp4-NInfer` — 18,324,064,000 bytes, SHA256: `bce5f00d066c0f20f1317bf1fdcb458264cf95837c3b1f3fbec163694627893a`
- Groupwise-int: `neroued/Qwen3.6-27B-NInfer` — 17,069,498,368 bytes
- Download via wget from HF CDN: `https://huggingface.co/neroued/Qwen3.6-27B-nvfp4-NInfer/resolve/main/qwen3_6_27b_nvfp4.ninfer`

### ninfer-serve Flags
```bash
ninfer-serve model.ninfer \
  --host 0.0.0.0 --port 8080 \
  --model-id qwen3.6-27b-nvfp4 \
  --max-context 262144 \
  --spec mtp --draft-tokens 3 --lm-head-draft \
  --kv-dtype int8 \
  --api-key "$(cat /root/.ninfer-key)" \
  --request-log-jsonl /tmp/ninfer-requests.jsonl
```
- Omit `--vision` to save ~3 GB VRAM (text-only deployment)
- Omit `--no-thinking` to keep thinking enabled (default)
- VRAM: ~27.5 GB used of 31.8 GB at 262K context

### LiteLLM Integration (ap-desktop)
The proxy runs as Docker container at `ghcr.io/berriai/litellm:main-stable`.
Config: `/home/amyn/repos/porb-server-2026/compose/litellm/config.yaml`
Restart: `docker restart <container_id>`

Model entry pattern:
```yaml
  - model_name: qwen3.6-27b-nvfp4
    litellm_params:
      model: openai/qwen3.6-27b-nvfp4
      drop_params: false
      api_base: http://<tailscale-ip>:8080/v1
      api_key: os.environ/VLLM_API_KEY
    model_info:
      mode: chat
      max_input_tokens: 262144
      max_tokens: 16384
      supports_function_calling: true
      supports_vision: false
      supports_reasoning: true
```

Fast variant (thinking disabled):
```yaml
  - model_name: qwen3.6-27b-nvfp4-fast
    litellm_params:
      model: openai/qwen3.6-27b-nvfp4
      extra_body:
        enable_thinking: false
      # ... same as above
    model_info:
      supports_reasoning: false
      # ...
```
