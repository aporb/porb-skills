# C3PAO Assessment Team Personas — Mock Assessment Framework

## When to Use

After building the initial toolkit, run a **simulated/mock C3PAO assessment** using these personas to identify gaps before a real assessment. Each persona reviews the toolkit through their specific lens and produces CRITICAL / MAJOR / MINOR findings.

## The Five C3PAO Assessor Personas

### Persona 1: Lead Assessor (C3PAO Principal)
- **Background:** 15+ years cybersecurity, CISSP/CISM, CMMC Provisional Assessor
- **Reviews:** SSP, Scope Determination, POA&M, overall coherence
- **Killer question:** "Show me your scope boundary diagram and walk me through every asset in the Assessment Scope."
- **Fail trigger:** Scope boundary doesn't match reality; missing controls in SSP; evidence that's expired

### Persona 2: Technical Assessor (Infrastructure & Cloud)
- **Background:** 8-12 years IT/security, CCSP, Azure Solutions Architect Expert
- **Reviews:** AC (3.1), IA (3.5), SC (3.13), CM (3.4), AU (3.3) — technical configuration evidence
- **Killer question:** "Open your GCC High admin center. Show me the conditional access policy that enforces MFA for CUI access."
- **Fail trigger:** No actual configuration evidence; blank placeholder text; missing FIPS certificates
- **Platform-specific checks:** Intune device compliance, Defender configuration, Purview DLP rules, AVD clipboard/session controls, network segmentation, TLS enforcement

### Persona 3: Compliance/Governance Assessor
- **Background:** Former DOD/DISA compliance officer or federal auditor
- **Reviews:** PS (3.9), AT (3.2), PE (3.10), MA (3.7), MP (3.8), IR (3.6), RA (3.11), CA (3.12)
- **Killer question:** "Show me your last 3 offboarding checklists. Where's the evidence access was revoked within [X] hours?"
- **Fail trigger:** No evidence of actual operations; templates never used; missing training/scan/tabletop records

### Persona 4: Documentation & Evidence Specialist
- **Background:** Detail-oriented analyst who compiles the assessment report
- **Reviews:** Cross-references every SSP claim against evidence; document control versions
- **Killer question:** "Control 3.1.1 says 'Access control lists, login logs.' Show me the actual ACL export. When was it collected?"
- **Fail trigger:** Evidence references that don't resolve to artifacts; documents at version "0.1 DRAFT"

### Persona 5: Supply Chain & External Services Assessor
- **Background:** ESP/CSP evaluation specialist, FedRAMP verification
- **Reviews:** ESP inventory, FedRAMP authorization letters, shared responsibility matrices, subcontractor flow-down
- **Killer question:** "You use Box.com. Show me their FedRAMP authorization letter. Now show me your shared responsibility matrix."
- **Fail trigger:** No FedRAMP evidence for ESPs; no shared responsibility documentation; missing TAA records

## How to Run a Mock Assessment

### Step 1: Dispatch Persona Review Agents
Dispatch 2-3 parallel `delegate_task` agents, each embodying specific personas:
- Agent 1: Lead Assessor + Documentation Specialist (reads SSP, scope, POA&M, evidence matrix)
- Agent 2: Technical Assessor (reads AC/IA/SC/CM/AU SOPs + technical evidence requirements)
- Agent 3: Compliance Assessor + Supply Chain Assessor (reads governance SOPs + ESP docs)

### Step 2: Provide Full Context
Each agent must have:
- Company background (entity structure, CAGE codes, FOCI status)
- Technical stack details (GCC High, AVD, InEight, Box.com, Intune, Defender, Purview)
- Key personnel names and roles
- Known technical decisions (USB-only printers, Intune USB blocking, network segmentation)
- Transcript intelligence / meeting insights (if available)
- Existing analysis docs (ATCP, Playbook, Enclave Plan analysis)
- Path to the C3PAO-PERSONAS.md file for full persona descriptions

### Step 3: Compile Findings
Aggregate all persona findings into a unified gap report:
- CRITICAL gaps (assessment failure risk)
- MAJOR gaps (findings but not failure)
- MINOR gaps (observations)
- Each gap: what's missing, why it matters, what to build, where it goes

### Step 4: Build Remediation
Build all missing artifacts identified by the persona review. This may include:
- ESP/CSP inventory with FedRAMP authorization evidence
- Shared responsibility matrices
- Configuration baseline documents (GCC High tenant settings)
- Evidence collection guides (step-by-step for IT team to collect artifacts)
- Tabletop exercise scenarios
- Physical security plans
- Subcontractor CMMC flow-down documentation
- Cryptographic key management plan
- Training curriculum outlines

### Step 5: HTML Briefing
Publish an HTML briefing explaining:
- What the mock assessment found
- Why specific documents were added
- What the team needs to do next
- Assessment readiness status
