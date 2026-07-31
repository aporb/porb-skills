# Technical Evaluator Review — Product Architecture & Feasibility

A specialized adversarial review persona focusing on the TECHNICAL viability of a proposed product or technical approach within a GovCon response. This is distinct from the general adversarial review's PWS line-item compliance focus — it evaluates whether the proposed technology stack, architecture, and team can actually deliver what's promised.

**Trigger:** User requests a "technical evaluator review," "product viability assessment," "architecture review," or asks whether a proposed system/solution is technically sound and buildable by the proposed team.

## Review Dimensions (weighted)

| Dimension | Weight | What It Evaluates |
|---|---|---|
| **Product Viability** | ×2 | Is the technology stack appropriate for the problem? Does it scale? What's missing? |
| **Architecture Soundness** | ×2 | Is there an architecture description at all? Data model? Integration map? Security boundary? |
| **Build vs Buy** | ×1.5 | Could COTS tools do this better/cheaper? Is the build justification credible? |
| **Feasibility (Team × Timeline)** | ×2.5 | Can the proposed team size actually build AND operate? Do the math. |
| **AI Claims Credibility** | ×1.5 | Are AI claims backed by domain-specific evidence? Or is it general AI applied to a new domain? |
| **PWS Technical Coverage** | ×1.5 | What PWS technical requirements does the product approach NOT address? |
| **Team Credential Leverage** | ×1.5 | How well does the response USE the team's actual credentials? Is it underselling by leaving verified credentials unstated or declaring gaps that are already filled? |

Total weight: 12.5. Final score = weighted sum / (max per dimension × total weight) × 100.

## Methodology

### 1. Product Viability Assessment

For any proposed product built on a platform stack (e.g., "M365-native using Power Platform + SPFx"), verify:

- **Platform capacity limits:** Dataverse storage, Power Automate API request limits, connector throttling. Does the proposal acknowledge and plan for these?
- **Connector availability:** Does the platform have native connectors for the systems it claims to integrate with? Custom connectors are development work — they're not free.
- **Analytics capability:** SPFx is a UI framework. Where are analytics, dashboards, and ML model serving handled? Power BI is often the missing piece.
- **Existing-system awareness:** If the PWS mentions an existing application/tool, does the proposal address integration or replacement strategy? Building a replacement while operating the existing one is parallel-operations risk.
- **Data source accessibility — the most commonly falsified claim:** When the response claims to integrate government data sources (OFAC, HHS OIG, BIS, FDA enforcement, DEA, etc.), verify EVERY source independently. Check whether each has a documented REST API or is a downloadable flat file. Check whether the source covers the specific data type claimed (e.g., openFDA has drug recall data but NOT warning letters or 483s). This is the single most common failure mode in due diligence/screening proposals — see `references/common-fact-check-targets.md` for the full patterns catalog. A response whose core architecture depends on real-time API calls to sources that only publish downloadable files has a P0 product viability failure.

### 2. Architecture Assessment

**Red flag:** The entire architecture description is one paragraph of platform names with no data model, integration architecture, API strategy, RBAC, or DR/BC plan.

**Worse-than-red-flag: No architecture description exists at all.** Some drafts abandon a prior product concept but replace it with aspirational language ("AI agents automate X") that describes capabilities without describing HOW. When there is zero architecture — no data flow, no integration map, no security boundary — score 2/10 or lower. A response that says "we'll use AI to do license reconciliation" without describing where the data lives, how it's ingested, what platform processes it, or how the AI connects to anything is not an architecture. It's a wish. Score accordingly.

At minimum, a credible architecture description should address:
- Data sources → ingestion → normalization → storage → processing → presentation
- Integration points with existing systems (especially those the PWS names)
- Security boundary: ATO inheritance claims must distinguish platform-level from application-level authorization
- Identity/RBAC: Especially important for multi-division federal environments (11 OpDivs = federated governance)

### 3. Build vs Buy Analysis

Always ask: **Does a mature COTS product already solve this?**

