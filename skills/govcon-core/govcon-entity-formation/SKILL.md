---
name: govcon-entity-formation
description: Create LLCs for GovCon. State choice, SAM.gov, anonymity.
---

# GovCon Entity Formation

## When to Use

A client, partner, or the user needs to **create a new legal entity** for federal contracting — a prime bidding vehicle, a subcontracting entity, a holding company, a separate entity for anonymity/privacy reasons, or an LLC to serve as a pass-through for a specific contract vehicle. This skill covers the full process from state selection through formation, registration in SAM.gov, tax classification, and ongoing compliance.

Also triggered when evaluating which state to form in, comparing anonymous LLC options, or when the entity needs to be structured as a disregarded-entity subsidiary of an existing LLC (parent-subsidiary structure).

## The Framework: State Selection

For federal contracting entities, four states dominate: **Wyoming, Delaware, Nevada, and New Mexico**. Each has different tradeoffs across the dimensions that matter for GovCon.

### Decision Matrix

| Factor | **Wyoming** ⭐ | Delaware | Nevada | New Mexico |
|--------|--------------|----------|--------|------------|
| **Anonymous formation** | ✅ Members not on Articles of Org | ✅ Members not on Articles | ❌ Initial List of Managers REQUIRED | ✅ Members not on Articles |
| **Anonymous ongoing** | ✅ Only RA + address on annual report | ✅ No annual report (flat $300 tax) | ❌ Annual List REQUIRES members | ✅ **No annual report** |
| **Formation fee** | $100–$104 | $90 | $425 (includes initial list + biz license) | $50 |
| **Annual state cost** | $60 (annual report) | **$300** (franchise tax, flat) | **$350** ($150 list + $200 biz license) | **$0** |
| **Registered agent (Northwest)** | $125/yr | $125/yr | $125/yr | $125/yr |
| **3-year total** | **$631** | $1,340 | $1,850+ | **$425** |
| **Legal precedent** | Strong | **Gold standard** (Chancery Court) | Good | Limited |
| **State income tax** | 0% | 8.7% corp (not on non-DE income) | 0% (Commerce Tax >$4M rev) | 0% (corp income tax, not LLC) |
| **GovCon credibility** | Good | Best (investors know DE) | Good | Low (primes/banks skeptical) |

### Which State to Choose

| If your priority is… | Choose |
|---|---|
| **Best overall balance** for a GovCon subcontract entity | **Wyoming** — low cost, anonymous, strong case law, 0% state tax |
| **Absolute lowest cost** and strongest anonymity | **New Mexico** — $50 formation, $0 annual, no reporting. Caveat: limited case law, primes may not trust it |
| **Investor/VC/IPO track** | **Delaware** — Gold standard corporate law, $300/yr franchise tax but worth it for exit-readiness |
| **Nevada must be avoided** | It sounds good (0% tax) but requires **public manager listing** on the Annual List — defeats anonymity and adds $350+/yr cost |

## Anonymity & Privacy

### What "Anonymous" Means Here

Anonymity is at the **state public record level** — the LLC's formation documents filed with the Secretary of State do NOT list the members/managers by name. Your name only appears on:

1. **IRS documents** (EIN application, tax returns) — not public
2. **Bank KYC** (Know Your Customer checks) — private, bank-only
3. **SAM.gov admin account** (Login.gov identity proofing) — private, GSA-only
4. Contractual documents shared with your prime/client — private by agreement

### How to Achieve It

1. **Use a registered agent's address** as the principal office address — not your home/business address
2. **Hire a formation service** to act as "Organizer" on the Articles of Organization — your name never appears on the public filing
3. **Never list members in the Articles** — in WY, DE, NM the Articles only require: LLC name, registered agent, RA address, organizer name/address (the formation service)
4. **The Operating Agreement is internal** — it names the real members but is never filed with the state

### What About the Corporate Transparency Act / BOI Reporting?

> **As of March 2025**, FinCEN revised the BOI reporting rule under the Corporate Transparency Act. **Domestic U.S. entities (including LLCs) are now EXEMPT** from beneficial ownership reporting. Only foreign entities registered to do business in the U.S. must report.
>
> Source: fincen.gov/boi

This means the CTA **does not** undermine anonymous LLCs formed by U.S. persons in anonymous states.

## Registered Agent Selection

