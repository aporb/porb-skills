# DOE/NNSA Nuclear Fabrication & Fuel Supply Market Research

## When to Use
Researching the DOE/NNSA nuclear fabrication, fuel supply, or advanced reactor market — TerraPower Natrium, X-energy TRISO-X, Centrus enrichment, HALEU supply chain, SMR/microreactor deployment, or nuclear component fabrication. This market is **not well captured by USASpending API** because most spending flows through DOE cooperative agreements (ARDP), cost-share arrangements, NNSA direct contracts, and private investment. Web-search-based research is the primary methodology.

## Market Overview

The U.S. nuclear fabrication market is undergoing its largest expansion since the 1970s due to:
- **Advanced Reactor Demonstration Program (ARDP):** $3.6B+ DOE cost-share commitment for TerraPower Natrium + X-energy Xe-100
- **HALEU supply chain buildout:** DOE HALEU Availability Program allocating 21+ metric tons; Centrus $900M+ enrichment expansion at Piketon, OH
- **NNSA pit production:** Up to $25B SRPPF at Savannah River Site (50 pits/year by ~2030)
- **Nuclear microreactors for military installations:** ANPI program — Radiant (Buckley SFB), Westinghouse (Malmstrom AFB), Antares (JBSA) — first deployments 2028
- **SMR deployment program:** $900M DOE fund; TVA $400M grant + NuScale up to 6 GW
- **Sentinel ICBM modernization:** $13.3B EMD phase, launch infrastructure EPC by Bechtel
- **Hanford WTP vitrification:** $12-20B waste treatment plant; hot commissioning began Oct 2025

## Key Entities

| Entity | Role | Key Programs | Estimated Budget |
|--------|------|-------------|------------------|
| **Bechtel National Inc.** | EPC prime for DOE/NNSA mega-projects | Natrium, Sentinel, WTP, Naval Nuclear, Y-12, WIPP | $12-25B per major project |
| **Centrus Energy (NYSE: LEU)** | Only U.S. HALEU producer; LEU enrichment | Piketon expansion, HALEU production, $900M DOE enrichment contract | $1.2B+ raised; $2.3B backlog |
| **TerraPower** | Natrium SFR (345 MWe + storage) | $4B demonstration at Kemmerer, WY; NRC permit issued March 2026 | $2B DOE + $2B private |
| **X-energy** | Xe-100 HTGR + TRISO-X fuel | TRISO-X facility Oak Ridge, TN; ARDP $1.6B | $1.6B DOE cost-share; Amazon $500M |
| **Westerman Inc.** (Bremen, OH) | Largest U.S. UF6 cylinder manufacturer | Cylinder types 5B/12B/30B/48G/48X/48Y; ANSI N14.1/NQA-1/10CFR71 | ~$72M (2012); $300M+ gov services group in build |
| **Radiant Nuclear** | Portable microreactor (Kaleidos, 1 MWe) | Buckley SFB deployment 2028; DIU/ANPI; DOE HALEU allocation | Pre-revenue; VC/DOE funded |
| **Kairos Power** | Molten salt reactor (Hermes) | Oak Ridge demonstration; NRC permit issued 2023 | $303M ARDP fixed-price |
| **Fluor Federal Services** | SRPPC construction management at SRS | Pit production facility, HFTOC training center | Part of $25B SRPPF |
| **Northrop Grumman** | Sentinel ICBM prime contractor | Sentinel EMD $13.3B; 450 silos, 24 launch centers | $13.3B EMD + production |
| **Global Nuclear Fuel (GNF-A)** | GE-led JV; Natrium fuel fabrication | $200M+ Natrium Fuel Facility near Wilmington, NC | Joint TerraPower/DOE funded |

## Research Methodology

### Phase 1: Company Press Releases (Primary Source)
Nuclear market announcements are almost always published as press releases, not contract awards. Key sources:

```python
# Research pattern: company + program + "announces" / "awarded" / "selected"
queries = [
    # Per company
    f"{company_name} {program_name} contract award {year_range}",
    f"{company_name} {program_name} DOE announcement",
    f"{company_name} {program_name} NRC application",
    # Per project
    f"{project_name} {data_point} {year_range}",
    f"{project_name} cost estimate",
    f"{project_name} construction timeline"
]
```

Source priority:
1. **Company press releases** (prnewswire.com, company newsrooms) — most accurate for program details
2. **DOE/NNSA press releases** (energy.gov, nnsa.energy.gov) — authoritative for DOE-funded programs
3. **SEC filings** (sec.gov) — for public companies (Centrus LEU, Bechtel subsidiary filings)
4. **Industry trade press** (ans.org/news, world-nuclear-news.org, powermag.com, enr.com)
5. **NRC documents** (nrc.gov) — for licensing milestones and construction permits
6. **DOE HALEU Allocation Program** (energy.gov/ne) — for HALEU fuel allocation data
7. **GAO reports** (gao.gov) — for cost/schedule assessments of major DOE programs

### Phase 2: Parallel Web Search by Topic
Split the research into independent subtopics and search simultaneously:

