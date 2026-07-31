# Mode B Worked Example: Leatherneck Federal Consulting Competitive Scan

**Date:** July 18, 2026  
**Opportunities:** DARPA DICE (HR001126S0010) + State Dept DFOP0018157

## Pattern Summary

Two simultaneous opportunity-specific competitive scans for a new SDVOSB. One BAA (DARPA), one cooperative agreement (State Dept).

## Query Patterns Used

### DARPA DICE — Contract Search

```bash
# Contract awards with AI/multi-agent keywords under DARPA
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["A","B","C","D"],
      "time_period": [{"start_date": "2020-01-01", "end_date": "2026-07-18"}],
      "agencies": [{"type": "awarding", "tier": "subtier",
                     "name": "Defense Advanced Research Projects Agency"}],
      "naics_codes": ["541715"]
    },
    "fields": ["Award ID", "Recipient Name", "Description", "Award Amount",
               "Start Date", "End Date", "NAICS Code"],
    "sort": "Award Amount", "order": "desc", "limit": 20
  }'
```

### State Dept DFOP0018157 — Grant Search

```bash
# Grant/cooperative agreement awards with EXBS/nonproliferation keywords
curl -s -X POST "https://api.usaspending.gov/api/v2/search/spending_by_award/" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "award_type_codes": ["02","03","04","05"],
      "time_period": [{"start_date": "2020-01-01", "end_date": "2026-07-18"}],
      "agencies": [{"type": "awarding", "tier": "subtier",
                     "name": "Department of State"}],
      "keywords": ["export control", "nonproliferation", "EXBS",
                   "strategic trade", "diversion", "counterproliferation"]
    },
    "fields": ["Award ID", "Recipient Name", "Description", "Award Amount",
               "Awarding Sub Agency", "Start Date", "End Date"],
    "sort": "Award Amount", "order": "desc", "limit": 15
  }'
```

## Parallel Search Strategy

Launched 6 simultaneous web searches in the first wave:
1. DARPA DICE BAA details and PM background
2. DARPA IPTO AI/multi-agent performers (small business focus)
3. Related DARPA programs (ACE, OFFSET, CODE, MATHBAC)
4. State Dept EXBS contractors and incumbents
5. State Dept data analytics/AI contractors
6. State Dept grant awardees in nonproliferation space

## Key Competitive Intel Discovered

### DARPA DICE
- PM: Dr. Susmit Jha — joined IPTO Aug 2025, formerly Technical Director at SRI International
- SRI International is the #1 competitive threat (PM's former employer)
- STR LLC ($46.9M JAWS award), Kudu Dynamics ($8.1M HACCS), JHU/APL ($231M DARPA support) are all well-positioned
- TA3 (T&E) is competed separately — lower barrier for new entrants
- Realistic path: subcontractor to university prime, or TA3 prime

### State Dept DFOP0018157
- Culmen International — EXBS prime since 2009, $23.2M current schedule, but NOT a data analytics firm
- CTP Inc. — EXBS IDIQ holder since 1993, export compliance SME, but NOT a tech firm
- Improvix Technologies — 8(a) small business, State Dept data analytics past performance, credible tech competitor
- This is a NEW scope (data analytics + AI + app dev + training) — incumbency advantage is limited
- Mode B pitfall validated: both contractors and grants needed for full picture

## Output Structure

The briefing was structured as:
1. Executive summary with winnability assessments
2. Opportunity summary tables for each opportunity
3. PM Intelligence section (DARPA)
4. Competitive Landscape tiered by threat level
5. Related programs table with known performers
6. USAspending.gov award data tables
7. Teaming opportunity matrices
8. Strategic assessment + recommendations
9. Appendix with data sources

Saved to: `~/govcon_research/leatherneck-pipeline/competitive-landscape.md`