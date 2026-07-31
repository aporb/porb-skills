# Company Charter Adversarial Review Checklist

## When Reviewing a Company Charter / Capability Statement

Company charters differ from PWS-anchored proposal responses. There is no governing PWS — the standard is internal consistency, factual accuracy, and what a prime contractor would expect to see.

### Charter-Specific P0 Checks

1. **GitHub repo count**: Verify via `curl -s https://api.github.com/users/<user> | jq .public_repos`. Flag any discrepancy >10%.
2. **Published books**: Verify via web_search or Amazon. Flag if the book doesn't exist or the title doesn't match.
3. **SBIR status**: "Active" vs "Prior." If the founder says it ended, it's "Prior (completed [date])."
4. **SBIR designation**: Verify the exact agency/sponsor chain. "DAF SBIR PI" ≠ "DoD/DoW CDAO SBIR PI."
5. **SDVOSB claims**: Do NOT let "SDVOSB-eligible" through unless the founder has a VA disability rating. Default to VOSB-eligible.
6. **Protest language**: "Under protest" = active. "Protest survived/denied" = resolved. Verify via GAO docket.
7. **Contract numbers**: If present, verify via USAspending.gov or OrangeSlices AI.
8. **Residential address**: Flag if a full street address is published in a company charter — privacy risk.
9. **"Nearly two decades"**: Calculate from first professional engagement, not degree date. Flag if stretched >2 years.
10. **Bus-factor acknowledgment**: A solo practitioner charter MUST include this. Flag as P0 if absent.
11. **Scope boundaries**: A charter MUST include what the company does NOT do. Flag as P0 if absent.
12. **Past performance attribution**: If contracts were performed as an employee, the charter MUST state this. Ambiguity is P0.

### Charter-Specific P1 Checks

1. **Products vs. repos**: The document should list named products, not GitHub repo names. "FARchat" not "the FARchat repo."
2. **Federal/private balance**: Count the word/paragraph allocation. If they claim 60/40 but the commercial section is 10%, flag it.
3. **Hedging language**: "Architecture-level understanding," "familiarity with," "exposure to" — replace with declarative verbs.
4. **All links hyperlinked**: Every Amazon link, GitHub URL, product URL, and email should be `<a href>`.
5. **Date ordering in past performance tables**: Newest first, chronologically descending. Multi-year spans before single years.
6. **Solo practitioner language**: "Cannot staff" and "cannot serve as prime" foreclose growth. Flag and suggest growth-positive alternatives.
7. **Socio-economic designation**: Should match entity status. Don't claim SDVOSB without rating. Don't claim VOSB without honorable discharge.
8. **Full SAM registration language**: "Pending" is OK but should clarify what can and cannot be done (subcontract = yes, prime = no).
