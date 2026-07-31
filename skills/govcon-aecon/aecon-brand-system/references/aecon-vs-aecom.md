# Aecon vs AECOM — Disambiguation Reference

Two unrelated companies that are constantly confused. Wikipedia carries an explicit hatnote on both articles. Getting them wrong wastes an entire research/build cycle and produces useless deliverables.

## The Two Entities

| Attribute | **Aecon** (Amyn's employer) | **AECOM** (NOT Amyn's employer) |
|---|---|---|
| Full name | Aecon Group Inc. | AECOM (formerly AECOM Technology Corporation) |
| HQ | Toronto, Ontario, Canada | Dallas, Texas, USA (relocated from LA in 2021) |
| Stock exchange | **TSX: ARE** | **NYSE: ACM** |
| Website | aecon.com | aecom.com |
| Wikipedia | en.wikipedia.org/wiki/Aecon | en.wikipedia.org/wiki/AECOM |
| Type | Construction contractor | Infrastructure consulting (A&E, planning, program mgmt) |
| Revenue (most recent) | ~CA$4B range | ~US$16.1B (FY2025) |
| Fortune rank | — | Fortune 500 (#291 in 2023) |
| Employees | ~14,000 (Canada-weighted) | ~51,000 (global) |
| Identity markers | Canadian English, orange safety vests, CMMC/federal compliance work (Amyn's FBU), Univers LT Pro brand font | American, Dallas HQ, recently acquired Norwegian AI startup Consigli ($390M), GSA OASIS+ holder (Dec 2025) |
| M365 environment | **Amyn's tenant** — commercial + GCC High enclave, FBU work, CMMC L2 (Nov 2026 deadline) | Unknown — not Amyn's concern |

## How to Tell Which One a Task Means

1. **Default to Aecon** if the task involves:
   - Amyn's employer / his daily work
   - FBU (Federal Business Unit)
   - CMMC, GCC High, CUI, compliance
   - Canadian infrastructure / construction
   - His @aecon.com email context

2. **Likely AECOM (American)** if the task:
   - Names the ticker ACM / NYSE explicitly
   - Is a competitor/benchmark scan of large US infrastructure firms
   - References Dallas HQ, the Consigli acquisition, or Amentum (AECOM's 2019 spinoff)
   - Discusses GSA OASIS+ or major US federal A&E vehicles

3. **Still ambiguous?** ASK. One sentence: "Aecon (your employer) or AECOM (the American firm)? They're different companies." Surface this BEFORE any tool calls.

## Why This Matters Operationally

- A 17-page research briefing on the wrong company is worse than no briefing — it looks thorough and is therefore trusted, but every fact is about a different organization.
- Brand assets are NOT interchangeable. Aecon uses Univers LT Pro + #E51937/#C8102E reds (this skill). AECOM uses different branding entirely.
- Internal contacts, org charts, M365 tenants, contract vehicles — all completely different. Mixing them in a deliverable is a credibility-destroying error.

## Session Log

- **July 7, 2026:** A research task literally titled "AECOM" was executed against the American firm (NYSE: ACM). The loaded `aecon-brand-system` skill context (Amyn's @aecon.com email, FBU/M365 references) strongly indicated Aecon was the intended subject. The ambiguity was flagged only in the final report, after ~15 primary sources had been fetched and a 17KB findings doc written. The lesson: **confirm at task kickoff, not at delivery.**
