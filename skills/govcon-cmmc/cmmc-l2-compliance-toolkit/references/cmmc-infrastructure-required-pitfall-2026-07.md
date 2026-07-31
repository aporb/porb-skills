# CMMC L2 Infrastructure Requirement — Pitfall & Delivery Paths

**Session:** July 20, 2026 — Leatherneck+HARBOR CMMC product strategy
**Trigger:** Agent incorrectly assumed CMMC L2 Self-Assessment required only documentation, not infrastructure. User corrected. Full research conducted.

## The Pitfall

When advising on CMMC L2 Self-Assessment products for micro-businesses, agents (and humans) easily fall into the trap of assuming that "self-assessment" means policy documents and templates alone are sufficient. This is wrong and dangerous.

NIST SP 800-171 Rev 2 includes technical controls that CANNOT be satisfied with policy alone:
- **IA.2.083** — Multi-factor authentication
- **SC.3.177** — Encryption at rest for CUI
- **AU.2.041-044** — Audit logging and monitoring
- **AC.3.012-017** — Access control enforcement (not just policies)
- **AC.3.010** — Session lock after inactivity
- **SC.3.180-183** — Network boundary protection, communications encryption

**Verdict:** Every CMMC L2 engagement MUST deliver or resell a secure CUI environment. Documentation alone does not equal compliance.

## Three Infrastructure Delivery Paths

### Path A: M365 Business Premium GCC High
- **Cost:** ~$22/user/mo
- **Coverage:** ~90-95 of 110 controls with proper configuration
- **Partner requirements:** Microsoft CSP Indirect Reseller authorization (MAICPP enrollment, business verification, MPA signing, GCC High eligibility). 2-4 weeks. FY26 security score requirements.
- **Pros:** Lowest ongoing cost for customers. Customer owns the tenant. We control the full stack.
- **Cons:** CSP authorization overhead. 1-3 week deployment per customer. Configuration complexity.
- **Source:** Microsoft launched BP for GCC High Nov 3, 2025, targeting ≤300-seat organizations. Secureframe analysis confirms it's "often sufficient for CMMC Level 2." 40-60% cheaper than enterprise G-series.

### Path B: PreVeil Partner Resale
- **Cost:** $450/mo for 3 users (PreVeil Pass)
- **Coverage:** 102 of 110 controls (FedRAMP Moderate Equivalent, FIPS 140-3, AWS GovCloud)
- **Partner requirements:** Free web form. No fees. Deal registration. 500+ existing partners. Co-marketing included.
- **Pros:** Zero enrollment friction. Deploys in hours. No tenant migration. Battle-tested: 100+ perfect 110 CMMC scores. C3PAO-preferred. 3,000+ existing customers for cross-sell.
- **Cons:** Dependent on PreVeil's pricing/roadmap. Higher customer monthly cost. We're one of 500+ partners.
- **Source:** preveil.com/preveil-pass, preveil.com/partners-network, preveil.com/partner-resources

### Path C: Cuick Trac Managed GCC-H Enclave
- **Cost:** Custom (enterprise sales)
- **Coverage:** 264 of 320 assessment objectives (82%)
- **Partner requirements:** Unknown — no public partner program page found
- **Pros:** Turnkey managed service. Inherits most controls. Coalfire CPAN partnership.
- **Cons:** Enterprise pricing. Opaque sales process. Overkill for micro-businesses.
- **Source:** cuicktrac.com

## Strategic Recommendation (July 2026)

**Lead with Path B (PreVeil), offer Path A (M365) as Phase 2 alternative.** PreVeil enables revenue within days of partnership approval. M365 requires 2-4 week CSP enrollment. Once we have 5+ Hill 2/3 deliveries generating cash flow, pursue CSP authorization to add the lower-cost M365 path. Both paths are presented as tiered options to customers: PreVeil as the premium fast-deploy, M365 as the value option.

## Market Context
- $6.8B CMMC compliance services market (2025), growing to $39.4B at 21.5% CAGR (MarketIntelo)
- 300,000+ DIB organizations, <15% fully compliant with NIST 800-171
- Only ~100 C3PAO assessors for 300K+ organizations
- SBA estimates $388K-$594K per certification
- CMMC Phase II C3PAO suspension (July 13, 2026) shifts demand toward self-assessment enablement
