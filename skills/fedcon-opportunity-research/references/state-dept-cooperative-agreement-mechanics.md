# State Department Cooperative Agreement Submission Mechanics

**Knowledge domain:** State Department grant/cooperative agreement application mechanics — MyGrants, SF-424 forms, indirect cost rates, compliance certifications, branding, reporting, and audit requirements.

**Source of truth:** DFOP0018157 NOFO, 2 CFR 200, 2 CFR 175, 2 CFR 600-604, eCFR, grants.gov, MyGrants, HHS PMS. All verified via eCFR as of July 2026.

**When to load this reference:** Any State Department NOFO requiring a cooperative agreement or grant submission, especially from ACN/EXBS. Complement with `references/exbs-program-intelligence.md` for program-specific competitive landscape.

---

## 1. Submission Platform: MyGrants

The Department of State uses **MyGrants** (not grants.gov) for electronic application submission. Applications submitted via other methods are rejected.

### Attachment Order (Mandatory)
```
A — Table of Contents
B — Required SF Forms (SF-424 + SF-424A combined PDF)
C — Proposal Narrative (Word, .docx)
D — Risk Assessment (stand-alone attachment)
E — Scope of Work / SOW (Word, outline form)
F — Detailed Budget (Excel, DOS template only)
G — Budget Narrative (Word)
H — NICRA (PDF, only if org has negotiated indirect cost rate)
I — A-133 Audit or audited financial statements (PDF, most recent)
J — Other Supporting Documents (optional)
```

### File Naming Convention
- Max 49 characters including spaces
- Format: `DocumentType_NOFONumber` (e.g., `Table_of_Contents_DFOP0018157`)
- Include LOE number only if applicable (`_LOE1`)

### Format Specifications (MANDATORY — non-compliance = disqualification)
- **Proposal Narrative:** 15pt Open Sans (not 12pt, not Times New Roman), single-spaced, 1" margins, 8.5×11 letter paper, all pages numbered
- **Budget:** Calibri 12pt, 8.5×11 letter paper
- **All documents:** English, U.S. dollars with NO cents (whole dollars only)
- **Language:** All in English

---

## 2. SF-424 Family Forms

### SF-424 Key Fields (State Dept NOFOs)
| Field | Standard Value |
|---|---|
| Type of Application | "New" |
| Assistance Listing Number | Varies by program (e.g., 19.317 for Counterproliferation) |
| Funding Opportunity Number | From NOFO (e.g., DFOP0018157) |
| Estimated Funding | Total budget, whole dollars, no cents |
| Project Start/End Date | From NOFO anticipated dates |

### SF-424A Cost Category Mapping
| Section | Category | Notes |
|---|---|---|
| A | Personnel | Direct-hire only; contractors go under Contractual |
| B | Fringe Benefits | % of Personnel |
| C | Travel | Fly America Act for international |
| D | Equipment | >=$10,000/unit, useful life >1 year |
| E | Supplies | <$10,000/unit |
| F | Contractual | Subawards, subcontracts, consultants — ALL go here |
| G | Construction | Capital assets |
| H | Other Direct Costs | Venue, translation, participant support, subscriptions |
| J | Indirect Costs | NICRA rate OR 15% de minimis on MTDC |

### Critical SF-424A Errors
- Contractors in Personnel instead of Contractual → REJECTED
- Indirect costs on total direct costs (not MTDC) → non-compliant
- Cost share listed when not committed → becomes binding obligation
- Cents in any budget field → non-compliant

---

## 3. 15% De Minimis Indirect Cost Rate (2 CFR 200.414(f))

### When Available
For organizations that have NEVER had a NICRA (negotiated indirect cost rate agreement). No documentation required. Can be used indefinitely across all federal awards.

### MTDC Definition (2 CFR 200.1)
**Included in MTDC base:** All direct salaries/wages, fringe benefits, materials/supplies, services, travel, and FIRST $50,000 of EACH subaward.

