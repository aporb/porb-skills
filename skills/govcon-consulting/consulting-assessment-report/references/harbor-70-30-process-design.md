# HARBOR 70/30 Framework for Process Design

When designing an internal process or workflow for a client organization, apply the
70/30 principle from *Shrink-Wrap It* Chapter 11: **70% standardized core that ships
identically to every deployment. 30% configurable surface that adapts to the specific
organization.**

Below 70% standardized = you have a framework, not a product. Above 90% = you can't
meet org-specific requirements. The discipline is knowing which 30% to flex.

## 70/30 Boundary for Internal Process Products

For an internal process (procurement intake, access management, compliance workflow, etc.):

### Standardized 70% Core
These ship identically regardless of the client org:
- Intake form fields and validation logic
- Multi-stage approval flow structure
- SLA timers and escalation rules
- SharePoint list schemas and relationships
- Power Automate flow patterns
- Role definitions (what each role does — not who fills it)
- Status tracking and reporting categories
- Renewal management cadence and alert windows
- Audit trail requirements

### Configurable 30% Surface
These are client-specific and defined during the engagement:
- Financial approval thresholds ($10K / $50K / $100K+ tiers)
- Role-to-person mapping (which specific person fills each defined role)
- Org-specific compliance checklist items (GCC High, FAR 12, DFARS, etc.)
- Business unit taxonomy and naming conventions
- Escalation target mapping (who gets notified at each level)
- Vendor category taxonomy
- Budget code integration

### Custom Work (Outside the Product Boundary)
Do not include these in the standardized product — they are separate engagements:
- Integration with existing ERP/procurement platforms
- Custom reporting or dashboarding beyond standard SharePoint views
- Premium Power Platform features (requires license upgrade)
- External system API integration
- Multi-tenant or subsidiary complexity

## The 70/30 Test

For each element in the process design, ask:
1. Would this be the same at any $4B+ enterprise? → 70% core.
2. Does this depend on who works here and how they're organized? → 30% configurable.
3. Does this require custom development or integration with a specific system? → Custom work (out of scope).

## Applying This to a Proposal

When proposing a process design to a client stakeholder:
1. Present the 70% core as "what the process looks like" — proven, repeatable, no reinvention
2. Present the 30% surface as "what we configure together" — their org, their thresholds, their people
3. Explicitly call out what's NOT included to prevent scope creep

This framing lets the stakeholder see it as a product they're adopting, not a custom build
they're commissioning. It makes the proposal feel low-risk because the core is proven.
