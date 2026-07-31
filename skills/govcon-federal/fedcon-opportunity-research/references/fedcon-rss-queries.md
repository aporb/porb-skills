# Federal Contracting Research RSS Query Patterns

This file contains the complete list of Google News RSS query patterns used for federal contracting opportunity research, organized by source category.

## Base RSS URL

All queries use this base pattern:
```
https://news.google.com/rss/search?q=<QUERY>&hl=en-US&gl=US&ceid=US:en
```

Replace `<QUERY>` with any of the patterns below.

---

## 1. SAM.gov and Federal Solicitations (5 queries)

Primary source for active solicitation discovery.

```bash
# General SAM.gov solicitations
curl -sL "https://news.google.com/rss/search?q=SAM.gov+solicitation+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# Direct API attempts (often blocked, backup only)
curl -sL "https://api.sam.gov/entityapi/v2/opportunities?api_key=DEMO&postedFrom=06/30/2026&postedTo=07/07/2026&ptype=o&limit=50"

# Alternative SAM.gov API format
curl -sL "https://sam.gov/api/v1/opportunities?format=json&limit=50"

# Federal RFP searches
curl -sL "https://news.google.com/rss/search?q=federal+contract+opportunity+RFP+July+2026&hl=en-US&gl=US&ceid=US:en"
```

---

## 2. SBIR/STTR Open Solicitations (5 queries)

Target small business innovation research opportunities.

```bash
# SBIR/STTR general
curl -sL "https://www.sbir.gov/sbirsearch/solicitations?latest=open"

# SBIR/STTR specific queries
curl -sL "https://news.google.com/rss/search?q=SBIR+STTR+solicitation+2026&hl=en-US&gl=US&ceid=US:en"

# DoD SBIR
curl -sL "https://news.google.com/rss/search?q=DoD+SBIR+open+topic+2026&hl=en-US&gl=US&ceid=US:en"

# AFWERX SBIR
curl -sL "https://news.google.com/rss/search?q=AFWERX+SBIR+2026&hl=en-US&gl=US&ceid=US:en"

# NSF SBIR
curl -sL "https://news.google.com/rss/search?q=NSF+SBIR+pitch+2026&hl=en-US&gl=US&ceid=US:en"
```

---

## 3. Major GWAC/IDIQ Vehicle News (5 queries)

Monitor major contracting vehicles for task order opportunities.

```bash
# GSA MAS Schedule
curl -sL "https://news.google.com/rss/search?q=GSA+MAS+schedule+2026&hl=en-US&gl=US&ceid=US:en"

# General GWAC/IDIQ
curl -sL "https://news.google.com/rss/search?q=GWAC+IDIQ+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# NASA SEWP
curl -sL "https://news.google.com/rss/search?q=NASA+SEWP+2026&hl=en-US&gl=US&ceid=US:en"

# CIO-SP4
curl -sL "https://news.google.com/rss/search?q=CIO-SP4+2026&hl=en-US&gl=US&ceid=US:en"

# Alliant 3
curl -sL "https://news.google.com/rss/search?q=Alliant+3+2026&hl=en-US&gl=US&ceid=US:en"
```

---

## 4. FedScoop, GovConWire, Federal Times (3 queries)

Industry news sources with detailed solicitation coverage.

```bash
# FedScoop (sometimes 404s, backup)
curl -sL "https://news.google.com/rss/search?q=site:fedscoop.com+RFP+solicitation&hl=en-US&gl=US&ceid=US:en"

# GovCon Wire (highly reliable, full content)
curl -sL "https://news.google.com/rss/search?q=site:govconwire.com+opportunity+solicitation&hl=en-US&gl=US&ceid=US:en"

# Federal Times
curl -sL "https://news.google.com/rss/search?q=site:federaltimes.com+contract+opportunity&hl=en-US&gl=US&ceid=US:en"
```

---

## 5. Defense Innovation Programs (3 queries)

Defense Innovation Unit, NSIN, SOFWERX opportunities.

