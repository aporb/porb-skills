# Determining NEW WORK vs RECOMPETE for a SAM.gov Notice ID

Verified 2026-07-18 (two batches: 8-example batch + 7-example medical/training/curriculum batch). Used when the user hands a list of SAM.gov Notice IDs and wants to know whether each is new work or a recompete/continuation, plus the prior incumbent.

## Core insight

**SAM.gov Notice IDs are not on USAspending.** A Notice ID (e.g. `36C26226Q1049`) identifies a *solicitation* — a pre-award instrument. USAspending only holds *awards*. So a direct keyword search for the Notice ID on `spending_by_award` returns an empty `results` array. This is the single most common trap and the reason the task feels "impossible" until you flip to topic+agency search.

## Method that works

1. Open the SAM.gov notice detail page (via search box, see below) to read the title, description, PSC/NAICS, and contracting office. The title and description usually telegraph recompete vs new work (phrases like "New Task Order", "Annual Support Renewal", "Sustainment", "Continuation", "FY27+", "Recompete").
2. Pull the **contracting-office prefix** from the Notice ID — the first ~6 chars before the year/fiscal-segment. Examples:
   - `36C26226Q1049` → office prefix `36C262` (VA NCO 22)
   - `FA303026Q0029` → office prefix `FA3030` (Air Force 17 CONS, Goodfellow AFB)
   - `7571TE26Q00124` → office prefix `7571TE` or recipient-award prefix `75N98` / `75H710` (NIH/HHS)
   - `36C10B26Q0658` → office prefix `36C10B` (VA TAC NJ) / incumbent award prefix `36C263` (VISN 23)
   - `36C10B26R0017` → office prefix `36C10B` (VA TAC NJ) — same office awarded prior `36C10B23F0345` (VISN 5 RFID) to VIT LLC
   - `M0068126Q0063` → office prefix `M00681` (USMC Camp Pendleton CG) — same office awarded prior `M0068124P0008` (TCCC) to Templar Medical LLC
   - `36C24426Q0800` → office prefix `36C244` (VA NCO 4 / VISN 4) — same office awarded annual MedBridge chain `36C24421N0971`..`36C24426N0002`
   - `N0018926RW025` → office prefix `N00189` (NAVSUP WSS Mechanicsburg) — same office awarded prior `N0018918PQ058` (NAVSUP WSS ERP TRAINING) to Purdy Group LLC
   - `FA254926R0002` → office prefix `FA2549` (STARCOM Contracting PK, Patrick SFB) — only 2 prior awards under this office, neither matching the new Civilian Guardian Course scope
