---
name: counterfactual-reviewer
description: Counterfactual-debating reviewer for fleet responses. Use when a gov-api-mcp-fleet tool produced a numeric, categorical, or list output and you want to stress-test it. The reviewer poses 3-5 adversarial counterfactuals ("what if the NAICS was wrong?", "what if the date window was inverted?") and produces a confidence score + recommended follow-ups. Trigger automatically when the user is about to make a decision based on a single fleet query.
type: quality
---

# Counterfactual Reviewer

When the gov-api fleet returns a numeric, categorical, or list answer, this skill stress-tests it before you act on it.

## When to invoke

- The user just got a fleet response and asks "is that right?", "are you sure?", "let me double-check"
- The fleet output drives a high-stakes decision (proposal go/no-go, recompete timing, vendor selection, allocation > $1M)
- A response feels suspicious (round-numbered, suspiciously low/high, only one row when many expected)
- The user explicitly asks for a "counterfactual review" or "adversarial check"

## How it works

For any answer A produced by an MCP tool call T(args), generate 3-5 counterfactuals by perturbing args:

### The perturbation menu

| Dimension | Perturbation | Why |
|---|---|---|
| **NAICS code** | swap to adjacent (541512 → 541330, 541330 → 541512) | NAICS confusion is a common silent error |
| **Time window** | flip start/end; double the window | Date inversions return empty or wrong-period data |
| **Geography code** | use state USPS instead of FIPS; uppercase/lowercase | FIPS vs USPS is a common mismatch |
| **Set-aside filter** | include `set_aside=null` vs `set_aside=SBA` | Set-aside filtering can hide majority of records |
| **Date format** | pass YYYYMMDD where YYYY-MM-DD expected (openFDA quirk) | Date format zoo is server-specific |
| **NAICS column name** | NAICS2017 vs NAICS2022 (Census CBP) | The 2022 CBP uses NAICS2017 — easy miss |
| **Pagination** | request page 2 instead of page 1 | Page-1 hits aren't always representative |
| **Tier filter** | omit any filters → check if the unfiltered universe matches | "I only got 5 results" — was there a filter? |

### The 5-question rubric

For each perturbation, ask:

1. **Does the answer change?** If yes → which is right?
2. **Is the change directional or random?** (E.g., NAICS swap should produce a related but distinct result; flipped dates should return empty)
3. **Does the original answer hold up when the perturbed query is run?** (Run it, compare)
4. **Is there a reason the original method was the *right* one to use?** (Justification step)
5. **What's the confidence in the original answer on a 0-1 scale?**

## Output format

When invoked, the reviewer produces:

```
COUNTERFACTUAL REVIEW — [tool: T, args: args, result: R]
─────────────────────────────────────────────────────────

Perturbation 1: <description>
  Run: T(perturbed_args)
  Got: <perturbed result>
  Verdict: ✓ consistent / ⚠ diverged / ✗ contradiction

Perturbation 2: <description>
  …

…

Overall confidence: <0.0-1.0>
Recommended follow-up:
  - [ ] Run T2(other_args) to validate
  - [ ] Cite the source for <claim>
  - [ ] Reduce confidence to ≤<X>% if perturbation 2 cannot be resolved
```

## Worked example

**Original tool call:**
```
usaspending.find_competitor_awards(naics="541512", lookback_days=365)
→ Top: Booz Allen Hamilton ($X billion)
```

**Counterfactual review:**

| # | Perturbation | Result | Verdict |
|---|---|---|---|
| 1 | naics="541330" (swap) | Different top: Engineering Inc | ✓ consistent (different NAICS, different leaders) |
| 2 | lookback_days=30 | Booz Allen still on top | ✓ confirms steady leadership |
| 3 | lookback_days=365, agency=097 (DoD only) | Booz Allen still on top | ✓ DoD-specific check passes |
| 4 | lookback_days=2000 (10-year window) | Booz Allen still on top, $X×4 | ✓ trend stable |
| 5 | No NAICS filter | Top changes (broader market) | ✓ NAICS filter is the right scope |

**Confidence: 0.92**
**Follow-up:**
- Cite usaspending.gov directly in the response
- If proposal hinges on Booz Allen's #1 position, run perturbation 3 again with `set_aside=SBA` to verify exclusion of small-business set-asides

## When NOT to apply

- Discovery queries ("what's available?") — there's no claim to falsify
- Listing tools (lookup tables, dictionaries) — they're not estimates
- Cache hits younger than 5 minutes — perturbation will just hit cache, not the upstream API
- When the upstream is rate-limited (SBIR.gov, SAM personal-tier) — burns quota for marginal value

## Code form (Inspect AI scorer-compatible)

`evals/scorers/counterfactual.py` (see gov-api-mcp-fleet repo) implements this as an Inspect AI custom scorer that takes a baseline tool call and runs 3 perturbations, scoring on agreement.

## Trigger phrases

These phrases from the user should automatically invoke this skill:

- "are you sure"
- "double-check"
- "stress-test that"
- "counterfactual"
- "adversarial review"
- "what if the [naics/date/geo/agency] was wrong"
- "is that the right [tool/server/filter]"
- "before I decide"

## Related skills

- See `pr-review-toolkit:silent-failure-hunter` for catching silent fallbacks in code
- See `hookify:conversation-analyzer` for conversation-level review
