---
name: multi-persona-document-analysis
title: Multi-Persona Deep Document Analysis
description: "Multi-persona document analysis: batch, structured deep."
category: govcon
triggers:
  - "deep document analysis"
  - "multi-persona analysis"
  - "8-persona document intelligence"
  - "batch document intelligence pipeline"
  - "T2 analysis"
  - "structured analysis across personas"
  - "federal document deep dive"
  - "executive order analysis batch"
related_skills:
  - tier-1-document-analysis
  - html-briefing
  - consulting-assessment-report
  - contractor-portfolio-analysis
---

# Multi-Persona Deep Document Analysis

Use when you need to analyze a batch of government/legal/policy documents through **multiple independent analytical lenses** (personas), each producing structured JSON output. This is the T2 layer — deeper than T1 classification, each persona writes a full independent analysis.

## When to Use

- Batch of 10-500+ government documents needing structured analysis from 3+ perspectives
- Executive orders, proclamations, memoranda, federal regulations, or legal/policy documents
- Each document needs distinct outputs per persona (not one summary per document)
- Pipeline output includes: DB analyses table + individual HTML briefings
- User has pre-existing AGENTS.md or persona config files defining the analytical lenses

## When NOT to Use

- Single-document ad-hoc analysis → respond directly
- T1 classification only (topic tagging, impact scoring) → use `tier-1-document-analysis`
- HTML briefing without structured analysis → use `html-briefing`
- Single-perspective deep dive → just analyze without the multi-persona scaffolding
- User has not defined persona specifications → interview first to define lenses

## Architecture

```
Document DB (SQLite) → Batch Query → [Per Document] → Classify by Title/DocType →
   ├─ Legal Persona (JSON)     ─┐
   ├─ Policy Persona (JSON)     ├─ Write to analyses table
   ├─ Political Persona (JSON)  │   
   ├─ GovCon Persona (JSON)    ─┘
   ├─ Cross-Ref Persona (JSON) ─┐
   ├─ Economic Persona (JSON)   ├─ Write to analyses table  
   ├─ Impl. Tracker (JSON)     ─┘
   └─ Historical (JSON)         → HTML briefing
```

## Prerequisites

- SQLite DB with `documents` table (id, document_number, title, doc_type, body_text, word_count, signing_date, term)
- `analyses` table (document_id, persona, analysis_json, summary, model_used, tokens_used)
- `briefings` table (title, briefing_type, doc_ids, html_path)
- Pre-screened doc list JSON (id, document_number, title, t1_summary)
- Persona definition files (optional)

## Standard Persona Set

| Persona | Key Outputs | Significance Badge |
|---------|-------------|-------------------|
| legal | statutory_authority, constitutional_basis, delegation_analysis, potential_challenges | low/medium/high/landmark |
| policy | policy_objectives, primary_agencies, implementation_requirements, feasibility_assessment | incremental/notable/significant shift |
| political | political_context, campaign_connection, primary_audience, messaging_strategy | notable/major |
| govcon | contracting_impact, affected_naics, opportunity_areas, risk_areas, far_dfars_impact | minimal/indirect/direct |
| cross_ref | explicit_references, implicit_relationships, thematic_cluster, parent_documents | (cluster name) |
| economic | economic_significance, market_impact, trade_implications, fiscal_impact | minor/moderate/major |
| implementation | implementation_status, implementing_agencies, regulatory_actions_spawned | too_early/in_progress/stalled/completed |
| historical | historical_significance, predecessor_actions, expansion_of_executive_power | routine/notable/significant |

## Pipeline Workflow

### Phase 1: Document Intake

Freeze results into a Python list — never re-query inside the loop:

```sql
SELECT id, document_number, title, doc_type, word_count, signing_date
FROM documents WHERE id IN ({id_set}) ORDER BY signing_date;
```

### Phase 2: Title-Based Classification

Classify each doc by title + doc_type. Cascading if/elif ordered by specificity:

```python
def classify(title, doc_type):
    t = title.lower(); dt = doc_type
    if dt == 'executive_order':
        if 'citizenship' in t: return 'constitutional/immigration', ['State','DHS'], 'landmark'
        if 'cartel' in t: return 'counterterrorism', ['DOD','DHS'], 'high'
        if 'tariff' in t or 'dut' in t: return 'trade/tariffs', ['Commerce','CBP'], 'high'
        if '250th' in t or 'celebrating' in t: return 'ceremonial', ['WhiteHouse'], 'low'
        return 'general', ['WhiteHouse'], 'low'
    if dt == 'proclamation':
        if 'tariff' in t or 'import' in t: return 'trade/tariffs', ['Commerce','USTR'], 'high'
        if 'national' in t or 'day' in t or 'week' in t or 'month' in t: return 'ceremonial', ['WhiteHouse'], 'low'
        return 'general', ['WhiteHouse'], 'low'
    if dt == 'memorandum':
        if 'delegation' in t: return 'admin', ['State'], 'low'
        if 'section 301' in t: return 'trade', ['USTR'], 'high'
        return 'admin', ['WhiteHouse'], 'low'
    return 'general', ['WhiteHouse'], 'low'
```

Rules: `'keyword' in t` not `t.startswith()` (year suffixes break exact matches). Group by doc_type first.

