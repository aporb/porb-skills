# Subcontract Research Pipeline — DNS/OSINT/Tech Stack Recon

From the July 2026 Westerman Inc. engagement. Toolchain for mapping a target counterparty's tech stack, IT providers, and compliance posture before pitching.

## DNS Reconnaissance

```bash
# Mail provider (M365 vs Google vs on-prem)
dig +short mx target.com

# SPF record — reveals email security vendor (Mimecast, Proofpoint, Barracuda, M365)
dig +short txt target.com | grep 'v=spf1'

# DMARC — reveals reporting and policy
dig +short txt _dmarc.target.com

# DKIM — reveals signing domain (often vendor-specific)
dig +short txt selector1._domainkey.target.com

# CNAME enumeration — common subdomains reveal CRM, ticketing, HR systems
for sub in mail remote vpn secure portal hr benefits time clock erp crm intranet wiki helpdesk support; do
  echo "$sub.target.com -> $(dig +short CNAME $sub.target.com || echo 'no CNAME')"
done

# Nameservers — reveal DNS hosting provider
dig +short ns target.com
```

## HTTP/S Banner Analysis

```bash
# Server header, Set-Cookie patterns reveal tech stack
curl -sI https://www.target.com | grep -i 'server\|x-powered-by\|set-cookie\|cf-ray\|x-served-by'

# JS bundle analysis — download and check for vendor traces
curl -s https://www.target.com | grep -oP 'src="[^"]*\.js"' | head -20
```

## LinkedIn Analysis

Extract from key personnel profiles:
- Current role & title
- Career history (where they worked before — reveals past employers, domain experience)
- Connections to target company (mutual follows, shared groups)
- Certifications (PMP, CISSP, PE, NQA-1 auditor, etc.)
- Education (reveals clearance background if service academy or ROTC)

## SAM.gov Entity Search

```bash
# Check if entity has active SAM registration
curl -s "https://api.sam.gov/entity-information/v3/entities?api_key=$SAM_API_KEY&ueiDUNS=X" | jq

# USAspending — search by UEI or DUNS for prime contracts
curl -s "https://api.usaspending.gov/api/v2/search/spending_by_category/awarding_agency/?filters={%22recipient_uei%22:%22X%22}" | jq '.results[:10]'
```

## DNS-Based MSP Detection

Certain DNS patterns reveal the incumbent IT managed service provider:

- **M365 IM:** Look for `target-com.mail.protection.outlook.com` MX
- **Barracuda:** Look for `barracuda` in MX hostnames or SPF include
- **Proofpoint:** `pphosted.com` in MX or SPF
- **Mimecast:** `mimecast` in MX or `_netblocks.mimecast.com` in SPF
- **Fortinet:** Look for `fortigate` CNAMEs or `fortimail` MX
- **Cisco:** `c1.esez.com` MX or `ss.eas.outlook.com`

## OSINT Fallback (When Automated Probes Fail)

- Shodan: `shodan.io/search?query=hostname:target.com`
- BuiltWith: `builtwith.com/target.com` (available via web_extract)
- Wappalyzer: browser extension inspection (manual)
- Censys: `search.censys.io` certificate transparency search
- Crtsh: `crt.sh/?q=%25.target.com` for subdomain enumeration via SSL certs

## Research Repo Structure

```
research/
├── infrastructure-profile.md      # DNS, tech stack, hosting, MSP
├── personnel/                      # Key decision maker profiles
│   └── douglas-henderson.md
├── compliance-gaps.md             # CMMC, DOE, NQA-1 gap register
├── incumbent-provider-analysis.md  # NexusTek-style competitive map
├── doe-order-471-1b-vendor-requirements.md  # DOE-specific research
└── <engagement>-pipeline-go-nogo.md  # Go/no-go decision with risks
```

All agents producing research MUST save their full logs (tool calls + results) to the live transcripts directory and their final output to `research/` in the engagement repo. No untraced research.
