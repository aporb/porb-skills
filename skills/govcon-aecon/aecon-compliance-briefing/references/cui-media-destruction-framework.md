# CUI Media Destruction Framework — Regulatory & Procurement Guidance

**Source session:** July 22, 2026 — SRS Secure Document Destruction Briefing
**Authoritative briefing:** `aecon-srs-shredder-compliance.html` in Nextcloud briefings

## Governing Controls

| Control | NIST SP 800-171 Rev 2 | CMMC Level 2 |
|---------|----------------------|--------------|
| Sanitize/destroy media containing CUI before disposal | 3.8.3 — references NIST SP 800-88 | MP.L2-3.8.6 |
| Control access to CUI on media to be destroyed | 3.8.4 | MP.L2-3.8.7 |
| Implement cryptographic sanitization or physical destruction | 3.8.5 | MP.L2-3.8.8 |

All three controls are assessed during CMMC Level 2. CUI destruction applies to paper and digital media.

## NIST SP 800-88 Rev 2 (September 2025) — Current Standard

Rev 1 was withdrawn September 26, 2025. Rev 2 shifts from hands-on sanitization guidance to program-focused guidelines. Paper destruction specs remain the same as Rev 1:

| Method | Specification | Source |
|--------|-------------|--------|
| Cross-cut shredding (single-step) | Particles ≤ 1mm × 5mm (0.04in × 0.2in) | NIST SP 800-88 Rev 2, Table A-1 |
| Pulverize/disintegrate | 3/32in (2.4mm) security screen | NIST SP 800-88 Rev 2 |
| Multi-step (shred + recycle/destroy) | Permitted alternative; CUI must be "unreadable, indecipherable, and irrecoverable" | CUI Notice 2019-03; 32 CFR 2002.14(f)(2) |
| Burn method | Residue reduced to white ash | NIST SP 800-88 |

## NSA Evaluated Products List (EPL) — Paper Shredders

The NSA EPL is the authoritative source for compliant equipment. Shredders on this list have been tested to meet CUI/classified destruction specs.

URL: https://www.nsa.gov/resources/everyone/media-destruction/

Key data per listing: manufacturer, model, NSA EPL number, particle size specification.

## CUI Notice 2019-03 — Multi-Step Destruction

- Agencies may use multi-step destruction as a permitted alternative
- First step: shred (does NOT need to meet 1mm × 5mm single-step standard)
- Subsequent step: recycle into new paper OR destroy via certified contractor
- Process must render CUI unreadable, indecipherable, and irrecoverable
- **Must be verified and found satisfactory by the organization**
- Recycling processes that convert paper into other products (e.g., cardboard) do NOT always meet this standard

## Outsourced Destruction — Service Provider Verification

When using a third-party destruction vendor (e.g., via Fluor at SRS):

Required SSP documentation:
1. Service provider name and contact
2. Verification that process meets NIST SP 800-88 Rev 2
3. Chain of custody from locked bin to destruction
4. Certificate of Destruction (CoD) process and sample
5. Frequency of pickup
6. Contract/service agreement references
7. Right-to-audit clause for CMMC assessment

## Section 889 — Application to Non-Telecom Hardware

Understanding Section 889 scope for office equipment:

| Equipment Type | Section 889 Applies? | Rationale |
|---------------|---------------------|-----------|
| Basic mechanical shredder (no network) | **No** | Not telecommunications or video surveillance equipment |
| "Smart" shredder with WiFi/BLE/camera | **Maybe** — if from prohibited manufacturer | Has network capability; data exfiltration or remote command risk |
| Shredder with cloud-based usage tracking | **Maybe** — assess manufacturer and data path | Cloud connectivity creates supply chain risk |
| Shredder manufacturer on 889 list (Huawei, ZTE, Hikvision, Dahua, Hytera) | **Yes** — any product from these entities | Prohibited regardless of product type |

**Recommendation:** For CUI destruction in an enclave, select a non-networked ("dumb") shredder with no WiFi/BLE/Ethernet/camera. Verify manufacturer is not on the Section 889 prohibited list.

## TAA — Country of Origin for Destruction Equipment

The Trade Agreements Act (19 U.S.C. §§ 2501–2581) requires federal contractors to purchase products manufactured in the US or a TAA-designated country. China, Russia, India, Malaysia, Thailand are excluded.

TAA-compliant shredder manufacturers:
- HSM (Germany) — many models on NSA EPL
- Dahle (Germany) — select industrial models
- IDEAL (Germany) — cross-cut models
- Fellowes (USA) — select models; verify SKU-level origin

Non-compliant: most budget/consumer shredders manufactured in China.

## Supply Chain Risk Assessment for Enclave Hardware

Before procuring any physical device for a CMMC enclave, assess:

1. Manufacturer country of origin
2. Component sourcing (motor, controller, PCB from prohibited country?)
3. Network connectivity: WiFi/BLE/Ethernet present? If so, from which manufacturer?
4. Data storage: Does device have memory that could store CUI metadata or images?
5. Firmware update mechanism: Can device receive updates from a foreign server?
6. IoT/cloud features: Usage tracking, app pairing, auto-detect, user logging?

For CUI enclaves, select devices with no smart features, no network connectivity, and no cloud services. A "dumb" device has no attack surface.

## DOE/Site-Specific Considerations (e.g., Savannah River Site)

When the enclave is located at a DOE facility (e.g., Savannah River Site managed by Fluor):
- The site M&O (Management & Operations) contractor's existing processes may already satisfy CUI destruction — but must be independently verified for SSP documentation
- DOE Order 470.4B (Safeguards and Security Program) may add requirements above CMMC baseline
- Coordinate with site security before introducing new destruction equipment
- Existing locked-bin + third-party destruction may be pre-approved by DOE — leverage this if documentation is available

## Media Destruction Log Template

Required evidence artifact for CMMC assessors:

| Field | Description |
|-------|-------------|
| Date | Date of destruction |
| Document description | Type/ID of destroyed material |
| CUI category | Applicable CUI category |
| Destruction method | Shredder make/model, or vendor name |
| Performing person | Name of person who witnessed/destroyed |
| Certificate of Destruction # | If outsourced, reference CoD number |
| Notes | Any exceptions or special circumstances |

Store in enclave tracking system. Retain for minimum 3 years (per FAR record retention requirements).

## Key Regulatory References

- **32 CFR 2002.14(f)(2):** CUI must be destroyed "in a manner that makes it unreadable, indecipherable, and irrecoverable"
- **CUI Notice 2019-03:** Multi-step destruction guidance; single-step cross-cut to 1mm × 5mm
- **NIST SP 800-88 Rev 2 (September 2025):** Current media sanitization standard
- **NIST SP 800-171 Rev 2:** Controls 3.8.3, 3.8.4, 3.8.5
- **Section 889, NDAA FY 2019:** FAR 52.204-24/25/26
- **Trade Agreements Act (19 U.S.C. §§ 2501–2581):** FAR 52.225-5/6
- **DOE O 470.4B:** Safeguards and Security Program
