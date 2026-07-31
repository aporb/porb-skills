# SSP Entry Template: FIPS-Validated Cryptography Exemption — Internal Enclave Applications

**SSP Section:** SC.L2-3.13.11 — CUI Encryption (FIPS-Validated Cryptography)  
**Related Controls:** SC.L2-3.13.8 (Data in Transit), SC.L2-3.13.16 (Data at Rest)  
**System / Enclave:** [Client] [Enclave Name]  
**CMMC Target Level:** [Level] — Target Assessment Date: [Date]  
**Prepared By:** [Name / Role]  
**Date:** [Date]  
**Classification:** For Official Use Only

---

## 1. Purpose and Scope

This entry documents the approach to compliance with **SC.L2-3.13.11 (CUI Encryption)**, specifically the exemption from FIPS-validated cryptography for encryption used *within* the protected environment boundary of the covered OSA information system. Per DIB SCC CyberAssist guidance, FIPS-validated cryptographic modules are required only when CUI is transmitted or stored **outside** the protected environment. Internal application-to-application communication and data handling that remains wholly within the enclave boundary is exempt under this provision. FIPS-validated cryptography is applied at all boundary egress points.

---

## 2. Regulatory Authority — DIB SCC SC.L2-3.13.11 "Further Discussion"

The following language from the DIB SCC CyberAssist SC.L2-3.13.11 "Further Discussion" section provides the controlling authority for this exemption (emphasis added):

> *"FIPS-validated cryptography means the cryptographic module has to have been tested and validated to meet FIPS 140-2 requirements. Simply using an approved algorithm is not sufficient – the module (software and/or hardware) used to implement the algorithm must be separately validated under FIPS 140. **Accordingly, FIPS-validated cryptography is required to protect CUI when transmitted or stored outside the protected environment of the covered OSA information system (including wireless/remote access). Encryption used for other purposes, such as within applications or devices within the protected environment of the covered OSA information system, would not need to use FIPS-validated cryptography.**"*

> — DIB SCC CyberAssist, Cybersecurity Maturity Model Certification > Level 2 > SC.L2-3.13.11 CUI Encryption, "Further Discussion"  
> Source: https://ndisac.org/dibscc/cyberassist/cybersecurity-maturity-model-certification/level-2/sc-l2-3-13-11/

**Interpretation:** The DIB SCC explicitly distinguishes between (a) externally-facing cryptographic protections that must be FIPS-validated, and (b) internal encryption within the protected environment boundary that is exempt from the FIPS validation requirement. This exemption is the foundation for the enclave architecture described below.

### Supporting Reference — SC.L2-3.13.8 (Alternative Physical Safeguards)

SC.L2-3.13.8 further recognizes that "alternative physical safeguards" may substitute for cryptographic protections when data in transit is protected against electronic or physical intercept:

> *"An example of an alternative physical safeguard is a protected distribution system (PDS) where the distribution medium is protected against electronic or physical intercept, thereby ensuring the confidentiality of the information being transmitted."*

> — DIB SCC CyberAssist, Cybersecurity Maturity Model Certification > Level 2 > SC.L2-3.13.8 Data in Transit, "Discussion [NIST SP 800-171 R2]"  
> Source: https://ndisac.org/dibscc/cyberassist/cybersecurity-maturity-model-certification/level-2/sc-l2-3-13-8/

The enclave's boundary controls (firewall, network segmentation, physical access controls, and access control enforcement) together constitute the alternative physical and logical safeguards that protect CUI from unauthorized disclosure while in transit within the enclave.

### Additional: SC.L2-3.13.8 "Further Discussion" (Chain to SC.L2-3.13.11)

> *"This requirement, SC.L2-3.13.8, requires cryptographic mechanisms be used to prevent the disclosure of CUI in-transit and leverages SC.L2-3.13.11, which specifies that the algorithms used must be FIPS-validated cryptography."*

This reinforces that SC.L2-3.13.11's scope limitation (protected environment exception) flows through to the transmission requirement — if internal transmission is protected by the enclave boundary, FIPS-validated cryptography is not required for that path.

---

## 3. Protected Environment Boundary — [Enclave Name]

### 3.1 Boundary Definition

The **[Enclave Name]** is a logically and physically demarcated protected environment that serves as the covered OSA information system for all CUI processed by [Organization/Unit]. The enclave boundary comprises:

| Boundary Layer | Control(s) Applied |
|---|---|
| **Physical Access** | [Describe: controlled-access facility, badge access, video surveillance, visitor escort] |
| **Network Perimeter** | [Describe: firewall policies, VLAN isolation, no direct internet from app servers] |
| **Access Control** | [Describe: authentication boundary, MFA, Conditional Access, RBAC] |
| **Endpoint Boundary** | [Describe: managed/joined endpoints, endpoint protection, disk encryption] |
| **Logical Segmentation** | [Describe: dedicated VLANs, inter-VLAN routing restrictions] |

