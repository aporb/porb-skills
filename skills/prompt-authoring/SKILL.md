---
name: prompt-authoring
description: "Design effective, copy-paste-ready prompts for Hermes Agent that ship real artifacts. Use when creating or improving prompts for agentic workflows, building a prompt library, or converting user intent into executable agent instructions."
version: 1.0.0
metadata:
  hermes:
    tags: [prompts, authoring, agent, orchestrator, briefing]
    related_skills: [spec-driven-workflow, daily-briefing, research-briefing]
tier: B
moat_test: "(TBD — auto-classified; needs human classification per HARBOR moat test)"
---

# Prompt Authoring

Design effective, copy-paste-ready prompts that turn Hermes into a shipping engine.
Every prompt targets a shipped artifact — a live URL, a populated database, a
published file — never a description of one.

## When to Use

- Creating a new prompt for the prompt library
- Converting a user's workflow idea into an executable agent prompt
- Improving an existing prompt that produces weak or incomplete output
- Designing prompts that demonstrate Hermes's value to non-technical users
- Any time a prompt needs to produce a real deliverable, not a plan

## Core Pattern: Agent Orchestrator

Every prompt opens with an explicit orchestrator instruction. This prevents the
common failure mode where a single context window tries to do everything and
produces shallow, fragile results.

```markdown
You are an Agent Orchestrator. Your role is to decompose complex tasks, plan the
work, delegate to specialized sub-agents, track progress, and synthesize results.
You do NOT execute implementation directly. You plan, route, track, and synthesize.
```

**Key elements of the orchestrator instruction:**
- **Role definition** — "You are an Agent Orchestrator" (not a coder, not a writer)
- **Scope boundary** — "You do NOT execute implementation directly"
- **Function list** — plan, route, track, synthesize (not: build, write, code)
- **Tone** — authoritative, constraining, unambiguous

## Prompt Structure (4-Phase)

### Phase 1 — Spec Package (mandatory, before any execution)
The LLM produces a spec BEFORE delegating work. The spec package includes:

- **Mission** — one paragraph: what, who, success metric
- **Tech Stack** — language, framework, dependencies, deployment target
- **Requirements** — RFC 2119 keywords (MUST/SHOULD/MAY), grouped by domain
- **Scenarios** — GIVEN/WHEN/THEN for every MUST requirement (happy path + edge case)
- **Validation Plan** — how to verify the build succeeded
- **Out of Scope** — explicit exclusions with reasons

This is the contract. Implementation only begins after spec review.

### Phase 2 — Delegation (sub-agent breakdown)
Decompose into 3-4 sub-agents with clear input/output contracts:

```markdown
**Sub-agent 1 — [Name]**
- [Specific task with concrete deliverable]
- Input: [what it receives]
- Output: [exact format and contents]

**Sub-agent 2 — [Name]**
...
```

**Delegation rules:**
- Parallel sub-agents must be independent (no shared state)
- Sequential sub-agents must have explicit input/output handoffs
- Maximum 3-4 sub-agents to avoid context fragmentation
- Each sub-agent has exactly ONE deliverable type

### Phase 3 — Synthesis (after all sub-agents complete)
A structured summary the user can verify at a glance:

```markdown
## Result
- [Primary deliverable with verifiable handle: URL, file path, record count]

## Execution Summary
- Sub-tasks completed: N/M
- Agents used: [list]
- Failures or retries: [describe or "none"]

## Spec Compliance
- [Each MUST requirement: ✓/✗ with brief note]
```

### Phase 4 — Operational Constraints (at the bottom)
Hard rules that prevent common failure modes:

```markdown
## OPERATIONAL CONSTRAINTS
- NEVER fabricate data — if not in source, mark as "not found"
- NEVER skip the spec phase and jump to building
- NEVER describe what you would build — build it
- If a sub-agent fails, retry with narrower scope; do not silently skip
- Maximum N sub-agents active at once
- All files must exist on disk before declaring done
```

## Briefing Output Format

When the output is an HTML briefing, use the **Anthropic HTML Artifact Format**
(ThariqS/html-effectiveness style). Reference: `references/anthropic-html-artifact-format.md`.

Key rules:
- Ivory background (#FAF9F5), serif headings, sans body, mono metadata
- Self-contained single file — no external CSS, CDN fonts, or JS frameworks
- 1.5px borders, 8-14px border-radius, callout boxes with 3px clay left-border accent
- No heavy shadows, no gradients, no emoji decoration
- Print-friendly via @media print

## Prompt Quality Checklist

Before delivering a prompt, verify:

- [ ] Opens with explicit orchestrator instruction ("You do NOT execute")
- [ ] Spec package phase is mandatory and comes before any execution
- [ ] Every requirement has at least one GIVEN/WHEN/THEN scenario
- [ ] Out-of-scope list has at least 3 explicit exclusions with reasons
- [ ] Sub-agent delegation has concrete I/O contracts (not "build the thing")
- [ ] "NEVER fabricate data" constraint is present and prominent
- [ ] Synthesis format includes verifiable handles (URL, path, record count)
- [ ] Prompt targets a shipped artifact, not a description
- [ ] No banned Constitution words (P7: delve, tapestry, leverage, robust, etc.)
- [ ] If briefing output: uses Anthropic HTML artifact format

## Common Pitfalls

- **Prompt is too vague about the output.** "Build me a website" produces a
  description. "Build a Next.js site at localhost:3000 with real data from
  ~/Downloads/resume.pdf" produces a website.
- **No validation gate.** Without a spec review phase, the LLM jumps to building
  and produces something that misses half the requirements.
- **Sub-agents are too broad.** "Build the whole app" as one sub-agent defeats
  the orchestrator pattern. Decompose into DB, API, frontend, verification.
- **Missing operational constraints.** Without explicit "NEVER fabricate" and
  "build it, don't describe it" rules, the LLM defaults to helpful-but-useless
  planning output.
- **Briefing format default.** Without explicit HTML artifact format instructions,
  briefings come out as generic dark-header layouts that don't match the Anthropic
  publication-quality standard.

## Reference Repos for Inspiration

When researching prompt patterns, consult:
- `https://github.com/ai-boost/awesome-prompts` — 328 prompts across all domains
- `https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools` — production system prompts from Cursor, Claude Code, Devin, Augment, Windsurf
- `https://github.com/ThariqS/html-effectiveness` — Anthropic HTML artifact format (briefing style)
- `https://github.com/f/awesome-chatgpt-prompts` — community prompt collection
- `https://github.com/dair-ai/Prompt-Engineering-Guide` — academic prompt engineering patterns
