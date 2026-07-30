---
name: nda-draft
description: Generate a HARBOR-branded NDA (Mutual or One-Way) from template. Outputs HTML matching the AXOLTL NDA format already in repo, then pipes to /deck-to-pdf for client delivery. Pre-fills HARBOR party info; prompts for counterparty info.
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
model: sonnet
user-invocable: true
---

# /nda-draft — HARBOR NDA Generator

**Reference implementation:** `HARBOR_portfolio/axoltl_chandler/06-legal/Mutual_NDA_Amyn_AXOLTL_2026_PE.pdf` and the HTML source it was generated from. That format is the gold standard — match it exactly. The Apr 10 NDA editorial cleanup (LRN-20260410-007) caught 9 em-dashes and several editorial drift issues that will not happen again because this skill enforces them at generation time.

## When to Use

- First-touch with a new prospect who needs to share confidential information
- Beginning of a paid engagement (pair with the SOW signing)
- Before a deep technical or financial discovery call where the prospect will share non-public materials
- When a prospect's own NDA is unworkable (overly broad, missing carve-outs, hostile choice-of-law) and HARBOR needs to counter with its own template

## When NOT to Use

- The conversation is at the introductory / "meet for coffee" stage — no NDA yet
- Public information is the only thing being exchanged
- An NDA from the counterparty is acceptable as-is (review, sign, no need to draft your own)

## Two Variants

| Variant | Use For | Both parties bound? |
|---------|---------|---------------------|
| **Mutual** (default) | Most paid engagements, partnerships, joint pursuit teams | Yes — both sides have confidentiality obligations |
| **One-Way (HARBOR receiving)** | When HARBOR is reviewing a prospect's IP, financials, or technical materials and HARBOR has nothing confidential to share | No — only the disclosing party (counterparty) is protected |
| **One-Way (HARBOR disclosing)** | Rare. When sharing HARBOR proprietary frameworks before a paid engagement. | No — only HARBOR is protected |

Default to **Mutual** unless one of the asymmetric cases clearly applies.


## Execution

This skill dispatches to **ledger-agent**. It does not execute the playbook inline. See `.claude/skills/SKILL-PATTERN.md` for why.

### Step 1 — Resolve inputs

Parse arguments from the invocation. For each missing required input, use `AskUserQuestion` (max 4 per call, 2-3 rounds if needed). Do not guess.

### Step 2 — Gather local context

Read these files yourself so you can include their contents or paths in the dispatch prompt:
  - `HARBOR_portfolio/<slug>/ (counterparty folder; create 06-legal/ if missing)`
  - `operations/practice/legal/templates/ (NDA templates)`
  - `operations/practice/legal/ndas-ledger.md (append entry)`
  - `operations/practice/brand/ (HTML styling)`

### Step 3 — Dispatch to ledger-agent

Call the **Agent** tool with:

- `subagent_type`: `ledger-agent`
- `description`: `"Draft a HARBOR NDA (Mutual or One-Way) for a portfolio counterparty"`
- `prompt`: a structured block with (in this order):
  1. **Command as invoked** — `/nda-draft <resolved args>`
  2. **Operator** — `Amyn Porbanderwala (HARBOR founder)`
  3. **Playbook** — `Read .claude/skills/nda-draft/SKILL.md for the detailed workflow. The sections below this Execution block are your authoritative reference.`
  4. **Inputs** — the paths from Step 2, with any values you already resolved
  5. **Expected output** — `HTML NDA at HARBOR_portfolio/<slug>/06-legal/<date>-nda-<variant>.html + ndas-ledger row`
  6. **Hard constraints** — `Run your MANDATORY BOOT SEQUENCE first (timestamp, ledger/memory scan, Pineapple Protocol gate). Do not send any outbound artifact. If any check fails, STOP and report to CEO rather than proceeding.`

### Step 4 — Handle return

Pipe the HTML NDA to /deck-to-pdf for client delivery.

If the agent returns an error or requests clarification, relay to Amyn; do not retry silently.

---

The detailed playbook below is what ledger-agent reads as its authoritative reference when executing this skill.

## Invocation

```
/nda-draft <portfolio-slug> [--variant mutual|oneway-receiving|oneway-disclosing]
```

Examples:
```
/nda-draft silverlight_jabbar
/nda-draft new_prospect --variant oneway-receiving
```

If `portfolio-slug` is omitted, ask via AskUserQuestion. If the directory doesn't exist, create it: `HARBOR_portfolio/<portfolio-slug>/06-legal/`.

## Workflow

