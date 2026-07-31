# Embedding / Vector Search Pipeline for Document Archives

A repeatable pattern for adding semantic search to any FR API document archive using cheap embedding models via OpenRouter + SQLite native vector storage. Built during the Trump EO archive project (1,391 docs, $0.0242 total).

## Architecture

```
SQLite (documents table)
    │
    ▼
┌──────────────────────┐
│  scripts/embed.py    │  ← body_text → OpenRouter API → vector
│                      │      Qwen3-Embedding-8B, 4096 float32 dims
│                      │      Batch 20 docs/call, ~5 sec/batch
│                      │      Total cost: ~$0.02/1,400 docs
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  embeddings table    │  ← BLOB (4096 × float32 = 16KB/doc)
│                      │      ON CONFLICT DO UPDATE
│  queries via         │
│  embed.py --search   │  ← cosine similarity inline
└──────────────────────┘
```

## Model Selection

| Model | Dimensions | Price/MTok | Context | Notes |
|-------|-----------|-----------|---------|-------|
| **Qwen3-Embedding-8B** (qwen/qwen3-embedding-8b) | 4096 | $0.01 | 32K | MRL support, best quality/$ ratio |
| text-embedding-3-small (OpenAI) | 1536 | $0.02 | 8K | Smaller, faster, less nuanced |
| text-embedding-3-large (OpenAI) | 3072 | $0.13 | 8K | 13× cost, marginal quality gain |

**Recommendation:** Qwen3-Embedding-8B via OpenRouter is the clear winner for bulk pipelines. 4096 dims at $0.01/M is ~5× cheaper than the next best option for comparable quality.

## Embeddings Table Schema

```sql
CREATE TABLE IF NOT EXISTS embeddings (
    document_id INTEGER PRIMARY KEY,
    vector BLOB NOT NULL,              -- 16,384 bytes (4096 × float32)
    model TEXT NOT NULL DEFAULT 'qwen/qwen3-embedding-8b',
    dimensions INTEGER NOT NULL DEFAULT 4096,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
```

## Embedding Script Structure

### Python Implementation

```python
import requests
import struct
import sqlite3
import json
import hashlib
import time

API_URL = "https://openrouter.ai/api/v1/embeddings"
HEADERS = {
    "Authorization": "Bearer <OPENROUTER_KEY>",
    "Content-Type": "application/json"
}
MODEL = "qwen/qwen3-embedding-8b"
BATCH_SIZE = 20
DIMENSIONS = 4096

def embed_texts(texts):
    """Embed a list of texts. Returns list of float32 vectors."""
    if not texts:
        return []
    resp = requests.post(API_URL, headers=HEADERS, json={
        "model": MODEL,
        "input": texts[:BATCH_SIZE]
    }, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return [item["embedding"] for item in data["data"]]

def vector_to_blob(vector):
    """Convert float32 list to 16KB SQLite BLOB."""
    return struct.pack(f'{len(vector)}f', *vector)

def blob_to_vector(blob):
    """Convert SQLite BLOB back to float32 list."""
    return list(struct.unpack(f'{len(blob)//4}f', blob))

def cosine_similarity(vec_a, vec_b):
    """Native Python cosine similarity (no numpy dependency)."""
    dot = sum(a*b for a, b in zip(vec_a, vec_b))
    n_a = sum(a*a for a in vec_a) ** 0.5
    n_b = sum(b*b for b in vec_b) ** 0.5
    return dot / (n_a * n_b) if n_a and n_b else 0.0

def embed_all_docs(db_path):
    """Embed all documents that don't have embeddings yet."""
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    # Get docs without embeddings
    cursor.execute("""
        SELECT d.id, d.body_text
        FROM documents d
        LEFT JOIN embeddings e ON d.id = e.document_id
        WHERE d.body_text IS NOT NULL AND e.document_id IS NULL
        ORDER BY d.id
    """)
    docs = cursor.fetchall()
    
    total = len(docs)
    batch = []
    cost_est = 0.0
    
    for idx, (doc_id, body_text) in enumerate(docs, 1):
        # Truncate to 32K tokens
        text = body_text[:32000]
        batch.append((doc_id, text))
        
        if len(batch) >= BATCH_SIZE or idx == total:
            texts = [t for _, t in batch]
            ids = [i for i, _ in batch]
            
            vectors = embed_texts(texts)
            
            for doc_id, vector in zip(ids, vectors):
                blob = vector_to_blob(vector)
                cursor.execute("""
                    INSERT INTO embeddings (document_id, vector, model, dimensions)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(document_id) DO UPDATE SET
                        vector = excluded.vector,
                        model = excluded.model,
                        dimensions = excluded.dimensions,
                        updated_at = datetime('now')
                """, (doc_id, blob, MODEL, DIMENSIONS))
            
            db.commit()
            print(f"  [{idx}/{total}] Batch OK ({len(batch)} docs, est. ${cost_est:.4f} total so far)")
            batch = []
            
            # Rate limiting
            time.sleep(0.5)
    
    db.close()
    print(f"\nDone. {total} documents embedded.")
```

