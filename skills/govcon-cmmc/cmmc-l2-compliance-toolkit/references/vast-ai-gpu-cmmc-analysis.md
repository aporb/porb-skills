# Vast.ai GPU Infrastructure — CMMC L2 Gap Analysis

**Date:** July 28, 2026
**Source:** Multi-perspective CMMC L2 analysis session

## Infrastructure Profile
- **Provider:** Vast.ai (bare-metal GPU rental marketplace)
- **Hardware:** 4× RTX 5090 (128 GB VRAM total), NVFP4 weights
- **Engine:** vLLM with tensor-parallel-size=4, --enforce-eager (SM120 requirement)
- **Proxy:** LiteLLM + PostgreSQL prompt capture
- **Networking:** Tailscale tunnel (WireGuard) to Vast.ai host
- **Cost:** ~$1.07-$1.50/hr compute, ~$0.09/hr stopped (storage)

## Key Finding — Not a Managed Cloud
Vast.ai is a marketplace for renting GPU time from individual hosts. No FedRAMP authorization, no SOC 2, no BAA, no CUI handling guarantee. You get root access to a bare-metal box.

## Gap Summary
- **50 GAP** (not implemented), **28 DOC** (documentation only), **13 COMPENSATING** (partial), **19 PRESENT** (actually implemented)

## Critical Families (all/nearly all GAP)
1. **Awareness and Training (AT)** — 3/3 GAP
2. **Audit and Accountability (AU)** — 6/9 GAP
3. **Incident Response (IR)** — 3/3 GAP
4. **Risk Assessment (RA)** — 2/3 GAP
5. **Security Assessment (CA)** — 4/4 GAP
6. **System and Information Integrity (SI)** — 7/7 GAP

## Hard Truths
- Physical Protection (PE) is impossible on Vast.ai — you don't own the hardware or datacenter
- SSP fill is the longest pole (250-350 hours for 110 controls)
- C3PAO assessment costs $30K-$200K — no way around this
- CUI on commercial GPU = False Claims Act exposure — keep CUI in GCC High

## Six Infrastructure Options (Ranked)
1. **GCC High** ($12K-18K/mo) — FedRAMP, self-assessment path
2. **PreVeil Pass** ($450/mo) — Fastest deploy, not for GPU workloads
3. **Hardened Vast.ai** ($4K-8K/mo) — Cheapest GPU, C3PAO required
4. **Hybrid (Recommended)** ($6K-12K/mo) — GCC High for CUI + Vast.ai for inference
5. **Cuick Trac** (enterprise) — Managed GCC High, overkill for micro-businesses
6. **On-Prem** ($50K-100K upfront) — Nuclear option, 12-18 months to build

## Gap Remediation Priority
1. AC (3.1), IA (3.5): MFA, RBAC, session management, rate limiting
2. AU (3.3): deploy SIEM (Wazuh + syslog-ng + centralized log server)
3. IR (3.6): write NIST 800-61 IR plan, set up DIBNet reporting
4. SI (3.14): vulnerability scanning, Falco runtime detection
5. CA (3.12): start SSP fill (250-350h) and POA&M creation

**First-year cost for hybrid approach:** $124K-$389K
**Implementation timeline:** 24 weeks (6 months) at 430+ hours total
