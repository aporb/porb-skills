# CMMC Competitive Landscape — July 2026

Compiled from browser research on FutureFeed, PreVeil, and NIST CPRT during the
CMMC L2 Self-Assessment product architecture session (July 20, 2026).

---

## Market Snapshot

CMMC Phase II (L2 with C3PAO assessments) was suspended on July 13, 2026.
L2 Self-Assessment (SPRS submission against NIST 800-171 Rev 2) remains mandatory.
This creates a market window: every micro-business in the DIB that needs self-assessment
but can't afford $500K-$1M GCC High enclaves is looking for a software solution.

## Key Competitors

### FutureFeed (futurefeed.co)

**Tagline:** "Attain. Maintain. Prove It Anytime.™"

**Scale:** 4,086 users, 1,400+ companies, 447 CAGE codes, 300+ partners, 16 MEPs

**Pricing (July 2026):**
- Innovator (≤25 FTEs): $100/mo ($1,196/yr billed annually)
- Standard (26-999 FTEs): $400/mo ($4,796/yr billed annually)
- Enterprise (1,000+ FTEs): Custom annual contract
- All plans: unlimited users, AWS GovCloud (FedRAMP High) data storage

**Core Features:**
- Live SSP management
- POA&M management
- Project management
- CMMC Level 1 support
- Add other frameworks (multi-framework capability)
- Recently announced partnership with Teramis for automated CUI discovery

**Positioning:** Platform for managed compliance programs, not just assessment.
Strong partner/MSP ecosystem ("Powered-by-FutureFeed" partners). Not AI-native —
traditional SaaS with human consultant overlay.

**Key Weakness for Micro-Businesses:** $100/mo Innovator is reasonable, but the
platform still requires significant compliance knowledge to operate effectively.
The "Build Your Plan" pricing wizard on their site offers add-on frameworks
suggesting upselling from a base price, but the core experience is template-based,
not AI-guided.

### PreVeil (preveil.com)

**Tagline:** "The Leading CMMC Compliance Solution. Save 75% vs GCC High."

**Scale:** Over 3,000 defense contractors & C3PAOs. 100+ customers achieved
perfect 110/110 CMMC scores.

**Pricing (July 2026):**
- Basic: Free (5GB encrypted storage, email + file encryption)
- Individual: $25/mo (5TB storage, annual payment required)
- Business: $30/user/mo (HIPAA, FERPA, SOC 2, GLB, FTC, IRS compliance)
- Gov Community: Custom (CMMC L2, DFARS 7012, ITAR, FedRAMP Moderate, FIPS 140-3, AWS GovCloud)
- PreVeil Pass for SMEs: $450/mo (3 Gov Community licenses + Compliance Accelerator with pre-filled CMMC documentation + 1-on-1 compliance support)

