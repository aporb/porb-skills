---
name: agentic-swe-evaluation
description: "Analyze and interpret output from agentic SWE evaluation frameworks (datacurve-ai/pier, SWE-bench, Terminal-Bench, NL2Repo). Read job/trial/reward structures, parse agent trajectories for quality signals, diagnose failures (rate limits, submission errors, test failures), and compile results into briefings."
version: 1.0.0
tags: [evaluation, swebench, agentic-coding, pier, mini-swe-agent, llm-benchmarking]
tier: B
---

# Agentic SWE Evaluation Analysis

## What This Covers

Agentic SWE evaluation frameworks test whether an LLM can autonomously solve
real-world software engineering tasks (feature implementation, bug fixes) inside
a sandboxed environment, then verify the solution against hidden test suites.
This is fundamentally different from academic benchmarks (MMLU, GSM8K) — the
model must explore a codebase, write code across multiple files, debug iteratively,
and submit. See `evaluating-llms-harness` for academic benchmark evaluation.

**Frameworks in this class:**
- `datacurve-ai/pier` — Docker-sandboxed agent evaluator (what we use)
- SWE-bench / SWE-bench Verified / SWE-bench Pro
- Terminal-Bench 2.0
- NL2Repo
- Aider polyglot

## When to Load This Skill

- User asks you to review, analyze, or summarize evaluation results from a SWE-bench-style harness
- You need to diagnose why tasks failed (rate limits vs. model quality vs. infrastructure)
- You need to compile evaluation results into an HTML briefing or report
- User is setting up or configuring a new evaluation run and needs guidance on parameters

## How to Analyze pier Evaluation Output

### Directory Structure

```
<project-root>/
├── deep-swe/                    # Dataset (git repo: datacurve-ai/deep-swe)
│   └── tasks/                   # 116 task directories
│       └── <task-name>/
│           ├── task.toml        # Task metadata (language, repo, category, timeouts)
│           ├── instruction.md   # The task prompt given to the agent
│           ├── tests/
│           │   ├── test.sh      # Test runner script
│           │   └── test.patch   # Hidden test code applied during verification
│           ├── solution/
│           │   ├── solve.sh
│           │   └── solution.patch
│           └── environment/
│               └── Dockerfile
├── jobs/                        # Evaluation runs
│   └── <YYYY-MM-DD__HH-MM-SS>/  # One per run
│       ├── config.json          # Run configuration
│       ├── result.json          # Aggregate results (READ THIS FIRST)
│       ├── lock.json
│       ├── job.log
│       └── <task-name>__<id>/   # One per task trial
│           ├── config.json      # Per-task config (model, env vars)
│           ├── trial.log        # Execution log
│           ├── exception.txt    # Present if task errored (READ for failure mode)
│           ├── agent/
│           │   ├── mini-swe-agent.txt           # Full agent output log
│           │   └── mini-swe-agent.trajectory.json # Structured trajectory
│           ├── verifier/
│           │   ├── reward.txt    # "0" or "1" — binary pass/fail
│           │   └── test-stdout.txt  # Full test output (baseline + new tests)
│           └── artifacts/
│               └── model.patch   # The diff the agent produced
```

### Analysis Workflow

**Step 1 — Read result.json for the aggregate picture.**

Key fields:
- `stats.n_completed_trials` / `stats.n_errored_trials` — how many ran vs. crashed
- `stats.evals.<eval-name>.metrics[0].mean` — the pass rate (0.0–1.0)
- `stats.evals.<eval-name>.reward_stats.reward` — maps reward values to task lists
- `stats.evals.<eval-name>.exception_stats` — maps exception types to task lists
- `stats.n_input_tokens` / `stats.n_output_tokens` — token economics
- `finished_at: null` means the job is still running (check `n_running_trials`)

**Step 2 — Classify failures into three buckets.**

1. **Rate limit / API errors** (`RateLimitError`, `NonZeroAgentExitCodeError`):
   Infrastructure problem, not model quality. Check `exception.txt` and
   `agent/mini-swe-agent.trajectory.json` → `info.exit_status`. Fix: reduce
   `n_concurrent_trials`, use standalone API instead of Coding Plan.

