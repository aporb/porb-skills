# InEight Document — A-LIGN SAR Analysis (July 10, 2026)

## Source Document
FedRAMP Security Assessment Report (SAR) for InEight Inc. — Document - US Government
- Version 1.0, 12/17/2025
- Prepared by: A-LIGN, Inc. (Tampa, FL) — FedRAMP-recognized 3PAO
- FedRAMP Unique ID: FR2520254824
- Impact Level: Moderate | Service Model: SaaS | Deployment: Government-Only Cloud

## What We Confirmed

### Table 2-2: ALL ZEROS
Zero open risks at every severity level — High, Moderate, Low. Zero across all testing types: OS scans, web scans, DB scans, container scans, penetration testing, CM-6 configuration checks. Zero operational requirements. Zero vendor dependencies.

**Meaning:** Initial assessment closed with no findings. Meets the strictest condition (zero control-related POA&Ms) from the DoD's Dec 2023 equivalency memo.

### A-LIGN's Recommendation (Page 9)
Explicit quote: "A-LIGN recommends this system for FedRAMP Equivalency in accordance with the DoD Memorandum for the Federal Risk and Authorization Management Program Moderate Equivalency for Cloud Service Provider's Cloud Service Offerings."

**Meaning:** The assessment was explicitly designed around the DoD equivalency framework, not the standard FedRAMP JAB authorization path. This aligns with our legal analysis.

### Weaknesses Found and Remediated
1. Apple corecrypto Module 18.3 used for MFA — not yet FIPS validated (status: "Review Pending" as of 10/15/2025)
2. Push-based MFA with number context — not phishing-resistant
Both remediated "following post-interview testing." Both closed.

### Scope
- 100% of FedRAMP Moderate security controls assessed
- Assessment period: Sept 29 — Dec 17, 2025 (~10 weeks)
- All security controls identified in approved SAP Version 2.2, dated 09/22/2025
- SSP Version 3.6 referenced as the system description

### Architecture
- Runs on Azure Government
- Multi-tenant Government-Only Cloud (shared with other InEight government clients)
- Separate from Aecon's commercial enterprise tenant
- Uses Azure Entra ID for RBAC, Azure VNETs/NSGs/subnets for boundary protection

### Documentation Artifacts Reviewed (Appendix E)
2025 Information Security Compliance Training, SECURITY CONSIDERATIONS FOR A.I., Incident Response Process & DR/BCP, Supply Chain Security Component Authenticity & Anti-Counterfeiting, Data Spillage Training, A-LIGN Red Team Operation, Clean Desk Clear Screen Policy, 2025 Incident Response Tabletop, Vendor Risk Analysis, 2025 IT Risk Assessment

### Penetration Test (Appendix F)
Conducted remotely by A-LIGN on 10/31/2025. Separate report file (not included in the SAR PDF).

## What We Cannot Answer from the SAR

| Question | Why Not |
|---|---|
| Sponsoring agency | The SAR references the DoD memo but does not name the specific agency. FR2520254824 confirms it was in the pipeline. DoD component is the strongest inference. |
| CR26 transition plans | SAR predates CR26 (12/17/2025 vs CR26 effective 7/4/2026). Nothing in the document about new rules. |
| Continuous monitoring state | Table 2-2 is point-in-time at assessment conclusion (12/17/2025). Any findings from ongoing scans since then would be in a separate continuous monitoring POA&M. |
| Raw scan data / SRTM / pen test report | Referenced as zip files not included in the PDF. Required for C3PAO CMMC evidence, but findings already summarized in Table 2-2. |

## CR26 Implications
- The SAR was conducted under the old FedRAMP framework (pre-CR26)
- A-LIGN's recommendation references the DoD equivalency memo which is where CR26 redirects equivalency questions
- CR26 early-adoption window: July 4, 2026 — January 1, 2027
- If InEight does not pursue a CR26 certification class by Jan 1, 2027, the legal basis for claiming equivalency weakens
- For Aecon's immediate needs: the equivalency is sufficient under DFARS 7012. The January 2027 deadline affects long-term planning, not the current decision.

## Skill Signal
This session established a repeatable pattern for analyzing a 3PAO SAR: extract Table 2-2, read recommendation paragraph, identify weaknesses and remediation, check appendix structure for embedded artifacts, distinguish initial assessment findings from continuous monitoring.
