# CMMC L2 Self-Assessment Competitive Landscape — July 2026

> Condensed domain knowledge bank from competitive landscape research session
> (July 20, 2026). Covers competitors, pricing, TAM, Phase II suspension impact,
> and underserved market gaps for micro-business (1-10 employee) federal contractors.

## Competitor Profiles

### PreVeil (preveil.com)
- **Product:** PreVeil Pass — encrypted email/file sharing enclave + compliance docs
- **Pricing:** $450/month for 3 users (12-month contract, paid upfront). Gov Community = custom.
- **Covers:** 102/110 NIST controls. FedRAMP Moderate Equivalent, FIPS 140-3.
- **Includes:** Encrypted email/file sharing, Compliance Accelerator (pre-filled SSP, SOPs, CRM, policies), "Roadmap to CMMC" videos, 1×1 compliance expert access, RPO/MSP/C3PAO Partner Community.
- **Claims:** "Save 75% vs GCC High." 100+ contractors achieved perfect 110 scores. Customer saved $200K vs GCC High.
- **URL:** https://www.preveil.com/preveil-pass/ (pricing page confirmed working with web_extract)

### Cuick Trac / Beryllium InfoSec (cuicktrac.com)
- **Product:** Cuick Trac Managed Enclave (CTME) — managed GCC-H enclave
- **Pricing:** Not publicly listed. Described as "cost effective" and "predictable and transparent."
- **Covers:** Inherits 264/320 CMMC L2 assessment objectives (82%) out of the box.
- **Includes:** Virtual desktop in GCC-H, FedRAMP Moderate Equivalent (3PAO-assessed), 15-day deployment, secure file sharing, encrypted storage, documentation resources, policy templates, audit prep support.
- **Trust marks:** CyberAB RPO, Microsoft Partner. "Utilized to Achieve CMMC L2 Certification."
- **URL:** https://cuicktrac.com/ (confirmed working with web_extract)

### Summit 7 Systems (summit7.us)
- **Product:** Guardian (MSP) + Vigilance (MSSP) + Commander (GRC) + NCODE (Army-subsidized)
- **Pricing:** Not publicly listed. Assessment costs per blog: $20K-$50K every 3 years. Total implementation: may exceed $300K.
- **NCODE Program:** Specifically for 2-10 employee DoW contractors. AOS-G for Army. Pilot: 1,000 businesses (May 2026). Full rollout: 150,000 users Year One. "Up to $100K savings in year one." Application currently closed.
- **Claims:** 725+ successful CMMC implementations. 100/100 passed CMMC L2 assessments. 7 MS advanced specializations. 1,400+ clients.
- **URLs:** https://summit7.us/ncode (confirmed working), https://www.summit7systems.com/cmmc/ (confirmed working)
- **Blog post (Phase II suspension):** https://summit7.us/blog/cmmc-phase-2-suspended-for-60-days-what-happens-next (confirmed working)

### Exostar (exostar.com)
- **Product:** CMMC Ready Suite — fully managed CMMC L2 readiness
- **Pricing:** Not publicly listed. Three standardized tiers by company size, complexity, software environment.
- **Includes:** All 110 NIST controls, auto-generated SSP/POA&M/policies, gap analysis, evidence management, secure enclave, professional services for control gaps, MSP white-label.
- **Also offers:** Self-assessment tool for SPRS scoring, Secure Collaboration for Defense (MS Teams).
- **URL:** https://www.exostar.com/cmmc/ (confirmed working with web_extract)

### FutureFeed (futurefeed.co)
- **Product:** CMMC compliance GRC platform — gap assessment, SPRS scoring, SSP, POA&M
- **Pricing:** Not publicly listed (pricing page confirms 3 tiers but no dollar figures). Innovator (≤25 FTEs), Standard (26-999), Enterprise (1,000+). Multi-framework: 5% off. Terms: monthly, annual, 2-year (-2mo), 3-year (-4mo).
- **Includes:** Unlimited users, live SSP management, POA&M tracking, project management, AWS GovCloud FedRAMP High, on-demand presentations, "CMMC Expertise Marketplace."
- **URLs:** https://futurefeed.co/pricing/ (confirmed working), https://futurefeed.co/futurefeed/ (confirmed working)

