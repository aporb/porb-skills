# DFARS 7012 / NIST SP 800-171 / ATO Regulatory Research

> Regulatory compliance findings for cloud services handling CUI under DoD contracts.
> Compiled from eCFR, FedRAMP 2026 Consolidated Rules (OMB M-24-15), and NIST SP 800-171 Rev. 3.

## Source Locations

| Document | Location | How to Access |
|----------|----------|--------------|
| DFARS 252.204-7012 | eCFR §252.204-7012 | eCFR API versioner (browser blocks direct navigation) |
| OMB M-24-15 | FedRAMP 2026 Consolidated Rules | fedramp.gov/2026 → FedRAMP → FedRAMP's Authority → OMB M-24-15 |
| NIST SP 800-171 Rev. 3 | NIST Special Publication | nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf |
| FedRAMP Authorization Act | 44 U.S.C. §3600 et seq. | uscode.house.gov |

### ⚠️ DFARS 7012(b)(2)(ii)(D) — Corrected Text

**This is commonly misquoted. The correct text:**

> *(D) If the Contractor intends to use an external cloud service provider to store, process, or transmit any covered defense information in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets **security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline**.*

Source: Cornell LII — 48 CFR §252.204-7012 — verified via live curl extraction on 2026-07-10.

**Contrast with the common misquote:**
- ❌ **Wrong:** "shall not acquire from a CSP that has a FedRAMP authorization at the Moderate or High baseline"
- ✅ **Right:** "shall require and ensure that the CSP meets security requirements **equivalent to** FedRAMP Moderate"

The actual text uses "equivalent to" — it supports equivalency, not undermines it.

## OMB M-24-15 Key Provisions (July 25, 2024)

### §IV.a — Presumption of Adequacy
- If a CSO has a FedRAMP authorization at a given FIPS 199 impact level, agencies **must presume** the security assessment is adequate for issuing their own ATO at or below that level.
- Agencies may overcome this presumption only for a "demonstrable need" or if the package is "wholly or substantially deficient."
- Does **not** supersede FISMA authorities of agency heads.

### §IV.b — Authorization Process Requirements
- FedRAMP defines criteria for authorization.
- FedRAMP should enable expedited authorization for agencies with mature processes.
- Recognizes shared responsibility between agency and CSP.

### §IV.c — Authorization Paths
1. **Agency Authorization**: Signed by agency's Authorizing Official. Can be single agency or joint (multiple agencies pooling resources). Joint authorizations replace the old JAB P-ATO concept.
2. **Program Authorization**: Signed by FedRAMP Director. For CSOs without an identified agency sponsor but with expected multi-agency use.
3. **Other Paths**: Designed by FedRAMP PMO with OMB/NIST consultation.

### §IV.d — Assessing Security Postures
- FedRAMP should assess complex architectures, encryption schemes, and operate "red team" assessments.
- Threat-based control baseline analysis in collaboration with CISA.
- FedRAMP Board sets requirements; PMO handles individual package review.

### §IV.e — Supporting the Marketplace
- **Temporary authorization**: Up to 12 months for piloting; extendable if full authorization in progress.
- **Marketplace** is authoritative for which CSOs are authorized.
- FedRAMP authorization as condition of contract award is permissible if adequate competition exists.

### §X — Rescissions
Rescinds the December 8, 2011 OMB memo ("Security Authorization of Information Systems in Cloud Computing Environments") **in its entirety**.

### Key Footnotes
- **Footnote 5**: *"the appropriate agency authorizing officials must issue an authorization when reusing artifacts (such as system security plans and assessments) in the FedRAMP repository."*
- **Footnote 10**: *"Existing JAB P-ATOs at the time of the issuance of this memorandum will be re-designated as determined by the FedRAMP PMO in collaboration with the CSP."*

## FedRAMP Equivalency — Post-M-24-15 Status

### What Changed
- Pre-2024 FedRAMP recognized "Equivalency Authorizations" — when an existing agency authorization was deemed equivalent to FedRAMP without full JAB or FedRAMP review.
- M-24-15 rescinded the 2011 memo that was the legal foundation for equivalency.
- No blanket grandfather clause, sunset date, or transition period was provided for equivalency authorizations.

### Risk Assessment
- CSPs with equivalency-only authorizations that were not formally re-designated by the FedRAMP PMO face legal uncertainty for DFARS 7012(b)(2)(ii)(D) compliance.
- The FedRAMP 2026 Consolidated Rules site warns: *"Historical FedRAMP information is now often wrong! Nearly all of that historical information no longer applies after FedRAMP was rescinded and replaced in 2024."*
- Safest verification: check the FedRAMP Marketplace for current authorization status.
- Existing JAB P-ATOs were explicitly slated for re-designation (fn. 10); equivalency authorizations were NOT given equivalent treatment.

### Contrast Scale

| Auth Type | Pre-M-24-15 | Post-M-24-15 | Valid for DFARS 7012? |
|-----------|-------------|--------------|----------------------|
| Full FedRAMP (JAB) | Authorized | Re-designated or re-certified | Yes (if current) |
| Full FedRAMP (Agency) | Authorized | Transitioned to Agency Auth path | Yes (if current) |
| Agency Equivalency | Deemed equivalent | Rescission makes legal basis unclear | Uncertain — verify Marketplace |
| FedRAMP Ready | Readiness only | Still exists (being retired) | No — not an authorization |

## ATO Distinctions Summary

| Party | Gets ATO? | Cites What | For What |
|-------|-----------|-----------|----------|
| CSP | Yes (FedRAMP Authorization/Certification) | FedRAMP criteria | Their cloud service offering |
| Federal Agency | Yes (ATO/ATU) | FedRAMP package + own risk acceptance | Their information system using the CSP |
| Contractor | No | N/A | Their CUI environment under the contract is governed by NIST SP 800-171 compliance, not ATO |

## NIST SP 800-171 Rev. 3 — Cloud Guidance

Section **03.16.03 (External System Services)** addresses cloud services. Key principle: organizations must use FedRAMP-authorized CSPs for CUI in cloud environments. The requirement aligns with DFARS 7012(b)(2)(ii)(D).

## Best Practices for Contractor Cloud Compliance (DFARS 7012)

1. **Verify CSP FedRAMP status** on the FedRAMP Marketplace (not vendor press releases alone).
2. **Check authorization class**: Must be Moderate or High (Class C or D) for CDI/CUI.
3. **Confirm currency**: Pre-2024 equivalency authorizations carry post-rescission risk.
4. **Document the NIST SP 800-171 compliance posture** of your own CUI environment (the system *using* the cloud service).
5. **Do not conflate "ATO" with compliance**: The contractor does not need an ATO. The contractor needs (a) FedRAMP-authorized CSP selection and (b) NIST SP 800-171 self-assessment.

## Technical Note — Research Tools

- **eCFR browser blocks**: Use the API versioner, not browser navigation, for DFARS sections.
- **FedRAMP 2026 SPA**: `browser_snapshot` truncates full article text. Use `browser_console` with `document.querySelector('article').innerText` to extract complete content.
- **M-24-15 PDF**: Original whitehouse.gov URL may 404. The full text is available at fedramp.gov/2026 in the FedRAMP → OMB Memorandum M-24-15 section.
- **NIST PDF**: Download directly from nvlpubs.nist.gov and use `pdftotext` for offline extraction.
