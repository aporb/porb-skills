---
name: architecture-exploration
description: Explore an unfamiliar codebase and produce a future-architecture document with honest findings, options, tradeoffs, a recommended path, migration plan, and open questions. Use when a user asks "look at this repo and tell me what we should do about X" or "should we keep the current stack or redesign?" before any implementation. Distinct from writing-plans (which assumes you already know what to build) and gstack-spec (which produces a GitHub-issue spec, not a strategy doc).
version: 1.0.0
metadata:
  hermes:
    tags: [architecture, exploration, planning, audit, codebase, strategy, redesign]
    related_skills: [plan, writing-plans, spec-driven-workflow, subagent-driven-development, pi-agent, kanban, github-pr-workflow, requesting-code-review]
tier: A
---

# Architecture Exploration

For the user request pattern: *"explore this repo, understand it deeply, tell me what we should do."* The deliverable is a future-architecture document — NOT code, NOT a spec, NOT an implementation plan. Those come later, after the user answers the open questions.

## When to use this skill

Trigger phrases (user explicitly asking):
- "Explore this repo and tell me if we should rebuild"
- "Should we keep the current stack or redesign?"
- "What would a future architecture look like?"
- "Audit the current architecture and recommend changes"
- "Help me understand this codebase and what to do about X"

**Do NOT use this skill for:**
- Already-scoped feature work → `writing-plans`
- Turning vague intent into a GitHub issue → `gstack-spec`
- Writing a short tactical plan → `plan`
- Implementing code → `subagent-driven-development`

### Mandatory load: if the user said "explore this repo," load this skill

If the user message contains words like **explore / audit / look at this repo / should we rebuild / future architecture / what should we do about this codebase**, **load this skill before reading any code**. The skill encodes the meta-doc-first discipline that prevents re-discovering what the maintainer already documented, the `.learnings/`-is-often-auto-generated trap, and the "don't swarm a codebase you haven't read" rule. Skipping the load costs ~30 min of avoidable re-discovery and produces generic essays instead of cited findings.

If you're tempted to skip because "I already know how to read a repo," read Step 2 anyway — the maintainer's `*_PLAN.md` files, `TODO.md`, and recent commit chain are the single highest-signal data sources, and reading them first is the difference between a useful doc and a generic one.

## Core principles

### 1. Explore BEFORE you delegate

If the user says "use pi/GPT-5.5 for the coding work," they're describing the *implementation phase*. The exploration phase is different: it requires reading many small files (plans, workflows, scripts, configs, LEARNINGS, code headers) and stitching together a mental model.

**Rule:** Read the codebase directly in the orchestrator thread. Do not spawn a subagent swarm for the initial mapping. Reserve subagents (pi or otherwise) for tasks that benefit from a fresh context window — delta analysis, second opinions, long-running deep dives, or parallel fact-gathering on distinct topics.

**Why:** A 5-agent swarm on a codebase it hasn't seen will produce generic "self-hosted vs cloud" essays. The value of an architecture doc comes from citing *specific files, line numbers, and commit chains* in the current system — which requires you to read them yourself.

### 2. Read the repo's docs about itself FIRST

Most non-trivial repos already have:
- `README.md` — usually accurate if recent
- `ARCHITECTURE.md` / `DESIGN.md` / `docs/` — the maintainer's own thinking
- `TODO.md` / `ROADMAP.md` — what's planned and what's deferred
- `.learnings/LEARNINGS.md` — sometimes real, sometimes auto-generated noise (check the timestamps and patterns)
- `CHANGELOG.md` / commit history — what changed recently and why
- Existing implementation plans (e.g., `DASHBOARD_PLAN.md`, `DEPLOYMENT_PLAN.md`)

**Rule:** Read these BEFORE forming your own analysis. They will answer 60-80% of "what does this system do" and "what's been tried." They will also tell you what's already been hardened (so your "fragility" claims don't repeat work already done).

