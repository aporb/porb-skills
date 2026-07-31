---
name: kanban
description: Hermes Kanban orchestrator and worker - decomposition, routing, multi-agent workflow
version: 1.0.0
author: Hermes Agent
license: MIT
platforms:
  - linux
  - macos
metadata:
  hermes:
    tags:
      - kanban
      - multi-agent
      - orchestration
      - workflow
tier: B
moat_test: TBD
---

# Hermes Kanban

Multi-agent task orchestration via Kanban board. Covers both orchestrator decomposition patterns and worker execution guidance.

---

## SECTION 1: Orchestrator - When to Use the Board

Create Kanban tasks when:

1. **Multiple specialists needed** — Research + analysis + writing
2. **Work should survive crash/restart** — Long-running or important
3. **User might want to interject** — Human-in-the-loop
4. **Multiple subtasks can run in parallel** — Fan-out for speed
5. **Review/iteration expected** — Reviewer profile loops on drafter output
6. **Audit trail matters** — Board rows persist in SQLite

If none apply — small one-shot reasoning task — use `delegate_task` or answer directly.

---

## SECTION 2: Orchestrator - Anti-Temptation Rules

Your job: **route, don't execute**

- **Do not execute the work yourself**
- **For any concrete task, create a Kanban task and assign it**
- **If no specialist fits, ask the user which profile to create**
- **Decompose, route, and summarize — that's the whole job**

---

## SECTION 3: Orchestrator - Standard Specialist Roster

Unless user's setup is customized, assume these exist:

| Profile | Does | Typical workspace |
|---------|-----|-------------------|
| `researcher` | Reads sources, gathers facts | `scratch` |
| `analyst` | Synthesizes, ranks, de-dupes | `scratch` |
| `writer` | Drafts prose in user's voice | `scratch` or `dir:` into vault |
| `reviewer` | Reads output, gates approval | `scratch` |
| `backend-eng` | Writes server-side code | `worktree` |
| `frontend-eng` | Writes client-side code | `worktree` |
| `ops` | Runs scripts, manages services | `dir:` into ops repo |
| `pm` | Writes specs, acceptance criteria | `scratch` |

---

## SECTION 4: Orchestrator - Decomposition Playbook

### Step 1: Understand the Goal

**Explore before asking.** If task involves codebase/repo, read structure, README, config files, and key source files BEFORE asking questions. Most onboarding questions are answered by the code.

### Step 2: Sketch the Task Graph

Draft graph out loud. Example for "Analyze Postgres migration":

```
T1  researcher        research: Postgres cost vs current
T2  researcher        research: Postgres performance vs current
T3  analyst           synthesize migration recommendation       parents: T1, T2
T4  writer            draft decision memo                       parents: T3
```

Show to user — let them correct before creating anything.

### Step 3: Create Tasks and Link

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="researcher",
    body="Compare estimated infrastructure costs, migration costs, and ongoing ops costs over 3 years."
)

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="researcher",
    body="Compare query latency, throughput, scaling at ~500GB, 10k QPS."
)

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="analyst",
    body="Read findings from T1 and T2. Produce 1-page recommendation with trade-offs.",
    parents=[t1, t2]
)

t4 = kanban_create(
    title="draft decision memo",
    assignee="writer",
    body="Turn analyst's recommendation into 2-page CTO memo.",
    parents=[t3]
)
```

`parents=[...]` gates promotion — children stay in `todo` until every parent reaches `done`.

### Step 4: Complete Your Own Task

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 researchers parallel, 1 analyst, 1 writer",
    metadata={"task_graph": {
        "T1": {"assignee": "researcher", "parents": []},
        "T2": {"assignee": "researcher", "parents": []},
        "T3": {"assignee": "analyst", "parents": ["T1", "T2"]},
        "T4": {"assignee": "writer", "parents": ["T3"]},
    }}
)
```

### Step 5: Report to User

Tell them what you created in plain prose:
> I've queued 4 tasks:
> - **T1** (researcher): cost comparison
> - **T2** (researcher): performance comparison, parallel with T1
> - **T3** (analyst): synthesizes T1 + T2
> - **T4** (writer): turns T3 into CTO memo

---

## SECTION 5: Common Patterns

**Fan-out + fan-in (research → synthesize):**
N `researcher` tasks with no parents, one `analyst` task with all as parents.

**Pipeline with gates:**
`pm → backend-eng → reviewer`. Each stage's `parents=[previous_task]`.

