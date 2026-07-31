# VA GenISIS Program — Domain Intelligence

## Critical: GenISIS ≠ Generic IT

GENISIS stands for **Genomic Information System for Integrative Sciences** — a VA Office of Research & Development (ORD) high-performance computing platform supporting the **Million Veterans Program (MVP)**. It is NOT a generic IT program name. When you see "GenISIS" in a solicitation title, the scope is genomics HPC infrastructure, not general-purpose IT.

## Program Ecosystem (USASpending-verified)

| Component | Current Contractor | Value | Period | Award ID |
|---|---|---|---|---|
| GenISIS Sustainment | GOVCIO, LLC | $11.5M | 2022-2027 | 36C10B22N10030035 |
| Previous Sustainment | GOVCIO, LLC | $10.0M | 2017-2022 | VA11817F10030016 |
| GenISIS 2 Sustainment | LIBERTY IT SOLUTIONS | $9.6M | 2018-2023 | 36C10B18N10150032 |
| Hardware Tech Refresh | EPOCH CONCEPTS LLC | $13.9M | 2023-2025 | 36C10A23F0110 |
| WAF + Firewall | EPOCH CONCEPTS LLC | $367K | 2024-2028 | 36C10B24F0398/0397 |
| HPC Maint Support | EPOCH CONCEPTS LLC | $241K | 2025-2027 | 36C10B25F0189 |
| Red Hat Software | ARCHITECHTURE SOLUTIONS | $372K | 2022-2025 | 36C10B22F0100 |
| Storage/Compute (historical) | MERLIN INTERNATIONAL | $687K | 2012-2013 | VA11812F0063 |
| SAS License | EXECUTIVE INFORMATION SYSTEMS | $215K | 2023-2026 | 36C10B23F0158 |
| ImageX Platform | MEDICOM TECHNOLOGIES | $117K | 2025-2027 | 36C10B25C0024 |

## SIEM Component — IBM QRadar-based

The VA's GenISIS security monitoring runs on IBM QRadar SIEM. Historical QRadar contracts:

| Contractor | Value | Period | Award ID |
|---|---|---|---|
| CYNERGY PROFESSIONAL SYSTEMS | $6.3M | 2018-2023 | 36C10A18F0329 |
| THUNDERCAT TECHNOLOGY | $0 (SaaS) | 2020-2023 | 36C10B20F0313 |
| V3GATE, LLC | $111K | 2022-2023 | 36C10B22F0168 |
| METGREEN SOLUTIONS | $114K | 2019-2020 | 36C10B19F0319 |
| I3 FEDERAL LLC | $423K | 2016-2017 | VA11817F1765 |

## Incumbent Chain for SIEM Task Order (36C10B26Q0650)

The Sources Sought 36C10B26Q0650 is specifically for "SIEM software and support, New Task Order (VA-26-00049417)" under the GenISIS umbrella. The SIEM component has historically been handled separately from the main GenISIS sustainment contract. Key incumbents:

1. **CYNERGY** ($6.3M QRadar SIEM, 2018-2023) — largest previous SIEM-only contract
2. **EPOCH CONCEPTS** — current holder of GenISIS security components (WAF, firewall, HPC maintenance)
3. **GOVCIO** — current GenISIS sustainment prime ($11.5M, may subcontract SIEM)

**Merlin International**: Had one GenISIS hardware contract in 2012 ($687K storage/compute nodes). NO subsequent GenISIS contracts. NOT the SIEM incumbent.

**Peraton Inc.**: Major VA contractor ($121M IaaS, $6.5M EPMS) but NO direct GenISIS SIEM contracts in USASpending. May be involved through subcontracting.

### 2026-07-18 Research Update — RFI 36C10B26Q0650 (CORRECTED)

**This is an RFI, NOT a Sources Sought.** The previously documented classification as "Sources Sought" was incorrect — the solicitation document itself is titled "Request for Information." The SAM.gov metadata was misleading (the SAM.gov public UI may label RFIs as "Sources Sought" in the notice-type chip). Trust the document title over the UI label.