```bash
# DIU
curl -sL "https://news.google.com/rss/search?q=DIU+defense+innovation+contract+2026&hl=en-US&gl=US&ceid=US:en"

# NSIN
curl -sL "https://news.google.com/rss/search?q=NSIN+opportunity+2026&hl=en-US&gl=US&ceid=US:en"

# SOFWERX
curl -sL "https://news.google.com/rss/search?q=SOFWERX+2026&hl=en-US&gl=US&ceid=US:en"
```

---

## Capability-Specific Search Patterns

When focusing on specific capability areas (AI, cybersecurity, data, cloud):

```bash
# AI opportunities
curl -sL "https://news.google.com/rss/search?q=federal+AI+contract+solicitation+RFP+July+2026&hl=en-US&gl=US&ceid=US:en"

# Cybersecurity opportunities
curl -sL "https://news.google.com/rss/search?q=cybersecurity+contract+opportunity+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# DHS/CISA
curl -sL "https://news.google.com/rss/search?q=DHS+CISA+contract+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# DOJ/FBI
curl -sL "https://news.google.com/rss/search?q=DOJ+FBI+IT+contract+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# VA opportunities
curl -sL "https://news.google.com/rss/search?q=veterans+affairs+VA+IT+contract+RFP+2026&hl=en-US&gl=US&ceid=US:en"

# Set-asides
curl -sL "https://news.google.com/rss/search?q=set-aside+small+business+SDVOSB+contract+2026&hl=en-US&gl=US&ceid=US:en"

# Department of War contracts
curl -sL "https://news.google.com/rss/search?q=Department+of+War+contract+award+July+2026&hl=en-US&gl=US&ceid=US:en"
```

---

## Python RSS Parsing Script

Save this as `parse_rss.py` and use for all RSS feeds:

```python
import re

def parse_rss_feed(xml_file, limit=30):
    """Parse Google News RSS XML and extract items"""
    xml = open(xml_file).read()
    items = re.findall(r'<item>(.*?)</item>', xml, re.S)
    
    results = []
    for i, it in enumerate(items[:limit]):
        title = re.search(r'<title>(.*?)</title>', it, re.S)
        pub = re.search(r'<pubDate>(.*?)</pubDate>', it, re.S)
        link = re.search(r'<link>(.*?)</link>', it, re.S)
        src = re.search(r'<source[^>]*>(.*?)</source>', it, re.S)
        
        t = title.group(1) if title else 'N/A'
        t = re.sub(r'&[a-z]+;', ' ', t)
        p = pub.group(1) if pub else 'N/A'
        l = link.group(1) if link else 'N/A'
        s = src.group(1) if src else 'N/A'
        
        results.append({
            'index': i+1,
            'title': t,
            'date': p,
            'link': l,
            'source': s
        })
    
    return results

# Filter by date window
def filter_by_date_window(items, start_date, end_date):
    """Filter items within date window (YYYY-MM-DD format)"""
    # Implement date filtering logic here
    # Use datetime parsing on pubDate field
    filtered = [item for item in items if is_in_window(item['date'], start_date, end_date)]
    return filtered
```

---

## GovCon Wire Content Extraction

GovCon Wire provides the most complete solicitation details. Use this extraction script:

```python
import re

def extract_govconwire_content(html):
    """Extract title, meta description, and paragraphs from GovCon Wire article"""
    
    # Extract title
    title = re.search(r'<title>(.*?)</title>', html)
    title_text = title.group(1) if title else 'N/A'
    
    # Extract meta description
    meta = re.search(r'<meta name="description"[^>]*content="([^"]*)"', html)
    meta_text = meta.group(1) if meta else 'N/A'
    
    # Extract article paragraphs (first 15)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)[:15]
    
    content_paras = []
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if len(clean) > 50:
            content_paras.append(clean[:400])
    
    return {
        'title': title_text,
        'meta': meta_text,
        'paragraphs': content_paras
    }
```

---