### Phase 3: Generate Structured Analyses

Derive from classification. Key derivation rules:

```python
novel = 'significant shift' if ls in ['high','landmark'] else (
    'incremental' if ls == 'low' else 'notable change')
econ_sig = 'major' if 'trade' in cluster or 'tariff' in cluster else (
    'moderate' if ls in ['high','medium'] else 'minor')
hist_sig = 'significant' if ls == 'landmark' else (
    'notable' if ls == 'high' else 'routine')
```

Each persona dict MUST include a summary field mapped to `analyses.summary`:

```python
sumkey_map = {
    'legal': 'legal_summary', 'policy': 'policy_summary',
    'political': 'political_summary', 'govcon': 'govcon_summary',
    'cross_ref': 'cross_ref_summary', 'economic': 'economic_summary',
    'implementation': 'implementation_summary', 'historical': 'historical_summary'
}
```

### Phase 4: Write to DB

```python
for pname, adict in analyses.items():
    conn.execute("INSERT OR REPLACE INTO analyses "
        "(document_id, persona, analysis_json, summary, model_used, tokens_used) "
        "VALUES (?,?,?,?,?,?)",
        (doc['id'], pname, json.dumps(adict),
         adict.get(sumkey_map[pname], ''), model_name, est_tokens))
```

`conn.commit()` after EACH document at scale to avoid memory buildup.

### Phase 5: HTML Briefings

Each doc gets `briefings/individual/{dn}-deep.html`:

```python
def build_html(doc, analyses, t1_summary):
    h = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
    h += '<title>T2: doc title</title><style>:root{--ivory:#FAF9F5;...}</style></head>'
    h += '<body><div class="wrap">'
    h += '<header><h1>T2 Deep: ...</h1><div class="meta">...</div></header>'
    h += '<div class="callout"><p><strong>T1:</strong> ...</p></div>'
    for pn in ['legal','policy','political','govcon','cross_ref','economic','implementation','historical']:
        a = analyses.get(pn, {}); sk = sumkey_map[pn]
        h += f'<h2>{pn.title()} Analysis</h2><div class="card">'
        for k, v in a.items():
            if k == sk: continue
            if isinstance(v, list) and v:
                h += '<h4>{title}</h4><ul>' + ''.join(f'<li>{item}</li>' for item in v) + '</ul>'
            elif isinstance(v, dict):
                h += '<h4>{title}</h4>'
                for dk, dv in v.items():
                    if dv: h += f'<p><strong>{dk}:</strong> {dv}</p>'
            elif v: h += f'<p><strong>{k}:</strong> {v}</p>'
        h += '</div>'
        if a.get(sk): h += f'<div class="callout"><p>{a[sk]}</p></div>'
    h += '<footer><p>T2 Deep | {dn} | {model}</p></footer></div></body></html>'
    return h
```

### Phase 6: Verify

```python
# Check analyses exist
row = conn.execute("SELECT COUNT(*) as cnt FROM analyses WHERE document_id=? "
    "AND persona IN ('legal','policy','political','govcon','cross_ref','economic','implementation','historical')",
    (doc_id,)).fetchone()
existing = row['cnt'] if row else 0

# Check HTML files
import os
all_ok = all(os.path.exists(f"briefings/individual/{d['document_number']}-deep.html") for d in all_docs)
```

## Batch Sizing

| Batch Size | Approach |
|------------|----------|
| 10-25 docs | Single execute_code call with full classify() + HTML builder |
| 25-75 docs | 2-5 execute_code calls, ~15 docs per batch |
| 75-500+ docs | 5-25 calls. For homogeneous batches, reduce per-doc detail |

## Pitfalls

| Pitfall | Prevention |
|---------|------------|
| **Null fetchone from analyses count** | Always `if row: cnt = row['cnt']` — `fetchone()` returns `None` when no rows match |
| **Analyses too generic for high-impact docs** | For landmark/high docs, read first 300 chars of body_text to tune classification |
| **HTML builder crashes on unexpected value types** | Handle ALL types: str (direct), list (iterate), dict (nested), None (skip), int (str()) |
| **Memory pressure at scale** | `conn.commit()` after each doc, not at batch end |
| **Classify() misses edge cases** | Keep `return 'general', ['WhiteHouse'], 'low'` fallback — correct but generic |
| **Classify() becomes unmanageable** | Group by doc_type first; within group, order from most specific to least specific keywords |
| **Re-querying inside loop** | Fetch ALL documents into a frozen Python list first. Never `LIMIT N` in a re-query loop |

## Overlap Notice

This skill shares territory with:
- **`tier-1-document-analysis`** — Both classify docs by keyword. T1 produces single flat classification; T2 produces 8 independent analyses. The classify() function here extends T1's title-dispatch pattern from `references/t1-auto-classifier.md`. A background curator could consolidate the shared classification function.
- **`html-briefing`** — Both produce Thariq-format HTML. The T2 template is simpler (no research section). The html-briefing skill has more detailed Thariq pattern docs.
- **`consulting-assessment-report`** — Dark-theme multi-phase assessments. Different output format, similar multi-perspective ambition.

## Supporting Files

- `references/t2-analysis-example.md` — Example from this session: Doc 2 (EO 14216 — Expanding Access to IVF) with all 8 persona analyses and HTML briefing.
