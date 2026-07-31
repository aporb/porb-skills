#!/usr/bin/env python3
"""Fetch full award detail (description, NAICS, office) from USAspending.gov.

Use this AFTER a `spending_by_award` keyword search — the keyword search returns
`Description of Requirement` as NULL, but the detail endpoint at
`/api/v2/awards/{generated_internal_id}/` returns the populated `description`.

Workflow:
  1. Run `templates/usaspending-batch-research.py` (or any keyword search) to get
     candidate award IDs and their `generated_internal_id` values.
  2. Pass the PIIDs you want to drill into as CLI args to this script.
  3. The script looks up each PIID via keyword search, then fetches its detail.

Usage:
  python3 scripts/usaspending-detail-fetch.py 7571PS26F00305 75D30124C18540 15F06722C0000304

Output: one block per award with PIID, recipient, POP, amount, office, description.
"""
import sys
import json
import urllib.request

SEARCH_API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
DETAIL_BASE = "https://api.usaspending.gov/api/v2/awards/"
FIELDS = ["Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount",
          "Description of Requirement", "Awarding Agency", "Awarding Sub Agency"]


def find_by_piid(piid):
    """Keyword search by exact PIID. Returns first result (with generated_internal_id)."""
    payload = {
        "fields": FIELDS,
        "filters": {
            "keywords": [piid],
            "award_type_codes": ["A", "B", "C", "D"]
        },
        "limit": 5, "page": 1,
        "sort": "Award Amount", "order": "desc"
    }
    req = urllib.request.Request(
        SEARCH_API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    results = d.get("results", [])
    return results[0] if results else None


def get_detail(generated_id):
    """GET /awards/{generated_internal_id}/ — returns full award object."""
    url = DETAIL_BASE + generated_id + "/"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}


def report(piid):
    res = find_by_piid(piid)
    if res is None:
        print(f"=== {piid} — no award found ===\n")
        return
    gen_id = res.get("generated_internal_id") or res.get("Award ID")
    print(f"=== {res.get('Award ID')} | {res.get('Recipient Name')} | "
          f"{res.get('Start Date')} to {res.get('End Date')} | "
          f"${res.get('Award Amount')} ===")
    print(f"  Generated ID: {gen_id}")
    print(f"  Agency: {res.get('Awarding Agency')} / {res.get('Awarding Sub Agency')}")
    detail = get_detail(gen_id)
    if "error" in detail:
        print(f"  Detail fetch failed: {detail['error']}")
    else:
        print(f"  Description: {detail.get('description')}")
        naics = detail.get("naics") or {}
        print(f"  NAICS: {naics.get('code')} - {naics.get('description')}")
        awarding = detail.get("awarding_agency") or {}
        print(f"  Office: {awarding.get('office_agency_name')}")
        print(f"  Subtier: {(awarding.get('subtier') or {}).get('subtier_name')}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for piid in sys.argv[1:]:
        try:
            report(piid)
        except Exception as e:
            print(f"ERROR for {piid}: {e}\n")