| Provider | Annual Cost | Notes |
|----------|-------------|-------|
| **Northwest Registered Agent** ⭐ | $125/yr | Best for privacy, includes business address for principal office, multi-state discount at 5+ states ($100/yr) |
| Harbor Compliance | $149/yr | Enterprise compliance platform, good for multi-state |
| ZenBusiness | $199/yr | Heavy upselling, sells data |
| LegalZoom | $249–299/yr | Most expensive, sells customer data |

**Always use a professional registered agent** — never your personal address. The registered agent's address becomes the LLC's public address. Northwest is the recommended provider for all four states considered above.

## Ownership Structure: Parent-Subsidiary (Disregarded Entity)

When the contracting entity will be **100% owned by another LLC** (e.g., HARBOR Initiative LLC owns the contracting LLC):

```
Parent LLC (operating entity, has UEI/SAM, does other work)
    │
    100% ownership
    │
    ▼
Contracting Entity LLC (single-member, new entity for this contract)
    • Taxed as a disregarded entity (default for single-member LLC)
    • No separate federal tax return
    • All income/expenses flow to parent's return
    • Parent files Form 1065 (partnership) or 1120-S (S-Corp)
    • Parent eligible for QBI deduction on flow-through income
```

### Key Requirements

| Requirement | Action |
|-------------|--------|
| Separate EIN | Obtain IRS EIN in Contracting Entity's name (not parent's EIN) |
| Separate bank account | Open in Contracting Entity's name with its EIN |
| Separate books/records | QuickBooks/Xero file for Contracting Entity only |
| Contracts in LLC name | All subcontracts, NDAs, proposals in Contracting Entity name |
| No commingling | Parent pays contracting entity's expenses via documented capital contributions or loans |
| Separate insurance | Professional liability, cyber, general liability in Contracting Entity name |
| Operating Agreement | Internal document naming Parent as sole member, manager-managed |

### What NOT to Do

- Do NOT use the parent's EIN for the contracting entity's bank account
- Do NOT commingle funds or sign contracts in the wrong entity name
- Do NOT skip the Operating Agreement — without it, a court may pierce the corporate veil

## Tax Classification Options

| Type | Tax Rate | Forms | Best For |
|------|----------|-------|----------|
| **Disregarded entity** (default SMLLC) | Pass-through → parent's return | Parent files; subsidiary files nothing | **Most GovCon subs** — simple, QBI-eligible |
| Partnership (multi-member) | Pass-through via K-1s | Form 1065 + K-1s | Multiple owners |
| S-Corp election (Form 2553) | Pass-through + payroll | Form 1120-S + K-1s | Self-employment tax savings on distributions; owner on payroll |
| C-Corp election (Form 8832) | 21% flat + dividend tax | Form 1120 | VC/IPO track, retained earnings |

**For a pure subcontracting vehicle**: default disregarded entity is almost always correct. C-Corp is overkill — double taxation, no QBI deduction, 5-year lock-in.

## SAM.gov Registration

### Prerequisites Before Registering

1. ✅ LLC formed and stamped Articles of Organization received
2. ✅ EIN obtained (IRS online, immediate)
3. ✅ Business bank account opened (not strictly required before SAM, but have ready)
4. ✅ Registered agent's address available as physical address

### Registration Process

