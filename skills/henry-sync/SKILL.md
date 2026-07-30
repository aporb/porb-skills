---

name: henry-sync
description: "Sync Henry/Hermes shared infrastructure between laptop and Hostinger. Two targets: `vault` (Obsidian notes, default) and `wiki` (cross-repo entity wiki). Default action pulls from server. Pass 'commit' to push local edits, 'status' for a 3-way view, 'refresh-soul' to re-snapshot Henry's SOUL.md, or 'enable-auto' / 'disable-auto' to toggle the daily launchd pull. Prefix any action with `wiki` to act on the wiki instead of the vault (e.g. `/henry-sync wiki`, `/henry-sync wiki commit \"msg\"`)."
---

# /henry-sync — Henry/Hermes Sync (Vault + Wiki)

Wraps the scripts in `operations/henry-hermes/scripts/` plus the launchd plists in `operations/henry-hermes/launchd/`. One skill, one shortcut, no typing long paths. Two sync targets share the same control surface: the Obsidian **vault** and the cross-repo **wiki**.

## Targets

| Token | Submodule | Server path | Default | Auto-sync slot |
|---|---|---|---|---|
| (none) / `vault` | `operations/henry-hermes/vault` | `/root/Documents/Henry Vault` | yes | 09:00 local (launchd) |
| `wiki` | `operations/henry-hermes/wiki` | `/root/Documents/Henry Wiki` | no | 10:00 local (launchd) |

If the first arg is `wiki`, the action token shifts right one position. Everything else is identical.

## Vault actions (default)

| Arg | What it does | Script |
|---|---|---|
| `pull` (default) | Fetch + rebase from origin; fails if local vault is dirty | `scripts/henry-sync.sh` |
| `commit [msg]` | Stage, commit, push local vault edits; timestamp fallback if no message | `scripts/henry-commit.sh` |
| `status` | 3-way view: laptop submodule, GitHub origin, server via ssh | `scripts/henry-status.sh` |
| `refresh-soul` | Re-snapshot Henry's SOUL.md from the server to `config/SOUL.md.mirror` | `scripts/refresh-soul-mirror.sh` |
| `enable-auto` | Copy + `launchctl load` the daily 09:00 local vault pull | `launchd/com.harbor.henry-sync.plist` |
| `disable-auto` | `launchctl unload` and remove the vault plist | `launchd/com.harbor.henry-sync.plist` |

No arg = vault `pull`. That's the 90% path.

## Wiki actions

Identical action vocabulary, prefixed with `wiki`:

| Arg | What it does | Script |
|---|---|---|
| `wiki` (= `wiki pull`) | Fetch + rebase wiki from origin; fails if local wiki is dirty | `scripts/henry-wiki-sync.sh` |
| `wiki commit [msg]` | Stage, commit, push local wiki edits | `scripts/henry-wiki-commit.sh` |
| `wiki status` | 3-way view for the wiki | `scripts/henry-wiki-status.sh` |
| `wiki enable-auto` | Copy + `launchctl load` the daily 10:00 local wiki pull | `launchd/com.harbor.henry-wiki-sync.plist` |
| `wiki disable-auto` | `launchctl unload` and remove the wiki plist | `launchd/com.harbor.henry-wiki-sync.plist` |

`refresh-soul` is vault-only — the wiki has no SOUL mirror.


## Execution (pure tool)

This skill is a **mechanical wrapper**. No agent dispatch. See `.claude/skills/SKILL-PATTERN.md` Tier D.

**Rationale:** rsync wrapper that pushes/pulls an Obsidian vault between laptop and Hostinger server. Deterministic file sync; no judgment. Agent dispatch would waste tokens.

The invocation contract below is the complete tool interface. If cognitive work (triage, composition, voice-check) ever gets added to this skill, that work must be delegated to the appropriate specialist agent rather than inlined here.

---

The procedural playbook below is the tool contract.

## Run it

```bash
# --- vault (default target) ---

# default: pull vault from server
bash operations/henry-hermes/scripts/henry-sync.sh

# push local vault edits
bash operations/henry-hermes/scripts/henry-commit.sh "updated People/Amyn.md"

# 3-way vault status
bash operations/henry-hermes/scripts/henry-status.sh

# refresh the SOUL.md mirror
bash operations/henry-hermes/scripts/refresh-soul-mirror.sh

# enable daily auto-pull (vault, 09:00)
cp operations/henry-hermes/launchd/com.harbor.henry-sync.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.harbor.henry-sync.plist

# disable daily auto-pull (vault)
launchctl unload ~/Library/LaunchAgents/com.harbor.henry-sync.plist && rm ~/Library/LaunchAgents/com.harbor.henry-sync.plist

# --- wiki (use 'wiki' as first arg to /henry-sync) ---

# pull wiki from server
bash operations/henry-hermes/scripts/henry-wiki-sync.sh

# push local wiki edits
bash operations/henry-hermes/scripts/henry-wiki-commit.sh "added concept page for foo"

# 3-way wiki status
bash operations/henry-hermes/scripts/henry-wiki-status.sh

# enable daily auto-pull (wiki, 10:00)
cp operations/henry-hermes/launchd/com.harbor.henry-wiki-sync.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.harbor.henry-wiki-sync.plist

# disable daily auto-pull (wiki)
launchctl unload ~/Library/LaunchAgents/com.harbor.henry-wiki-sync.plist && rm ~/Library/LaunchAgents/com.harbor.henry-wiki-sync.plist
```

When this skill runs: read the args, pick the target (`wiki` if first arg = `wiki`, else `vault`) and the action (default `pull`), execute the one command, and report the exit status plus the last few lines of output. Do not pre-check the state of the submodule, do not re-verify, do not summarize what the scripts are about to do. Run, report, stop.

## Error handling

- `exit 1` from `henry-sync.sh` / `henry-wiki-sync.sh` = dirty target. Tell the user to run `/henry-sync commit "msg"` (vault) or `/henry-sync wiki commit "msg"` (wiki) first.
- `exit 3` from any script = submodule not initialized. Run `git submodule update --init operations/henry-hermes/vault` (vault) or `git submodule update --init operations/henry-hermes/wiki` (wiki).
- `ssh_hostinger` failure inside either status script = server unreachable or zsh alias not resolving in bash subshell. Known gotcha — the scripts already work around it via `HOSTINGER_SSH`. If it breaks again, `LRN-20260414-001` has the fix.

## Output budget

Under 10 lines unless there's a conflict or error. This is a sync skill, not a briefing. Amyn's feedback memory `feedback_terse_status_reports.md` applies: where it is + what changed + what's left. Skip the verification table.

## See also

- `operations/henry-hermes/README.md` — full description of the control plane
- `operations/henry-hermes/runbook.md` — recovery procedures (conflicts, key rotation, nuke+rebuild)
- `.learnings/LEARNINGS.md` LRN-20260414-001 — zsh alias not inheriting to bash subshells
- Private repo: https://github.com/aporb/henry-hermes-vault
