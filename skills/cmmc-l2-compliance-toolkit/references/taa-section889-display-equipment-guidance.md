# TAA / Section 889 Guidance for Display Equipment in Federal Enclaves

This reference file captures the legal analysis and equipment guidance produced during the July 2026
Aecon Federal engagement — specifically the question "do TVs in a federal enclave need to be
TAA-compliant when displaying CUI?"

## The Core Distinction

The answer depends on **how the TV receives the CUI signal**, not what's displayed on it.

### Scenario A: HDMI from a laptop running VDI
- TV is purely a pixel renderer — same risk profile as a desktop monitor
- The laptop (VDI endpoint) is the CUI system, not the TV
- TAA/Section 889/NIST 800-171 apply to the laptop, not the TV
- **No compliance concern with the TV itself**

### Scenario B: Network-connected display
- TV receives/processes CUI data over the network
- Smart OS has ACR telemetry that screenshots whatever is on screen and phones home
- TAA, Section 889, and NIST 800-171 all apply

### Scenario C: Both (HDMI + smart features)
- Latent risk regardless of which method is used
- ACR telemetry captures anything on screen regardless of source

## Why Smart TV Differs From Desktop Monitor

| Factor | Desktop Monitor | Smart TV |
|--------|----------------|----------|
| OS | None | Tizen, WebOS, Android TV |
| Network | None | WiFi + Ethernet |
| Telemetry | None | ACR screenshots on-screen content |
| Attack surface | None | Firmware CVEs, app store |
| Section 889 risk | None | Chinese components (TCL, Hisense, Skyworth) |

## Recommended Equipment

TAA-compliant commercial "dumb" displays:
- Samsung WM-N series — TAA (Korea), no smart OS, ~$500-900
- LG US-B series — TAA (Korea), webOS can be disabled, ~$400-800
- Peerless-AV / Sharp — TAA (Mexico/Japan), signage-purpose

To avoid: TCL, Hisense, Skyworth (Chinese, Section 889 risk)

## Three Frameworks

1. TAA (FAR 52.225-5) — Country of origin. Applies if acquired under contract.
2. Section 889 NDAA (FAR 52.204-25) — Prohibits Huawei/ZTE/Hikvision/Dahua components.
3. NIST SP 800-171 — Smart TV ACR = exfiltration risk if CUI displayed.

## Key Citations
- FAR 52.225-5: https://www.acquisition.gov/far/52.225-5
- FAR 52.204-25: https://www.acquisition.gov/far/52.204-25
- FAR Subpart 25.4: https://www.acquisition.gov/far/subpart-25.4
- 19 USC 2501: https://www.law.cornell.edu/uscode/text/19/2501
- 41 USC 182: https://www.law.cornell.edu/uscode/text/41/182
- NIST SP 800-171: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final
