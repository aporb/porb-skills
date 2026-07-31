# Document Archive Pipeline: Bulk FR API → SQLite → Multi-Stage Analysis

A repeatable pattern for ingesting ALL documents of a given type from the Federal Register API, storing in SQLite, bulk-extracting full text, vector embeddings, and staged multi-persona analysis with parallel agent dispatch.

## When to Use

- "Build a complete queryable archive of all Trump EOs, proclamations, and memoranda"
- "Archive all Biden proclamations for analysis"
- Any task with scope of **hundreds to thousands of FR documents** needing a queryable local store with semantic search and staged persona analysis

## Architecture (8-Persona v4)

```
FR API (no keys, no rate limits)
    │
    ▼
┌──────────────────────────┐
│  scripts/ingest.py       │  ← API → SQLite (metadata + dates + FR#)
│                          │      per_page=1000, incremental
└────────┬─────────────────┘
         │
         ▼
┌───────────────────────────────┐
│ scripts/fetch_full_text.py    │  ← body_html_url → cleaned text
│                               │      BeautifulSoup + html.parser
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│  Vector Embeddings (optional) │  ← Qwen3-Embedding-8B via OpenRouter
│  scripts/embed.py             │      4096 dims, ~$0.02/1,400 docs
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│  T1: Heuristic Classification │  ← Regex-based: topics, impact, urgency
│  (all docs, ~2 min, $0)       │      No LLM cost. All docs get HTML briefings
└───────────┬───────────────────┘
            │
            ▼
┌───────────────────────────────┐
│  Adversarial Review            │  ← Independent audit: DB integrity, design
│                               │      compliance, score distributions
└───────────┬───────────────────┘
            │
            ▼
┌────────────────────────────────────────────┐
│  T2: Deep Persona Analysis (300 docs)      │
│  ───────────────────────────────────       │
│   3 parallel agents × 100 docs × 8 personas│
│                                            │
│   1. Legal Analyst                         │
│   2. Policy Analyst                        │
│   3. Political Analyst                     │
│   4. GovCon Analyst                        │
│   5. Cross-Reference                       │
│   6. Economic Analyst  ✨ (v4 addition)    │
│   7. Implementation Tracker ✨ (v4)        │
│   8. Historical-Comparative ✨ (v4)         │
│                                            │
│   → Deep HTML briefings per doc            │
└───────────┬────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│  T3: Cross-Reference Synthesis  │  ← Thematic clustering, temporal mapping
│  (post-T2)                      │      Aggregate briefings per theme
└─────────────────────────────────┘
```

## Phase 0: FR API Discovery

```bash
curl -s "https://www.federalregister.gov/api/v1/documents.json?conditions%5Btype%5D%5B%5D=PRESDOCU&conditions%5Bpresident%5D%5B%5D=donald-trump&per_page=1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count', 'unknown'))"
```

President slugs: `donald-trump` (2017-2021 + 2025+), `joseph-r-biden-jr`, `barack-obama`.

Document subtypes: `executive_order` (has `executive_order_number`), `proclamation`, `memorandum` (uses `document_number` only).

### fields[] encoding quirk — ALWAYS use requests params dict

```python
params = {
    "conditions[type][]": ["PRESDOCU"],
    "conditions[president][]": ["donald-trump"],
    "per_page": 1000,
    "fields[]": ["title", "subtype", "executive_order_number", "body_html_url", "publication_date", "document_number"]
}
resp = requests.get(url, params=params)
```

Manual URL encoding double-encodes brackets. Always use `params=`.

## Phase 1: SQLite Schema

Uses separate `analyses` table — adding personas requires no migration.

### documents table

