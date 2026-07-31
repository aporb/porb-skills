# External Data Sources for Contractor Portfolio Analysis

Beyond USAspending.gov, these sources provide critical data that federal APIs don't expose.

---

## 1. SBA Certifications Portal

**URL:** `https://search.certifications.sba.gov/profile/<UEI>/<CAGE>`

**What it provides:**
- Current/historical SBA certification status (8(a), WOSB, EDWOSB, SDVOSB, HUBZone)
- **Suspension status** — shows "This certification is currently suspended" with warning icon
- Entrance date, scheduled exit date (9-year term for 8(a))
- SBA Servicing Office (district office name and code)
- Full NAICS code list with small-business size status per code
- Self-certifications: ISBEE, Indian Economic Enterprise, etc.
- Capabilities narrative, keywords, special equipment
- Bonding levels (construction and service)
- Current principals (may differ from company website leadership)

**Why it matters:** SBA certification status is the #1 explanation for contract portfolio erosion. A suspended 8(a) means the company cannot receive 8(a) sole-source awards — every expiring 8(a) contract has no 8(a) renewal mechanism. This is often the root cause that the USAspending data alone cannot explain.

**Scraping pattern:**
```bash
curl -sL -A "Mozilla/5.0" "https://search.certifications.sba.gov/profile/<UEI>/<CAGE>" | python3 -c "
import sys, re
html = sys.stdin.read()
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.S)
clean = re.sub(r'<[^>]+>', ' ', clean).strip()
clean = re.sub(r'\s+', ' ', clean)
for kw in ['suspended', 'certified', '8(a)', 'WOSB', 'EDWOSB', 'entrance date', 'exit date']:
    idx = clean.lower().find(kw.lower())
    if idx > 0:
        print(f'--- {kw} ---')
        print(clean[max(0,idx-100):idx+300])
        print()
"
```

---

## 2. OrangeSlices AI

**URL:** `https://orangeslices.ai/`

**What it provides:**
- Full task order ceiling values (not just obligations) for competitive awards
- Number of competitors beaten for an award
- Protest filings and outcomes with GAO file numbers and decision dates
- GAO decision digests (one-paragraph summaries)
- Set-aside type and solicitation number

**Why it matters:** USAspending only shows obligated amounts. For SeaPort-NxG and other IDIQ task orders, the ceiling can be 50-100x the current obligation. OrangeSlices reports the full ceiling and competitive details.

**Article URL pattern:**
- Award articles: `https://orangeslices.ai/<company>-beats-out-<n>-to-win-<value>m-<agency>-<scope>-task/`
- Protest articles: `https://orangeslices.ai/protest-filed-<agency>-<solicitation>-<protester>/`

**Search via Google News RSS:**
```bash
curl -sL "https://news.google.com/rss/search?q=site:orangeslices.ai+<company>&hl=en-US&gl=US&ceid=US:en"
```

---

## 3. GAO Bid Protest Docket

**URL:** `https://www.gao.gov/legal/bid-protests/search?processed=1&file=<docket_number>&outcome=all`
**Decision URL:** `https://www.gao.gov/products/b-<number>`

**What it provides:**
- Protester name, file number, decision date
- Outcome: Denied, Sustained, Withdrawn, Dismissed
- Full decision text and digest

⚠ **GAO.gov blocks curl with Akamai Access Denied.** Use a browser or rely on OrangeSlices AI articles which reliably report the GAO digest, file number, and outcome.

**Alternative: Search Google News for the GAO file number:**
```bash
curl -sL "https://news.google.com/rss/search?q=%22B-<number>%22&hl=en-US&gl=US&ceid=US:en"
```

---

## 4. cage.report

**URL:** `https://cage.report/SAM/<CAGE>`

**What it provides:**
- SAM registration details: CAGE, DUNS, UEI
- Entity structure, business start date
- Primary NAICS code from SAM
- Government business POC name and email
- SAM registration/expiration dates
- Historical SAM data snapshots

**Why it matters:** Often has more accurate address and POC data than USAspending. Shows the SAM primary NAICS which may differ from operational NAICS.

---

## 5. HigherGov

**URL:** `https://www.highergov.com/awardee/<company-slug>/`

**What it provides:**
- Federal awardee profile with UEI/CAGE
- NAICS classification
- Award history summary

---

## 6. Company Website Scraping Targets

When scraping a contractor's website, extract from specific pages:

| Page | What to Extract |
|------|----------------|
| `/about/` or `/about-us/` | Leadership team (CEO, President, CSO, CGO), founding date, ownership structure |
| `/clients/` or `/partners/` | Contract vehicles with full PIID numbers, client agencies |
| `/solutions/` or `/services/` | Service lines, specializations, platform expertise |
| `/newsroom/` | Recent awards, Inc. 5000 rankings, SBIR wins, JVs, rebrands |
| Footer | Legal entity name, DBA, copyright notice (confirms legal name) |
| `/careers/` | Open positions (indicates growth areas), office locations |

**Pattern:** Strip scripts/styles, extract text, search for keywords like "8(a)", "Inc. 5000", "SeaPort", "GSA", "JV", "SBIR".

---

## 7. Brand-New Entity Detection Checklist

When all USAspending queries return zero results, run this checklist:

| Check | Method | What It Reveals |
|-------|--------|----------------|
| Website "Coming Soon" status | Direct HTTP curl + source-code extraction | SAM registration inference, operational maturity |
| Domain age & prior ownership | `curl "https://web.archive.org/cdx/search/cdx?url=<domain>&output=text&limit=1&fl=timestamp,original"` | First archive date — if domain predates entity by years, it was repurposed |
| Wayback archive of prior entity | `web.archive.org/web/<timestamp>/<domain>` | Prior business name, industry, geographic focus |
| EIN prefix cross-check | IRS EIN prefix tables (prefix 01-06 = PA, 20-26 = VA, etc.) | State of principal owner vs stated entity state |
| Self-declared certifications | Website footer or Coming Soon page | DVOSB / SDVOSB claims that need verification |
| Named contact emails | Source-code extraction from Coming Soon page | Operational sophistication signal; not typical for first-time formations |
| SAM.gov HTTP probe | `curl -sL -o /dev/null -w "%{http_code}" "https://sam.gov/entity/<search-term>"` | 200 with SPA shell = no confirmed entity from public-facing search |
| SBA DSBS availability | `search.certifications.sba.gov` | 503 = system down, NOT confirmed absence |
| cage.report | `cage.report/SAM/search?q=<variant>` | 200 with PHP error/notice = no entity match |

**Key principle:** For brand-new entities, absence of records IS the story. Do not speculate about capability. Report confirmations of absence with honest confidence ratings.

**URL:** `https://www.linkedin.com/company/<company-slug>`

**What it provides:**
- Employee count estimate
- Headquarters and satellite offices
- Company description
- Recent posts (may announce contract wins)

⚠ LinkedIn requires JavaScript and/or authentication. Use Google News RSS or ddgr for LinkedIn-indexed content.
