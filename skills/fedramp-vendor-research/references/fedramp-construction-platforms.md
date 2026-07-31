# FedRAMP-Authorized Construction Platforms (Updated July 2026)

Condensed reference of FedRAMP-authorized construction software. Use when evaluating tools for federal construction contracts subject to CMMC L2 / DFARS 7012. Last updated with Procore for Government authorization and Deltek Costpoint GCCM.

> **Source:** FedRAMP Marketplace (marketplace.fedramp.gov), vendor press releases, and direct vendor documentation. Verified July 2026.

## FedRAMP Authorized / Certified Construction Platforms

| Platform | FedRAMP Status | Marketplace ID | Hosting | Primary Purpose | Notes |
|---|---|---|---|---|---|
| **Procore for Government** | FedRAMP Moderate Authorized (Jan 2026) | FR2516365096 | AWS GovCloud (US) | Full construction PM: Project Mgmt, BIM, Financials, Bid Mgmt, Quality & Safety, Analytics | Most comprehensive FedRAMP construction platform. Logically isolated government-only environment. Supports CMMC L2. Limited app marketplace vs commercial Procore. |
| **Deltek Costpoint GCCM** | FedRAMP Moderate Equivalency Assessed | FR2405880485 | Deltek cloud | GovCon ERP: project accounting, procurement, labor, compliance (FAR/DFARS/DCAA) | Industry-standard ERP for federal contractors. Covers job costing across FFP/CPFF/T&M. Not construction-specific PM — pairs with Procore/ProjectTeam. |
| **ProjectTeam.com** | FedRAMP Moderate Authorized | Marketplace listed | ProjectTeam cloud | Construction PM: RFIs, submittals, change orders, cost tracking, Gantt, docs, photos | Connected collaboration model (subs work inside compliant boundary). No-code customization. Smaller than Procore but built for federal from scratch. |
| **Kahua** | Authorized & DoD IL2 | Marketplace listed | Kahua cloud | Full lifecycle project tracking for federal GCs | DoD IL2 approved. |
| **e-Builder Enterprise (Trimble)** | Authorized via Dept of Energy | Marketplace listed | Trimble cloud | Capital improvement program delivery for government owners | Government owner/agency focused rather than contractor-focused. |

## NOT FedRAMP Authorized (Critical Gaps)

| Platform | Status | Workaround |
|---|---|---|
| **Autodesk Construction Cloud** (ACC/BIM 360) | **NOT FedRAMP Authorized** | Desktop Revit + Navisworks on CMMC-compliant endpoints. BIM data stays on-prem or in authorized file storage. Procore for Government BIM module is an alternative CDE. |
| **Oracle Primavera P6 Cloud** | **NOT FedRAMP Authorized** | On-prem P6 deployment on compliant infrastructure. P6 files exchanged via authorized channels. InEight Schedule or Procore scheduling as alternatives. |
| **Bluebeam Cloud (Studio)** | **NOT FedRAMP Authorized** | Desktop Bluebeam on compliant endpoints is fine. Keep PDFs within authorized boundary. |
| **Sage 300 CRE / Viewpoint Vista / CMiC** | **NOT FedRAMP Authorized** | On-prem deployment with CUI segregation. For CUI-bearing accounting, use Deltek Costpoint GCCM. |
| **ConstructConnect OST** | No FedRAMP, no SOC 2 | Desktop-only mode with no cloud uploads. |

## Market Gaps (No FedRAMP Solution Exists)

- **Estimating/Takeoff SaaS** — No FedRAMP-authorized estimating platform exists. Desktop workaround only.
- **CPM Scheduling SaaS** — No FedRAMP-authorized scheduling platform with native CPM. P6 is the federal standard but Oracle hasn't pursued FedRAMP for cloud.

## Key Distinction

FedRAMP authorization is not the only path — DFARS 7012(b)(2)(ii)(D) requires cloud providers to meet "security requirements equivalent to those established by the Government for FedRAMP Moderate baseline." A vendor with properly documented FedRAMP Moderate Equivalency (3PAO-assessed) can satisfy this. However, a vendor with NO third-party attestation at all cannot.
