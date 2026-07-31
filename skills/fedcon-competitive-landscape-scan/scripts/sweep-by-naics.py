#!/usr/bin/env python3
"""
Reusable USASpending.gov sweep-by-NAICS script.
Queries spending_by_award for each NAICS code (contracts + IDVs separately),
collects unique awards, and writes a CSV.

Usage: Edit TARGET_NAICS, START_DATE, END_DATE, MIN_AMOUNT, MAX_AMOUNT below.
       python3 sweep-by-naics.py

Key API behaviors encoded:
  - award_type_codes REQUIRED (422 without), contracts/IDVs must be separate queries
  - NAICS and PSC are returned as objects {code, description}, not flat strings
  - page_metadata.total may show 0 — paginate by hasNext
  - time_period uses action_date (most recent modification)
  - Set Aside fields are ALWAYS null in spending_by_award responses
"""

import requests, csv, json, time, os
from datetime import datetime, timedelta
from collections import defaultdict

# ─── CONFIGURATION ───
TARGET_NAICS = ["541611", "541519", "611430", "541618", "541690"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=180)
MIN_AMOUNT, MAX_AMOUNT = 0, 500000
OUTPUT_CSV = "usaspending_awards.csv"
MAX_NAICS_PAGES = 15  # pages per NAICS × award type group
MAX_COMP_PAGES = 5    # pages per competitor × award type group

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
CONTRACT_TYPES = ["A", "B", "C", "D"]
IDV_TYPES = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]

FIELDS = [
    "Award ID", "Recipient Name", "Recipient UEI", "recipient_id",
    "Award Amount", "Total Outlays",
    "Awarding Agency", "Awarding Agency Code", "Awarding Sub Agency", "Awarding Sub Agency Code",
    "Funding Agency", "Funding Agency Code", "Funding Sub Agency", "Funding Sub Agency Code",
    "NAICS", "PSC", "Start Date", "End Date", "Last Date to Order",
    "Description", "Contract Award Type", "Award Type",
    "Place of Performance State Code", "Place of Performance Country Code",
    "Place of Performance City Code", "Place of Performance Zip5",
]

CSV_HEADERS = [  # flattened output fields
    "award_id", "recipient_name", "recipient_uei", "recipient_id",
    "award_amount", "total_outlays",
    "awarding_agency", "awarding_agency_code", "awarding_sub_agency", "awarding_sub_agency_code",
    "funding_agency", "funding_agency_code", "funding_sub_agency", "funding_sub_agency_code",
    "naics_code", "naics_description", "psc_code", "psc_description",
    "start_date", "current_end_date", "last_date_to_order",
    "description", "award_type", "contract_award_type",
    "pop_state_code", "pop_country_code", "pop_city_code", "pop_zip5",
    "is_sdvosb", "source_query",
]


