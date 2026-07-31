---
name: inspect-eval
description: Score new deliverables against a 50-brief gold set using Inspect AI. Continuous-eval loop for output quality drift. Bootstrap starts with 10 gold; grows via accepted-deliverable promotion.
version: 0.1.0
tags: [quality, eval, inspect-ai, harbor, measurement]
tier: A
owning_profile: reviewer
moat_test: "Gold set is composed of Amyn's actually-approved HARBOR deliverables — domain-specific quality baseline. Not generic LLM eval."
---

# Inspect Eval

Continuous-eval loop. Every accepted deliverable enters the gold set; every new draft is scored against the closest gold of its type. Drift trends surface in weekly ops review.

**One-line:** You can't fix what you can't score.

## Status (initial bootstrap)

This is **v0.1** — bootstrap. The full v1 needs 50 gold deliverables per `v2.0 §3.4`. Bootstrap target: 10 across types. Grows weekly.

## When to load this skill

- After `adversarial-reviewer` returns `verdict: ship` and before delivery — scores against gold, flags drift
- Weekly: full eval pass over the prior week's deliverables for the weekly ops review

## Setup

### Phase A — Install Inspect AI

```bash
/Users/amynporb/.hermes/hermes-agent/venv/bin/pip install inspect-ai
```

### Phase B — Bootstrap gold set

`~/.hermes/state/gold-set/` directory structure:
```
gold-set/
  daily-briefing/
    2026-05-22-daily.json        # extracted from daily-2026-05-22.html
    2026-05-19-daily.json
    ...
  engagement-brief/
    2026-05-22-engagement.json
    ...
  pre-assessment/
    ace-of-cloud-2026-05-19.json   # extracted from Ace-of-Cloud-HARBOR-Assessment-2026-05-19.html
    soal-2026-05-10.json
  intel-canvas/
    ace-of-cloud-canvas-2026-05-19.json
  meeting-prep/
    north-ai-tim-otto-2026-05-20.json
```

Each gold sample has shape:
```json
{
  "type": "pre-assessment",
  "path": "/Users/amynporb/Documents/Briefings/Ace-of-Cloud-HARBOR-Assessment-2026-05-19.html",
  "ingested_at": "2026-05-25T...",
  "rubric_anchors": {
    "factual_density": 4.5,
    "citation_density": 4.8,
    "tone_alignment": 4.2,
    "structural_completeness": 5.0,
    "actionability": 4.6
  },
  "characteristic_excerpts": [
    {"dimension": "factual_density", "passage": "..."},
    ...
  ],
  "metadata": {
    "client": "ace-of-cloud",
    "lens": "federal",
    "word_count": 4250,
    "sections_count": 6
  }
}
```

### Phase C — Bootstrap script

`~/.hermes/scripts/bootstrap-gold-set.py`:

```python
#!/usr/bin/env python3
"""Initial gold set: 10 deliverables across 4 types from existing approved artifacts."""
from pathlib import Path
import json, re

GOLD = Path("/Users/amynporb/.hermes/state/gold-set")
GOLD.mkdir(parents=True, exist_ok=True)
BR = Path("/Users/amynporb/Documents/Briefings")

# Type-specific source files (Amyn-approved)
SOURCES = {
    "daily-briefing":   [BR / f"daily-2026-05-{d}.html" for d in ["19","22","23","24","25"]],
    "engagement-brief": [BR / f"engagement-2026-05-{d}.html" for d in ["19","22","24"]],
    "pre-assessment":   [BR / "Ace-of-Cloud-HARBOR-Assessment-2026-05-19.html",
                         BR / "Soal-Technologies-HARBOR-Assessment-2026-05-10.html"],
    "intel-canvas":     [BR / "ace-of-cloud-intelligence-canvas-2026-05-19.html"],
    "meeting-prep":     [BR / "north-ai-tim-otto-meeting-prep-2026-05-20.html"],
    "competitive-canvas":[BR / "north-ai-govradar-competitive-canvas-2026-05-19.html"],
}

# Default rubric anchors — start at 4.5/5 for these proven artifacts; the reviewer can
# downgrade specific dimensions per artifact if it finds gaps.
DEFAULT_ANCHORS = {
    "factual_density": 4.5,
    "citation_density": 4.5,
    "tone_alignment": 4.5,
    "structural_completeness": 4.5,
    "actionability": 4.5,
}

for kind, files in SOURCES.items():
    (GOLD / kind).mkdir(exist_ok=True)
    for f in files:
        if not f.exists():
            print(f"skip (missing): {f}")
            continue
        slug = f.stem
        text = f.read_text(encoding="utf-8", errors="ignore")
        sample = {
            "type": kind,
            "path": str(f),
            "ingested_at": "2026-05-25T22:00:00Z",
            "rubric_anchors": dict(DEFAULT_ANCHORS),
            "characteristic_excerpts": [],   # populate later via reviewer
            "metadata": {
                "word_count": len(re.findall(r"\b\w+\b", text)),
                "sections_count": len(re.findall(r"<h[12]", text, re.IGNORECASE)),
            }
        }
        out = GOLD / kind / f"{slug}.json"
        out.write_text(json.dumps(sample, indent=2))
        print(f"wrote {out}")

print(f"\nTotal gold: {sum(1 for _ in GOLD.rglob('*.json'))} samples across {len(SOURCES)} types")
```

