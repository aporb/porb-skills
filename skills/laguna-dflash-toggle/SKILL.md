---
name: laguna-dflash-toggle
description: Enable or disable DFlash speculative decoding on a Laguna S 2.1 vLLM
  deployment on Vast.ai. Covers download, restart with speculative config, acceptance
  rate verification, and rollback.
---

# Laguna DFlash Toggle

Enable or disable DFlash speculative decoding on a running Laguna S 2.1 vLLM deployment.

## Prerequisites

- vLLM already running with Laguna S 2.1
- HF_TOKEN available (check `~/.env.local` on local machine)
- Instance SSH accessible

## Enabling DFlash

### 1. Download draft model (do this while vLLM is still serving)

```bash
HF_TOKEN=$(grep "^HF_TOKEN=" ~/.env.local | cut -d= -f2-)
ssh -i ~/.ssh/id_vast_ai_ed25519 -p PORT root@HOST \
  "source /opt/laguna-venv/bin/activate && export HF_TOKEN='$HF_TOKEN' && HF_HUB_ENABLE_HF_XET=0 python3 -c \"
from huggingface_hub import snapshot_download
snapshot_download('poolside/Laguna-S-2.1-DFlash-NVFP4', local_dir='/models/Laguna-S-2.1-DFlash-NVFP4')
print('Done')
\""
```

### 2. Save rollback script (no DFlash version)

Write `/root/rollback-vllm.sh` on the instance with the current vLLM command minus `--speculative-config`.

### 3. Kill vLLM (use bracket trick!)

```bash
ssh ... "tmux kill-session -t vllm 2>/dev/null; sleep 2; pkill -9 -f '[v]llm serve' 2>/dev/null"
```

NEVER use `pkill -f vllm` without brackets — it matches the SSH command and kills your session.

### 4. Launch with DFlash

Write a launch script on the instance (avoids SSH nested-quoting issues):

```bash
#!/bin/bash
source /opt/laguna-venv/bin/activate
export HF_HUB_ENABLE_HF_XET=0
vllm serve poolside/Laguna-S-2.1-NVFP4 \
    --host 0.0.0.0 --port 8000 \
    --api-key 'KEY' \
    --tensor-parallel-size 4 \
    --max-model-len 262144 \
    --max-num-seqs 8 \
    --gpu-memory-utilization 0.85 \
    --enforce-eager \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --served-model-name laguna-s-2.1 \
    --speculative-config '{"model":"/models/Laguna-S-2.1-DFlash-NVFP4","num_speculative_tokens":5,"method":"dflash"}' \
    2>&1 | tee /tmp/vllm.log
```

Launch: `tmux new -d -s vllm /root/launch-vllm-dflash.sh`

### 5. Verify DFlash is working (NOT just health check)

Health 200 ≠ DFlash working. Check actual metrics:

```bash
# Fire a real completion
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Authorization: Bearer KEY' \
  -d '{"model":"laguna-s-2.1","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'

# Check spec decode counters
curl -s http://localhost:8000/metrics | grep -E 'spec_decode_num_drafts_total|spec_decode_num_accepted_tokens_total'
```

Acceptance rate = accepted / drafts. Expect 40-60% for Laguna DFlash.

### 6. Verify VRAM

```bash
nvidia-smi --query-gpu=memory.used --format=csv,noheader
```

With DFlash at TP-4 on 5090: expect ~28 GB/GPU. Without: ~31 GB/GPU.

## Disabling DFlash

Run the rollback script: `bash /root/rollback-vllm.sh`

## Updating on-start script

After confirming DFlash works, update the local `vastai-on-start.sh` then register:

```bash
ONSTART_B64=$(base64 -i vastai-on-start.sh | tr -d '\n')
vastai update instance INSTANCE_ID --image "IMAGE_UUID" --onstart "$ONSTART_B64"
```

Vast.ai CLI requires both `--image` and `--onstart` together.

## Gotchas

- **pkill bracket trick**: Always `pkill -f '[v]llm serve'` on remote — bare `pkill -f vllm` kills your SSH session
- **Local path > HF path**: Use `/models/Laguna-S-2.1-DFlash-NVFP4` in speculative-config, not the HF repo ID — no token needed at startup
- **Download before kill**: Download the draft model while vLLM is still serving to minimize downtime
- **Don't trust health check alone**: A 200 on /health doesn't mean spec decode is producing results — check /metrics
- **DFlash shards across TP group**: ~280 MB/GPU at TP-8, not 2 GB on one GPU