### 3.2 Operational Scope

- **All CUI processing, storage, and transmission** by [applications] occurs entirely within this protected boundary.
- No cloud connectivity exists for the on-premises application servers listed in Section 4.
- Remote user access traverses the boundary through FIPS-validated VPN tunnels (see Section 6).
- Email egress and file transfer outbound from the enclave traverse FIPS-validated TLS gateways (see Section 6).

**Conclusion:** The [Enclave Name] satisfies the definition of the "protected environment of the covered OSA information system" as referenced in the DIB SCC SC.L2-3.13.11 Further Discussion, and therefore internal cryptographic operations within the enclave are exempt from the FIPS-validation requirement.

---

## 4. Covered Applications and Servers

*Repeat this table for each application covered by the exemption:*

### 4.1 [Application Name]

| Attribute | Detail |
|---|---|
| **Application** | [Application Name] |
| **Version / Edition** | [Insert version] |
| **Server Count** | [N servers — list roles: App Server, DB Server, Web/Reporting Server] |
| **Server Hostnames** | [hostname-01, hostname-02, ...] |
| **Deployment** | On-premises, wholly within the [Enclave Name] |
| **Cloud Connectivity** | None — [no cloud sync, no SaaS back-end] |
| **CUI Handled** | [Describe CUI types processed] |
| **Cryptography in Use (Internal)** | [Describe internal crypto — e.g., app-layer TLS, DB encryption-at-rest] — these are **not** FIPS-validated (per Section 2 exemption) |
| **Cryptography in Use (Boundary)** | N/A — servers have no direct external connectivity; all external access is mediated through boundary services (Section 6) |

---

## 5. Inter-Application Communication Within the Enclave

### 5.1 [Connector Name / App-to-App Path]

- **Transport:** Internal VLAN-to-VLAN routing within the enclave, subject to firewall rules allowing only specific source/destination IP:port pairs.
- **Protocol:** [e.g., HTTPS/TLS, ODBC/JDBC, REST API over TLS, SMB]
- **Boundary Status:** All packets traverse **only** enclave-internal network segments. No packet leaves the protected environment boundary.
- **FIPS Status:** The encryption used for inter-application data transfer is **not** FIPS-validated. Permitted under SC.L2-3.13.11 exemption.

### 5.2 Certification Statement

> *[Organization] certifies that all inter-application communication between [App A] and [App B] occurs solely within the [Enclave Name] protected environment boundary. No CUI traverses external or untrusted networks during inter-application data exchange. The connector traffic is logically confined to dedicated enclave VLANs with firewall-enforced routing restrictions. Network flow logs are retained for audit verification.*

---

## 6. FIPS-Validated Cryptography at Boundary Egress Points

FIPS-validated cryptography **is** applied at all points where CUI exits the protected environment boundary.

### 6.1 Boundary Egress Point Inventory

