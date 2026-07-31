# InEight Document — FedRAMP Equivalency Research (July 2026)

> Session findings from adversarial review of the InEight Document FedRAMP Equivalency briefing.
> All sources verified live on 2026-07-10.

## Key Findings

### Marketplace Status
- **InEight Document**: NOT on FedRAMP Marketplace. Search returns "Could not find exact match for 'InEight'."
- **InEight Complete Suite**: NOT on Marketplace either (despite earlier briefing claiming it was FedRAMP Moderate authorized)
- **Trimble Unity Construct Government Edition**: ON Marketplace — FedRAMP Certified, Class C (Moderate), Package ID F1603307884
- **Microsoft Azure**: ON Marketplace — FedRAMP High / Class D, multiple authorizations

### InEight's Own Claims
- **Dedicated FedRAMP page**: ineight.com/fedramp/ — uses "FedRAMP Moderate Equivalency Authorization" and "FedRAMP-Authorized Document Control" in page hero. The "Equivalency" qualifier only appears deeper.
- **Security page**: ineight.com/company/security/ — says "our solutions are hosted in Microsoft's Azure Cloud Platform"
- **Jan 8, 2026 press release**: GLOBE NEWSWIRE — states "achieved Federal Risk and Authorization Management Program (FedRAMP®) Moderate Equivalency Authorization"
- **Press release self-contradiction**: Tells readers to "confirm InEight's FedRAMP status in the FedRAMP Marketplace" — but InEight is NOT on the Marketplace as of July 10, 2026

### Regulatory Status

Three authorities produce different answers:

| Authority | Recognition of Equivalency | Source |
|-----------|---------------------------|--------|
| DFARS 252.204-7012(b)(2)(ii)(D) | Requires "security requirements **equivalent to**" FedRAMP Moderate (not "authorization") | Cornell LII / eCFR |
| DoD CIO Dec 21, 2023 Memo | Expliticly recognizes equivalency under conditions (3PAO, zero POA&Ms, annual reassessment, shared BoE) | media.defense.gov (PDF 403'd — unverifiable from primary source) |
| FedRAMP CR26 (Consolidated Rules for 2026) | "FedRAMP does not support or provide 'equivalency.'" Redirects to Department of War | fedramp.gov/2026/ (Cloud Service Providers tab) |

### CR26 Confirmed Quotes

From the CR26 Cloud Service Providers page (verified via browser_console extraction):

> *"FedRAMP does not support or provide 'equivalency.'"*

> *"All questions about 'FedRAMP Equivalency' or the application of FedRAMP Certification requirements for CMMC should be directed to the Department of War."*

> *"FedRAMP will not list products or services that are outside the explicit statutory scope of FedRAMP; services used by private companies to meet other compliance requirements (such as CMMC) that do not also meet one of the above use cases are outside the scope of FedRAMP."*

### Marketplace Terminology Change (RFC-0020)
- "FedRAMP Authorization" → "FedRAMP Certification"
- Impact Levels (Low/Moderate/High) → Classes A-D
- Marketplace banner says "Effective immediately" (verified live)
- Legacy terms shown in parentheses until Dec 31, 2026

### Critical DFARS Misquote Warning
**This is the single most common error** in FedRAMP compliance briefings. The incorrect paraphrase:
> ❌ "FedRAMP authorization at the Moderate or High baseline"

is often substituted for the actual regulatory text:
> ✅ "security requirements **equivalent to** those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline"

The incorrect paraphrase makes DFARS 7012 appear hostile to equivalency. The actual text supports it. Always verify from: `curl -sL -A "Mozilla/5.0" "https://www.law.cornell.edu/cfr/text/48/252.204-7012" | grep -A2 -B2 "equivalent to"`

### Open Questions
1. Does InEight Document actually meet the Dec 2023 DoD CIO memo conditions (specifically zero control-related POA&Ms)?
2. Which agency sponsored the equivalency? Need the actual authorization letter.
3. Is InEight running inside Aecon's GCC High tenant or a separate InEight-managed Azure tenant?
4. Has InEight begun full FedRAMP Certification under CR26?
5. Does the InEight Complete Suite's authorization scope actually exclude the Document module?

### URLs Referenced
- InEight FedRAMP page: https://ineight.com/fedramp/
- InEight Security page: https://www.ineight.com/company/security/
- FedRAMP Marketplace: https://marketplace.fedramp.gov/products/
- CR26 Rules: https://www.fedramp.gov/2026/
- CR26 CSP tab: https://www.fedramp.gov/2026/cloud-service-providers/
- Press release: https://itbusinessnet.com/2026/01/fedramp-authorized-ineight-document-delivers/
- DFARS 7012 (Cornell LII): https://www.law.cornell.edu/cfr/text/48/252.204-7012
- Trimble Unity Construct: Package ID F1603307884
