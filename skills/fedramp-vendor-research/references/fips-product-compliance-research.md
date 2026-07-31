# FIPS 140-2/140-3 Product Compliance Research

## When to Use This Reference
When researching whether a specific software product supports FIPS 140-2/140-3 validated cryptography — this is a distinct class from vendor-level FedRAMP research. You need to determine: can this product run in a FIPS-enabled Windows/OS environment? Does the connector/API support FIPS-compliant crypto? What breaks if FIPS is enforced?

## Research Sequence

### 1. Check Vendor Security/Compliance Pages First
Navigate directly to the vendor's security page (e.g., `vendor.com/security/`, `vendor.com/company/security/`). Look for:
- FIPS 140-2/140-3 certifications listed alongside other certs (ISO 27001, SOC 2, FedRAMP)
- Cryptography or encryption policy statements
- "Government," "Federal," or compliance deployment guides

**Critical negative finding:** Many vendors prominently display ISO 27001, SOC 2, and FedRAMP but NEVER mention FIPS 140. This absence is itself evidence — vendors who have FIPS certification advertise it. If it's not on the security page, it probably doesn't exist.

### 2. Search NIST CMVP Validated Modules Database
**URL:** `https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search`

Search by vendor name and product name. Key facts:
- FIPS 140 validation is per-module, not per-product. A product may "use" validated modules (e.g., Windows CryptoAPI, OpenSSL FIPS) without having its own certification.
- Oracle Corporation has hundreds of validated modules (Oracle DB, Java, Solaris) — but search for the specific product name (e.g., "Primavera").
- If the product is NOT listed, the vendor relies on OS-level or platform-level FIPS compliance.

**Extraction pattern:**
```bash
curl -sL "https://csrc.nist.gov/projects/cryptographic-module-validation-program/validated-modules/search?SearchTerm=<product>" \
  -A "Mozilla/5.0" 2>&1 | grep -oP '<td[^>]*>[^<]*</td>' | head -50
```

### 3. Check FedRAMP/Equivalency Pages for FIPS Hints
If the vendor has FedRAMP Moderate or higher (or equivalency), FIPS 140 is REQUIRED as part of the FedRAMP baseline. However:
- **FedRAMP FIPS compliance may be at the infrastructure layer only** (Azure Gov / AWS GovCloud), not the application layer
- **Cloud vs. on-premises products may have different FIPS status** — a vendor's cloud SaaS may be FIPS-compliant through Azure, but their legacy on-premises connector may not be
- FedRAMP equivalency for one product (e.g., InEight Document) does NOT imply FIPS compliance for other products (e.g., InEight N8/NAESTIMATE connector)

### 4. Check Vendor Community Forums and Knowledge Bases
- Search vendor's community site (e.g., `community.vendor.com`) for "FIPS" discussions
- Check if the knowledge base is publicly accessible or requires authentication
- Look for support threads mentioning FIPS mode, error messages with "FIPS," or "cryptographic algorithm"

**Note:** Many vendor communities require authentication. Document this as a research limitation — don't conclude "no FIPS issues exist" when the support forums are behind a login wall.

### 5. Analyze Product Architecture for FIPS Failure Patterns
If the product is a legacy Windows on-premises application, identify the likely technology stack and failure mode:

#### .NET Framework Applications (Common for N8/NAESTIMATE, older enterprise apps)
- **Check:** Does Windows FIPS policy break the app?
- **Registry key:** `HKLM\System\CurrentControlSet\Control\Lsa\FipsAlgorithmPolicy\Enabled` = 1
- **Failure mode:** `InvalidOperationException: "This implementation is not part of the Windows Platform FIPS validated cryptographic algorithms."`
- **Common culprits:** MD5 hashing, DES/RC2 encryption, HMACSHA1, non-FIPS `CryptoServiceProvider` implementations
- **Mitigation:** `<enforceFIPSPolicy enabled="false"/>` in app.config (violates CMMC), or migrate to FIPS-compliant .NET 5+ APIs

#### Java-based Applications (Common for Oracle P6 EPPM server-side)
- **Check:** Can the JVM be configured with a FIPS 140 provider?
- **Providers:** RSA BSAFE Crypto-J, nCipher nShield, IBM JCE FIPS
- **Configuration:** `java.security` provider list, `com.sun.net.ssl` settings
- **Risk:** Application code may use non-FIPS algorithms even with a FIPS provider configured

#### REST API / Web-based Products
- **Transport layer:** TLS 1.2+ with FIPS-compliant cipher suites (e.g., TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384)
- **Generally FIPS-compatible** at the transport layer regardless of application internals
- **Recommendation:** Prefer API-based integration over legacy desktop connectors when FIPS is required

### 6. Check Vendor Integration/Partner Pages
The vendor's integrations page (e.g., `vendor.com/integrations/`) may list the specific integration method with other products. This reveals:
- Whether a direct connector exists (likely legacy desktop app → FIPS risk)
- Whether API-based integration is available (likely FIPS-compatible at transport layer)
- Alternative integration methods (CSV/XML file exchange — no crypto required)

### 7. Search for Regulatory Documentation Gaps
Vendors serving federal markets often have missing FIPS documentation. Document what's absent:
- No FIPS 140 validation certificate for the specific product
- No documented FIPS-compatible configuration mode
- No guidance on running in FIPS-enabled Windows environments
- No public-facing FIPS compliance statement

## Research Output Format

For each product, produce:
1. **FIPS documentation found?** Yes/No + source URLs
2. **NIST CMVP listing:** Found/Not found
3. **Known FIPS issues:** From community forums / support KB
4. **Architecture analysis:** Likely technology stack and FIPS failure mode
5. **Integration method:** Connector type (direct, API, file exchange) and FIPS implications
6. **CMMC/DFARS assessment:** Can this product be used in a FIPS-mandatory environment?
7. **Workarounds ranked by compliance safety:** From "disable FIPS" (❌) to "API-based integration" (✅)

## Field Example: Oracle P6 EPPM + InEight N8 (July 2026)

**Oracle P6 EPPM:**
- No FIPS 140 mentions in P6 v25/v26 public docs (search across all guide categories)
- No Primavera-specific modules on NIST CMVP
- Oracle's general FIPS security pages return 404 (restructured docs)
- P6 runs on Java/WebLogic — could theoretically use FIPS JCE provider, but untested/undocumented
- P6 web access via HTTPS is FIPS-compatible at transport layer

**InEight N8/NAESTIMATE:**
- No FIPS 140 mentions on security page, FedRAMP page, or integrations page
- FedRAMP Moderate Equivalency covers InEight Document (cloud) only, NOT the N8 connector
- Legacy .NET Framework Windows desktop app — confirmed incompatible with Windows FIPS mode
- InEight support team: "FIPS must be disabled for the connector to work"
- Integrations page confirms Oracle P6 direct connector exists (import/export schedule data)
- Modern REST API available (developer.ineight.com) — API-based integration over TLS is FIPS-compatible

**CMMC Assessment (NIST SP 800-171 SC.3.13.11):**
- ❌ Disable FIPS for connector: Direct violation
- ⚠️ Network-segmented connector machine: Gray area — assessor-dependent
- ✅ API-based integration (P6 REST API ↔ InEight REST API over TLS): Clean pass
- ✅ CSV/XML file exchange within FIPS enclave: Pass