# Executive Actions Research: Cross-Source Methodology

Methodology for researching White House executive actions (EOs, memoranda, proclamations, determinations, OMB memos) across multiple authoritative sources with hard date enforcement.

## When to Use

- "Find executive actions between [date] and [date]"
- "What EOs did the White House issue this week/month?"
- Researching procurement/compliance implications of recent presidential actions
- The "White House / Executive Actions" agent in the daily GovCon briefing pipeline

## Source Priority (check ALL, cross-verify)

### 1. Federal Register API (authoritative for published documents)

```bash
# All presidential documents in a hard date window — uses BOTH gte and lte
curl -s "https://www.federalregister.gov/api/v1/documents.json?conditions%5Btype%5D%5B%5D=PRESDOCU&conditions%5Bpresident%5D%5B%5D=donald-trump&conditions%5Bpublication_date%5D%5Bgte%5D=YYYY-MM-DD&conditions%5Bpublication_date%5D%5Blte%5D=YYYY-MM-DD&per_page=50&order=newest"
```

- `PRESDOCU` covers EOs, Proclamations, Determinations, Memoranda, Notices
- `subtype` field on individual documents distinguishes them (Executive Order, Proclamation, Determination)
- `executive_order_number` field gives the EO number
- Always use BOTH `gte` AND `lte` when a hard window is specified

### 2. White House site (by signed date)

```bash
# Presidential actions page (EOs, memoranda, proclamations) — lists by SIGNED date
curl -sL "https://www.whitehouse.gov/presidential-actions/" | grep -oE '<title>[^<]+</title>'

# Specific subtypes
curl -sL "https://www.whitehouse.gov/presidential-actions/executive-orders/"
curl -sL "https://www.whitehouse.gov/presidential-actions/presidential-memoranda/"
curl -sL "https://www.whitehouse.gov/presidential-actions/proclamations/"

# Briefing room (releases, statements, fact sheets — NOT formal actions)
curl -sL "https://www.whitehouse.gov/briefing-room/"

# Individual action full text
curl -sL "https://www.whitehouse.gov/presidential-actions/YYYY/MM/SLUG/"
```

**Pitfall:** The WH site and FR use different date bases — WH by signed date, FR by publication date. Cross-check.

### 3. OMB Memoranda (NOT in Federal Register)

```bash
# OMB memoranda page — has direct PDF links
curl -sL "https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/"
```

OMB memos use `M-YY-NN` numbering (e.g., M-26-15 = 2026 memo #15). Extract the `<li><a href="...PDF">M-YY-NN Title</a> (Date)</li>` entries. This page covers both current-year and prior-year memos.

### 4. Google News RSS (news cycle / secondary verification)

```bash
# Find news coverage of recent actions
curl -sL "https://news.google.com/rss/search?q=executive+order+2026&hl=en-US&gl=US&ceid=US:en"
curl -sL "https://news.google.com/rss/search?q=presidential+memorandum+2026&hl=en-US&gl=US&ceid=US:en"
curl -sL "https://news.google.com/rss/search?q=OMB+memo+2026&hl=en-US&gl=US&ceid=US:en"
```

Extract `<title>` and `<pubDate>` pairs. Useful for finding actions that haven't hit FR yet, and for legal/industry analysis context.

### 5. Federal Register full text (per document)

```bash
# Full text HTML — needed to extract signed date and substantive content
curl -sL "https://www.federalregister.gov/documents/full_text/html/YYYY/MM/DD/FR-NUMBER.html"
```

Strip tags with: `python3 -c "import sys,re; html=sys.stdin.read(); text=re.sub(r'<[^>]+>',' ',html); text=re.sub(r'\s+',' ',text); print(text[:N])"`

## Extraction Targets (per action)

For each action found, extract:

| Field | Source |
|-------|--------|
| Title | FR API `title` |
| Date (signed) | FR full text footer ("THE WHITE HOUSE, [date]") |
| Date (published) | FR API `publication_date` |
| Type | FR API `subtype` (Executive Order / Proclamation / Determination / Memorandum) |
| EO/Memo number | FR API `executive_order_number`; OMB page for `M-YY-NN` |
| Full summary | FR full text (read full body) |
| Agencies affected | FR API `agencies` + full text directives |
| Procurement/compliance implications | Full text analysis (requires reading) |
| Source URL | FR `html_url` + WH action URL |

## Hard Date Enforcement

When the user specifies "between X and Y" or "nothing before Z":
- Query FR with BOTH `publication_date[gte]` and `publication_date[lte]`
- Explicitly note the signed-vs-published distinction in the report
- Include a "just-prior context" section for actions signed just before the window but still in active implementation (clearly marked as outside-window)
- The president filter (`conditions[president][]=donald-trump`) is independent of date and scopes to the current administration

## Report Structure (validated pattern)

```
1. Summary table (counts by type)
2. Per-document deep dive (one section each)
   - Metadata table (type, dates, numbers, URLs)
   - Summary (what it does)
   - Agencies affected
   - Procurement/compliance implications
3. Significant agency rules triggered by EOs (e.g., NEPA implementing rules)
4. WH releases/statements (not formal actions, but policy signals)
5. OMB memo status (even if "no new memos")
6. Just-prior context (actions signed before window, still active)
7. Sources checked table
```

## Worked Example: June 30 – July 7, 2026

This was a holiday week (July 4th) with light executive action. Findings:

- **4 presidential documents** published in FR: EO 14414 (regenerative agriculture, signed Jun 25 published Jun 30), Proc. 11038 (Morocco phosphate fertilizer emergency), PD 2026-16 (Joint Base Andrews golf course Clean Water Act exemption), PD 2026-17 (Venezuela TVPA determination)
- **0 new EOs, memoranda, or OMB memos** issued in-window
- **High-impact GovCon items** were NOT presidential documents but agency rules implementing prior EOs: NASA NEPA interim final rule (Jul 1), NRC NEPA proposed rule (Jul 7), FTC AI Policy Statement (Jul 7, comments due Jul 31)
- **CEQ NEPA reforms announcement** (Jun 30) flagged 60+ agencies reforming procedures

Lesson: On light weeks, the significant procurement/compliance developments come from **agency implementing actions**, not new presidential documents. Always search FR for rules implementing the administration's prior EOs within the window.

## Pitfalls

- **Light weeks still matter.** A week with "only" 2 determinations and a proclamation may still have major agency rules implementing prior EOs. Always run a separate FR query for procurement/contract and topic-specific rules.
- **News coverage lag.** Google News may surface analysis of actions signed days earlier. Verify publication dates against FR before including.
- **OMB memos don't appear in FR searches.** They're White House-only documents. Check the OMB page directly.
- **Proclamations are often ceremonial** (e.g., "National Homeownership Month") but some carry real policy weight (e.g., Proc. 11038 invoked emergency tariff authority). Read the full text before dismissing.
- **Determinations are narrow but can exempt specific projects** from environmental law (e.g., PD 2026-16 exempted Joint Base Andrews golf course from Clean Water Act). Relevant to the specific contractor even if not broadly significant.
