# Competitive Landscape via Contracting Office Prefix

Contracting office analysis — identifying everyone who works with a specific contracting
office, not just the incumbent on a single solicitation. Generates a tiered competitive
landscape that reveals who could bid on a recompete beyond the obvious incumbent.

## When to Use

- A Sources Sought or solicitation has an identifiable contracting office prefix (e.g.,
  M67004, 36C262, FA3030, N62470)
- You need to know who else competes for work at that office, not just who holds the
  current contract
- You're evaluating whether an entity with no past performance on a specific contract
  could find a prime partner — the Tier 2 list IS your teaming partner shortlist
- You want to understand competitive intensity trends (number of offers over cycles)

## Phase 1: Identify the Contracting Office Prefix

The Contracting Office Code is typically the first segment of the Solicitation/Notice ID,
before the fiscal-year segment:

| Notice ID | Contracting Office | Office |
|-----------|-------------------|--------|
| M6700426R0008 | M67004 | MARCORLOGCOM, Albany GA |
| 36C10B26Q0650 | 36C10B | VA NCO 10 (VISN 10) |
| FA303026Q0001 | FA3030 | AF Life Cycle Management Center |
| N6247023F4081 | N62470 | NAVFAC Atlantic |

**Method:** Split on the last `XX` before the 2-digit fiscal year. The prefix is everything
before `-` or the digit pair that represents the fiscal year.

## Phase 2: Search USAspending for ALL Awards Under That Prefix

Use the USAspending `search/spending_by_award` endpoint with the prefix as an `award_ids`
filter. This returns every active/past award under that office, regardless of topic.

```bash
curl -s "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -X POST -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["A","B","C","D"],
      "award_ids": ["M67004"]
    },
    "fields": [
      "Award ID","Recipient Name","Description","Award Amount",
      "Start Date","End Date","Contract Award Type",
      "naics_description","Base Obligation Date"
    ],
    "sort": "Award Amount",
    "order": "desc",
    "limit": 100
  }'
```

**Parameters:**
- `award_type_codes: ["A","B","C","D"]` — contracts only
- `award_ids: ["M67004"]` — prefix match; the API matches on the leading characters of
  the Award ID field
- `sort: "Award Amount"` / `order: "desc"` — largest awards first (usually the strategic
  programs)
- `limit: 25-100` — adjust based on the office's activity level; large commands (HHS,
  DoN) may need pagination

**Interpretation:** The results show every contract the office has awarded, sorted by
dollar value. The top 10-15 results by value ARE the command's strategic portfolio —
even if they look unrelated to your specific solicitation.

## Phase 3: Build the Tiered Competitive Landscape

From the results, classify each contractor into one of three tiers:

### Tier 1: Incumbent & Near-Incumbent

The current and prior holders of the specific contract being recompeted.

**How to identify:** Filter the prefix results by topic keyword that matches the
solicitation description (e.g., "DMSS", "Distribution Management", "Logistics Support").
The most recent award with matching description is the incumbent. Prior awards with the
same description (different fiscal years) are prior incumbents.

**When the prefix alone returns dozens of unrelated awards:** Use a two-stage search:
1. First, search the entire DoD/agency by topic keyword + NAICS to find the incumbent
   (how `usaspending-new-work-vs-recompete.md` works)
2. Then, search by pure prefix to see what ELSE the office buys — the Tier 2 contractors
   may not have touched your specific topic

### Tier 2: Major Office Contractors (The Teaming Pool)

These are contractors who have large-dollar awards UNDER THE SAME CONTRACTING OFFICE
but on different topics. They know the customer, have relationships, and may pursue
anything the office puts out.

**Why they matter:**
- A Tier 2 contractor may bid on EVERY recompete under this office, even outside their
  core lane
- They are the most likely teaming partners for an entity with complementary capabilities
- They know the CO, the contracting patterns, the key personnel — relationships that take
  years to build

### Tier 3: Wildcards

Entities from adjacent contracting offices, SDVOSB firms that entered on set-asides, or
national primes who may enter on a large-dollar rotation. Harder to predict but worth
flagging when:
- The contract value is above $50M (attracts national primes)
- The NAICS shift opens a small business set-aside (SDVOSB entrants)
- A known disruptor has entered the agency

## Phase 4: Multi-Cycle Contract Lineage Reconstruction

For understanding competitive intensity, reconstruct the full award history of the
specific contract across multiple cycles. This is more nuanced than single-cycle
incumbent identification.

**Method:**

1. **Start with the most recent award** — search by topic keyword + agency + NAICS
2. **Fetch full award detail** via `/awards/{generated_internal_id}/` — read
   `description`, `period_of_performance_start_date`, `period_of_performance_current_end_date`,
   and `product_or_service_code` from `latest_transaction_contract_data`
3. **Trace the chain backward** — search for PRIOR awards with the same contracting
   office prefix + same PSC + award amounts in a similar range. The keywords in the
   description field often change between cycles, but the PSC and dollar range stay
   consistent.
4. **For each cycle, capture:** award ID, recipient, obligated amount, ceiling amount,
   contracting vehicle, set-aside status, number of offers received

**Example output (MARCORLOGCOM DMSS):**

| Cycle | Award ID | Holder | Obligated | Vehicle | Offers |
|-------|----------|--------|-----------|---------|--------|
| 2018 | M6700418F4044 | PAI | $5.36M | GSA Schedule | Unknown |
| 2020 | M6700420F4104 | Cervello Global | $10.93M | GSA FSS | 3 |
| 2023 | M6700423F3000 | PAI | $11.35M | SEAPORT-NxG | 7 |
| 2026 | M67004-26-R-0008 | TBD | ~$20M | TBD | TBD |