2. **Submitted but failed verification** (`exit_status: "Submitted"`, reward 0):
   Model wrote code but it didn't pass hidden tests. Read
   `verifier/test-stdout.txt` to see exactly which tests failed and why.
   Read `artifacts/model.patch` to see what the model produced.

3. **Agent loop / timeout** (`AgentTimeoutError`): Model got stuck in a loop
   or exceeded the timeout. Check step count in trajectory.

**Step 3 — Parse agent trajectories for quality signals.**

From `mini-swe-agent.trajectory.json`:
- `info.model_stats.api_calls` — number of model invocations (agent steps)
- `info.exit_status` — `"Submitted"`, `"RateLimitError"`, `"CancelledError"`
- `info.model_stats.instance_cost` — cost (often $0 on Coding Plan)
- `messages` array length — total messages exchanged

From `mini-swe-agent.txt` (grep for `"mini-swe-agent (step"`):
- Count of steps = number of agent actions
- Read last ~20 lines to see how the agent terminated
- Look for `COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT` — the submission signal

**Step 4 — Read test output for near-miss analysis.**

`verifier/test-stdout.txt` shows:
- Step 1: Captures model.patch
- Step 2: Resets + applies hidden test.patch
- Step 3: Runs baseline tests (should all pass)
- Step 4: Runs new tests (this is the pass/fail gate)

A model that passes 17/18 new tests is qualitatively different from one that
passes 0/18. The near-miss pattern is a strong quality signal — read the
specific assertion failures to understand what the model got close on.

**Step 5 — Check task metadata for context.**

From `task.toml`:
- `task.language` — python, typescript, go, rust, javascript
- `task.category` — feature_request, bugfix, enhancement
- `task.repository_url` — which real-world repo
- `verifier.timeout_sec` / `agent.timeout_sec` — time constraints
- `environment.allow_internet` — usually false (sandboxed)

### Compiling Results into a Briefing

When asked to add evaluation results to an existing report or create one:
- Use stat cards for headline numbers (pass rate, tokens consumed, max steps, cost)
- Per-task breakdown table: task name, language, API calls, patch size, outcome
- Callout boxes for key findings (rate limiting patterns, quality signals)
- Token economics section (input/cache/output tokens, cost comparison)
- Timeline of test runs with status
- "What happens next" section with planned follow-up runs

## Configuration Reference (pier config.json)

Key fields in the run-level `config.json`:
- `n_concurrent_trials` — parallel tasks (reduce if hitting rate limits)
- `agents[0].model_name` — e.g. `anthropic/glm-5.2`
- `agents[0].env` — API endpoint config (e.g. `ANTHROPIC_API_BASE`)
- `datasets[0].path` — path to task dataset
- `datasets[0].n_tasks` — number of tasks to sample
- `datasets[0].task_names` — glob patterns for specific task selection
- `retry.max_retries` — retry count for failed trials
- `retry.include_exceptions` / `retry.exclude_exceptions` — which errors to retry

## Common Pitfalls

- **Rate limits mask true model quality.** Always separate "errored" from
  "failed verification" before drawing conclusions about model capability.
  A 0% pass rate where 50% of tasks died on rate limits tells you nothing
  about the model's coding ability.
- **Coding Plan throttling is aggressive.** Z.ai's GLM Coding Plan rate-limits
  heavily under concurrent load. Reduce `n_concurrent_trials` to 1 for retries.
  Standalone API (when available) should have different limits.
- **Submission command failures.** The agent's final `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`
  can fail (exit code -1) but the patch is still in the working tree. Verification
  runs against whatever is in the tree, not against successful submission.
- **Trajectory JSON structure varies by agent version.** `mini-swe-agent` v2.4.1
  uses `info.model_stats.api_calls` for step count. Don't assume from `environment`
  array (can be empty in some versions). Grep the text log for step markers instead.

## Reference Files

- `references/datacurve-pier-output-structure.md` — detailed field reference for pier output files, with the GLM-5.2 evaluation as a worked example