For SAM/license management specifically:
- Flexera, Snow Software, ServiceNow SAM Pro, USU, Aspera are all FedRAMP-authorized and have federal deployments
- Compare the build proposal against COTS capabilities: publisher recognition library (2M+ SKUs), native connector support, audit defense package generation, True-Up calculation engines

The strongest federal IT approach is usually: buy COTS foundation → build custom analytics/reporting/AI augmentation on top. Proposals that propose to rebuild COTS-equivalent capability from scratch need an extraordinary justification — and the response should acknowledge the COTS alternative and explain why it was rejected.

### 4. Feasibility Math

**The core question:** Can the proposed team size simultaneously RUN the operational requirements AND BUILD the product?

Method:
1. Count PWS operational roles and estimate FTE per role from the PWS description
2. Estimate development team size needed to build the product to MVP in the proposed timeline
3. Check for overlap — can any one person do both operations and development?
4. If the math doesn't add up (e.g., 4 people covering 8 PWS roles + building a SAM platform), flag it.

**Multiplier claims are red flags:** "AI makes us 3x more productive" without methodology, benchmarks, or domain-specific evidence. Flag these as P1 every time.

### 5. AI Claims Credibility

**The AI-DDSF pattern** (common in GovCon responses): A team built an AI system for Domain A (e.g., Air Force decision intelligence). They now propose applying "the same architecture" to Domain B (e.g., HHS software license management). Evaluate:

