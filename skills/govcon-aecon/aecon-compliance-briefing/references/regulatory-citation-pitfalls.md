# Regulatory Citation Pitfalls — Federal Hardware Compliance

Captured from adversarial review of the federal laptop standard briefing (July 22, 2026). These are the most commonly flagged citation errors in Aecon hardware compliance briefings.

## NIST SP 800-171 Revision (CMMC Context)

**Error:** Citing SP 800-171 Rev 3 as the CMMC L2 basis.

**Correct:** CMMC 2.0 (32 CFR 170, effective Dec 16, 2024) references NIST SP 800-171 **Rev 2**. Rev 3 was published May 2024 but DoD has NOT incorporated it into the CMMC program. Assessment guides, C3PAO procedures, and SPRS scoring all reference Rev 2.

**Fix:** "NIST SP 800-171 Rev 2 (Rev 3 adoption pending separate rulemaking)."

**Severity:** P0 — a C3PAO assessor or knowledgeable federal CO will flag this immediately.

## FAR 52.204-30 Attribution

**Error:** Listing FAR 52.204-30 as a Section 889 clause alongside 52.204-24/25/26.

**Correct:** FAR 52.204-30 is the **Federal Acquisition Supply Chain Security Act (FASCSA)** clause — covers orders issued under FASCSA to exclude or remove covered articles. It is NOT a Section 889 clause.

**Section 889 clauses:**
- 52.204-24 — Representation Regarding Certain Telecommunications and Video Surveillance Services or Equipment
- 52.204-25 — Prohibition on Contracting for Certain Telecommunications and Video Surveillance Services or Equipment
- 52.204-26 — Covered Telecommunications Equipment or Services—Representation

**Severity:** P0 — anyone who works with these clauses catches this immediately.

## Current-State Assumptions

**Error:** Using "is being evaluated" or "pending" language for operational systems whose status can be verified.

**Example:** "Azure Virtual Desktop is being evaluated as the workspace delivery model" when AVD is already deployed.

**Fix:** Verify current-state assumptions with the user or source documents before writing them into a deliverable. If unsure, ask — don't default to "being evaluated."

## TCO for STIG-Hardened Devices

**Error:** Using standard enterprise support costs ($250/3yr) for federal devices.

**Correct:** STIG-hardened devices require 3-5× higher support: $600-1,200/3yr. Include STIG maintenance (quarterly re-application), NIST SP 800-88 secure disposal ($50-100/device), and deployment/provisioning for hardened images ($150-300).

## FIPS Mode as Default

**Error:** Prescribing Windows FIPS AlgorithmPolicy enforcement without noting application compatibility risk.

**Fix:** Always add an operational risk note — FIPS mode breaks .NET and SCHANNEL apps, including construction tools. Require pilot testing before fleet-wide enforcement. Document exceptions with risk acceptance.

## Windows 10 EOL

**Error:** Omitting current-state assessment of Windows 10 devices in hardware standard recommendations.

**Fix:** Windows 10 EOL was October 14, 2025. Any existing Windows 10 devices in a federal fleet are already noncompliant. Include a current-state assessment and migration urgency section.
