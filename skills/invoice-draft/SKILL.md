---
name: invoice-draft
description: Generate a HARBOR-branded invoice for a fixed-scope productized engagement (Harvest Sprint, Architect Workshop, Build Pilot, Federal Activation Audit, Advisor Retainer). Outputs Markdown invoice with payment terms, Stripe payment link slot, and HARBOR brand. Pipes to /deck-to-pdf for client delivery.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
model: sonnet
user-invocable: true
---

# /invoice-draft — Productized Engagement Invoice Generator

**Born from the Apr 10 productization audit** — HARBOR delivered 7 engagements for $0 in revenue across early 2026 because invoicing was ad-hoc and engagement scope was implicit. This skill makes invoicing mechanical, scope explicit, and payment terms enforceable.

## When to Use

- An engagement deliverable has been accepted by the client
- A retainer cycle has begun (Advisor Retainer monthly)
- A Build Pilot milestone has been reached
- An advance has been agreed for a Harvest Sprint or Architect Workshop

## When NOT to Use

- The work is unpaid (relationship plays, intros, community work)
- The engagement is still in proposal stage (use `/portfolio-deck` instead)
- The client has not yet signed an SOW or accepted scope (resolve that first)

## The Five Engagement Models (Pricing Source of Truth)

These are the only models. If a client engagement doesn't fit one of these, that's a scope problem — flag to CEO before invoicing.

| Model | Price | Duration | Payment Terms | Trigger |
|-------|-------|----------|---------------|---------|
| **Harvest Sprint** | $15,000 | 14 days | 50% on start, 50% on delivery | Client signs SOW |
| **Architect Workshop** | $25,000 | 30 days | 50% on start, 50% on go/no-go decision | Client signs SOW |
| **Build Pilot** | $50,000 | 90 days | 30% on start, 30% at midpoint, 40% on first paying customer | Client signs SOW |
| **Federal Activation Audit** | $12,500 | 21 days | 100% on delivery (net 14) | Client signs SOW |
| **Advisor Retainer** | $5,000/month | Recurring (month 6+ only after Build Pilot) | Monthly, net 14 | Build Pilot complete + retainer SOW signed |


## Execution

This skill dispatches to **ledger-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `HARBOR_portfolio/<slug>/engagement.md (verify scope + active status)`
  - `operations/practice/pricing/productized-engagements-v1.md (source of truth)`
  - `operations/practice/billing/templates/ (invoice template)`
  - `operations/practice/billing/ledger.md (append row after draft)`

### Step 3 — Dispatch to ledger-agent

Call the **Agent** tool with:

- `subagent_type`: `ledger-agent`
- `description`: `"Draft a HARBOR invoice for a productized engagement milestone"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/invoice-draft <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/invoice-draft/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `Markdown invoice written to operations/practice/billing/invoices/<YYYY-MM-DD>-<slug>-<model>.md + ledger row appended`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

If user requested PDF delivery: after agent returns, invoke /deck-to-pdf on the invoice path.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what ledger-agent reads as its authoritative reference when executing this skill.

## Invocation

```
/invoice-draft <client-slug> <engagement-model> [--milestone <description>]
```

Examples:
```
/invoice-draft focus_consulting "Federal Activation Audit"
/invoice-draft bravent "Build Pilot" --milestone "30% start payment"
/invoice-draft axoltl "Advisor Retainer" --milestone "April 2026 retainer"
```

If `client-slug` or `engagement-model` is omitted, ask via AskUserQuestion. Slug must match an existing directory under `HARBOR_portfolio/`.

## Workflow

### Step 1: Validate Engagement

Read `HARBOR_portfolio/<client-slug>/engagement.md` (created by delivery-agent). Verify:
- The model in the invoice request matches `engagement.md`
- The engagement status is `active`
- No `**SCOPE DRIFT**` flags are unresolved

If any check fails, STOP and report to CEO. Do not invoice into a drift situation — it locks in unpaid extras.

### Step 2: Gather Invoice Details

Use AskUserQuestion to confirm:
- Invoice number (auto-suggest: `HARBOR-<YYYY>-<NNN>` based on highest existing invoice in `operations/practice/billing/invoices/`)
- Issue date (default: today)
- Due date (default: today + 14 days for net-14 terms)
- Specific milestone description (if not passed via flag)
- Stripe payment link (paste from Stripe dashboard, or leave as `[STRIPE_PAYMENT_LINK]` placeholder for manual fill)

### Step 3: Read Client Billing Info

Read `HARBOR_portfolio/<client-slug>/billing.md` if it exists. If not, prompt for:
- Legal entity name (the company being billed, not the contact person)
- Billing email
- Billing address (optional)
- Tax ID / EIN (if W-9 was exchanged)

Save the answers to `HARBOR_portfolio/<client-slug>/billing.md` for next time.

### Step 4: Generate the Invoice

Output a Markdown file at:
```
HARBOR_portfolio/<client-slug>/billing/HARBOR-<YYYY>-<NNN>.md
operations/practice/billing/invoices/HARBOR-<YYYY>-<NNN>.md  (mirror copy for global tracking)
```

Format:

```markdown
# Invoice HARBOR-<YYYY>-<NNN>

**Issue date:** YYYY-MM-DD
**Due date:** YYYY-MM-DD (net 14)
**Engagement:** <Model> — <description>

