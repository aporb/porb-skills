# SSP Classification, Enclave Placement, Liability, and Assessor Access

Dual-perspective analysis (DIBCAC regulatory + Compliance Officer/Legal) for the recurring
question: **Is the SSP CUI or CDI? Does it have to stay in the enclave? What's the liability
if it's on commercial SharePoint? How do assessors actually access it?**

## 1. Is the SSP CDI under DFARS 252.204-7012? → NO (by default)

CDI requires a **two-prong test**:

**Prong 1 (content):** Must be "controlled technical information" OR "other information, as
described in the CUI Registry... that requires safeguarding or dissemination controls."

**Prong 2 (provenance):** Must be either:
- (1) "Marked or otherwise identified in the contract... and provided to the contractor by or
  on behalf of DoD," OR
- (2) "Collected, developed, received, transmitted, used, or stored by or on behalf of the
  contractor in support of the performance of the contract."

**The SSP fails Prong 2(1)** — DoD does not provide it; the contractor creates it. It arguably
satisfies Prong 2(2) (developed by the contractor in support of contract performance, since
NIST 800-171 control 3.12.4 mandates the SSP).

**But Prong 1 is the real fight:** The SSP is not "controlled technical information" (which is
DoD technical data for defense articles/services per DoDI 5230.24), and it is not automatically
a CUI Registry category. The SSP is internal compliance documentation.

**Source:** DFARS 252.204-7012(a) — "Covered defense information means unclassified controlled
technical information or other information, as described in the Controlled Unclassified
Information (CUI) Registry... that requires safeguarding or dissemination controls pursuant to
and consistent with law, regulations, and Governmentwide policies, and is—(1) Marked or
otherwise identified in the contract... and provided to the contractor by or on behalf of DoD
in support of the performance of the contract; or (2) Collected, developed, received,
transmitted, used, or stored by or on behalf of the contractor in support of the performance of
the contract."

## 2. Is the SSP CUI? → NOT by default, but CAN BE — and DoD treats its copies AS CUI

- The SSP is not marked CUI, not designated CUI in the contract, and not listed as a discrete
  CUI Registry category.
- **HOWEVER:** SSP content (architecture diagrams, port/protocol details, vulnerability status
  via POA&M, control gaps) maps closely to the CUI Registry category **"Information Systems
  Vulnerability Information"** (under Critical Infrastructure). A sufficiently detailed SSP is
  functionally this category.

**The smoking gun — DFARS 252.204-7020(g)(3):**
> "A High NIST SP 800-171 DoD Assessment may result in documentation in addition to that listed
> in this clause. DoD will retain and protect any such documentation as 'Controlled
> Unclassified Information (CUI)' and intended for internal DoD use only."

DoD itself designates assessment documentation (which includes the reviewed SSP) as CUI. **If
DoD treats its copy of your SSP as CUI, the contractor's copy warrants the same treatment.**

## 3. Does the SSP legally have to stay in the enclave? → No explicit mandate, strong pressure says YES

- **No DFARS or 32 CFR provision says "the SSP must reside in the NIST 800-171 environment."**
  The word "enclave" does not even appear in 32 CFR Part 170 (it uses "information system" and
  "CMMC Assessment Scope").
- **BUT** 32 CFR § 170.19(c) Table 3 requires that CUI Assets, Security Protection Assets, and
  Contractor Risk Managed Assets all be "documented in the SSP" and assessed in-scope. The SSP
  *describes* these assets.

**The enclave-description paradox:** If the SSP leaves the enclave, the document proving you
protect CUI is itself unprotected. A sufficiently detailed SSP in the wild is a roadmap for
attacking the very systems it describes.

**Conservative, defensible position:** Treat the SSP as if it were CUI because (a) its content
maps to "Information Systems Vulnerability Information," and (b) DoD's own DFARS 7020(g)(3)
designation creates a reasonable expectation that contractors mirror that protection level.

## 4. Key Distinction: SSP DESCRIBES the enclave but is NOT PART of it

> The SSP is documentation ABOUT the enclave, not a component of it.

Under 32 CFR § 170.19(c), the CMMC Assessment Scope is the set of **assets** (CUI Assets,
Security Protection Assets, Contractor Risk Managed Assets). The SSP is not itself an in-scope
asset. It is the **mandatory description** of those assets (NIST 800-171 control 3.12.4).

**BUT** — documentation describing CUI infrastructure is itself a security-sensitive artifact.
The correct legal framing is not "is the SSP CUI?" but **"what is our risk exposure if the SSP
is mishandled?"** The answer: significant, whether or not it technically meets the CDI definition.

## 5. Liability Matrix: SSP on Commercial SharePoint

