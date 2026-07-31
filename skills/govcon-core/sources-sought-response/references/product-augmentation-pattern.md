# Product Augmentation Pattern for Management Consulting PWS

## When It Applies

The PWS defines a management consulting engagement (NAICS 541611, PSC R408) with specialist roles, deliverables, and operational governance. The agency already runs Microsoft 365 E5 and has existing VMO/SAM tooling. AI automation is mentioned in the PWS Additional Requirements.

## The Pattern: Augment, Don't Replace

The ground-up replacement failure mode: "We'll build you a VMO product from scratch" — ignores existing application, creates vendor lock-in, triggers EPLC without acknowledgment.

The valid augmentation pattern: "We'll build you a Teams-integrated analytics layer on top of your existing VMO tools."

### Three Rules

1. **Do NOT claim to maintain or administer a system you don't understand.** Never say "we will maintain your existing [X] application" when you don't know what [X] is — a SharePoint site? A ServiceNow module? A Flexera deployment? An Access database? If the KO asks about it and you have no answer, credibility evaporates. Instead, use honest framing: "we administer the current VMO application and site per PWS requirements" or "we ingest data from whatever VMO tooling HHS currently operates." This acknowledges the requirement without pretending you know the system.

2. Frame as full VMO operations support (~80%) + modernized tooling (~20%), not product-only. Lead with management consulting functions the PWS prioritizes.

3. Acknowledge the compliance path: "Custom code undergoes standard EPLC security review within the existing M365 compliance boundary. No separate FedRAMP ATO needed — inherits tenant authorization."

### Technical Architecture

- Surface: SharePoint Framework (SPFx) web parts as Teams tab applications
- Back-end: Power Platform (Power Apps, Power Automate, Dataverse)
- Analytics: Power BI dashboards
- Auth: Microsoft Graph API + existing PIV/HSPD-12
- Storage: SharePoint document libraries with version control
- Compliance: Inherits tenant FIPS 199, NIST 800-53, and existing ATO

### Differentiator Language

"We have built this kind of product before." — Cite DAF DTO SBIR Phase I (W519TC25P0046) with third-party verification (OrangeSlices AI, Defense TechConnect).

### Team Role Pivot

Amyn shifts from "Technical Lead doing consulting" to "Product Lead, VMO Platform."
