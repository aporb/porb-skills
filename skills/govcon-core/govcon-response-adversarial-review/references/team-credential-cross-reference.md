# Team Credential Cross-Reference — Detailed Procedure

Systematic cross-reference of team bios against a Sources Sought/proposal draft to identify where credentials fill gaps, replace weak claims, fix attribution errors, and enable new sections.

## When to Use

- Team bios/resumes are available (PDFs, people dossiers, call transcripts, session memory)
- A draft response exists and needs review
- The draft acknowledges capability gaps that team members might fill
- The draft has thin or vague claims that real credentials can replace
- You suspect team members are invisible in the draft

## Step 1: Consolidate All Team Bios

Extract every credential from every available source. Build a master table per person:

```markdown
### [Name] — [Proposed Role]
- **Education:** [degrees, institutions]
- **Certifications:** [PMP, DAWIA, CISA, FAC-C, etc.]
- **Service:** [branch, years, MOS/role]
- **Key Roles + Scale:** [title, employer, years, dollar value, team size]
- **Domain Skills:** [regulatory knowledge (FAR/DFARS/NIST), platforms, languages, clearance]
- **Published Work:** [books, playbooks, policies authored]
```

**Source priorities:**
1. PDF resume/CV (most authoritative)
2. LinkedIn profile (extracted via pdftotext)
3. People dossiers / company research files
4. Call transcripts (for self-reported credentials not on paper)
5. Session memory (context from prior conversations)

**Red flags during consolidation:**
- Credential appears in one source but not another → verify before using
- Self-reported credential with no documentation → treat as unverified
- "15+ years" claims without specific roles/dates → ask for dates

## Step 2: Section-by-Section Mapping

For each section in the draft, answer four questions:

| Question | What to Look For |
|----------|-----------------|
| **Gap Filler?** | Does the draft acknowledge a gap (e.g., "we don't have a DAWIA-certified person") that a team member's credential fills? |
| **Claim Strengthener?** | Does the draft make a weak/vague claim (e.g., "USMC veteran with operational planning") that a team member's specific credential can replace (e.g., "managed $20B+ procurement with 84-person team under DOE 413.3B")? |
| **Misattribution?** | Is a capability credited to the wrong person (e.g., FOCI mitigation credited to the technical lead when the compliance director is the actual SME)? |
| **Missing Person?** | Is a team member entirely absent from the section where their credential belongs? |

## Step 3: Flag Critical Error Patterns

These are the most common mistakes found in cross-reference:

### Pattern 1: Aspirational Credentials That Are Already Held
```
Draft: "Leatherneck commits to ensuring the PM holds PMP by contract start date"
Reality: Person already holds PMP + DAWIA Level III
Fix: Replace with "holds current PMP and DAWIA Level III — exceeding the PWS requirement"
Severity: P0 — makes the team look unqualified when they're overqualified
```

### Pattern 2: Gap Notes for Gaps That Are Filled
```
Draft: "Acknowledged gap: we do not have a DAWIA-certified acquisition professional"
Reality: Mark Payne holds DAWIA III Contracting + MS Acquisition & Contracting
Fix: Delete the gap note. Add Mark Payne as Acquisition Specialist.
Severity: P0 — advertises a weakness that doesn't exist
```

### Pattern 3: Wrong Attribution
```
Draft: "He [Amyn] handles FOCI mitigation, CUI/CDI handling..."
Reality: Douglas is the FOCI mitigation SME — led secure enclave design at Westerman
Fix: Move FOCI mitigation to Douglas's section. Amyn handles technical security implementation.
Severity: P0 — misattributes core capability to wrong person
```

### Pattern 4: Missing Team Members
```
Draft: Key Personnel section lists 2 people
Reality: 4-person team exists
Fix: Add all team members with their credentials
Severity: P1 — the evaluator can only score what they can see
```

### Pattern 5: Thin Claims Replaceable by Real Credentials
```
Draft: "A USMC veteran with operational planning and mission execution experience"
Reality: Person managed $20B+ procurement, 84-person team, DOE 413.3B, EVMS for $28B
Fix: Replace with specific scale and outcomes
Severity: P1 — the draft undersells the team
```

### Pattern 6: Unused Credentials
```
Draft: No mention of JD, PsyD, MS CS, Spanish proficiency, EVMS, Shipley certification
Reality: All exist across team members
Fix: Weave relevant credentials into appropriate sections
Severity: P2 — missed opportunities to differentiate
```

## Step 4: Produce the Gap-to-Strength Matrix

Output format per section:

```
### Section X.Y: [Name]

| Aspect | Current Draft | Gap/Weakness | Team Credential Replacement |
|--------|--------------|-------------|---------------------------|
| [specific claim or gap] | [what the draft says] | [why it's weak/wrong] | [exact credential + edit instruction] |
```

Add a priority column if the matrix will drive editing:
- **P0:** Must fix before submission (false claims, gap notes for filled gaps, wrong attribution)
- **P1:** Should fix (thin claims, missing team members, missing capabilities)
- **P2:** Nice to fix (unused credentials, formatting, style)

## Step 5: Identify New Sections

Team credentials may enable entirely new sections the draft doesn't include:

- **Subcontract Management section** — when a team member manages federal subcontracts
- **Acquisition Strategy section** — when a team member has 15+ years of contracting officer experience
- **Compliance Program Maturity section** — when a team member has built compliance programs from scratch
- **Transition Management section** — when a team member has managed M&O transitions
- **Multi-Language section** — when a team member has foreign language proficiency

## Step 6: Compile a Capability Gaps Summary

```
| Gap | Before (Current Draft) | After (With Full Team) |
|-----|----------------------|----------------------|
| Acquisition Specialist | ❌ GAP — subcontract needed | ✅ FILLED — Mark Payne, DAWIA III |
| PM Certification | ❌ GAP — "will obtain" | ✅ FILLED — already holds PMP + DAWIA III |
| License Specialist | ❌ GAP | ❌ STILL A GAP — sole remaining gap |
```

This summary is the most valuable output — it tells the team exactly what changed and what still needs work.

## Real Session Example: HHS OCIO VMO (7571TE26Q00092)

**Draft reviewed:** `7571TE26Q00092-final.html` — 5-page Sources Sought response for HHS OCIO VMO support.

**Team bios sourced from:**
- Douglas Henderson: 12-page PDF resume (pdftotext extracted)
- Mark Payne: Aecon people dossier + pre-start briefing
- Justin Frawley: Aecon people dossier + pre-start briefing
- Amyn Porbanderwala: Draft content + task summary

**Findings (11 total):**
1. Douglas already has PMP + DAWIA III — draft says "will obtain" (P0)
2. Mark Payne fills the Acquisition gap — draft proposes subcontracting (P0)
3. Mark Payne missing from Key Personnel (P0)
4. Justin Frawley missing from Key Personnel (P0)
5. FOCI mitigation misattributed to Amyn — Douglas is the SME (P0)
6. Douglas's NIST 800-171/800-53 compliance leadership missing (P1)
7. Douglas's FAR/DFARS/DEAR expertise unmentioned (P1)
8. Past performance lists only Amyn — missing 3 team members' track records (P1)
9. Key Personnel shows 2 of 4 team members (P1)
10. 10 team credentials unused (JD, PsyD, MS CS, EVMS, Spanish, etc.) (P2)
11. License Specialist gap remains — sole remaining gap (acceptable)

**Result:** 5 P0 fixes, 4 P1 improvements, 1 P2 enhancement, 1 acceptable gap. The matrix became the edit plan for the next draft revision.