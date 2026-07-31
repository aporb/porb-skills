# HARBOR 6-Stage Opportunity Analysis Framework

## When to Use

When the user drops a SAM.gov opportunity link and says "let's think about this one" or "go through the workflow" or "use the HARBOR process" — they want the full HARBOR 6-stage analytical framework applied to evaluate a single opportunity, produce a strategic briefing, and determine whether/how to respond.

This is distinct from:
- **Standard opportunity research** (discovering opportunities across a date window) — that's the parent SKILL.md
- **Sources Sought response drafting** — that's the `sources-sought-response` skill, which comes AFTER this analysis
- **Multi-opportunity pipeline assessment** — that's the batch grants/SAM.gov pipeline workflow

This is: **one opportunity, analyzed through all 6 HARBOR stages, producing one strategic HTML briefing.**

## Workflow

### Phase 0: Extract + Interview (15 min)

1. Load the SAM.gov detail page (browser_navigate to `/opp/<id>/view`)
2. Extract: title, agency, solicitation number, deadline, set-aside, PSC, NAICS, incumbent, description, POC
3. If an HTML briefing already exists for this opportunity (e.g., from a daily sweep), load it for context
4. Check the deadline — if < 7 days, the briefing MUST include a 48-hour action plan
5. **Interview the user** if the approach isn't obvious. The session's key moment came from Amyn's mid-turn insight: "we could productize most of this and automate it in their environment with their already licensed tools." That one sentence reframed the entire analysis from SaaS resale → M365 productization. Don't skip the interview.

### Phase 1: HARVEST — Opportunity Discovery (Research)

**Goal:** Understand what's being bought, who's buying it, who currently provides it, and what the competitive landscape looks like.

Dispatch 3 parallel leaf agents with distinct research personas:

| Agent | Research Focus | Key Questions |
|-------|---------------|---------------|
| **Incumbent Analyst** | The current vendor/product | What does the incumbent solution do? Pricing? Weaknesses? Federal footprint? Is it a walled garden or does it have APIs? |
| **Market / Requirement Analyst** | The end user's mission, regulatory drivers, federal landscape | What's the agency's actual need? What regulations drive this? Has anything changed recently (new NIST guidance, policy shifts)? How big is the federal market for this? |
| **Alternative / Build-vs-Buy Analyst** | Technical alternatives | Can this be built on existing agency infrastructure (M365, Salesforce, ServiceNow)? What's already licensed? What public data sources could replace commercial databases? Has anyone done this before? |

Run these as `delegate_task` calls in parallel — they are independent. Do NOT wait for results before starting Phase 2 architecture work — start framing the strategic approach while agents run.

### Phase 2: ARCHITECT — Strategic Approach

**Goal:** Determine the highest-leverage way to position Leatherneck/HARBOR for this opportunity.

Key strategic question: **Is this a "resell someone else's tool" play or a "productize on existing infrastructure" play?**

The HARBOR thesis favors the latter. The pattern:
1. Audit what the agency already licenses (M365, Salesforce, ServiceNow)
2. Identify unused or under-leveraged platform capabilities (Power Platform, custom apps, automation)
3. Build tailored automation on the owned platform instead of buying new SaaS
4. Eliminate the SaaS subscription cost
5. Ongoing maintenance contract = recurring revenue

This pattern works when:
- The agency already licenses M365 GCC/GCC High (almost all of HHS does)
- The requirement is a workflow/automation problem, not a proprietary data problem
- Public data sources (OFAC, SAM.gov, SEC EDGAR) can supplement or replace commercial databases
- A recent regulatory shift (new NIST framework, policy change) creates demand for tailored solutions

Document the approach as a comparison table: SaaS replacement vs. M365 productization — cost, FedRAMP, integration, customization, lock-in, contract vehicle.

### Phase 3: RISK-PROOF — Compliance & Authorization

**Goal:** Map the authorization pathway and identify blockers.

For M365 productization plays, the key finding is usually: **FedRAMP inherited from the existing tenant.** No new ATO needed. This is a massive advantage over SaaS alternatives that require separate authorization.

Check:
- What cloud environment does the agency use? (GCC, GCC High, DoD?)
- Is Power Platform authorized in that environment? (GCC = FedRAMP High + DISA IL2; GCC High = IL4)
- What data classification applies? (CUI, PII, PHI?)
- Are there recent regulatory frameworks the solution should align with? (NIST SP 1326 C-SCRM, HHS C-SCRM guidance)

For Leatherneck specifically ($0 past performance): address FAR 15.305(a)(2)(iv) neutral rating, position as new approach not re-compete, rest on team credentials and proof-of-concept demo.

