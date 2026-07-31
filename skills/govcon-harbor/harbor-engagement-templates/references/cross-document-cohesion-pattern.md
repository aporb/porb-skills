# Cross-Document Cohesion Pattern

## When to use

When building multiple deliverables for a single engagement (pitch deck + internal brief + SOW + entity guide) that will be read together or in sequence by related stakeholders.

## The core insight

Each document serves a different reader and a different purpose — but they MUST appear to come from the same company, tell the same story, and ask for the same decision. Contradictions between documents are more damaging than any single document's errors because they signal that the team isn't aligned.

## The 4 dimensions of cohesion

### 1. Evidence Consistency (the baseline)

Every fact, figure, and citation must be identical across all deliverables.

| Check | Example Find |
|-------|-------------|
| Entity name matches everywhere | HARBOR Initiative LLC (Texas) in all three docs |
| Same dollar figures | ITAR penalty $1,271,078 in deck AND brief |
| Same regulatory citations | 22 CFR §127.10(a)(1)(i) in deck AND brief |
| Same CLIN ranges | Phase 2 = "CLINs 0003-0006" everywhere |
| Same competitor descriptions | Vendors described identically in deck AND brief |

**Tool:** Build a consistency matrix. Claims as rows. Deliverables as columns. Every red cell is P0.

### 2. Vocabulary Consistency (the upgrade)

Signature terms that appear in one document must appear in ALL documents.

| Term | Pitch Deck | Brief | SOW |
|------|-----------|-------|-----|
| "Nuclear Renaissance" | ✅ Slide 1 title | ✅ Executive summary | ✅ Background section |
| "Compliance Moat" | ✅ Slide 1 subtitle | ⚠️ Not present | ⚠️ Not present |
| "HARBOR Compliance Framework" | ⚠️ Not present | ✅ §5 intro | ⚠️ Not defined |
| "37 AI Agents" | ✅ Slide 5 | ✅ §6 | ⚠️ Not mentioned |
| "FSO-credentialed team" | ⚠️ Not present | ⚠️ Not present | ⚠️ Not present |

**Fix:** After building the vocabulary matrix, add the missing terms. "Compliance Moat" should appear in the brief's executive summary. The SOW should define "HARBOR Compliance Framework." The brief should have a "HARBOR Team Capabilities" subsection.

### 3. CTA Consistency (the ask)

The call to action must be the same outcome, expressed at different levels of detail for each audience.

| Document | Right |
|----------|-------|
| **Pitch Deck** | "Authorize CLINs 0000, 0001, and 0002 today. $55K begins immediately. No long-term commitment until you see what we deliver." |
| **Brief** | "The ask: Jacob authorizes Phase A (CLINs 0000, 0001, 0002). Everything else contingent on discovery. Doug gets tentative approval. SOW signed within 1 week." |
| **SOW** | "Immediate Authorization box at top: Phase A is authorized upon signature. Phase B requires mutual agreement after CLIN 0000 completion." |

**Wrong:** Pitch deck says "Authorize the Discovery Sprint" while brief says "Authorize Phase A" while SOW has no framing. This confuses stakeholders who read multiple documents.

### 4. Narrative Arc Consistency (the story)

The pitch deck's slide order should be the brief's section order. Don't tell different stories.

| Pitch Deck Slide | Brief Section |
|-----------------|---------------|
| Slide 1: Nuclear Renaissance | §2: Nuclear Renaissance |
| Slide 2: Market Moving Fast | §3: Current State (OSINT findings) |
| Slide 3: Why Must Happen Now | §3b: Cost of Inaction (new section) |
| Slide 4: The Engagement | §5: Proposed Engagement |
| Slide 5: Why HARBOR | Must come AFTER competitive analysis: §7 (Competitive) → §4 (Amyn Profile) |

**If the brief leads with a section the deck doesn't have**, either add it to the deck or consider whether it's important enough to be a section at all. Every section in the brief should be tracable to a slide or a paragraph in the deck.

## Worked example: Westerman Inc. (July 2026)

Three deliverables for Douglas Henderson (internal sponsor) → Jacob Garrett (CEO):

| Dimension | Initial State | Fixed By |
|-----------|--------------|----------|
| Evidence consistency | ✅ Already matched (adversarial review caught ITAR citation mismatch) | Adversarial gate |
| Vocabulary consistency | "Compliance Moat" in deck only. "HARBOR Compliance Framework" undefined. | Phase 3 unification |
| CTA consistency | Deck: "Authorize $25K Discovery Sprint." SOW: No framing. Brief: "Doug presents → Jacob approves." | Unified to "Phase A: CLINs 0000-0002" |
| Narrative arc | Brief had competitive analysis AFTER Amyn profile. Reordered to tell the same story as deck. | Phase 1 structural change |

## Pitfalls

- **Don't assume one fix propagates.** A single error (e.g., "CMMC-registered RPO") often appears across 4+ files from the same authoring session. After patching the primary file, grep for the root of the error across EVERY file.
- **Don't forget CLIN renumbering.** If the SOW adds a CLIN and shifts all subsequent numbers, the pitch deck's Phase 2-3 ranges AND the brief's pricing table AND the brief's risk register ALL need updating. Search for old ranges, not just exact matches.
- **The internal brief can be more explicit** than the pitch deck. But it cannot CONTRADICT the deck. If the brief mentions a risk the deck doesn't, the deck isn't wrong — but the brief adds depth. If the brief says "$55K entry" and the deck says "$25K entry," one of them is wrong.
