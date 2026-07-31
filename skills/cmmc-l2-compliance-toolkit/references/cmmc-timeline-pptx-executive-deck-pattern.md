# CMMC Timeline PPTX — Executive Deck Pattern

**When to use:** Building a CMMC L2 certification timeline presentation for executive leadership (Sr. Director level). The audience needs a business-focused deck — not a technical audit report. This reference captures the structure, palette, and content patterns that worked for the Brian Gregorio (July 2026) deck.

## Deck Structure (10 Slides)

| # | Slide | Purpose |
|---|-------|---------|
| 1 | Title | Dark navy background. Company name + "CMMC Level 2 Certification: Timeline & Implementation Path." Subtitle with target date. Prepared-for line with executive name. |
| 2 | Executive Summary | Stat cards (readiness %, target, effort, deadline). TL;DR paragraph. Callout box for the strategic context (e.g., "Brian's direction is to stay ahead despite Phase 2 suspension"). |
| 3 | Where We Are Today | Progress bar (complete vs in-progress vs not started). Two-column: BUILT vs GAPS. Staffing note at bottom. |
| 4 | Seven-Phase Gantt Timeline | Month-axis Gantt with colored bars. 7 phases from Toolkit Build through C3PAO Assessment. Red vertical line for Phase 2 deadline (Nov 2026). Critical path callout at bottom. |
| 5 | Phase 2 Deadline Impact | Big deadline date. Three impact cards (will miss it / BD gap / existing work unaffected). Mitigation note. |
| 6 | Critical Path Detail | Effort breakdown table (SSP fill, evidence collection, SOP refinement, gap assessment). Hours + owner + notes. Dependency callout box in red. |
| 7 | Acceleration Opportunities | 5-row table: lever, time saved, cost/trade-off, feasibility rating, notes. Opportunities to compress timeline. |
| 8 | BD Lead-Time Reference Card | Three scenario cards (L2 Self / C3PAO baseline / accelerated). Bid eligibility decision tree (4-step checklist). |
| 9 | Decisions Required | 7-row decision table: decision, owner, when, status badge (red=urgent PENDING, gold=PLANNED/non-urgent). Summary: "X of Y decisions are urgent." |
| 10 | Regulatory Framework + Next Steps | Two columns: governing regs + next steps. Prepared-by footer. |

## Design Palette: Midnight Executive

```
navy:   "1E2761"  — dark slide backgrounds, table headers
dark:   "0F1535"  — darker variant
ice:    "CADCFC"  — branding text, subtitle on dark
white:  "FFFFFF"  — main text on dark, light slide backgrounds
clay:   "D97757"  — accent (stat numbers, in-progress bars)
gold:   "D4A853"  — emphasis, critical-path bars, callouts
olive:  "788C5D"  — complete/done indicators
rust:   "BC4742"  — urgent status badges, deadline markers
gray:   "8892A4"  — muted metadata
lgray:  "E8ECF1"  — light slide backgrounds, alternating table rows
dgray:  "3A4260"  — card backgrounds on dark slides
```

Typography: Cambria (headers) + Calibri (body). Both render reliably in LibreOffice QA and PowerPoint.

## Key Content Decisions

- **Honest about Phase 2 miss.** Don't sugarcoat that the Nov 2026 deadline won't be met. Call out the ~6-month BD gap explicitly. BD lead-time reference card helps the team plan around it.
- **Stat cards on slide 2.** Four big numbers (readiness %, target date, effort hours, deadline) give the executive a 5-second scan before diving in.
- **Acceleration table shows what it costs.** Each lever has a feasibility rating. "HIGH" in olive green signals easy wins.
- **Decisions table has status badges.** Red = urgent PENDING, gold = PLANNED. The summary line at bottom ("5 of 7 decisions are PENDING and urgent") makes it actionable.
- **Suspension context in callout.** Phase 2 suspension (July 2026) was flagged in a gold italic callout — acknowledges the regulatory shift without undermining the deck's purpose.

## PPTX Generation: Gantt Chart Gotchas

When building Gantt charts with pptxgenjs:

- **Text-on-bar labels: only for bars ≥3 months wide** (≥ ~2.1" at 0.72"/month). Narrower bars get the label clipped or ghosted in LibreOffice rendering.
- **Deadline marker: use a thin vertical rectangle + text ABOVE the chart area.** Text placed below the chart collides with footers and gets read as a stray element.
- **Bar colors: avoid `PALETTE.lgray` (`#E8ECF1`) on white backgrounds** — too low contrast. Use `"B0B5C0"` for future-phase bars to maintain visibility.
- **Zebra striping with alternating rect shapes** (not table objects) gives more control over cell padding in data-heavy slides.
- **Validate with `python scripts/office/validate.py`** after generation, then **visual QA with LibreOffice → pdf → pdftoppm → vision_analyze**. The LibreOffice renderer catches real PowerPoint issues (text overflow, element collision) that schema validation misses.

## Pre-Build Research: Review Call Recordings

Before building an executive deck about CMMC timeline:

1. **Search call transcripts for the executive's name** — what did they actually say they want? What was their stated position?
2. **Check recent 1-on-1 calls** for strategic context (e.g., "Brian wants to move forward despite the suspension")
3. **Cross-reference against internal assessments** (mock C3PAO, gap reports) so the deck doesn't contradict what the executive has been told elsewhere
4. **Parallel research agents work well** for reviewing 10-15 call transcripts simultaneously