**Pitfall:** `.learnings/` directories sometimes contain auto-generated agent failure logs, not authored learnings. Check the file format — if entries are timestamped STOP events from a single session, that's not reliability data on the system under study.

### 3. Grade the current state with confidence intervals

A future-architecture doc for a system that **already works well** is fundamentally different from one for a system being designed from scratch. Most architecture essays assume the latter. If the system has been recently hardened (look at the last 10-20 commits, look for PRs labeled `fix/*` or `chore/*`), your job is to:

1. Identify what's actually still fragile (with evidence).
2. Identify what was just fixed and stop proposing the same fix.
3. Quantify confidence on each claim ("85% that X is a real bug", not "X is definitely a bug").

**Rule:** For each "fragility point" in your doc, cite the specific file path, line, or commit that supports the claim. If you can't cite it, hedge or drop it.

### 4. Don't assume the user wants to rewrite

Most architecture-exploration requests are *not* "rebuild from scratch." They're "tell me whether we should change anything." The honest answer is often "the system is mostly fine; here's the one or two things actually worth fixing."

**Rule:** Always include a "minimal change" option in your options matrix (often called Option A or "harden in place"). The most common correct recommendation is the option that changes the least while addressing the most concrete bugs.

### 5. Surface the unknowns as numbered questions

You will discover unknowns that the codebase cannot answer: deployment details, secrets, user distribution, infrastructure preferences, business priorities. Don't guess.

**Rule:** Put unknowns in a dedicated "Open Questions" section, numbered Q1, Q2, ... Each question should be specific and answerable. Resist the urge to recommend without knowing — implementation can wait.

## The process

### Step 1: Set up

- Clone the repo (or read it in place).
- Confirm git history is reachable (`git log --oneline -20`).
- Identify the user's preferred branch strategy (most teams want a working branch for exploration, not main).

### Step 2: Read the meta-documents

Before reading code, read in this order:
1. `README.md`
2. Any `ARCHITECTURE.md`, `DESIGN.md`, `*_PLAN.md` files
3. `TODO.md`, `ROADMAP.md`, deferred-items files
4. The most recent 20 commits (`git log --oneline -20`)
5. `.learnings/LEARNINGS.md` if it exists — *verify it's authored, not auto-generated*
6. CI/CD config (`.github/workflows/`, `.gitlab-ci.yml`, etc.)

This takes 5-10 minutes and gives you 60-80% of the mental model. Without it, you waste tokens re-discovering what the maintainer already wrote down.

### Step 3: Read the key code paths

Now go deeper. Read:
- The main entry points (e.g., `pipeline/run_brief.py`, `src/app.py`)
- The LLM / AI / provider seam if any
- The database / persistence layer
- The API routes / endpoints
- The deployment / runbook scripts
- The authentication / secrets handling

Don't read tests exhaustively. Sample the top of test files to see what's covered. Tests tell you what the maintainer thought was risky.

### Step 4: Form the fragility hypothesis

List concrete fragility points with evidence (file:line or commit). For each, give a confidence interval. Be honest about what you don't know.

**Common fragility patterns to look for:**
- Ephemeral filesystem writes in serverless / free-tier contexts (SQLite in `/tmp`, log files)
- Optimistic-locking races in concurrent commit APIs
- Single-region / single-machine failure modes
- Missing observability (no structured logs, no alerting)
- Secrets in multiple stores with no rotation path
- Single-provider AI / service dependencies with no failover
- Missing test coverage on the deploy path

**Separate the strong claims from the weak ones.** Claims that imply a real production bug ("feedback votes are being wiped on every deploy") need an empirical verification step before they get written into a migration plan. The doc should mark each fragility claim with a confidence interval AND a flag for "needs empirical verification before fix." Claims that survive verification become Phase 1 work; claims that don't either get demoted to "documented risk" or dropped.

### Step 5: Build the options matrix

