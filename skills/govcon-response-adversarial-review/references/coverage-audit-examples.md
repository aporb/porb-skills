# PWS-vs-Response Line-Count Methodology

## Quick Coverage Audit

For a detailed PWS with table-structured requirements (like the VA SIEM PD with 82 line items across 5 tables), the fastest way to get an honest coverage score:

1. **Read the PWS first — cold.** Before reading any response. This prevents the response's framing from coloring your understanding of what the PWS actually asks for.

2. **Count ALL specific requirements.** Every table row is a requirement. Every "shall" statement is a requirement. Every deliverable with a frequency is a requirement. Count them.

3. **For each requirement, mark one of three states:**
   - ADDRESSED: The response specifically names and addresses this requirement
   - PARTIALLY: The response touches the general area but doesn't address the specific requirement
   - NOT MENTIONED: The requirement has zero coverage

4. **Calculate raw coverage:** (ADDRESSED + PARTIALLY/2) / TOTAL × 100

5. **This ratio IS the PWS Alignment score** (multiply by 10).

## The Inverted Emphasis Test

The single most common structural failure in GovCon responses:

1. Estimate the % of response content devoted to each topic
2. Estimate the % of PWS requirements devoted to each topic
3. If a topic gets 80% of response content but 2% of PWS requirements → RESPONSE IS INVERTED

This pattern is so common it deserves its own test. The response's content proportions should ROUGHLY match the PWS's requirement proportions.

## Real Session Example

**VA SIEM PD (36C10B26Q0650):** 82 specific requirements across 5 tables + Sections 2-7
**Response coverage:** ~5 of 82 requirements addressed = ~6% coverage
**Score:** 3/10 PWS Alignment

**HHS VMO PWS (7571TE26Q00092):** 8 specialist roles, 13 deliverables, 5 task areas, security section
**Response coverage:** ~30% of requirements addressed
**Inverted emphasis:** AI is 1 sentence in PWS, 80% of response content
**Score:** 4/10 PWS Alignment

**Treasury FMBSS PWS (2032H326N00011):** 6 task areas, 7 named systems, 30+ regulations
**Response coverage:** Maps to all 6 conceptually, zero demonstrated capability
**Score:** 3/10 PWS Alignment

## Fact-Check Results Log (Example Session)

| Claim | Claimed | Actual | Source | Severity |
|---|---|---|---|---|
| GitHub repos | 103 | 30 | github.com/aporb API | P0 |
| Published book | "Shrink-Wrap It" | VERIFIED | Amazon B0GQT9T1NF | — |
| Phone number | (803) 555-0142 | FAKE | 555 = fictional exchange | P0 |
| IL6 experience | claimed | UNVERIFIED | No project/dates/system | P1 |
| Revenue | $140K | ATTRIBUTED TO SUB, NOT PRIME | Entity factsheet | P1 |
| Portfolio companies | 16+ managed | UNVERIFIED | No names/deliverables | P1 |
| Efficiency ratio | 15-20 person equiv | UNSUBSTANTIATED | No methodology/benchmark | P1 |

## Persistent Errors Across Sessions

When the same error survives multiple review cycles, it indicates a process problem:

- **Fake phone "(803) 555-0142":** Flagged P0 in v1 gap analysis. Unfixed in v2. Persisted into this adversarial review. Flag it again with increased severity and a note: "Third review cycle — this was flagged 2 days ago and remains unfixed."
- **"103 repos":** Appeared in all three responses across two agencies. The number was never verified before being written into all drafts.
- **"15-20 person" ratio:** Same unsubstantiated claim across all three responses. Copied without verification.

## Counter-Example: What GOOD Coverage Looks Like (HHS VMO v4)

After the v3 adversarial review scored 42/100 (FAIL), the response was rebuilt from scratch with a management-consulting-first approach:

**HHS VMO v4 (7571TE26Q00092) — rebuilt response:**
- **8/8 PWS specialist roles** explicitly addressed — each either Covered, Gap, or Subcontract with named mitigation
- **13/13 deliverables** listed in a table with frequencies
- **AI/automation reduced** from 80% of content to ~15% — described as augmentation of specific roles, not replacement
- **All false claims removed:** no "103 repos," no "$140K," no "16+ portfolio companies," no "Fractional CAIO," no IL6 overclaims, no FAR 15.305 misapplication
- **FAR Part 10 market research framing** replaced FAR 15.305 proposal evaluation framing
- **Led with management consulting understanding** citing FITARA D score, MEGABYTE Act, Dell BPA, 11 OpDivs by name, incumbent RiverNorth
- **Honest gap assessment:** Acquisition Specialist and License Specialist both acknowledged as gaps with specific subcontract/hire mitigation plans
- **Estimated score after rebuild:** 65-75 (PASS threshold)

**Key pattern:** The v3 adversarial review wasn't just a quality gate — it identified a structural failure (inverted emphasis + PWS blindness). The rebuild didn't just fix individual errors; it restructured the response around what the PWS actually prioritizes. Use adversarial reviews to identify structural problems, not just factual errors.