# FIPS Mode for Enclave Applications — Compliance Guidance

**Last updated:** July 21, 2026
**Source briefing:** https://brief.h.porb.dev/aecon-fips-enclave-applications.html

## The Controlling Requirement

**SC.L2-3.13.11** (NIST SP 800-171 Rev. 2): "Employ FIPS-validated cryptography when used to protect the confidentiality of CUI."

Related controls: AC.L2-3.1.13 (remote access), AC.L2-3.1.17 (wireless), AC.L2-3.1.19 (mobile devices), SC.L2-3.13.8 (transmission), SC.L2-3.13.16 (data at rest).

## The Protected Environment Exception

Source: NDISAC / DIB SCC CyberAssist, SC.L2-3.13.11 "Further Discussion" section.

> "FIPS-validated cryptography is required to protect CUI when transmitted or stored **outside the protected environment** of the covered OSA information system (including wireless/remote access). Encryption used for other purposes, such as **within applications or devices within the protected environment** of the covered OSA information system, would **not** need to use FIPS-validated cryptography."

Reinforced by **SC.L2-3.13.8**: "Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission **unless otherwise protected by alternative physical safeguards.**"

## Aecon FBU Mapping

- The **GCC High enclave** constitutes the protected environment
- **On-prem applications** running entirely within the enclave do NOT require FIPS mode for internal cryptographic operations
- **FIPS-validated crypto IS required** on all CUI egress paths:
  - Email containing CUI sent to external parties
  - File transfers to the commercial M365 tenant
  - API calls to cloud services outside GCC High
  - VPN/VDI remote access into the enclave
  - CUI stored on mobile devices or portable media that can leave the facility

## Decision Framework

For each on-prem application:
1. **Does it transmit CUI outside the GCC High enclave boundary?** → YES: FIPS required on egress path
2. **Does it allow remote access from outside the physical facility?** → YES: FIPS required on access channel
3. **Does it operate entirely within the enclave, with no CUI egress and no remote access?** → YES: FIPS NOT required

## SSP Documentation Template

For apps that don't require FIPS mode:
> "Application X operates entirely within the GCC High protected environment. Per the DIB SCC SC.L2-3.13.11 guidance, FIPS-validated cryptography is not required for encryption internal to the protected environment."

### Full SSP Entry Template

When the user needs a complete, auditor-ready SSP entry documenting the FIPS exemption for specific enclave applications — not just a one-sentence justification but a full section suitable for direct SSP insertion — use the template in `references/ssp-fips-enclave-entry-template.md`. This is a 10-section markdown document covering: purpose, regulatory authority with verbatim DIB SCC citations, protected environment boundary description, covered applications/server inventory, inter-application communication certification, boundary egress FIPS inventory, FIPS 140-2 expiry risk with POA&M actions, compliance posture summary, evidence references, and approval block. Fill in the `[Insert ...]` placeholders per the client's environment.

## FIPS 140-2 Expiry Risk — September 21, 2026

### The Transition Date

Per the NIST CMVP FAQ:

> *"FIPS 140-2 validated modules will remain on the active list through September 21, 2026. On September 22, 2026, only FIPS 140-3 module validations will remain on the active list."*

— NIST CSRC, Cryptographic Module Validation Program (CMVP), Frequently Asked Questions
Source: https://csrc.nist.gov/Projects/cryptographic-module-validation-program/faqs

**What this means in practice:** On September 21, 2026, the CMVP moves every active FIPS 140-2 certificate to the Historical List. This is NOT a certificate revocation — historical modules remain valid for existing deployments — but federal procurement and assessment standards require *active* certificates. After the transition, any module relying solely on a FIPS 140-2 certificate will no longer satisfy SC.L2-3.13.11 for CMMC assessment purposes.

### Impact on Aecon FBU

- The FIPS 140-2 sunset lands **two months before** Aecon's CMMC L2 certification target (November 2026)
- **Internal enclave applications (P6, N8/NAESTIMATE):** Not affected — internal application cryptography is exempt per the protected environment exception. The FIPS 140-2 → 140-3 transition does not change the exemption.
- **Boundary egress modules (VPN, email gateways, file transfer):** CRITICAL — every FIPS-validated module on a CUI egress path must hold an active FIPS 140-3 certificate at assessment time. Assessors will expect FIPS 140-3, not FIPS 140-2.
- **Required action before August 2026:** Inventory all boundary egress FIPS modules, contact vendors for FIPS 140-3 certification status/timelines, replace any module that won't achieve FIPS 140-3 validation, and update the SSP with confirmed FIPS 140-3 certificate numbers.

## FIPS Mode Compatibility Risks

Enabling FIPS mode can break applications. Known conflicts (from Totem Technologies tracking):
- QuickBooks
- MasterCAM 2022
- SolidWorks Inspection
- Some older firmware versions on FortiGate, SonicWall

## Key Sources

- **NDISAC / DIB SCC CyberAssist**: https://ndisac.org/dibscc/cyberassist/cybersecurity-maturity-model-certification/level-2/sc-l2-3-13-11/
- **DoD CMMC Level 2 Assessment Guide**: https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf
- **NIST SP 800-171 Rev. 2**: Controls 3.13.8, 3.13.11, 3.13.16
- **32 CFR 170.4(b)**: Temporary deficiency definition
- **Totem Technologies**: "What the heck is FIPS-validated cryptography?" (protected environment scoping, FIPS mode breakage)
- **112Cyber**: "FIPS Encryption Requirements in CMMC and NIST SP 800-171" (temporary deficiency documentation)
- **Theodosian**: "CMMC Level 2 Encryption Requirements Explained" (per-file encryption, C3PAO assessment expectations)
