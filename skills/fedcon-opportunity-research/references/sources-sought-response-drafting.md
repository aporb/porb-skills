# Sources Sought Response Drafting — Template & Patterns

## Overview

This reference covers the structure and content patterns for drafting Sources Sought capability statements. It complements `sources-sought-pipeline.md` (orchestration) and `sources-sought-classification-deep-dive.md` (classification) by providing the actual drafting template and mandatory response elements.

## Mandatory Response Elements (per SS Notice instructions)

Every Sources Sought response MUST include these items when the notice requests them:

| Element | Required? | Pattern |
|---|---|---|
| Company identification (name, address, UEI, CAGE) | Always | Section 1 of response |
| Business size & socioeconomic status | Always | Section 2; include cert status |
| Relevant experience & capability | Always | Sections 5 + 7 |
| Teaming/subcontracting interest | Always | Section 8 |
| Contract vehicles held | Always | Section 9(e) |
| **PD sufficiency assessment (YES/NO)** | If asked in SS | Section 10 — answer directly |
| **ROM estimate with methodology** | If asked in SS | Section 11 — with data sources |
| **SBA VetCert proof** | If SS requires it | Flag gap honestly in Section 2 |
| **Section 508 compliance** | If ICT procurement | Note in Section 5 + subcontract scope |

## 11-Section Template Structure

Sections that appeared in the v2 VA SIEM response (36C10B26Q0650) — a proven structure:

```
1. COMPANY IDENTIFICATION (table: legal name, UEI, CAGE, address, NAICS, PSC, personnel, revenue)
2. BUSINESS SIZE & SOCIOECONOMIC STATUS (with certification gap disclosure if applicable)
3. NATURE OF REQUIREMENT (document what the PD actually asks for — hardware vs services)
4. TRANSPARENCY: SCOPE & LIMITATIONS (what you are NOT + what you ARE)
5. CORE CAPABILITIES (capability table + Section 508 note if ICT)
6. KEY PERSONNEL QUALIFICATIONS (bios + team differentiator)
7. PAST PERFORMANCE & EXPERIENCE (cite FAR 15.305(a)(2)(iv) if $0 PP)
8. TEAMING INTEREST (sub, teaming partner, SDVOSB participation credit)
9. RESPONSE TO SS INFORMATION REQUESTS (itemized table a-e)
10. DRAFT PD SUFFICIENCY ASSESSMENT (YES [X] NO [ ] with rationale)
11. ROUGH ORDER OF MAGNITUDE (ROM with methodology and disclaimer)
```

## Critical Patterns

### SDVOSB Certification Gap Disclosure

When the entity is self-attested SDVOSB but the SS notice requires SBA VetCert proof:

- **DO:** Disclose the gap prominently in Section 2. State that you're responding as market research input only. Cite both paths: (a) complete VetCert before solicitation, or (b) subcontract to a certified SDVOSB prime.
- **DO NOT:** Let the self-attested status pass as if it satisfies the requirement. This is misrepresentation.
- **Phrasing:** "IMPORTANT — SBA VetCert Certification Gap: [Entity]'s SDVOSB status is currently self-attested via SAM.gov. The Sources Sought Notice explicitly requires proof of SBA certification. [Entity] has not yet obtained SBA VetCert certification (application in process) and therefore cannot currently provide the SBA certification proof required by the notice."

### PD Sufficiency Assessment (YES/NO)

When the SS asks "Has the draft PD provided sufficient detail to describe the technical requirements?":

- Answer YES if the PD identifies capability domains adequately for qualified offerors in the space. Most PDs WILL be sufficient for the vendors they target.
- Answer NO only if the PD is genuinely deficient (missing entire capability domains, contradictory requirements, etc.) — and provide specific technical comments.
- Always include a rationale paragraph explaining your answer.
- If you're not positioning as a prime, note that your assessment reflects sufficiency for qualified offerors in that space, not for your own capability set.

### ROM Estimate Methodology

When the SS requests a Rough Order of Magnitude:

- **Sources:** Prior awards for the same program/agency (USASpending), comparable awards from the same contracting office, industry benchmarks for the product/service category.
- **Structure:** State the range first, then provide numbered methodology points with specific award references.
- **Range rationale:** Explain both the lower and upper bound assumptions.
- **Disclaimer:** Always include that this is market-research only, not based on IGCE access.

### Section 508 Compliance (ICT Procurements)

For ICT (Information and Communication Technology) procurements:

- Add a "Section 508 Compliance" row to the capability table
- Include a standalone compliance note referencing 36 CFR Part 1194
- Weave 508 into the subcontract scope description
- If the entity has accessibility testing/validation capability, document it

### Transparency in Scope & Limitations

Always include a "what we are not" / "what we are" section. This:

- Prevents misrepresentation (you're not claiming capabilities you don't have)
- Builds credibility (the CO sees you understand the requirement)
- Frames your subcontract/teaming positioning clearly

## Practical: Multi-Patch File Construction

When drafting large response files (10+ KB markdown) in Hermes, the `write_file` tool may time out on the full content. Build the file incrementally:

1. Write a skeleton with `write_file` (sections 1-3, ~1.5 KB)
2. Add sections 4-5 with `patch` (append after last paragraph)
3. Add sections 6-8 with `patch`
4. Add sections 9-11 with `patch`
5. Add closing + submission block with `patch`

Each patch: match on the LAST paragraph of the existing file as `old_string`, append the new content in `new_string`. The match must be unique — use a complete paragraph as the anchor.

## Simultaneous Research File Updates

When the SS response draft reveals errors in the research file (wrong deadline, missing POC, incorrect classification):

1. Patch the research file's deadline, POC table, and timeline narrative
2. Update any downstream references that cascade from the research file
3. The research file is the source of truth for classification — keep it in sync

## Worked Example

The v2 VA SIEM response (`36C10B26Q0650-draft-v2.md`) in `~/sources-sought-responses/drafts/` demonstrates all patterns above:
- SDVOSB cert gap disclosed (Section 2)
- Hardware procurement reframed from services (Section 3)
- PD sufficiency answered YES with rationale (Section 10)
- ROM $3M-$8M with 5-point methodology (Section 11)
- Section 508 compliance noted (Section 5 + throughout)
- 10-page limit compliance noted in footer
- Dual POC submission (Ethan Goldring + Edward Hebert)
- Deadline corrected from Jul 23 → Jul 28 across research file and draft