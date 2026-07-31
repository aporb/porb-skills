# DoD CIO Website Bot Detection Blockade

## Problem

The DoD CIO website (`dodcio.defense.gov`) blocks all automated downloads with 403 Access Denied due to aggressive bot detection. This affects:

- **curl** attempts: `curl -sL https://dodcio.defense.gov/Portals/0/Documents/CMMC/ScopingGuideL2v2.pdf` returns 403
- **browser_navigate** attempts: Hermes Browserbase integration returns "Access Denied" with bot detection warnings
- **User-agent spoofing**: Does not work — DoD CIO uses advanced fingerprinting beyond User-Agent headers

## Impact

All DoD CIO and DCSA CMMC/FOCI reference documents cannot be downloaded automatically:

1. **CMMC L2 Scoping Guide v2.13** — Defines what is in/out of scope for CMMC L2 assessment. Essential for scoping decisions.
2. **CMMC Assessment Process (CAP) Level 2 v2.13** — How the C3PAO will conduct the assessment. Essential for preparing for assessment.
3. **CMMC Environment Assessment Guide L2** — Assessment environment setup requirements.
4. **CMMC Documentation Landing Page** — Full catalog of CMMC reference documents.
5. **DCSA FOCI Information Page** — FOCI mitigation instruments (SSA, Proxy, Voting Trust), requirements, process overview.
6. **DCSA Main Site** — FCL process, NISPOM guidance.

## URLs

**DoD CIO — All return 403 to automated tools:**
- Scoping Guide v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/ScopingGuideL2v2.pdf`
- CAP Level 2 v2.13: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/CAP-Level2-Version-2-13.pdf`
- Environment Assessment Guide L2: `https://dodcio.defense.gov/Portals/0/Documents/CMMC/EnvironmentAssessmentGuideL2v2.pdf`
- CMMC Documentation Landing: `https://dodcio.defense.gov/CMMC/`

**DCSA — All return 403 to automated tools:**
- FOCI Information Page: `https://www.dcsa.mil/mc/ctp/foci/`
- DCSA Main Site: `https://www.dcsa.mil/`

## Verification Script

```bash
# Test URLs (will all return 403 or 000/dns failure)
echo "=== DoD CIO ==="
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://dodcio.defense.gov/Portals/0/Documents/CMMC/ScopingGuideL2v2.pdf"
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://dodcio.defense.gov/Portals/0/Documents/CMMC/CAP-Level2-Version-2-13.pdf"
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://dodcio.defense.gov/Portals/0/Documents/CMMC/EnvironmentAssessmentGuideL2v2.pdf"
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://dodcio.defense.gov/CMMC/"
echo ""
echo "=== DCSA ==="
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://www.dcsa.mil/mc/ctp/foci/"
curl -sL -o /dev/null -w "HTTP %{http_code}" --max-time 10 "https://www.dcsa.mil/"
```

## Resolution

### Manual Download from Corporate Browser

1. **User must download manually** from a corporate browser (or via a VPN that bypasses DoD bot detection)
2. **Save to:**
   - `compliance-toolkit/reference-docs/ScopingGuideL2v2.pdf`
   - `compliance-toolkit/reference-docs/CAP-Level2-Version-2-13.pdf`
3. **Scan into Nextcloud:**
   ```bash
   cd /home/amyn/repos/aecon-fcs
   sg www-data -c "docker exec --user www-data nextcloud php occ files:scan --path='/amyn/files/briefings'"
   ```

### Document in GAP-ANALYSIS.md

Always document this gap in `GAP-ANALYSIS.md` as a manual action item:

```
## Critical Gaps Requiring Manual Action

### 1. DoD CIO Documents — Bot Detection Blockade

**Problem:** The DoD CIO website (dodcio.defense.gov) blocks all automated downloads (both curl and browser) with 403 Access Denied due to aggressive bot detection.

**Impact:** Two critical reference documents are missing:
- CMMC L2 Scoping Guide v2.13 — Defines what is in/out of scope for CMMC L2 assessment. Essential for scoping decisions.
- CMMC Assessment Process (CAP) Level 2 v2.13 — How the C3PAO will conduct the assessment. Essential for preparing for assessment.

**Resolution Required:**
1. User must download these files manually from a corporate browser (or via a VPN that bypasses DoD bot detection)
2. Save to:
   - `compliance-toolkit/reference-docs/ScopingGuideL2v2.pdf`
   - `compliance-toolkit/reference-docs/CAP-Level2-Version-2-13.pdf`
3. Run: `cd /home/amyn/repos/aecon-fcs && git add compliance-toolkit/reference-docs/*.pdf && git commit -m "Add CMMC L2 Scoping Guide v2.13 and CAP Level2 v2.13 (manual download)"`

**Estimated Time:** 5 minutes manual download
```

## Alternative Workarounds (Not Recommended)

These workarounds may work but are **not recommended** because they may violate DoD acceptable use policies:

1. **Corporate VPN:** If the user has access to a corporate VPN that bypasses DoD bot detection, they can download via the VPN.
2. **Alternative mirrors:** Some third-party sites may host copies of these documents, but they may not be up-to-date and may violate DoD copyright.
3. **Wayback Machine:** Archive.org may have cached versions, but they may be outdated and not authoritative.

## Best Practice

**Always assume DoD CIO downloads will fail.**

When building a CMMC L2 compliance toolkit, plan for manual DoD CIO downloads and document the gap in `GAP-ANALYSIS.md` upfront. This prevents false promises of automated delivery and sets clear expectations with the user.

## Related Issues

- Heresy: The same blockade affects other DoD CIO-hosted documents beyond CMMC (e.g., DoD IT policies, cybersecurity frameworks)
- Pattern: Federal agencies increasingly block automated downloads (OMB, GSA, NIST may follow)

## See Also

- NIST SP 800-171 Rev 2 (downloadable via curl — https://csrc.nist.gov/pubs/sp/800-171/rev/2/final)
- NIST SP 800-171A Rev 2 (downloadable via curl — https://csrc.nist.gov/pubs/sp/800-171a/rev/2/final)
- 32 CFR Part 170 (downloadable via curl — https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XII/part-170)