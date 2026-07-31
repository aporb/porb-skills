# CUI Incident Reporting — Aecon FBU

## Executive Summary

When employees mishandle CUI or need to report security incidents, they should **report directly to Amyn (CICS)** as the first point of contact. This is correct and defensible — Amyn holds R/A (Responsible/Accountable) for ALL security domains in the FBU RACI matrix.

However, the process is incomplete above Amyn. There's **no documented escalation chain** and **no designated officer for the DIBNet filing** required by DFARS 252.204-7012.

## What the Research Found

### 1. Amyn is the right first point of contact
- Amyn's RACI entry shows R/A on all security domains — the only manager with both
- Aecon FBU doesn't have a CISO, ISSM, or SSO for this enclave — Amyn is functionally all three
- For a mid-size defense contractor, the compliance lead as SPOC is standard practice

### 2. Amyn does NOT make the 72-hour DoD notification
- DFARS 252.204-7012 requires the contractor to report via DIBNet within 72 hours
- The IRP template (`Incident-Response-Plan.md`, §8.2) assigns this to the "Federal Compliance Project Director"
- This maps to **Douglas Henderson** (FCD role) — a director-level obligation
- This is a corporate officer requirement, not an individual contributor's task

### 3. The IRP template defines a full escalation chain (but it's unfilled)
```
Level 1: Incident detected (employee reports)
Level 2: IR Coordinator (Sr Cybersecurity Analyst) — technical triage
Level 3: IR Team Lead (Sr Manager GRC) — coordination, decision authority
Level 4: Executive Leadership (CIO, COO, General Counsel)
Level 5: Board (significant impact only)
```

External reporting (IRP §10): DIBNet (DoD), C3PAO, CISA, FBI/IC3, state AG (if PII). The IR Team Lead and Federal Compliance Project Director jointly own external notifications.

### 4. THERE IS NO ESTABLISHED IR PROCESS YET
- The readiness scorecard flags: "No incident response plan for the Charlotte/Sentinel enclave exists… The 72-hour DFARS 7012 reporting requirement has no process owner."
- The IRP template is unfilled — all contacts are `[INSERT]`
- IR is scored "Not Started"
- Amyn's job description includes "Crisis management for breaches" — confirming this is his to build

### 5. NIST SP 800-171 §3.6.2 requires reporting to "designated officials"
- The control states: "Track, document, and report incidents to designated officials and/or authorities both internal and external."
- The "designated officials" are defined by the contractor's own IRP
- The SSP template (§3.6.2) leaves this as `[INSERT ROLE]` — the org must explicitly name them
- Right now, nobody is named except Amyn (via the cheat sheet, informally)

## What the Incident Reporting Structure SHOULD Be

| Step | Who | Action |
|------|-----|--------|
| 1. Employee detects incident | Any employee | Report immediately to **Amyn (CICS)** — this is the single point of contact. Also acceptable: IT helpdesk (Olivia/Joe) who escalates to Amyn. |
| 2. Triage & investigation | Amyn (CICS) + IR Coordinator (if assigned) | Assess severity, preserve evidence, document. |
| 3. Escalate to senior authority | Amyn → **Douglas Henderson (FCD)** or Brian Gregorio | Decision on whether DFARS 72-hour clock is triggered. |
| 4. DoD notification (if CUI/CDI breach) | **Douglas/Brian (director-level)** via DIBNet | Within 72 hours of discovery. Also notify DoD Contracting Officer + C3PAO. |
| 5. External notifications | IR Team Lead / Legal | CISA, FBI/IC3 as applicable. |

## Key Takeaways

- **Employees reporting to Amyn is the right first step.** The cheat sheet instruction "Report to Amyn Porbanderwala" is correct for the employee-facing step.

- **The gap is above Amyn, not at Amyn.** There's no documented escalation and no designated DIBNet filing officer.

- **This is an IRP gap, not a cheat sheet gap.** The cheat sheet correctly directs employees. The missing piece is what happens after the report — that belongs in the IRP template.

- **Amyn's call on timing.** Whether to build out the IRP now or defer to the CMMC L2 timeline (Nov 2026) is a strategic decision. The current state (IRP unfilled, readiness scorecard "Not Started") is documented and visible to leadership.

## References

- `Incident-Response-Plan.md` — IRP template with escalation chain (unfilled)
- `SSP-Template.md` — §3.6.1–3.6.3 IR controls (unfilled)
- `deliverables/enclave-readiness-scorecard.html` — IR = "Not Started"
- `deliverables/aecon-org-structure-map.html` — reporting chain / RACI
- DFARS 252.204-7012 clause — 72-hour notification requirement