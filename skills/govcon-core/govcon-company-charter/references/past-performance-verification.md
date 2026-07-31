# Past Performance Verification — Federal Contract Claims

## When to Verify

The founder or client provides a list of past contract claims (year, dollar value, agency, role). Before including these in a capability document, cross-reference against public federal records. Unverified claims with hedging language ("Source: Amyn's accounting") damage credibility. For NDA partner documents, verification gives you confidence to state claims declaratively.

## Databases to Search

- **USASpending.gov** — keyword search by company name, UEI, contract number
- **FPDS (Federal Procurement Data System)** — via SAM.gov or USASpending
- **GAO Bid Protest Docket** — `gao.gov/products/b-XXXXXX` for protest decisions
- **OrangeSlices AI** — GovCon award tracking with company profiles
- **GovTribe** — federal vendor profiles, contract histories
- **GDICWins / GDI Consulting** — active RFP and award profiles
- **HigherGov** — contract pages with award details
- **Company press releases** — Significance Inc., Navaide, etc. often publish award announcements
- **LinkedIn** — founder posts about contract wins, roles, speaking engagements
- **Department of Defense contract announcements** — defense.gov or war.gov daily contract listings

## What to Extract for Each Claim

For every contract:
- Contract/award number (e.g., N0003925F3009, N6247025D0004)
- Referenced IDV (e.g., N0017819D8402 for SeaPort NxG)
- Agency and sub-agency
- Prime contractor name
- Award date and period of performance
- Total value (award + modifications)
- Number of bidders
- Set-aside status
- GAO protest number and decision date (if applicable)
- Founder's verified role (from press releases, LinkedIn, or named in award)

## Verification Verdicts

- **VERIFIED** — contract number, agency, value, and role confirmed in public records
- **PARTIALLY VERIFIED** — dollar pattern and agency match but dates or exact values differ
- **CANNOT VERIFY** — no public record found (subcontractor roles often invisible)
- **PLAUSIBLE** — activity level consistent with known contracts but specifics unverified

## Red River Resources / Navaide Identity

Navaide operates under Red River Resources LLC (UEI HZCDXJV7M8Z9). When searching federal databases, search BOTH names. The SeaPort NxG IDIQ is held under Red River Resources.

## Significance Inc. Context

Significance Inc. (Annapolis, MD) is a Women-Owned Small Business. Their press release page (significanceinc.com/headlines) is a good source for contract announcements. Key contracts include BSO-52 NERP (Navaide listed as teaming partner), BUMED Financial Services ($10.2M), and NAVFAC Real Property (N6247025D0004, $40M→$78M).

## How to Dispatch Verification

Use a delegate_task sub-agent with explicit instructions to search all the databases above. Provide the full list of claims, any known UEIs, and the founder's employment timeline. The sub-agent should return a structured table with verdicts and source URLs for every claim.
