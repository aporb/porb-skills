# FAR Revolutionary Overhaul — XML Extraction Patterns

This reference captures the concrete extraction patterns used for the EO 14275 FAR RFO analysis (June 2026). Use as a template for similar FAR rulemaking analysis.

## The 4 Published Rules (Phase 2, June 23, 2026)

| FR Number | FAR Parts | FR Pages | Comments Due |
|-----------|-----------|----------|-------------|
| 2026-12559 | 1, 2, 4, 33, 39, 40, 52, 53 | 37550–37634 | 2026-07-23 |
| 2026-12560 | 6, 7, 10, 18, 26, 37, 41, 52 | 37636–37674 | 2026-07-23 |
| 2026-12561 | 5, 24, 29, 52 | 37676–37695 | 2026-07-23 |
| 2026-12562 | 3, 49 | 37698–37764 | 2026-07-23 |

Total: 20 FAR parts across 4 rules. Part 52 appears in ALL 4 rules (cross-cutting).

## Section Header Variations

Different rules in the same rulemaking used different section header formats:

```
# Format 1 (most common):
"B. Summary of Changes to FAR Part 1"

# Format 2 (used in Rule 2026-12560):
"B. FAR Part 6"

# Format 3 (used in Rule 2026-12562):
"B. Summary of Proposed Changes to FAR Part 3"
```

The unified regex that catches all three:

```
r'^[ \t]*([A-Z])\. (?:Summary of (?:Proposed )?Changes to )?FAR Part (\d+)'
```

## File Sizes and Extraction Approach

### Discussion Sections (small, analysis-ready)
- Most per-part discussions: 200–12,000 chars
- Safe to read whole file into subagent context

### Regulatory Text Sections (large, trim before analysis)
- Part 52 combined: ~120,000 chars (all 4 rules)
- Part 53: ~69,000 chars (forms list)
- Trim at "List of Subjects in 48 CFR" or "Therefore, OFPP" markers

### PRA Section Filtering
PRA sections duplicate part numbers and cause false matches. Filter them out:

```python
cut_pos = len(discussion_only)
for marker in ['IV. Executive Orders', 'V. Executive Orders', 
               'Paperwork Reduction Act', 'D. Comments Regarding Paperwork Burden']:
    idx = discussion_only.find(marker)
    if idx > 0 and idx < cut_pos:
        cut_pos = idx
```

## Part 52 Consolidation Pattern

Part 52 appears in all 4 rules. Always consolidate before analysis:

```python
part52_files = {
    '2026-12559': '/tmp/far_discussion/2026-12559_Part52.txt',
    '2026-12560': '/tmp/far_discussion_v2/2026-12560_Part52.txt',  # use v2 if re-extracted
    '2026-12561': '/tmp/far_discussion/2026-12561_Part52.txt',
    '2026-12562': '/tmp/far_discussion/2026-12562_Part52.txt',
}
```

## Impact Rating Convention

Used in the HTML briefing:
- `<span class="impact-high">HIGH</span>` — Direct compliance cost, system changes, or strategic risk
- `<span class="impact-med">MEDIUM</span>` — Operational changes needed, moderate cost
- `<span class="impact-low">LOW</span>` — Editorial/formatting changes only, no compliance impact

## Analysis Agent Dispatch Strategy

For 20 parts with 3 concurrent agent limit:

1. Group parts by rule (logical grouping)
2. Dispatch batches of 3 parts at a time via `delegate_task(tasks=[...])`
3. Each subagent reads its file from `/tmp/` filesystem
4. Collect all results, then synthesize into final HTML briefing

## FAR RFO Part Topics (Quick Reference)

| Part | Title | Rule |
|------|-------|------|
| 1 | Federal Acquisition Regulations System | 12559 |
| 2 | Definitions | 12559 |
| 3 | Improper Business Practices | 12562 |
| 4 | Administrative Matters | 12559 |
| 5 | Publicizing Contract Actions | 12561 |
| 6 | Competition Requirements | 12560 |
| 7 | Acquisition Planning | 12560 |
| 10 | Market Research (now RESERVED) | 12560 |
| 18 | Emergency Acquisitions (now RESERVED) | 12560 |
| 24 | Protection of Privacy/FOIA | 12561 |
| 26 | Other Socioeconomic Programs | 12560 |
| 29 | Taxes | 12561 |
| 33 | Protests, Disputes, Appeals | 12559 |
| 37 | Service Contracting | 12560 |
| 39 | Information and Communication Technology | 12559 |
| 40 | Sustainability and Environmental (NEW) | 12559 |
| 41 | Acquisition of Utility Services | 12560 |
| 49 | Termination of Contracts | 12562 |
| 52 | Solicitation Provisions and Clauses | ALL |
| 53 | Forms | 12559 |
