#!/usr/bin/env python3
"""Research federal awards via USAspending API — batch NEW-vs-RECOMPETE research.

Usage:
  1. Copy to /tmp/research_awards.py
  2. Edit CANDIDATES (topic keywords) and RECIPIENT_QUERIES (incumbent names)
  3. python3 /tmp/research_awards.py | tee /tmp/awards_dump.txt

One terminal call runs ~50 keyword searches in sequence and dumps full results —
dramatically more efficient than one curl per keyword and avoids the tool-call cap.

Uses only the USAspending public API (no key required). Output is plain text to
stdout; redirect to a file with `> /tmp/awards_dump.txt` if needed.

See references/usaspending-new-work-vs-recompete.md for the full method, the
single-token keyword strategy, office-prefix matching, and 15 worked examples.
"""
import json
import urllib.request

API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
FIELDS = ["Award ID", "Recipient Name", "Award Amount", "Description",
          "Start Date", "End Date", "Awarding Agency", "Awarding Sub Agency",
          "NAICS Code", "Contract Award Type"]
CONTRACT_CODES = ["A", "B", "C", "D"]  # BPA Call, PO, Delivery Order, Definitive Contract


def search_awards(query, limit=10, time_start="2015-01-01", time_end="2026-07-18"):
    """Single-token keyword search on USAspending. Multi-word phrases often return 0.

    Rules of thumb:
    - Single tokens work best: "RFID", "MedBridge", "TCCC", "Guardian", "IHS"
    - Two-word ENTITY names work: "Templar Medical", "Purdy Group" (recipient_name
      is one logical token)
    - Multi-word TOPIC phrases are hit-or-miss: "Tactical Combat Casualty Care"
      works (canonical program name in DoD award descriptions) but
      "Civilian Guardian Course" does not (too novel/specific)
    - If 0 results, broaden to a single token or fall back to a known recipient name
    """
    payload = {
        "filters": {
            "keywords": [query],
            "award_type_codes": CONTRACT_CODES,
            "time_period": [{"start_date": time_start, "end_date": time_end}]
        },
        "fields": FIELDS,
        "page": 1, "limit": limit,
        "sort": "Award Amount", "order": "desc"
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(API, data=data,
                                 headers={"Content-Type": "application/json"})
    print(f"\n=== '{query}' ===")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
    except Exception as e:
        print(f"  ERR: {e}")
        return []
    results = d.get("results", [])
    for r in results:
        rname = (r.get("Recipient Name") or "?")[:42]
        amt = r.get("Award Amount") or 0
        sd = r.get("Start Date") or "?"
        ed = r.get("End Date") or "?"
        sub = (r.get("Awarding Sub Agency") or "")[:25]
        aid = (r.get("Award ID") or "?")[:70]
        desc = (r.get("Description") or "")[:160]
        print(f"  {rname} | ${amt:,.0f} | {sd} - {ed} | {sub}")
        print(f"    ID: {aid} | Desc: {desc}")
    print(f"  Total: {len(results)}")
    return results


# === EDIT THESE LISTS FOR YOUR BATCH ===

# Single-token topic keywords — one token works best (no phrase matching).
# Two-word entity names also work (recipient_name is one logical token).
# Replace these with keywords relevant to YOUR Notice IDs.
CANDIDATES = [
    # E.g. for a medical/training/curriculum batch:
    "MedBridge",            # VA MedBridge rehabilitation education
    "RFID",                 # VA RFID asset tracking
    "TCCC",                 # Tactical Combat Casualty Care
    "NAVSUP WSS",           # NAVSUP WSS training (this 2-word phrase works — appears in award descs)
    "Guardian",             # Civilian Guardian / Space Force
    "curriculum development",
    "IHS dental",           # IHS dental CE
    "play therapy",         # VA LEGO play therapy
    "LEGO",                 # LEGO (expect construction-company noise — filter by sub-agency)
    "recreation therapy",   # VA recreation therapy
]

# Once you have a candidate incumbent, search their name to confirm the
# office-prefix pattern and find related awards the topic keyword missed.
RECIPIENT_QUERIES = [
    # E.g.:
    # "Veteran Information Technologies",  # VIT LLC — VA RFID incumbent
    # "Templar Medical",                   # TCCC incumbent
    # "Purdy Group",                       # NAVSUP WSS ERP training incumbent
    # "California Rural Indian Health",    # IHS dental CE prior awardee
]

# Specific prior Award IDs to verify (run as keyword search — returns exact record).
# Fill these in AFTER the CANDIDATES pass surfaces candidate prior awards.
VERIFY_AWARD_IDS = [
    # E.g.:
    # "M0068124P0008",   # Templar Medical TCCC
    # "36C10B23F0345",  # VIT VISN 5 RFID
    # "36C24426N0002",  # MedBridge VISN04 current
]


if __name__ == "__main__":
    print("########## TOPIC KEYWORD SEARCHES ##########")
    for q in CANDIDATES:
        search_awards(q, limit=10)

    print("\n########## RECIPIENT-NAME VERIFICATION ##########")
    for q in RECIPIENT_QUERIES:
        search_awards(q, limit=10)

    print("\n########## PRIOR AWARD ID VERIFICATION ##########")
    for aid in VERIFY_AWARD_IDS:
        search_awards(aid, limit=5)


# === HOW TO USE THE RESULTS ===
#
# After the script dumps all results, scan for Award IDs whose prefix matches the
# Notice ID's office prefix (first ~6 chars before the fiscal-year segment).
# Examples:
#
#   Notice ID          Office prefix   Match these prior Award ID prefixes
#   36C10B26R0017      36C10B          36C10B23F0345, 36C10B25F0154 (VIT RFID)
#   M0068126Q0063      M00681          M0068124P0008 (Templar TCCC)
#   36C24426Q0800      36C244          36C24421N0971..36C24426N0002 (MedBridge chain)
#   N0018926RW025      N00189          N0018918PQ058, N0018916CQ006/7 (Purdy ERP)
#   FA254926R0002      FA2549          FA254925F0001, FA254926F0001 (different scope -> NEW)
#
# The most recent same-office same-topic recipient is your incumbent. Cross-check
# by searching the recipient name (RECIPIENT_QUERIES section) to surface ALL their
# awards and confirm the office-prefix pattern is consistent.
#
# Expected output format (deliver to user):
#   Notice ID | Title | New Work or Recompete? | Prior incumbent | Prior award value | 1-2 line description