- Is the architectural similarity claim credible? (Data ingestion + normalization + analytics + explainable output IS a reusable pattern)
- Has any component been applied to the new domain? (If zero domain-specific AI work has been done, it's aspirational, not demonstrated)
- Does the response acknowledge the adaptation gap? (Honest: "architecture is the foundation; VMO-specific models need to be built." Dishonest: "our AI-DDSF IS the VMO Command Center.")

**The PWS AI emphasis inversion:** If the response spends 80% of its technical content on AI while the PWS mentions AI in one permissive sentence buried in Additional Requirements, flag this as P0 structural failure. The response's content proportions must match the PWS's requirement proportions.

### 6. PWS Technical Coverage Gaps Specific to Product Approach

Beyond the general PWS coverage audit, identify gaps that are SPECIFIC to the product/build approach:

- Does the PWS mention an existing system the response proposes to replace? (Parallel-operations risk)
- Does the PWS require coordination with specific teams/tools the product needs to integrate with? (SAM team, existing VMO app)
- Does the PWS require compliance frameworks (EPLC, SDLC) that apply to custom development? (If yes, flag non-acknowledgment)
- Does the PWS require transition-out training? (Custom-built tools create vendor lock-in for the government — must be addressed)

### 7. Team Credential Leverage Assessment

**This dimension exists because teams often leave their strongest credentials unused in the draft.** A separate team credential gap analysis document may exist (check `~/sources-sought-responses/plans/<agency>-team-credential-gap-analysis.md` or similar). If it does, compare it against the draft: how many of the gap analysis's recommendations were actually incorporated?

Scoring drivers:
- **+2:** Draft fully leverages team credentials — every team member appears in Key Personnel, credentials stated as current (not aspirational), gap notes reflect actual gaps
- **0:** Draft uses ~half of available credentials; some team members invisible; some credentials stated as aspirational when already held
- **-2:** Draft actively undersells the team — declares gaps that are filled, presents held credentials as "will obtain," omits team members entirely, credits wrong person for core capability

**Common failure modes this dimension catches:**
- PMP/DAWIA III already held but presented as "will obtain by start date"
- Acquisition gap declared when a DAWIA III Contracting professional is on the team
- Team members (especially those filling PWS-mandated specialist roles) completely invisible in Key Personnel
- FOCI/compliance expertise attributed to wrong person
- Response presents a 2-person team when 4+ qualified people exist on the roster

**Method:** Cross-reference the draft's Key Personnel, gap notes, credential claims, and vendor governance language against the team credential gap analysis (if available) or against team bios/resumes. Flag every credential the team HAS but the draft doesn't USE. Score based on what fraction of available team depth made it into the response.

## Deliverable Structure

```markdown
# TECHNICAL EVALUATOR REVIEW — [Product Name] Approach

## OVERALL SCORE: XX/100 — [VERDICT]

[Weighted score table]

## 1. PRODUCT VIABILITY — X/10
[Stack appropriateness, capacity, connectors, analytics, existing-system awareness. +/- scored.]

## 2. ARCHITECTURE — X/10
[Architecture depth, data model, integration map, security boundary, RBAC, DR/BC. +/- scored.]

## 3. BUILD vs BUY — X/10
[COTS alternatives, build justification, proposed augmentation strategy.]

## 4. FEASIBILITY — X/10
[Team size math, operational workload vs development workload, multiplier claims.]

## 5. AI CLAIMS — X/10
[Infrastructure reality, domain adaptation evidence, emphasis inversion vs PWS.]

## 6. PWS TECHNICAL COVERAGE GAPS — X/10
[Product-approach-specific gaps table. Existing systems, integrations, compliance frameworks, transition.]

## RECOMMENDATIONS
[P0/P1 prioritized fixes. Strategic reframing recommendations.]

## SCORING DETAIL
[Per-dimension +/- breakdown]
```

## Pitfalls

- **Don't evaluate AI infrastructure instead of AI domain fit.** Real infrastructure (+2 points) doesn't compensate for zero domain-specific evidence (-2 points). A .45 caliber pistol is real and effective, but it's the wrong tool for heart surgery. Same principle.
- **Do the feasibility math.** Don't just say "4 people seems thin." Calculate: 8 PWS roles × 0.5-1.0 FTE = 4-8 FTEs for operations alone. Development: 3-5 FTEs for 12-24 months. If ops + dev > team size × 2.0 (compressed), it's not feasible.
- **Watch for the "connectors are free" fallacy.** Power Automate has ~600 built-in connectors. VLSC, Oracle LMS, and Salesforce GovCloud are NOT among them. Custom connectors require development, authentication setup, and ongoing maintenance. The response should acknowledge this or it's naively optimistic.
- **The "no ATO" claim is always qualified.** Platform services may be authorized under the tenant's ATO, but custom application components (SPFx code, Dataverse schemas, Power Automate flows with custom connectors) change the security boundary and require review under EPLC/SDLC. Never accept "inherits ATO" at face value without checking what custom development actually requires in that agency's compliance framework.
- **Build vs buy isn't an aesthetic preference.** The SAM tool market has 5+ FedRAMP-authorized products with decades of development. Proposing to build equivalent capability on Power Platform needs an extraordinary justification, not just "it's in the existing tenant." If the justification isn't in the response, flag it as a technical blind spot.
- **The review MUST quote the PWS.** Every claim about what the PWS does or doesn't require must trace back to a specific PWS line. Never paraphrase from memory — the adversarial reviewer from 2 days ago may have gotten it wrong, or the response may have been built against an earlier draft.
- **Cross-reference the team credential gap analysis before scoring feasibility.** If a gap analysis document exists at `~/sources-sought-responses/plans/<agency>-team-credential-gap-analysis.md`, load it. It often reveals that declared gaps are already filled, credentials already held are presented as aspirational, and team members who fill PWS-mandated roles are invisible in the draft. Scoring feasibility without this cross-reference will miss the single most common failure mode: the team is 3x stronger than the response makes them look.
- **Verify every data source claim independently — never accept at face value.** The most common false claim in GovCon tech proposals is that government enforcement/compliance databases are available as free APIs. OFAC publishes CSV downloads, not a REST API. HHS OIG publishes a monthly CSV, not a REST API. FDA openFDA has no Warning Letter or 483 endpoint. BIS publishes a .txt file. Only SEC EDGAR and USAspending.gov have true open REST APIs. For every claimed data source, navigate to the agency developer page and confirm the access method. A single unverified data source claim that proves false can crater the entire Product Viability score. See references/common-fact-check-targets.md for the complete verification checklist.
- **Don't treat "no architecture" the same as "bad architecture."** When a prior draft had a product concept and the current draft dropped it entirely, score Architecture Soundness LOWER for the current draft — at least the prior version had something to evaluate. Aspirational language ("AI agents will automate reporting") without any architectural description is scored as having no architecture, not as having a weak one.