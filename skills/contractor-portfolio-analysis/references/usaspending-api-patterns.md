# USAspending.gov API Patterns

## Base URL

```
https://api.usaspending.gov/api/v2/
```

All endpoints are POST with JSON body (except award detail which is GET). No API key required.

---

## Endpoint Reference

### 1. Award Search: `search/spending_by_award/`

Returns individual contract awards matching filters. This is the primary workhorse for portfolio analysis.

**Valid award_type_codes:**
- `A` — Definitive Contract
- `B` — Purchase Order
- `C` — Delivery Order
- `D` — Task Order
- `IDV_A` — IDV (Generic)
- `IDV_B` — IDV (Indefinite Delivery Vehicle)
- `IDV_B_A` — IDV (Government-Wide Acquisition Contract (GWAC))
- `IDV_B_B` — IDV (Indefinite Delivery/Indefinite Quantity (IDIQ))
- `IDV_B_C` — IDV (Indefinite Delivery/Definite Quantity (IDDQ))
- `IDV_C` — IDV (Federal Supply Schedule (FSS))
- `IDV_D` — IDV (Other Transaction Authority (OTA))
- `IDV_E` — IDV (Blanket Purchase Agreement (BPA))

⚠ **`"IDV"` (bare) is NOT valid** — it will return a 400 with the full list of valid codes. Always use the granular codes.

**Available fields:**
```json
["Award ID", "Recipient Name", "Award Amount", "Description", 
 "Start Date", "End Date", "Awarding Agency", "Awarding Sub Agency",
 "Contract Award Type", "generated_internal_id", "recipient_id"]
```

**Response:** `{ "results": [...], "page_metadata": {...} }`

**Proven query pattern:**
```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2020-01-01", "end_date": "2026-12-31"}],
      "award_type_codes": ["A", "B", "C", "D"]
    },
    "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", 
               "Start Date", "End Date", "Awarding Agency", "Awarding Sub Agency", 
               "Contract Award Type", "generated_internal_id"],
    "page": 1,
    "limit": 100,
    "sort": "Award Amount",
    "order": "desc"
  }'
```

### 2. Spending Over Time: `search/spending_over_time/`

Returns aggregated obligations grouped by fiscal year or month. Use for revenue trend charts.

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_over_time/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2019-01-01", "end_date": "2026-12-31"}],
      "award_type_codes": ["A", "B", "C", "D"]
    },
    "group": "fiscal_year"
  }'
```

**Response:** `{ "results": [{ "aggregated_amount": N, "time_period": { "fiscal_year": "2025" } }] }`

### 3. Spending by Category: `search/spending_by_category/<dimension>/`

Aggregates spending by a category dimension. Useful dimensions:
- `awarding_agency` — which agencies pay the company
- `naics` — what business types (NAICS codes)
- `recipient` — who receives (less useful for company analysis)
- `psc` — product/service codes

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_category/naics/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": { "recipient_search_text": ["Company"], "time_period": [{"start_date": "2019-01-01", "end_date": "2026-12-31"}], "award_type_codes": ["A", "B", "C", "D"] },
    "limit": 15
  }'
```

### 4. Award Detail: `awards/<generated_internal_id>/` (GET)

**This is the BEST source for recipient details** — UEI, business categories, address, parent company.

```bash
curl -s "https://api.usaspending.gov/api/v2/awards/CONT_AWD_N0018924FZ680_9700_47QTCA20D0063_4732/"
```

**Key fields in response:**
```json
{
  "description": "...",
  "total_obligation": 23618859.16,
  "total_outlay": null,
  "date_signed": "2024-06-27",
  "period_of_performance": { "start_date": "2024-07-19", "end_date": "2026-07-18" },
  "recipient": {
    "recipient_name": "RED RIVER RESOURCES LLC",
    "recipient_uei": "HZCDXJV7M8Z9",
    "business_categories": ["8(a) Program Participant", "American Indian Owned Business", ...],
    "location": { "city_name": "SAN DIEGO", "state_code": "CA", "address_line1": "..." }
  }
}
```

