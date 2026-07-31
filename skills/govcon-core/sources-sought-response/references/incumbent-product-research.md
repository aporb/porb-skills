# Incumbent Commercial Product Research — Methodology for Sources Sought Competitive Intelligence

## When to Use

The Sources Sought notice identifies a named commercial product the agency currently uses (e.g., "Dow Jones RiskCenter Financial Crime with Factiva and UBO — 10-user subscription"). Before drafting the response, you need to understand the incumbent product's strengths, weaknesses, pricing model, integration capabilities, and competitive landscape to position an alternative.

This phase runs BEFORE Phase 0 (respondent web presence research) and BEFORE any drafting. It is distinct from `fedcon-competitive-landscape-scan` Mode B (which uses USASpending.gov API for prior award data) — this is lateral competitive intelligence on the product itself.

## The 7-Dimension Research Framework

Research the incumbent product across these seven dimensions in parallel:

### 1. Core Product Capabilities
- What does the product actually do? What are its named features?
- How many risk profiles / data points does it claim (look for specific numbers)?
- What risk categories does it cover (sanctions, PEPs, adverse media, UBO, etc.)?
- What's included in the subscription tier the agency likely has (e.g., 10-user)?
- Product pages are the primary source; look for detailed feature lists, "what's included" sections, and data quality reports

### 2. Integration Ecosystem
- What does the "plus" component add? (e.g., Factiva adds to Financial Crime Search)
- Which data sources are OWNED vs. LICENSED? (critical for lock-in analysis — licensed data is available to competitors too)
- How does the secondary product differentiate the primary offering?
- Look for partnership announcements, press releases, and data quality reports

### 3. Data Sources & Partnerships
- Which datasets are proprietary vs. third-party?
- Third-party data (e.g., D&B UBO) means competitors can license the same data
- Government-provided data (e.g., FinCEN CTA registry) may provide free alternatives
- Search for "partnership," "powered by," "data sources," "coverage"

### 4. Pricing Model
- Per-seat vs. per-search vs. subscription? Platform fee + usage?
- Actual price ranges (public sources: Vendr, TrustRadius, G2, Gartner reviews, state procurement contracts)
- Hidden costs: overage fees, API access surcharges, professional services, training
- Government contract vehicles: GSA Schedule availability, existing federal pricing
- **Critical:** Never trust vendor list prices; cross-reference with anonymized transaction data (Vendr) and public contract award data

### 5. Competitive Landscape
- Who are the named competitors in this space?
- What are their differentiators relative to the incumbent?
- Which competitors already have federal contract vehicles?
- Which competitors have government-specific features the incumbent lacks?
- Search for competitor comparison pages, analyst reports (Gartner Magic Quadrant, Forrester Wave), and federal procurement databases

### 6. Federal Agency Usage
- Which agencies use this product or its competitors?
- Are there known federal contracts for this product?
- What alternatives does the specific agency already license? (e.g., M365 GCC High, Salesforce, ServiceNow)
- Search SAM.gov, USASpending.gov, agency procurement forecasts, trade press (FedScoop, GovCon Wire)

### 7. Weaknesses, Gaps & API Flexibility
- User reviews: G2, TrustRadius, Gartner Peer Insights, Reddit, LinkedIn
- Known pain points: cost, complexity, false positives, poor UX, limited customization
- API documentation: developer portal, Swagger/OpenAPI specs, versioning policies
- Integration limitations: walled garden vs. open ecosystem
- Industry-specific gaps: does the product serve the agency's actual mission (e.g., pharmaceutical supply chain vs. financial AML/KYC)?

## Research Technique: Parallel Web Research + Extraction

**Phase A — Discovery (batch web searches):**
Run 4-6 web searches in parallel across the seven dimensions. Use broad queries first, then narrow. Search for vendor product pages, third-party reviews, pricing data, competitor comparison pages, and federal contract references.

**Phase B — Deep Extraction (batch web_extract):**
Extract content from the most promising pages in parallel (up to 5 at once). Prioritize: vendor product pages, vendor developer portal, pricing intelligence sites (Vendr), and federal procurement aggregators.

**Phase C — Gap-Fill Searches:**
Identify remaining gaps and run targeted searches for specific dimensions (e.g., user reviews, API docs, federal contract vehicles).

**Key sources by dimension:**

| Dimension | Best Sources | Fallback |
|-----------|-------------|----------|
| Product capabilities | Vendor product pages (`web_extract`) | Data quality reports, analyst briefs |
| Pricing | Vendr (`web_extract`), state procurement contracts | Gartner/TrustRadius pricing tabs |
| Integration | Vendor developer portal, partnership press releases | API docs, integration partner pages |
| Competitors | Competitor product pages, SaaSworthy/Gartner alternatives | Burton-Taylor AML/KYC reports |
| Federal usage | SAM.gov, USASpending.gov, agency procurement forecasts | Trade press (FedScoop, GovCon Wire) |
| Weaknesses | G2/TrustRadius reviews, LinkedIn comments, Reddit | Analyst reports (limitations sections) |
| API flexibility | Developer portal Swagger docs, versioning policies | SDK availability, community forums |

## Output: Competitive Positioning Grid

Include a capability comparison matrix in the final report that maps the incumbent against key competitors across the dimensions that matter to the agency's mission:

| Capability | Incumbent | Competitor A | Competitor B | Competitor C |
|------------|:---:|:---:|:---:|:---:|
| [Dimension 1] | ★★★★ | ★★★★ | ★★★★★ | ★★★ |
| [Dimension 2] | ... | ... | ... | ... |

Use star ratings (★) with brief evidence notes in a companion table. This is the artifact the response drafter uses to position the alternative.

## Strategic Positioning: The Build-vs-Buy Analysis

The most valuable output of incumbent product research is the **build-vs-buy determination**:

**When to propose a competing SaaS:**
- The incumbent has no unique data moat (all data is licensed from third parties or publicly available)
- Multiple competitors exist with federal contract vehicles, making the procurement competitive
- The agency's mission requires features the incumbent doesn't provide

**When to propose a custom build (M365/Power Platform):**
- The agency already licenses a platform (M365 GCC High, Salesforce Government Cloud, ServiceNow) that can host the solution
- The incumbent's core value is the UI/workflow, not proprietary data
- The agency's mission requires customization the SaaS doesn't support
- The per-user SaaS cost exceeds the build cost over the contract period
- Government-specific compliance requirements (FAR/DFARS, CMMC, Buy American) are better served by a custom build

## Worked Example

Full competitive intelligence report for HHS ASPR Sources Sought (ACQ-OMAS-2026-SAT-0015_Sources) — Dow Jones RiskCenter Financial Crime / Factiva / UBO — at `~/dj_competitive_intelligence.md` (July 2026, 379 lines, ~25KB). Covers all seven dimensions with specific product details, pricing estimates, competitor grid, federal usage patterns, API analysis, and strategic build-vs-buy recommendation.
