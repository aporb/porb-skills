# Bechtel Pipeline Action Deck — Worked Example

**Date:** July 25, 2026
**User:** @watch_n3rd (Douglas Henderson, LFC co-founder)
**Context:** Douglas shared a Bechtel Project Opportunity Report (PDF) — 17 projects across Energy, Infrastructure, Mining, and Nuclear/Security. Goal: classify go/no-go and build outreach materials.

## Key Corrections from the Session

1. **Scope was too narrow initially** — First pass filtered for federal compliance only. User corrected: "it's not just federal work... look at what Harbor does and what I bring to the table." Evaluate across ALL capabilities.
2. **Branding was wrong** — First pass mentioned HARBOR and Amyn as separate entities. User corrected: "everything goes through lfc." LFC is the single external face.
3. **Missing hyperlinks** — All 17 projects must be hyperlinked to external sources (bechtel.com project pages, press releases, news articles). Never internal brief.h.porb.dev URLs.
4. **One file, not two** — The action deck MUST be merged into the decision briefing as additional tabs, not a separate file.
5. **Adversarial review** — "Run everything through an adversarial/judge review" before delivery.
6. **Send-by dates** — "Put recommendations on dates." Every email draft must include a send-by recommendation.
7. **Domain** — Use `leatherneckconsulting.com`. Never harborgovcon.com or other domains.
8. **Style guide compliance** — Must compare output against html-effectiveness gallery before delivery.

## Final Pipeline Classification

| Verdict | Count | Projects |
|---------|-------|----------|
| **GO** | 5 | Sentinel GBSD, Ras Al Hekma, WTP Hanford, Natrium, Australia HSR |
| **WATCH** | 6 | Louisiana LNG, Poland AP1000, Thacker Pass, Corpus Christi Stage 3, Rio Grande LNG, Micron NY Fab |
| **NO-GO** | 8 | Pluto LNG, Maple Creek, Salt River, Kilby, Combined Cycle, Solar, Ar Rjum Gold, Eva Copper |

Pipeline value: $1.0M–$3.0M assuming 1–2 engagements in 12 months, risk-adjusted $130K–$350K.

## Key Research Findings

- John Platt — SVP EPC Transformation (NEW role, Feb 2026). Primary LinkedIn target. His mandate = AI/robotics/digital EPC.
- Catherine Hunt Ryan — Director, Innovation Culture at Bechtel. LinkedIn target accepted, post-connection approach ready.
- Dena Volovar — new NS&E President (~Jul 2026). Strategy refresh window for Sentinel/WTP/Natrium.
- Australia HSR — A$61B. Bechtel named Delivery Partner (Jul 13, 2026). GO #5.
- Poland AP1000 — EPC NOT signed confirmed. Stay WATCH, re-check Oct-Nov 2026.
- Micron NY — $100B semiconductor fab, Bechtel EPC partner. Add to WATCH.
- Bechtel Innovate — 250+ deployments, NVIDIA AI partnership, BDAC. Frame as "accelerating" not "introducing."

## HTML Deck Structure

Single file, 8 tabs:

| Tab | Content |
|-----|---------|
| Analysis & Decisions | BLUF, decision summary, criteria, master table, GO/WATCH/NO-GO deep dives, discoveries, service lines, pipeline value, action plan |
| 1. Sentinel Email | Full draft to sentinelgbsd_sba@bechtel.com + A/B subject lines |
| 2. Supplier Portal | Step-by-step registration with NAICS codes |
| 3. Tech Advisory Capability | One-pager for SL2 (technology advisory for EPC programs) |
| 4. Outreach Emails | Ras Al Hekma, WTP, Natrium, LA LNG drafts with dates |
| 5. Nuclear Compliance | CMMC/DOE compliance capability statement |
| 6. LinkedIn Targets | Platt, Hunt Ryan, Volovar with approach strategy |
| 7. Poland + HSR Monitor | Poland status, AU HSR intel, Micron NY, innovation programs |

## HTML Bugs Found & Fixed

- **No tab CSS** — `display: none` on `.tab-panel` and tab button styling was completely missing. Added inline CSS.
- **BLUF wall of text** — Two dense paragraphs split into 6 scannable `<p>` tags.
- **Missing `.callout.olive`** — Used in HTML but no CSS rule. Added.
- **Wrong domain** — `harborgovcon.com` in early drafts. Replaced with `leatherneckconsulting.com`.

## Branding Snapshot

- External: Leatherneck Federal Consulting LLC (LFC)
- Internal delivery: HARBOR Initiative + Amyn Porbanderwala
- Domain: leatherneckconsulting.com
- UEI VU2HV8458J93, CAGE 21BA0
- SDVOSB status in email
