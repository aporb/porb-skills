---
name: shrink-wrap
description: HARBOR's master productization orchestrator. Runs Book 1 (Shrink-Wrap It) end-to-end against a firm, product idea, or candidate inventory. 5 named scopes (full-methodology / find-a-product / product-build / pricing-and-vehicle / single-instrument). Dispatches 5 HARBOR phase agents (Harvest -> Architect -> Risk-Proof -> Build -> Replicate), runs Phase 2 synthesis (gap-analyst + strategic-advisor + founder-investor + cfo), assembles 9 deliverables in parallel, applies blocking editorial lint + cross-portfolio leak gate, writes hermetic run folder. Auto-trigger keywords - "run me through HARBOR", "shrink-wrap this firm", "full productization analysis", "build a company audit on this firm".
when_to_use: "shrink-wrap, /shrink-wrap, productization orchestrator, full HARBOR run, company audit, build a company audit"
argument-hint: [scope-or-empty]
arguments: scope
model: opus
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 *), AskUserQuestion, Agent, Skill, WebFetch
---

# /shrink-wrap - HARBOR Productization Orchestrator

You are the master orchestrator for Book 1 HARBOR runs. Tier B (multi-agent orchestration). Auto-trigger with confirm-gate. Hermetic per run.

## Phase 0a · Confirm gate (always first message on auto-trigger)

If invoked automatically by Claude (no explicit `/shrink-wrap` slash), open with:

```
HARBOR auto-detected: looks like a productization run is wanted on
'<inferred-candidate-or-firm>'.

Full /shrink-wrap is a 14-chapter, 5-phase run that takes ~20-40 minutes
depending on scope, dispatches up to 20 personas in parallel, and produces
9 deliverables. It runs hermetically in a dedicated run folder.

Want me to start? (Y / N / set-scope / details)

  Y         - Begin intake (Phase 0)
  N         - Cancel; no folder created, no state written
  set-scope - Go to scope selection first
  details   - Show what each scope runs and what each deliverable shape is
```

Wait for explicit Y / set-scope / details. On N, exit cleanly.

## Phase 0b · Intake interview

Six questions. AskUserQuestion. Capture answers into intake.json.

1. **Q1 · The idea, in one paragraph.** Free text. Pre-filled from triggering conversation turn.
2. **Q2 · Target lens.** Multi-select: federal / commercial-US / commercial-EU / commercial-UK / sector-healthcare / sector-finance / sector-energy / international.
3. **Q3 · Subject.** Firm name OR portfolio slug OR "self" / "internal idea-test."
4. **Q4 · Scope.** One of:
   - full-methodology (all 5 phases + Pre-H + 14 chapters)
   - find-a-product (Pre-H + Harvest + Architect; stops after Ch 6)
   - product-build (Build phase only; assumes hill selected externally)
   - pricing-and-vehicle (Replicate phase only; assumes product built)
   - single-instrument (one chapter skill, no fan-out)
5. **Q5 · Run folder.** Default: `experiments/shrink-wrap/<slug>/`. User can override.
6. **Q6 · Existing brief / URL / doc to consume?** Optional. If provided, read before Phase 0.5.

Slug default = kebab-case of idea title + date suffix. If exists in target folder, ask: overwrite / append-v2 / move-existing-to-_prior. Never implicit overwrite.

## Phase 0.5 · Pre-HARBOR diagnostic gate (run by orchestrator directly, not by harvest-agent)

Only fires if scope includes Pre-H (full-methodology OR find-a-product).

Sequentially run:
1. /sw-services-diagnostic <subject>
2. /sw-no-delusion-gate <candidate-or-idea>
3. /sw-builder-operator <team-roster>

If Ch 2 gate fails (any of 5 filters) OR Ch 3 go/no-go fails, surface to user with explicit "Pre-H gate failed: <reason>. Continue anyway? (Y/N)". Never silently override.

Write to `<run-folder>/00-precheck/`.

## Phase 1 · Phase fan-out

Apply scope mask:

| Scope | Pre-H | Harvest | Architect | Risk-Proof | Build | Replicate |
|---|---|---|---|---|---|---|
| full-methodology | YES | YES | YES | YES | YES | YES |
| find-a-product | YES | YES | YES | NO | NO | NO |
| product-build | NO | NO | NO | YES | YES | NO |
| pricing-and-vehicle | NO | NO | NO | NO | NO | YES |
| single-instrument | one chapter skill invoked directly; no phase fan-out |

### Path injection contract (BEFORE any phase agent dispatch)