**Signals to watch in the chain:**
- **Number of offers increasing** — competition is intensifying (3→7 is a 2.3x jump)
- **Vehicle changes** — GSA Schedule → SEAPORT-NxG suggests the office is consolidating
  onto strategic buying vehicles
- **Company size status changes** — if incumbent graduated from small→large between
  cycles, a set-aside recompete becomes viable
- **Set-aside presence/absence** — alternating cycles of set-aside vs full-and-open
  signal the CO's small business rotation strategy

## Phase 5: NAICS Shift Analysis

When a Sources Sought changes the NAICS code from the prior award, this is a deliberate
signal worth analyzing — not a clerical change.

**Step 1: Identify the shift**
- Old NAICS: from the prior award's `latest_transaction_contract_data.naics` or
  the `naics_description` in the award search results
- New NAICS: from the Sources Sought / solicitation text

**Step 2: Compare size standards**

| NAICS | Description | Size Standard |
|-------|-------------|---------------|
| 541330 | Engineering Services | $25.5M |
| 541614 | Process, Physical Distribution, & Logistics Consulting | $20.0M |
| 541512 | Computer Systems Design | $34.0M |
| 541611 | Administrative Management Consulting | $25.5M |
| 518210 | Data Hosting / Cloud | $40.0M |
| 541715 | R&D in Physical/Engineering/Life Sciences | $1,030.0 |
| 541690 | Other Scientific/Technical Consulting | $25.5M |

**Step 3: Check the incumbent's SAM registration for the NEW NAICS**
- If the incumbent is registered as "other_than_small_business" (`large business`) under
  the NEW NAICS, they become ineligible for any small business set-aside under that NAICS
- This is the biggest competitive opening a new entrant can have
- Cross-reference with `recertify-size-status` language in the Sources Sought — if
  present, the CO is deliberately signaling that the incumbent may not qualify

**Step 4: Assess whether the shift changes the competitive pool**
- A smaller size standard ($20M instead of $25.5M) may disqualify mid-sized incumbents
- A larger size standard may invite national primes who were previously blocked
- The new NAICS may have different SBA revenue calculations — some NAICS exclude cost of
  goods sold, others don't

**Step 5: Integrate into the tiered landscape**
- If the new NAICS opens a small business set-aside, ADD all SDVOSB/8(a)/HUBZone firms
  with 541614 registration to your wildcard tier
- If the incumbent is disqualified by the shift, raise Tier 2 contractors' win
  probability significantly — they're now competing against peers, not the entrenched
  incumbent

## Phase 6: Synthesize the Competitive Landscape

Structure the final output as a tiered table with win-probability estimates for each
identified competitor.

### Template

```markdown
## Competitive Landscape: [Solicitation Title]

### Tier 1: Incumbent & Near-Incumbent

| Entity | Role | Last Win | Advantage | Vulnerability |
|--------|------|----------|-----------|---------------|
| Company A | Current incumbent | 2023 | Incumbent knowledge, relationships | May be large under new NAICS |
| Company B | Prior incumbent | 2020 | Past performance on exact scope | Lost last cycle, 3+ years cold |

### Tier 2: Major Office Contractors (Teaming Pool)

| Entity | Office Portfolio | Complementary Capability | Teaming Fit |
|--------|-----------------|-------------------------|-------------|
| Company C | $X in M67004 awards | Analytics, data | Medium — has in-house |
| Company D | $Y in M67004 awards | Logistics ops | High — lacks analytics |

### Tier 3: Wildcards

- SDVOSB firms under new NAICS 541614
- National primes (would enter at >$50M only)
```

### Competitive Intensity Verdict

| Cycle | Offers | Verdict |
|-------|--------|---------|
| 2020 | 3 | Moderately competitive |
| 2023 | 7 | Highly competitive (+133%) |
| 2026 (proj) | 7-12 | Highly competitive |

## Worked Example: MARCORLOGCOM M67004-26-R-0008 (DMSS)

Full worked example at the session-level assessment:
`~/repos/federal-bd-pipeline/marcorlogcom-m67004-26-r-0008/research/c-suite-assessment.md`

**Key findings:**
- M67004 prefix search returned 25 awards, top 10 valued $246M-$34M
- Competitive landscape revealed 4 Tier 2 contractors (Cherokee Nation, Primetech,
  Vertex Aerospace, CGI Federal) with $43M-$94M in MARCORLOGCOM work on unrelated topics
- 4-cycle chain: PAI (2018) → Cervello (2020) → PAI (2023) → recompete (2026)
- NAICS shift 541330→541614 with PAI now "other_than_small_business" under SAM
- Offers doubled from 3 to 7 between cycles

## Limitations

- **USAspending does not index pre-2007 awards.** For contracts older than 2007, the
  chain may be incomplete.
- **Vehicle name changes may hide continuity.** If the contracting office migrated from
  GSA FSS to SEAPORT-NxG to a new vehicle, the Award IDs change completely — you need
  the description keywords + PSC + dollar band to reconnect the chain.
- **Not all offices use a consistent prefix.** Some offices use different prefixes for
  different procurement vehicles (e.g., the same office may use one prefix for
  GSA-schedule orders and another for IDIQ task orders).
- **Prefix-only search may miss work awarded through shared service centers.** If the
  office delegated procurement to a strategic buying center (e.g., HHS OMAS SBC-IT using
  7571TE instead of the end-user office code), the prefix won't match. Always run a
  topic-keyword fallback.
- **Number of offers is only available on the award detail endpoint**
  (`/awards/{generated_internal_id}/`) — absent from `spending_by_award` search results.
  You must fetch each award's detail individually to get this competitive intensity
  signal.
