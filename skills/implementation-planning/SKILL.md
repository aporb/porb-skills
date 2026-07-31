---
name: implementation-planning
description: Produce implementation-ready project plans and technical specifications that minimize ambiguity, reduce implementation risk, and enable developers to execute with confidence. Use when asked to plan a feature, write a spec, create a PRD, scope a project, or produce a technical design document.
---

# Implementation Planning & Specification Author

## Trigger

User asks to:
- Plan a feature, project, or initiative
- Write a technical specification, PRD, or design document
- Scope work before implementation
- Produce an engineering plan with milestones and work breakdown
- Bridge business requirements to technical execution

Also triggered when the user provides a problem statement, user story, or business need and expects a structured plan before coding begins.

## Guiding Principles

### Understand before proposing
Develop a complete understanding of the business problem, user needs, existing system, architecture, constraints, and objectives before recommending solutions. Never optimize for implementation before understanding the problem.

### Be outcome-driven
Focus on solving the underlying business problem. Requirements should describe desired outcomes and measurable success rather than preferred implementation techniques whenever possible.

### Reduce ambiguity
Every requirement should be clear, specific, testable, verifiable, and unambiguous. Assume the developer has never seen this project before. The specification should answer nearly every implementation question before coding begins.

### Separate "What" from "How"
Define what must happen, why it matters, expected behavior, constraints, and success conditions. Avoid prescribing implementation unless technical or architectural constraints require it. Developers should retain engineering judgment.

### Think end-to-end
Evaluate the solution from: product, engineering, architecture, UX, security, performance, accessibility, scalability, operations, monitoring, deployment, documentation, and long-term maintenance. Do not optimize one area while ignoring another.

### Challenge assumptions
Actively search for missing requirements, hidden dependencies, contradictions, undefined behavior, edge cases, invalid assumptions, technical risks, and product risks. Document them. Do not silently make assumptions.

### Design for maintainability
Prefer solutions that are simple, modular, extensible, reusable, observable, and maintainable. Avoid unnecessary complexity.

### Identify dependencies early
Identify technical dependencies, external services, APIs, infrastructure, existing systems, team dependencies, required sequencing, and potential blockers. Surface these before implementation begins.

### Plan for change
Document assumptions, constraints, decisions, alternatives considered, tradeoffs, and future considerations. The plan should remain useful as the project evolves.

### Make everything verifiable
Every requirement should be traceable. Every deliverable should include Acceptance Criteria and Definition of Done. Everything should be objectively measurable.

### Optimize for execution
Produce documentation that allows developers to work independently, minimize clarification meetings, parallelize work where appropriate, and understand priorities and sequencing.

### Validate continuously
Review the specification from multiple perspectives before finalizing. At minimum: Product Owner, Senior Engineer, QA, Security, Operations. Resolve conflicts before implementation.

### Prefer evidence over opinion
Base recommendations on existing code, documentation, architecture, standards, research, user requirements, and business objectives. Avoid unsupported opinions.

### Expose risks
Every significant feature should identify technical risks, product risks, operational risks, security risks, unknowns, and mitigation strategies.

## Workflow

### Phase 1: Discovery
1. **Understand the problem** — Read any provided context, existing specs, related code, and project conventions. If insufficient context, ask clarifying questions before proceeding.
2. **Identify stakeholders** — Who needs to approve? Who will build? Who will operate? Who will use?
3. **Map the current state** — If modifying an existing system, understand the current architecture, workflows, limitations, and technical debt.
4. **Surface unknowns** — List open questions that need decisions before planning can proceed.

### Phase 2: Specification
Produce the deliverable with these sections (include only what the project scope warrants):

#### Required sections (every plan):
- **Executive Summary** — High-level overview in 3-5 sentences
- **Objectives** — Business objectives, technical objectives, success metrics, expected outcomes
- **Scope** — Explicitly in-scope and out-of-scope items
- **Functional Requirements** — Complete functional behavior, user flows (primary, alternative, failure paths, edge cases)
- **Acceptance Criteria** — Specific, measurable, testable outcomes for every feature
- **Definition of Done** — Completion checklist covering quality, testing, docs, deployment readiness, security, performance
- **Risks & Mitigations** — Technical, business, operational, security risks with mitigation strategies

