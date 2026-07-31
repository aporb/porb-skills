---
name: warm-opportunity-intake
description: "Warm opportunity intake: materials, call, analysis."
category: govcon
triggers:
  - Contact reaches out via DM, email, or phone with an opportunity
  - User says "help me review this proposal, RFP, or opportunity"
  - Needs materials extraction from email, call transcription, gap analysis
  - Partner or subcontractor role scoping
---

# Warm Opportunity Intake Pipeline

When a contact reaches out with a proposal or contract opportunity (often via LinkedIn DM, email, or phone), this pipeline turns the initial contact into structured deliverables within hours.

## Pipeline Overview

```
Contact Inbound -> Call -> Audio -> Transcribe -> Materials Review -> Gap Analysis -> Deliverables -> Repo
```

## Phase 1: Initial Contact and Call

### Research the contact (before the call)
- Run contact intelligence: LinkedIn profile, company UEI/CAGE if SAM.gov registered
- Check Misfit Network or other shared directories for existing dossiers
- Build a pre-call briefing with the contact's background and relevant context
- Do NOT over-research — this is a warm intro, not adversarial intel

### During the call
- Record only your side (speakerphone) or get consent if recording both
- Note: proposal due date is THE critical number
- Listen for: roles needed, budget range, timeline, what is written vs TBD
- Note the engagement posture: materials review vs named sub vs fractional

### After the call
- Capture mental notes immediately (voice memo or text)
- If one-sided recording: annotate inferred turns from context
- Record: decisions made, action items, open questions

## Phase 2: Materials Intake

### Email extraction
- Check email from the contact (Zoho, Maildir, or configured provider)
- Extract all attachments (PDFs, DOCX, XLSX, images)
- Save the raw email (.eml format) to the repo

### DOCX extraction (fast + fallback)
- Primary: `uvx markitdown file.docx > text.txt`
- Fallback (no pip, no uvx): `unzip -p file.docx word/document.xml | python3 -c "import sys,re; print(re.sub(r'<[^>]+>',' ',sys.stdin.read()).strip()[:50000])"`

### PDF extraction
- `python3 -c "import pdfplumber; pdf=pdfplumber.open('file.pdf'); [print(p.extract_text()) for p in pdf.pages]"`
- `uvx markitdown file.pdf > text.txt` for markdown

### RFP and Proposal analysis
Read the materials for:
- **Client:** Who is the buyer? Public, municipal, federal, or commercial?
- **Funding:** Grant, contract, internal budget? Ceiling amount?
- **Scope:** Deliverables, timeline, key requirements
- **Team:** Who is already on the team vs TBD
- **Deadline:** The absolute drop-dead date
- **Gaps:** Specific roles or services the contact needs filled
- **Your fit:** Is your expertise relevant here?

## Phase 3: One-Sided Call Transcription

When the recording captures ONLY your side (common with speakerphone voice memos):

1. Transcribe via xAI STT (diarize=true)
2. Build turns via the audio-transcription skill's build_turns.py script
3. Insert **context gaps** between each of your spoken turns:
   - Infer what the other person likely said from context
   - Mark them clearly with arrows and color coding
   - Base inferences on your responses, the email they sent, their bio, the proposal
4. Add a post-call notes section for personal observations

Reference: `~/repos/art-gis-proposal/call-transcript-2026-07-28.html` for a worked example.

## Phase 4: Gap Analysis

Build a structured gap analysis comparing what the contact HAS vs what the RFP NEEDS:

| What They Have | What Is Missing | What You Can Fill |
|---|---|---|
| Written proposal ~80% complete | Generic methodology in one area | Technical section rewrite + referral |
| Trusted local partner | Infrastructure analysis TBD | Domain expert referral |
| Fee within budget | Cost breakdown unclear | Cost estimation for your scope |
| RFP compliance matrix | Letters of support missing | Draft letter |

### Key questions:
- Contribution model: named sub? fractional consultant? informal reviewer?
- Win probability given team composition and competition
- Post-award risk if they win
- Paid proposal support or goodwill?

## Phase 5: Deliverables

Always produce these three deliverables:

### 1. Call Transcript (HTML)
- Annotated with context gaps if one-sided
- Post-call personal observations section
- Save to repo and Nextcloud briefings

### 2. Meeting Minutes (HTML)
- TL;DR block (dark slate callout)
- Meta bar (date, time, duration, platform, participants)
- Decisions made (numbered list)
- Action items table (owner, priority, status)
- Opportunity summary card
- Risks and considerations

### 3. Holistic Opportunity Briefing (HTML)
- The Opportunity: project, client, funding, type, geography, period
- The Players: contact, their named subs, your role
- RFP Scope: component breakdown with key deliverables
- The Gaps: detailed per missing role
- Proposal Assessment: what is strong vs what is missing
- Recommended Next Steps: timeline-driven
- Risks and Open Questions: with mitigations
- Sources: every artifact cited
- Save to Nextcloud briefings

## Phase 6: Repo Setup

- `mkdir -p ~/repos/<project-slug>`
- Commit: RFP, proposal text, raw email, transcript, minutes, briefing
- Push to GitHub as private (ask user for confirmation)

## Pitfalls

- **3-day deadline is common.** Design deliverables for 24-48 hour turnaround.
- **Commercial vs federal.** Municipal grants are not FedRAMP or CMMC. Check funding source.
- **No budget for proposal support.** Clarify terms early (goodwill, win-share, or paid).
- **One-sided audio.** Do not present inferred content as verbatim. Mark context gaps clearly.
- **SAM.gov search is unreliable.** Search by UEI directly, not company name.
- **DOCX-as-ZIP is lossy.** Verify first 1000 chars. Use only as fallback.
- **No overcommit.** Treat proposal support as low-time-investment until award.
- **Permission before sharing.** Ask the contact before sharing their proposal with your network.
