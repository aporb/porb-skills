# EXBS Program Intelligence Reference

> Domain knowledge bank compiled July 2026 for Leatherneck Federal Consulting LLC DFOP0018157 proposal — export control data analytics, AI, and trade diversion detection.

## CFDA Number Mapping

| Context | CFDA/Assistance Listing | Notes |
|---------|------------------------|-------|
| **USASpending (existing awards)** | 19.901 | Most EXBS cooperative agreements use this |
| **DFOP0018157 (new opportunity)** | 19.317 | Export Controls and Border Security |
| **EXBS Program CFDA (SAM.gov)** | 19.317 | Listed on simpler.grants.gov listing |

**Key insight:** The CFDA number shift from 19.901 to 19.317 means USASpending queries using `cfda_numbers: ["19.317"]` will find zero EXBS awards. Always search EXBS awards using either `cfda_numbers: ["19.901"]` or the agencies+keywords combo below.

## USASpending EXBS Award Query Recipe

```bash
# Proven: agencies + keywords combo (CFDA filter is unreliable)
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["02","03","04","05"],
      "agencies": [{"type":"awarding","tier":"toptier","name":"Department of State"}],
      "keywords": ["EXBS","Export Control","Border Security"],
      "time_period": [{"start_date":"2019-10-01","end_date":"2026-09-30"}]
    },
    "fields": ["Award ID","Recipient Name","Award Amount","Description",
               "cfda_number","Award Type","Start Date","End Date",
               "recipient_entity_type","Recipient UEI"],
    "limit": 100, "page": 1, "sort": "Award Amount", "order": "desc",
    "subawards": false
  }' | python3 -m json.tool
```

## EXBS Major Recipients (CFDA 19.901, FY2017–2026)

| Recipient | Typical Award Range | Primary Role |
|-----------|-------------------|-------------|
| CRDF Global (U.S. Civilian Research and Development Foundation) | $177K–$1.7M | Cadre of foreign STC experts, logistics, regional program management, Libyan Customs College, border guard training (Iraq/Jordan) |
| Middlebury College / MIIS | $642K–$2.48M | SSTMA Academy, legislative assistance, due diligence workshops, port state control |
| King's College London | $233K–$955K | Counter-proliferation financing, sanctions compliance, CPF controls platform |
| SUNY Research Foundation | $257K–$707K | ITT controls, STC implementation (Indonesia/Sri Lanka/Vietnam), microelectronics diversion |
| Culmen International, LLC | $579K–$5.2M | Border security academies (North Africa, Libya), SSTMA partner at UH |
| Institute for Science and International Security | $703K | PPI tracking 200 countries including 57 EXBS partners |
| Conflict Armament Research Ltd. | $983K | Iranian materiel attribution toolkit |
| CCSI (Compliance and Capacity Skills International) | $346K–$360K | Chemical/missile interdiction training |
| World Learning Inc. | $1.3M–$1.85M | EXBS logistics support |
| Sincerus Global Solutions Inc. | $452K–$586K | Counter-IED technical assistance (East Africa) |
| UNODC | $194K–$1.15M | Investigative/prosecutorial capacity building |
| IOM (International Organization for Migration) | $73K–$1.53M | Border security systems, MIDAS deployment |

## EXBS Five Core Assistance Areas

Per CBP EXBS Program Overview:
1. **Laws and Regulations** — Drafting and strengthening legal frameworks
2. **Licensing** — Building licensing capacity for dual-use and military items
3. **Enforcement** — Border security, customs, investigation capabilities
4. **Government-Industry Cooperation** — Public-private partnerships for compliance
5. **Interagency and International Cooperation and Coordination**

## SSTMA (Security & Strategic Trade Management Academy)

- **Current Host (2023+):** University of Houston, Cullen College of Engineering Technology Division
- **Implementation Partner:** Culmen International, LLC + Borders, Trade and Immigration Institute
- **Prior Host:** Middlebury College / MIIS (through 2022)
- **Format:** Two-week residential academy, up to 30 participants per session
- **Curriculum areas:** International law, public policy, supply chain/logistics, transportation policy, cybersecurity, program management, non-proliferation, enforcement
- **NOFO SFOP0009793 / SFOP0006758:** ~$1.5M cooperative agreement for continuation
- **Evaluation:** Aug 2024 SSTMA Evaluation Executive Summary classifies SSTMA as "high-cost event" with "significant strategic value"

## Key Data Sources for Export Control Trade Analysis

| Source | Use |
|--------|-----|
| UN Comtrade | Global bilateral trade flow analysis |
| ITC Trade Map | Market access, export/import data visualization |
| Panjiva / S&P Global | Maritime shipping data, bills of lading |
| Harmonized System (HS) Codes | Mapping controlled items to trade data |
| ECCN / EU Dual-Use List | Export control classification |
| Wassenaar Arrangement Lists | Multilateral regime standards |
| Automated Export System (AES) | U.S. export declarations |
| OpenCorporates / Orbis | Beneficial ownership, shell company detection |
| Denied Parties Lists | Consolidated screening |

## Diversion Detection Methodologies

1. **Trade Discrepancy Analysis** — Comparing Country A exports vs Country B imports
2. **HS Code Jump Analysis** — Detecting reclassification of controlled items into uncontrolled categories
3. **Unit Price Anomaly Detection** — Declared value vs known market prices
4. **Transshipment Hub Identification** — High-risk transit points
5. **End-Use/End-User Verification** — Cross-referencing trade data with known proliferation entities
6. **Network Analysis** — Corporate ownership mapping for shell companies and front organizations

## Competitive Landscape for DFOP0018157

- **No prior EXBS data analytics/AI cooperative agreements identified** — this is a new niche
- **No SDVOSB incumbents in EXBS** — Leatherneck would be first-mover with SDVOSB status
- **Key differentiator:** Tech-forward positioning (data science, AI/ML, mobile apps) vs. traditional incumbent approach (think tanks, academic training, logistics)
- **For-profit allowed but no profit** — eligible but must demonstrate cost-structure-as-direct-program-expenses
- **Single $5.9M award** — more than double the largest EXBS cooperative agreement (SSTMA $2.48M)

## C4ADS Methodology Note

C4ADS uses publicly available information (PAI) for data-driven, tech-powered investigations into illicit networks. Their NTI partnership tested scalable analytic approaches to detect high-risk trade in trade data, finding that list-based screening methodologies have limited effectiveness — they recommend advanced analytics approaches. This finding supports the rationale for DFOP0018157's data analytics component.