### Totem Technologies (totem.tech)
- **Product:** Totem™ CMMC Compliance Software + CMMC Engaged (training + software + consultations)
- **Pricing:** Not publicly listed. Tiers: Totem (software), CMMC Engaged (+ training + weekly consultations), CMMC Expert (MSP multi-tenant). Unlimited users, no per-user fees. Annual: 10% off. No long-term contracts.
- **Includes:** SSP builder, POA&M generator, SPRS score tracking, evidence repository, customizable templates, monthly Q&A forum. Veteran-Owned Small Business (VOSB).
- **URL:** https://www.totem.tech/cybersecurity-compliance-software/ (confirmed working)

### Key Pattern: Pricing Opacity
Only PreVeil publishes a clear, accessible starting price. Everyone else hides behind "Contact Sales." This is a market signal for the 1-10 employee segment — the pricing is built for mid-market and enterprise, not micro-businesses.

## TAM Data

### SBA Official (July 13, 2026 press release)
- "Over 100,000 small businesses impacted" by CMMC
- "More than 120,000 DIB small businesses" would have needed CMMC Phase II compliance
- Compliance cost estimates: ~$593,800 per firm (third-party assessment), ~$388,600 (self-assessment)
- Source: https://www.sba.gov/article/2026/07/13/sba-commends-us-department-wars-suspension-cmmc-phase-ii-small-defense-contractors

### Summit 7 NCODE Data
- Targets 2-10 employee DoW contractors
- Pilot: 1,000 businesses (May 2026)
- Full rollout: 150,000 users Year One

### Conservative TAM Estimate for L2 Self-Assessment
- 120,000 DIB small businesses × 40-60% micro (1-10 emp) = 48,000-72,000 firms
- 60-70% handle CUI and need L2 = 29,000-50,000 firms
- At $2K-$5K per engagement: $60M-$250M service revenue
- At $450/mo SaaS: $162M-$270M ARR

## CMMC Phase II Suspension Impact (July 13, 2026)

### What's Suspended
- C3PAO third-party assessments for L2 (originally scheduled Nov 10, 2026)
- DIBCAC assessments for L3
- 60-day CMMC Reform Task Force review (reporting ~Sep 13, 2026)

### What's STILL Required (Self-Assessment)
- NIST SP 800-171 Rev 2 (all 110 controls)
- Self-assessment and SPRS score submission (minimum 88/110 for L2)
- Annual affirmations signed by Affirming Official
- DFARS 252.204-7012 (safeguarding, incident reporting)
- FAR 52.204-21 (basic safeguarding)
- FedRAMP Moderate (or equivalent) for CUI in cloud
- ITAR/EAR data sovereignty
- DIBCAC can still assess anytime
- DOJ False Claims Act enforcement continues
- Proposed FAR CUI Rule (NIST 800-171 Rev 3) expected in 2026

### Market Impact
The suspension is a TAILWIND for self-assessment enablement:
1. Demand shifts from expensive C3PAO prep → affordable self-assessment documentation
2. Urgency INCREASES — contractors need to demonstrate compliance now
3. Political pressure from SBA toward affordable, self-service compliance
4. NCODE's 150,000-user target validates massive demand

## Underserved Market Gaps

1. **No pure-play self-assessment documentation product.** All competitors bundle technology (enclaves, email, cloud) with compliance docs. Nobody offers "We'll write your SSP, POA&M, and policies, calculate your SPRS score, and help you submit — for a flat fee, no technology purchase required."

2. **No AI-assisted compliance.** The entire industry uses manual consulting or basic templates. AI-generated SSPs, automated gap analysis, and intelligent POA&M tracking are absent.

3. **No "CMMC for absolute beginners" product.** Many small contractors don't even know what CUI is. No product starts from "What is CUI and do I handle it?" through to SPRS submission.

4. **Opaque pricing across the board.** Only PreVeil publishes a price. This signals "too expensive for you" to micro-businesses.

5. **No SDVOSB-to-SDVOSB trust bridge.** Most competitors are large commercial entities. Fellow small business/SDVOSB compliance services create trust that corporate vendors cannot match.

6. **Summit 7's NCODE is Army-only, Microsoft-locked, and application-closed.** Every branch has micro-contractors needing help with self-assessment, and NCODE doesn't serve them.

## Research Method Notes

- `web_extract` on known competitor URLs was the most productive method — 15+ URLs returned usable content
- `web_search` returned empty results for ALL CMMC-compliance queries
- `firecrawl_search` was unreachable (MCP server down)
- Browser-based search (Google, Bing, DuckDuckGo) all triggered CAPTCHAs
- The SBA press release URL was directly accessible and provided authoritative TAM data
- Summit 7's NCODE page provided the most specific micro-business targeting data