**RFI metadata (from extracted documents):**
- RFI Solicitation #: 36C10B26Q0115
- Task Order #: VA-26-00049417
- Response Deadline: **July 28, 2026, 12:00 PM EST** (NOT July 23 — the July 23 date was from incomplete SAM.gov UI extraction)
- PSC: 7A20 (IT and Telecom - Application Development Software) — NOT DB01
- NAICS: 541519, 150 employees
- Set-Aside: SDVOSB anticipated
- Page Limit: **10 pages** with strict content requirements (no marketing materials, no generic capability statements)
- POC: Ethan Goldring, Ethan.Goldring@va.gov, 848-377-5180
- CO: Edward Hebert, Edward.Hebert@va.gov, 848-377-5040
- VA PM: Brian Ibbison, brian.ibbison@va.gov, 774-826-1269
- COR: Margaret Mitchell, Margaret.Mitchell@va.gov, 571-394-3108
- Place of Performance: VA Boston HCS (Boston, MA) + VA Pittsburgh HC (Pittsburgh, PA)

**Attachments (extracted successfully from local cache):**
- `36C10B26Q0650.docx` (108 lines) — RFI instructions, response requirements, submittal info
- `FY26-PD-GenISIS-SIEM Draft.docx` (436 lines) — Full Product Description with ~108 discrete requirements across 5 tables

**PD Requirements Summary:**
- Table 1 (Platform, 11 items): Air-gapped self-hosted Docker container-native, 3+ data centers, 1,000-3,000 endpoints +10% annual growth, OMB M-21-31 EL2 at delivery + EL3 roadmap within 12 months, NIST SP 800-137 Continuous Monitoring Plan within 60 days
- Table 2 (Observability, 19 items + sub-items): Full protocol suite (syslog/WMI/JDBC/SNMP/IPFIX/PCAP), DLP integration with 12+18 month retention, passive DNS, near-real-time ≤5 min ingestion, OMB M-21-31 Appendix C full retention matrix
- Table 3 (Discovery, 27 items): Full-text/regex/plain-English search, statistical operations, custom search commands via DSL/API, set operations, <15s search for ~5TB
- Table 4 (Telemetry, 13 items): Multi-threshold per element, >5M records 3x daily
- Table 5 (Enterprise Command Center, 17 items + sub-items): Predictive analytics, SOAR readiness assessment within 90 days, UBA roadmap within 90 days, CISA/FBI data export, automated anomaly detection, behavioral analysis
- Compliance: Section 508 WCAG 2.0 AA, ENERGY STAR/EPEAT, VA TRM, SSN reduction, IPv6 native + dual stack
- Period: Base year + 3 option years (4-year total support)

**USAspending VA Enterprise SIEM Incumbent Analysis (2026-07-18, multi-keyword queries):**

VA is a dual-platform SIEM shop — both IBM QRadar and Splunk are heavily deployed:

**IBM QRadar at VA:**
| Contractor | Value | Award ID | Description |
|---|---|---|---|
| Four Points Technology (SDVOSB) | $2.59M | VA11818F2496 | QRadar maintenance for 223 deployed licenses |
| Premier Technical Services | $3.22M | VA11815F0225 | QRadar hardware + software licenses + maintenance |
| i3 Federal LLC | $610K | VA11816F1517 | QRadar Core Appliance + maintenance |
| i3 Federal LLC | $423K | VA11817F1765 | QRadar SIEM software maintenance |
| Merlin International (SDVOSB) | $591K | VA11816F0536 | QRadar SIEM software maintenance |

**Splunk at VA:**
| Contractor | Value | Award ID | Description |
|---|---|---|---|
| Red River Technology | $11.6M | VA11816F1139 | Splunk Enterprise license + support |
| ThunderCat Technology (SDVOSB) | $3.25M | VA11817F2334 | Splunk UBA + professional services for NSOC |
| ThunderCat Technology (SDVOSB) | $254K | VA11817F2107 | Splunk Enterprise license + install |
| Alvarez LLC (SDVOSB) | $176K | VA11815F0128 | Splunk |
| Sterling Computers (SDVOSB) | $51K | VA11816F0813 | Splunk |
| V3Gate LLC (SDVOSB) | $87K | VA11815F0424 | Splunk Enterprise + services |

