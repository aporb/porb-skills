# Aecon Vendor FedRAMP Reviews — Registry

Tracked FedRAMP/CMMC vendor reviews completed for Aecon FCS enclave. Each entry links to the briefing file and key vendor contacts.

## Completed Reviews

### 1. InEight Document (July 2026)
- **Vendor:** InEight Inc.
- **Product:** InEight Document — US Government
- **Status:** FedRAMP Moderate Equivalency (DoD 2023 memo path, not full authorization)
- **3PAO:** A-LIGN (assessment concluded Dec 17, 2025 — all zeros)
- **Infrastructure:** Azure Government (GovCloud-equivalent), multi-tenant
- **Key Contact:** Habie Ng (Aecon-side liaison); Jeff Hoge (Director, Federal Compliance, InEight); Scott Workman (Chief Admin Officer / CISO, InEight)
- **Marketplace:** Listing expired (was FedRAMP Ready, Jun 2025); equivalency never produced a listing
- **Key Issue:** Equivalent to FedRAMP Moderate but not listed on Marketplace; SAR is "Final Draft"
- **Briefing:** `03-research/compliance/ineight-document-fedramp-equivalency-2026-07-10.html` (in aecon-fcs repo)
- **Outcome:** Aecon proceeding with InEight; recommending LOA from A-LIGN + contract language

### 2. Autodesk AFG (July 2026)
- **Vendor:** Autodesk, Inc.
- **Product:** Autodesk for Government (AFG)
- **Status:** Full FedRAMP Moderate Authorization — Government Cloud Community Cloud
- **Marketplace:** Active listing (confirmed by Anthony Renteria)
- **Infrastructure:** AWS commercial regions with tenant isolation (NOT GovCloud)
- **Key Contact:** Anthony Renteria (Industry Strategy, Digital Project Delivery); Amir (Aecon-side Autodesk contact per Cynan); Francesca (handles CRM distribution)
- **Key Issue:** AWS commercial region hosting creates CUI justification gap; SSP/POA&M restricted to Gov ID holders
- **Briefing:** `https://brief.h.porb.dev/aecon-autodesk-fedramp-review-2026-07-28.html`
- **NDA Status:** In progress as of July 28
- **Outcome:** Under review; awaiting NDA execution + CRM release

## Pending / Future

- (none tracked yet)

## Vendor-Specific Contacts

| Vendor | Person | Role | Contact Path | Notes |
|--------|--------|------|-------------|-------|
| Autodesk | Anthony Renteria (he/him) | Industry Strategy, Digital Project Delivery | Email (initial thread via Amyn) | Sent AFG FedRAMP responses; can forward whitepaper |
| Autodesk | Francesca | (CRM distribution) | Via Anthony | Handles CRM release after NDA verification |
| InEight | Jeff Hoge | Director, Federal Compliance | Via Habie Ng | Offered LOA from A-LIGN; engaging FedRAMP PMO for CR26 re-listing |
| InEight | Scott Workman | Chief Admin Officer / CISO | Via Habie Ng | Confirmed Marketplace re-listing is "number one priority" |

## Standard Questions for New Vendor FedRAMP Reviews

1. FedRAMP authorization level (Moderate or High) and authorization date
2. Deployment model (GovCloud, Community Cloud, Commercial + tenant isolation)
3. Specific products covered by the authorization (verify each Aecon uses)
4. SSP/POA&M availability (and if Gov ID restricted)
5. CRM availability (and NDA requirement to access)
6. Last 3PAO assessment date and next due date
7. Continuous monitoring POA&M status (open findings?)
8. DoD customer references (if any)
9. CMMC tracking (vendor tracks it? or Aecon must self-map)
10. CR26 transition plan (pipeline? date?)
11. Letter of Attestation availability
12. Whitepaper / technical documentation available without NDA