#### Conditional sections (include when applicable):
- **Current State** — Existing architecture, workflow, limitations, known technical debt
- **Proposed Solution** — High-level solution, major design decisions, architectural approach
- **Nonfunctional Requirements** — Performance, security, reliability, accessibility, maintainability, scalability, observability, compliance
- **Architecture** — System interactions, components, data flow, integration points, external services
- **Data Model** — Entities, relationships, schema changes, migration considerations
- **API Requirements** — Endpoints, contracts, authentication, authorization, error handling, versioning
- **Dependencies** — Internal, external, infrastructure, third-party services
- **Assumptions** — Explicit assumptions documented
- **Constraints** — Technical, business, regulatory, environmental constraints
- **Milestones** — Major delivery checkpoints and decision gates
- **Work Breakdown** — Major phases, logical sequencing, dependencies, parallel work opportunities
- **Validation Strategy** — Testing, QA, verification, performance validation, security validation, operational readiness
- **Rollback Strategy** — Recovery approach, deployment rollback, data rollback
- **Open Questions** — Unknowns requiring decisions
- **Appendix** — Supporting research, references, diagrams, additional documentation

### Phase 3: Validation
Before considering the specification complete, verify:
1. The business problem is clearly defined
2. Success metrics are measurable
3. Scope and non-scope are explicit
4. Requirements are complete and testable
5. Edge cases are documented
6. Risks have mitigation plans
7. Dependencies are identified
8. Assumptions are documented
9. Constraints are documented
10. Architecture is understandable
11. Acceptance Criteria are objective
12. Definition of Done is complete
13. Validation strategy exists
14. Open questions are identified
15. The specification minimizes ambiguity
16. A developer could begin implementation with minimal clarification
17. The plan balances flexibility with sufficient implementation guidance

## Output Format

Deliver the specification as a well-structured Markdown document, or an HTML document if the user needs a print-ready deliverable.

For Markdown:
- Use clear heading hierarchy (## for sections, ### for subsections)
- Use tables for structured data (requirements, risks, milestones)
- Use checklists for Definition of Done
- Use mermaid diagrams for architecture and data flow when helpful
- Keep prose concise; prefer bulleted lists over dense paragraphs

For HTML (when printing/distribution matters):
- Self-contained with inline CSS
- Professional, clean aesthetic
- Print-friendly with `@page` rules

## Pitfalls

- **Do NOT prescribe implementation details when not required.** "Use PostgreSQL with a users table" is implementation. "Persist user identity with the following attributes" is a requirement. Let engineers choose the how.
- **Do NOT skip edge cases.** "What happens when the API is down?" "What if the input is empty?" "What if the user has no permissions?" Document these.
- **Do NOT leave acceptance criteria vague.** "Works correctly" is not testable. "Returns 200 with JSON body containing `status: 'active'` when user exists and token is valid" is.
- **Do NOT optimize one dimension at the expense of others.** A fast system that is insecure is not a good plan. A secure system that is unusable is not a good plan.
- **Do NOT silently assume.** If you don't know the authentication model, the deployment environment, or the scale requirements, ask or document the assumption explicitly.
- **Do NOT ship a plan without risks.** Every plan has risks. If you can't find any, you haven't looked hard enough.
- **Do NOT conflate scope creep with thoroughness.** Every section in the specification must earn its place. A 3-day feature doesn't need a 20-page spec. A 6-month platform migration does. Scale the deliverable to the project.
- **Do NOT produce a plan that can't be actioned.** If the work breakdown doesn't enable parallel work or the milestones aren't verifiable, the plan fails its primary purpose: execution with confidence.
- **Do NOT skip the Definition of Done.** "Code is merged" is not done. Done means tested, documented, deployed, monitored, and validated against acceptance criteria.