## Execution Pattern

```bash
# 1. Create workdir
mkdir -p /tmp/govcon
cd /tmp/govcon

# 2. Fetch all RSS feeds in parallel
curl -sL "https://news.google.com/rss/search?q=SAM.gov+solicitation+RFP+2026&hl=en-US&gl=US&ceid=US:en" -o sam_news.xml
curl -sL "https://news.google.com/rss/search?q=SBIR+STTR+solicitation+2026&hl=en-US&gl=US&ceid=US:en" -o sbir.xml
curl -sL "https://news.google.com/rss/search?q=site:govconwire.com+opportunity+solicitation&hl=en-US&gl=US&ceid=US:en" -o govconwire.xml
# ... continue for all feeds

# 3. Parse and filter
python3 parse_rss.py

# 4. Fetch full articles from GovCon Wire for relevant items
curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  "https://www.govconwire.com/articles/<slug>" > article.html

# 5. Extract content
python3 extract_govcon.py article.html
```

---

## Known Issues and Workarounds

### SAM.gov API Blocks Access
```
HTTP/2 403 Forbidden
```
**Workaround:** Use Google News RSS and secondary sources (GovCon Wire, Federal News Network) that report on SAM.gov postings.

### SBIR.gov Blocks Access
```
403 Forbidden
```
**Workaround:** Use Google News RSS for SBIR topic discovery.

### Google News Redirects Require JavaScript
Google News RSS links contain encoded article IDs that require browser JavaScript to resolve.

**Workaround:** Use RSS feed for discovery, then fetch articles directly from source sites:
- GovCon Wire: `https://www.govconwire.com/articles/<slug>`
- FedScoop: `https://fedscoop.com/articles/<slug>`
- Federal Times: `https://federaltimes.com/articles/<slug>`

### FedScoop/DefenseScoop 404s
Some FedScoop and DefenseScoop article links return 404.

**Workaround:** Focus on GovCon Wire (most reliable) and Federal News Network via RSS. Mark 404 articles as unavailable and move on.

### GovCon Wire URL Patterns
URL slugs may not match exactly what you expect. Try variations:

- `https://www.govconwire.com/articles/tsa-13b-tsa-gold-plus-airport-screening-idiq-solicitation`
- `https://www.govconwire.com/articles/doi-484m-cisco-idiq-small-business`

Pattern: `https://www.govconwire.com/articles/<hyphenated-title>`

---

## Reliable Sources

| Source | Reliability | Content Depth | Best For |
|--------|-------------|---------------|----------|
| **GovCon Wire** | ⭐⭐⭐⭐⭐ | Full PWS, deadlines, values, set-asides | Solicitation details, contract awards |
| Federal News Network | ⭐⭐⭐⭐ | Good summaries, values, deadlines | Agency policy, major programs |
| OrangeSlices AI | ⭐⭐⭐⭐ | Small business focus, set-asides | Set-aside opportunities |
| Breaking Defense | ⭐⭐⭐⭐ | Defense tech, contracts | Defense-specific opportunities |
| PR Newswire | ⭐⭐⭐ | Contract award announcements | Award notifications |
| FedScoop | ⭐⭐⭐ | Tech-focused | IT/tech opportunities (some 404s) |
| DefenseScoop | ⭐⭐⭐ | Defense innovation | DIU, SOCOM, AI in defense (some 404s) |

---

## Output Structure

After parsing all feeds, structure findings as:

1. **Executive Summary** - Total opportunities, total value, key highlights
2. **Active Solicitations** - Open for bid, with deadlines
3. **Contract Awards** - Recent awards (task order opportunities)
4. **GWAC/IDIQ Awards** - Vehicle award announcements (task order pipeline)
5. **Major Programs** - Long-term strategic opportunities
6. **Small Business Set-Aside Summary** - Table of set-aside opportunities
7. **Recommended Actions** - Immediate, this month, ongoing

Save to: `~/govcon_research/raw/<date>/opportunities.md`