def api_post(payload, max_retries=3):
    for attempt in range(max_retries):
        try:
            resp = requests.post(API, json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP Error: {e}")
            if resp.status_code == 422:
                print(f"    Body: {resp.text[:300]}")
                return None
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return None


def fetch_all(naics=None, recipient=None, max_pages=MAX_NAICS_PAGES):
    """Fetch all pages for a query — runs both contract and IDV queries."""
    all_awards, seen = [], set()
    for award_types, label in [(CONTRACT_TYPES, "contracts"), (IDV_TYPES, "IDVs")]:
        print(f"  Querying {label}...")
        for page in range(1, max_pages + 1):
            filters = {
                "award_type_codes": award_types,
                "time_period": [{"start_date": START_DATE.strftime("%Y-%m-%d"), "end_date": END_DATE.strftime("%Y-%m-%d")}],
                "award_amounts": [{"lower_bound": MIN_AMOUNT, "upper_bound": MAX_AMOUNT}],
            }
            if naics:
                filters["naics_codes"] = naics
            if recipient:
                filters["recipient_search_text"] = [recipient]

            data = api_post({
                "filters": filters, "fields": FIELDS,
                "sort": "Award Amount", "order": "desc",
                "page": page, "limit": 100, "subawards": False,
            })
            if not data:
                break

            results = data.get("results", [])
            has_next = data.get("page_metadata", {}).get("hasNext", False)
            total_shown = data.get("page_metadata", {}).get("total", "?")

            new = 0
            for award in results:
                aid = award.get("Award ID", "")
                if aid and aid not in seen:
                    seen.add(aid)
                    all_awards.append(award)
                    new += 1

            print(f"    Page {page}: {len(results)} ({new} new), total={total_shown}, hasNext={has_next}")
            if not has_next or len(results) == 0:
                break
            time.sleep(0.6)
    return all_awards


def extract_naics_psc(val):
    """Extract code/description from NAICS/PSC objects returned by API."""
    if isinstance(val, dict):
        return val.get("code", ""), val.get("description", "")
    return str(val), ""


def flatten(award, source=""):
    """Flatten API response to CSV row."""
    naics_code, naics_desc = extract_naics_psc(award.get("NAICS"))
    psc_code, psc_desc = extract_naics_psc(award.get("PSC"))
    return {
        "award_id": award.get("Award ID", ""),
        "recipient_name": award.get("Recipient Name", "") or "",
        "recipient_uei": award.get("Recipient UEI", "") or "",
        "recipient_id": award.get("recipient_id", "") or "",
        "award_amount": award.get("Award Amount", ""),
        "total_outlays": award.get("Total Outlays", ""),
        "awarding_agency": award.get("Awarding Agency", "") or "",
        "awarding_agency_code": award.get("Awarding Agency Code", "") or "",
        "awarding_sub_agency": award.get("Awarding Sub Agency", "") or "",
        "awarding_sub_agency_code": award.get("Awarding Sub Agency Code", "") or "",
        "funding_agency": award.get("Funding Agency", "") or "",
        "funding_agency_code": award.get("Funding Agency Code", "") or "",
        "funding_sub_agency": award.get("Funding Sub Agency", "") or "",
        "funding_sub_agency_code": award.get("Funding Sub Agency Code", "") or "",
        "naics_code": naics_code, "naics_description": naics_desc,
        "psc_code": psc_code, "psc_description": psc_desc,
        "start_date": award.get("Start Date", "") or "",
        "current_end_date": award.get("End Date", "") or "",
        "last_date_to_order": award.get("Last Date to Order", "") or "",
        "description": (award.get("Description", "") or "")[:500],
        "award_type": award.get("Award Type", "") or "",
        "contract_award_type": award.get("Contract Award Type", "") or "",
        "pop_state_code": str(award.get("Place of Performance State Code", "") or ""),
        "pop_country_code": str(award.get("Place of Performance Country Code", "") or ""),
        "pop_city_code": str(award.get("Place of Performance City Code", "") or ""),
        "pop_zip5": str(award.get("Place of Performance Zip5", "") or ""),
        "is_sdvosb": "N",  # filled by enrich-sdvosb.py
        "source_query": source,
    }


# ─── MAIN ───
if __name__ == "__main__":
    print(f"USASpending Sweep: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"NAICS: {TARGET_NAICS} | Amount: ${MIN_AMOUNT:,}–${MAX_AMOUNT:,}")

    all_awards, seen_ids = [], set()

    for naics in TARGET_NAICS:
        print(f"\n--- NAICS {naics} ---")
        awards = fetch_all(naics=[naics])
        print(f"  Total: {len(awards)}")
        for a in awards:
            aid = a.get("Award ID", "")
            if aid and aid not in seen_ids:
                seen_ids.add(aid)
                all_awards.append(a)
        time.sleep(1)

    print(f"\nTotal unique: {len(all_awards)}")

    rows = [flatten(a, f"naics_{a.get('NAICS',{}).get('code','')}" if isinstance(a.get('NAICS'), dict) else "naics")
            for a in all_awards]
    rows.sort(key=lambda r: float(r["award_amount"] or 0), reverse=True)

    os.makedirs(os.path.dirname(OUTPUT_CSV) or ".", exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in CSV_HEADERS})
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")