**GenISIS Program Incumbents (USASpending keyword: "GenISIS"):**
| Contractor | Value | Award ID | Description |
|---|---|---|---|
| GovCIO, LLC | $10.01M | VA11817F10030016 | GenISIS Sustainment (PRIMARY) |
| Booz Allen Hamilton | $914K | VA119A15J0193 | GenISIS Analysis & Strategy Support |
| The MITRE Corporation | $3.77M | VA118A15J0272 | GenISIS FFRDC Support |
| Minburn Technology Group | $2.42M | VA11817F2380 | GenISIS Hardware Refresh |

**Key Observations:**
1. **GenISIS IS the genomics program.** The GenISIS PIA (Dec 2024) confirms: ~230 HPC compute nodes, ~10PB storage, Boston + Pittsburgh sites, serves Million Veteran Program (MVP) with genomic data on 1M+ Veterans. There is no separate "Generalized Integrated Security Information System" — that was a speculative alternative expansion that doesn't exist. The PD explicitly says "VA Center for Data and Computational Sciences (C-DACS)... for the Veterans Health Administration (VHA)... research data and analysis systems for the VA Office of Research and Development (ORD)." This is the genomics HPC environment.
2. **GovCIO is the dominant GenISIS incumbent** at $10M+. They likely have the inside track on any GenISIS-related procurement.
3. **The SDVOSB reseller model is well-established at VA.** Multiple SDVOSB primes have successfully resold Splunk and QRadar through NASA SEWP and GSA Schedule vehicles. This is the standard procurement pattern.
4. **Both Splunk and QRadar are already in the VA TRM.** Any new SIEM that isn't already TRM-listed faces an additional adoption barrier.
5. **The "SIEM matches Siemens" pitfall is real.** The USASpending keyword search for "SIEM" returns Siemens-dominated results. Always use product names (Splunk, QRadar, ArcSight) or program names (GenISIS) as keyword surrogates, not the generic "SIEM" string. Confirmed working: the `"QRadar"` keyword as the most selective SIEM proxy for VA-specific queries.

**Non-Manufacturer Rule for SDVOSB SIEM Resellers:** For this product procurement, the SDVOSB prime must comply with the non-manufacturer rule (13 CFR 121.406). Splunk, IBM, and Elastic are all large businesses — resellers need either a non-manufacturer rule waiver or must navigate the "cost of materials" exclusion under VAAR 852.219-73(d)(2)(i). See `references/sdvosb-product-procurement-patterns.md`.

## Research Pitfalls Specific to GenISIS/SIEM

### "SIEM" keyword problem
Searching USASpending or SAM.gov for "SIEM" returns **SIEMENS-dominated results**. The five letters "SIEM" match Siemens Healthcare, Siemens Industry, and Siemens Government Technologies — all large VA contractors at much higher dollar values than the actual SIEM contracts. Solutions:
- Use `"Security Information and Event Management"` as exact phrase (16 chars, distinctive)
- Use `QRadar` as keyword surrogate (IBM's SIEM product used by VA)
- Search for `GenISIS` and manually filter for security-scoped contracts (WAF, SIEM, firewall)
- Combine `GenISIS` + `SIEM` keywords (NOT `Merlin` + `SIEM` — Merlin matches Siemens)

### Program name ambiguity
"GenISIS" is also a company name (GenISIS Global LLC, an unrelated fuel-tank repair contractor). Always filter GenISIS search results by:
- Awarding office prefix `36C10*` (VA TAC NJ)
- PSC code: DB01, 7A20, 7J20 (IT security/compute)
- Description containing "VA" "Veterans" "genomic" or "MVP"

### Attachment download
SAM.gov attachment download requires JavaScript execution in an authenticated browser context. The browser tool's click on attachment links does NOT trigger a file download (the SAM.gov Angular app uses service workers and blob APIs). Accept this limitation and extract PWS content from:
1. The solicitation description field (often blank — "intentionally left blank")
2. Secondary sources (GovTribe, Bloomberg Gov, FPDS if mirrored)
3. USASpending award descriptions for scope inference
4. Direct inquiry to the Contracting Officer (email the POC)