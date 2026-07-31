# Aecon FBU M365 Environment

Summary of known Aecon Federal Business Unit Microsoft 365 tenant configuration, AI licensing, and compliance environment. **Current as of July 3, 2026.** Verify before making recommendations — tenant state can change.

## Tenant Architecture

| Environment | Type | Status | Purpose |
|-------------|------|--------|---------|
| Commercial M365 Tenant | Standard commercial | Active | Day-to-day FBU operations, Teams, SharePoint, email |
| GCC High Enclave | Government cloud (GCC High) | Live | CUI handling, CMMC L2 compliance boundary |

FBU currently operates primarily in the **commercial tenant**. The GCC High enclave is already stood up but CUI still lives partially in box.com (FedRAMP-authorized) and the enclave (unstructured). The November 2026 task is **configuring FBU SharePoint/Teams inside the existing enclave**, not building it from scratch.

## Copilot / AI Licensing

- **M365 Copilot license status**: Unknown for FBU users as of July 2026
- **M365 Copilot add-on**: ~$30/user/mo (or bundled in Business Premium with Copilot at $32/mo)
- **Copilot Cowork**: GA as of June 16, 2026, but requires M365 Copilot license
- **GCC High Copilot**: Separate "Copilot for US Government" SKU; Copilot Cowork availability in GCC High not yet confirmed
- **Copilot Chat (free tier)**: Available to any M365 account; no work-data grounding; safe for general research

## IT Contact Points

| Person | Role | Tenant Access |
|--------|------|---------------|
| Olivia Baer | IT — GCC High Admin | Commercial + GCC High |
| Joe Smith | IT — GCC High Admin | Commercial + GCC High |

Olivia and Joe are dotted-line to Enzo. They control tenant configuration, license assignment, and GCC High administration.

## Compliance Contacts (for deliverable authoring)

**Important:** All compliance deliverables (cheat sheets, briefings, reports) must list **Amyn Porbanderwala (aporbanderwala@aecon.com)** as the sole contact point. Do NOT list Brian Gregorio or other FBU staff as contacts in user-facing artifacts. Brian's role is listed below for internal understanding only.

| Person | Role | Notes |
|--------|------|-------|
| Amyn Porbanderwala | CICS (Controlled Information Compliance Specialist) | **Sole contact for all deliverables.** aporbanderwala@aecon.com |
| Brian Gregorio | Sr. Director, Federal Compliance | Compliance tool approval authority — internal reference only, never list as contact in deliverables |

## CMMC / Compliance Context

- **Target**: CMMC Level 2 certification by **November 2026**
- **Current CUI storage**: box.com (external, FedRAMP-authorized) + GCC High enclave (unstructured)
- **Key constraint**: Any AI tool processing CUI must operate within the GCC High compliance boundary
- **Audit lead**: Eric Atkinson (Director, Federal Audit)

## Relevant Microsoft SKUs

| SKU | Environment | Includes Copilot? |
|-----|-------------|-------------------|
| M365 Government G5 | GCC / GCC High / DoD | Copilot Chat (free); full Copilot requires add-on |
| M365 Government G3 | GCC / GCC High / DoD | Copilot Chat (free); full Copilot requires add-on |
| M365 Business Premium for GCC-High | GCC High only | Copilot Chat (free); full Copilot requires add-on |
| Copilot for US Government (add-on) | GCC / GCC High | Full M365 Copilot features |

**Cowork availability in Copilot for US Government**: Not verified as of July 2026. Commercial tenant confirmed to support Cowork as of June 16, 2026 GA.

## FBU SharePoint Governance (for reference when discussing Copilot scope)

| Role | Holder | SharePoint Permission |
|------|--------|----------------------|
| Site Owner | Brian Gregorio | Full control, governance approver |
| Co-Owner | Ryan Aragon | Full control, BD content |
| Compliance Officer (day-to-day admin) | Amyn Porbanderwala | Full control, compliance content |

## Key Dates

- **June 29, 2026**: Amyn start date
- **November 2026**: CMMC Level 2 certification deadline
- **June 16, 2026**: Copilot Cowork GA (commercial)