1. **Create Login.gov account** — needs Amyn (or whoever the admin is) as a real person. Government ID, SSN, phone number required for identity proofing. This is **private** — not displayed in SAM.gov public records.
2. **Register entity in SAM.gov** — provide:
   - Legal business name (exactly as on Articles)
   - Physical address (registered agent's address — PO Box not allowed)
   - EIN
   - NAICS codes (e.g., 541611 Management Consulting)
   - Business type (LLC)
3. **Wait 10–15 business days** for entity validation
4. **Receive UEI + CAGE code** — required to receive any federal contract or subcontract

### What SAM.gov Shows About Your Entity

- Legal business name and physical address
- UEI and CAGE code
- NAICS/PSC codes
- SBA small business certifications
- **No beneficial owner information** — this is not public in SAM.gov

### Anonymous LLC + SAM.gov: Compatibility Check

| Concern | Resolution |
|---------|------------|
| "Will my name be public?" | No. SAM.gov shows entity-level info only. Your name only appears in the admin account (Login.gov), which is private. |
| "What about the registered agent address?" | The RA's address is what appears in SAM.gov as your physical address — not your personal address. |
| "Do I need to disclose my ownership?" | SAM.gov does not have a beneficial ownership disclosure field. |
| "Will the prime/CO know who owns this?" | Only if you tell them (contract terms, kickoff meeting, etc.). The SAM.gov public record does not reveal it. |

## Annual Compliance Calendar

### Wyoming (Recommended)

| Filing | Due | Cost | How |
|--------|-----|------|-----|
| Annual Report | Anniversary month of formation | $60 ($62 online) | WY SOS online |
| Registered Agent Renewal | Anniversary | $125 | Northwest auto-renews |
| Federal Tax | Mar 15 / Apr 15 | N/A | Filed by parent (disregarded entity) |
| State Tax (Texas, if parent is TX entity) | May 15 | ~0.375% of margin >$2.47M | Filed by parent (combined group) |

### New Mexico (Cheapest)

| Filing | Due | Cost | How |
|--------|-----|------|-----|
| **No annual report** | N/A | **$0** | Nothing to file |
| Registered Agent Renewal | Anniversary | $125 | Provider auto-renews |

### Delaware

| Filing | Due | Cost |
|--------|-----|------|
| Franchise Tax | June 1 | $300 flat |
| Registered Agent Renewal | Anniversary | $125 |

### Nevada — Avoid (public listing defeats anonymity)

| Filing | Due | Cost |
|--------|-----|------|
| Annual List + Business License | Anniversary month | $150 + $200 = $350 |
| Registered Agent Renewal | Anniversary | $125 |

## Action Plan (Standard Sequence)

### Phase 1: Formation (Week 1)
1. Choose state (recommended: Wyoming)
2. Engage Northwest Registered Agent for formation + RA service
3. Provide: preferred LLC name, member name (parent LLC), organizer/integration
4. Northwest files Articles of Organization, provides stamped copy
5. Receive stamped Articles + operating agreement template

### Phase 2: EIN & Banking (Week 2)
6. Apply for EIN via IRS Form SS-4 online (free, immediate)
7. Open business bank account in Contracting Entity name with its EIN
8. Draft and execute Operating Agreement (parent as sole member, manager-managed)

### Phase 3: SAM.gov Registration (Week 2–3)
9. Create Login.gov account (admin identity proofing)
10. Register entity in SAM.gov
11. Wait 10–15 business days for UEI + CAGE code

### Phase 4: Subcontract Ready (Week 3–4)
12. Obtain Certificate of Good Standing ($10, WY SOS online)
13. Set up compliance calendar
14. Execute subcontract in Contracting Entity name

## Pitfalls

- **Nevada sounds good but defeats anonymity** — its Annual List of Managers/Members is a public filing. Anyone searching the Nevada SOS can see who owns the LLC. Do not recommend Nevada when privacy is required.
- **New Mexico's lack of annual reporting is a double-edged sword** — primes and banks sometimes view entities with no annual report as less credible or as potential shell companies. WY's $60 annual report signals the entity is maintained.
- **Login.gov admin identity cannot be anonymous** — the SAM.gov account admin must be a real person with government ID. This is private (not in public SAM records) but a real person must undergo identity proofing.
- **Registered agent cost is the same across states** — providers like Northwest charge the same $125/yr regardless of state. Do not let the RA cost drive state selection.
- **Delaware is overkill for a subcontract vehicle** — the $300/yr franchise tax and prestige come at a premium, and the Court of Chancery is rarely needed for a subcontract-only entity. Reserve for VC-backed or IPO-track entities.
- **BOI/CTA is now moot for domestic entities** — as of March 2025, domestic LLCs are exempt. Do not advise clients to worry about this or structure around it.
- **Bank KYC will reveal the beneficial owner** — the anonymity is from the public record, not from banks. When opening an account, the bank will ask for ownership structure and may request the Operating Agreement. This is normal.
- **"No annual report" states can trigger bank flags** — some banks' compliance algorithms flag entities in NM because the lack of reporting is associated with shell companies. Wyoming's annual report is an advantage here, not a cost burden.
- **The subcontract itself will reference the contracting entity** — the anonymity keeps your name off state records. The entity name still appears in the subcontract, in SAM.gov, and potentially in FPDS if the subcontract flows up to the prime's reporting. You are anonymous from the public, not from the contracting parties or the government.

## Support Files

- `references/session-2026-07-26-westerman-llc-research.md` — The session's full research brief covering the Westerman subcontract context, cost comparisons, tax analysis, action plan, and risk mitigation. Useful as a concrete worked example for future entity formation tasks.