# USASpending Bulk Pull → Interactive Dashboard Pipeline

## When to use this

The user asks to "pull ALL" SAM.gov/USASpending data — no limits, no filters, full dataset — and build an interactive dashboard from it. This is the "everything" workflow, distinct from targeted opportunity research or competitive landscape scanning.

## Architecture

```
USASpending API (free, no key)
  ├── /api/v2/search/spending_by_award/     → award-level data by NAICS
  │   ├── Query: {filters: {naics_codes: [...], award_type_codes: ["A","B","C","D"],
  │   │         time_period: [{start_date, end_date}]}, fields: [...], limit: 100}
  │   └── Paginate via `page` param; stop when hasNext=false or results empty
  │
  ├── /api/v2/awards/aggregate/             → agency-level rollups
  │   └── POST {group: "agency"}, read `amount` field (not aggregated_amount)
  │
  └── USASpending response field mapping    → compact keys for UI
      └── See "Field Name Mapping" below

Dashboard assembly (see "Assembly Pattern" below)
  ├── 1. Python script: query + save JSON files per NAICS
  ├── 2. Python: merge → analyze → export _unified_analysis.json (60-80KB)
  ├── 3. write_file: HTML skeleton with {{DATA_PLACEHOLDER}}
  └── 4. Terminal: patch data into placeholder → rescan Nextcloud
```

## USASpending API Recipes

### Award-level bulk query (`spending_by_award`)

```python
import requests, json

URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

NAICS_CODES = ["541611","541612","541613","541618","541614","541219","541519",
               "541511","541512","541513","541690","541715","541330","541990",
               "518210","561110","561990","611430","611310","611420",
               "611710","611430","611699","611710","541850","541820"]

ALL_FIELDS = [
    "Award ID", "Recipient Name", "Award Amount", "Description of Requirement",
    "Awarding Agency", "Awarding Sub Agency", "Start Date", "End Date",
    "NAICS", "naics_description", "Last Modified Date", "Base Obligation Date",
    "Contract Award Type", "Recipient UEI", "Current Total Value of Award",
    "Generated Unique Award ID"
]

def pull_naics(naics, fields=ALL_FIELDS, max_pages=10, start_date="2026-04-25"):
    """Pull all pages for one NAICS code."""
    all_results = []
    payload = {
        "filters": {
            "naics_codes": [naics],
            "award_type_codes": ["A","B","C","D"],
            "time_period": [{"start_date": start_date, "end_date": "2026-07-24"}]
        },
        "fields": fields,
        "limit": 100,
        "page": 1,
        "sort": "Base Obligation Date",
        "order": "desc"
    }
    for page in range(1, max_pages + 1):
        payload["page"] = page
        resp = requests.post(URL, json=payload, timeout=60)
        if resp.status_code != 200:
            break
        data = resp.json()
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        if not data.get("page_metadata", {}).get("hasNext"):
            break
    return all_results
```

**Caveats:**
- `fields` array is REQUIRED — 422 without it
- `award_type_codes` is REQUIRED. Contracts = ["A","B","C","D"]. Cannot mix with IDV type codes in same query
- NAICS code in response is a nested object: `award["NAICS"]["code"]` / `award["NAICS"]["description"]`
- `Description of Requirement` field is often NULL — it returns the field name but the content is empty for most records
- `page_metadata.total` is unreliable (may show 0 even when results exist). Paginate by `hasNext`
- Sort: `"Base Obligation Date"` for contracts (not `"Action Date"` — transaction-level field). IDV sort fields differ
- 100 results per page, ~10KB per page of JSON

### Agency rollup (aggregate)

```python
URL = "https://api.usaspending.gov/api/v2/awards/aggregate/"
payload = {
    "group": "agency",
    "filters": {
        "award_type_codes": ["A","B","C","D"],
        "time_period": [{"start_date": start_date, "end_date": end_date}],
        "naics_codes": NAICS_CODES
    }
}
resp = requests.post(URL, json=payload)
# Field name is `amount`, NOT `aggregated_amount`
agencies = resp.json().get("results", [])
```

### Terminal-based pull (safer for large data)

The Python `execute_code` tool can truncate large JSON outputs. For real bulk pulls, use a file-first approach:

```bash
# Save raw response to file first
python3 << 'PYEOF' > /tmp/pull_naics_data.py
import requests, json
...
PYEOF
python3 /tmp/pull_naics_data.py

# Then parse the saved file
cat /tmp/naics_541611.json
```