| Scenario | Liability Level | Basis |
|---|---|---|
| SSP is CUI (detailed, includes vuln info) on commercial SharePoint | **SEVERE** — Reportable cyber incident under DFARS 7012(c); 72-hour DIBNet reporting; SPRS score damage; potential contract suspension | DFARS 7012(c), 7019(b) |
| SSP is NOT CUI but exfiltrated | **MODERATE** — No DFARS reporting trigger, but False Claims Act exposure if you certified compliance while mishandling; reputational harm; usable as evidence in breach litigation; C3PAO/DIBCAC will flag as control failure (3.12.4 implementation) | Common law negligence, FCA 31 U.S.C. § 3729 |
| SSP on commercial SharePoint with read-only, MFA, conditional access, NDA'd consultants | **LOW-MODERATE** — Defensible if you can articulate why it's not CUI and show reasonable security; risky if C3PAO disagrees with your classification | Risk-based judgment |

## 6. How DIBCAC and C3PAOs Actually Access the SSP

Per **DFARS 252.204-7020(c):**
> "The Contractor shall provide access to its facilities, systems, and personnel necessary for
> the Government to conduct a Medium or High NIST SP 800-171 DoD Assessment."

The assessment methodology uses three techniques:

1. **Document review** — SSP, POA&M, policies, evidence shared with assessment team
2. **Verification/examination/demonstration** (DFARS 7020 High Assessment definition):
   > "Verification, examination, and demonstration of a Contractor's system security plan to
   > validate that NIST SP 800-171 security requirements have been implemented as described in
   > the contractor's system security plan"
3. **Discussions/interviews** with contractor personnel

**In practice:** DIBCAC (for Level 3) and C3PAOs (for Level 2 certification assessments under
32 CFR § 170.19) receive the SSP via secure file exchange under NDA. The contractor maintains
the authoritative copy within their environment.

**This undercuts any "but consultants/C3PAOs need access" justification for storing the SSP on
commercial SharePoint.** You can share a controlled copy with C3PAOs under NDA without storing
the working version outside the enclave.

## 7. How DoD Handles Its Own SSPs (Precedent)

Under RMF (NIST SP 800-37, incorporated by reference at 32 CFR § 170.4(b)), DoD SSPs are
maintained within the system's authorization boundary and treated as sensitive documentation.
DoD SSPs are typically designated CUI (often "Controlled" or "Security" category) when they
contain vulnerability or architecture information. This reinforces the conservative position.

## 8. Bottom-Line Recommendation for Compliance Officers

1. **Maintain the authoritative SSP within the NIST 800-171 environment** (GCC High enclave).
   No statute explicitly mandates this, but it is the defensible, lowest-risk position given
   DFARS 7020(g)(3)'s CUI designation and the enclave-description paradox.
2. **Share controlled copies** with C3PAOs, DIBCAC, legal counsel, and consultants via secure,
   NDA-protected, auditable channels — not by parking the working document on commercial
   SharePoint.
3. **If you must use commercial SharePoint** for collaboration, store only a **redacted version**
   (remove architecture diagrams, port/protocol details, POA&M vulnerability specifics) and keep
   the full SSP in the enclave.
4. **Document your classification decision in writing** — if you determine the SSP is not CUI,
   record the rationale. This protects against later second-guessing by a C3PAO or DIBCAC
   assessor.

## Source Documents Verified

All regulatory citations in this reference were verified against authoritative sources during
the July 2026 analysis session:

- **DFARS 252.204-7012** (CDI definition, safeguarding, cyber incident reporting) — Cornell LII
  mirror: `https://www.law.cornell.edu/cfr/text/48/252.204-7012`
- **DFARS 252.204-7019** (NIST 800-171 assessment requirements, SPRS scoring) — Cornell LII:
  `https://www.law.cornell.edu/cfr/text/48/252.204-7019`
- **DFARS 252.204-7020** (Medium/High assessment definitions, assessor access, CUI designation
  at (g)(3)) — Cornell LII: `https://www.law.cornell.edu/cfr/text/48/252.204-7020`
- **32 CFR § 170.19** (CMMC scoping, Table 3 asset categories) — Cornell LII:
  `https://www.law.cornell.edu/cfr/text/32/170.19`
- **32 CFR § 170.3** (applicability) — Cornell LII:
  `https://www.law.cornell.edu/cfr/text/32/170.3`
- **CUI Registry** (category list including "Information Systems Vulnerability Information"):
  `https://www.archives.gov/cui/registry/category-list`

**Note:** eCFR (`ecfr.gov`) and DoD CIO (`dodcio.defense.gov`) block automated access. Use the
Cornell LII mirror (`law.cornell.edu/cfr/text/`) for all CFR sections — it returns clean,
curl-accessible HTML.
