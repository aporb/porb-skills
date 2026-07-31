# FedRAMP Moderate SaaS Landscape — Construction + Adjacent
## Research Date: July 21, 2026

Comprehensive catalog of FedRAMP Moderate construction and construction-adjacent SaaS products, parent company movement, and equivalency candidates with 3PAO/SOC 2 evidence. Use as quick-reference when evaluating CSP options for federal construction contracts.

## Quick-Reference Table: Key Products

| Product | Vendor | FedRAMP ID | Status | Level | Category |
|---------|--------|-----------|--------|-------|----------|
| Autodesk for Government (AFG) | Autodesk | FR2226322745 | FedRAMP Certified | Moderate | BIM/Docs/Field/PM/Takeoff |
| Oracle Primavera Cloud for Gov | Oracle | FR2534673267 | Agency Auth In Process | Moderate | CPM Scheduling/Controls |
| ArcGIS Online (AGO) | ESRI | FR1811073663A | FedRAMP Certified | Moderate | GIS/Mapping/Analytics |
| Esri Managed Cloud Services Adv+ | ESRI | F1311252651 | FedRAMP Certified | Moderate | GIS Managed Hosting |
| DocuSign Federal (eSignature) | DocuSign | F1609267945 | Agency Authorized | Moderate + DoD IL4 | E-Signature |
| DocuSign CLM | DocuSign | F1609267945 | Agency Authorized | Moderate + DoD IL4 | Contract Lifecycle |
| Box Government Cloud | Box | F1212191840A | FedRAMP High | High | Document Management |
| Procore for Government | Procore | FR2516365096 | JAB | Moderate | Construction PM |

## Parent Company FedRAMP Movement

| Company | FedRAMP | GovRAMP | SOC 2 | ISO 27001 | CMMC | Notes |
|---------|---------|---------|-------|-----------|------|-------|
| Autodesk | ✅ Moderate (AFG) | — | ✅ | ✅ | — | Desktop tools NOT covered |
| Oracle | 🔄 In Process (Primavera) | — | ✅ | ✅ | — | First CPM SaaS in pipeline |
| Trimble | ❌ No | ✅ | ✅ Type 2 | ✅ 27001:2022 | ✅ Certified | NIST 800-171 Rev 2 |
| Bentley | ❌ No | — | ❌ Not found | ❌ Not found | — | DPF only |
| Hexagon | ❌ Unreachable | — | — | — | — | Trust page blocked |
| Topcon | ❌ Not checked | — | — | — | — | No evidence |

## Equivalency Candidates

### InEight (Strongest Case)
- **3PAO:** A-LIGN assessed, FedRAMP Ready at Moderate Equivalency
- **SOC 2 Type II:** Since 2019, recertified 2025 (3rd 3-year cycle)
- **SOC 1 Type II:** Yes
- **ISO 27001:2022, ISO 27701:2019, ISO 9001:2015:** All certified
- **Pen testing:** Annual third-party + regular internal
- **Hosting:** Microsoft Azure, customer-chosen region
- **Products:** Document, Schedule, Estimate, Control, Compliance, Model, Contract, Change
- **Evidence:** https://ineight.com/fedramp/ ; https://ineight.com/company/security/

### Trimble Viewpoint/e-Builder
- **FedRAMP:** e-Builder was previously DoE Authorized — not on current Marketplace
- **GovRAMP:** Certified
- **TX-RAMP:** Certified
- **CMMC:** Certified
- **SOC 2 Type II:** Yes
- **ISO 27001:2022:** Yes
- **NIST 800-171 Rev 2:** Compliant
- **Pen testing:** Bugcrowd VDP program
- **Evidence:** https://trust.trimble.com/ (SafeBase portal)

## Category Coverage Map

| Category | FedRAMP Available? | Products | Gap? |
|----------|-------------------|----------|------|
| E-Signature | ✅ | DocuSign Federal (FedRAMP + IL4) | — |
| GIS/Mapping | ✅ | Esri ArcGIS Online, Esri MC Services | — |
| BI/Analytics | ✅ (via Azure) | Power BI (Azure Gov/M365 GCC High) | — |
| Document Mgmt | ✅ | Box Gov (High), SharePoint (GCC High) | — |
| BIM/Digital Twin | ✅ PARTIAL | Autodesk AFG | Desktop tools gap |
| CPM Scheduling | 🔄 IN PROCESS | Oracle Primavera Cloud for Gov | Not yet authorized |
| Field Management | ✅ PARTIAL | Autodesk Build (AFG), InEight (equiv) | — |
| Estimating/Takeoff | ❌ | Autodesk Takeoff (AFG part), InEight Estimate (equiv) | — |
| Drone Data | ❌ | No DroneDeploy/Skyward on Marketplace | MAJOR GAP |
| Safety Mgmt | ⚠️ PARTIAL | InEight Compliance (equiv) | No FedRAMP |
| Cost Control | ⚠️ PARTIAL | Autodesk Build Cost (AFG), InEight Control (equiv) | — |
| Communication | ✅ | MS Teams (GCC High), Webex (FedRAMP) | — |

## Research Methodology

FedRAMP Marketplace data extracted via curl + regex on embedded SSR JavaScript state. Vendor trust pages extracted via web_extract and direct curl. web_search returned empty for all queries — pivoted to direct URL extraction. Firecrawl MCP was unreachable.

## Marketplace Note

The FedRAMP Marketplace lists 18 products under "Construction" business category. Only ~5-7 are "true" construction project management SaaS — the rest are broad platforms cross-categorized (ERP, GIS, collaboration, infrastructure management).