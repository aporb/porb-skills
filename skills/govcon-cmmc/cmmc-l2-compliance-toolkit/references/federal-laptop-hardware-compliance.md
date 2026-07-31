# Federal Laptop Hardware Compliance — Quick Reference

> Condensed from full research at `/home/amyn/federal-laptop-hardware-compliance-research.md`
> Last updated: July 2026

## The One-Paragraph Answer

For CMMC L2 / NIST 800-171 / DOD IL-4: procure **Secured-core certified laptops** (Dell Latitude 7000/5000, HP EliteBook 800/1000, Lenovo ThinkPad T/X series) with **TPM 2.0 (FIPS 140-2 validated)**, **Windows 11 Enterprise**, manage via **Intune/Autopilot in GCC High**, apply **Windows 11 STIG v2r8**, and verify **EPEAT Gold + Energy Star** at procurement time. That single sentence satisfies every framework below.

---

## Framework-by-Framework Requirements

### CMMC Level 2 (32 CFR Part 170)
- **SC.L2-3.13.11**: FIPS-validated cryptography → TPM 2.0 (FIPS 140-2) + BitLocker (AES-256)
- **SC.L2-3.13.8**: Encryption at rest and in transit → BitLocker with TPM+PIN
- **SC.L2-3.05.03**: MFA → Windows Hello for Business (TPM-backed) or CAC/PIV
- **SC.L2-3.01.18**: Mobile device encryption → full-disk BitLocker on all laptops
- **No separate "CMMC hardware list" exists** — compliance flows from NIST 800-171 controls

### NIST SP 800-171 Rev 3 (May 2024)
Key endpoint-relevant controls (confirmed via NIST HTML extraction July 2026):
| Control | Title | Hardware Implication |
|---------|-------|---------------------|
| 03.13.11 | Cryptographic Protection | FIPS-validated TPM; references FIPS 140-3 |
| 03.13.08 | Transmission & Storage Confidentiality | BitLocker for CUI at rest; TLS/IPsec in transit |
| 03.13.10 | Key Management | TPM secure key storage |
| 03.05.03 | MFA | TPM-backed Windows Hello or hardware token |
| 03.05.02 | Device Auth | 802.1X with EAP-TLS; device certs in TPM |
| 03.05.04 | Replay-Resistant Auth | TPM-based challenge-response |
| 03.01.18 | Mobile Device Controls | Full-device encryption for portable CUI |
| 03.14.01 | Flaw Remediation | Firmware updates within defined time period |

Rev 3 aligned with SP 800-53 Rev 5 moderate baseline. FIPS 140-3 transition underway (from 140-2).

### DOD Impact Levels (CC SRG v1r4)
| Level | Data | Key Endpoint Requirement |
|-------|------|------------------------|
| IL-2 | Non-CUI | Standard security |
| **IL-4** | **CUI (Aecon's level)** | **CAC/PIV reader, TPM 2.0 FIPS-validated, BitLocker TPM+PIN, Windows 11 STIG, EDR** |
| IL-5 | Higher-sensitivity CUI / NSS | IL-4 + TEMPEST, NIAP VPN, dedicated facilities |

### DISA STIG — Windows 11
- **Current**: Windows 11 STIG v2r8 (July 10, 2026); SCAP Benchmark v2r9
- **~250 settings**: Secure Boot ON, TPM 2.0, Credential Guard, HVCI, FIPS mode, audit logging, disabled SMBv1/TLS 1.0/LLMNR/NetBIOS
- **Deployment**: Intune policy packs (July 2026), GPO backups, Chef, SCCM baselines
- **STIG > NIST 800-171**: STIG compliance exceeds NIST 800-171 requirements — adopt as safe harbor
- DISA does NOT distribute pre-hardened OS images; STIG is applied post-install

### FedRAMP
- Does NOT directly regulate endpoints — covers cloud services
- Endpoints connecting to GCC High (FedRAMP High) fall under **customer responsibility matrix**
- Equivalent controls required on laptops: FIPS crypto, MFA, encryption, logging

### Management Platform
- **Intune + Autopilot** (GCC High): Policy-driven compliance, device attestation, Conditional Access
- **OEM tools** (Dell Command | Configure, HP Manageability Kit): BIOS config, firmware lifecycle
- Intune compliance policies provide evidence for controls 3.1.18, 3.13.8, 3.14.1, 3.5.2

---

## Minimum Laptop Hardware Spec

| Category | Requirement |
|----------|------------|
| TPM | 2.0, FIPS 140-2 validated, TCG-compliant |
| CPU | Intel 12th-gen+ / AMD Ryzen 6000+ / Snapdragon X |
| RAM | 16 GB minimum (VBS/Credential Guard overhead) |
| Storage | NVMe SSD, 256 GB+ |
| BIOS | UEFI 2.7+, Secure Boot enabled, CSM/legacy disabled |
| Smart Card | Contact + contactless CAC/PIV reader |
| Biometric | Windows Hello IR camera or fingerprint |
| Wi-Fi | Wi-Fi 6E/7, WPA3-Enterprise |
| Security chip | TPM 2.0 or Microsoft Pluton |
| DMA Protection | Kernel DMA Protection (Thunderbolt 4) |

### Preferred Models
- Dell Latitude 7450 / 5550 (Secured-core, EPEAT Gold, FIPS TPM)
- HP EliteBook 840 G11 / 1040 G11 (Sure Start BIOS, EPEAT Gold)
- Lenovo ThinkPad T14s Gen 5 / X1 Carbon Gen 12 (ThinkShield, EPEAT Gold)
- Microsoft Surface Laptop 7 for Business (Pluton, Secured-core)

---

## Environmental / Sustainability (FAR 23.1, EO 14057)

| Certification | Requirement |
|--------------|-------------|
| **EPEAT** | Gold preferred, Silver minimum; 95% of federal IT purchases must be EPEAT-registered |
| **Energy Star** | Mandatory for all federal IT equipment; Computers v8.0 specification |
| **TCO Certified** | Accepted alternative; covers social responsibility + environmental |
| **FAR Clause 52.223-23** | Defines sustainable products; references EPA Recommendations |

EPEAT 2.0 criteria cover: Climate Change Mitigation, Sustainable Use of Resources, Chemicals of Concern, Responsible Supply Chains. Verify registration at www.epeat.net.

---

## Deployment Stack (Build Order)

1. **Firmware**: Secure Boot ON, TPM 2.0 active, DMA Protection, BIOS password, USB boot disabled
2. **OS**: Windows 11 Enterprise, BitLocker (TPM+PIN), Credential Guard, HVCI
3. **Management**: Intune-enrolled via Autopilot, compliance policies aligned to NIST 800-171
4. **STIG**: Windows 11 STIG v2r8 via Intune policy / GPO
5. **EDR**: Microsoft Defender for Endpoint P2 (or DoD-approved equivalent)
6. **MFA**: Windows Hello for Business (TPM-backed) + CAC/PIV

---

## Key Sources

- NIST SP 800-171 Rev 3: https://doi.org/10.6028/NIST.SP.800-171r3
- DISA STIGs: https://public.cyber.mil/stigs/downloads/
- FedRAMP: https://www.fedramp.gov/
- EPEAT: https://www.epeat.net/
- EPA EPP: https://www.epa.gov/greenerproducts
- Microsoft TPM Overview: https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/
- EO 14057 (Federal Sustainability Plan): https://www.federalregister.gov/d/2021-27114