**Same-profile queue:**
50 tasks, all assigned to `translator`, no dependencies. Dispatcher serializes.

**Human-in-the-loop:**
Task can `kanban_block()` to wait for input. Dispatcher respawns after `/unblock`.

---

## SECTION 6: Worker - Workspace Handling

Your workspace kind determines how you work:

| Kind | What it is | How to work |
|------|-----------|-------------|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely; gets GC'd when archived |
| `dir:<path>` | Shared persistent directory | Other runs read what you write. Treat as long-lived state |
| `worktree` | Git worktree at resolved path | If `.git` doesn't exist, run `git worktree add <path> <branch>` first |

---

## SECTION 7: Worker - Good Summary + Metadata Shapes

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated"],
    }
)
```

**Research task:**
```python
kanban_complete(
    summary="3 libraries reviewed; vLLM wins on throughput, SGLang on latency",
    metadata={
        "sources_read": 12,
        "recommendation": "vLLM",
        "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72}
    }
)
```

**Review task:**
```python
kanban_complete(
    summary="reviewed PR #123; 2 blocking issues found",
    metadata={
        "pr_number": 123,
        "findings": [
            {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL"},
            {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF"}
        ],
        "approved": False
    }
)
```

---

## SECTION 8: Worker - Claiming Cards You Created

```python
# GOOD - capture return values
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF", assignee="web-worker")

kanban_complete(
    summary="Review done; spawned remediations",
    metadata={"pr_number": 123},
    created_cards=[c1["task_id"], c2["task_id"]]
)

# BAD - claiming phantom ids
kanban_complete(
    summary="Created cards t_a1b2c3d4, t_deadbeef",  # hallucinated
    created_cards=["t_a1b2c3d4", "t_deadbeef"]  # → gate rejects
)
```

Only list ids you captured from successful `kanban_create` return values.

---

## SECTION 9: Worker - Block Reasons That Get Answered Fast

Bad: `"stuck"` — human has no context.

Good: one sentence naming the specific decision you need:
```python
kanban_comment(task_id=os.environ["HERMES_KANBAN_TASK"], body="Full context here...")
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth)?")
```

---

## SECTION 10: Worker - Heartbeats Worth Sending

Good heartbeats name progress:
- `"epoch 12/50, loss 0.31"`
- `"scanned 1.2M/2.4M rows"`
- `"uploaded 47/120 videos"`

Bad: `"still working"`, empty notes, sub-second intervals. Every few minutes max; skip entirely for tasks under ~2 minutes.

---

## SECTION 11: Worker - Retry Scenarios

If you open the task and `kanban_show` shows `runs: [...]`, you're a retry. Check prior runs' `outcome`/`summary`/`error`:

- `outcome: "timed_out"` — hit `max_runtime_seconds`. Chunk the work.
- `outcome: "crashed"` — OOM or segfault. Reduce memory.
- `outcome: "spawn_failed"` + error — profile config issue. Ask human via `kanban_block`.
- `outcome: "reclaimed"` + summary: "task archived..." — operator archived under you. Check status.

---

## SECTION 12: Worker - Do NOT

- Call `delegate_task` as substitute for `kanban_create`. `delegate_task` is for short reasoning subtasks inside YOUR run.
- Modify files outside `$HERMES_KANBAN_WORKSPACE` unless task body says to.
- Create follow-up tasks assigned to yourself — assign to right specialist.
- Complete a task you didn't actually finish. Block it instead.

---

## SECTION 13: Pitfalls

### Orchestrator

**"hermes kanban swarm" requires --verifier and --synthesizer**
Both flags are required positional-ish arguments:
```bash
hermes kanban swarm "Goal" \
  --verifier reviewer \
  --synthesizer pm \
  --worker backend-eng:"Build API":api-testing
```

**Board switching doesn't persist**
`hermes kanban boards switch <slug>` only affects current shell. Use env var instead:
```bash
HERMES_KANBAN_BOARD=<slug> hermes kanban list
```

**Tasks cannot be moved between boards**
No `kanban move` command. If created on wrong board, archive and recreate. Always set `HERMES_KANBAN_BOARD=<slug>` before `kanban create`.

**Task creation on wrong board is silent failure**
Without `HERMES_KANBAN_BOARD=<slug>`, tasks land on current board (usually `default`). Fix: prefix every `kanban create` with the env var.
**Faux pas: asking questions you could answer by exploring repo**

Explore the codebase first (README, package.json, key source files). Only ask what code cannot tell you.

**Deeper variant for architecture / strategy work:** the right read-order is meta-docs FIRST, code SECOND. Before reading any `.py` / `.ts` / `.go`, read in this order:
1. `README.md`
2. Any `ARCHITECTURE.md` / `DESIGN.md` / `*_PLAN.md`
3. `TODO.md` / `ROADMAP.md` / deferred-items files
4. Most recent 20 commits (`git log --oneline -20`)
5. `.learnings/` if present — but verify it's authored reliability data, not auto-generated agent-failure logs (single-session STOP events = noise, not signal)
6. CI/CD config (`.github/workflows/`, deploy scripts)

This 5-10 minute sequence answers 60-80% of "what does this system do" and "what's already been hardened" before you spend tokens on code. Without it, downstream researchers / analysts / reviewers will re-discover what the maintainer already wrote down. See `architecture-exploration` skill for the full workflow.

**`delegate_task` model parameter ignored**
If workers crash with `invalid_request_error`, the dispatcher overrides your model. Pivot to `execute_code` for parallel work — slower but reliable.

### Worker

**Profile misconfiguration causes silent crash loops**
Workers crash immediately when:
- Skill not installed in profile's `skills/` directory. Fix: `cp -r ~/.hermes/skills/<path> ~/.hermes/profiles/<name>/skills/`
- Profile `.env` missing API keys. Fix: copy from `~/.hermes/.env`
- Model provider doesn't match credentials. Fix: `hermes -p <name> config set model.provider <provider>`
- Crash loop limit is 5 failures; after that auto-blocks.

**Skill resolver collision from nested duplicates**
If profile has skill in two places (e.g., `skills/devops/kanban-worker/kanban-worker/SKILL.md`), resolver refuses to pick. Delete nested directory:
```bash
rm -rf ~/.hermes/profiles/<name>/skills/devops/kanban-worker/kanban-worker
```

**Task state can change between dispatch and startup**
Between dispatch and your boot, task may have been blocked, reassigned, or archived. Always `kanban_show` first.

**Workspace may have stale artifacts**
`dir:` and `worktree` workspaces can have files from previous runs. Read comment thread for context.

---

## SECTION 14: Pre-Flight Profile Validation

Before dispatching to a profile, verify it can boot:

```bash
# Check model/provider
hermes profile show <name> | grep "Model:"

# Verify API key exists
grep -c "DEEPSEEK_API_KEY" ~/.hermes/profiles/<name>/.env  # must be ≥1

# Smoke-test: can profile answer?
hermes -p <name> chat -q "hello" --quiet

# Verify skill exists in profile (NOT just in default profile)
ls ~/.hermes/profiles/<name>/skills/<category>/<skill>/
```

If missing skill:
```bash
cp -r ~/.hermes/skills/<category>/<skill> ~/.hermes/profiles/<name>/skills/<category>/
```

---

## SECTION 15: CLI Fallback

Every tool has CLI equivalent:
- `kanban_show` ↔ `hermes kanban show <id> --json`
- `kanban_complete` ↔ `hermes kanban complete <id> --summary "..."`
- `kanban_block` ↔ `hermes kanban block <id> "reason"`
- `kanban_create` ↔ `hermes kanban create "title" --assignee <profile>`

Use tools from inside agent; CLI exists for human operators.

---

## Summary Table

| Role | Focus | Key Actions |
|------|-------|-------------|
| Orchestrator | Decompose, route, summarize | `kanban_create`, `kanban_complete` with task_graph |
| Worker | Execute in workspace, report | `kanban_show`, work in `$HERMES_KANBAN_WORKSPACE`, `kanban_complete` |
| Both | Follow anti-temptation rules | Don't do other role's job |

---

## Quick Start

**As Orchestrator:**
1. Understand goal (explore first, then ask if needed)
2. Sketch task graph, show to user
3. Create tasks with `kanban_create`, link with `parents=[...]`
4. Complete with `kanban_complete(summary=..., metadata={"task_graph": {...}})`
5. Report to user

**As Worker:**
1. `kanban_show` — check status, see if you're a retry
2. Read task body, understand what workspace kind you have
3. Execute work in `$HERMES_KANBAN_WORKSPACE`
4. Send heartbeats for long tasks: `kanban_heartbeat(note="progress...")`
5. If blocked: `kanban_comment(...)` + `kanban_block(reason="one-sentence question")`
6. When done: `kanban_complete(summary=..., metadata={...}, created_cards=[...])`