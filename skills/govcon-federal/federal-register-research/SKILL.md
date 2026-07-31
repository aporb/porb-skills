---
name: federal-register-research
description: Research, extract, and analyze Federal Register rulemakings AND presidential documents (EOs, proclamations, determinations, memoranda, OMB memos) using the FR API, XML parsing, cross-source verification, and multi-agent parallel analysis. Covers proposed rules, interim rules, final rules, and executive actions across all federal agencies.
category: research
---

# Federal Register Research & Analysis

## Trigger Conditions
- Need to find and analyze proposed/final rules in the Federal Register
- Need to understand changes across multiple FAR parts, CFR sections, or agency rules
- Need to extract discussion/analysis sections from Federal Register XML
- Need to split a large rulemaking into per-topic sections for parallel analysis
- **Need to research executive actions (EOs, memoranda, proclamations, OMB memos) in a date window** — see `references/executive-actions-research.md` for the cross-source methodology
- **Need to build a complete queryable archive of ALL documents of a given type (e.g., all Trump EOs)** — see `references/document-archive-pipeline.md` for the bulk pipeline: FR API ingest → SQLite → full text → staged multi-persona analysis → HTML briefings
- **Need to add semantic search / vector embeddings to a document archive** — see `references/embedding-vector-pipeline.md` for cheap embedding with OpenRouter models (Qwen3-Embedding-8B) + SQLite BLOB vector storage + cosine similarity search, all for ~$0.02/1,400 docs

## Research Phase

### Choosing Your Method

The Federal Register can be researched via three paths, listed by reliability:

| Method | Reliability | Use When |
|--------|-------------|----------|
| **web_extract on daily issue TOC** | ⭐⭐⭐ HIGHEST | Browser blocked, API unreachable, or scanning all documents across multiple days |
| **FR API (curl)** | ⭐⭐ MEDIUM | Direct HTTP access available, need structured JSON, targeting specific terms/rules |
| **Browser navigation** | ⭐ LOW | FederalRegister.gov actively blocks browser scraping (bot detection → "Request Access" page) |

**Key insight:** `web_extract` on `federalregister.gov/documents/YYYY/MM/DD` returns clean, parseable TOC pages and **bypasses bot detection entirely**. This is the most reliable path and should be your default for date-window research.

### Method A: Daily Issue TOC via web_extract (RECOMMENDED DEFAULT)

**Workflow for a date-window scan:**
1. Call `web_extract` with all daily-issue URLs in parallel (one per day in the range)
2. Full content is cached to `~/.hermes/cache/web/www.federalregister.gov-<hash>.md`
3. Large issues (500+ entries) will be truncated — use `read_file` with offsets to page through
4. Scan TOC for agency names matching your topic filter (DoD, SBA, NIST, GSA, DHS, etc.)
5. Note document numbers and types (RULE, PRORULE, NOTICE, PRESDOCU) for deep-dives
6. For high-value items, extract the individual permalink: `web_extract` on `federalregister.gov/d/FR-NUMBER`

**GovCon-specific agency filter:** Defense Department, Army, Navy, Air Force, GSA, SBA, NIST, DHS/CISA, OMB, Presidential Documents, NASA, Committee for Purchase From People Who Are Blind or Severely Disabled.

**White House cross-reference:** In parallel, browser-navigate to `whitehouse.gov/presidential-actions/` for EOs, proclamations, and memoranda. The WH site does NOT block browser access. Filter by sub-page (Executive Orders, Presidential Memoranda) and check dates against your window.

**Pitfall: Truncated files.** Daily issues can be 1,000+ lines. `web_extract` truncates large pages at ~15K chars with head+tail sections. Always check for a `[TRUNCATED]` footer — if present, read the full cached file with `read_file` using offsets.

**Pitfall: Individual document 404s.** Some permalink URLs (`federalregister.gov/d/FR-NUMBER`) return 404 even when linked from the daily TOC. This is a public-inspection timing issue — the TOC data (title, type, agency, citation, pages) is usually sufficient for GovCon impact assessment. Do not get stuck retrying individual document pages; move on.

**Pitfall: Weekend gaps.** The Federal Register does not publish on Saturday or Sunday. A 7-day window (Mon-Sun) typically has only 5 issue dates. Check the date picker on any daily issue page to identify which dates have content.

### Method B: Federal Register API (curl)

### Query by Term and Date

```bash
# Search for documents matching a term, published on or after a date
curl -s "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=YOUR+QUERY&conditions%5Bpublication_date%5D%5Bgte%5D=YYYY-MM-DD&order=relevance&per_page=20"
```

### Presidential Documents (EOs, Proclamations, Determinations, Memoranda)

