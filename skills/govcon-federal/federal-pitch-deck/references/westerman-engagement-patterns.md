# Westerman Engagement — Patterns & Decisions (Jul 2026)

This file captures durable patterns from the Westerman pitch deck build (Jul 2026) that generalize to similar engagements.

## Engagement Profile

- **Client:** Westerman — nuclear component manufacturer (UF₆ cylinders), $616M in contracts, 4 locations (Bremen OH, Tulsa OK, Nevada, Oak Ridge)
- **Sponsor:** Doug Henderson (part-owner, reports CEO Jacob Garrett)
- **Phase 1 scope:** Export control assessment + Technology Control Plan + website modernization
- **Phase 1 budget:** ~$55K immediate (websites + TCP discovery)

## Key Decisions

### What Got Vetoed (Don't Repeat)

| Decision | Why Vetoed | Signal |
|----------|------------|--------|
| "How This Came Together" slide (Doug's voice) | Deck is Amyn's narrative — sponsor doesn't pitch from their own slide | User: "Remove Doug's voice from the deck" |
| Separate 5-slide "Jacob Pitch" deck | Redundant — the 22-slide deck IS for Jacob | User: "Why are we creating a new C — Jacob Pitch?" |
| Capability cards on competitive slide | Redundant — repeats Team and Pricing content | User: "It's just repeating stuff" |
| 8-column comparison table | Unreadable at presentation scale | Screenshot feedback: broken headers |
| "FSO-credentialed" on team slide | Not what the client needs | Doug: "We sell export control, not FSO" |
| Exact agent counts | Invites unnecessary precision debate | User pattern: round to ~30 |
| Names in CTA slide | Makes closing dependent on scheduling | User: "Remove names" |
| Stating Centrus acquisition as fact | Not public — could leak | User: "Do we really want to state this?" |
| Exposing 1099/HARBOR structure | Internal plumbing, not client-facing | User: "Remove this" |
| "I was 22 years old" origin story | Age framing weakens credibility | User: "Remove this" |

### What Got Built (Pattern to Reuse)

| Pattern | Detail |
|---------|--------|
| 4-row competitive punch list | HARBOR | Fractional CAIO | Big 4 | CMMC shops — one punch per row, cost-of-inaction header |
| Four-question filter slide | "Do you know where your data lives?" diagnostic — reframes sale as risk management |
| Before/After slide | Two columns, Today vs 14 Days Later, concrete bullet points |
| Risk acknowledgment slide | "What Could Go Wrong" — honest risks + mitigations per risk |
| Section dividers | Letter + one-line summary between each major section |
| Phase Overview footer | One line per slide: which CLINs, which phase, dollar range |
| Pricing bundle framing | Market rate $25K/each → bundle at $15K/each for long-term engagement |

## Sponsor Realignment Flow

When the sponsor gives direction that contradicts scope or another stakeholder:

1. **Trace** — Build a timeline of every claim the sponsor made in conversation
2. **Verify** — Check claims against public data (contract values, DOE participation, nuclear contracts)
3. **Identify sellable scope** — What can this sponsor actually sell to their CEO?
4. **Realign** — Strip content that doesn't match the sellable scope; double down on what does
5. **Re-verify** — Cross-document alignment after every realignment pass

## Doug's Actual Sellable Scope (Westerman)

Despite Doug wanting a full IT transformation (CMMC, M365 GCC High, cyber program), he can only sell two things to Jacob:

1. **Export controls** — TCP implementation (14 days to operational)
2. **Website modernization** — Two broken WordPress sites → secure, modern, export-controlled

Everything else (CMMC, GCC High, cyber program) is future scope — honest on the risk slide but not in the ask.

## Cross-Document Alignment Save

A $25K error in Phase 1 subtotal (SOW said $145K, deck said $70K-$80K) went unnoticed for hours. Fix required updating all three files:
- Deck: 3 separate locations (Phase Overview footer, Pricing slide, math)
- Brief: Base total and breakdown
- SOW: Phase subtotal row and CLIN totals

Lesson: Pricing lives in 3+ places per document. After ANY change, grep for the old number across ALL files.