```
Topic 1: "TerraPower Natrium $4 billion schedule NRC permit 2026"
Topic 2: "Centrus Energy Piketon expansion 900 million GE Vernova contract"
Topic 3: "TRISO-X Oak Ridge NRC 40-year license HALEU allocation 2025"
Topic 4: "Westerman Inc UF6 cylinders Bremen Ohio Centrus HALEU supply chain"
Topic 5: "Radiant Kaleidos microreactor ANPI Buckley Space Force Base 2028"
Topic 6: "Anduril Industries Arsenal manufacturing subcontracting nuclear"
...
```

Run 4-6 searches in parallel across all subtopics. Web_search with the Firecrawl MCP provider works well for these queries (DOE/company press releases are well-indexed). If firecrawl_search or web_search fail, fall back to:
1. `ddgr` (DuckDuckGo CLI) — `/usr/bin/ddgr --json -n 10 "query"`
2. Browser navigation to specific press release sites

### Phase 3: Extract & Cross-Reference
Key data points to extract for each entity:
- **Contact value/DOE funding** — distinguish between "total program cost," "DOE share," and "private investment"
- **Key milestones** — NRC actions, construction milestones, planned operational dates
- **Supply chain position** — which tier (prime/subcontractor/vendor), what they supply, who they supply
- **Certifications** — NQA-1, 10CFR71, ANSI N14.1, ASME code stamps
- **Key personnel** — government services leads, business development contacts
- **Subcontracting channels** — bechtel.com/supplier, WTP monthly awards, supplier portals

Cross-reference claims: A company press release may say "$2B DOE award" while the actual DOE cooperative agreement is "$2B cost-share (50%)" meaning real DOE funding is $1B over 7 years. Always check the source document.

### Phase 4: Report Structure
For a DOE/NNSA nuclear market landscape report, organize by:

1. **Landscape overview** — market size, tailwinds, key trends
2. **Per-project/topic deep dives** — program details, timeline, budget, key players, supply chain
3. **Prime contractor analysis** — Bechtel, Fluor, Northrop Grumman, Centrus — their project portfolio and subcontracting channels
4. **Supplier/Vendor positioning** — where Westerman and similar fabricators fit
5. **Strategic implications** — for the specific client/subcontractor being positioned
6. **Key contacts & resources** — decision-makers, portal URLs, procurement channels

**Format:** For internal intelligence/research, structured markdown is acceptable. For client-facing deliverables, convert to self-contained HTML using the Thariq/html-effectiveness aesthetic (see `html-briefing` skill).

## Key Supply Chain Links

| Supplier Type | Companies | Demand Driver |
|--------------|-----------|---------------|
| UF6 Cylinders | **Westerman Inc.** (sole domestic mfr) | Centrus enrichment expansion, HALEU transport |
| Pressure Vessels | Westerman, Precision Custom Components, BWX Technologies | SRPPF, WTP, advanced reactor fabrication |
| TRISO Fuel Fabrication | X-energy (TRISO-X), Standard Nuclear, GEH | Xe-100, Kaleidos, eVinci |
| HALEU Enrichment | **Centrus Energy** (sole domestic) | All advanced reactors |
| HALEU Deconversion | Six firms named Oct 2024 (BWX, GE-Vernova, etc.) | HALEU UF6 → oxide/metal conversion |
| EPC/Construction | Bechtel, Fluor, AECOM, Geiger Brothers | Natrium, WTP, SRPPF, Sentinel, Piketon |
| NQA-1 Certified Fab | Westerman, BWXT, Precision, Curtiss-Wright | All nuclear projects |

## Key Contacts Referenced

| Contact | Role | Organization | Channel |
|---------|------|-------------|---------|
| Douglas J. Henderson | Dir. Government Services (JD, MBA, MS CS, PMP) | Westerman Inc. | LinkedIn (Columbia, SC) |
| Dave Cline | Sales (Nuclear) | Westerman Inc. | Dave.cline@westermaninc.com |
| Amir Vexler | CEO | Centrus Energy | centrusenergy.com |
| Dan Leistikow | VP Corporate Communications | Centrus Energy | centrusenergy.com |
| Doug Bernauer | CEO & Founder | Radiant Nuclear | radiantnuclear.com |

## Pitfalls

- **DOE cooperative agreements ≠ contracts.** ARDP awards are cost-share arrangements, not traditional procurement contracts. They don't appear in USASpending.gov as standard awards.
- **"Billion" vs "million" in headlines.** Many trade press headlines round aggressively — always verify exact figures from the primary DOE document or SEC filing.
- **Program delays are the norm.** The Natrium project was originally targeted for 2027; NRC permit came in 2026, pushing operations to ~2030. Assume all advanced reactor timelines will slip 2-4 years.
- **Westerman has zero direct public company presence.** No SEC filings, no investor relations — they're private (formerly a Worthington subsidiary, acquired 2012, since divested). All information comes from their website, DOE RFI responses, and LinkedIn.
- **"Westerman" search noise.** The name clashes with a UK indie musician (Will Westerman). Use `"Westerman Inc"`, `"Westerman Nuclear"`, or `"Westerman UF6"` to filter.
- **Centrus has NOT acquired Westerman.** They have a strategic supply chain relationship (Westerman supplies Centrus with UF6 cylinders and requested HALEU consortium inclusion). No M&A deal has been announced. Do not report as an acquisition.
- **Radiant and X-energy are DIFFERENT companies.** Radiant (Kaleidos microreactor, 1 MWe) is separate from X-energy (Xe-100 HTGR). They share TRISO fuel technology but have different reactor designs, investors, and target markets. Do not conflate them.
