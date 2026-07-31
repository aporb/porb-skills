---
name: cmmc-l2-cloud-compliance
title: CMMC L2 Cloud Compliance
description: Build CMMC L2 on FedRAMP or hardened clouds.
category: security
---

# Cmmc L2 Cloud Compliance

## Trigger
Building CMMC L2 compliant cloud/GPU infrastructure (Vast.ai, Lambda, etc) or mapping existing infra to NIST 800-171.

## What CMMC L2 Requires
- 110 NIST SP 800-171 Rev 2 controls across 14 families (3.1 AC through 3.14 SI)
- 32 CFR §170.14(c)(3): CMMC L2 = NIST 800-171 R2 exactly
- Phase 2 enforcement: ~Nov 10, 2026 (L2(C3PAO) becomes award condition)
- 3-year validity + annual affirmation (§170.22)
- C3PAO assessment: $30K-$200K

## Dual-Path Architecture

### Tier 1: FedRAMP/GCC High
- Azure Government GCC High or AWS GovCloud
- FedRAMP provides ~85% of 110 controls automatically
- Cost: ~$12K-18K/month for 4x A10/A40 GPU
- Assessment: self-attestation (L2 Self)

### Tier 2: Hardened Commercial
- Vast.ai/Lambda/RunPod with security overlay
- All 110 controls via compensating controls
- Cost: ~$4K-8K/month for 4x RTX 5090
- Assessment: C3PAO required

## Security Overlay (Tier 2)

### Identity & Access (3.5)
- MFA: Tailscale SSH + Supabase Auth/Azure AD MFA
- JWT/OAuth 2.0 for API access
- SSH CA + command allowlist

### Audit & Accountability (3.3)
- auditd to syslog-ng
- Wazuh agent (HIDS + correlation)
- Centralized SIEM (90+ day retention)
- Separate audit log server + encryption

### Configuration Management (3.4)
- Ansible + CIS benchmark
- Git version-controlled configs
- AppArmor for vLLM/LiteLLM
- Peer review + impact analysis

### Incident Response (3.6)
- NIST 800-61 IR plan
- DIBNet 72-hour reporting
- Quarterly tabletop exercises
- PagerDuty/Slack alerts

### Vulnerability Management (3.14)
- Qualys/OSS weekly scans
- CVE monitoring + 72-hour SLA
- Automated patch management
- ClamAV + Falco runtime detection

## Documentation
- SSP (110 controls) — use ~/repos/aecon-fcs/compliance-toolkit/ template
- POA&M (110 rows, correct control IDs from nist_800_171_controls.json)
- 14 SOPs (CS-[FAMILY]-####.SOP.md, one per family)
- Evidence Collection Matrix (14 families mapped to evidence types)

## Implementation Steps
1. Gap Analysis (Week 1-2) — Map 110 controls, compensating controls doc
2. Security Overlay (Week 2-4) — auditd, Wazuh, Ansible, Vault, Falco, Fail2ban
3. Documentation (Week 4-8) — SSP, 14 SOPs, evidence collection
4. Internal Assessment (Week 8-12) — Mock C3PAO, close Priority 1, IR tabletop
5. C3PAO Assessment (Week 12-24) — Engage C3PAO, certify, post to SPRS

## Key Sources
- 32 CFR Part 170, NIST SP 800-171 Rev 2
- DoD CIO CMMC L2 Scoping Guide v2.13 + CAP Level 2 v2.13
- ~/repos/aecon-fcs/compliance-toolkit/ (14 SOPs, 11 templates, nist_800_171_controls.json)
- ~/repos/aecon-fcs/03-research/strategy/aecon-cmmc-timeline-jv-to-audit-2026-07-08.html

## Pitfalls
- DoD CIO blocks automated downloads (403). Scoping Guide + CAP manual only.
- C3PAO must be "Authorized" (not "Candidate") on Cyber AB Marketplace.
- SSP content fill = 4-6 weeks for 110 control descriptions. Longest pole.
- Phase 2 suspension (July 13, 2026) = temporary 60-day review, not repeal.