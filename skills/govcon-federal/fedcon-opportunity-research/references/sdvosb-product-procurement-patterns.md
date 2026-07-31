# SDVOSB Product Procurement Patterns — Reseller Model, Non-Manufacturer Rule, VAAR 852.219-73

## Overview

When an SDVOSB primes a federal product procurement (software/hardware, not services), the compliance landscape differs fundamentally from services contracting. This reference covers the three interacting rules that govern SDVOSB product procurement: the non-manufacturer rule, the limitations on subcontracting, and the "cost of materials" exclusion — and the practical reseller model that SDVOSBs use at VA.

## The VA SDVOSB SIEM Reseller Model (Proven Pattern)

Multiple SDVOSB primes have successfully sold SIEM products to VA through the reseller model:

| SDVOSB Prime | SIEM Platform | Largest VA Award | Vehicle |
|---|---|---|---|
| ThunderCat Technology | Splunk | $3.25M | NASA SEWP V |
| Four Points Technology | IBM QRadar | $2.59M | NASA SEWP V |
| Merlin International | IBM QRadar | $591K | NASA SEWP V |
| Alvarez LLC | Splunk | $176K | NASA SEWP V / GSA |
| Sterling Computers | Splunk | $51K | NASA SEWP V |
| V3Gate LLC | Splunk | $87K | NASA SEWP V |

**How it works:**
1. SDVOSB becomes an authorized reseller/partner of the SIEM vendor
2. SDVOSB primes the procurement using its GWAC/IDIQ vehicle (typically NASA SEWP or GSA Schedule)
3. The SIEM vendor provides the product (licenses, hardware, support)
4. The SDVOSB adds a markup and handles the procurement paperwork
5. Some SDVOSBs add integration/implementation services as value-add

## The Three Interlocking Rules

### 1. VAAR 852.219-73 — Limitations on Subcontracting

For supply/product contracts, the SDVOSB prime "will not pay more than 50% of the amount paid by the government to the prime for contract performance, **excluding the cost of materials**, to firms that are not VIP-listed SDVOSBs."

**The "cost of materials" exclusion is the key enabler for product resellers.** SIEM software licenses, hardware appliances, and tier-3 vendor support qualify as "cost of materials" — they are EXCLUDED from the 50% calculation. The 50% limit only applies to the value-added portion (services, integration, program management).

**Practical example for a $3M SIEM procurement:**
- SIEM licenses + hardware: $2.2M → "cost of materials" → EXCLUDED
- Implementation services: $500K → subject to 50% limit
- Program management: $300K → performed by SDVOSB prime
- 50% check: can the SDVOSB self-perform at least $250K of the $500K service portion? If yes → compliant.

### 2. 13 CFR 121.406 — Non-Manufacturer Rule

For supply contracts set aside for small businesses, the prime must either:
- **(a)** Be the manufacturer of the product, OR
- **(b)** Supply the product of a **domestic small business manufacturer**, OR
- **(c)** Obtain a **non-manufacturer rule waiver** from SBA (13 CFR 121.406(b)(5))

**The problem for SIEM resellers:** Splunk, IBM, Elastic, and Exabeam are all large businesses — they are NOT domestic small business manufacturers. An SDVOSB reseller cannot satisfy condition (b). They must either:

- **Waiver path:** Request an SBA non-manufacturer rule waiver. SBA may grant a waiver if no small business manufacturer supplies the class of product. Given the established SIEM reseller ecosystem at VA, waivers appear to be obtainable for SIEM products — the existing SDVOSB resellers have navigated this.
- **Software-as-product distinction:** Software licenses may be treated differently from manufactured goods. The non-manufacturer rule was designed for physical products; software licensing may not be a strict "manufacturing" situation. Consult the CO on classification.
- **Mixed contract approach:** If the procurement is classified as predominantly services (NAICS 541519), the non-manufacturer rule may not apply — it applies to supply contracts, not service contracts. The NAICS code drives the rule's applicability.

### 3. 13 CFR 125.6 — Similarly Situated Entities

Only VIP-listed SDVOSBs count as "similarly situated." Any work subcontracted to a non-SDVOSB (including the SIEM vendor) counts toward the 50% limitation. An SDVOSB subcontractor that further subcontracts to a non-SDVOSB — that further subcontract ALSO counts toward the prime's 50% cap.

## Practical Compliance Checklist for SDVOSB Product Resellers

When assessing an SDVOSB product procurement:

- [ ] **NAICS check:** Is the NAICS code for services (541519) or supply? If services, the non-manufacturer rule may not apply. The 50% limit applies to the service portion only.
- [ ] **Cost of materials identification:** What costs qualify as "cost of materials" under VAAR 852.219-73(d)(2)(i)? Software licenses, hardware, vendor support — document these explicitly.
- [ ] **Self-performance calculation:** What services will the SDVOSB self-perform? Must be ≥50% of the service portion (after excluding cost of materials). Program management, integration, training, compliance documentation, AI/ML customization all count.
- [ ] **Non-manufacturer rule waiver:** If the product manufacturer is a large business, has a waiver been obtained or is one available? Check with the CO or SBA PCR.
- [ ] **Teaming disclosure:** The RFI/Sources Sought requires disclosure of all team members, subcontracting percentages, and which PWS requirements will be subcontracted. Be specific — vague teaming disclosures weaken the response.
- [ ] **Vehicle eligibility:** Does the SDVOSB's GWAC/IDIQ vehicle (SEWP, GSA) allow product resale at the required dollar value? Check ceiling and scope.
- [ ] **Vendor partnership:** Is there an active reseller agreement with the SIEM vendor? Can the vendor provide ROM pricing on short notice?
- [ ] **Past performance:** Does the SDVOSB (or a team member) have past performance selling this class of product to federal agencies? Even one relevant contract with agency, POC, dollar value, and contract number is far better than zero.

## RFI Response Pattern for SDVOSB Product Resellers

In the RFI response, the SDVOSB should:

1. **Be explicit about the reseller model:** "As an authorized reseller of [SIEM Vendor], we will supply [Vendor]'s [Product] through our [GWAC/IDIQ vehicle]. The software licenses and hardware appliances constitute cost of materials under VAAR 852.219-73(d)(2)(i). [SDVOSB] will self-perform program management, integration services, compliance documentation, and training — representing [X]% of the service portion."

2. **Disclose team members fully:** Name the SIEM vendor as a subcontractor/teaming partner. Specify what work they perform (product supply, tier-3 support) vs. what the prime performs.

3. **Address the non-manufacturer rule head-on:** Don't avoid it. State: "[SDVOSB] will supply [Vendor]'s product as an authorized reseller. We will work with the Contracting Officer to address any non-manufacturer rule requirements, including waiver if applicable."

4. **Provide ROM with cost-of-materials breakout:** Separate the product costs (licenses, hardware) from service costs. This demonstrates understanding of the compliance framework and helps the CO assess the 50% calculation.

## Red Flags — When NOT to Prime a Product Procurement

- **No vendor partnership exists.** Cannot get ROM pricing from the SIEM vendor. The response will lack credibility.
- **No GWAC/IDIQ vehicle.** Product procurement through open-market solicitations is far harder than through an existing vehicle.
- **No past performance selling this product class.** "We'll figure it out" is not a credible RFI response.
- **Financial capacity concern.** The SDVOSB must float the hardware/software purchase before government payment. A $2M hardware order requires working capital.
- **Established SDVOSB reseller competition.** If ThunderCat, Four Points, or Merlin are also responding, a new entrant without vendor partnership or product-specific past performance is at a severe disadvantage.