Presidential documents use `type=PRESDOCU`. The `subtype` field distinguishes Executive Order / Proclamation / Determination / Memorandum / Notice. Use the `president` filter to scope to an administration.

```bash
# All presidential documents in a date window (HARD date enforcement)
curl -s "https://www.federalregister.gov/api/v1/documents.json?conditions%5Btype%5D%5B%5D=PRESDOCU&conditions%5Bpresident%5D%5B%5D=donald-trump&conditions%5Bpublication_date%5D%5Bgte%5D=YYYY-MM-DD&conditions%5Bpublication_date%5D%5Blte%5D=YYYY-MM-DD&per_page=50&order=newest"

# Get subtype, EO number, and full-text URL for a specific document
curl -s "https://www.federalregister.gov/api/v1/documents/FR-NUMBER.json?fields%5B%5D=title&fields%5B%5D=subtype&fields%5B%5D=executive_order_number&fields%5B%5D=body_html_url&fields%5B%5D=publication_date"
```

**Pitfall: signed date ≠ published date.** Presidential documents are signed on one date and published in the Federal Register days later (e.g., EO 14414 signed Jun 25, published Jun 30). When the user gives a date window, query by `publication_date` but report both dates. The FR full text reveals the signed date ("THE WHITE HOUSE, June 25, 2026").

**Pitfall: WH site lists actions by signed date, FR by publication date.** The same EO may appear in different date ranges depending on source. Cross-check both.

