# CMMC Entity Scope & Corporate Structure — Regulatory Reference

Condensed knowledge bank of CMMC 2.0 entity-scope, enclave, and corporate-structure rules.
Built from 32 CFR Part 170 (via Cornell LII mirroring official eCFR), DFARS Subpart 204.75
and clauses 252.204-7019/7020/7021 (NOV 2025), and the Aecon AFSI enclave deployment plan.
All citations are to the binding regulation unless noted "(guidance)".

## Certification Level: Entity, Enclave, or System?

**CMMC certification is granted at the INFORMATION SYSTEM level** — recorded per-system in
SPRS with a 10-char CMMC UID — scoped by a "CMMC Assessment Scope." It is NOT entity-level.

- § 170.4: "The CMMC Status of an OSA **information system** is officially stored in SPRS."
- § 170.19(a)(1): "The CMMC Assessment Scope is the set of all assets in the OSA's
  environment that will be assessed against CMMC security requirements."
- DFARS 252.204-7021(d)(1): CMMC status required "for all information systems used in
  performance of the contract...that process, store, or transmit FCI or CUI."

**"Enclave" is NOT a defined term in 32 CFR Part 170.** It appears only in the DoD CIO
Scoping Guide (a guidance doc referenced in Appendix A). The regulation speaks of
"information system," "CMMC Assessment Scope," and "OSA's environment." Practitioners use
"enclave" to mean a logically isolated set of in-scope assets = the Assessment Scope.

## Multiple Enclaves / Mixed Levels — PERMITTED

A company can have multiple Assessment Scopes (enclaves) at different levels.
- § 170.16(a): "...for the **same** CMMC Assessment Scope" implies different scopes exist.
- § 170.19(d): "The Level 3 CMMC Assessment Scope must be equal to or a subset of the
  Level 2 CMMC Assessment Scope" — nested scopes at different levels are contemplated.
Each scope gets its own CMMC UID in SPRS.

## Multiple CAGE Codes / Business Units — ONE CERT CAN COVER MANY

Each CAGE code does NOT need separate certification. CAGE codes are LISTED in the SPRS
record; one Assessment Scope can cover many. Plural language throughout:
- § 170.15(a)(1)(i)(D) [L1]: "All industry CAGE code(s) associated with the information
  system(s) addressed by the CMMC Assessment Scope."
- § 170.16(a)(1)(i)(D) [L2 self]: identical plural language.
- § 170.17(a)(1)(i)(E) [L2 C3PAO]: identical plural language.
- DFARS 252.204-7019(d)(1)(i)(C)(1): "All industry CAGE code(s)...if more than one plan exists."

## Enclave Expansion (Adding CAGE Codes / Business Units)

Not a regulatory term, but the mechanism is a SCOPE CHANGE triggering reassessment:
1. Adding systems/CAGEs/BUs to the certified environment = change to Assessment Scope.
2. "Current" status requires "no changes in compliance" since the Status date
   (DFARS 204.7501). A material scope expansion likely invalidates "Current" if unassessed.
3. Process: update SSP (§ 170.19(c)(1) — CUI Assets, Security Protection Assets, etc.) →
   update Assessment Scope definition → C3PAO delta/supplemental assessment → C3PAO posts
   updated results to eMASS→SPRS with expanded CAGE list → new/updated CMMC UID.
4. Segregation pen-test advisable before declaring operational.

## Multiple Legal Entities Sharing One Enclave — PERMITTED

The OSA (§ 170.4) is "the entity seeking to undergo...assessment for a given information
system." The regulation keys on systems + CAGE codes, NOT legal-entity boundaries.
- Parent + subsidiary: permitted (e.g., Canadian parent → US subsidiaries).
- Sister companies: permitted if they share the same assessed system, listed by CAGE.
- Conditions: all CUI systems within one Assessment Scope, assessed together; logical
  segregation documented in SSP; each entity's CAGE listed in SPRS; OSA accepts scope
  responsibility.
- Foreign ownership: not a CMMC bar, but triggers FOCI/CTA review + ATCP/ITAR controls
  (parallel to, not part of, CMMC). Assessors examine foreign-national access under AC/IA.

## Acquisitions / Mergers — NO AUTOMATIC TRANSFER

Cert attaches to the information system + its Assessment Scope, not the corporate entity.
- If acquired systems remain operationally unchanged, cert MAY remain valid; acquirer
  becomes the new OSA and assumes annual affirmation obligations (§ 170.22).
- Material change to architecture/personnel/policies/scope = "change in compliance" →
  can invalidate "Current" status (DFARS 204.7501). Reassessment typically required.
- New parent must update SPRS (CAGE codes, affirming official) and SSP.