---

**FROM**
HARBOR Initiative
[Legal entity name from brandkit]
ap@harborgovcon.com
EIN: [from brandkit]

**TO**
<Client legal name>
<Client billing email>
<Client billing address>

---

## Services

| # | Description | Amount |
|---|------------|--------|
| 1 | <Engagement model> — <milestone> | $X,XXX.XX |
|   | **Total** | **$X,XXX.XX** |

## Payment Terms

Net 14. Payment due by YYYY-MM-DD.

**Pay online:** [Stripe payment link]

**ACH / Wire:** [bank details from brandkit]

**Check:** Make payable to "HARBOR Initiative" and mail to [address].

---

## Notes

<Optional: thank-you note, scope reminder, next milestone>

---

*Invoice generated YYYY-MM-DD. Questions: ap@harborgovcon.com*
```

### Step 4.5: Editorial Lint (BLOCKING gate, LRN-20260411-014)

The invoice Markdown has free-text fields (Notes, milestone description) that are client-facing. Run the editorial lint before converting to PDF:

```bash
INV="HARBOR_portfolio/<client-slug>/billing/HARBOR-<YYYY>-<NNN>.md"

grep -n -P '[\x{2013}\x{2014}]' "$INV" && echo "BLOCK: em/en dash in invoice" && exit 1
grep -n ' -- ' "$INV" && echo "BLOCK: double-hyphen in invoice" && exit 1
grep -n -i -E 'rebuild|rebuilt|single sharpest|existential anchor|mind.blow|unprecedented|groundbreaking' "$INV" && echo "BLOCK: banned phrase in invoice" && exit 1
grep -n -P '\bAmy\b(?!n)' "$INV" && echo "BLOCK: Amy not Amyn in invoice" && exit 1

# Cross-client leak grep
python3 <<PY
import re
aliases = {}
current = None
with open("admin/memory/portfolio-aliases.md") as fh:
    for line in fh:
        m = re.match(r"^###\s+(.+)$", line)
        if m: current = m.group(1).strip(); aliases[current] = []; continue
        m = re.match(r"^-\s+(.+?)(?:\s*\(|$)", line)
        if m and current: aliases[current].append(m.group(1).strip())

this_slug = "<client-slug>"
with open("$INV") as fh: content = fh.read().lower()
leaks = []
for slug, alist in aliases.items():
    if slug == this_slug: continue
    for alias in alist:
        if alias.lower() in content: leaks.append(f"{slug}: {alias}")
if leaks:
    print("CROSS-CLIENT LEAK in invoice:")
    for l in leaks: print(f"  {l}")
    exit(1)
PY
```

If any gate fires, fix the Markdown before proceeding to PDF conversion.

### Step 5: Convert to PDF

Pipe to `/deck-to-pdf`:
```
/deck-to-pdf HARBOR_portfolio/<client-slug>/billing/HARBOR-<YYYY>-<NNN>.md
```

### Step 6: Update Billing Ledger

Append to `operations/practice/billing/ledger.md`:

```markdown
| Invoice | Client | Engagement | Issued | Due | Amount | Status |
|---------|--------|------------|--------|-----|--------|--------|
| HARBOR-2026-001 | Focus Consulting | Federal Activation Audit | 2026-04-15 | 2026-04-29 | $12,500.00 | Sent |
```

### Step 7: Present to CEO

Show CEO:
- Invoice path (Markdown + PDF)
- Engagement model + milestone
- Amount + due date
- Payment link (or placeholder if not yet generated)
- Recommended cover email draft (run `/email-lint` first)

**Pineapple Protocol applies to sending the invoice.** Never email the invoice directly. CEO presents to Amyn, Amyn confirms with codeword + multi-word affirmation.

---

# Status Tracking

After an invoice is sent, the ledger row gets updated by the **ledger-agent** (not this skill). States:

| Status | Meaning |
|--------|---------|
| Draft | Generated but not yet sent |
| Sent | Email delivered to client |
| Viewed | Client opened the email (if Stripe link tracking is on) |
| Paid | Stripe webhook fired or manual payment confirmed |
| Overdue | Past due date, no payment |
| Disputed | Client raised an issue |
| Written off | Decision to abandon collection |

## Limitations

- **Does not handle multi-currency.** USD only. International clients need a manual override on the wire details.
- **Does not handle sales tax.** HARBOR engagements are services-only and not subject to TX state sales tax. Reconfirm if any product/SaaS revenue is invoiced through this skill.
- **Does not generate Stripe payment links automatically.** Manual paste from Stripe dashboard for now. Future: API integration once volume justifies it.
- **Does not handle credit memos or refunds.** Those go through the ledger-agent directly with a separate flow.
- **Does not handle 1099 reporting.** Year-end 1099-NEC compilation is a ledger-agent quarterly task.

## See Also

- `operations/practice/pricing/productized-engagements-v1.md` — Source of truth for engagement models, pricing, scope
- `feedback_productized_engagement_pattern.md` — Why fixed-scope engagements replaced free reports + retainer asks
- `delivery-agent.md` — Owns the engagement scope file this skill reads from
- `ledger-agent.md` — Owns post-invoice tracking, payment status, collections
- `/deck-to-pdf` — Used by Step 5 for PDF generation
- `/email-lint` — Required for any cover email before sending
