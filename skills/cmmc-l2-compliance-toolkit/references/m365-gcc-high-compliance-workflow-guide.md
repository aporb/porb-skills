# M365 GCC High Compliance Workflow Guide
## SharePoint + Teams + Power Automate + Purview for Clearance Management

**Source:** July 2026 session — Aecon GCC High enclave clearance management system design
**Full guide:** `/home/amyn/aecon-gcc-high-compliance-workflow-guide.md`

This reference condenses the architecture decisions, patterns, and pitfalls for building compliance workflows (access requests, clearance verification, NDA recertification, citizenship verification) in a Microsoft 365 GCC High environment with a C3PAO audit trail.

---

## Three-List SharePoint Architecture

Build three interconnected SharePoint lists rather than a single monolithic list:

### List 1: Personnel Roster (Master Record)
- `CitizenshipStatus` (Choice: US Citizen, US Person, Non-US Person)
- `ClearanceLevel` (Choice: None, Secret, Top Secret, TS/SCI)
- `ClearanceExpiry` (Date; calculated column for 5/6 year cycles)
- `NDAStatus` / `NDAExpiry` (annual recertification tracking)
- Enable versioning (keep all), indexed columns on Email/ClearanceStatus/Expiry

### List 2: Access Requests (Intake)
- `Status` (Choice: Draft → Submitted → Manager Approved → Security Review → Approved/Denied)
- `ApprovalChain` (JSON-serialized approval trail)
- `RequestType` (New Access, NDA Renewal, Clearance Upgrade)

### List 3: Audit Log (Optional — Unified Audit Log is primary)
- Timestamp, Action, ItemID, PerformedBy, PreviousValue, NewValue

### Permission Model
- Site Owners: clearance owner + enclave lead (full control on Personnel Roster)
- Site Members: lifecycle manager
- Custom permission level "Access Request Submitter" (add-only)
- Broken inheritance on Personnel Roster

---

## Power Automate Approval Pattern: Sequential with Parallel Branches

```
Trigger: Item created → Status = Submitted
  → Get Manager → Start approval (7-day timeout, escalation)
  → Approved → Status = "Manager Approved"
  → Parallel Branch A: Verify NDA status (send recertification if expired)
  → Parallel Branch B: Verify clearance (manual DISS/JPAS check)
  → Wait for BOTH → Send to Security Officer approval
  → Approved → Send to Enclave Lead approval
  → Approved → Update Personnel Roster, notify requestor
  → Any reject → Denied, notify requestor
```

**GCC High key considerations:**
- Use "Start and wait for approval" (not older "Send email with options")
- Service account connections (never personal accounts)
- Concurrency control: sequential for Personnel Roster writes (prevent race conditions)
- Solution-aware flows for ALM/source control
- Approval connectors: ✅ available. Premium/third-party: ❌ mostly not available.

---

## Forms: Power Apps Customized SharePoint Form (Recommended)

### GCC High Availability
- Microsoft Forms: ✅ Available (simple intake, no conditional logic, no file upload with metadata)
- Power Apps canvas/model-driven: ✅ Available
- Power Apps portals: ❌ Likely restricted (verify tenant)
- Power Apps customized SharePoint form: ✅ Available directly from list ribbon

### Recommendation
Use **Power Apps customized SharePoint form** (not standalone canvas app):
- Conditional field visibility (show clearance fields only for "New Access" type)
- Validation rules
- File attachments for supporting documents
- Data stored directly in SharePoint list — no separate data source

---

## Purview Integration: Container-Level Labeling

**Critical limitation:** Sensitivity labels apply to files/documents, NOT SharePoint list items.

### Recommended Approach
1. Create sensitivity labels: "CUI — Controlled", "CMMC Level 2", "Export Controlled"
2. Apply container label to SharePoint site (Groups & sites scope, private, blocked external sharing)
3. Configure default library label for document libraries
4. Auto-labeling policies for workflow-generated documents (approval PDFs, NDA attestations)
5. DLP policies for PII detection in SharePoint (SSN, passport numbers in notes fields)

### GCC High Purview Availability
- Sensitivity labels: ✅ (including default library labels)
- Auto-labeling: ✅
- DLP for SharePoint Online: ✅
- Activity Explorer: ✅

---

## Teams Integration Pattern

```
Team: "Aecon GCC High Enclave"
  ├── General (announcements, policies)
  ├── Access Requests (SharePoint list tab + adaptive cards for approvals)
  ├── Clearance Tracking (Personnel Roster tab)
  └── Compliance (audit reports, C3PAO evidence)
```

- Adaptive Cards: Power Automate posts rich cards to channels, @mentions security officer
- Sharing: Files in Teams inherit the site's Purview container label
- Guest access: Typically disabled in GCC High

---

## C3PAO Audit Trail: Multi-Layer Strategy

### Layer 1: Unified Audit Log (Primary Evidence)
```powershell
Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true
Set-AdminAuditLogConfig -AuditLogAgeLimit 365  # 1 year with E5/G5

# Export for C3PAO evidence
Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-90) -EndDate (Get-Date) `
  -RecordType SharePoint -Operations FileAccessed,FileDownloaded,ListItemCreated,ListItemModified `
  -ResultSize 5000 | Export-Csv "C3PAO_SharePoint_Audit.csv"
```

### Layer 2: SharePoint Version History
- Enable versioning on all lists, keep all versions
- Each version captures: who, when, old/new values

### Layer 3: Power Automate Run History
- 28-day default retention — **must export regularly for C3PAO**
- Use Power Automate Management connector for programmatic export

### Layer 4: Purview Audit (Premium)
- With E5/G5: 1-year retention, intelligent insights

---

## GCC High Limitations Quick Reference

| Available ✅ | Limited ⚠️ | Not Available ❌ |
|---|---|---|
| SharePoint Online (full) | Third-party Power Automate connectors | Power Apps portals |
| Teams (channels, tabs, apps) | AI Builder (delayed) | Microsoft Forms Pro |
| Power Automate (standard) | Power BI (separate instance) | Yammer Communities |
| Power Apps (canvas/model-driven) | Dataverse (some features lag) | Bookings |
| Microsoft Forms (internal) | SharePoint Syntex (delayed) | Public CDN |
| Purview labels + DLP + Audit | Power Virtual Agents (restricted) | Some Azure regions |

---

## Key Pitfalls Encountered

1. **Firecrawl/search tools can exhaust credits** — when `web_search`, `firecrawl_search`, `web_extract` all fail with 402, fall back to: `browser_navigate` to known authoritative sources → `browser_console` JS extraction → `terminal curl` → model knowledge. See web-research skill for the pattern.

2. **MS Learn URL volatility** — Microsoft restructures learn.microsoft.com URLs frequently. When a 404 returns, try the search results suggested on the 404 page (they often link to the correct new path).

3. **Purview labels don't apply to list items** — they apply to files/documents/sites. Protect list data through container labeling + DLP policies, not item-level labeling.