⚠ **Pitfall:** The `awarding_agency`, `awarding_sub_agency`, and `award_type` fields at the root level are often `null` in this endpoint. Get those from the search results instead.

### 5. Recipient Autocomplete: `autocomplete/recipient/`

Quick name lookup to find exact legal entity name variants.

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/autocomplete/recipient/" \
  -H "Content-Type: application/json" \
  -d '{"search_text": "Red River Resources", "limit": 10}'
```

⚠ Returns name variants but NOT UEI/DUNS. Get those from the award detail endpoint.

### 6. Recipient Profile: `recipient/<UUID>/` (GET) — Works with UUID-based ID

The `/api/v2/recipient/` endpoint with `recipient_search_text` filter does NOT filter by search text — it returns all entities sorted by total amount. **However**, the `recipient/<recipient_id>/` GET endpoint DOES work when you pass the UUID-based `recipient_id` found in award/transaction results.

**Finding the recipient_id:** It appears in `spending_by_award` and `spending_by_transaction` results as `recipient_id` with format `<UUID>-<level>`:
- `<UUID>-C` → Child recipient (specific location/division)
- `<UUID>-P` → Parent recipient (the company overall)
- `<UUID>-R` → Root recipient

```bash
# Get full recipient profile using UUID-based ID
curl -s "https://api.usaspending.gov/api/v2/recipient/942a2bde-c189-6421-6a4d-a9b1c2f00d41-C/"
```

**Returns:** name, alternate_names, duns, uei, business_types, location, total_transaction_amount, total_transactions, parent info. The `business_types` array uses machine codes like `8a_program_participant`, `woman_owned_business`, `american_indian_owned_business`, etc.

⚠ Numeric `internal_id` values from search results (e.g., `310038855`) do NOT work with this endpoint — they return 400 Bad Request. Only the UUID-based `recipient_id` works.

### 7. Transaction Search: `search/spending_by_transaction/` (POST)

Returns individual transaction-level records (each modification/obigation action under an award). Essential for granular revenue analysis and understanding spending velocity.

⚠ **This endpoint uses DIFFERENT field names than `spending_by_award/`.** Invalid field names cause 422 errors. The `sort` parameter is REQUIRED.

**Valid fields for spending_by_transaction:**
```
Action Date, Action Type, Award ID, Award Type, Awarding Agency,
awarding_agency_id, awarding_agency_slug, Awarding Sub Agency,
cfda_number, cfda_title, def_codes, Funding Agency,
funding_agency_slug, Funding Sub Agency, generated_internal_id,
internal_id, Issued Date, Last Date to Order, Loan Value, Mod,
naics_code, naics_description, pop_city_name, pop_country_name,
pop_state_code, product_or_service_code,
product_or_service_description, recipient_id,
recipient_location_address_line1, recipient_location_address_line2,
recipient_location_address_line3, recipient_location_city_name,
recipient_location_country_name, recipient_location_state_code,
Recipient Name, Recipient UEI, Subsidy Cost, Transaction Amount,
Transaction Description, Assistance Listing, NAICS,
Primary Place of Performance, PSC, Recipient Location
```

**Note the naming convention differences from spending_by_award:**
- `"Transaction Amount"` (not `"amount"` or `"Award Amount"`)
- `"Transaction Description"` (not `"Description"`)
- `"Action Date"` (the date of the transaction action)
- `"Mod"` (modification number: `"0"` for initial, `"P00001"` for modifications)

**Proven query pattern:**
```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_transaction/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2019-10-01", "end_date": "2026-09-30"}],
      "award_type_codes": ["A", "B", "C", "D"]
    },
    "fields": ["Award ID", "Recipient Name", "Transaction Amount", "Action Date",
               "Action Type", "Transaction Description", "Mod",
               "Awarding Agency", "Awarding Sub Agency",
               "generated_internal_id", "recipient_id", "Recipient UEI",
               "naics_code", "naics_description",
               "pop_city_name", "pop_state_code"],
    "page": 1,
    "limit": 100,
    "sort": "Transaction Amount",
    "order": "desc"
  }'
