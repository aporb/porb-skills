# Compliance Documentation Reference Pattern

## User Question

"Joe (IT admin) asked 'where is the SSP?' How should I answer, and what should we add to the document?"

## The Problem

Operational documents (cheat sheets, SOPs, job aids) focus on what to DO (data placement, access rules, incident response). They don't answer WHERE to find the formal compliance documents (SSP, POA&M, TCP, assessment results).

When IT staff or assessors look for these docs, they expect a pointer. Not finding one creates friction and makes the operational doc look incomplete.

## The Solution: Brief Callout Box

Add a concise reference section that:
1. **Answers the question directly** — names the docs, specifies the location
2. **Stays operational in tone** — not an audit checklist, not a list of controls
3. **Is general** — no callouts to specific situations or people
4. **Separates concerns** — makes clear these are audit docs, not day-to-day references

## Template (Ivory Callout Box)

```
WHERE TO FIND COMPLIANCE DOCS
SSP, POA&M, and TCP live in /compliance/ on the enclave. These formal audit documents are kept separate from this operational cheat sheet to maintain focus on daily workflows. Reference them for audit preparation, not task execution.
```

**Word count:** 43 words (under 60-word limit)
**Visual style:** Ivory background (#FAF9F5) with red left border
**Placement:** Near the end, before the footer or regulatory authority table

## Positioning Strategy

### Page 4 of a 4-page cheat sheet (Aecon GCC High Enclave example)

The compliance callout goes on page 4, right after the running header:
- **Placement:** Between page header and "People, Access & Prohibited Actions" section
- **Rationale:** Connects operational rules (access, prohibited actions) to formal compliance framework without disrupting flow
- **Effect:** 4 lines, negligible space, answers the question before the user scrolls

### Alternative positions

- **Near the beginning** (page 1): Risk of getting buried in overview content
- **With regulatory authority table** (end of doc): Good, but may feel tacked on
- **As a sidebar note:** Harder to format consistently across deliverables

**Verdict:** Page 4, after running header, before main content sections

## Why This Works

### For IT Staff (Joe's perspective)
- Clear answer: "SSP lives in /compliance/"
- No hunting around or asking IT again
- Knows it's not a daily-use doc

### For Assessors
- Can find the SSP without asking
- Understands the doc's purpose (audit prep)
- Sees that compliance is being tracked

### For Operational Staff
- Won't waste time reading the SSP looking for day-to-day guidance
- Separation of concerns is explicit
- The cheat sheet stays focused on operations

## Variations by Document Type

### For a cheat sheet (operational reference)
Use the template above. The callout answers "where do I find the formal docs?" and explains why they're separate.

### For a SOP (procedural document)
Add a single line in the "References" section:
> **Compliance Documents:** SSP, POA&M, and TCP are maintained in `/compliance/` on the enclave.

### For a training deck or briefing
Add a slide titled "Where to Find Compliance Documentation" with:
- Bullet list of documents (SSP, POA&M, TCP)
- Path: `/compliance/`
- One-sentence note: "These are maintained separately from this training for audit purposes."

## What to Avoid

### Don't make it a compliance checklist
**Wrong:** A 10-row table listing every compliance doc, its owner, last update date, and link.

**Right:** One callout box naming the key docs and their location.

### Don't call out specific situations
**Wrong:** "If you're unsure whether a document is CUI, check the SSP section 5.2."

**Right:** General reference: "These are formal audit documents. Reference them for audit preparation."

### Don't replace content with references
**Wrong:** "For data placement rules, see SSP section 5.3.1."

**Right:** The operational doc itself should state the rules. The reference is only for the formal compliance artifacts.

## When NOT to Add This Section

If the document is ALREADY a compliance document:
- SSP template itself (obviously it contains the SSP)
- POA&M tracker (it references controls directly)
- Assessment briefings (they discuss SSP findings)

Only add this section to **operational** documents where the formal compliance docs are out of scope by design.

## Eval Criteria (Judge Agent Checklist)

When a draft is proposed, evaluate against these criteria:

1. **Answers Joe's question?** — Does it state where the SSP lives (/compliance/)?
2. **Not a compliance checklist?** — Is it brief (<60 words) and not listing controls/requirements?
3. **General enough?** — No specific situations or people named?
4. **Logically positioned?** — Does it flow naturally with the document structure?
5. **Operational tone?** — Is the focus on "where to find for audit prep" not "what to comply with"?
6. **Useful for IT/operational staff?** — Would both groups actually use this reference?

## Real-World Example (Aecon GCC High Enclave Cheat Sheet)

**Context:** 4-page PDF cheat sheet for enclave operations (data placement, access, quick-ref cards).

**Implementation:**
- Added ivory callout to page 4 (43 words)
- References SSP, POA&M, TCP explicitly
- Specifies `/compliance/` location
- Explains separation rationale ("maintain focus on daily workflows")
- Positioned after running header, before "People, Access & Prohibited Actions"

**Effect:**
- Joe (IT) knows where to find the SSP without asking
- Assessors see the pointer immediately
- No page count increase (4 pages maintained via layout compression)
- Cheat sheet remains operational, not a compliance checklist

**Source:** See `~/repos/aecon-fcs/deliverables/Aecon_GCC_High_Enclave_Cheat_Sheet.html` (page 4, lines ~760-765).