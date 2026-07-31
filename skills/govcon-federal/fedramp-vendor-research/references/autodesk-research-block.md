# Autodesk.com — Aggressive Bot Blocking

**Discovered:** July 21, 2026 (Aecon Enclave Autodesk research session)

## Problem

Autodesk.com blocks ALL automated access. Every approach fails:

| Tool | Result |
|------|--------|
| `web_extract` | "Failed to fetch url" |
| `web_search` (any query) | `{data: {web: []}}` (silent empty) |
| `browser_navigate` to autodesk.com/* | "Access Denied" page (title + single h1) |
| `firecrawl_search` | 402 (if credits exhausted) or blocked |
| `terminal curl` | Empty / blocked |

This applies to ALL subdomains: autodesk.com, knowledge.autodesk.com, help.autodesk.com, forums.autodesk.com.

## Workaround

### 1. FedRAMP Marketplace (browser) — WORKS
The FedRAMP Marketplace at `fedramp.gov/marketplace` is a government site that does NOT block browser access. Search for "Autodesk" in the product search to find FedRAMP-certified Autodesk products.

```
browser_navigate → fedramp.gov/marketplace
browser_type → search box with "Autodesk"
browser_click → search button
browser_console → extract('document.querySelectorAll("h3")') for product names
```

As of July 21, 2026: 2 results — "Autodesk for Government" (FedRAMP Certified, Class C, Rev5) and "Masterworks Cloud Platform" (false positive from keyword overlap).

### 2. Meeting Transcripts — When Available
If Aecon has had a recent meeting with Autodesk (check `to-transcribe/` for new recordings), the meeting transcript is the richest source of technical detail about licensing models, deployment options, and FedRAMP architecture. The Autodesk account team disclosed more in one 65-minute meeting than exists in all public documentation.

### 3. Third-Party Sources
- Reddit r/Autodesk, r/Revit — user experiences with VDI, network licensing, offline mode
- Autodesk Community Forums — may work via browser (not tested)
- FedRAMP Marketplace — for certification status only
- Reseller/partner documentation — often less aggressively blocked

## Key Facts (from transcript, not web)

These were obtained from the Aecon-Autodesk meeting (New Recording 9, July 21, 2026), not from public documentation:

- Desktop products (AutoCAD, Revit, etc.) are NOT FedRAMP certified — "We don't provide desktop compliant packages for the federal space" (Anthony Renteria, Autodesk FedRAMP specialist)
- Only Revit has direct cloud collaboration with AFG (Revit Cloud Worksharing)
- No Desktop Connector for government cloud
- AFG runs on AWS commercial region with tenant isolation — NOT GovCloud
- VDI deployment is supported for government customers
- Network License (multi-user / FlexLM) and Named User models both available
- Government licensing is a separate SKU/price list
