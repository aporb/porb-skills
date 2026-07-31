# Section 889 Scope Analysis — Non-Telecom Equipment

## The Canonical Question

> "Does a [non-telecom device / non-connected item / office supply] need to be Section 889 compliant?"

The answer is almost always **NO** — but the reasoning path matters, and the edge cases matter more.

## FAR Source

- **Definition of covered telecommunications equipment or services**: FAR 4.2101 (identical text also in FAR 52.204-25)
- **Prohibition**: FAR 4.2102
- **Exceptions**: FAR 4.2102(b)
- **Clause text**: FAR 52.204-25 (inserted in all solicitations and contracts per 4.2105(b))

## Scope Analysis Decision Tree

### Step 1: Is the equipment "telecommunications equipment"?

The FAR does not define "telecommunications equipment" separately — but the definition at FAR 4.2101 lists *specific entities and categories*:

1. Telecommunications equipment produced by **Huawei** or **ZTE** (or subsidiaries/affiliates)
2. Video surveillance and telecommunications equipment from **Hytera**, **Hikvision**, or **Dahua** (for public safety/security/critical infrastructure)
3. Telecommunications or video surveillance services from such entities
4. Equipment/services from entities the SoD believes are PRC-owned/controlled

**Test**: Does the item provide voice, data, or video transmission over a network? If NO (motorized blade box, lighting fixture, desk, chair, filing cabinet, hand tool), it's not covered equipment. **Skip to Step 4.**

If YES (router, switch, camera, VoIP phone, cellular modem, IoT sensor with network capability), proceed.

### Step 2: Is it used as a "substantial or essential component" or "critical technology"?

If the item is telecommunications equipment (Step 1 = YES), does it contain covered telecom components as a substantial or essential part of its function? The standard is:

> *"Substantial or essential component* means any *component* necessary for the proper function or performance of a piece of equipment, system, or service." (FAR 4.2101)

**Test**: Does the item incorporate a Huawei or ZTE chip/component that is *necessary* for it to function? A generic microcontroller or off-the-shelf IC from a non-covered Chinese fab is NOT covered telecom equipment. Only components that ARE themselves covered telecom equipment trigger this.

### Step 3: Exceptions

Even if Steps 1-2 flag it, there are exceptions:

- Service that connects to third-party facilities (backhaul, roaming, interconnection)
- Telecommunications equipment that **cannot route or redirect user data traffic** or **permit visibility into any user data or packets** (FAR 4.2102(b)(2))

### Step 4 (the usual answer): Not covered, no further action needed

For devices that:
- Have **no network connectivity** (no Wi-Fi, Bluetooth, Ethernet, cellular, Zigbee, Z-Wave, LoRa, or any other communications interface)
- Are **not video surveillance devices**
- Do not **process, store, or transmit telecommunications or video data**

**Verdict**: Categorically outside Section 889 scope. No representation, waiver, or further analysis required.

## Edge Cases That Cross the Line

| Equipment | Analysis | Verdict |
|---|---|---|
| "Smart" shredder with Wi-Fi for usage tracking or auto-reorder | Connects to network; may incorporate covered telecom component | **FLAG** — needs Step 2-3 analysis |
| Network-connected printer (even next to the shredder) | Telecommunications/video? No, but it has network connectivity | **NOT covered** (printer is not telecom/video equipment) — but Hikvision or Dahua cameras *in* the printer would be. |
| IoT-connected office appliance | If it uses cellular/NB-IoT for telemetry | **MAYBE** — depends on chipset and manufacturer |
| Door access control system with IP connectivity | Access control, not telecom/video surveillance | **NOT covered** unless using covered camera equipment |
| Traditional landline phone | Telecommunications equipment | **YES — must verify** manufacturer is not Huawei/ZTE |

## Practical Guidance

- **Don't over-apply Section 889.** It targets a specific list of Chinese telecom and video surveillance entities. It is NOT a general "Chinese-made goods ban." The FAR explicitly limited scope to telecommunications and video surveillance.
- **Do check for IoT/smart capability.** A "traditional" device with IoT features added (e.g., Fellowes AutoMax with Wi-Fi) crosses the analysis boundary. If the device can phone home, it's worth a Step 2 check.
- **Representation language** (FAR 52.204-26) asks about "covered telecommunications equipment or services" — not about Chinese-origin goods generally. A shredder made in China from generic components is not covered telecom equipment.
- **For enclave environments**, the security concern is different from the procurement compliance concern. NSA/CSS 02-01 and NISPOM destruction standards set technical specifications (cross-cut, particle size) — these are orthogonal to Section 889. A shredder must satisfy BOTH: (a) meets the destruction standard for the material handled in that enclave, and (b) complies with the procurement requirements of the contract vehicle used to buy it.

## References

- FAR 4.2101 (definitions): https://www.acquisition.gov/far/4.2101
- FAR 4.2102 (prohibition): https://www.acquisition.gov/far/4.2102
- FAR 52.204-25 (clause text): https://www.acquisition.gov/far/52.204-25
- FAR 52.204-26 (representation): https://www.acquisition.gov/far/52.204-26
- FAR Subpart 4.21: https://www.acquisition.gov/far/subpart-4.21
