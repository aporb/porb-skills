# TAA & Buy American Scope Analysis — Non-IT Equipment

## The Canonical Question

> "Does a [office supply / non-IT device / widget] need to be TAA-compliant or Buy American-compliant? It's not connected to anything."

Two separate regulatory regimes with different scope definitions, threshold rules, and exceptions. Frequently conflated with Section 889 — they are independent.

---

## Part 1: Trade Agreements Act (TAA) — FAR Subpart 25.4

### FAR Source
- Clause: FAR 52.225-5 (Trade Agreements) — https://www.acquisition.gov/far/52.225-5
- Scope: FAR 25.400 — https://www.acquisition.gov/far/25.400
- Exceptions: FAR 25.401(a) — https://www.acquisition.gov/far/25.401
- Thresholds: FAR 25.402(b) — https://www.acquisition.gov/far/25.402

### How TAA Applies
TAA waives the Buy American statute for "eligible products" from designated countries (WTO GPA, FTA, least-developed, Caribbean Basin countries). When incorporated, FAR 52.225-5 requires delivery of only U.S.-made or designated-country end products.

### The Threshold Question
TAA clauses are mandated when expected acquisition value exceeds these thresholds:

| Agreement | Supply Threshold |
|---|---|
| WTO GPA | $174,000 |
| Most FTAs (Australia, CAFTA-DR, Chile, Colombia, Singapore) | $105,767 |
| Korea FTA | $100,000 |
| Israel Trade Act | $50,000 |

**Critical**: Threshold determines whether 52.225-5 is *required*. Once the clause IS in the contract, **all deliveries must comply** regardless of individual order value. A $200 shredder under a $5M IDIQ with 52.225-5 must be TAA-compliant.

### Exceptions (FAR 25.401(a))
1. **Small business set-asides** — most common practical exception
2. Arms/ammunition/war materials
3. Acquisitions for resale
4. FPI/NP (AbilityOne)
5. Non-competitive acquisitions
6. Services excluded by agreement schedules

### Substantial Transformation Test
TAA compliance hinges on where an item is "substantially transformed" (FAR 52.225-5(a), 25.003). Country of origin on the product label is generally the country of substantial transformation.

### Application
| Equipment Type | TAA Analysis |
|---|---|
| Any non-IoT office equipment (shredder, desk, filing cabinet) | **End product**. Must be U.S.-made or designated-country if 52.225-5 is in the contract. |
| IT equipment | Same as above, plus security requirements. |

---

## Part 2: Buy American Act — FAR Subpart 25.1

### How Buy American Works (vs TAA)
Two-part test for manufactured end products:
1. **Manufactured in the United States** — binary
2. **Domestic content test** — cost of domestic components exceeds applicable percentage (60% now, 65% 2024-2028, 75% 2029+)

### The COTS Waiver — Commonly Misunderstood
Per FAR 25.101(a)(2)(i), COTS items have the **domestic content percentage test waived**. This means a U.S.-made COTS item doesn't need component tracking.

**Common error**: "COTS items from Canada/Mexico/Germany are treated as domestic." **Wrong.** The COTS waiver only waives the content percentage — it does NOT waive the "manufactured in the United States" requirement. A Germany-made shredder is NOT a "domestic end product" under Buy American — it's an eligible product under TAA (if the contract carries 52.225-5).

### Buy American Exceptions (FAR 25.103)
- Unreasonable cost (foreign offer is significantly lower)
- Nonavailability
- Public interest
- COTS items (content test waived, NOT US manufacture test)
- Items predominantly iron/steel — stricter 5% foreign iron/steel threshold, NOT waived for COTS

---

## Part 3: Combined Matrix

| Scenario | Buy American | TAA | Result |
|---|---|---|---|
| Contract with 52.225-5, German shredder | Fails BA (not US-made) | Passes TAA (WTO GPA) | **Compliant** — TAA overrides BA |
| Contract with 52.225-5, Chinese shredder | Fails BA | Fails TAA | **NOT compliant** |
| Contract without 52.225-5 (small biz set-aside), COTS China shredder | Fails BA (not US-made) | TAA not in contract | **NOT compliant** under BA |
| Micro-purchase, China shredder | BA technically applies | | **Low enforcement risk**, but technically non-compliant |
| GSA Schedule, China shredder | 52.225-5 likely in Schedule | 52.225-5 applies to all orders | **NOT compliant** |

---

## Part 4: Security Standards vs Procurement Compliance

The most common conflation in enclave/SCIF analyses:

| Requirement | Authority | What It Governs |
|---|---|---|
| NSA/CSS EPL listing | 32 CFR § 2001.42(b) | Destruction standard (particle size, cross-cut) |
| NISPOM destruction | 32 CFR § 117.15(b)(2) | Classified material destruction methods |
| CUI destruction | 32 CFR § 2002.16(h) | Requires destruction — no specific particle size mandated |
| TAA | FAR Subpart 25.4 | Country of origin |
| Section 889 | FAR Subpart 4.21 | Telecom/video surveillance equipment |

**These are orthogonal.** A shredder must satisfy BOTH sets independently:
- Security: meets destruction standard for the material level
- Procurement: meets country-of-origin/889 requirements of the ordering vehicle

---

## References
- FAR 52.225-5: https://www.acquisition.gov/far/52.225-5
- FAR 25.402(b): https://www.acquisition.gov/far/25.402
- FAR 25.401(a): https://www.acquisition.gov/far/25.401
- FAR 52.225-1: https://www.acquisition.gov/far/52.225-1
- FAR 25.101(a)(2)(i): https://www.acquisition.gov/far/25.101
- FAR 25.103: https://www.acquisition.gov/far/25.103
- FAR 25.003: https://www.acquisition.gov/far/25.003
- 32 CFR § 2001.42(b): https://www.ecfr.gov/current/title-32/part-2001/section-2001.42
- 32 CFR § 2002.16(h): https://www.ecfr.gov/current/title-32/part-2002
