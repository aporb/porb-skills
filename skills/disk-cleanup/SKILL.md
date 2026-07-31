---
name: disk-cleanup
description: macOS disk-space cleanup — measure the TRUE free space, scan for the biggest consumers, interview the user on goals and risk tolerance, then reclaim space in safety tiers (auto-clean regenerable caches; confirm judgment calls). Use this whenever the user wants to free up / clean up / reclaim disk space, says their Mac is full or low on storage, asks what's eating their disk, mentions purgeable space, or wants to prune caches, Docker, node_modules, AI model weights (HuggingFace/ Ollama), or Xcode data — even if they don't say the word "cleanup".
argument-hint: "[optional: GB to free, or a focus area like 'docker' or 'AI models']"
---

# Disk Cleanup (macOS)

Reclaim disk space safely and measurably. The method has three commitments:

1. **Measure ground truth, not appearances.** Use `diskutil` container free space,
   never `df`. Report the *measured* before/after delta, never the sum of what you
   deleted (APFS accounting shifts in real time).
2. **Tier by reversibility.** Auto-clean only regenerable junk (a re-download or
   recompute away). Everything that could be wanted — AI models, app data, media —
   is a confirmed decision, never an automatic one.
3. **Prefer the tool's own cache command over `rm -rf`.** pnpm hardlinks, Go's
   read-only modcache, and HuggingFace refs all break under a blind delete.

This skill is macOS/APFS-specific. Its scripts live at `${CLAUDE_SKILL_DIR}/`.

## Workflow

### 1. Measure + scan
Run the read-only scanner and read the whole output before reasoning:
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/scan.sh"        # add --quick to skip the slow $HOME walk
```
It prints true free space, % full, the biggest consumers in `~`, `~/Library`,
`Application Support`, `~/.cache`, package-manager cache sizes, known hogs,
snapshot count, and Docker usage. Classify what it finds against
`references/targets.md` (Tier 1 safe / Tier 2 ask / Tier 3 never).

### 2. Interview the user
Before deleting anything, ask with the `AskUserQuestion` tool. These four
questions have proven to capture intent well — adapt wording, keep the shape:

- **Goal** — Free as much as possible · Hit a target number · Find the biggest hogs · Set up recurring hygiene
- **Risk** — Conservative (caches/Trash/logs only) · Moderate (+ dev artifacts) · Aggressive (+ large media, dormant VMs/images) · I approve each
- **Targets** (multi-select) — Dev artifacts · Docker/VMs/AI models · Downloads/caches/logs · Backups & large media
- **Mode** — Scan then propose · Auto-clean safe tier then ask about the rest · Report only

Let their **Mode** and **Risk** answers drive everything below. (`AskUserQuestion`
allows max 4 options per question — split if you need more.)

### 3. Execute the safe tier
Unless Mode is "Report only", reclaim the regenerable tier. Preview first if the
user is cautious:
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/safe_clean.sh" --dry-run   # show what would go
bash "${CLAUDE_SKILL_DIR}/scripts/safe_clean.sh"             # do it, with measured before/after
```
This covers package-manager caches (via tool commands), Trash, browser HTTP
caches, and Docker dangling/build cache only. It deliberately does **not** touch
anything in Tier 2/3.

### 4. Handle the judgment calls (Tier 2)
For everything the user greenlit that isn't pure cache, confirm in batches with
sizes, then act per `references/targets.md`:
- **HuggingFace** — delete whole `models--<org>--<name>` dirs. Show the user the
  per-model sizes (`du -sh ~/.cache/huggingface/hub/* | sort -h`) and let them pick.
- **Ollama** — `ollama rm` for whole models; for leftover blobs run
  bash "${CLAUDE_SKILL_DIR}/scripts/ollama_gc.sh"` (read-only) then `--apply`.
- **Xcode** `DerivedData` (safe-ish), `iOS DeviceSupport`, `xcrun simctl delete unavailable`. Never auto-touch `Archives`.
- **Electron app caches** — quit the app, clear only the cache subdirs (see targets.md).
- **Docker images / Downloads / large media / stale node_modules** — list with sizes, confirm, delete.

Always use exact paths (not globs) when removing a specific model or dir, so a
sibling with a longer name isn't caught.

### 5. Verify + report
Re-measure and confirm nothing wanted was lost:
```bash
diskutil info / | grep "Container Free Space"
ollama list 2>/dev/null                                  # kept models intact?
ls ~/.cache/huggingface/hub | grep '^models'             # kept HF models intact?
```
Report the **measured** delta (start free → end free), a per-round breakdown, and
explicitly list what you kept. If free space barely moved despite big deletes,
suspect purgeable space held by snapshots and offer to thin them.

### 6. Offer follow-ups
- **Recurring hygiene** — the big regenerating caches (uv, pnpm, brew, Docker) will
  creep back. Offer a weekly `launchd` job that runs `safe_clean.sh`.
- If the user keeps a session log (e.g. `~/.remember/`), offer to append a one-line entry.

## Honest reporting
State the measured number even when it's less than the arithmetic suggests, and
explain why (purgeable / live writes). Confirm kept items by listing them. If a
deletion failed or a tool was missing, say so — never imply more was freed than the
container delta shows.

## Scripts
- `scripts/scan.sh [--quick]` — read-only discovery + classification. Never deletes.
- `scripts/safe_clean.sh [--dry-run]` — auto-clean the safe tier, measured.
- `scripts/ollama_gc.sh [--apply]` — orphan-blob reaper; read-only unless `--apply`; hard-aborts if no manifests.

## Reference
- `references/targets.md` — full Tier 1/2/3 catalog with exact paths, the tool
  commands, and the APFS gotchas (diskutil-not-df, purgeable space, du over-reporting).