**Core Features:**
- End-to-end encrypted Drive (Windows Explorer, Mac Finder, browser)
- End-to-end encrypted Email (Outlook, Gmail, Apple Mail, browser, mobile)
- Compliance Accelerator: pre-filled SSP, CRM, SOPs (documentation bundle)
- Trusted Community DLP
- Admin console with system logs
- Free accounts for 3rd parties (subcontractors don't need paid licenses)
- AWS GovCloud storage (FedRAMP High)

**Positioning:** "GCC High alternative." Their entire pitch is: don't migrate to
GCC High — layer PreVeil on top of your existing M365/Google Workspace. The
encrypted Drive + Email act as a lightweight CUI enclave. The Compliance
Accelerator + GRC module handle the documentation.

**Key Weakness for Our Positioning:** PreVeil IS the infrastructure (encrypted
enclave). Our product thesis is that most micro-businesses don't need
infrastructure — they need guidance. PreVeil solves BOTH for $450/mo. But at
$149/mo for guidance-only (no enclave), we're cheaper and the enclave
infrastructure is PreVeil itself (integration partner, not competitor).

### NIST CPRT (Free Reference Tool)

**URL:** csrc.nist.gov/projects/cprt/catalog

**What it is:** NIST's free Cybersecurity and Privacy Reference Tool. Interactive
browsing of NIST SP 800-171 control data in Excel/JSON export formats. No
assessment workflow, no SSP generation, no SPRS calculator — just the raw
control text in machine-readable format.

**Relevance:** This is the "free alternative" our $149/mo product competes
against. The value prop is: "CPRT gives you the controls. We give you the answers."

### Other Notable Players (Not Researched in This Session)
- **Exostar** — Identity and access management for defense supply chain
- **Summit 7** — MSP + compliance platform, GCC High-focused
- **Kojensi** — archTIS product for secure collaboration + CUI handling
- **Totem** — CMMC compliance automation platform
- **Coalfire** — C3PAO + compliance services (not SaaS)

---

## GCC High vs Lightweight Alternatives — The Core Strategic Question

### GCC High (Full Enclave)
- **Cost:** $500K-$1M build, $50-100K/year ongoing
- **Tenant provisioning:** 3-6 months
- **Required for:** CUI at rest at scale, ITAR, C3PAO assessment track, prime contractors
- **Who sells it:** MSPs (Summit 7, etc.), Microsoft partners
- **Market:** ~5% of DIB contractors (primes + sub-primes with heavy CUI)

### PreVeil (Lightweight CUI Enclave — SaaS)
- **Cost:** $450/mo (PreVeil Pass) to $X/mo (Gov Community, custom)
- **Setup:** Days, not months
- **Required for:** Handling CUI in email/files without GCC High migration
- **Who sells it:** PreVeil direct + partner network
- **Market:** ~20% of DIB contractors (handle CUI but can't afford GCC High)

### Policy Templates + DIY (No Enclave)
- **Cost:** $0-2K (template packs, PTAC guidance)
- **Setup:** Self-service, 200-400 hours of labor
- **Required for:** Self-assessment only, no CUI at rest
- **Who sells it:** Nobody (this is the gap — no one owns this segment)
- **Market:** ~75% of DIB contractors (want to be compliant, don't handle CUI at rest)

### Our Product Thesis: The "Guidance Layer"
The product sits BETWEEN PreVeil and DIY — a $149/mo SaaS platform that guides
the user through self-assessment, auto-generates their SSP, calculates their SPRS
score, and tells them whether they need PreVeil, GCC High, or nothing. It is NOT
an enclave. It is NOT just templates. It is AI-powered guidance that reduces the
200-400 hour DIY gap to ~40 hours.

---

## Pricing Benchmarks

| Product | Monthly Price (Entry) | Annual Cost | Per-User? | GovCloud? |
|---------|----------------------|-------------|-----------|-----------|
| FutureFeed | $100 (≤25 FTE) / $400 (26-999) | $1,196 / $4,796 | No (unlimited users) | Yes (AWS GovCloud FedRAMP High) |
| PreVeil Pass | $450 (SMEs) | $5,400 | 3 licenses included | Yes (AWS GovCloud) |
| PreVeil Business | $30/user/mo | $360/user/yr | Yes | Yes |
| HARBOR (proposed) | $149-199 | $1,788-2,388 | No (unlimited users) | Commercial (no CUI stored) |

**Pricing sweet spot:** $149/mo is 1/3 of FutureFeed Standard, 1/3 of PreVeil
Pass, and positions as "affordable AI-guided compliance" vs "enterprise compliance
management platform."

---

## Phase II Suspension Market Window

**What happened:** July 13, 2026 — CMMC Phase II (L2 with C3PAO assessments) was
suspended. L2 Self-Assessment remains mandatory.

**Market implications:**
1. Every DIB contractor that was planning C3PAO assessment now needs self-assessment
   as an interim step
2. The "just wait and see" crowd now has to actually do something (self-assessment
   has a real deadline)
3. When Phase II restarts (estimated late 2026-2027), every self-assessed contractor
   becomes a C3PAO upgrade lead
4. Products that capture self-assessment users now get automatic upgrade pipeline
   when C3PAO certs become mandatory again

**Strategic positioning:** "Get self-assessment done now. When Phase II restarts,
you'll already be halfway to C3PAO certification because your SSP, POA&M, and
evidence are all in one platform."
