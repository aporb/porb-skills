# GovCon Weekly Federal Register Scan Methodology

## When to Use

- User asks for Federal Register roundup for a specific date window (e.g., "research FR rules from July 13-20")
- GovCon daily/weekly briefing pipeline needs FR and executive actions input
- Standalone GovCon regulatory intelligence sweep

## Core Approach: web_extract on Daily Issue TOCs

The Federal Register publishes one issue per business day (Mon-Fri, no weekends or holidays). The most reliable path is:

```
web_extract on:
  https://www.federalregister.gov/documents/YYYY/MM/DD  (one per day in the range)
```

This bypasses browser bot-detection and returns clean, parseable TOC pages. Large issues are truncated — use `read_file` with offsets to page through the cached file.

## Agency Filter for GovCon Relevance

When scanning daily TOCs, filter for these agencies (in priority order):

| Priority | Agency | GovCon Relevance |
|----------|--------|-----------------|
| P1 | Defense Department (incl. Army, Navy, Air Force) | Defense contracting, DFARS, military procurement |
| P1 | General Services Administration (GSA) | FAR, GSAR, schedules, MAS |
| P1 | Small Business Administration (SBA) | Small business contracting, SBIR/STTR, disaster, 8(a) |
| P1 | Presidential Documents | EOs, proclamations, presidential memoranda |
| P2 | National Institute of Standards and Technology (NIST) | Cybersecurity standards (SP 800-171/172), CMMC |
| P2 | Homeland Security Department | FedRAMP, CISA, cybersecurity |
| P2 | Office of Management and Budget (OMB) | Procurement policy, NAICS, M-series memos |
| P2 | National Aeronautics and Space Administration (NASA) | SBIR, space procurement |
| P3 | Energy Department | DPA, DOE contracting, national labs |
| P3 | Commerce Department (BIS, NIST) | Export controls (EAR), standards |
| P3 | Committee for Purchase From People Who Are Blind or Severely Disabled | AbilityOne procurement list |

## Impact Tiering

Classify every found item into one of three tiers:

| Tier | Criteria | Examples |
|------|----------|----------|
| **HIGH** | Directly changes procurement rules, contract obligations, or creates new authorities | DPA rule, FAR/DFARS case, new EO on procurement, Section 301 investigation affecting IT contractors |
| **MODERATE** | Affects a subset of contractors, creates compliance obligations, or signals policy direction | COI rules, advisory committee nominations, BIS export rule changes, NIST standards notices |
| **LOW** | Administrative, informational, or tangentially related | Disaster declarations (routine), information collections, meeting notices |

## White House Cross-Reference

In parallel with FR extraction, browser-navigate to:
- `https://www.whitehouse.gov/presidential-actions/` — scan for EOs, memos, proclamations signed in the date window
- The WH site does NOT block browser access (unlike federalregister.gov)
- WH lists by signed date; FR lists by publication date — cross-check both
- OMB memoranda: `https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/`

## Output Structure

Save to `~/govcon_research/raw/<date>/federal-register.md` with this structure:

```markdown
# Federal Register & Executive Actions Summary: <date range>
> Prepared, focus areas, sources, methodology

## EXECUTIVE SUMMARY
(2-3 paragraph narrative of the week's key findings)

## HIGHLY RELEVANT ACTIONS
(One detailed table per HIGH item: FR doc #, date, agency, type, citation, pages, permalink, GovCon impact paragraph)

## MODERATELY RELEVANT ACTIONS
(Table per MODERATE item, same fields, shorter impact)

## WHITE HOUSE EXECUTIVE ORDERS & PRESIDENTIAL MEMORANDA
(Table: date, action name, type, GovCon relevance tier)

## ADDITIONAL ITEMS OF INTEREST
(Agency-by-agency listing of LOW-tier items)

## GAPS & BLANK SPOTS
(Negative-results table: topics with zero activity — FAR, DFARS, CMMC, FedRAMP, SBIR, AI, etc.)

## COMMENT DEADLINES & ACTION ITEMS
(Calendar of upcoming deadlines)

## KEY TAKEAWAYS
(Numbered practitioner-oriented conclusions)
```

## Negative Results Are Intelligence

When covering a date window, explicitly document what was NOT found. A "Gaps & Blank Spots" table showing zero activity on CMMC, FedRAMP, FAR/DFARS, SBIR/STTR, or AI policy is itself valuable intelligence for stakeholders tracking those pipelines. Quiet periods are meaningful.

## Pitfalls Specific to This Workflow

- **Firecrawl MCP may be unreachable.** If `firecrawl_search` returns connection errors, fall back to `web_extract` + `web_search` immediately — do not retry.
- **web_search may return empty for .gov queries.** Even simple queries like "federal register today" can return `data.web: []`. Use `web_extract` for direct .gov URLs.
- **Browser tools fail on federalregister.gov.** The site's bot detection returns a "Request Access" page. Use `web_extract` exclusively.
- **Weekends have no FR issues.** July 18-19, 2026 (Sat-Sun) returned 404s — this is expected. The date picker on any daily issue page shows which dates have content.
- **Individual FR document pages may 404.** Public-inspection timing can cause permalink 404s even for documents listed in the TOC. The TOC data is sufficient for impact assessment — don't spend cycles retrying.
- **Don't conflate FR publication date with WH signature date.** Presidential documents in the FR carry the publication date in citation but the signature date in the body text. Report both.
