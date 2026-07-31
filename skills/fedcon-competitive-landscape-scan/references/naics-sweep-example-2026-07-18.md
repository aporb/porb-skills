# NAICS Sweep Example — 2026-07-18

## Configuration

```
Date Range: 2026-01-19 to 2026-07-18 (180 days)
NAICS: 541611, 541519, 611430, 541618, 541690
Award Band: $0–$500,000
Competitors: GOVSMART, V3GATE, FCN, THUNDERCAT, ADVANCED COMPUTER CONCEPTS,
             PROMETHEUS COMPUTING, REDHAWK IT SOLUTIONS, NEW TECH SOLUTIONS,
             BLUE TECH, COUNTERTRADE, ACCESSAGILITY
```

## Results

- **12,454** unique awards from **62** agencies
- **$1.49B** total obligated spending
- **4,423** unique recipients
- **676** SDVOSB awards (5.4% of total), **$90.7M** SDVOSB spending
- **3,198** awards expiring before Dec 2026 (1,499 at ≥$100K)

## Agency Rankings (Top 15 by Spending)

| Rank | Agency | Spending | Awards | SDVOSB % |
|------|--------|----------|--------|----------|
| 1 | Department of Defense | $221M | 1,663 | 2.0% |
| 2 | Department of Health and Human Services | $162M | 907 | 0.6% |
| 3 | Department of Veterans Affairs | $133M | 895 | **49.4%** |
| 4 | Department of Justice | $110M | 857 | 2.5% |
| 5 | Department of State | $105M | 559 | 9.1% |
| 6 | Department of the Treasury | $83M | 475 | 3.6% |
| 7 | Department of Homeland Security | $79M | 485 | 2.7% |
| 8 | Department of Commerce | $78M | 496 | 1.8% |
| 9 | Department of Transportation | $77M | 466 | 1.1% |
| 10 | Department of the Interior | $74M | 539 | 0.6% |
| 11 | Department of Energy | $49M | 281 | 3.0% |
| 12 | Department of Agriculture | $44M | 240 | 2.0% |
| 13 | NASA | $40M | 476 | 5.0% |
| 14 | Environmental Protection Agency | $29M | 142 | 0.0% |
| 15 | Department of Labor | $28M | 128 | 18.0% |

## Competitor Rankings

| Competitor | Awards | Total Value | SDVOSB? | SDVOSB Value |
|------------|--------|-------------|---------|--------------|
| NEW TECH SOLUTIONS | 492 | $74.9M | No | $0 |
| FCN | 447 | $56.1M | No | $0 |
| ADVANCED COMPUTER CONCEPTS | 444 | $38.2M | No | $0 |
| THUNDERCAT | 341 | $49.3M | **Yes** | $6.4M |
| COUNTERTRADE | 318 | $23.8M | No | $0 |
| V3GATE | 269 | $18.8M | **Yes** | $3.9M |
| GOVSMART | 260 | $29.5M | No | $0 |
| BLUE TECH | 215 | $26.5M | No | $0 |
| REDHAWK IT SOLUTIONS | 206 | $17.7M | **Yes** | $6.2M |
| ACCESSAGILITY | 202 | $19.7M | No | $0 |
| PROMETHEUS COMPUTING | 32 | $6.0M | No | $0 |

## SDVOSB Patterns

- **VA dominates SDVOSB set-asides** — 442 awards (49.4% of all VA awards in these NAICS)
- **State Department** is the #2 SDVOSB buyer by count (51 awards, 9.1%)
- **DoD** has the highest absolute SDVOSB count after VA/State (33 awards) but lowest percentage (2.0%)
- Three of 11 tracked competitors hold SDVOSB status: THUNDERCAT, V3GATE, REDHAWK
- **REDHAWK** has the most SDVOSB awards among competitors (55, $6.2M) followed by THUNDERCAT (32, $6.4M) and V3GATE (32, $3.9M)

## Top SDVOSB Recipients (Non-Competitor)

| Recipient | SDVOSB Value |
|-----------|-------------|
| FOUR POINTS TECHNOLOGY | $7.5M |
| MINBURN TECHNOLOGY GROUP | $6.6M |
| ALVAREZ LLC | $6.0M |
| UNIVERSAL STRATEGY GROUP | $3.4M |
| TOTALLY JOINED FOR ACHIEVING COLLABORATIVE TECHNIQUES | $2.8M |
| ARCHITECHTURE SOLUTIONS LLC | $2.8M |
| CYNERGY PROFESSIONAL SYSTEMS | $2.6M |

## Recompete Opportunities (≥$100K, expiring before Dec 2026)

- **1,499** awards worth ≥$100K expiring before December 2026
- **DoD**: 316 contracts ($85.5M) — largest recompete pipeline
- **State**: 132 contracts ($42.1M), 18 SDVOSB — strongest SDVOSB recompete signal
- **VA**: 123 contracts ($33.8M), 62 SDVOSB — highest SDVOSB density
- Competitor contracts expiring:
  - NEW TECH SOLUTIONS: 91 contracts ($21.3M)
  - FCN: 59 contracts ($13.6M)
  - THUNDERCAT: 58 contracts ($15.9M)
  - GOVSMART: 28 contracts ($6.5M)

## NAICS Distribution

| NAICS | Awards | Description |
|-------|--------|-------------|
| 541519 | 5,528 | Other Computer Related Services |
| 541611 | 3,049 | Admin Management Consulting |
| 611430 | 1,588 | Professional/Management Development Training |
| 541690 | 1,580 | Other Scientific and Technical Consulting |
| 541618 | 220 | Other Management Consulting Services |
| (others) | 489 | From competitor name searches (non-target NAICS) |

## API Quirks Encountered

1. **`award_type_codes` required** — 422 without it. Contracts (A–D) and IDVs (IDV_A–E) must be separate queries.
2. **NAICS/PSC are nested objects** — `{code, description}` not flat strings. Field names are `NAICS` and `PSC`, not `NAICS Code` / `Product or Service Code (PSC)`.
3. **`page_metadata.total` shows 0** — API returns `total: 0, hasNext: true` on many queries. Paginate by `hasNext` only.
4. **Set-aside fields always null** — `Set Aside`, `Type of Set Aside`, `Extent Competed` all return null in `spending_by_award`. SDVOSB detection requires separate query with `set_aside_type_codes` filter.
5. **`time_period` uses `action_date`** — competitor searches return old awards with recent modifications. These are active contracts, not stale data.
6. **`recipient_search_text` is fuzzy** — "BLUE TECH" matches "BLUE TECH INC." and similar. Scan for false positives.

## Source Files

- `query_usaspending.py` — primary extraction (5 NAICS + 11 competitors, 12,131 initial rows)
- `enrich_sdvosb.py` — SDVOSB cross-reference (+323 new SDVOSB awards, 676 total flagged)
- `usaspending_small_dollar_awards.csv` — 12,454 rows × 33 columns
- `usaspending_agency_summary.csv` — 62 agencies × 9 columns