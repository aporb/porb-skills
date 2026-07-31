# USAspending Patterns for Opportunity Research

Verified 2026-07-18. All calls are unauthenticated POSTs to `https://api.usaspending.gov/api/v2/...`.

## Sub-$250K awards in a NAICS set (recent band)

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "time_period": [{"start_date": "2026-06-18", "end_date": "2026-07-18"}],
      "naics_codes": ["541611","541519","611430"],
      "award_type_codes": ["A","B","C","D"],
      "award_amounts": [{"lower_bound": 1, "upper_bound": 250000}]
    },
    "fields": ["Award ID", "Recipient Name", "Start Date", "Award Amount", "Awarding Agency", "NAICS"],
    "limit": 100, "order": "desc", "sort": "Start Date"
  }'
```

Use this to (a) confirm a NAICS produces sub-$250K actions at volume and (b) name the incumbent small-biz winners a new entrant will compete against. Snapshot 2026-07-18: of the latest 100 such awards, 84 were 541519, 10 were 541611, 6 were 611430. Frequent winners in this band: GOVSMART, FCN, THUNDERCAT TECHNOLOGY, ADVANCED COMPUTER CONCEPTS, BLUE TECH, COUNTERTRADE PRODUCTS, PROMETHEUS COMPUTING.

## Agency spend rollup (where to focus BD)

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_category/awarding_agency/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "time_period": [{"start_date": "2026-04-18", "end_date": "2026-07-18"}],
      "naics_codes": ["541611","541519","611430"],
      "award_type_codes": ["A","B","C","D"]
    },
    "category": "awarding_agency", "limit": 50
  }'
```

Top 3 for those NAICS in that 90-day window: DHS $1.25B, VA $995M, HHS $919M (total across 50 agencies ≈ $6.1B).

## Pitfalls

- `business_categories: ["small_business"]` matches the recipient's SAM registration status, NOT award size — base IDV ceilings of $100M–$1B+ awarded to small-business-registered holders pass the filter. Always pair with an `award_amounts` band when hunting genuinely small actions.
- `Start Date` is period-of-performance start and can be in the FUTURE on modifications; a descending sort surfaces far-future dates (2027+) first. Don't read them as data errors.
- The `Award Type` field requested on this endpoint returns null — ignore it.
- Overlap note: the `contractor-portfolio-analysis` skill's `references/usaspending-api-patterns.md` covers the same API from the portfolio-analysis angle — check both before adding new USAspending patterns.
