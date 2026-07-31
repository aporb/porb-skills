# Client-Specific Implementation Examples for CMMC L2 Control Matrix

These are the Aecon Federal Services Inc. (AFSI) implementation examples written after the user corrected "the example should be Aecon specific." They cover the most technically significant controls and demonstrate the level of specificity expected.

## Pattern for Writing Examples

Each example should reference:
- **Specific platform/services** by name (GCC High, Entra ID, Intune, Defender, Purview, AVD)
- **Named personnel** (Olivia Baer, Joe Smith, Brian Gregorio, Amyn Porbanderwala, Enzo Zoratto)
- **Specific locations** (Charlotte FCS office, Savannah River Site)
- **Known technical decisions** (USB-only printers, Intune USB block, AVD clipboard disabled)
- **Specific configurations** (policy names, timeout values, threshold numbers)

## Aecon Examples by Control

### AC — Access Control (3.1.x)

```
3.1.1: AFSI GCC High Entra ID limits access to authorized AFSI personnel with DoD CAC/FICAM PIV credentials. Service accounts use Entra ID PIM with JIT elevation. Break-glass accounts monitored via Sentinel, rotated every 72 hours.

3.1.2: AFSI RBAC roles: GCC High Admins (Olivia Baer, Joe Smith), CUI Viewers (project managers, engineers), Compliance Auditors (Brian Gregorio, Amyn Porbanderwala). SharePoint permissions mapped to CUI sensitivity labels.

3.1.3: Purview sensitivity labels with trainable classifiers detect CUI markings. DLP blocks CUI from external share (except Box.com FedRAMP Moderate), USB copy, and unmanaged device download. Conditional access requires Intune-compliant devices for CUI.

3.1.4: Entra ID PIM with separation: admins cannot approve own elevation. AVD disables clipboard/drive mapping to prevent cross-domain transfer. SharePoint separates content creators from approvers.

3.1.5: Entra ID PIM with Global Admin requiring FBU Head approval, max 8-hour elevation. Quarterly access reviews verify continued need. Custom roles for GCC High Mail Admin, SharePoint Admin, Intune Admin.

3.1.16: Intune compliance: Windows 11 22H2+, BitLocker, Defender active/updated, firewall enabled, patched within 30 days. Non-compliant devices blocked from GCC High. Reported monthly.

3.1.20: External CUI sharing: Box.com (FedRAMP Moderate) with encrypted links + expiration; GCC High SharePoint with access requests, 30-day expiry, DLP block on CUI email to unauthorized domains (allow fluor.com, srns.gov, doe.gov only).
```

### IA — Identification and Authentication (3.5.x)

```
3.5.1: All AFSI GCC High users identified via Entra ID with unique UPN. Service accounts identified as srv- prefix with managed credentials in Vaultwarden. Devices identified by Intune enrollment with asset tag.

3.5.2: Multi-factor authentication (MFA) enforced via Microsoft Authenticator or FIDO2 security keys for all GCC High users. Conditional access requires MFA for all cloud app access.

3.5.7: Entra ID password protection with smart lockout (10 attempts), banned password list (top 1000 + custom Aecon-related terms), password expiration 60 days (where still using passwords — MFA primary auth).
```

### SC — System and Communications Protection (3.13.x)

```
3.13.1: Azure Firewall with NSG deny-all-inbound policy. AVD subnet allows only AVD gateway health probes. GCC High tenant isolated from commercial Aecon tenant with no cross-tenant federation.

3.13.8: TLS 1.3 enforced for all Azure AD and Microsoft 365 communications. Weak cipher suites disabled via conditional access and tenant policy. FIPS 140-2 validated crypto required for all GCC High connections.

3.13.16: BitLocker encryption enabled on all AVD session hosts and Intune-managed Windows 11 devices. Recovery keys stored in Entra ID and backed up to GCC High SharePoint protected library.
```

### RA — Risk Assessment (3.11.x)

```
3.11.1: Quarterly risk assessment using NIST SP 800-30 methodology with 5x5 scoring matrix. Risk register in GCC High SharePoint. Vuln scanning via Microsoft Defender for Cloud weekly, authenticated scan quarterly, pen test annually.
```

## General Pattern for Non-Technical Controls

For operational/governance controls (AT, PS, PE, MA, MP), use client context where possible:

```
3.2.1: Annual CUI security awareness training via GCC High SharePoint online modules, completed before accessing CUI systems. Training records in Compliance SharePoint library. Phishing simulations run quarterly via Microsoft Defender for Office 365.
```

## Reference Data Sources for Client Specifics

When building implementation examples for a new client:
1. Onboarding documents (ONBOARDING-SUMMARY.html or equivalent)
2. Transcripts of calls/meetings (00-calls/ directory)
3. Existing analysis documents (ATCP, Enclave Plan, Playbook)
4. Working docs (spec reconciliations, compensating control docs, advisory memos)
5. Technical stack documentation (platform names, FedRAMP levels, versions)
6. Org charts / personnel lists with roles