### Step 1: Gather Counterparty Info

Use AskUserQuestion (4 questions max per call) to collect:

**Round 1:**
- Counterparty legal entity name (the company, not the contact person)
- Counterparty signatory name and title
- Counterparty signatory email
- Counterparty business address (street, city, state, zip)

**Round 2 (if any are unclear):**
- Effective date (default: today)
- Term length (default: 2 years confidentiality, 5 years for trade secrets)
- Choice of law (default: Texas — HARBOR's home state)
- Any specific carve-outs the counterparty has requested

Save the answers to `HARBOR_portfolio/<client-slug>/06-legal/nda-counterparty.md` so future NDAs for the same counterparty don't re-prompt.

### Step 2: Read HARBOR Party Info

From the brand kit (already in repo):
- Legal entity: HARBOR Initiative
- Signatory: Amyn Porbanderwala, Founder
- Email: ap@harborgovcon.com
- Business address: [from brandkit]
- State of formation: Texas

### Step 3: Read the Template

Read `operations/practice/legal/templates/nda-mutual-template.html` (or oneway variants). If the template doesn't exist, bootstrap it from the AXOLTL reference NDA HTML by:
1. Reading `HARBOR_portfolio/axoltl_chandler/06-legal/` for the source HTML
2. Stripping AXOLTL-specific values
3. Replacing them with `{{counterparty_name}}`, `{{counterparty_signatory}}`, `{{effective_date}}` placeholders
4. Saving as `operations/practice/legal/templates/nda-mutual-template.html`
5. **Run /email-lint editorial rules across the template** — no em-dashes, no rebuild language, no AI-tells. Per LRN-20260410-007, this is a hard rule.

### Step 4: Render the NDA

Substitute placeholders in the template. Output to:
```
HARBOR_portfolio/<client-slug>/06-legal/Mutual_NDA_HARBOR_<CounterpartyShortName>_<YYYY>.html
```

Example: `Mutual_NDA_HARBOR_Silverlight_2026.html`

### Step 5: Editorial Lint Pass (BLOCKING gate, LRN-20260411-014)

The NDA is a client-facing document and gets the same editorial rules as a client email, deck, and briefing. This is NOT a soft check. It BLOCKS rendering if it fails.

```bash
NDA="HARBOR_portfolio/<client-slug>/06-legal/Mutual_NDA_HARBOR_<CounterpartyShortName>_<YYYY>.html"

# Hard editorial rules (aligned with /email-lint and ceo-briefing render.mjs)
grep -n -P '[\x{2013}\x{2014}]' "$NDA" && echo "BLOCK: em/en dash in NDA" && exit 1
grep -n ' -- ' "$NDA" && echo "BLOCK: double-hyphen in NDA" && exit 1
grep -n -i -E 'rebuild|rebuilt|single sharpest|existential anchor|mind.blow|unprecedented|groundbreaking' "$NDA" && echo "BLOCK: banned phrase in NDA" && exit 1
grep -n -P '\bAmy\b(?!n)' "$NDA" && echo "BLOCK: Amy not Amyn in NDA" && exit 1

# Soft checks (warn, do not block)
grep -n -i "you showed me\|you mentioned" "$NDA" && echo "WARN: redundant shared-context phrase"
grep -n -i "while you're\|on that note\|circling back" "$NDA" && echo "WARN: connective tissue filler"

# Cross-client leak grep against portfolio-aliases.md
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
with open("$NDA") as fh: content = fh.read().lower()
leaks = []
for slug, alist in aliases.items():
    if slug == this_slug: continue
    for alias in alist:
        if alias.lower() in content: leaks.append(f"{slug}: {alias}")
if leaks:
    print("CROSS-CLIENT LEAK in NDA:")
    for l in leaks: print(f"  {l}")
    exit(1)
PY
```

If any hard check fires, fix the TEMPLATE (not just the rendered copy) and re-run. The template at `operations/practice/legal/templates/nda-mutual-template.html` should be clean; violations usually indicate counterparty data (address, name) containing stray characters that look like em-dashes.

### Step 6: Verify 2-Page Constraint

Per ERR-20260410-XXX (the AXOLTL NDA fit-on-2-pages fix), the HTML is configured to render to exactly 2 pages when converted to PDF. Verify:
- Margins match the AXOLTL reference (`@page { margin: 0.5in; }`)
- No Chrome-injected header/footer (`@page { @top-left { content: none; } @top-right { content: none; } }`)
- Font sizes match
- Line spacing matches

If the rendered HTML would overflow 2 pages, reduce margins or condense whitespace BEFORE converting to PDF.

### Step 7: Convert to PDF

```
/deck-to-pdf HARBOR_portfolio/<client-slug>/06-legal/Mutual_NDA_HARBOR_<CounterpartyShortName>_<YYYY>.html
```

Output: same path with `.pdf` extension.

### Step 8: Generate Cover Email

Draft a short cover email for the NDA. Run `/email-lint` on it. Example body:

```
<Counterparty signatory first name> —

NDA attached. HARBOR's standard mutual format. Choice of law is Texas.

If you have a different template you'd prefer to use, send it over and I'll review.

Thanks!
```

### Step 9: Present to CEO

Show CEO:
- HTML source path
- PDF output path
- Cover email draft
- Counterparty info captured

**Pineapple Protocol applies to sending the NDA.** Never email it directly. Wait for codeword + multi-word affirmation.

### Step 10: Update Engagement and Ledger

After send is confirmed:
- Append a `commitments.md` entry: "[ ] **YYYY-MM-DD due** — Countersigned NDA from <counterparty> — source: NDA sent on YYYY-MM-DD"
- Append to `operations/practice/legal/ndas-ledger.md` (a separate ledger from invoices):
  ```markdown
  | Date Sent | Counterparty | Variant | Status | Countersigned | File |
  |-----------|-------------|---------|--------|---------------|------|
  | 2026-04-11 | Silverlight Labs | Mutual | Sent | — | <path> |
  ```

When the countersigned NDA returns, update the row to `Countersigned` with date and the executed file path.

---

## Hard Editorial Rules (Same As Client Emails)

These are mechanically enforced by the lint pass in Step 5. They are hard rules — they BLOCK rendering, they don't warn:

| Rule | Example violation |
|------|------------------|
| Zero em-dashes in prose | "the parties — both bound by..." |
| No "rebuild" / "rebuilt" / "rebuilding" | "rebuilding the assessment process" |
| No "you showed me" / "you mentioned" inside questions | "Did you show me the timeline?" |
| No connective tissue between paragraphs | "While we're at it..." |
| No filler hedging | "It appears that the parties shall..." |

## Carve-Outs (Standard Mutual NDA)

The default mutual NDA includes these carve-outs (information NOT considered confidential):

1. Information already public at the time of disclosure
2. Information known to receiving party before disclosure (with documentation)
3. Information independently developed without reference to confidential information
4. Information lawfully received from a third party without restriction
5. Information required to be disclosed by law or court order (with prompt notice to disclosing party)

If a counterparty asks for additional carve-outs, NEVER add them without Amyn's review. Flag to CEO.

## Choice of Law and Venue

Default: **Texas** (HARBOR's home state).

If counterparty pushes for their state, the answer is "I'm open to it but need to understand the trade-off." Some states (Delaware, New York, California) have well-developed case law and are acceptable. Others may introduce uncertainty.

Never accept a venue that requires HARBOR to defend in a state with no business presence.

## Term Length

Default: **2 years confidentiality, 5 years trade secrets.**

If counterparty asks for shorter, fine. If counterparty asks for longer (e.g., "perpetual"), flag to CEO — perpetual confidentiality obligations are a long-tail risk for a solo operator.

## Limitations

- **Not legal advice.** This skill generates a draft. Amyn signs it. For high-stakes engagements (>$50K, regulated industries, IP-heavy), have a real lawyer review before signing.
- **Does not handle redlines from counterparties.** If the counterparty edits the NDA and sends back, that's a manual review by Amyn. This skill does not produce redline tracking.
- **Does not handle non-disclosure of HARBOR's own proprietary methodology.** The HARBOR framework itself is published in Book 1 — there is nothing to keep secret. Don't try to NDA it.
- **Does not handle non-compete or non-solicit clauses.** Those are separate agreements (NCAs, NSAs) and outside this skill's scope.

## See Also

- `HARBOR_portfolio/axoltl_chandler/06-legal/` — Reference NDA implementation (the gold standard)
- `LRN-20260410-007` — The 9-em-dash editorial cleanup that prompted the editorial lint pass
- `feedback_email_editorial_patterns.md` — The 10 editorial rules
- `ledger-agent.md` — Owns the NDA ledger and follow-up cadence for countersignature
- `delivery-agent.md` — Reads the NDA status from `engagement.md` and surfaces "still awaiting countersig" in pre-call briefs
- `/email-lint` — Same rules apply
- `/deck-to-pdf` — Used by Step 7 for PDF generation
