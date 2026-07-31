# SAM.gov API v2 — Reality Check

Discovered 2026-07-18. SAM.gov API key from https://api.sam.gov, tested against `https://api.sam.gov/opportunities/v2/search`.

## What Works

| Feature | Status | Details |
|---|---|---|
| API Key Authentication | ✅ Works | Key `SAM-xxx` authenticates, returns HTTP 200 |
| `postedFrom` / `postedTo` | ✅ Works | Date range filters DO constrain results |
| `limit` / `offset` | ✅ Works | Pagination works |
| `active=Y` | ✅ Works | Only returns active opportunities |

## What Does NOT Work

All content filters are SILENTLY IGNORED. The API always returns the full corpus (27,925–45,624 results depending on date range):

| Parameter | Status | Notes |
|---|---|---|
| `naicsCode` | ❌ Broken | Returns same 29,583 results regardless of NAICS code |
| `setAside` | ❌ Broken | `SDVOSBC`, `SBA`, `NONE` — all return identical results |
| `pscCode` | ❌ Broken | `R408`, `U008` etc. have no filtering effect |
| `noticeType` | ❌ Broken | `c`, `s`, `p`, `k` — all ignored |
| `dept` | ❌ Untested | Likely broken like the others |

## Endpoint That Works (for auth, not filtering)

```
GET https://api.sam.gov/opportunities/v2/search
  ?api_key=SAM-xxx
  &postedFrom=04/18/2026
  &postedTo=09/16/2026
  &limit=100
  &offset=0
  &active=Y
```

Returns: ~29,583 active opportunities across ALL domains, ALL NAICS, ALL set-asides.

## API Rate Limits

- 10 calls per day per key (public key tier)
- Each call takes 20-45 seconds
- Plan accordingly — 10 calls × 100 results = 1,000 opportunities max per day

## What Actually Works Instead

| Alternative | Reliability | Use For |
|---|---|---|
| **SAM.gov browser UI** | ✅ Filters work | Set-aside + Sources Sought keyword searches |
| **SAM.gov detail pages** (browser) | ✅ Full detail | Set-aside, PSC, description, attachments, POC |
| **SAM.gov APIs via browser_console** | ✅ Works from browser session | Full opportunity JSON, attachment listing, resource IDs |
| **USASpending API** | ✅ All filters work | Award history, incumbent discovery, competitive intel |
| **SBIR portal** (sbir.porbanderwala.cloud) | ✅ Full topic dump | SBIR/STTR opportunity scoring |

## Set-Aside Filter Trap

When SAM.gov browser UI DOES filter by SDVOSB set-aside, the results are overwhelmingly DLA/DoD hardware parts. Federal services opportunities (NAICS 541611/541519/611430) with set-aside tags rarely appear — they flow through GSA Schedules, VA IDIQs, and GWAC task orders that don't surface as standalone solicitations.

**For services:** search by keyword + Sources Sought type (not by set-aside), or use the USASpending small-dollar award approach to find which agencies and offices buy services from SDVOSBs, then track those offices for upcoming opportunities.

## Key Takeaway

Do NOT design agent dispatch workflows around SAM.gov API filtering. Use the browser for targeted UI searches (set-aside + Sources Sought + keywords) and the USASpending API for competitive-intel-grade award analysis. The API key is useful for one thing only: pulling the raw firehose (1,000 opportunities/day) for local CSV filtering — which is the "cast wide net" approach.

## Browser Console API Access (discovered 2026-07-18)

SAM.gov APIs that return 401/403/406 from direct curl work perfectly when called from within the authenticated browser session via `browser_console(expression=...)` with JavaScript `fetch()`. The Angular SPA holds a session token that authenticates these API calls transparently.

### Key API Endpoints (accessible via browser_console fetch)

```js
// 1. Full opportunity detail (JSON with all metadata)
fetch('https://sam.gov/api/prod/opps/v2/opportunities/{oppId}?api_key=null')
  .then(r => r.json())

// 2. Attachment/resource listing (requires hal+json Accept header)
fetch('https://sam.gov/api/prod/opps/v3/opportunities/{oppId}/resources?api_key=null&excludeDeleted=false&withScanResult=false',
  { headers: { 'Accept': 'application/hal+json' } })
  .then(r => r.json())
// Returns: opportunityAttachmentList[].attachments[] with resourceId, name, size, mimeType, accessLevel
```

### API URL Discovery Pattern

To find the API calls the Angular SPA makes (so you know which endpoints to call):

```js
// In browser_console — list all /api/prod calls the page made
performance.getEntriesByType('resource')
  .filter(e => e.name.includes('api/prod'))
  .map(e => e.name)
```

The opportunity ID (`oppId`) is the 32-char hex string from the SAM.gov URL:
`https://sam.gov/workspace/contract/opp/{32-char-hex-id}/view`

### File Download Limitation

**SAM.gov PDF attachments CANNOT be downloaded via browser_console fetch or curl — even when marked "Public."** The download endpoints return 404 for unauthenticated requests and the signed-URL generation requires a full browser session token that isn't accessible to `fetch()`. The opportunity detail and resource listing APIs work, but actual file downloads require manual browser interaction (clicking the download button in the SAM.gov UI with a logged-in session). When the PWS is in a PDF attachment, note it as inaccessible and infer what you can from the listing text and USASpending award descriptions.