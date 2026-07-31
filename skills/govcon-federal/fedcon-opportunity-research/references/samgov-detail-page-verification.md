# SAM.gov Detail Page Verification — New vs Re-compete Classification

Proven workflow for opening individual SAM.gov contract opportunity detail pages to extract: set-aside status, PSC code, description, past performance requirements, and new-vs-recompete signals.

## When to Use

SAM.gov search results don't show set-aside, value, or past performance requirements in the list view. Detail pages are the only way to verify these fields. This workflow is essential for:
- Classifying opportunities as NEW WORK or RE-COMPETE
- Identifying past performance blockers
- Finding the actual set-aside (list view often says "TBD")
- Extracting POC email addresses for capability statement submissions

## Workflow

### Step 1: Navigate to the detail page

```
browser_navigate → https://sam.gov/workspace/contract/opp/<32-char-hex-id>/view
```

The 32-char hex ID comes from the SAM.gov search results URL or the permalink.

### Step 2: Scroll down to trigger SPA content load

SAM.gov is a single-page application — the detail content doesn't render in the initial snapshot. Scroll down first:

```
browser_scroll → direction="down"
```

### Step 3: Full snapshot to extract fields

```
browser_snapshot → full=true
```

### Step 4: Parse the snapshot

Key fields to extract from the snapshot output:

| Field | Where to find it |
|-------|-----------------|
| **Title** | `heading "…" [level=1]` near the top |
| **Status** | Text "Active" or "Inactive" next to the title |
| **Notice ID** | `heading` under "Notice ID" label |
| **Related Notice** | `heading` under "Related Notice" — `(blank)` = NEW WORK, a notice ID = RE-COMPETE |
| **Contract Opportunity Type** | Sources Sought, Combined Synopsis/Solicitation, Solicitation, Special Notice, Presolicitation |
| **Response Date** | `heading` under "Response Date" or "Date Offers Due" |
| **Original Set Aside** | `heading` under "Original Set Aside" — the actual value (not TBD from list view) |
| **PSC** | `heading` under "Product Service Code" |
| **NAICS Code** | `heading` under "NAICS Code" |
| **Department/Agency** | `heading` under "Department/Ind. Agency" |
| **Sub-tier / Office** | `heading` under "Sub-tier" / "Office" |
| **Description** | Paragraphs under the "Description" section heading |
| **Contact Info** | `heading` for primary/alternative POC names, `email` links |
| **Attachments** | Links in the "Attachments" table — look for "Past Performance" in filenames |

### Step 5: Classify New vs Re-compete

Use these signals, ranked by reliability:

1. **Related Notice field:** blank = NEW WORK (no predecessor notice). A notice ID = RE-COMPETE.
2. **Contract Opportunity Type:** "Sources Sought" = market research, almost certainly NEW WORK (they're still figuring out the acquisition strategy).
3. **Amendment count:** "Amendment 1" or higher and language about "site visit" = RE-COMPETE (ongoing contract, they're modifying an existing solicitation).
4. **Attachments named "Past Performance Questionnaire" or "Relevant Past Performance Template"** = RE-COMPETE (they expect to evaluate past performance, meaning an incumbent exists).
5. **Description language:** "Follow-on to…", "Continuation of…", "Re-compete of…" = RE-COMPETE. "New requirement", "Establish…", "First-time…" = NEW.
6. **Published date:** Very recent publish date + Sources Sought type = NEW WORK. Older notice with amendments = RE-COMPETE.

### Step 6: Check for past performance blocker

Look for these in the attachments table:
- "Past Performance Questionnaire"
- "Relevant Past Performance Template"
- "Past Performance Information"
- "CPARS"

If any of these exist, the solicitation requires past performance. For entities with $0 contracts, this is a blocker unless:
- The Sources Sought/RFI stage doesn't require it (only the eventual RFP will)
- The entity can team with a prime that has past performance
- The solicitation explicitly allows "no past performance" submissions

### Example: HHS OCIO Vendor Mgmt Support (7571TE26Q00092)

- Related Notice: **(blank)** → NEW WORK
- Contract Opportunity Type: **Sources Sought** → confirms NEW
- Original Set Aside: **No Set aside used** (not "Total SB" as list view suggested)
- PSC: **R408** — Program Management/Support
- Description: "establish, operate, and mature a Vendor Management Office (VMO)" — clearly new
- Attachments: Draft SOW, Notice PDF — **no past performance questionnaire**
- POC: Joseph Kozar (joseph.kozar@hhs.gov)

→ **Classification: NEW WORK. No past performance required. High fit.**

### Example: FBI Communication Support (15F06726Q0000322)

- Related Notice: **(blank)**
- Contract Opportunity Type: **Combined Synopsis/Solicitation** (not Sources Sought — actual RFQ)
- Original Set Aside: **Service-Disabled Veteran-Owned Small Business (SDVOSB) Set-Aside (FAR 19.14)**
- PSC: **T006** — Film/Video Tape Production
- Description: "firm fixed price contract" per SOW
- Attachments: **Attachment E - Past Performance Questionnaire.docx** → PAST PERF REQUIRED

→ **Classification: Likely RE-COMPETE (FFP SDVOSB contract with past perf evaluation). SDVOSB eligibility confirmed but past performance is the blocker.**

### Example: VA CCTV Service (36C26226Q1049)

- Related Notice: **(blank)**
- Contract Opportunity Type: **Solicitation** (amended)
- Original Set Aside: **(blank)** — no set-aside
- PSC: **J063** — Maintenance/Repair/Rebuild of Alarm/Signal/Security Detection Systems
- Description: "AMENDMENT ONE SITE VISIT"
- Version history: 2 versions (original + amendment)
- Published: Jul 14, amended Jul 17

→ **Classification: RE-COMPETE. Amendment for site visit confirms ongoing contract. Incumbent likely the current CCTV maintenance provider.**

## Downloading Attachments

To download the actual PWS/SOW/Synopsis PDFs (not just the text description shown on the detail page), use the browser API interception technique documented in `references/samgov-attachment-download.md`. The detail page's "Download All" button triggers an API call to `/api/prod/opps/v3/opportunities/<oppId>/resources/download/zip` which returns a JSON redirect to an S3 presigned URL — download that with curl, unzip, and parse with `pdftotext -layout`. This is the only reliable way to get the full PWS text without SAM.gov API credentials.
