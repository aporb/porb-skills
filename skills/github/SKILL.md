---
name: github
description: Complete GitHub workflow - authentication, PRs, issues, code review, repository management
version: 1.0.0
author: Hermes Agent
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags:
      - GitHub
      - Git
      - Pull-Requests
      - Issues
      - Code-Review
      - CI/CD
      - Repositories
tier: A
moat_test: TBD
---

# GitHub Workflow

Complete GitHub workflow covering authentication, pull requests, issues, code review, and repository management. Each section shows the `gh` CLI way first, then the `git` + `curl` fallback.

## Prerequisites and Auth Setup

Before any GitHub workflow, ensure authentication is configured.

### Detection Flow

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated -> use `gh` for everything
2. If `gh` is installed but not authenticated -> use "gh auth" method
3. If `gh` is not installed -> use "git-only" method

---

## SECTION 1: Authentication Setup

### Git-Only Authentication (No gh, No sudo)

**HTTPS with Personal Access Token (Recommended)**

Create token at: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Scopes: `repo`, `workflow`, `read:org` (if org repos)

```bash
# Set up credential helper
git config --global credential.helper store

# Test operation - prompts for credentials
git ls-remote https://github.com/<username>/<repo>.git

# Configure git identity
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

**SSH Key Authentication**

```bash
# Generate ed25519 key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Add to GitHub at: https://github.com/settings/keys
cat ~/.ssh/id_ed25519.pub

# Test connection
ssh -T git@github.com

# Rewrite HTTPS URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### gh CLI Authentication

```bash
# Interactive browser login
gh auth login

# Token-based login
echo "<TOKEN>" | gh auth login --with-token
gh auth setup-git

# Verify
gh auth status
```

---

## SECTION 2: Repository Management

### Cloning

```bash
# Standard clone
git clone https://github.com/owner/repo.git

# Shallow clone (faster)
git clone --depth 1 https://github.com/owner/repo.git

# Clone specific branch
git clone --branch develop https://github.com/owner/repo.git

# With gh
gh repo clone owner/repo -- --depth 1
```

### Creating Repositories

**With gh:**
```bash
gh repo create my-project --public --clone
gh repo create my-project --private --description "Description" --license MIT
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name": "my-project", "private": false, "auto_init": true}'
```

### Forking

```bash
# With gh
gh repo fork owner/repo --clone

# Manual
git clone https://github.com/$USER/repo.git
cd repo
git remote add upstream https://github.com/owner/repo.git
```

### Keeping Fork Synced

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## SECTION 3: Pull Request Workflow

### Branch Creation

```bash
git checkout main && git pull origin main
git checkout -b feat/add-feature
```

Naming conventions:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

### Committing

```bash
git add files...
git commit -m "feat: add feature

Description of what changed.

- Added endpoint
- Added tests
"
```

### Pushing and Creating PR

```bash
git push -u origin HEAD
```

**With gh:**
```bash
gh pr create \
  --title "feat: add feature" \
  --body "Summary of changes

Closes #42"
```

**With curl:**
```bash
BRANCH=$(git branch --show-current)
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{\"title\": \"feat: add feature\", \"head\": \"$BRANCH\", \"base\": \"main\"}"
```

### Monitoring CI

```bash
# With gh
gh pr checks
gh pr checks --watch

# With curl
SHA=$(git rev-parse HEAD)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status
```

### Merging

```bash
# With gh - squash merge
gh pr merge --squash --delete-branch

# With curl - squash merge
PR_NUMBER=123
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d '{"merge_method": "squash"}'

# Delete branch
git push origin --delete $BRANCH
git checkout main && git pull origin main
git branch -d $BRANCH
```

---

## SECTION 4: Issues Management

### Viewing Issues

```bash
# With gh
gh issue list
gh issue list --state open --label "bug"
gh issue view 42

# With curl
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open"
```

### Creating Issues

```bash
# With gh
gh issue create \
  --title "Bug title" \
  --body "## Description

Steps to reproduce:
1. Step one
2. Step two

Expected: X
Actual: Y" \
  --label "bug" \
  --assignee username

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{"title": "Bug title", "body": "Description", "labels": ["bug"]}'
```

### Managing Issues

```bash
# Add labels
gh issue edit 42 --add-label "priority:high,bug"

# Assign
gh issue edit 42 --add-assignee username

# Comment
gh issue comment 42 --body "Working on this"

# Close
gh issue close 42
gh issue reopen 42
```

---

## SECTION 5: Code Review

### Reviewing Local Changes

```bash
# Get diff
git diff main...HEAD
git diff main...HEAD --stat
git diff main...HEAD --name-only

# Check for issues
git diff main...HEAD | grep -n "print(\|console\.log\|TODO"
git diff main...HEAD | grep -in "password\|secret"
```

### Reviewing PRs

```bash
# View PR
gh pr view 123
gh pr diff 123

# Checkout locally
gh pr checkout 123
git diff main...pr-123
```

### Submitting Reviews

```bash
# Approve
gh pr review 123 --approve --body "LGTM!"

# Request changes
gh pr review 123 --request-changes --body "See inline comments"

# Comment only
gh pr review 123 --comment --body "Some suggestions"
```

**With curl - multi-comment review:**

```bash
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123 \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123/reviews \
  -d '{
    "commit_id": "'"$HEAD_SHA"'",
    "event": "COMMENT",
    "body": "Review summary",
    "comments": [
      {"path": "src/file.py", "line": 45, "body": "Suggestion"}
    ]
  }'
```

### Review Checklist

- **Correctness**: Does code do what it claims? Edge cases?
- **Security**: No secrets, input validation, no injection attacks
- **Quality**: Clear naming, focused functions, DRY
- **Testing**: New paths tested, happy path + errors covered

---

## SECTION 6: GitHub Actions

```bash
# With gh
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>

# With curl
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10"
```

### Secrets

```bash
# With gh (simpler)
gh secret set API_KEY --body "value"
gh secret list
gh secret delete API_KEY
```

---

## SECTION 7: Releases

```bash
# With gh
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease
gh release list
gh release download v1.0.0 --dir ./downloads

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name": "v1.0.0", "name": "v1.0.0", "generate_release_notes": true}'
```

---

## Pitfalls

**git push hangs on macOS with osxkeychain**

When osxkeychain credential helper can't complete auth, git push hangs indefinitely.

**Workaround - use GitHub API:**
```bash
gh api repos/OWNER/REPO/contents/PATH -X PUT \
  -f message="Commit" \
  -f content="$(base64 -i file)" \
  -f branch="main"
```

---

## Quick Reference

| Action | gh | git + curl |
|--------|-----|-----------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name` | `curl POST /user/repos` |
| Create PR | `gh pr create --title "..."` | `curl POST /repos/o/r/pulls` |
| List issues | `gh issue list` | `curl GET /repos/o/r/issues` |
| Merge PR | `gh pr merge --squash` | `curl PUT /repos/o/r/pulls/N/merge` |
| Submit review | `gh pr review N --approve` | `curl POST /repos/o/r/pulls/N/reviews` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |