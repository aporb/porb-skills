# Software Procurement Governance Checklist
## GCC High / CMMC Enclave — FBU Compliance Gate for Software Intake

**Effective:** July 2026 | **Source:** FAR Part 12 (FAC 2026-01), DFARS Change 5/7/2026, 32 CFR Part 170 (CMMC)

---

## Regulatory Framework Quick Reference

### Which FAR Part Applies?

| Purchase Type | Primary FAR | Notes |
|---|---|---|
| Commercial software (COTS) sold to general public | **FAR Part 12** | FAR 12.102(a): Shall use Part 12 for commercial items |
| COTS via GSA Schedule | FAR Part 12 (terms) + **FAR Part 8** (vehicle) | FAR 8.4 governs ordering; commercial terms flow through FAR 12 |
| Micro-purchases (= $10K) | **FAR Part 13** only | FAR 12.102(e): Part 12 does NOT apply at/below micro-purchase threshold |
| Simplified acquisitions ($10K-$250K) | FAR Part 12 + **FAR Part 13** | FAR 13.003(a): Use simplified procedures to maximum extent |
| Commercial items $250K-$9M | FAR Part 12 + **FAR 13.5** | FAR 13.5: Simplified procedures for commercial items up to $9M ($15M DoD) |

### Critical DFARS Clauses

| Clause | What It Requires | Applies To |
|---|---|---|
| **252.204-7012** (May 2024) | NIST SP 800-171; 72-hr cyber incident reporting | Any contract handling CUI/CDI; flows to subs handling CDI |
| **252.204-7019** (Nov 2023) | Pre-award: offeror must have current SPRS score | Solicitations where 7012 applies |
| **252.204-7020** (Nov 2023) | Post-award: NIST 800-171 assessment requirements | Contracts where 7012 applies; subs except COTS |
| **252.204-7021** (Nov 2025) | CMMC certification at specified level; annual affirmation | Contracts handling FCI or CUI; subs except COTS |
| **252.204-7024** | SPRS item/price/supplier risk search before award | All solicitations including FAR Part 12 |
| **252.239-7010** (Jan 2023) | Cloud SRG compliance; US data residency | Any contract using cloud services |
| **252.204-7016/7017/7018** | Section 889 — no covered telecom (Huawei/ZTE) | ALL contracts (statutory, not waivable) |
| **FAR 52.204-23** | Kaspersky prohibition | ALL contracts |
| **FAR 52.204-25** | Section 889(a)(1)(A) telecom prohibition | ALL contracts |
| **FAR 52.204-27** | ByteDance/TikTok prohibition | Discretionary — CO checked in 52.212-5 |

### Threshold Dollar Amounts (2026)

| Threshold | Amount | What Changes |
|---|---|---|
| Micro-purchase | $10,000 | FAR Part 12 not required; minimal clauses |
| Simplified Acquisition (SAT) | $250,000 | FAR Part 13 simplified procedures |
| Commercial items (13.5) | Up to $9M ($15M DoD) | Simplified procedures for commercial |
| COTS exemption — Buy American | Any | COTS exempt from domestic content test (FAR 12.505(a)) |
| COTS exemption — CMMC flow-down | Any | 252.204-7021 does NOT flow to COTS subcontracts |

### FedRAMP vs. DoD Impact Levels

DoD does NOT use FedRAMP directly. It uses the DoD Cloud Computing SRG with Impact Levels:
- IL2 = FedRAMP Low equivalent
- IL4 = FedRAMP Moderate equivalent (minimum for CUI)
- IL5 = Higher-sensitivity CUI (nuclear, export-controlled)
- IL6 = Classified

A FedRAMP Moderate ATO does NOT automatically authorize at IL4/IL5 — the CSP must also meet DoD SRG controls.

---

## FBU Software Intake Checklist

### GATE 1: Threshold Classification (Auto-routing)

| If... | Then... |
|---|---|
| <= $10K AND software does NOT touch CUI/FCI | **INFORM only.** Auto-approve with Section 889 + SAM check |
| <= $10K BUT software may touch CUI/FCI | **GATE 2 required.** FBU Consulted |
| $10K-$100K (any software) | **GATE 2 required.** FBU Consulted |
| >$100K | Full procurement governance (not covered here) |

### GATE 2: CUI/FCI Determination

**Will this software process, store, or transmit CUI or FCI?**

| Answer | Path |
|---|---|
| **NO** — tool outside enclave (e.g., public analytics, HR system with no DoD data) | **LIGHT CHECK.** Gate 3-A. FBU = Informed |
| **YES** — touches contract data, technical specs, personnel clearances | **FULL CHECK.** Gate 3-B. FBU = Consulted |
| **UNCLEAR** | Default to YES. Escalate to FBU |

### GATE 3-A: Light Check (No CUI/FCI — FBU Informed)

| # | Check | Evidence |
|---|---|---|
| 1 | SAM Check — vendor not debarred/suspended | SAM.gov lookup |
| 2 | Section 889 — no covered telecom (Huawei, ZTE, Hytera, Hikvision, Dahua) | SAM rep or signed cert |
| 3 | Kaspersky — not a Kaspersky product | Self-evident |
| 4 | ByteDance/TikTok — not a ByteDance app | Self-evident |
| 5 | Data residency — if SaaS, data stays in US/outlying areas | Vendor docs |

### GATE 3-B: Full Check (CUI/FCI — FBU Consulted)

| # | Check | What to Verify | Evidence |
|---|---|---|---|
| 1 | SAM Check | Not debarred, suspended, or proposed | SAM.gov |
| 2 | Section 889 | No covered telecom (FAR 52.204-25, DFARS 7016/7017/7018) | SAM rep or cert |
| 3 | Kaspersky/ByteDance | Not prohibited vendor (FAR 52.204-23, 52.204-27) | Self-evident |
| 4 | SPRS Score | Current NIST SP 800-171 assessment in SPRS (<=3 years). Minimum: Basic (self-assessment) | SPRS lookup with CAGE |
| 5 | CMMC Level | Vendor holds required CMMC level. For CUI -> Level 2 (C3PAO or Self) | SPRS CMMC entry |
| 6 | Cloud — DoD Impact Level | If SaaS: authorized at IL4 (min for CUI) or IL5 (higher sensitivity). Check DoD PA listing | DoD PA listing or FedRAMP + SRG mapping |
| 7 | Data Residency | All gov data stored/processed in US or outlying areas | Vendor SOC 2 / contract |
| 8 | Supply Chain Risk | SPRS supplier risk not flagged high; no foreign ownership concerns for critical tech | SPRS, DCSA where applicable |
| 9 | Subcontractor Flow-Down | If vendor uses subs handling CUI, confirm flow-down of 7012/7020/7021 | Vendor sub mgmt plan |

---

## Minimum Viable vs. Over-Engineering (sub-$100K)

### The Five MVP Checks

1. **Is the vendor in good standing?** (SAM check — 30 seconds)
2. **Section 889 clean?** (covered telecom prohibition — checkbox)
3. **Does the software touch CUI?** (if NO -> stop, approve)
4. **If YES — SPRS score on file?** (vendor has at minimum a self-assessment)
5. **If SaaS — authorized at correct Impact Level?** (IL5 for GCC High nuclear CUI; IL4 min for general CUI)

### What NOT to Do (Over-Engineering)

| Over-Engineering | Why Wrong | What Instead |
|---|---|---|
| Full CMMC L2 certification for non-CUI software | CMMC 7021 only applies when FCI/CUI involved | Use Light Check (Gate 3-A) |
| Demanding FedRAMP ATO for $20K SaaS | DoD uses own PA process + SRG. Check existing PA listing | Verify existing DoD PA at correct IL |
| Full supply chain risk assessment for mass-market COTS | SPRS supplier risk check sufficient for sub-$100K | SPRS supplier lookup (30 seconds) |
| Legal review of EULA for standard COTS | FAR 12.302 says terms match commercial practice | Accept commercial EULA unless conflicts with federal law |
| Custom DFARS clause tailoring per sub-$100K buy | FAR Part 13 aims to reduce admin costs and avoid burdens (FAR 13.002) | Standard FAR 12/13 boilerplate |
| NIST 800-171 for on-prem tool inside already-accredited GCC High enclave | Enclave itself is the security boundary; tools inherit accreditation | Verify enclave boundary controls cover tool |
| Multi-week FBU review cycle | Gates should be gates, not bottlenecks | SLA: 2 days Light, 5 days Full |

### FBU Review SLA

- Light Check (Gate 3-A): <= 2 business days
- Full Check (Gate 3-B): <= 5 business days

---

## Additional Regulatory Notes

1. **FAR 12.212 — Computer Software:** Dedicated section for software acquisition under commercial items. Government gets same license rights as commercial customers — no unlimited government-purpose rights unless separately negotiated.

2. **52.212-4 / 52.212-5:** Mandatory commercial contract clauses. 52.212-4 covers terms (inspection, payment, disputes, termination). 52.212-5 is a "checklist clause" — CO checks which statutes apply. DFARS clauses (7012, 7019, 7020, 7021) are added via 52.212-5 flow-down or agency supplement.

3. **CMMC Phased Rollout (as of July 2026):**
   - Phase 1 (Nov 10, 2025 - Nov 9, 2026): CMMC Level 1 and Level 2 self-assessments
   - **Phase II suspended July 13, 2026** pending 60-day task force review
   - For now, SPRS self-assessment + CMMC Level 2 (Self) is sufficient

4. **SPRS Access:** SPRS is at https://piee.eb.mil (PIEE). CAGE code is the lookup key. FBU compliance team should have SPRS access.

*Last verified against acquisition.gov (FAR FAC 2026-01, DFARS Change 5/7/2026). This is a governance tool, not legal advice.*