**Excluded from MTDC base:** Equipment, capital expenditures, rental costs, tuition remission, scholarships/fellowships, participant support costs, and portion of each subaward exceeding $50,000.

### Budget Tiebreaker
Per Executive Order 14332 Section 4(b)(iii): the applicant with the lower indirect cost rate wins tie scores. Using 15% de minimis provides a clear, defensible, low rate.

### For-Profit Alternative
For-profits without established overhead/G&A rate can instead allocate all indirect costs directly to appropriate cost categories (executive salaries → Personnel, office rent → Other Direct Costs, etc.).

---

## 4. Compliance Certifications

### Trafficking in Persons (2 CFR 175)
- **Trigger:** Services outside U.S. > $500,000 → certification REQUIRED
- Must have documented compliance plan prohibiting: severe trafficking, commercial sex acts, forced labor, identity document confiscation, failure to provide return transportation, fraudulent recruitment, recruitment fees
- Must inform federal agency and Inspector General immediately of any allegations
- Must flow down to ALL subrecipients

### PHFFA (Promoting Human Flourishing in Foreign Assistance — 2 CFR 602-604)
PHFFA is the umbrella. Three component parts:
- **2 CFR 602:** Protecting Life — abortion restrictions on foreign assistance
- **2 CFR 603:** Gender Ideology — restrictions on gender ideology programs
- **2 CFR 604:** Discriminatory Equity Ideology — DEI-related restrictions
- All three must flow down to ALL subrecipients
- Allowable compliance costs: familiarization, training, monitoring, recordkeeping, reporting

### Other Required Certifications
- Drug-Free Workplace (2 CFR 182)
- Never Contract with the Enemy (2 CFR 183)
- Debarment and Suspension (2 CFR 180)
- Lobbying certification (SF-LLL, if applicable)

### Funding Restrictions (State Dept NOFOs)
- NO funds to UNRWA
- No mass-migration caravan activities
- No alcoholic beverages (award funds)
- No entertainment expenses
- No policy advocacy for foreign governments/political factions
- No activities contrary to Executive Orders (verify at federalregister.gov)
- Buy America preference (2 CFR 200.322)
- No profit/fee for for-profit recipients or subrecipients (cost recovery only)

### For-Profit Cost Rules (State Dept Specific)
- **No profit/fee allowed** — budget must be cost recovery only
- Cost accounting follows **48 CFR 30** (Cost Accounting Standards) and **48 CFR Part 31** (Contract Cost Principles) — NOT just 2 CFR 200 Subpart E
- This is per 2 CFR 600.101(b): "The FAR at 48 CFR part 30, Cost Accounting Standards, and Part 31 Contract Cost Principles and Procedures takes precedence over the cost principles in Subpart E for Federal awards to U.S. and foreign for-profit entities."

---

## 5. Branding Requirements

### State Department Brand System
Reference: https://brand.america.gov/

All deliverables must display:
1. U.S. Department of State logo
2. Funding acknowledgment: "This [X] is funded by the U.S. Department of State, Bureau of [Name]"
3. Disclaimer: "The views expressed herein do not necessarily reflect those of the U.S. Department of State or the United States Government."

### Where Marking Applies
- Training materials (every slide/page)
- Data dashboards and portals (header/footer)
- Smartphone applications (splash screen + About page + app store listing)
- Reports and deliverables (cover page)
- Workshop/event materials (signage, agendas, certificates)

---

## 6. Reporting Requirements

### Financial Reporting
- Federal Financial Report (SF-425) via **HHS Payment Management System (PMS)**
- Default payment method: **Reimbursement** (org must float costs between draws)
- Advance payments possible but require: strong justification + Grants Officer approval + Deputy Assistant Secretary approval + Assistant Secretary approval

### Program Reporting
- Progress Performance Report (PPR) using agency-provided template
- Quarterly: Q1 Jan 30, Q2 Apr 30, Q3 Jul 30, Q4 Oct 30
- Foreign Assistance Data Review (FADR): track from budgeting through disbursement; separate accounting records if multiple FADR Data Elements