### Phase D — Eval task

`~/.hermes/scripts/inspect-eval.py`:

```python
#!/usr/bin/env python3
"""Score a new draft against the closest gold samples of its type."""
import argparse, json
from pathlib import Path
import re

GOLD = Path("/Users/amynporb/.hermes/state/gold-set")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True, type=Path)
    ap.add_argument("--type", required=True)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    gold_dir = GOLD / args.type
    if not gold_dir.exists():
        print(json.dumps({"error": f"no gold for type '{args.type}'"}))
        return 1
    samples = list(gold_dir.glob("*.json"))
    if not samples:
        print(json.dumps({"error": f"no gold samples in {gold_dir}"}))
        return 1

    # Top-3 closest by word-count similarity (cheap baseline; v0.2 swaps in embeddings)
    draft_text = args.draft.read_text(encoding="utf-8", errors="ignore")
    draft_wc = len(re.findall(r"\b\w+\b", draft_text))
    ranked = sorted(samples, key=lambda s: abs(json.loads(s.read_text())["metadata"]["word_count"] - draft_wc))[:3]

    # For each candidate gold, compare on 5 dimensions and compute deltas.
    # v0.1 uses placeholder scoring; v0.2 invokes inspect-ai with an llm-jury scorer.
    deltas = []
    for g_path in ranked:
        gold = json.loads(g_path.read_text())
        deltas.append({
            "gold": g_path.name,
            "gold_anchors": gold["rubric_anchors"],
            "draft_estimated": {k: None for k in gold["rubric_anchors"]},  # to be filled by llm-jury in v0.2
            "delta": "TODO: invoke inspect-ai llm-jury here"
        })

    args.out.write_text(json.dumps({
        "draft_path": str(args.draft),
        "type": args.type,
        "compared_against": [s.name for s in ranked],
        "deltas": deltas,
        "version": "0.1-bootstrap"
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## Workflow when invoked per draft

1. Reviewer returns `verdict: ship` for a daily-briefing.
2. Call: `python3 inspect-eval.py --draft ~/Documents/Briefings/daily-2026-05-26.html --type daily-briefing --out /tmp/eval-result.json`
3. In v0.1: returns word-count-nearest gold + placeholders. Logs the draft as "would-eval".
4. In v0.2 (TBD): inspect-ai dispatches an LLM jury (3-judge ensemble, deepseek-v4-flash + claude-haiku-4.5 + glm-4.7) to score each dimension. Drift = mean(draft_scores) - mean(gold_anchors). Drift > 0.5 in any dimension triggers an alert in the next weekly ops review.

## Growth path

Each accepted deliverable (Amyn approves via Telegram thumb-up or `post-queue approve`) becomes a candidate for gold-set promotion. Monthly review:
1. List all "would-eval" entries from past month.
2. Pick ~5-10 to promote — those Amyn explicitly approved + that are best-of-type.
3. Run the bootstrap script's anchor-scoring on them (currently default 4.5; v0.2 derives from reviewer).
4. Add to `gold-set/<type>/`.

## v0.2 backlog

- LLM-jury scoring (3 judges, ensemble)
- Embedding-based nearest-gold selection (instead of word-count)
- Auto-promotion: accepted-deliverable confidence_score ≥ 95 auto-promotes after 7-day cooling window
- Weekly drift dashboard in ops review
- Rubric-anchor evolution (anchors update as the gold set grows)

## Related

- v2.0 §3.4
- HARBOR Constitution (the rubric)
- Weekly ops review skill (consumes review-log.jsonl)
