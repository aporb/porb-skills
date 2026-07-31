# InEight / Trimble FedRAMP Research — July 2026

## InEight Document
- **Status**: FedRAMP Moderate Equivalency Authorization (announced Jan 8, 2026)
- **Path**: Agency Authorization (sponsored by a federal agency) — pre-M-24-15 framework
- **Marketplace**: **NOT FOUND.** Searched 2026-07-10 on updated Marketplace (fedramp.gov/marketplace). Query returned 9 results — all false positives (substring matches: "Insight", "Contract Insight", "Eightfold"). Zero actual InEight products.
- **Documentation**: https://ineight.com/fedramp/ — dedicated page claims "FedRAMP Moderate Equivalency Authorization" for Document module
- **Security page**: https://ineight.com/company/security/ — lists Azure as underlying CSP, ISO 27001/27701, SOC 1/2 Type 2, FedRAMP Moderate Equivalency section
- **Press release**: GLOBE NEWSWIRE via IT Business Net — https://itbusinessnet.com/2026/01/fedramp-authorized-ineight-document-delivers-a-faster-path-to-secure-document-control-for-federal-agencies-and-contractors/
- **FAQ on page**: Clickable FAQ sections cover "Who audited and verified?" and "Where can I find more info?" — but answers are JS-controlled and may not render in browser snapshots

## InEight Suite (Complete Suite)
- **Status per vendor**: Previously claimed as FedRAMP Moderate authorized
- **Marketplace**: **NOT FOUND.** Same search returned no results for "InEight" or "Viewpoint"
- **Note**: The Document module is authorized separately from the suite
- **Practical mitigation**: All InEight products run on Microsoft Azure (FedRAMP High / Class D) — the infrastructure-layer authorization is the compensating control

## Other Trimble/Viewpoint Products on Marketplace

| Product | CSP | Status | Class | Package ID |
|---------|-----|--------|-------|------------|
| Trimble Unity Construct Government Edition | e-Builder, A Trimble Company | FedRAMP Certified | Class C (Moderate) | F1603307884 |

No other Viewpoint, Trimble, or InEight products found on Marketplace.

## FedRAMP Terminology Change (RFC-0020)
- Proposed: January 13, 2026
- Closed: February 19, 2026
- Key change: "FedRAMP Authorization" → "FedRAMP Certification"; Impact Levels → Classes A-D (A=Pilot, B=Low, C=Moderate, D=High)
- Transition period: Until Dec 31, 2026, old impact levels shown in parentheses
- Full transition: January 2027
- "Equivalency" Agency Auth path has no direct mapping under new terminology
- Marketplace now shows blue banner confirming these changes (confirmed 2026-07-10)

## Verifying the Marketplace (as of July 2026)
- Old URL `marketplace.fedramp.gov` permanently redirects to `fedramp.gov/marketplace/`
- SvelteKit SPA — use browser tools, not curl
- Filter categories: "FedRAMP Certified" (530 results), "FedRAMP Ready" (68), "Agency Auth In Process" (59), "FedRAMP In Process" (12)
- No "Equivalency" category exists as a filter
- Searched "InEight" — returned 9 results, all false positive substrings. Visual inspection confirmed zero InEight products.
- Searched "Trimble" — returned 1 result: Trimble Unity Construct Government Edition
- Searched "Viewpoint" — returned 0 results