### Semantic Search

```python
def search(db_path, query, top_k=10):
    """Search documents by semantic similarity to query text."""
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    # Embed query
    resp = requests.post(API_URL, headers=HEADERS, json={
        "model": MODEL,
        "input": [query]
    }, timeout=60)
    resp.raise_for_status()
    query_vec = resp.json()["data"][0]["embedding"]
    
    # Load all embeddings (small DB — 1,400 × 16KB = ~22MB)
    cursor.execute("""
        SELECT e.document_id, e.vector, d.document_number, d.title, d.doc_type, d.signing_date
        FROM embeddings e
        JOIN documents d ON e.document_id = d.id
    """)
    
    results = []
    for doc_id, blob, doc_num, title, doc_type, date in cursor.fetchall():
        vec = blob_to_vector(blob)
        sim = cosine_similarity(query_vec, vec)
        results.append((sim, doc_id, doc_num, title, doc_type, date))
    
    results.sort(reverse=True)
    db.close()
    return results[:top_k]
```

### CLI Interface

```python
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", help="Semantic search query")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--db", default="data/eo.db")
    args = parser.parse_args()
    
    DB_PATH = args.db
    
    if args.search:
        results = search(DB_PATH, args.search, args.top)
        print(f"\nTop {len(results)} results for: \"{args.search}\"")
        print(f"\n  {'#':>3}  {'Sim':>6} Type    Num       Date  Title")
        print("-" * 90)
        for i, (sim, doc_id, doc_num, title, doc_type, date) in enumerate(results, 1):
            doc_type_short = "exec" if doc_type == "executive_order" else \
                           "proc" if doc_type == "proclamation" else "memo"
            title_trunc = title[:60] if len(title) > 60 else title
            print(f"  {i:>3}  {sim:.4f}  {doc_type_short:<5} {doc_num:<18} {date or '':10}  {title_trunc}")
    else:
        embed_all_docs(DB_PATH)
```

## Cost Math

| Batch Size | Docs | Cost Estimate | Time |
|-----------|------|--------------|------|
| 20 | 1,391 | $0.024 | ~7 min |
| 20 | 10,000 | $0.17 | ~50 min |
| 20 | 100,000 | $1.70 | ~8.5 hr |

The input is the text to embed (1,391 docs × ~6K tokens avg = ~8.3M tokens = $0.083 at $0.01/M input). The cost comes out lower in practice because many docs are short (<2K tokens).

## Pitfalls

- **struct.pack overflow.** Python `struct.pack` with `4096f` creates a 16,384-byte blob. Verify with `len(blob)` before writing. If dimensions change (e.g., swapping to a 1536-dim model), update the format string.
- **ORM impedance.** Do NOT use an ORM for embedding storage. Raw SQLite with BLOBs and `struct` is faster than any ORM at this scale.
- **SQLite memory for search.** Loading all 1,400 vectors into memory is ~22 MB (1,400 × 16 KB). Fine for SQLite. For >50K docs, switch to a vector DB (pgvector, qdrant, chromadb) or paginate the scan.
- **MRL dimensions.** Qwen3-Embedding-8B supports Matryoshka Representation Learning. You can truncate the output vector to 1024 or 2048 dims for faster search at minor accuracy loss. Pass `input_type: "passage"` in the API request for documents, omit for short queries.
- **Text length limit.** Qwen3-Embedding-8B has 32K context. Truncate body_text to ~32K chars before embedding. Longer documents lose tail — consider chunking for very long docs (>50K chars).
- **Rate limiting.** OpenRouter imposes ~350 RPM for most models. Batching at 20 docs/call with 0.5s delay stays well under this (~120 RPM).
- **SQLite WAL during batch writes.** If the DB is modified during embedding (e.g., concurrent full-text fetch), the embeddings table may lag. Lock or sequence writes: full text → embed → analyze, not interleaved.
- **dimensions config drift.** If you change models mid-run, the dimensions column tracks what you used. Always check `dimensions` when converting BLOBs back to vectors — `struct.unpack` length is derived from blob length, so different dimensions silently produce different-length lists.
- **Updated_at tracking.** The `updated_at` column defaults to now() but needs an explicit column definition, not a generated or computed column. `ALTER TABLE` with `DEFAULT` works but must be done before writes.

## When NOT to Use This Pattern

- **One-off search queries** — just search the live FR API or use web_extract. Don't build a vector DB for a single query.
- **Real-time search on very large datasets** (>100K docs) — the full-scan-over-SQLite approach works for 1-20K docs, but beyond that use pgvector, qdrant, or another vector DB.
- **Documents where text is under 200 chars** — embedding noise won't produce meaningful similarity scores.
- **User explicitly wants a different model** (e.g. OpenAI text-embedding-3-large) — respect the choice.
