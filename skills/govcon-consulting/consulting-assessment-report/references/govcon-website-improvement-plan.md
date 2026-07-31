# GovCon Website Improvement Plan — Variant Patterns

Session-specific detail for the **website audit + rebuild plan** variant of the consulting assessment (mirror live site → assess → improvement plan). Loaded alongside SKILL.md's core workflow and aesthetic standards (dark theme, phase badges, no framework name in body).

## Report structure (10 sections)

1. **Current-state audit** — what's live, what works, what fails (table per page section).
2. **Tech & infrastructure recon** — registrar, DNS (A/MX/TXT/NS), host, site builder, CDN, TLS, app stack (see brand-kit-extraction `references/spa-crawl-and-host-fingerprinting.md` for fingerprinting).
3. **GovCon gap analysis** — score against the checklist below.
4. **Design-trend application** — adopt vs. avoid for B2G (substance over flash; most consumer trends are wrong for federal buyers).
5. **Positioning strategy** — audience, wedge service, differentiator, set-aside framing, tone.
6. **Rebuild/migration plan** — owner-assigned numbered steps, with an explicit "immediate takedown" step if there's exposure.
7. **Content architecture** — recommended site map with priorities.
8. **Deployment/cutover plan** — DNS records to change vs. leave alone (MX/SPF/M365 TXT — changing them breaks email).
9. **Action plan & checklist** — now / next / later.
10. **Appendix** — mirror path, prototype path/URL, file map.

## GovCon website content checklist (gap-analysis yardstick)

What contracting officers and primes actually look for:
- **Capabilities statement PDF** (1 page, branded, text-searchable, `CompanyName_CapabilityStatement_YEAR.pdf`) — the #1 conversion asset. Everything on the site funnels to this download.
- **NAICS codes** displayed, primary flagged; **CAGE + UEI** displayed with DSBS verification links.
- **Set-aside status** — phrase carefully: self-attested SDVOSB ≠ SBA-certified. Never claim "certified" until it lands.
- **Past performance** — pre-revenue firms frame it as anonymized "representative program experience" of the team; never fabricate company awards.
- Contract vehicles (add when won), teaming/subcontracting page, clear CO contact path (form + capabilities-brief CTA, not just a mailto), Section 508 accessibility, multi-page IA (one-page sites cap out fast).

## Anonymity rule (user-corrected, hard constraint)

When principals hold day jobs at another company, **NEVER name them on public-facing material**: no names, no headshots, no current-employer text. Scrub the JSON-LD `employee` block (machine-readable — it's what Google surfaces) and the `og:image` headshot (unfurls on every social share). Present leadership in aggregate: combined years, program dollar figures, agency lineage (e.g. "former Marine Corps acquisition officers"), credential pillars. Named bios belong only in the capabilities-statement PDF shared directly with prospects — never on the crawled public site. Flag any live exposure as a **critical finding with an immediate takedown recommendation**, independent of the rebuild timeline.

## 2026 B2G design-trend filter

- **Adopt:** typography-as-architecture (oversized confident headlines), dark-mode native, neo-serif + monospace pairing (serif headings + mono for NAICS/contract numbers), modular/bento capability cards, trust/proof architecture (metrics above the fold), TL;DR structure, restrained micro-motion, machine-readable semantic HTML + JSON-LD.
- **Avoid:** kinetic/scroll-jacked animation, organic anti-grid chaos, heavy glassmorphism/3D, stock photography (instantly reads fake in GovCon — no photos over stock photos), cute-alism/playful brutalism, video hero backgrounds.
- Positioning principle: the site should feel like a *capabilities document that happens to be a website* — type-led, dark, precise, numbers-forward.
