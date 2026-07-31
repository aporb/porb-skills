---
name: hermes-chief-of-staff-workflow
description: Core Hermes workflows for Amyn's GovCon + AI-native ops.
about: Use when tasking Hermes with research, briefings, proposals, content, deploys, or coding for Amyn Porbanderwala (HARBOR Initiative / porb-server). Covers multi-agent dispatch, HTML+Nextcloud pipeline, proposal adversarial review, server deploy workflow, entity masking, and AI provider fallback chain.
category: hermes
---

# Hermes Chief-of-Staff Workflow

## Core Workflow: Plan → Approve → Execute → Gap → Fix → Deploy

### 1. Multi-Agent Intelligence Briefing
**Trigger:** Complex research topic, industry tracking, or need to understand a space.
**Pattern:**
1. Load relevant skills (govcon-daily-briefing-cmo, federal-register-research, etc.)
2. Dispatch 3-7 subagents in parallel, each on a tight slice (never overlap)
3. Include fallback chain in context: `curl > curl|grep > Python+requests` (Firecrawl is unstable)
4. Synthesize findings, connect dots, identify what actually matters
5. Write self-contained HTML (Thariq aesthetic)
6. Save to `/data/nextcloud/data/amyn/files/briefings/`
7. Run `docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"`
8. Send `brief.h.porb.dev/filename.html` link (never attach to Discord)

### 2. GovCon CMO Content Pipeline
**Trigger:** Need to post on LinkedIn/X for the week ahead.
**Pattern:** Anti-repetition check → 3 uncontested gaps → 3 LinkedIn posts + 1 X thread → schedule Wed 7AM, Thu 7:30AM, Fri 7AM, Fri noon.

### 3. Proposal Adversarial Review
**Trigger:** Federal proposal preparation or review.
**Pattern:** Extract ZIPs → web_extract → load fedcon-opportunity-research → interview → dispatch fix agents → verify → re-score → final briefing → convert to DOCX → cross-doc math audit.

### 4. Server Deployment
**Pattern:** research → interview → write plan → seed config + secrets → deploy → verify end-to-end → gap analysis → fix fallout → update all docs → commit + push per service.

### 5. HTML Briefing Delivery
- Self-contained HTML, Thariq tokens (ivory #FAF9F5, clay #D97757, slate #141413, oat #E3DACC, olive #788C5D)
- Save to Nextcloud briefings → occ files:scan → send `brief.h.porb.dev/filename.html` ONLY
- Never attach HTML files to Discord

### 6. AI Provider Fallback Chain
z.ai custom → DeepSeek V4 Flash → OpenRouter → SiliconFlow → DigOcean. Embeddings: qwen3-embedding-8b. Search: Tavily → ddgr → curl.

### 7. Entity Masking
DE LLC sub-k. No HARBOR parent, no personal names, no concurrent roles in client docs. No M&A speculation. Cross-doc math audit before delivery (90+ score required).
