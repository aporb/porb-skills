---
name: smart-commit
description: "Research git changes, group them logically, and commit with technically insightful conventional commit messages. No pushes."
version: 1.0.0
tags: [git, commit, conventional-commits, workflow]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Smart Commit

Analyze all working-tree changes, understand the WHY behind each one, group related changes into logical commits, and write technically insightful conventional commit messages. Never pushes.

## When to load this skill

- User says "commit", "smart commit", "commit my changes", or similar
- User wants to group and commit work in progress
- After completing a feature, fix, or refactor

## Cost-optimized variant (v3.1 — Haiku delegation pattern)

When the primary session is deep in context (>50K tokens) and you don't want to
pollute it with commit-message authoring, dispatch the message draft to a cheap
subagent via `delegate_task`:

```
delegate_task(
  profile="researcher",
  task="Read these staged diffs and write a conventional-commit message.\n\n"
       "git diff --cached output:\n{cached_diff}\n\n"
       "Rules: type(scope): summary. Body = WHY in 1-3 sentences. "
       "Footer: Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
  model="deepseek-v4-flash",
  max_iterations=3,
)
```

Flash-tier produces a serviceable message at ~5% of pro-tier cost. Use when
working through a multi-commit session where each commit is mostly mechanical
and the diff is self-explanatory.

## Workflow

This is a 4-step process. Execute each step thoroughly — do not skip research.

### Step 1: Research all changes

```bash
git status --short
git diff           # unstaged changes
git diff --cached  # staged changes
```

Read every changed file in full. For each file, understand:
- What changed (the diff)
- Why it changed (read surrounding code, check imports, trace callers)
- What subsystem it belongs to (which app, package, or concern)

Use `search_files` and `read_file` to trace context beyond the diff — understand motivation, not just mechanics.

### Step 2: Analyze and group

Group changes by logical subsystem and motivation. Rules:

- Changes to the same subsystem with the same purpose belong together
- A single file can be its own commit if the change is meaningfully distinct
- Cross-cutting changes (e.g., linting, type fixes across the repo) can group together if trivial
- Do NOT lump unrelated changes into one commit just to be done faster

Check recent commits for style reference:
```bash
git log --oneline -5
```

### Step 3: Commit each group

For each group, in order of dependency (foundational → dependent):

1. Stage only the relevant files:
   ```bash
   git add <file1> <file2> ...
   ```

2. Write a commit message with this exact format:
   ```
   type(scope): concise imperative description (max 72 chars)

   Body: 1-3 lines explaining the technical WHY — motivation, constraint,
   or consequence. Not a restatement of the diff. What problem does this
   solve? What would break without it?
   ```

3. Commit using a HEREDOC to preserve multiline formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): description

   Body explaining the why.
   EOF
   )"
   ```

**Valid types**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`

**Scope**: Use the workspace package name or app name from the monorepo (e.g., `runtime`, `control`, `knowledge`, `skills`, `db`, `auth`). Use `repo` for root-level changes.

### Step 4: Summarize

After all commits, show a summary table:

```
| Commit | Message |
|--------|---------|
| abc1234 | type(scope): description |
| def5678 | type(scope): description |
```

## Constraints (non-negotiable)

- **Do NOT push to remote** — under any circumstances
- **Do NOT add attribution lines** — no "Co-Authored-By", no "Claude", no "Hermes", no sign-off
- **If nothing to commit**, say so clearly and stop
- **Commit messages must be insightful** — explain motivation and impact, not just restate the diff
- **Use `git add <specific files>`** — never `git add -A` or `git add .` (prevents accidental inclusion)
- **Uncommitted files stay uncommitted** — if a file doesn't fit any group, leave it unstaged and mention it

## Pitfalls

### Empty commits
`git diff --cached` must show actual staged content before `git commit`. If `git add` doesn't stage anything (file already committed, or path wrong), git will reject the commit.

### HEREDOC variable expansion
Use `<<'EOF'` (quoted) to prevent `$variable` expansion inside the commit body. Unquoted `<<EOF` will expand shell variables and corrupt messages.

### Binary files
`git diff` on binary files (images, .db, .woff2) produces unreadable output. Use `git diff --stat` to identify them, then `read_file` to assess if they're new/modified. Include them in commits but don't try to "understand" the diff content.

### Pre-commit hooks
If the repo has pre-commit hooks (lint-staged, husky), they will run on `git commit`. If hooks fail, fix the issues and re-stage before re-committing.

### Hermes terminal watchdog blocks git commit
Hermes' terminal tool detects `git commit -m "..."` (and HEREDOC variants) as a long-lived server process and refuses to run them in foreground mode. This includes `git commit -m "$(cat <<'EOF'...)"`. **Workaround**:
1. Stage files in foreground: `git add <files>` (works fine)
2. Commit in background: use `background=true` with `notify_on_complete=true`
3. Poll completion with `process(action='poll', session_id='...')`