## Reciprocity Across Contracts — YES (portable)

CMMC is system/scope-specific, not contract-specific. A cert is portable across contracts
at the same or lower level.
- DFARS 252.204-7021(c): "CMMC assessments will not duplicate efforts from any other
  comparable DoD assessment."
- § 170.17(a): L2(C3PAO) "also satisfies...Level 1 (Self) and Level 2 (Self)...for the same
  CMMC Assessment Scope."
- Contracting officers check SPRS by CMMC UID (DFARS 204.7503(b)).
Limitations: contract CUI must flow through the CERTIFIED system; specific contracts may
add requirements (NIST 800-172, classified, ITAR) beyond CMMC L2.

## Assessment Boundary — What Determines It

The boundary = the CMMC Assessment Scope = the in-scope asset set per § 170.19, documented
in the SSP. It is tied to:
1. The information system(s) processing/storing/transmitting FCI or CUI — the defining element.
2. Asset categories in § 170.19(c)(1) Table 3 (L2): CUI Assets, Security Protection Assets,
   Contractor Risk Managed Assets, Specialized Assets (in); Out-of-Scope Assets (excluded).
3. CAGE codes (listed, not defining).
4. The contract's data that necessitates the scope — but once defined, serves all contracts
   using that system.
NOT tied to: a single contract, a single CAGE code, or the entire company.

## NIST SP 800-171 Rev 2 → Rev 3 — REV 2 IS CURRENT FOR CMMC

- § 170.14(c)(3): "The security requirements in CMMC Level 2 are identical to the
  requirements in **NIST SP 800-171 R2**." Incorporated by reference (§ 170.2).
- CMMC Final Rule (eff. Dec 16, 2024) and DFARS CMMC rule (eff. Nov 10, 2025) both cite
  Rev 2. No regulatory amendment yet updates § 170.14(c)(3) to Rev 3.
- Rev 3 (published 2024, ~97 requirements reorganized) is NOT mandatory for CMMC and has
  NO firm transition date in regulation. DoD must publish a rule amendment to incorporate it.
- Guidance: build to Rev 2 (110 controls) for certification now; track Rev 3 deltas for
  future migration; do not delay certification awaiting Rev 3.

## CMMC Final Rule Phase-In Timeline (through 2028+)

### 32 CFR § 170.3(e) — Four Implementation Phases (program-side)
- Phase 1: begins on effective date of DFARS CMMC Acquisition Rule (Nov 10, 2025). DoD
  intends L1(Self)/L2(Self); may include L2(C3PAO).
- Phase 2: ~Nov 2026 (1 yr after Phase 1). Adds L2(C3PAO) as award condition.
- Phase 3: ~Nov 2027 (1 yr after Phase 2). L2(C3PAO) all applicable + option periods;
  L3(DIBCAC) all applicable critical contracts.
- Phase 4 (~Nov 2028): full implementation — CMMC in all applicable solicitations/contracts
  incl. option periods on pre-Phase-4 contracts.

### DFARS 204.7504(a) — Hard Clause Prescription Dates
- (a)(1): Clause 252.204-7021 used "Until November 9, 2028" if CO determines CMMC level
  required (discretionary during phase-in).
- (a)(2): "On or after November 10, 2028" clause used whenever contractor systems
  process/store/transmit FCI or CUI (mandatory, broad).

| Date | Milestone |
|---|---|
| Dec 16, 2024 | 32 CFR Part 170 (CMMC Program Rule) effective |
| Nov 10, 2025 | DFARS CMMC Acquisition Rule effective → Phase 1 begins |
| ~Nov 2026 | Phase 2 (L2 C3PAO as award condition) |
| ~Nov 2027 | Phase 3 (L2 C3PAO + L3 DIBCAC broadly) |
| Nov 9, 2028 | Last day discretionary/phase-in clause use |
| Nov 10, 2028 | Full mandatory implementation (FCI/CUI trigger) |

## Authoritative Source Access Notes (see SKILL.md Pitfalls)

- **32 CFR Part 170**: eCFR + Federal Register BLOCK automated access (return "Request
  Access" page). Use Cornell LII instead — accessible via curl, mirrors official text:
  `curl -sL "https://www.law.cornell.edu/cfr/text/32/170.19"` (any § 170.NN).
- **DFARS**: local archive at `reference-docs/dfars-extracted/dita_html/` is authoritative.
  Key files: `SUBPART_204.75.html`, `204.7500-7504.html` (acquisition policy + timeline),
  `dfars-key-clauses/DFARS-252.204-7019/7020/7021-*.html`.
- **DoD CIO Scoping Guide / CAP**: still blocks all automated access (manual download only).