```

### 8. Keyword Search (DBA/Product Name Discovery)

The `keywords` filter searches award and transaction descriptions. Use this when a company's DBA, product name, or project codename doesn't appear as a registered recipient entity.

```bash
# Find awards mentioning a DBA/product name
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_transaction/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "keywords": ["ProductOrDBAName"],
      "award_type_codes": ["A", "B", "C", "D"],
      "time_period": [{"start_date": "2019-10-01", "end_date": "2026-09-30"}]
    },
    "fields": ["Award ID", "Recipient Name", "Transaction Amount", "Transaction Description", "Action Date"],
    "page": 1, "limit": 100,
    "sort": "Transaction Amount", "order": "desc"
  }'
```

This reveals which legal entity (e.g., "RED RIVER RESOURCES LLC") holds contracts mentioning the DBA/product (e.g., "Navaide").

### 9. Award Count & Transaction Count: `spending_by_award_count/` and `spending_by_transaction_count/`

Quick count endpoints — no `fields` or `sort` required. Returns totals by award type category.

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award_count/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "recipient_search_text": ["Company Name"],
      "time_period": [{"start_date": "2019-10-01", "end_date": "2026-09-30"}],
      "award_type_codes": ["A", "B", "C", "D"]
    }
  }'
# → {"results": {"contracts": 170, "idvs": 0, "grants": 0, ...}}
```

### 10. Additional Category Endpoints

Beyond `awarding_agency`, `naics`, and `psc`, the `spending_by_category/<dimension>/` endpoint supports:
- `federal_account` — which federal accounts fund the awards (returns account codes like `017-1804`)
- `budget_function` — may 404 depending on filters

---

## Field Naming and Response Format Quirks (discovered 2026-07-18)

These quirks were discovered during intensive multi-NAICS landscape scanning. They apply to `spending_by_award` unless noted otherwise.

### NAICS and PSC are NESTED OBJECTS, not strings

In `spending_by_award` results, `NAICS` and `PSC` return as objects:
```json
{
  "NAICS": {"code": "541611", "description": "ADMINISTRATIVE MANAGEMENT AND GENERAL MANAGEMENT CONSULTING SERVICES"},
  "PSC": {"code": "R408", "description": "SUPPORT- PROFESSIONAL: PROGRAM MANAGEMENT/SUPPORT"}
}
```

Extract with: `naics.get("code", "")` and `naics.get("description", "")` — NOT as a raw string field.

### Field names in `spending_by_award` response

Use these EXACT field names in the `fields` array:
- `NAICS` (NOT `NAICS Code`)
- `PSC` (NOT `Product or Service Code (PSC)`)
- `Award Amount` (NOT `amount`)
- `Start Date`, `End Date` (NOT `Period of Performance Start Date`)
- `Recipient UEI` (NOT `recipient_uei` — note the uppercase)
- `Awarding Agency`, `Awarding Sub Agency`
- `Contract Award Type`

### `award_type_codes` is REQUIRED and contracts/IDVs can't mix

The API returns 422 if `award_type_codes` is omitted. Also 422 if you mix contract types (A–D) with IDV types (IDV_A–E) in a single query. Always query contracts and IDVs in separate API calls.

### `set_aside_type_codes` works as INPUT filter, not OUTPUT field

You CAN filter by set-aside codes:
```json
{"set_aside_type_codes": ["SDVOSBC", "SDVOSB"]}
```

But the response fields `Set Aside`, `Type of Set Aside`, and `Extent Competed` are ALWAYS null in `spending_by_award` results. To detect SDVOSB awards: run a separate query with the filter, collect the returned award IDs, then cross-reference against your master dataset.

### `page_metadata.total` is unreliable

Many queries return `"total": 0` with `"hasNext": true` and valid results. Always paginate by `hasNext` — stop when it's `false` or when the results array is empty. Do not trust the `total` field for page-count logic.