---

## 7. Audit Requirements

### Application Submission
NOFO language: "Most recent audit — include most recent single audit, program-specific audit, annual external audit, or audited financial statements."

- If org has never had single audit (no federal awards >$1M): submit audited financial statements
- Org WILL need single audit after receiving award (if >$1M in total federal awards)
- Audit costs may be included in proposal budget

### Single Audit Threshold
Per 2 CFR 200 Subpart F: $1,000,000 or more in total federal awards during fiscal year.

---

## 8. Cooperative Agreement vs Grant

### Substantial Involvement
Cooperative agreements have "substantial involvement" by the agency. For EXBS, this typically includes:
1. Reviewing/approving engagement outlines, draft agendas, supplemental materials
2. Reviewing/approving draft course content and revisions
3. Reviewing/approving list of proposed participants
4. Reviewing/approving scheduling and logistical arrangements
5. Reviewing/approving all final training materials

### Grantee Still Responsible For
Travel, lodging, venue, catering (non-alcoholic), interpretation/translation, A/V support, all logistics.

### Work Plan Implications
- Build 2-3 week buffer for every approval cycle
- Align milestones with EXBS approval gates
- Use "for EXBS review and approval" language in SOW activities
- PPR template is agency-provided — no custom format

---

## 9. Research Methodology and Pitfalls

### Researching Mechanics from a NOFO (Proven Pattern)
1. **Extract the NOFO fully:** pdftotext for PDFs, native parsing for .docx/.xlsx
2. **Read the formatting section FIRST** — format requirements (font, margins, page limits) are disqualifying if missed
3. **Map the attachment order** — non-sequential attachments may be rejected
4. **Cross-reference every "see X" or "per Y" reference** — trace each to the actual regulation
5. **Verify regulatory citations against eCFR** — NOFOs sometimes paraphrase; confirm exact wording

### Web Research Pitfalls Encountered (July 2026)
- **Firecrawl MCP can be unreachable** (402 credit exhaustion OR server down). Fall back to `web_extract` on known URLs (ecfr.gov, grants.gov, state.gov) and `web_search` for discovery.
- **web_search may return empty** for government-focused queries. Prefer `web_extract` directly on known authoritative URLs.
- **Large write_file calls time out** (>30K chars). Break content into multiple smaller writes using terminal heredocs (`cat >> file << 'EOF'`) or `patch(mode=replace)`.

### Writing Large Compliance Documents
- **Break into sections at natural boundaries** (one section per write/patch call)
- **Terminal heredoc with quoted delimiter** (`<< 'ENDOFFILE'`) prevents shell variable expansion
- **patch(mode=replace)** is reliable for appending/replacing content blocks
- **Verify structure after completion** with `grep "^## " file.md` to confirm all sections present

---

## 10. Key Regulatory Roadmap

| Regulation | What It Governs |
|---|---|
| 2 CFR 200 | Uniform Guidance — admin, cost principles, audit |
| 2 CFR 200.414(f) | 15% de minimis indirect cost rate |
| 2 CFR 200.1 | MTDC definition |
| 2 CFR 25 | Universal Identifier and SAM |
| 2 CFR 170 | Subaward/executive compensation reporting |
| 2 CFR 175 | Trafficking in Persons certification |
| 2 CFR 180 | Debarment and Suspension |
| 2 CFR 182 | Drug-Free Workplace |
| 2 CFR 183 | Never Contract with the Enemy |
| 2 CFR 600 | DOS-specific admin requirements |
| 2 CFR 602 | PHFFA — Protecting Life in Foreign Assistance |
| 2 CFR 603 | PHFFA — Gender Ideology |
| 2 CFR 604 | PHFFA — Discriminatory Equity Ideology |
| 48 CFR 30 | Cost Accounting Standards (for-profits) |
| 48 CFR 31 | Contract Cost Principles (for-profits) |