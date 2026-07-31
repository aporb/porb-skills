# State Entity Verification — When SAM.gov Is Inaccessible

Use state business registries to cross-verify entity existence, legal name, formation date, and tax registration status when SAM.gov entity search is gated behind sign-in (as of July 2026).

## Texas

### Franchise Tax Account Status Search

**URL:** `https://comptroller.texas.gov/taxes/franchise/account-status/search`

This is the TX Comptroller's public search — no login required. It returns Taxpayer Number, entity name, and ZIP.

**Search by SOS File Number (most reliable):**

```
1. Navigate to the page
2. Type the TX SOS File Number into the "Texas Secretary of State File Number:" field
3. Click "Submit"
```

Returns a table with:
- **Name** — legal entity name (clickable for detail)
- **Taxpayer Number** — 11-digit Comptroller's Taxpayer Number (e.g., `32106002309`)
- **Zip** — 5-digit ZIP

**What this confirms:**
- Entity exists and is registered with the TX Comptroller
- Taxpayer Number is assigned
- ZIP matches canonical address

**Pitfall:** The "Name" link in the results table is JavaScript-rendered and may not navigate to a detail page in headless browsers. The search results table itself is sufficient for verification — it confirms name, Taxpayer Number, and ZIP.

### Alternative: TX SOS Direct

**URL:** `https://www.sos.state.tx.us/corp/sosda/index.shtml` (SOSDirect)

Requires account/login. The Comptroller search is preferable for quick verification.

### Key TX Identifiers (Harbor Initiative LLC example)

| Identifier | Value | Source |
|-----------|-------|--------|
| TX SOS File Number | `806595324` | Formation filing |
| TX Comptroller Taxpayer # | `32106002309` | Franchise Tax search |
| Formation Date | 2026-05-11 | SOS filing |
| ZIP | 77459 | Both SOS + Comptroller |

**Lesson:** The SOS File Number is the most reliable search key across TX systems. It's assigned at formation and never changes. The Taxpayer Number is assigned later (typically 3-4 weeks after formation) and is a separate identifier.

## General Pattern

When SAM.gov is inaccessible and the entity is brand-new (no USAspending data):

1. **State business registry search** — confirms legal existence, formation date
2. **State tax comptroller search** — confirms tax registration, Taxpayer Number
3. **Cross-reference** — do ZIP, entity name, and formation date match canonical records?

If both state sources confirm the entity exists, and the canonical records cite a specific SAM.gov UEI issuance email (date, sender, message ID), the UEI itself is credible even without direct SAM.gov verification. Full SAM *registration* (with CAGE, NAICS/PSC codes) is a separate step from UEI *issuance* — the UEI can be valid while full registration remains pending.