```sql
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_number TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    doc_type TEXT NOT NULL DEFAULT 'executive_order',
    executive_order_number TEXT,
    signing_date TEXT,
    publication_date TEXT,
    president TEXT DEFAULT 'donald-trump',
    term INTEGER,
    body_text TEXT,
    word_count INTEGER DEFAULT 0,
    scraped_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

### analyses table (one row per persona per doc)

```sql
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    persona TEXT NOT NULL,
    analysis_json TEXT,
    summary TEXT,
    model_used TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    UNIQUE(document_id, persona)
);
```

### embeddings table

```sql
CREATE TABLE IF NOT EXISTS embeddings (
    document_id INTEGER PRIMARY KEY,
    vector BLOB NOT NULL,
    model TEXT NOT NULL DEFAULT 'qwen/qwen3-embedding-8b',
    dimensions INTEGER NOT NULL DEFAULT 4096,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
```

### Full text extraction

```python
def fetch_and_clean(url):
    import requests; from bs4 import BeautifulSoup; import re
    resp = requests.get(url, timeout=15)
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.find('div', id='content')
    text = content.get_text(separator='\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
```

Signed date from last paragraph: `r'THE WHITE HOUSE,\s+([A-Z][a-z]+ \d+, 20\d{2})'`.

## Phase 2: Repository Structure

```
repo/
├── data/eo.db                    # SQLite (gitignored)
├── data/raw/                     # Raw HTML (gitignored)
├── briefings/individual/         # Per-doc HTML briefings (gitignored)
├── scripts/
│   ├── ingest.py                 # FR API → SQLite
│   ├── fetch_full_text.py        # body_html_url → cleaned text
│   ├── query.py                  # CLI: --stats, --search, --eo, --topic
│   ├── embed.py                  # Vector embeddings
│   └── t1_batch_processor.py     # Heuristic T1 classifier
├── agents/personas/              # 8 persona definition files
│   ├── legal-analyst.md, policy-analyst.md, political-analyst.md, govcon-analyst.md
│   ├── cross-reference.md, economic-analyst.md, implementation-tracker.md
│   └── historical-comparative.md
├── AGENTS.md                     # Agent instruction manual (MANDATORY)
└── README.md
```

### The 8-Persona Framework

| # | Persona | Core Question | Est. Tokens |
|---|---------|--------------|-------------|
| 1 | Legal Analyst | What authority, vulnerability to challenge? | ~5K |
| 2 | Policy Analyst | Objective, feasibility? | ~5K |
| 3 | Political Analyst | Audience, political context? | ~5K |
| 4 | GovCon Analyst | Federal contractor/procurement impact? | ~5K |
| 5 | Cross-Reference | Relationship to other corpus docs? | ~5K |
| 6 | **Economic Analyst** | Market, trade, fiscal, industry effects? | ~6K |
| 7 | **Implementation Tracker** | What actually happened after signing? | ~6K |
| 8 | **Historical-Comparative** | Precedents, executive power expansion? | ~6K |

Why the three additions: Economic (Trump's signature domain is tariffs/trade — GovCon only covers procurement), Implementation (gap between what EOs say and do is the most journalistically valuable angle), Historical (provides institutional memory across administrations).

## Phase 2.5: Vector Embeddings

See `references/embedding-vector-pipeline.md`. Key numbers: Qwen3-Embedding-8B via OpenRouter, 4096 dims, 1,391 docs for $0.024 total.

## Phase 3: T1 Batch Analysis (Heuristic, NOT LLM)

Regex-based classifier. ~2 min for 1,400 docs. Cost: $0.

Output fields: summary, topics (controlled taxonomy), impact_score (1-10), section_count, primary_agencies, urgency (immediate/phased/routine/ceremonial), is_ceremonial.

## Phase 3.5: Adversarial Review (MANDATORY before T2)

Independent audit of DB integrity, HTML design compliance, score distribution anomalies, schema issues.

## Phase 4: T2 Deep Persona Analysis — Parallel Dispatch

### Selection criteria (recency-weighted, not pure impact)

Top 250 most recent EOs + 50 high-impact procs/memos (impact_score >= 6) = 300 docs.

### Dispatch pattern: 3 parallel agents × 100 docs each

```python
delegate_task(tasks=[
    {"goal": "T2 Agent 1 — docs #1-#100 (most recent EOs)", ...},
    {"goal": "T2 Agent 2 — docs #101-#200", ...},
    {"goal": "T2 Agent 3 — docs #201-#250 + 50 procs/memos", ...},
])
```

Each agent reads AGENTS.md + all 8 persona files. For each doc: runs 8 persona analyses → writes to analyses table → generates `briefings/individual/{doc_number}-deep.html`.

### T2 Cost: 300 × 8 × ~6K tokens ≈ ~$18-30

## Pitfalls

- **fields[] URL encoding.** Always use `requests.get(url, params=...)`.
- **per_page=1000 works.** Don't assume standard limits.
- **signed ≠ published.** FR publishes days after signing. Store both dates.
- **DB lock during bulk ingest.** Don't parallelize reads/writes.
- **T1 is heuristic, not LLM.** Don't waste LLM cost on bulk classification.
- **T2 sub-agents take 6-8 hours.** 100 docs × 8 persona analyses × ~30s each. Monitor live transcripts via `tail -f .hermes/cache/delegation/live/deleg_*/task-*.log`.
- **Ceremonial proclamations (~35%).** Skip T2 for is_ceremonial=true.
- **Memoranda have no eo_number.** Query by document_number.
- **Sub-agent JSON output is unreliable.** Always validate schema in orchestrator before writing to DB.
