# SBIR/STTR Topic Scraping Reference

Proven recipes for enumerating open SBIR/STTR topics with close dates, written after a July 2026 scan. Covers SBIR.gov (Drupal, curl-able), the real DoD portal (DSIP), a hijacked-domain warning, and the browser pattern for Next.js aggregators.

## Portal map

| Portal | URL | Access | Notes |
|--------|-----|--------|-------|
| SBIR.gov topics | `https://www.sbir.gov/topics` | **curl works** with browser UA | Authoritative cross-agency listing; ~46 open topics, 10/page (`?page=0..4`) |
| DSIP (DoD) | `https://www.dodsbirsttr.mil/` | JS-heavy; use browser tool | "DoW SBIR/STTR Innovation Portal" — the ONLY canonical DoD submission portal |
| ~~sbir.defensebusiness.org~~ | — | **HIJACKED** | Parked domain serving gambling/e-commerce spam (observed Indonesian poker storefront, July 2026). Never cite or use. Any GovCon-looking domain showing casino/storefront content = hijack signal; bail to the .mil/.gov canonical |
| sbir.gov `/sbirsearch/*` | — | 404 / dead | Old search endpoints are gone; don't bother |
| Porbanderwala SBIR Portal API | `https://sbir.porbanderwala.cloud/api/opportunities` | **JSON API works with curl** | Aggregates DoD DSIP + SBIR.gov. Paginated, 413 topics. Preferred data source. |

## DoD batch cadence (the two-batch trap)

DoW releases topics the **first Wednesday of each month**, closing the **last Wednesday of the following month** (e.g. opens 03/26, closes 04/23). Consequence:

- When batch N+1 goes live on SBIR.gov `/topics`, batch N (often with only **days** left) **drops off the SBIR.gov listing entirely** but remains open on DSIP/aggregators.
- A scan limited to SBIR.gov will report "nothing closes in the next 30 days" while a batch closes in 3 days. **Always cross-check DSIP or an aggregator for the outgoing batch.**
- Solicitation numbers encode the batch: `26.BZ03` vs `26.BZ04` etc. (`BZ`=SBIR broad, `BX`=SBIR xTech/open-topic, `TZ`=STTR; the trailing two digits increment per cycle).

## SBIR.gov listing scrape (works via curl)

```bash
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
mkdir -p details
for p in 0 1 2 3 4; do
  curl -sL -A "$UA" "https://www.sbir.gov/topics?page=$p" -o "topics_p$p.html"
done
# Topic links look like: href="/topics/12805"
grep -ohE 'href="/topics/[0-9]+"' topics_p*.html | sort -u
# Then fetch each detail page:
for id in 12805 ...; do curl -sL -A "$UA" "https://www.sbir.gov/topics/$id" -o "details/$id.html"; done
```

Note: `https://www.sbir.gov/sbirsearch/topic/current` (the old bookmark) returns **404** — use `/topics`.

## SBIR.gov detail-page parser (Drupal, server-rendered)

Gotchas discovered the hard way:
- `<title>` is just `"Topic | SBIR"` — useless.
- The topic title is in an `<h2>`, but the FIRST `<h2>` on the page is `"Dashboard Login"` (nav). Skip `{'dashboard login','topic'}` and take the first `<h2>` longer than ~10 chars.
- Fields render as pipe-delimited plain text after stripping tags: `Funding Agency | DOW | MDA |`, `Close Date | August 19, 2026 |`. Match with `re.escape(label) + r'\s*\|\s*([^|]+)'`. `Funding Agency` can have 1–3 pipe-separated values (department + component).
- `Description |` is followed by several empty pipe cells before the text: use `Description\|(?:\s*\|){0,4}\s*([^|]{40,1400})`.

```python
import re
from html import unescape

def textify(html):
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    t = re.sub(r'\|+', '|', unescape(t))
    return re.sub(r'[ \t]+', ' ', t)

def field(text, label):
    m = re.search(re.escape(label) + r'\s*\|\s*([^|]+)', text)
    return m.group(1).strip() if m else ''

def parse_detail(html):
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.S)
    title = next((re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>','',h))).strip()
                  for h in h2s
                  if len(re.sub(r'<[^>]+>','',h).strip()) > 10
                  and re.sub(r'<[^>]+>','',h).strip().lower() not in {'dashboard login','topic'}), '')
    text = textify(html)
    ag = re.search(r'Funding Agency\s*\|((?:[^|]+\|){1,3})', text)
    agency = ' / '.join(v.strip() for v in ag.group(1).split('|') if v.strip()) if ag else ''
    desc = re.search(r'Description\|(?:\s*\|){0,4}\s*([^|]{40,1400})', text)
    return dict(
        title=title, agency=agency,
        topic_number=field(text,'Topic Number:'), solicitation=field(text,'Solicitation Number:'),
        tags=field(text,'Tagged as:'), status=field(text,'Solicitation Status:'),
        release=field(text,'Release Date'), open_date=field(text,'Open Date'),
        due=field(text,'Due Date(s)'), close=field(text,'Close Date'),
        description=re.sub(r'\s+',' ',desc.group(1)).strip()[:700] if desc else '',
    )
```

