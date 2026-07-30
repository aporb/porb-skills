---
name: auto-shutdown-fix
description: Fix and deploy auto-shutdown.sh for Vast.ai instances — counter comparison,
  metric extraction, launchd destroy timer, and verification
---

# auto-shutdown fix deployment

Deploy fixes for Vast.ai instance auto-shutdown.sh covering: idle counter comparison, metric extraction, Mac-side destroy timer.

## Quick reference

- Instance: `root@ssh1.vast.ai` (port varies — check `vastai show instance ID`)
- SSH key: `~/.ssh/id_vast_ai_ed25519`
- Script path on instance: `/opt/auto-shutdown.sh`
- Cron: `*/5 * * * * /opt/auto-shutdown.sh`
- Vast.ai API key: `grep "^VAST_AI_API_KEY=" ~/.env.local | cut -d= -f2-` (NEVER `source ~/.env.local` — has unquoted SSH keys)
- Launchd: `~/.vastai/destroy-46047030.plist`

## Deploy cycle

```bash
scp -i ~/.ssh/id_vast_ai_ed25519 -P PORT auto-shutdown.sh root@ssh1.vast.ai:/opt/auto-shutdown.sh
ssh -i ~/.ssh/id_vast_ai_ed25519 -p PORT root@ssh1.vast.ai 'rm -f /tmp/idle_count /tmp/vllm_counter_last; IDLE_THRESHOLD=18 bash /opt/auto-shutdown.sh'
```

## Testing checklist

1. **Counter comparison**: make vLLM request, confirm "Counter advanced" log, idle_count=0
2. **Fail-safe**: kill vLLM, confirm "metrics unreachable — treating as active", exit 0
3. **Metric extraction**: `curl -sf localhost:8000/metrics | grep "^vllm:request_success_total{" | awk '{s+=$2} END {print s+0}'`
4. **Guard bypass**: if using process-age guard, touch `/tmp/vllm.log` to be old before test runs
5. **Destroy timer**: `launchctl start destroy-46047030` then `tail ~/.vastai/destroy-timer-46047030.log`
6. **Deploy verify**: `md5sum` both local and remote copies match

## Common pitfalls

- `set -euo pipefail` + `cmd | head -1` → SIGPIPE exits non-zero → use `|| true` + `"${var:-default}"` fallback
- vLLM metrics have labels: pattern is `vllm:request_success_total{engine="0",...}` — grep with `{`
- Multi-GPU: use `sort -n | tail -1` for max GPU utilization, not `head -1`
- Launchd: must add `~/.local/bin` to PATH via `EnvironmentVariables` or use full paths
- Vast.ai CLI has ANSI color codes: strip with `sed 's/\x1b\[[0-9;]*m//g'`
- Don't `source ~/.env.local` — SSH key lines will be executed as commands