**Pitfall: OMB memoranda are NOT in the Federal Register.** Check the OMB memoranda page directly: `https://www.whitehouse.gov/omb/information-resources/guidance/memoranda/`. OMB memos use the `M-YY-NN` numbering scheme (e.g., M-26-15 = 2026 memo #15).

For full cross-source methodology (WH site + FR API + Google News RSS + OMB), see `references/executive-actions-research.md`.

### Get Document Metadata

```bash
# Get full document metadata including FR number, pages, dates
curl -s "https://www.federalregister.gov/api/v1/documents/FR-NUMBER.json"
```

Key fields from the response:
- `title` — Full document title
- `document_number` — FR document number (e.g., 2026-12559)
- `start_page`, `end_page` — Federal Register page range
- `publication_date` — Date published
- `comments_close_on` — Comment deadline
- `abstract` — Summary
- `action` — Type (e.g., "Proposed rule.")
- `body_html_url` — Full text HTML URL
- `full_text_xml_url` — Full text XML URL (best for parsing)

### Get Full Text URLs

```bash
# Get body_html_url and full_text_xml_url
curl -s "https://www.federalregister.gov/api/v1/documents/FR-NUMBER.json?fields[]=body_html_url&fields[]=full_text_xml_url"
```

## Extraction Phase: XML Parsing

### Download XML

```bash
curl -sO "https://www.federalregister.gov/documents/full_text/xml/YYYY/MM/DD/FR-NUMBER.xml"
```

### Parse the XML Structure

The Federal Register XML has this structure:

```xml
<PRORULE>
  <PREAMB>
    <AGENCY>...</AGENCY>
    <CFR>48 CFR Parts X, Y, Z</CFR>
    <SUBJECT>...</SUBJECT>
    <SUM>...summary...</SUM>
    <EFFDATE>...dates...</EFFDATE>
  </PREAMB>
  <SUPLINF>
    <!-- This contains the SUPPLEMENTARY INFORMATION —
         the actual discussion and analysis -->
    <HD>I. Background</HD>
    <P>...text...</P>
    <HD>II. Discussion and Analysis</HD>
    <HD>A. General</HD>
    <HD>B. Summary of Changes to FAR Part X</HD>
    ...
  </SUPLINF>
</PRORULE>
```

### Extract SUPLINF Text

```python
import xml.etree.ElementTree as ET

def extract_text(elem):
    """Recursively extract all text from an XML element."""
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(extract_text(child))
        if child.tail:
            parts.append(child.tail)
    return ''.join(parts)

tree = ET.parse('FR-NUMBER.xml')
root = tree.getroot()
# Find SUPLINF element
for elem in root.iter():
    tag = elem.tag.split('}')[1] if '}' in elem.tag else elem.tag
    if tag == 'SUPLINF':
        text = extract_text(elem)
        break
```

### Split by Topic/Part Section

Federal Register rules often have sections like:
- "B. Summary of Changes to FAR Part X"
- "C. FAR Part X" (shorter format)
- "D. Summary of Proposed Changes to FAR Part X"

Use regex to find section headers:

```python
import re

pattern = r'^[ \t]*([A-Z])\. (?:Summary of (?:Proposed )?Changes to )?(?:FAR )?Part (\d+)'
matches = list(re.finditer(pattern, text, re.MULTILINE))

for i, m in enumerate(matches):
    part_num = m.group(2)
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    section_text = text[start:end].strip()
    # Save to file or process
```

**Pitfall: PRA sections interleaved.** Many rules have Paperwork Reduction Act (PRA) sections that repeat the same part numbers. Cut the text at "IV. Executive Orders" or "Paperwork Reduction Act" or "D. Comments Regarding Paperwork Burden" to get only the discussion sections:

```python
cut_pos = len(text)
for marker in ['IV. Executive Orders', 'V. Executive Orders', 'Paperwork Reduction Act', 'D. Comments Regarding Paperwork Burden', 'List of Subjects in 48 CFR']:
    idx = text.find(marker)
    if idx > 0 and idx < cut_pos:
        cut_pos = idx
discussion_only = text[:cut_pos]
```

## Analysis Phase: Multi-Agent Parallel Delegation

### When to Use Multi-Agent Analysis

Use for complex rulemakings that affect multiple code sections (e.g., FAR parts, CFR titles). Send each section to a separate leaf subagent for focused analysis.

### Batch Pattern (3 concurrent)

```python
# Prepare per-section files, then dispatch in batches of 3
from hermes_tools import terminal

tasks = [
    {
        "goal": "Analyze [section] proposed changes. Read /path/to/file.txt. Produce: (1) Key changes, (2) Impact on stakeholders, (3) Strategic significance, (4) Comment angles.",
        "context": f"File path: /path/to/partX.txt. Background context about the overall rule.",
        "toolsets": ["file"]
    },
    # ... up to 3 tasks per batch
]

# Dispatch via delegate_task with tasks array
```

**Important constraints:**
- Max 3 concurrent children per user (configured via `delegation.max_concurrent_children` in config.yaml)
- Each subagent reads files from the filesystem — pass file paths in context, not file content
- Subagents return structured summaries; they cannot use `delegate_task`, `clarify`, `memory`, or `execute_code`
- Results come back as a consolidated message when all tasks in the batch complete

### Handling Part 52 (Cross-Cutting Sections)

When the same code section (e.g., FAR Part 52 for clauses) appears in multiple rules, combine all rule-specific extracts into one analysis file before dispatching:

```python
combined = "=== FAR PART 52 - Combined Across All Rules ===\n\n"
for fr_num in sorted(rules_with_part_52):
    with open(f'/tmp/far_discussion/{fr_num}_Part52.txt') as f:
        combined += f"\n--- From RULE {fr_num} ---\n\n" + f.read()
```

### Analysis Agent Prompt Template

Each analysis agent should receive this structured prompt:

```
Analyze [FAR/CFR Part X] proposed changes under [Rule Name].
Read the file at /path/to/part.txt and the background at /path/to/background.txt.

Produce a structured analysis covering:
(1) Key proposed changes (what, why, and where in the regulation)
(2) Impact on industry/regulated entities
(3) Impact on government/officials
(4) Strategic significance (why this matters beyond the specific change)
(5) Comment angles/public input opportunities

Keep concise (under 1000 words) and actionable.
```

## Synthesis Phase: HTML Briefing

After all per-section analyses return, compile into a self-contained HTML briefing using the Thariq/html-effectiveness aesthetic:

### Design Tokens

```css
:root {
  --ivory:  #FAF9F5;
  --paper:  #FFFFFF;
  --slate:  #141413;
  --clay:   #D97757;
  --clay-d: #B85C3E;
  --oat:    #E3DACC;
  --olive:  #788C5D;
  --g100:   #F0EEE6;
  --g200:   #E6E3DA;
  --g300:   #D1CFC5;
  --g500:   #87867F;
  --g700:   #3D3D3A;
  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
}
```

### Briefing Structure

1. **Title + Metadata bar** (rule name, publication date, comment deadline, page count)
2. **Table of Contents** (collapsible card)
3. **Executive Summary** with key numbers in a callout box
4. **Rule-by-rule breakdown** with tables linking FR numbers to affected sections
5. **Per-section analysis** (cards with change descriptions, impact ratings, comment angles)
6. **Cross-cutting themes** section
7. **Strategic implications** for different stakeholder types
8. **Comment strategy** with ranked action items
9. **What's coming next** (pending rules roadmap)

### Deployment

```bash
# Write to Nextcloud briefings
cp /tmp/briefing.html /data/nextcloud/data/amyn/files/briefings/filename.html

# Scan for Nextcloud index
docker exec --user www-data nextcloud php occ files:scan --path="/amyn/files/briefings"

# Verify via web
curl -s -o /dev/null -w "%{http_code}" https://brief.h.porb.dev/filename.html
```

## Pitfalls

- **FR API pagination:** Default is 20 results per page. Use `&per_page=100` for larger result sets, or handle `&page=N` pagination.
- **Date format trap:** Use `YYYY-MM-DD` for the API. The `publication_date[gte]` parameter is inclusive.
- **Comments close date:** Is always in the document metadata. Verify it — it's sometimes set to 60 days from publication, which may differ from what external briefings report.
- **Part 52 cross-cutting:** When multiple rules amend the same section (e.g., FAR Part 52 appears in all 4 RFO rules), combine them into one analysis — don't treat each rule's Part 52 changes as independent.
- **Plain text vs. XML:** The HTML version (`body_html_url`) renders for humans; the XML (`full_text_xml_url`) is easier to parse programmatically. Always prefer XML for extraction.
- **Character encoding:** FR XML is UTF-8. Some old documents may have HTML entities. Handle with `xml.etree.ElementTree` which handles both.
- **Agency field format:** Agencies in the FR API have nested structure (`parent_id`). Use `raw_name` for display.
- **Avoid duck-typing False patterns:** Never conclude "no matching sections found" because a regex didn't match — check the actual text format first. Different rulemakings use different section header conventions.
- **Shell quoting with `conditions[type][]` filters:** URL-encoding `conditions[type][]=RULE` inline in a curl string often gets mangled by the shell (the `[]` and `+` characters interact badly). The API's `type` filter for "Proposed Rule" as `PROPOSED+RULE` returns 0 results — the correct value is just `PRORULE`. For multi-value type filters, prefer `curl -G --data-urlencode` to avoid shell mangling, or use the broad `conditions[type]=RULE` (which returns both final and proposed rules) combined with term-based searches to catch proposed rules.
- **FederalRegister.gov blocks browser navigation.** Attempting `browser_navigate` to federalregister.gov URLs triggers bot detection ("Request Access" page with IP whitelist). Use `web_extract` instead — it bypasses this entirely and returns clean TOC content. NEVER use browser tools for federalregister.gov; ALWAYS use web_extract.
- **web_search is unreliable for .gov sites.** `web_search` may return empty results (`data.web: []`) for queries targeting federalregister.gov, whitehouse.gov, or regulations.gov — even for simple queries like "federal register today." Do not waste retries. Use `web_extract` for specific .gov URLs and browser navigation for whitehouse.gov (which does not block).
- **Negative results are reportable findings.** When covering a date window for GovCon intelligence, documenting that "zero CMMC/FedRAMP/FAR Council/SBIR rules were published this week" is itself valuable intelligence — include a negative-results table. Quiet periods for specific topics are meaningful to stakeholders tracking those pipelines.

## Related Skills

- `web-research` — General web research techniques for context about rulemakings; complements this skill's FR API focus
- `daily-briefing` — HTML briefing format, same Thariq/html-effectiveness aesthetic and Nextcloud/brief.h.porb.dev delivery pattern
- `home-server-service-audits` — Similar multi-agent orchestration pattern for parallel analysis

## Reference Files

- `references/executive-actions-research.md` — Cross-source methodology for White House executive actions (EOs, memoranda, proclamations, determinations, OMB memos) across FR API, whitehouse.gov, Google News RSS, and OMB memoranda page. Includes hard-date-window enforcement, signed-vs-published date pitfall, and worked example (Jun 30–Jul 7, 2026). Use when the task involves presidential actions rather than agency rulemakings.
- `references/document-archive-pipeline.md` — **Updated to v4 (8-persona framework).** Bulk document archive: FR API ingest → SQLite (separate analyses table) → heuristic T1 ($0) → adversarial review → T2 deep analysis via 3 parallel agents × 8 personas × 300 docs (~$18-30). Key changes from v2: expanded from 5 to 8 personas (added Economic, Implementation, Historical), recency-weighted selection (250 recent EOs + 50 high-impact procs), parallel 3-agent dispatch pattern, and cost estimates updated from $5-10 to $18-30.
- `references/far-rfo-extraction-patterns.md` — FAR RFO extraction patterns
- `references/govcon-weekly-fr-scan.md` — GovCon-focused weekly Federal Register scan methodology: web_extract-based daily issue review, agency filtering, impact tiering (HIGH/MODERATE/LOW), negative-results table, and structured output format. Use when scanning a date window specifically for GovCon-relevant items (procurement, defense, cybersecurity, small business, AI policy).
- `references/embedding-vector-pipeline.md` — Cheap vector embedding pipeline for document archives: OpenRouter-hosted Qwen3-Embedding-8B (4096 dim, float32, $0.01/M), SQLite BLOB storage, batch processing, and cosine similarity search. From the Trump EO archive build (1,391 docs embedded for $0.024). Use when adding semantic search to any document archive.
