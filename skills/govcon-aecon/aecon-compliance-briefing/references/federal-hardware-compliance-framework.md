# Federal IT Hardware Compliance Framework — Multi-Regime Reference

## Overview

Federal IT hardware procurement (especially laptops) must simultaneously satisfy up to five distinct regulatory regimes. This reference provides the condensed compliance framework for each regime and the synthesis approach.

---

## 1. Trade Agreements Act (TAA) — FAR 52.225-5

| Element | Answer |
|---------|--------|
| **Legal test** | "Substantial transformation" — where final assembly occurs, not component origin. 19 U.S.C. §2501; FAR 25.001(c)(2) |
| **Designated countries for IT hardware** | WTO GPA (47: EU, Japan, South Korea, Taiwan, Singapore, Canada, Mexico, etc.), FTA (17), Least Developed (42), Caribbean Basin (22) |
| **NOT designated** | China, India, Vietnam, Malaysia, Thailand, Indonesia, Philippines, Brazil, Russia |
| **FAR trigger** | FAR 52.225-5 applies ≥$174K (WTO GPA threshold). Below that, Buy American (52.225-1/3) applies |
| **COTS waiver** | 52.225-1 domestic content test is waived for COTS items (FAR 12.505(a)(1)) |
| **Flow-down** | 52.225-5 is NOT on mandatory flow-down list (52.244-6) but primes should flow down anyway |
| **Key sourcing truth** | Major OEMs (Dell, HP, Lenovo) manufacture in both China and designated countries. Only specific SKUs are TAA-compliant. Verify per SKU, not per brand. |
| **Vendor evidence** | TAA Compliance Certificate per SKU from vendor federal sales team |
| **Key source URLs** | acquisition.gov/far/52.225-5, acquisition.gov/far/25.401 (exceptions) |

## 2. Section 889 (FY19 NDAA) — FAR 52.204-24/25/26

| Element | Answer |
|---------|--------|
| **Covered entities** | Huawei, ZTE, Hytera Communications, Hikvision, Dahua Technology + subsidiaries/affiliates |
| **Parts** | (A) Gov't procurement ban; (B) Prohibition on contracting with entities that USE covered equipment |
| **Laptop component risk** | LOW. No major enterprise laptop uses Huawei/ZTE silicon. Concern is parent-company relationships (Lenovo) or network infrastructure, not laptop internals. |
| **Required FAR clauses** | 52.204-24 (representation), 52.204-25 (prohibition), 52.204-26 (covered telecom), 52.204-30 (operations) |
| **Representation** | Required in SAM.gov. Annual recertification. Vendor must provide formal representation letter. |
| **Lenovo-specific** | Not banned by name under Section 889. But DoD/IC agencies routinely apply heightened SCRM to Chinese-parent vendors. Some agencies have informal Lenovo restriction policies. |
| **FCC Covered List** | fcc.gov/supplychain/covered-list — maintained list of covered entities |
| **Key source URLs** | acquisition.gov/far/52.204-24, acquisition.gov/far/subpart-4.21 |

## 3. CMMC Level 2 — NIST SP 800-171 Rev 3

| Element | Answer |
|---------|--------|
| **Rule** | 32 CFR 170; CMMC 2.0; 110 controls aligned with NIST SP 800-171 Rev 3 |
| **Key hardware control** | SC.L2-3.13.11 — FIPS-validated cryptography for CUI confidentiality |
| **Hardware baseline** | TPM 2.0 (FIPS 140-2 validated) + Secure Boot + BitLocker with TPM+PIN + Windows 11 Enterprise |
| **What matters** | The BIOS/OS config and management stack, NOT the brand sticker. Any Secured-core certified laptop satisfies CMMC L2 hardware layer. |
| **OS requirement** | Windows 11 minimum — TPM 2.0, 8th-gen Intel / Ryzen 2000+ CPU |
| **Assessment evidence** | Intune compliance policies + Conditional Access reports serve as evidence for multiple controls |
| **Key source URLs** | csrc.nist.gov (NIST SP 800-171 Rev 3), dodcio.defense.gov/CMMC/ |

## 4. DoD IL-4 (Cloud Computing SRG v1r4)

| Element | Answer |
|---------|--------|
| **Likely level for CUI work** | IL-4. IL-2 for non-CUI; IL-5 adds TEMPEST/dedicated facility requirements |
| **Hardware requirements** | CAC/PIV smart card reader, FIPS 140-2 TPM, full disk encryption, STIG-hardened Windows 11, EDR |
| **Additional for IL-5** | All IL-4 + hardware-based MFA (CAC), TEMPEST considerations, NIAP-certified VPN |
| **Key source URLs** | public.cyber.mil/dccs/ (DCCS/SRG) |

## 5. DISA Windows 11 STIG v2r8 (July 2026)

| Element | Answer |
|---------|--------|
| **Current version** | Microsoft Windows 11 STIG - Ver 2, Rel 8 (July 10, 2026) |
| **Settings count** | ~250 |
| **Deployment methods** | Intune STIG policy packs (July 2026 release), GPO, SCCM, SCAP |
| **Key requirements** | UEFI Secure Boot ON, TPM 2.0 for BitLocker, Credential Guard + HVCI, FIPS 140-2 mode, WDAC/AppLocker, disabled legacy protocols (SMBv1, TLS 1.0/1.1, LLMNR, NetBIOS) |
| **CMMC relationship** | STIG compliance is NOT directly required by CMMC but satisfies DFARS 252.204-7012. STIG-hardened endpoints inherently exceed NIST 800-171. |
| **Key source URLs** | public.cyber.mil/stigs/downloads/ |

