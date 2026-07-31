# Sources Sought Response Pipeline — Multi-Agent Orchestrator Pattern

Architected 2026-07-18 for Leatherneck Federal Consulting LLC (SDVOSB, $0 past performance). A 6-phase, 8-persona, 3-quality-gate pipeline for producing submission-ready Sources Sought responses at scale.

## When To Use

- Entity has 4+ Sources Sought to respond to in a short window (7 days)
- Entity is a new contractor ($0 past performance) — each response needs past performance strategy
- The responses must be tailored (not generic), evidence-backed, and reviewed for credibility
- You have an orchestrator agent that can dispatch parallel sub-agents

## Architecture

```
Phase 0: Setup → Entity factsheet, workspace, opportunity list
Phase 1: 6 Parallel Research Agents → Extract SAM.gov, parse attachments, USASpending incumbent research
  Gate 1: Research Verification → All attachments parsed? PWS extracted? Classification done?
Phase 2: 3 Parallel Persona Reviews → Strategist (Margaret Chen), Technical SME (Dr. Okonkwo), Contracts (Whit Whitfield)
  User GO/NO-GO Decision → Which opportunities to pursue
Phase 3: Response Planning → Per-opportunity plan: key messages, past perf strategy, evidence inventory
  Gate 2: Plan Verification → Every GO opportunity has credible past perf strategy
Phase 4: Drafting Teams → 2-agent teams (Technical Writer Patricia + Domain SME Dr. Chen) per opportunity
Phase 5: Gap Analysis → 1 judge agent per response with structured JSON output (P0/P1/P2 gaps)
Phase 6: Fix + Adversarial Review → Apply fixes, then adversarial KO (Frank Morrison) reads like real evaluator
  Gate 3: Final Adversarial Review → ADVANCE / BORDERLINE / DECLINE verdicts
Phase 7: Final Compilation → Clean versions, submission tracker, orchestration trace, HTML briefing
```

## Persona Library

| Persona | Role | Phase |
|---|---|---|
| Opportunity Research Agent | SAM.gov extraction, PWS parsing, incumbent discovery | Phase 1 (×6 parallel) |
| Margaret Chen | Senior Proposal Manager, 22yr, $4B+ wins, SDVOSB specialist | Phase 2 |
| Dr. Sarah Okonkwo | Technical SME, PhD CS, former DARPA PM, 200+ tech volumes | Phase 2 |
| James "Whit" Whitfield | Former SBA PCR, FAR Part 19 expert, $0 past perf workarounds | Phase 2 |
| Patricia Nakamura | GovCon Technical Writer, 18yr, 300+ proposals | Phase 4 |
| Dr. Marcus Chen | Domain SME, rotates by opportunity domain | Phase 4 |
| Color Team Reviewer | Gap analysis, 500+ proposals reviewed, structured JSON output | Phase 5 |
| Frank Morrison | Former DOD KO, 30+ SSEB chairs, adversarial evaluator | Phase 6 |

## Critical Rules

1. **SAM.gov interaction MUST use browser tools** — curl on SAM.gov returns unauthorized or garbage
2. **USAspending keywords do NOT do phrase matching** — use single tokens
3. **$0 past performance must be ADDRESSED DIRECTLY** — never hide it. Cite FAR 15.305(a)(2)(iv), use key personnel + teaming partner past performance.
4. **Never fabricate evidence** — acknowledge gaps and propose mitigation
5. **Sub-agents get self-contained specs** — they know nothing about conversation history
6. **Every quality gate MUST pass** before next phase begins

## Gap Severity Levels

- **P0**: Response is misleading, non-compliant, or would damage credibility → MUST fix
- **P1**: Weakens response significantly → SHOULD fix
- **P2**: Would improve → NICE to fix

## Workspace Structure

```
~/sources-sought-responses/
├── raw/                    Entity factsheet + per-opportunity attachments
│   ├── entity-factsheet.md
│   └── <notice-id>/        Downloaded SAM.gov attachments
├── research/               Phase 1 output — per-opportunity research files
│   └── 00-master-matrix.md
├── plans/                  Phase 2 + 3 output — persona reviews + response plans
├── drafts/                 Phase 4 output — draft responses + SME input
├── reviews/                Phase 5 + 6 output — gap analysis JSON + adversarial reviews
└── final/                  Phase 7 output — submission-ready + tracker + trace
```

## Entity Factsheet Template

The entity factsheet is the single context file every sub-agent receives. It must be self-contained and include:
- Legal name, UEI, CAGE, EIN, formation details
- SAM status, NAICS codes, PSC codes
- SDVOSB status, business size
- Key personnel with bios
- Core capabilities with EVIDENCE (not claims)
- Teaming structure description
- Past performance strategy (the honest framing)
- What NOT to disclose (confidential items like clearance status)

See `references/leatherneck-harbor-entity-factsheet.md` for the current factsheet.

## Time Budget

Phase 0: 15 min | Phase 1: 30 min | Phase 2: 20 min | Phase 3: 20 min | Phase 4: 45 min | Phase 5: 20 min | Phase 6: 50 min | Phase 7: 30 min
**Total: ~4-6 hours for 4-6 opportunities**