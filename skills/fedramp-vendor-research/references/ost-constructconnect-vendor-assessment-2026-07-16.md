# OST/ConstructConnect Vendor Security Assessment — Worked Example (July 2026)

Full end-to-end example of a CMMC/FedRAMP vendor compliance assessment for a non-FedRAMP desktop application. Demonstrates the cross-reference methodology: extract internal assessment claims → pull vendor public pages → cross-reference → identify gaps → produce meeting prep questions.

## Context

Aecon (federal contractor) assessing On-Screen Takeoff (OST) by ConstructConnect for use in federal/CMMC-aligned environments with CUI. The internal assessment document claimed OST can operate on-prem with cloud features disabled, but Aecon hasn't received sufficient assurance.

## Workflow

### 1. Extract Internal Assessment Document
Two screenshots of an internal Aecon executive summary were processed via `vision_analyze`. Key claims extracted:
- OST operates as customer-hosted, on-premises desktop app
- Cloud features (Takeoff Boost, AutoNaming, Project Express) can be disabled
- Outbound comms limited to licensing/entitlement + telemetry
- Deployed in virtualized environments with VDI sizing guidance
- No SOC 2 or third-party assurance reports publicly available
- Technical security meeting with vendor still pending

### 2. Pull Vendor Public Pages

**Sources scraped:**
- `constructconnect.com/products/on-screen-takeoff` — product page (browser)
- `oncenter.com/products/on-screen-takeoff/` — legacy product page (browser)
- `constructconnect.com/privacy-policy` — data collection/sharing (browser)
- `constructconnect.com/acceptable-use-policy` — security contact only (ddgr)
- `help.constructconnect.com` — KB with system requirements (SPA, direct link 404'd)
- `oncenter.com/ost-getting-started/` — Project Express description (ddgr)

**Firecrawl was credit-exhausted** — fell back to browser navigation + ddgr terminal search. See `web-research` skill (`references/firecrawl-credit-exhaustion-fallback.md`) for the fallback sequence.

### 3. Cross-Reference: Claims vs. Public Evidence

| Assessment Claim | Public Evidence | Match |
|---|---|---|
| Desktop app, on-prem possible | Confirmed — product pages describe installed software, KB has VDI docs | ✅ Match |
| Cloud features can be disabled | **Unverifiable** — no public documentation of disablement; marketing aggressively promotes cloud AI | ⚠️ Gap |
| Only licensing/telemetry outbound | **Privacy policy contradicts** — broad data collection (IP, geolocation, internet activity); no carve-out for on-prem mode | ❌ Gap |
| No SOC 2 / assurance reports | **Confirmed** — zero security/compliance page exists; only `security@constructconnect.com` in AUP | ✅ Match |
| VDI deployment documented | KB has "Classic License Managers" and "ELM Virtual Server Edition" articles | ✅ Match |
| Infrastructure sizing guidance provided | KB article exists but couldn't be loaded (SPA 404) | ⚠️ Unverified |

### 4. Key Gaps Identified

- **No security page**: No /security, /compliance, /trust, or /fedramp URL
- **No architecture docs**: No data flow diagrams, network diagrams, deployment architecture
- **No third-party attestations**: No SOC 2 Type II, ISO 27001, FedRAMP, CMMC
- **No offline/air-gapped mode**: All licensing appears internet-dependent
- **No CUI/CDI handling guidance**: No documentation for CUI or Covered Defense Information
- **Takeoff Boost requires plan uploads**: Explicitly marketed as "upload a plan... right in your browser"
- **Project Express transfers files via cloud**: "Send and receive OST project files without ever leaving OST"
- **Auto Name uses cloud AI**: "Automatically rename plan pages" via cloud processing

### 5. Produced Deliverable

Self-contained HTML briefing at `brief.h.porb.dev/ost-vendor-page-analysis.html` using Thariq ivory/clay aesthetic (internal compliance briefing, not external consulting deliverable). Included:
- Source table with URLs and relevance
- Claim-by-claim cross-reference table with match/gap tags
- Privacy policy analysis of data leaving the environment
- Gap list (what the vendor doesn't publish)
- 7 meeting prep questions for the technical security review

### 6. Meeting Prep Questions Generated

1. Licensing telemetry: exact data fields transmitted during license checks
2. Cloud feature disablement: toggle, GPO, or firewall rule? Enforceable via registry?
3. Update mechanism: auto-update domains/IPs; air-gapped via WSUS/SCCM?
4. Network diagram: complete outbound endpoint list for "cloud-disabled" deployment
5. SOC 2 / audit reports: shareable under NDA?
6. Data at rest: encryption, temp files, caches, logs
7. Authentication: Entra ID / AD SSO or standalone local accounts?

## Pattern Takeaways

- **Browser + ddgr is the reliable fallback** when Firecrawl credits exhaust. Browser navigates pages; ddgr discovers URLs. Neither has credit limits.
- **Privacy policies are compliance goldmines** — they describe data collection that applies regardless of deployment mode. Always extract them.
- **Cross-reference tables** (claim vs. evidence) are the most efficient way to surface compliance gaps. Visually immediate.
- **Meeting prep questions** turn a gap analysis into an operational deliverable. Every gap should generate a specific, answerable question for the vendor's security team.
- **Thariq ivory/clay** is the correct aesthetic for internal compliance briefings. HARBOR dark theme is for external consulting deliverables.
