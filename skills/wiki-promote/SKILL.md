---
name: wiki-promote
description: Promote a session insight, query answer, or working/episodic note into a canonical synthesis page in the wiki. Karpathy's "filed-back syntheses" pattern — ensures conversations compound into the knowledge base instead of evaporating. Three sub-actions. (1) `synthesis <slug>` — promote an episodic query/summary into `syntheses/<slug>.md` with full v2 frontmatter. (2) `draft <slug>` — promote a `_drafts/<slug>.md` page into canonical `entities/<slug>.md`. (3) `audit` — list all working/episodic pages older than their `expires:` date as supersession candidates. Default action is `synthesis` if a slug is given without sub-action.
user-invocable: true
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Grep
---

# /wiki-promote — File a session insight back into the wiki

Implements the Karpathy "compound knowledge" pattern from his April 2026 LLM-wiki tweet:

> "I end up 'filing' the outputs back into the wiki to enhance it for further queries. So my own explorations and queries always 'add up' in the knowledge base."

The HARBOR wiki has an `episodic/` tier (session summaries + query answers) and a `semantic/` tier (durable cross-session facts, including `syntheses/`). Without a promotion path, episodic content evaporates after 30-90 days. This skill is the bridge.

## Actions

### `synthesis <slug>` — episodic → semantic

When a query answer in `wiki/episodic/` (or even an inline session insight) deserves to outlive its session:

1. Read the source page (or the conversation context if no source page).
2. Write `wiki/syntheses/<slug>.md` with:
   - `type: synthesis`
   - `tier: semantic`
   - `lifecycle: active`
   - `source_count: N` (number of distinct sources cited)
   - `last_verified: <today>`
   - `contradicts: []` (or fill if conflicts noted)
   - `tags:` from the source content
   - `sources:` paths into vault/ if applicable
   - At least 2 outbound `[[wikilinks]]` to existing entities/concepts.
3. Update the source episodic page (if any) to set `superseded_by: <new-slug>`.
4. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] promote-synthesis | <slug>
   - Promoted from <source-page> (or session)
   - Outbound links: [[a]], [[b]], [[c]]
   - source_count: N
   ```
5. Run `python3 scripts/build-indices.py` to refresh `syntheses/index.md`.
6. Run `python3 scripts/validate.py` to confirm clean health.

### `draft <slug>` — _drafts/ → entities/

When an auto-extracted entity page in `wiki/_drafts/` (e.g., from a portfolio member's first-3-mention promotion) has been reviewed and approved:

1. Read `wiki/_drafts/<slug>.md`.
2. **Cross-engagement check** — grep the draft body for any other portfolio member's name (see `admin/memory/portfolio-aliases.md` — never reproduce that list inline). If found, halt and surface the leak before proceeding.
3. Move file: `git mv _drafts/<slug>.md entities/<slug>.md`.
4. Update frontmatter: `lifecycle: draft` → `lifecycle: active`.
5. Add to `index.md` (the top-level dispatcher).
6. Append to `log.md`: `## [YYYY-MM-DD] promote-draft | <slug>`.
7. Re-run `build-indices.py` + `validate.py`.

### `audit` — find expired working/episodic pages

1. Read every page in `wiki/working/` and `wiki/episodic/`.
2. List those whose `expires:` field is in the past, OR whose `created:` date is older than the tier's max retention (working: 14 days, episodic: 90 days).
3. For each, propose: archive (move to `_archive/`) OR promote to synthesis OR delete.
4. Output a table; do not act without explicit user approval.

## Pineapple Protocol

Cross-engagement confidentiality is enforced by the `draft` action's grep step. The `synthesis` action does not face the same risk because syntheses are by nature cross-cutting — but if a synthesis touches portfolio data, the same grep applies.

Any action that would push to the wiki's GitHub origin gates through user approval (default: commit only on submodule, parent pointer not bumped automatically).

## Output style

After the action completes, report in the format established by the validator:

```
promote-synthesis: <slug>
  source: <source-page-or-session>
  links: [[a]], [[b]], [[c]] (3 outbound)
  source_count: 2 last_verified: 2026-04-27
  syntheses/index.md regenerated (1 page total)
  health: 0 errors, 143 warnings, 1 info
```

Terse status, evidence-backed.

## Status

This skill is a **stub** as of 2026-04-27 — the protocol is documented and the wiki schema (SCHEMA.md v2) supports it, but the directory layout (`syntheses/`, `_drafts/`) was just created today and has 0 pages. First production use will exercise the `synthesis` action when a session generates an insight worth filing.

The companion validator (`wiki/scripts/validate.py`) and index-generator (`wiki/scripts/build-indices.py`) exist and are wired into `henry-wiki-status.sh`. The promotion flow itself runs in this skill at agent-time; no separate Python entry point.

## Related

- `wiki/SCHEMA.md` — the v2 contract this skill enforces
- `.claude/skills/henry-sync/SKILL.md` — vault + wiki sync wrappers
- `wiki/scripts/validate.py` — runs health check after every promote
- `wiki/scripts/build-indices.py` — refreshes per-directory indices