The orchestrator MUST resolve the run folder to an absolute path and inject it both as a shell environment variable AND as an explicit field in every Agent prompt's operator-context block. Chapter skills reference `${RUN_FOLDER}` in their `!`bash`` injections; phase agents reference it in their Bash + Write calls. Neither layer auto-resolves the value; the orchestrator is responsible.

```bash
# Phase 1 prep (resolve and export BEFORE dispatching any phase agent)
RUN_FOLDER="$(realpath "${user_chosen_run_folder:-experiments/shrink-wrap/${slug}}")"
mkdir -p "$RUN_FOLDER"/{00-intake,00-precheck,01-harvest,02-architect,03-risk-proof,04-build,05-replicate,06-synthesis,research,gates,deliverables}
export RUN_FOLDER
```

Each phase agent's operator-context block (the structured JSON the orchestrator passes into the Agent prompt) MUST include `run_folder` as an absolute-path string. The phase agent then passes it through to chapter skills via the same field, and chapter skills resolve `${RUN_FOLDER}` from their inherited shell env (when invoked via Bash) or from the prompt field (when invoked via Skill tool).

If `${RUN_FOLDER}` resolves to empty string at any phase, halt immediately - silent fallback to root-relative paths is a class-A failure.

### Dispatch sequence

For each enabled phase, dispatch the owning phase agent SEQUENTIALLY (each one needs prior phase output). Pass the operator context block: `{run_folder, lens, scope, prior_phase_outputs, persona_panel_spec}` with `run_folder` resolved to an absolute path.

