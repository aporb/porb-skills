# Prime Contractor Project Opportunity List Verification

## Overview

Large EPC/federal prime contractors publish **Project Opportunity Lists** on their supplier-facing websites. These are publicly accessible tables of every current and pending project with procurement contacts, scope descriptions, dates, and registration portals.

**Why this matters for adversarial reviews:** A single scrape of one Project Opportunity List can verify 10-20+ claims in minutes — faster and more reliable than searching each claim individually. This is the single most efficient fact-check pattern for pre-sales decks targeting large primes.

## Contractors Known to Publish Project Opportunity Lists

| Contractor | URL | Notes |
|---|---|---|
| **Bechtel** | `https://www.bechtel.com/supplier/project-opportunities` | Full table, updated weekly. Listed as "Bechtel Public Report" with last-updated timestamp. ~12K chars. Covers Energy, Infrastructure, Nuclear/Security, Mining & Metals. Provides procurement contact names, emails, phone numbers. |
| **AECOM** | `https://www.aecom.com/suppliers/opportunities/` | Check current availability |
| **Jacobs** | Check supplier portal | May require registration |
| **KBR** | Check supplier portal | May require registration |
| **Fluor** | Check supplier portal | May require registration |

## Verification Workflow

### Step 1: Locate the Portal

The typical URL pattern is `<contractor.com>/supplier` or `<contractor.com>/supplier/project-opportunities`. A web search for `<Contractor Name> supplier portal project opportunities` usually lands on the right page.

### Step 2: Scrape the Full Page

These are single-page HTML tables with no pagination or JavaScript rendering. Use web_extract with a generous char_limit to capture the full table.

### Step 3: Search & Cross-Reference

For each claim in the deck under review, search the extracted text for:
- Project name (try variants: full name, abbreviation, acronym)
- Contact email (exact match)
- Contact name (last name is usually enough)
- Key phrase from scope description

**Corroboration logic:**
- ✅ **Project listed + email matches + scope consistent** = CONFIRMED
- ✅ **Project listed + contact different** = possible role change, flag MEDIUM
- ❌ **Project NOT listed** = possible expired, not yet added, or speculative. Flag P2 and note "not in official Project Opportunity List"
- ⚠️ **Project listed + email matches but role described differently** = the deck's pitch angle may not match the actual scope for that project

### Step 4: Check the Update Timestamp

Most portals show a "Last Updated" timestamp. Notes:
- **If < 2 weeks old:** high confidence in contact accuracy
- **If > 1 month old:** contacts may have rotated; flag as medium confidence
- **If not shown:** flag all contacts as unverifiable

## Pitfalls

- **The portal is the source of truth, not the contractor's marketing site.** A press release may describe a project's "vision," but the portal describes current procurement needs. The portal's scope description is what the deck should match.
- **Procurement contacts ≠ decision-makers.** The program SBA contact, procurement manager, and project SVP are three different people at three different org levels. Verify which one the deck claims.
- **Generic mailboxes vs named contacts.** If the portal lists only a generic inbox (e.g., `cm2023@bechtel.com`, `sentinelgbsd_sba@bechtel.com`), the deck should acknowledge this is likely a monitored but not individually-responded-to inbox. Named contacts are higher value.
- **Portal may not cover all business units.** The Bechtel portal covers Energy, Infrastructure, Nuclear/Security, Mining & Metals — but materials, equipment, and corporate services may be on a different system.
- **Job numbers can infer age.** A job number like `26713` (Ras Al Hekma, opened Nov 2024) vs `24590` (WTP, opened Dec 2000) tells you how long the project has been in procurement. Old job numbers may have active but stable procurement cadences — new ones are more likely to need suppliers.