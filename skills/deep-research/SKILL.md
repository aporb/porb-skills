---
name: deep-research
description: Multi-source deep research on any topic — markets, companies, people, technologies, policy. Fans out across Serper, SerpAPI, Perplexity and Brave, then synthesizes an HTML report. Use for prospect research, market analysis, or any topic that needs more than a single web search.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList
disable-model-invocation: true
model: opus
---

# Deep Research

HARBOR entry point for the multi-source deep-research capability. The
providers and engine live in the hermes layer; this skill dispatches to
the agent that drives them.

## Execution

This skill dispatches to the **researcher** agent (Tier A). It does not
execute inline. See `.claude/skills/SKILL-PATTERN.md`.

### Step 1 — Resolve inputs

Parse from the invocation: the research topic or brief; mode (`quick`
default, or `deep`); scoping (`direct` default, or `interactive`); an
optional output path. For any missing required input, use AskUserQuestion.
Do not guess the topic.

### Step 2 — Dispatch to researcher

Call the Agent tool with subagent_type `researcher` and a prompt
containing, in order:

1. The command as invoked.
2. Playbook: "Follow `~/.hermes/skills/research/deep-research/SKILL.md`
   as the authoritative workflow."
3. The resolved topic, mode, scoping, and output path.
4. Expected output: a self-contained HTML report in the thariq design
   system, no markdown. For a portfolio member, write it into that
   member's folder; otherwise into `admin/research/`.
5. Hard constraints: cite every claim with a source URL; respect the
   engine cost cap; if the run stopped partial, say so in the report.

### Step 3 — Handle the return

Relay the report path to the operator. If the researcher reports a
cost-cap stop or provider failures, surface that plainly. Do not retry
silently.

## Notes

- The four search providers and the fan-out engine are built by the
  deep-research provider and engine plans. This skill assumes they are
  installed under `~/.hermes/`.
- Quick mode is one fan-out pass; deep mode is an iterative loop. Deep
  mode escalates to the paid providers and costs more.