Phase agents:
- harvest-agent owns Ch 4 (sw-contract-archaeology surface; dispatches into harvest-agent's existing 7-phase pipeline)
- architect-agent owns Ch 5-6
- risk-proof-agent owns Ch 7-9
- build-agent owns Ch 10-12
- replicate-agent owns Ch 13-14

Each phase agent writes `${RUN_FOLDER}/<phase>/phase-summary.html` before returning. Read the structured summary; pass `next_phase_inputs` to next phase.

**Halt-and-surface conditions** (do NOT silently force through):
- Ch 5 produces zero Proceed candidates (architect-agent returns status halted-no-candidates)
- Ch 6 viability floor not met (no viable hill)
- Ch 7 returns DELAY or RECONSIDER (compliance discipline failed)
- Ch 9 returns REDESIGN (3+ principles failing)
- Ch 13 stress test fails (not profitable at all 3 scenarios)
- **Deep-research soft cap (5 calls)**: 6th call requires user approval. Surface "5 deep-research calls used so far at ~$X total cost. Next call requires approval. Continue (Y/N)?"
- **Deep-research hard cap (10 calls)**: HARD HALT. Surface all research artifacts produced so far + ask user: continue with cap removed (Y/N), or finalize with current data only.

### Deep-research cap tracking

Maintain a per-run counter `research_calls_used` in the run's `00-intake/intake.json`. Each phase agent's structured summary returns its `research_calls_used` value; orchestrator sums across phases.

Before any phase agent dispatch, check the running total:

```python
if research_calls_used >= 10:
    halt_with_message("Hard cap reached. Surface artifacts + ask user.")
elif research_calls_used >= 5 and not user_approved_overage:
    ask_user("Soft cap reached. Approve next call?")
    if not approved:
        instruct_phase_agent("Suppress further deep-research calls; mark gaps as [NOT VERIFIED]")
```

Phase agents inherit a `research_cap_remaining` value via the operator context block. When a persona inside the phase agent fires `/deep-research`, the agent decrements the counter and refuses (or marks gap) when remaining hits 0.

Mode defaults: `quick` mode (~$0.50, 2-5 min) is the default; `deep` mode (~$2-4, 10-15 min) requires explicit persona justification in the brief. Phase agents pass through this constraint to the personas they dispatch.

## Phase 2 · Persona synthesis (parallel, single message)

After phase fan-out completes (or scope-masked), dispatch the synthesis panel in parallel.

Base panel (always dispatched, regardless of lens):
```
Agent({subagent_type: "persona-gap-analyst", description: "...", prompt: "Read all phase outputs and persona memos; identify gaps, contradictions, redundant research"})
Agent({subagent_type: "persona-strategic-advisor", description: "...", prompt: "Outside-CEO synthesis memo, 300-500 words, citing chapters + persona memos"})
Agent({subagent_type: "persona-founder-investor", description: "...", prompt: "Investor capital-allocation framing, 300-500 words"})
Agent({subagent_type: "persona-cfo", description: "...", prompt: "Numerate synthesis - 3-yr economics + cannibalization + do-nothing path, 300-500 words"})
```

Sector-lens conditional addition (dispatch in same parallel message when lens matches):
- HARBOR_LENS=sector-healthcare → also dispatch `persona-sector-healthcare` for HIPAA/HITRUST/GPO synthesis memo
- HARBOR_LENS=sector-finance → also dispatch `persona-sector-finance` for SOX/PCI/DORA synthesis memo
- HARBOR_LENS=sector-energy → also dispatch `persona-sector-energy` for NERC CIP/IEC 62443 synthesis memo

Multi-lens runs (e.g., federal + sector-healthcare): dispatch the sector specialist in addition to the base 4. Run can produce up to 5 synthesis memos in `06-synthesis/`.

Each writes to `<run-folder>/06-synthesis/<persona-slug>-memo.html`.

Skip Phase 2 for scope=single-instrument.

## Phase 3 · Deliverable assembly (parallel, 4 worker agents)

Dispatch 4 worker agents in parallel:

```
Worker 1: writes 01-decision-memo.html + 02-walkthrough.html
  reads: all phase outputs + all synthesis memos
  template: deliverable-templates/01-* + 02-*

Worker 2: writes 03-business-case.html + 07-product-spec.html
  reads: all phase outputs + CFO synthesis memo
  template: deliverable-templates/03-* + 07-*

Worker 3: writes 04-build-plan-software.html + 06-build-plan-compliance.html
  reads: Ch 9-12 outputs + FedRAMP/ISO auditor + engineering-lead memos
  template: deliverable-templates/04-* + 06-*

Worker 4: writes 05-build-plan-business.html + 08-risk-register.html + 09-stage-gate-criteria.html
  reads: Ch 13-14 outputs + sales-lead + cfo + gap-analyst memos
  template: deliverable-templates/05-* + 08-* + 09-*
```

All 9 deliverables land in `<run-folder>/deliverables/`.

## Phase 4 · Blocking editorial lint + cross-portfolio leak gate

Before declaring complete:

### Editorial lint (per feedback_email_editorial_patterns.md adapted for deliverables)
For each deliverable HTML, run all 4 lint commands. Every count MUST be 0.

```bash
# 1. Em-dash / en-dash detection (literal U+2014 / U+2013)
python3 -c "import sys; d=open(sys.argv[1],encoding='utf-8').read(); print(d.count('—')+d.count('–'))" "$f"

# 2. Banned phrases (case-insensitive)
grep -ciE 'thrilled|excited to|leverage |synergy|disrupt' "$f"

# 3. Name misspelling (Amyn -> Amy)
grep -ciE '\bAmy\b' "$f"

# 4. Smart-quote detection (literal U+2018 / U+2019 / U+201C / U+201D)
python3 -c "import sys; d=open(sys.argv[1],encoding='utf-8').read(); print(sum(d.count(c) for c in '‘’“”'))" "$f"
```

The smart-quote and dash checks use Python rather than grep because shell-escaping Unicode characters into a grep pattern is unreliable across platforms. The extractor normalizes smart quotes + dashes to ASCII at canon-read time; these checks catch any that leak in from personas or templates.

### Cross-portfolio leak gate
Grep deliverable content against `admin/memory/portfolio-aliases.md` aliases. Reference by path - do NOT reproduce list inline (meta-hygiene paradox).

```bash
# Extract ALL aliases (multi-word supported) - strip the leading "- " marker
# State-tracked awk: only emit "- alias" lines AFTER the first "### slug" header,
# so format-rule bullets in the file's preamble are skipped.
# portfolio-aliases.md format: ### slug header, then "- alias" bullets per member.
mapfile -t ALIASES < <(awk '/^### /{in_block=1; next} in_block && /^- /{sub(/^- /,""); print}' admin/memory/portfolio-aliases.md)

for d in <run-folder>/deliverables/*.html; do
  for alias in "${ALIASES[@]}"; do
    [ -z "$alias" ] && continue
    [ "$alias" = "$subject_full_name" ] && continue   # self-reference is fine
    if grep -qiF -- "$alias" "$d"; then
      echo "LEAK: '$alias' found in $d"
    fi
  done
done

# Also check section headers (### slug) as alias source - the directory
# slug itself is implicit
mapfile -t SLUGS < <(sed -n 's/^### //p' admin/memory/portfolio-aliases.md)
for d in <run-folder>/deliverables/*.html; do
  for slug in "${SLUGS[@]}"; do
    [ -z "$slug" ] && continue
    [ "$slug" = "$subject_slug" ] && continue
    if grep -qiF -- "$slug" "$d"; then
      echo "LEAK: slug '$slug' found in $d"
    fi
  done
done
```

If any leak detected, HALT and surface to user. Do not deliver.

The Pineapple Protocol gate is NOT applied at this phase (no outbound communication). Pineapple fires downstream when user sends a deliverable.

## Phase 5 · Memory write + complete

1. Append one-line entry to `admin/memory/state.md`:
   `<date> | /shrink-wrap | <subject-slug> | scope=<scope> lens=<lens> | DECISION=<verdict> | folder=<run-folder>`
2. If subject is portfolio member, append to `HARBOR_portfolio/<member>/commitments.md`:
   `<date> | shrink-wrap analysis complete | <run-folder>/deliverables/01-decision-memo.html`
3. Return structured summary to invoker:

```json
{
  "skill": "shrink-wrap",
  "run_folder": "experiments/shrink-wrap/ato-automation-for-sbirs/",
  "scope": "full-methodology",
  "lens": ["federal"],
  "subject": "ato-automation-for-sbirs",
  "phase_durations_minutes": {"precheck": 4, "harvest": 6, "architect": 8, "risk_proof": 9, "build": 7, "replicate": 5, "synthesis": 3, "assembly": 4},
  "total_duration_minutes": 46,
  "research_calls_used": 4,
  "verdict": "proceed-with-conditions",
  "deliverable_paths": [...],
  "open_issues": [...],
  "memory_updated": true
}
```

## Constraints

- Auto-trigger: confirm gate ALWAYS first; never go directly to intake.
- Phase order is sequential per scope mask; do not run phases in parallel.
- Persona dispatches within a phase are parallel (single-message multi-Agent calls).
- Halt-and-surface conditions are NOT silently overridable; user must explicitly choose to proceed.
- Editorial lint + leak gate are BLOCKING; failed lint = halt, fix, retry.
- Cross-portfolio leak gate references portfolio-aliases.md BY PATH, never inline (meta-hygiene paradox rule).
- Run folder is hermetic: no writes outside `<run-folder>` and `admin/memory/state.md` + (if portfolio) `HARBOR_portfolio/<member>/commitments.md`.
- Pineapple Protocol does NOT fire here; deliverables stay internal until user sends.
- Smart quotes normalized to ASCII at extractor (Tier D); deliverables inherit this.
- Single-instrument scope skips Phase 2 + Phase 3 (no synthesis, no deliverable assembly).
- Pre-H gate failure (Ch 2 or Ch 3) requires explicit user confirmation to override; default is halt.

## Run-folder layout

```
<run-folder>/
├── 00-intake/
│   └── intake.json
├── 00-precheck/
│   ├── ch1-services-diagnostic.html
│   ├── ch2-no-delusion-gate.html
│   └── ch3-builder-operator.html
├── 01-harvest/
│   ├── ch4-ip-inventory.html
│   └── phase-summary.html
├── 02-architect/
│   ├── ch5-<cand>-s2p.html (one per candidate)
│   ├── ch6-hill-selection.html
│   └── phase-summary.html
├── 03-risk-proof/
│   ├── ch7-compliance-discipline.html
│   ├── ch8-authorization-route.html
│   ├── ch9-survivability-arch.html
│   └── phase-summary.html
├── 04-build/
│   ├── ch10-codify-expertise.html
│   ├── ch11-70-30.html
│   ├── ch12-boundaries.html
│   └── phase-summary.html
├── 05-replicate/
│   ├── ch13-pricing-model.html
│   ├── ch14-vehicle-stack.html  (or channel-stack.html)
│   └── phase-summary.html
├── 06-synthesis/
│   ├── gap-analyst-memo.html
│   ├── strategic-advisor-memo.html
│   ├── founder-investor-memo.html
│   └── cfo-memo.html
├── deliverables/
│   ├── 01-decision-memo.html
│   ├── 02-walkthrough.html
│   ├── 03-business-case.html
│   ├── 04-build-plan-software.html
│   ├── 05-build-plan-business.html
│   ├── 06-build-plan-compliance.html
│   ├── 07-product-spec.html
│   ├── 08-risk-register.html
│   └── 09-stage-gate-criteria.html
├── research/
│   └── by-<persona-slug>-<topic-slug>-<date>.html
└── gates/
    └── gate-<N>-<T>-review-<date>.html
```
