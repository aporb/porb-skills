# T2 Analysis Example: EO 14216 — Expanding Access to IVF

This reference shows a complete 8-persona analysis for one document from the 100-doc batch processed in July 2026. Use as a template for new T2 analysis sessions.

## Document Metadata

- **Document Number:** 2025-03064
- **Title:** Expanding Access to In Vitro Fertilization
- **Type:** Executive Order (EO 14216)
- **Signed:** February 18, 2025
- **Words:** 406
- **Term:** Trump T2
- **Cluster:** healthcare
- **Agencies:** HHS, CDC
- **Legal Sig:** medium

## Classification

```python
if 'ivf' in t or 'vitro' in t:
    return 'healthcare', ['HHS'], 'medium'
```

## Derivations

```python
novel = 'notable change'  # medium → not low, not high/landmark
econ_sig = 'moderate'     # medium but not trade/tariff
hist_sig = 'notable'      # medium → not routine, not significant
pol_sig = 'notable'       # medium → not landmark
```

## Sample Analysis Structure (Legal Persona)

```json
{
  "statutory_authority": ["Article II, US Constitution"],
  "constitutional_basis": "Article II (Vesting Clause, Take Care Clause)",
  "legal_framework": "Operates within existing healthcare regulatory framework",
  "delegation_analysis": "Delegates to: HHS",
  "potential_challenges": ["APA compliance", "Statutory authorization"],
  "precedent_analysis": "Consistent with presidential authority in healthcare",
  "separation_of_powers_concerns": "Moderate",
  "regulatory_impact": "Affects CFR titles for healthcare",
  "legal_significance": "medium",
  "legal_summary": "Executive order on healthcare. Sig: medium."
}
```

## Key Patterns Used

1. **`'medium'` significance** produces moderate separation-of-powers, moderate economic impact, notable historical significance
2. **Short doc (406 words)** → timeline tagged as `immediate` vs `phased` for longer docs
3. **No trade keywords** → economic significance stays `moderate` not `major`
4. **Default agencies** fallback to the primary agency (HHS) when classification returns a short list
5. **HTML briefing** at `briefings/individual/2025-03064-deep.html` in Thariq ivory/clay format