3. Query USAspending `spending_by_award` by **topic keyword + awarding agency/subtier**, optionally filtered by NAICS, and scan the results for prior awards whose `Award ID` starts with the same office prefix (or with a related NIH/HHS recipient-prefix like `75N98`, `75H710`). The recipient on the most recent same-office same-topic award is your incumbent.
4. Verify the incumbent chain by running a second `spending_by_award` query with the prior Award ID as the keyword — returns the exact prior award record (recipient, value, POP) if you guessed the prefix right. Also run a recipient-name search to see all their awards — confirms whether the office prefix is used consistently (e.g. searching "Veteran Information Technologies" confirms VIT's 36C10B RFID awards and reveals additional VISN-5 VSS/PACS awards).

## Keyword strategy — single tokens only (CRITICAL)

**USAspending `spending_by_award` keywords do NOT do phrase matching.** Multi-word queries return empty results — this is NOT a "no awards exist" signal, it is a query-shape failure.

| Query shape | Result | What it means |
|---|---|---|
| `["Civilian Guardian Course"]` | 0 results | Phrase not indexed as a single token — useless |
| `["Civilian Guardian"]` | 0 results | Two-word phrase — still fails |
| `["MedBridge"]` | 8 results | Single token — works, surfaces MedBridge Education LLC chain |
| `["Templar Medical"]` | 9 results | Two-word *entity name* — works because the recipient name is a single indexed token group |
| `["RFID"]` | 8 results | Single token — works, surfaces VIT LLC via 36C10B23F0345 |
| `["Tactical Combat Casualty Care"]` | 10 results | Multi-word phrase — *works* here because the phrase appears as a literal in award descriptions |
| `["NAVSUP WSS OJT"]` | 0 results | Fails — too specific |
| `["NAVSUP WSS"]` | 8 results | Works — appears in many award descriptions |

**Rules of thumb:**
- **Start broad with a single-token keyword** ("RFID", "MedBridge", "TCCC", "Guardian", "IHS", "NAVSUP").
- **Two-word entity names work** ("Templar Medical", "Purdy Group", "Veteran Information Technologies") because the recipient-name field is one logical token.
- **Multi-word topical phrases are hit-or-miss** — "Tactical Combat Casualty Care" works (it's a canonical program name in DoD award descriptions) but "Civilian Guardian Course" does not (too novel/specific).
- **Iteratively broaden**: if the first keyword returns 0, try a broader single token, a related term, or the recipient's known name. The VIT RFID example required trying "VISN 5 RFID", "asset awareness", and "Veteran Information Technologies" before the full chain surfaced.
- **Cross-check by recipient name**: once you have a candidate incumbent, search the recipient name to see ALL their awards — this confirms the office-prefix pattern and reveals related awards the topic keyword missed.
- **Run 2-3 complementary single-token queries for broad-scope opportunities.** When an RFI spans hardware + software + sustainment (e.g. "Patient Queuing Kiosks"), a single keyword surfaces only one vendor ecosystem. Run "kiosk" AND "queuing" AND "patient kiosk" as separate queries — each surfaces different incumbents, different NAICS codes, and different contracting offices. Merge the result sets to build the full competitive landscape before classifying the opportunity as new work vs recompete. A "no incumbent" verdict from one query is not reliable without complementary queries.

## API contract quirk (must follow)

`filters.award_type_codes` must contain codes from **exactly one** award-type group:

- contracts: `A` (BPA Call), `B` (Purchase Order), `C` (Delivery Order), `D` (Definitive Contract)
- idvs: `IDV_A`..`IDV_E` (GWAC / IDC / FSS / BOA / BPA)
- grants, loans, direct payments, other_financial_assistance — separate groups

Mixing groups (e.g. `["A","B","C","D","IDV_A"]`) returns HTTP 400 with the `"'award_type_codes' must only contain types from one group"` message and a description of all valid groups. For NEW-vs-RECOMPETE work on contract solicitations, use `["A","B","C","D"]` only. IDV ceilings/vehicles are out of scope for this task.

## Query template (incumbent discovery)

```bash
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["A","B","C","D"],
      "keywords": ["<topic-1>","<topic-2>"],
      "agencies": [{"type":"awarding","tier":"subtier","name":"<Agency Name as in USAspending>"}]
    },
    "fields": ["Award ID","Recipient Name","Start Date","End Date","Award Amount","Description","NAICS Code"],
    "limit": 25, "page": 1, "sort":"Award Amount","order":"desc"
  }'
```

**Agency-name gotcha:** the `agencies[].name` must match the USAspending subtier label verbatim. Working examples:
- `Department of Veterans Affairs`
- `Department of the Air Force`
- `Indian Health Service`
- `Department of Health and Human Services` (for NIH unless you can use sub-agency)

Pipe results through `python3 -c "import sys,json; d=json.load(sys.stdin); [print(r.get('Recipient Name'),'|',r.get('Award ID'),'|',r.get('Award Amount'),'|',r.get('Start Date'),'-',r.get('End Date'),'|',(r.get('Description') or '')[:120]) for r in d.get('results',[])]"` for a quick scan.

## Title / type signals (from SAM.gov notice)

| Signal in title or description | Read as |
|---|---|
| "New Task Order" + Sources Sought | Recompete — competed as a new TO under an existing IDV/GWAC; the *capability* is incumbent-held, the *vehicle* may differ |
| "Annual Support Renewal", "Sustainment", "Maintenance", FY-year in title | Recompete / continuation — recurring annual license/support buy |
| "Sources Sought" / "Request for Information" with no incumbent pattern on USAspending | Likely new work — capability being scoped for the first time |
| "Recompete", "Continuation", "Follow-on" in title or description | Recompete (explicit) |
| Solicitation under an existing BPA/IDIQ/GWAC (vehicle ID referenced) | Recompete at the TO level — incumbent may or may not be on the parent vehicle |
| Notice ID position-7 letter = **Q** or **R** | Solicitation (Combined Synopsis/Solicitation or full Solicitation) — full detail page on SAM.gov |
| Notice ID position-7 letter = **W** | Special Notice / Sources Sought / RFI — often NOT in active SAM.gov search results after response date (short visibility window) |
| Notice ID position-7 letter = **P** | Purchase Order — already awarded; rare to see as a notice |

## SAM.gov notice detail page (browser workflow)

**Do NOT** navigate to `https://sam.gov/opp/<notice-id>/view` — it 404s. The Notice ID is not the URL slug; SAM.gov uses an internal 32-char hex opportunity ID.

Working sequence:
1. Navigate to `https://sam.gov/search/` (fresh load).
2. Click the **Contracting** domain button in the result-list listbox (or it defaults to All Domains and the keyword box sometimes ignores Enter).
3. Type the Notice ID into the top searchbox (`New Search`, ref ~`@e16`) and click `New Search` (ref ~`@e17`). The keyword-text filter chip appears under the Simple Search panel.
4. Result count updates; the matching opportunity appears as an `h3` link in the results list. Click it.
5. The detail page's Description field is **usually readable** — it may be a single line (e.g. "Automated Asset Management Using Passive Radiofrequency Identification and Bluetooth Low Energy") or a full multi-paragraph SOW excerpt (e.g. the Civilian Guardian Course FA254926R0002 description runs ~4 paragraphs covering scope, 40-hour curriculum structure, LMS build-out, ISD support). Occasionally it collapses to amendment text only ("AMENDMENT ONE SITE VISIT") when the real SOW lives in the attachments (`.docx`/`.pdf`, sometimes gated). To extract whatever description text IS on the page, run via `browser_console`:

```js
const t = document.body.innerText;
const i = t.search(/Description/i);
JSON.stringify({desc: i>-1 ? t.slice(i, i+3500) : 'none'})
```

That returns the description section plus the surrounding fields (Notice ID, type, dates, agency, classification, contact, attachments list) — usually enough to read the topic, set-aside, NAICS, and contracting office.

**Additional fields worth capturing from the detail page** (the snapshot includes them as `heading "..." [level=5]` next to label StaticText):
- Contract Opportunity Type (Solicitation / Combined Synopsis/Solicitation / Sources Sought)
- Original Set Aside (e.g. "Total Small Business Set-Aside (FAR 19.5)", "No Set aside used")
- Product Service Code (e.g. `U008 - EDUCATION/TRAINING- TRAINING/CURRICULUM DEVELOPMENT`)
- NAICS Code (e.g. `611430 - Professional and Management Development Training`)
- Department/Ind. Agency, Sub-tier, Major Command, Office (e.g. "FA2549 STARCOM CONTRACTING PK" confirms the office prefix mapping)
- Attachments list — the PWS filename often telegraphs the scope (e.g. "A1-PWS _USMC_Advanced_Medical_Training_FY26 R4.pdf" confirms FY26 recurring training)

## Sources Sought / W-prefix visibility trap

Notice IDs with **W at position 7** (e.g. `N0018926RW025`, `IHS1523043`) are Special Notices / Sources Sought / RFIs. After their response date passes, they often disappear from active SAM.gov search results — the search returns "No matches found" even with Inactive checked. Don't conclude the Notice ID is wrong; it's a visibility-window artifact. For these:
- Rely on the title/topic the user provided plus USAspending incumbent-pattern evidence.
- The PWS scope is inferable from the prior-award chain (same office prefix, same topic keyword).
- If the user has the PWS as an attachment, parse it directly — don't waste tool calls trying to re-open the SAM.gov page.

## Batch efficiency (avoid tool-call cap)

When handed N Notice IDs, do ALL the USAspending `spending_by_award` curls in a SINGLE assistant turn (parallel terminal calls), then iterate the SAM.gov browser opens. Opening SAM.gov pages sequentially — navigate → type → click → snapshot → click → console — costs ~6 tool calls per notice and is the main reason a long batch hits the max-iterations cap. Better: pull all incumbent hypotheses from USAspending first, then open SAM.gov only for the notices whose topic is ambiguous from the title alone.

**Further optimization (learned from the 7-notice medical/training batch):** Write a single Python script (`/tmp/research_awards.py`) that loops through ALL candidate keywords in one `python3` invocation — one terminal call, ~50 keyword queries, full results dump. This is dramatically more efficient than one curl per keyword and avoids the tool-call cap entirely. The script can also iterate recipient-name searches and award-ID verification searches in the same run. Reserve browser SAM.gov opens for the 2-3 notices where the description or set-aside status is genuinely needed.

## Expected output format

When the user asks for a batch NEW-vs-RECOMPETE classification, the expected deliverable is a **pipe-delimited or table row per notice** with these columns:

```
Notice ID | Title | New Work or Recompete? | Prior incumbent (if any) | Prior award value (if any) | 1-2 line description of work
```

Deliver as a markdown table or a per-notice section with the same fields. Include:
- **Verdict** with confidence: "RECOMPETE (strong evidence)", "LIKELY RECOMPETE", "NEW WORK", "LIKELY NEW WORK".
- **Prior incumbent**: recipient legal name + the specific prior Award ID(s) that match the office prefix.
- **Prior award value**: the most recent same-office award's total obligation, with its POP dates so the user can see whether it's expiring.
- **1-2 line description of work**: pulled from the SAM.gov description field + PWS attachment filename + the prior award's Description field on USAspending. Keep it tight — the user wants to scan a table, not read paragraphs.

## Worked examples (2026-07-18 first batch — 8 notices)

| Notice ID | Topic query | Incumbent identified via prefix match | Verdict |
|---|---|---|---|
| 36C26226Q1049 | `["CCTV","security camera"]` + VA | Cynergy Professional Systems LLC — prior award `36C26222F0594` matches office prefix `36C262` | Recompete |
| 36C10B26Q0641 | `["queuing kiosk"]` + `["kiosk"]` + `["queuing"]` + VA (3 complementary queries) | Vecna Technologies — dominant VPS kiosk incumbent ($100M+ since 2011); same 36C10B office managed Vecna sustainment `36C10B19F0509` $24.4M 2019-2022. Active sustainment: `36C24723F0018` $2.7M (2022-2026), `36C24122P1428` $4.3M via Minuteman (2023-2026). QMATIC ecosystem: Alvarez LLC 6+ contracts $144K-$569K, NAMTEK $823K, Minburn $442K. Plus Thundercat kiosk accessibility $6.9M, Salient CRGT gravesite kiosks $11.3M (different scope). | **RECOMPETE / CONTINUATION** — Vecna VetLink is the installed VPS kiosk base; this RFI likely replaces or expands the aging platform. Blank set-aside field but description cites VAAR 852.219-73 SDVOSB (market research phase). NAICS 541519, PSC 5820 (hardware kiosks). Date discrepancy: description body says Jul 20, metadata says Jul 21. Use 3 complementary single-token queries ("kiosk", "queuing", "patient kiosk") for full landscape — each surfaces different vendor ecosystems. |
| 36C10B26Q0650 | `["SIEM"]` + VA + title "New Task Order" | Merlin International (`VA798A11F1066`) + Peraton ArcSight | Recompete under new TO |
| 36C10B26Q0658 | `["Corepoint"]` + VA | Interoperability Bidco (`36C26325C0018`) + Corepoint Health FY20-24 (`36C2632xNxxxx`) | Recompete (long-running recurring) |
| 36C24226Q0802 | `["wheelchair washing"]` | We Care Products, Medco Equipment | Likely recompete (small recurring) |
| FA303026Q0029 | `["SIPR thin client"]` + USAF | Transource Services Corp (`FA303026F0015`, "17 TRSS zero client") matches office `FA3030` | Recompete / continuation |
| 7571TE26Q00124 | `["HD492"]` | EEG Enterprises Inc — long chain `75N98025P00777`, `75N98023P02824`, `75N98021K00020`, `HHSN263201600566A` | Recompete (annual renewal) |
| SSN-IHS1529571 | `["materials management software"]` + IHS | Morris Systems Incorporated — dozens FY09-FY26 (`75H71025P00155`, `75H70625P00127`, etc.) | Recompete (Sources Sought for competition to long-time sole source) |

## Worked examples (2026-07-18 second batch — 7 medical/training/curriculum notices)

| Notice ID | Title | Verdict | Incumbent | Prior award value | Work covered |
|---|---|---|---|---|---|
| 36C10B26R0017 | 6515--Automated Asset Management using RFID and BLE (VA-26-00044895) | **RECOMPETE** (strong evidence) | Veteran Information Technologies, LLC (VIT) | `36C10B23F0345` $6.06M 2023-09 to 2026-09 (expiring); `36C10B25F0154` $1.41M 2025-07 to 2027-07 | Passive RFID + BLE automated asset tracking/management systems across VA medical facilities; NAICS 541519, PSC 6515, VA TAC NJ office 36C10B |
| FA254926R0002 | CIVILIAN GUARDIAN COURSE (CGC) CURRICULUM DEVELOPMENT AND ITERATION | **NEW WORK** (different scope from prior FA2549 office awards) | None for this scope (Linquest & Gemini Tech hold FA2549 awards but for STARCOM T&E / collaboration license, not curriculum dev) | FA254925F0001 $2.97M (Gemini, 3IS-III T&E); FA254926F0001 $2.09M (Linquest, STARCOM IDIQ) — neither matches | 40-hour high-engagement multi-modal curriculum for USSF Civilian Guardians (space awareness/superiority); classes, lessons, instructor guides, LMS config, capstone event; <4-month delivery; notice explicitly states "no government furnished information on the space element"; NAICS 611430, PSC U008; Full & Open; STARCOM Contracting PK, Patrick SFB |
| N0018926RW025 | NAVSUP WSS OJT Training Services | **LIKELY RECOMPETE** (W-prefix Sources Sought, SAM.gov page not retrievable) | Purdy Group LLC (prior NAVSUP WSS ERP training at same N00189 office) | `N0018918PQ058` $3.38M 2018-19 "NAVSUP WSS ERP TRAINING"; `N0018916CQ006` $3.98M 2016-18 "FY17 ERP TRAINING"; `N0018916CQ007` $3.98M 2016-18 "WSS N7 LOCAL ACQUISITION ED" | On-the-job training (OJT) services for NAVSUP Weapon Systems Support personnel — likely ERP/system training curriculum building on prior Purdy Group scope; W-prefix = Special Notice/Sources Sought |
| M0068126Q0063 | Tactical Combat Casualty Care | **RECOMPETE** (definitive) | Templar Medical LLC (USMC Camp Pendleton M00681 office) | `M0068124P0008` $1.011M 2024-01-05 to 2026-09-30 "TACTICAL COMBAT CASUALTY CARE (TCCC) TRAINING" — expiring 9/30/2026, directly replaced; plus `M0068124P0024` $84.5K, `M0068125P0012` $83.4K, `M0068125P0003` $29.9K (all Advanced Medical Training) | One-day period of instruction in TCCC for USMC/MCIWEST Camp Pendleton; Small Business Set-Aside; PSC U099, NAICS 611430; PWS attachment "A1-PWS _USMC_Advanced_Medical_Training_FY26 R4.pdf" confirms FY26 recurring training |
| IHS1523043 | IHS Dental Support Center CE | **LIKELY NEW WORK** (no prior awards under IHS1523 office prefix) | None under IHS1523 (prior IHS dental CE was under different offices — HHSI2352 California Area to CRIHB, HHSI2852 to USET) | HHSI2352-prefix CRIHB awards $19K-$39K each 2012-2018 "DENTAL ADVISORY COMMITTEE SEMI-ANNUAL MEETING AND DENTAL CONTINUING EDUCATION UNITS"; USET `HHSI28525006` $173K 2011 | Continuing education (CE) for dental professionals serving IHS-funded tribal/urban Indian health programs; likely dental support center convening CE workshops; W-prefix-equivalent (short visibility), SAM.gov page not retrievable |
| 36C24426Q0800 | VA MedBridge Rehabilitation Education | **RECOMPETE** (clear annual recurring chain) | MedBridge Education, LLC (VA NCO 4 / VISN 4, 36C244 office) | Annual VISN04 subscription chain: `36C24421N0971` $48.96K (21-22) → `36C24423N0064` $55.4K → `36C24424N0038` $62.5K → `36C24425N0037` $64.6K → `36C24426N0002` $64.5K 2025-10 to 2026-09 (current, expiring this fall) | Enterprise subscription licenses to MedBridge online rehabilitation education platform for VA NCO 4 (VISN 4) clinical staff; recurring annual SaaS; Sources Sought indicates VA gathering market intelligence ahead of next subscription cycle |
| 36C26226Q1147 | VA LEGO Play Therapy Workshop | **NEW WORK** (no prior awards anywhere for LEGO/play therapy/therapeutic LEGO) | None | None (only related 36C262 office award is `36C26224C0062` $109.7K to The Underdogs Unlimited for "RECREATIONAL THERAPY POOL CLEANING & MAINTENANCE" — completely different scope) | Workshop/training on LEGO-based play therapy methodology for VA NCO 22 (VISN 22) recreation/rehabilitation therapists; one-time skills-based workshop procurement; Sources Sought gauging market interest in novel therapeutic modality |

## Pitfalls

- **Empty results ≠ no incumbent.** The Notice-ID keyword search will always be empty; that's the trap. Switch to topic + agency.
- **Empty results on a MULTI-WORD topic phrase ≠ no awards.** USAspending keywords do not do phrase matching. "Civilian Guardian Course" returns 0 even though related awards exist. Fall back to single-token keywords ("Guardian", "MedBridge", "RFID") or known recipient names ("Templar Medical"). See the Keyword strategy section above.
- **Wrong agency label.** "Department of Health and Human Services" works for NIH at the subtier in some queries but NIH-specific awards often surface under "Indian Health Service" or the recipient-award prefix (`75N98`, `75H710`). If a subtier filter returns nothing, drop the agency filter and rely on keyword + award-prefix matching alone.
- **Multiple offices share a topic.** CCTV awards span NCO 22, NCO 24, NCO 25, NCO 26. RFID awards span NCO 5 (36C10B VIT), VISN 20 (36C260 Integration Technologies Group), Northern Arizona (36C10B VIT). Always match the Notice ID's office prefix (chars before the fiscal-year segment) against the prior Award ID's prefix — not just the topic.
- **Some VA offices use multiple award prefixes.** NCO 4 / VISN 4 uses both `36C244` (VISN04 subscription chain) AND `36C241` (other MedBridge awards). When tracing an incumbent, search the recipient name to surface awards under ALL prefixes the office uses — don't stop at the first prefix match.
- **"New Task Order" is still a recompete at the capability level.** The vehicle may be new, but the *work* is incumbent-held. Report it as Recompete/continuation unless the RFI explicitly introduces a net-new capability with no prior awards at the agency.
- **Sources Sought ≠ New Work by default.** A Sources Sought is often an IHS-style "market research to challenge a long-time sole source" — read the incumbent pattern, not just the notice type. Conversely, a Sources Sought with NO prior-award pattern under the office prefix (e.g. 36C26226Q1147 LEGO Play Therapy, IHS1523043 Dental CE) is genuinely new work.
- **W-prefix Notices may not be retrievable on SAM.gov after the response date.** `N0018926RW025` and `IHS1523043` both returned "No matches found" even with Inactive checked. Don't burn tool calls retrying; infer scope from the user-provided title + the prior-award chain.
- **Description field is NOT always truncated to amendment text.** The 7-notice batch showed full single-line descriptions ("Automated Asset Management Using Passive Radiofrequency Identification and Bluetooth Low Energy") and full multi-paragraph SOW excerpts (Civilian Guardian Course). The truncation-to-amendment case is one possibility, not the default — read whatever is there before falling back to attachments.
- **USAspending `business_categories` matches recipient SAM registration status, NOT award size.** Base IDV ceilings of $100M-$1B+ awarded to small-business-registered holders pass the filter. Always pair with an `award_amounts` band when hunting genuinely small actions. Sub-$250K-band queries also double as competitive intel: they name the incumbent small-biz winners. See `references/usaspending-opportunity-patterns.md`.
- **Searching USAspending by a SAM.gov Notice ID returns empty.** A Notice ID identifies a solicitation (pre-award), and USAspending only holds awards. To determine whether a Notice is new work or a recompete, search by topic keyword + awarding agency/subtier + NAICS, then match the contracting-office prefix on the Notice ID (chars before the fiscal-year segment) against prior Award ID prefixes. The most recent same-prefix same-topic recipient is the incumbent.
- **SAM.gov `/opp/<notice-id>/view` URLs 404.** The Notice ID is not the URL slug; SAM.gov uses an internal 32-char hex opportunity ID. To open a notice: navigate to `sam.gov/search/`, click the Contracting domain button, type the Notice ID into the New Search box, click New Search, then click the h3 link in the results.
- **USAspending `Start Date` is period-of-performance start and can be in the FUTURE on modifications** — a descending sort surfaces far-future dates (2027+) first. Not a data error; don't filter on it as "award recency".
- **Deadlines change.** Always verify deadlines on SAM.gov before acting. Article reports may be delayed or outdated.
- **Set-aside status may be ambiguous.** Some solicitations do not explicitly state set-aside. Mark as "Not specified" rather than guessing.
- **SAM.gov description-body deadline may differ from metadata Response Date.** The body text of a Sources Sought/RFI often states a specific deadline (e.g. "Monday, July 20, 2026") while the SAM.gov metadata `Response Date` field shows a different date (e.g. "Jul 21, 2026"). The description body is usually the authoritative deadline — it was written by the Contract Specialist. Always cross-check both and note the discrepancy. When the two dates are one calendar day apart and one is a Sunday/Monday, the description body date is likely correct. Flag this to the user so they do not miss the submission window.
- **Sources Sought: blank Original Set Aside + SDVOSB signal in description.** A Sources Sought with a blank set-aside field BUT a description that cites VAAR 852.219-73 (SDVOSB total set-aside) or FAR 52.219-27 (SDVOSB) is the standard market-research pattern: the agency has not yet formally determined the set-aside but is signaling their intent and testing the market. Treat as "Likely SDVOSB set-aside" and respond accordingly — the blank field is procedural, not a policy gap.
- **USAspending `fields`: `awarding_agency_name` is always null in search results.** Requesting `awarding_agency_name` in the `fields` array of `search/spending_by_award` returns `null` for every result row even when the agency filter is applied correctly. This is a known API quirk — the field is exposed but never populated at the search level. To get the awarding agency name, fetch each award's detail via `/api/v2/awards/{generated_internal_id}/` and read `awarding_agency.subtier.subtier_name` and `awarding_agency.office_agency_name`. The search endpoint alone cannot tell you which office within an agency issued the award — you must infer office prefix from the Award ID or fetch details.
- **Complementary keyword queries for competitive landscape mapping.** A single keyword query ("kiosk") surfaces one vendor ecosystem (Vecna); a related keyword ("queuing") surfaces a completely different ecosystem (QMATIC, Alvarez, ACF, ScriptPro). When the opportunity spans a broad market (hardware kiosks + patient queuing software), run 2-3 complementary single-token queries and merge the result sets. Each keyword surfaces different incumbents, different NAICS codes, and different contracting offices. The "no incumbent" verdict from one query may be completely wrong from a complementary query. This is especially important for Sources Sought research where the RFI scope is intentionally broad.
- **USAspending `Description of Requirement` field in search results is always null.** The field name appears in the API docs and you can request it, but it returns null for every row. Use the `/awards/{generated_internal_id}/` detail endpoint to get the populated `description` field (1-10 lines of scope text). This is documented in the skill's SKILL.md Critical section; the pitfall here is that new researchers predictably fall into this trap.