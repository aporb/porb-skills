---
name: spec-driven-workflow
description: "OpenSpec-inspired artifact-driven workflow for all Hermes tasks. Use for any multi-step initiative. Applies to Kanban task decomposition, solo work, and multi-agent orchestration."
version: 1.0.0
metadata:
  hermes:
    tags: [workflow, spec, planning, kanban, openspec]
    related_skills: [kanban-orchestrator, kanban-worker, writing-plans]
tier: B
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Spec-Driven Artifact Workflow

Inspired by OpenSpec (https://github.com/Fission-AI/OpenSpec). Use this for ALL tasks that involve planning, building, or changing anything in the Hermes ecosystem. The default approach for anything more complex than a single tool call.

## Core Principles

1. **Artifacts, not phases** — proposal, specs, design, tasks. Create/update any time, not locked in order.
2. **Delta specs** — describe what's CHANGING, not restate the whole system.
3. **GIVEN/WHEN/THEN scenarios** — every requirement gets concrete, testable scenarios.
4. **Changes as folders** — each initiative is self-contained: PRD + spec + design + task checklist.
5. **Fluid iteration** — update artifacts during implementation when you learn something.
6. **Review gate** — no implementation without spec review approval.

## The Four Artifacts

### 1. Proposal (`proposal.md`)
Captures **intent**, **scope**, and **approach** at high level.

```markdown
# Proposal: [Title]

## Intent
Why are we doing this? What problem does it solve?

## Scope
In scope:
- Item 1
- Item 2

Out of scope:
- Item (future work)

## Approach
High-level strategy (2-3 sentences).
```

### 2. Specs (`specs/<domain>/spec.md`)
Behavior contract — **what** the system must do, NOT how.

```markdown
# [Domain] Specification

## Purpose
What this spec covers.

## Requirements

### Requirement: [Name]
The system SHALL [behavior].

#### Scenario: [Happy path]
- GIVEN [precondition]
- WHEN [action]
- THEN [expected outcome]
- AND [additional outcome]

#### Scenario: [Edge case]
- GIVEN [edge precondition]
- WHEN [action]
- THEN [expected error/behavior]
```

**RFC 2119 keywords**: MUST/SHALL (absolute), SHOULD (recommended), MAY (optional).

**Spec vs Design test**: If implementation can change without changing externally visible behavior, it does NOT belong in the spec.

### 3. Design (`design.md`)
Technical approach — **how** we'll build it.

```markdown
# Design: [Title]

## Technical Approach
Brief overview.

## Architecture Decisions
### Decision: [Name]
Choosing [X] over [Y] because:
- Reason 1
- Reason 2

## Data Flow
[Diagram or description]

## File Changes
- path/to/file (new/modified)
```

### 4. Tasks (`tasks.md`)
Implementation checklist with hierarchical numbering.

```markdown
# Tasks

## 1. [Phase Name]
- [ ] 1.1 [Task description]
- [ ] 1.2 [Task description]

## 2. [Phase Name]
- [ ] 2.1 [Task description]
```

## Delta Spec Pattern

For changes to existing systems, use ADDED/MODIFIED/REMOVED sections. Never restate the entire system.

## Kanban Task Graph Pattern

Standard 4-phase decomposition for any significant initiative:

```
Phase 1 - Research (parallel, researcher profile)
Phase 2 - PRDs and Specs (one per research task, pm profile)
Phase 3 - Review (one per spec, reviewer profile)
Phase 4 - Implement (gated on review approval)
```

## Standard Profile Roster

All profiles use deepseek-v4-pro via deepseek provider:

| Profile | Role |
|---------|------|
| researcher | Reads sources, gathers facts, writes findings |
| pm | Writes PRDs, specs, acceptance criteria |
| reviewer | Reviews specs, leaves findings, gates approval |
| backend-eng | Writes server-side code, implements features |
| ops | Runs scripts, manages services, configures tools |

Pre-flight for each profile:
- Model: deepseek-v4-pro via deepseek provider (`hermes -p <profile> config set model.provider deepseek && model.default deepseek-v4-pro`)
- DEEPSEEK_API_KEY and OPENROUTER_API_KEY in profile .env
- kanban-worker and spec-driven-workflow skills copied to profile skills dir
- Supabase RAG wired: memory.provider: supabase-rag in config.yaml, Supabase env vars (PGHOST/PGPORT/etc.) in .env, supabase-local-rag skill copied to profile skills dir. See `supabase-local-rag` skill for the batch-wire recipe.
- Smoke test: `hermes -p <profile> chat -q "hello" --quiet`

### ⚠️ PITFALL: Don't use broad sed to set memory.provider

When adding `provider: supabase-rag` for the memory section, a naive `sed 's/provider:.*/provider: supabase-rag/'` corrupts `model.provider` too, changing it from `deepseek` to `supabase-rag`. Symptoms: all workers crash immediately with "Unknown provider 'supabase-rag'". Fix: use Python to scope the replacement precisely, or add the `memory:` block only if missing rather than editing `provider:` globally. See `supabase-local-rag` skill for the full fix recipe.

## Workflow Rules

1. No implementation without spec review approval
2. Update artifacts during implementation when design changes
3. GIVEN/WHEN/THEN on every requirement (minimum one scenario)
4. Delta specs only (describe what's changing)
5. Research before spec (researcher gathers facts before pm writes)
6. Parallel where possible (research parallel, review parallel)

## When NOT to Use

Skip for: single tool calls, sub-5-call tasks, trivial config changes, emergency hotfixes. Use delegate_task or direct answer instead.

## Pitfalls

- Don't skip review — catches missing edge cases before implementation
- Don't put implementation details in specs — that's design.md
- Don't pre-create the full graph if shape depends on intermediate findings
- Profile isolation: workers need their own .env and skills. Test before dispatching.
- ⚠️ Commented-out `.env` keys look "not set" in `hermes status`. Always check for `# KEY_NAME=...` lines before assuming a key is absent. Uncomment with `sed`, don't echo a duplicate.
- ⚠️ Subagent timeouts (600s) hit BOTH file I/O AND web-heavy research. Bulk file creation AND research tasks with many web_search calls can both time out. The subagent's API calls count toward the timeout — 8+ web_search calls often hit 600s. Mitigation: (a) for research, prefer direct `web_search`/`web_extract` calls from the parent session where practical, (b) for bulk file creation, write files directly, (c) for subagent research, limit to 1-2 focused queries per task and set expectations that 600s may not be enough for broad research.
- ⚠️ `delegate_task` has `max_concurrent_children=3` — if you dispatch 4+ tasks, you'll get an error. Split into batches of 3 or fewer. This applies to `--tasks` arguments, not individual task context — one `delegate_task` call with 4 tasks will fail, even though each task is a separate subagent.
- ⚠️ Web search auto-fallback: `web_search` and `web_extract` now have a built-in fallback chain at the tool layer (firecrawl → serper → brave-free → tavily → perplexity for search; firecrawl → tavily for extract). On any failure, the tool transparently rolls to the next provider and cools down the failed one. Check `_meta.attempts` in the response to see what happened. Only when `success: false` AND `_meta.attempts` shows every chain provider failed should you escalate: (a) `browser` tool for direct navigation, (b) terminal `curl` to OpenRouter/Perplexity — see `references/perplexity-fallback.md`, (c) training knowledge for stable domains (law, tax basics), (d) locally-available documents on disk.
- Multi-spec decomposition: when a system has distinct components (infrastructure, orchestration, agents, integrations, deployment), create separate spec files under `specs/<component>.md` rather than one monolithic spec. Each gets its own Requirements + Scenarios sections. The design.md ties them together with cross-cutting architecture.
- **⚠️ Don't ship half a product.** When building something meant to be SOLD (not just used internally), the technical backbone isn't enough. The product is only complete when it includes: (a) credential collection wizard that tests connections live, (b) validation that blocks deployment on bad credentials, (c) personalized welcome package generator using real deployed values, (d) client intake form, (e) setup guides per credential type, and (f) operator SOP from payment to first daily briefing. See `references/product-repo-structure.md` for the full pattern. If the client would need to touch a terminal, manually edit a .env, or read API docs — it's not done.

## Configuration Interview Pattern

When the task requires user decisions about configuration (cron jobs, service setup, migration choices), use this structured interview format rather than guessing and getting it wrong:

– **10 questions maximum** per session — keeps it focused and respects user attention
– **A–D options** for every question — gives the user a decision scaffold, not an open-ended demand
– **Concise language** — no preamble, no justification bloat; each question is one line plus 4 option bullets
– **State decisions as they lock** — after each answer, confirm what was decided: "Q1: THE DAILY + X Engagement only ✓"
– **Final recap before execution** — after all 10, present a summary table so the user can correct anything before you act

Example:
```
Question 1 of 10 — Which cron jobs to bring to local?

– A) All 8 — replicate exactly
– B) Briefing/alerts only (THE DAILY, GovRadar, X Engagement)
– C) Utility jobs only (Repo Audit, vault-sync, EconPulse)
– D) None right now — I'll specify
```

This pattern is particularly useful for server-to-local migrations, cron job setup, and any situation where the user has existing production config you can't directly access.

## Reference: Product Repo Structure

When building a repo that IS the sellable product (deployment packages, agency-in-a-box, configuration-as-a-product), see `references/product-repo-structure.md` for the full layout pattern — OpenSpec artifacts + build scripts + configs + skills + sales collateral in one repo.

## Reference: Static Portfolio Site Pattern

When the task is "build a resume/portfolio site from a PDF," skip sub-agent delegation and execute directly. The pattern is fully documented in `references/static-portfolio-pattern.md` — extract with pdftotext → hand-write typed data file → template-driven Next.js components → `vercel --yes --prod`. This ~20-file project finishes faster with direct file writes than with sub-agent round-trips. Use the validation checklist in the reference as your pre-deployment gate.