| Egress Point | Traffic Type | Cryptographic Protection | FIPS-Validated Module | Certificate / Reference |
|---|---|---|---|---|
| **Remote User Access (VPN)** | All CUI access by remote users | [IPsec/TLS VPN] | [Module name] | [FIPS cert #] |
| **Email (Outbound CUI)** | SMTP to external recipients | TLS 1.2/1.3 FIPS ciphers; S/MIME | [Module name] | [FIPS cert #] |
| **File Transfer (Outbound)** | SFTP/FTPS, external sharing | TLS 1.2/1.3 FIPS ciphers | [Module name] | [FIPS cert #] |
| **Remote Administration** | SSH/RDP from external | SSH with FIPS ciphers / RDP over FIPS TLS | [Module name] | [FIPS cert #] |
| **External API / Web Services** | CUI to external authorized endpoints | TLS 1.2/1.3 FIPS ciphers | [Module name] | [FIPS cert #] |

### 6.2 Certification Statement

> *[Organization] certifies that all CUI transmitted or stored outside the [Enclave Name] protected environment boundary is protected by FIPS-validated cryptographic modules. No CUI leaves the enclave without traversing a boundary egress point under FIPS-validated cryptographic protection.*

---

## 7. Noted Item: FIPS 140-2 Certificate Transition to Historical List — September 21, 2026

### 7.1 Risk Identification

On **September 21, 2026**, the NIST CMVP will move **all remaining active FIPS 140-2 validation certificates to the Historical List**. Effective September 22, 2026, **only FIPS 140-3 validated modules will appear on the CMVP Active List**.

> *"FIPS 140-2 validated modules will remain on the active list through September 21, 2026. On September 22, 2026, only FIPS 140-3 module validations will remain on the active list."*

> — NIST CSRC, Cryptographic Module Validation Program (CMVP), Frequently Asked Questions  
> Source: https://csrc.nist.gov/Projects/cryptographic-module-validation-program/faqs

**Note:** Historical status is NOT revocation. Historical modules remain valid for existing deployments but no longer satisfy procurement or assessment requirements that mandate an *active* certificate.

### 7.2 Impact Assessment

| Impact Area | Assessment |
|---|---|
| **Internal Enclave Applications** | **Minimal / No Impact.** Internal application cryptography is exempt from FIPS validation per Section 2. The FIPS 140-2 → 140-3 transition does not affect the exemption. |
| **Boundary Egress Points** | **Significant — Requires Verification.** All boundary egress cryptographic modules must be confirmed as FIPS 140-3 validated (or have an active FIPS 140-3 certification in process by September 2026). Modules relying solely on FIPS 140-2 certificates will no longer satisfy SC.L2-3.13.11 after the transition date. |
| **CMMC Assessment Timing** | **Directly Relevant if assessment is after September 2026.** At the time of assessment, assessors will expect all boundary egress cryptographic modules to hold active FIPS 140-3 validations, not FIPS 140-2. |

### 7.3 Required Action (POA&M)

1. **Inventory all FIPS-validated modules** currently deployed at boundary egress points and identify which hold FIPS 140-2 vs. FIPS 140-3 certificates.
2. **Contact each vendor** to confirm FIPS 140-3 certification status, timeline, and any required software/firmware updates.
3. **Prioritize replacement or upgrade** of any boundary module that will not achieve FIPS 140-3 validation before September 21, 2026.
4. **Document compensating controls or enduring exceptions** for any boundary module that cannot be transitioned, with risk acceptance signed by the Authorizing Official.
5. **Update this SSP entry** by August 2026 with confirmed FIPS 140-3 certificate numbers for all boundary egress modules.

### 7.4 Risk Acceptance

> *[To be completed by the Authorizing Official / ISSM: Acknowledge the FIPS 140-2 transition risk, document the transition plan, or accept residual risk with compensating controls and a defined review date.]*

---

## 8. Summary of Compliance Posture

| SC.L2-3.13.11 Requirement | How Addressed |
|---|---|
| FIPS-validated cryptography for CUI transmitted **outside** the protected environment | **Satisfied.** All boundary egress points (VPN, email, file transfer, remote admin) employ FIPS-validated cryptographic modules (Section 6). |
| FIPS-validated cryptography for CUI stored **outside** the protected environment | **Satisfied.** No CUI is stored outside the enclave without FIPS-validated encryption (Section 6). |
| Encryption used **within** the protected environment | **Exempt.** Per DIB SCC SC.L2-3.13.11 Further Discussion, internal application encryption is not required to use FIPS-validated modules. |
| Alternative physical safeguards (SC.L2-3.13.8) | **Applied.** The enclave boundary provides physical, logical, and access control protections equivalent to a Protected Distribution System. |
| FIPS 140-2 → 140-3 transition risk | **Noted.** Boundary modules must be transitioned to FIPS 140-3 before September 21, 2026; internal exempt applications are unaffected. |

---

## 9. Evidence and References

| Reference | Description |
|---|---|
| DIB SCC SC.L2-3.13.11 Further Discussion | https://ndisac.org/dibscc/cyberassist/cybersecurity-maturity-model-certification/level-2/sc-l2-3-13-11/ |
| DIB SCC SC.L2-3.13.8 Data in Transit | https://ndisac.org/dibscc/cyberassist/cybersecurity-maturity-model-certification/level-2/sc-l2-3-13-8/ |
| NIST CMVP FAQ — FIPS 140-2 Historical Transition | https://csrc.nist.gov/Projects/cryptographic-module-validation-program/faqs |
| CMMC Level 2 Assessment Guide | https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf |
| NIST SP 800-171 Rev 2 | Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations |
| Enclave Network Diagram | [Insert reference to enclave network architecture diagram] |
| Firewall Rule Set (Enclave VLANs) | [Insert reference to firewall configuration / rule documentation] |
| FIPS Certificate Inventory | [Insert reference to FIPS module inventory spreadsheet] |

---

## 10. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| **ISSM / Security Manager** | [Insert] | | |
| **System Owner** | [Insert] | | |
| **Authorizing Official** | [Insert] | | |

---

*This SSP entry is current as of [Insert Date]. It must be reviewed and updated no later than August 2026 to confirm FIPS 140-3 transition status for all boundary egress cryptographic modules, and again prior to the CMMC Level 2 assessment.*