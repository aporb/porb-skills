---
name: litellm-skill-hub-sync
description: Sync managed skills from a git repo to OMP and PI agents via LiteLLM Skill Hub registration
triggers:
  - register skill on hub
  - sync skills to agents
  - skill hub registration
  - liteLLM plugin
  - plugin registration
---
# LiteLLM Skill Hub → Agent Sync

## Architecture

```
GitHub repo (porb-skills)
    │  skills/<name>/SKILL.md
    ▼
LiteLLM Skill Hub (/claude-code/plugins)
    │  git-subdir plugin registration
    ▼
┌──────────────┐  ┌──────────────┐
│  OMP agent   │  │  PI agent    │
│  sync script │  │  extension   │
│  symlink     │  │  clone+sym   │
└──────────────┘  └──────────────┘
```

## Registration

```bash
curl -X POST \
  -H "Authorization: Bearer <MASTER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "plugin-name",
    "version": "1.0.0",
    "description": "...",
    "source": {
      "source": "git-subdir",
      "url": "https://github.com/user/repo",
      "path": "skills"
    },
    "enabled": true
  }' \
  "https://litellm.h.porb.dev/claude-code/plugins"
```

**Critical**: `path` MUST be `segment/segment` format (e.g. `skills`). Using `"."` returns error.

## Verification

```bash
# Public hub
curl -s https://litellm.h.porb.dev/public/skill_hub | jq '.plugins[].name'

# Marketplace
curl -s https://litellm.h.porb.dev/claude-code/marketplace.json | jq '.plugins[].name'
```

## OMP Integration

Git clone/pull + symlink pattern. Script at `~/.omp/bin/sync-skills.sh`:
- Clone from GitHub into `~/.omp/agent/managed-skills/porb-skills/`
- Symlink each `skills/<name>/` into `managed-skills/<name>/`
- `-L` tests need `${var%/}` to strip trailing slash (dereferences symlinks)

## PI Extension Pattern

Extension files in `~/.pi/agent/extensions/` are auto-discovered.
Template: export default function (pi: ExtensionAPI), register commands with `pi.registerCommand()`, onStart hook with `pi.on("session_start", ...)`.

## Skill Format

Minimum frontmatter:
```yaml
---
name: kebab-case-name
description: Single-line description.
---
```

Extra fields (triggers, compatibility, metadata) are preserved — consumers that don't understand them will ignore.

## Undo

```bash
curl -X DELETE \
  -H "Authorization: Bearer <MASTER_KEY>" \
  "https://litellm.h.porb.dev/claude-code/plugins/plugin-name"
```
