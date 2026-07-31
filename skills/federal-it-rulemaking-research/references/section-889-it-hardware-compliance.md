# Section 889 IT Hardware Compliance — Laptops, Components, and Procurement

## Scope

This reference covers the full Section 889 compliance framework for federal contractors procuring IT hardware (laptops, desktops, servers, networking gear) and their components. It complements `section-889-scope-analysis.md`, which covers the narrower "does this non-telecom device need to comply" question.

## Two Distinct Prohibitions

| Prohibition | Effective | What It Covers |
|---|---|---|
| **889(a)(1)(A)** | Aug 13, 2019 | Government can't *buy* covered equipment |
| **889(a)(1)(B)** | Aug 13, 2020 | Government can't *contract with entities that use* covered equipment — **including the contractor's own internal systems, regardless of whether that use is in performance of the federal contract** |

The "use" prohibition (Part B) is the one that catches contractors off guard. An employee laptop with a Huawei LTE modem, a building security camera system from Hikvision, an office PBX from ZTE — all can disqualify the entire entity from federal contracting.

## Key Definitions (FAR 4.2101 / 52.204-25)

### Covered Telecommunications Equipment or Services — Four Categories
1. Telecom equipment from **Huawei** or **ZTE** (and subsidiaries/affiliates)
2. Video surveillance/telecom from **Hytera**, **Hikvision**, or **Dahua** (public safety/security purposes)
3. Services provided by or using the above
4. Equipment/services from entities the **Secretary of Defense** designates as PRC government-connected

### "Substantial or essential component"
> Any component necessary for the proper function or performance of a piece of equipment, system, or service.

This is a functional test — if the equipment can't perform its intended function without the component, it's in scope.

### "Reasonable inquiry"
> An inquiry designed to uncover any information in the entity's possession about the identity of the producer or provider of covered telecommunications equipment or services used by the entity that **excludes the need to include an internal or third-party audit.**

This is the compliance standard — contractors don't need full supply chain audits, but must conduct inquiries designed to uncover covered equipment.

## FAR Clauses (all required in ALL solicitations, per FAR 4.2105)

| Clause | Type | Purpose |
|--------|------|---------|
| **52.204-26** | Provision | Initial representation: "does/does not provide" and "does/does not use" |
| **52.204-24** | Provision | Detailed representation with mandatory disclosures if answering affirmatively |
| **52.204-25** | Clause | Contractual prohibition + 1-business-day reporting requirement + mandatory flow-down to all subcontracts |

### DFARS (DoD-Specific) Versions
- **252.204-7016**: Covered Defense Telecommunications Equipment or Services — Representation
- **252.204-7017**: Prohibition on Acquisition — Representation
- **252.204-7018**: Prohibition on the Acquisition — Clause

## Laptop / IT Hardware Supply Chain Risk Matrix

| Scenario | Analysis |
|----------|----------|
| Huawei-branded laptop | Clearly prohibited (category 1) |
| Dell/HP laptop with Huawei LTE modem | If modem is necessary for function → **prohibited** (substantial/essential component) |
| Intel CPU fabricated in China | Intel is NOT a covered entity. Manufacturing location ≠ trigger. **Not prohibited.** |
| Laptop with HiSilicon chipset | HiSilicon is a Huawei subsidiary → **prohibited** if substantial/essential component |
| Loongson / Phytium processor | Chinese-designed, NOT explicitly listed in categories (1)-(3). Not designated under (4) as of 2026. **Not currently prohibited** but high risk of future designation. |
| TPM chip from Chinese entity | If from non-covered entity → not prohibited. Monitor for category (4) designations. |
| Generic capacitor/resistor from Chinese fab | Commodity part; unlikely to be "substantial or essential" individually. **Not prohibited.** |
| Dell/HP laptop assembled in China | Assembly location is not a trigger. **Not prohibited** (assuming no covered-entity components). |

## Lenovo: Unique Scrutiny

- **Lenovo is NOT a listed covered entity.** It does not appear in categories (1)-(3) of the definition and has not been designated under category (4).
- Lenovo laptops continue to be sold through GSA Schedule and other federal contract vehicles.
- **Why scrutiny exists:** Chinese parentage (Legend Holdings / Chinese Academy of Sciences ties), past security incidents (2015 Superfish), supply chain transparency concerns.
- **Perception risk:** Some agencies/prime contractors have internal policies against Lenovo regardless of Section 889 status. For sensitive DoD/IC work, Lenovo may face de facto exclusion even if technically compliant.
- **Practical note:** If procuring Lenovo for federal contract performance, document the reasonable inquiry and keep the Lenovo Section 889 compliance letter from their government sales team.

## Representations and SAM.gov

**Flow:**
1. Contractor registers in SAM.gov
2. Annual reps & certs include Section 889 representations (FAR 52.204-8(d), 52.212-3(v))
3. For each solicitation: 52.204-26 (initial) → 52.204-24 (detailed if affirmative)
4. Contracting Officer may rely on "does not" representations unless reason to question (FAR 4.2103(a))
5. False representations → False Claims Act exposure (treble damages + civil penalties)

**SAM.gov exclusion list:** Must be reviewed before making representations. Entities excluded for "covered telecommunications equipment or services" are recorded in SAM (FAR 4.2102(d)).

## Enforcement

- **False Claims Act:** Treble damages + $13,508-$27,018 per false claim (inflation-adjusted)
- **Suspension and Debarment:** Under FAR Subpart 9.4
- **Breach of Contract:** Termination for default
- **Criminal:** 18 U.S.C. § 1001 (false statements) — DOJ has brought criminal resolutions under Section 889
- **Reporting requirement:** If covered equipment discovered during performance → 1 business day to report (52.204-25(d))

## Compliance Roadmap for IT Hardware

1. **Inventory** all IT hardware (laptops, servers, networking, phones, cameras, BMS)
2. **Identify** any Huawei/ZTE/Hytera/Hikvision/Dahua equipment or components
3. **Remediate** — remove and replace covered equipment
4. **Procurement controls** — require Section 889 compliance representations from all IT vendors; include in POs
5. **SAM.gov updates** — ensure consistency between annual reps and solicitation-specific reps
6. **Ongoing monitoring** — watch for new category (4) designations and SAM.gov exclusion updates
7. **Documentation** — maintain records of reasonable inquiries, vendor certifications, compliance decisions

## Key Sources

- FAR Subpart 4.21 (FAC 2026-01, effective 03/13/2026): `https://www.acquisition.gov/far/subpart-4.21`
- FAR 52.204-24: `https://www.acquisition.gov/far/52.204-24`
- FAR 52.204-25: `https://www.acquisition.gov/far/52.204-25`
- FAR 52.204-26: `https://www.acquisition.gov/far/52.204-26`
- FAR 4.2104 (waivers): `https://www.acquisition.gov/far/4.2104`
- DFARS 252.204-7016/7017/7018 (DoD-specific): `https://www.acquisition.gov/dfars/252.204-7016` (trailing period required for clause-level DFARS URLs)
- Federal Register Interim Rule: 85 FR 42653 (July 14, 2020)
- SAM.gov exclusion records for covered telecommunications equipment or services