Present 3-5 concrete options, scoped to "what could plausibly change about how this runs." Include at least one minimal-change option and one ambitious option. For each, list tradeoffs on:
- Time to ship
- Reversibility
- Operational toil (ongoing cost)
- Reliability delta
- Cost delta
- Risk of regression

### Step 6: Recommend with a phase plan

Pick a recommendation. Most often it's "the minimal option for the next 1-4 weeks, with a decision gate before committing to anything bigger." Implementation is gated on the open questions in Step 7.

### Step 7: List open questions

Specific, answerable questions. Each should be one the codebase *cannot* answer. Examples:
- "What's the Vercel plan (Hobby / Pro / Enterprise)?"
- "How many active users hit the dashboard, and from where?"
- "What's the AI provider budget for the campaign?"

### Step 8: Write the doc, commit, push

The deliverable is a markdown document in the user's preferred location (often `docs/future/` in the repo). Commit it on a working branch. Do NOT merge to main. Push the branch and report the branch name, files committed, summary, and open questions.

## Document structure

A future-architecture doc typically has 10-12 sections:

1. Current repo and system understanding
2. Current deployment and automation flow
3. Known or likely fragility points (with confidence intervals)
4. Architecture options (3-5)
5. Tradeoffs for each option (matrix form)
6. Recommended future architecture
7. Migration path from current state to recommended state
8. Open questions for the user
9. Risks and assumptions
10. Proposed implementation roadmap
11. Suggested Kanban breakdown for future execution

Two-document pattern works well:
- `docs/future/README.md` — one-page index, working assumptions, how to read
- `docs/future/architecture.md` — the full doc

Avoid the multi-file spec-driven-workflow artifact set for a brainstorm. That's overkill for a strategy doc and adds navigation cost.

## Pitfalls

### Pitfall: Spawning a subagent swarm for initial codebase mapping
The first 30-60 minutes of codebase archaeology is best done in the orchestrator thread. Subagents add latency without adding insight on tasks where the entire context fits in your head.

### Pitfall: Treating `.learnings/` as authoritative
Some agents auto-generate failure logs into `.learnings/`. Look at the timestamps — if they're all from a single session and all STOP events, that's not a "what the maintainer learned" document. Read it as a hint to look at the actual code, not as evidence about the system.

### Pitfall: Generic "Vercel vs Docker" essays
The user has usually already considered the obvious architectural questions. Your value is in citing *specific* code paths, configs, and recent commits — not in enumerating tradeoffs they could have read in any blog post.

### Pitfall: Recommending a rewrite when the system works
If the recent commit history shows deliberate hardening (multiple `fix/reliability*`, `fix/safety*`, `fix/race*` PRs), the system is being actively maintained against its failure modes. A wholesale rewrite loses that institutional knowledge.

### Pitfall: Long flat lists of files-read
If you read 30+ files, an "Appendix: files read" is fine. But put it at the bottom and keep it short. The body of the doc should be organized by *finding*, not by *file*.

### Pitfall: Implementing before the open questions are answered
Architecture exploration is exploratory. The doc is the deliverable. Do not write code, do not merge to main, do not push implementation PRs. Wait for the user to answer the open questions.

### Pitfall: Vague option names
"A" "B" "C" are fine if labeled ("harden in place", "dashboard to VPS", "full self-host"). "Option 1", "Option 2" without labels forces the reader to remember which is which.

### Pitfall: Forgetting to push the branch
The user can't read your doc if it's only in your local clone. After committing, push to the remote and verify (`git ls-remote --heads origin <branch-name>`).

## Verification

Before reporting "done," verify:
- `git log --oneline -3` shows your commit on the working branch
- `git ls-remote --heads origin <branch>` shows the branch on the remote
- The doc is in the location the user asked for (often `docs/future/`)
- The doc has the 11 sections above (or whatever structure they specified)
- The doc has a "Open Questions" section
- The branch is NOT merged to main
- The final report to the user includes: branch name, files committed, key findings, recommended direction, and the open questions