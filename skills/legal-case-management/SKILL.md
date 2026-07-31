---
name: legal-case-management
description: End-to-end employment law case management — jurisdiction analysis, attorney research and outreach across multiple states, legal document preparation (cover letters, case summaries, timelines, exhibit indices), and intake packet assembly. Professional HTML output, first-person narrative, print-ready formatting.
tags: [legal, attorney, employment, USERRA, case-preparation, jurisdiction, outreach, submission]
related_skills: [personal-task-orchestrator, writing-plans]
tier: A
moat_test: "(TBD — auto-classified v3.1; needs human classification per HARBOR moat test)"
---
# Legal Case Management

End-to-end employment law case management. Covers two phases: (1) attorney research and parallel outreach across jurisdictions, (2) legal document preparation and intake packet assembly. Produces professional HTML documents, never markdown.

## When to Load

- User asks to find attorneys for an employment law matter
- User needs to prepare legal submission packets for counsel
- User mentions USERRA, Title VII, FEHA, VHRA, or state employment claims
- User needs jurisdiction analysis for a remote-work case
- References sending documents to a law firm intake specialist
- Any attorney outreach or document prep task

---

## Phase 1: Attorney Research & Outreach

### Jurisdiction Analysis (FIRST)

Before contacting attorneys, determine the correct jurisdiction:

1. **Work location nexus matters more than employer headquarters.** Remote employees sue where they worked, not where the company is based.
2. Federal claims (USERRA, Title VII) apply nationwide. State claims (FEHA, VHRA, VVA) require state nexus.
3. Check the employment agreement for in-office requirements (e.g., "25% in Virginia office" = Virginia jurisdiction).

| Scenario | Primary Jurisdiction | Secondary |
|----------|---------------------|-----------|
| Remote from TX, 25% VA office | Texas | Virginia |
| Remote from CA, 100% remote | California | None |
| In-office VA only, lives MD | Virginia | Maryland |

See `references/jurisdiction-lessons-mehtani-call.md` for detailed analysis.

### Attorney Research Methodology

**Search patterns:**
- `[State] USERRA attorney contingency employee-side military veteran discrimination`
- `[State] employment attorney contingency plaintiff wrongful termination Super Lawyers`
- `"Board Certified Labor and Employment Law" [State]`

**Ranking criteria (in order):**
1. USERRA/military experience — explicit mention in practice areas
2. Employee-side only — no employer conflicts
3. Board certification — state equivalents
4. Contingency fee — no upfront costs
5. Super Lawyers / peer recognition
6. Geographic proximity

**Red flags:** Firms representing both employees AND employers, no contingency fee structure, employer-side focus.

### Parallel Outreach Strategy

- Contact 2-3 attorneys in parallel, not sequentially
- Compare offers, contingency terms, and strategic advice
- Select based on technical fit AND gut feel

**Questions to ask during consultation:**
1. Jurisdiction recommendation given work arrangement
2. USERRA claim strength
3. State law value-add
4. Contingency percentage and expense responsibility
5. Timeline to filing and resolution
6. Witness requirements
7. Overall strategy (litigation vs. settlement)

### Document Structure

```
lawyer/
├── [STATE]_ATTORNEY_OUTREACH.md       # Research, rankings, comparison
├── README_[STATE]_OUTREACH.md          # Process, checklist, next actions
└── submission/
    ├── [STATE]-cover-letter-[firm].html
    └── TEMPLATE-cover-letter.html
```

---

## Phase 2: Legal Document Preparation

### Core Conventions

- **Light theme ONLY:** white background, dark text `#1a1a1a`, gold accent `#d4a853`
- **Font:** Georgia / Times New Roman (serif — legal convention)
- **Print-ready:** 8.5"×11", `@page` rules, `page-break-inside: avoid`
- **FIRST PERSON throughout:** "I was terminated," "my supervisor told me," "I have not signed"
- **No emoji, no AI feel**
- **File format:** HTML only — no `.md` files in submission folders

### Packet Structure

```
submission/
├── 00-cover-letter.html       ← Cover letter to attorney/intake specialist
├── 01-case-summary.html       ← Full case overview (key document)
├── 02-employment-timeline.html ← Chronological events with significance tags
├── 03-exhibits-index.html     ← Catalog of all supporting PDFs
└── exhibits/                  ← Copies of supporting PDFs (numbered)
```

### 01 — Case Summary (most important)

Must include: Case Overview, Employment Background, Termination Details, The Pattern, Legal Claims, Key Evidence, Witnesses, Severance Status, Current Status.

### 02 — Employment Timeline

Chronological events. Each: date, description, legal significance note. Color-coded tags: Retaliation, Key Evidence, CRD Filed, Terminated.

### Cover Letter Requirements

- Address to specific attorney (not generic)
- Reference firm's specific expertise
- Include jurisdiction basis
- Single page when printed (11pt font, 1.45 line-height)
- Verify with Chrome headless: `--headless --print-to-pdf`

### Witness Handling

- Do NOT embellish — only write what user explicitly stated
- Don't infer presence at events unless user confirmed
- Partners/affiliates of opposing party should NOT be listed as witnesses
- Use user's own descriptions

---

## Key Pitfalls

### Don't assume employer headquarters = jurisdiction
Remote employees cannot sue in employer's HQ state. Jurisdiction follows work location nexus.

### Don't contact attorneys sequentially
Contact 2-3 in parallel to compare offers and contingency terms.

### Don't delegate document creation
User explicitly said: "do not delegate. do everything yourself." Build all HTML directly.

### Dates must be correct
Verify day-of-week matches calendar date with `date` or `gws calendar +agenda`.

### Table column widths: holistic, not uniform
Text-heavy columns get 35-55% width. Identifier columns get 4-12%.

### Cover letter must be 1 page
Start with 11pt, 1.45 line-height. Reduce to 10.5pt if needed. Verify with Chrome headless.

### Severance language: first person only
"I have not signed" — not "DO NOT SIGN."

### MD files are not for submission
Submission folders: HTML and PDF only. MD files are internal reference only.

### PDF conversion
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="output.pdf" "file://input.html"
```

---

## References

- `references/jurisdiction-lessons-mehtani-call.md` — Jurisdiction analysis from May 2026 counsel call
- `references/outreach-template.md` — Attorney outreach document templates
- `references/navaide-witnesses.md` — Witness handling rules and pitfalls
