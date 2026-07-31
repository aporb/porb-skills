---
name: pr-review
description: Simulates a startup CTO's tiger team for PR review. Fetches a GitHub
  PR diff, runs 4 specialized persona subagents (Security Shepherd, Data Architect,
  Performance Hound, Quality Advocate) in parallel, synthesizes their findings through
  a CTO subagent, and posts structured comments back to the GitHub PR. Also reads
  linked GitHub issues and auto-detects repo conventions (framework, ORM, auth pattern)
  so each persona is repo-aware. Use when the user asks to review a PR, audit a pull
  request, run a tiger team review, or check a GitHub PR with persona-based analysis.
compatibility: Requires GitHub CLI (gh) authenticated. Run `gh auth status` to verify.
metadata:
  requires_bins:
  - gh
triggers:
- review: review this PR / review PR / PR review / code review
- pr: pull request / github.com/*/pull/
- tiger: tiger team / persona review / cto review
---

# PR Review — CTO's Tiger Team

Simulates a startup CTO's tiger team: 4 specialist personas review the PR in
parallel, then the CTO synthesizes their findings and posts structured comments
back to the GitHub PR. **Now repo-aware** — auto-detects framework, ORM, auth
pattern, and testing conventions so each persona knows what to look for. **Now
issue-aware** — fetches linked GitHub issues and checks that the PR actually solves
what was asked.

## Quick Check

Verify `gh` is authenticated before starting:

```bash
gh auth status
```

If not authenticated, run `gh auth login`.

## Workflow (5 Stages)

```
STAGE 0:   Fetch PR + extract linked issues
STAGE 0.5: Gather repo context (auto-detect framework, ORM, auth, tests)
STAGE 1:   Parallel persona reviews (with repo context + issues)
STAGE 2:   CTO synthesis (with repo context + issues)
STAGE 3:   Post comments to GitHub PR
```

---

### Stage 0: Fetch PR + Linked Issues

If the user provides a full PR URL (e.g. `https://github.com/owner/repo/pull/123`),
extract `owner/repo` and use `--repo owner/repo` on all `gh` commands. If only a
PR number is given, assume the current repo (`gh pr view` defaults to it).

```bash
# Step 1: Fetch PR metadata and diff
gh pr view <url-or-number> --json title,body,files,additions,deletions,baseRefName,headRefName,number,url
gh pr diff <url-or-number> > /tmp/pr-review-<pr-number>.diff
```

Extract from the JSON:
- `pr_title`, `pr_description`, `pr_number`, `pr_url`
- `files_changed`: comma-separated list of filenames
- `diff_size`: total additions + deletions (e.g. "+120 / -45")

**Important:** The PR diff is saved to `/tmp/pr-review-{pr_number}.diff`.
Subagents read it from this file — it is NOT embedded in task strings to avoid
enormous prompts for large PRs.

```bash
# Step 2: Extract linked issue references from PR body
# Look for patterns: Closes #123, Fixes #456, Resolves #789, or bare #NNN
# In the PR body text. Then fetch each issue:
gh issue view <issue-number> --json title,body,state,labels
```

Build a `linked_issues` text block for persona prompts. Example format:

```
Linked Issues:
- #123: "Add team invite endpoint" (open)
  Requirements: POST /api/teams/:id/invite, validate email, send invite email,
  check team membership. Edge cases: already-invited email, team at max members,
  non-member access.

- #456: "Fix invite email not sending on staging" (closed)
  This issue is closed — verify the fix is not regressed by this PR.
```

If no linked issues found:
```
Linked Issues: None detected. Review the PR on its own merits.
```

---

### Stage 0.5: Gather Repo Context

Read the context-gathering playbook at `references/context.md` (path relative to
this skill directory: `${CLAUDE_SKILL_DIR}/references/context.md`).

Follow the instructions in that file to:

1. **Check for `.pi/pr-review.json`** — optional per-repo config file. If it
   exists, use it. Skip auto-detection.
2. **Auto-detect framework and conventions** — lightweight `ls`/`grep` checks:
   - Framework: Gemfile+Rails → rails, package.json+next → nextjs, go.mod → go, etc.
   - ORM: db/schema.rb → ActiveRecord, prisma/schema.prisma → Prisma, alembic/ → Alembic
   - Auth pattern: app/policies/ → Pundit, authenticate_user! → Devise, auth() → NextAuth/Clerk
   - Test framework: spec/ → RSpec, __tests__/ → Jest, tests/ → Pytest
   - Migration tool: db/migrate/ → ActiveRecord, prisma/migrations/ → Prisma
   - CI: .github/workflows/ → GitHub Actions
3. **Build a `repo_context` text block.** Format:

```
Repo: framework=Rails, ORM=ActiveRecord, auth=Devise JWT, tests=RSpec, migrations=ActiveRecord
Auth indicators: authenticate_user! before_action on controllers
Policy pattern: app/policies/ (Pundit)
Migration pattern: db/migrate/*.rb
Test pattern: spec/ (RSpec + FactoryBot)
CI: GitHub Actions (.github/workflows/)
```

If detection returns all unknowns:
```
Repo context: not auto-detected. Apply generic checks.
```

The `repo_context` and `linked_issues` text blocks are injected into every
persona's task prompt. The persona reference files have `{repo_context}` and
`{linked_issues}` placeholders — replace them with the actual text.

---

### Stage 1: Parallel Persona Reviews

Launch 4 async fresh-context reviewer subagents simultaneously. Each receives
the PR diff, the repo context, the linked issues, and their persona-specific
lens.

Use `subagent()` with a parallel pattern. Each task:

1. **Read the persona reference prompt** from this skill's references/ directory.
2. **Read the shared schemas** from `references/schemas.md`.
3. **Review the PR diff** through their specific lens, using the repo context to
   target the right patterns and the linked issues to verify requirements.
4. **Return structured JSON** matching their schema.

{skill_dir} = `${CLAUDE_SKILL_DIR}`

```typescript
subagent({
  tasks: [
    {
      agent: "reviewer",
      task: "Read the Security Shepherd persona prompt from {skill_dir}/references/shepherd.md and the schemas from {skill_dir}/references/schemas.md. Read the PR diff from /tmp/pr-review-{pr_number}.diff. Then review this PR diff through the security lens.\n\n{repo_context}\n\n{linked_issues}\n\nPR Title: {pr_title}\nPR Description: {pr_description}\nFiles Changed: {files_changed}\n\nReturn structured JSON per the Security Shepherd schema.",
      output: "reviews/shepherd.json",
      outputMode: "file-only",
      reads: true
    },
    {
      agent: "reviewer",
      task: "Read the Data Architect persona prompt from {skill_dir}/references/architect.md and the schemas from {skill_dir}/references/schemas.md. Read the PR diff from /tmp/pr-review-{pr_number}.diff. Then review this PR diff through the data integrity lens.\n\n{repo_context}\n\n{linked_issues}\n\nPR Title: {pr_title}\nPR Description: {pr_description}\nFiles Changed: {files_changed}\n\nReturn structured JSON per the Data Architect schema.",
      output: "reviews/architect.json",
      outputMode: "file-only",
      reads: true
    },
    {
      agent: "reviewer",
      task: "Read the Performance Hound persona prompt from {skill_dir}/references/hound.md and the schemas from {skill_dir}/references/schemas.md. Read the PR diff from /tmp/pr-review-{pr_number}.diff. Then review this PR diff through the performance lens.\n\n{repo_context}\n\n{linked_issues}\n\nPR Title: {pr_title}\nPR Description: {pr_description}\nFiles Changed: {files_changed}\n\nReturn structured JSON per the Performance Hound schema.",
      output: "reviews/hound.json",
      outputMode: "file-only",
      reads: true
    },
    {
      agent: "reviewer",
      task: "Read the Quality Advocate persona prompt from {skill_dir}/references/advocate.md and the schemas from {skill_dir}/references/schemas.md. Read the PR diff from /tmp/pr-review-{pr_number}.diff. Then review this PR diff through the quality lens.\n\n{repo_context}\n\n{linked_issues}\n\nPR Title: {pr_title}\nPR Description: {pr_description}\nFiles Changed: {files_changed}\n\nReturn structured JSON per the Quality Advocate schema.",
      output: "reviews/advocate.json",
      outputMode: "file-only",
      reads: true
    }
  ],
  concurrency: 4,
  context: "fresh",
  async: true
})
```

The Advocate is the primary issue-alignment checker. It maps each issue
requirement to a test, flags missing coverage, and reports scope creep.

Check the async run with `subagent({ action: "status", id: "..." })`.

### Between Stages 1 and 2: Failure Handling

Before launching the CTO synthesizer, the parent MUST read each review JSON
file and handle failures:

```python
# Pseudocode for the parent orchestrator
persona_files = {
    "shepherd": "reviews/shepherd.json",
    "architect": "reviews/architect.json",
    "hound": "reviews/hound.json",
    "advocate": "reviews/advocate.json"
}

personas = {}
failed = []

for name, path in persona_files.items():
    try:
        with open(path) as f:
            data = json.load(f)
        if "_failed" in data or "_capped" in data:
            failed.append(name)
            personas[name] = '{"verdict": "no_output", "summary": f"Persona {name} failed to produce output"}'
        else:
            personas[name] = json.dumps(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        failed.append(name)
        personas[name] = '{"verdict": "no_output", "summary": f"Persona {name} error: {e}"}'

# Report failures to user:
if failed:
    print(f"⚠️ {len(failed)} persona(s) failed: {', '.join(failed)}")
    print("Continuing with degraded CTO synthesis.")
```

The CTO synthesizer receives all four persona outputs — including the degraded
`no_output` placeholders for failed personas. It accounts for missing reviews
in its verdict (e.g., "Architect failed — data review is incomplete; proceed
with caution or re-run").

---

### Stage 2: CTO Synthesis

After all 4 persona reviews complete, read each review JSON file. Launch a CTO
synthesizer subagent that receives all persona outputs + repo context + linked
issues:

```typescript
subagent({
  agent: "reviewer",
  task: "Read the CTO Synthesizer persona prompt from {skill_dir}/references/synthesizer.md and the schemas from {skill_dir}/references/schemas.md.\n\nHere are the four persona reviews:\n\nSecurity Shepherd: {shepherd_json}\n\nData Architect: {architect_json}\n\nPerformance Hound: {hound_json}\n\nQuality Advocate: {advocate_json}\n\n{repo_context}\n\n{linked_issues}\n\nPR Context:\nTitle: {pr_title}\nDescription: {pr_description}\nFiles: {files_changed}\nDiff Size: {diff_size} lines\n\nSynthesize these into a CTO verdict. Check that the PR actually solves the linked issues. Return structured JSON per the CTO Synthesizer schema. The synthesis_comment MUST be complete markdown ready to post as a GitHub comment.",
  output: "reviews/cto-synthesis.json",
  outputMode: "file-only",
  reads: true,
  context: "fresh",
  async: true
})
```

---

### Stage 3: Post Comments to GitHub

After the CTO synthesis completes, read each review JSON file. For each persona
and the CTO, derive the comment body from the JSON fields. Then post to GitHub.

**Deriving comment text from JSON schemas:**

| Comment Section | Derived From |
|-----------------|-------------|
| Persona verdict line | `{verdict}` field — map to emoji: approved→✅, approved_with_notes/conditions→⚠️, blocked→❌ |
| Risk level | `{risk_level}` field (low/medium/high) |
| Checked summary | Iterate `{checked}` object. Each key with `pass: true` → ✅, `pass: false` → ❌ with `note` |
| Findings | Iterate `{findings}` array. Format: severity emoji (critical→🔴, high→🟠, medium→🟡, low→🔵, info→⚪) + file:line + title + recommendation |
| Architect schema | Also include `{migrations}` and `{schema_changes}` arrays with reversible/backwards_compat flags |

**CTO synthesis comment:** Use the `synthesis_comment` field directly from
`cto-synthesis.json`. It is already complete markdown.

Post in this order (1-4 persona comments, then CTO). Use the
`{pr_number}` extracted in Stage 0 for all `gh pr comment` commands:

```bash
# 1. Security Shepherd — derive body from shepherd.json fields
gh pr comment {pr_number} --body "$(cat <<'EOF'
## 🔒 Security Shepherd — approved_with_notes

Risk level: **medium**

**Checks:**
- ✅ authn — JWT middleware on route
- ✅ authz — row-level team membership check
- ✅ input_validation — Zod schema on body
- ✅ secrets — clean
- ⚠️ surface_area — new endpoint exposes member emails (resolved: intentional)
- ✅ dependencies — no new packages
- ✅ data_exposure — email exposure is by design

**Findings:** none blocking

**Verdict:** ⚠️ APPROVED WITH NOTES
EOF
)"

# 2. Data Architect
gh pr comment {pr_number} --body "$(cat <<'EOF'
## 🗄️ Data Architect — approved_with_conditions

...
EOF
)"

# 3. Performance Hound
# 4. Quality Advocate
# 5. CTO Synthesis — use synthesis_comment directly
gh pr comment {pr_number} --body "$(cat <<'EOF'
{cto_synthesis_comment_from_json_file}
EOF
)"
```

---

### Stage 4: Report to User

After all comments are posted, report the verdict to the user:

```
📊 PR Review Complete — {pr_url}

Repo: {repo_context_summary}
Issues: {linked_issues_summary}

Shepherd:   {shepherd_verdict_emoji} {shepherd_verdict}
Architect:  {architect_verdict_emoji} {architect_verdict}
Hound:      {hound_verdict_emoji} {hound_verdict}
Advocate:   {advocate_verdict_emoji} {advocate_verdict}

Issue alignment: {issue_alignment_verdict}

CTO Decision: {go_decision}

All comments posted to the PR.
```

---

## Important Constraints

- **Lane discipline**: Persona subagents MUST NOT comment outside their domain.
  The persona prompts enforce this; validate the outputs.
- **Fresh context**: Every subagent runs in `context: "fresh"` mode. They see only
  the PR diff, repo context, linked issues, and their persona prompt — not the
  parent conversation.
- **No edits**: Persona subagents are review-only. They do not modify files.
- **One writer**: Only the parent posts comments to GitHub. Subagents never touch
  GitHub.
- **Failure isolation**: If one persona subagent fails or produces malformed JSON,
  continue with the others. Record the failure in the CTO synthesis. The brief
  always ships.
- **Async first**: Launch all subagents with `async: true`. The parent monitors and
  continues when results arrive.
- **Repo context is gathered once** at Stage 0.5 and injected into all personas.
  It does not change between persona calls.
- **Issue alignment is the Advocate's primary job.** The CTO synthesizer makes the
  final call but defers to the Advocate's traceability analysis.

## Persona Reference Files

Load these on-demand when launching subagents:

| Persona | Path |
|---------|------|
| Context Gathering (parent) | `references/context.md` |
| Security Shepherd | `references/shepherd.md` |
| Data Architect | `references/architect.md` |
| Performance Hound | `references/hound.md` |
| Quality Advocate | `references/advocate.md` |
| CTO Synthesizer | `references/synthesizer.md` |
| JSON Schemas (shared) | `references/schemas.md` |

All paths are relative to this skill directory.

## Example: End-to-End (with repo context + issues)

User says: "Review https://github.com/myorg/rails-api/pull/247"

1. Parent pi loads this skill (pr-review)
2. Parent runs `gh pr view 247 --json ...` → gets PR metadata
3. Parent runs `gh pr diff 247` → gets diff
4. Parent scans PR body for `Closes #187`, runs `gh issue view 187 --json ...` →
   linked issue with requirements and edge cases
5. Parent reads `references/context.md`, runs detection commands →
   Ruby/Rails, ActiveRecord, Devise JWT, RSpec, Pundit policies
6. Parent checks for `.pi/pr-review.json` — not found, uses auto-detected
7. Parent builds `repo_context` and `linked_issues` text blocks
8. Parent launches 4 parallel async reviewer subagents with:
   - Persona prompt (from references/)
   - Repo context (framework=Rails, ORM=ActiveRecord, auth=Devise, ...)
   - Linked issues (#187: "Add team invite endpoint")
   - PR diff
9. Parent waits for all 4 to complete (check status)
10. Parent reads review JSON files → extracts shepherd/architect/hound/advocate output
11. Parent launches CTO synthesizer subagent with all 4 reviews + repo context + issues
12. Parent reads cto-synthesis.json
13. Parent posts 5 comments to PR (4 persona + 1 CTO synthesis)
14. Parent reports verdict to user with issue alignment callout

The entire workflow is orchestrated by the parent pi session using the
`subagent()` tool from pi-subagents. The parent reads this skill file,
follows the sequence, and posts results back.
