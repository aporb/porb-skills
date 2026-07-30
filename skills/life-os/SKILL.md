---
name: life-os
description: "Continuous always-on dashboard at http://localhost:9876/. Replaces /weekly-knockout and /ceo-briefing with a single OODA-framed (Observe / Orient / Decide / Act) dashboard backed by a producer-cache-consumer kernel."
---
---
name: life-os
description: "Skill: life-os"
---# life-os

Tier C (CEO-direct). Continuous always-on dashboard at http://localhost:9876/.

Replaces `/weekly-knockout` and `/ceo-briefing` with a single OODA-framed (Observe / Orient / Decide / Act) dashboard backed by a hardened producer-cache-consumer kernel.

## Run

```bash
# First-time setup: brew deps + register launchd agents + start kernel
brew install terminal-notifier fswatch
bash .claude/skills/life-os/lib/install-launchd.sh --apply

# Open dashboard
open http://localhost:9876/
```

## What it does

1. Four launchd LaunchAgents run continuously: `com.lifeos.kernel` (HTTP server), `com.lifeos.pulse` (4x/day full sweep), `com.lifeos.auth` (hourly auth probe), `com.lifeos.notify` (alert dispatcher via fswatch + terminal-notifier).
2. 15 drivers in `drivers/probe-*.sh` write atomic JSON to `admin/briefings/private/cache/probes/`.
3. Synthesize layer reads probes (with last-known-good fallback), runs cross-portfolio leak grep, atomically writes `admin/briefings/private/cache/state.json`.
4. Dashboard polls `/api/state` every 30s, renders OODA quadrants via safe DOM methods (createElement + textContent, never innerHTML on user content).

## Privacy

Localhost only. Server binds to 127.0.0.1. All endpoints reject non-localhost Host headers. Cache lives in `admin/briefings/private/cache/` (gitignored). Cross-portfolio leak grep is a build-time block, not a warning.

## Interactivity

Whitelist of safe actions (refresh / sync / open): one-click on dashboard. Outbound actions (send mail, post X, sign documents) gated by Pineapple Protocol modal: codeword + 3-word affirmation, server-side validated, every attempt audit-logged.

## Tests

```bash
cd .claude/skills/life-os && python -m pytest tests/ -v
bash tests/test_e2e.sh
bash tests/test_leak_e2e.sh
```

## Dispatch tier: C

Per `.claude/skills/SKILL-PATTERN.md`. CEO-direct, no agent dispatch.

## Migration from `/weekly-knockout` + `/ceo-briefing`

Both old skills are deprecated 2026-04-30. After 14 days of stable life-os operation (~2026-05-14), they get deleted. During the transition, legacy runners continue to work.

See `docs/superpowers/specs/2026-04-30-life-os-phase1-design.md`.