## 6. Federal Sustainability — EO 14057 / FAR 23.1

| Element | Answer |
|---------|--------|
| **EO 14057 mandate** | Net-zero federal procurement by 2050; 65% reduction by 2030 |
| **FAR requirement** | FAR 23.1 — sustainable products "to maximum extent practicable" |
| **EPEAT** | 95% of federal laptop purchases must be EPEAT-registered. Gold preferred. Verify at epeat.net |
| **Energy Star** | All federal IT equipment must be Energy Star certified (v8.0 for computers) |
| **Key source URLs** | epeat.net, energystar.gov/products/computers, acquisition.gov/far/part-23 |

---

## Vendor Compliance Summary (for Laptops, July 2026)

| Vendor | TAA | §889 Risk | CMMC L2 Ready | EPA+ES | Enterprise Mgmt | Lifecycle | Est. Price Range |
|--------|-----|-----------|---------------|--------|-----------------|-----------|-----------------|
| **HP EliteBook** | Broad (Mexico/Taiwan TH) | Low (US parent) | Yes — Secured-core | Gold + ES 8.0 | vPro, MIK, Intune, SCCM | 18-24mo (fed ext avail) | $1,000–$2,400 |
| **Dell Latitude** | Broad (Mexico/Taiwan/TH) | Low (US parent) | Yes — Secured-core | Gold + ES 8.0 | vPro, Command Suite, Intune | 18-24mo (fed ext avail) | $1,100–$2,500 |
| **Panasonic Toughbook** | Default (Japan assembly) | Low (JP parent) | Yes | Silver + ES | vPro (select), Intune, limited | 36-60mo | $3,500–$7,000 |
| **Lenovo ThinkPad** | TAA SKUs exist (Mexico/JP) | Medium (CN parent) | Yes — if TAA SKU | Gold + ES | vPro, ThinkShield, Intune | 12-18mo (federal avail) | $1,000–$2,200 |
| **Microsoft Surface** | Limited TAA SKUs | Low (US parent) | Yes — if TAA SKU | Gold + ES | Autopilot native, DFCI, no vPro | 16-20mo | $1,200–$2,500 |
| **Apple MacBook Pro** | Not TAA-compliant (China) | Low (US parent) | Not for CMMC | Gold + ES | Limited (Jamf/Intune), no vPro | Annual | $1,600–$4,000 |
| **Getac** | Default (Taiwan assembly) | Low (TW parent) | Yes | Silver | Limited, Intune | 36-60mo | $3,000–$5,000 |

---

## Multi-Regime Synthesis Pattern

When researching federal IT hardware compliance, follow this sequence:

1. **Identify ALL regimes** that apply — don't stop at the first one. For a laptop to be used on a DoD CUI contract, you need TAA + Section 889 + CMMC L2 + IL-4 + STIG + sustainability simultaneously.

2. **Determine which regimes constrain vendor choice vs. config**: TAA and Section 889 constrain WHICH SKUs you can buy (vendor + origin). CMMC/NIST, STIGs, and IL-4 constrain HOW you configure them (OS, encryption, auth). Sustainability constrains which certifications the product must carry.

3. **Research in parallel**: Delegate TAA research to one agent, Section 889 to another, CMMC/STIG/IL-4 to a third. Synthesize at the end.

4. **Build a compliance checklist for procurement**: The combined set of vendor-supplied documents (TAA cert + §889 letter + EPEAT ID + Energy Star listing) should be collected per SKU at procurement time, not after.

5. **Verify per SKU, not per brand**: TAA compliance varies by manufacturing line within the same brand. A standard Dell Latitude (China-assembled) is not TAA-compliant; a Dell Latitude configured for federal (Mexico-assembled) is. Always verify the specific SKU.

---

## Key Authoritative URLs (Fallback When Search Fails)

| URL Pattern | Purpose |
|------------|---------|
| acquisition.gov/far/[PART] | FAR text (52.225-5, 52.204-24, etc.) |
| csrc.nist.gov/publications/ | NIST SP 800-171, FIPS 140 |
| public.cyber.mil/stigs/ | DISA STIGs |
| public.cyber.mil/dccs/ | DoD Cloud Computing SRG |
| dodcio.defense.gov/CMMC/ | CMMC program rule |
| federalregister.gov/documents/ | Rulemaking notices, interim rules |
| fcc.gov/supplychain/covered-list | Section 889 covered entities list |
| epeat.net | EPEAT product registry |
| energystar.gov/products/computers | Energy Star qualified computers |
| sam.gov | System for Award Management (representations) |
| gsa.gov/advantage | GSA Advantage catalog (TAA filter) |

---

*Reference compiled July 22, 2026. Regulatory citations verified against FAR FAC 2026-01, NIST SP 800-171 Rev 3, DISA STIG v2r8 (July 2026), 32 CFR 170 (CMMC 2.0). Verify currency before reuse — TAA thresholds and STIG versions change periodically.*