## Porbanderwala SBIR Portal — JSON API (PREFERRED DATA SOURCE)

The `sbir.porbanderwala.cloud` portal is a Next.js app that aggregates DoD DSIP + SBIR.gov data. While most Next.js paths return empty shells to curl, **`/api/opportunities` returns clean paginated JSON** — this is the fastest way to enumerate all SBIR/STTR topics.

```bash
# List all topics (paginated, default pageSize=20)
curl -s "https://sbir.porbanderwala.cloud/api/opportunities?page=1&pageSize=50" | python3 -m json.tool

# Response shape:
# { "results": [{...}], "total": 413, "page": 1, "pageSize": 50, "totalPages": 9 }
```

**Topic object fields:** `id` (UUID), `title`, `abstract` (often empty — see pitfall below), `agency`, `subAgency`, `program` (SBIR/STTR), `phase` (I/II/BOTH), `solicitationNumber`, `topicNumber`, `topicCode`, `awardAmount` (null most of the time), `openDate`, `closeDate`, `topicStatus` (open/pre_release/closed), `component`, `command`, `sourceUrl` (link to DSIP topic page), `createdAt`.

**Pull all topics at once (~413 as of July 2026):** Loop `?page=1..22&pageSize=50` — the API returns exactly what's requested (last page has remainder). Store as JSON for keyword scoring.

**Filtering is client-side:** The `?search=cyber` and `?status=open` query params are NOT respected by the API — they always return all 413 topics sorted by recency. Filter + score in Python after pulling the full dataset.

**Abstracts are sparse:** Only ~40 of 413 topics have a non-empty `abstract` field. The rest are `""`. When the abstract is empty, score on the `title` alone and use the `sourceUrl` (DSIP topic page) for full details. The DSIP pages themselves are JS-heavy and 403 from curl — open them with `browser_navigate` when the title alone isn't enough to classify.

**Detail pages:** The portal's `/topic/<topicCode>` route returns 404. Detail views are rendered inline via JavaScript in the search UI — use the browser tool with the search page, not direct detail routes.

**Status distribution (July 2026 snapshot):** 337 closed, 48 open, 27 pre_release, 1 unknown. The gap between "active" (~75) and "open now" (~48) means pre-release topics (open date in the future) are worth tracking for pipeline planning.

## Next.js / RSC aggregators (browser tool required)

Modern aggregator portals are Next.js apps: curl returns a ~16KB shell with RSC streaming chunks (`self.__next_f.push`) and no data; there is often NO `__NEXT_DATA__` script and no discoverable `/api/*` in the HTML. Pattern that works:

1. `browser_navigate` to the search URL. Pagination may be URL-driven (`?page=2`) — if clicking a page button doesn't advance, navigate directly with the query param.
2. Cards are `<h3>` titles inside clickable generics; extract all cards in one shot via `browser_console`:

```js
(() => { const seen = new Set(); const out = [];
  document.querySelectorAll('main h3').forEach(h => {
    const a = h.closest('a');
    if (h.textContent.trim() && !seen.has(h.textContent)) {
      seen.add(h.textContent);
      out.push({title: h.textContent.trim(), url: a ? a.href : ''});
    }});
  return out; })()
```

3. Detail pages render label/value as adjacent text lines — read them by line-walking `innerText` (labels like `Close Date` appear on the line AFTER the value, because of layout order):

```js
(() => { const lines = document.body.innerText.split('\n').map(l=>l.trim()).filter(Boolean);
  const i = lines.findIndex(l=>l==='Close Date');
  const a = lines.findIndex(l=>l==='Abstract'), d = lines.findIndex(l=>l==='Details');
  return { close: i>=0 ? lines[i-1] : '',
           abstract: lines.slice(a+1, d).join(' ').slice(0,700) }; })()
```

4. "N days left" badges on cards are computed client-side from the close date — trust the detail page's explicit `Close Date` field over badge math.

## Relevance scoring hint (cyber/compliance/training/PM/IT)

Keyword-scoring over `title + ' ' + description` with weighted patterns worked well (5: zero trust/RMF/NIST 800-53/STIG/CVE/cyber; 4: compliance/ATO/audit/training/program management/digital engineering; 3: AI/ML/software platform). Watch false positives: NIH parent grants match on the word "readiness" (Commercialization Readiness Pilot) — require ≥2 cyber-family hits before awarding a 5. Store results as JSON (`scored.json`) and sort by `(-relevance, close_date)`.