### `time_period` uses `action_date`, not award start date

The time_period filter matches awards where the most recent ACTION (modification, delivery order, BPA call) falls within the window. This means competitor searches will return awards from 2010 with 2026 modifications — these ARE active contracts. Do not filter them out based on old `current_end_date`.

### `award_amounts` filter

```json
{"award_amounts": [{"lower_bound": 0, "upper_bound": 500000}]}
```

Works correctly. Use `lower_bound` and `upper_bound` as integers. Both bounds are inclusive.

### `recipient_search_text` is fuzzy

Matches are substring-based, not exact. `["BLUE TECH"]` will match "BLUE TECH INC.", "BLUE TECHNOLOGY SOLUTIONS LLC", etc. Scan results for false positives when competitor names are short or common words.

### Additional valid filter fields

The `spending_by_award` endpoint also supports these filters (documented but less commonly used):
- `agencies` — filter by agency name
- `psc_codes` — filter by PSC codes (as array of strings or PSCCodeObject)
- `place_of_performance_locations` — filter by location
- `recipient_type_names` — filter by entity type
- `contract_pricing_type_codes` — filter by pricing arrangement
- `extent_competed_type_codes` — filter by competition type
- `description` — search award descriptions

### Date Ranges
```json
"time_period": [{"start_date": "2024-10-01", "end_date": "2025-09-30"}]
```
Federal fiscal year: Oct 1 – Sep 30.

### Recipient Search
```json
"recipient_search_text": ["Company Name"]
```
Accepts array — can pass multiple name variants. Use the legal name from SAM.gov or company website footer.

---

## jq Parsing Patterns

### Extract award list as TSV
```bash
| jq -r '.results[] | [.generated_internal_id, ."Award Amount", ."Description", ."Start Date", ."End Date", ."Awarding Sub Agency"] | @tsv'
```

### Extract structured award objects
```bash
| jq '.results[] | {award_id: .generated_internal_id, recipient: ."Recipient Name", amount: ."Award Amount", desc: ."Description", start: ."Start Date", end: ."End Date", agency: ."Awarding Agency", sub_agency: ."Awarding Sub Agency", type: ."Contract Award Type"}'
```

### Extract spending over time
```bash
| jq '.results[] | {fy: .time_period.fiscal_year, amount: .aggregated_amount}'
```

### Extract award detail
```bash
| jq '{description: .description, total_obligation: .total_obligation, pop_start: .period_of_performance.start_date, pop_end: .period_of_performance.end_date, recipient: .recipient.recipient_name, uei: .recipient.recipient_uei, business_categories: .recipient.business_categories}'
```

---

## Contract Lifecycle Classification Logic

After pulling all awards, classify each:

1. **Compare POP end date to today:**
   - Past → Expired/Lost or Reduced (check if a replacement award exists)
   - Within 90 days → At Risk
   - Beyond 90 days → Secure

2. **Check for replacement contracts:**
   - Same agency + similar description → likely a recompete (Reduced if value dropped)
   - No similar new award from same agency → Lost

3. **Calculate portfolio metrics:**
   - Total lost revenue (expired, no replacement)
   - Total reduced revenue (rebid at lower value — calculate delta)
   - At-risk amount (expiring in 90 days)
   - Secured floor (contracts running > 12 months)

---

## Award ID Format

USAspending generated_internal_id format:
```
CONT_AWD_<PIID>_<agency_toptier_code>_<referenced_IDV_PIID>_<referenced_agency_code>
```

Example: `CONT_AWD_N0018924FZ680_9700_47QTCA20D0063_4732`
- PIID: N0018924FZ680
- Agency: 9700 (DoD)
- Vehicle PIID: 47QTCA20D0063 (GSA MAS)
- Vehicle Agency: 4732 (GSA)

The vehicle PIID tells you the contract vehicle:
- `47QTCA*` / `47QTCB*` → GSA MAS (IT Schedule)
- `N00178*` → SeaPort-NxG
- If no vehicle PIID (`-NONE-`) → standalone definitive contract