## Field Name Mapping (USASpending → Compact)

When building a dashboard UI, map USASpending's verbose field names to compact keys:

| USASpending Field | Compact Key | Notes |
|---|---|---|
| `Award ID` | `id` | String identifier |
| `Recipient Name` | `recipient` | Contractor name |
| `Awarding Agency` | `agency` | Toptier agency name |
| `Award Amount` | `amount` | Numeric > int for charting |
| `NAICS.code` | `naics` | String code e.g. "541611" |
| `NAICS.description` or `naics_description` | `naics_desc` | Text description |
| `Description of Requirement` | `desc` | Often NULL, fallback to empty string |
| `Base Obligation Date` | `start` | YYYY-MM-DD string |
| `End Date` / `Current End Date` | `end` | YYYY-MM-DD string |
| `Contract Award Type` | `type` | "Definitive Contract", "Purchase Order", etc. |

## Dashboard Assembly Pattern

### 1. Data generation (Python)

Build a unified analysis JSON with:
- `metadata`: total_awards, total_recipients, total_agencies, total_value, top_agency
- `agency_rollup`: array of {agency, count, total_value, avg_value, top_naics}
- `all_awards_sample`: full award list with compact field names (flattened NAICS objects)

Save to `/tmp/dashboard_data.json`.

### 2. HTML skeleton (write_file)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Dashboard Title</title>
  <style>/* full CSS inline */</style>
</head>
<body>
  <div class="wrap">
    <!-- Masthead -->
    <div class="masthead">...</div>
    <!-- Stats row -->
    <div id="stats-row" class="stat-grid"></div>
    <!-- All content sections -->
  </div>
  <script>
    const DATA = {{DATA_PLACEHOLDER}};
    // All render functions
  </script>
</body>
</html>
```

### 3. Data injection (terminal)

```bash
DATA=$(cat /tmp/dashboard_data.json)
python3 -c "
html = open('dash.html').read()
html = html.replace('{{DATA_PLACEHOLDER}}', DATA)
open('dash.html', 'w').write(html)
"
```

### 4. JS debugging

If the dashboard shows empty/zero data in one section but not others, the render function is using wrong field names. Debug via browser console:

```javascript
var s = DATA.all_awards_sample;
Object.keys(s[0]); // Returns actual field names
s[0]; // Check data shape for one record
```

### 5. Nextcloud deploy

```bash
docker exec --user www-data nextcloud php occ files:scan \
  --path="/amyn/files/briefings"
```

## Dashboard Sections (proven layout)

| Section | Content | Data Source |
|---|---|---|
| Stats Row | 4 metric cards: total awards, total value, recipients, agencies | `metadata` |
| Agency Command Center | Sortable/filterable table with search + sort dropdown | `agency_rollup` |
| NAICS Heatmap | Bar chart by NAICS code, color-coded by category | computed from `awards_sample` |
| Competitive Landscape | Top 15 contractors bar chart | `recipients` rollup |
| Top 25 Awards | Full-table ranked by amount | `awards_sample` sorted |
| Productization Scanner | Keyword-based pattern detection on descriptions | `desc` + `naics_desc` texts |
| SAM.gov Radar | Active opportunity counts (from browser scrape) | separate SAM.gov data |
| Positioning | Agency targeting, 30-day action plan | derived analysis |

## Pitfalls

- **Don't mix contract and IDV award_type_codes in one query.** Query separately.
- **`Description of Requirement` is NULL for most records.** Don't rely on it for classification. Use NAICS description instead.
- **Data JSON can exceed tool output limits.** Always save to file, don't try to display full JSON in terminal output.
- **60KB data JSON is at the edge of what `patch` tool can handle.** The placeholder replacement is a single string swap so it works, but the placeholder anchor `{{DATA_PLACEHOLDER}}` must be a simple text search — never a regex.
- **JS render functions must use compact field names** (`a.recipient` not `a["Recipient Name"]`), not the USASpending verbatim names. Test with `browser_console` before declaring done.
- **Browser console expressions can't use `return`** outside a function. Wrap in `(() => { ... })()` for multi-line debugging.
- **`browser_navigate` output truncates deep page content.** The snapshot is sufficient to confirm rendering. Use `browser_vision` for visual checks of chart layout.