### Phase 4: BUILD — Response Strategy

**Goal:** Outline what the actual Sources Sought response should say.

This is NOT the full response draft — that comes later under `sources-sought-response`. This is the strategic outline:
- Core narrative (1-2 sentences)
- Response sections (5-7, bullet-level)
- Key differentiators to emphasize
- What to downplay or omit
- Pricing strategy (ROM if applicable)

### Phase 5: OPERATE — Boundaries

**Goal:** Define what Leatherneck will and won't do. Prevents scope creep in the response.

Document:
- In-scope deliverables
- Out-of-scope items (explicitly)
- Team roles (all 4 co-founders, with specific assignments — never "Douglas/Amyn" as default)
- Contract vehicle recommendation

### Phase 6: REPLICATE — Expansion Path

**Goal:** Show why this opportunity is bigger than one contract. The HARBOR framework is about productizing and scaling.

Map the follow-on opportunities:
- Other OPDIVs/components within the same agency with similar needs
- Other agencies with the same pattern
- Reusable components that could be productized

## Briefing Structure

Output: self-contained HTML to `/data/nextcloud/data/amyn/files/briefings/` → `https://brief.h.porb.dev/<filename>.html`

Structure the briefing around the HARBOR stages:
1. **Header** — Notice ID, title, deadline, bidding entity, generated date
2. **Verdict** — BLUF (Bottom Line Up Front): GO/NO-GO with 1-paragraph rationale
3. **H: HARVEST** — SAM.gov detail table, incumbent analysis table, competitive landscape
4. **A: ARCHITECT** — Strategic approach, comparison table (SaaS vs. build), architecture diagram
5. **R: RISK-PROOF** — Authorization pathway, compliance checklist, risks + mitigations
6. **B: BUILD** — Response outline (section-by-section)
7. **O: OPERATE** — Scope boundaries, team role assignments
8. **R: REPLICATE** — Follow-on opportunities, expansion path
9. **Action Items** — 48-hour or weekly plan with named owners
10. **Strategic Context** — Why this matters beyond this one opportunity

Use the Thariq/html-effectiveness aesthetic (ivory/clay/slate/oat). Store in Nextcloud briefings directory. After writing, run `docker exec` scan and send the link only in Discord.

## Delegation Agent Pattern

The research phase uses 3 parallel leaf agents via `delegate_task`. Each gets:
- A specific research persona (Incumbent, Market, Build-vs-Buy)
- Full context about the opportunity, the bidding entity, and the strategic approach
- The Leatherneck-Harbor entity factsheet (`references/leatherneck-harbor-entity-factsheet.md`)

Dispatch all three simultaneously. They are independent. Continue with architecture framing while they run — do not block on agent results. The briefing integrates findings from all sources (agents + direct research).

## Worked Example

**HHS ASPR Due Diligence (July 2026):** SAM.gov Sources Sought for Financial Crime Search replacement. Incumbent: Dow Jones. The analysis reframed the requirement from "which SaaS to buy" to "build due diligence automation on HHS's existing M365 GCC High using Power Platform." Key factors: NIST SP 1326 C-SCRM guide released July 2026 (timing advantage), Power Apps GCC High is FedRAMP High, public data sources (OFAC, SAM.gov, OIG LEIE) can supplement commercial databases, 2-day deadline required 48-hour action plan. Briefing: `hhs-aspr-due-diligence-harbor-analysis-2026-07-21.html`.

## Pitfalls

- **Don't default to SaaS resale.** The HARBOR thesis is "productize on existing infrastructure." Before pitching a LexisNexis or Refinitiv resale, ask: does the agency already license the platform to build this natively?
- **Don't skip the interview.** Amyn's mid-turn insight ("we could productize this with their already licensed tools") changed the entire analysis. If the approach isn't obvious, ask. A 30-second clarification saves hours of wrong-direction work.
- **2-day deadlines need 48-hour action plans.** If the Sources Sought closes within 48 hours, the briefing MUST include a day-by-day action plan with named owners. Don't just analyze — tell them what to do and when.
- **Don't put Douglas/Amyn as default owners for everything.** All 4 Leatherneck co-founders (Douglas, Mark, Justin, Amyn) must appear in the team roles and action items with specific assignments.
- **Don't wait for delegation agents.** Dispatch them and continue building. The briefing integrates all sources — agents + direct research + the strategic framework.
- **NIST timing hooks are gold.** When a new NIST framework drops the same month as a Sources Sought, lead with it. "This tool wasn't built for SP 1326" is a powerful differentiator.
