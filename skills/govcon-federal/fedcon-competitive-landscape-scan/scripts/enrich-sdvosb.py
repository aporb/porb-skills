#!/usr/bin/env python3
"""
SDVOSB enrichment script for USASpending landscape scans.

The spending_by_award endpoint does NOT return set-aside fields in results
(they're always null). This script runs SEPARATE queries with the
set_aside_type_codes filter to find SDVOSB awards, then cross-references
award IDs against an existing CSV to flag them.

Usage: python3 enrich-sdvosb.py <input_csv> <output_csv>
       (default: usaspending_small_dollar_awards.csv in cwd)

Requires: the primary sweep CSV with award_id column already populated.
"""

import requests, csv, json, time, os, sys
from collections import defaultdict

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
CONTRACT_TYPES = ["A", "B", "C", "D"]
IDV_TYPES = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]
SDVOSB_CODES = ["SDVOSBC", "SDVOSB"]

# Match your primary sweep config
TARGET_NAICS = ["541611", "541519", "611430", "541618", "541690"]
START_DATE, END_DATE = "2026-01-19", "2026-07-18"
MAX_PAGES = 10

FIELDS = ["Award ID", "Recipient Name", "Recipient UEI", "Award Amount",
          "Awarding Agency", "NAICS", "PSC", "Start Date", "End Date",
          "Description", "Contract Award Type"]


def api_post(payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            resp = requests.post(API, json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
    return None


def fetch_sdvosb_ids(naics_list):
    """Fetch SDVOSB award IDs for given NAICS codes."""
    ids = set()
    for naics in naics_list:
        for atypes, label in [(CONTRACT_TYPES, "contracts"), (IDV_TYPES, "IDVs")]:
            for page in range(1, MAX_PAGES + 1):
                data = api_post({
                    "filters": {
                        "award_type_codes": atypes,
                        "naics_codes": [naics],
                        "award_amounts": [{"lower_bound": 0, "upper_bound": 500000}],
                        "set_aside_type_codes": SDVOSB_CODES,
                        "time_period": [{"start_date": START_DATE, "end_date": END_DATE}],
                    },
                    "fields": FIELDS, "sort": "Award Amount", "order": "desc",
                    "page": page, "limit": 100, "subawards": False,
                })
                if not data:
                    break
                for award in data.get("results", []):
                    aid = award.get("Award ID", "")
                    if aid:
                        ids.add(aid)
                if not data.get("page_metadata", {}).get("hasNext"):
                    break
                time.sleep(0.6)
    return ids


def main():
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "usaspending_small_dollar_awards.csv"
    output_csv = sys.argv[2] if len(sys.argv) > 2 else input_csv

    print(f"Enriching {input_csv} with SDVOSB flags...")

    # Read existing CSV
    rows, existing_ids = [], set()
    with open(input_csv, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
            existing_ids.add(row["award_id"])

    print(f"  Existing awards: {len(rows)}")

    # Fetch SDVOSB award IDs
    print("  Querying SDVOSB awards...")
    sdvosb_ids = fetch_sdvosb_ids(TARGET_NAICS)
    print(f"  SDVOSB IDs found: {len(sdvosb_ids)}")

    # Update flags
    updated = 0
    for row in rows:
        if row["award_id"] in sdvosb_ids:
            row["is_sdvosb"] = "Y"
            updated += 1

    print(f"  Flagged as SDVOSB: {updated} ({updated/len(rows)*100:.1f}%)")

    # Write updated CSV
    headers = list(rows[0].keys())
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"  Wrote {len(rows)} rows to {output_csv}")

    # Print SDVOSB agency breakdown
    agency_sdvosb = defaultdict(lambda: {"count": 0, "spend": 0.0})
    for row in rows:
        if row["is_sdvosb"] == "Y":
            agency = row["awarding_agency"]
            agency_sdvosb[agency]["count"] += 1
            try:
                agency_sdvosb[agency]["spend"] += float(row["award_amount"] or 0)
            except (ValueError, TypeError):
                pass

    print("\n  SDVOSB by Agency:")
    for agency, data in sorted(agency_sdvosb.items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
        print(f"    {agency[:45]}: {data['count']} awards, ${data['spend']:,.0f}")


if __name__ == "__main__":
    main()